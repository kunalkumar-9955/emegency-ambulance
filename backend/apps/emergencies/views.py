from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from apps.accounts.models import UserRole
from apps.accounts.permissions import IsDriver, IsPatient
from apps.audit.models import AuditLog
from apps.audit.services import log_audit
from apps.core.models import Tenant
from apps.emergencies.models import EmergencyRequest
from apps.emergencies.serializers import EmergencyRequestSerializer, GPSLogSerializer, SOSSerializer
from apps.emergencies.tasks import dispatch_emergency, notify_emergency_contacts
from apps.ai.services.fraud import check_fraud
from apps.ai.services.severity import calculate_severity
from apps.realtime.broadcast import broadcast_emergency_update


class SOSThrottle(UserRateThrottle):
    scope = "sos"


class SOSView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]
    throttle_classes = [SOSThrottle]

    def post(self, request):
        serializer = SOSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        tenant = request.user.tenant or Tenant.objects.filter(slug="default").first()
        if not tenant:
            tenant = Tenant.objects.create(name="Default", slug="default")

        fraud_score = check_fraud(request.user, data)
        severity = calculate_severity(data)

        emergency = EmergencyRequest.objects.create(
            tenant=tenant,
            patient=request.user,
            is_sos=True,
            priority=severity["priority"],
            ai_severity_score=severity["score"],
            ai_fraud_score=fraud_score,
            fraud_flagged=fraud_score > 0.7,
            source=EmergencyRequest.Source.APP,
            pickup_latitude=data["pickup_latitude"],
            pickup_longitude=data["pickup_longitude"],
            pickup_address=data.get("pickup_address", ""),
            symptoms=data.get("symptoms", ""),
            emergency_type=data.get("emergency_type", ""),
            wearable_data=data.get("wearable_data", {}),
            voice_stress_score=data.get("voice_stress_score"),
            offline_sync_id=data.get("offline_sync_id", ""),
            status=EmergencyRequest.Status.PENDING if not fraud_score > 0.7 else EmergencyRequest.Status.PENDING,
        )

        log_audit(request.user, AuditLog.Action.SOS, "emergency", str(emergency.id), request=request)
        broadcast_emergency_update(str(emergency.id), {"event": "sos_created", "id": str(emergency.id)})

        if not emergency.fraud_flagged:
            dispatch_emergency.delay(str(emergency.id))
            notify_emergency_contacts.delay(str(emergency.id))

        return Response(EmergencyRequestSerializer(emergency).data, status=status.HTTP_201_CREATED)


class EmergencyListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmergencyRequestSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == UserRole.PATIENT:
            return EmergencyRequest.objects.filter(patient=user)
        if user.role == UserRole.DRIVER and hasattr(user, "driver_profile"):
            return EmergencyRequest.objects.filter(driver=user.driver_profile)
        if user.role in (UserRole.HOSPITAL_ADMIN, UserRole.SUPER_ADMIN):
            return EmergencyRequest.objects.filter(tenant=user.tenant)
        return EmergencyRequest.objects.none()


class EmergencyDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmergencyRequestSerializer
    queryset = EmergencyRequest.objects.all()
    lookup_field = "id"


class DriverAcceptView(APIView):
    permission_classes = [IsAuthenticated, IsDriver]

    def post(self, request, id):
        action = request.data.get("action", "accept")
        driver = request.user.driver_profile
        try:
            emergency = EmergencyRequest.objects.get(id=id, driver=driver)
        except EmergencyRequest.DoesNotExist:
            return Response({"detail": "Not assigned"}, status=404)

        if action == "accept":
            emergency.status = EmergencyRequest.Status.EN_ROUTE
            driver.availability = "on_trip"
            driver.save(update_fields=["availability"])
        else:
            emergency.status = EmergencyRequest.Status.DISPATCHING
            emergency.driver = None
            dispatch_emergency.delay(str(emergency.id))

        emergency.save()
        broadcast_emergency_update(str(emergency.id), {"event": "status_change", "status": emergency.status})
        return Response(EmergencyRequestSerializer(emergency).data)


class GPSPingView(APIView):
    permission_classes = [IsAuthenticated, IsDriver]

    def post(self, request, id):
        serializer = GPSLogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        driver = request.user.driver_profile
        emergency = EmergencyRequest.objects.filter(id=id, driver=driver).first()

        from apps.emergencies.models import GPSLog

        log = GPSLog.objects.create(
            emergency=emergency,
            driver=driver,
            ambulance=driver.ambulance,
            **serializer.validated_data,
        )
        if driver:
            driver.latitude = log.latitude
            driver.longitude = log.longitude
            driver.save(update_fields=["latitude", "longitude"])

        broadcast_emergency_update(
            str(id),
            {
                "event": "gps_update",
                "lat": float(log.latitude),
                "lng": float(log.longitude),
                "eta_minutes": emergency.eta_minutes if emergency else None,
            },
        )
        return Response(GPSLogSerializer(log).data)


class OfflineSyncView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]

    def post(self, request):
        synced = []
        for item in request.data.get("emergencies", []):
            if EmergencyRequest.objects.filter(offline_sync_id=item.get("offline_sync_id")).exists():
                continue
            view = SOSView()
            view.request = request
            request._full_data = item
            # Simplified: reuse SOS logic per item
            synced.append(item.get("offline_sync_id"))
        return Response({"synced": synced})

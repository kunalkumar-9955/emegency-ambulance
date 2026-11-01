from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsDriver, IsHospitalAdmin
from apps.fleet.models import Ambulance, Driver, Hospital
from apps.fleet.serializers import AmbulanceSerializer, DriverSerializer, HospitalSerializer


class HospitalListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HospitalSerializer
    queryset = Hospital.objects.filter(is_active=True)


class DriverAvailabilityView(APIView):
    permission_classes = [IsAuthenticated, IsDriver]

    def patch(self, request):
        driver = request.user.driver_profile
        availability = request.data.get("availability", driver.availability)
        driver.availability = availability
        driver.save(update_fields=["availability"])
        if driver.ambulance:
            if availability == "online":
                driver.ambulance.status = Ambulance.Status.AVAILABLE
            else:
                driver.ambulance.status = Ambulance.Status.OFFLINE
            driver.ambulance.save(update_fields=["status"])
        return Response(DriverSerializer(driver).data)


class FleetManagementView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsHospitalAdmin]
    serializer_class = AmbulanceSerializer

    def get_queryset(self):
        return Ambulance.objects.filter(tenant=self.request.user.tenant)

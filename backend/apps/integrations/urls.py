from django.urls import path
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.integrations.maps import geocode_address, get_directions


class GeocodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        address = request.query_params.get("address", "")
        result = geocode_address(address)
        if not result:
            return Response({"detail": "Not found"}, status=404)
        return Response(result)


class DirectionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = get_directions(
            float(request.query_params["origin_lat"]),
            float(request.query_params["origin_lng"]),
            float(request.query_params["dest_lat"]),
            float(request.query_params["dest_lng"]),
        )
        return Response(result)


class SMSWebhookView(APIView):
    """Offline SMS emergency — Twilio webhook."""

    permission_classes = [AllowAny]

    def post(self, request):
        from apps.core.models import Tenant
        from apps.emergencies.models import EmergencyRequest
        from apps.accounts.models import User

        phone = request.data.get("From", "")
        body = request.data.get("Body", "")
        user = User.objects.filter(phone=phone).first()
        if not user:
            return Response({"detail": "Unknown number"}, status=400)
        tenant = user.tenant or Tenant.objects.get(slug="default")
        EmergencyRequest.objects.create(
            tenant=tenant,
            patient=user,
            is_sos=True,
            source=EmergencyRequest.Source.SMS,
            pickup_latitude=0,
            pickup_longitude=0,
            pickup_address=body[:500],
            symptoms=body,
        )
        return Response({"status": "queued"})


urlpatterns = [
    path("maps/geocode/", GeocodeView.as_view()),
    path("maps/directions/", DirectionsView.as_view()),
    path("webhooks/sms/", SMSWebhookView.as_view()),
]

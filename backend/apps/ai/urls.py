from django.urls import path
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsHospitalOrSuperAdmin
from apps.ai.models import AIAnalytics
from apps.ai.services.traffic import predict_traffic


class TrafficPredictionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lat = float(request.query_params.get("lat", 0))
        lng = float(request.query_params.get("lng", 0))
        return Response(predict_traffic(lat, lng))


class AnalyticsDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsHospitalOrSuperAdmin]

    def get(self, request):
        reports = AIAnalytics.objects.order_by("-generated_at")[:20]
        return Response([
            {"id": str(r.id), "type": r.report_type, "data": r.data, "generated_at": r.generated_at}
            for r in reports
        ])


urlpatterns = [
    path("ai/traffic/", TrafficPredictionView.as_view()),
    path("ai/analytics/", AnalyticsDashboardView.as_view()),
]

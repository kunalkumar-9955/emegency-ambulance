from datetime import timedelta

from django.db import connection
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminPanelRequest, IsSuperAdmin
from apps.ai.models import AIAnalytics
from apps.emergencies.models import EmergencyRequest
from apps.audit.models import AuditLog


class AdminPanelBaseView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin, IsAdminPanelRequest]


class AdminAnalyticsView(AdminPanelBaseView):
    def get(self, request):
        today = timezone.now().date()
        emergencies_today = EmergencyRequest.objects.filter(created_at__date=today).count()
        active = EmergencyRequest.objects.filter(
            status__in=["pending", "dispatching", "assigned", "en_route"]
        ).count()
        latest_ai = AIAnalytics.objects.order_by("-generated_at")[:5]
        return Response({
            "emergencies_today": emergencies_today,
            "active_emergencies": active,
            "ai_reports": [
                {"type": r.report_type, "generated_at": r.generated_at, "summary": r.data.get("summary")}
                for r in latest_ai
            ],
            "heatmap_preview": self._heatmap(),
        })

    def _heatmap(self):
        from django.db.models import Count
        qs = (
            EmergencyRequest.objects.filter(status="completed")
            .values("pickup_latitude", "pickup_longitude")
            .annotate(count=Count("id"))[:50]
        )
        return list(qs)


class AdminEmergenciesView(AdminPanelBaseView):
    def get(self, request):
        qs = EmergencyRequest.objects.select_related("patient", "driver", "hospital").order_by("-created_at")[:100]
        return Response([
            {
                "id": str(e.id),
                "status": e.status,
                "priority": e.priority,
                "is_sos": e.is_sos,
                "patient": e.patient.email,
                "created_at": e.created_at,
                "fraud_flagged": e.fraud_flagged,
            }
            for e in qs
        ])


class AdminSystemHealthView(AdminPanelBaseView):
    def get(self, request):
        db_ok = True
        try:
            connection.ensure_connection()
        except Exception:
            db_ok = False
        return Response({
            "database": "ok" if db_ok else "error",
            "timestamp": timezone.now().isoformat(),
            "audit_logs_24h": AuditLog.objects.filter(
                created_at__gte=timezone.now() - timedelta(hours=24)
            ).count(),
        })


class AdminBackupView(AdminPanelBaseView):
    def post(self, request):
        from apps.integrations.backup import trigger_backup
        task_id = trigger_backup()
        return Response({"status": "backup_queued", "task_id": task_id})

from django.db.models import Avg, Count
from django.utils import timezone

from apps.ai.models import AIAnalytics
from apps.emergencies.models import EmergencyRequest


def generate_daily_analytics(tenant_id=None):
    now = timezone.now()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    qs = EmergencyRequest.objects.filter(created_at__gte=start)
    if tenant_id:
        qs = qs.filter(tenant_id=tenant_id)

    stats = qs.aggregate(
        total=Count("id"),
        avg_severity=Avg("ai_severity_score"),
        avg_response=Avg("eta_minutes"),
    )
    by_hour = {}
    for e in qs:
        h = e.created_at.hour
        by_hour[h] = by_hour.get(h, 0) + 1

    report = AIAnalytics.objects.create(
        tenant_id=tenant_id,
        report_type=AIAnalytics.ReportType.RESPONSE_TIME,
        period_start=start,
        period_end=now,
        data={
            "summary": f"{stats['total']} emergencies today",
            "total": stats["total"],
            "avg_severity": stats["avg_severity"],
            "avg_eta": stats["avg_response"],
            "peak_hours": sorted(by_hour.items(), key=lambda x: -x[1])[:3],
        },
    )
    return report

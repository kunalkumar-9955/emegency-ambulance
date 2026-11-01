"""AI Fraud Detection — fake bookings, GPS spoofing, bots."""

from datetime import timedelta

from django.core.cache import cache
from django.utils import timezone


def check_fraud(user, data: dict) -> float:
    score = 0.0
    cache_key = f"sos_rate:{user.id}"
    count = cache.get(cache_key, 0)
    if count > 5:
        score += 0.5
    cache.set(cache_key, count + 1, 3600)

    lat = float(data.get("pickup_latitude", 0))
    lng = float(data.get("pickup_longitude", 0))
    if lat == 0 and lng == 0:
        score += 0.4
    if abs(lat) > 90 or abs(lng) > 180:
        score += 0.8

    from apps.emergencies.models import EmergencyRequest

    recent = EmergencyRequest.objects.filter(
        patient=user,
        created_at__gte=timezone.now() - timedelta(minutes=30),
    ).count()
    if recent > 3:
        score += 0.3

    return min(1.0, score)

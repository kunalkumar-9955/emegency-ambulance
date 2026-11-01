"""AI Smart Ambulance Dispatch — nearest ambulance, hospital, route."""

import math

from apps.fleet.models import Ambulance, Driver, Hospital


def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371
    p = math.pi / 180
    a = 0.5 - math.cos((lat2 - lat1) * p) / 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * (1 - math.cos((lon2 - lon1) * p)) / 2
    return 2 * r * math.asin(math.sqrt(a))


def run_smart_dispatch(emergency) -> dict:
    pickup_lat = float(emergency.pickup_latitude)
    pickup_lng = float(emergency.pickup_longitude)

    drivers = Driver.objects.filter(
        tenant=emergency.tenant,
        availability=Driver.Availability.ONLINE,
        latitude__isnull=False,
    ).select_related("ambulance", "user")

    best_driver = None
    best_distance = float("inf")

    for driver in drivers:
        dist = haversine_km(pickup_lat, pickup_lng, float(driver.latitude), float(driver.longitude))
        traffic_factor = 1.1  # Placeholder for AI traffic prediction integration
        score = dist * traffic_factor / max(float(driver.rating), 0.1)
        if score < best_distance:
            best_distance = score
            best_driver = driver

    hospital = (
        Hospital.objects.filter(tenant=emergency.tenant, is_active=True, icu_beds_available__gt=0)
        .order_by("icu_beds_available")
        .first()
    )

    if not best_driver:
        available_amb = Ambulance.objects.filter(tenant=emergency.tenant, status=Ambulance.Status.AVAILABLE).first()
        return {"eta_minutes": None, "hospital_id": str(hospital.id) if hospital else None}

    eta_minutes = max(3, int(best_distance * 3))
    return {
        "driver_id": str(best_driver.id),
        "ambulance_id": str(best_driver.ambulance_id) if best_driver.ambulance_id else None,
        "hospital_id": str(hospital.id) if hospital else None,
        "eta_minutes": eta_minutes,
        "distance_km": round(best_distance, 2),
    }

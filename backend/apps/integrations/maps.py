import requests
from django.conf import settings


def geocode_address(address: str) -> dict | None:
    """Free geocoding via OpenStreetMap Nominatim."""
    if not settings.OPENSTREETMAP_ENABLED:
        return None
    base = getattr(settings, "NOMINATIM_BASE_URL", "https://nominatim.openstreetmap.org")
    resp = requests.get(
        f"{base.rstrip('/')}/search",
        params={"q": address, "format": "json", "limit": 1},
        headers={"User-Agent": "EmergencyAmbulance/1.0"},
        timeout=10,
    )
    if resp.ok and resp.json():
        r = resp.json()[0]
        return {"lat": float(r["lat"]), "lng": float(r["lon"])}
    return None


def get_directions(origin_lat, origin_lng, dest_lat, dest_lng) -> dict:
    """Free routing via OSRM (same response shape for existing API clients)."""
    base = getattr(settings, "OSRM_BASE_URL", "https://router.project-osrm.org").rstrip("/")
    coords = f"{origin_lng},{origin_lat};{dest_lng},{dest_lat}"
    url = f"{base}/route/v1/driving/{coords}"
    resp = requests.get(
        url,
        params={"overview": "false", "steps": "false"},
        timeout=15,
    )
    if resp.ok:
        data = resp.json()
        if data.get("code") == "Ok" and data.get("routes"):
            route = data["routes"][0]
            return {
                "distance_km": route["distance"] / 1000,
                "duration_minutes": max(1, int(route["duration"] / 60)),
            }
    return {"distance_km": 5.0, "duration_minutes": 12}

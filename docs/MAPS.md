# Map System — 100% Free (OSM + OSRM)

All paid map APIs (**Mapbox**, **Google Maps**) have been **removed**.

| Layer | Technology | Cost |
|-------|------------|------|
| Map display | **OpenStreetMap** + `flutter_map` | Free |
| Offline tiles | `flutter_map_cache` | Free |
| Routing & ETA | **OSRM** | Free |
| Geocoding (API) | **Nominatim** | Free |
| Live tracking | Django WebSocket | Unchanged |
| Driver GPS POST | Django REST | Unchanged |

## Flutter package: `mobile/map_kit/`

```
map_kit/
├── config/map_env.dart
├── services/
│   ├── osrm_routing_service.dart   # Routes (GeoJSON → polyline)
│   ├── osm_tile_cache.dart         # OSM + Carto dark tiles
│   ├── map_websocket_service.dart
│   ├── location_service.dart
│   └── map_service.dart
├── controllers/
│   ├── map_controller.dart         # EmergencyMapController
│   └── tracking_controller.dart    # OSRM refresh every N seconds
└── screens/
    ├── map_screen.dart
    └── live_tracking_screen.dart
```

## Configuration

Copy optional env (no keys required):

```bash
cp mobile/patient_app/.env.example mobile/patient_app/.env
```

```env
OSRM_BASE_URL=https://router.project-osrm.org
ROUTE_REFRESH_SECONDS=5
```

**Production:** run your own [OSRM](https://github.com/Project-OSRM/osrm-backend) instance and point `OSRM_BASE_URL` to it. The public demo server is rate-limited.

## Features

- Real-time ambulance tracking (WebSocket)
- Nearby hospitals (`GET /hospitals/` — existing API)
- Live OSRM route with emergency red highlight
- Source / destination / ambulance markers
- Dark & light map modes
- Zoom controls + center on user
- Offline OSM tile cache
- Low-end optimizations (`RepaintBoundary`, reduced tile buffer)

## Backend (same API paths)

- `GET /api/v1/maps/geocode/?address=...` — Nominatim
- `GET /api/v1/maps/directions/?origin_lat=...` — OSRM

```env
OSRM_BASE_URL=https://router.project-osrm.org
NOMINATIM_BASE_URL=https://nominatim.openstreetmap.org
```

## Permissions

**Android:** `ACCESS_FINE_LOCATION`, `INTERNET`  
**iOS:** `NSLocationWhenInUseUsageDescription`

## Nominatim usage policy

Use a valid `User-Agent`, respect rate limits (1 req/s), or self-host Nominatim for production geocoding volume.

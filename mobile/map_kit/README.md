# map_kit

**100% free** map module for Emergency Ambulance apps.

| Feature | Service |
|---------|---------|
| Map tiles | OpenStreetMap (`flutter_map`) |
| Offline cache | `flutter_map_cache` |
| Routing | [OSRM](https://project-osrm.org/) |
| Geocoding (backend) | Nominatim |
| Live GPS | Django WebSocket (unchanged) |

No Mapbox, Google Maps, or paid APIs.

## Setup

Optional `.env` (defaults work without it):

```env
OSRM_BASE_URL=https://router.project-osrm.org
ROUTE_REFRESH_SECONDS=5
```

For production traffic, **self-host OSRM** and set `OSRM_BASE_URL` to your server.

## Usage

```dart
await MapEnv.load(fileName: '.env');

final mapService = MapService(
  apiBase: 'http://10.0.2.2:8000/api/v1',
  wsBase: 'ws://10.0.2.2:8000/ws',
  authToken: token,
);

Navigator.push(
  context,
  MaterialPageRoute(
    builder: (_) => LiveTrackingScreen(
      mapService: mapService,
      emergencyId: emergencyId,
      patientLocation: LatLng(lat, lng),
    ),
  ),
);
```

## Architecture

```
map_env.dart          → OSRM / OSM URLs
osrm_routing_service  → Route polylines + ETA
osm_tile_cache        → Tiles + dark mode
map_websocket_service → Live ambulance position
map_service           → Facade
emergency_map_controller / tracking_controller
emergency_map_widget  → flutter_map UI
```

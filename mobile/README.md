# Flutter Mobile Apps

## Map stack (100% free)

- **OpenStreetMap** — `flutter_map` + cached tiles
- **OSRM** — routing and ETA
- **No Mapbox, no Google Maps, no API keys required**

See [../docs/MAPS.md](../docs/MAPS.md).

## Apps

| App | Path |
|-----|------|
| Patient | `patient_app/` |
| Driver | `driver_app/` |
| Map module | `map_kit/` |

## Setup

```bash
cd patient_app
flutter pub get
flutter run
```

Optional `.env` overrides (see `.env.example`).

## API

```dart
// lib/core/config.dart
static const apiBase = 'http://10.0.2.2:8000/api/v1';
static const wsBase = 'ws://10.0.2.2:8000/ws';
```

Patient: **Map** and **Live Tracking Map** after SOS.  
Driver: **Navigate** with OSRM route + GPS POST.

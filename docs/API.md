# API Reference (v1)

Base: `http://localhost:8000/api/v1`

## Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register/` | Register patient/driver |
| POST | `/auth/login/` | JWT access + refresh |
| POST | `/auth/refresh/` | Refresh token |
| POST | `/auth/logout/` | Logout (audit) |

## Emergencies
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/emergencies/sos/` | One-tap SOS (throttled) |
| GET | `/emergencies/` | List user emergencies |
| GET | `/emergencies/{id}/` | Detail |
| POST | `/emergencies/{id}/accept/` | Driver accept/reject |
| POST | `/emergencies/{id}/gps/` | Driver GPS ping |
| POST | `/emergencies/offline-sync/` | Offline queue sync |

## WebSocket
- `ws://host/ws/emergency/{id}/` — Live tracking
- `ws://host/ws/driver/{id}/` — Driver position

## AI
- `GET /ai/traffic/?lat=&lng=` — Traffic prediction
- `GET /ai/analytics/` — Dashboard data

## OTA
- `GET /ota/check/?app=patient&platform=android&build=100`
- `POST /ota/push/` — Super admin only
- `POST /ota/{id}/rollback/`

## Super Admin (localhost + `X-Admin-Panel-Key`)
- `GET /admin-panel/analytics/`
- `GET /admin-panel/emergencies/live/`
- `GET /admin-panel/system/health/`
- `POST /admin-panel/backup/trigger/`

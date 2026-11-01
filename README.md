# Emergency Ambulance Booking Platform

AI-powered, production-ready emergency ambulance ecosystem with real-time tracking, smart dispatch, multi-tenant architecture, and encrypted communication.

## Problem & Solution

| Problem | Solution |
|---------|----------|
| Late ambulance arrival | AI nearest-ambulance dispatch + traffic-aware routing |
| No live tracking | WebSocket GPS streaming + family live tracking |
| Poor hospital coordination | Smart hospital matching + ICU/bed APIs |
| Traffic delays | AI traffic prediction + alternate routes |
| Fake bookings | AI fraud detection + GPS spoofing checks |
| No centralized monitoring | Super Admin dashboard + emergency heatmap |
| No priority management | AI severity detection + triage queue |
| Rural accessibility | Offline SMS mode + low-bandwidth support |
| No real-time comms | E2E encrypted chat + voice/video |
| No analytics | AI analytics dashboard + hotspot prediction |

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                     │
├──────────────┬──────────────┬──────────────┬──────────────────────────┤
│ Flutter      │ Next.js Web  │ Super Admin  │ Wearables / Drones (IoT) │
│ Patient/Driver│ Marketing    │ localhost    │ Future integrations      │
└──────┬───────┴──────┬───────┴──────┬───────┴──────────────┬───────────┘
       │              │              │                      │
       └──────────────┴──────────────┴──────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Nginx (TLS/LB)   │
                    └─────────┬─────────┘
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
┌──────▼──────┐    ┌──────────▼──────────┐   ┌──────▼──────┐
│ Django API  │    │ Django Channels     │   │ Celery      │
│ (REST/JWT)  │    │ (WebSockets)        │   │ Workers     │
└──────┬──────┘    └──────────┬──────────┘   └──────┬──────┘
       │                      │                      │
       └──────────────────────┼──────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
       ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
       │ PostgreSQL  │ │ Redis       │ │ S3/GCS      │
       │ (multi-tenant)│ │ cache/queue │ │ media/E2E   │
       └─────────────┘ └─────────────┘ └─────────────┘
```

## Monorepo Structure

```
├── backend/              # Django + DRF + Channels + Celery
├── frontend-web/         # Next.js marketing + booking portal
├── mobile/               # Flutter patient + driver apps
├── admin-panel/          # Localhost Super Admin (encrypted)
├── infrastructure/       # Docker, Nginx, CI/CD, K8s-ready
└── docs/                 # Architecture & API docs
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for web/admin)
- Flutter 3.16+ (for mobile)
- Python 3.12+ (local dev without Docker)

### Run with Docker

```bash
cp backend/.env.example backend/.env
docker compose up -d --build
```

| Service | URL |
|---------|-----|
| API | http://localhost:8000/api/v1/ |
| API Docs | http://localhost:8000/api/docs/ |
| WebSocket | ws://localhost:8000/ws/ |
| Website | http://localhost:3000 |
| Super Admin | http://localhost:5173 (localhost only) |
| Flower (Celery) | http://localhost:5555 |

### Default Super Admin (change in production)
- Email: `admin@emergency.local`
- Password: set via `python manage.py createsuperuser`

## User Roles (RBAC)

| Role | Scope |
|------|-------|
| `patient` | SOS, booking, tracking, medical profile |
| `driver` | Accept requests, navigation, earnings |
| `hospital_admin` | Fleet, beds, staff, arrivals |
| `super_admin` | Full system (localhost panel) |
| `volunteer` | Crowd emergency alerts |

## Security

- JWT + refresh tokens with rotation
- End-to-end encryption (libsodium) for medical messages
- API rate limiting (Redis-backed)
- Audit logs on all sensitive actions
- Device session management
- RBAC per tenant

## Maps (Flutter)

- **OpenStreetMap** + **OSRM** — 100% free (`mobile/map_kit`)
- No Mapbox, Google Maps, or paid map APIs — see `docs/MAPS.md`

## AI Services

Microservice-ready modules under `backend/apps/ai/`:
- Smart dispatch
- Traffic prediction
- Severity detection
- Fraud detection
- Analytics aggregation

## License

Proprietary — Emergency Ambulance Platform

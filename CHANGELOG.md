# Changelog

---

## v1.2.0 — Project Architecture

### Added

- Project resource
- Project CRUD API
- Project database model
- Project repository
- Project service
- Project schemas
- Project migration

### Improved

- API Keys now belong to Projects
- Identity endpoint returns Project information
- Dashboard redesigned around Projects
- Swagger documentation
- Platform architecture

### Architecture

Nativeee is now built around:

```text
Project
↓
API Keys
↓
Usage
↓
Analytics
↓
Dashboard
```

This architecture prepares the platform for the upcoming Developer Console and Enterprise features.

---

## v1.0.0 — Platform Foundation

**Released:** 2026

### Added

- FastAPI Backend
- Provider Registry
- API Keys
- Swagger Authentication
- Usage Logging
- Analytics Foundation
- Rate Limiting Foundation
- SQLAlchemy
- Alembic
- Railway Deployment
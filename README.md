
# Nativee Platform

> AI infrastructure platform powering Nativee Mobile, Web, Developer Platform, and Enterprise integrations.

---

# Overview

Nativee Platform is an AI infrastructure system designed to remove language barriers through Speech, Translation, and Voice technologies.

The platform currently powers:

- Nativee Mobile
- Nativee Web
- Developer Platform (Console)
- Enterprise Integrations

---

# Technology Stack

## Backend
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Python 3.11+
- Railway

## AI Runtime
- Groq Whisper (Speech-to-Text)
- Google Translation Provider
- Edge TTS (Text-to-Speech)
- Provider Registry Architecture

## Platform Layer
- JWT Authentication
- API Key Authentication
- Project-based Multi-tenancy
- Dynamic Plans
- Rate Limiting Engine
- Usage Logging System
- Analytics Engine
- Customer Dashboard
- Project Dashboard

---

# Platform Architecture

The system follows a clean layered architecture:

```text
Routes
    ↓
Dependencies / Middleware
    ↓
Services
    ↓
Repositories
    ↓
Models
    ↓
PostgreSQL
````

### Why this architecture?

* Separation of concerns
* Scalable business logic layer
* Independent database access layer
* Easy testing and maintainability
* Clean API boundaries

---

# Core Domain Model

The platform is built around a **Project-based multi-tenant architecture**:

```text
User
  │
  ├── Project
  │     ├── API Keys
  │     ├── Usage Logs
  │     ├── Analytics
  │     └── Dashboards
```

### Key Principles

* Users can own multiple projects
* Each project isolates data and usage
* API keys belong to projects (not users directly)
* Usage and analytics are project-scoped
* JWT defines user identity
* API keys define execution access

---

# Core Resources

* Users
* Projects
* API Keys
* Plans
* Usage Logs
* Analytics
* Dashboards
* Identity System

---

# AI APIs

* Conversation API
* Translation API
* Speech API

---

# Platform APIs

## Authentication

* POST `/v1/auth/register`
* POST `/v1/auth/login`
* GET `/v1/auth/me`

## Projects

* GET `/v1/projects`
* POST `/v1/projects`
* GET `/v1/projects/{id}`
* PATCH `/v1/projects/{id}`
* DELETE `/v1/projects/{id}`

## API Keys

* GET `/v1/api-keys`
* POST `/v1/api-keys`
* PATCH `/v1/api-keys/{id}/enable`
* PATCH `/v1/api-keys/{id}/disable`
* POST `/v1/api-keys/{id}/rotate`
* DELETE `/v1/api-keys/{id}`

## Usage & Analytics

* GET `/v1/usage`
* GET `/v1/analytics/overview`

## Dashboards

* GET `/v1/dashboard` (Customer Dashboard)
* GET `/v1/projects/{project_id}/dashboard` (Project Dashboard)

## Platform

* GET `/v1/plans`
* GET `/v1/me`
* GET `/v1/health`

---

# ⚙️ Features

## Identity & Access

* JWT Authentication
* API Key Authentication
* Role-Based Access Control
* Project Ownership Enforcement

## Project Management

* Create Projects
* Update Projects
* Delete Projects
* Multi-project Support per User

## API Platform

* API Key Management
* Dynamic Billing Plans
* Rate Limiting System
* Monthly Quotas

## Observability

* Usage Logging
* Analytics Engine
* Customer Dashboard
* Project Dashboard
* Performance Metrics

## AI Runtime

* Provider Registry
* Groq Whisper Speech-to-Text
* Google Translation API
* Edge Text-to-Speech

---

# Project Structure

```text
app/
├── api/
├── core/
├── database/
├── dependencies/
├── middleware/
├── models/
├── pipelines/
├── providers/
├── repositories/
├── routes/
├── schemas/
├── services/
├── utils/
└── main.py

migrations/
```

---

# Backend Status

Current system supports:

* Authentication system
* Project-based architecture
* API key system
* Usage tracking
* Analytics engine
* Customer dashboard
* Project dashboard
* AI runtime layer
* Speech & Translation APIs
* Health monitoring

---

# 🛣️ Roadmap

## Phase 1 Foundation

* Layered Architecture
* Repository Pattern
* Service Layer
* Project-based Multi-tenancy
* API Versioning
* Dashboard Foundation
* Provider Registry

## Phase 2 Developer Console

* Project Management UI
* API Key Management UI
* Usage Dashboard
* Analytics Dashboard
* Nativee Console

## Phase 3 Platform Expansion

* Billing System
* Teams & Organizations
* Audit Logs
* SDKs (Python, JS)
* Webhooks
* API Explorer
* Enterprise Features

---

# Run Locally

```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

alembic upgrade head

uvicorn main:app --reload
```

---

# Deployment

## Production

* Railway

## Planned Domains

* api.nativee.in
* console.nativee.in
* developer.nativee.in
* docs.nativee.in
* status.nativee.in

---

# Final Note

Nativee Platform is evolving into a **fully multi-tenant AI developer platform** with:

* Project isolation
* Usage-based analytics
* Scalable AI runtime
* Developer-first APIs

```

---

If you want next upgrade, I can also create:
- :contentReference[oaicite:0]{index=0}
- or :contentReference[oaicite:1]{index=1}
- or :contentReference[oaicite:2]{index=2}
```

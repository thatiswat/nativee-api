<<<<<<< HEAD

# Nativee Platform
=======
# 🚀 Nativee Platform
>>>>>>> 903ba11 (refactor: reorganize backend into scalable AI platform architecture)

> AI Infrastructure Platform for multilingual communication.
>
> Nativee enables developers and enterprises to integrate Speech Recognition, Translation, and Text-to-Speech through a scalable API platform.

---

<<<<<<< HEAD
# Overview
=======
# 🌍 Vision
>>>>>>> 903ba11 (refactor: reorganize backend into scalable AI platform architecture)

Nativee is building the AI infrastructure layer for multilingual communication.

Our mission is to remove language barriers by providing production-ready APIs that power applications across mobile, web, enterprise, and AI agents.

---

<<<<<<< HEAD
# Technology Stack
=======
# 🏛 Platform Overview

Nativee consists of two independent platform surfaces built on a shared backend.

```text
                 Nativee Platform
                        │
        ┌───────────────┴────────────────┐
        │                                │
        ▼                                ▼
 Nativee Console                  Nativee AI Platform
 (JWT Authentication)             (API Key Authentication)

 Dashboard                        Conversation API
 Projects                         Translation API
 API Keys                         Future AI APIs
 Analytics                        SDKs
 Billing                          Enterprise Integrations
```

---

# ⚙ Technology Stack
>>>>>>> 903ba11 (refactor: reorganize backend into scalable AI platform architecture)

## Backend

- FastAPI
- Python 3.11+
- PostgreSQL
- SQLAlchemy
- Alembic

## AI Runtime

- Groq Whisper (Speech-to-Text)
- Google Translation Provider
- Edge TTS
- Provider Registry Architecture

## Infrastructure

- Railway
- Supabase PostgreSQL
- JWT Authentication
- API Key Authentication

---

<<<<<<< HEAD
# Platform Architecture
=======
# 🏗 Architecture
>>>>>>> 903ba11 (refactor: reorganize backend into scalable AI platform architecture)

Nativee follows a layered architecture designed for long-term maintainability.

```text
HTTP Request
      │
      ▼
API Layer
      │
Dependencies
Middleware
      │
      ▼
Service Layer
      │
      ▼
Repository Layer
      │
      ▼
Database Models
      │
      ▼
PostgreSQL
```

AI execution is handled independently through pipelines.

```text
Conversation API
        │
        ▼
Conversation Pipeline
        │
 ┌──────┼────────┐
 │      │        │
 ▼      ▼        ▼
STT  Translation  TTS
        │
        ▼
Provider Registry
```

---

<<<<<<< HEAD
# Core Domain Model
=======
# 🔐 Authentication Model
>>>>>>> 903ba11 (refactor: reorganize backend into scalable AI platform architecture)

Nativee uses two authentication mechanisms with different responsibilities.

## Customer Authentication (JWT)

Used only for the Developer Console.

Supports:

- Login
- Dashboard
- Projects
- API Keys
- Analytics
- Billing

---

## API Authentication (API Keys)

Used only for AI APIs.

Example:

```http
Authorization: Bearer ntv_live_xxxxxxxxxxxxxxxxx
```

Supports:

- Conversation API
- Translation API
- Future AI APIs

---

# 🧠 Core Domain Model

```text
User
 │
 ├── Projects
 │      │
 │      ├── API Keys
 │      ├── Usage Logs
 │      ├── Analytics
 │      └── Dashboard
 │
 └── Billing
```

### Design Principles

- Project-based multi-tenancy
- Resource isolation
- Project-scoped analytics
- API key ownership
- Usage-based billing foundation

---

<<<<<<< HEAD
# Core Resources
=======
# 📦 Platform Components
>>>>>>> 903ba11 (refactor: reorganize backend into scalable AI platform architecture)

## Identity

- JWT Authentication
- API Key Authentication
- Ownership Validation

<<<<<<< HEAD
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
=======
## Project Platform

- Projects
- API Keys
- Plans
- Usage
- Analytics
>>>>>>> 903ba11 (refactor: reorganize backend into scalable AI platform architecture)

## AI Runtime

- Conversation Pipeline
- Translation Pipeline
- Provider Registry
- Speech Processing
- Text-to-Speech

---

# Project Structure

```text
app/
│
├── api/
│   └── v1/
│       ├── customer/
│       ├── ai/
│       └── platform/
│
├── core/
├── database/
├── dependencies/
├── middleware/
├── models/
├── pipelines/
├── providers/
├── repositories/
├── schemas/
├── security/
├── services/
├── utils/
└── workers/

migrations/
```

---

<<<<<<< HEAD
# Backend Status
=======
# 🌐 API Surfaces
>>>>>>> 903ba11 (refactor: reorganize backend into scalable AI platform architecture)

## Customer APIs

JWT Protected

```text
/v1/customer/auth
/v1/customer/projects
/v1/customer/api-keys
/v1/customer/dashboard
/v1/customer/analytics
/v1/customer/usage
/v1/customer/profile
```

---

## AI APIs

<<<<<<< HEAD
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
=======
API Key Protected

```text
/v1/ai/conversation
/v1/ai/translate
```

---

## Platform APIs

```text
/v1/platform/plans
/v1/platform/health
/v1/platform/status
/v1/platform/version
```

---

# 🔄 AI Runtime

Current Providers

| Capability | Provider |
|------------|----------|
| Speech Recognition | Groq Whisper |
| Translation | Google |
| Text-to-Speech | Edge TTS |

Future providers can be added without changing business logic through the Provider Registry.

---

# 📊 Platform Features

## Identity

- JWT Login
- API Key Authentication
- Ownership Enforcement

## Project Management

- Multiple Projects
- Project Isolation
- API Key Management

## Analytics

- Usage Logging
- Performance Metrics
- Customer Dashboard
- Project Dashboard

## Platform

- Dynamic Plans
- Rate Limiting
- Monthly Quotas
- Health Monitoring

---

# 🚀 Current Status

## Foundation ✅

- Layered Architecture
- Repository Pattern
- Service Layer
- Provider Registry
- Conversation Pipeline
- Project-based Multi-tenancy
- API Versioning
- Usage Logging
- Analytics Engine
- Customer Dashboard
- Project Dashboard

---

# 🛣 Roadmap

## Phase 2 — Developer Platform

- Nativee Console
- API Playground
- Live Request Logs
- Developer Documentation
- SDK Downloads

---

## Phase 3 — Platform Expansion

- Organizations
- Team Management
- Billing
- Audit Logs
- Webhooks
- Python SDK
- JavaScript SDK
- Streaming APIs
- Batch Processing

---

## Phase 4 — Enterprise

- SSO
- Private Deployments
- Provider Failover
- Enterprise Analytics
- Dedicated Infrastructure

---

# 💻 Development
>>>>>>> 903ba11 (refactor: reorganize backend into scalable AI platform architecture)

```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

alembic upgrade head

uvicorn main:app --reload
```

---

<<<<<<< HEAD
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
=======
# 🌍 Deployment

Production Services
>>>>>>> 903ba11 (refactor: reorganize backend into scalable AI platform architecture)

```text
api.nativee.in
console.nativee.in
developer.nativee.in
docs.nativee.in
status.nativee.in
```

---

# 🎯 Philosophy

Nativee is designed as an AI infrastructure platform rather than a single AI application.

The architecture emphasizes:

- Scalability
- Clear separation of concerns
- Project-based multi-tenancy
- Provider abstraction
- Production-ready APIs
- Developer-first experience

Our goal is to provide a robust foundation for multilingual AI applications that can scale from individual developers to enterprise deployments.
# Nativeee Platform Architecture

---

# Philosophy

Nativeee follows a layered architecture.

```
Client

↓

Authentication Middleware

↓

Platform Middleware

↓

Routes

↓

Services

↓

Repositories

↓

Database

↓

AI Providers
```

Each layer owns exactly one responsibility.

---

# Platform Architecture

```
                    Nativeee Platform

            Mobile        Web        SDK
                │
                ▼
      Authentication Middleware
                │
                ▼
          Request Context
                │
                ▼
        Dynamic Rate Limiting
                │
                ▼
              Routes
                │
                ▼
             Services
                │
                ▼
        Provider Registry
                │
      ┌─────────┴─────────┐
      ▼                   ▼
 Groq Whisper      Google Provider
                          │
                          ▼
                     Edge TTS
                │
                ▼
          Usage Logging
                │
                ▼
           PostgreSQL
```

---

# Folder Structure

```
app/

api/
core/
database/
middleware/
models/
providers/
repositories/
routes/
schemas/
services/
utils/
```

---

# Layer Responsibilities

## Middleware

Responsible for

- Authentication
- Rate Limiting
- Request Context

---

## Routes

Responsible for

- HTTP
- Request Validation
- Response Models

Routes never contain SQL or business logic.

---

## Services

Responsible for business logic.

Current Services

- APIKeyService
- PlanService
- UsageService
- IdentityService
- DashboardService

---

## Repositories

Responsible for database access.

Current Repositories

- APIKeyRepository
- PlanRepository
- UsageRepository

---

## Providers

Responsible for external AI integrations.

Current Providers

- Groq Whisper
- Google Translation
- Edge TTS

---

## Schemas

Responsible for API contracts.

Current Schemas

- MeResponse
- UsageSummaryResponse
- DashboardResponse

---

# Request Lifecycle

Conversation Request

↓

Authentication Middleware

↓

API Key Lookup

↓

Plan Resolution

↓

Dynamic Rate Limiting

↓

Business Route

↓

Business Service

↓

Provider Registry

↓

Speech / Translation / TTS

↓

Usage Logging

↓

Response

---

# Developer APIs

Identity

GET /v1/me

Usage

GET /v1/usage

Dashboard

GET /v1/dashboard

Plans

GET /v1/plans

API Keys

POST /v1/api-keys

---

# Engineering Principles

- Repository Pattern
- Service Layer
- Provider Abstraction
- Thin Routes
- Typed Response Schemas
- Dependency Injection
- Single Responsibility Principle

---

# Current Status

Platform Foundation

✅ Complete

Developer Platform

✅ Complete

Platform Intelligence

🚧 In Progress

Commercial Platform

⏳ Planned

Enterprise Platform

⏳ Planned
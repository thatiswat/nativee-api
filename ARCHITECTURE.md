# 🏛 Nativee Platform Architecture

---

# Philosophy

Nativee is designed as an AI infrastructure platform, not a single AI application.

The platform follows a layered architecture with strict separation of responsibilities.

```
Client

↓

API Layer

↓

Authentication / Dependencies

↓

Business Services

↓

Repositories

↓

PostgreSQL

↓

AI Providers
```

Each layer owns exactly one responsibility.

No layer bypasses another.

---

# Platform Architecture

```
                        Nativee Platform

                 ┌──────────────────────────┐
                 │     Nativee Console      │
                 │     (JWT Protected)      │
                 └─────────────┬────────────┘
                               │
                               │
                 ┌─────────────▼────────────┐
                 │      Nativee AI API      │
                 │    (API Key Protected)   │
                 └─────────────┬────────────┘
                               │
                               ▼
                      Authentication Layer
                               │
                               ▼
                    Rate Limiting & Validation
                               │
                               ▼
                           API Layer
                               │
                               ▼
                        Business Services
                               │
                               ▼
                       Conversation Pipeline
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        Speech-to-Text    Translation     Text-to-Speech
              │                │                │
              └──────────── Provider Registry ────────────┘
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
```

---

# Layer Responsibilities

## API Layer

Responsible for

- HTTP Endpoints
- Request Validation
- Response Models

Routes never contain business logic or SQL.

---

## Dependencies

Responsible for

- JWT Authentication
- API Key Authentication
- Ownership Validation
- Database Sessions

---

## Services

Responsible for

- Business Rules
- Platform Logic
- Orchestration

Current Services

- AuthService
- ProjectService
- APIKeyService
- UsageService
- AnalyticsService
- CustomerDashboardService
- ProjectDashboardService
- ConversationService

Services never contain SQL.

---

## Pipelines

Responsible for AI orchestration.

Current Pipelines

- Conversation Pipeline

Pipeline flow

```
Speech

↓

Speech Recognition

↓

Translation

↓

Text-to-Speech

↓

Result
```

Pipelines never authenticate users or access the database.

---

## Repositories

Responsible only for database access.

Current Repositories

- UserRepository
- ProjectRepository
- APIKeyRepository
- UsageRepository
- AnalyticsRepository
- PlanRepository

Repositories never contain business rules.

---

## Providers

Responsible for external AI integrations.

Current Providers

- Groq Whisper
- Google Translation
- Edge TTS

Future Providers

- IndicTrans2
- Deepgram
- ElevenLabs
- OpenAI
- Azure Speech

Providers never interact with the database.

---

## Schemas

Responsible for API contracts.

Examples

- ConversationResponse
- DashboardResponse
- UsageSummaryResponse
- AnalyticsResponse

---

# Authentication Model

Nativee separates customer identity from application identity.

## Customer Authentication

```
Email

↓

JWT

↓

Console APIs
```

Supports

- Dashboard
- Projects
- API Keys
- Analytics
- Usage
- Billing

---

## API Authentication

```
API Key

↓

AI APIs
```

Supports

- Conversation
- Translation
- Future AI APIs

---

# Request Lifecycle

```
Client

↓

Authentication

↓

Ownership Validation

↓

Rate Limiting

↓

API Route

↓

Business Service

↓

Pipeline

↓

Provider Registry

↓

AI Providers

↓

Usage Logging

↓

Response
```

---

# Platform APIs

## Customer APIs (JWT)

```
/v1/customer/auth
/v1/customer/projects
/v1/customer/api-keys
/v1/customer/dashboard
/v1/customer/analytics
/v1/customer/usage
/v1/customer/profile
```

---

## AI APIs (API Key)

```
/v1/ai/conversation
/v1/ai/translate
```

---

## Platform APIs

```
/v1/platform/plans
/v1/platform/health
/v1/platform/status
/v1/platform/version
```

---

# Engineering Principles

- Layered Architecture
- Repository Pattern
- Service Layer
- Provider Abstraction
- Pipeline Architecture
- Thin API Layer
- Dependency Injection
- Project-based Multi-tenancy
- Strong Ownership Validation
- Single Responsibility Principle

---

# Current Platform Status

## Foundation

✅ Complete

- Layered Architecture
- API Versioning
- Repository Pattern
- Service Layer
- Provider Registry
- Conversation Pipeline

---

## Platform

✅ Complete

- JWT Authentication
- API Key Authentication
- Projects
- API Keys
- Usage Logging
- Analytics
- Customer Dashboard
- Project Dashboard

---

## Developer Platform

🚧 In Progress

- Developer Console
- API Playground
- Live Logs
- SDKs

---

## Enterprise Platform

⏳ Planned

- Organizations
- Team Management
- Billing
- Audit Logs
- Webhooks
- Streaming APIs
- Enterprise Infrastructure

---

# Design Principles

Nativee is built around three architectural principles.

### 1. Human Identity

Users authenticate with JWT to manage their account.

### 2. Application Identity

Applications authenticate using API Keys to access AI services.

### 3. Project Isolation

Every request, API Key, usage log, and analytic belongs to a project, providing strong isolation for security, billing, and scalability.
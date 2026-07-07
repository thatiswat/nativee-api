# Nativee Platform Architecture

---

# Philosophy

Nativee separates platform infrastructure from AI execution.

The platform is responsible for authentication, project management, API key management, usage tracking, analytics, billing foundations, and request authorization.

AI execution is delegated to the Nativee Engine.

Every layer has a single responsibility and communicates only with adjacent layers.

---

# Platform Architecture

```text
                           Nativee Platform

                ┌────────────────────────────────┐
                │        Nativee Console         │
                │        (JWT Protected)         │
                └───────────────┬────────────────┘
                                │
                                │
                ┌───────────────▼────────────────┐
                │          Nativee API          │
                │      (API Key Protected)      │
                └───────────────┬────────────────┘
                                │
                                ▼
                    Authentication & Authorization
                                │
                                ▼
                     Ownership & Rate Limiting
                                │
                                ▼
                            API Layer
                                │
                                ▼
                        Business Services
                                │
                                ▼
                    Nativee Engine Client
                                │
                                ▼
                         Nativee Engine
                                │
                                ▼
                          Usage Logging
                                │
                                ▼
                            PostgreSQL
```

---

# Folder Structure

```text
app/

├── api/
│   └── v1/
│       ├── ai/
│       ├── customer/
│       └── platform/
│
├── core/
├── database/
├── dependencies/
├── middleware/
├── models/
├── repositories/
├── schemas/
├── security/
├── services/
├── utils/
└── main.py

migrations/
```

---

# Layer Responsibilities

## API Layer

Responsible for

- HTTP endpoints
- Request validation
- Response models

Routes never contain business logic.

---

## Dependencies

Responsible for

- JWT authentication
- API key authentication
- Database sessions
- Ownership validation

Dependencies never contain business rules.

---

## Services

Responsible for

- Business logic
- Request orchestration
- Platform workflows
- Communication with Nativee Engine

Current Services

- AuthService
- ProjectService
- APIKeyService
- UsageService
- AnalyticsService
- CustomerDashboardService
- ProjectDashboardService
- ConversationService

Services never execute SQL directly.

---

## Repositories

Responsible only for database operations.

Current Repositories

- UserRepository
- ProjectRepository
- APIKeyRepository
- UsageRepository
- AnalyticsRepository
- PlanRepository

Repositories never contain business logic.

---

## Schemas

Responsible for API contracts.

Examples

- ConversationResponse
- TranslateResponse
- DashboardResponse
- UsageSummaryResponse
- AnalyticsResponse

Schemas are shared between the API layer and clients.

---

# Authentication Model

Nativee separates customer identity from application identity.

## Customer Authentication

```text
User

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

```text
Application

↓

API Key

↓

AI APIs
```

Supports

- Conversation API
- Translation API
- Future AI APIs

---

# Request Lifecycle

```text
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

Nativee Engine

↓

Usage Logging

↓

Response
```

The API delegates AI execution to Nativee Engine and records request metadata for analytics and billing.

---

# API Surface

## Customer APIs

```text
/v1/customer/auth
/v1/customer/profile
/v1/customer/projects
/v1/customer/api-keys
/v1/customer/dashboard
/v1/customer/analytics
/v1/customer/usage
```

---

## AI APIs

```text
/v1/ai/conversation
/v1/ai/translate
```

These endpoints authenticate requests and forward execution to Nativee Engine.

---

## Platform APIs

```text
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
- Thin API Layer
- Dependency Injection
- Project-based Multi-tenancy
- Strong Ownership Validation
- Separation of Platform and AI Runtime
- Single Responsibility Principle

---

# Platform Status

## Foundation

Completed

- Layered Architecture
- API Versioning
- Repository Pattern
- Service Layer
- JWT Authentication
- API Key Authentication
- Project Management
- Usage Tracking
- Analytics
- Dashboard Foundation

---

## Platform

Completed

- Projects
- API Keys
- Customer Dashboard
- Project Dashboard
- Usage Logging
- Analytics
- Rate Limiting

---

## In Progress

- Developer Console
- API Playground
- SDKs
- Billing

---

## Planned

- Organizations
- Team Management
- Audit Logs
- Webhooks
- Enterprise Features

---

# Design Principles

Nativee is built around three architectural concepts.

## Human Identity

Users authenticate with JWT to access the Nativee Console.

---

## Application Identity

Applications authenticate with API Keys to access AI services.

---

## Platform Isolation

Every project owns its API keys, usage records, analytics, and billing data, providing secure multi-tenant isolation.

---

# Relationship with Nativee Engine

The Nativee API is the platform gateway.

The Nativee Engine is an independent execution runtime.

```text
Client
    │
    ▼
Nativee API
    │
    ▼
Nativee Engine
    │
    ▼
Speech Recognition
Translation
Speech Synthesis
Benchmarking
Streaming
```

This separation allows the platform and the AI runtime to evolve independently while maintaining a stable public API.
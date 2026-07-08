# 📦 Changelog

---

# v3.0.0 — Distributed Platform

> Nativee evolves from a monolithic backend into a distributed AI platform with independent Identity, API, and Engine services.

Released: July 2026

---

## 🚀 Added

### Nativee Identity

- Dedicated authentication service
- RS256 JWT authentication
- RSA key infrastructure
- Refresh token support
- Session management
- Identity verification endpoints
- Independent deployment
- Independent PostgreSQL database

---

### Nativee API

- JWT verification using Nativee Identity
- Business platform separation
- Identity integration
- Business user architecture
- Project management
- API Key lifecycle
- Usage tracking
- Analytics
- Dashboard APIs
- Plan management
- Engine gateway

---

### Nativee Engine

- Independent AI runtime
- Streaming architecture
- Speech recognition
- Translation
- Voice synthesis
- Provider abstraction
- Performance benchmarking

---

### Platform Infrastructure

- Distributed service architecture
- Independent Railway deployments
- Independent databases
- Environment isolation
- RS256 public/private key authentication
- Cross-service authentication

---

## 🏗 Architecture

Nativee now consists of three independent backend services.

```text
                Nativee Platform

          Mobile • Web • SDKs
                   │
                   ▼
           Nativee Identity
         Authentication • JWT
                   │
              RS256 JWT
                   │
      ┌────────────┴────────────┐
      ▼                         ▼
 Nativee API              Nativee Engine
Business Platform          AI Runtime
```

---

## 🔐 Authentication

Authentication has been completely redesigned.

### Previous

```text
API

↓

JWT_SECRET

↓

Authentication
```

### Current

```text
Nativee Identity

↓

RS256 JWT

↓

Nativee API

↓

JWT Verification
```

Improvements

- Centralized authentication
- Public/private key cryptography
- Independent identity service
- Service-to-service trust
- Improved security model

---

## 🗄 Database Architecture

Previous

```text
Single PostgreSQL Database
```

Current

```text
Identity Database

↓

Users
Sessions
Identity Data

----------------------

Platform Database

↓

Projects
Plans
API Keys
Usage
Analytics

----------------------

Nativee Engine

Independent AI Runtime
```

---

## 🚀 Deployment

Nativee services are now deployed independently.

- Nativee Identity
- Nativee API
- Nativee Engine

Each service has

- Independent Railway deployment
- Independent environment variables
- Independent release cycle

---

## 🎯 Platform Capabilities

Nativee now supports

- Centralized authentication
- RS256 JWT verification
- Project management
- API key management
- Usage tracking
- Analytics
- Subscription plans
- Dashboard APIs
- AI gateway
- Speech recognition
- Translation
- Voice synthesis

---

## 🔄 Breaking Changes

- Authentication removed from Nativee API.
- JWT generation moved to Nativee Identity.
- API now verifies Identity-issued JWTs.
- Platform architecture split into multiple services.
- Authentication migrated from shared secret to RS256.
- Independent Identity database introduced.

---

## 📈 Engineering Improvements

- Service-Oriented Architecture
- Repository Pattern
- Service Layer
- Dependency Injection
- Multi-Tenant Foundation
- Independent Deployments
- Independent Databases
- Production RS256 Authentication

---

## 🚧 Next Milestones

- Automatic Business User Provisioning
- Organizations
- Teams
- Billing
- SDKs
- Webhooks
- Enterprise Features

---

# v2.0.0 — Platform Foundation

Released: June 2026

## Added

### Platform

- Layered architecture
- Repository pattern
- Service layer
- API versioning
- Customer APIs
- AI APIs
- Platform APIs

### Resources

- Projects
- API Keys
- Plans
- Usage
- Analytics
- Dashboard

### AI

- Conversation pipeline
- Provider registry
- Groq Speech Recognition
- Google Translation
- Edge Text-to-Speech

### Infrastructure

- Health endpoints
- Rate limiting
- Alembic migrations
- Railway deployment

---

# v1.0.0 — Initial Backend

Released: 2026

## Added

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Swagger/OpenAPI
- Initial AI APIs
- Initial authentication
- First Railway deployment

---

## Notes

This release established the initial Nativee backend and laid the foundation for what would become the Nativee Platform.
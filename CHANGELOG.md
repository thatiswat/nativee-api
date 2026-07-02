# 📦 Changelog

---

# v2.0.0 — Nativee Platform Architecture

> Major platform refactor transforming Nativee from a backend application into a scalable AI infrastructure platform.

Released: 2026

---

## 🚀 Added

### Platform Architecture

- Layered architecture
- API versioning
- Customer API surface
- AI API surface
- Platform API surface
- Modular API package structure

---

### Authentication

- JWT Authentication
- API Key Authentication
- Project ownership validation
- Authentication separation between Console and AI APIs

---

### Project Platform

- Project resource
- Project CRUD
- Project repository
- Project service
- Project dashboard
- Project-based multi-tenancy

---

### API Platform

- API Key generation
- API Key rotation
- Enable / Disable API Keys
- API Key ownership validation
- Project-scoped API Keys

---

### Usage & Analytics

- Usage logging engine
- Analytics engine
- Customer dashboard
- Project dashboard
- Usage summaries
- Performance metrics

---

### AI Runtime

- Conversation Pipeline
- Provider Registry
- Groq Speech-to-Text
- Google Translation Provider
- Edge Text-to-Speech

---

### Infrastructure

- Health endpoints
- Dynamic plans
- Rate limiting foundation
- SQLAlchemy repositories
- Alembic migrations
- Railway deployment

---

## 🏗 Architecture Improvements

### API Structure

Reorganized API into dedicated platform surfaces.

```text
/v1/customer

/v1/ai

/v1/platform
```

---

### Folder Structure

Migrated to a modular package layout.

```text
app/

api/
core/
database/
dependencies/
middleware/
models/
pipelines/
providers/
repositories/
schemas/
security/
services/
utils/
workers/
```

---

### Authentication Model

Separated customer identity from application identity.

```text
JWT

↓

Customer Console
```

```text
API Key

↓

AI Platform
```

---

### Request Flow

```text
Request

↓

Authentication

↓

Service Layer

↓

Pipeline

↓

Provider Registry

↓

AI Providers

↓

Usage Logging

↓

Database
```

---

## 🔄 Breaking Changes

- API routes reorganized into Customer, AI, and Platform modules.
- Project ownership now controls API Key ownership.
- Request Context architecture removed.
- AI runtime now uses pipeline-based execution.
- API structure reorganized for long-term scalability.

---

## 🎯 Platform Capabilities

Nativee now supports:

- Multi-project architecture
- Project isolation
- API Key management
- Usage logging
- Analytics
- Customer dashboard
- Project dashboard
- Speech Recognition
- Translation
- Text-to-Speech
- Provider abstraction
- AI pipelines

---

# v1.0.0 — Platform Foundation

Released: 2026

---

## Added

- FastAPI Backend
- SQLAlchemy
- Alembic
- PostgreSQL
- Railway Deployment
- Initial Authentication
- Provider Registry
- API Keys
- Swagger Documentation
- Usage Logging Foundation
- Analytics Foundation
- Rate Limiting Foundation

---

## Notes

This release established the initial backend foundation for Nativee and introduced the first version of the AI platform architecture.
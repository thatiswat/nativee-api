# Nativee Platform Architecture

The Nativee Platform is a distributed, service-oriented architecture designed to separate authentication, business logic, and AI execution into independent services.

Each service owns a single responsibility and communicates through well-defined interfaces, enabling independent deployment, scaling, and evolution.

---

# Platform Overview

```text
                           Nativee Platform

                Mobile • Web • SDKs • CLI
                         │
                         ▼
                 Nativee Identity
        Authentication • Sessions • JWT
                         │
                  RS256 Access Token
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
     Nativee API                 Nativee Engine
 Business Platform               AI Runtime
          │                             │
          ▼                             ▼
 PostgreSQL                     AI Providers
```

---

# Service Responsibilities

## Nativee Identity

Responsible for authentication and user identity.

Owns

- User Accounts
- Passwords
- Sessions
- Refresh Tokens
- Email Verification
- Password Reset
- JWT Generation
- RSA Keys

Never owns

- Projects
- API Keys
- Billing
- Analytics

Database

```
Identity Database
```

---

## Nativee API

Responsible for the business platform.

Owns

- Business Users
- Projects
- API Keys
- Plans
- Usage
- Analytics
- Dashboard
- Rate Limits
- Engine Gateway

Never owns

- Passwords
- Sessions
- Authentication
- Token Generation

Database

```
Platform Database
```

---

## Nativee Engine

Responsible for AI execution.

Owns

- Speech Recognition
- Translation
- Voice Synthesis
- Streaming
- AI Provider Management
- Performance Benchmarking

Never owns

- Authentication
- Users
- Billing
- Projects

---

# Authentication Flow

```text
User

↓

Nativee Identity

↓

Authenticate

↓

RS256 JWT

↓

Nativee API

↓

Verify Signature

↓

Resolve Business User

↓

Projects
```

Authentication is centralized inside Nativee Identity.

Nativee API only verifies Identity-issued JWTs.

---

# Business User Flow

```text
Identity User

↓

JWT

↓

Nativee API

↓

Business User Exists?

      │

      ├── Yes

      │

      └── No

           ↓

Create Business User

↓

Assign Starter Plan

↓

Return User
```

This automatic provisioning is the foundation for platform onboarding.

---

# AI Request Flow

```text
Application

↓

API Key

↓

Nativee API

↓

Validate API Key

↓

Ownership Check

↓

Rate Limit

↓

Nativee Engine

↓

Speech

↓

Translation

↓

Voice

↓

Usage Logging

↓

Response
```

---

# Internal Layer Architecture

```text
HTTP Request

↓

Middleware

↓

Dependencies

↓

API Routes

↓

Business Services

↓

Repositories

↓

PostgreSQL
```

---

# Folder Structure

```text
app/

├── api/
│   ├── platform/
│   │   ├── ai/
│   │   └── console/
│   │
│   ├── client/
│   └── legacy/
│
├── core/
├── database/
├── dependencies/
├── middleware/
├── models/
├── repositories/
├── schemas/
│   ├── platform/
│   ├── shared/
│   └── client/
│
├── services/
│   ├── platform/
│   ├── shared/
│   └── client/
│
├── utils/
└── main.py
```

---

# Layer Responsibilities

## Middleware

Responsible for

- Request IDs
- Logging
- Timing
- CORS
- Error Handling

---

## Dependencies

Responsible for

- JWT Verification
- API Key Authentication
- Database Sessions
- Rate Limit Resolution
- Identity Resolution

Dependencies never contain business logic.

---

## API Layer

Responsible for

- HTTP Endpoints
- Request Validation
- Response Models

Routes remain thin.

---

## Services

Responsible for

- Business Rules
- Platform Workflows
- Engine Communication
- Resource Orchestration

Services never execute SQL.

---

## Repositories

Responsible only for

- Create
- Read
- Update
- Delete

Repositories never contain business logic.

---

## Schemas

Responsible for

- Request Models
- Response Models
- Shared Contracts

---

# Security Model

## Human Identity

```text
User

↓

Nativee Identity

↓

JWT

↓

Nativee API
```

Protected using RS256.

---

## Application Identity

```text
Developer

↓

API Key

↓

Nativee API

↓

Nativee Engine
```

Protected using hashed API Keys.

---

# Platform Principles

- Service-Oriented Architecture
- Repository Pattern
- Service Layer
- Dependency Injection
- Multi-Tenant Isolation
- Principle of Least Privilege
- Separation of Authentication and Business Logic
- Independent Deployments
- Independent Databases
- RS256 Authentication

---

# Current Platform Status

## Completed

- Nativee Identity
- Nativee API
- Nativee Engine
- RS256 Authentication
- Railway Deployment
- API Keys
- Plans
- Projects
- Usage Tracking
- Analytics
- Dashboard
- Engine Integration

---

## In Progress

- Automatic Business User Provisioning
- Developer Console
- SDKs
- Billing Foundations

---

## Planned

- Organizations
- Teams
- Role-Based Access Control
- Audit Logs
- Webhooks
- Enterprise Features
- Marketplace Integrations

---

# Design Philosophy

Nativee is built on three independent domains.

```
Identity

↓

Business Platform

↓

AI Runtime
```

Each domain owns its own data, responsibilities, deployment pipeline, and release cycle.

This separation allows Nativee to scale from a single developer to enterprise workloads while maintaining a clean, maintainable architecture.
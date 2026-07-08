# Nativee API

The business platform powering the Nativee ecosystem.

Nativee API provides project management, API key management, plans, usage tracking, analytics, developer resources, and acts as the gateway between applications and the Nativee Engine.

Authentication is handled by **Nativee Identity** using RS256 JWTs. Nativee API verifies Identity-issued tokens and never stores passwords or issues authentication tokens.

---

# Overview

```
                    Nativee Platform

             Mobile • Web • SDKs • CLI
                       │
                       ▼
               Nativee Identity
        Authentication • Sessions • JWT
                       │
                 RS256 Access Token
                       │
                       ▼
                  Nativee API
┌──────────────────────────────────────────────────────┐
│ Business Users                                       │
│ Projects                                              │
│ API Keys                                              │
│ Plans                                                 │
│ Usage Tracking                                        │
│ Analytics                                             │
│ Dashboard                                             │
│ Rate Limiting                                         │
│ Engine Client                                         │
└────────────────────────┬─────────────────────────────┘
                         │
                   Internal HTTP
                         │
                         ▼
                  Nativee Engine
┌──────────────────────────────────────────────────────┐
│ Speech Recognition                                   │
│ Translation                                          │
│ Voice Synthesis                                      │
│ Streaming                                            │
│ AI Providers                                         │
│ Performance Optimization                             │
└────────────────────────┬─────────────────────────────┘
                         │
              Groq • Google • Edge • Future Providers
```

---

# Responsibilities

Nativee API is responsible for:

- Business User Management
- Project Management
- API Key Lifecycle
- Subscription Plans
- Usage Tracking
- Analytics
- Dashboard APIs
- Rate Limits & Quotas
- Engine Orchestration

Nativee API is **not responsible for**:

- User Authentication
- Password Storage
- Session Management
- Token Generation

These responsibilities belong exclusively to **Nativee Identity**.

---

# Authentication

Customer authentication is delegated to Nativee Identity.

```
User

↓

Nativee Identity

↓

RS256 JWT

↓

Nativee API

↓

JWT Verification

↓

Business User

↓

Projects
```

The API verifies:

- Signature
- Issuer
- Audience
- Token Type

before serving protected resources.

---

# Features

## Developer Platform

- Projects
- API Keys
- Usage Tracking
- Analytics
- Dashboard
- Subscription Plans

## AI Platform

- Speech Conversation
- Translation
- Streaming Audio
- Engine Gateway

## Platform

- Health Monitoring
- Version Discovery
- Engine Connectivity
- OpenAPI Documentation

---

# API Resources

## Console

```
Projects
API Keys
Plans
Dashboard
Usage
Analytics
```

## AI

```
POST /ai/conversation
POST /ai/translate
```

## Platform

```
Health
Version
OpenAPI
```

---

# Engine Integration

Nativee API communicates with Nativee Engine using internal HTTP.

```
Developer

↓

Nativee API

↓

Engine Client

↓

Nativee Engine

↓

AI Providers
```

This separation allows the Engine to evolve independently without changing the public API.

---

# Current AI Pipeline

```
Audio

↓

Speech Recognition

↓

Translation

↓

Voice Synthesis

↓

Streaming Audio
```

---

# Performance

Current local performance

| Stage | Average |
|--------|---------:|
| Speech Recognition | ~300–500 ms |
| Translation | ~40–900 ms |
| First Audio | ~600–800 ms |
| Engine Pipeline | ~1.1 s |

---

# Security

## Customer Console

Authentication uses Identity-issued RS256 JWTs.

```
Authorization: Bearer <access_token>
```

## AI APIs

Authentication uses Nativee API Keys.

```
Authorization: Bearer ntv_live_xxxxxxxxx
```

Nativee API validates:

- JWT Signature
- Issuer
- Audience
- API Key Status
- Project Ownership
- Rate Limits

---

# Local Development

```bash
git clone https://github.com/nativeee/nativeee-api

cd nativeee-api

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload
```

Swagger

```
http://127.0.0.1:8001/docs
```

---

# Environment Variables

```env
DATABASE_URL=

ENGINE_URL=

IDENTITY_URL=

IDENTITY_PUBLIC_KEY=

IDENTITY_ISSUER=

IDENTITY_AUDIENCE=

IDENTITY_ALGORITHM=RS256

GROQ_API_KEY=
```

---

# Companion Services

```
                Nativee Platform

          ┌────────────────────┐
          │ Nativee Identity   │
          │ Authentication     │
          └─────────┬──────────┘
                    │
             RS256 JWT
                    │
          ┌─────────▼──────────┐
          │  Nativee API       │
          │ Business Platform  │
          └─────────┬──────────┘
                    │
          Internal HTTP
                    │
          ┌─────────▼──────────┐
          │ Nativee Engine     │
          │ AI Runtime         │
          └────────────────────┘
```

---

# Current Status

- ✅ Nativee Identity Integration
- ✅ RS256 Authentication
- ✅ Project Management
- ✅ API Key Management
- ✅ Plans
- ✅ Usage Tracking
- ✅ Analytics
- ✅ Engine Integration
- ✅ Railway Deployment

---

# Roadmap

### Platform

- Automatic Business User Provisioning
- Organizations & Teams
- Role-Based Access Control
- Billing & Subscriptions
- Audit Logs

### Developer Experience

- Python SDK
- JavaScript SDK
- CLI
- Webhooks

### AI Platform

- Streaming Conversations
- Additional AI Providers
- Model Routing
- Observability

---

# License

**Proprietary Software**

Copyright © Nativee Technologies.
All rights reserved.
# Nativeee Platform

> AI Language Platform powering Nativeee Mobile, Web, and the future Developer Platform.

---

## Overview

Nativeee Platform is an AI infrastructure platform designed to remove language barriers through Speech, Translation and Voice technologies.

The platform currently powers:

- Nativeee Mobile
- Nativeee Web
- Future Public Developer APIs
- Enterprise Integrations

---

# Technology Stack

## Backend

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Railway

## AI Runtime

- Groq Whisper (Speech-to-Text)
- Google Translation Provider
- Edge TTS
- Provider Registry

## Platform

- API Key Authentication
- Dynamic Plans
- Dynamic Rate Limiting
- Usage Logging
- Developer Dashboard APIs

---

# Platform APIs

## AI

- Conversation API
- Translation API

## Developer Platform

- GET /v1/me
- GET /v1/usage
- GET /v1/dashboard
- GET /v1/plans
- POST /v1/api-keys

---

# Current Features

## Identity

- API Keys
- Authentication Middleware
- Plans
- Identity API

## Traffic Control

- Dynamic Rate Limiting
- Plan Based Limits

## Observability

- Usage Logging
- Usage API
- Dashboard API

## AI Runtime

- Provider Registry
- Groq STT
- Google Translation
- Edge TTS

---

# Documentation

See

- ARCHITECTURE.md
- ROADMAP.md

---

# Run Locally

```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload
```

---

# Deployment

Production

Railway

Future

api.nativeee.in
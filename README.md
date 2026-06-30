# Nativee Platform

> AI language platform powering Nativeee Mobile, Web, and the future Developer Platform.

---

# Overview

<<<<<<< HEAD
Nativee Platform is an AI infrastructure platform designed to remove language barriers through Speech, Translation and Voice technologies.
=======
Nativee Platform is an AI infrastructure platform designed to remove language barriers through Speech, Translation, and Voice technologies.
>>>>>>> 161289a (feat(platform): introduce project-based platform architecture)

The platform currently powers:

- Nativee Mobile
- Nativee Web
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
- Projects
- Dynamic Plans
- Dynamic Rate Limiting
- Usage Logging
- Developer Dashboard APIs

---

# Platform Architecture

Nativee follows a layered architecture.

```text
Routes
    ↓
Services
    ↓
Repositories
    ↓
Models
    ↓
PostgreSQL
```

This separation keeps business logic independent from HTTP endpoints and database access, making the platform easier to test, maintain, and extend.

---

# Resources

The platform is organized around the following core resources:

- Projects
- API Keys
- Plans
- Usage
- Analytics
- Dashboard
- Identity

---

# Platform APIs

## AI APIs

- Conversation API
- Translation API
- Speech API

## Developer Platform APIs

- GET `/v1/me`
- GET `/v1/dashboard`
- GET `/v1/usage`
- GET `/v1/plans`
- GET `/v1/projects`
- POST `/v1/projects`
- GET `/v1/api-keys`
- POST `/v1/api-keys`
- GET `/v1/health`

---

# Current Features

## Identity

- API Keys
- Authentication Middleware
- Projects
- Plans
- Identity API

## Traffic Control

- Dynamic Rate Limiting
- Plan-based Limits

## Observability

- Usage Logging
- Usage API
- Analytics API
- Dashboard API

## AI Runtime

- Provider Registry
- Groq Speech-to-Text
- Google Translation
- Edge Text-to-Speech

---

# Project Structure

```text
app/
├── api/
├── middleware/
├── models/
├── repositories/
├── routes/
├── schemas/
├── services/
└── utils/

migrations/
```

---

# Backend Milestone

The platform currently supports:

- Authentication
- API Keys
- Projects
- Plans
- Usage
- Analytics
- Dashboard
- Identity
- Speech
- Translation
- Health
- Audio

---

# Documentation

See:

- `ARCHITECTURE.md`
- `ROADMAP.md`
- `CHANGELOG.md`

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

## Production

Railway

## Future

<<<<<<< HEAD
api.nativee.in
=======
- `api.nativee.in`
- Developer Console
- Enterprise Platform
>>>>>>> 161289a (feat(platform): introduce project-based platform architecture)

# Nativeee API

> AI Language Platform powering Nativeee.

---

## Overview

Nativeee API is the backend platform that powers:

- Nativeee Mobile
- Nativeee Web
- Future Developer Platform
- Third-party integrations

Current AI Stack

- Groq Whisper (Speech-to-Text)
- Translation Provider Registry
- Edge TTS
- FastAPI
- PostgreSQL
- SQLAlchemy
- Railway

---

## Features

- API Key Authentication
- Usage Analytics
- Rate Limiting
- Conversation Pipeline
- Provider Registry
- Swagger Documentation
- Structured Logging
- Alembic Migrations

---

## Architecture

See:

ARCHITECTURE.md

---

## Roadmap

See:

ROADMAP.md

---

## Running locally

```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload
```

---

## Deployment

Production:

Railway

Future:

api.nativeee.in
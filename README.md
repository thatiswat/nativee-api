# Nativee API

The developer platform for building multilingual AI applications.

Nativee API provides authentication, API key management, projects, usage tracking, analytics, billing foundations, and a unified interface to the Nativeee Engine.

The API itself does **not** perform AI inference. All speech recognition, translation, and voice synthesis are delegated to the Nativeee Engine.

---

## Architecture

```
                    Nativee Platform

                  Mobile / Web / SDKs
                          │
                          ▼
                    Nativee API
┌─────────────────────────────────────────────────────┐
│ Authentication (JWT)                                │
│ API Key Validation                                  │
│ Projects                                             │
│ Plans                                                │
│ Usage & Analytics                                    │
│ Rate Limiting & Quotas                               │
│ Engine Client                                        │
└───────────────────────┬─────────────────────────────┘
                        │
                 Internal HTTP
                        │
                        ▼
                  Nativeee Engine
┌─────────────────────────────────────────────────────┐
│ Speech Recognition                                  │
│ Translation                                         │
│ Voice Synthesis                                     │
│ Streaming                                           │
│ Provider Abstraction                                │
│ Performance Profiling                               │
└───────────────────────┬─────────────────────────────┘
                        │
              Groq • Google • Edge
```

---

## Features

### Customer Platform

- Customer Authentication (JWT)
- Project Management
- API Key Management
- Usage Tracking
- Analytics
- Plans
- Dashboard APIs

### AI Platform

- Speech Conversation
- Text Translation
- Streaming Speech
- Audio Delivery

### Platform

- Health Monitoring
- Version Discovery
- Engine Connectivity
- OpenAPI Documentation

---

## API Endpoints

### AI

```
POST /v1/ai/conversation
POST /v1/ai/translate
```

### Customer

```
Authentication
Projects
API Keys
Dashboard
Usage
Analytics
```

### Platform

```
GET /v1/platform/health
GET /v1/platform/version
GET /v1/platform/plans
```

---

## Engine Integration

Nativeee API communicates with the Nativeee Engine over HTTP.

```
Developer

↓

Nativeee API

↓

Engine Client

↓

Nativeee Engine

↓

Groq
Google
Edge
```

This architecture allows the Engine to evolve independently without changing the public API.

---

## Current AI Pipeline

```
Audio

↓

Speech Recognition

↓

Translation

↓

Voice Synthesis

↓

Audio Response
```

---

## Performance

Current average local performance:

| Stage | Average |
|--------|---------:|
| Speech Recognition | ~300–500 ms |
| Translation | ~40–900 ms |
| First Audio (TTFA) | ~600–800 ms |
| Engine Pipeline | ~1.1 s |

---

## Security

### Customer Console

Uses JWT authentication.

```
Authorization: Bearer <JWT>
```

### AI APIs

Uses Nativeee API Keys.

```
Authorization: Bearer ntv_live_xxxxxxxxx
```

---

## Running Locally

```bash
git clone https://github.com/nativeee/nativeee-api

cd nativeee-api

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python -m uvicorn app.main:app --reload
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

## Environment Variables

```
DATABASE_URL=

JWT_SECRET_KEY=

GROQ_API_KEY=

ENGINE_URL=http://127.0.0.1:8001
```

---

## Companion Project

Nativeee API relies on the Nativeee Engine for AI inference.

```
nativeee-api
        │
        ▼
nativeee-engine
```

The Engine is responsible for:

- Speech Recognition
- Translation
- Voice Synthesis
- Streaming
- AI Provider Management
- Performance Optimization

---

## Roadmap

- Streaming Conversation API
- SDKs (Python & JavaScript)
- Billing
- Organizations & Teams
- Enterprise Features
- Additional AI APIs
- Monitoring & Observability

---

## License

Proprietary © Nativee Technologies
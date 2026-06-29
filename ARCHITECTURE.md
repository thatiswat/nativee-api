# Nativeee Platform Architecture

## Philosophy

Nativeee follows a layered architecture.

```
Client

↓

Middleware

↓

Routes

↓

Services

↓

Pipelines

↓

Providers

↓

Repositories

↓

Database
```

Every layer has one responsibility.

---

## Folder Structure

app/

api/

core/

database/

middleware/

models/

pipelines/

providers/

repositories/

routes/

schemas/

services/

utils/

---

## Request Flow

Conversation

↓

Authentication

↓

Rate Limit

↓

Conversation Route

↓

Conversation Service

↓

Conversation Pipeline

↓

Provider Registry

↓

Groq

↓

Translation Provider

↓

Edge TTS

↓

Usage Logging

↓

Response

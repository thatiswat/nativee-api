from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()


# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


# ==========================================================
# API Keys
# ==========================================================

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    "",
).strip()

API_KEY = os.getenv(
    "API_KEY",
    "",
).strip()


# ==========================================================
# Database
# ==========================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "",
).strip()

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is missing. Please set it in your environment variables."
    )


# ==========================================================
# Translation
# ==========================================================

TRANSLATION_PROVIDER = os.getenv(
    "TRANSLATION_PROVIDER",
    "google",
).strip().lower()


# ==========================================================
# Nativee Engine
# ==========================================================

ENGINE_URL = os.getenv(
    "ENGINE_URL",
    "http://127.0.0.1:8001",
).strip()


# ==========================================================
# Identity Service
# ==========================================================

IDENTITY_URL = os.getenv(
    "IDENTITY_URL",
    "http://127.0.0.1:8000",
).strip()


# ==========================================================
# Identity Security
# ==========================================================

IDENTITY_ISSUER = os.getenv(
    "IDENTITY_ISSUER",
    "http://127.0.0.1:8000",
).strip()


IDENTITY_AUDIENCE = os.getenv(
    "IDENTITY_AUDIENCE",
    "nativeee",
).strip()


IDENTITY_PUBLIC_KEY = os.getenv(
    "IDENTITY_PUBLIC_KEY",
    "",
).strip()


IDENTITY_ALGORITHM = os.getenv(
    "IDENTITY_ALGORITHM",
    "RS256",
).strip()


# ==========================================================
# Supabase
# ==========================================================

SUPABASE_URL = os.getenv(
    "SUPABASE_URL",
    "",
).strip()


SUPABASE_PROJECT_REF = os.getenv(
    "SUPABASE_PROJECT_REF",
    "",
).strip()
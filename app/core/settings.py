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
# Nativeee Engine
# ==========================================================

ENGINE_URL = os.getenv(
    "ENGINE_URL",
    "http://127.0.0.1:8001",
).strip()


# ==========================================================
# JWT
# ==========================================================

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "",
).strip()

JWT_ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256",
).strip()

JWT_EXPIRE_MINUTES = int(
    os.getenv(
        "JWT_EXPIRE_MINUTES",
        "60",
    )
)

if not JWT_SECRET_KEY:
    raise RuntimeError(
        "JWT_SECRET_KEY is missing. Please set it in your environment variables."
    )
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    "",
).strip()

API_KEY = os.getenv(
    "API_KEY",
    "",
).strip()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "",
).strip()

# ✅ Ensure DATABASE_URL exists (fail fast on startup)
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing. Please set it in your environment variables.")

TRANSLATION_PROVIDER = os.getenv(
    "TRANSLATION_PROVIDER",
    "google",
).strip().lower()

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
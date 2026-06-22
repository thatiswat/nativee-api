from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(
    exist_ok=True
)

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

print(
    "Groq Key Loaded:",
    GROQ_API_KEY[:10] + "..."
    if GROQ_API_KEY
    else "NOT FOUND"
)
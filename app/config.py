from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Uploads folder
UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(
    exist_ok=True
)

# Groq API key
GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    ""
).strip()

# Debug
print(
    "Groq Key Loaded:",
    repr(GROQ_API_KEY)
)
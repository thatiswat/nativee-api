import time
from pathlib import Path

from groq import Groq
from fastapi import HTTPException

from app.config import GROQ_API_KEY


# ==========================================================
# Global Groq Client
# ==========================================================

client = Groq(
    api_key=GROQ_API_KEY,
)

MODEL = "whisper-large-v3"


# ==========================================================
# Speech To Text
# ==========================================================

async def speech_to_text(
    audio_path: str,
) -> str:
    """
    Convert speech to text using Groq Whisper.

    Args:
        audio_path: Path to audio file.

    Returns:
        Transcript string.
    """

    start = time.perf_counter()

    try:

        with open(audio_path, "rb") as audio_file:

            result = client.audio.transcriptions.create(
                model=MODEL,
                file=audio_file,
                response_format="json",
                temperature=0,
            )

        elapsed = time.perf_counter() - start

        print(f"🧠 Groq STT        : {elapsed:.3f}s")

        transcript = result.text.strip()

        if not transcript:
            raise HTTPException(
                status_code=400,
                detail="No speech detected.",
            )

        return transcript

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Speech recognition failed: {exc}",
        )
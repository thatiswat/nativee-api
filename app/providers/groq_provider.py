import time

from groq import Groq
from fastapi import HTTPException

from app.core.settings import GROQ_API_KEY
from app.core.logger import logger


client = Groq(api_key=GROQ_API_KEY)

MODEL = "whisper-large-v3"


async def speech_to_text(audio_path: str) -> str:
    """
    Convert speech to text using Groq Whisper.
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

        logger.info("Groq STT %.3fs", elapsed)

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
        logger.exception("Groq STT failed")

        raise HTTPException(
            status_code=500,
            detail=f"Speech recognition failed: {exc}",
        )
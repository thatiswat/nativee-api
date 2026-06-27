import time
import uuid
from pathlib import Path

import edge_tts
from fastapi import HTTPException

from app.config import UPLOAD_DIR


# ==========================================================
# Voice Mapping
# ==========================================================

VOICE_MAP = {
    "en": "en-IN-NeerjaNeural",
    "hi": "hi-IN-SwaraNeural",
    "kn": "kn-IN-SapnaNeural",
    "ta": "ta-IN-PallaviNeural",
    "te": "te-IN-ShrutiNeural",
    "ml": "ml-IN-SobhanaNeural",
}

DEFAULT_VOICE = "en-IN-NeerjaNeural"


# ==========================================================
# Text To Speech
# ==========================================================

async def text_to_speech(
    text: str,
    language: str,
) -> str:
    """
    Generate speech using Edge TTS.

    Returns
    -------
    Path to generated MP3.
    """

    start = time.perf_counter()

    voice = VOICE_MAP.get(
        language,
        DEFAULT_VOICE,
    )

    output_file = (
        UPLOAD_DIR /
        f"{uuid.uuid4().hex}.mp3"
    )

    try:

        communicate = edge_tts.Communicate(
            text=text.strip(),
            voice=voice,
        )

        await communicate.save(
            str(output_file)
        )

        elapsed = (
            time.perf_counter()
            - start
        )

        print(
            f"🔊 Edge TTS : {elapsed:.3f}s"
        )

        return str(output_file)

    except Exception as exc:

        if output_file.exists():
            output_file.unlink(
                missing_ok=True,
            )

        raise HTTPException(
            status_code=500,
            detail=f"TTS failed: {exc}",
        )
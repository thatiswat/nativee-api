import time
import uuid

import edge_tts
from fastapi import HTTPException

from app.core.settings import UPLOAD_DIR
from app.core.logger import logger


VOICE_MAP = {
    "en": "en-IN-NeerjaNeural",
    "hi": "hi-IN-SwaraNeural",
    "kn": "kn-IN-SapnaNeural",
    "ta": "ta-IN-PallaviNeural",
    "te": "te-IN-ShrutiNeural",
    "ml": "ml-IN-SobhanaNeural",
}

DEFAULT_VOICE = "en-IN-NeerjaNeural"


async def text_to_speech(
    text: str,
    language: str,
) -> str:

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

        await communicate.save(str(output_file))

        elapsed = time.perf_counter() - start

        logger.info("Edge TTS %.3fs", elapsed)

        return str(output_file)

    except Exception as exc:

        output_file.unlink(missing_ok=True)

        logger.exception("Edge TTS failed")

        raise HTTPException(
            status_code=500,
            detail=f"TTS failed: {exc}",
        )
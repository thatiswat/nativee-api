import time
import uuid

import edge_tts

from app.config import UPLOAD_DIR

VOICE_MAP = {
    "en": "en-IN-NeerjaNeural",
    "hi": "hi-IN-SwaraNeural",
    "kn": "kn-IN-SapnaNeural",
    "ta": "ta-IN-PallaviNeural",
    "te": "te-IN-ShrutiNeural",
    "ml": "ml-IN-SobhanaNeural",
}


async def text_to_speech(
    text: str,
    language: str,
):
    # Start TTS timer
    start = time.perf_counter()

    output_file = (
        UPLOAD_DIR /
        f"{uuid.uuid4()}.mp3"
    )

    voice = VOICE_MAP.get(
        language,
        "en-IN-NeerjaNeural",
    )

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
    )

    await communicate.save(
        str(output_file)
    )

    tts_only = time.perf_counter() - start

    print(f"🔊 edge-tts only : {tts_only:.3f}s")

    return str(output_file)
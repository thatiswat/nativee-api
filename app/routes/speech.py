from pathlib import Path
import shutil
import time

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
)

from app.services.stt import speech_to_text
from app.services.translator import translate_text
from app.services.tts import text_to_speech

from app.config import UPLOAD_DIR

router = APIRouter()


@router.post("/conversation")
async def conversation(
    audio: UploadFile = File(...),
    source_language: str = Form(...),
    target_language: str = Form(...),
):
    # Start total timer
    request_start = time.perf_counter()

    # Save uploaded audio
    save_start = time.perf_counter()

    audio_path = UPLOAD_DIR / audio.filename

    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    save_time = time.perf_counter() - save_start

    # Speech to Text
    stt_start = time.perf_counter()

    original = await speech_to_text(str(audio_path))

    stt_time = time.perf_counter() - stt_start

    # Translation
    translation_start = time.perf_counter()

    translated = await translate_text(
        original,
        source_language,
        target_language,
    )

    translation_time = time.perf_counter() - translation_start

    # Text to Speech
    tts_start = time.perf_counter()

    audio_output = await text_to_speech(
        translated,
        target_language,
    )

    tts_time = time.perf_counter() - tts_start

    # Total request time
    total_time = time.perf_counter() - request_start

    filename = Path(audio_output).name

    print("\n========== Nativeee Performance ==========")
    print(f"Save         : {save_time:.3f}s")
    print(f"STT          : {stt_time:.3f}s")
    print(f"Translation  : {translation_time:.3f}s")
    print(f"TTS          : {tts_time:.3f}s")
    print("------------------------------------------")
    print(f"TOTAL        : {total_time:.3f}s")
    print("==========================================\n")

    return {
        "original": original,
        "translated": translated,
        "audio_url": f"/audio/{filename}",
        "save_time": round(save_time, 3),
        "stt_time": round(stt_time, 3),
        "translation_time": round(translation_time, 3),
        "tts_time": round(tts_time, 3),
        "total_time": round(total_time, 3),
    }
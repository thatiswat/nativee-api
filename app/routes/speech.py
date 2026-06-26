from pathlib import Path
import os
import shutil
import time
import uuid

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
    # ==========================================
    # Nativeee Benchmark
    # ==========================================

    backend_start = time.perf_counter()

    # -------------------------
    # Save Upload
    # -------------------------
    save_start = time.perf_counter()

    extension = Path(audio.filename).suffix or ".m4a"
    audio_path = UPLOAD_DIR / f"{uuid.uuid4()}{extension}"

    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
        buffer.flush()

    save_time = time.perf_counter() - save_start

    # -------------------------
    # Speech To Text
    # -------------------------
    stt_start = time.perf_counter()

    try:
        original = await speech_to_text(str(audio_path))
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

    stt_time = time.perf_counter() - stt_start

    # -------------------------
    # Translation
    # -------------------------
    translation_start = time.perf_counter()

    translated = await translate_text(
        original,
        source_language,
        target_language,
    )

    translation_time = time.perf_counter() - translation_start

    # -------------------------
    # Text To Speech
    # -------------------------
    tts_start = time.perf_counter()

    audio_output = await text_to_speech(
        translated,
        target_language,
    )

    tts_time = time.perf_counter() - tts_start

    # -------------------------
    # Backend Total
    # -------------------------
    backend_total = time.perf_counter() - backend_start

    filename = os.path.basename(audio_output)

    print()
    print("=======================================================")
    print("              🚀 Nativeee Backend Benchmark")
    print("=======================================================")
    print(f"💾 Save Upload      : {save_time:.3f}s")
    print(f"🧠 Speech To Text   : {stt_time:.3f}s")
    print(f"🌍 Translation      : {translation_time:.3f}s")
    print(f"🔊 Text To Speech   : {tts_time:.3f}s")
    print("-------------------------------------------------------")
    print(f"⚙️ Backend Total    : {backend_total:.3f}s")
    print("=======================================================")
    print()

    return {
        "original": original,
        "translated": translated,
        "audio_url": f"/audio/{filename}",

        "metrics": {
            "save": round(save_time, 3),
            "stt": round(stt_time, 3),
            "translation": round(translation_time, 3),
            "tts": round(tts_time, 3),
            "backend_total": round(backend_total, 3),
        },
    }
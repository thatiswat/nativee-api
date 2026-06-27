from pathlib import Path
import os
import time
import uuid
from typing import Any

import aiofiles

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException,
    Request,
)

from app.config import UPLOAD_DIR

from app.services.stt import speech_to_text
from app.services.translator import translate_text
from app.services.tts import text_to_speech


router = APIRouter()


# ==========================================================
# Helpers
# ==========================================================

async def save_upload_file(
    upload: UploadFile,
    destination: Path,
) -> float:
    """
    Save uploaded audio asynchronously.

    Returns:
        Time taken in seconds.
    """

    start = time.perf_counter()

    async with aiofiles.open(destination, "wb") as out_file:
        while chunk := await upload.read(1024 * 1024):
            await out_file.write(chunk)

    return time.perf_counter() - start


def benchmark_line(title: str, value: float):
    print(f"{title:<22}: {value:.3f}s")


# ==========================================================
# Conversation
# ==========================================================

@router.post("/conversation")
async def conversation(
    request: Request,
    audio: UploadFile = File(...),
    source_language: str = Form(...),
    target_language: str = Form(...),
):
    request_id = request.state.id

    backend_start = time.perf_counter()

    extension = Path(audio.filename or "audio.m4a").suffix

    if not extension:
        extension = ".m4a"

    audio_path = UPLOAD_DIR / f"{uuid.uuid4()}{extension}"

    try:

        # --------------------------------------------------
        # Upload
        # --------------------------------------------------

        save_time = await save_upload_file(
            audio,
            audio_path,
        )

        # --------------------------------------------------
        # Speech To Text
        # --------------------------------------------------

        stt_start = time.perf_counter()

        original = await speech_to_text(
            str(audio_path)
        )

        stt_time = (
            time.perf_counter()
            - stt_start
        )

        # Remove uploaded recording immediately.
        audio_path.unlink(missing_ok=True)

        if not original:
            raise HTTPException(
                status_code=400,
                detail="Speech could not be recognized.",
            )

        # --------------------------------------------------
        # Translation
        # --------------------------------------------------

        translation_start = time.perf_counter()

        translated = await translate_text(
            original,
            source_language,
            target_language,
        )

        translation_time = (
            time.perf_counter()
            - translation_start
        )
                # --------------------------------------------------
        # Text To Speech
        # --------------------------------------------------

        tts_start = time.perf_counter()

        audio_output = await text_to_speech(
            translated,
            target_language,
        )

        tts_time = (
            time.perf_counter()
            - tts_start
        )

        backend_total = (
            time.perf_counter()
            - backend_start
        )

        filename = Path(audio_output).name

        # --------------------------------------------------
        # Benchmark
        # --------------------------------------------------

        print()
        print("=" * 70)
        print(f"🚀 Nativeee Backend Benchmark [{request_id}]")
        print("=" * 70)

        benchmark_line("Upload", save_time)
        benchmark_line("Speech To Text", stt_time)
        benchmark_line("Translation", translation_time)
        benchmark_line("Text To Speech", tts_time)

        print("-" * 70)

        benchmark_line("Backend Total", backend_total)

        print("=" * 70)
        print()

        return {
            "success": True,
            "request_id": request_id,

            "original": original,
            "translated": translated,

            "audio_url": f"/audio/{filename}",

            "metrics": {
                "upload": round(save_time, 3),
                "stt": round(stt_time, 3),
                "translation": round(
                    translation_time,
                    3,
                ),
                "tts": round(
                    tts_time,
                    3,
                ),
                "backend_total": round(
                    backend_total,
                    3,
                ),
            },
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Conversation failed: {str(exc)}",
        )

    finally:
        audio_path.unlink(missing_ok=True)
        await audio.close()
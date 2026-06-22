from pathlib import Path
import shutil
import time

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form
)

from app.services.stt import speech_to_text
from app.services.translate import translate_text
from app.services.tts import text_to_speech

from app.config import UPLOAD_DIR

router = APIRouter()


@router.post("/conversation")
async def conversation(
    audio: UploadFile = File(...),
    source_language: str = Form(...),
    target_language: str = Form(...)
):

    audio_path = (
        UPLOAD_DIR /
        audio.filename
    )

    with open(
        audio_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            audio.file,
            buffer
        )

    start = time.time()

    original = await speech_to_text(
        str(audio_path)
    )

    stt_time = round(
        time.time() - start,
        2
    )

    translation_start = time.time()

    translated = await translate_text(
        original,
        source_language,
        target_language
    )

    translation_time = round(
        time.time() - translation_start,
        2
    )

    tts_start = time.time()

    audio_output = await text_to_speech(
        translated,
        target_language
    )

    tts_time = round(
        time.time() - tts_start,
        2
    )

    filename = Path(
        audio_output
    ).name

    return {
        "original": original,
        "translated": translated,
        "audio_url": f"/audio/{filename}",
        "stt_time": stt_time,
        "translation_time": translation_time,
        "tts_time": tts_time
    }
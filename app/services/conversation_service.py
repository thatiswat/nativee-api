from pathlib import Path
import time
import uuid

import aiofiles
from fastapi import HTTPException

from app.core.logger import logger
from app.core.settings import UPLOAD_DIR
from app.providers.groq_provider import speech_to_text
from app.providers.edge_provider import text_to_speech
from app.router.translation_router import translate
from app.schemas.conversation import (
    ConversationMetrics,
    ConversationResult,
)


async def save_upload_file(
    upload,
    destination: Path,
) -> float:
    """
    Save uploaded audio asynchronously.
    """

    start = time.perf_counter()

    async with aiofiles.open(destination, "wb") as out_file:
        while chunk := await upload.read(1024 * 1024):
            await out_file.write(chunk)

    return time.perf_counter() - start


class ConversationService:
    async def process(
        self,
        audio,
        source_language: str,
        target_language: str,
    ) -> ConversationResult:
        """
        Process a complete conversation.

        Upload
        ↓
        Speech-to-Text
        ↓
        Translation
        ↓
        Text-to-Speech
        ↓
        Response
        """

        backend_start = time.perf_counter()

        extension = Path(audio.filename or "audio.m4a").suffix

        if not extension:
            extension = ".m4a"

        audio_path = UPLOAD_DIR / f"{uuid.uuid4()}{extension}"

        # ---------------------------------------
        # Upload
        # ---------------------------------------

        save_time = await save_upload_file(
            audio,
            audio_path,
        )

        # ---------------------------------------
        # Speech To Text
        # ---------------------------------------

        stt_start = time.perf_counter()

        original = await speech_to_text(
            str(audio_path)
        )

        stt_time = time.perf_counter() - stt_start

        audio_path.unlink(missing_ok=True)

        if not original:
            raise HTTPException(
                status_code=400,
                detail="Speech could not be recognized.",
            )

        logger.info(
            "STT completed in %.3fs",
            stt_time,
        )

        # ---------------------------------------
        # Translation
        # ---------------------------------------

        translation_start = time.perf_counter()

        translated = await translate(
            original,
            source_language,
            target_language,
        )

        translation_time = (
            time.perf_counter()
            - translation_start
        )

        logger.info(
            "Translation completed in %.3fs",
            translation_time,
        )

        # ---------------------------------------
        # Text To Speech
        # ---------------------------------------

        tts_start = time.perf_counter()

        audio_output = await text_to_speech(
            translated,
            target_language,
        )

        tts_time = (
            time.perf_counter()
            - tts_start
        )

        logger.info(
            "TTS completed in %.3fs",
            tts_time,
        )

        backend_total = (
            time.perf_counter()
            - backend_start
        )

        filename = Path(audio_output).name

        return ConversationResult(
            success=True,
            # Will be provided by the route in the next step.
            request_id="",
            original=original,
            translated=translated,
            audio_url=f"/audio/{filename}",
            metrics=ConversationMetrics(
                upload=round(save_time, 3),
                stt=round(stt_time, 3),
                translation=round(translation_time, 3),
                tts=round(tts_time, 3),
                backend_total=round(backend_total, 3),
            ),
        )
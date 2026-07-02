from pathlib import Path
import time
import uuid

import aiofiles
from fastapi import HTTPException

from app.core.logger import logger
from app.core.settings import UPLOAD_DIR
from app.pipelines.conversation_pipeline import (
    ConversationPipeline,
)
from app.schemas.conversation import (
    ConversationMetrics,
    ConversationResult,
)
from app.services.usage_service import UsageService

pipeline = ConversationPipeline()


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
        db,
        api_key,
        request_id: str,
        audio,
        source_language: str,
        target_language: str,
    ) -> ConversationResult:
        """
        Process a complete conversation.

        Upload
        ↓
        Conversation Pipeline
        ↓
        Usage Logging
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
        # Conversation Pipeline
        # ---------------------------------------

        result = await pipeline.run(
            audio_path=str(audio_path),
            source_language=source_language,
            target_language=target_language,
        )

        audio_path.unlink(missing_ok=True)

        if not result["original"]:
            raise HTTPException(
                status_code=400,
                detail="Speech could not be recognized.",
            )

        logger.info(
            "Pipeline completed in %.3fs",
            result["pipeline_total"],
        )

        backend_total = (
            time.perf_counter()
            - backend_start
        )

        # ---------------------------------------
        # Usage Logging
        # ---------------------------------------

        UsageService(db).log(
            api_key=api_key,
            endpoint="/conversation",
            provider=result.get("provider", "unknown"),
            latency_ms=backend_total * 1000,
            success=True,
        )

        filename = Path(
            result["audio_output"]
        ).name

        return ConversationResult(
            success=True,
            request_id=request_id,
            original=result["original"],
            translated=result["translated"],
            audio_url=f"/audio/{filename}",
            metrics=ConversationMetrics(
                upload=round(save_time, 3),
                stt=round(result["stt"], 3),
                translation=round(result["translation"], 3),
                tts=round(result["tts"], 3),
                backend_total=round(backend_total, 3),
            ),
        )
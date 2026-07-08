import time

from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from app.core.logger import logger
from app.engine import engine
from app.schemas.platform.conversation import (
    ConversationMetrics,
    ConversationResult,
)
from app.services.platform.usage import UsageService


class ConversationService:

    def __init__(
        self,
        db,
    ):
        self.db = db
        self.engine = engine
        self.usage = UsageService(db)

    async def process(
        self,
        api_key,
        request_id: str,
        audio,
        source_language: str,
        target_language: str,
    ) -> ConversationResult:

        overall_start = time.perf_counter()

        # ---------------------------------------
        # Nativeee Engine
        # ---------------------------------------

        engine_start = time.perf_counter()

        result = await self.engine.conversation(
            audio=audio,
            source_language=source_language,
            target_language=target_language,
        )

        engine_elapsed = (
            time.perf_counter()
            - engine_start
        )

        logger.info(
            "Engine response: %s",
            result,
        )

        if not result.get("original"):
            raise HTTPException(
                status_code=400,
                detail="Speech could not be recognized.",
            )

        profiling = result.get(
            "profiling",
            {},
        )

        engine_latency = (
            profiling.get(
                "engine",
                {},
            ).get(
                "latency_ms",
                0,
            )
        )

        logger.info(
            "Engine completed in %.2f ms",
            engine_latency,
        )

        # ---------------------------------------
        # Usage Tracking
        # ---------------------------------------

        usage_start = time.perf_counter()

        self.usage.log(
            api_key=api_key,
            endpoint="/conversation",
            provider=result.get(
                "provider",
                "unknown",
            ),
            latency_ms=(
                time.perf_counter()
                - overall_start
            ) * 1000,
            success=True,
        )

        usage_elapsed = (
            time.perf_counter()
            - usage_start
        )

        # ---------------------------------------
        # Backend Total
        # ---------------------------------------

        backend_total = (
            time.perf_counter()
            - overall_start
        )

        logger.info(
            """
==============================
Nativeee API Profiler
==============================
Engine : %.3fs
Usage  : %.3fs
Total  : %.3fs
==============================
""",
            engine_elapsed,
            usage_elapsed,
            backend_total,
        )

        # ---------------------------------------
        # Metrics
        # ---------------------------------------

        return ConversationResult(
            success=True,
            request_id=request_id,
            original=result.get(
                "original",
                "",
            ),
            translated=result.get(
                "translated",
                "",
            ),
            audio_url=result.get(
                "audio_url",
                "",
            ),
            metrics=ConversationMetrics(
                upload=profiling.get(
                    "input",
                    {},
                ).get(
                    "latency_ms",
                    0,
                ),
                stt=profiling.get(
                    "speech",
                    {},
                ).get(
                    "latency_ms",
                    0,
                ),
                translation=profiling.get(
                    "translation",
                    {},
                ).get(
                    "latency_ms",
                    0,
                ),
                tts=profiling.get(
                    "voice",
                    {},
                ).get(
                    "latency_ms",
                    0,
                ),
                backend_total=round(
                    backend_total * 1000,
                    2,
                ),
            ),
        )

    async def process_stream(
        self,
        api_key,
        audio,
        source_language: str,
        target_language: str,
    ):
        """
        Stream translated speech from Nativeee Engine.
        """

        response = await self.engine.conversation_stream(
            audio=audio,
            source_language=source_language,
            target_language=target_language,
        )

        async def iterator():

            try:

                async for chunk in response.aiter_bytes():

                    yield chunk

            finally:

                await response.aclose()

        return StreamingResponse(
            iterator(),
            media_type="audio/mpeg",
        )
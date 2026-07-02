import time

from app.providers.edge_provider import text_to_speech
from app.providers.groq_provider import speech_to_text
from app.providers.registry import ProviderRegistry


class ConversationPipeline:

    async def run(
        self,
        audio_path: str,
        source_language: str,
        target_language: str,
    ):
        pipeline_start = time.perf_counter()

        # ---------------------------------------
        # Speech-to-Text (STT)
        # ---------------------------------------

        stt_start = time.perf_counter()

        original = await speech_to_text(
            audio_path,
        )

        stt_time = (
            time.perf_counter()
            - stt_start
        )

        # ---------------------------------------
        # Translation
        # ---------------------------------------

        translation_start = time.perf_counter()

        translated = await ProviderRegistry.translate(
            original,
            source_language,
            target_language,
        )

        translation_time = (
            time.perf_counter()
            - translation_start
        )

        provider = ProviderRegistry.current_provider()

        # ---------------------------------------
        # Text-to-Speech (TTS)
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

        # ---------------------------------------
        # Total Pipeline Time
        # ---------------------------------------

        pipeline_total = (
            time.perf_counter()
            - pipeline_start
        )

        return {
            "original": original,
            "translated": translated,
            "audio_output": audio_output,
            "provider": provider,
            "stt": stt_time,
            "translation": translation_time,
            "tts": tts_time,
            "pipeline_total": pipeline_total,
        }
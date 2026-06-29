import time
from functools import lru_cache

from fastapi import HTTPException
from deep_translator import GoogleTranslator


# ==========================================================
# Config
# ==========================================================

SOURCE_LANGUAGE = "auto"


# ==========================================================
# Internal Cached Translator
# ==========================================================

@lru_cache(maxsize=2048)
def _cached_translate(
    text: str,
    target_language: str,
) -> str:
    """
    Cached Google translation call.
    """

    return GoogleTranslator(
        source=SOURCE_LANGUAGE,
        target=target_language,
    ).translate(text)


# ==========================================================
# Provider (PLATFORM STYLE)
# ==========================================================

class GoogleProvider:
    """
    Google Translation Provider

    Wrapped as a class so it can be registered
    inside ProviderRegistry.
    """

    async def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> str:

        start = time.perf_counter()

        try:
            translated = _cached_translate(
                text.strip(),
                target_language,
            )

            elapsed = time.perf_counter() - start

            print(f"🌍 Translation : {elapsed:.3f}s")

            return translated

        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Translation failed: {exc}",
            )
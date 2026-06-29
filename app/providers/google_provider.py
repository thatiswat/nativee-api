import time
from functools import lru_cache

from fastapi import HTTPException
from deep_translator import GoogleTranslator


# ==========================================================
# Translator
# ==========================================================

SOURCE_LANGUAGE = "auto"


# ==========================================================
# Translation Cache
# ==========================================================

@lru_cache(maxsize=2048)
def cached_translate(
    text: str,
    target_language: str,
) -> str:

    return GoogleTranslator(
        source=SOURCE_LANGUAGE,
        target=target_language,
    ).translate(text)


# ==========================================================
# Translation
# ==========================================================

async def translate_text(
    text: str,
    source_language: str,
    target_language: str,
) -> str:
    """
    Translate text.

    Args:
        text:
            Original text.

        source_language:
            Reserved for future models
            (IndicTrans / NLLB / AI4Bharat)

        target_language:
            Target language.

    Returns
    -------
        Translated text.
    """

    start = time.perf_counter()

    try:

        translated = cached_translate(
            text.strip(),
            target_language,
        )

        elapsed = time.perf_counter() - start

        print(
            f"🌍 Translation : {elapsed:.3f}s"
        )

        return translated

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {exc}",
        )
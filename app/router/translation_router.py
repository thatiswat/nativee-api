from app.core.settings import TRANSLATION_PROVIDER

from app.providers.google_provider import (
    translate_text as google_translate,
)

# Future
# from app.providers.indic_provider import (
#     translate_text as indic_translate,
# )


async def translate(
    text: str,
    source_language: str,
    target_language: str,
):
    """
    Route translation requests to the configured provider.
    """

    provider = TRANSLATION_PROVIDER

    if provider == "google":
        return await google_translate(
            text=text,
            source_language=source_language,
            target_language=target_language,
        )

    # Future GPU
    # elif provider == "indic":
    #     return await indic_translate(
    #         text=text,
    #         source_language=source_language,
    #         target_language=target_language,
    #     )

    raise RuntimeError(
        f"Unsupported translation provider: {provider}"
    )
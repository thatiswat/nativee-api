from app.core.settings import TRANSLATION_PROVIDER

from app.providers.google_provider import (
    translate_text,
)


class ProviderRegistry:

    @staticmethod
    def current_provider():
        """
        Return the currently configured translation provider.
        """
        return TRANSLATION_PROVIDER

    @staticmethod
    async def translate(
        text: str,
        source_language: str,
        target_language: str,
    ):

        if TRANSLATION_PROVIDER == "google":

            return await translate_text(
                text,
                source_language,
                target_language,
            )

        raise RuntimeError(
            "Unknown Translation Provider"
        )
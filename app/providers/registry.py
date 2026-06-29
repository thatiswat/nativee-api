from app.core.settings import TRANSLATION_PROVIDER

from app.providers.google_provider import GoogleProvider


class ProviderRegistry:
    """
    Central registry for translation providers.

    Register new providers here without changing the
    translation flow elsewhere in the application.
    """

    PROVIDERS = {
        "google": GoogleProvider(),
        # "ai4bharat": AI4BharatProvider(),
        # "nativeee": NativeeeGPUProvider(),
    }

    @classmethod
    def current_provider(cls) -> str:
        """
        Return the configured translation provider.
        """
        return TRANSLATION_PROVIDER

    @classmethod
    def get_provider(cls):
        """
        Return the configured provider instance.
        """
        provider = cls.PROVIDERS.get(TRANSLATION_PROVIDER)

        if provider is None:
            raise RuntimeError(
                f"Unknown translation provider: {TRANSLATION_PROVIDER}"
            )

        return provider

    @classmethod
    async def translate(
        cls,
        text: str,
        source_language: str,
        target_language: str,
    ):
        """
        Translate text using the configured provider.
        """
        provider = cls.get_provider()

        return await provider.translate(
            text=text,
            source_language=source_language,
            target_language=target_language,
        )
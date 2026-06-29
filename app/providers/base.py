from abc import ABC
from abc import abstractmethod


class TranslationProvider(ABC):

    @abstractmethod
    async def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ):
        pass
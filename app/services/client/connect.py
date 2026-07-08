from sqlalchemy.orm import Session

from app.services.platform.conversation import (
    ConversationService,
)


class MobileConnectService:

    def __init__(self):
        self.conversation = ConversationService()

    async def translate(
        self,
        db: Session,
        user,
        audio,
        source_language: str,
        target_language: str,
    ):
        """
        One-shot speech translation.
        """

        return await self.conversation.process(
            db=db,
            api_key=None,
            request_id=f"mobile-{user.id}",
            audio=audio,
            source_language=source_language,
            target_language=target_language,
        )

    async def stream(
        self,
        db: Session,
        user,
        audio,
        source_language: str,
        target_language: str,
    ):
        """
        Stream translated speech.
        """

        return await self.conversation.process_stream(
            db=db,
            api_key=None,
            audio=audio,
            source_language=source_language,
            target_language=target_language,
        )
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Request,
)

from app.services.conversation_service import ConversationService

router = APIRouter()

conversation_service = ConversationService()


# ==========================================================
# Conversation
# ==========================================================

@router.post("/conversation")
async def conversation(
    request: Request,
    audio: UploadFile = File(...),
    source_language: str = Form(...),
    target_language: str = Form(...),
):
    request_id = request.state.id

    return await conversation_service.process(
        request_id=request_id,
        audio=audio,
        source_language=source_language,
        target_language=target_language,
    )


# ==========================================================
# Previous implementation (kept temporarily for reference)
# Remove after verifying the new service returns identical
# responses and the mobile app works correctly.
# ==========================================================

"""
The previous implementation has been intentionally commented out
during the refactor.

It previously handled:

- Upload
- Speech-to-Text
- Translation
- Text-to-Speech
- Benchmarking
- Response formatting
- Cleanup

Those responsibilities now live in:

    app.services.conversation_service.ConversationService

After verifying:

- /conversation
- /translate
- Mobile app

you can safely delete the old implementation.
"""
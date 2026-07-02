from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Request,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.api_key import require_api_key
from app.schemas.conversation import ConversationResult
from app.schemas.error import ErrorResponse
from app.services.conversation_service import ConversationService

router = APIRouter(
    tags=["Speech"],
)

conversation_service = ConversationService()


# ==========================================================
# Speech Conversation
# ==========================================================

@router.post(
    "/conversation",
    response_model=ConversationResult,
    summary="Speech Conversation",
    description="""
Convert speech into another language.

Pipeline

Speech → Text

↓

Translation

↓

Text → Speech

Returns:

- Original transcript
- Translated text
- Generated audio URL
- Processing performance metrics
""",
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Invalid audio or speech not detected",
        },
        401: {
            "model": ErrorResponse,
            "description": "Unauthorized",
        },
        403: {
            "model": ErrorResponse,
            "description": "API key disabled",
        },
        429: {
            "model": ErrorResponse,
            "description": "Rate limit or monthly quota exceeded",
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error",
        },
    },
)
async def conversation(
    request: Request,
    api_key=Depends(require_api_key),
    db: Session = Depends(get_db),
    audio: UploadFile = File(...),
    source_language: str = Form(...),
    target_language: str = Form(...),
):
    """
    Process a multilingual speech conversation.

    Accepts an audio file, performs speech recognition,
    translates the transcript, synthesizes translated
    speech, and returns the complete conversation result.
    """

    return await conversation_service.process(
        db=db,
        api_key=api_key,
        request_id=request.state.id,
        audio=audio,
        source_language=source_language,
        target_language=target_language,
    )
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Request,
    UploadFile,
)
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import require_api_key
from app.schemas.conversation import ConversationResult
from app.schemas.error import ErrorResponse
from app.services.conversation_service import ConversationService


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
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

Authentication:

Authorization: Bearer ntv_live_xxxxxxxxx

Pipeline:

Speech
↓
Text Recognition
↓
Translation
↓
Text To Speech

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
            "description": "Invalid or missing API key",
        },
        403: {
            "model": ErrorResponse,
            "description": "API key disabled",
        },
        429: {
            "model": ErrorResponse,
            "description": "Rate limit or quota exceeded",
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
    Process multilingual speech conversion.

    Uses API Key authentication.
    """

    return await conversation_service.process(
        db=db,
        api_key=api_key,
        request_id=request.state.id,
        audio=audio,
        source_language=source_language,
        target_language=target_language,
    )


# ==========================================================
# Streaming Speech Conversation
# ==========================================================

@router.post(
    "/conversation/stream",
    response_class=StreamingResponse,
    summary="Streaming Speech Conversation",
    description="""
Real-time multilingual speech translation.

Returns translated audio as a streaming MP3 directly from
Nativeee Engine.
""",
)
async def conversation_stream(
    api_key=Depends(require_api_key),
    db: Session = Depends(get_db),
    audio: UploadFile = File(...),
    source_language: str = Form(...),
    target_language: str = Form(...),
):
    return await conversation_service.process_stream(
        db=db,
        api_key=api_key,
        audio=audio,
        source_language=source_language,
        target_language=target_language,
    )
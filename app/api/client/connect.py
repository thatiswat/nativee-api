from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
)
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.services.client.connect import (
    MobileConnectService,
)


router = APIRouter(
    prefix="/connect",
    tags=["Mobile Connect"],
)


# ==========================================================
# One-shot Speech Translation
# ==========================================================

@router.post("/translate")
async def translate(
    audio: UploadFile = File(...),
    source_language: str = Form(...),
    target_language: str = Form(...),

    user: User = Depends(
        get_current_user,
    ),

    db: Session = Depends(
        get_db,
    ),
):
    """
    One-shot speech translation.
    """

    service = MobileConnectService()

    return await service.translate(
        db=db,
        user=user,
        audio=audio,
        source_language=source_language,
        target_language=target_language,
    )


# ==========================================================
# Streaming Speech Translation
# ==========================================================

@router.post(
    "/stream",
    response_class=StreamingResponse,
)
async def stream(
    audio: UploadFile = File(...),
    source_language: str = Form(...),
    target_language: str = Form(...),

    user: User = Depends(
        get_current_user,
    ),

    db: Session = Depends(
        get_db,
    ),
):
    """
    Stream translated speech.
    """

    service = MobileConnectService()

    return await service.stream(
        db=db,
        user=user,
        audio=audio,
        source_language=source_language,
        target_language=target_language,
    )
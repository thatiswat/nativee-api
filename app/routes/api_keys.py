from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.api_key import (
    CreateAPIKeyRequest,
    CreateAPIKeyResponse,
)
from app.services.api_key_service import APIKeyService

router = APIRouter(
    prefix="/api-keys",
    tags=["API Keys"],
)

service = APIKeyService()


@router.post(
    "",
    response_model=CreateAPIKeyResponse,
)
def create_key(
    request: CreateAPIKeyRequest,
    db: Session = Depends(get_db),
):
    return service.create_key(
        db=db,
        name=request.name,
        live=request.live,
        plan_id=request.plan_id,  # ✅ added
    )
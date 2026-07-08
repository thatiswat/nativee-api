from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.platform.api_key import (
    APIKeyListResponse,
    CreateAPIKeyRequest,
    CreateAPIKeyResponse,
    MessageResponse,
    RotateAPIKeyResponse,
)
from app.schemas.platform.error import ErrorResponse
from app.services.platform.apikeys import APIKeyService

router = APIRouter(
    prefix="/api-keys",
    tags=["API Keys"],
)

service = APIKeyService()


# ==========================================================
# Create API Key
# ==========================================================

@router.post(
    "",
    response_model=CreateAPIKeyResponse,
    summary="Create API Key",
    description="""
Creates a new Nativeee API Key.

The plaintext API key is returned only once.
Store it securely because it cannot be retrieved again.
""",
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Plan or Project not found",
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error",
        },
    },
)
def create_key(
    request: CreateAPIKeyRequest,
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    return service.create_key(
        db=db,
        user_id=current_user.id,
        name=request.name,
        live=request.live,
        project_id=request.project_id,
        plan_id=request.plan_id,
    )


# ==========================================================
# List API Keys
# ==========================================================

@router.get(
    "",
    response_model=APIKeyListResponse,
    summary="List API Keys",
    description="""
Returns all API Keys owned by the authenticated user.

Each API Key includes its status and assigned plan.
""",
    responses={
        500: {
            "model": ErrorResponse,
            "description": "Internal server error",
        },
    },
)
def get_api_keys(
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    keys = service.get_all_keys(
        db,
        current_user.id,
    )

    return {
        "api_keys": [
            {
                "id": key.id,
                "name": key.name,
                "active": key.active,
                "plan": key.plan.name,
            }
            for key in keys
        ]
    }


# ==========================================================
# Disable API Key
# ==========================================================

@router.patch(
    "/{api_key_id}/disable",
    response_model=MessageResponse,
    summary="Disable API Key",
    description="""
Disables an API Key.

Disabled keys can no longer authenticate requests.
""",
    responses={
        404: {
            "model": ErrorResponse,
            "description": "API Key not found",
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error",
        },
    },
)
def disable_api_key(
    api_key_id: int,
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    service.disable_key(
        db,
        current_user.id,
        api_key_id,
    )

    return {
        "success": True,
        "message": "API Key disabled",
    }


# ==========================================================
# Enable API Key
# ==========================================================

@router.patch(
    "/{api_key_id}/enable",
    response_model=MessageResponse,
    summary="Enable API Key",
    description="""
Re-enables a previously disabled API Key.
""",
    responses={
        404: {
            "model": ErrorResponse,
            "description": "API Key not found",
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error",
        },
    },
)
def enable_api_key(
    api_key_id: int,
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    service.enable_key(
        db,
        current_user.id,
        api_key_id,
    )

    return {
        "success": True,
        "message": "API Key enabled",
    }


# ==========================================================
# Rotate API Key
# ==========================================================

@router.post(
    "/{api_key_id}/rotate",
    response_model=RotateAPIKeyResponse,
    summary="Rotate API Key",
    description="""
Generates a new API Key and invalidates the previous one.

The new plaintext API Key is returned only once.
Store it securely.
""",
    responses={
        404: {
            "model": ErrorResponse,
            "description": "API Key not found",
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error",
        },
    },
)
def rotate_api_key(
    api_key_id: int,
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    return service.rotate_key(
        db,
        current_user.id,
        api_key_id,
    )


# ==========================================================
# Delete API Key
# ==========================================================

@router.delete(
    "/{api_key_id}",
    response_model=MessageResponse,
    summary="Delete API Key",
    description="""
Permanently deletes an API Key.

This action cannot be undone.
""",
    responses={
        404: {
            "model": ErrorResponse,
            "description": "API Key not found",
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error",
        },
    },
)
def delete_api_key(
    api_key_id: int,
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    return service.delete_key(
        db,
        current_user.id,
        api_key_id,
    )
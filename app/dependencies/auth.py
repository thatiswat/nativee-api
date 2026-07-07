from fastapi import (
    Depends,
    HTTPException,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database.dependencies import get_db
from app.repositories.api_key_repository import APIKeyRepository
from app.repositories.user_repository import UserRepository
from app.utils.crypto import hash_api_key


# ==========================================================
# Separate Security Schemes
# ==========================================================

# Customer Console Authentication
# Used with:
# Authorization: Bearer <JWT>

jwt_security = HTTPBearer(
    scheme_name="CustomerJWT",
    auto_error=False,
)


# Developer API Authentication
# Used with:
# Authorization: Bearer ntv_live_xxxxxxxxx

api_key_security = HTTPBearer(
    scheme_name="APIKeyAuth",
    auto_error=False,
)


# ==========================================================
# API KEY AUTH
# Developer / Service Authentication
# ==========================================================

async def require_api_key(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        api_key_security,
    ),
    db: Session = Depends(get_db),
):
    """
    Authenticate requests using a Nativee API Key.

    Expected header:

        Authorization: Bearer ntv_live_xxxxxxxxx

    Used by:

        /v1/ai/*
    """

    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
        )

    api_key = credentials.credentials

    key_hash = hash_api_key(
        api_key,
    )

    repository = APIKeyRepository(
        db,
    )

    record = repository.get_by_hash(
        key_hash,
    )

    if record is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key",
        )

    if not record.active:
        raise HTTPException(
            status_code=403,
            detail="API Key Disabled",
        )

    return record


# ==========================================================
# JWT AUTH
# Customer Authentication
# ==========================================================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        jwt_security,
    ),
    db: Session = Depends(get_db),
):
    """
    Authenticate customer requests using JWT.

    Expected header:

        Authorization: Bearer <jwt_token>

    Used by:

        /v1/customer/*
    """

    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
        )

    token = credentials.credentials

    payload = decode_access_token(
        token,
    )

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    user_id = payload.get(
        "sub",
    )

    if user_id is None or not str(user_id).isdigit():
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    repository = UserRepository(
        db,
    )

    user = repository.get_by_id(
        int(user_id),
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User disabled",
        )

    return user
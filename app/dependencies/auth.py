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


security = HTTPBearer()


# ==========================================================
# API KEY AUTH (Developer / Service Auth)
# ==========================================================
async def require_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Authenticate requests using a Bearer API key.

    Expected header:
        Authorization: Bearer <api_key>
    """

    api_key = credentials.credentials

    key_hash = hash_api_key(api_key)

    repository = APIKeyRepository(db)
    record = repository.get_by_hash(key_hash)

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
# JWT AUTH (User Auth)
# ==========================================================
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Authenticate requests using JWT Bearer token.

    Expected header:
        Authorization: Bearer <jwt_token>
    """

    print("AUTH HEADER:", credentials)

    token = credentials.credentials

    print("TOKEN:", token)

    try:
        payload = decode_access_token(token)
        print("PAYLOAD:", payload)
    except Exception as e:
        print("JWT ERROR:", repr(e))
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    user_id = payload.get("sub")
    print("USER ID:", user_id)

    if user_id is None or not str(user_id).isdigit():
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    repository = UserRepository(db)

    user = repository.get_by_id(
        int(user_id),
    )

    print("USER:", user)

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
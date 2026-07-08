from fastapi import (
    Depends,
    HTTPException,
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from sqlalchemy.orm import Session

from app.database.dependencies import (
    get_db,
)

from app.repositories.api_key_repository import (
    APIKeyRepository,
)

from app.utils.crypto import (
    hash_api_key,
)

from app.core.identity import (
    verify_access_token,
)

from app.schemas.shared.identity import (
    IdentityClaims,
)


# ==========================================================
# Security Schemes
# ==========================================================

# Customer Authentication
# Authorization: Bearer <JWT>

jwt_security = HTTPBearer(
    scheme_name="CustomerJWT",
    auto_error=False,
)


# Developer API Authentication
# Authorization: Bearer ntv_live_xxxxxxxxx

api_key_security = HTTPBearer(
    scheme_name="APIKeyAuth",
    auto_error=False,
)


# ==========================================================
# API KEY AUTH
# ==========================================================

async def require_api_key(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        api_key_security,
    ),
    db: Session = Depends(
        get_db,
    ),
):
    """
    Authenticate requests using Nativee API Key.
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
# ==========================================================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        jwt_security,
    ),
):
    """
    Authenticate customer requests using Identity JWT.
    """

    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
        )

    try:

        payload = verify_access_token(
            credentials.credentials,
        )

        return IdentityClaims(
            id=int(
                payload["sub"],
            ),
            public_id=payload["pid"],
            email=payload["email"],
            name=payload["name"],
            role=payload["role"],
            session_id=payload["sid"],
            is_active=payload["is_active"],
        )

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )
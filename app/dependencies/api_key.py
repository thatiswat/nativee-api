from fastapi import (
    Depends,
    HTTPException,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.api_key_repository import APIKeyRepository
from app.utils.crypto import hash_api_key


security = HTTPBearer()


async def require_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(
        security,
    ),
    db: Session = Depends(get_db),
):
    """
    Authenticate requests using a Bearer API Key.

    Expected header:

        Authorization: Bearer ntv_live_xxxxxxxxxxxxx
    """

    api_key = credentials.credentials

    key_hash = hash_api_key(api_key)

    repository = APIKeyRepository(db)

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
            detail="API Key disabled",
        )

    return record
from fastapi import (
    Depends,
    Header,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.api_key_repository import APIKeyRepository
from app.utils.crypto import hash_api_key


async def require_api_key(
    authorization: str = Header(None),
    db: Session = Depends(get_db),
):
    """
    Authenticate requests using a Bearer API key.

    Expected header:

        Authorization: Bearer <api_key>
    """

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization header",
        )

    api_key = authorization.replace(
        "Bearer ",
        "",
        1,
    )

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
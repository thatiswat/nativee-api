from fastapi import HTTPException

from app.repositories.api_key_repository import APIKeyRepository
from app.utils.crypto import hash_api_key


class APIKeyAuthService:
    """
    Handles API Key authentication.

    Responsibilities:
    - Validate Authorization header
    - Authenticate API Key
    - Verify active status
    """

    def __init__(self, db):
        self.repository = APIKeyRepository(db)

    def authenticate(
        self,
        authorization: str | None,
    ):
        # ---------------------------------------
        # Authorization Header
        # ---------------------------------------

        if not authorization:
            raise HTTPException(
                status_code=401,
                detail="Missing Authorization Header",
            )

        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Invalid Authorization Header",
            )

        api_key = authorization.replace(
            "Bearer ",
            "",
        ).strip()

        # ---------------------------------------
        # Lookup
        # ---------------------------------------

        record = self.repository.get_by_hash(
            hash_api_key(api_key)
        )

        if not record:
            raise HTTPException(
                status_code=401,
                detail="Invalid API Key",
            )

        # ---------------------------------------
        # Active Check
        # ---------------------------------------

        if not record.active:
            raise HTTPException(
                status_code=403,
                detail="API Key Disabled",
            )

        return record
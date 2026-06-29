from app.core.security import (
    generate_api_key,
    hash_api_key,
)

from app.models.api_key import APIKey
from app.repositories.api_key_repository import APIKeyRepository
from app.schemas.api_key import CreateAPIKeyResponse


class APIKeyService:

    def create_key(
        self,
        db,
        name: str,
        live: bool = True,
    ):
        """
        Create a Nativeee API Key.

        The plaintext key is returned only once.
        Only the SHA256 hash is stored in the database.
        """

        # 1. Generate plaintext API key
        api_key = generate_api_key(
            live=live,
        )

        # 2. Hash it
        key_hash = hash_api_key(
            api_key,
        )

        # 3. Create model instance (not yet persisted)
        record = APIKey(
            name=name,
            key_hash=key_hash,
            active=True,
        )

        # 4. Persist using repository layer
        record = APIKeyRepository.create(
            db,
            record,
        )

        # 5. Return the response schema
        return CreateAPIKeyResponse(
            id=record.id,
            name=record.name,
            api_key=api_key,
        )
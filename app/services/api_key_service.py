from fastapi import HTTPException

from app.utils.crypto import (
    generate_api_key,
    hash_api_key,
)

from app.models.api_key import APIKey
from app.repositories.api_key_repository import APIKeyRepository
from app.repositories.plan_repository import PlanRepository
from app.schemas.api_key import CreateAPIKeyResponse


class APIKeyService:

    def create_key(
        self,
        db,
        name: str,
        live: bool = True,
        plan_id: int = 1,
    ):
        """
        Create a Nativeee API Key.

        - Validates plan
        - Generates API key (returned only once)
        - Stores only hashed version
        """

        # ---------------------------------------
        # 1. Validate plan exists (business rule)
        # ---------------------------------------
        plan_repo = PlanRepository(db)
        plan = plan_repo.get(plan_id)

        if not plan:
            raise HTTPException(
                status_code=404,
                detail="Plan not found",
            )

        # ---------------------------------------
        # 2. Generate API key
        # ---------------------------------------
        api_key = generate_api_key(live=live)

        # ---------------------------------------
        # 3. Hash API key
        # ---------------------------------------
        key_hash = hash_api_key(api_key)

        # ---------------------------------------
        # 4. Create model
        # ---------------------------------------
        record = APIKey(
            name=name,
            key_hash=key_hash,
            active=True,
            plan_id=plan_id,
        )

        # ---------------------------------------
        # 5. Persist (repository instance)
        # ---------------------------------------
        repository = APIKeyRepository(db)
        record = repository.create(record)

        # ---------------------------------------
        # 6. Response
        # ---------------------------------------
        return CreateAPIKeyResponse(
            id=record.id,
            name=record.name,
            api_key=api_key,
        )
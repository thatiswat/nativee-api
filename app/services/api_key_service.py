from fastapi import HTTPException

from app.models.api_key import APIKey
from app.repositories.api_key_repository import APIKeyRepository
from app.repositories.plan_repository import PlanRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.api_key import CreateAPIKeyResponse
from app.utils.crypto import (
    generate_api_key,
    hash_api_key,
)


class APIKeyService:
    # ---------------------------------------
    # Create API Key
    # ---------------------------------------

    def create_key(
        self,
        db,
        user_id: int,
        name: str,
        live: bool = True,
        project_id: int = 1,
        plan_id: int = 1,
    ):
        """
        Create a Nativeee API Key.

        - Validates project ownership
        - Validates plan
        - Generates API key (returned only once)
        - Stores only hashed version
        """

        # ---------------------------------------
        # 1. Validate project belongs to user
        # ---------------------------------------
        project_repo = ProjectRepository(db)

        project = project_repo.get_owned(
            user_id,
            project_id,
        )

        if not project:
            raise HTTPException(
                status_code=404,
                detail="Project not found",
            )

        # ---------------------------------------
        # 2. Validate plan exists
        # ---------------------------------------
        plan_repo = PlanRepository(db)

        plan = plan_repo.get(plan_id)

        if not plan:
            raise HTTPException(
                status_code=404,
                detail="Plan not found",
            )

        # ---------------------------------------
        # 3. Generate API key
        # ---------------------------------------
        api_key = generate_api_key(
            live=live,
        )

        # ---------------------------------------
        # 4. Hash API key
        # ---------------------------------------
        key_hash = hash_api_key(
            api_key,
        )

        # ---------------------------------------
        # 5. Create model
        # ---------------------------------------
        record = APIKey(
            name=name,
            key_hash=key_hash,
            active=True,
            project_id=project_id,
            plan_id=plan_id,
        )

        # ---------------------------------------
        # 6. Persist
        # ---------------------------------------
        repository = APIKeyRepository(db)

        record = repository.create(record)

        # ---------------------------------------
        # 7. Response
        # ---------------------------------------
        return CreateAPIKeyResponse(
            id=record.id,
            name=record.name,
            api_key=api_key,
        )

    # ---------------------------------------
    # List API Keys
    # ---------------------------------------

    def get_all_keys(
        self,
        db,
        user_id: int,
    ):
        repository = APIKeyRepository(db)

        return repository.get_by_user(
            user_id,
        )

    # ---------------------------------------
    # Disable API Key
    # ---------------------------------------

    def disable_key(
        self,
        db,
        user_id: int,
        api_key_id: int,
    ):
        repository = APIKeyRepository(db)

        record = repository.get_owned(
            user_id,
            api_key_id,
        )

        if not record:
            raise HTTPException(
                status_code=404,
                detail="API Key not found",
            )

        record.active = False

        return repository.update(record)

    # ---------------------------------------
    # Enable API Key
    # ---------------------------------------

    def enable_key(
        self,
        db,
        user_id: int,
        api_key_id: int,
    ):
        repository = APIKeyRepository(db)

        record = repository.get_owned(
            user_id,
            api_key_id,
        )

        if not record:
            raise HTTPException(
                status_code=404,
                detail="API Key not found",
            )

        record.active = True

        return repository.update(record)

    # ---------------------------------------
    # Delete API Key
    # ---------------------------------------

    def delete_key(
        self,
        db,
        user_id: int,
        api_key_id: int,
    ):
        repository = APIKeyRepository(db)

        record = repository.get_owned(
            user_id,
            api_key_id,
        )

        if not record:
            raise HTTPException(
                status_code=404,
                detail="API Key not found",
            )

        repository.delete(record)

        return {
            "success": True,
            "message": "API Key deleted",
        }

    # ---------------------------------------
    # Rotate API Key
    # ---------------------------------------

    def rotate_key(
        self,
        db,
        user_id: int,
        api_key_id: int,
    ):
        repository = APIKeyRepository(db)

        record = repository.get_owned(
            user_id,
            api_key_id,
        )

        if not record:
            raise HTTPException(
                status_code=404,
                detail="API Key not found",
            )

        new_key = generate_api_key(
            live=True,
        )

        record.key_hash = hash_api_key(
            new_key,
        )

        repository.update(record)

        return {
            "success": True,
            "api_key": new_key,
        }
from sqlalchemy.orm import Session, joinedload

from app.models.api_key import APIKey
from app.models.project import Project


class APIKeyRepository:
    def __init__(self, db: Session):
        self.db = db

    # ----------------------------------
    # Create
    # ----------------------------------

    def create(
        self,
        api_key: APIKey,
    ) -> APIKey:
        self.db.add(api_key)
        self.db.commit()
        self.db.refresh(api_key)
        return api_key

    # ----------------------------------
    # Read
    # ----------------------------------

    def get(
        self,
        api_key_id: int,
    ) -> APIKey | None:
        return (
            self.db.query(APIKey)
            .options(
                joinedload(APIKey.plan),
                joinedload(APIKey.project),
            )
            .filter(APIKey.id == api_key_id)
            .first()
        )

    def get_owned(
        self,
        user_id: int,
        api_key_id: int,
    ) -> APIKey | None:
        return (
            self.db.query(APIKey)
            .options(
                joinedload(APIKey.plan),
                joinedload(APIKey.project),
            )
            .join(APIKey.project)
            .filter(
                APIKey.id == api_key_id,
                Project.user_id == user_id,
            )
            .first()
        )

    def get_all(
        self,
    ) -> list[APIKey]:
        return (
            self.db.query(APIKey)
            .options(
                joinedload(APIKey.plan),
                joinedload(APIKey.project),
            )
            .order_by(APIKey.created_at.desc())
            .all()
        )

    def get_by_user(
        self,
        user_id: int,
    ) -> list[APIKey]:
        return (
            self.db.query(APIKey)
            .options(
                joinedload(APIKey.plan),
                joinedload(APIKey.project),
            )
            .join(APIKey.project)
            .filter(
                Project.user_id == user_id,
            )
            .order_by(
                APIKey.created_at.desc(),
            )
            .all()
        )

    def count_by_user(
        self,
        user_id: int,
    ) -> int:
        return (
            self.db.query(APIKey)
            .join(APIKey.project)
            .filter(
                Project.user_id == user_id,
            )
            .count()
        )

    def get_by_hash(
        self,
        key_hash: str,
    ) -> APIKey | None:
        return (
            self.db.query(APIKey)
            .options(
                joinedload(APIKey.plan),
                joinedload(APIKey.project),
            )
            .filter(APIKey.key_hash == key_hash)
            .first()
        )

    # ----------------------------------
    # Update
    # ----------------------------------

    def update(
        self,
        api_key: APIKey,
    ) -> APIKey:
        self.db.commit()
        self.db.refresh(api_key)
        return api_key

    # ----------------------------------
    # Delete
    # ----------------------------------

    def delete(
        self,
        api_key: APIKey,
    ) -> None:
        self.db.delete(api_key)
        self.db.commit()
from sqlalchemy.orm import Session, joinedload

from app.models.api_key import APIKey


class APIKeyRepository:
    def __init__(self, db: Session):
        self.db = db

    # ----------------------------------
    # Create
    # ----------------------------------

    def create(self, api_key: APIKey) -> APIKey:
        self.db.add(api_key)
        self.db.commit()
        self.db.refresh(api_key)
        return api_key

    # ----------------------------------
    # Read
    # ----------------------------------

    def get(self, api_key_id: int) -> APIKey | None:
        return (
            self.db.query(APIKey)
            .options(
                joinedload(APIKey.plan),
                joinedload(APIKey.project),
            )
            .filter(APIKey.id == api_key_id)
            .first()
        )

    def get_all(self) -> list[APIKey]:
        return (
            self.db.query(APIKey)
            .options(
                joinedload(APIKey.plan),
                joinedload(APIKey.project),
            )
            .order_by(APIKey.created_at.desc())
            .all()
        )

    def get_by_hash(self, key_hash: str) -> APIKey | None:
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

    def update(self, api_key: APIKey) -> APIKey:
        self.db.commit()
        self.db.refresh(api_key)
        return api_key

    # ----------------------------------
    # Delete
    # ----------------------------------

    def delete(self, api_key: APIKey) -> None:
        self.db.delete(api_key)
        self.db.commit()
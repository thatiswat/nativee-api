from sqlalchemy.orm import Session

from app.models.api_key import APIKey


class APIKeyRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        api_key: APIKey,
    ):
        self.db.add(api_key)
        self.db.commit()
        self.db.refresh(api_key)

        return api_key

    def get_by_hash(
        self,
        key_hash: str,
    ):
        return (
            self.db.query(APIKey)
            .filter(APIKey.key_hash == key_hash)
            .first()
        )
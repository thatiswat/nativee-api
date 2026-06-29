from app.models.api_key import APIKey


class APIKeyRepository:

    @staticmethod
    def create(
        db,
        api_key: APIKey,
    ):
        db.add(api_key)
        db.commit()
        db.refresh(api_key)

        return api_key
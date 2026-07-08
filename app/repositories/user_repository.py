from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # ----------------------------------
    # Create
    # ----------------------------------

    def create(
        self,
        user: User,
    ) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    # ----------------------------------
    # Read
    # ----------------------------------

    def get_by_id(
        self,
        user_id: int,
    ) -> User | None:
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )


    def get_by_identity_id(
        self,
        identity_id: str,
    ) -> User | None:
        return (
            self.db.query(User)
            .filter(
                User.identity_id == identity_id,
            )
            .first()
        )


    def get_by_email(
        self,
        email: str,
    ) -> User | None:
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )


    def get_all(
        self,
    ) -> list[User]:
        return (
            self.db.query(User)
            .order_by(User.created_at.desc())
            .all()
        )

    # ----------------------------------
    # Update
    # ----------------------------------

    def update(
        self,
        user: User,
    ) -> User:
        self.db.commit()
        self.db.refresh(user)

        return user

    # ----------------------------------
    # Delete
    # ----------------------------------

    def delete(
        self,
        user: User,
    ) -> None:
        self.db.delete(user)
        self.db.commit()
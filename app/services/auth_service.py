from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserCreateRequest,
    UserLoginRequest,
)


class AuthService:
    def __init__(
        self,
        db: Session,
    ):
        self.users = UserRepository(db)

    # ----------------------------------
    # Register
    # ----------------------------------

    def register(
        self,
        request: UserCreateRequest,
    ) -> User:
        existing = self.users.get_by_email(
            request.email,
        )

        if existing:
            raise ValueError(
                "Email already registered."
            )

        user = User(
            name=request.name,
            email=request.email,
            password_hash=hash_password(
                request.password,
            ),
            role="customer",
            is_active=True,
        )

        return self.users.create(user)

    # ----------------------------------
    # Login
    # ----------------------------------

    def login(
        self,
        request: UserLoginRequest,
    ) -> str:
        user = self.users.get_by_email(
            request.email,
        )

        if user is None:
            raise ValueError(
                "Invalid email or password."
            )

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise ValueError(
                "Invalid email or password."
            )

        if not user.is_active:
            raise ValueError(
                "User account is disabled."
            )

        return create_access_token(
            user.id,
        )

    # ----------------------------------
    # Current User
    # ----------------------------------

    def get_current_user(
        self,
        user_id: int,
    ) -> User | None:
        return self.users.get_by_id(
            user_id,
        )
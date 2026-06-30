from datetime import datetime
from datetime import timedelta
from datetime import timezone

from jose import JWTError
from jose import jwt
from passlib.context import CryptContext

from app.core.settings import (
    JWT_ALGORITHM,
    JWT_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(
    password: str,
) -> str:
    return pwd_context.hash(password)


def verify_password(
    password: str,
    password_hash: str,
) -> bool:
    return pwd_context.verify(
        password,
        password_hash,
    )


def create_access_token(
    user_id: int,
) -> str:
    expire = datetime.now(
        timezone.utc,
    ) + timedelta(
        minutes=JWT_EXPIRE_MINUTES,
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def decode_access_token(
    token: str,
) -> dict | None:
    try:
        return jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )
    except JWTError:
        return None
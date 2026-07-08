from jose import jwt

from app.core.settings import (
    IDENTITY_PUBLIC_KEY,
    IDENTITY_ALGORITHM,
    IDENTITY_ISSUER,
    IDENTITY_AUDIENCE,
)


with open(
    IDENTITY_PUBLIC_KEY,
    "r",
) as f:
    PUBLIC_KEY = f.read()


def verify_access_token(
    token: str,
):

    return jwt.decode(
        token,
        PUBLIC_KEY,
        algorithms=[
            IDENTITY_ALGORITHM,
        ],
        issuer=IDENTITY_ISSUER,
        audience=IDENTITY_AUDIENCE,
    )
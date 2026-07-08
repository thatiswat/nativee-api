import os

from jose import jwt

from app.core.settings import (
    IDENTITY_PUBLIC_KEY,
    IDENTITY_ALGORITHM,
    IDENTITY_ISSUER,
    IDENTITY_AUDIENCE,
)

# Support both:
# Local  -> IDENTITY_PUBLIC_KEY = /path/to/public.pem
# Railway -> IDENTITY_PUBLIC_KEY = -----BEGIN PUBLIC KEY-----...
if os.path.exists(IDENTITY_PUBLIC_KEY):
    with open(IDENTITY_PUBLIC_KEY, "r") as f:
        PUBLIC_KEY = f.read()
else:
    PUBLIC_KEY = IDENTITY_PUBLIC_KEY


def verify_access_token(token: str):
    return jwt.decode(
        token,
        PUBLIC_KEY,
        algorithms=[IDENTITY_ALGORITHM],
        issuer=IDENTITY_ISSUER,
        audience=IDENTITY_AUDIENCE,
    )
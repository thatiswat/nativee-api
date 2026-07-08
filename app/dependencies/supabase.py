from fastapi import (
    Depends,
    HTTPException,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from app.core.supabase import supabase


security = HTTPBearer(
    auto_error=False,
)


async def get_current_client(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        security,
    ),
):
    """
    Verify Supabase JWT.

    Returns the JWT payload.
    """

    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
        )

    token = credentials.credentials

    try:

        payload = await supabase.verify(
            token,
        )

        return payload

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid access token",
        )
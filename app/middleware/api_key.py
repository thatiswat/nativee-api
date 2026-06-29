from fastapi import Header, HTTPException
from app.core.settings import API_KEY


async def verify_api_key(
    authorization: str | None = Header(default=None),
):
    """
    Verify Bearer API key.
    """

    if authorization is None:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization header",
        )

    token = authorization.replace("Bearer ", "").strip()

    if token != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key",
        )
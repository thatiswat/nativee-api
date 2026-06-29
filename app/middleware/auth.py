from starlette.middleware.base import BaseHTTPMiddleware

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.core.request_context import RequestContext
from app.database.session import SessionLocal
from app.repositories.api_key_repository import APIKeyRepository
from app.services.rate_limit_service import RateLimitService
from app.utils.crypto import hash_api_key


PUBLIC_ROUTES = {
    "/",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/v1/health",
}


class AuthenticationMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        if request.url.path in PUBLIC_ROUTES:
            return await call_next(request)

        auth = request.headers.get("Authorization")

        if not auth:
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing Authorization Header"},
            )

        if not auth.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid Authorization Header"},
            )

        api_key = auth.replace("Bearer ", "")

        db = SessionLocal()

        try:
            record = (
                APIKeyRepository(db)
                .get_by_hash(hash_api_key(api_key))
            )

            if not record:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid API Key"},
                )

            if not record.active:
                return JSONResponse(
                    status_code=403,
                    content={"detail": "API Key Disabled"},
                )

            # -------------------------------------------------
            # Rate Limiting (UPDATED LINE)
            # -------------------------------------------------
            rate_limiter = RateLimitService(db)

            result = rate_limiter.is_allowed(
                record   # ✅ CHANGED: was record.id
            )

            if not result["allowed"]:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded",
                )

            request.state.rate_limit = result
            request.state.api_key = record

            request.state.context = RequestContext(
                request_id=request.headers.get("X-Request-ID", ""),
                api_key_id=record.id,
            )

            response = await call_next(request)

            response.headers["X-RateLimit-Limit"] = str(result["limit"])
            response.headers["X-RateLimit-Remaining"] = str(result["remaining"])

            return response

        finally:
            db.close()
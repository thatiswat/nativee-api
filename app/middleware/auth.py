from starlette.middleware.base import BaseHTTPMiddleware

from fastapi import HTTPException

from app.database.session import SessionLocal
from app.services.api_key_auth_service import APIKeyAuthService
from app.services.quota_service import QuotaService
from app.services.rate_limit_service import RateLimitService
from app.services.request_context_builder import (
    RequestContextBuilder,
)


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

        db = SessionLocal()

        try:
            # -------------------------------------------------
            # Authenticate API Key
            # -------------------------------------------------

            record = (
                APIKeyAuthService(db)
                .authenticate(
                    request.headers.get(
                        "Authorization"
                    )
                )
            )

            # -------------------------------------------------
            # Rate Limiting
            # -------------------------------------------------

            rate_limiter = RateLimitService(db)

            result = rate_limiter.is_allowed(
                record,
            )

            if not result["allowed"]:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded",
                )

            # -------------------------------------------------
            # Monthly Quota
            # -------------------------------------------------

            quota_service = QuotaService(db)

            quota = quota_service.is_allowed(
                record,
            )

            if not quota["allowed"]:
                raise HTTPException(
                    status_code=429,
                    detail="Monthly quota exceeded",
                )

            # -------------------------------------------------
            # Store Request State
            # -------------------------------------------------

            request.state.rate_limit = result
            request.state.quota = quota
            request.state.api_key = record

            request.state.context = (
                RequestContextBuilder()
                .build(
                    request=request,
                    api_key=record,
                )
            )

            response = await call_next(request)

            # -------------------------------------------------
            # Rate Limit Headers
            # -------------------------------------------------

            response.headers["X-RateLimit-Limit"] = str(
                result["limit"]
            )

            response.headers["X-RateLimit-Remaining"] = str(
                result["remaining"]
            )

            # -------------------------------------------------
            # Monthly Quota Headers
            # -------------------------------------------------

            response.headers["X-Quota-Limit"] = str(
                quota["limit"]
            )

            response.headers["X-Quota-Used"] = str(
                quota["used"]
            )

            response.headers["X-Quota-Remaining"] = str(
                quota["remaining"]
            )

            return response

        finally:
            db.close()
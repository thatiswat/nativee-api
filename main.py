from contextlib import asynccontextmanager
import asyncio
import secrets
import time

import httpx

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import (
    FileResponse,
    ORJSONResponse,
)
from fastapi.security import HTTPBearer

from app.api.v1 import router as api_router
from app.core.logger import logger
from app.core.settings import (
    GROQ_API_KEY,
    UPLOAD_DIR,
)
from app.database.session import SessionLocal
from app.middleware.auth import AuthenticationMiddleware
from app.services.plan_service import PlanService


# ---------------------------------------------------------------------
# Startup Checks
# ---------------------------------------------------------------------

if GROQ_API_KEY:
    logger.info("Groq provider configured.")
else:
    logger.warning("Groq API key missing.")


# ---------------------------------------------------------------------
# Application Lifespan
# ---------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Create shared resources and initialize the platform.
    """

    app.state.http = httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),
        limits=httpx.Limits(
            max_keepalive_connections=20,
            max_connections=100,
        ),
    )

    # ---------------------------------------------------------
    # Platform Initialization
    # ---------------------------------------------------------

    db = SessionLocal()

    try:
        PlanService(db).seed_defaults()
        logger.info("Default plans initialized.")
    finally:
        db.close()

    yield

    await app.state.http.aclose()


# ---------------------------------------------------------------------
# FastAPI
# ---------------------------------------------------------------------

app = FastAPI(
    title="Nativee API",
    version="1.0.0",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

bearer_scheme = HTTPBearer(
    bearerFormat="API Key",
    scheme_name="BearerAuth",
    description=(
        "Paste your Nativee API Key.\n\n"
        "Example:\n"
        "Bearer ntv_live_xxxxxxxxxxxxxxxxx"
    ),
)

logger.info("Nativee API Started")


# ---------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://nativee.vercel.app",
        "https://nativee.com",
        "https://www.nativee.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
)

app.add_middleware(
    AuthenticationMiddleware,
)


@app.middleware("http")
async def benchmark(request: Request, call_next):
    request.state.id = secrets.token_hex(4)

    start = time.perf_counter()

    response = await call_next(request)

    elapsed_ms = (time.perf_counter() - start) * 1000

    response.headers["X-Request-Time"] = f"{elapsed_ms:.2f}ms"
    response.headers["X-Request-ID"] = request.state.id

    logger.info(
        "[%s] %s %s %.2fms",
        request.state.id,
        request.method,
        request.url.path,
        elapsed_ms,
    )

    return response


# ---------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------

app.include_router(api_router)


# ---------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------

@app.get("/")
async def root():
    return {
        "status": "running",
        "product": "Nativee",
        "version": "1.0.0",
    }


# ---------------------------------------------------------------------
# Audio
# ---------------------------------------------------------------------

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Audio file not found",
        )

    async def cleanup():
        await asyncio.sleep(10)
        file_path.unlink(missing_ok=True)

    asyncio.create_task(cleanup())

    return FileResponse(
        path=file_path,
        media_type="audio/mpeg",
        filename=file_path.name,
    )


# ---------------------------------------------------------------------
# OpenAPI
# ---------------------------------------------------------------------

def custom_openapi():

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="Nativee Platform API",
        routes=app.routes,
    )

    openapi_schema.setdefault("components", {})

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "API Key",
        }
    }

    for path in openapi_schema["paths"].values():
        for operation in path.values():
            if isinstance(operation, dict):
                operation["security"] = [
                    {
                        "BearerAuth": []
                    }
                ]

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi
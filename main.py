import asyncio

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse, ORJSONResponse

from app.api.platform import router as developer_router
from app.api.client import router as client_router
from app.core.lifespan import lifespan
from app.core.logger import logger
from app.core.middleware import benchmark
from app.core.settings import (
    GROQ_API_KEY,
    UPLOAD_DIR,
)
from app.schemas.shared.root import RootResponse


# ---------------------------------------------------------------------
# Startup Checks
# ---------------------------------------------------------------------

if GROQ_API_KEY:
    logger.info(
        "Groq provider configured."
    )
else:
    logger.warning(
        "Groq API key missing."
    )


# ---------------------------------------------------------------------
# FastAPI
# ---------------------------------------------------------------------

app = FastAPI(
    title="Nativee API",
    version="1.0.0",
    description="""
Nativee is an AI Language Platform for Indian languages.

The platform provides APIs for:

• Speech Recognition

• Translation

• Text-to-Speech

Designed for developers and enterprises.
""",
    contact={
        "name": "Nativee",
        "url": "https://nativee.in",
        "email": "support@nativee.in",
    },
    license_info={
        "name": "Proprietary",
    },
    terms_of_service="https://nativee.in/terms",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


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


# ---------------------------------------------------------------------
# Request Benchmark Middleware
# ---------------------------------------------------------------------

@app.middleware("http")
async def benchmark_middleware(
    request: Request,
    call_next,
):
    return await benchmark(
        request,
        call_next,
    )


# ---------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------

app.include_router(
    developer_router,
)

app.include_router(
    client_router,
)


# ---------------------------------------------------------------------
# Platform
# ---------------------------------------------------------------------

@app.get(
    "/",
    tags=["Platform"],
    response_model=RootResponse,
    summary="Platform Information",
)
async def root():

    return RootResponse(
        name="Nativee API",
        status="running",
        version="1.0.0",
        documentation="https://developer.nativee.in",
        status_page="https://status.nativee.in",
    )


# ---------------------------------------------------------------------
# Audio
# ---------------------------------------------------------------------

@app.get(
    "/audio/{filename}",
    tags=["Audio"],
    summary="Download Audio",
)
async def get_audio(
    filename: str,
):

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Audio file not found",
        )

    async def cleanup():

        await asyncio.sleep(
            10,
        )

        file_path.unlink(
            missing_ok=True,
        )

    asyncio.create_task(
        cleanup(),
    )

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

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    schema.setdefault(
        "components",
        {},
    )

    schema["components"]["securitySchemes"] = {

        "CustomerJWT": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        },

        "APIKeyAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "API Key",
        },

    }

    app.openapi_schema = schema

    return schema


app.openapi = custom_openapi
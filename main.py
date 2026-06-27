from pathlib import Path
from contextlib import asynccontextmanager
import asyncio
import secrets
import time

import httpx

from fastapi import (
    FastAPI,
    Request,
    HTTPException,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import (
    FileResponse,
    ORJSONResponse,
)

from app.routes.speech import router as conversation_router
from app.routes.translate import router as translate_router
from app.routes.stream import router as stream_router

from app.config import UPLOAD_DIR


# ---------------------------------------------------------------------
# Application Lifespan
# ---------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Create shared resources once during startup.
    """

    app.state.http = httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),
        limits=httpx.Limits(
            max_keepalive_connections=20,
            max_connections=100,
        ),
        http2=True,
    )

    yield

    await app.state.http.aclose()


# ---------------------------------------------------------------------
# FastAPI
# ---------------------------------------------------------------------

app = FastAPI(
    title="Nativeee API",
    version="1.0.0",
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

        # Web
        "https://nativeee.vercel.app",
        "https://nativeee.com",
        "https://www.nativeee.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
)


@app.middleware("http")
async def benchmark(request: Request, call_next):
    request.state.id = secrets.token_hex(4)

    start = time.perf_counter()

    response = await call_next(request)

    elapsed_ms = (time.perf_counter() - start) * 1000

    response.headers["X-Request-Time"] = f"{elapsed_ms:.2f}ms"
    response.headers["X-Request-ID"] = request.state.id

    print(
        f"[{request.state.id}] "
        f"{request.method} "
        f"{request.url.path} "
        f"{elapsed_ms:.2f}ms"
    )

    return response


# ---------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------

app.include_router(conversation_router)
app.include_router(translate_router)
app.include_router(stream_router)


# ---------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------

@app.get("/")
async def root():
    return {
        "status": "running",
        "product": "Nativeee",
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
        # Allow the client time to finish downloading.
        await asyncio.sleep(10)

        # Delete generated audio.
        file_path.unlink(missing_ok=True)

    asyncio.create_task(cleanup())

    return FileResponse(
        path=file_path,
        media_type="audio/mpeg",
        filename=file_path.name,
    )
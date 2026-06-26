from pathlib import Path
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, ORJSONResponse

from app.routes.speech import router as conversation_router
from app.routes.translate import router as translate_router

from app.config import UPLOAD_DIR

app = FastAPI(
    title="Nativeee API",
    version="1.0.0",
    default_response_class=ORJSONResponse,
)

# CORS
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

# GZip Compression
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
)

# Routes
app.include_router(conversation_router)
app.include_router(translate_router)


@app.get("/")
async def root():
    return {
        "status": "running",
        "product": "Nativeee",
        "version": "1.0.0",
    }


@app.get("/audio/{filename}")
async def get_audio(filename: str):
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        return {
            "error": "Audio file not found",
        }

    async def cleanup():
        # Give the client enough time to download the file.
        await asyncio.sleep(10)

        # Delete the generated MP3.
        file_path.unlink(missing_ok=True)

    # Run cleanup in the background.
    asyncio.create_task(cleanup())

    return FileResponse(
        path=file_path,
        media_type="audio/mpeg",
        filename=file_path.name,
    )
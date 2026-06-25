from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.routes.speech import router as conversation_router
from app.routes.translate import router as translate_router

from app.config import UPLOAD_DIR

app = FastAPI(
    title="Nativee API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",

        # Web
        "https://nativeee.vercel.app",   # replace with your Vercel domain
        "https://nativeee.com",
        "https://www.nativeee.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(conversation_router)
app.include_router(translate_router)

@app.get("/")
async def root():
    return {
        "status": "running",
        "product": "Nativee",
        "version": "1.0.0",
    }


@app.get("/audio/{filename}")
async def get_audio(filename: str):

    file_path = UPLOAD_DIR / filename

    return FileResponse(
        file_path,
        media_type="audio/mpeg",
    )
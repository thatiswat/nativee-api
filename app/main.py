from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.routes.conversation import router
from app.config import UPLOAD_DIR

app = FastAPI(
    title="iSpeak API",
    version="0.1.0"
)

# ----------------------------------
# CORS
# ----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://ispeak-frontend.vercel.app",
        "https://1speak.in",
        "https://www.1speak.in",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ----------------------------------
# ROUTES
# ----------------------------------

app.include_router(router)

# ----------------------------------
# ROOT
# ----------------------------------

@app.get("/")
async def root():

    return {
        "status": "running",
        "product": "iSpeak"
    }

# ----------------------------------
# AUDIO FILES
# ----------------------------------

@app.get("/audio/{filename}")
async def get_audio(filename: str):

    file_path = UPLOAD_DIR / filename

    return FileResponse(
        file_path,
        media_type="audio/mpeg"
    )
from fastapi import APIRouter

from app.routes.speech import router as speech_router
from app.routes.translate import router as translate_router
from app.routes.api_keys import router as api_key_router

router = APIRouter(prefix="/v1")

router.include_router(speech_router)
router.include_router(translate_router)
router.include_router(api_key_router)


@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": "1.0.0",
    }
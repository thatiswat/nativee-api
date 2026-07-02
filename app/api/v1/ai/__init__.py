from fastapi import APIRouter

from .conversation import router as conversation_router
from .translate import router as translate_router

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)

router.include_router(conversation_router)
router.include_router(translate_router)
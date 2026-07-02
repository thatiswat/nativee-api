from fastapi import APIRouter

from .customer import router as customer_router
from .ai import router as ai_router
from .platform import router as platform_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(customer_router)
router.include_router(ai_router)
router.include_router(platform_router)
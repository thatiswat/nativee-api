from fastapi import APIRouter

from app.engine import engine

router = APIRouter(
    prefix="/health",
)


@router.get("")
async def health():

    engine_health = await engine.health()

    return {
        "api": "healthy",
        "engine": engine_health,
    }
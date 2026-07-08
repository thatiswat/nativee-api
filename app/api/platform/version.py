from fastapi import APIRouter

from app.engine import engine

router = APIRouter(
    prefix="/version",
)


@router.get("")
async def version():

    engine_version = await engine.version()

    return {
        "api": {
            "service": "nativeee-api",
            "version": "1.0.0",
        },
        "engine": engine_version,
    }
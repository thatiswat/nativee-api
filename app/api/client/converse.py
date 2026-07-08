from fastapi import APIRouter

router = APIRouter(
    prefix="/converse",
    tags=["Mobile Converse"],
)

@router.post("/start")
async def start():
    return {
        "success": True,
        "message": "Coming soon",
    }


@router.post("/stream")
async def stream():
    return {
        "success": True,
        "message": "Coming soon",
    }


@router.post("/stop")
async def stop():
    return {
        "success": True,
        "message": "Coming soon",
    }
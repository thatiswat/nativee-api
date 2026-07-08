from fastapi import APIRouter

router = APIRouter(
    prefix="/chat",
    tags=["Mobile Chat"],
)


@router.get("/conversations")
async def conversations():
    return {
        "success": True,
        "message": "Coming soon",
    }


@router.get("/messages")
async def messages():
    return {
        "success": True,
        "message": "Coming soon",
    }


@router.post("/send")
async def send():
    return {
        "success": True,
        "message": "Coming soon",
    }
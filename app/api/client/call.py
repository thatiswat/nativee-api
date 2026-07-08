from fastapi import APIRouter

router = APIRouter(
    prefix="/call",
    tags=["Mobile Call"],
)


@router.post("/create")
async def create():
    return {
        "success": True,
        "message": "Coming soon",
    }


@router.post("/join")
async def join():
    return {
        "success": True,
        "message": "Coming soon",
    }


@router.post("/leave")
async def leave():
    return {
        "success": True,
        "message": "Coming soon",
    }
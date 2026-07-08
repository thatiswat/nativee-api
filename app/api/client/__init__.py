from fastapi import APIRouter


from .connect import router as connect_router
from .converse import router as converse_router
from .profile import router as profile_router
from .chat import router as chat_router
from .call import router as call_router


router = APIRouter(
    prefix="/mobile",
)



router.include_router(profile_router)
router.include_router(connect_router)
router.include_router(converse_router)
router.include_router(chat_router)
router.include_router(call_router)
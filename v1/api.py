from fastapi import APIRouter
from v1.endpoints import videos, chats

router = APIRouter(
    prefix="/v1",
    tags=["v1"],
    responses={404: {"description": "Not found"}},
)

router.include_router(videos.router)
router.include_router(chats.router)

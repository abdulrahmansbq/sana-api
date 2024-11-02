from fastapi import APIRouter
from v1.endpoints import videos, chats, snaps, exams

router = APIRouter(
    prefix="/v1",
    tags=["v1"],
    responses={404: {"description": "Not found"}},
)

router.include_router(videos.router)
router.include_router(chats.router)

router.include_router(snaps.router)

router.include_router(exams.router)

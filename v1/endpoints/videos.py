from fastapi import APIRouter, Response
from core.controllers.video_controller import VideoController

router = APIRouter(
    prefix="/videos",
    tags=["videos"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{video_id}/embed")
async def embed(video_id: str, response: Response):
    video = VideoController(video_id, response)
    response = await video.embed()
    return response

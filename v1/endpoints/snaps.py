from fastapi import APIRouter, Form
from core.controllers.snap_controller import SnapController

router = APIRouter(
    prefix="/snaps",
    tags=["snaps"],
    responses={404: {"description": "Not found"}},
)


@router.post("/generate")
async def snap_generator(namespace_id: str = Form(...), namespace_type: str = Form(...), transcript: str = Form(...)):
    snaps  = await SnapController(namespace_id, transcript, namespace_type).generate()
    return {"status": "Success", "message": snaps}
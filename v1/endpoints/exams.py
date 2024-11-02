from fastapi import APIRouter, Form
from core.controllers.exam_controller import ExamController

router = APIRouter(
    prefix="/exams",
    tags=["exams"],
    responses={404: {"description": "Not found"}},
)


@router.post("/generate")
async def exam_generator(namespace_id: str = Form(...), namespace_type: str = Form(...), transcript: str = Form(...)):
    response  = await ExamController(namespace_id=namespace_id, namespace_type=namespace_type, transcript=transcript).generate()
    return {"status": "Success", "message": response}
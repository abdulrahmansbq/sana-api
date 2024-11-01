from fastapi import APIRouter, Form
from core.controllers.chat_controller import ChatController

router = APIRouter(
    prefix="/chats",
    tags=["chats"],
    responses={404: {"description": "Not found"}},
)


@router.post("/{namespace_id}/chat")
async def embed(namespace_id: str, message: str = Form(...)):
    chat = ChatController(namespace_id, message)
    return await chat.chat()

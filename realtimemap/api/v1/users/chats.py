from fastapi import APIRouter

router = APIRouter(
    prefix="/chat",
    tags=["chats"],
)


class PersonalChatManager:
    def __init__(self):
        pass

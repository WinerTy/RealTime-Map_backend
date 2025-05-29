from typing import List, Annotated, Any, Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends
from pydantic import Field, BaseModel, ValidationError

from crud.mark import MarkRepository
from dependencies.crud import get_mark_repository

router = APIRouter(prefix="/ws")


class Coordinates(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class WebsocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        # self.marks_repo = marks_repo

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def set_geom(self):
        pass

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    def validate_params(self, data: Dict[str, Any]) -> Coordinates:
        try:
            return Coordinates(**data)
        except ValidationError as e:
            self.broadcast("Ошибка  епта")
            raise ValueError(f"Invalid coordinates: {e.errors()}")


manager = WebsocketManager()


@router.get("/")
async def set_state(value: int, request: Request):
    request.state.my_value = value
    return value


@router.websocket("/")
async def websocket_endpoint(
    websocket: WebSocket,
    repo: Annotated["MarkRepository", Depends(get_mark_repository)],
):
    await manager.connect(websocket)
    while True:
        try:
            data = await websocket.receive_json()
            coords = manager.validate_params(data)
            result = await repo.get_marks(
                longitude=coords.longitude, latitude=coords.latitude
            )
            result_json = [mark.model_dump() for mark in result]

            await websocket.send_json(result_json)

        except WebSocketDisconnect:
            await manager.disconnect(websocket)

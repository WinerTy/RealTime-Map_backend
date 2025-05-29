from typing import Dict, Optional, List

from fastapi import WebSocket
from pydantic import BaseModel, Field, ValidationError

from models.mark.schemas import ReadMark
from .base import WebsocketManager


class Coordinates(BaseModel):
    latitude: float = Field(..., ge=-180, le=180, examples=["75.445675"])
    longitude: float = Field(..., ge=-90, le=90, examples=["63.201907"])


class MarkWebSocket(WebsocketManager):
    def __init__(self):
        super().__init__()
        self.connection_data: Dict[WebSocket, Optional[Coordinates]] = {}

    async def connect(self, websocket: WebSocket):
        await super().connect(websocket)
        self.connection_data[websocket] = None

    async def update_coordinates(
        self, websocket: WebSocket, new_coords: Dict[str, float]
    ):
        coords = await self._validate_coords(websocket, new_coords)
        if websocket in self.active_connections:
            self.connection_data[websocket] = coords

    async def _validate_coords(
        self, websocket: WebSocket, coords: Dict[str, float]
    ) -> Coordinates:
        try:
            return Coordinates(**coords)
        except ValidationError as e:
            await websocket.send_text(str(e))
            await self.disconnect(websocket)

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            await super().disconnect(websocket)
            self.connection_data.pop(websocket)

    def get_user_cords(self, websocket: WebSocket) -> Coordinates:
        return self.connection_data.get(websocket)

    @staticmethod
    async def broadcast_json(websocket: WebSocket, data: List[ReadMark]):
        await websocket.send_json(data)


marks_websocket = MarkWebSocket()

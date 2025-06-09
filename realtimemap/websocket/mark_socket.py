from typing import Dict, Optional, List

from fastapi import WebSocket
from pydantic import ValidationError

from models.mark.schemas import ReadMark, MarkCoordinates
from .base import WebsocketManager


class MarkWebSocket(WebsocketManager):
    def __init__(self):
        super().__init__()
        self.connection_data: Dict[WebSocket, Optional[MarkCoordinates]] = {}

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
    ) -> MarkCoordinates:
        try:
            return MarkCoordinates(**coords)
        except ValidationError as e:
            await websocket.send_text(str(e))
            await self.disconnect(websocket)

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            await super().disconnect(websocket)
            self.connection_data.pop(websocket)

    def get_user_cords(self, websocket: WebSocket) -> MarkCoordinates:
        return self.connection_data.get(websocket)

    @staticmethod
    async def broadcast_json(websocket: WebSocket, data: List[ReadMark]):
        await websocket.send_json(data)


marks_websocket = MarkWebSocket()

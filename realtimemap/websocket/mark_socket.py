from typing import Dict, Optional

from fastapi import WebSocket
from pydantic import ValidationError

from models.mark.schemas import MarkCoordinates, MarkRequestParams
from .base import WebsocketManager, AbstractWebSocket


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

    async def check_include_mark(self):
        pass


marks_websocket = MarkWebSocket()


class MarksWebSocket(AbstractWebSocket):
    def __init__(self):
        self.connections: Dict[WebSocket, Optional[MarkRequestParams]] = dict()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections[websocket] = None

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.connections:
            self.connections.pop(websocket)

    async def set_params(self, websocket: WebSocket, params: MarkRequestParams):
        if websocket in self.connections:
            self.connections[websocket] = params

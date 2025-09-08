import asyncio
from typing import Dict, Optional, Set

from fastapi import WebSocket

from models.mark.schemas import MarkRequestParams


class MarkManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # noinspection PyTypeHints
            cls._instance.connections: Dict[WebSocket, Optional[MarkRequestParams]] = (
                dict()
            )
            cls._instance._lock = asyncio.Lock()
        return cls._instance

    async def connect(self, websocket: WebSocket):
        async with self._lock:
            await websocket.accept()
            self.connections[websocket] = None

    async def disconnect(self, websocket: WebSocket):
        async with self._lock:
            self.connections.pop(websocket, None)

    async def set_params(self, websocket: WebSocket, params: MarkRequestParams):
        async with self._lock:
            if websocket in self.connections:
                self.connections[websocket] = params

    async def get_sockets_by_params(self, filter_func) -> Set[WebSocket]:
        async with self._lock:
            return {
                ws
                for ws, params in self.connections.items()
                if params is not None and filter_func(params)
            }

    async def broadcast(self, message: dict, filter_func=None):
        targets = (
            await self.get_sockets_by_params(filter_func)
            if filter_func
            else set(self.connections.keys())
        )

        for websocket in targets:
            await websocket.send_json(message)

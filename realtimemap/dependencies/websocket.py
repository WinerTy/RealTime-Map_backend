from websocket.mark_socket import MarkManager


async def get_mark_websocket_manager() -> MarkManager:
    yield MarkManager()

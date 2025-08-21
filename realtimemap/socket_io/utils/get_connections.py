from typing import Optional, List

from core.app.socket import sio


def get_sids(namespace: str = "/") -> List[Optional[str]]:
    try:
        connections = sio.manager.rooms.get(namespace, {})
        if not connections:
            return []
        result = []
        for room_sid in connections:
            if room_sid:
                result.append(room_sid)
        return result
    except Exception:
        return []

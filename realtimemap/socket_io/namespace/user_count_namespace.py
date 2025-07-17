from socketio import AsyncNamespace


class UserCountNamespace(AsyncNamespace):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count: int = 0

    async def on_connect(self, sid, environ):
        self.count += 1
        await self.emit("user_count", {"count": self.count})

    async def on_disconnect(self, sid):
        self.count -= 1
        await self.emit("user_count", {"count": self.count})

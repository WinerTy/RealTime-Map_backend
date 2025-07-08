from socketio import AsyncNamespace


class ChatNamespace(AsyncNamespace):
    async def on_connect(self, sid, environ, auth):
        print(auth)

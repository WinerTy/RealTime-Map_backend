import socketio

from core.config import conf
from socket_io.namespace.chat_namespace import ChatNamespace
from socket_io.namespace.mark_namespac import MarksNamespace

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    client_manager=socketio.AsyncManager(),
)
sio_app = socketio.ASGIApp(socketio_server=sio)
sio.instrument(
    auth={
        "username": conf.socket.username,
        "password": conf.socket.password,
    }
)

sio.register_namespace(MarksNamespace(conf.socket.prefix.marks))
sio.register_namespace(ChatNamespace(conf.socket.prefix.chat))

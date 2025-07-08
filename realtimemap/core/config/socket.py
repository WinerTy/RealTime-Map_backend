from pydantic import BaseModel


class SocketIOPrefixConfig(BaseModel):
    marks: str = "/marks"
    chat: str = "/chat"


class SocketIOConfig(BaseModel):
    prefix: SocketIOPrefixConfig = SocketIOPrefixConfig()
    username: str
    password: str

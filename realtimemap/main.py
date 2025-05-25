import shutil
import uuid
from pathlib import Path
from typing import Optional, Annotated

from fastapi import UploadFile, File, HTTPException, Form
from fastapi_babel import BabelConfigs, BabelMiddleware, _  # noqa
from pydantic import BaseModel, model_validator
from pydantic_core.core_schema import ValidationInfo
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket

from core.app import create_app
from core.config import conf

app = create_app()


class FileUploadResponse(BaseModel):
    received_name: str
    file_path: str
    unique_filename: str
    message: str
    url: Optional[str] = None

    @model_validator(mode="after")
    def generate_full_url(self, info: ValidationInfo) -> "FileUploadResponse":
        # info.context будет None, если контекст не передан при model_validate
        if info.context and "request" in info.context and self.unique_filename:
            request: Request = info.context["request"]
            try:
                # Используем имя, указанное при монтировании статики
                self.url = str(request.url_for("static", path=self.unique_filename))
            except Exception as e:
                # Логирование ошибки или установка url в None, если генерация не удалась
                print(f"Error generating URL in Pydantic model: {e}")
                self.url = None  # или оставить как было, если уже None
        return self


STATIC_DIR = conf.static


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


class TestPostFile(BaseModel):
    name: str
    file: UploadFile = File(...)


@app.post("/test")
async def test_upload(
    data: Annotated[TestPostFile, Form(media_type="multipart/form-data")],
    request: Request,
):
    if not data.file.filename:
        raise HTTPException(
            status_code=400,
            detail="Файл не был предоставлен или имя файла отсутствует.",
        )

    try:
        file_extension = Path(data.file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_save_path = STATIC_DIR / unique_filename

        with open(file_save_path, "wb") as buffer:
            shutil.copyfileobj(data.file.file, buffer)
        result = {
            "received_name": data.file.filename,
            "file_path": str(file_save_path),
            "unique_filename": unique_filename,
            "message": "Файл Загружен",
        }
        return FileUploadResponse.model_validate(result, context={"request": request})
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Произошла ошибка при загрузке файла: {str(e)}",
        )
    finally:
        await data.file.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=conf.server.host, port=conf.server.port)

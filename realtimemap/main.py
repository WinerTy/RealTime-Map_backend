from typing import Optional

from fastapi_babel import BabelConfigs, BabelMiddleware, _  # noqa
from pydantic import BaseModel, model_validator
from pydantic_core.core_schema import ValidationInfo
from starlette.requests import Request

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=conf.server.host, port=conf.server.port)

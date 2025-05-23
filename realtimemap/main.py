import shutil
import uuid
from pathlib import Path
from typing import Optional

from fastapi import UploadFile, File, HTTPException
from fastapi_babel import BabelConfigs, BabelMiddleware, _  # noqa
from geojson_pydantic import Point
from pydantic import BaseModel

from core.app import create_app
from core.config import conf

app = create_app()


class TestPost(BaseModel):
    name: str
    photo: Optional[UploadFile]


class Coordinates(BaseModel):
    longitude: float
    latitude: float


class MarkResponse(BaseModel):
    mark_name: str
    mark_type: str
    coordinates: Coordinates  # Отдельные поля для координат

    class Config:
        from_attributes = True


class FileUploadResponse(BaseModel):
    received_name: str
    file_path: str
    message: str


class TestMark(BaseModel):
    id: int
    mark_name: str
    type_mark: str
    coords: Point


STATIC_DIR = Path("static")


@app.post("/test")
async def test_upload(file: UploadFile = File(description="Файл для загрузки")):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Файл не был предоставлен или имя файла отсутствует.",
        )

    try:
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_save_path = STATIC_DIR / unique_filename

        with open(file_save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return FileUploadResponse(
            received_name=file.filename,  # Use actual filename instead of hardcoded value
            file_path=str(file_save_path),
            message="Файл успешно загружен.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Произошла ошибка при загрузке файла: {str(e)}",
        )
    finally:
        await file.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=conf.server.host, port=conf.server.port)

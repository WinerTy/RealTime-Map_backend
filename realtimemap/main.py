import logging

from fastapi import Request, Path
from fastapi.responses import RedirectResponse, ORJSONResponse
from libcloud.storage.drivers.local import LocalStorageDriver
from libcloud.storage.types import ObjectDoesNotExistError
from sqlalchemy_file.storage import StorageManager
from starlette.responses import FileResponse, StreamingResponse

from core.app import create_app
from core.config import conf
from errors import HttpIntegrityError

logger = logging.getLogger(__name__)

app = create_app()


@app.exception_handler(HttpIntegrityError)
async def http_exception_handler(request: Request, exc: HttpIntegrityError):
    logger.info(f"DataBase Integrity Error. Request: {request.url.path}")
    return ORJSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
        headers=exc.headers,
    )


@app.get("/", tags=["Root"], status_code=307)
async def redirect_root():
    logger.info("Redirecting to /docs")
    return RedirectResponse(url="/docs")


@app.get("/media/{storage}/{file_id}", tags=["Root"], name="get_file")
def serve_files(
    storage: str = Path(...),
    file_id: str = Path(...),
):
    try:
        file = StorageManager.get_file(f"{storage}/{file_id}")

        # Для локального хранилища просто отдаем файл.
        # FileResponse сам выставит нужные заголовки для отображения в браузере.
        if isinstance(file.object.driver, LocalStorageDriver):
            return FileResponse(
                file.object.get_cdn_url(),  # get_cdn_url для LocalStorageDriver вернет локальный путь
                media_type=file.content_type,
                filename=file.filename,
                headers={"Content-Disposition": "inline"},
            )

        # Если есть публичный URL (напр. S3), делаем редирект
        if file.get_cdn_url():
            return RedirectResponse(file.get_cdn_url())

        # Для других хранилищ (без CDN) отдаем поток, но с правильным заголовком
        return StreamingResponse(
            file.object.as_stream(),
            media_type=file.content_type,
            headers={"Content-Disposition": "inline"},
        )

    except (ObjectDoesNotExistError, RuntimeError):
        logger.info(f"File does not exist: {storage}/{file_id}")
        return ORJSONResponse({"detail": "Not found"}, status_code=404)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=conf.server.host, port=conf.server.port)

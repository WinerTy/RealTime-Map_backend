import os
import time

from fastapi import Request, Path
from fastapi.responses import RedirectResponse, ORJSONResponse
from libcloud.storage.drivers.local import LocalStorageDriver
from libcloud.storage.types import ObjectDoesNotExistError
from sqlalchemy_file.storage import StorageManager
from starlette.responses import FileResponse, StreamingResponse

from core.app import create_app
from core.config import conf

app = create_app()

os.makedirs("uploads/category", exist_ok=True)
os.makedirs("uploads/default", exist_ok=True)
os.makedirs("uploads/mark", exist_ok=True)

default_container = LocalStorageDriver("uploads").get_container("default")
category_container = LocalStorageDriver("uploads").get_container("category")
mark_container = LocalStorageDriver("uploads").get_container("mark")

StorageManager.add_storage("default", default_container)
StorageManager.add_storage("category", category_container)
StorageManager.add_storage("mark", mark_container)


@app.get("/")
async def redirect_root():
    return RedirectResponse(url="/docs")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/{storage}/{file_id}")
def serve_files(storage: str = Path(...), file_id: str = Path(...)):
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
        print("StreamResponse")
        return StreamingResponse(
            file.object.as_stream(),
            media_type=file.content_type,
            headers={"Content-Disposition": "inline"},
        )

    except ObjectDoesNotExistError:
        return ORJSONResponse({"detail": "Not found"}, status_code=404)


STATIC_DIR = conf.static


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=conf.server.host, port=conf.server.port)

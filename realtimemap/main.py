import time

from fastapi import Request

from core.app import create_app
from core.config import conf

app = create_app()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


STATIC_DIR = conf.static


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=conf.server.host, port=conf.server.port)

from core.app import create_app
from core.config import conf

app = create_app()


STATIC_DIR = conf.static


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=conf.server.host, port=conf.server.port)

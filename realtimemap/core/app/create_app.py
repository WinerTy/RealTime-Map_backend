from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_babel import BabelConfigs, BabelMiddleware
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from api.v1 import router as v1_router
from core.config import conf
from .admin import setup_admin
from .lifespan import lifespan
from .socket import sio_app

ROOT_DIR = Path(__file__).parent.parent


def setup_pagination(app: FastAPI) -> None:
    add_pagination(app)


# pybabel init -i messages.pot -d i18n -l en -D messages
# pybabel compile -d i18n -D messages
def add_babel_middleware(app: FastAPI) -> None:
    babel = BabelConfigs(
        ROOT_DIR=ROOT_DIR,
        BABEL_DEFAULT_LOCALE="en",
        BABEL_TRANSLATION_DIRECTORY="i18n",
    )
    app.add_middleware(BabelMiddleware, babel_configs=babel)


def add_routers(app: FastAPI):
    app.include_router(v1_router)


def mount_socket_io(app: FastAPI) -> None:
    app.mount("/ws", app=sio_app)


def setup_file_storage():
    pass


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)
    app.mount(
        "/static", StaticFiles(directory=ROOT_DIR.parent / conf.static), name="static"
    )
    add_routers(app)
    add_babel_middleware(app)
    setup_pagination(app)
    setup_admin(app)
    setup_file_storage()  # FIX
    mount_socket_io(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

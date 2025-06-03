from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_babel import BabelConfigs, BabelMiddleware
from fastapi_pagination import add_pagination
from starlette.staticfiles import StaticFiles

from api.v1 import router as v1_router
from core.config import conf
from .lifespan import lifespan

ROOT_DIR = Path(__file__).parent.parent


def setup_pagination(app: FastAPI) -> None:
    add_pagination(app)


def add_babel_middleware(app: FastAPI) -> None:
    babel = BabelConfigs(
        ROOT_DIR=ROOT_DIR,
        BABEL_DEFAULT_LOCALE="en",
        BABEL_TRANSLATION_DIRECTORY="i18n",
    )
    app.add_middleware(BabelMiddleware, babel_configs=babel)


def add_routers(app: FastAPI):
    app.include_router(v1_router)


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)
    app.mount(
        "/static", StaticFiles(directory=ROOT_DIR.parent / conf.static), name="static"
    )
    add_routers(app)
    add_babel_middleware(app)
    setup_pagination(app)
    return app

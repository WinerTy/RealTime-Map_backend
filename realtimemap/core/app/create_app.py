import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination
from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy_file.storage import StorageManager
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.staticfiles import StaticFiles

from api.v1 import router as v1_router
from core.admin.admin import setup_admin
from core.config import conf
from .lifespan import lifespan
from .socket import sio_app

ROOT_DIR = Path(__file__).parent.parent


def setup_pagination(app: FastAPI) -> None:
    add_pagination(app)


def setup_logging() -> None:
    os.makedirs("logs", exist_ok=True)


def add_header_middleware(app: FastAPI) -> None:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=[conf.server.domains])


def add_routers(app: FastAPI):
    app.include_router(v1_router)


def mount_socket_io(app: FastAPI) -> None:
    app.mount("/socket.io", app=sio_app)


def setup_file_storage():
    os.makedirs("static", exist_ok=True)
    os.makedirs("uploads/default", exist_ok=True)
    os.makedirs("uploads/marks", exist_ok=True)
    os.makedirs("uploads/users", exist_ok=True)
    os.makedirs("uploads/category", exist_ok=True)

    default_container = LocalStorageDriver("uploads").get_container("default")
    category_container = LocalStorageDriver("uploads").get_container("category")
    mark_container = LocalStorageDriver("uploads").get_container("marks")
    users_container = LocalStorageDriver("uploads").get_container("users")

    StorageManager.add_storage("default", default_container)
    StorageManager.add_storage("category", category_container)
    StorageManager.add_storage("marks", mark_container)
    StorageManager.add_storage("users", users_container)


def create_app() -> FastAPI:
    setup_file_storage()
    setup_logging()
    app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)
    app.mount(
        "/static", StaticFiles(directory=ROOT_DIR.parent / conf.static), name="static"
    )
    add_header_middleware(app)
    add_routers(app)
    mount_socket_io(app)
    setup_pagination(app)
    setup_admin(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

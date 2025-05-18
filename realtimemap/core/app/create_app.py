from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import auth_router
from .lifespan import lifespan


def add_routers(app: FastAPI):
    app.include_router(auth_router)


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)
    add_routers(app)
    return app

from fastapi import FastAPI
from fastapi_amis_admin.admin import AdminSite, Settings

from core.config import conf
from .admin_model import AdminCategory


def setup_admin(app: FastAPI) -> None:
    adm = AdminSite(
        settings=Settings(
            database_url_async=str(conf.db.url),
            host=conf.server.host,
            port=conf.server.port,
        )
    )
    adm.register_admin(AdminCategory)
    adm.mount_app(app)

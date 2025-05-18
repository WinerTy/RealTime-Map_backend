from fastapi_users.authentication import BearerTransport

from core.config import conf

bearer_transport = BearerTransport(
    tokenUrl=conf.api.v1.auth.login_url,
)

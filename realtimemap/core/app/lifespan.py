from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_limiter import FastAPILimiter
from redis import asyncio as asyncredis
from starlette.templating import Jinja2Templates
from yookassa import Configuration

from core.config import conf
from database.helper import db_helper
from integrations.payment.yookassa import YookassaClient
from utils.cache import OrJsonEncoder, custom_key_builder

# Говнокод ON
ROOT_DIR = Path(__file__).parent.parent.parent
# Говнокод OFF


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = asyncredis.from_url(str(conf.redis.url))
    await FastAPILimiter.init(redis=redis)
    app.state.redis = redis
    app.state.root_dir = ROOT_DIR
    app.state.templates = Jinja2Templates(directory=ROOT_DIR / "templates")
    FastAPICache.init(
        RedisBackend(redis),
        prefix=conf.redis.prefix,
        coder=OrJsonEncoder,
        key_builder=custom_key_builder,
    )
    Configuration.secret_key = conf.payment.secret_key
    Configuration.account_id = conf.payment.shop_id
    yookassa_client = YookassaClient()
    app.state.yookassa_client = yookassa_client
    yield
    await FastAPILimiter.close()
    await db_helper.dispose()

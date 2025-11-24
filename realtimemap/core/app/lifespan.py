from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_limiter import FastAPILimiter
from redis import asyncio as asyncredis
from yookassa import Configuration

from core.config import conf
from database.helper import db_helper
from integrations.payment.yookassa import YookassaClient
from modules.events.bus import EventType, event_bus
from modules.events.gamefication_handler import GameFicationEventHandler
from utils.cache import OrJsonEncoder, custom_key_builder
from .templating import TemplateManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = asyncredis.from_url(str(conf.redis.url))
    await FastAPILimiter.init(redis=redis)
    app.state.redis = redis
    app.state.templates = TemplateManager(conf.template_dir)
    FastAPICache.init(
        RedisBackend(redis),
        prefix=conf.redis.prefix,
        coder=OrJsonEncoder,
        key_builder=custom_key_builder,  # noqa
    )
    Configuration.secret_key = conf.payment.secret_key
    Configuration.account_id = conf.payment.shop_id
    yookassa_client = YookassaClient()
    app.state.yookassa_client = yookassa_client
    gamefication_handler = GameFicationEventHandler()
    for event_type in [
        EventType.MARK_CREATE,
    ]:
        event_bus.subscribe(event_type, gamefication_handler.handle_exp_event)
    yield
    await FastAPILimiter.close()
    await db_helper.dispose()

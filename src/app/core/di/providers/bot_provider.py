import logging
from collections.abc import AsyncIterable

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import (
    BaseEventIsolation,
    BaseStorage,
    DefaultKeyBuilder,
)
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisEventIsolation, RedisStorage
from aiogram.types import TelegramObject
from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    provide,
)
from dishka.integrations.aiogram import setup_dishka
from orjson import orjson
from redis.asyncio import Redis

from app.bot import handlers, middlewares
from app.core.types import TelegramId

from ...config import settings


class BotProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_bot(self) -> AsyncIterable[Bot]:
        try:
            if settings.get("bot.use_local_server"):
                session = AiohttpSession(
                    api=TelegramAPIServer.from_base(
                        base=settings.get("bot.api_server_base"),
                        is_local=settings.get("bot.is_local"),
                    ),
                    json_loads=orjson.loads,
                )
            else:
                session = AiohttpSession()

            async with Bot(
                token=settings.get("bot.token"),
                session=session,
                default=DefaultBotProperties(
                    parse_mode=ParseMode.HTML,
                    allow_sending_without_reply=True,
                ),
            ) as bot:
                yield bot
        except Exception as e:
            logging.exception(e)


class DispatcherProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_dispatcher(
        self,
        container: AsyncContainer,
        event_isolation: BaseEventIsolation,
        fsm_storage: BaseStorage,
    ) -> Dispatcher:
        dp = Dispatcher(
            storage=fsm_storage,
            events_isolation=event_isolation,
        )
        setup_dishka(container=container, router=dp)
        middlewares.setup(dp)
        handlers.setup(dp)
        return dp

    @provide
    async def provide_fsm_storage(self) -> BaseStorage:
        fsm_type = settings.get("bot.bot.fsm_type")
        if fsm_type == "memory":
            return MemoryStorage()
        elif fsm_type == "redis":
            redis = Redis(
                host=settings.get("redis.host"),
                port=settings.get("redis.port"),
                db=settings.get("redis.db"),
                password=settings.get("redis.password"),
            )
            return RedisStorage(
                redis,
                json_loads=orjson.loads,
                json_dumps=orjson.dumps,
                key_builder=DefaultKeyBuilder(with_destiny=True),
            )
        else:
            return MemoryStorage()

    @provide
    async def provide_event_isolation(
        self,
        redis: Redis,
    ) -> BaseEventIsolation:
        return RedisEventIsolation(redis)


class TelegramIdProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def provide_telegram_id(
        self,
        request: TelegramObject,
    ) -> TelegramId:
        if hasattr(request, "from_user") and request.from_user:
            return request.from_user.id
        raise ValueError("Telegram user ID not found in request")

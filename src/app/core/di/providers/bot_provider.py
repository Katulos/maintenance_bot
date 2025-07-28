import logging
from collections.abc import AsyncIterable

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import (
    BaseEventIsolation,
    BaseStorage,
    DefaultKeyBuilder,
)
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
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
from app.bot.sessions.session import SmartSession
from app.core.config.bot import BotConfig, BotFsmType
from app.core.config.main import Config


class BotProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_bot(self, config: BotConfig) -> AsyncIterable[Bot]:
        try:
            if config.use_local_server:
                session = SmartSession(
                    api=TelegramAPIServer.from_base(
                        base=config.api_server_base,
                        is_local=config.is_local,
                    ),
                    json_loads=orjson.loads,
                )
            else:
                session = SmartSession(
                    json_loads=orjson.loads,
                )

            async with Bot(
                token=config.token,
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
    def provide_dispatcher(
        self,
        config: Config,
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
    def provide_fsm_storage(self, config: Config) -> BaseStorage:
        match config.bot.fsm_type:
            case BotFsmType.MEMORY:
                return MemoryStorage()
            case BotFsmType.REDIS:
                redis = Redis(
                    host=config.redis.host,
                    port=config.redis.port,
                    db=config.redis.db,
                    password=config.redis.password,
                )
                return RedisStorage(
                    redis,
                    json_loads=orjson.loads,
                    json_dumps=orjson.dumps,
                    key_builder=DefaultKeyBuilder(with_destiny=True),
                )
            case _:
                return MemoryStorage()

    @provide
    def provide_event_isolation(self) -> BaseEventIsolation:
        return BaseEventIsolation()

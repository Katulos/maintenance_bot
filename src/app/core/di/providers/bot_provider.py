import logging
from collections.abc import AsyncIterable

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import (
    BaseEventIsolation,
    BaseStorage,
)
from aiogram.fsm.storage.memory import MemoryStorage
from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    provide,
)
from dishka.integrations.aiogram import setup_dishka
from orjson import orjson

from app.bot import handlers, middlewares
from app.bot.sessions.session import SmartSession
from app.core.config.bot import BotConfig
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
    def provide_fsm_storage(self) -> BaseStorage:
        return MemoryStorage()

    @provide
    def provide_event_isolation(self) -> BaseEventIsolation:
        pass

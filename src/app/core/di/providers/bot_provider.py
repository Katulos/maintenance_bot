import logging
from collections.abc import AsyncIterable

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram_dialog.api.protocols import MessageManagerProtocol
from aiogram_dialog.manager.message_manager import MessageManager
from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    provide,
)
from dishka.integrations.aiogram import setup_dishka

from app.core.config.bot import BotConfig


class BotProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_bot(self, config: BotConfig) -> AsyncIterable[Bot]:
        try:
            session = AiohttpSession()
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
        container: AsyncContainer,
        config: BotConfig,
        message_manager: MessageManagerProtocol,
    ) -> Dispatcher:
        dp = Dispatcher()
        setup_dishka(container=container, router=dp)
        return dp


class DialogManagerProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_manager(self) -> MessageManagerProtocol:
        return MessageManager()

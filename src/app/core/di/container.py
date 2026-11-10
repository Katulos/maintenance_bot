from dishka import AsyncContainer, make_async_container
from dishka.integrations.aiogram import AiogramProvider
from dishka.integrations.fastapi import FastapiProvider

from .providers.bot_provider import (
    BotProvider,
    DispatcherProvider,
    TelegramIdProvider,
)
from .providers.db_provider import DbProvider
from .providers.fastapi_command_provider import (
    FastAPICommandProvider,
)
from .providers.odoo_provider import OdooProvider
from .providers.redis_provider import RedisProvider
from .providers.scheduler_provider import SchedulerProvider


def get_async_container() -> AsyncContainer:
    providers = [
        #
        AiogramProvider(),
        BotProvider(),
        DispatcherProvider(),
        TelegramIdProvider(),
        #
        SchedulerProvider(),
        #
        RedisProvider(),
        #
        DbProvider(),
        #
        OdooProvider(),
        #
        FastapiProvider(),
        FastAPICommandProvider(),
    ]
    container = make_async_container(*providers)
    return container

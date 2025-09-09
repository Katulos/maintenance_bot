import pathlib

from dishka import AsyncContainer, make_async_container
from dishka.integrations.aiogram import AiogramProvider
from dishka.integrations.fastapi import FastapiProvider

from app.core.di.providers.bot_provider import (
    BotProvider,
    DispatcherProvider,
    TelegramIdProvider,
)
from app.core.di.providers.config_provider import ConfigProvider
from app.core.di.providers.db_provider import DbProvider
from app.core.di.providers.fastapi_command_provider import (
    FastAPICommandProvider,
)
from app.core.di.providers.odoo_provider import OdooProvider
from app.core.di.providers.redis_provider import RedisProvider
from app.core.di.providers.scheduler_provider import SchedulerProvider


def get_async_container(config_path: pathlib.Path) -> AsyncContainer:
    providers = [
        ConfigProvider(config_path),
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

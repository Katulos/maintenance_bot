import pathlib

from dishka import AsyncContainer, make_async_container
from dishka.integrations.aiogram import AiogramProvider

from app.core.di.providers.bot_provider import (
    BotProvider,
    DispatcherProvider,
)
from app.core.di.providers.config_provider import ConfigProvider
from app.core.di.providers.odoo_provider import OdooProvider
from app.core.di.providers.redis_provider import RedisProvider


def get_async_container(config_path: pathlib.Path) -> AsyncContainer:
    providers = [
        ConfigProvider(config_path),
        #
        AiogramProvider(),
        BotProvider(),
        DispatcherProvider(),
        #
        OdooProvider(),
        #
        RedisProvider(),
    ]
    container = make_async_container(*providers)
    return container

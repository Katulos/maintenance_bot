import logging
import pathlib
from functools import partial

from aiogram import Bot, Dispatcher

from app.core.config.main import Config
from app.core.di.container import get_async_container

logging.basicConfig(level=logging.INFO)


async def _aiogram_on_startup_polling(
    dispatcher: Dispatcher,
    bot: Bot,
    config: Config,
) -> None:
    await bot.delete_webhook()


async def _aiogram_on_shutdown_polling(
    dispatcher: Dispatcher,
    bot: Bot,
    config: Config,
) -> None:
    await bot.session.close()
    await dispatcher.storage.close()


async def run(config_path: pathlib.Path) -> None:
    _container = get_async_container(config_path)

    config = await _container.get(Config)

    bot = await _container.get(Bot)

    dp = await _container.get(Dispatcher)

    dp.startup.register(
        partial(_aiogram_on_startup_polling, dp, bot, config),
    )
    dp.shutdown.register(
        partial(_aiogram_on_shutdown_polling, dp, bot, config),
    )
    await dp.start_polling(bot)

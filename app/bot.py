from __future__ import annotations

import asyncio
import os
import pathlib
from typing import TYPE_CHECKING

import tenacity
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram_dialog import setup_dialogs
from aiogram_fsm_sqlitestorage import SQLiteStorage
from fluent.runtime import FluentLocalization, FluentResourceLoader
from orjson import orjson

from . import dialogs, utils
from .config import settings
from .handlers import user
from .middlewares import (
    AntiFloodMiddleware,
    I18nMiddleware,
    StructLoggingMiddleware,
)
from .middlewares.odoo_register import OdooRegisterMiddleware
from .utils import connect_to_services

if TYPE_CHECKING:
    import structlog


async def create_odoo_connections(dp: Dispatcher) -> None:
    logger: structlog.typing.FilteringBoundLogger = dp["business_logger"]

    logger.debug(
        "Connecting to Odoo",
        host=settings.odoo.host,
        port=settings.odoo.port,
    )
    try:
        odoo = await connect_to_services.wait_odoo(
            logger=dp["odoo_logger"],
            host=settings.odoo.host,
            port=settings.odoo.port,
            protocol=settings.odoo.protocol,
        )
    except tenacity.RetryError:
        logger.exception(
            "Failed to connect to Odoo",
            host=settings.odoo.host,
            port=settings.odoo.port,
        )
        exit(1)
    else:
        logger.debug(
            "Successfully connected to Odoo",
            host=settings.odoo.host,
            port=settings.odoo.port,
        )
    dp["odoo"] = odoo


def make_i18n_middleware() -> I18nMiddleware:
    default_locale = settings.app.default_locale
    supported_locales = settings.app.supported_locales
    loader = FluentResourceLoader(
        os.path.join(
            pathlib.Path(__file__).resolve().parent.parent,
            "locales",
            "{locale}",
        ),
    )
    l10ns = {
        locale: FluentLocalization(
            [locale, default_locale],
            ["main.ftl"],
            loader,
        )
        for locale in supported_locales
    }
    return I18nMiddleware(l10ns, default_locale)


def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(user.prepare_router())
    dp.include_router(dialogs.dialog)


def setup_middlewares(dp: Dispatcher) -> None:
    # logger middleware
    dp.update.outer_middleware(
        StructLoggingMiddleware(logger=dp["aiogram_logger"]),
    )

    # Check odoo registration middleware
    dp.message.middleware(AntiFloodMiddleware())
    dp.callback_query.middleware(AntiFloodMiddleware())

    # i18n middleware
    dp.message.middleware(make_i18n_middleware())
    dp.callback_query.middleware(make_i18n_middleware())

    # Check odoo registration middleware
    dp.message.middleware(OdooRegisterMiddleware())
    dp.callback_query.middleware(OdooRegisterMiddleware())


def setup_logging(dp: Dispatcher) -> None:
    dp["aiogram_logger"] = utils.logging.setup_logger(
        settings.app.logging_level,
    ).bind(type="aiogram")
    dp["business_logger"] = utils.logging.setup_logger(
        settings.app.logging_level,
    ).bind(type="business")
    dp["odoo_logger"] = utils.logging.setup_logger(
        settings.app.logging_level,
    ).bind(type="odoo")


async def setup_aiogram(dp: Dispatcher) -> None:
    setup_logging(dp)
    logger = dp["aiogram_logger"]
    await create_odoo_connections(dp)
    setup_handlers(dp)
    setup_middlewares(dp)
    logger.info("Configured aiogram")


async def aiogram_on_startup_polling(
    dispatcher: Dispatcher,
    bot: Bot,
) -> None:
    await setup_aiogram(dispatcher)


async def aiogram_on_shutdown_polling(
    dispatcher: Dispatcher,
    bot: Bot,
) -> None:
    await bot.session.close()
    await dispatcher.storage.close()


def main() -> None:
    aiogram_session_logger = utils.logging.setup_logger(
        settings.app.logging_level,
    ).bind(type="aiogram_session")

    session = utils.smart_session.SmartAiogramAiohttpSession(
        json_loads=orjson.loads,
        logger=aiogram_session_logger,
    )
    db_path = os.path.join(
        pathlib.Path(__file__).resolve().parent.parent,
        "data",
        "fsm_storage.db",
    )
    dp = Dispatcher(
        storage=SQLiteStorage(
            db_path=db_path,
        ),
    )
    # dp = Dispatcher(storage=MemoryStorage())

    bot = Bot(
        token=settings.bot.token,
        session=session,
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    dp["aiogram_session_logger"] = aiogram_session_logger

    dp.startup.register(aiogram_on_startup_polling)

    dp.shutdown.register(aiogram_on_shutdown_polling)
    setup_dialogs(dp)

    asyncio.run(dp.start_polling(bot))

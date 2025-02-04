from __future__ import annotations

import asyncio
import os
from typing import TYPE_CHECKING

import tenacity
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram_sqlite_storage.sqlitestore import SQLStorage
from fluent.runtime import FluentLocalization, FluentResourceLoader
from orjson import orjson

from . import utils
from .config import settings
from .handlers.user import prepare_router
from .middlewares import I18nMiddleware, StructLoggingMiddleware
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


def make_i18n_middleware():
    default_locale = settings.app.default_locale
    supported_locales = settings.app.supported_locales
    loader = FluentResourceLoader(
        os.path.join(
            os.path.dirname(__file__),
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
    dp.include_router(prepare_router())


def setup_middlewares(dp: Dispatcher) -> None:
    dp.update.outer_middleware(
        StructLoggingMiddleware(logger=dp["aiogram_logger"]),
    )
    dp.message.middleware(make_i18n_middleware())
    dp.callback_query.middleware(make_i18n_middleware())


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


def main():
    aiogram_session_logger = utils.logging.setup_logger(
        settings.app.logging_level,
    ).bind(type="aiogram_session")

    session = utils.smart_session.SmartAiogramAiohttpSession(
        json_loads=orjson.loads,
        logger=aiogram_session_logger,
    )

    dp = Dispatcher(storage=SQLStorage(settings.app.fsm_storage_path))

    bot = Bot(
        token=settings.bot.token,
        session=session,
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    dp["aiogram_session_logger"] = aiogram_session_logger

    dp.startup.register(aiogram_on_startup_polling)

    dp.shutdown.register(aiogram_on_shutdown_polling)

    asyncio.run(dp.start_polling(bot))

from __future__ import annotations

import asyncio

import aiojobs
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.telegram import TelegramAPIServer
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware
from aiohttp import web
from orjson import orjson

from . import handlers, web_handlers
from .config import settings
from .middlewares import StructLoggingMiddleware
from .utils import logging, smart_session


def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(handlers.user.prepare_router())


def setup_middlewares(dp: Dispatcher) -> None:
    dp.update.outer_middleware(
        StructLoggingMiddleware(logger=dp["aiogram_logger"]),
    )
    i18n = I18n(
        path=settings.app.BASE_DIR / "locales",
        domain="messages",
        default_locale=settings.app.default_locale,
    )
    dp.update.outer_middleware(
        SimpleI18nMiddleware(i18n),
    )


def setup_logging(dp: Dispatcher) -> None:
    dp["aiogram_logger"] = logging.setup_logger().bind(type="aiogram")
    dp["business_logger"] = logging.setup_logger().bind(type="business")


async def setup_aiogram(dp: Dispatcher) -> None:
    setup_logging(dp)
    logger = dp["aiogram_logger"]
    logger.debug("Configuring aiogram")
    setup_handlers(dp)
    setup_middlewares(dp)
    logger.info("Configured aiogram")


async def aiohttp_on_startup(app: web.Application) -> None:
    dp: Dispatcher = app["dp"]
    workflow_data = {"app": app, "dispatcher": dp}
    if "bot" in app:
        workflow_data["bot"] = app["bot"]
    await dp.emit_startup(**workflow_data)


async def aiohttp_on_shutdown(app: web.Application) -> None:
    dp: Dispatcher = app["dp"]
    for i in [app, *app._subapps]:
        if "scheduler" in i:
            scheduler: aiojobs.Scheduler = i["scheduler"]
            scheduler._closed = True
            while scheduler.pending_count != 0:
                dp["aiogram_logger"].info(
                    f"Waiting for {scheduler.pending_count} tasks to complete",
                )
                await asyncio.sleep(1)
    workflow_data = {"app": app, "dispatcher": dp}
    if "bot" in app:
        workflow_data["bot"] = app["bot"]
    await dp.emit_shutdown(**workflow_data)


async def aiogram_on_startup_webhook(
    dispatcher: Dispatcher,
    bot: Bot,
) -> None:
    await setup_aiogram(dispatcher)
    webhook_logger = dispatcher["aiogram_logger"].bind(
        webhook_url=settings.app.main_webhook_address,
    )
    webhook_logger.debug("Configuring webhook")
    await bot.set_webhook(
        url=settings.app.main_webhook_address.format(
            token=settings.bot.bot_token,
            bot_id=settings.bot.bot_token.split(":")[0],
        ),
        allowed_updates=dispatcher.resolve_used_update_types(),
        secret_token=settings.app.main_webhook_secret_token,
    )
    webhook_logger.info("Configured webhook")


async def aiogram_on_shutdown_webhook(
    dispatcher: Dispatcher,
    bot: Bot,
) -> None:
    dispatcher["aiogram_logger"].debug("Stopping webhook")
    await bot.session.close()
    await dispatcher.storage.close()
    dispatcher["aiogram_logger"].info("Stopped webhook")


async def aiogram_on_startup_polling(
    dispatcher: Dispatcher,
    bot: Bot,
) -> None:
    if settings.bot.drop_previous_updates:
        await bot.delete_webhook(drop_pending_updates=True)
    await setup_aiogram(dispatcher)
    dispatcher["aiogram_logger"].info("Started polling")


async def aiogram_on_shutdown_polling(
    dispatcher: Dispatcher,
    bot: Bot,
) -> None:
    dispatcher["aiogram_logger"].debug("Stopping polling")
    await bot.session.close()
    await dispatcher.storage.close()
    dispatcher["aiogram_logger"].info("Stopped polling")


async def setup_aiohttp_app(
    bot: Bot,
    dp: Dispatcher,
) -> web.Application:
    scheduler = aiojobs.Scheduler()
    app = web.Application()
    subapps: list[tuple[str, web.Application]] = [
        ("/tg/webhooks/", web_handlers.tg_updates_app),
    ]
    for prefix, subapp in subapps:
        subapp["bot"] = bot
        subapp["dp"] = dp
        subapp["scheduler"] = scheduler
        app.add_subapp(prefix, subapp)
    app["bot"] = bot
    app["dp"] = dp
    app["scheduler"] = scheduler
    app.on_startup.append(aiohttp_on_startup)
    app.on_shutdown.append(aiohttp_on_shutdown)
    return app


def main() -> None:
    aiogram_session_logger = logging.setup_logger().bind(
        type="aiogram_session",
    )
    if settings.bot.use_custom_api_server:
        session = smart_session.SmartAiogramAiohttpSession(
            api=TelegramAPIServer(
                base=settings.bot.custom_api_server_base,
                file=settings.bot.custom_api_server_file,
                is_local=settings.bot.custom_api_server_is_local,
            ),
            json_loads=orjson.loads,
            logger=aiogram_session_logger,
        )
    else:
        session = smart_session.SmartAiogramAiohttpSession(
            json_loads=orjson.loads,
            logger=aiogram_session_logger,
        )
    bot = Bot(
        settings.bot.token,
        session=session,
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    dp = Dispatcher(
        storage=MemoryStorage(),
    )
    dp["aiogram_session_logger"] = aiogram_session_logger

    if settings.bot.use_webhook:
        dp.startup.register(aiogram_on_startup_webhook)
        dp.shutdown.register(aiogram_on_shutdown_webhook)
        web.run_app(
            asyncio.run(setup_aiohttp_app(bot, dp)),
            handle_signals=True,
            host=settings.bot.main_webhook_listening_host,
            port=settings.bot.main_webhook_listening_port,
        )
    else:
        dp.startup.register(aiogram_on_startup_polling)
        dp.shutdown.register(aiogram_on_shutdown_polling)
        asyncio.run(dp.start_polling(bot))

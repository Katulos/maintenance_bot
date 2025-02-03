from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import aiojobs
import tenacity
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.client.telegram import TelegramAPIServer
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware
from aiohttp import web
from orjson import orjson

from . import handlers, web_handlers
from .config import settings
from .middlewares import StructLoggingMiddleware
from .utils import connect_to_services, logging, smart_session

if TYPE_CHECKING:
    import structlog


async def create_odoo_connections(dp: Dispatcher) -> None:
    logger: structlog.typing.FilteringBoundLogger = dp["business_logger"]
    logger.debug("Connecting to Odoo")
    try:
        odoo = await connect_to_services.wait_odoo(
            logger=dp["odoo_logger"],
            host=settings.odoo.host,
            port=settings.odoo.port,
            protocol=settings.odoo.protocol,
        )
    except tenacity.RetryError:
        logger.exception("Failed to connect to Odoo")
        exit(1)
    else:
        logger.debug("Successfully connected to Odoo")
    dp["odoo"] = odoo


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
    dp["odoo_logger"] = logging.setup_logger().bind(type="odoo")


async def setup_aiogram(dp: Dispatcher) -> None:
    setup_logging(dp)
    logger = dp["aiogram_logger"]
    logger.debug("Configuring aiogram")
    await create_odoo_connections(dp)
    setup_handlers(dp)
    setup_middlewares(dp)
    logger.info("Configured aiogram")


async def setup_default_commands(bot: Bot) -> None:
    await bot.delete_my_commands()
    await bot.set_my_commands(
        commands=[
            types.BotCommand(command="start", description="Start Bot"),
            types.BotCommand(command="help", description="Get Help"),
            types.BotCommand(
                command="equipments",
                description="Get My Equipments",
            ),
        ],
    )


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
    webhook_logger.info("Setup default commands")
    await setup_default_commands(bot)


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
    await setup_default_commands(bot)
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

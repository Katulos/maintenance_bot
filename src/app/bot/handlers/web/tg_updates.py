import logging
import secrets
from types import NoneType
from typing import Any

import aiohttp.web
import aiojobs
import orjson
from aiogram import Bot, Dispatcher, types
from aiohttp import web

from app.core.config.bot import BotConfig


def create_tg_updates_app(config: BotConfig) -> web.Application:
    tg_updates_app = web.Application()

    async def process_update(
        upd: types.Update,
        bot: Bot,
        dp: Dispatcher,
        workflow_data: dict[str, Any],
    ) -> None:
        await dp.feed_webhook_update(bot, upd, **workflow_data)

    async def execute(req: web.Request) -> web.Response:
        if config.webhook_secret_token is NoneType:
            logging.critical("webhook_secret_token is not defined")
            raise aiohttp.web.HTTPNotFound
        else:
            if not secrets.compare_digest(
                req.headers.get("X-Telegram-Bot-Api-Secret-Token", ""),
                config.webhook_secret_token,
            ):
                logging.error("X-Telegram-Bot-Api-Secret-Token not matched")
                raise aiohttp.web.HTTPNotFound

        if not secrets.compare_digest(
            req.match_info["bot_id"],
            str(config.bot_id),
        ):
            logging.error("bot_id not matched")
            raise aiohttp.web.HTTPNotFound

        dp: Dispatcher = req.app["dp"]
        scheduler: aiojobs.Scheduler = req.app["scheduler"]

        if scheduler.pending_count > config.webhook_max_updates_in_queue:
            raise web.HTTPTooManyRequests
        if scheduler.closed:
            raise web.HTTPServiceUnavailable(reason="Closed queue")

        await scheduler.spawn(
            process_update(
                types.Update(**(await req.json(loads=orjson.loads))),
                req.app["bot"],
                dp,
                {"dp": dp},
            ),
        )

        return web.Response()

    tg_updates_app.add_routes(
        [web.post("/bot/{bot_id}", execute)],
    )

    return tg_updates_app

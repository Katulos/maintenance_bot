import asyncio
import pathlib
from collections.abc import Callable
from typing import Any

import asyncclick as click

from app.api import api as _api
from app.bot import bot as _tgbot


def common_command_options(func: Callable[..., Any]) -> Callable[..., Any]:
    func = click.option(
        "--config",
        "-c",
        type=click.Path(dir_okay=False, path_type=pathlib.Path),
        default="config.yml",
        help="Path to config file. Defaults to config.yml.",
    )(func)
    return click.pass_context(func)


@click.group()
async def cli() -> None:
    pass


@cli.group()
async def run() -> None:
    """Run application components."""
    pass


@run.command()
@common_command_options
async def api(ctx: click.Context, config: pathlib.Path) -> None:
    """Run API server."""
    try:
        await _api.run(config)
    except asyncio.exceptions.CancelledError:
        pass


@run.command()
@common_command_options
async def bot(ctx: click.Context, config: pathlib.Path) -> None:
    """Run Telegram Bot application."""
    try:
        await _tgbot.run(config)
    except asyncio.exceptions.CancelledError:
        pass


@run.command()
@common_command_options
async def client(ctx: click.Context, config: pathlib.Path) -> None:
    """Run Telegram Client application."""
    pass

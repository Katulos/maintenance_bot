import asyncio
import logging
import pathlib
from collections.abc import Callable
from typing import Any

import click
from alembic import command
from alembic.config import Config

from app.api import api as _api
from app.bot import bot as _tgbot
from app.core.config.db import DbConfig
from app.core.config.loader import ConfigLoader
from app.core.infrastructure.db.alembic.config import get_alembic_config_path
from app.scheduler import scheduler as _scheduler


def load_config_or_exit(config_path: pathlib.Path) -> DbConfig:
    if not config_path.exists():
        logging.critical("Config file not found")
        raise click.FileError(str(config_path), "Config file not found")
    return ConfigLoader.load_config(config_path).db


def with_alembic_config(
    config: DbConfig,
    callback: Callable[[Config], None],
) -> None:
    alembic_path_gen = get_alembic_config_path()
    try:
        alembic_path = next(alembic_path_gen)
    except StopIteration:
        logging.error("Alembic config path not found")
        return

    alembic_cfg = Config(str(alembic_path))
    alembic_cfg.set_main_option("sqlalchemy.url", config.dsn)
    callback(alembic_cfg)


@click.group()
def cli() -> None:
    """Main CLI group."""
    pass


@cli.group()
def run() -> None:
    """Run application components."""
    pass


@cli.group()
def migrations() -> None:
    """Database migrations management."""
    pass


def common_command_options(func: Callable[..., Any]) -> Callable[..., Any]:
    func = click.option(
        "--config",
        "-c",
        type=click.Path(dir_okay=False, path_type=pathlib.Path),
        default="config.yml",
        help="Path to config file. Defaults to config.yml.",
    )(func)
    return click.pass_context(func)


@run.command()
@common_command_options
def api(ctx: click.Context, config: pathlib.Path) -> None:
    """Run API server."""
    ctx.invoke(upgrade, config=config)
    logging.info("Running API server")
    _api.run(config)


@run.command()
@common_command_options
def bot(ctx: click.Context, config: pathlib.Path) -> None:
    """Run bot application."""
    ctx.invoke(upgrade, config=config)
    asyncio.run(_tgbot.run(config))


@run.command()
@common_command_options
def scheduler(ctx: click.Context, config: pathlib.Path) -> None:
    """Run scheduler."""
    ctx.invoke(upgrade, config=config)
    asyncio.run(_scheduler.run(config))


@migrations.command()
@common_command_options
@click.argument("message", required=True)
def autogenerate(
    ctx: click.Context,
    config: pathlib.Path,
    message: str,
) -> None:
    """Autogenerate new migration."""
    db_config = load_config_or_exit(config)
    with_alembic_config(
        db_config,
        lambda cfg: command.revision(cfg, autogenerate=True, message=message),
    )


@migrations.command()
@common_command_options
@click.argument("revision", default="head")
def upgrade(ctx: click.Context, config: pathlib.Path, revision: str) -> None:
    """Upgrade database to specified revision."""
    db_config = load_config_or_exit(config)
    with_alembic_config(db_config, lambda cfg: command.upgrade(cfg, revision))


@migrations.command()
@common_command_options
@click.argument("revision", default="head")
def downgrade(
    ctx: click.Context,
    config: pathlib.Path,
    revision: str,
) -> None:
    """Downgrade database to specified revision."""
    db_config = load_config_or_exit(config)
    with_alembic_config(
        db_config,
        lambda cfg: command.downgrade(cfg, revision),
    )

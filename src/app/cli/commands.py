import asyncio
import logging
from collections.abc import Callable

import click
from alembic import command
from alembic.config import Config

from app.api import api as _api
from app.bot import bot as _tgbot
from app.core.infrastructure.db.alembic.config import get_alembic_config_path
from app.scheduler import scheduler as _scheduler

from ..core.config import settings


def with_alembic_config(
    callback: Callable[[Config], None],
) -> None:
    alembic_path_gen = get_alembic_config_path()
    try:
        alembic_path = next(alembic_path_gen)
    except StopIteration:
        logging.error("Alembic config path not found")
        return

    alembic_cfg = Config(str(alembic_path))
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        settings.get("db.database_url"),
    )
    callback(alembic_cfg)


@click.group()
def cli() -> None:
    """Main CLI group."""
    debug = settings.get("core.debug")

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


@cli.group()
def run() -> None:
    """Run application components."""
    pass


@cli.group()
def migrations() -> None:
    """Database migrations management."""
    pass


@run.command()
def api(ctx: click.Context) -> None:
    """Run API server."""
    ctx.invoke(upgrade)
    logging.info("Running API server")
    _api.run()


@run.command()
def bot(ctx: click.Context) -> None:
    """Run bot application."""
    ctx.invoke(upgrade)
    asyncio.run(_tgbot.run())


@run.command()
def scheduler(ctx: click.Context) -> None:
    """Run scheduler."""
    ctx.invoke(upgrade)
    asyncio.run(_scheduler.run())


@migrations.command()
@click.argument("message", required=True)
def autogenerate(
    message: str,
) -> None:
    """Autogenerate new migration."""
    with_alembic_config(
        lambda cfg: command.revision(cfg, autogenerate=True, message=message),
    )


@migrations.command()
@click.argument("revision", default="head")
def upgrade(revision: str) -> None:
    """Upgrade database to specified revision."""
    with_alembic_config(lambda cfg: command.upgrade(cfg, revision))


@migrations.command()
@click.argument("revision", default="head")
def downgrade(
    revision: str,
) -> None:
    """Downgrade database to specified revision."""
    with_alembic_config(
        lambda cfg: command.downgrade(cfg, revision),
    )

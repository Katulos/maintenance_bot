import pathlib
import uuid

import pytest
import pytest_asyncio
from alembic.config import Config
from dishka import AsyncContainer
from yarl import URL

from app.core.config.db import DbConfig
from app.core.di.container import get_async_container
from app.core.infrastructure.db.alembic.config import get_alembic_config_path
from tests.utils.sqlachemy_utils import (
    create_database,
    database_exists,
    drop_database,
)


@pytest_asyncio.fixture(scope="session")
async def db_url():
    container: AsyncContainer = get_async_container(
        config_path=pathlib.Path("config.yml"),
    )
    db_config = await container.get(DbConfig)
    original_dsn = db_config.dsn

    url = URL(original_dsn)
    is_sqlite = "sqlite" in url.scheme

    if is_sqlite:
        original_path = pathlib.Path(
            url.path[1:] if url.path.startswith("/") else url.path,
        )
        test_db_path = original_path.with_name(
            f"{original_path.stem}.pytest.{uuid.uuid4().hex}{original_path.suffix}",
        )
        test_dsn = f"{url.scheme}:///{test_db_path.as_posix()}"
    else:
        tmp_name = f"{uuid.uuid4().hex}_pytest"
        test_dsn = str(url.with_path(tmp_name))
        if not await database_exists(test_dsn):
            await create_database(test_dsn)

    try:
        yield test_dsn
    finally:
        await drop_database(test_dsn)
        await container.close()


@pytest.fixture(scope="session")
def alembic_config(db_url):
    alembic_path_gen = get_alembic_config_path()
    alembic_path = next(alembic_path_gen)
    alembic_cfg = Config(str(alembic_path))
    alembic_cfg.set_main_option(
        "script_location",
        str(alembic_path.parent / "migrations"),
    )
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    return alembic_cfg

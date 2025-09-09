import asyncio
import logging
import pathlib

from arq import Worker

from app.core.config.main import Config
from app.core.di.container import get_async_container

logger = logging.getLogger("app.scheduler")


async def run(config_path: pathlib.Path) -> None:
    _container = get_async_container(config_path)
    config = await _container.get(Config)

    if config.core.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    worker = await _container.get(Worker)

    try:
        await worker.async_run()
    except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
        pass
    except Exception as e:
        logger.error(e)
    finally:
        await _container.close()
        await worker.close()

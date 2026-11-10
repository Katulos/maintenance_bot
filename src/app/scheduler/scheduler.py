import asyncio
import logging
import sys

from arq import Worker

from app.core.di.container import get_async_container

_logger = logging.getLogger("app.scheduler")


async def run() -> None:
    _container = get_async_container()

    worker = await _container.get(Worker)

    try:
        await worker.async_run()
    except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
        pass
    except Exception as e:
        _logger.error(e)
        sys.exit(1)
    finally:
        await _container.close()
        await worker.close()

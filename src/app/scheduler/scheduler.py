import asyncio
import logging
import sys

from arq import Worker

from app.core.di.container import get_async_container


async def run() -> None:
    container = get_async_container()

    worker = await container.get(Worker)

    try:
        await worker.async_run()
    except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
        pass
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    finally:
        await container.close()
        await worker.close()

import asyncio
import pathlib
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

import app
from app.api.exceptions import include_exception_handlers
from app.api.v1.routes import include_routers
from app.core.config.main import Config
from app.core.di.container import get_async_container


@asynccontextmanager
async def lifespan(fast_app: FastAPI) -> AsyncIterator[None]:
    yield
    await fast_app.state.dishka_container.close()


fast_app = FastAPI(
    title="My Cool API",
    lifespan=lifespan,
    root_path="/api",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    version=app.__version__,
)


def run(config_path: pathlib.Path) -> None:
    _container = get_async_container(config_path)

    setup_dishka(container=_container, app=fast_app)

    config = asyncio.run(_container.get(Config))

    include_routers(fast_app)
    include_exception_handlers(fast_app)

    uvicorn.run(
        fast_app,
        port=config.api.port,
        host=config.api.bind,
        access_log=config.api.enable_access_log,
        # log_config=None,
    )

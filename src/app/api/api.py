from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

import app
from app.api.exceptions import include_exception_handlers
from app.api.v1.routes import include_routers
from app.core.di.container import get_async_container

from ..core.config import settings


@asynccontextmanager
async def lifespan(fast_app: FastAPI) -> AsyncGenerator[None]:
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


def run() -> None:
    _container = get_async_container()

    setup_dishka(container=_container, app=fast_app)

    include_routers(fast_app)
    include_exception_handlers(fast_app)

    uvicorn.run(
        fast_app,
        port=settings.get("api.port"),
        host=settings.get("api.bind"),
        access_log=settings.get("api.enable_access_log"),
        # log_config=None,
    )

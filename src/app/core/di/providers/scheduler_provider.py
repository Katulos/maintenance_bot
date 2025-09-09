from collections.abc import AsyncIterable

from arq import Worker, cron
from arq.connections import ArqRedis, RedisSettings, create_pool
from arq.typing import WorkerSettingsBase
from arq.worker import create_worker
from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    provide,
)
from dishka.integrations.arq import setup_dishka

from app.core.config.redis import RedisConfig
from app.scheduler.jobs.sync import sync_all, upsert_maintenance_request


def at_every_x_minutes(x: int, start: int = 0, end: int = 59):
    return {*list(range(start, end, x))}


class WorkerSettings(WorkerSettingsBase):
    pass


class SchedulerProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_worker_settings(self, pool: ArqRedis) -> WorkerSettings:
        settings = WorkerSettings()
        settings.redis_pool = pool
        settings.cron_jobs = [
            cron(
                sync_all,
                # hour=0,
                # minute=0,
                minute=at_every_x_minutes(1),
                run_at_startup=True,
            ),
        ]
        settings.functions = [upsert_maintenance_request]

        return settings

    @provide
    async def provide_worker(
        self,
        container: AsyncContainer,
        worker_settings: WorkerSettings,
    ) -> AsyncIterable[Worker]:
        worker = create_worker(worker_settings)
        setup_dishka(container=container, worker_settings=worker)
        yield worker

    @provide
    async def provide_pool(
        self,
        config: RedisConfig,
    ) -> AsyncIterable[ArqRedis]:
        pool = await create_pool(
            RedisSettings(
                host=config.host,
                port=config.port,
                database=config.db,
                username=config.username,
                password=config.password,
            ),
        )
        yield pool
        await pool.aclose()

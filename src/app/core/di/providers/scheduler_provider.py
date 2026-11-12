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

from ....scheduler.jobs import (
    sync_all,
    upsert_maintenance_request,
)
from ...config import settings


def _at_every_x_minutes(x: int, start: int = 0, end: int = 59):
    return {*list(range(start, end, x))}


def _at_every_x_hours(x: int, start: int = 0, end: int = 23):
    return {*list(range(start, end, x))}


class WorkerSettings(WorkerSettingsBase):
    redis_pool: ArqRedis
    functions = []


class SchedulerProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_worker_settings(self, pool: ArqRedis) -> WorkerSettings:
        settings = WorkerSettings()
        settings.redis_pool = pool
        settings.cron_jobs = [
            cron(
                sync_all,
                name="Sync Odoo",
                # hour=_at_every_x_hours(1),
                minute=_at_every_x_minutes(1),
                run_at_startup=True,
                # timeout=1500,
                # max_tries=5,
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
    ) -> AsyncIterable[ArqRedis]:
        pool = await create_pool(
            RedisSettings(
                host=settings.get("redis.host"),
                port=settings.get("redis.port"),
                database=settings.get("redis.db"),
                username=settings.get("redis.username"),
                password=settings.get("redis.password"),
            ),
        )
        yield pool
        await pool.aclose()

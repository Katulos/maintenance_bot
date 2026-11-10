import logging
from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from redis.asyncio.client import Redis

from ...config import settings


class RedisProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_redis(
        self,
    ) -> AsyncIterable[Redis]:
        try:
            async with Redis(
                host=settings.get("redis.host"),
                port=settings.get("redis.port"),
                db=settings.get("redis.db"),
                username=settings.get("redis.username"),
                password=settings.get("redis.password"),
            ) as redis:
                yield redis
        except Exception as e:
            logging.error(e)

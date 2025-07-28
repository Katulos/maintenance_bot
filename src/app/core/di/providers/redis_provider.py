import logging
from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from redis.asyncio.client import Redis

from app.core.config.redis import RedisConfig


class RedisProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_redis(
        self,
        config: RedisConfig,
    ) -> AsyncIterable[Redis]:
        try:
            async with Redis(
                host=config.host,
                port=config.port,
                db=config.db,
                username=config.username,
                password=config.password,
            ) as redis:
                yield redis
        except Exception as e:
            logging.exception(e)

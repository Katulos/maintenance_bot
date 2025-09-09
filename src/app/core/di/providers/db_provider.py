import base64
import hashlib
from collections.abc import AsyncIterable
from typing import Protocol

from cryptography.fernet import Fernet
from dishka import AnyOf, Provider, Scope, provide
from sqlalchemy import make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config.db import DbConfig
from app.core.config.main import Config
from app.core.infrastructure.db.dao import DAO


class Committer(Protocol):
    async def commit(self) -> None:
        raise NotImplementedError


class DbProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_cipher_suite(self, config: Config) -> Fernet:
        secret_key = config.core.secret_key.encode()
        hashed_key = hashlib.sha256(secret_key).digest()
        key = base64.urlsafe_b64encode(hashed_key)
        return Fernet(key)

    @provide(scope=Scope.APP)
    async def provide_async_sessionmaker(
        self,
        engine: AsyncEngine,
        cipher_suite: Fernet,
    ) -> async_sessionmaker[AsyncSession]:
        class CipherAsyncSession(AsyncSession):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.cipher_suite = cipher_suite

        session_factory = async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
            autoflush=False,
            class_=CipherAsyncSession,
        )
        return session_factory

    @provide(scope=Scope.APP)
    async def provide_engine(
        self,
        config: DbConfig,
    ) -> AsyncIterable[AsyncEngine]:
        engine = create_async_engine(
            url=make_url(config.dsn),
            future=True,
            echo=config.echo,
        )
        yield engine
        await engine.dispose(close=True)

    @provide(scope=Scope.REQUEST)
    async def provide_session(
        self,
        engine: AsyncEngine,
    ) -> AsyncIterable[AnyOf[AsyncSession, Committer]]:
        async with AsyncSession(
            bind=engine,
            autoflush=False,
            expire_on_commit=False,
        ) as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def provide_dao(self, session: AsyncSession) -> DAO:
        return DAO(session)


# class DbProvider(Provider):
#     pass


# async def provide_cipher_suite(config: Config) -> Fernet:
#     secret_key = config.core.secret_key.encode()
#     hashed_key = hashlib.sha256(secret_key).digest()
#     key = base64.urlsafe_b64encode(hashed_key)
#     return Fernet(key)


# async def provide_async_engine(
#     config: DbConfig,
# ) -> AsyncIterator[AsyncEngine]:
#     connection_url = config.dsn
#     engine = create_async_engine(
#         url=make_url(connection_url),
#         future=True,
#         echo=config.echo,
#     )
#     yield engine
#     await engine.dispose()


# async def provide_async_sessionmaker(
#     engine: AsyncEngine,
#     cipher_suite: Fernet,
# ) -> async_sessionmaker[AsyncSession]:
#     class CipherAsyncSession(AsyncSession):
#         def __init__(self, **kwargs):
#             super().__init__(**kwargs)
#             self.cipher_suite = cipher_suite

#     session_factory = async_sessionmaker(
#         bind=engine,
#         expire_on_commit=False,
#         autoflush=False,
#         class_=CipherAsyncSession,
#     )
#     return session_factory


# async def provide_async_session(
#     session_factory: async_sessionmaker[AsyncSession],
# ) -> AsyncIterator[AsyncSession]:
#     async with session_factory() as session:
#         yield session


# async def provide_dao(session: AsyncSession) -> DAO:
#     return DAO(session)


# def db_provider() -> DbProvider:
#     provider = DbProvider()
#     provider.provide(provide_cipher_suite, scope=Scope.APP)
#     provider.provide(provide_async_engine, scope=Scope.APP)
#     provider.provide(provide_async_sessionmaker, scope=Scope.APP)
#     provider.provide(provide_async_session, scope=Scope.REQUEST)
#     provider.provide(provide_dao, scope=Scope.REQUEST)

#     return provider

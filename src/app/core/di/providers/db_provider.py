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

from app.core.infrastructure.db.dao import DAO

from ...config import settings


class Committer(Protocol):
    async def commit(self) -> None:
        raise NotImplementedError


class DbProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_cipher_suite(self) -> Fernet:
        secret_key = settings.get("db.core.secret_key").encode()
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
    ) -> AsyncIterable[AsyncEngine]:
        engine = create_async_engine(
            url=make_url(settings.get("db.database_url")),
            future=True,
            echo=settings.get("db.echo"),
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

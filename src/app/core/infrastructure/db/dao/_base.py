from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infrastructure.db.models import Base

_T = TypeVar(
    "_T",
    bound=Base,
)


class BaseDao(Generic[_T]):
    def __init__(self, model: type[_T], session: AsyncSession) -> None:
        self.model: type[_T] = model
        self.session: AsyncSession = session

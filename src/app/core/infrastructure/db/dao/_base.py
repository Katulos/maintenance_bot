from typing import Generic, TypeVar

from ..models import Base
from ..session import AsyncSession

_T = TypeVar(
    "_T",
    bound=Base,
)


class BaseDao(Generic[_T]):
    def __init__(self, model: type[_T], session: AsyncSession) -> None:
        self.model: type[_T] = model
        self.session: AsyncSession = session

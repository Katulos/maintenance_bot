from __future__ import annotations

import typing

import orjson
import pydantic
from pydantic import ConfigDict


def orjson_dumps(
    v: typing.Any,
    *,
    default: typing.Callable[[typing.Any], typing.Any] | None,
) -> str:
    result = orjson.dumps(v, default=default).decode()
    return typing.cast(str, result)


class BaseModel(pydantic.BaseModel):
    model_config = ConfigDict()

from __future__ import annotations

import logging
import sys

import structlog

from ..models import orjson_dumps


def setup_logger(
    logging_level: int = logging.INFO,
) -> structlog.typing.FilteringBoundLogger:
    logging.basicConfig(
        level=logging_level,
        stream=sys.stdout,
    )
    log: structlog.typing.FilteringBoundLogger = structlog.get_logger(
        structlog.stdlib.BoundLogger,
    )
    shared_processors: list[structlog.typing.Processor] = [
        structlog.processors.add_log_level,
    ]
    processors: list[structlog.typing.Processor] = [*shared_processors]
    if sys.stderr.isatty():
        processors.extend(
            [
                structlog.processors.TimeStamper(fmt="iso", utc=True),
                structlog.dev.ConsoleRenderer(),
            ],
        )
    else:
        processors.extend(
            [
                structlog.processors.TimeStamper(fmt=None, utc=True),
                structlog.processors.dict_tracebacks,
                structlog.processors.JSONRenderer(serializer=orjson_dumps),
            ],
        )
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging_level),
    )
    logging.getLogger("aiogram.event").handlers.clear()
    logging.getLogger("aiogram.event").propagate = False
    logging.getLogger("aiogram.dispatcher").handlers.clear()
    logging.getLogger("aiogram.dispatcher").propagate = False
    return log

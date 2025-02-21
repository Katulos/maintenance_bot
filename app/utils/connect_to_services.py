from __future__ import annotations

import odoorpc
import structlog
import tenacity
from tenacity import _utils

TIMEOUT_BETWEEN_ATTEMPTS = 2
MAX_TIMEOUT = 30


def before_log(retry_state: tenacity.RetryCallState) -> None:
    if retry_state.outcome is None:
        return
    if retry_state.outcome.failed:
        verb, value = "raised", retry_state.outcome.exception()
    else:
        verb, value = "returned", retry_state.outcome.result()
    logger = retry_state.kwargs["logger"]
    logger.info(
        "Retrying {callback} in {sleep} seconds as it {verb} {value}",
        callback=_utils.get_callback_name(retry_state.fn),
        sleep=retry_state.next_action.sleep,
        verb=verb,
        value=value,
        extra={
            "callback": _utils.get_callback_name(retry_state.fn),
            "sleep": retry_state.next_action.sleep,
            "verb": verb,
            "value": value,
        },
    )


def after_log(retry_state: tenacity.RetryCallState) -> None:
    logger = retry_state.kwargs["logger"]
    logger.info(
        "Finished call to {callback!r} after {time:.2f}, this was the {attempt} time calling it.",
        callback=_utils.get_callback_name(retry_state.fn),
        time=retry_state.seconds_since_start,
        attempt=_utils.to_ordinal(retry_state.attempt_number),
        extra={
            "callback": _utils.get_callback_name(retry_state.fn),
            "time": retry_state.seconds_since_start,
            "attempt": _utils.to_ordinal(retry_state.attempt_number),
        },
    )


@tenacity.retry(
    wait=tenacity.wait_fixed(TIMEOUT_BETWEEN_ATTEMPTS),
    stop=tenacity.stop_after_delay(MAX_TIMEOUT),
    before_sleep=before_log,
    after=after_log,
)  # type: ignore
async def wait_odoo(
    logger: structlog.typing.FilteringBoundLogger,
    host: str,
    port: int,
    protocol: str,
) -> odoorpc.ODOO:
    odoo = odoorpc.ODOO(
        host=host,
        port=port,
        protocol=protocol,
    )

    logger.info("Connecting to Odoo version %s", odoo.version)
    logger.debug(
        "Available Odoo databases: {}".format(
            ", ".join(map(str, odoo.db.list())),
        ),
    )
    return odoo

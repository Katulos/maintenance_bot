from __future__ import annotations

import tenacity
from tenacity import _utils


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
        callback=_utils.get_callback_name(retry_state.fn),  # type: ignore[arg-type]
        sleep=retry_state.next_action.sleep,  # type: ignore[union-attr]
        verb=verb,
        value=value,
        extra={
            "callback": _utils.get_callback_name(retry_state.fn),  # type: ignore[arg-type]
            "sleep": retry_state.next_action.sleep,  # type: ignore[union-attr]
            "verb": verb,
            "value": value,
        },
    )


def after_log(retry_state: tenacity.RetryCallState) -> None:
    logger = retry_state.kwargs["logger"]
    logger.info(
        "Finished call to {callback!r} after {time:.2f}, this was the {attempt} time calling it.",
        callback=_utils.get_callback_name(retry_state.fn),  # type: ignore[arg-type]
        time=retry_state.seconds_since_start,
        attempt=_utils.to_ordinal(retry_state.attempt_number),
        extra={
            "callback": _utils.get_callback_name(retry_state.fn),  # type: ignore[arg-type]
            "time": retry_state.seconds_since_start,
            "attempt": _utils.to_ordinal(retry_state.attempt_number),
        },
    )

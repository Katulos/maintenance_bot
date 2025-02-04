from __future__ import annotations

import odoorpc
import tenacity

TIMEOUT_BETWEEN_ATTEMPTS = 2
MAX_TIMEOUT = 30


@tenacity.retry(
    wait=tenacity.wait_fixed(TIMEOUT_BETWEEN_ATTEMPTS),
    stop=tenacity.stop_after_delay(MAX_TIMEOUT),
)
async def wait_odoo(
    host: str,
    port: int,
    protocol: str,
) -> odoorpc.ODOO:
    odoo = odoorpc.ODOO(
        host=host,
        port=port,
        protocol=protocol,
    )
    return odoo

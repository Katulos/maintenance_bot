from __future__ import annotations


async def maintenance_requests_getter(**_kwargs):
    return {
        "maintenance_requests": [
            (f"Maintenance Requests {i}", i) for i in range(1, 300)
        ],
    }

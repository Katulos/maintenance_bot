from __future__ import annotations


async def equipments_getter(**_kwargs):
    return {
        "equipments": [(f"Equipment {i}", i) for i in range(1, 100)],
    }

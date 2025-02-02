from __future__ import annotations

import odoorpc
from aiogram import types
from aiogram.fsm.context import FSMContext

from ... import states


async def start(
    msg: types.Message,
    state: FSMContext,
    odoo: odoorpc.ODOO,
) -> None:
    if msg.from_user is None:
        return
    await state.set_state(states.user.UserMainMenu.menu)

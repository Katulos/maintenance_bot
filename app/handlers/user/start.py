from __future__ import annotations

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from ... import states
from ...keyboards import default, inline


async def start(
    msg: types.Message,
    state: FSMContext,
) -> None:
    if msg.from_user is None:
        return
    await msg.answer(
        text=_("Select a menu item below"),
        reply_markup=inline.user.MainMenu.main_menu(),
    )
    # await state.set_state(states.user.UserMainMenu.main_menu)

from __future__ import annotations

from aiogram import html, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from ... import states


async def start(msg: types.Message, state: FSMContext) -> None:
    if msg.from_user is None:
        return
    m = [
        f'Hello, <a href="tg://user?id={msg.from_user.id}">{html.quote(msg.from_user.full_name)}</a>',
    ]

    m = [
        _(
            "Hello, <a href='tg://user?id={user_id}'>{user_full_name}</a>",
        ).format(
            user_id=msg.from_user.id,
            user_full_name=msg.from_user.full_name,
        ),
    ]
    await msg.answer("\n".join(m))
    await state.set_state(states.user.UserMainMenu.menu)

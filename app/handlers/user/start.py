from __future__ import annotations

from aiogram import html, types
from aiogram.fsm.context import FSMContext


async def start(msg: types.Message, state: FSMContext) -> None:
    user = msg.from_user
    user_id = user.id
    user_full_name = html.quote(user.full_name)
    m = [
        "Hello, <a href='tg://user?id={user_id}'>{user_full_name}</a>!".format(
            user_id=user_id,
            user_full_name=user_full_name,
        ),
    ]
    await msg.answer("\n".join(m))

from __future__ import annotations

from aiogram import types
from aiogram_dialog import DialogManager, StartMode

from ...states import DialogSG


async def start(
    message: types.Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(DialogSG.MAIN, mode=StartMode.RESET_STACK)
    # user = msg.from_user
    # user_id = user.id
    # user_full_name = html.quote(user.full_name)
    # m = [
    #     "Hello, <a href='tg://user?id={user_id}'>{user_full_name}</a>!".format(
    #         user_id=user_id,
    #         user_full_name=user_full_name,
    #     ),
    # ]
    # await msg.answer("\n".join(m))

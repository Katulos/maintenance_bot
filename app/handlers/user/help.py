from __future__ import annotations

from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.methods.get_my_commands import GetMyCommands

from ... import states


async def help(msg: types.Message, state: FSMContext, bot: Bot) -> None:
    commands = await bot(GetMyCommands())

    result = "\n".join(
        f"{cmd.command}: {cmd.description}"
        for cmd in commands
        if cmd.command not in {"start", "help"}
    )

    if result:
        await msg.answer(result)

    await state.set_state(states.user.UserMainMenu.menu)

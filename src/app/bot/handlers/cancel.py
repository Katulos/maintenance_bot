from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button


async def cancel_command(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.reply(
        "Canceled",
        reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
    )


# aiogram_dialog Bug: Cancel() ignore show_mode
async def close_button_handler(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    await dialog_manager.done()

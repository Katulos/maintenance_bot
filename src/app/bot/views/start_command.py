from aiogram.types import BotCommand

from app.bot.utils.i18n_format import I18NFormat

START_COMMAND = BotCommand(
    command="start",
    description=I18NFormat("start-command-description"),
)

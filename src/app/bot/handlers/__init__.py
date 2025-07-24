from aiogram import Dispatcher
from aiogram_dialog import BgManagerFactory
from aiogram_dialog.api.protocols import MessageManagerProtocol

from app.bot import dialogs
from app.bot.handlers import errors  # , base
from app.core.config.bot import BotConfig


def setup(
    dp: Dispatcher,
    config: BotConfig,
    message_manager: MessageManagerProtocol,
) -> BgManagerFactory:
    errors.setup(dp)
    # dp.include_router(base.setup())
    bg_manager_factory = dialogs.setup(dp, message_manager)
    return bg_manager_factory

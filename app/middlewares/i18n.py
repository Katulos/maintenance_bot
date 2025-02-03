from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, Protocol, Union

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from fluent.runtime import FluentLocalization

I18N_FORMAT_KEY = "aiogd_i18n_format"


class I18nMiddleware(BaseMiddleware):
    def __init__(
        self,
        l10ns: Dict[str, FluentLocalization],
        default_lang: str,
    ):
        super().__init__()
        self.l10ns = l10ns
        self.default_lang = default_lang

    async def __call__(
        self,
        handler: Callable[
            [Union[Message, CallbackQuery], Dict[str, Any]],
            Awaitable[Any],
        ],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any],
    ) -> Any:
        if event.from_user:
            lang = event.from_user.language_code
        else:
            lang = self.default_lang
        if lang not in self.l10ns:
            lang = self.default_lang

        l10n = self.l10ns[lang]
        data[I18N_FORMAT_KEY] = l10n.format_value

        return await handler(event, data)


class Values(Protocol):
    def __getitem__(self, item: Any) -> Any:
        raise NotImplementedError


def default_format_text(text: str, data: Values) -> str:
    return text.format_map(data)


class I18NFormat(Text):
    def __init__(self, text: str, when: WhenCondition = None):
        super().__init__(when)
        self.text = text

    async def _render_text(self, data: Dict, manager: DialogManager) -> str:
        format_text = manager.middleware_data.get(
            I18N_FORMAT_KEY,
            default_format_text,
        )
        return format_text(self.text, data)

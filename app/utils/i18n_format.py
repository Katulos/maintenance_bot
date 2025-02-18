from __future__ import annotations

from typing import Any, Protocol

from aiogram import MagicFilter
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text

I18N_FORMAT_KEY = "aiogd_i18n_format"


class Values(Protocol):
    def __getitem__(self, item: Any) -> Any:
        raise NotImplementedError


def default_format_text(text: str, data: Values) -> str:
    return text.format_map(data)


""" Thnx @Tishka17! :-D

see <https://t.me/aiogram_dialog/159549> """


class Transformer(Text):
    def __init__(
        self,
        text: Text,
        mapping: dict[str, MagicFilter],
        when: WhenCondition = None,
    ):
        super().__init__(when)
        self.text = text
        self.mapping = mapping

    def _transform(self, data: Values) -> Values:
        return {
            key: transformer.resolve(data)
            for key, transformer in self.mapping.items()
        }

    async def _render_text(self, data: Values, manager: DialogManager) -> str:
        return await self.text.render_text(self._transform(data), manager)


class I18NFormat(Text):
    def __init__(self, text: str, when: WhenCondition = None):
        super().__init__(when)
        self.text = text

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        format_text = manager.middleware_data.get(
            I18N_FORMAT_KEY,
            default_format_text,
        )
        return format_text(self.text, data)

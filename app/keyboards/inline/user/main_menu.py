from __future__ import annotations

from aiogram import types
from typing import List

from aiogram.utils.i18n import gettext as _

from ..consts import InlineConstructor


class MainMenu(InlineConstructor):
    @staticmethod
    def main_menu():
        schema = [2]
        actions = [
            {'text': _("⚙️ My Equipments"), 'cb': 'eq'},
            {'text': _("🛠 My Maintenance Requests"), 'cb': 'req'},
        ]
        return MainMenu._create_kb(actions, schema)

    @staticmethod
    def equipments_list(equipments: List[str]):
        schema = [1]
        btns = [_("◀️Back")]
        actions = []
        for i in equipments:
            actions.append({'text': i.name, 'cb': 'eq'})
            schema.append(1)
        actions.append({'text': _("◀️Back"), 'cb': 'main'})
        return MainMenu._create_kb(actions, schema)

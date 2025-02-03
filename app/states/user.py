from __future__ import annotations

from aiogram.fsm.state import State, StatesGroup


class UserMainMenu(StatesGroup):
    main_menu = State()

    choosing_equipment = State()

    choosing_equipment = State()

    choosing_maintenance_request = State()

    close_maintenance_request = State()

    forward_maintenance_request = State()

from __future__ import annotations

from aiogram_dialog import (
    Dialog,
)

from . import equipment_window, maintenance_window, start_window

dialog = Dialog(
    start_window.window,
    equipment_window.window,
    maintenance_window.window,
)

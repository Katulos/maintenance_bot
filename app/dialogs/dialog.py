from __future__ import annotations

from aiogram_dialog import (
    Dialog,
)

from app.dialogs import start
from app.dialogs.equipment import equipment_info, equipments
from app.dialogs.maintenance import maintenance_info, maintenances

dialog = Dialog(
    start.window,
    equipments.window,
    equipment_info.window,
    maintenances.window,
    maintenance_info.window,
)

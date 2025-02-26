from __future__ import annotations

from aiogram_dialog import (
    Dialog,
)

from . import start
from .equipment import equipment_info, equipments
from .maintenance import (
    maintenance_accept,
    maintenance_close,
    maintenance_forward,
    maintenance_info,
    maintenance_new,
    maintenances,
)

dialog = Dialog(
    start.window,
    equipments.window,
    equipment_info.window,
    maintenance_accept.window,
    maintenance_close.window,
    maintenance_forward.window,
    maintenance_info.window,
    maintenance_new.window,
    maintenances.window,
)

from dataclasses import dataclass
from typing import Any

from .enums.kanban import KanbanState


@dataclass
class MaintenanceEquipmentCategory:
    odoo_id: int
    name: str


@dataclass
class MaintenanceStage:
    odoo_id: int
    name: str
    sequence: int


@dataclass
class MaintenanceEquipment:
    odoo_id: int
    name: str
    model: str | bool
    serial_no: str | bool
    maintenance_count: int
    category_id: MaintenanceEquipmentCategory | bool
    # technician_user_id: ResUser | Any
    # owner_user_id: ResUser | Any


@dataclass
class MaintenanceRequest:
    odoo_id: int
    name: str
    equipment_id: MaintenanceEquipment | Any
    stage_id: MaintenanceStage
    # user_id: ResUser | Any
    # create_uid: ResUser | bool | Any | None
    # owner_user_id: ResUser | bool | Any | None
    kanban_state: KanbanState

from dataclasses import dataclass

from .enums.kanban import KanbanState
from .res_users import ResUser


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
    category_id: MaintenanceStage
    technician_user_id: int
    owner_user_id: int


@dataclass
class MaintenanceRequest:
    odoo_id: int
    name: str
    equipment_id: MaintenanceEquipment
    stage_id: MaintenanceStage
    user_id: ResUser
    create_uid: ResUser
    owner_user_id: ResUser
    kanban_state: KanbanState

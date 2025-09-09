from dataclasses import dataclass

from .enums.kanban import KanbanState
from .res_users import ResUsers, ResUsersResponse


@dataclass
class MaintenanceEquipmentCategory:
    odoo_id: int
    name: str


@dataclass
class MaintenanceEquipmentCategoryResponse:
    id: int
    odoo_id: int
    name: str


@dataclass
class MaintenanceStage:
    odoo_id: int
    name: str
    sequence: int


@dataclass
class MaintenanceStageResponse:
    id: int
    odoo_id: int
    name: str
    sequence: int


@dataclass
class MaintenanceEquipment:
    odoo_id: int
    name: str
    model: str
    serial_no: str
    maintenance_count: int
    category_id: MaintenanceStage
    technician_user_id: int
    owner_user_id: int


@dataclass
class MaintenanceEquipmentResponse:
    id: int
    odoo_id: int
    name: str
    model: str
    serial_no: str
    maintenance_count: int
    category_id: MaintenanceStageResponse
    technician_user_id: ResUsersResponse
    owner_user_id: ResUsersResponse


@dataclass
class MaintenanceRequest:
    odoo_id: int
    name: str
    equipment_id: MaintenanceEquipment
    stage_id: MaintenanceStage
    user_id: ResUsers
    kanban_state: KanbanState


@dataclass
class MaintenanceRequestResponse:
    id: int
    odoo_id: int
    name: str
    equipment_id: MaintenanceEquipmentResponse
    stage_id: MaintenanceStageResponse
    user_id: ResUsersResponse
    kanban_state: KanbanState

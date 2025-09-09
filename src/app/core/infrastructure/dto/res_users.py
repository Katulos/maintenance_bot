from dataclasses import dataclass

from app.core.infrastructure.dto.enums import EmployeeType


@dataclass
class ResUsers:
    odoo_id: int
    telegram_id: int
    name: str
    employee_type: EmployeeType


@dataclass
class ResUsersResponse:
    id: int
    odoo_id: int
    telegram_id: int
    name: str
    employee_type: EmployeeType

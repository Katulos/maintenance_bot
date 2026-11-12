from dataclasses import dataclass, field
from datetime import datetime

from .enums.res_users import EmployeeType


@dataclass
class ResUser:
    odoo_id: int
    telegram_id: int | None
    name: str
    employee_type: EmployeeType | bool
    create_date: datetime
    write_date: datetime
    last_sync_time: datetime = field(
        default_factory=lambda: datetime.now().replace(microsecond=0),
    )

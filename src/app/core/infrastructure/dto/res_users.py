from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ResUser:
    odoo_id: int
    telegram_id: int
    name: str
    create_date: datetime
    write_date: datetime
    last_sync_time: datetime = field(
        default_factory=lambda: datetime.now().replace(microsecond=0),
    )

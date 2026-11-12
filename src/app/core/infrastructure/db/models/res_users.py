import uuid
from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm

from app.core.infrastructure.dto.enums.res_users import EmployeeType

from ... import dto
from ._base import Base
from ._mixins import ExternalSyncMixin

if TYPE_CHECKING:
    from .maintenances import MaintenanceEquipment


class ResUser(Base, ExternalSyncMixin):
    __tablename__ = "res_users"

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.Uuid(),
        primary_key=True,
        default=uuid.uuid4,
    )

    odoo_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer(),
        unique=True,
    )

    telegram_id: orm.Mapped[int | None] = orm.mapped_column(
        sa.BigInteger(),
        nullable=False,
    )

    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(),
    )

    employee_type: orm.Mapped[EmployeeType]

    create_date: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime())

    write_date: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime())

    last_sync_time: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime())

    maintenance_equipments_technician: orm.Mapped["MaintenanceEquipment"] = (
        orm.relationship(
            foreign_keys="MaintenanceEquipment.technician_user_id",
            back_populates="technician_user",
        )
    )

    maintenance_equipments_owner: orm.Mapped["MaintenanceEquipment"] = (
        orm.relationship(
            foreign_keys="MaintenanceEquipment.owner_user_id",
            back_populates="owner_user",
        )
    )

    def to_dto(self) -> dto.ResUser:
        return dto.ResUser(
            # id=self.id,
            odoo_id=self.odoo_id,
            telegram_id=self.telegram_id,
            name=self.name,
            employee_type=self.employee_type,
            create_date=self.create_date,
            write_date=self.write_date,
        )

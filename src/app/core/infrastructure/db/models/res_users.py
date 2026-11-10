from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from ... import dto
from ._base import Base
from ._mixins import ExternalSyncMixin


class ResUser(Base, ExternalSyncMixin):
    __tablename__ = "res_users"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer(),
        primary_key=True,
        autoincrement=True,
    )

    odoo_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer(),
        unique=True,
    )

    telegram_id: orm.Mapped[int | None] = orm.mapped_column(
        sa.Integer(),
        nullable=True,
    )

    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(),
    )

    create_date: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime())

    write_date: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime())

    # maintenance_equipments_technician: orm.Mapped["MaintenanceEquipment"] = (
    #     orm.relationship(
    #         foreign_keys="MaintenanceEquipment.technician_user_id",
    #         back_populates="technician_user",
    #     )
    # )

    # maintenance_equipments_owner: orm.Mapped["MaintenanceEquipment"] = (
    #     orm.relationship(
    #         foreign_keys="MaintenanceEquipment.owner_user_id",
    #         back_populates="owner_user",
    #     )
    # )

    def to_dto(self) -> dto.ResUser:
        return dto.ResUser(
            # id=self.id,
            odoo_id=self.odoo_id,
            telegram_id=self.telegram_id,
            name=self.name,
            # employee_type=self.employee_type,
            create_date=self.create_date,
            write_date=self.write_date,
        )

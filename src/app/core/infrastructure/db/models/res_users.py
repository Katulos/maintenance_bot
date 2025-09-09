import sqlalchemy as sa
from sqlalchemy import orm

from app.core.infrastructure import dto
from app.core.infrastructure.db.models import Base, CreatedUpdatedAtMixin
from app.core.infrastructure.dto.enums import EmployeeType


class ResUsers(Base, CreatedUpdatedAtMixin):
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

    telegram_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer(),
        nullable=True,
    )

    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(),
    )

    employee_type: orm.Mapped[EmployeeType] = orm.mapped_column(
        default=EmployeeType.EMPLOYEE,
        nullable=True,
    )

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

    def to_dto(self) -> dto.ResUsersResponse:
        return dto.ResUsersResponse(
            id=self.id,
            odoo_id=self.odoo_id,
            telegram_id=self.telegram_id,
            name=self.name,
            employee_type=self.employee_type,
        )

import sqlalchemy as sa
from sqlalchemy import orm

from app.core.infrastructure import dto
from app.core.infrastructure.db.models import Base, CreatedUpdatedAtMixin
from app.core.infrastructure.db.models.res_users import ResUsers
from app.core.infrastructure.dto.enums import KanbanState


class MaintenanceEquipmentCategory(Base, CreatedUpdatedAtMixin):
    __tablename__ = "maintenance_equipment_category"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer(),
        primary_key=True,
        autoincrement=True,
    )

    odoo_id: orm.Mapped[int] = orm.mapped_column(sa.Integer(), unique=True)

    name: orm.Mapped[str] = orm.mapped_column(sa.String())

    equipment: orm.Mapped[list["MaintenanceEquipment"]] = orm.relationship()

    def to_dto(self) -> dto.MaintenanceEquipmentCategoryResponse:
        return dto.MaintenanceEquipmentCategoryResponse(
            id=self.id,
            odoo_id=self.odoo_id,
            name=self.name,
        )


class MaintenanceEquipment(Base, CreatedUpdatedAtMixin):
    __tablename__ = "maintenance_equipment"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer(),
        primary_key=True,
        autoincrement=True,
    )

    odoo_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer(),
        unique=True,
    )

    name: orm.Mapped[str] = orm.mapped_column(sa.String())

    model: orm.Mapped[str] = orm.mapped_column(sa.String(), nullable=True)

    serial_no: orm.Mapped[str] = orm.mapped_column(sa.String(), nullable=True)

    maintenance_count: orm.Mapped[int] = orm.mapped_column(
        sa.Integer(),
        nullable=True,
    )

    category_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("maintenance_equipment_category.id"),
        nullable=True,
    )

    technician_user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("res_users.id"),
        nullable=True,
    )

    owner_user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("res_users.id"),
        nullable=True,
    )

    technician_user: orm.Mapped["ResUsers"] = orm.relationship(
        foreign_keys=[technician_user_id],
        back_populates="maintenance_equipments_technician",
    )

    owner_user: orm.Mapped["ResUsers"] = orm.relationship(
        foreign_keys=[owner_user_id],
        back_populates="maintenance_equipments_owner",
    )

    def to_dto(self) -> dto.MaintenanceEquipmentResponse:
        return dto.MaintenanceEquipmentResponse(
            id=self.id,
            odoo_id=self.odoo_id,
            name=self.name,
            model=self.model,
            serial_no=self.serial_no,
            maintenance_count=self.maintenance_count,
            category_id=self.category_id,
            owner_user_id=self.owner_user_id,
            technician_user_id=self.technician_user_id,
        )


class MaintenanceRequest(Base, CreatedUpdatedAtMixin):
    __tablename__ = "maintenance_request"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer(),
        primary_key=True,
        autoincrement=True,
    )

    odoo_id: orm.Mapped[int] = orm.mapped_column(sa.Integer(), unique=True)

    name: orm.Mapped[str] = orm.mapped_column(sa.String())

    stage_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("maintenance_stage.id"),
    )

    equipment_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("maintenance_equipment.id"),
        nullable=True,
    )

    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("res_users.id"),
        nullable=True,
    )

    kanban_state: orm.Mapped[KanbanState] = orm.mapped_column(
        default=KanbanState.NORMAL,
    )

    def to_dto(self) -> dto.MaintenanceRequestResponse:
        return dto.MaintenanceRequestResponse(
            id=self.id,
            odoo_id=self.odoo_id,
            name=self.name,
            equipment_id=self.equipment_id,
            stage_id=self.stage_id,
            user_id=self.user_id,
            kanban_state=self.kanban_state,
        )


class MaintenanceStage(Base, CreatedUpdatedAtMixin):
    __tablename__ = "maintenance_stage"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer(),
        primary_key=True,
        autoincrement=True,
    )

    odoo_id: orm.Mapped[int] = orm.mapped_column(sa.Integer(), unique=True)

    name: orm.Mapped[str] = orm.mapped_column(sa.String())

    sequence: orm.Mapped[int] = orm.mapped_column(sa.Integer())

    def to_dto(self) -> dto.MaintenanceStageResponse:
        return dto.MaintenanceStageResponse(
            id=self.id,
            odoo_id=self.odoo_id,
            name=self.name,
            sequence=self.sequence,
        )

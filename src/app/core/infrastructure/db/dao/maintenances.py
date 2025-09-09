import logging
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infrastructure import dto
from app.core.infrastructure.db import models
from app.core.infrastructure.db.dao import BaseDao


class MaintenanceEquipment(BaseDao[models.MaintenanceEquipment]):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        super().__init__(models.MaintenanceEquipment, session)

    async def create(
        self,
        maintenance_equipment: dto.MaintenanceEquipment,
    ) -> dto.MaintenanceEquipmentResponse:
        stmt = (
            insert(models.MaintenanceEquipment)
            .values(
                odoo_id=maintenance_equipment.odoo_id,
                name=maintenance_equipment.name,
            )
            .on_conflict_do_update(
                index_elements=[models.MaintenanceEquipment.odoo_id],
                set_={
                    "name": maintenance_equipment.name,
                    "updated_at": datetime.now(),
                },
            )
            # .returning(models.MaintenanceEquipment)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        # return result.scalar_one().to_dto()
        # try:
        #     async with self.session.begin():
        #         category_id = None
        #         technician_user_id = None
        #         owner_user_id = None

        #         if (
        #             hasattr(maintenance_equipment, "category_id")
        #             and maintenance_equipment.category_id
        #         ):
        #             stmt_category = (
        #                 insert(models.MaintenanceEquipmentCategory)
        #                 .values(
        #                     odoo_id=maintenance_equipment.category_id.odoo_id,
        #                     name=maintenance_equipment.category_id.name,
        #                 )
        #                 .on_conflict_do_update(
        #                     index_elements=[
        #                         models.MaintenanceEquipmentCategory.odoo_id
        #                     ],
        #                     set_={
        #                         "name": maintenance_equipment.category_id.name,
        #                         "updated_at": datetime.now(),
        #                     },
        #                 )
        #                 .returning(models.MaintenanceEquipmentCategory.id)
        #             )
        #             _res = await self.session.execute(stmt_category)
        #             category_id = _res.scalar_one()

        #         if (
        #             hasattr(maintenance_equipment, "technician_user_id")
        #             and maintenance_equipment.technician_user_id
        #         ):
        #             stmt_technician = (
        #                 insert(models.ResUsers)
        #                 .values(
        #                     odoo_id=maintenance_equipment.technician_user_id.odoo_id,
        #                     name=maintenance_equipment.technician_user_id.name,
        #                 )
        #                 .on_conflict_do_update(
        #                     index_elements=[models.ResUsers.odoo_id],
        #                     set_={
        #                         "name": maintenance_equipment.technician_user_id.name,
        #                         "updated_at": datetime.now(),
        #                     },
        #                 )
        #                 .returning(models.ResUsers.id)
        #             )
        #             _res = await self.session.execute(stmt_technician)
        #             technician_user_id = _res.scalar_one()

        #         if (
        #             hasattr(maintenance_equipment, "owner_user_id")
        #             and maintenance_equipment.owner_user_id
        #         ):
        #             stmt_owner = (
        #                 insert(models.ResUsers)
        #                 .values(
        #                     odoo_id=maintenance_equipment.owner_user_id.odoo_id,
        #                     name=maintenance_equipment.owner_user_id.name,
        #                 )
        #                 .on_conflict_do_update(
        #                     index_elements=[models.ResUsers.odoo_id],
        #                     set_={
        #                         "name": maintenance_equipment.owner_user_id.name,
        #                         "updated_at": datetime.now(),
        #                     },
        #                 )
        #                 .returning(models.ResUsers.id)
        #             )
        #             _res = await self.session.execute(stmt_owner)
        #             owner_user_id = _res.scalar_one()

        #         stmt_equipment = (
        #             insert(models.MaintenanceEquipment)
        #             .values(
        #                 odoo_id=maintenance_equipment.odoo_id,
        #                 name=maintenance_equipment.name,
        #                 model=maintenance_equipment.model,
        #                 serial_no=maintenance_equipment.serial_no,
        #                 maintenance_count=maintenance_equipment.maintenance_count,
        #                 category_id=category_id,
        #                 technician_user_id=technician_user_id,
        #                 owner_user_id=owner_user_id,
        #             )
        #             .on_conflict_do_update(
        #                 index_elements=[models.MaintenanceEquipment.odoo_id],
        #                 set_={
        #                     "name": maintenance_equipment.name,
        #                     "model": maintenance_equipment.model,
        #                     "serial_no": maintenance_equipment.serial_no,
        #                     "maintenance_count": maintenance_equipment.maintenance_count,
        #                     "category_id": category_id,
        #                     "technician_user_id": technician_user_id,
        #                     "owner_user_id": owner_user_id,
        #                     "updated_at": datetime.now(),
        #                 },
        #             )
        #             .returning(models.MaintenanceEquipment)
        #         )

        #         result = await self.session.execute(stmt_equipment)
        #         equipment = result.scalar_one().to_dto()

        #         return equipment

        # except Exception as e:
        #     await self.session.rollback()
        #     logging.error(e)

    async def get_all(self) -> list[dto.MaintenanceEquipmentResponse]:
        stmt = select(models.MaintenanceEquipment)
        result = await self.session.execute(stmt)
        equipments = result.all().to_dto()
        return [equipment for equipment in equipments]


class MaintenanceEquipmentCategory(
    BaseDao[models.MaintenanceEquipmentCategory],
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(models.MaintenanceEquipmentCategory, session)

    async def upsert(
        self,
        category: dto.MaintenanceEquipmentCategory,
    ) -> dto.MaintenanceEquipmentCategoryResponse:
        stmt = (
            insert(models.MaintenanceEquipmentCategory)
            .values(
                odoo_id=category.odoo_id,
                name=category.name,
            )
            .on_conflict_do_update(
                index_elements=[models.MaintenanceEquipmentCategory.odoo_id],
                set_={
                    "name": category.name,
                    "updated_at": datetime.now(),
                },
            )
            .returning(models.MaintenanceEquipmentCategory)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one().to_dto()


class MaintenanceStage(
    BaseDao[models.MaintenanceStage],
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(models.MaintenanceStage, session)

    async def upsert(
        self,
        data: dto.MaintenanceStage,
    ) -> dto.MaintenanceStageResponse:
        stmt = (
            insert(models.MaintenanceStage)
            .values(
                odoo_id=data.odoo_id,
                name=data.name,
                sequence=data.sequence,
            )
            .on_conflict_do_update(
                index_elements=[models.MaintenanceStage.odoo_id],
                set_={
                    "name": data.name,
                    "sequence": data.sequence,
                    "updated_at": datetime.now(),
                },
            )
            .returning(models.MaintenanceStage)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one().to_dto()


class MaintenanceRequest(
    BaseDao[models.MaintenanceRequest],
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(models.MaintenanceRequest, session)

    async def upsert(
        self,
        maintenance_request: dto.MaintenanceRequest,
    ) -> dto.MaintenanceRequestResponse:
        try:
            category_id = None
            technician_user_id = None
            owner_user_id = None
            equipment_id = None
            user_id = None
            stage_id = None
            async with self.session.begin():
                # Create stage
                if (
                    hasattr(maintenance_request, "stage_id")
                    and maintenance_request.stage_id
                ):
                    stmt_stage = (
                        insert(models.MaintenanceStage)
                        .values(
                            odoo_id=maintenance_request.stage_id.odoo_id,
                            name=maintenance_request.stage_id.name,
                            sequence=maintenance_request.stage_id.sequence,
                        )
                        .on_conflict_do_update(
                            index_elements=[models.MaintenanceStage.odoo_id],
                            set_={
                                "name": maintenance_request.stage_id.name,
                                "sequence": maintenance_request.stage_id.sequence,
                                "updated_at": datetime.now(),
                            },
                        )
                        .returning(models.MaintenanceStage.id)
                    )
                    _res = await self.session.execute(stmt_stage)
                    stage_id = _res.scalar_one()
                # Create equipment
                if (
                    hasattr(maintenance_request, "equipment_id")
                    and maintenance_request.equipment_id
                ):
                    if (
                        hasattr(
                            maintenance_request.equipment_id,
                            "technician_user_id",
                        )
                        and maintenance_request.equipment_id.technician_user_id
                    ):
                        stmt_technician = (
                            insert(models.ResUsers)
                            .values(
                                odoo_id=maintenance_request.equipment_id.technician_user_id.odoo_id,
                                telegram_id=maintenance_request.equipment_id.technician_user_id.telegram_id,
                                name=maintenance_request.equipment_id.technician_user_id.name,
                                employee_type=maintenance_request.equipment_id.technician_user_id.employee_type,
                            )
                            .on_conflict_do_update(
                                index_elements=[models.ResUsers.odoo_id],
                                set_={
                                    "name": maintenance_request.equipment_id.technician_user_id.name,
                                    "telegram_id": maintenance_request.equipment_id.technician_user_id.telegram_id,
                                    "employee_type": maintenance_request.equipment_id.technician_user_id.employee_type,
                                    "updated_at": datetime.now(),
                                },
                            )
                            .returning(models.ResUsers.id)
                        )
                    _res = await self.session.execute(stmt_technician)
                    technician_user_id = _res.scalar_one()
                    #
                    if (
                        hasattr(
                            maintenance_request.equipment_id,
                            "owner_user_id",
                        )
                        and maintenance_request.equipment_id.owner_user_id
                    ):
                        stmt_owner = (
                            insert(models.ResUsers)
                            .values(
                                odoo_id=maintenance_request.equipment_id.owner_user_id.odoo_id,
                                telegram_id=maintenance_request.equipment_id.owner_user_id.telegram_id,
                                name=maintenance_request.equipment_id.owner_user_id.name,
                                employee_type=maintenance_request.equipment_id.owner_user_id.employee_type,
                            )
                            .on_conflict_do_update(
                                index_elements=[models.ResUsers.odoo_id],
                                set_={
                                    "name": maintenance_request.equipment_id.owner_user_id.name,
                                    "telegram_id": maintenance_request.equipment_id.owner_user_id.telegram_id,
                                    "employee_type": maintenance_request.equipment_id.owner_user_id.employee_type,
                                    "updated_at": datetime.now(),
                                },
                            )
                            .returning(models.ResUsers.id)
                        )
                    _res = await self.session.execute(stmt_owner)
                    owner_user_id = _res.scalar_one()
                    if (
                        hasattr(
                            maintenance_request.equipment_id,
                            "category_id",
                        )
                        and maintenance_request.equipment_id.category_id
                    ):
                        stmt_category = (
                            insert(models.MaintenanceEquipmentCategory)
                            .values(
                                odoo_id=maintenance_request.equipment_id.category_id.odoo_id,
                                name=maintenance_request.equipment_id.category_id.name,
                            )
                            .on_conflict_do_update(
                                index_elements=[
                                    models.MaintenanceEquipmentCategory.odoo_id,
                                ],
                                set_={
                                    "name": maintenance_request.equipment_id.category_id.name,
                                    "updated_at": datetime.now(),
                                },
                            )
                            .returning(models.MaintenanceEquipmentCategory.id)
                        )
                        _res = await self.session.execute(stmt_category)
                        category_id = _res.scalar_one()
                    #
                    stmt_equipment = (
                        insert(models.MaintenanceEquipment)
                        .values(
                            odoo_id=maintenance_request.equipment_id.odoo_id,
                            name=maintenance_request.equipment_id.name,
                            model=maintenance_request.equipment_id.model,
                            serial_no=maintenance_request.equipment_id.serial_no,
                            maintenance_count=maintenance_request.equipment_id.maintenance_count,
                            technician_user_id=technician_user_id,
                            owner_user_id=owner_user_id,
                            category_id=category_id,
                        )
                        .on_conflict_do_update(
                            index_elements=[
                                models.MaintenanceEquipment.odoo_id,
                            ],
                            set_={
                                "name": maintenance_request.equipment_id.name,
                                "model": maintenance_request.equipment_id.model,
                                "serial_no": maintenance_request.equipment_id.serial_no,
                                "maintenance_count": maintenance_request.equipment_id.maintenance_count,
                                "technician_user_id": technician_user_id,
                                "owner_user_id": owner_user_id,
                                "category_id": category_id,
                                "updated_at": datetime.now(),
                            },
                        )
                        .returning(models.MaintenanceEquipment.id)
                    )
                    _res = await self.session.execute(stmt_equipment)
                    equipment_id = _res.scalar_one()
                # Create user
                if (
                    hasattr(maintenance_request, "user_id")
                    and maintenance_request.user_id
                ):
                    stmt_user = (
                        insert(models.ResUsers)
                        .values(
                            odoo_id=maintenance_request.user_id.odoo_id,
                            telegram_id=maintenance_request.user_id.telegram_id,
                            name=maintenance_request.user_id.name,
                            employee_type=maintenance_request.user_id.employee_type,
                        )
                        .on_conflict_do_update(
                            index_elements=[models.ResUsers.odoo_id],
                            set_={
                                "name": maintenance_request.user_id.name,
                                "telegram_id": maintenance_request.user_id.telegram_id,
                                "employee_type": maintenance_request.user_id.employee_type,
                                "updated_at": datetime.now(),
                            },
                        )
                        .returning(models.ResUsers.id)
                    )
                    _res = await self.session.execute(stmt_user)
                    user_id = _res.scalar_one()
                # Create request
                stmt_request = (
                    insert(models.MaintenanceRequest)
                    .values(
                        odoo_id=maintenance_request.odoo_id,
                        name=maintenance_request.name,
                        equipment_id=equipment_id,
                        user_id=user_id,
                        stage_id=stage_id,
                        kanban_state=maintenance_request.kanban_state,
                    )
                    .on_conflict_do_update(
                        index_elements=[models.MaintenanceRequest.odoo_id],
                        set_={
                            "name": maintenance_request.name,
                            "user_id": user_id,
                            "equipment_id": equipment_id,
                            "stage_id": stage_id,
                            "kanban_state": maintenance_request.kanban_state,
                            "updated_at": datetime.now(),
                        },
                    )
                    .returning(models.MaintenanceRequest)
                )
                result = await self.session.execute(stmt_request)
                request = result.scalar_one().to_dto()
                return request
        except Exception as e:
            await self.session.rollback()
            logging.error(e)

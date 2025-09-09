import logging
from pprint import pprint
from typing import Any

from adaptix import P, Chain, Retort, loader
from arq import ArqRedis
from dishka import AsyncContainer, FromDishka
from dishka.integrations.arq import inject
from odoorpc import ODOO

from app.core.infrastructure import dto
from app.core.infrastructure.db.dao import DAO

_logger = logging.getLogger("app.scheduler.sync.all")


_retort = Retort(
    recipe=[
        loader(
            dto.MaintenanceRequest,
            lambda data: (
                dto.MaintenanceRequest(
                    odoo_id=data.id,
                    name=data.name,
                    equipment_id=(
                        dto.MaintenanceEquipment(
                            odoo_id=data.equipment_id.id,
                            name=data.equipment_id.name,
                            model=(
                                data.equipment_id.model
                                if data.equipment_id.model
                                else None
                            ),
                            serial_no=(
                                data.equipment_id.serial_no
                                if data.equipment_id.serial_no
                                else None
                            ),
                            maintenance_count=data.equipment_id.maintenance_count,
                            category_id=(
                                dto.MaintenanceEquipmentCategory(
                                    odoo_id=data.equipment_id.category_id.id,
                                    name=data.equipment_id.category_id.name,
                                )
                                if data.equipment_id.category_id
                                else None
                            ),
                            technician_user_id=(
                                dto.ResUsers(
                                    odoo_id=data.equipment_id.technician_user_id.id,
                                    telegram_id=data.equipment_id.technician_user_id.telegram_id,
                                    name=data.equipment_id.technician_user_id.name,
                                    employee_type=dto.EmployeeType(
                                        data.equipment_id.technician_user_id.employee_type,
                                    ),
                                )
                                if data.equipment_id.technician_user_id
                                else None
                            ),
                            owner_user_id=(
                                dto.ResUsers(
                                    odoo_id=data.equipment_id.owner_user_id.id,
                                    telegram_id=data.equipment_id.owner_user_id.telegram_id,
                                    name=data.equipment_id.owner_user_id.name,
                                    employee_type=dto.EmployeeType(
                                        data.equipment_id.owner_user_id.employee_type,
                                    ),
                                )
                                if data.equipment_id.owner_user_id
                                else None
                            ),
                        )
                        if data.equipment_id
                        else None
                    ),
                    stage_id=dto.MaintenanceStage(
                        odoo_id=data.stage_id.id,
                        name=data.stage_id.name,
                        sequence=data.stage_id.sequence,
                    ),
                    user_id=(
                        dto.ResUsers(
                            odoo_id=data.user_id.id,
                            telegram_id=data.user_id.telegram_id,
                            name=data.user_id.name,
                            employee_type=dto.EmployeeType(
                                data.user_id.employee_type,
                            ),
                        )
                        if data.user_id
                        else None
                    ),
                    kanban_state=dto.KanbanState(
                        data.kanban_state,
                    ),
                )
            ),
        ),
    ],
)


@inject
async def sync_all(
    ctx: dict[str, Any],
    odoo: FromDishka[ODOO],
    scheduler: FromDishka[ArqRedis],
) -> None:
    try:
        model = odoo.env["maintenance.request"]
        page_size = 1
        total_records = model.search_count([])
        total_pages = (total_records + page_size - 1) // page_size

        for page in range(total_pages):
            offset = page * page_size
            ids = model.search(
                [],
                limit=page_size,
                offset=offset,
            )
            records = model.browse(ids)
            for record in records:
                rec = _retort.load(record, dto.MaintenanceRequest)
                await scheduler.enqueue_job("upsert_maintenance_request", rec)
    except Exception as e:
        _logger.error(e)


@inject
async def upsert_maintenance_request(
    ctx: dict[str, Any],
    record: dto.MaintenanceRequest,
) -> None:
    container: AsyncContainer = ctx["dishka_request_container"]
    dao: DAO = await container.get(DAO)
    await dao.maintenance_requests.upsert(record)

import logging
from typing import Any

from adaptix import Chain, P, Retort, loader, name_mapping
from arq import ArqRedis
from dishka import AsyncContainer, FromDishka
from dishka.integrations.arq import inject
from odoorpc import ODOO

from ....core.infrastructure import dto
from ....core.infrastructure.db.dao import DAO


class ObjMapping:
    def __init__(self, obj):
        self.obj = obj

    def __contains__(self, item):
        return hasattr(self.obj, item)

    def __getitem__(self, name):
        return getattr(self.obj, name)

    def get(self, name, default=None):
        return getattr(self.obj, name, default)


# _retort = Retort(
#     recipe=[
#         loader(
#             dto.MaintenanceRequest,
#             lambda data: dto.MaintenanceRequest(
#                 odoo_id=data.id,
#                 name=data.name,
#                 equipment_id=(
#                     dto.MaintenanceEquipment(
#                         odoo_id=data.equipment_id.id,
#                         name=data.equipment_id.name,
#                         model=(
#                             data.equipment_id.model
#                             if data.equipment_id.model
#                             else False
#                         ),
#                         serial_no=(
#                             data.equipment_id.serial_no
#                             if data.equipment_id.serial_no
#                             else False
#                         ),
#                         maintenance_count=data.equipment_id.maintenance_count,
#                         category_id=(
#                             dto.MaintenanceEquipmentCategory(
#                                 odoo_id=data.equipment_id.category_id.id,
#                                 name=data.equipment_id.category_id.name,
#                             )
#                             if data.equipment_id.category_id
#                             else False
#                         ),
#                         technician_user_id=(
#                             dto.ResUser(
#                                 odoo_id=data.equipment_id.technician_user_id.id,
#                                 telegram_id=data.equipment_id.technician_user_id.telegram_id,
#                                 create_date=data.equipment_id.technician_user_id.create_date,
#                                 write_date=data.equipment_id.technician_user_id.write_date,
#                                 name=data.equipment_id.technician_user_id.name,
#                                 employee_type=dto.EmployeeType(
#                                     data.equipment_id.technician_user_id.employee_type,
#                                 ),
#                             )
#                             if data.equipment_id.technician_user_id
#                             else False
#                         ),
#                         owner_user_id=(
#                             dto.ResUser(
#                                 odoo_id=data.equipment_id.owner_user_id.id,
#                                 telegram_id=data.equipment_id.owner_user_id.telegram_id,
#                                 name=data.equipment_id.owner_user_id.name,
#                                 create_date=data.equipment_id.owner_user_id.create_date,
#                                 write_date=data.equipment_id.owner_user_id.write_date,
#                                 employee_type=dto.EmployeeType(
#                                     data.equipment_id.owner_user_id.employee_type,
#                                 ),
#                             )
#                             if data.equipment_id.owner_user_id
#                             else False
#                         ),
#                     )
#                     if data.equipment_id
#                     else False
#                 ),
#                 stage_id=dto.MaintenanceStage(
#                     odoo_id=data.stage_id.id,
#                     name=data.stage_id.name,
#                     sequence=data.stage_id.sequence,
#                 ),
#                 user_id=(
#                     dto.ResUser(
#                         odoo_id=data.user_id.id,
#                         telegram_id=data.user_id.telegram_id,
#                         name=data.user_id.name,
#                         create_date=data.user_id.create_date,
#                         write_date=data.user_id.write_date,
#                         employee_type=dto.EmployeeType(
#                             data.user_id.employee_type,
#                         ),
#                     )
#                     if data.user_id
#                     else False
#                 ),
#                 create_uid=dto.ResUser(
#                     odoo_id=data.create_uid.id,
#                     telegram_id=data.create_uid.telegram_id,
#                     name=data.create_uid.name,
#                     create_date=data.create_uid.create_date,
#                     write_date=data.create_uid.write_date,
#                     employee_type=dto.EmployeeType(
#                         data.create_uid.employee_type,
#                     ),
#                 ),
#                 owner_user_id=dto.ResUser(
#                     odoo_id=data.owner_user_id.id,
#                     telegram_id=data.owner_user_id.telegram_id,
#                     name=data.owner_user_id.name,
#                     create_date=data.owner_user_id.create_date,
#                     write_date=data.owner_user_id.write_date,
#                     employee_type=dto.EmployeeType(
#                         data.owner_user_id.employee_type,
#                     ),
#                 ),
#                 kanban_state=dto.KanbanState(
#                     data.kanban_state,
#                 ),
#             ),
#         ),
#     ],
# )

_retort = Retort(
    recipe=[
        loader(
            P[
                dto.MaintenanceRequest,
                dto.MaintenanceEquipment,
                dto.MaintenanceEquipmentCategory,
                dto.MaintenanceStage,
                dto.ResUser,
            ],
            ObjMapping,
            Chain.FIRST,
        ),
        name_mapping(dto.MaintenanceRequest, map={"odoo_id": "id"}),
        name_mapping(dto.MaintenanceEquipment, map={"odoo_id": "id"}),
        name_mapping(dto.MaintenanceEquipmentCategory, map={"odoo_id": "id"}),
        name_mapping(dto.MaintenanceStage, map={"odoo_id": "id"}),
        name_mapping(dto.ResUser, map={"odoo_id": "id"}),
        # loader(dto.MaintenanceRequest, ObjMapping, Chain.FIRST)
    ],
)


@inject
async def sync_all(
    ctx: dict[str, Any],
    odoo: FromDishka[ODOO],
    scheduler: FromDishka[ArqRedis],
) -> None:
    # try:
    model = odoo.env["maintenance.request"]
    page_size = 80
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


# except Exception as e:
#     logging.error(e)


@inject
async def upsert_maintenance_request(
    ctx: dict[str, Any],
    record: dto.MaintenanceRequest,
) -> None:
    container: AsyncContainer = ctx["dishka_request_container"]
    dao: DAO = await container.get(DAO)
    logging.error(record)
    # await dao.maintenance_requests.upsert(record)

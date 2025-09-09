from pprint import pprint
from typing import Any

from adaptix import Retort, name_mapping
from arq import ArqRedis
from dishka import AsyncContainer, FromDishka
from dishka.integrations.arq import inject
from odoorpc import ODOO
from odoorpc.models import Model

from app.core.infrastructure import dto
from app.core.infrastructure.db.dao import DAO


@inject
async def sync_maintenance_stages(
    _,
    odoo: FromDishka[ODOO],
    scheduler: FromDishka[ArqRedis],
) -> None:
    model: Model = odoo.env["maintenance.stage"]
    records = model.search_read([], fields=["id", "name", "sequence"])
    retort = Retort(
        recipe=[
            name_mapping(dto.MaintenanceStageCreate, map={"odoo_id": "id"}),
        ],
    )
    vals = retort.load(records, list[dto.MaintenanceStageCreate])
    for val in vals:
        await scheduler.enqueue_job("upsert_maintenance_stage", val)


@inject
async def upsert_maintenance_stage(
    ctx: dict[str, Any],
    data: dto.MaintenanceStageCreate,
) -> None:
    request_container: AsyncContainer = ctx["dishka_request_container"]
    dao: DAO = await request_container.get(DAO)

    await dao.maintenance_stages.upsert(data)


@inject
async def sync_maintenance_equipment_categories(
    _,
    odoo: FromDishka[ODOO],
    scheduler: FromDishka[ArqRedis],
) -> None:
    model: Model = odoo.env["maintenance.equipment.category"]
    records = model.search_read(
        [],
        fields=[
            "id",
            "name",
        ],
    )
    retort = Retort(
        recipe=[
            name_mapping(
                dto.MaintenanceEquipmentCategoryCreate,
                map={"odoo_id": "id"},
            ),
        ],
    )
    vals = retort.load(records, list[dto.MaintenanceEquipmentCategoryCreate])
    for val in vals:
        await scheduler.enqueue_job(
            "upsert_maintenance_equipment_category",
            val,
        )


@inject
async def upsert_maintenance_equipment_category(
    ctx: dict[str, Any],
    data: dto.MaintenanceEquipmentCategoryCreate,
) -> None:
    request_container: AsyncContainer = ctx["dishka_request_container"]
    dao: DAO = await request_container.get(DAO)

    await dao.maintenance_equipment_categories.upsert(data)


@inject
async def sync_create_maintenance_equipments(
    _,
    odoo: FromDishka[ODOO],
    scheduler: FromDishka[ArqRedis],
) -> None:
    model: Model = odoo.env["maintenance.equipment"]

    records = model.search_read(
        [("active", "=", True)],
        fields=[
            "id",
            "name",
        ],
    )

    retort = Retort(
        recipe=[
            name_mapping(
                dto.MaintenanceEquipmentCreate,
                map={"odoo_id": "id"},
            ),
        ],
    )
    vals = retort.load(records, list[dto.MaintenanceEquipmentCreate])
    for val in vals:
        await scheduler.enqueue_job("create_maintenance_equipment", val)


@inject
async def sync_update_maintenance_equipments(
    _,
    odoo: FromDishka[ODOO],
    dao: FromDishka[DAO],
    scheduler: FromDishka[ArqRedis],
) -> None:
    ids = await dao.maintenance_equipments.get_all()
    pprint(ids)
    # model: Model = odoo.env["maintenance.equipment"]

    # records = model.browse(ids)

    # retort = Retort(
    #     recipe=[
    #         name_mapping(
    #             dto.MaintenanceRequestCreate,
    #             map={"odoo_id": "id"},
    #         ),
    #         # loader(
    #         #     P[dto.MaintenanceRequestCreate].equipment_id,
    #         #     lambda data: (
    #         #         dto.MaintenanceEquipmentCreate(
    #         #             odoo_id=int(data[0]), name=data[1]
    #         #         )
    #         #         if data and isinstance(data, list) and len(data) == 2
    #         #         else None
    #         #         if data is False
    #         #         else data
    #         #     ),
    #         # ),
    #         # loader(
    #         #     P[dto.MaintenanceRequestCreate].stage_id,
    #         #     lambda data: (
    #         #         dto.MaintenanceStageCreate(
    #         #             odoo_id=int(data[0]), name=data[1]
    #         #         )
    #         #         if data and isinstance(data, list) and len(data) == 2
    #         #         else None
    #         #         if data is False
    #         #         else data
    #         #     ),
    #         # ),
    #     ],
    # )
    # vals = retort.load(records, list[dto.MaintenanceEquipmentUpdate])
    # pprint(vals)
    # # for val in vals:
    # #     await scheduler.enqueue_job("update_maintenance_equipment", val)


@inject
async def update_maintenance_equipment(
    ctx,
    data: dto.MaintenanceEquipmentCreate,
) -> None:
    request_container: AsyncContainer = ctx["dishka_request_container"]
    dao: DAO = await request_container.get(DAO)

    await dao.maintenance_equipments.create(data)


@inject
async def create_maintenance_equipment(
    ctx,
    data: dto.MaintenanceEquipmentCreate,
) -> None:
    request_container: AsyncContainer = ctx["dishka_request_container"]
    dao: DAO = await request_container.get(DAO)

    await dao.maintenance_equipments.create(data)


@inject
async def upsert_maintenance_equipment(
    ctx,
    data: dto.MaintenanceEquipmentCreate,
) -> None:
    request_container: AsyncContainer = ctx["dishka_request_container"]
    dao: DAO = await request_container.get(DAO)

    await dao.maintenance_equipments.upsert(data)


@inject
async def sync_maintenance_requests(
    _,
    odoo: FromDishka[ODOO],
    scheduler: FromDishka[ArqRedis],
) -> None:
    model: Model = odoo.env["maintenance.request"]


#     model: Model = odoo.env["maintenance.request"]
#     records = model.search_read(
#         [("archive", "=", False)],
#         fields=["id", "name", "equipment_id", "stage_id", "kanban_state"],
#     )
#     retort = Retort(
#         recipe=[
#             name_mapping(
#                 dto.MaintenanceRequestCreate,
#                 map={"odoo_id": "id"},
#             ),
#             loader(
#                 P[dto.MaintenanceRequestCreate].equipment_id,
#                 lambda data: (
#                     dto.MaintenanceEquipmentCreate(
#                         odoo_id=int(data[0]), name=data[1]
#                     )
#                     if data and isinstance(data, list) and len(data) == 2
#                     else None
#                     if data is False
#                     else data
#                 ),
#             ),
#             loader(
#                 P[dto.MaintenanceRequestCreate].stage_id,
#                 lambda data: (
#                     dto.MaintenanceStageCreate(
#                         odoo_id=int(data[0]), name=data[1]
#                     )
#                     if data and isinstance(data, list) and len(data) == 2
#                     else None
#                     if data is False
#                     else data
#                 ),
#             ),
#         ],
#     )
#     vals = retort.load(records, list[dto.MaintenanceRequestCreate])
#     for val in vals:
#         await scheduler.enqueue_job("create_maintenance_request", val)


@inject
async def upsert_maintenance_request(
    ctx,
    data: dto.MaintenanceRequestCreate,
) -> None:
    pass

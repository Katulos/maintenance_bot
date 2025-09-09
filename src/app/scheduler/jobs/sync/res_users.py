import logging

from adaptix import Retort, name_mapping
from arq import ArqRedis
from dishka import AsyncContainer, FromDishka
from dishka.integrations.arq import inject
from odoorpc import ODOO
from odoorpc.models import Model

from app.core.infrastructure import dto
from app.core.infrastructure.db.dao import DAO


@inject
async def sync_res_users(
    _,
    odoo: FromDishka[ODOO],
    scheduler: FromDishka[ArqRedis],
) -> None:
    try:
        model: Model = odoo.env["res.users"]
        records = model.search_read(
            ["&", ("telegram_id", "!=", False), ("active", "=", True)],
            fields=[
                "id",
                "telegram_id",
                "name",
                "employee_type",
            ],
        )
        retort = Retort(
            recipe=[
                name_mapping(
                    dto.ResUsersCreate,
                    map={"odoo_id": "id"},
                ),
            ],
        )
        vals = retort.load(records, list[dto.ResUsersCreate])
        for val in vals:
            await scheduler.enqueue_job("upsert_res_user", val)
    except Exception as e:
        logging.error(e)


@inject
async def upsert_res_user(
    ctx,
    data: dto.ResUsersUpdate,
) -> None:
    container: AsyncContainer = ctx["dishka_request_container"]
    dao: DAO = await container.get(DAO)

    await dao.res_users.upsert(data)

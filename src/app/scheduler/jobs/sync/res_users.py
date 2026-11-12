import logging

from adaptix import P, Retort, loader, name_mapping
from arq import ArqRedis
from dishka import AsyncContainer, FromDishka
from dishka.integrations.arq import inject
from odoorpc import ODOO
from odoorpc.error import RPCError
from odoorpc.models import Model

from ....core.infrastructure import dto
from ....core.infrastructure.db.dao import DAO

_retort = Retort(
    recipe=[
        name_mapping(
            dto.ResUser,
            map={
                "odoo_id": "id",
            },
        ),
        loader(P[dto.ResUser].telegram_id, lambda x: int(x)),
    ],
)


@inject
async def sync_res_users(
    _,
    odoo: FromDishka[ODOO],
    scheduler: FromDishka[ArqRedis],
) -> None:
    try:
        model: Model = odoo.env["res.users"]
        records = model.search_read(
            [("share", "=", False)],
            fields=[
                "id",
                "telegram_id",
                "name",
                "employee_type",
                "create_date",
                "write_date",
            ],
        )

        vals: list[dto.ResUser] = _retort.load(records, list[dto.ResUser])
        for val in vals:
            if val.telegram_id != 0:
                await scheduler.enqueue_job(
                    "upsert_res_user",
                    val,
                )

    except RPCError as e:
        # TODO: disable sync
        logging.error(e)
    except Exception as e:
        logging.error(e)


@inject
async def upsert_res_user(
    ctx,
    data: dto.ResUser,
) -> None:
    container: AsyncContainer = ctx["dishka_request_container"]
    dao: DAO = await container.get(DAO)
    await dao.res_users.upsert(data)

import logging
from pprint import pprint

from adaptix import Retort, name_mapping
from arq import ArqRedis
from dishka import AsyncContainer, FromDishka
from dishka.integrations.arq import inject
from odoorpc import ODOO
from odoorpc.error import RPCError
from odoorpc.models import Model

from app.core.infrastructure import dto
from app.core.infrastructure.db.dao import DAO

_logger = logging.getLogger(__name__)

_retort = Retort(
    recipe=[
        name_mapping(
            dto.ResUser,
            map={"odoo_id": "id"},
        ),
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
                "create_date",
                "write_date",
            ],
        )

        vals = _retort.load(records, list[dto.ResUser])
        pprint(vals)
        # for val in vals:
        #     await scheduler.enqueue_job("upsert_res_user", val)

    except RPCError as e:
        # TODO: disable sync
        logging.getLogger("odoorpc").error(e)
    except Exception as e:
        _logger.error(e)


@inject
async def upsert_res_user(
    ctx,
    data: dto.ResUser,
) -> None:
    container: AsyncContainer = ctx["dishka_request_container"]
    dao: DAO = await container.get(DAO)

    await dao.res_users.upsert(data)

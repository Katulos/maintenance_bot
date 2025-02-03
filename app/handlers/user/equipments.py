from __future__ import annotations

import aiogram
import odoorpc
import structlog
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from ... import states
from ...config import settings
from ...keyboards import default, inline


async def equipments(
    msg: types.Message,
    state: FSMContext,
    odoo: odoorpc.ODOO,
    business_logger: structlog.typing.FilteringBoundLogger,
) -> None:
    user_id = msg.from_user.id
    if msg.from_user is None:
        return

    odoo.login(
        db=settings.odoo.database,
        login=settings.odoo.users[user_id].username,
        password=settings.odoo.users[user_id].password,
    )
    hr = odoo.env["hr.employee"]
    employee_id = hr.search([("telegram_id", "=", user_id)], limit=1)
    equip = odoo.env["maintenance.equipment"]
    equipment_ids = equip.search([("employee_id", "=", employee_id)])

    equipments = equip.browse(equipment_ids)
    m = [_("Equipments:"), ""]
    names = []
    for i, info in enumerate(
        sorted(equipments, key=lambda k: k.name),
        start=1,
    ):
        m.append(
            f"{i}) - {info.name}",
        )
        m.append("")
        names.append(info.name)
    await msg.answer(
        "\n".join(m),
        reply_markup=inline.user.MainMenu.equipments_list(equipments),
    )

    # await state.set_state(states.user.UserMainMenu.choosing_equipment)

from __future__ import annotations

import odoorpc
import structlog
from aiogram.types import User
from aiogram_dialog import DialogManager, ShowMode, Window
from aiogram_dialog.widgets.kbd import (
    Cancel,
    CurrentPage,
    FirstPage,
    LastPage,
    NextPage,
    PrevPage,
    Row,
    ScrollingGroup,
    Select,
)
from aiogram_dialog.widgets.text import Format

from ...config import settings
from ...handlers.user.equipments import equipment_info
from ...states import MAIN_MENU_BTN, DialogSG
from ...utils.i18n_format import I18NFormat


async def _equipments_getter(
    event_from_user: User,
    dialog_manager: DialogManager,
    odoo_logger: structlog.typing.FilteringBoundLogger,
    **kwargs,
):
    try:
        odoo: odoorpc.ODOO = dialog_manager.middleware_data.get("odoo")
        user_id = event_from_user.id

        if user_id not in settings.odoo.users:
            odoo_logger.error("User is missing from the configuration file")
            return {"equipments": []}

        odoo.login(
            db=settings.odoo.database,
            login=settings.odoo.users[user_id].username,
            password=settings.odoo.users[user_id].password,
        )

        equipment = odoo.env["maintenance.equipment"]
        equipment_ids = equipment.search(
            [("employee_id.telegram_id", "=", user_id)],
        )
        equipments = equipment.browse(equipment_ids)

        return {"equipments": equipments}

    except odoorpc.error.RPCError as e:
        odoo_logger.error(e)
        return {"equipments": []}


window = Window(
    I18NFormat("equipments-title"),
    ScrollingGroup(
        Select(
            Format("{item[0].name}"),
            id="s_equipments",
            items="equipments",
            item_id_getter=lambda x: x.id,
            type_factory=int,
            on_click=equipment_info,
        ),
        width=1,
        height=10,
        hide_pager=True,
        id="scroll_equipments",
    ),
    Row(
        FirstPage(
            scroll="scroll_equipments",
            text=Format("⏮️ {target_page1}"),
        ),
        PrevPage(
            scroll="scroll_equipments",
            text=Format("◀️"),
        ),
        CurrentPage(
            scroll="scroll_equipments",
            text=Format("{current_page1}"),
        ),
        NextPage(
            scroll="scroll_equipments",
            text=Format("▶️"),
        ),
        LastPage(
            scroll="scroll_equipments",
            text=Format("{target_page1} ⏭️"),
        ),
    ),
    Row(
        PrevPage(scroll="scroll_equipments"),
        NextPage(scroll="scroll_equipments"),
        MAIN_MENU_BTN,
        Cancel(
            text=I18NFormat("close-button"),
            show_mode=ShowMode.DELETE_AND_SEND,
        ),
    ),
    getter=_equipments_getter,
    state=DialogSG.EQUIPMENTS_PAGER,
)

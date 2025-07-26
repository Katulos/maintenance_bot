from aiogram import F
from aiogram_dialog import StartMode, Window
from aiogram_dialog.widgets.kbd import Row, Select, Start, SwitchTo
from aiogram_dialog.widgets.text import List

from app.bot.dialogs.maintenances.getters import maintenance_getter
from app.bot.handlers.maintenances import (
    maintenance_close_switch,
    maintenance_forward_switch,
)
from app.bot.states.dialog import MainMenuSG, MaintenancesMenuSG
from app.bot.utils.i18n_format import I18NFormat, Transformer

window = Window(
    List(
        Transformer(
            I18NFormat("maintenances-info-when-category"),
            mapping={"category": F["item"].category_id.name},
            when=F["item"].category_id,
        ),
        items="maintenances",
    ),
    List(
        Transformer(
            I18NFormat("maintenances-info-when-name"),
            mapping={"name": F["item"].name},
        ),
        items="maintenances",
    ),
    List(
        Transformer(
            I18NFormat("maintenances-info-when-equipment"),
            mapping={"equipment": F["item"].equipment_id.name},
        ),
        when=F["item"].equipment_id,
        items="maintenances",
    ),
    List(
        Transformer(
            I18NFormat("maintenances-info-when-created"),
            mapping={"created": F["item"].create_uid.name},
        ),
        items="maintenances",
    ),
    List(
        Transformer(
            I18NFormat("maintenances-info-when-request-date"),
            mapping={"request_date": F["item"].create_date},
        ),
        items="maintenances",
    ),
    List(
        Transformer(
            I18NFormat("maintenances-info-when-user"),
            mapping={"user": F["item"].user_id.name},
            when=F["item"].user_id,
        ),
        items="maintenances",
    ),
    Row(
        Select(
            text=I18NFormat("complete-button"),
            id="close_maintenance",
            items="maintenances",
            item_id_getter=lambda x: x.id,
            type_factory=int,
            on_click=maintenance_close_switch,
        ),
        Select(
            text=I18NFormat("forward-button"),
            id="forward_maintenance",
            items="maintenances",
            item_id_getter=lambda x: x.id,
            type_factory=int,
            on_click=maintenance_forward_switch,
        ),
    ),
    Row(
        SwitchTo(
            text=I18NFormat("back-button"),
            id="info_maintenance",
            state=MaintenancesMenuSG.MAINTENANCE_PAGER,
        ),
        Start(
            I18NFormat("menu-button"),
            id="main",
            state=MainMenuSG.MAIN,
            mode=StartMode.RESET_STACK,
        ),
    ),
    getter=maintenance_getter,
    state=MaintenancesMenuSG.MAINTENANCE_INFO,
)

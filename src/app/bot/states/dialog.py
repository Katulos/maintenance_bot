from aiogram.fsm.state import State, StatesGroup


class MainMenuSG(StatesGroup):
    MAIN = State()


class MaintenanceMenuSG(StatesGroup):
    MAINTENANCE_ACCEPT = State()
    MAINTENANCE_CLOSE = State()
    MAINTENANCE_FORWARD = State()
    MAINTENANCE_INFO = State()
    MAINTENANCE_NEW = State()
    MAINTENANCE_PAGER = State()


class EquipmentsMenuSG(StatesGroup):
    EQUIPMENTS_PAGER = State()
    EQUIPMENT_INFO = State()

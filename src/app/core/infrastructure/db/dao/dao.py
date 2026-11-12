from ..session import AsyncSession
from .maintenances import (
    MaintenanceEquipment,
    MaintenanceEquipmentCategory,
    MaintenanceRequest,
    MaintenanceStage,
)
from .res_users import ResUser


class DAO:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

        # self.bot_flag: BotFlag = BotFlag(self.session)

        self.res_users: ResUser = ResUser(self.session)

        self.maintenance_stages: MaintenanceStage = MaintenanceStage(
            self.session,
        )

        self.maintenance_equipment_categories: MaintenanceEquipmentCategory = MaintenanceEquipmentCategory(
            self.session,
        )

        self.maintenance_equipments: MaintenanceEquipment = (
            MaintenanceEquipment(self.session)
        )

        self.maintenance_requests: MaintenanceRequest = MaintenanceRequest(
            self.session,
        )

    async def commit(self):
        await self.session.commit()

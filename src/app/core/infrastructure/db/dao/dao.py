from app.core.infrastructure.db import dao
from app.core.infrastructure.db.session import AsyncSession


class DAO:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

        self.bot_flag: dao.BotFlag = dao.BotFlag(self.session)

        self.res_user: dao.ResUser = dao.ResUser(self.session)

        # self.maintenance_stages: dao.MaintenanceStage = dao.MaintenanceStage(
        #     self.session,
        # )

        # self.maintenance_equipment_categories: dao.MaintenanceEquipmentCategory = dao.MaintenanceEquipmentCategory(
        #     self.session,
        # )

        # self.maintenance_equipments: dao.MaintenanceEquipment = (
        #     dao.MaintenanceEquipment(self.session)
        # )

        # self.maintenance_requests: dao.MaintenanceRequest = (
        #     dao.MaintenanceRequest(self.session)
        # )

    async def commit(self):
        await self.session.commit()

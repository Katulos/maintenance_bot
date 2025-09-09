from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infrastructure.db import dao


class DAO:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

        self.res_users: dao.ResUsers = dao.ResUsers(self.session)

        self.maintenance_stages: dao.MaintenanceStage = dao.MaintenanceStage(
            self.session,
        )

        self.maintenance_equipment_categories: dao.MaintenanceEquipmentCategory = dao.MaintenanceEquipmentCategory(
            self.session,
        )

        self.maintenance_equipments: dao.MaintenanceEquipment = (
            dao.MaintenanceEquipment(self.session)
        )

        self.maintenance_requests: dao.MaintenanceRequest = (
            dao.MaintenanceRequest(self.session)
        )

    async def commit(self):
        await self.session.commit()

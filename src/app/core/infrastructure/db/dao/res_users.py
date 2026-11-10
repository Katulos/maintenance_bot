from datetime import datetime

from sqlalchemy.dialects.postgresql import insert

from ... import dto
from ...db import models
from ...db.dao import BaseDao
from ...db.session import AsyncSession


class ResUser(BaseDao[models.ResUser]):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        super().__init__(models.ResUser, session)

    async def upsert(self, data: dto.ResUser) -> dto.ResUser:
        stmt = (
            insert(models.ResUser)
            .values(
                odoo_id=data.odoo_id,
                name=data.name,
                telegram_id=data.telegram_id,
                employee_type=data.employee_type,
            )
            .on_conflict_do_update(
                index_elements=[
                    models.ResUser.odoo_id,
                ],
                set_={
                    "name": data.name,
                    "telegram_id": data.telegram_id,
                    "employee_type": data.employee_type,
                    "updated_at": datetime.now(),
                },
            )
            .returning(models.ResUser)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one().to_dto()

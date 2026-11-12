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
                create_date=data.create_date,
                write_date=data.write_date,
                last_sync_time=data.last_sync_time,
            )
            .on_conflict_do_update(
                index_elements=[
                    models.ResUser.odoo_id,
                ],
                set_={
                    "name": data.name,
                    "telegram_id": data.telegram_id,
                    "employee_type": data.employee_type,
                    "write_date": data.write_date,
                },
            )
            .returning(models.ResUser)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one().to_dto()

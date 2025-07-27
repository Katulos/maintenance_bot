from typing import Any, Protocol

import odoorpc


class Odoo(Protocol):
    def login(self, login: str, password: str, db: str) -> None:
        raise NotImplementedError

    async def fetch_user(
        self,
        user_id: int,
    ) -> odoorpc.models.Model | None:
        raise NotImplementedError

    async def fetch_users(
        self,
        limit: int,
        offset: int,
    ) -> list[dict[str, Any]] | None:
        raise NotImplementedError

    async def fetch_users_count(
        self,
    ) -> int | None:
        raise NotImplementedError

    async def fetch_equipment(
        self,
        equipment_id: int,
    ) -> odoorpc.models.Model | None:
        raise NotImplementedError

    async def fetch_user_equipments(
        self,
        user_id: int,
        limit: int,
        offset: int,
    ) -> odoorpc.models.Model | None:
        raise NotImplementedError

    async def fetch_user_equipments_count(
        self,
        user_id: int,
    ) -> int | None:
        raise NotImplementedError

    async def fetch_maintenance(
        self,
        maintenance_id: int,
    ) -> odoorpc.models.Model | None:
        raise NotImplementedError

    async def fetch_user_maintenances(
        self,
        user_id: int,
        limit: int,
        offset: int,
    ) -> odoorpc.models.Model | None:
        raise NotImplementedError

    async def fetch_user_maintenances_count(
        self,
        user_id: int,
    ) -> int | None:
        raise NotImplementedError

    async def forward_maintenance(
        self,
        maintenance_id: int,
        user_id: int,
    ) -> bool:
        raise NotImplementedError

import asyncpg

from src.models.users import User
from src.database import get_connect_with_database


class OrderRepository:
    db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create(self, client_id: int) -> int:
        self.db = await get_connect_with_database()
        row = await self.db.fetchrow(
            f"INSERT INTO orders (client_id) VALUES ('{client_id}') RETURNING id"
        )

        return row[0]

    async def set_cost(self, id_: int, cost: int):
        self.db = await get_connect_with_database()
        await self.db.execute(
            f"UPDATE orders SET cost = {cost}, is_confirm = true WHERE id = {id_}"
        )


order_repository = OrderRepository()

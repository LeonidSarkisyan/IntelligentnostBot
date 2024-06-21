import asyncpg

from src.models.users import User


class OrderRepository:
    db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create(self, client_id: int) -> int:
        row = await self.db.fetchrow(
            f"INSERT INTO orders (client_id) VALUES ('{client_id}') RETURNING id"
        )

        return row[0]

    async def set_cost(self, id_: int, cost: int):
        await self.db.execute(
            f"UPDATE orders SET cost = {cost}, is_confirm = true WHERE id = {id_}"
        )


order_repository = OrderRepository()

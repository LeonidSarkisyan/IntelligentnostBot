import asyncpg

from src.models.users import User
from src.database import get_connect_with_database


class FindRepository:
    db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create(self, client_id: int, cost: int) -> int:
        self.db = await get_connect_with_database()
        row = await self.db.fetchrow(
            f"INSERT INTO finds (client_id, cost) VALUES ('{client_id}', '{cost}') RETURNING id"
        )

        return row[0]

    async def confirm(self, id_: int):
        self.db = await get_connect_with_database()
        await self.db.execute(
            f"UPDATE finds SET is_confirm = true, datetime_confirmed = CURRENT_TIMESTAMP WHERE id = {id_}"
        )

    async def deny(self, id_: int) -> int:
        self.db = await get_connect_with_database()
        stmt = f"DELETE FROM finds WHERE id = {id_} RETURNING cost"
        row = await self.db.fetchrow(stmt)
        return row[0]

    async def get_user(self, id_: int) -> User:
        self.db = await get_connect_with_database()
        query = f"SELECT u.id, u.username, u.balance FROM finds f JOIN users u ON f.client_id = u.id WHERE f.id = {id_}"
        row = await self.db.fetchrow(query)
        return User(row[0], row[1], row[2])


find_repository = FindRepository()

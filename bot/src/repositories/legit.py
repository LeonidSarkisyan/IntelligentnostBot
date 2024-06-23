import asyncpg

from src.models.users import User
from src.database import get_connect_with_database


class LegitRepository:
    db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create(self, client_id: int, cost: int) -> int:
        self.db = await get_connect_with_database()
        row = await self.db.fetchrow(
            f"INSERT INTO legits (client_id, cost) VALUES ('{client_id}', '{cost}') RETURNING id"
        )

        return row[0]

    async def original(self, id_: int):
        self.db = await get_connect_with_database()
        await self.db.execute(
            f"""
            UPDATE legits 
            SET is_confirm = true, datetime_confirmed = CURRENT_TIMESTAMP, decision = true
            WHERE id = {id_}
            """
        )

    async def not_original(self, id_: int, client_id: int):
        self.db = await get_connect_with_database()
        await self.db.execute(
            f"""
            UPDATE legits 
            SET is_confirm = true, datetime_confirmed = CURRENT_TIMESTAMP, decision = false
            WHERE id = {id_} AND client_id = {client_id}
            """
        )

    async def deny(self, id_: int) -> int:
        self.db = await get_connect_with_database()
        stmt = f"DELETE FROM legits WHERE id = {id_} RETURNING cost"
        row = await self.db.fetchrow(stmt)
        return row[0]

    async def get_user(self, id_: int) -> User:
        self.db = await get_connect_with_database()
        query = f"SELECT u.id, u.username, u.balance FROM legits l JOIN users u ON l.client_id = u.id WHERE l.id = {id_}"
        row = await self.db.fetchrow(query)
        return User(row[0], row[1], row[2])


legit_repository = LegitRepository()

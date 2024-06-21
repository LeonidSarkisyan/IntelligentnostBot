import asyncpg

import src.models.users


class UserRepository:
    db = None

    async def connect(self, db: asyncpg.connection.Connection):
        self.db = db

    async def create(self, id_: int, username: str) -> Exception:
        try:
            await self.db.execute(f"INSERT INTO users (id, username) VALUES ('{id_}', '{username}')")
        except asyncpg.exceptions.UniqueViolationError as e:
            print(f"Пользователь id = {id_} username = {username} уже есть в базе.")
            return e

    async def get(self, id_: int) -> src.models.users.User:
        query = "SELECT id, username, balance FROM users WHERE id = $1"

        record = await self.db.fetchrow(query, id_)

        if not record:
            raise ValueError(f"пользователя с id = {id_} нет в базе.")

        u = src.models.users.User(id_, record[1], record[2])

        return u

    async def add_money(self, id_: int, added_money: int):
        stmt = f"UPDATE users SET balance = balance + {added_money} WHERE id = {id_}"
        await self.db.execute(stmt)

    async def spend_money(self, id_: int, spent_money: int):
        stmt = f"UPDATE users SET balance = balance - {spent_money} WHERE id = {id_}"
        await self.db.execute(stmt)


user_repository = UserRepository()

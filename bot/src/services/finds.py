from aiogram import Bot

from src.handlers.transactions import back_money_to_balance
from src.repositories.finds import FindRepository, find_repository


class FindService:
    def __init__(self, r: FindRepository):
        self.r = r

    async def create(self, user_id: int, cost: int) -> int:
        return await self.r.create(user_id, cost)

    async def confirm(self, id_: int):
        await self.r.confirm(id_)

    async def deny(self, bot: Bot, id_: int):
        user = await self.r.get_user(id_)
        cost = await self.r.deny(id_)
        await back_money_to_balance(bot, user, cost)


find_service = FindService(find_repository)

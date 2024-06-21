from aiogram import Bot

from src.handlers.transactions import back_money_to_balance
from src.repositories.legit import LegitRepository, legit_repository


class LegitService:
    def __init__(self, r: LegitRepository):
        self.r = r

    async def create(self, user_id: int, cost: int) -> int:
        return await self.r.create(user_id, cost)

    async def original(self, id_: int):
        await self.r.original(id_)

    async def not_original(self, id_: int, client_id: int):
        await self.r.not_original(id_, client_id)

    async def deny(self, bot: Bot, id_: int):
        user = await self.r.get_user(id_)
        cost = await self.r.deny(id_)
        await back_money_to_balance(bot, user, cost)


legit_service = LegitService(legit_repository)


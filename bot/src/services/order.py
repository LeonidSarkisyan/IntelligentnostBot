from aiogram import Bot

from src.handlers.transactions import back_money_to_balance
from src.repositories.order import OrderRepository, order_repository


class OrderService:
    def __init__(self, r: OrderRepository):
        self.r = r

    async def create(self, user_id: int) -> int:
        return await self.r.create(user_id)

    async def set_cost(self, id_: int, cost: int):
        await self.r.set_cost(id_, cost)


order_service = OrderService(order_repository)

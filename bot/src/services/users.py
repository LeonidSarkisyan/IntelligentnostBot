from src.repositories.users import UserRepository, user_repository
from src.services.exceptions import InvalidAddMoney, EnoughMoney


class UserService:
    def __init__(self, r: UserRepository):
        self.r = r

    async def create(self, id_: int, username: str):
        return await self.r.create(id_, username)

    async def get(self, id_: int):
        return await self.r.get(id_)

    async def add_money(self, id_: int, added_money: int):
        if added_money <= 0:
            raise InvalidAddMoney("добавить можно только положительно число денег")

        return await self.r.add_money(id_, added_money)

    async def spend_money(self, id_: int, spent_money: int):
        user = await self.get(id_)

        if user.balance - spent_money < 0:
            raise EnoughMoney(
                f"У пользователя id = {user.id} username = {user.username} недостаточно средств на оплату."
            )

        return await self.r.spend_money(id_, spent_money)


user_service = UserService(user_repository)

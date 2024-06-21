from aiogram import Bot
from aiogram.types import Message

from src.models.users import User
from src.services.users import user_service
from src.texts.transactions import get_added_money_message, get_back_money_message


async def add_money_to_balance(message: Message, added_money: int):
    user = await user_service.get(message.from_user.id)
    await user_service.add_money(user.id, added_money)
    await message.answer(
        get_added_money_message(user.balance, added_money)
    )


async def back_money_to_balance(bot: Bot, user: User, money: int):
    await user_service.add_money(user.id, money)
    await bot.send_message(user.id, get_back_money_message(user.balance, money))

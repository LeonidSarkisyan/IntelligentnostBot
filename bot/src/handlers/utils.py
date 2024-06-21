from aiogram.types import Message

from src.keyboards.balance import get_balance_show_keyboard, get_enough_money_keyboard
from src.texts.utils import get_enough_money_message


async def enough_money_handler(message: Message, count_need_money: int):
    await message.answer(get_enough_money_message(count_need_money), reply_markup=get_enough_money_keyboard())

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup


def get_order_keyboard(user_id: int, order_id: int):
    ikb = InlineKeyboardBuilder()

    ikb.button(text="Написать стоимость выкупа  💲", callback_data=f"write_cost:{user_id}:{order_id}")
    ikb.button(text=" ", callback_data="nothing")
    ikb.button(text="Отказать в услуге  🚫", callback_data=f"order_fail:{user_id}:{order_id}")

    ikb.adjust(1)

    return ikb.as_markup()

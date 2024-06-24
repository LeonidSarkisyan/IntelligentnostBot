from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from src.config import SITE_CARD


def get_order_keyboard(user_id: int, order_id: int):
    ikb = InlineKeyboardBuilder()

    ikb.button(text="Написать стоимость выкупа  💲", callback_data=f"write_cost:{user_id}:{order_id}")
    ikb.button(text=" ", callback_data="nothing")
    ikb.button(text="Отказать в услуге  🚫", callback_data=f"order_fail:{user_id}:{order_id}")

    ikb.adjust(1)

    return ikb.as_markup()


def get_pay_after_order_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()

    ikb.button(text="Оплатить заказ", url=SITE_CARD)
    ikb.button(text="Скинуть скрин перевода", callback_data="send__receipt")
    
    ikb.adjust(1)

    return ikb.as_markup()
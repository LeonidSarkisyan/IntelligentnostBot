from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup


def get_balance_show_keyboard(amount: int = 0) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()

    ikb.button(text="Пополнить баланс", callback_data=f"deposit", pay=True)
    ikb.button(text="Назад", callback_data=f"start")

    ikb.adjust(1)

    return ikb.as_markup()

def get_enough_money_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()

    ikb.button(text="Пополнить баланс", url="http:localhost")

    return ikb.as_markup()
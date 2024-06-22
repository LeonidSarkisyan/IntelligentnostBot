from aiogram.types.web_app_info import WebAppInfo
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

    ikb.button(text="Пополнить баланс", url="http://intelligent-store.ru/card")
    ikb.button(text="Скинуть скрин перевода", callback_data="send__receipt")

    #  ikb.button(text="Пополнить баланс", web_app=WebAppInfo(url="http://intelligent-store.ru/card"))

    ikb.adjust(1)

    return ikb.as_markup()
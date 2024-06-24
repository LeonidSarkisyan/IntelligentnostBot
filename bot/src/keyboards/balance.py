from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from src.config import SITE_CARD


def get_enough_money_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()

    ikb.button(text="Пополнить баланс", url=SITE_CARD)
    ikb.button(text="Скинуть скрин перевода", callback_data="send__receipt")
    ikb.button(text="Назад", callback_data="start")
    
    #  ikb.button(text="Пополнить баланс", web_app=WebAppInfo(url="http://intelligent-store.ru/card"))

    ikb.adjust(1)

    return ikb.as_markup()
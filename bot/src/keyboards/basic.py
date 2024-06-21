from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup


def get_start_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()

    ikb.button(text="Заказать вещь", callback_data="order")
    ikb.button(text="Legit Chek", callback_data="start__legit")
    ikb.button(text="Поиск айтема", callback_data="start__find")
    ikb.button(text="Мой баланс", callback_data="balance")
    ikb.button(text="О нас", callback_data="about")

    ikb.adjust(2, 2, 1)

    return ikb.as_markup()


def get_back_to_start_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()

    ikb.button(text="Назад", callback_data="start")

    return ikb.as_markup()

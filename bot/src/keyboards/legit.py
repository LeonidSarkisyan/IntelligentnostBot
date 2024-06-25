from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup


def get_legit_confirm_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()

    ikb.button(text="Перейти к проверке", callback_data="ask__photos")
    ikb.button(text="Ознакомиться с инструкцией", url="https://telegra.ph/Instrukciya-dlya-legit-checka-06-05")
    ikb.button(text="Назад", callback_data=f"start")

    ikb.adjust(1)

    return ikb.as_markup()


def get_ask_text_keyboard() -> ReplyKeyboardMarkup:
    ikb = ReplyKeyboardBuilder()

    ikb.button(text="Без текста")

    ikb.adjust(1)

    return ikb.as_markup(
        resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Выбери действие..."
    )


def get_solve_legit_keyboard(user_id: int, legit_id: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()

    ikb.button(text="Оригинал  ✅", callback_data=f"legit_check:true:{user_id}:{legit_id}")
    ikb.button(text="Подделка  ❌", callback_data=f"legit_check:false:{user_id}:{legit_id}")
    ikb.button(text=" ", callback_data="nothing")
    ikb.button(text="Отказать в услуге  🚫", callback_data=f"legit_check:fail:{user_id}:{legit_id}")

    ikb.adjust(1)

    return ikb.as_markup()

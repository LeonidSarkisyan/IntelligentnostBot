from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup


def get_find_confirm_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()

    ikb.button(text="Начать поиск", callback_data="find")
    ikb.button(text="Назад", callback_data=f"start")

    ikb.adjust(1)

    return ikb.as_markup()


def get_no_links_keyboard() -> ReplyKeyboardMarkup:
    rkb = ReplyKeyboardBuilder()

    rkb.button(text="Ссылок нет")

    return rkb.as_markup(
        resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Выбери действие..."
    )


def get_links_keyboard(user_id: int, find_id: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()

    ikb.button(text="Отправить ссылки  ⤴️", callback_data=f"send__links__{user_id}__{find_id}")
    ikb.button(text="Отказать в услуге  ❌", callback_data=f"deny__links__{user_id}__{find_id}")

    ikb.adjust(1)

    return ikb.as_markup()


def get_photos_done_keyboard() -> ReplyKeyboardMarkup:
    rkb = ReplyKeyboardBuilder()

    rkb.button(text="Готово")

    return rkb.as_markup(
        resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Выбери действие..."
    )


def get_condition_choose_keyboard() -> ReplyKeyboardMarkup:
    rkb = ReplyKeyboardBuilder()

    rkb.button(text="Новое")
    rkb.button(text="Б \\ У")
    rkb.button(text="Не имеет значения")

    rkb.adjust(1)

    return rkb.as_markup(
        resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Выбери действие..."
    )


def get_location_choose_keyboard() -> ReplyKeyboardMarkup:
    rkb = ReplyKeyboardBuilder()

    rkb.button(text="В России")
    rkb.button(text="За рубежом")
    rkb.button(text="Не имеет значения")

    rkb.adjust(1)

    return rkb.as_markup(
        resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Выбери действие..."
    )


def get_sure_keyboard() -> ReplyKeyboardMarkup:
    rkb = ReplyKeyboardBuilder()

    rkb.button(text="ПОДТВЕРЖДАЮ  ✅")
    rkb.button(text="ОТМЕНА  ❌")

    rkb.adjust(1)

    return rkb.as_markup(
        resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Выбери действие..."
    )

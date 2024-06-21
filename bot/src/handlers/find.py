from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder

from src.config import MODERATOR_ID, FIND_PRICE
from src.handlers.utils import enough_money_handler
from src.keyboards.basic import get_start_keyboard
from src.services.exceptions import EnoughMoney
from src.services.finds import find_service
from src.services.users import user_service
from src.texts.find import (
    START_FIND_MESSAGE, ASK_SIZE_MESSAGE, ASK_LINK_MESSAGE, ASK_PHOTOS_MESSAGE, NOT_CORRECT_LINKS_MESSAGE,
    ASK_CONDITION_MESSAGE, INCORRECT_CONDITION_MESSAGE, ASK_LOCATION_MESSAGE, INCORRECT_LOCATION_MESSAGE,
    THANKS_REPORT_MESSAGE, get_new_report_find_message, ASK_SEND_LINKS_MESSAGE, SEND_LINKS_MESSAGE,
    SUCCESS_SENT_MESSAGE, get_sent_links_message, SEND_REASON_DENY_MESSAGE,
    FIND_DESCRIPTION, REASON_DENY_SENT_MESSAGE, get_deny_find_message, SURE_MESSAGE, NO_SURE_MESSAGE
)
from src.texts.utils import get_price_message, get_sure_message
from src.models.find import FindForm
from src.keyboards.find import (
    get_no_links_keyboard, get_condition_choose_keyboard, get_location_choose_keyboard, get_photos_done_keyboard,
    get_links_keyboard, get_find_confirm_keyboard, get_sure_keyboard
)
from src.utils.links_checker import check_links


router = Router()


class FindFormStates(StatesGroup):
    get_confirm = State()
    get_name = State()
    get_size = State()
    get_link = State()
    get_photos = State()
    get_condition = State()
    get_location = State()
    get_sure = State()


class SendLinksStates(StatesGroup):
    get_links = State()
    get_reason_deny = State()


@router.callback_query(F.data == "start__find")
async def send_info_about_find(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(FIND_DESCRIPTION, reply_markup=get_find_confirm_keyboard())


@router.message(F.text == "/find")
async def start_find_handler(message: Message):
    await message.answer(FIND_DESCRIPTION, reply_markup=get_find_confirm_keyboard())


@router.callback_query(F.data == "find")
async def start_find_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(START_FIND_MESSAGE)
    await state.update_data(find_form=FindForm())
    await state.set_state(FindFormStates.get_name)


@router.message(FindFormStates.get_name)
async def get_name(message: Message, state: FSMContext):
    await message.answer(f"Ваше название модели: <b>{message.text}</b>")

    data = await state.get_data()
    data["find_form"].name = message.text

    await state.update_data(find_form=data["find_form"])
    await state.set_state(FindFormStates.get_size)
    await message.answer(ASK_SIZE_MESSAGE)


@router.message(FindFormStates.get_size)
async def get_size(message: Message, state: FSMContext):
    await message.answer(f"Ваш размер: <b>{message.text}</b>")

    data = await state.get_data()
    data["find_form"].size = message.text

    await state.update_data(find_form=data["find_form"])
    await state.set_state(FindFormStates.get_link)
    await message.answer(ASK_LINK_MESSAGE, reply_markup=get_no_links_keyboard())


@router.message(FindFormStates.get_link)
async def get_link(message: Message, state: FSMContext):
    if not check_links(message.text) and message.text != "Ссылок нет":
        await message.answer(NOT_CORRECT_LINKS_MESSAGE)
        return
    elif message.text == "Ссылок нет":
        links = []
    else:
        links = message.text.split(" ")

    data = await state.get_data()
    data["find_form"].links = links

    await state.update_data(find_form=data["find_form"])
    await state.set_state(FindFormStates.get_photos)
    await message.answer(ASK_PHOTOS_MESSAGE, reply_markup=get_photos_done_keyboard())


@router.message(FindFormStates.get_photos)
async def get_photos(message: Message, state: FSMContext):
    if message.photo:
        data = await state.get_data()
        data["find_form"].photos_ids.append(message.photo[0].file_id)
        await state.update_data(find_form=data["find_form"])

    elif message.text == "Готово":
        await state.set_state(FindFormStates.get_condition)
        await message.answer(ASK_CONDITION_MESSAGE, reply_markup=get_condition_choose_keyboard())


@router.message(FindFormStates.get_condition)
async def get_condition(message: Message, state: FSMContext):
    data = await state.get_data()

    try:
        data["find_form"].set_condition(message.text)
    except ValueError:
        await message.answer(INCORRECT_CONDITION_MESSAGE)
        return

    await state.update_data(find_form=data["find_form"])
    await state.set_state(FindFormStates.get_location)
    await message.answer(ASK_LOCATION_MESSAGE, reply_markup=get_location_choose_keyboard())


@router.message(FindFormStates.get_location)
async def get_location(message: Message, state: FSMContext):
    data = await state.get_data()

    try:
        data["find_form"].set_location(message.text)
    except ValueError:
        await message.answer(INCORRECT_LOCATION_MESSAGE)
        return

    await state.update_data(find_form=data["find_form"])
    await state.set_state(FindFormStates.get_sure)

    user = await user_service.get(message.from_user.id)

    await message.answer(get_sure_message(user.balance, FIND_PRICE), reply_markup=get_sure_keyboard())


@router.message(FindFormStates.get_sure)
async def get_sure(message: Message, state: FSMContext, bot: Bot):
    if message.text == "ОТМЕНА  ❌":
        await message.answer(NO_SURE_MESSAGE, reply_markup=get_start_keyboard())
        return

    if message.text != "ПОДТВЕРЖДАЮ  ✅":
        await message.answer(SURE_MESSAGE, reply_markup=get_sure_keyboard())
        return

    user = await user_service.get(message.from_user.id)

    try:
        await user_service.spend_money(message.from_user.id, FIND_PRICE)
    except EnoughMoney:
        await enough_money_handler(message, FIND_PRICE - user.balance)
        return

    find_id = await find_service.create(message.from_user.id, FIND_PRICE)
    await message.answer(THANKS_REPORT_MESSAGE)

    data = await state.get_data()

    message_for_moderation = get_new_report_find_message(message.from_user.username, data["find_form"])

    if len(data["find_form"].photos_ids) > 0:
        album_builder = MediaGroupBuilder(
            caption=message_for_moderation
        )

        for photo_id in data["find_form"].photos_ids:
            album_builder.add_photo(photo_id)

        await bot.send_media_group(MODERATOR_ID, album_builder.build())
    else:
        await bot.send_message(MODERATOR_ID, message_for_moderation)

    await bot.send_message(MODERATOR_ID, ASK_SEND_LINKS_MESSAGE, reply_markup=get_links_keyboard(
        message.from_user.id, find_id
    ))
    await state.clear()


# В случае, если пользователь отправил корректные данные


@router.callback_query(F.data.startswith("send__links__"))
async def get_links_and_send_user(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(SEND_LINKS_MESSAGE)
    await state.set_state(SendLinksStates.get_links)
    user_id = int(call.data.split("__")[-2])
    find_id = int(call.data.split("__")[-1])
    await state.update_data(user_id=user_id, find_id=find_id)


@router.message(SendLinksStates.get_links)
async def send_links_user(message: Message, state: FSMContext, bot: Bot):
    await message.answer(SUCCESS_SENT_MESSAGE)
    data = await state.get_data()
    await bot.send_message(data["user_id"], get_sent_links_message(message.html_text), disable_web_page_preview=True)
    await find_service.confirm(data["find_id"])
    await state.clear()


# В случае, если пользователь отправил НЕкорректные данные


@router.callback_query(F.data.startswith("deny__links__"))
async def get_links_and_send_user(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(SEND_REASON_DENY_MESSAGE)
    await state.set_state(SendLinksStates.get_reason_deny)
    user_id = int(call.data.split("__")[-2])
    find_id = int(call.data.split("__")[-1])
    await state.update_data(user_id=user_id, find_id=find_id)


@router.message(SendLinksStates.get_reason_deny)
async def send_links_user(message: Message, state: FSMContext, bot: Bot):
    await message.answer(REASON_DENY_SENT_MESSAGE)
    data = await state.get_data()
    await bot.send_message(data["user_id"], get_deny_find_message(message.text), disable_web_page_preview=True)
    await find_service.deny(bot, data["find_id"])
    await state.clear()

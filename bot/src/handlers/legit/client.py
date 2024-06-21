from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder

from src.config import LEGIT_PRICE, MODERATOR_ID
from src.handlers.utils import enough_money_handler
from src.keyboards.basic import get_start_keyboard
from src.keyboards.find import get_photos_done_keyboard, get_sure_keyboard
from src.keyboards.legit import get_legit_confirm_keyboard, get_legit_guide_keyboard, get_ask_text_keyboard, \
    get_solve_legit_keyboard
from src.services.exceptions import EnoughMoney
from src.services.legit import legit_service
from src.services.users import user_service
from src.texts.legit import LEGIT_DESCRIPTION, LEGIT_GUIDE_MESSAGE, ASK_PHOTOS_MESSAGE, INCORRECT_PHOTOS_MESSAGE, \
    ONE_MORE_PHOTO_MESSAGE, ASK_TEXT_MESSAGE, THANKS_REPORT_MESSAGE, NO_SURE_MESSAGE_LEGIT, \
    get_new_report_legit_message, ASK_SOLVE_MESSAGE
from src.texts.utils import get_price_message, get_sure_message


class LegitStates(StatesGroup):
    get_photos = State()
    get_text = State()
    get_sure = State()


router = Router()


@router.callback_query(F.data == "start__legit")
async def show_legit_description(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(LEGIT_DESCRIPTION, reply_markup=get_legit_confirm_keyboard())


@router.callback_query(F.data == "legit")
async def get_guide_before_send(call: CallbackQuery):
    await call.answer()
    await call.message.answer(LEGIT_GUIDE_MESSAGE, reply_markup=get_legit_guide_keyboard())


@router.callback_query(F.data == "ask__photos")
async def ask_photos(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(ASK_PHOTOS_MESSAGE, reply_markup=get_photos_done_keyboard())
    await state.update_data(photos_ids=[])
    await state.set_state(LegitStates.get_photos)


@router.message(LegitStates.get_photos)
async def get_photo(message: Message, state: FSMContext):
    if message.photo:
        data = await state.get_data()
        data["photos_ids"].append(message.photo[0].file_id)
        await state.update_data(photos_ids=data["photos_ids"])
        return

    if not message.photo and message.text != "Готово":
        await message.answer(INCORRECT_PHOTOS_MESSAGE)
        return
    elif message.text != "Готово":
        await message.answer(INCORRECT_PHOTOS_MESSAGE)
        return

    data = await state.get_data()
    if len(data["photos_ids"]) == 0:
        await message.answer(ONE_MORE_PHOTO_MESSAGE)
        return

    await message.answer(ASK_TEXT_MESSAGE, reply_markup=get_ask_text_keyboard())
    await state.set_state(LegitStates.get_text)


@router.message(LegitStates.get_text)
async def get_photo(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(LegitStates.get_sure)
    user = await user_service.get(message.from_user.id)
    await message.answer(get_sure_message(user.balance, LEGIT_PRICE), reply_markup=get_sure_keyboard())


@router.message(LegitStates.get_sure)
async def get_sure(message: Message, state: FSMContext, bot: Bot):
    if message.text == "ОТМЕНА  ❌":
        await message.answer(NO_SURE_MESSAGE_LEGIT, reply_markup=get_start_keyboard())
        return

    user = await user_service.get(message.from_user.id)

    if message.text != "ПОДТВЕРЖДАЮ  ✅":
        await message.answer(get_sure_message(user.balance, LEGIT_PRICE), reply_markup=get_sure_keyboard())
        return

    try:
        await user_service.spend_money(message.from_user.id, LEGIT_PRICE)
    except EnoughMoney:
        await enough_money_handler(message, LEGIT_PRICE - user.balance)
        return

    legit_id = await legit_service.create(message.from_user.id, LEGIT_PRICE)
    await message.answer(THANKS_REPORT_MESSAGE)

    data = await state.get_data()

    message_for_moderation = get_new_report_legit_message(message.from_user.username, data["text"])

    if len(data["photos_ids"]) > 0:
        album_builder = MediaGroupBuilder(
            caption=message_for_moderation
        )

        for photo_id in data["photos_ids"]:
            album_builder.add_photo(photo_id)

        await bot.send_media_group(MODERATOR_ID, album_builder.build())
    else:
        await bot.send_message(MODERATOR_ID, message_for_moderation)

    await bot.send_message(MODERATOR_ID, ASK_SOLVE_MESSAGE, reply_markup=get_solve_legit_keyboard(message.from_user.id,
                                                                                                  legit_id))
    await state.clear()

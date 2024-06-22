from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder

from src.config import MODERATOR_ID
from src.keyboards.find import get_photos_done_keyboard
from src.keyboards.order import get_order_keyboard
from src.services.order import order_service
from src.texts.order import ORDER_START_MESSAGE, ASK_TWO_SCREENS_MESSAGE, get_minimal_screens_message, \
    SCREENS_SENT_TO_MODERATOR_MESSAGE, new_order_message, DECISION_ORDER_MESSAGE

NEED_MINIMAL_SCREENS = 2


class OrderStates(StatesGroup):
    get_screens = State()


router = Router()


@router.callback_query(F.data == "order")
async def show_order_details(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text(
        ORDER_START_MESSAGE
    )
    await call.message.answer(
        ASK_TWO_SCREENS_MESSAGE, reply_markup=get_photos_done_keyboard()
    )
    await state.set_state(OrderStates.get_screens)
    await state.update_data(screens=[])


@router.message(F.text == "/order")
async def show_order_details(message: Message, state: FSMContext):
    await message.answer(
        ORDER_START_MESSAGE
    )
    await message.answer(
        ASK_TWO_SCREENS_MESSAGE, reply_markup=get_photos_done_keyboard()
    )
    await state.set_state(OrderStates.get_screens)
    await state.update_data(screens=[])


@router.message(OrderStates.get_screens)
async def get_screens(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()

    if message.photo:
        data["screens"].append(message.photo[0].file_id)

    elif message.text == "Готово" and len(data["screens"]) < NEED_MINIMAL_SCREENS:
        await message.answer(get_minimal_screens_message(NEED_MINIMAL_SCREENS))

    elif message.text == "Готово":
        await message.answer(SCREENS_SENT_TO_MODERATOR_MESSAGE)

        message_for_moderation = new_order_message(message.from_user.username)

        album_builder = MediaGroupBuilder(
            caption=message_for_moderation
        )

        for photo_id in data["screens"]:
            album_builder.add_photo(photo_id)

        order_id = await order_service.create(message.from_user.id)
        await bot.send_media_group(MODERATOR_ID, album_builder.build())
        await bot.send_message(
            MODERATOR_ID,
            DECISION_ORDER_MESSAGE,
            reply_markup=get_order_keyboard(message.from_user.id, order_id)
        )

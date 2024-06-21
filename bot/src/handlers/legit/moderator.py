from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.services.legit import legit_service
from src.texts.find import SEND_REASON_DENY_MESSAGE, REASON_DENY_SENT_MESSAGE
from src.texts.legit import DECISION_SENT_TO_USER_MESSAGE, ORIGINAL_MESSAGE, NOT_ORIGINAL_MESSAGE, \
    get_deny_legit_message


class SendReasonStates(StatesGroup):
    get_reason_deny = State()


router = Router()


@router.callback_query(F.data.startswith("legit_check:true:"))
async def legit_true_handler(call: CallbackQuery, bot: Bot):
    await call.answer()
    user_id = call.data.split(":")[-2]
    legit_id = call.data.split(":")[-1]
    await legit_service.original(legit_id)
    await call.message.answer(DECISION_SENT_TO_USER_MESSAGE)
    await bot.send_message(user_id, ORIGINAL_MESSAGE)


@router.callback_query(F.data.startswith("legit_check:false:"))
async def legit_false_handler(call: CallbackQuery, bot: Bot):
    await call.answer()
    user_id = call.data.split(":")[-2]
    legit_id = call.data.split(":")[-1]
    await legit_service.not_original(legit_id, user_id)
    await call.message.answer(DECISION_SENT_TO_USER_MESSAGE)
    await bot.send_message(user_id, NOT_ORIGINAL_MESSAGE)


@router.callback_query(F.data.startswith("legit_check:fail:"))
async def legit_fail_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()
    user_id = call.data.split(":")[-2]
    legit_id = call.data.split(":")[-1]
    await call.message.answer(SEND_REASON_DENY_MESSAGE)
    await state.update_data(user_id=user_id, legit_id=legit_id)
    await state.set_state(SendReasonStates.get_reason_deny)


@router.message(SendReasonStates.get_reason_deny)
async def send_reason_deny(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()

    try:
        await legit_service.deny(bot, data["legit_id"])
    except TypeError as e:
        print(e)

    await message.answer(REASON_DENY_SENT_MESSAGE)
    await bot.send_message(data["user_id"], get_deny_legit_message(message.text))
    await state.clear()

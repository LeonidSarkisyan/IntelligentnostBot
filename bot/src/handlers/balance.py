from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.config import MODERATOR_ID
from src.keyboards.balance import get_enough_money_keyboard
from src.services.users import user_service
from src.texts.balance import ASK_RECEIPT_MESSAGE, SUCCESS_SENT_RECEIPT, get_balance_show_message, get_user_send_receipt_message
from src.texts.incorrect import ASK_PHOTO


class BalanceStates(StatesGroup):
    get_amount = State()
    get_receipt = State()


router = Router()


@router.callback_query(F.data == "balance")
async def show_balance(call: CallbackQuery):
    await call.answer()
    user = await user_service.get(call.from_user.id)
    await call.message.edit_text(get_balance_show_message(user.balance), reply_markup=get_enough_money_keyboard())


@router.message(F.text == "/balance")
async def show_balance(message: Message):
    user = await user_service.get(message.from_user.id)
    await message.answer(get_balance_show_message(user.balance), reply_markup=get_enough_money_keyboard())


@router.callback_query(F.data == "send__receipt")
async def get_receipt(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(ASK_RECEIPT_MESSAGE)
    await state.set_state(BalanceStates.get_receipt)


@router.message(BalanceStates.get_receipt)
async def send_receipt_to_moderator(message: Message, state: FSMContext, bot: Bot):
    if not message.photo:
        await message.answer(ASK_PHOTO)
        return
    
    await bot.send_photo(MODERATOR_ID, message.photo[0].file_id, caption=get_user_send_receipt_message(message.from_user.id, message.from_user.username))
    await message.answer(SUCCESS_SENT_RECEIPT)
    await state.clear()
    
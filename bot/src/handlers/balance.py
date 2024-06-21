from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.handlers.transactions import add_money_to_balance
from src.keyboards.balance import get_balance_show_keyboard, get_enough_money_keyboard
from src.services.users import user_service
from src.texts.balance import get_balance_show_message, ASK_AMOUNT_MESSAGE, INCORRECT_AMOUNT_MESSAGE, \
    get_minimal_amount_message

MINIMAL_DEPOSIT = 100


class BalanceStates(StatesGroup):
    get_amount = State()


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

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.services.order import order_service
from src.texts.balance import INCORRECT_AMOUNT_MESSAGE
from src.texts.find import SEND_REASON_DENY_MESSAGE
from src.texts.order import ASK_COST_MESSAGE, get_cost_message, COST_SEND_USER_MESSAGE, get_deny_reason_order_message


class OrderStates(StatesGroup):
    get_cost = State()
    get_reason_deny = State()


router = Router()


@router.callback_query(F.data.startswith("write_cost:"))
async def ask_cost_buy(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split(":")[-2]
    order_id = call.data.split(":")[-1]

    await call.answer()
    await state.set_state(OrderStates.get_cost)
    await call.message.answer(ASK_COST_MESSAGE)
    await state.update_data(user_id=user_id, order_id=order_id)


@router.message(OrderStates.get_cost)
async def get_cost_and_send_user(message: Message, state: FSMContext, bot: Bot):
    try:
        cost = int(message.text)
    except ValueError:
        await message.answer(INCORRECT_AMOUNT_MESSAGE)
        return

    data = await state.get_data()

    await order_service.set_cost(data["order_id"], cost)

    await bot.send_message(
        data["user_id"], get_cost_message(cost)
    )

    await message.answer(COST_SEND_USER_MESSAGE)
    await state.clear()


@router.callback_query(F.data.startswith("order_fail:"))
async def ask_cost_buy(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(OrderStates.get_reason_deny)
    await call.message.answer(SEND_REASON_DENY_MESSAGE)

    user_id = call.data.split(":")[-2]
    order_id = call.data.split(":")[-1]
    await state.update_data(user_id=user_id, order_id=order_id)


@router.message(OrderStates.get_reason_deny)
async def get_reason_deny_and_send_user(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()

    await bot.send_message(
        data["user_id"], get_deny_reason_order_message(message.text)
    )

    await message.answer(COST_SEND_USER_MESSAGE)
    await state.clear()

from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.config import COUNT_START_BONUS_MONEY
from src.handlers.transactions import add_money_to_balance
from src.texts.basic import START_MESSAGE, CANCEL_MESSAGE
from src.keyboards.basic import get_start_keyboard
from src.services.users import user_service


router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    err = await user_service.create(message.from_user.id, message.from_user.username)

    await message.answer_photo(
        photo=FSInputFile("src/media/start.jpg")
    )

    await message.answer(
        START_MESSAGE, reply_markup=get_start_keyboard()
    )

    if not err:
        await add_money_to_balance(message, COUNT_START_BONUS_MONEY)

    await state.clear()


@router.callback_query(F.data == "start")
async def start_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text(START_MESSAGE, reply_markup=get_start_keyboard())
    await state.clear()


@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    await message.answer(CANCEL_MESSAGE, reply_markup=get_start_keyboard())
    await state.clear()


@router.callback_query(F.data == "nothing")
async def nothing_handler(call: CallbackQuery):
    await call.answer()

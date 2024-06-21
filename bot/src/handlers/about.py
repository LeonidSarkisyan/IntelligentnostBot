from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery

from src.keyboards.basic import get_back_to_start_keyboard
from src.texts.about import ABOUT_MESSAGE


router = Router()


F: CallbackQuery


@router.callback_query(F.data == "about")
async def start_handler(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(ABOUT_MESSAGE, disable_web_page_preview=True, reply_markup=get_back_to_start_keyboard())


@router.message(F.text == "/about")
async def about_handler(message: Message):
    await message.answer(ABOUT_MESSAGE, disable_web_page_preview=True, reply_markup=get_back_to_start_keyboard())

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.inline import main_menu_kb
from config import SALON_NAME

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        f"👋 Добро пожаловать в <b>{SALON_NAME}</b>!\n\n"
        f"Выберите действие:",
        reply_markup=main_menu_kb(),
        parse_mode="HTML"
    )

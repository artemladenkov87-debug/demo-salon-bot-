from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import main_menu_kb
from config import SERVICES, SALON_NAME

router = Router()

@router.callback_query(F.data == "info_services")
async def show_services(callback: CallbackQuery):
    lines = [f"💇 <b>Услуги {SALON_NAME}:</b>\n"]
    for s in SERVICES:
        lines.append(f"• {s['name']} — {s['price']}₽ ({s['duration']} мин)")
    await callback.message.edit_text(
        "\n".join(lines),
        reply_markup=main_menu_kb(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "info_contacts")
async def show_contacts(callback: CallbackQuery):
    await callback.message.edit_text(
        f"📍 <b>Контакты {SALON_NAME}:</b>\n\n"
        f"📌 Адрес: ул. Примерная, 1\n"
        f"📞 Телефон: +7 (999) 000-00-00\n"
        f"📸 Instagram: @beauty_studio_demo\n"
        f"🕐 Работаем: Пн–Вс 10:00–18:00",
        reply_markup=main_menu_kb(),
        parse_mode="HTML"
    )
    await callback.answer()

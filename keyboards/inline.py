from datetime import date, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SERVICES, MASTERS, TIME_SLOTS

_DAYS_RU = {"Mon":"Пн","Tue":"Вт","Wed":"Ср","Thu":"Чт","Fri":"Пт","Sat":"Сб","Sun":"Вс"}

def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Записаться",   callback_data="book_start")],
        [InlineKeyboardButton(text="💇 Наши услуги",  callback_data="info_services")],
        [InlineKeyboardButton(text="📍 Контакты",     callback_data="info_contacts")],
    ])

def services_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"{s['name']} — {s['price']}₽ ({s['duration']} мин)",
            callback_data=f"svc:{s['name']}"
        )]
        for s in SERVICES
    ])

def masters_kb() -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text=m, callback_data=f"mst:{m}")] for m in MASTERS]
    buttons.append([InlineKeyboardButton(text="◀️ Назад", callback_data="book_start")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def dates_kb() -> InlineKeyboardMarkup:
    today = date.today()
    buttons = []
    for i in range(1, 6):
        d = today + timedelta(days=i)
        day_en = d.strftime("%a")
        label = f"{d.strftime('%d.%m')} ({_DAYS_RU.get(day_en, day_en)})"
        buttons.append([InlineKeyboardButton(text=label, callback_data=f"dt:{d.isoformat()}")])
    buttons.append([InlineKeyboardButton(text="◀️ Назад", callback_data="book_master")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def times_kb(taken_slots: set | None = None) -> InlineKeyboardMarkup:
    taken_slots = taken_slots or set()
    buttons = [
        [InlineKeyboardButton(text=t, callback_data=f"tm:{t}")]
        for t in TIME_SLOTS if t not in taken_slots
    ]
    if not buttons:
        buttons.append([InlineKeyboardButton(text="❌ Нет свободных слотов", callback_data="no_slots")])
    buttons.append([InlineKeyboardButton(text="◀️ Назад", callback_data="book_date")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def confirm_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_yes"),
        InlineKeyboardButton(text="❌ Отмена",      callback_data="confirm_no"),
    ]])

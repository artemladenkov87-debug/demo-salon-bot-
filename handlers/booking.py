from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.inline import main_menu_kb, services_kb, masters_kb, dates_kb, times_kb, confirm_kb
from database import get_connection, add_booking, is_slot_taken
from config import ADMIN_ID, SALON_NAME, TIME_SLOTS

router = Router()

class BookingStates(StatesGroup):
    choosing_service = State()
    choosing_master  = State()
    choosing_date    = State()
    choosing_time    = State()
    confirming       = State()

@router.callback_query(F.data == "book_start")
async def start_booking(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BookingStates.choosing_service)
    await callback.message.edit_text("💇 Выберите услугу:", reply_markup=services_kb())
    await callback.answer()

@router.callback_query(F.data.startswith("svc:"))
async def choose_service(callback: CallbackQuery, state: FSMContext):
    service = callback.data.split(":", 1)[1]
    await state.update_data(service=service)
    await state.set_state(BookingStates.choosing_master)
    await callback.message.edit_text(
        f"✅ Услуга: <b>{service}</b>\n\nВыберите мастера:",
        reply_markup=masters_kb(), parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "book_master")
async def back_to_master(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BookingStates.choosing_master)
    await callback.message.edit_text("Выберите мастера:", reply_markup=masters_kb())
    await callback.answer()

@router.callback_query(F.data.startswith("mst:"))
async def choose_master(callback: CallbackQuery, state: FSMContext):
    master = callback.data.split(":", 1)[1]
    await state.update_data(master=master)
    await state.set_state(BookingStates.choosing_date)
    await callback.message.edit_text(
        f"✅ Мастер: <b>{master}</b>\n\nВыберите дату:",
        reply_markup=dates_kb(), parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "book_date")
async def back_to_date(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BookingStates.choosing_date)
    await callback.message.edit_text("Выберите дату:", reply_markup=dates_kb())
    await callback.answer()

@router.callback_query(F.data.startswith("dt:"))
async def choose_date(callback: CallbackQuery, state: FSMContext):
    date_str = callback.data.split(":", 1)[1]
    data = await state.get_data()
    await state.update_data(date=date_str)
    await state.set_state(BookingStates.choosing_time)

    async with get_connection() as conn:
        taken = {slot for slot in TIME_SLOTS
                 if await is_slot_taken(conn, data["master"], date_str, slot)}

    await callback.message.edit_text(
        f"✅ Дата: <b>{date_str}</b>\n\nВыберите время:",
        reply_markup=times_kb(taken_slots=taken), parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "no_slots")
async def no_slots(callback: CallbackQuery):
    await callback.answer("Нет свободных слотов на эту дату", show_alert=True)

@router.callback_query(F.data.startswith("tm:"))
async def choose_time(callback: CallbackQuery, state: FSMContext):
    time_slot = callback.data.split(":", 1)[1]
    await state.update_data(time_slot=time_slot)
    await state.set_state(BookingStates.confirming)
    data = await state.get_data()
    await callback.message.edit_text(
        f"📋 <b>Подтвердите запись:</b>\n\n"
        f"💇 Услуга: {data['service']}\n"
        f"👤 Мастер: {data['master']}\n"
        f"📅 Дата: {data['date']}\n"
        f"🕐 Время: {time_slot}",
        reply_markup=confirm_kb(), parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "confirm_no")
async def cancel_booking(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Запись отменена.", reply_markup=main_menu_kb())
    await callback.answer()

@router.callback_query(F.data == "confirm_yes")
async def confirm_booking(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    username = callback.from_user.username or str(callback.from_user.id)

    async with get_connection() as conn:
        if await is_slot_taken(conn, data["master"], data["date"], data["time_slot"]):
            await callback.message.edit_text(
                "⚠️ Это время только что заняли. Пожалуйста, выберите другое.",
                reply_markup=main_menu_kb()
            )
            await callback.answer()
            return
        await add_booking(
            conn,
            user_id=callback.from_user.id,
            username=username,
            service=data["service"],
            master=data["master"],
            date=data["date"],
            time_slot=data["time_slot"]
        )

    await state.clear()

    await callback.message.edit_text(
        f"🎉 <b>Вы записаны!</b>\n\n"
        f"💇 {data['service']} у мастера {data['master']}\n"
        f"📅 {data['date']} в {data['time_slot']}\n\n"
        f"Ждём вас в <b>{SALON_NAME}</b>!",
        reply_markup=main_menu_kb(), parse_mode="HTML"
    )
    await callback.answer("Запись подтверждена!")

    if ADMIN_ID:
        await bot.send_message(
            ADMIN_ID,
            f"📅 <b>Новая запись!</b>\n\n"
            f"Услуга: {data['service']}\n"
            f"Мастер: {data['master']}\n"
            f"Дата: {data['date']} в {data['time_slot']}\n"
            f"Клиент: @{username}",
            parse_mode="HTML"
        )

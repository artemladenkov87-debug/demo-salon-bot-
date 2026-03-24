from keyboards.inline import (
    main_menu_kb, services_kb, masters_kb, dates_kb, times_kb, confirm_kb
)
from aiogram.types import InlineKeyboardMarkup

def test_main_menu_kb_returns_markup():
    kb = main_menu_kb()
    assert isinstance(kb, InlineKeyboardMarkup)
    texts = [btn.text for row in kb.inline_keyboard for btn in row]
    assert any("Записаться" in t for t in texts)

def test_services_kb_has_all_services():
    from config import SERVICES
    kb = services_kb()
    texts = [btn.text for row in kb.inline_keyboard for btn in row]
    for svc in SERVICES:
        assert any(svc["name"] in t for t in texts)

def test_masters_kb_has_all_masters():
    from config import MASTERS
    kb = masters_kb()
    texts = [btn.text for row in kb.inline_keyboard for btn in row]
    for master in MASTERS:
        assert master in texts

def test_dates_kb_has_5_days():
    kb = dates_kb()
    buttons = [btn for row in kb.inline_keyboard for btn in row]
    date_buttons = [btn for btn in buttons if btn.callback_data.startswith("dt:")]
    assert len(date_buttons) == 5

def test_times_kb_excludes_taken_slots():
    from config import TIME_SLOTS
    taken = {"11:30", "13:00"}
    kb = times_kb(taken_slots=taken)
    texts = [btn.text for row in kb.inline_keyboard for btn in row]
    for slot in taken:
        assert slot not in texts
    for slot in TIME_SLOTS:
        if slot not in taken:
            assert slot in texts
            break  # at least one available slot is shown

def test_confirm_kb_has_confirm_and_cancel():
    kb = confirm_kb()
    texts = [btn.text for row in kb.inline_keyboard for btn in row]
    assert any("Подтвердить" in t for t in texts)
    assert any("Отмена" in t for t in texts)

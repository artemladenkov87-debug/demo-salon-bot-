from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from handlers.start import cmd_start
from handlers.info import show_services, show_contacts
from config import SERVICES, SALON_NAME

@pytest.fixture
def mock_message():
    msg = MagicMock()
    msg.answer = AsyncMock()
    return msg

@pytest.fixture
def mock_callback():
    cb = MagicMock()
    cb.message = MagicMock()
    cb.message.edit_text = AsyncMock()
    cb.answer = AsyncMock()
    return cb

@pytest.mark.asyncio
async def test_cmd_start_sends_message(mock_message):
    await cmd_start(mock_message)
    mock_message.answer.assert_called_once()
    text = mock_message.answer.call_args[0][0]
    assert SALON_NAME in text

@pytest.mark.asyncio
async def test_show_services_contains_all_services(mock_callback):
    await show_services(mock_callback)
    mock_callback.message.edit_text.assert_called_once()
    text = mock_callback.message.edit_text.call_args[0][0]
    for svc in SERVICES:
        assert svc["name"] in text

@pytest.mark.asyncio
async def test_show_contacts_contains_phone(mock_callback):
    await show_contacts(mock_callback)
    mock_callback.message.edit_text.assert_called_once()
    text = mock_callback.message.edit_text.call_args[0][0]
    assert "+7 (999) 000-00-00" in text

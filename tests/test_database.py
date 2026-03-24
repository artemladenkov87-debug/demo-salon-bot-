import pytest
import pytest_asyncio
import aiosqlite
from database import init_db, add_booking, is_slot_taken

@pytest_asyncio.fixture
async def db(tmp_path):
    db_path = str(tmp_path / "test.db")
    async with aiosqlite.connect(db_path) as conn:
        await init_db(conn)
        yield conn

@pytest.mark.asyncio
async def test_init_db_creates_table(db):
    async with db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='bookings'"
    ) as cursor:
        row = await cursor.fetchone()
    assert row is not None

@pytest.mark.asyncio
async def test_add_booking(db):
    await add_booking(db, user_id=123, username="test", service="Стрижка",
                      master="Анна", date="2026-03-26", time_slot="11:30")
    async with db.execute("SELECT * FROM bookings") as cursor:
        rows = await cursor.fetchall()
    assert len(rows) == 1

@pytest.mark.asyncio
async def test_is_slot_taken_false_when_empty(db):
    result = await is_slot_taken(db, master="Анна", date="2026-03-26", time_slot="11:30")
    assert result is False

@pytest.mark.asyncio
async def test_is_slot_taken_true_after_booking(db):
    await add_booking(db, user_id=123, username="test", service="Стрижка",
                      master="Анна", date="2026-03-26", time_slot="11:30")
    result = await is_slot_taken(db, master="Анна", date="2026-03-26", time_slot="11:30")
    assert result is True

@pytest.mark.asyncio
async def test_different_master_same_slot_not_taken(db):
    await add_booking(db, user_id=123, username="test", service="Стрижка",
                      master="Анна", date="2026-03-26", time_slot="11:30")
    result = await is_slot_taken(db, master="Мария", date="2026-03-26", time_slot="11:30")
    assert result is False

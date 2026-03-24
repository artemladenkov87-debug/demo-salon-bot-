import aiosqlite
from contextlib import asynccontextmanager

DB_PATH = "salon.db"

@asynccontextmanager
async def get_connection():
    conn = await aiosqlite.connect(DB_PATH)
    try:
        yield conn
    finally:
        await conn.close()

async def init_db(conn: aiosqlite.Connection):
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            username   TEXT,
            service    TEXT NOT NULL,
            master     TEXT NOT NULL,
            date       TEXT NOT NULL,
            time_slot  TEXT NOT NULL,
            status     TEXT NOT NULL DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    await conn.commit()

async def add_booking(conn: aiosqlite.Connection, user_id: int, username: str,
                      service: str, master: str, date: str, time_slot: str):
    await conn.execute(
        "INSERT INTO bookings (user_id, username, service, master, date, time_slot) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, username, service, master, date, time_slot)
    )
    await conn.commit()

async def is_slot_taken(conn: aiosqlite.Connection,
                        master: str, date: str, time_slot: str) -> bool:
    async with conn.execute(
        "SELECT 1 FROM bookings WHERE master=? AND date=? AND time_slot=? AND status='active'",
        (master, date, time_slot)
    ) as cursor:
        return await cursor.fetchone() is not None

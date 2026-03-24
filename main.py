import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from database import get_connection, init_db
from handlers import start, info, booking
import config

logging.basicConfig(level=logging.INFO)

async def on_startup():
    async with get_connection() as conn:
        await init_db(conn)
    logging.info("Database initialized")

async def main():
    await on_startup()
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start.router)
    dp.include_router(info.router)
    dp.include_router(booking.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

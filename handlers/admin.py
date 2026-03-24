from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from database import get_connection
from config import ADMIN_ID

router = Router()


def admin_only(func):
    async def wrapper(message: Message, *args, **kwargs):
        if message.from_user.id != ADMIN_ID:
            return
        return await func(message, *args, **kwargs)
    return wrapper


@router.message(Command("stats"))
@admin_only
async def cmd_stats(message: Message):
    async with get_connection() as conn:
        async with conn.execute(
            "SELECT COUNT(*) FROM bookings WHERE status='active'"
        ) as cur:
            total = (await cur.fetchone())[0]

        async with conn.execute(
            "SELECT COUNT(*) FROM bookings WHERE status='active' AND date=date('now','localtime')"
        ) as cur:
            today = (await cur.fetchone())[0]

        async with conn.execute(
            "SELECT COUNT(*) FROM bookings WHERE status='active' "
            "AND date >= date('now','localtime') AND date <= date('now','localtime','+6 days')"
        ) as cur:
            week = (await cur.fetchone())[0]

        async with conn.execute(
            "SELECT service, COUNT(*) as cnt FROM bookings WHERE status='active' "
            "GROUP BY service ORDER BY cnt DESC LIMIT 1"
        ) as cur:
            top_row = await cur.fetchone()
            top_service = f"{top_row[0]} ({top_row[1]} зап.)" if top_row else "—"

    await message.answer(
        f"📊 <b>Статистика салона</b>\n\n"
        f"Всего активных записей: <b>{total}</b>\n"
        f"Сегодня: <b>{today}</b>\n"
        f"На этой неделе: <b>{week}</b>\n\n"
        f"🏆 Популярная услуга: <b>{top_service}</b>",
        parse_mode="HTML"
    )


@router.message(Command("masters"))
@admin_only
async def cmd_masters(message: Message):
    async with get_connection() as conn:
        async with conn.execute(
            "SELECT master, COUNT(*) as cnt FROM bookings WHERE status='active' "
            "GROUP BY master ORDER BY cnt DESC"
        ) as cur:
            rows = await cur.fetchall()

    if not rows:
        await message.answer("Записей пока нет.")
        return

    lines = []
    medals = ["🥇", "🥈", "🥉"]
    for i, (master, cnt) in enumerate(rows):
        medal = medals[i] if i < 3 else "▪️"
        lines.append(f"{medal} <b>{master}</b> — {cnt} зап.")

    await message.answer(
        f"👥 <b>Загрузка мастеров</b>\n\n" + "\n".join(lines),
        parse_mode="HTML"
    )


@router.message(Command("days"))
@admin_only
async def cmd_days(message: Message):
    async with get_connection() as conn:
        async with conn.execute(
            "SELECT date, COUNT(*) as cnt FROM bookings WHERE status='active' "
            "AND date >= date('now','localtime') "
            "GROUP BY date ORDER BY date ASC LIMIT 7"
        ) as cur:
            rows = await cur.fetchall()

    if not rows:
        await message.answer("Предстоящих записей нет.")
        return

    lines = []
    max_cnt = max(r[1] for r in rows)
    for date, cnt in rows:
        bar = "█" * cnt + "░" * (max_cnt - cnt)
        lines.append(f"<code>{date}</code>  {bar}  <b>{cnt}</b>")

    await message.answer(
        f"📅 <b>Загрузка по дням</b>\n\n" + "\n".join(lines),
        parse_mode="HTML"
    )


@router.message(Command("bookings"))
@admin_only
async def cmd_bookings(message: Message):
    async with get_connection() as conn:
        async with conn.execute(
            "SELECT date, time_slot, master, service, username FROM bookings "
            "WHERE status='active' AND date >= date('now','localtime') "
            "ORDER BY date ASC, time_slot ASC LIMIT 20"
        ) as cur:
            rows = await cur.fetchall()

    if not rows:
        await message.answer("Предстоящих записей нет.")
        return

    lines = []
    current_date = None
    for date, time_slot, master, service, username in rows:
        if date != current_date:
            current_date = date
            lines.append(f"\n📅 <b>{date}</b>")
        lines.append(f"  {time_slot} — {master}, {service} (@{username})")

    await message.answer(
        f"📋 <b>Ближайшие записи</b>" + "\n".join(lines),
        parse_mode="HTML"
    )

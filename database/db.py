import aiosqlite
import logging

DATABASE = 'osint_bot.db'


async def init_db():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                phone_number TEXT
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS banned_users (
                user_id INTEGER PRIMARY KEY
            )
        ''')
        await db.commit()
        logging.info("База данных инициализирована.")


async def save_user(user_id: int, username: str, phone_number: str):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            "INSERT OR REPLACE INTO users (user_id, username, phone_number) VALUES (?, ?, ?)",
            (user_id, username, phone_number)
        )
        await db.commit()
        logging.info(f"Сохранён юзер: @{username}, номер: {phone_number}")


async def is_user_banned(user_id: int) -> bool:
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT 1 FROM banned_users WHERE user_id = ?", (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result is not None


async def ban_user(user_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("INSERT OR IGNORE INTO banned_users (user_id) VALUES (?)", (user_id,))
        await db.commit()
        logging.info(f"Пользователь с ID {user_id} был забанен.")


async def unban_user(user_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("DELETE FROM banned_users WHERE user_id = ?", (user_id,))
        await db.commit()
        logging.info(f"Пользователь с ID {user_id} был разбанен.")


async def find_user_by_username(username: str) -> dict:
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT username, phone_number FROM users WHERE username = ?", (username,)) as cursor:
            result = await cursor.fetchone()
            return {"username": result[0], "phone_number": result[1]} if result else None


async def find_user_by_phone(phone_number: str) -> dict:
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT username, phone_number FROM users WHERE phone_number = ?", (phone_number,)) as cursor:
            result = await cursor.fetchone()
            return {"username": result[0], "phone_number": result[1]} if result else None

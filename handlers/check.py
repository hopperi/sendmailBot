from aiogram import Router, types
from aiogram.filters import Command
from database.db import find_user_by_username
import logging

router = Router()

@router.message(Command("check"))
async def cmd_check(message: types.Message):
    query = message.text.replace("/check", "").strip()
    if not query or not query.startswith('@'):
        await message.reply("используй: /check @username")
        return
    
    username = query[1:] 
    logging.info(f"Юзер {message.from_user.id} проверяет: {username}")
    result = await find_user_by_username(username)
    
    if result:
        await message.reply(f"вот @{username}: {result['phone_number']}")
    else:
        await message.reply(f"Юзер @{username} не найден в базе данных.")
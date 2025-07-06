from aiogram import Router, types
from aiogram.filters import Command
from database.db import find_user_by_phone
import logging

router = Router()

@router.message(Command("info"))
async def cmd_info(message: types.Message):
    query = message.text.replace("/info", "").strip()
    if not query:
        await message.reply("дай номер, пример: /info +1234567890")
        return
    
    logging.info(f"Юзер {message.from_user.id} проверяет номер: {query}")
    result = await find_user_by_phone(query)
    
    if result:
        await message.reply(f"Номер {query} принадлежит @{result['username']}")
    else:
        await message.reply("Этот номер не в базе данных.")
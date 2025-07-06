from aiogram import Router, types
from aiogram.filters import Command
from database.db import ban_user
import logging

router = Router()

# ID администратора (ставим ваш ID)
ADMIN_USER_ID = 7604368576

@router.message(Command("ban"))
async def cmd_ban(message: types.Message):
    user_id = message.from_user.id
    
    if user_id != ADMIN_USER_ID:
        await message.reply("У вас нет прав для использования этой команды.")
        return

    args = message.text.strip().split()
    
    if len(args) != 2 or not args[1].isdigit():
        await message.reply("Неправильный формат команды. Используйте: /ban <user_id>")
        return
    
    target_user_id = int(args[1])

    await ban_user(target_user_id)

    await message.reply(f"Пользователь с ID {target_user_id} был забанен.")

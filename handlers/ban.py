from aiogram import Router, types
from aiogram.filters import Command
from database.db import ban_user, is_user_banned
import logging

router = Router()

ADMIN_USER_ID = 7604368576  # Поставим ваш ID как админский

@router.message(Command("ban"))
async def cmd_ban(message: types.Message):
    user_id = message.from_user.id

    if user_id != ADMIN_USER_ID:
        await message.reply("У вас нет прав для использования этой команды.")
        return

    if not message.reply_to_message:
        await message.reply("Используйте команду /ban в ответ на сообщение пользователя, которого хотите забанить.")
        return

    target_user_id = message.reply_to_message.from_user.id

    if await is_user_banned(target_user_id):
        await message.reply(f"Пользователь с ID {target_user_id} уже забанен.")
        return

    # Баним пользователя
    await ban_user(target_user_id)
    await message.reply(f"Пользователь с ID {target_user_id} был забанен.")

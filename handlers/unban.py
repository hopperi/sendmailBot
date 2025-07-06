from aiogram import Router, types
from aiogram.filters import Command
from database.db import unban_user, is_user_banned

router = Router()

@router.message(Command("unban"))
async def cmd_unban(message: types.Message):
    user_id = message.from_user.id
    

    if user_id != 7604368576:  # Ваш ID
        await message.reply("У вас нет прав для использования этой команды.")
        return


    args = message.text.strip().split()
    if len(args) != 2 or not args[1].isdigit():
        await message.reply("Неправильный формат команды. Используйте: /unban <user_id>")
        return
    
    target_user_id = int(args[1])


    if not await is_user_banned(target_user_id):
        await message.reply(f"Пользователь с ID {target_user_id} не забанен.")
        return


    await unban_user(target_user_id)
    await message.reply(f"Пользователь с ID {target_user_id} был разбанен.")

from aiogram import Router, types
from aiogram.filters import Command
from aiogram import F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.db import ban_user, is_user_banned

router = Router()

def get_inline_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="ℹ️ Информация", callback_data="info"),
                InlineKeyboardButton(text="📬 Как отправить", callback_data="howto")
            ]
        ]
    )

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id

    if await is_user_banned(user_id):
        await message.answer("🚫 Вы забанены и не можете пользоваться ботом.")
        return

    await message.reply(
        "Привет, я бот который отправляет письма.\n\n"
        "✉️ Используй:\n"
        "`/sendmail email@example.com Текст сообщения`",
        reply_markup=get_inline_keyboard(),
        parse_mode="Markdown"
    )

@router.message(F.text & ~F.text.startswith("/"))
async def handle_random_message(message: types.Message):
    await message.reply(
        "🤖 Я не понял. Чтобы отправить письмо, используй команду:\n\n"
        "`/sendmail example@gmail.com <text>`",
        reply_markup=get_inline_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "info")
async def callback_info(callback: types.CallbackQuery):
    await callback.message.answer("👤 Создатель бота: @normcheal")
    await callback.answer()

@router.callback_query(F.data == "howto")
async def callback_howto(callback: types.CallbackQuery):
    await callback.message.answer(
        "✉️ Чтобы отправить письмо, напиши:\n"
        "`/sendmail почта@домен.com текст_письма`",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.message(Command("ban"))
async def cmd_ban(message: types.Message):
    user_id = message.from_user.id

    if user_id != 7604368576:  # Ваш Telegram user ID
        await message.reply("У вас нет прав для использование этой команды")
        return

    args = message.text.strip().split()
    if len(args) != 2 or not args[1].isdigit():
        await message.reply("неправильный формат команды. Используйте: /ban <user_id>")
        return

    target_user_id = int(args[1])

    if await is_user_banned(target_user_id):
        await message.reply(f"пользователь с ID {target_user_id} уже забанен")
        return

    await ban_user(target_user_id)
    await message.reply(f"пользователь с ID {target_user_id} был забанен")

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from services.email import send_email
from config import load_config
from database.db import is_user_banned
import logging

router = Router()

user_data = {}

@router.message(Command("sendmail"))
async def cmd_sendmail(message: types.Message):
    user_id = message.from_user.id

    # 🔒 Проверка на бан
    if await is_user_banned(user_id):
        await message.reply("🚫 Вы забанены")
        return

    args = message.text.replace("/sendmail", "").strip().split(maxsplit=1)

    if len(args) < 2:
        await message.reply("Используй правильный формат: /sendmail <email> <сообщение>")
        return

    to_email, email_message = args
    logging.info(f"пользователь {user_id} отправляет письмо на {to_email}")

    user_data[user_id] = {'email': to_email, 'message': email_message}

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1", callback_data="sendmail_count_1")],
        [InlineKeyboardButton(text="5", callback_data="sendmail_count_5")],
        [InlineKeyboardButton(text="10", callback_data="sendmail_count_10")]
    ])

    await message.reply("Выберите сколько раз отправить письмо:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith('sendmail_count_'))
async def process_count_selection(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # 🔒 Проверка на бан
    if await is_user_banned(user_id):
        await callback_query.answer("🚫 Вы забанены")
        return

    count = int(callback_query.data.split("_")[-1])  

    email = user_data.get(user_id, {}).get('email')
    message = user_data.get(user_id, {}).get('message')

    if not email or not message:
        await callback_query.answer("произошла ошибка, попробуйте снова")
        return

    config = load_config()

    logging.info(f"пользователь {user_id} отправляет письмо на {email} {count} раз.")
    logging.info(f"текст письма: {message}")

    try:
        for i in range(count):
            await send_email(config['EMAIL_ADDRESS'], config['EMAIL_PASSWORD'],
                             email, "spammer - tg @normcheal", message,
                             config['SMTP_SERVER'], config['SMTP_PORT'])
            logging.info(f"письмо {i + 1} отправлено на {email}!")

        await callback_query.message.edit_text(f"письмо отправлено на {email} {count} раз")
        await callback_query.answer(f"письмо отправлено на {email} {count} раз")

    except Exception as e:
        logging.error(f"ошибка отправки письма: {e}")
        await callback_query.answer("не удалось отправить сообщение, попробуйте позже")

    if user_id in user_data:
        del user_data[user_id]

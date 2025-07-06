import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import load_config
from handlers import start, sendmail, unban  # 

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def main():
    config = load_config()
    logging.debug(f"DEBUG BOT_TOKEN: {config['BOT_TOKEN']}")
    logging.debug(f"DEBUG EMAIL_ADDRESS: {config['EMAIL_ADDRESS']}")
    logging.debug(f"DEBUG EMAIL_PASSWORD: {config['EMAIL_PASSWORD']}")
    
    bot = Bot(token=config['BOT_TOKEN'])
    dp = Dispatcher()
    
    dp.include_router(start.router)
    dp.include_router(sendmail.router)
    dp.include_router(unban.router)  
    
    logging.info("Бот успешно запущен")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

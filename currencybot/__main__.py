import logging
import asyncio

from aiogram import Dispatcher, Bot

from handlers.exchange_rate import currency_router
from handlers.introduction import help_router

from config import BOT_TOKEN


async def main():
    dp = Dispatcher()
    bot = Bot(BOT_TOKEN)
    dp.include_routers(help_router, currency_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

def configure_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s]: %(message)s',
                        datefmt='%d/%m/%Y %H:%M.%S')

if __name__ == '__main__':
    configure_logging()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
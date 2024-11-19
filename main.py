import os
import sys
import asyncio
import logging
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from core.handlers import cmdstart
from core.db.db import init_db

dp = Dispatcher()
load_dotenv()

async def main() -> None:
    dp.include_routers(
        cmdstart.router,
    )

    bot = Bot(os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Bot stopped')

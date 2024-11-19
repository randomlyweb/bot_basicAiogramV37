<<<<<<< HEAD
import os
import sys
import asyncio
import logging
from dotenv import load_dotenv
=======
import sys
import asyncio
import logging
>>>>>>> f303ad37dd6858a445d658d19d6e9450fedd06f8

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

<<<<<<< HEAD
=======
from config import TOKEN
>>>>>>> f303ad37dd6858a445d658d19d6e9450fedd06f8
from core.handlers import cmdstart
from core.db.db import init_db

dp = Dispatcher()
<<<<<<< HEAD
load_dotenv()
=======

>>>>>>> f303ad37dd6858a445d658d19d6e9450fedd06f8

async def main() -> None:
    dp.include_routers(
        cmdstart.router,
    )
<<<<<<< HEAD
    bot = Bot(os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
=======
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
>>>>>>> f303ad37dd6858a445d658d19d6e9450fedd06f8
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

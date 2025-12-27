import asyncio
import logging
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher
from aiogram.utils import executor

import config
import handlers
import utils


async def on_startup(_):
    await utils.load_quotes()
    asyncio.create_task(handlers.every_day_wisdom())


def setup_logging():
    logfile = f'{config.data_folder}/log/debug.log'
    handler = RotatingFileHandler(logfile, maxBytes=5 * 1024 * 1024, backupCount=2)
    
    logging.basicConfig(
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%y-%m-%d %H:%M:%S',
        level=logging.DEBUG,
        handlers=[handler]
    )


def main():
    setup_logging()
    
    bot = Bot(token=config.tb_token)
    dp = Dispatcher(bot)
    
    handlers.register_handlers(dp)
    
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    main()
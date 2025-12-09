import time
import traceback
from aiogram import Bot
import config
bot = Bot(token=TB_TOKEN)

async def exception():
    await bot.send_message(config.wiz_id, f"```\n{time.ctime()}\n{traceback.format_exc()}```", parse_mode="Markdown")
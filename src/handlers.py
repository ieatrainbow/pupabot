import random
import re
import asyncio
from functools import partial

import aioschedule
from aiogram import Dispatcher, types
from transliterate import translit

import config
import services
import utils
from helpers import exception


async def send_random_quote(bot, message):
    try:
        await bot.send_chat_action(message.chat.id, 'typing')
        import time
        time.sleep(2)
        await message.reply(random.choice(utils.get_pupa_quotes()).upper())
    except Exception:
        await exception()


async def technik_quote(bot, message):
    try:
        await bot.send_chat_action(message.chat.id, 'typing')
        import time
        time.sleep(2)
        await message.reply(random.choice(utils.get_technik_quotes()))
    except Exception:
        await exception()


async def russia(bot, message):
    try:
        await bot.send_chat_action(message.chat.id, 'upload_video')
        import time
        time.sleep(2)
        await bot.send_animation(message.chat.id, 
                               animation=open(f'{config.data_folder}/gif/russia.gif', 'rb'))
    except Exception:
        await exception()


async def think(bot, message):
    try:
        await bot.send_chat_action(message.chat.id, 'upload_video')
        import time
        time.sleep(2)
        await bot.send_animation(message.chat.id, 
                               animation=open(f'{config.data_folder}/video/think.mp4', 'rb'))
    except Exception:
        await exception()


async def send_sticker(bot, message):
    try:
        sti = open(f'{config.data_folder}/stickers/{random.randint(1, 35)}.webp', 'rb')
        await bot.send_chat_action(message.chat.id, 'choose_sticker')
        import time
        time.sleep(1)
        await bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)
    except Exception:
        await exception()


async def hueficator(bot, message):
    try:
        if not re.match(r'(https?://)', message.text):
            text = translit(message.text, 'ru')
            re_text = re.sub(r'[^А-Яа-яёЁ\s]+', '', text)
            if re_text != '':
                word = re_text.lower().strip().split()[-1]
                vowels = 'аеёиоуыэюя'
                rules = {
                    'а': 'я',
                    'о': 'е',
                    'у': 'ю',
                    'ы': 'и',
                    'э': 'е',
                }

                for letter in word:
                    if letter in vowels:
                        if letter in rules:
                            word = rules[letter] + word[1:]
                        break
                    else:
                        word = word[1:]
                hword = 'ху' + word if word else random.choice(utils.get_pupa_quotes()).upper()
                await bot.send_chat_action(message.chat.id, 'typing')
                import time
                time.sleep(1)
                await message.reply(hword.upper())
    except Exception:
        await exception()


async def send_video(bot, message, video_name):
    try:
        await bot.send_chat_action(message.chat.id, 'upload_video')
        import time
        time.sleep(2)
        video_path = f'{config.data_folder}/video/{video_name}.mp4'
        await bot.send_video(message.chat.id, video=open(video_path, 'rb'))
    except Exception:
        await exception()


# Regex handlers
key_video_names = {
    r'(\bг\s*о\s*й\s*д\s*а)': 'goyda',
    r'(\bday\s*is\s*ruined|\bdisappointment\s*is\s*immeasurable|\bдень\s*испорчен)': 'ruined',
    r'(\bя\s*уста*л)': 'tired',
    r'(\bзаебался*)': 'tired_tech',
    r'(\bчика\s*пака)': 'chica',
    r'(\bне\s*хочу\s.*работать)': 'work',
    r'(\bахует*)': 'ahuet',
    r'(\bв\s*о\s*т\s*т\s*у\s*т\s*в\s*е\s*р\s*ю)|(\bприду\b)': 'trust'
}

key_names = {
    r'(\bп.п\s*з.йди\s*|\bх.хл.\s*спросим)': send_random_quote,
    r'(\bп.п\s*м.др.сть)': services.wisdom_create,
    r'(\bп.зици.\s*техника)': technik_quote,
    r'(\bр\s*[ао]\s*с\s*и\s*я)': russia,
    r'(\bп\s*а\s*б\s*е\s*д\s*а)|(^😡)': services.enrage,
    r'(\bн\s*а\s*е\s*б\s*)': services.lying_voice_reply,
    r'(\bп.п\s*голос)': services.random_voice_reply
}

key_functions = {**{key: partial(send_video, video_name=value) for key, value in key_video_names.items()},
                 **key_names}


async def process_message(message: types.Message):
    rand = random.randrange(30)
    regex_condition_met = False
    
    for regex, function in key_functions.items():
        if re.search(regex, message.text.lower()):
            regex_condition_met = True
            if isinstance(function, str):
                await message.answer(function)
            else:
                await function(message.bot, message)
            break
    
    if not regex_condition_met:
        if message.from_user.id == config.pupa_id:
            with open(f'{config.data_folder}/log/messages_log.txt', 'a', encoding='utf-8') as f:
                f.write(message.text)
                f.write('\n')
        
        if rand in [5, 15]:
            await send_random_quote(message.bot, message)
        elif rand in [10]:
            await hueficator(message.bot, message)
        elif rand == 30:
            await send_sticker(message.bot, message)
        elif rand == 25:
            await think(message.bot, message)


async def send_mp3(message: types.Message):
    if message.sticker.file_unique_id == 'AgADGwADsZeTFg':
        await services.enrage(message.bot, message)
    elif message.sticker.file_unique_id == 'AgADPAADsZeTFg':
        await services.lying_voice_reply(message.bot, message)


async def handle_photo_or_video(message: types.Message):
    random_number = random.randint(1, 30)
    if random_number == 10:
        await send_random_quote(message.bot, message)
    elif random_number == 15:
        await send_sticker(message.bot, message)


async def every_day_wisdom():
    aioschedule.every().day.at("05:00").do(lambda: services.wisdom_create(None, config.UBERPEPOLIS_CHAT_ID))
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(process_message, content_types=['text'])
    dp.register_message_handler(send_mp3, content_types=['sticker'])
    dp.register_message_handler(handle_photo_or_video, content_types=['photo', 'video'])
    dp.register_message_handler(services.speech_to_text, content_types=['voice', 'video_note'])
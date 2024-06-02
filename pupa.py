import asyncio
import logging
import random
import re
import subprocess
import textwrap as tw
import time
import traceback
from functools import partial
from logging.handlers import RotatingFileHandler

import aioschedule
import openai
import speech_recognition as sr
from PIL import Image, ImageDraw, ImageFont
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from gtts import gTTS
from transliterate import translit

import config

# Configure logging
lofgile = f'{config.patch}/log/debug.log'
handler = RotatingFileHandler(lofgile, maxBytes=5 * 1024 * 1024, backupCount=2)
logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%y-%m-%d %H:%M:%S',
                    level=logging.DEBUG,
                    handlers=[handler]
                    )

# Initialize bot and dispatcher
bot = Bot(token=config.tbtoken)
dp = Dispatcher(bot)
openai.api_key = config.openai_token

# Opening files, dividing line by line, then close
with open(f'{config.patch}/text/pupa_q.txt', 'r', encoding='UTF-8') as pupa_q:
    pupa_quotes = pupa_q.read().split('\n')
    pupa_q.close()

with open(f'{config.patch}/text/pupa_w.txt', 'r', encoding='UTF-8') as pupa_w:
    pupa_wisdom = pupa_w.read().split(';')
    pupa_w.close()

with open(f'{config.patch}/text/technik_q.txt', 'r', encoding='UTF-8') as technik_q:
    technik_quotes = technik_q.read().split('\n')
    technik_q.close()


# Functions
async def send_random_quote(message):
    try:
        await bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(2)
        await message.reply(random.choice(pupa_quotes).upper())
    except Exception:
        await exception()


async def speech_to_text(message):
    max_attempts = 3
    attempt = 0
    while attempt < max_attempts:
        try:
            await bot.send_chat_action(message.chat.id, 'typing')
            # Save file
            if message.content_type == 'voice':
                file_info = await bot.get_file(message.voice.file_id)
            elif message.content_type == 'video_note':
                file_info = await bot.get_file(message.video_note.file_id)
            elif message.content_type == 'video':
                file_info = await bot.get_file(message.video.file_id)
            elif message.content_type == 'audio':
                file_info = await bot.get_file(message.audio.file_id)
            else:
                file_info = None

            await bot.download_file(file_info.file_path, f'{config.patch}/audio/new_file.mp4')
            # Convert mp4 to wav
            src_filename = f'{config.patch}/audio/new_file.mp4'
            dest_filename = f'{config.patch}/audio/sample.wav'
            subprocess.run(['ffmpeg', '-y', '-i', src_filename, dest_filename], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)

            # Convert speech-to-text
            try:
                r = sr.Recognizer()
                with sr.AudioFile(dest_filename) as source:
                    r.adjust_for_ambient_noise(source, duration=0)
                    r.pause_threshold = 0.8
                    # listen for the data (load audio to memory)
                    audio_data = r.record(source)
                    # recognize (convert from speech to text)
                    speech_text = r.recognize_google(audio_data, language='ru-RU', pfilter=0)
                await message.reply(speech_text)
                break  # exit the loop if successful
            except sr.UnknownValueError:
                await message.reply(random.choice(['каво', 'не слышу', 'ммм?']))
        except Exception:
            await exception()
        attempt += 1
        await asyncio.sleep(10)  # add a delay before retrying


async def random_voice_reply(message):
    try:
        await bot.send_chat_action(message.chat.id, 'record_audio')
        time.sleep(2)
        s = gTTS(random.choice(pupa_quotes), lang='ru', slow=False)
        s.save(f'{config.patch}/audio/sample.ogg')
        await bot.send_voice(message.chat.id, reply_to_message_id=message.message_id,
                             voice=open(f'{config.patch}/audio/sample.ogg', 'rb'))
    except Exception:
        await exception()


async def lying_voice_reply(message):
    try:
        await bot.send_chat_action(message.chat.id, 'record_audio')
        time.sleep(2)
        await bot.send_voice(message.chat.id, reply_to_message_id=message.message_id,
                             voice=open(f'{config.patch}/audio/lying.ogg', 'rb'))
    except Exception:
        await exception()


async def technik_quote(message):
    try:
        await bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(2)
        await message.reply(random.choice(technik_quotes))
    except Exception:
        await exception()


async def wisdom_create(chat_id):
    max_attempts = 3
    attempt = 0
    while attempt < max_attempts:
        try:
            await bot.send_chat_action(chat_id, 'upload_photo')  # show the bot "upload_photo"
            time.sleep(2)
            # Make image with quote
            img = Image.open(f'{config.patch}/pupaups/{random.randint(1, 12)}.jpg')
            position = (320, 0)
            text = random.choice(pupa_wisdom)
            color = [(255, 165, 0), (0, 128, 128), (128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 0, 128)]
            dedented_text = tw.fill(tw.dedent(text).strip(), width=15)
            font = ImageFont.truetype(f'{config.patch}/font/Lobster-Regular.ttf', 60)
            ImageDraw.Draw(img).multiline_text(position, tw.fill(dedented_text, width=15), font=font, stroke_width=20,
                                               stroke_fill=random.choice(color),
                                               spacing=-40, anchor='ma',
                                               align='center')
            image_name_output = f'{config.patch}/pupaups/wisdom.jpg'
            img.save(image_name_output)

            # Send image
            await bot.send_photo(chat_id, photo=open(image_name_output, 'rb'))
            img.close()
            break  # exit the loop if successful
        except Exception:
            await exception()
        attempt += 1
        await asyncio.sleep(10)  # add a delay before retrying


async def russia(message):
    try:
        await bot.send_chat_action(message.chat.id, 'upload_video')
        time.sleep(2)
        await bot.send_animation(message.chat.id, animation=open(f'{config.patch}/gif/russia.gif', 'rb'))
    except Exception:
        await exception()


async def send_sticker(message):
    try:
        sti = open(f'{config.patch}/stickers/{random.randint(1, 35)}.webp', 'rb')
        await bot.send_chat_action(message.chat.id, 'choose_sticker')
        time.sleep(1)
        await bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)
    except Exception:
        await exception()


async def enrage(message):
    audio_path = f'{config.patch}/audio/enrage.mp3'
    audio_file = open(audio_path, 'rb')

    try:
        await bot.send_chat_action(message.chat.id, 'upload_document')
        await asyncio.sleep(1)
        await bot.send_audio(message.chat.id, audio_file, reply_to_message_id=message.message_id)
    finally:
        audio_file.close()


async def hueficator(message):
    try:
        if not re.match(r'(https?://)', message.text):
            text = translit(message.text, 'ru')
            re_text = re.sub(r'[^А-Яа-я\s]+', '', text)
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
                hword = 'ху' + word if word else random.choice(pupa_quotes).upper()
                await bot.send_chat_action(message.chat.id, 'typing')
                time.sleep(1)
                await message.reply(hword.upper())
            else:
                pass
        else:
            pass
    except Exception:
        await exception()


async def exception():
    await bot.send_message(config.wiz_id, f"```\n{time.ctime()}\n{traceback.format_exc()}```", parse_mode="Markdown")


async def every_day_wisdom():
    # Schedule message (-7h from msk)
    aioschedule.every().day.at("05:00").do(wisdom_create, config.uberpepolis_chat_id)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(every_day_wisdom())


# Ai func
# max_token_count = 4096
# messages = [
#
#     {
#
#         "role": "system",
#         "content": "Im PupAI, assistant at uberpepolis channel"
#     }
#
# ]
#
#
# def update(messages, role, content):
#     messages.append({"role": role, "content": content})
#
#
# def reset_messages():
#     messages.clear()
#
#     messages.append({
#
#         "role": "system",
#         "content": "Im PupAI, assistant at uberpepolis channel"
#
#     })
#
#
# async def pupai(message):
#     try:
#
#         update(messages, 'user', message.text)
#
#         response = openai.ChatCompletion.create(
#
#             model="gpt-3.5-turbo-16k",
#
#             messages=messages,
#
#             max_tokens=max_token_count,
#
#         )
#
#         if response['usage']['total_tokens'] >= max_token_count:
#             await message.answer(
#
#                 f'В данный момент вы использовали максимум токенов в рамках контекста:
#                 {response["usage"]["total_tokens"]}, будет произведена очистка памяти')
#
#             reset_messages()
#
#         await message.answer(response['choices'][0]['message']['content'], parse_mode="HTML")
#
#     except Exception:
#         await exception()


async def send_video(message, video_name):
    try:
        await bot.send_chat_action(message.chat.id, 'upload_video')
        time.sleep(2)
        video_path = f'{config.patch}/video/{video_name}.mp4'
        await bot.send_video(message.chat.id, video=open(video_path, 'rb'))
    except Exception:
        await exception()


# Regex handlers
key_video_names = {
    r'(\bг\s*о\s*й\s*д\s*а)': 'goyda',
    r'(\bday\s*is\s*ruined|\bdisappointment\s*is\s*immeasurable|\bдень\s*испорчен)': 'ruined',
    r'(\bя\s*уста*л)': 'tired',
    r'(\bчика\s*пака)': 'chica',
    r'(\bне\s*хочу\s.*работать)': 'work',
    r'(\bахует*)': 'ahuet',
    r'(\bв\s*о\s*т\s*т\s*у\s*т\s*в\s*е\s*р\s*ю)|(\bприду\b)': 'trust'
}

key_names = {
    r'(\bп.п\s*з.йди\s*|\bх.хл.\s*спросим)': send_random_quote,
    r'(\bп.п\s*м.др.сть)': wisdom_create,
    r'(\bп.зици.\s*техника)': technik_quote,
    r'(\bр\s*[ао]\s*с\s*и\s*я)': russia,
    r'(\bп\s*а\s*б\s*е\s*д\s*а)|(^😡)': enrage,
    r'(\bн\s*а\s*е\s*б\s*)': lying_voice_reply,
    r'(\bп.п\s*голос)': random_voice_reply
}

key_functions = {**{key: partial(send_video, video_name=value) for key, value in key_video_names.items()},
                 **key_names}


# Handlers


@dp.message_handler(content_types=['text'])
async def process_message(message: types.Message):
    rand = random.randrange(30)
    regex_condition_met = False
    for regex, function in key_functions.items():
        if re.search(regex, message.text.lower()):
            regex_condition_met = True
            if isinstance(function, str):
                await dp.bot.send_message(message.chat.id, function)
            else:
                await function(message)
            break
    if not regex_condition_met:
        if message.from_user.id == config.pupa_id:
            with open(f'{config.patch}/log/messages_log.txt', 'a', encoding='utf-8') as f:
                f.write(message.text)
                f.write('\n')
                f.close()
        if rand in [5, 15]:
            await send_random_quote(message)
        elif rand in [10, 20]:
            await hueficator(message)
        elif rand == 30:
            await send_sticker(message)
        else:
            pass


@dp.message_handler(content_types=['sticker'])
async def send_mp3(message: types.Message):
    if message.sticker.file_unique_id == 'AgADGwADsZeTFg':
        await enrage(message)
    elif message.sticker.file_unique_id == 'AgADPAADsZeTFg':
        await lying_voice_reply(message)
    else:
        pass


@dp.message_handler(content_types=['photo', 'video'])
async def handle_photo_or_video(message: types.Message):
    random_number = random.randint(1, 30)
    if random_number == 10:
        await send_random_quote(message)
    elif random_number == 15:
        await send_sticker(message)


@dp.message_handler(content_types=['voice', 'video_note'])
async def stt(message: types.voice and types.video_note):
    await speech_to_text(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

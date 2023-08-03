import asyncio
import logging
import random
import re
import subprocess
import textwrap as tw
import time
import traceback
from logging.handlers import RotatingFileHandler

import aioschedule
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


# Regex handlers
@dp.message_handler(regexp=r'(\bп.п\s*м.др.сть)')
async def wisdom(message: types.Message):
    await wisdom_create(message.chat.id)


@dp.message_handler(regexp=r'(\bп.зици.\s*техника)')
async def technik(message: types.Message):
    await technik_quote(message)


@dp.message_handler(regexp=r'(\bр\s*[ао]\s*с\s*и\s*я)')
async def send_gif(message: types.Message):
    await gif(message)


@dp.message_handler(regexp=r'(\bг\s*о\s*й\s*д\s*а)')
async def send_goyda(message: types.Message):
    await goyda(message)


@dp.message_handler(regexp=r'(\bн\s*а\s*е\s*б\s*)')
async def send_lie(message: types.Message):
    await lying_voice_reply(message)


@dp.message_handler(regexp=r'(\bday\s*is\s*ruined|\bdisappointment\s*is\s*immeasurable)')
async def send_ruined(message: types.Message):
    await ruined(message)


@dp.message_handler(regexp=r'(\bя\s*уста*л)')
async def send_tired(message: types.Message):
    await tired(message)


@dp.message_handler(regexp=r'(\bв\s*о\s*т\s*т\s*у\s*т\s*в\s*е\s*р\s*ю)|(\bприду\b)')
async def send_trust(message: types.Message):
    await trust(message)


@dp.message_handler(regexp=r'(\bп\s*а\s*б\s*е\s*д\s*а)|(^😡)')
async def send_mp3(message: types.Message):
    await enrage(message)


@dp.message_handler(regexp=r'(\bп.п\s*голос)')
async def send_voice(message: types.Message):
    await random_voice_reply(message)


@dp.message_handler(regexp=r'(\bп.п\s*з.йди\s*|\bх.хл.\s*спросим|\bpupetor.?bot)')
async def pupa_come(message: types.Message):
    await random_quote(message)


# Content type handlers
@dp.message_handler(content_types=['sticker'])
async def send_mp3(message: types.Message):
    if message.sticker.file_unique_id == 'AgADGwADsZeTFg':
        await enrage(message)
    else:
        pass


@dp.message_handler(content_types=['text'])
async def echo(message: types.Message):
    rand = random.randrange(30)
    if message.from_user.id == config.pupa_id:
        with open(f'{config.patch}/log/messages_log.txt', 'a', encoding='utf-8') as f:
            f.write(message.text)
            f.write('\n')
            f.close()
    if rand in [5, 15]:
        await random_quote(message)
    elif rand in [10, 20]:
        await hueficator(message)
    elif rand == 30:
        await sticker(message)
    else:
        pass


@dp.message_handler(content_types=['photo', 'video'])
async def echo2(message: types.message):
    rand = random.randrange(30)
    if rand == 10:
        await random_quote(message)
    elif rand == 15:
        await sticker(message)
    else:
        pass


@dp.message_handler(content_types=['voice', 'video_note'])
async def stt(message: types.voice and types.video_note):
    await speech_to_text(message)


# Functions

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


async def random_quote(message):
    try:
        await bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(2)
        await message.reply(random.choice(pupa_quotes).upper())
    except Exception:
        await exception()


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


async def gif(message):
    try:
        await bot.send_chat_action(message.chat.id, 'upload_video')
        time.sleep(2)
        await bot.send_animation(message.chat.id, animation=open(f'{config.patch}/gif/russia.gif', 'rb'))
    except Exception:
        await exception()


async def trust(message):
    try:
        await bot.send_chat_action(message.chat.id, 'upload_video')
        time.sleep(2)
        await bot.send_video(message.chat.id, video=open(f'{config.patch}/video/trust.mp4', 'rb'))
    except Exception:
        await exception()


async def goyda(message):
    try:
        await bot.send_chat_action(message.chat.id, 'upload_video')
        time.sleep(2)
        await bot.send_video(message.chat.id, video=open(f'{config.patch}/video/goyda.mp4', 'rb'))
    except Exception:
        await exception()


async def tired(message):
    try:
        await bot.send_chat_action(message.chat.id, 'upload_video')
        time.sleep(2)
        await bot.send_video(message.chat.id, video=open(f'{config.patch}/video/tired.mp4', 'rb'))
    except Exception:
        await exception()


async def ruined(message):
    try:
        await bot.send_chat_action(message.chat.id, 'upload_video')
        time.sleep(2)
        await bot.send_video(message.chat.id, video=open(f'{config.patch}/video/day_ruined.mp4', 'rb'))
    except Exception:
        await exception()


async def sticker(message):
    try:
        sti = open(f'{config.patch}/stickers/{random.randint(1, 35)}.webp', 'rb')
        await bot.send_chat_action(message.chat.id, 'choose_sticker')
        time.sleep(1)
        await bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)
    except Exception:
        await exception()


async def enrage(message):
    try:
        enrage_mp3 = open(f'{config.patch}/audio/enrage.mp3', 'rb')
        await bot.send_chat_action(message.chat.id, 'upload_document')
        time.sleep(1)
        await bot.send_audio(message.chat.id, enrage_mp3, reply_to_message_id=message.message_id)
    except Exception:
        await exception()


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


# async def every_day_wisdom2():
#     # Schedule message (-7h from msk)

#     aioschedule.every().day.at("17:49").do(wisdom_create, config.test_chat_id_2)
#     while True:
#         await aioschedule.run_pending()
#         await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(every_day_wisdom())
    # asyncio.create_task(every_day_wisdom2())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

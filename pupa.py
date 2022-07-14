import asyncio
import logging
import random
import subprocess
import textwrap as tw
import time
import traceback

import aioschedule
import speech_recognition as sr
from PIL import Image, ImageDraw, ImageFont
from aiogram import Bot, Dispatcher, executor, types
from gtts import gTTS

import config

# Configure logging
logging.basicConfig(filename=f'{config.patch}/log/debug.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

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


# Handlers
@dp.message_handler(regexp=r'(^п.п\s*м.др.сть\s*)')
async def wisdom(message: types.Message):
    await wisdom_create(message.chat.id)


@dp.message_handler(regexp=r'(^п.зиция\s*техника\s*)')
async def technik(message: types.Message):
    await technik_quote(message)


@dp.message_handler(regexp=r'(^р\s*[ао]\s*с\s*и\s*я\s*?)')
async def send_gif(message: types.Message):
    await gif(message)


@dp.message_handler(regexp=r'(^п.п\s*голос\s*)')
async def send_voice(message: types.Message):
    await random_voice_reply(message)


@dp.message_handler(regexp=r'(^п.п\s*з.йди\s*|^х.хл.\s*спросим\s*)')
async def pupa_come(message: types.Message):
    await random_quote(message)


@dp.message_handler(content_types=['text'])
async def echo(message: types.Message):
    if message.from_user.id == config.pupa_id:
        with open(f'{config.patch}/log/messages_log.txt', 'a', encoding='utf-8') as f:
            f.write(message.text)
            f.write('\n')
            f.close()
    if random.randint(1, 13) == 3:
        await random_quote(message)
    elif random.randint(1, 20) == 7:
        await sticker(message)
    else:
        pass


@dp.message_handler(content_types=['photo', 'video'])
async def echo2(message: types.message):
    if random.randint(1, 25) == 10:
        await random_quote(message)
    elif random.randint(1, 25) == 15:
        await sticker(message)
    else:
        pass


@dp.message_handler(content_types=['voice', 'video_note'])
async def stt(message: types.voice and types.video_note):
    await speech_to_text(message)


# Functions
async def speech_to_text(message):
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
                r.adjust_for_ambient_noise(source)
                r.pause_threshold = 0.6
                # listen for the data (load audio to memory)
                audio_data = r.record(source)
                # recognize (convert from speech to text)
                speech_text = r.recognize_google(audio_data, language='ru-RU', pfilter=0)
            await message.reply(speech_text)
        except sr.UnknownValueError:
            await message.reply(random.choice(['каво', 'не слышу', 'ммм?']))
    except Exception:
        await exception()


async def random_quote(message):
    try:
        await bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(1)
        await message.reply(random.choice(pupa_quotes))
    except Exception:
        await exception()


async def random_voice_reply(message):
    try:
        await bot.send_chat_action(message.chat.id, 'record_audio')
        time.sleep(1)
        s = gTTS(random.choice(pupa_quotes), lang='ru', slow=False)
        s.save(f'{config.patch}/audio/sample.ogg')
        await bot.send_voice(message.chat.id, reply_to_message_id=message.message_id,
                             voice=open(f'{config.patch}/audio/sample.ogg', 'rb'))
    except Exception:
        await exception()


async def technik_quote(message):
    try:
        await bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(1)
        await message.reply(random.choice(technik_quotes))
    except Exception:
        await exception()


async def wisdom_create(chat_id):
    try:
        await bot.send_chat_action(chat_id, 'upload_photo')  # show the bot "upload_photo"
        time.sleep(1)
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
    except Exception:
        await exception()


async def gif(message):
    try:
        await bot.send_chat_action(message.chat.id, 'upload_video')
        await bot.send_animation(message.chat.id, animation=open(f'{config.patch}/gif/russia.gif', 'rb'))
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


async def exception():
    await bot.send_message(config.wiz_id, f"```\n{traceback.format_exc()}```", parse_mode="Markdown")


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

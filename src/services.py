import asyncio
import random
import subprocess
import time
import textwrap as tw

import speech_recognition as sr
from aiogram import Bot
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont

import config
from helpers import exception
import utils


async def speech_to_text(bot: Bot, message):
    max_attempts = 2
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

            await bot.download_file(file_info.file_path, f'{config.data_folder}/audio/new_file.mp4')
            
            # Convert mp4 to wav
            src_filename = f'{config.data_folder}/audio/new_file.mp4'
            dest_filename = f'{config.data_folder}/audio/sample.wav'
            subprocess.run(['ffmpeg', '-y', '-i', src_filename, dest_filename], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Convert speech-to-text
            try:
                r = sr.Recognizer()
                with sr.AudioFile(dest_filename) as source:
                    r.adjust_for_ambient_noise(source, duration=0)
                    r.pause_threshold = 0.8
                    audio_data = r.record(source)
                    speech_text = r.recognize_google(audio_data, language='ru-RU', pfilter=0)
                await message.reply(speech_text)
                break
            except sr.UnknownValueError:
                await message.reply(random.choice(['каво', 'не слышу', 'ммм?']))
        except Exception:
            await exception()
        attempt += 1
        await asyncio.sleep(10)


async def random_voice_reply(bot: Bot, message):
    try:
        await bot.send_chat_action(message.chat.id, 'record_audio')
        time.sleep(2)
        s = gTTS(random.choice(utils.get_pupa_quotes()), lang='ru', slow=False)
        s.save(f'{config.data_folder}/audio/sample.ogg')
        await bot.send_voice(message.chat.id, reply_to_message_id=message.message_id,
                           voice=open(f'{config.data_folder}/audio/sample.ogg', 'rb'))
    except Exception:
        await exception()


async def lying_voice_reply(bot: Bot, message):
    try:
        await bot.send_chat_action(message.chat.id, 'record_audio')
        time.sleep(2)
        await bot.send_voice(message.chat.id, reply_to_message_id=message.message_id,
                           voice=open(f'{config.data_folder}/audio/lying.ogg', 'rb'))
    except Exception:
        await exception()


async def enrage(bot: Bot, message):
    audio_path = f'{config.data_folder}/audio/enrage.mp3'
    try:
        await bot.send_chat_action(message.chat.id, 'upload_document')
        await asyncio.sleep(1)
        with open(audio_path, 'rb') as audio_file:
            await bot.send_audio(message.chat.id, audio_file, reply_to_message_id=message.message_id)
    except Exception:
        await exception()


async def wisdom_create(bot, chat_id):
    max_attempts = 3
    attempt = 0
    
    while attempt < max_attempts:
        try:
            await bot.send_chat_action(chat_id, 'upload_photo')
            time.sleep(2)
            
            # Make image with quote
            img = Image.open(f'{config.data_folder}/pupaups/{random.randint(1, 12)}.jpg')
            position = (320, 0)
            text = random.choice(utils.get_pupa_wisdom())
            color = [(255, 165, 0), (0, 128, 128), (128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 0, 128)]
            dedented_text = tw.fill(tw.dedent(text).strip(), width=15)
            font = ImageFont.truetype(f'{config.data_folder}/font/Lobster-Regular.ttf', 60)
            
            ImageDraw.Draw(img).multiline_text(
                position, tw.fill(dedented_text, width=15), font=font, stroke_width=20,
                stroke_fill=random.choice(color), spacing=-40, anchor='ma', align='center'
            )
            
            image_name_output = f'{config.data_folder}/pupaups/wisdom.jpg'
            img.save(image_name_output)

            # Send image
            await bot.send_photo(chat_id, photo=open(image_name_output, 'rb'))
            img.close()
            break
        except Exception:
            await exception()
        attempt += 1
        await asyncio.sleep(10)
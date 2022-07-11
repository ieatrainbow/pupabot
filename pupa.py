import datetime
import random
import re
import subprocess
import threading
import time
import traceback

import schedule
import speech_recognition as sr
import telebot
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS

import config

# The token that @botfather give
bot = telebot.TeleBot(config.tbtoken)

# Opening Files
pupa = open(f'{config.patch}/text/pupa_q.txt', 'r', encoding='UTF-8')
technik = open(f'{config.patch}/text/technik_q.txt', 'r', encoding='UTF-8')

pupa_trig = open(f'{config.patch}/text/pupa_t.txt', 'r', encoding='UTF-8')
technik_trig = open(f'{config.patch}/text/technik_t.txt', 'r', encoding='UTF-8')

pupa_w = open(f'{config.patch}/text/pupa_w.txt', 'r', encoding='UTF-8')
pupa_g = open(f'{config.patch}/text/pupa_g.txt', 'r', encoding='UTF-8')

# Dividing line by line
pupa_quotes = pupa.read().split('\n')
technik_quotes = technik.read().split('\n')
pupa_wisdom = pupa_w.read().split(';')
pupa_gena = pupa_g.read().split('\n')

pupa_triggers = pupa_trig.read().split('\n')
technik_triggers = technik_trig.read().split('\n')

wisdom_triggers = ['пупмудрость']
voice_triggers = ['пупголос']
gif_triggers = ['расия']

# Closing files
pupa.close()
pupa_trig.close()
technik.close()
technik_trig.close()
pupa_w.close()
pupa_g.close()

CONTENT_TYPES = ['text', 'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact',
                 'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo',
                 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id',
                 'migrate_from_chat_id', 'pinned_message']


@bot.message_handler(content_types=CONTENT_TYPES)
def handle(message):
    try:
        # Set the size of the random
        rand = random.randint(1, 35)

        # Logging messages from user
        if message.from_user.id == config.pupa_id and message.content_type == 'text':
            with open(f'{config.patch}/log/messages_log.txt', 'a', encoding='utf-8') as f:
                f.write(message.text)
                f.write('\n')
                f.close()

        # If simple text
        if message.content_type == 'text':
            # Removing extra characters from a string
            tg_mess = re.sub(r"[$^&()+#%!@*,.? =_'-]", "", message.text.casefold())

            # If match with triggers
            if tg_mess in pupa_triggers:
                random_reply(message)
            elif tg_mess in voice_triggers:
                random_voice_reply(message)
            elif tg_mess in wisdom_triggers:
                wisdom_create(message.chat.id)
            elif tg_mess in technik_triggers:
                bot.send_chat_action(message.chat.id, 'typing')
                time.sleep(2)
                bot.reply_to(message, random.choice(technik_quotes))
            elif tg_mess in gif_triggers:
                bot.send_chat_action(message.chat.id, 'upload_video')
                time.sleep(2)
                bot.send_animation(message.chat.id, animation=open(f'{config.patch}/gif/russia.gif', 'rb'),
                                   reply_to_message_id=message.message_id)

            # If message from specific user and random
            elif message.from_user.id == config.major_id and rand == 2:
                major_reply(message)

            # Random choice of message to reply with a sticker
            elif rand == 3:
                sti = open(f'{config.patch}/stickers/{random.randint(1, 35)}.webp', 'rb')
                bot.send_chat_action(message.chat.id, 'choose_sticker')
                time.sleep(2)
                bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)

            # Random choice of message to reply
            elif rand in [1, 35]:
                random_reply(message)
            elif rand == 35:
                random_voice_reply(message)

        # If other content type
        elif message.content_type not in ['text', 'voice', 'video_note']:
            # If message from specific user and random
            if message.from_user.id == config.major_id and rand == 1:
                major_reply(message)

            # Random choice of message to reply
            elif rand in [1, 35]:
                random_reply(message)

        elif message.content_type in ['voice', 'video_note']:
            voice_to_text(message)

    except Exception:
        with open(f'{config.patch}/log/log.txt', 'a', encoding='utf-8') as f:
            f.write(f'{datetime.datetime.now()}\n{traceback.format_exc()}\n')
            f.close()
        with open(f'{config.patch}/log/last_error.txt', 'w', encoding='utf-8') as f:
            f.write(f'{datetime.datetime.now()}\n{traceback.format_exc()}\n')
            f.close()
        bot.send_document(config.wiz_id, document=open(f'{config.patch}/last_error.txt', 'rb'))


def major_reply(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(2)
    bot.reply_to(message, random.choice(pupa_gena))


def random_reply(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(2)
    bot.reply_to(message, random.choice(pupa_quotes))


def random_voice_reply(message):
    bot.send_chat_action(message.chat.id, 'record_audio')
    time.sleep(2)
    # tts = random.choice(pupa_quotes)
    s = gTTS(random.choice(pupa_quotes), lang='ru', slow=False)
    s.save(f'{config.patch}/audio/sample.ogg')
    bot.send_voice(message.chat.id, reply_to_message_id=message.message_id,
                   voice=open(f'{config.patch}/audio/sample.ogg', 'rb'))


def wisdom_create(chat_id):
    bot.send_chat_action(chat_id, 'upload_photo')  # show the bot "upload_photo"
    time.sleep(2)
    # Make image with quote
    img = Image.open(f'{config.patch}/pupaups/{random.randint(1, 12)}.jpg')
    position = (320, 50)
    text = random.choice(pupa_wisdom)
    font = ImageFont.truetype(f'{config.patch}/font/Lobster-Regular.ttf', 38)
    ImageDraw.Draw(img).multiline_text(position, text, font=font, stroke_width=2, stroke_fill=0, anchor='ms',
                                       align='center')
    image_name_output = f'{config.patch}/pic/wisdom.jpg'
    img.save(image_name_output)

    # Send image
    bot.send_photo(chat_id, photo=open(image_name_output, 'rb'))
    img.close()


def voice_to_text(message):
    bot.send_chat_action(message.chat.id, 'typing')
    # Save file
    if message.content_type == 'voice':
        file_info = bot.get_file(message.voice.file_id)
    elif message.content_type == 'video_note':
        file_info = bot.get_file(message.video_note.file_id)
    else:
        file_info = None
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'{config.patch}/audio/new_file.mp4', 'wb') as new_file:
        new_file.write(downloaded_file)

    # Convert mp4 to wav
    src_filename = f'{config.patch}/audio/new_file.mp4'
    dest_filename = f'{config.patch}/audio/sample.wav'
    subprocess.run(['ffmpeg', '-y', '-i', src_filename, dest_filename], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)

    # Convert speech-to-text
    try:
        r = sr.Recognizer()
        with sr.AudioFile(dest_filename) as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            speech_text = r.recognize_google(audio_data, language='ru-RU')
        bot.reply_to(message, speech_text)
    except Exception:
        bot.reply_to(message, random.choice(['каво', 'не слышу', 'ммм?']))


def schedule_job():
    # Schedule message (-7h from msk)
    schedule.every().day.at("05:00").do(wisdom_create, config.uberpepolis_chat_id)
    while True:
        schedule.run_pending()
        time.sleep(1)


def run_bot():
    bot.polling()


if __name__ == "__main__":
    t1 = threading.Thread(target=run_bot)
    t2 = threading.Thread(target=schedule_job)
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()

import random
import re
import time

import telebot
from PIL import Image, ImageDraw, ImageFont

import config

# The token that @botfather give
bot = telebot.TeleBot(config.tbtoken)

# Opening Files
pupa = open(f'{config.patch}/pupa_q.txt', 'r', encoding='UTF-8')
technik = open(f'{config.patch}/technik_q.txt', 'r', encoding='UTF-8')

pupa_trig = open(f'{config.patch}/pupa_t.txt', 'r', encoding='UTF-8')
technik_trig = open(f'{config.patch}/technik_t.txt', 'r', encoding='UTF-8')

pupa_w = open(f'{config.patch}/pupa_w.txt', 'r', encoding='UTF-8')
pupa_g = open(f'{config.patch}/pupa_g.txt', 'r', encoding='UTF-8')

# Dividing line by line
pupa_quotes = pupa.read().split('\n')
technik_quotes = technik.read().split('\n')
pupa_wisdom = pupa_w.read().split(';')
pupa_gena = pupa_g.read().split('\n')

pupa_triggers = pupa_trig.read().split('\n')
technik_triggers = technik_trig.read().split('\n')

wisdom_triggers = ['пупмудрость']

# Closing files
pupa.close()
pupa_trig.close()
technik.close()
technik_trig.close()
pupa_w.close()

CONTENT_TYPES = ['text', 'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact',
                 'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo',
                 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id',
                 'migrate_from_chat_id', 'pinned_message']


@bot.message_handler(content_types=CONTENT_TYPES)
def handle(message):
    try:
        # Logging messages from user
        if message.from_user.id == config.pupa_id and message.content_type == 'text':
            with open(f'{config.patch}/messages_log.txt', 'a', encoding='utf-8') as f:
                f.write(message.text)
                f.write('\n')
                f.close()

        # Set the size of the random
        rand = random.randint(1, 10)

        # If simple text
        if message.content_type == 'text':
            # Removing extra characters from a string
            tg_mess = re.sub(r"[$^&()+#%!@*,.? =_'-]", "", message.text.casefold())

            # If match with pupa_triggers
            if tg_mess in pupa_triggers:
                bot.send_chat_action(message.chat.id, 'typing')  # show the bot "typing" (max. 5 secs)
                time.sleep(3)
                bot.reply_to(message, random.choice(pupa_quotes))

            # If match with technik_triggers
            elif tg_mess in technik_triggers:
                bot.send_chat_action(message.chat.id, 'typing')
                time.sleep(3)
                bot.reply_to(message, random.choice(technik_quotes))

            # If match with wisdom_triggers
            elif tg_mess in wisdom_triggers:
                bot.send_chat_action(message.chat.id, 'upload_photo')  # show the bot "upload_photo"
                time.sleep(3)

                # Make image with quote
                img = Image.open(f'{config.patch}/pupaups/{random.randint(1, 12)}.jpg')
                position = (320, 50)
                text = random.choice(pupa_wisdom)
                font = ImageFont.truetype(f'{config.patch}/Lobster-Regular.ttf', 38)
                ImageDraw.Draw(img).multiline_text(position, text, font=font, stroke_width=2, stroke_fill=0,
                                                   anchor='ms',
                                                   align='center')

                image_name_output = f'{config.patch}/wisdom.jpg'
                img.save(image_name_output)
                # Send image
                bot.send_photo(message.chat.id, photo=open(image_name_output, 'rb'))
                img.close()

            # If message from specific user and random
            elif message.from_user.id == config.major_id and rand == 1:
                major_reply(message)

            # Random choice of message to reply with a sticker
            elif rand == 2:
                sti = open(f'{config.patch}/stickers/{random.randint(1, 35)}.webp', 'rb')
                bot.send_chat_action(message.chat.id, 'choose_sticker')
                time.sleep(3)
                bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)

            # Random choice of message to reply
            elif rand in [7, 10]:
                random_reply(message)

        # If other content type
        elif message.content_type != 'text':
            # Random choice of message to reply
            if rand == 7:
                random_reply(message)

            # If message from specific user and random
            elif message.from_user.id == config.major_id and rand == 1:
                major_reply(message)

    except Exception as e:
        with open(f'{config.patch}/log.txt', 'a', encoding='utf-8') as f:
            f.write(str(e))
            f.write('\n')
            f.close()
        bot.send_message(message.chat.id, 'Im broke (help me, guys)')


def major_reply(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(3)
    bot.reply_to(message, random.choice(pupa_gena))


def random_reply(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(3)
    bot.reply_to(message, random.choice(pupa_quotes))


bot.polling()

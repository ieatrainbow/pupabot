import random
import re
import time

import telebot
from PIL import Image, ImageDraw, ImageFont

import config

# The token that @botfather give
bot = telebot.TeleBot(config.tbtoken)

# Opening quotes
pupa = open(f'{config.patch}/pupa_q.txt', 'r', encoding='UTF-8')
technik = open(f'{config.patch}/technik_q.txt', 'r', encoding='UTF-8')

# Opening triggers
pupa_trig = open(f'{config.patch}/pupa_t.txt', 'r', encoding='UTF-8')
technik_trig = open(f'{config.patch}/technik_t.txt', 'r', encoding='UTF-8')

# Opening wisdom
pupa_w = open(f'{config.patch}/pupa_w.txt', 'r', encoding='UTF-8')

# Dividing quotes line by line
pupa_quotes = pupa.read().split('\n')
technik_quotes = technik.read().split('\n')
pupa_wisdom = pupa_w.read().split(';')

# Dividing triggers line by line
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

        # Set the size of the random
        rand = random.randint(1, 7)

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

                img = Image.open(f'{config.patch}/{random.randint(1, 4)}.jpg')
                position = (320, 50)

                text = random.choice(pupa_wisdom)
                font = ImageFont.truetype(f'{config.patch}/Lobster-Regular.ttf', 38)

                ImageDraw.Draw(img).multiline_text(position, text, font=font, stroke_width=2, stroke_fill=0,
                                                   anchor='ms',
                                                   align='center')

                image_name_output = f'{config.patch}/wisdom.jpg'
                img.save(image_name_output)

                bot.send_photo(message.chat.id, photo=open(image_name_output, 'rb'))
                img.close()

            # Random selection of a message for a reply
            elif rand == 3:
                bot.send_chat_action(message.chat.id, 'typing')
                time.sleep(3)
                bot.reply_to(message, random.choice(pupa_quotes))

            # Inaction if trigger words did not come
            else:
                pass

        # If other content type
        elif message.content_type != 'text':

            # Random selection of a message for a reply
            if rand == 3:
                bot.send_chat_action(message.chat.id, 'typing')  # show the bot "typing" (max. 5 secs)
                time.sleep(3)
                bot.reply_to(message, random.choice(pupa_quotes))

            # Inaction if trigger words did not come
            else:
                pass

        else:
            pass

    except Exception:
        pass


bot.polling()

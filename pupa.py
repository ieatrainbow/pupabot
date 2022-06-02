import random
import re
import time
import config

import telebot

# The token that @botfather give
bot = telebot.TeleBot(config.tbtoken)

# Opening quotes
pupa = open('data/pupa_q.txt', 'r', encoding='UTF-8')
# pupa = open('/home/pupabot/data/pupa_q.txt', 'r', encoding='UTF-8')
technik = open('data/technik_q.txt', 'r', encoding='UTF-8')
# technik = open('/home/pupabot/data/technik_q.txt', 'r', encoding='UTF-8')

# Opening triggers
pupa_trig = open('data/pupa_t.txt', 'r', encoding='UTF-8')
# pupa_trig = open('/home/pupabot/data/pupa_t.txt', 'r', encoding='UTF-8')
technik_trig = open('data/technik_t.txt', 'r', encoding='UTF-8')
# technik_trig = open('/home/pupabot/data/technik_t.txt', 'r', encoding='UTF-8')

# Dividing quotes line by line
pupa_quotes = pupa.read().split('\n')
technik_quotes = technik.read().split('\n')

# Dividing triggers line by line
pupa_triggers = pupa_trig.read().split('\n')
technik_triggers = technik_trig.read().split('\n')

# Closing files
pupa.close()
pupa_trig.close()
technik.close()
technik_trig.close()

CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]


@bot.message_handler(content_types=CONTENT_TYPES)
def handle(message):
    try:

        # Set the size of the random
        rand = random.randint(1, 7)

        # If simple text
        if message.content_type == "text":
            # Removing extra characters from a string
            tg_mess = re.sub(r"[$^&()+#%!@*,.? =_'-]", "", message.text.casefold())

            # If match with pupa_triggers
            if tg_mess in pupa_triggers:
                bot.send_chat_action(message.chat.id, 'typing')  # show the bot "typing" (max. 5 secs)
                time.sleep(3)
                bot.reply_to(message, random.choice(pupa_quotes))

            # If match with technik_triggers
            elif tg_mess in technik_triggers:
                bot.send_chat_action(message.chat.id, 'typing')  # show the bot "typing" (max. 5 secs)
                time.sleep(3)
                bot.reply_to(message, random.choice(technik_quotes))

            # Random selection of a message for a reply
            elif rand == 3:
                bot.send_chat_action(message.chat.id, 'typing')  # show the bot "typing" (max. 5 secs)
                time.sleep(3)
                bot.reply_to(message, random.choice(pupa_quotes))

            # Inaction if trigger words did not come
            else:
                pass

        # If other content type
        elif message.content_type != "text":

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

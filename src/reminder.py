import json
import os
import asyncio
import datetime
import logging
import config
from config import data_folder, call_link

REMINDER_FILE = f"{data_folder}/reminders.json"

ACTIVE_MEMBERS = set()

def get_reminders():
    if os.path.exists(REMINDER_FILE):
        try:
            with open(REMINDER_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        except: return []
    return []

def add_reminder(time_str):
    times = get_reminders()
    if time_str not in times:
        times.append(time_str)
        with open(REMINDER_FILE, "w", encoding='utf-8') as f:
            json.dump(times, f)

def remove_reminder(time_str):
    times = get_reminders()
    if time_str in times:
        times.remove(time_str)
        with open(REMINDER_FILE, "w", encoding='utf-8') as f:
            json.dump(times, f)

def update_members(username):
    """Просто добавляем в сет в памяти"""
    if username:
        ACTIVE_MEMBERS.add(f"@{username}")

async def reminder_cron(bot):
    logging.info("--- ЦИКЛ REMINDER ЗАПУЩЕН ЖЭС ---")
    while True:
        try:
            # Получаем текущее время
            now = datetime.datetime.now().strftime("%H:%M")
            reminders = get_reminders()
            
            # Для отладки: печатаем каждую минуту, что видит бот
            # logging.debug(f"Проверка времени: {now}. В очереди: {reminders}")

            if now in reminders:
                logging.info(f"!!! СРАБОТАЛО ВРЕМЯ {now} !!!")
                
                # Сразу удаляем из списка, чтобы не спамить в эту же минуту
                remove_reminder(now)
                
                # Берем список мемберов (убедись, что ты им писал в чат!)
                tags = " ".join(ACTIVE_MEMBERS) if ACTIVE_MEMBERS else "а каво звать..."
                
                chat_id = config.uberpepolis_chat_id
                text = (
                    f"🚨 **БОЖЕ** 🚨\n\n"
                    f"МАЛЫШИ НАШИ ПОДЪЕМ: {tags}\n\n"
                    f"ВРЕМЯ {now} ПЛЮС МИНУС\n\n"
                    f"ПОЖИЛАЯ КОНФЕРЕНЦИЯ: {call_link}"
                )
                
                # ОТПРАВКА
                logging.info(f"Пытаюсь отправить в чат {chat_id}...")
                await bot.send_message(chat_id, text)
                logging.info("Отправлено успешно!")
                
                # Спим 61 сек, чтобы проскочить эту минуту
                await asyncio.sleep(61)
            
        except Exception as e:
            logging.error(f"ОШИБКА В ЦИКЛЕ ДЕСАНТА: {e}")
            
        # Проверяем каждые 15 секунд для точности
        await asyncio.sleep(15)
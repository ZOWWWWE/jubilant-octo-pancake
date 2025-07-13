import os
import asyncio
import sqlite3
from pyrogram import Client
import random

# Конфиг
API_ID = os.getenv("API_ID", 12345)  # Из переменных Replit
API_HASH = os.getenv("API_HASH", "ваш_api_hash")  
PHONE = "+79226900408"  # Ваш номер Telegram
TARGET = "@StaticNum_bot"  # Куда отправлять
DB_NAME = "phones.db"  # База данных

# Инициализация БД
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS phones (
        id INTEGER PRIMARY KEY,
        number TEXT UNIQUE
    )
    """)
    conn.commit()
    conn.close()

# Генератор номеров (без повторов в БД)
def generate_phone():
    while True:
        first_digit = '8'
        other_digits = random.sample('0123456789', 10)
        phone = first_digit + ''.join(other_digits)
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM phones WHERE number = ?", (phone,))
        exists = cursor.fetchone()
        conn.close()
        
        if not exists:
            return phone

# Сохранение номера в БД
def save_phone(phone):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO phones (number) VALUES (?)", (phone,))
    conn.commit()
    conn.close()

# Отправка в Telegram
async def send_telegram_message():
    init_db()  # Создаём БД при старте
    
    async with Client("my_account", API_ID, API_HASH) as app:
        await app.start(PHONE)
        print("✅ Авторизация успешна!")
        
        while True:
            phone = generate_phone()
            save_phone(phone)
            await app.send_message(TARGET, phone)
            print(f"📞 Отправлен номер: {phone}")
            await asyncio.sleep(86400)  # 24 часа

if __name__ == "__main__":
    asyncio.run(send_telegram_message())
import asyncio
import logging
from datetime import datetime, timedelta
import pytz
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Твой токен
TOKEN = "8471259728:AAENcc8jzuCepgfOWuFZd3FjAo0tRsjiWhE"

# Часовой пояс Челябинска
tz = pytz.timezone("Asia/Yekaterinburg")

# Создаём бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Логирование (для дебага)
logging.basicConfig(level=logging.INFO)

# Список сообщений для напоминаний
reminders = [
    "Иля, пора пить таблетки 💊",
    "Не забудь про таблетки, Иля 🌸",
    "Таблетки ждут тебя, Иля ❤️",
    "Илюша, выпей таблеточки 🙏",
    "Иля, самое время для лекарств ⚕️",
]

# Кнопки для ответа
keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Я выпила"), KeyboardButton(text="Не выпила ещё")]],
    resize_keyboard=True
)

# Функция отправки ежедневного напоминания
async def send_daily_reminder(user_id: int):
    message = reminders[datetime.now(tz).day % len(reminders)]
    await bot.send_message(user_id, message, reply_markup=keyboard)

    # Запускаем повторные напоминания (каждые 10 минут в течение часа)
    scheduler = AsyncIOScheduler(timezone=tz)
    end_time = datetime.now(tz) + timedelta(hours=1)

    def condition():
        return datetime.now(tz) < end_time

    async def repeat():
        if condition():
            await bot.send_message(user_id, "Пей давай 💊", reply_markup=keyboard)

    scheduler.add_job(repeat, "interval", minutes=10)
    scheduler.start()

# Хендлер на команду /start
@dp.message(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Привет, Иля 🌷 Я буду напоминать тебе пить таблетки каждый день в 18:00!")

    # Планировщик для ежедневных напоминаний
    scheduler = AsyncIOScheduler(timezone=tz)
    scheduler.add_job(send_daily_reminder, "cron", hour=18, minute=0, args=[message.from_user.id])
    scheduler.start()

# Ответы на кнопки
@dp.message()
async def reply_handler(message: types.Message):
    if message.text == "Я выпила":
        await message.answer("Умничка моя ❤️ Напоминания выключены до завтра!")
    elif message.text == "Не выпила ещё":
        await message.answer("Ну пей давай 💊")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

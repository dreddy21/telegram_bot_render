import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz

TOKEN = "8471259728:AAENcc8jzuCepgfOWuFZd3FjAo0tRsjiWhE"
bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone=pytz.timezone("Asia/Yekaterinburg"))

# Фразы для напоминаний
reminders = [
    "Иля, пора пить таблетки 💊",
    "Не забудь про таблетки, Иля ✨",
    "Таблеточки ждут тебя, Иля ❤️",
    "Пей давай, Иля 😘"
]

# Клавиатура
keyboard = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="Я выпила"),
        KeyboardButton(text="Не выпила ещё")
    ]],
    resize_keyboard=True
)

# Активные напоминания
active_jobs = {}

async def send_reminders(chat_id):
    active_jobs[chat_id] = True
    for i in range(6):  # 6 раз по 10 минут = час
        if chat_id not in active_jobs:
            break
        await bot.send_message(chat_id, reminders[i % len(reminders)], reply_markup=keyboard)
        await asyncio.sleep(600)
    active_jobs.pop(chat_id, None)

@dp.message(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer("Привет, Иля! Я буду напоминать тебе про таблетки ❤️", reply_markup=keyboard)
    # каждый день в 18:00 запускать напоминалки
    scheduler.add_job(send_reminders, "cron", hour=18, minute=0, args=[message.chat.id])

@dp.message()
async def reply_handler(message: types.Message):
    chat_id = message.chat.id
    if message.text == "Я выпила":
        active_jobs.pop(chat_id, None)
        await message.answer("Умничка моя ❤️")
    elif message.text == "Не выпила ещё":
        await message.answer("Пей давай 😠")

async def main():
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Главное меню с красивыми кнопками
def get_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏰ Настроить напоминание", callback_data="remind")],
        [InlineKeyboardButton(text="📰 Новости и патчи", callback_data="news")],
        [InlineKeyboardButton(text="📊 Моя статистика", callback_data="stats")],
        [InlineKeyboardButton(text="📅 Расписание турниров", callback_data="schedule")],
        [InlineKeyboardButton(text="ℹ️ О боте", callback_data="about")]
    ])

@dp.message(CommandStart())
async def start(message: types.Message):
    text = (
        f"👋 **Привет, {message.from_user.first_name}!**\n\n"
        "Что я умею:\n"
        "⏰ — напоминания\n"
        "📰 — новости и патчи\n"
        "📊 — проверка профиля\n"
        "📅 — расписание турниров\n\n"
        "Нажми на нужную кнопку 👇"
    )
    await message.answer(text, reply_markup=get_main_menu(), parse_mode="Markdown")

# Обработка кнопок (редактирование сообщения)
@dp.callback_query(F.data == "schedule")
async def schedule(callback: types.CallbackQuery):
    text = (
        "📅 **Ближайшие турниры:**\n\n"
        "1️⃣ **M8 Wild Card**\n"
        "📍 Бангкок, Таиланд\n"
        "🗓 17–20 декабря 2026\n\n"
        "2️⃣ **M8 Main Stage**\n"
        "📍 Стамбул, Турция\n"
        "🗓 Январь 2027\n"
        "💵 Призовой фонд: $1,000,000"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📺 Смотреть матчи", url="https://www.youtube.com/@MobileLegendsEsports")],
        [InlineKeyboardButton(text="⬅️ В меню", callback_data="back")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(F.data == "about")
async def about(callback: types.CallbackQuery):
    text = (
        "🤖 **О боте**\n\n"
        "Я — твой личный помощник по Mobile Legends. Моя задача — следить за порядком, чтобы ты всегда был в курсе событий и не пропускал важное."
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ В меню", callback_data="back")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(F.data == "news")
async def news(callback: types.CallbackQuery):
    text = (
        "📰 **Свежие новости и патчи:**\n\n"
        "Нажми кнопку ниже, чтобы перейти на официальный сайт. Там ты найдешь все обновления и анонсы."
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Открыть новости", url="https://www.mobilelegends.com/news")],
        [InlineKeyboardButton(text="⬅️ В меню", callback_data="back")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(F.data == "stats")
async def stats(callback: types.CallbackQuery):
    text = (
        "📊 **Проверка профиля:**\n\n"
        "Нажми кнопку ниже, чтобы открыть трекер. Введи туда свой ID и Zone ID из игры, и увидишь свой уровень, ранг и винрейт."
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔎 Открыть трекер", url="https://www.mobilelegends.com/")],
        [InlineKeyboardButton(text="⬅️ В меню", callback_data="back")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(F.data == "remind")
async def remind(callback: types.CallbackQuery):
    text = "⏰ Напоминания в разработке (скоро тут будет форма)."
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ В меню", callback_data="back")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard)

@dp.callback_query(F.data == "back")
async def back(callback: types.CallbackQuery):
    text = (
        f"👋 **С возвращением, {callback.from_user.first_name}!**\n\n"
        "Выбирай, куда двигаемся дальше:"
    )
    await callback.message.edit_text(text, reply_markup=get_main_menu(), parse_mode="Markdown")

# Веб-сервер для проверки Render
async def handle(request):
    return web.Response(text="Bot is alive!")

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 8080)))
    await site.start()
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

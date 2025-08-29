# weather_bot.py
import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# === НАСТРОЙКИ ===
TELEGRAM_TOKEN = "ВСТАВЬ_СВОЙ_TELEGRAM_TOKEN"
OPENWEATHER_API_KEY = "ВСТАВЬ_СВОЙ_OPENWEATHER_KEY"
BASE_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

# === КОМАНДА /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌤️ Привет! Я — бот, который расскажет погоду.\n"
        "Напиши мне название города, например: Москва"
    )

# === ОБРАБОТКА СООБЩЕНИЯ (название города) ===
async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text.strip()

    # Формируем URL запроса
    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'lang': 'ru',
        'units': 'metric'  # градусы Цельсия
    }

    response = requests.get(BASE_WEATHER_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        city_name = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description'].capitalize()
        wind_speed = data['wind']['speed']

        # Смайлики для атмосферы
        emoji = "🌤️"
        if "облач" in description.lower():
            emoji = "☁️"
        elif "дожд" in description.lower():
            emoji = "🌧️"
        elif "гроз" in description.lower():
            emoji = "⛈️"
        elif "снег" in description.lower():
            emoji = "❄️"
        elif "ясно" in description.lower():
            emoji = "☀️"

        weather_text = (
            f"{emoji} <b>Погода в {city_name}, {country}</b>\n"
            f"🌡️ <b>Температура:</b> {temp}°C (ощущается как {feels_like}°C)\n"
            f"📝 <b>Состояние:</b> {description}\n"
            f"💧 <b>Влажность:</b> {humidity}%\n"
            f"💨 <b>Скорость ветра:</b> {wind_speed} м/с"
        )

        await update.message.reply_text(weather_text, parse_mode='HTML')

    else:
        await update.message.reply_text(
            "❌ Не удалось найти погоду для этого города.\n"
            "Проверь название и попробуй снова."
        )

# === ОСНОВНАЯ ФУНКЦИЯ ===
def main():
    print("Запуск бота...")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_weather))

    print("Бот запущен! Нажми Ctrl+C для остановки.")
    app.run_polling()

if __name__ == '__main__':
    main()

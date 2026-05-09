import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 8000))

# Telegram limits: 50MB for bots when sending files
MAX_FILE_SIZE_MB = 50 

DOWNLOADS_DIR = "downloads"

if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

# Multilingual strings
STRINGS = {
    'uz': {
        'welcome': "👋 Assalomu alaykum! YouTube Shorts yuklovchi botga xush kelibsiz.\n\nIltimos, tilni tanlang:",
        'lang_selected': "🇺🇿 O'zbek tili tanlandi. Menga Shorts havolasini yuboring!",
        'invalid_url': "❌ Iltimos, haqiqiy YouTube Shorts havolasini yuboring.",
        'fetching': "🔍 Shorts ma'lumotlari olinmoqda...",
        'downloading': "⏳ Yuklanmoqda... Iltimos, kuting.",
        'sending': "🚀 Yuborilmoqda...",
        'error': "❌ Xatolik yuz berdi.",
        'too_large': "⚠️ Fayl juda katta. Telegram limiti 50MB.",
        'done': "✅ Yuklab olindi!",
        'start_over': "🔄 Qayta boshlash uchun /start bosing."
    },
    'ru': {
        'welcome': "👋 Здравствуйте! Добро пожаловать в бот для загрузки YouTube Shorts.\n\nПожалуйста, выберите язык:",
        'lang_selected': "🇷🇺 Выбран русский язык. Отправьте мне ссылку на Shorts!",
        'invalid_url': "❌ Пожалуйста, отправьте корректную ссылку на YouTube Shorts.",
        'fetching': "🔍 Получение информации о Shorts...",
        'downloading': "⏳ Загрузка... Пожалуйста, подождите.",
        'sending': "🚀 Отправка...",
        'error': "❌ Произошла ошибка.",
        'too_large': "⚠️ Файл слишком большой. Лимит Telegram 50МБ.",
        'done': "✅ Загружено!",
        'start_over': "🔄 Нажмите /start, чтобы начать заново."
    },
    'en': {
        'welcome': "👋 Hello! Welcome to the YouTube Shorts downloader bot.\n\nPlease choose your language:",
        'lang_selected': "🇺🇸 English selected. Send me a Shorts link!",
        'invalid_url': "❌ Please send a valid YouTube Shorts link.",
        'fetching': "🔍 Fetching Shorts info...",
        'downloading': "⏳ Downloading... Please wait.",
        'sending': "🚀 Sending...",
        'error': "❌ An error occurred.",
        'too_large': "⚠️ File too large. Telegram limit is 50MB.",
        'done': "✅ Downloaded!",
        'start_over': "🔄 Press /start to start over."
    }
}

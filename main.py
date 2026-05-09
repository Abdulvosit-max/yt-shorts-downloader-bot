import uvicorn
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import BOT_TOKEN, PORT
import bot

app = FastAPI()

# Telegram Application setup
telegram_app = Application.builder().token(BOT_TOKEN).build()

# Handlers
telegram_app.add_handler(CommandHandler("start", bot.start_command))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
telegram_app.add_handler(CallbackQueryHandler(bot.handle_callback))

@app.on_event("startup")
async def startup_event():
    """Botni ishga tushirish (webhook or polling emas, faqat initialized)"""
    await telegram_app.initialize()
    await telegram_app.start()

@app.on_event("shutdown")
async def shutdown_event():
    """Botni to'xtatish"""
    await telegram_app.stop()
    await telegram_app.shutdown()

@app.post("/webhook")
async def webhook_handler(request: Request):
    """Telegram webhook xabarlarini qabul qilish"""
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"status": "ok"}

@app.get("/")
async def health_check():
    """Render uchun health check va bot holati"""
    return {"status": "alive", "message": "YouTube Downloader Bot is running"}

if __name__ == "__main__":
    # Localda sinash uchun (Polling rejimida ishlatish mumkin)
    # Ammo Renderda Webhook rejimida ishlaydi
    uvicorn.run(app, host="0.0.0.0", port=PORT)

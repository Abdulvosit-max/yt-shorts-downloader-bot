import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import downloader
from config import MAX_FILE_SIZE_MB

# YouTube URL regex
YOUTUBE_REGEX = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start buyrug'i uchun handler"""
    await update.message.reply_text(
        "👋 Assalomu alaykum! Men YouTube videolarini yuklab beruvchi botman.\n\n"
        "Menga YouTube havolasini yuboring va men sizga yuklab beraman!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xabarlarni qayta ishlash"""
    text = update.message.text
    
    if not text:
        return

    # YouTube linkini tekshirish
    match = re.search(YOUTUBE_REGEX, text)
    if not match:
        await update.message.reply_text("❌ Iltimos, haqiqiy YouTube havolasini yuboring.")
        return

    url = match.group(0)
    wait_message = await update.message.reply_text("🔍 Video ma'lumotlari olinmoqda...")

    info = await downloader.get_video_info(url)
    if not info:
        await wait_message.edit_text("❌ Video ma'lumotlarini olib bo'lmadi.")
        return

    # Tugmalarni yaratish
    keyboard = [
        [
            InlineKeyboardButton("🎬 720p", callback_data=f"vid|720|{url}"),
            InlineKeyboardButton("🎬 480p", callback_data=f"vid|480|{url}"),
        ],
        [
            InlineKeyboardButton("🎬 360p", callback_data=f"vid|360|{url}"),
            InlineKeyboardButton("🎵 MP3 Audio", callback_data=f"aud|0|{url}"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    caption = f"🎬 {info['title']}\n"
    duration_min = info['duration'] // 60
    duration_sec = info['duration'] % 60
    caption += f"⏱ Davomiyligi: {duration_min}:{duration_sec:02d}\n\n"
    caption += "Sifatni tanlang:"

    await wait_message.delete()
    await update.message.reply_photo(
        photo=info['thumbnail'],
        caption=caption,
        reply_markup=reply_markup
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tugmalar bosilganda"""
    query = update.callback_query
    await query.answer()
    
    data = query.data.split('|')
    action = data[0] # vid yoki aud
    quality = data[1]
    url = data[2]

    status_message = await query.message.reply_text("⏳ Yuklanmoqda... Iltimos, kuting.")

    try:
        if action == 'vid':
            file_path = await downloader.download_video(url, quality)
        else:
            file_path = await downloader.download_audio(url)

        if not file_path or not os.path.exists(file_path):
            await status_message.edit_text("❌ Yuklashda xatolik yuz berdi.")
            return

        # Fayl hajmini tekshirish
        file_size = os.path.getsize(file_path) / (1024 * 1024)
        if file_size > MAX_FILE_SIZE_MB:
            await status_message.edit_text(f"⚠️ Fayl hajmi juda katta ({file_size:.1f} MB). Telegram limiti 50MB.")
            if os.path.exists(file_path):
                os.remove(file_path)
            return

        await status_message.edit_text("🚀 Yuborilmoqda...")
        
        if action == 'vid':
            await query.message.reply_video(video=open(file_path, 'rb'), caption="✅ Yuklab olindi!")
        else:
            await query.message.reply_audio(audio=open(file_path, 'rb'), caption="✅ Yuklab olindi!")

        await status_message.delete()
        
    except Exception as e:
        await status_message.edit_text(f"❌ Xatolik: {str(e)}")
    finally:
        # Faylni o'chirish (diskni to'ldirmaslik uchun)
        if 'file_path' in locals() and file_path and os.path.exists(file_path):
            os.remove(file_path)

import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import downloader
from config import STRINGS, MAX_FILE_SIZE_MB

# Shorts focus regex
SHORTS_REGEX = r'(https?://)?(www\.)?(youtube\.com/shorts/|youtu\.be/)([^&=%\?]{11})'

def get_str(context, key):
    """Foydalanuvchi tiliga mos xabarni olish"""
    lang = context.user_data.get('lang', 'uz')
    return STRINGS.get(lang, STRINGS['uz']).get(key, "")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tilni tanlash tugmalarini ko'rsatish"""
    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="setlang|uz"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="setlang|ru"),
            InlineKeyboardButton("🇺🇸 English", callback_data="setlang|en"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Default xabar (hali til tanlanmagan bo'lsa)
    await update.message.reply_text(
        STRINGS['uz']['welcome'],
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xabarlarni qayta ishlash (Shorts focus)"""
    text = update.message.text
    if not text:
        return

    # Til tanlanganini tekshirish
    if 'lang' not in context.user_data:
        await start_command(update, context)
        return

    # Shorts linkini tekshirish
    match = re.search(SHORTS_REGEX, text)
    if not match:
        await update.message.reply_text(get_str(context, 'invalid_url'))
        return

    url = match.group(0)
    wait_message = await update.message.reply_text(get_str(context, 'fetching'))

    # Shorts uchun sifat tanlamaymiz (faqat eng yaxshisini yuklaymiz)
    try:
        await wait_message.edit_text(get_str(context, 'downloading'))
        
        # Shorts odatda kichik bo'ladi, sifatni cheklamaymiz
        file_path = await downloader.download_video(url, quality='1080')

        if not file_path or not os.path.exists(file_path):
            await wait_message.edit_text(get_str(context, 'error'))
            return

        # Hajmini tekshirish
        file_size = os.path.getsize(file_path) / (1024 * 1024)
        if file_size > MAX_FILE_SIZE_MB:
            await wait_message.edit_text(get_str(context, 'too_large'))
            if os.path.exists(file_path):
                os.remove(file_path)
            return

        await wait_message.edit_text(get_str(context, 'sending'))
        
        await update.message.reply_video(
            video=open(file_path, 'rb'), 
            caption=get_str(context, 'done')
        )
        await wait_message.delete()
        
    except Exception as e:
        await wait_message.edit_text(f"{get_str(context, 'error')} {str(e)}")
    finally:
        if 'file_path' in locals() and file_path and os.path.exists(file_path):
            os.remove(file_path)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tugmalar bosilganda (tilni o'rnatish)"""
    query = update.callback_query
    await query.answer()
    
    data = query.data.split('|')
    if data[0] == 'setlang':
        lang = data[1]
        context.user_data['lang'] = lang
        
        # Til o'zgargani haqida xabar
        await query.message.edit_text(STRINGS[lang]['lang_selected'])

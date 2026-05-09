import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 8000))

# Telegram limits: 50MB for bots when sending files
# We will try to stick to this, or use higher quality if it fits
MAX_FILE_SIZE_MB = 50 

DOWNLOADS_DIR = "downloads"

if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

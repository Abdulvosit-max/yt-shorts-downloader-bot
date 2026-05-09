# 🎬 YouTube Downloader Telegram Bot

Ushbu bot YouTube videolarini yuklab olish uchun mo'ljallangan. 

## 🚀 Texnologiyalar
- **Python 3.10+**
- **python-telegram-bot** (Bot framework)
- **yt-dlp** (Video yuklovchi)
- **FastAPI** (Webhook server)

## 🛠 O'rnatish (Local)

1. Repozitoriyani klon qiling:
```bash
git clone <your-repo-url>
cd "You tube downloder bot"
```

2. Virtual muhit yarating va kutubxonalarni o'rnating:
```bash
python -m venv venv
source venv/bin/activate  # Windows uchun: venv\Scripts\activate
pip install -r requirements.txt
```

3. `.env` faylini yarating va quyidagilarni qo'shing:
```env
BOT_TOKEN=BotFather_dan_olingan_token
WEBHOOK_URL=https://sizning-domen.com/webhook
```

4. Botni ishga tushiring:
```bash
python main.py
```

## 🌍 Render.com ga Deploy qilish

1. GitHub-da yangi repozitoriya oching va kodni yuklang.
2. Render.com ga kiring va GitHub repongizni ulang.
3. **Web Service** sifatida yarating.
4. Environment Variables bo'limiga `BOT_TOKEN` va `WEBHOOK_URL` ni qo'shing.
5. Deploy muvaffaqiyatli yakunlangach, Telegram botingizga webhook-ni ulash uchun quyidagi havolaga brauzerda kiring:
`https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=https://your-app-name.onrender.com/webhook`

## ⚠️ Muhim
Telegram botlari uchun fayl hajmi limiti **50MB**. Agar video hajmi bundan katta bo'lsa, bot xatolik qaytaradi.

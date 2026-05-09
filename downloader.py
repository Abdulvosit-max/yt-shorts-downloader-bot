import yt_dlp
import os
import asyncio
from config import DOWNLOADS_DIR

async def get_video_info(url):
    """YouTube videosi haqida ma'lumot olish"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=False))
        return {
            'title': info.get('title', 'Video'),
            'duration': info.get('duration', 0),
            'thumbnail': info.get('thumbnail'),
            'formats': info.get('formats', [])
        }
    except Exception as e:
        print(f"Info error: {e}")
        return None

async def download_video(url, quality='1080'):
    """Video yuklab olish (Sodda variant - ffmpeg-siz ishlashga harakat qiladi)"""
    filename = f"{DOWNLOADS_DIR}/video_%(id)s.%(ext)s"
    
    # FFmpeg bo'lmasa, faqat bitta faylda video va audio bo'lgan formatni tanlaymiz
    # 'best[ext=mp4]/best' - bu asosan bitta faylli formatni oladi
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': filename,
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=True))
        file_path = yt_dlp.YoutubeDL(ydl_opts).prepare_filename(info)
        return file_path
    except Exception as e:
        print(f"Download error: {e}")
        return None

async def download_audio(url):
    """Audio yuklab olish (MP3 emas, m4a - ffmpeg kerak bo'lmasligi uchun)"""
    filename = f"{DOWNLOADS_DIR}/audio_%(id)s.%(ext)s"
    
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': filename,
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=True))
        file_path = yt_dlp.YoutubeDL(ydl_opts).prepare_filename(info)
        return file_path
    except Exception as e:
        print(f"Audio download error: {e}")
        return None

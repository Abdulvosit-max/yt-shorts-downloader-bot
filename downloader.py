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

async def download_video(url, quality='720'):
    """Video yuklab olish"""
    filename = f"{DOWNLOADS_DIR}/video_%(id)s.%(ext)s"
    
    # Sifatga qarab format tanlash
    # Telegram 50MB limiti borligi uchun 'bestvideo+bestaudio/best' o'rniga cheklov qo'shishimiz mumkin
    format_selector = f'best[height<={quality}][ext=mp4]/best[height<={quality}]/best'
    
    ydl_opts = {
        'format': format_selector,
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
    """Audio yuklab olish (MP3)"""
    filename = f"{DOWNLOADS_DIR}/audio_%(id)s.%(ext)s"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    try:
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=True))
        # Prepare filename manually because postprocessor changes extension to mp3
        base_path = yt_dlp.YoutubeDL(ydl_opts).prepare_filename(info)
        file_path = os.path.splitext(base_path)[0] + ".mp3"
        return file_path
    except Exception as e:
        print(f"Audio download error: {e}")
        return None

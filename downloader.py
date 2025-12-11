# downloader.py
import config
import os
from tqdm import tqdm
import yt_dlp

def download_videos_from_csv():
    os.makedirs(config.DOWNLOAD_DIR, exist_ok=True)

    ydl_opts = {
        'format': 'mp4',
        'outtmpl': os.path.join(config.DOWNLOAD_DIR, 'reel_%(autonumber)s.%(ext)s'),
        'quiet': False,
    }

    with open(config.CSV_FILE, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"[INFO] Downloading {len(urls)} videos...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)

# main.py

import os
import time
import schedule
import logging
import config  # ✅ Import the config module
import downloader
import editor
import uploader

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def cleanup_folder(folder):
    """Delete all files in a folder"""
    if not os.path.exists(folder):
        return
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isfile(path):
            os.remove(path)
            print(f"[🗑️] Deleted: {file}")

def job():
    logging.info("Starting TikTok Reel Bot...")

    # === STEP 1: Download Videos ===
    print("[📥] Downloading videos from YouTube...")
    try:
        downloader.download_videos_from_csv()
    except Exception as e:
        logging.error(f"Download failed: {e}")
        return

    # Get list of downloaded videos
    video_files = sorted([f for f in os.listdir(config.DOWNLOAD_DIR) if f.endswith(".mp4")])
    if not video_files:
        logging.warning("No videos downloaded.")
        return

    edited_videos = []

    # === STEP 2: Edit or Skip Based on EDIT_MODE ===
    if config.EDIT_MODE and len(video_files) >= 2:
        print("[🎬] Editing videos in split-screen mode...")

        # ✅ Update config values dynamically
        config.REMOVE_AUDIO = not config.KEEP_AUDIO

        try:
            edited_videos = editor.create_split_screen_videos()
        except Exception as e:
            logging.error(f"Editing failed: {e}")
            print("[⚠️] Editing failed. Uploading raw videos instead.")
            edited_videos = [os.path.join(config.DOWNLOAD_DIR, f) for f in video_files]

    else:
        if not config.EDIT_MODE:
            print("[⚠️] Edit mode disabled. Uploading raw videos...")
        else:
            print("[⚠️] Not enough videos to edit. Uploading raw...")
        edited_videos = [os.path.join(config.DOWNLOAD_DIR, f) for f in video_files]

    # === STEP 3: Upload ===
    print("[📤] Uploading videos to TikTok...")
    for video_path in edited_videos:
        try:
            uploader.upload_to_tiktok(video_path)
            logging.info(f"Uploaded: {os.path.basename(video_path)}")
        except Exception as e:
            logging.error(f"Upload failed {video_path}: {e}")

    # === STEP 4: Cleanup ===
    print("[🧹] Cleaning up...")
    if config.EDIT_MODE:
        cleanup_folder(config.EDITED_DIR)
    cleanup_folder(config.DOWNLOAD_DIR)

    logging.info("Daily job completed.")

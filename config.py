# config.py

import os

# Paths
CSV_FILE = 'data/links.csv'
DOWNLOAD_DIR = 'downloads/'
EDITED_DIR = 'edited/'
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"  # Or wherever it is


# TikTok Login
TIKTOK_USERNAME = 'shahmeerahmed749@gmail.com'
TIKTOK_PASSWORD = '4220170194951sam123@'

# Video Settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920

CHROMIUM_BINARY_PATH = "/usr/bin/chromium-browser"
# Runtime Flags (Updated by dashboard)
EDIT_MODE = True
KEEP_AUDIO = True
REMOVE_AUDIO = not KEEP_AUDIO  # Will be updated dynamically
COOKIE_FILE = 'data/tiktok_cookies.pkl'

"""
Configuration settings for the Media Converter App.
Contains paths, supported formats, and application settings.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# User's Downloads folder (for downloaded videos)
# This ensures videos go to the user's actual Downloads folder
USER_DOWNLOADS = Path.home() / "Downloads"
if not USER_DOWNLOADS.exists():
    USER_DOWNLOADS.mkdir(exist_ok=True)

# Directory paths
DOWNLOADS_DIR = USER_DOWNLOADS / "ConvertRocket"  # Downloads go to user's Downloads folder
UPLOADS_DIR = BASE_DIR / "uploads"
CONVERTED_DIR = BASE_DIR / "converted"

# Ensure directories exist
DOWNLOADS_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True)
CONVERTED_DIR.mkdir(exist_ok=True)

# Supported formats for conversion
SUPPORTED_FORMATS = {
    "video": ["mp4", "mkv", "webm", "avi", "mov"],
    "audio": ["mp3", "wav", "aac", "ogg", "flac"],
    "image": ["jpg", "jpeg", "png", "webp", "gif", "bmp"],  # Added jpeg separately
    "document": ["pdf", "docx", "txt"],
    "spreadsheet": ["xlsx", "xls", "csv"]
}

# FFmpeg settings
# Check for local binary first (portable mode), then system path
LOCAL_FFMPEG = BASE_DIR / "bin" / "ffmpeg.exe"
if LOCAL_FFMPEG.exists():
    FFMPEG_PATH = str(LOCAL_FFMPEG)
else:
    FFMPEG_PATH = os.getenv("FFMPEG_PATH", "ffmpeg")

# Download settings
MAX_VIDEO_DURATION = 3600  # 1 hour max
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

# Supported platforms for download
SUPPORTED_PLATFORMS = ["youtube", "tiktok", "instagram", "twitter", "facebook"]

# MIME type mappings
MIME_TYPES = {
    # Video
    "mp4": "video/mp4",
    "mkv": "video/x-matroska",
    "webm": "video/webm",
    "avi": "video/x-msvideo",
    "mov": "video/quicktime",
    # Audio
    "mp3": "audio/mpeg",
    "wav": "audio/wav",
    "aac": "audio/aac",
    "ogg": "audio/ogg",
    "flac": "audio/flac",
    # Image
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "webp": "image/webp",
    "gif": "image/gif",
    "bmp": "image/bmp",
    # Document
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "txt": "text/plain",
    # Spreadsheet
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "xls": "application/vnd.ms-excel",
    "csv": "text/csv"
}

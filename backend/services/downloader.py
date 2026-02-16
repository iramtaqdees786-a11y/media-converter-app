"""
Service for downloading videos from social media platforms using yt-dlp.
Supports YouTube, TikTok, Instagram, Twitter, and Facebook.
"""

import asyncio
import os
import re
from pathlib import Path
from typing import Dict, Optional, Any
from dataclasses import dataclass
import yt_dlp

from backend.config import DOWNLOADS_DIR, SUPPORTED_PLATFORMS
from backend.utils.helpers import generate_unique_filename


@dataclass
class DownloadResult:
    """Result of a download operation."""
    success: bool
    message: str
    filename: Optional[str] = None
    filepath: Optional[str] = None
    title: Optional[str] = None
    duration: Optional[int] = None
    filesize: Optional[int] = None
    thumbnail: Optional[str] = None


class DownloadProgress:
    """Track download progress."""
    
    def __init__(self):
        self.progress: float = 0
        self.status: str = "pending"
        self.speed: str = ""
        self.eta: str = ""
    
    def update(self, d: Dict[str, Any]):
        """Update progress from yt-dlp callback."""
        if d['status'] == 'downloading':
            self.status = 'downloading'
            # Extract percentage
            if 'downloaded_bytes' in d and 'total_bytes' in d:
                self.progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
            elif '_percent_str' in d:
                try:
                    self.progress = float(d['_percent_str'].strip('%'))
                except:
                    pass
            
            self.speed = d.get('_speed_str', '')
            self.eta = d.get('_eta_str', '')
        
        elif d['status'] == 'finished':
            self.status = 'finished'
            self.progress = 100


def _get_cookiefile() -> Optional[str]:
    """Return path to cookie file if configured via environment and exists."""
    cookie_path = os.getenv("YTDLP_COOKIES_FILE") or os.getenv("COOKIES_FILE")

    # 1) Env var takes priority if set
    if cookie_path:
        path = Path(cookie_path).expanduser()
        if path.is_file():
            return str(path)

    # 2) Fallback: look for cookies.txt in the project root directory
    # downloader.py is in backend/services, so project root is two levels up
    project_root = Path(__file__).resolve().parents[2]
    default_cookie = project_root / "cookies.txt"
    if default_cookie.is_file():
        return str(default_cookie)

    return None


def _build_http_headers(url: str) -> Dict[str, str]:
    """Build browser-like HTTP headers to reduce 403/anti-bot issues."""
    # Use the latest Chrome user agent for better compatibility
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )

    return {
        "User-Agent": user_agent,
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9," 
            "image/avif,image/webp,image/apng,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": url,
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Upgrade-Insecure-Requests": "1",
    }


def _base_ydl_options(url: str) -> Dict[str, Any]:
    """Common yt-dlp options for both info extraction and download."""
    opts: Dict[str, Any] = {
        "quiet": True,
        "no_warnings": True,
        "nocheckcertificate": True,
        "http_headers": _build_http_headers(url),
        "retries": 15,
        "fragment_retries": 15,
        "legacy_server_connect": True,
        "no_playlist": True,
        "playlist_items": "1",
        "geo_bypass": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["tv", "android_vr", "ios", "mweb"],
                "player_skip": [],
            }
        },
        "nocheckcertificate": True,
        "prefer_insecure": True,
        "youtube_include_dash_manifest": True,
        "youtube_include_hls_manifest": True,
        "youtube_skip_dash_manifest": False,
        "youtube_skip_hls_manifest": False,
        "socket_timeout": 30,
    }

    cookiefile = _get_cookiefile()
    if cookiefile:
        opts["cookiefile"] = cookiefile

    return opts


def detect_platform(url: str) -> Optional[str]:
    """
    Detect the platform from a URL.
    
    Args:
        url: The URL to analyze
    
    Returns:
        Platform name or None if not supported
    """
    patterns = {
        'youtube': r'(youtube\.com|youtu\.be|youtube\.com/shorts)',
        'tiktok': r'(tiktok\.com|vm\.tiktok\.com)',
        'instagram': r'(instagram\.com|instagr\.am)',
        'twitter': r'(twitter\.com|x\.com)',
        'facebook': r'(facebook\.com|fb\.watch)'
    }
    
    for platform, pattern in patterns.items():
        if re.search(pattern, url, re.IGNORECASE):
            return platform
    
    return None


def validate_url(url: str) -> tuple[bool, str]:
    """
    Validate if a URL is supported for download.
    
    Args:
        url: The URL to validate
    
    Returns:
        Tuple of (is_valid, error_message_or_platform)
    """
    if not url or not url.strip():
        return False, "URL cannot be empty"
    
    # Basic URL validation
    url_pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    
    if not url_pattern.match(url):
        return False, "Invalid URL format"
    
    platform = detect_platform(url)
    if not platform:
        return False, f"Unsupported platform. Supported: {', '.join(SUPPORTED_PLATFORMS)}"
    
    return True, platform


async def get_video_info(url: str) -> Dict[str, Any]:
    """
    Get video information without downloading.
    
    Args:
        url: Video URL
    
    Returns:
        Dictionary with video information
    """
    ydl_opts = _base_ydl_options(url)
    ydl_opts.update({
        'extract_flat': False,
    })
    
    loop = asyncio.get_event_loop()
    
    def extract_info():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)
    
    try:
        info = await loop.run_in_executor(None, extract_info)
        return {
            'title': info.get('title', 'Unknown'),
            'duration': info.get('duration', 0),
            'thumbnail': info.get('thumbnail', ''),
            'uploader': info.get('uploader', 'Unknown'),
            'view_count': info.get('view_count', 0),
            'description': info.get('description', '')[:200] if info.get('description') else '',
            'formats': len(info.get('formats', [])),
        }
    except Exception as e:
        return {'error': str(e)}


async def download_video(
    url: str,
    format_type: str = "video",
    quality: str = "best",
    progress_callback: Optional[callable] = None
) -> DownloadResult:
    """
    Download a video from a supported platform.
    
    Args:
        url: Video URL to download
        format_type: Type of download - 'video' or 'audio'
        quality: Quality setting - 'best', 'worst', or specific format
        progress_callback: Optional callback for progress updates
    
    Returns:
        DownloadResult with download status and file info
    """
    # Validate URL
    is_valid, result = validate_url(url)
    if not is_valid:
        return DownloadResult(success=False, message=result)
    
    platform = result
    progress = DownloadProgress()
    
    # Configure yt-dlp options
    output_template = str(DOWNLOADS_DIR / '%(title)s_%(id)s.%(ext)s')
    
    ydl_opts = _base_ydl_options(url)
    ydl_opts.update({
        'outtmpl': output_template,
        'progress_hooks': [progress.update],
        'restrictfilenames': True,  # Avoid special characters in filename
    })
    
    # Set format based on type
    if format_type == "audio":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        # Improved format selection for better YouTube compatibility
        if quality == "best":
            # Try progressive formats first (single file with video+audio)
            # Then fall back to adaptive formats (separate video+audio that need merging)
            ydl_opts['format'] = (
                'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            )
        elif quality == "1080p":
            ydl_opts['format'] = (
                'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/'
                'best[ext=mp4][height<=1080]/best[height<=1080]'
            )
        elif quality == "720p":
            ydl_opts['format'] = (
                'bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/'
                'best[ext=mp4][height<=720]/best[height<=720]'
            )
        elif quality == "480p":
            ydl_opts['format'] = (
                'bestvideo[ext=mp4][height<=480]+bestaudio[ext=m4a]/'
                'best[ext=mp4][height<=480]/best[height<=480]'
            )
        elif quality == "worst":
            ydl_opts['format'] = 'worstvideo+worstaudio/worst'
        else:
            ydl_opts['format'] = quality
        
        # Ensure output is MP4
        ydl_opts['merge_output_format'] = 'mp4'
    
    loop = asyncio.get_event_loop()
    
    def do_download():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=True)
    
    try:
        info = await loop.run_in_executor(None, do_download)
        
        if info is None:
            return DownloadResult(
                success=False,
                message="Metadata extraction failed. This video might be restricted or blocked."
            )
            
        # Build the expected filename or find the actual one
        video_id = info.get('id', 'unknown')
        
        # Look for the file in the downloads directory
        filepath = None
        for file in DOWNLOADS_DIR.iterdir():
            if video_id in file.name:
                filepath = file
                break
        
        if not filepath:
            # Fallback to the requested filename from info
            ext = info.get('ext', 'mp4')
            requested_file = DOWNLOADS_DIR / f"{info.get('title', 'video')}_{video_id}.{ext}"
            if requested_file.exists():
                filepath = requested_file
        
        if not filepath:
            return DownloadResult(
                success=False,
                message="Download completed but file could not be located on server."
            )
        
        return DownloadResult(
            success=True,
            message=f"Successfully downloaded from {platform}",
            filename=filepath.name,
            filepath=str(filepath.absolute()),
            title=info.get('title'),
            duration=info.get('duration'),
            filesize=filepath.stat().st_size if filepath.exists() else None,
            thumbnail=info.get('thumbnail')
        )
        
    except yt_dlp.DownloadError as e:
        error_msg = str(e)
        if "'NoneType' object has no attribute 'get'" in error_msg:
             return DownloadResult(success=False, message="Metadata corruption detected. YouTube is blocking this specific stream format. Try a different video.")
        
        # Provide user-friendly error messages
        if "Private video" in error_msg:
            return DownloadResult(success=False, message="This video is private.")
        elif "Video unavailable" in error_msg:
            return DownloadResult(success=False, message="This video is unavailable.")
        elif "Sign in" in error_msg.lower():
            return DownloadResult(success=False, message="This video requires login.")
        elif "copyright" in error_msg.lower():
            return DownloadResult(success=False, message="Copyright restriction detected.")
        elif "age" in error_msg.lower():
            return DownloadResult(success=False, message="This video is age-restricted.")
        elif "geo" in error_msg.lower() or "country" in error_msg.lower():
            return DownloadResult(success=False, message="Not available in your country.")
        elif "429" in error_msg or "rate" in error_msg.lower():
            return DownloadResult(success=False, message="Too many requests. Please wait a moment.")
        elif "403" in error_msg or "Forbidden" in error_msg:
            return DownloadResult(success=False, message="Access denied by YouTube. Try again in 5 minutes.")
        else:
            return DownloadResult(success=False, message=f"Platform Error: {error_msg[:100]}")
            
    except Exception as e:
        if "'NoneType' object has no attribute 'get'" in str(e):
            return DownloadResult(success=False, message="Engine error: YouTube blocked the extraction protocol. We are working on a fix.")
        print(f"Unexpected download error: {str(e)}")
        return DownloadResult(success=False, message=f"Connection Error: {str(e)[:100]}")


async def download_audio_only(url: str) -> DownloadResult:
    """
    Download only the audio track from a video.
    
    Args:
        url: Video URL
    
    Returns:
        DownloadResult with download status
    """
    return await download_video(url, format_type="audio")

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
    """Build browser-like HTTP headers matching the impersonated client."""
    # Matching Chrome 110 / Windows 10 for consistency with --impersonate
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Ch-Ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.google.com/",
    }


def _base_ydl_options(url: str) -> Dict[str, Any]:
    """Common yt-dlp options for both info extraction and download."""
    opts: Dict[str, Any] = {
        "quiet": True,
        "no_warnings": False,
        "nocheckcertificate": True,
        "http_headers": _build_http_headers(url),
        "retries": 15,
        "fragment_retries": 15,
        "no_playlist": True,
        "geo_bypass": True,
        "noproxy": True,
        # JavaScript runtime for YouTube challenge solving (required for yt-dlp 2026+)
        "js_runtimes": {"node": {}, "deno": {}},
        # Remote EJS components for YouTube n-parameter challenge solving
        "remote_components": ["ejs:github"],
        "extractor_args": {
            "youtube": {
                # Use multiple clients for maximum compatibility (Shorts + regular videos)
                "player_client": ["mweb", "tv", "ios", "android"],
            }
        },
        "youtube_include_dash_manifest": False,  # Often triggers 403s on specific streams
        "youtube_include_hls_manifest": True,
        "check_formats": "selected",
        "socket_timeout": 60,
        "concurrent_fragment_downloads": 5,
        "file_access_retries": 10,
    }

    cookiefile = _get_cookiefile()
    if cookiefile:
        print(f"DEBUG: Using cookie file at {cookiefile}")
        opts["cookiefile"] = cookiefile
    else:
        print("DEBUG: No cookies.txt found. YouTube downloads may fail if IP is flagged.")

    return opts


def normalize_url(url: str) -> str:
    """
    Format social media URLs for maximum compatibility with yt-dlp.
    CRITICAL: YouTube Shorts are ALWAYS converted to standard watch?v= format
    because the deployed server handles watch URLs reliably but /shorts/ URLs
    trigger YouTube access restrictions.
    """
    url = url.strip()
    
    # Ensure URL has protocol to easily pass regex validation
    if not url.lower().startswith("http"):
        url = "https://" + url
    
    # YouTube Shorts -> Standard Watch URL (MANDATORY for server compatibility)
    # Handles: youtube.com/shorts/ID, m.youtube.com/shorts/ID, www.youtube.com/shorts/ID
    # Also handles query params like ?feature=share, ?si=xxx
    shorts_match = re.search(r'(?:www\.|m\.)?youtube\.com/shorts/([a-zA-Z0-9_-]+)', url)
    if shorts_match:
        video_id = shorts_match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"
    
    # youtu.be/VIDEO_ID -> youtube.com/watch?v=VIDEO_ID
    be_match = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', url)
    if be_match:
        video_id = be_match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"
    
    # X.com -> Twitter.com (Some backend extractors still prefer the legacy domain)
    if "x.com" in url.lower():
        url = re.sub(r'x\.com', 'twitter.com', url, flags=re.IGNORECASE)
        
    # Instagram Reels -> Direct Post URL (Often bypassed cleaner)
    if "instagram.com/reels/" in url.lower():
        url = re.sub(r'/reels/', '/p/', url, flags=re.IGNORECASE)
        
    # TikTok mobile links - Ensure HTTPS
    if "tiktok.com" in url.lower() and not url.lower().startswith("http"):
        url = "https://" + url
        
    return url


def detect_platform(url: str) -> Optional[str]:
    """Detect the platform from a URL."""
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
        
    # Normalize before validation to ensure protocol exists
    url = normalize_url(url)
    
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
    url = normalize_url(url)
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


async def get_video_stream(
    url: str,
    format_type: str = "video",
    quality: str = "best"
) -> Dict[str, Any]:
    """
    Download a video to a temporary directory and prepare it for streaming.
    
    Returns:
        Dict containing success status, stream generator, and filename.
    """
    import tempfile
    import uuid
    import shutil
    
    url = normalize_url(url)
    is_valid, result = validate_url(url)
    if not is_valid:
        return {"success": False, "message": result}
    
    uid = uuid.uuid4().hex[:8]
    temp_dir = tempfile.gettempdir()
    output_template = os.path.join(temp_dir, f"{uid}_%(title)s.%(ext)s")
    
    ydl_opts = _base_ydl_options(url)
    ydl_opts.update({
        'outtmpl': output_template,
        'restrictfilenames': True,
    })
    
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
        if quality == "best":
            ydl_opts['format'] = 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[height<=1080]/best'
        elif quality == "1080p":
            ydl_opts['format'] = 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[height<=1080]/best'
        elif quality == "720p":
            ydl_opts['format'] = 'bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[height<=720]/best'
        elif quality == "480p":
            ydl_opts['format'] = 'bestvideo[ext=mp4][height<=480]+bestaudio[ext=m4a]/best[height<=480]/best'
        elif quality == "worst":
            ydl_opts['format'] = 'worstvideo+worstaudio/worst'
        else:
            ydl_opts['format'] = f'{quality}/best'
        ydl_opts['merge_output_format'] = 'mp4'

    loop = asyncio.get_event_loop()
    
    def do_download(client_cycle_index=0):
        clients = [
            ["ios", "android"],
            ["mweb", "tv"],
            ["tv", "web_creator"],
            ["android", "mweb"],
            ["default"],
        ]
        current_ydl_opts = ydl_opts.copy()
        current_ydl_opts["extractor_args"] = {
            "youtube": {"player_client": clients[client_cycle_index % len(clients)]}
        }
        with yt_dlp.YoutubeDL(current_ydl_opts) as ydl:
            return ydl.extract_info(url, download=True)

    max_retries = 4
    last_error = ""
    info = None
    
    try:
        for attempt in range(max_retries + 1):
            try:
                print(f"DEBUG: Streaming Attempt {attempt + 1} for URL: {url}")
                info = await loop.run_in_executor(None, do_download, attempt)
                if info is not None:
                    break
            except Exception as e:
                last_error = str(e)
                print(f"YTDLP ATTEMPT {attempt + 1} FAILED: {last_error}")
                if any(x in last_error.lower() for x in ["copyright", "private video"]):
                    break
                if attempt < max_retries:
                    await asyncio.sleep(1 + attempt)
                    continue

        if not info:
             error_msg = last_error
             if "sign in" in error_msg.lower() or "cookies" in error_msg.lower() or "403" in error_msg:
                 return {"success": False, "message": "YouTube is restricting this download. Try again later."}
             if "unavailable" in error_msg.lower():
                 return {"success": False, "message": "Video is unavailable or private."}
             return {"success": False, "message": error_msg.split(':')[0].strip()}

        # Find the downloaded file in temp_dir
        actual_file_path = None
        for f in os.listdir(temp_dir):
            if f.startswith(f"{uid}_"):
                actual_file_path = os.path.join(temp_dir, f)
                break

        if not actual_file_path or not os.path.exists(actual_file_path):
            return {"success": False, "message": "Download succeeded but file not found on disk."}

        filename = os.path.basename(actual_file_path)
        # Remove the uid prefix for the user-facing filename
        user_filename = filename.replace(f"{uid}_", "", 1)

        def iterfile():
            try:
                with open(actual_file_path, "rb") as f:
                    # Yield in 1MB chunks
                    while chunk := f.read(1024 * 1024):
                        yield chunk
            finally:
                # Cleanup the temp file when the generator is exhausted or closed
                try:
                    os.unlink(actual_file_path)
                    print(f"DEBUG: Cleaned up temp file {actual_file_path}")
                except Exception as e:
                    print(f"WARNING: Failed to cleanup temp file {actual_file_path}: {e}")

        return {
            "success": True,
            "stream_generator": iterfile,
            "filename": user_filename,
            "title": info.get('title')
        }

    except asyncio.TimeoutError:
        return {"success": False, "message": "The request timed out. Please try again."}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"success": False, "message": "A connection error occurred. YouTube might be blocking the request."}

import sys
import os
import re
from typing import Optional, Dict, Any

# Mocking the environment to test the function without full backend
def normalize_url(url: str) -> str:
    url = url.strip()
    shorts_match = re.search(r'youtube\.com/shorts/([a-zA-Z0-9_-]+)', url)
    if shorts_match:
        video_id = shorts_match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"
    be_match = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', url)
    if be_match:
        video_id = be_match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"
    if "x.com" in url.lower():
        url = re.sub(r'x\.com', 'twitter.com', url, flags=re.IGNORECASE)
    if "instagram.com/reels/" in url.lower():
        url = re.sub(r'/reels/', '/p/', url, flags=re.IGNORECASE)
    if "tiktok.com" in url.lower() and not url.lower().startswith("http"):
        url = "https://" + url
    return url

test_urls = [
    "https://www.youtube.com/shorts/dQw4w9WgXcQ",
    "https://youtu.be/dQw4w9WgXcQ",
    "https://x.com/elonmusk/status/123456789",
    "https://www.instagram.com/reels/C_something/",
    "tiktok.com/@user/video/123456"
]

print("--- URL Normalization Test ---")
for original in test_urls:
    normalized = normalize_url(original)
    print(f"Original:   {original}")
    print(f"Normalized: {normalized}")
    print("-" * 30)

# Now try a real extraction with the normalized URL
import yt_dlp
print("\n--- Real Extraction Test (YouTube Shorts -> Watch) ---")
target = "https://www.youtube.com/shorts/dQw4w9WgXcQ"
normalized_target = normalize_url(target)
ydl_opts = {
    "quiet": True,
    "no_warnings": True,
    "js_runtimes": {"node": {}},
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(normalized_target, download=False)
        print(f"Extraction Successful for: {normalized_target}")
        print(f"Title: {info.get('title')}")
except Exception as e:
    print(f"Extraction Failed: {str(e)}")

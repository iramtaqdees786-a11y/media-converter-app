import yt_dlp
import sys

url = "https://www.youtube.com/watch?v=klrS7yf3Z2E"
ydl_opts = {
    "impersonate": "chrome",
    "quiet": False,
    "no_warnings": False,
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print("Success!")
except Exception as e:
    print(f"ERROR TYPE: {type(e)}")
    print(f"ERROR STR: '{str(e)}'")
    import traceback
    traceback.print_exc()

import yt_dlp
import sys

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
ydl_opts = {
    "quiet": False,
    "no_warnings": False,
    "js_runtimes": {"node": {}},
    "remote_components": {"ejs": "github"},
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print("Success!")
        print(f"Title: {info.get('title')}")
except Exception as e:
    print(f"ERROR TYPE: {type(e)}")
    print(f"ERROR STR: '{str(e)}'")
    import traceback
    traceback.print_exc()

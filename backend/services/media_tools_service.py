import os
from pathlib import Path
from typing import Optional, List
import subprocess
from PIL import Image
import yt_dlp
import uuid

class MediaToolsService:
    def __init__(self, upload_dir: Path, converted_dir: Path, downloads_dir: Path):
        self.upload_dir = upload_dir
        self.converted_dir = converted_dir
        self.downloads_dir = downloads_dir

    async def download_thumbnail(self, url: str) -> dict:
        """Download high-res thumbnail for a video."""
        ydl_opts = {
            'skip_download': True,
            'writethumbnail': True,
            'outtmpl': str(self.downloads_dir / '%(id)s.%(ext)s'),
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # yt-dlp saves thumbnail as filename.jpg or webp
            # We need to find where it saved it.
            video_id = info['id']
            # Possible extensions
            for ext in ['jpg', 'webp', 'png']:
                thumb_path = self.downloads_dir / f"{video_id}.{ext}"
                if thumb_path.exists():
                     return {
                         "path": thumb_path,
                         "filename": thumb_path.name,
                         "title": info.get('title', 'thumbnail')
                     }
            
            # Fallback if not found locally, return url
            return {"url": info.get('thumbnail'), "title": info.get('title')}

    async def trim_video(self, file_path: Path, start_time: str, end_time: str, output_filename: str) -> Path:
        """
        Trim video using ffmpeg. 
        start_time and end_time format: HH:MM:SS or seconds.
        If end_time is not provided, it trims until end (not implemented here, but ffmpeg supports duration).
        The user asked to "cut first or last few seconds". 
        """
        output_path = self.converted_dir / output_filename
        
        # Build command
        # ffmpeg -i input -ss start -to end -c copy output (fast)
        # or -ss start -t duration.
        
        cmd = ["ffmpeg", "-i", str(file_path)]
        if start_time:
            cmd.extend(["-ss", start_time])
        if end_time:
            cmd.extend(["-to", end_time])
            
        cmd.extend(["-c", "copy", str(output_path)]) # Use stream copy for speed
        
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return output_path
        except subprocess.CalledProcessError as e:
            # If stream copy fails (keyframe issues), try re-encoding (slower but safer)
            cmd_reencode = ["ffmpeg", "-i", str(file_path)]
            if start_time:
                cmd_reencode.extend(["-ss", start_time])
            if end_time:
                cmd_reencode.extend(["-to", end_time])
            cmd_reencode.extend([str(output_path)])
            
            subprocess.run(cmd_reencode, check=True)
            return output_path

    async def strip_exif(self, file_path: Path, output_filename: str) -> Path:
        """Remove EXIF data from image."""
        output_path = self.converted_dir / output_filename
        
        with Image.open(file_path) as img:
            # We need to save it. If we just save, PIL strip exif by default unless 'exif' param passed?
            # actually usually it keeps it unless we just create a new image.
            data = list(img.getdata())
            image_without_exif = Image.new(img.mode, img.size)
            image_without_exif.putdata(data)
            image_without_exif.save(output_path)
            
        return output_path


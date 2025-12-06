import os
import sys
import requests
import subprocess
import time
from pathlib import Path

BASE_URL = "http://localhost:8000"
TEST_DIR = Path("test_media_files")
TEST_DIR.mkdir(exist_ok=True)

def log(msg, correct=True):
    icon = "✅" if correct else "❌"
    print(f"{icon} {msg}")

def check_ffmpeg():
    print("\n🔍 Checking FFmpeg Configuration...")
    
    # Check 1: Local bin folder
    local_bin = Path("bin/ffmpeg.exe")
    if local_bin.exists():
        log(f"Found local FFmpeg: {local_bin}")
        return str(local_bin)
    
    # Check 2: System PATH
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        log("Found FFmpeg in system PATH")
        return "ffmpeg"
    except (subprocess.CalledProcessError, FileNotFoundError):
        log("FFmpeg NOT found in system PATH or bin/", False)
        return None

def create_test_video(ffmpeg_path):
    print("\n🎥 Generating Test Video...")
    if not ffmpeg_path:
        log("Cannot generate test video without FFmpeg", False)
        return None
        
    output_file = TEST_DIR / "test_video.mp4"
    
    # Generate 5 second video with audio using lavfi
    # testsrc=duration=5:size=1280x720:rate=30 [v]; sine=frequency=1000:duration=5 [a]
    cmd = [
        ffmpeg_path,
        "-y",
        "-f", "lavfi", "-i", "testsrc=duration=5:size=640x480:rate=30",
        "-f", "lavfi", "-i", "sine=frequency=1000:duration=5",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        str(output_file)
    ]
    
    try:
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        if output_file.exists():
            log(f"Test video generated: {output_file} ({output_file.stat().st_size} bytes)")
            return output_file
    except Exception as e:
        log(f"Failed to generate video: {e}", False)
        return None

def test_conversion(file_path, target_format):
    print(f"\n🔄 Testing Conversion: {file_path.suffix} -> {target_format}...")
    
    if not file_path or not file_path.exists():
        log("Input file missing", False)
        return
        
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.name, f, 'video/mp4')}
            data = {'target_format': target_format}
            start_time = time.time()
            r = requests.post(f"{BASE_URL}/api/convert/upload", files=files, data=data)
            duration = time.time() - start_time
            
        if r.status_code == 200:
            result = r.json()
            if result.get('success'):
                log(f"Success! Time: {duration:.2f}s")
                log(f"Result: {result.get('converted_file')}")
            else:
                log(f"Server returned failure: {result.get('message')}", False)
        else:
            log(f"HTTP Error {r.status_code}: {r.text}", False)
            
    except requests.exceptions.ConnectionError:
        log("Could not connect to server. Is main.py running?", False)
    except Exception as e:
        log(f"Test failed: {e}", False)

def main():
    print("🚀 ConvertRocket Media Features Test")
    print("=" * 40)
    
    # 1. Check FFmpeg
    ffmpeg_exe = check_ffmpeg()
    
    if not ffmpeg_exe:
        print("\n⚠️ FATAL: FFmpeg is required for audio/video tests.")
        print("Please download ffmpeg.exe and place it in the 'bin' folder.")
        return

    # 2. Create Test Content
    video_path = create_test_video(ffmpeg_exe)
    
    # 3. Test Video Conversion (MP4 -> MOV)
    if video_path:
        test_conversion(video_path, "mov")
    
    # 4. Test Audio Extraction (MP4 -> MP3)
    if video_path:
        test_conversion(video_path, "mp3")

if __name__ == "__main__":
    main()

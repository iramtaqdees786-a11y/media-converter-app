import os
import requests
import time
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
TEST_FILE = Path("test_media_files/test_video.mp4")

def run_test():
    print("🎬 STARTING MP4 CONVERSION TEST")
    print("-" * 40)

    # 1. Check if we have the test video
    if not TEST_FILE.exists():
        print("❌ Test video not found. Generating simple valid MP4 header...")
        TEST_FILE.parent.mkdir(exist_ok=True)
        # Create a tiny dummy file if the real one does't exist (just to test the endpoint)
        # Note: This might fail ffmpeg processing if it's invalid data, 
        # but the previous test logged that it DID generate a valid one.
        print("⚠️ Previous generation might have failed. Requires manual check.")
        return

    print(f"✅ Found Input File: {TEST_FILE}")
    print(f"   Size: {TEST_FILE.stat().st_size} bytes")

    # 2. Send to Server (Convert MP4 -> MP3)
    target_format = "mp3"
    print(f"\n🚀 Sending to API (Convert to {target_format})...")
    
    try:
        with open(TEST_FILE, 'rb') as f:
            files = {'file': (TEST_FILE.name, f, 'video/mp4')}
            data = {'target_format': target_format}
            
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/api/convert/upload", 
                files=files, 
                data=data,
                timeout=60 # Wait up to 60s
            )
            elapsed = time.time() - start_time

        # 3. Analyze Result
        print(f"⏱️  Time taken: {elapsed:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("\n✅ SUCCESS! Conversion Completed.")
                print(f"   Original: {result.get('original_file')}")
                print(f"   Converted: {result.get('converted_file')}")
                print(f"   Saved at: {result.get('converted_file')}")
            else:
                print(f"\n❌ CONVERSION FAILED (API Error):")
                print(f"   Message: {result.get('message')}")
        else:
            print(f"\n❌ SERVER ERROR: {response.status_code}")
            print(f"   {response.text}")

    except Exception as e:
        print(f"\n❌ CONNECTION ERROR: {e}")
        print("   Is the server running on localhost:8000?")

if __name__ == "__main__":
    run_test()

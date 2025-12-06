"""
Example test script for the Media Converter App.
Demonstrates how to use the API endpoints for downloading and converting files.
"""

import requests
import time
import os

# API Base URL
BASE_URL = "http://localhost:8000"


def test_health():
    """Test the health endpoint."""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    return response.ok


def test_get_formats():
    """Test getting supported formats."""
    print("\n📋 Getting supported formats...")
    response = requests.get(f"{BASE_URL}/api/convert/formats")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Video formats: {data['formats']['video']}")
    print(f"   Audio formats: {data['formats']['audio']}")
    print(f"   Image formats: {data['formats']['image']}")
    return response.ok


def test_get_platforms():
    """Test getting supported platforms."""
    print("\n🌐 Getting supported platforms...")
    response = requests.get(f"{BASE_URL}/api/download/platforms")
    print(f"   Status: {response.status_code}")
    data = response.json()
    for platform in data['platforms']:
        print(f"   {platform['icon']} {platform['name']} ({platform['domain']})")
    return response.ok


def test_video_info(url: str):
    """Test getting video information."""
    print(f"\nℹ️  Getting video info for: {url[:50]}...")
    response = requests.post(
        f"{BASE_URL}/api/download/info",
        json={"url": url}
    )
    print(f"   Status: {response.status_code}")
    if response.ok:
        data = response.json()
        if data.get('success'):
            info = data['info']
            print(f"   Title: {info.get('title', 'N/A')[:50]}...")
            print(f"   Duration: {info.get('duration', 0)} seconds")
            print(f"   Platform: {data.get('platform', 'Unknown')}")
        else:
            print(f"   Error: {data.get('detail', 'Unknown error')}")
    return response.ok


def test_download_video(url: str, format_type: str = "video"):
    """Test downloading a video."""
    print(f"\n⬇️  Downloading {format_type} from: {url[:50]}...")
    response = requests.post(
        f"{BASE_URL}/api/download/start",
        json={
            "url": url,
            "format_type": format_type,
            "quality": "best"
        }
    )
    print(f"   Status: {response.status_code}")
    data = response.json()
    if response.ok and data.get('success'):
        print(f"   ✅ Downloaded: {data.get('filename')}")
        print(f"   📁 Download URL: {data.get('download_url')}")
        print(f"   📊 Size: {data.get('filesize', 0) / 1024 / 1024:.2f} MB")
        return data.get('filename')
    else:
        print(f"   ❌ Error: {data.get('detail', data.get('message', 'Unknown error'))}")
        return None


def test_image_conversion(image_path: str, target_format: str):
    """Test converting an image."""
    if not os.path.exists(image_path):
        print(f"\n⚠️  Image file not found: {image_path}")
        return None
    
    print(f"\n🔄 Converting image to {target_format}...")
    with open(image_path, 'rb') as f:
        response = requests.post(
            f"{BASE_URL}/api/convert/upload",
            files={"file": f},
            data={"target_format": target_format}
        )
    
    print(f"   Status: {response.status_code}")
    data = response.json()
    if response.ok and data.get('success'):
        print(f"   ✅ Converted: {data.get('converted_file')}")
        print(f"   📁 Download URL: {data.get('download_url')}")
        print(f"   📊 Original: {data.get('original_size')} → {data.get('converted_size')}")
        return data.get('converted_file')
    else:
        print(f"   ❌ Error: {data.get('detail', data.get('message', 'Unknown error'))}")
        return None


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("🧪 Media Converter App - Test Suite")
    print("=" * 60)
    
    # Basic tests
    test_health()
    test_get_formats()
    test_get_platforms()
    
    # Video info test (using a public domain video)
    test_url = "https://www.youtube.com/watch?v=BaW_jenozKc"  # Public domain example
    test_video_info(test_url)
    
    print("\n" + "=" * 60)
    print("✅ Basic API tests completed!")
    print("=" * 60)
    
    print("\n📝 To test downloads and conversions:")
    print("   1. Make sure the server is running (python main.py)")
    print("   2. Open http://localhost:8000 in your browser")
    print("   3. Try downloading a video or uploading a file to convert")
    
    print("\n💡 Example commands:")
    print('   curl -X POST http://localhost:8000/api/download/info \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}\'')


if __name__ == "__main__":
    run_all_tests()

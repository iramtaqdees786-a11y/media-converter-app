"""
Test script to verify the mp4-converter redirect is working
"""
import requests

def test_redirect():
    """Test that /mp4-converter.html redirects to /mp3-converter.html"""
    base_url = "http://localhost:8000"
    
    # Test the redirect
    response = requests.get(f"{base_url}/mp4-converter.html", allow_redirects=False)
    
    print("Testing /mp4-converter.html redirect...")
    print(f"Status Code: {response.status_code}")
    print(f"Location Header: {response.headers.get('location', 'Not set')}")
    
    if response.status_code == 301:
        print("✅ Redirect working correctly (301 Permanent Redirect)")
    elif response.status_code == 302:
        print("⚠️ Redirect working but using 302 (should be 301)")
    else:
        print(f"❌ Redirect not working (expected 301, got {response.status_code})")
    
    # Follow the redirect
    response_followed = requests.get(f"{base_url}/mp4-converter.html", allow_redirects=True)
    if response_followed.status_code == 200:
        print("✅ Final destination loads successfully")
    else:
        print(f"❌ Final destination failed ({response_followed.status_code})")

if __name__ == "__main__":
    try:
        test_redirect()
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Start the server with: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")

import urllib.request
import json
import time

url = "http://localhost:8000/api/download/start"
data = {
    "url": "https://www.youtube.com/watch?v=jNQXAC9IVRw",
    "format_type": "video",
    "quality": "best"
}

req = urllib.request.Request(
    url, 
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

print("Starting locally hosted download test...")
start_time = time.time()
try:
    with urllib.request.urlopen(req, timeout=120) as response:
        result = json.loads(response.read().decode())
        print("Response:", json.dumps(result, indent=2))
        if result.get('success'):
            print(f"✅ Download succeeded in {time.time() - start_time:.2f} seconds!")
            print(f"File: {result.get('filename')}")
        else:
            print("❌ Download failed as reported by API.")
except Exception as e:
    print("❌ Error calling local API:", repr(e))

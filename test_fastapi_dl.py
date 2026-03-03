from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_download():
    response = client.post(
        "/api/download/start",
        json={"url": "https://www.youtube.com/watch?v=jNQXAC9IVRw", "format_type": "video", "quality": "best"},
        timeout=120
    )
    print("Status code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except Exception as e:
        print("Error parsing JSON:", e)
        print("Response text:", response.text)

if __name__ == "__main__":
    test_download()

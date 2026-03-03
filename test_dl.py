import asyncio
from backend.services.downloader import download_video

async def main():
    result = await download_video("https://www.youtube.com/watch?v=jNQXAC9IVRw")
    print("Result:", result)

if __name__ == "__main__":
    asyncio.run(main())

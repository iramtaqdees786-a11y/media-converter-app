"""
API router for download endpoints.
Handles video downloads from social media platforms.
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, validator
from typing import Optional
from pathlib import Path

from backend.services.downloader import (
    get_video_stream,
    get_video_info,
    validate_url,
    detect_platform
)

from backend.config import DOWNLOADS_DIR
from backend.utils.helpers import get_mime_type

router = APIRouter(prefix="/api/download", tags=["download"])

class VideoInfoRequest(BaseModel):
    """Request model for video info."""
    url: str

class DownloadResponse(BaseModel):
    """Response model for download operations."""
    success: bool
    message: str
    filename: Optional[str] = None
    download_url: Optional[str] = None
    title: Optional[str] = None
    duration: Optional[int] = None
    filesize: Optional[int] = None
    thumbnail: Optional[str] = None

@router.get("/stream")
async def stream_download(
    url: str = Query(..., description="The URL of the video to download"),
    format_type: str = Query("video", description="video or audio"),
    quality: str = Query("best", description="Quality setting")
):
    """
    Start a video download and stream it directly to the client browser.
    Called directly via browser window/anchor tag to trigger a native download prompt.
    """
    try:
        # get_video_stream handles everything: validation, download to tmp, and returning generator
        result = await get_video_stream(
            url=url,
            format_type=format_type,
            quality=quality
        )
        
        if result.get("success"):
            generator = result["stream_generator"]
            filename = result["filename"]
            
            # Setup headers for native browser download
            headers = {
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
            return StreamingResponse(
                generator(),
                media_type="application/octet-stream",
                headers=headers
            )
        else:
            # If we fail before streaming starts, redirect to a safe error page,
            # or in this API context, return a 400 since it's a direct API hit via an a tag.
            raise HTTPException(status_code=400, detail=result.get("message", "Download failed"))
            
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An internal server error occurred.")


@router.post("/info")
async def get_info(request: VideoInfoRequest):
    """
    Get video information without downloading.
    
    Args:
        request: VideoInfoRequest with URL
    
    Returns:
        Video metadata including title, duration, thumbnail
    """
    try:
        info = await get_video_info(request.url)
        
        if 'error' in info:
            raise HTTPException(status_code=400, detail=info['error'])
        
        return {
            "success": True,
            "platform": detect_platform(request.url),
            "info": info
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/file/{filename}")
async def get_downloaded_file(filename: str):
    """
    Download a previously downloaded file.
    
    Args:
        filename: Name of the file to download
    
    Returns:
        File download response
    """
    filepath = DOWNLOADS_DIR / filename
    
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Security check - ensure file is in downloads directory
    try:
        filepath.resolve().relative_to(DOWNLOADS_DIR.resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Access denied")
    
    extension = filepath.suffix.lstrip('.')
    media_type = get_mime_type(extension)
    
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type=media_type
    )


@router.get("/platforms")
async def get_supported_platforms():
    """Get list of supported platforms for download."""
    return {
        "platforms": [
            {"name": "YouTube", "domain": "youtube.com", "icon": "🎬"},
            {"name": "TikTok", "domain": "tiktok.com", "icon": "🎵"},
            {"name": "Instagram", "domain": "instagram.com", "icon": "📸"},
            {"name": "Twitter/X", "domain": "twitter.com", "icon": "🐦"},
            {"name": "Facebook", "domain": "facebook.com", "icon": "👥"}
        ]
    }

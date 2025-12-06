"""
API router for download endpoints.
Handles video downloads from social media platforms.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl, validator
from typing import Optional
from pathlib import Path
import asyncio

from backend.services.downloader import (
    download_video,
    download_audio_only,
    get_video_info,
    validate_url,
    detect_platform
)
from backend.config import DOWNLOADS_DIR
from backend.utils.helpers import get_mime_type


router = APIRouter(prefix="/api/download", tags=["download"])


class DownloadRequest(BaseModel):
    """Request model for video download."""
    url: str
    format_type: str = "video"  # video or audio
    quality: str = "best"  # best, worst, or specific
    
    @validator('url')
    def validate_url_format(cls, v):
        is_valid, msg = validate_url(v)
        if not is_valid:
            raise ValueError(msg)
        return v
    
    @validator('format_type')
    def validate_format_type(cls, v):
        if v not in ['video', 'audio']:
            raise ValueError('format_type must be "video" or "audio"')
        return v


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


# Store for tracking download progress
download_progress = {}


@router.post("/start", response_model=DownloadResponse)
async def start_download(request: DownloadRequest):
    """
    Start a video download from a supported platform.
    
    Supported platforms:
    - YouTube
    - TikTok
    - Instagram
    - Twitter/X
    - Facebook
    
    Args:
        request: DownloadRequest with URL and format options
    
    Returns:
        DownloadResponse with download status and file info
    """
    try:
        result = await download_video(
            url=request.url,
            format_type=request.format_type,
            quality=request.quality
        )
        
        if result.success:
            return DownloadResponse(
                success=True,
                message=result.message,
                filename=result.filename,
                download_url=f"/api/download/file/{result.filename}",
                title=result.title,
                duration=result.duration,
                filesize=result.filesize,
                thumbnail=result.thumbnail
            )
        else:
            # Return the user-friendly message instead of raising
            return DownloadResponse(
                success=False,
                message=result.message
            )
            
    except Exception as e:
        # Log error for debugging
        print(f"Download error: {str(e)}")
        return DownloadResponse(
            success=False,
            message="Our download servers are busy. Please try again in a few seconds!"
        )


@router.post("/audio", response_model=DownloadResponse)
async def download_audio(request: VideoInfoRequest):
    """
    Download only the audio track from a video.
    
    Args:
        request: VideoInfoRequest with URL
    
    Returns:
        DownloadResponse with download status
    """
    try:
        result = await download_audio_only(request.url)
        
        if result.success:
            return DownloadResponse(
                success=True,
                message=result.message,
                filename=result.filename,
                download_url=f"/api/download/file/{result.filename}",
                title=result.title,
                duration=result.duration,
                filesize=result.filesize
            )
        else:
            raise HTTPException(status_code=400, detail=result.message)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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

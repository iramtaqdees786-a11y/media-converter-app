"""
API router for file conversion endpoints.
Handles file uploads and format conversions.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
from pathlib import Path
import shutil
import aiofiles

from backend.services.converter import convert_file, ConversionResult
from backend.config import UPLOADS_DIR, CONVERTED_DIR, SUPPORTED_FORMATS
from backend.utils.helpers import (
    generate_unique_filename,
    get_file_extension,
    get_file_category,
    validate_conversion,
    get_mime_type,
    format_file_size
)


router = APIRouter(prefix="/api/convert", tags=["convert"])


class ConversionResponse(BaseModel):
    """Response model for conversion operations."""
    success: bool
    message: str
    original_file: Optional[str] = None
    converted_file: Optional[str] = None
    download_url: Optional[str] = None
    original_size: Optional[str] = None
    converted_size: Optional[str] = None


class ConvertExistingRequest(BaseModel):
    """Request model for converting already uploaded/downloaded files."""
    filename: str
    target_format: str
    source_dir: str = "uploads"  # uploads or downloads


@router.post("/upload", response_model=ConversionResponse)
async def upload_and_convert(
    file: UploadFile = File(...),
    target_format: str = Form(...)
):
    """
    Upload a file and convert it to the target format.
    
    Supported conversions:
    - Video: mp4, mkv, webm, avi, mov
    - Audio: mp3, wav, aac, ogg, flac
    - Image: jpg, png, webp, gif, bmp
    - Document: pdf, docx, txt
    - Spreadsheet: xlsx, xls, csv
    
    Args:
        file: File to upload and convert
        target_format: Target format for conversion
    
    Returns:
        ConversionResponse with conversion status and download URL
    """
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    source_ext = get_file_extension(file.filename)
    target_format = target_format.lower().lstrip('.')
    
    # Validate conversion
    is_valid, error_msg = validate_conversion(source_ext, target_format)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)
    
    # Save uploaded file
    upload_filename = generate_unique_filename(file.filename)
    upload_path = UPLOADS_DIR / upload_filename
    
    try:
        # Write file asynchronously
        async with aiofiles.open(upload_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        # Perform conversion
        result = await convert_file(upload_path, target_format)
        
        if result.success:
            return ConversionResponse(
                success=True,
                message=result.message,
                original_file=result.original_file,
                converted_file=result.converted_file,
                download_url=f"/api/convert/file/{result.converted_file}",
                original_size=format_file_size(result.original_size) if result.original_size else None,
                converted_size=format_file_size(result.converted_size) if result.converted_size else None
            )
        else:
            # Return the user-friendly message from the converter
            return ConversionResponse(
                success=False,
                message=result.message
            )
            
    except HTTPException:
        raise
    except Exception as e:
        # Clean up on error
        if upload_path.exists():
            upload_path.unlink()
        # Return friendly error instead of raising
        print(f"Conversion error: {str(e)}")  # Log for debugging
        return ConversionResponse(
            success=False,
            message="We're experiencing high demand right now. Please try again in a moment!"
        )


@router.post("/existing", response_model=ConversionResponse)
async def convert_existing_file(request: ConvertExistingRequest):
    """
    Convert an already uploaded or downloaded file.
    
    Args:
        request: ConvertExistingRequest with filename and target format
    
    Returns:
        ConversionResponse with conversion status
    """
    # Determine source directory
    if request.source_dir == "downloads":
        from backend.config import DOWNLOADS_DIR
        source_dir = DOWNLOADS_DIR
    else:
        source_dir = UPLOADS_DIR
    
    source_path = source_dir / request.filename
    
    if not source_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    target_format = request.target_format.lower().lstrip('.')
    source_ext = get_file_extension(request.filename)
    
    # Validate conversion
    is_valid, error_msg = validate_conversion(source_ext, target_format)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)
    
    try:
        result = await convert_file(source_path, target_format)
        
        if result.success:
            return ConversionResponse(
                success=True,
                message=result.message,
                original_file=result.original_file,
                converted_file=result.converted_file,
                download_url=f"/api/convert/file/{result.converted_file}",
                original_size=format_file_size(result.original_size) if result.original_size else None,
                converted_size=format_file_size(result.converted_size) if result.converted_size else None
            )
        else:
            raise HTTPException(status_code=400, detail=result.message)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/file/{filename}")
async def get_converted_file(filename: str):
    """
    Download a converted file.
    
    Args:
        filename: Name of the converted file
    
    Returns:
        File download response
    """
    filepath = CONVERTED_DIR / filename
    
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Security check
    try:
        filepath.resolve().relative_to(CONVERTED_DIR.resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Access denied")
    
    extension = filepath.suffix.lstrip('.')
    media_type = get_mime_type(extension)
    
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type=media_type
    )


@router.get("/formats")
async def get_supported_formats():
    """Get all supported formats organized by category."""
    return {
        "formats": SUPPORTED_FORMATS,
        "conversions": {
            "video": {
                "from": SUPPORTED_FORMATS["video"],
                "to": SUPPORTED_FORMATS["video"] + SUPPORTED_FORMATS["audio"]
            },
            "audio": {
                "from": SUPPORTED_FORMATS["audio"],
                "to": SUPPORTED_FORMATS["audio"]
            },
            "image": {
                "from": SUPPORTED_FORMATS["image"],
                "to": SUPPORTED_FORMATS["image"]
            },
            "document": {
                "from": SUPPORTED_FORMATS["document"],
                "to": SUPPORTED_FORMATS["document"]
            },
            "spreadsheet": {
                "from": SUPPORTED_FORMATS["spreadsheet"],
                "to": SUPPORTED_FORMATS["spreadsheet"]
            }
        }
    }


@router.get("/formats/{category}")
async def get_formats_by_category(category: str):
    """Get supported formats for a specific category."""
    if category not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=404, 
            detail=f"Category not found. Available: {list(SUPPORTED_FORMATS.keys())}"
        )
    
    return {
        "category": category,
        "formats": SUPPORTED_FORMATS[category]
    }

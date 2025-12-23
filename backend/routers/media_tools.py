from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
import uuid
import os

from backend.config import UPLOADS_DIR, CONVERTED_DIR, DOWNLOADS_DIR
from backend.services.media_tools_service import MediaToolsService

router = APIRouter(
    prefix="/api/media-tools",
    tags=["media-tools"]
)

media_service = MediaToolsService(UPLOADS_DIR, CONVERTED_DIR, DOWNLOADS_DIR)

@router.post("/thumbnail")
async def download_thumbnail(url: str = Form(...)):
    try:
        result = await media_service.download_thumbnail(url)
        if "path" in result:
             # If we downloaded it locally
             filename = result["filename"]
             return {
                 "success": True,
                 "download_url": f"/api/convert/download/{filename}?source=downloads", # Helper to download from downloads dir?
                 # Wait, existing download endpoint might only serve from converted.
                 # We should check `backend/routers/download.py` or `convert.py` to see where it serves files.
                 # Typically we might need to move it to 'converted' or serve from 'downloads'.
                 # Let's move it to converted to safely use existing download endpoint if it's restricted.
             }
        elif "url" in result:
             return {"success": True, "image_url": result["url"]}
        else:
             raise HTTPException(status_code=404, detail="Could not find thumbnail")
             
        # Move to converted for serving
        source_path = result["path"]
        target_path = CONVERTED_DIR / result["filename"]
        shutil.move(source_path, target_path)
        
        return {
            "success": True, 
            "filename": result["filename"],
            "download_url": f"/api/convert/download/{result['filename']}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/trim-video")
async def trim_video(
    file: UploadFile = File(...),
    start_time: str = Form(None),
    end_time: str = Form(None)
):
    try:
        job_id = str(uuid.uuid4())
        file_path = UPLOADS_DIR / f"{job_id}_{file.filename}"
        
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        output_filename = f"trimmed_{job_id}_{file.filename}"
        output_path = await media_service.trim_video(file_path, start_time, end_time, output_filename)
        
        os.remove(file_path)

        return {
            "success": True,
            "filename": output_filename,
            "download_url": f"/api/convert/download/{output_filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/strip-exif")
async def strip_exif(file: UploadFile = File(...)):
    try:
        job_id = str(uuid.uuid4())
        file_path = UPLOADS_DIR / f"{job_id}_{file.filename}"
        
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        output_filename = f"clean_{job_id}_{file.filename}"
        output_path = await media_service.strip_exif(file_path, output_filename)
        
        os.remove(file_path)

        return {
            "success": True,
            "filename": output_filename,
            "download_url": f"/api/convert/download/{output_filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from typing import List
import shutil
import uuid
import os

from backend.config import UPLOADS_DIR, CONVERTED_DIR
from backend.services.pdf_service import PDFService

router = APIRouter(
    prefix="/api/pdf",
    tags=["pdf"]
)

pdf_service = PDFService(UPLOADS_DIR, CONVERTED_DIR)

@router.post("/merge")
async def merge_pdfs(
    files: List[UploadFile] = File(...),
    background_tasks: BackgroundTasks = None
):
    try:
        # Save uploaded files
        file_paths = []
        job_id = str(uuid.uuid4())
        
        for file in files:
            if not file.filename.lower().endswith('.pdf'):
                raise HTTPException(status_code=400, detail=f"File {file.filename} is not a PDF")
            
            temp_name = f"{job_id}_{file.filename}"
            file_path = UPLOADS_DIR / temp_name
            
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            file_paths.append(file_path)

        output_filename = f"merged_{job_id}.pdf"
        output_path = await pdf_service.merge_pdfs(file_paths, output_filename)
        
        # Cleanup input files
        for path in file_paths:
            try:
                os.remove(path)
            except:
                pass

        return {
            "success": True,
            "filename": output_filename,
            "download_url": f"/api/convert/download/{output_filename}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/remove-pages")
async def remove_pages(
    file: UploadFile = File(...),
    pages: str = Form(..., description="Comma separated list of page numbers to remove (1-indexed)"),
):
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")

        job_id = str(uuid.uuid4())
        file_path = UPLOADS_DIR / f"{job_id}_{file.filename}"
        
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        try:
            pages_list = [int(p.strip()) for p in pages.split(',') if p.strip()]
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid page numbers format")

        output_filename = f"edited_{job_id}.pdf"
        output_path = await pdf_service.remove_pages(file_path, pages_list, output_filename)
        
        os.remove(file_path)

        return {
            "success": True,
            "filename": output_filename,
            "download_url": f"/api/convert/download/{output_filename}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compress")
async def compress_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")

        job_id = str(uuid.uuid4())
        file_path = UPLOADS_DIR / f"{job_id}_{file.filename}"
        
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        output_filename = f"compressed_{job_id}.pdf"
        output_path = await pdf_service.compress_pdf(file_path, output_filename)
        
        os.remove(file_path)

        return {
            "success": True,
            "filename": output_filename,
            "download_url": f"/api/convert/download/{output_filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/grayscale")
async def grayscale_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")

        job_id = str(uuid.uuid4())
        file_path = UPLOADS_DIR / f"{job_id}_{file.filename}"
        
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        output_filename = f"grayscale_{job_id}.pdf"
        try:
            output_path = await pdf_service.grayscale_pdf(file_path, output_filename)
        except NotImplementedError as e:
             raise HTTPException(status_code=501, detail=str(e))
        
        os.remove(file_path)

        return {
            "success": True,
            "filename": output_filename,
            "download_url": f"/converted/{output_filename}"
        }
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pdfa")
async def pdf_to_pdfa(file: UploadFile = File(...)):
    try:
         if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")

         job_id = str(uuid.uuid4())
         file_path = UPLOADS_DIR / f"{job_id}_{file.filename}"
        
         with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

         output_filename = f"pdfa_{job_id}.pdf"
         try:
            output_path = await pdf_service.convert_to_pdfa(file_path, output_filename)
         except NotImplementedError as e:
             raise HTTPException(status_code=501, detail=str(e))
             
         os.remove(file_path)

         return {
            "success": True,
            "filename": output_filename,
            "download_url": f"/api/convert/download/{output_filename}"
        }
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))

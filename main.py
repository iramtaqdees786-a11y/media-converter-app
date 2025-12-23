"""
ConvertRocket - Main FastAPI Application
Domain: convertrocket.online

The fastest way to download videos & convert files online. 100% Free!
Supports downloading from YouTube, TikTok, Instagram and converting
various file formats including video, audio, images, documents, and spreadsheets.
"""

import os
import sys
from pathlib import Path

# Add the project root to path for imports
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import uvicorn

from backend.routers import download, convert, pdf_tools, media_tools
from backend.config import DOWNLOADS_DIR, UPLOADS_DIR, CONVERTED_DIR

# Create FastAPI application
app = FastAPI(
    title="ConvertRocket API",
    description="""
    # ConvertRocket - The Fastest Video Downloader & File Converter
    
    **Domain:** [convertrocket.online](https://convertrocket.online)
    
    Free online video downloader and file converter. Download from YouTube, TikTok, Instagram, Twitter, Facebook. Convert any file format instantly.
    
    ## 🚀 Features
    
    ### Video Download
    - Download videos from **YouTube**, **TikTok**, **Instagram**, **Twitter**, **Facebook**
    - Extract audio from any video (YouTube to MP3)
    - Get video information before downloading
    - Support for HD quality downloads
    
    ### File Conversion
    - **Video**: MP4, MKV, WebM, AVI, MOV
    - **Audio**: MP3, WAV, AAC, OGG, FLAC
    - **Images**: JPG, JPEG, PNG, WebP, GIF, BMP
    - **Documents**: PDF, DOCX, TXT
    - **Spreadsheets**: XLSX, XLS, CSV
    
    ## 🔒 Security
    - Files are processed securely
    - No permanent storage of user files
    - HTTPS encryption
    
    ## 🌍 Global
    - Available in 17+ languages
    - Works worldwide
    - No signup required
    
    ---
    **Keywords:** youtube downloader, tiktok downloader, instagram video download, mp4 to mp3, file converter, online converter, free video download
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "ConvertRocket Support",
        "url": "https://convertrocket.online",
        "email": "support@convertrocket.online"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=[
        {"name": "download", "description": "Video download operations from social media platforms"},
        {"name": "convert", "description": "File format conversion operations"}
    ]
)

# Configure CORS to allow Vercel frontend and custom domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://convertrocket.online",
        "https://www.convertrocket.online",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Middleware to add Cache-Control headers for static assets
@app.middleware("http")
async def add_cache_control_header(request: Request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/static/") or request.url.path.startswith("/css/") or request.url.path.startswith("/js/") or request.url.path.startswith("/img/"):
        # Cache for 1 day: 86400 seconds
        response.headers["Cache-Control"] = "public, max-age=86400"
    return response

# Include routers
app.include_router(download.router)
app.include_router(convert.router)
app.include_router(pdf_tools.router)
app.include_router(media_tools.router)

# Mount static files for frontend (only if they exist)
FRONTEND_DIR = PROJECT_ROOT / "frontend"
if FRONTEND_DIR.exists():
    # CSS
    css_dir = FRONTEND_DIR / "css"
    if css_dir.exists():
        app.mount("/css", StaticFiles(directory=str(css_dir)), name="css")
    # JS
    js_dir = FRONTEND_DIR / "js"
    if js_dir.exists():
        app.mount("/js", StaticFiles(directory=str(js_dir)), name="js")
    # Images (optional)
    img_dir = FRONTEND_DIR / "img"
    if not img_dir.exists():
        # create empty img folder to avoid runtime errors
        img_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/img", StaticFiles(directory=str(img_dir)), name="img")
    # Serve root static files (e.g., index.html)
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

    # Mount Generated Content Directories
    if not CONVERTED_DIR.exists():
        CONVERTED_DIR.mkdir(parents=True, exist_ok=True)
    app.mount("/converted", StaticFiles(directory=str(CONVERTED_DIR)), name="converted")
    
    if not DOWNLOADS_DIR.exists():
        DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
    app.mount("/downloads", StaticFiles(directory=str(DOWNLOADS_DIR)), name="downloads")



@app.get("/")
async def serve_frontend():
    """Serve the frontend application."""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return JSONResponse({
        "message": "Media Converter API",
        "docs": "/docs",
        "version": "1.0.0"
    })


@app.get("/pdf-to-excel")
@app.get("/pdf-to-excel.html")
async def serve_pdf_to_excel():
    return FileResponse(FRONTEND_DIR / "pdf-to-excel.html")

@app.get("/video-converter")
@app.get("/video-converter.html")
async def serve_video_converter():
    return FileResponse(FRONTEND_DIR / "video-converter.html")

@app.get("/mp3-converter")
@app.get("/mp3-converter.html")
async def serve_mp3_converter():
    return FileResponse(FRONTEND_DIR / "mp3-converter.html")

@app.get("/image-converter")
@app.get("/image-converter.html")
async def serve_image_converter():
    return FileResponse(FRONTEND_DIR / "image-converter.html")


@app.get("/pdf-tools")
@app.get("/pdf-tools.html")
async def serve_pdf_tools():
    return FileResponse(FRONTEND_DIR / "pdf-tools.html")


@app.get("/media-tools")
@app.get("/media-tools.html")
async def serve_media_tools():
    return FileResponse(FRONTEND_DIR / "media-tools.html")


@app.get("/pdf-merge")
async def serve_pdf_merge(): return FileResponse(FRONTEND_DIR / "pdf-merge.html")

@app.get("/pdf-compress")
async def serve_pdf_compress(): return FileResponse(FRONTEND_DIR / "pdf-compress.html")

@app.get("/pdf-remove-pages")
async def serve_pdf_remove(): return FileResponse(FRONTEND_DIR / "pdf-remove-pages.html")

@app.get("/pdf-grayscale")
async def serve_pdf_grayscale(): return FileResponse(FRONTEND_DIR / "pdf-grayscale.html")

@app.get("/pdf-pdfa")
async def serve_pdf_pdfa(): return FileResponse(FRONTEND_DIR / "pdf-pdfa.html")

@app.get("/yt-thumbnail")
async def serve_yt_thumbnail(): return FileResponse(FRONTEND_DIR / "yt-thumbnail.html")

@app.get("/video-trimmer")
async def serve_video_trimmer(): return FileResponse(FRONTEND_DIR / "video-trimmer.html")

@app.get("/exif-remover")
async def serve_exif_remover(): return FileResponse(FRONTEND_DIR / "exif-remover.html")


@app.get("/blogs")
@app.get("/blogs.html")
async def serve_blogs():
    if (FRONTEND_DIR / "blogs.html").exists():
        return FileResponse(FRONTEND_DIR / "blogs.html")
    return JSONResponse(status_code=404, content={"message": "Blogs page not found"})


@app.get("/blog/{slug}")
async def serve_blog_post(slug: str):
    """Serve individual blog posts."""
    # Ensure secure filename access
    slug = Path(slug).name
    if not slug.endswith(".html"):
        slug += ".html"
    
    post_path = FRONTEND_DIR / "blog" / slug
    if post_path.exists():
        return FileResponse(post_path)
    return JSONResponse(status_code=404, content={"message": "Blog post not found"})


@app.get("/sitemap.xml")
async def serve_sitemap():
    if (FRONTEND_DIR / "sitemap.xml").exists():
        return FileResponse(FRONTEND_DIR / "sitemap.xml", media_type="application/xml")
    return JSONResponse(status_code=404, content={"message": "Sitemap not found"})

@app.get("/robots.txt")
async def serve_robots():
    if (FRONTEND_DIR / "robots.txt").exists():
        return FileResponse(FRONTEND_DIR / "robots.txt", media_type="text/plain")
    return JSONResponse(status_code=404, content={"message": "Robots.txt not found"})

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "directories": {
            "downloads": str(DOWNLOADS_DIR),
            "uploads": str(UPLOADS_DIR),
            "converted": str(CONVERTED_DIR)
        }
    }


@app.get("/api/stats")
async def get_stats():
    """Get application statistics."""
    def count_files(directory: Path) -> dict:
        if not directory.exists():
            return {"count": 0, "size": 0}
        files = list(directory.iterdir())
        total_size = sum(f.stat().st_size for f in files if f.is_file())
        return {"count": len(files), "size": total_size}
    
    return {
        "downloads": count_files(DOWNLOADS_DIR),
        "uploads": count_files(UPLOADS_DIR),
        "converted": count_files(CONVERTED_DIR)
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "An unexpected error occurred",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    print("""
    ================================================================
                  ConvertRocket - convertrocket.online          
                                                                 
       Starting server at http://localhost:8000                    
       API Documentation: http://localhost:8000/docs               
                                                                 
       Downloads: YouTube, TikTok, Instagram, Twitter, Facebook    
       Converts: Video, Audio, Images, Documents, Spreadsheets     
       Languages: 17+ supported languages                          
    ================================================================
    """)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

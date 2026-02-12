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

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
import uvicorn
from datetime import datetime, timedelta

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

# WWW Redirect & Canonical URL Middleware (CRITICAL FOR SEO)
# WWW Redirect & Canonical URL Middleware (CRITICAL FOR SEO)
@app.middleware("http")
async def canonical_url_middleware(request: Request, call_next):
    """
    Ensures all traffic goes to www.convertrocket.online with proper redirects.
    Fixes Google Search Console indexing issues.
    """
    host = request.headers.get("host", "")
    scheme = request.url.scheme
    path = request.url.path
    query = request.url.query
    
    # 1. Force HTTPS in production
    if scheme == "http" and "localhost" not in host and "127.0.0.1" not in host:
        url = f"https://{host}{path}"
        if query:
            url += f"?{query}"
        return RedirectResponse(url=url, status_code=308) # use 308 for permanent redirect preserving method
    
    # 2. Force WWW subdomain (Critical for SEO)
    if host == "convertrocket.online":
        url = f"{scheme}://www.convertrocket.online{path}"
        if query:
            url += f"?{query}"
        return RedirectResponse(url=url, status_code=308)
    
    # 3. Remove trailing slashes for consistency (except root)
    if path != "/" and path.endswith("/") and not path.startswith("/api/"):
        new_path = path.rstrip("/")
        url = f"{scheme}://{host}{new_path}"
        if query:
            url += f"?{query}"
        return RedirectResponse(url=url, status_code=308)
    
    # 4. Redirect index.html to root
    if path == "/index.html":
        url = f"{scheme}://{host}/"
        if query:
            url += f"?{query}"
        return RedirectResponse(url=url, status_code=308)
    
    return await call_next(request)

# Custom Middleware for SEO & Performance
@app.middleware("http")
async def seo_and_performance_middleware(request: Request, call_next):
    # Process request
    response = await call_next(request)
    
    path = request.url.path
    
    # 1. Add Cache-Control & Expires for Assets
    if any(path.startswith(pre) for pre in ["/static/", "/css/", "/js/", "/img/", "/assets/"]) or \
       any(path.endswith(ext) for ext in [".js", ".css", ".png", ".jpg", ".jpeg", ".svg", ".webp", ".ico", ".woff", ".woff2"]):
        # Cache for 1 year for static assets (standard practice)
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        expires_date = (datetime.utcnow() + timedelta(days=365)).strftime("%a, %d %b %Y %H:%M:%S GMT")
        response.headers["Expires"] = expires_date
        return response

    # 2. Dynamic SEO Placeholder Replacement [MONTH_YEAR]
    content_type = response.headers.get("content-type", "")
    if "text/html" in content_type:
        try:
            # Safer way to handle FileResponse or regular Response
            if isinstance(response, FileResponse):
                # We skip replacement for binary or very large files if they were somehow served as text/html
                if response.path.endswith(".html"):
                    with open(response.path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    
                    current_date = datetime.now().strftime("%B %Y")
                    if "[MONTH_YEAR]" in content:
                        content = content.replace("[MONTH_YEAR]", current_date)
                        # We return a new Response with the modified content
                        new_response = Response(content=content, media_type="text/html", headers=dict(response.headers))
                        # Remove content-length as it changed
                        if "content-length" in new_response.headers:
                            del new_response.headers["content-length"]
                        return new_response
        except Exception as e:
            # LOG ERROR INSTEAD OF CRASHING
            print(f"SEO Middleware Error serving {path}: {e}")
            
    return response

# Extensionless URL Support (Friendly Links)
@app.middleware("http")
async def friendly_urls_middleware(request: Request, call_next):
    path = request.url.path
    
    # Redirect .html to clean URL
    if path.endswith(".html") and not path.startswith("/api/"):
        new_path = path[:-5]
        return RedirectResponse(url=new_path, status_code=308)

    if not path.endswith(".html") and not path.split("/")[-1].count(".") and path != "/" and not path.startswith("/api/"):
        potential_file = FRONTEND_DIR / f"{path.strip('/')}.html"
        if potential_file.exists():
             return FileResponse(potential_file)
    return await call_next(request)

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

# Redirect old mp4-converter URL to mp3-converter for backward compatibility
@app.get("/mp4-converter")
@app.get("/mp4-converter.html")
async def redirect_mp4_converter():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/mp3-converter.html", status_code=301)

@app.get("/image-converter")
@app.get("/image-converter.html")
async def serve_image_converter():
    return FileResponse(FRONTEND_DIR / "image-converter.html")
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
@app.get("/exif-remover.html")
async def serve_exif_remover(): return FileResponse(FRONTEND_DIR / "exif-remover.html")

@app.get("/all-tools")
async def serve_all_tools():
    return FileResponse(FRONTEND_DIR / "all-tools.html")

@app.get("/ai-lab")
async def serve_ai_lab():
    return FileResponse(FRONTEND_DIR / "ai-lab.html")

@app.get("/media-hub")
async def serve_media_hub():
    return FileResponse(FRONTEND_DIR / "media-hub.html")

@app.get("/pdf-lab")
async def serve_pdf_lab():
    return FileResponse(FRONTEND_DIR / "pdf-lab.html")

@app.get("/dev-suite")
async def serve_dev_suite():
    return FileResponse(FRONTEND_DIR / "dev-suite.html")

@app.get("/utilities")
async def serve_utilities():
    return FileResponse(FRONTEND_DIR / "utilities.html")

@app.get("/downloader")
async def serve_downloader():
    return FileResponse(FRONTEND_DIR / "downloader.html")

@app.get("/converter")
async def serve_converter():
    return FileResponse(FRONTEND_DIR / "converter.html")

@app.get("/json-formatter")
async def serve_json_formatter():
    return FileResponse(FRONTEND_DIR / "json-formatter.html")

@app.get("/base64-encoder")
async def serve_base64_encoder():
    return FileResponse(FRONTEND_DIR / "base64-encoder.html")

@app.get("/color-picker")
async def serve_color_picker():
    return FileResponse(FRONTEND_DIR / "color-picker.html")

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

@app.get("/ads.txt")
async def serve_ads_txt():
    if (FRONTEND_DIR / "ads.txt").exists():
        return FileResponse(FRONTEND_DIR / "ads.txt", media_type="text/plain")
    return JSONResponse(status_code=404, content={"message": "ads.txt not found"})

@app.get("/llms.txt")
async def serve_llms_txt():
    if (FRONTEND_DIR / "llms.txt").exists():
        return FileResponse(FRONTEND_DIR / "llms.txt", media_type="text/plain")
    return JSONResponse(status_code=404, content={"message": "llms.txt not found"})

@app.get("/privacy-policy")
@app.get("/privacy-policy.html")
async def serve_privacy():
    return FileResponse(FRONTEND_DIR / "privacy-policy.html")

@app.get("/terms-of-service")
@app.get("/terms-of-service.html")
async def serve_terms():
    return FileResponse(FRONTEND_DIR / "terms-of-service.html")

@app.get("/about")
@app.get("/about.html")
async def serve_about():
    return FileResponse(FRONTEND_DIR / "about.html")

@app.get("/contact")
@app.get("/contact.html")
async def serve_contact():
    return FileResponse(FRONTEND_DIR / "contact.html")

@app.get("/sitemap")
@app.get("/sitemap.html")
async def serve_sitemap():
    return FileResponse(FRONTEND_DIR / "sitemap.html")

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

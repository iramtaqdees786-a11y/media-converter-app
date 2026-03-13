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
import re
import json
import csv
import io
from datetime import datetime, timedelta

# --- Directory Constants (Defined Early for Middleware) ---
PROJECT_ROOT = Path(__file__).resolve().parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
UPLOADS_DIR = PROJECT_ROOT / "backend" / "uploads"
DOWNLOADS_DIR = PROJECT_ROOT / "backend" / "downloads"
CONVERTED_DIR = PROJECT_ROOT / "backend" / "converted"

# Ensure directories exist
for d in [UPLOADS_DIR, DOWNLOADS_DIR, CONVERTED_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Add the project root to path for imports
sys.path.insert(0, str(PROJECT_ROOT))

# FastAPI Imports
from fastapi import FastAPI, Request, Response, BackgroundTasks, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
import uvicorn

from backend.routers import convert, pdf_tools, media_tools
from backend.seo_config import SEO_METADATA, DEFAULT_METADATA, get_software_schema, get_faq_schema, FAQ_DATA
from backend.database import save_lead, get_all_leads

# Create FastAPI application
app = FastAPI(
    title="ConvertRocket API",
    description="Free online video downloader and file converter.",
    version="1.0.0",
)

# Static Resource Mounting
app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")
app.mount("/img", StaticFiles(directory=FRONTEND_DIR / "img"), name="img")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WWW Redirect & Canonical URL Middleware
@app.middleware("http")
async def canonical_url_middleware(request: Request, call_next):
    host = request.headers.get("host", "")
    scheme = request.url.scheme
    path = request.url.path
    query = request.url.query
    
    if path.startswith("/api/"): return await call_next(request)
    if scheme == "http" and "localhost" not in host and "127.0.0.1" not in host:
        url = f"https://{host}{path}"; return RedirectResponse(url=url, status_code=308)
    if host == "convertrocket.online":
        url = f"{scheme}://www.convertrocket.online{path}"; return RedirectResponse(url=url, status_code=308)
    if path != "/" and path.endswith("/") and not path.startswith("/api/"):
        url = f"{scheme}://{host}{path.rstrip('/')}"; return RedirectResponse(url=url, status_code=308)
    return await call_next(request)

# Static routes for trust files
@app.get("/ads.txt")
async def ads_txt():
    ads_file = FRONTEND_DIR / "ads.txt"
    if ads_file.exists(): return FileResponse(ads_file)
    return Response(content="google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0", media_type="text/plain")

# Main Application Middleware (SEO, Performance, Friendly URLs, Workspace)
@app.middleware("http")
async def main_application_middleware(request: Request, call_next):
    path = request.url.path
    if path.endswith(".html") and not path.startswith("/api/"):
        return RedirectResponse(url=path[:-5], status_code=308)

    response = None
    if not path.endswith(".html") and not path.split("/")[-1].count(".") and path != "/" and not path.startswith("/api/"):
        if path.startswith("/blog/"):
            potential_file = FRONTEND_DIR / "blog" / f"{path.split('/')[-1]}.html"
        else:
            potential_file = FRONTEND_DIR / f"{path.strip('/')}.html"
        if potential_file.exists(): response = FileResponse(potential_file)

    if response is None: response = await call_next(request)
    
    # Cache Control
    if any(path.startswith(pre) for pre in ["/css/", "/js/", "/img/"]) or any(path.endswith(ext) for ext in [".js", ".css", ".png", ".jpg", ".webp"]):
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        return response

    content_type = response.headers.get("content-type", "").lower()
    is_html_file = isinstance(response, FileResponse) and str(getattr(response, "path", "")).lower().endswith(".html")
    
    if "text/html" in content_type or is_html_file:
        try:
            if isinstance(response, FileResponse):
                with open(response.path, "r", encoding="utf-8", errors="ignore") as f: content = f.read()
            else:
                content = response.body.decode("utf-8", errors="ignore")
            
            # -- AdSense Auto Ads Injection --
            ads_txt_path = FRONTEND_DIR / "ads.txt"
            pub_id = "pub-0000000000000000"
            if ads_txt_path.exists():
                with open(ads_txt_path, "r") as f:
                    ads_text = f.read()
                    match = re.search(r"pub-\d+", ads_text)
                    if match: pub_id = match.group(0)
            
            if f"ca-{pub_id}" not in content and '</head>' in content:
                adsense_script = f'\n    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-{pub_id}" crossorigin="anonymous"></script>'
                content = content.replace('</head>', f'{adsense_script}\n</head>')

            # -- SEO Injections --
            current_year = "2026"
            content = content.replace("[YEAR]", current_year)
            
            # Canonical
            canonical_url = f"https://www.convertrocket.online{path}"
            if '</head>' in content:
                content = content.replace('</head>', f'    <link rel="canonical" href="{canonical_url}">\n</head>')

            # Metadata
            tool_meta = SEO_METADATA.get(path, DEFAULT_METADATA)
            title = tool_meta['title'].replace("[YEAR]", current_year)
            content = re.sub(r'<title>.*?</title>', f"<title>{title}</title>", content, flags=re.I, count=1)
            
            # Schema
            schemas = [get_software_schema(path, tool_meta)]
            faq_schema = get_faq_schema(path)
            if faq_schema: schemas.append(faq_schema)
            schema_html = "".join([f'\n    <script type="application/ld+json">\n    {json.dumps(s)}\n    </script>' for s in schemas])
            if '</head>' in content:
                content = content.replace('</head>', f'{schema_html}\n</head>')

            # Quick Guide
            if "quick_guide" in tool_meta and "<!-- SEO_QUICK_GUIDE -->" not in content:
                guide_steps = "".join([f"<li>{step}</li>" for step in tool_meta["quick_guide"]])
                guide_html = f'<section class="seo-quick-guide" style="margin-top: 50px; padding: 30px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px;"><h3>Quick Guide</h3><ol>{guide_steps}</ol></section><!-- SEO_QUICK_GUIDE -->'
                content = content.replace('</body>', f"{guide_html}\n</body>")

            # Trending Tools & Workspace
            if "<!-- SEO_TRENDING_CLOUD -->" not in content:
                seo_block = '<div class="seo-internal-links" style="margin-top: 60px; padding: 40px; border-top: 1px solid rgba(255,255,255,0.05); text-align: center;"><h4>Trending Tools [YEAR]</h4><a href="/pdf-to-excel" style="margin-right:15px;">PDF to Excel</a> <a href="/bg-remover">Background Remover</a></div><!-- SEO_TRENDING_CLOUD -->'
                content = content.replace('</body>', f"{seo_block}\n</body>")

            if 'src="/js/workspace-share.js"' not in content:
                content = content.replace('</body>', '<script src="/js/workspace-share.js"></script>\n</body>')

            # -- Blog Premium Injection --
            if path.startswith("/blog") or path == "/blogs":
                if 'blog-premium.css' not in content:
                    content = content.replace('</head>', '    <link rel="stylesheet" href="/css/blog-premium.css">\n</head>')
                if 'class="nav-premium"' not in content and '<body>' in content:
                    nav_html = """
    <div class="reading-progress" id="reading-progress"></div>
    <nav class="nav-premium">
        <div class="container" style="display:flex; justify-content:space-between; align-items:center; width:100%;">
            <a href="/" class="brand">🚀 <span>ConvertRocket</span></a>
            <div class="nav-links">
                <a href="/all-tools">All Tools</a>
                <a href="/media-hub">Media Hub</a>
                <a href="/pdf-lab">PDF Lab</a>
                <a href="/workspace">Workspace</a>
                <a href="/blogs">Blog</a>
            </div>
        </div>
    </nav>"""
                    content = content.replace('<body>', f'<body>{nav_html}')
                    progress_script = """
<script>
    window.onscroll = function() {
        let winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        let height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        let scrolled = (winScroll / height) * 100;
        let pr = document.getElementById("reading-progress");
        if(pr) pr.style.width = scrolled + "%";
    };
</script>"""
                    content = content.replace('</body>', f'{progress_script}\n</body>')

            new_response = Response(content=content, media_type="text/html", headers=dict(response.headers))
            if "content-length" in new_response.headers: del new_response.headers["content-length"]
            return new_response
        except Exception as e:
            print(f"[Middleware] Error: {e}")
            
    return response

# Routes
app.include_router(convert.router)
app.include_router(pdf_tools.router)
app.include_router(media_tools.router)

@app.get("/workspace")
async def workspace(): return FileResponse(FRONTEND_DIR / "workspace.html")

@app.get("/blog/{slug}")
async def serve_blog_post(slug: str):
    slug = Path(slug).name
    if not slug.endswith(".html"): slug += ".html"
    post_path = FRONTEND_DIR / "blog" / slug
    if post_path.exists(): return FileResponse(post_path)
    error_page = FRONTEND_DIR / "error.html"
    if error_page.exists():
        with open(error_page, "r", encoding="utf-8") as f: content = f.read()
        return Response(content=content.replace("{{ ERROR_MESSAGE }}", "Blog post not found."), media_type="text/html", status_code=404)
    return JSONResponse(status_code=404, content={"message": "Blog post not found"})

@app.get("/favicon.ico", include_in_schema=False)
async def favicon(): return Response(status_code=204)

class ShareRequest(BaseModel):
    sender_email: str
    recipient_email: str
    tool: str = None
    file_name: str = None

@app.post("/api/share-file")
async def share_file(request: ShareRequest):
    try:
        save_lead(request.sender_email, "active_user", request.tool)
        save_lead(request.recipient_email, "referral", request.tool)
        return {"success": True}
    except Exception as e: return {"success": False, "message": str(e)}

@app.get("/internal/export-leads")
async def export_leads(key: str = None):
    # Simple security key check
    if key != "rocket_leads_2026":
        raise HTTPException(status_code=403, detail="Unauthorized access")
    
    leads = get_all_leads()
    output = "email,role,tool,timestamp\n"
    for lead in leads:
        output += f"{lead[0]},{lead[1]},{lead[2]},{lead[3]}\n"
    
    return Response(content=output, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=convertrocket_leads.csv"
    })

@app.get("/{path:path}")
async def catch_all_tools(path: str):
    if not path or path == "/": return FileResponse(FRONTEND_DIR / "index.html")
    clean_path = path.rstrip("/")
    if clean_path.endswith(".html"): clean_path = clean_path[:-5]
    potential_file = FRONTEND_DIR / f"{clean_path}.html"
    if potential_file.exists(): return FileResponse(potential_file)
    raise HTTPException(status_code=404, detail="Page not found")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_page = FRONTEND_DIR / "error.html"
    if error_page.exists():
        with open(error_page, "r", encoding="utf-8") as f: content = f.read()
        msg = str(exc.detail) if hasattr(exc, "detail") else str(exc)
        return Response(content=content.replace("{{ ERROR_MESSAGE }}", msg), media_type="text/html", status_code=200)
    return JSONResponse(status_code=404, content={"message": "Not found"})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)

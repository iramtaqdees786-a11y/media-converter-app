import os
from pathlib import Path

# Config
FRONTEND_DIR = Path("frontend")
TOOLS_FOOTER_HTML = """
        <div class="footer-links-cloud" style="margin-top: 40px; padding-top: 30px; border-top: 1px solid rgba(255,255,255,0.05);">
            <h4 style="color: #fff; margin-bottom: 15px; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px;">Professional Utility Hub</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 15px; justify-content: center; font-size: 0.85rem;">
                <a href="/pdf-to-excel" style="color: var(--text-secondary);">Convert PDF to Excel</a>
                <a href="/video-converter" style="color: var(--text-secondary);">Video Converter</a>
                <a href="/json-formatter" style="color: var(--text-secondary);">JSON Formatter</a>
                <a href="/image-converter" style="color: var(--text-secondary);">Image Converter</a>
                <a href="/mp3-converter" style="color: var(--text-secondary);">MP3 Converter</a>
                <a href="/qr-generator" style="color: var(--text-secondary);">QR Generator</a>
                <a href="/pdf-merge" style="color: var(--text-secondary);">Merge PDF</a>
                <a href="/pdf-compress" style="color: var(--text-secondary);">Compress PDF</a>
                <a href="/image-compress" style="color: var(--text-secondary);">Compress Image</a>
                <a href="/svg-to-png" style="color: var(--text-secondary);">SVG to PNG</a>
                <a href="/bg-remover" style="color: var(--text-secondary);">AI Background Remover</a>
            </div>
        </div>
"""

def update_html_seo(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    # 1. Inject Footer Links Cloud
    if '<div class="footer-links">' in content and 'footer-links-cloud' not in content:
        content = content.replace('<div class="footer-links">', TOOLS_FOOTER_HTML + '\n        <div class="footer-links">')
    
    # 2. Fix H1/H2 Hierarchy
    # Ensure tool titles are in H1 if they are in H2 in some old templates
    # This is a bit risky to do blindly, but we can target specific patterns
    if "<h1></h1>" in content or "<h1>" not in content:
        # If no H1, try to find the first H2 and make it H1
        content = content.replace("<h2>", "<h1>", 1).replace("</h2>", "</h1>", 1)

    # 3. Add Alt Tags to Icons (Generic Fix)
    if 'class="card-icon"' in content and 'alt=' not in content:
         # Find common patterns and add alt if missing
         content = content.replace('class="card-icon">', 'class="card-icon" alt="ConvertRocket utility icon">')

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    print("Starting Global SEO Fix...")
    for html_file in FRONTEND_DIR.glob("*.html"):
        if html_file.name == "error.html": continue
        print(f"Fixing {html_file.name}...")
        update_html_seo(html_file)
    
    # Also fix blog files
    blog_dir = FRONTEND_DIR / "blog"
    if blog_dir.exists():
        for html_file in blog_dir.glob("*.html"):
            print(f"Fixing blog/{html_file.name}...")
            update_html_seo(html_file)

if __name__ == "__main__":
    main()

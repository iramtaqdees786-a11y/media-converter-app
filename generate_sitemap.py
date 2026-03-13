"""
XML Sitemap Generator for ConvertRocket
Generates SEO-optimized sitemap for Google Search Console
"""

import os
from datetime import datetime
from pathlib import Path

# Base URL
BASE_URL = "https://www.convertrocket.online"

# Page priorities and change frequencies
PAGES = [
    # Homepage - Highest priority
    {"url": "/", "priority": "1.0", "changefreq": "daily"},
    
    # Main hub pages
    {"url": "/all-tools", "priority": "0.9", "changefreq": "weekly"},
    {"url": "/media-hub", "priority": "0.9", "changefreq": "weekly"},
    {"url": "/pdf-lab", "priority": "0.9", "changefreq": "weekly"},
    {"url": "/dev-suite", "priority": "0.9", "changefreq": "weekly"},
    {"url": "/utilities", "priority": "0.9", "changefreq": "weekly"},
    {"url": "/ai-lab", "priority": "0.9", "changefreq": "weekly"},
    
    # Popular converters - High priority
    {"url": "/heic-to-jpg", "priority": "0.9", "changefreq": "weekly"},
    {"url": "/png-to-jpg", "priority": "0.9", "changefreq": "weekly"},
    {"url": "/webp-to-jpg", "priority": "0.9", "changefreq": "weekly"},
    {"url": "/pdf-to-word", "priority": "0.9", "changefreq": "weekly"},
    {"url": "/pdf-to-excel", "priority": "0.9", "changefreq": "weekly"},
    {"url": "/mp4-to-mp3", "priority": "0.9", "changefreq": "weekly"},
    {"url": "/downloader", "priority": "0.9", "changefreq": "weekly"},
    
    # Image converters
    {"url": "/jpg-to-png", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/jpg-to-pdf", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/jpg-to-webp", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/png-to-pdf", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/png-to-webp", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/webp-to-png", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/heic-to-png", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/bmp-to-jpg", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/bmp-to-png", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/tiff-to-jpg", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/tiff-to-png", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/gif-to-mp4", "priority": "0.8", "changefreq": "weekly"},
    
    # PDF tools
    {"url": "/pdf-compress", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/pdf-merge", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/pdf-to-text", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/pdf-to-txt", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/pdf-to-xlsx", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/pdf-remove-pages", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/pdf-grayscale", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/pdf-pdfa", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/word-to-pdf", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/excel-to-pdf", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/ppt-to-pdf", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/xlsx-to-pdf", "priority": "0.8", "changefreq": "weekly"},
    
    # Video converters
    {"url": "/video-converter", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/mp4-to-avi", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/mp4-to-mov", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/avi-to-mp4", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/mov-to-mp4", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/mkv-to-mp4", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/webm-to-mp4", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/flv-to-mp4", "priority": "0.8", "changefreq": "weekly"},
    
    # Audio converters
    {"url": "/mp3-converter", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/mp3-to-wav", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/wav-to-mp3", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/aac-to-mp3", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/flac-to-mp3", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/m4a-to-mp3", "priority": "0.8", "changefreq": "weekly"},
    
    # Media tools
    {"url": "/video-trimmer", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/image-converter", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/image-compress", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/exif-remover", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/yt-thumbnail", "priority": "0.8", "changefreq": "weekly"},
    
    # Downloaders
    {"url": "/tiktok-no-watermark", "priority": "0.8", "changefreq": "weekly"},
    {"url": "/insta-photo-down", "priority": "0.8", "changefreq": "weekly"},
    
    # Developer tools
    {"url": "/json-formatter", "priority": "0.7", "changefreq": "weekly"},
    {"url": "/base64-encoder", "priority": "0.7", "changefreq": "weekly"},
    {"url": "/qr-generator", "priority": "0.7", "changefreq": "weekly"},
    {"url": "/color-picker", "priority": "0.7", "changefreq": "weekly"},
    
    # AI tools
    {"url": "/ai-image-editor", "priority": "0.7", "changefreq": "weekly"},
    
    # Static pages
    {"url": "/blogs", "priority": "0.7", "changefreq": "weekly"},
    {"url": "/about", "priority": "0.5", "changefreq": "monthly"},
    {"url": "/contact", "priority": "0.5", "changefreq": "monthly"},
    {"url": "/privacy-policy", "priority": "0.3", "changefreq": "yearly"},
    {"url": "/terms-of-service", "priority": "0.3", "changefreq": "yearly"},
    {"url": "/sitemap", "priority": "0.3", "changefreq": "monthly"},
]

# Auto-detect HTML files in frontend directory
def auto_detect_pages(frontend_dir="frontend"):
    """Automatically detect HTML pages in frontend directory"""
    detected_pages = []
    
    if not os.path.exists(frontend_dir):
        return detected_pages
    
    for file in os.listdir(frontend_dir):
        if file.endswith('.html') and file not in ['sitemap.html']:
            url = f"/{file.replace('.html', '')}"
            
            # Skip if already in PAGES
            if any(p['url'] == url for p in PAGES):
                continue
            
            # Add with default priority
            detected_pages.append({
                "url": url,
                "priority": "0.7",
                "changefreq": "weekly"
            })
    
    return detected_pages

def generate_sitemap():
    """Generate XML sitemap"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Auto-detect additional pages
    auto_pages = auto_detect_pages()
    all_pages = PAGES + auto_pages
    
    # Sort by priority (highest first)
    all_pages.sort(key=lambda x: float(x['priority']), reverse=True)
    
    # Generate XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for page in all_pages:
        xml += '  <url>\n'
        xml += f'    <loc>{BASE_URL}{page["url"]}</loc>\n'
        xml += f'    <lastmod>{today}</lastmod>\n'
        xml += f'    <changefreq>{page["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{page["priority"]}</priority>\n'
        xml += '  </url>\n'
    
    xml += '</urlset>'
    
    return xml, len(all_pages)

def save_sitemap(xml, output_path="frontend/sitemap.xml"):
    """Save sitemap to file"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml)

def generate_robots_txt():
    """Generate robots.txt"""
    robots = f"""# ConvertRocket Robots.txt
# Optimized for maximum organic reach & engine cleanliness

User-agent: *
Allow: /
Disallow: /admin
Disallow: /api/internal
Disallow: /api/stats

# Sitemap
Sitemap: {BASE_URL}/sitemap.xml

# Crawl-delay for polite bots
Crawl-delay: 1
"""
    return robots

def save_robots_txt(robots, output_path="frontend/robots.txt"):
    """Save robots.txt to file"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(robots)

def main():
    """Generate sitemap and robots.txt"""
    print("Generating XML Sitemap...")
    print("=" * 60)
    
    # Generate sitemap
    xml, page_count = generate_sitemap()
    save_sitemap(xml)
    
    print(f"Sitemap generated: frontend/sitemap.xml")
    print(f"Total pages: {page_count}")
    print(f"URL: {BASE_URL}/sitemap.xml")
    print()
    
    # Generate robots.txt
    robots = generate_robots_txt()
    save_robots_txt(robots)
    
    print(f"Robots.txt generated: frontend/robots.txt")
    print(f"URL: {BASE_URL}/robots.txt")
    print()
    
    print("=" * 60)
    print("Sitemap generation complete!")
    print()
    print("Next Steps:")
    print("1. Verify sitemap at: https://www.xml-sitemaps.com/validate-xml-sitemap.html")
    print("2. Submit to Google Search Console:")
    print("   - Go to: https://search.google.com/search-console")
    print("   - Add property: convertrocket.online")
    print("   - Submit sitemap: /sitemap.xml")
    print("3. Monitor indexing status in Search Console")
    print()
    print("Page Breakdown:")
    
    # Count pages by priority
    priorities = {}
    for page in PAGES + auto_detect_pages():
        priority = page['priority']
        priorities[priority] = priorities.get(priority, 0) + 1
    
    for priority in sorted(priorities.keys(), reverse=True):
        count = priorities[priority]
        print(f"   Priority {priority}: {count} pages")

if __name__ == "__main__":
    main()

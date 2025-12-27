"""
Apply SEO hacks and Layout improvements to all HTML files.
"""
import os
import re
from pathlib import Path
from datetime import datetime

# SEO Hacks Content
LINK_CHUNKS = [
    '<link rel="stylesheet" href="/static/css/seo-hacks.css">',
    '<script src="/static/js/seo-hacks.js" defer></script>'
]

POWER_SILO_HTML = """
        <!-- POWER SILO (SEO Hack: Internal Linking) -->
        <div class="power-silo">
            <span class="power-silo-title">🔥 Trending:</span>
            <a href="/mp3-converter.html" class="power-silo-link">MP3 Converter</a>
            <a href="/pdf-tools.html" class="power-silo-link">PDF Tools</a>
            <a href="/video-converter.html" class="power-silo-link">Video Downloader</a>
            <a href="/blogs" class="power-silo-link">SEO Guides</a>
        </div>
"""

LAST_UPDATED_HTML = """
            <div class="last-updated-badge">
                <span>Last Updated: <span class="last-updated-date">[TODAY]</span></span>
            </div>
"""

def update_html_with_hacks(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Inject CSS/JS if not present
    for chunk in LINK_CHUNKS:
        if chunk not in content:
            content = content.replace('</head>', f'    {chunk}\n</head>')
    
    # 2. Inject Last Updated Badge in Header
    if '<div class="last-updated-badge">' not in content:
        # Try to find the header or free-label to place it after
        if '<div class="free-label">' in content:
            content = content.replace('<div class="free-label">', LAST_UPDATED_HTML + '            <div class="free-label">')
        elif '<header class="header">' in content:
            content = content.replace('<header class="header">', '<header class="header">\n' + LAST_UPDATED_HTML)

    # 3. Inject Power Silo links
    if 'class="power-silo"' not in content:
        # Place before tabs or first card
        if '</header>' in content:
            content = content.replace('</header>', '</header>\n' + POWER_SILO_HTML)
        elif '<main>' in content:
            content = content.replace('<main>', '<main>\n' + POWER_SILO_HTML)

    # 4. If it's a blog post, add a TL;DR box at the start of content
    if 'frontend/blog/' in str(file_path) and 'class="tldr-box"' not in content:
        # Find the first <p> in blog-content
        if '<div class="blog-content">' in content:
            tldr = '<div class="tldr-box"><p>Extract high-quality audio or convert files instantly with ConvertRocket. This guide shows you exactly how to optimize your media workflow using our 10x faster tools.</p></div>'
            content = content.replace('<div class="blog-content">', '<div class="blog-content">\n            ' + tldr)

    # 5. CTR Title Hack: Replace placeholders in title
    if '[MONTH_YEAR]' not in content:
        content = re.sub(r'<title>(.*?)</title>', r'<title>\1 ([MONTH_YEAR])</title>', content)
        content = re.sub(r'<h1(.*?)>(.*?)</h1>', r'<h1\1>\2 ([MONTH_YEAR])</h1>', content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Process all files
frontend_dir = Path('frontend')
html_files = list(frontend_dir.glob('*.html')) + list((frontend_dir / 'blog').glob('*.html'))

print(f"Applying SEO hacks to {len(html_files)} files...")
for html_file in html_files:
    try:
        update_html_with_hacks(html_file)
        print(f"✅ Enhanced: {html_file}")
    except Exception as e:
        print(f"❌ Failed {html_file}: {e}")

print("✨ All pages improved with SEO hacks and layout enhancements!")

"""
Update HTML files to use minified CSS and JS files
"""
import os
import re
from pathlib import Path

def update_html_file(file_path):
    """Update a single HTML file to use minified assets"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Replace CSS references
    content = re.sub(
        r'href="/static/css/styles\.css(\?v=[^"]*)?',
        r'href="/static/css/styles.min.css\1',
        content
    )
    content = re.sub(
        r'href="/static/css/mobile-optimizations\.css(\?v=[^"]*)?',
        r'href="/static/css/mobile-optimizations.min.css\1',
        content
    )
    content = re.sub(
        r'href="/static/css/styles-append\.css(\?v=[^"]*)?',
        r'href="/static/css/styles-append.min.css\1',
        content
    )
    
    # Replace JS references
    content = re.sub(
        r'src="/static/js/app\.js(\?v=[^"]*)?',
        r'src="/static/js/app.min.js\1',
        content
    )
    content = re.sub(
        r'src="/static/js/i18n\.js(\?v=[^"]*)?',
        r'src="/static/js/i18n.min.js\1',
        content
    )
    content = re.sub(
        r'src="/static/js/media-tools\.js(\?v=[^"]*)?',
        r'src="/static/js/media-tools.min.js\1',
        content
    )
    content = re.sub(
        r'src="/static/js/pdf-tools\.js(\?v=[^"]*)?',
        r'src="/static/js/pdf-tools.min.js\1',
        content
    )
    content = re.sub(
        r'src="/static/js/seo-hacks\.js(\?v=[^"]*)?',
        r'src="/static/js/seo-hacks.min.js\1',
        content
    )
    content = re.sub(
        r'href="/static/css/seo-hacks\.css(\?v=[^"]*)?',
        r'href="/static/css/seo-hacks.min.css\1',
        content
    )

    # Make internal links friendly (remove .html extension)
    # Only for local routes, not external links
    content = re.sub(
        r'href="/([^"]+)\.html"',
        r'href="/\1"',
        content
    )
    
    # Special case for index.html as /
    content = content.replace('href="/index"', 'href="/"')
    
    # Only write if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Find all HTML files in frontend directory
frontend_dir = Path('frontend')
html_files = []

# Get HTML files from root
html_files.extend(frontend_dir.glob('*.html'))

# Get HTML files from blog directory
blog_dir = frontend_dir / 'blog'
if blog_dir.exists():
    html_files.extend(blog_dir.glob('*.html'))

updated_count = 0
for html_file in html_files:
    if update_html_file(html_file):
        print(f"Updated: {html_file}")
        updated_count += 1
    else:
        print(f"  Skipped: {html_file} (no changes needed)")

print(f"\nDONE: Updated {updated_count} HTML files to use minified assets!")

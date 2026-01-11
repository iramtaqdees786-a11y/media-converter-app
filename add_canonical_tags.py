"""
Add canonical tags to all HTML files for SEO
This fixes duplicate content issues in Google Search Console
"""

import os
from pathlib import Path
import re

def add_canonical_tag(html_path: Path):
    """Add canonical tag to HTML file if it doesn't exist"""
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has canonical tag
    if 'rel="canonical"' in content:
        print(f"✓ {html_path.name} already has canonical tag")
        return False
    
    # Generate canonical URL from filename
    filename = html_path.name
    if filename == 'index.html':
        canonical_url = 'https://www.convertrocket.online/'
    else:
        page_name = filename.replace('.html', '')
        canonical_url = f'https://www.convertrocket.online/{page_name}'
    
    # Find the </head> tag and insert canonical before it
    canonical_tag = f'    <link rel="canonical" href="{canonical_url}">\n'
    
    if '</head>' in content:
        content = content.replace('</head>', f'{canonical_tag}</head>')
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Added canonical tag to {html_path.name}: {canonical_url}")
        return True
    else:
        print(f"✗ No </head> tag found in {html_path.name}")
        return False

def main():
    frontend_dir = Path(__file__).parent / 'frontend'
    
    print("=" * 60)
    print("Adding Canonical Tags for SEO")
    print("=" * 60)
    
    # Process all HTML files in frontend root
    html_files = list(frontend_dir.glob('*.html'))
    updated_count = 0
    
    for html_file in html_files:
        if add_canonical_tag(html_file):
            updated_count += 1
    
    # Process blog files
    blog_dir = frontend_dir / 'blog'
    if blog_dir.exists():
        print("\n" + "=" * 60)
        print("Processing Blog Posts")
        print("=" * 60)
        
        for blog_file in blog_dir.glob('*.html'):
            # Blog canonical URLs
            with open(blog_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'rel="canonical"' not in content:
                blog_slug = blog_file.name.replace('.html', '')
                canonical_url = f'https://www.convertrocket.online/blog/{blog_slug}'
                canonical_tag = f'    <link rel="canonical" href="{canonical_url}">\n'
                
                if '</head>' in content:
                    content = content.replace('</head>', f'{canonical_tag}</head>')
                    
                    with open(blog_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"✓ Added canonical tag to {blog_file.name}")
                    updated_count += 1
    
    print("\n" + "=" * 60)
    print(f"✓ Complete! Updated {updated_count} files with canonical tags")
    print("=" * 60)

if __name__ == '__main__':
    main()

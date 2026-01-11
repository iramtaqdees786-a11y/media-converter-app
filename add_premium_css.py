"""
Add premium-effects.css to all HTML files
"""

import os
from pathlib import Path

def add_premium_css_link(html_path: Path):
    """Add premium-effects.css link if not present"""
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has premium-effects.css
    if 'premium-effects.css' in content:
        print(f"✓ {html_path.name} already has premium-effects.css")
        return False
    
    # Find ultra-minimalist.css and add premium-effects.css after it
    premium_link = '    <link rel="stylesheet" href="/css/premium-effects.css">\n'
    
    if 'ultra-minimalist.css' in content:
        # Add after ultra-minimalist.css
        content = content.replace(
            'ultra-minimalist.css?v=4.0">',
            'ultra-minimalist.css?v=4.0">\n' + premium_link.strip()
        )
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Added premium-effects.css to {html_path.name}")
        return True
    elif '</head>' in content:
        # Add before closing head tag
        content = content.replace('</head>', f'{premium_link}</head>')
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Added premium-effects.css to {html_path.name} (before </head>)")
        return True
    else:
        print(f"✗ Could not add to {html_path.name}")
        return False

def main():
    frontend_dir = Path(__file__).parent / 'frontend'
    
    print("=" * 60)
    print("Adding Premium Effects CSS to All HTML Files")
    print("=" * 60)
    
    updated_count = 0
    
    # Process all HTML files except index.html (already done)
    html_files = [f for f in frontend_dir.glob('*.html') if f.name != 'index.html']
    
    for html_file in html_files:
        if add_premium_css_link(html_file):
            updated_count += 1
    
    # Process blog files
    blog_dir = frontend_dir / 'blog'
    if blog_dir.exists():
        print("\n" + "=" * 60)
        print("Processing Blog Posts")
        print("=" * 60)
        
        for blog_file in blog_dir.glob('*.html'):
            if add_premium_css_link(blog_file):
                updated_count += 1
    
    print("\n" + "=" * 60)
    print(f"✓ Complete! Updated {updated_count} files")
    print("=" * 60)

if __name__ == '__main__':
    main()

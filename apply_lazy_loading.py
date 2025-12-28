import os
import re
from pathlib import Path

def add_lazy_loading(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # regex to find images without loading="lazy"
    # and add it.
    original_content = content
    
    # find images that don't have loading="lazy" or loading='lazy'
    images = re.findall(r'<img[^>]+>', content)
    for img in images:
        if 'loading=' not in img:
            new_img = img.replace('>', ' loading="lazy">')
            content = content.replace(img, new_img)
            
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

frontend_dir = Path('frontend')
html_files = list(frontend_dir.glob('**/*.html'))

updated = 0
for html_file in html_files:
    if add_lazy_loading(html_file):
        print(f"Lazy loaded images in: {html_file}")
        updated += 1

print(f"Finished. Updated {updated} files.")

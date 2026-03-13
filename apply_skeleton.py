import os
import glob
import re

frontend_dir = r'c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend'
html_files = glob.glob(os.path.join(frontend_dir, '**/*.html'), recursive=True)

def apply_skeleton(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False
    
    # Add skeleton-loading class to main containers
    # Targets: bento-card, upload-zone, form-container
    targets = ['bento-card', 'upload-zone', 'form-container', 'bento-grid']
    for target in targets:
        # Avoid double adding
        if f'class="{target}"' in content and 'skeleton-loading' not in content:
            content = content.replace(f'class="{target}"', f'class="{target} skeleton-loading"')
            changed = True
        elif f"class='{target}'" in content and 'skeleton-loading' not in content:
            content = content.replace(f"class='{target}'", f"class='{target} skeleton-loading'")
            changed = True

    if changed:
        # Add a small script to remove the skeleton class once the main JS initializes
        if 'document.addEventListener(\'DOMContentLoaded\'' in content and 'skeleton-loading' not in content:
             # Find DOMContentLoaded and add cleanup
             content = content.replace(
                 'document.addEventListener(\'DOMContentLoaded\', () => {',
                 'document.addEventListener(\'DOMContentLoaded\', () => {\n            setTimeout(() => { document.querySelectorAll(\'.skeleton-loading\').forEach(el => el.classList.remove(\'skeleton-loading\')); }, 1500);'
             )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Run the application
count = 0
for file in html_files:
    if apply_skeleton(file):
        count += 1

print(f"Applied skeleton-loading to {count} pages.")

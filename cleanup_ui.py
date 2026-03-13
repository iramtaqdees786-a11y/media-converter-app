import os
import glob
import re

frontend_dir = r'c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend'
html_files = glob.glob(os.path.join(frontend_dir, '**/*.html'), recursive=True)

def fix_double_style(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False
    
    # Fix the specific double style issue created previously
    # <p style="color: var(--text-secondary); margin-bottom: 30px;" style="padding-left: 20px; color: var(--text-secondary);">
    if 'style="color: var(--text-secondary); margin-bottom: 30px;" style="padding-left: 20px; color: var(--text-secondary);"' in content:
        content = content.replace(
            'style="color: var(--text-secondary); margin-bottom: 30px;" style="padding-left: 20px; color: var(--text-secondary);"',
            'style="padding-left: 20px; color: var(--text-secondary); margin-bottom: 30px;"'
        )
        changed = True

    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Run the fix
for file in html_files:
    if fix_double_style(file):
        print(f"Fixed double style: {os.path.relpath(file, frontend_dir)}")

# 2. Delete yt-thumbnail.html
thumbnail_path = os.path.join(frontend_dir, 'yt-thumbnail.html')
if os.path.exists(thumbnail_path):
    os.remove(thumbnail_path)
    print("Deleted frontend/yt-thumbnail.html")

print("Cleanup complete.")

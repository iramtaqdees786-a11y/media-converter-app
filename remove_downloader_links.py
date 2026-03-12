import os
import glob

html_files = glob.glob(r'c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend\*.html')

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove simple downloader link
    content = content.replace('<a href="/downloader" class="cat-link"><span class="icon">⬇️</span> Downloader</a>', '')
    content = content.replace('<a href="/downloader" style="margin-left: 20px;">Downloader</a>', '')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Processed {len(html_files)} files to remove downloader links.")

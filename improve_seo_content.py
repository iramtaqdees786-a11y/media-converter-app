import os
import re

frontend_dir = r"c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend"

# SEO-Friendly Replacements for Technical Jargon
SEO_REPLACEMENTS = {
    r"Technical Dossier: Acoustic-Isolation": "Free MP4 to MP3 Converter Online",
    r"Technical Dossier: Temporal-Sync": "Fast Video Trimmer & Slicer",
    r"Technical Dossier: Cloud-transcode": "High-Quality Video Downloader & Converter",
    r"Technical Dossier: Pixel-Matrix": "Professional Image Converter & Editor",
    r"Technical Dossier: Neural-Dossier": "Secure PDF Tools & Editor",
    
    r"Neural Extraction": "Convert Video to MP3",
    r"Industrial Clipping": "Trim Video Online",
    r"Industrial Media Scan": "Download HD Videos",
    r"Dossier Fusion": "Merge PDF Files",
    r"Volume Reducer": "Compress PDF Online",
    
    r"Zero-telemetry architecture": "100% Private and Secure",
    r"volatile RAM buffers": "safe cloud processing",
    r"cryptographically wiped": "deleted permanently",
    r"temporal sharding buffer": "secure temporary storage",
    r"Bit-perfect neural audio extraction": "High-quality audio extraction for free",
    r"Lossless frame-accurate clipping": "Trim videos without losing quality",
    r"sharded cloud proxies": "high-speed secure servers",
    r"Acoustic Isolation Module": "Audio Extractor Pro",
    r"Precision Media Engine": "Video Utility Lab",
    r"Unified Media Protocol": "Universal Media Studio",
}

def improve_seo(content):
    new_content = content
    for tech, seo in SEO_REPLACEMENTS.items():
        new_content = re.sub(tech, seo, new_content, flags=re.IGNORECASE)
    
    # Also fix the general "Dossier" usage which sounds too "spy-like" for normal SEO
    new_content = re.sub(r"Dossier", "File", new_content)
    new_content = re.sub(r"dossier", "file", new_content)
    
    # Improve the "telemetry" cards specifically if they follow the standard pattern
    telemetry_pattern = r'\[0x03\] Cryptographic Purge</h3>\s*<p[^>]*>Zero-telemetry architecture\..*?</p>'
    telemetry_replacement = '[0x03] Maximum Privacy</h3><p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6;">100% Private and Secure. Your files are processed in real-time and deleted immediately after use, ensuring your data remains safe and protected.</p>'
    new_content = re.sub(telemetry_pattern, telemetry_replacement, new_content, flags=re.DOTALL)
    
    # Fix links (hyperlinks look bad)
    # Add a global style to the head if missing, or update existing link styles
    link_style_fix = """
    <style>
        a { transition: all 0.3s ease; }
        .seo-content a { color: var(--accent-primary); text-decoration: none; border-bottom: 1px solid transparent; }
        .seo-content a:hover { border-bottom: 1px solid var(--accent-primary); opacity: 0.8; }
        footer a { opacity: 0.7; text-decoration: none !important; }
        footer a:hover { opacity: 1; color: var(--accent-primary) !important; }
    </style>
    """
    if "</head>" in new_content and "<style>" not in new_content:
        new_content = new_content.replace("</head>", link_style_fix + "\n</head>")

    return new_content

def main():
    count = 0
    for root, dirs, files in os.walk(frontend_dir):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = improve_seo(content)
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    count += 1
    print(f"Improved SEO content in {count} files.")

if __name__ == "__main__":
    main()

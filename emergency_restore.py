import os

# Configuration
FRONTEND_DIR = r"c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend"

def emergency_restore(filepath):
    if not filepath.endswith((".html", ".js", ".css")):
        return

    try:
        # Read as bytes first to avoid encoding issues during detection
        with open(filepath, 'rb') as f:
            content_bytes = f.read()
        
        # dYs? in bytes (if it's literal string)
        # However, it might be mangled representation of a character.
        # Let's try to read as utf-8 with replacement and see what we get.
        content = content_bytes.decode('utf-8', errors='replace')
        
        if 'dYs?' in content:
            print(f"Purging garbage from: {os.path.basename(filepath)}")
            # Specifically remove the 'dYs?' string
            content = content.replace('dYs?', '')
            # Also common mangles like the null-ish character surrogate
            content = content.replace('\ufffd', '')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
    except Exception as e:
        print(f"Error restoring {filepath}: {e}")

def main():
    for root, dirs, files in os.walk(FRONTEND_DIR):
        for file in files:
            emergency_restore(os.path.join(root, file))

if __name__ == "__main__":
    main()

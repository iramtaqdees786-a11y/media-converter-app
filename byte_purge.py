import os

# Configuration
FRONTEND_DIR = r"c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend"
ROCKET_BYTES = b'\xf0\x9f\x9a\x80'

def byte_purge(filepath):
    if not filepath.endswith((".html", ".js", ".css")):
        return

    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        if ROCKET_BYTES in content:
            print(f"Purging interstitial bytes from: {os.path.basename(filepath)}")
            # We must be careful not to remove REAL rocket emojis if they were intended.
            # However, the corruption is so severe (one after every char) that removing all is safest,
            # then we can put back the brand ones if needed.
            # A simple .replace(ROCKET_BYTES, b'') should work.
            new_content = content.replace(ROCKET_BYTES, b'')
            
            with open(filepath, 'wb') as f:
                f.write(new_content)
                
    except Exception as e:
        print(f"Error purging {filepath}: {e}")

def main():
    for root, dirs, files in os.walk(FRONTEND_DIR):
        for file in files:
            byte_purge(os.path.join(root, file))

if __name__ == "__main__":
    main()

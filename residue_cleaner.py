import os

# Configuration
FRONTEND_DIR = r"c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend"

# Precise residues to purge/fix
# We replace mangled patterns with their intended literal symbols
REPLACEMENTS = {
    'dY",': '🔄',
    'dY" ': '📤',
    'dY-o,?': '🗜️',
    '-?': '★',
    '+\'': '→',
    '? ,?': '❤️',
    '+': '⭐',
    '': '', # Generic fallthrough
}

def clean_residue(filepath):
    if not filepath.endswith((".html", ".js", ".css")):
        return

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        original_content = content
        for mangled, fixed in REPLACEMENTS.items():
            if mangled in content:
                content = content.replace(mangled, fixed)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Cleaned residues in: {os.path.basename(filepath)}")
            
    except Exception as e:
        print(f"Error cleaning {filepath}: {e}")

def main():
    for root, dirs, files in os.walk(FRONTEND_DIR):
        for file in files:
            clean_residue(os.path.join(root, file))

if __name__ == "__main__":
    main()

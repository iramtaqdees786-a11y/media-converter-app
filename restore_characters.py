import os
from pathlib import Path

# Configuration
PROJECT_ROOT = r"c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app"
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")

# Replacements to UNDO
RESTORATIONS = {
    '⭐': '+',
    '★': '-',
    # '→': "+'", # This one is risky, let's see if it's actually in code
}

def restore_characters(filepath):
    if not filepath.endswith((".html", ".js", ".css")):
        return

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        original_content = content
        for emoji, original in RESTORATIONS.items():
            if emoji in content:
                # Special case for app.js where we saw ⭐ used as +
                content = content.replace(emoji, original)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Restored characters in: {os.path.relpath(filepath, PROJECT_ROOT)}")
            
    except Exception as e:
        print(f"Error restoring {filepath}: {e}")

def main():
    for root, dirs, files in os.walk(FRONTEND_DIR):
        for file in files:
            restore_characters(os.path.join(root, file))

if __name__ == "__main__":
    main()

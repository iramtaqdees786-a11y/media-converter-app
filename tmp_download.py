import requests
import os

# Trying esm.sh which is often more robust for module-based packages
url = "https://esm.sh/@imgly/background-removal"
target_dir = "frontend/js/libs"
target_file = os.path.join(target_dir, "background-removal.js")

try:
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    
    print(f"Fetching from {url}...")
    # Follow redirects for esm.sh
    response = requests.get(url, timeout=20, allow_redirects=True)
    response.raise_for_status()
    
    with open(target_file, "wb") as f:
        f.write(response.content)
    
    print(f"Successfully cached library to {target_file}")
except Exception as e:
    print(f"Final Fallback Failed: {e}")
    # Create a stub to prevent 404 and provide console feedback
    with open(target_file, "w") as f:
        f.write("console.warn('AI Background Removal Engine Failed to Load from CDN. Please check proxy/firewall settings.');")

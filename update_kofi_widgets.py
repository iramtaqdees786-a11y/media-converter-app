import os
import glob
import re

frontend_dir = r'c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend'
html_files = glob.glob(os.path.join(frontend_dir, '**/*.html'), recursive=True)

floating_widget_code = """
    <!-- Ko-fi Floating Widget -->
    <script src='https://storage.ko-fi.com/cdn/scripts/overlay-widget.js'></script>
    <script>
      kofiWidgetOverlay.draw('izyaan', {
        'type': 'floating-chat',
        'floating-chat.donateButton.text': 'Support me',
        'floating-chat.donateButton.background-color': '#794bc4',
        'floating-chat.donateButton.text-color': '#fff',
        'floating-chat.donateButton.position': 'Right'
      });
    </script>
"""

for file_path in html_files:
    # Skip folders that aren't part of the main app or blog
    if 'temp_repo' in file_path or '.git' in file_path:
        continue

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        # 1. Clean up old combined injections or top widgets
        old_patterns = [
            r"(?s)<!-- Ko-fi Widgets -->.*?kofiwidget2\.draw\(\);</script>",
            r"(?s)<!-- Ko-fi Top Widget -->.*?kofiwidget2\.draw\(\);</div>"
        ]
        for pattern in old_patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, "", content)
                changed = True
            
        # 2. Add Floating Widget before </body>
        if "<!-- Ko-fi Floating Widget -->" not in content and "</body>" in content:
            content = content.replace("</body>", floating_widget_code + "</body>")
            changed = True

        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated widgets in: {os.path.relpath(file_path, frontend_dir)}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print("Ko-fi widget cleanup and floating widget injection complete.")

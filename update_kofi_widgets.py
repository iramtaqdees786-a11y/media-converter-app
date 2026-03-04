import os
import glob
import re

frontend_dir = r'c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend'
html_files = glob.glob(os.path.join(frontend_dir, '**/*.html'), recursive=True)

top_widget_code = """
    <!-- Ko-fi Top Widget -->
    <div style="display:flex; justify-content:center; margin-top: 10px; margin-bottom: 10px; z-index: 1000; position: relative;">
        <script type='text/javascript' src='https://storage.ko-fi.com/cdn/widget/Widget_2.js'></script>
        <script type='text/javascript'>kofiwidget2.init('Fuel the Chaos 🔥', '#9a93f5', 'Q5Q81VCPM3');kofiwidget2.draw();</script>
    </div>
"""

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
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        # 1. Clean up old combined injections if they exist
        old_pattern = r"(?s)<!-- Ko-fi Widgets -->.*?kofiwidget2\.draw\(\);</script>"
        if re.search(old_pattern, content):
            content = re.sub(old_pattern, "", content)
            changed = True
            
        # 2. Add Top Widget after <body> tag
        if "<!-- Ko-fi Top Widget -->" not in content and "<body" in content:
            # find first <body... > tag and inject right after it
            content = re.sub(r'(<body[^>]*>)', r'\1' + top_widget_code, content, count=1)
            changed = True
            
        # 3. Add Floating Widget before </body>
        if "<!-- Ko-fi Floating Widget -->" not in content and "</body>" in content:
            content = content.replace("</body>", floating_widget_code + "</body>")
            changed = True

        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated widgets in: {os.path.relpath(file_path, frontend_dir)}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print("Ko-fi widget relocation complete.")

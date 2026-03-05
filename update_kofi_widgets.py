import os
import glob
import re

frontend_dir = r'c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend'
html_files = glob.glob(os.path.join(frontend_dir, '**/*.html'), recursive=True)

# Ko-fi Floating Widget with Custom Hover Content
floating_widget_code = """
    <!-- Ko-fi Floating Widget -->
    <style>
      /* Custom Hover Content Box for the Tip Widget */
      .kofi-hover-box {
        position: fixed;
        bottom: 90px;
        right: 20px;
        background: #fff;
        color: #333;
        padding: 12px 16px;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        max-width: 200px;
        z-index: 10000;
        opacity: 0;
        transform: translateY(10px);
        transition: all 0.3s ease;
        pointer-events: none;
        border: 1px solid rgba(121, 75, 196, 0.2);
      }
      .kofi-hover-box::after {
        content: '';
        position: absolute;
        bottom: -8px;
        right: 24px;
        border-left: 8px solid transparent;
        border-right: 8px solid transparent;
        border-top: 8px solid #fff;
      }
      /* Trigger hover on the Ko-fi container */
      .floatingchat-container:hover ~ .kofi-hover-box,
      .kofichat-container:hover ~ .kofi-hover-box {
        opacity: 1;
        transform: translateY(0);
      }
    </style>
    <script src='https://storage.ko-fi.com/cdn/scripts/overlay-widget.js'></script>
    <script>
      kofiWidgetOverlay.draw('izyaan', {
        'type': 'floating-chat',
        'floating-chat.donateButton.text': 'Support me',
        'floating-chat.donateButton.background-color': '#794bc4',
        'floating-chat.donateButton.text-color': '#fff',
        'floating-chat.donateButton.position': 'Right'
      });
      // Add the hover box to the body
      document.addEventListener('DOMContentLoaded', () => {
        const hb = document.createElement('div');
        hb.className = 'kofi-hover-box';
        hb.innerHTML = '<strong>Fuel the Lab! 🚀</strong><br>Tips help keep our conversion servers fast and ad-free.';
        document.body.appendChild(hb);
      });
    </script>
    <!-- /Ko-fi Floating Widget -->
"""

for file_path in html_files:
    # Skip folders that aren't part of the main app or blog
    if 'temp_repo' in file_path or '.git' in file_path:
        continue

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        # 1. Clean up ALL legacy or duplicated Ko-fi parts (STRICT SCOPE)
        old_patterns = [
            r"(?s)<!-- Ko-fi Widgets -->.*?kofiwidget2\.draw\(\);</script>",
            r"(?s)<!-- Ko-fi Top Widget -->.*?kofiwidget2\.draw\(\);</div>",
            r"(?s)<!-- Ko-fi Floating Widget -->.*?<!-- /Ko-fi Floating Widget -->", # Catch tagged floating widget (if we use end tag)
            r"(?s)<!-- Ko-fi Floating Widget -->.*?</script>", # Catch legacy floating widget
            r"(?s)<style>\s*/\* Custom Hover Content Box for the Tip Widget \*/.*?\.kofi-hover-box.*?</style>", # Strict style scope
            r"(?s)<script src='https://storage\.ko-fi\.com/cdn/scripts/overlay-widget\.js'></script>" # Catch library loader
        ]
        for pattern in old_patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, "", content)
                changed = True
            
        # 2. Cleanup redundant comment markers from previous runs
        if "<!-- Protocol Foundation Support -->" in content:
            content = re.sub(r'(<!-- Protocol Foundation Support -->\s*)+', "<!-- Protocol Foundation Support -->\n    ", content)
            changed = True

        # 3. Add Floating Widget before </body>
        if "</body>" in content:
            content = content.replace("</body>", "\n" + floating_widget_code + "\n</body>")
            changed = True

        if changed:
            # Final touch: remove triple/quadruple newlines
            content = re.sub(r'\n{3,}', '\n\n', content)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated widgets in: {os.path.relpath(file_path, frontend_dir)}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print("Ko-fi widget cleanup and floating widget injection complete.")

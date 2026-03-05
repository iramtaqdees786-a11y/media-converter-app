import os
import glob
import re

frontend_dir = r'c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend'
html_files = glob.glob(os.path.join(frontend_dir, '**/*.html'), recursive=True)

# Ko-fi Floating Widget with Interactive Context Box (Rocket Loader bypass)
floating_widget_code = """
    <!-- Ko-fi Floating Widget -->
    <style>
      /* Custom Interactive Box for the Tip Widget */
      .kofi-hover-box {
        position: fixed;
        bottom: 90px;
        right: 20px;
        background: #fff;
        color: #333;
        padding: 16px;
        border-radius: 16px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.25);
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        max-width: 240px;
        z-index: 10000;
        opacity: 0;
        transform: translateY(10px);
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        pointer-events: none;
        border: 1px solid rgba(121, 75, 196, 0.15);
      }
      .kofi-hover-box.active {
        opacity: 1;
        transform: translateY(0);
        pointer-events: auto;
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
      .kofi-hover-box strong { color: #794bc4; display: block; margin-bottom: 4px; }
      .kofi-btn-mini {
          display: inline-block;
          margin-top: 10px;
          background: #794bc4;
          color: #fff !important;
          padding: 6px 12px;
          border-radius: 8px;
          text-decoration: none;
          font-weight: 700;
          font-size: 0.8rem;
          transition: transform 0.2s;
      }
      .kofi-btn-mini:hover { transform: scale(1.05); }
      
      /* Trigger hover on the Ko-fi container */
      .floatingchat-container:hover ~ .kofi-hover-box,
      .kofichat-container:hover ~ .kofi-hover-box,
      .kofi-hover-box:hover {
        opacity: 1 !important;
        transform: translateY(0) !important;
        pointer-events: auto !important;
      }
    </style>
    <script data-cfasync="false" src='https://storage.ko-fi.com/cdn/scripts/overlay-widget.js'></script>
    <script data-cfasync="false">
      function initKofi() {
        if (typeof kofiWidgetOverlay !== 'undefined') {
          kofiWidgetOverlay.draw('izyaan', {
            'type': 'floating-chat',
            'floating-chat.donateButton.text': 'Support me',
            'floating-chat.donateButton.background-color': '#794bc4',
            'floating-chat.donateButton.text-color': '#fff',
            'floating-chat.donateButton.position': 'Right'
          });
          
          // Add the interactive box once drawn
          const hb = document.createElement('div');
          hb.className = 'kofi-hover-box';
          hb.innerHTML = '<strong>Fuel the Lab! 🚀</strong>Tips help us stay ad-free and keep our high-speed conversion servers running for everyone. <br><a href="https://ko-fi.com/izyaan" target="_blank" class="kofi-btn-mini">Tip Now</a>';
          document.body.appendChild(hb);
        } else {
          setTimeout(initKofi, 150);
        }
      }
      if (document.readyState === 'complete') {
        initKofi();
      } else {
        window.addEventListener('load', initKofi);
      }
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
            r"(?s)<!-- Ko-fi Floating Widget -->.*?<!-- /Ko-fi Floating Widget -->",
            r"(?s)<!-- Ko-fi Floating Widget -->.*?</script>",
            r"(?s)<style>\s*/\* Custom Hover Content Box for the Tip Widget \*/.*?\.kofi-hover-box.*?</style>",
            r"(?s)<style>\s*/\* Custom Interactive Box for the Tip Widget \*/.*?\.kofi-hover-box.*?</style>",
            r"(?s)<script data-cfasync=\"false\" src='https://storage\.ko-fi\.com/cdn/scripts/overlay-widget\.js'></script>",
            r"(?s)<script src='https://storage\.ko-fi\.com/cdn/scripts/overlay-widget\.js'></script>",
            r"(?s)<script type='text/javascript' src='https://storage\.ko-fi\.com/cdn/widget/Widget_2\.js'></script>",
            r"(?s)<script type='text/javascript'>\s*kofiwidget2\.init\(.*?\);\s*kofiwidget2\.draw\(.*?\);\s*</script>",
            r"(?s)<script>\s*kofiWidgetOverlay\.draw\(.*?\);\s*</script>", # Catch rogue scripts
            r"(?s)<!-- Blended Hero Support -->.*?</div>",
            r"(?s)<!-- Protocol Foundation Support -->.*? Fuel the Chaos.*?/section>", # Catch main section (Tip Panel)
            r"(?s)<section class=\"foundation-bridge\".*?Fuel the Chaos.*?/section>" # Catch main section
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

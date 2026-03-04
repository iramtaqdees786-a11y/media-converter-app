import os
import glob

frontend_dir = r'c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend'
html_files = glob.glob(os.path.join(frontend_dir, '**/*.html'), recursive=True)

head_injection = """
    <!-- Microsoft Clarity -->
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){
            c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        })(window, document, "clarity", "script", "vqfspxq9e7");
    </script>
"""

body_injection = """
    <!-- Ko-fi Widgets -->
    <script src='https://storage.ko-fi.com/cdn/scripts/overlay-widget.js'></script>
    <script>
      kofiWidgetOverlay.draw('izyaan', {
        'type': 'floating-chat',
        'floating-chat.donateButton.text': 'Support me',
        'floating-chat.donateButton.background-color': '#794bc4',
        'floating-chat.donateButton.text-color': '#fff'
      });
    </script>
    <script type='text/javascript' src='https://storage.ko-fi.com/cdn/widget/Widget_2.js'></script>
    <script type='text/javascript'>kofiwidget2.init('Fuel the Chaos 🔥', '#9a93f5', 'Q5Q81VCPM3');kofiwidget2.draw();</script>
"""

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        if 'vqfspxq9e7' not in content and '</head>' in content:
            content = content.replace('</head>', head_injection + '</head>')
            changed = True
            
        if 'kofiWidgetOverlay' not in content and '</body>' in content:
            content = content.replace('</body>', body_injection + '</body>')
            changed = True

        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Injected scripts into: {os.path.relpath(file_path, frontend_dir)}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print(f"Completed processing {len(html_files)} files.")

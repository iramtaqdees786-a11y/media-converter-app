import os
import glob
import re

frontend_dir = r'c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend'
html_files = glob.glob(os.path.join(frontend_dir, '**/*.html'), recursive=True)

# Premium Support Section HTML (Adblock-friendly names)
tip_section_code = """
    <!-- Protocol Foundation Support -->
    <section class="foundation-bridge" style="margin-top: 80px; margin-bottom: 40px; padding: 20px;">
        <div class="container" style="max-width: 800px; margin: 0 auto;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h2 style="font-size: 2.5rem; background: linear-gradient(135deg, #9a93f5, #794bc4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 15px;">Fuel the Chaos 🔥</h2>
                <p style="color: var(--text-secondary); font-size: 1.1rem;">Support the development of ConvertRocket's edge-case laboratory. Your contributions keep the servers running and the algorithms sharp.</p>
            </div>
            
            <div class="foundation-hub" style="
                background: #ffffff;
                border-radius: 24px;
                padding: 10px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.4), 0 0 20px rgba(121, 75, 196, 0.1);
                overflow: hidden;
                min-height: 720px;
                display: flex;
                justify-content: center;
                align-items: center;
            ">
                <iframe src='https://ko-fi.com/izyaan/?hidefeed=true&widget=true&embed=true' 
                    style='border:none; width:100%; border-radius: 14px; background: #ffffff;' 
                    height='712' title='izyaan'></iframe>
            </div>
            
            <div style="text-align: center; margin-top: 25px; opacity: 0.6; font-size: 0.85rem; color: var(--text-secondary);">
                Securely processed via Ko-fi. No data is stored on ConvertRocket servers.
            </div>
        </div>
    </section>
"""

# We'll inject this right before the footer
footer_marker = '<footer'

for file_path in html_files:
    if 'temp_repo' in file_path or '.git' in file_path:
        continue

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # NUCLEAR CLEANUP: Remove ANY section that looks like a Ko-fi support block
        # We search for several markers including the <iframe> to izyaan or the "Fuel the Chaos" text
        patterns_to_remove = [
            r'(?s)<!-- Premium Support Section -->.*?<div style="text-align: center; margin-top: 25px; opacity: 0.6; font-size: 0.85rem; color: var(--text-secondary);">.*?</div>.*?</div>\s*</section>',
            r'(?s)<!-- Protocol Foundation Support -->.*?<div style="text-align: center; margin-top: 25px; opacity: 0.6; font-size: 0.85rem; color: var(--text-secondary);">.*?</div>.*?</div>\s*</section>',
            r'(?s)<section class="support-chaos".*?Fuel the Chaos.*?/section>',
            r'(?s)<section class="foundation-bridge".*?Fuel the Chaos.*?/section>'
        ]
        
        orig_content = content
        for pattern in patterns_to_remove:
            content = re.sub(pattern, "", content)
        
        changed = (content != orig_content)

        if footer_marker in content:
            content = content.replace(footer_marker, tip_section_code + "\n    " + footer_marker)
            changed = True
        elif "</body>" in content:
            content = content.replace("</body>", tip_section_code + "\n</body>")
            changed = True

        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Sanitized Support Section in: {os.path.relpath(file_path, frontend_dir)}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print("Site-wide support section sanitization complete.")

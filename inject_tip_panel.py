import os
import glob
import re

frontend_dir = r'c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend'
html_files = glob.glob(os.path.join(frontend_dir, '**/*.html'), recursive=True)

# Premium Support Section HTML
# We use a glassmorphic container with a subtle glow
tip_section_code = """
    <!-- Premium Support Section -->
    <section class="support-chaos" style="margin-top: 80px; margin-bottom: 40px; padding: 20px;">
        <div class="container" style="max-width: 800px; margin: 0 auto;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h2 style="font-size: 2.5rem; background: linear-gradient(135deg, #9a93f5, #794bc4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 15px;">Fuel the Chaos 🔥</h2>
                <p style="color: var(--text-secondary); font-size: 1.1rem;">Support the development of ConvertRocket's edge-case laboratory. Your contributions keep the servers running and the algorithms sharp.</p>
            </div>
            
            <div class="glass-card" style="
                background: rgba(255, 255, 255, 0.03);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 24px;
                padding: 10px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.4), 0 0 20px rgba(121, 75, 196, 0.1);
                overflow: hidden;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            ">
                <iframe id='kofiframe' src='https://ko-fi.com/izyaan/?hidefeed=true&widget=true&embed=true&preview=true' 
                    style='border:none; width:100%; border-radius: 14px; background: rgba(255,255,255,0.02);' 
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
    # Skip folders that aren't part of the main app or blog
    if 'temp_repo' in file_path or '.git' in file_path:
        continue

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if "<!-- Premium Support Section -->" in content:
            continue

        if footer_marker in content:
            # Inject before the footer
            new_content = content.replace(footer_marker, tip_section_code + "\n    " + footer_marker)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Injected Tip Panel into: {os.path.relpath(file_path, frontend_dir)}")
        elif "</body>" in content:
            # Inject before closing body tag as fallback
            new_content = content.replace("</body>", tip_section_code + "\n</body>")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Injected Tip Panel into (fallback): {os.path.relpath(file_path, frontend_dir)}")
        else:
            print(f"Skipping {file_path}: No footer or body tag found.")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print("Premium Tip Panel injection complete.")

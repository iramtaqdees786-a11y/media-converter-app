import os
import glob
import re

frontend_dir = r'c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend'
html_files = glob.glob(os.path.join(frontend_dir, '**/*.html'), recursive=True)

# 1. Refined Premium Support Section (Lower Tip Area)
# We remove ?preview=true as it might cause visibility issues
tip_section_code = """
    <!-- Premium Support Section -->
    <section class="support-chaos" style="margin-top: 80px; margin-bottom: 40px; padding: 20px;">
        <div class="container" style="max-width: 800px; margin: 0 auto;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h2 style="font-size: 2.5rem; background: linear-gradient(135deg, #9a93f5, #794bc4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 15px;">Fuel the Chaos 🔥</h2>
                <p style="color: var(--text-secondary); font-size: 1.1rem;">Support the development of ConvertRocket's edge-case laboratory. Your contributions keep the servers running and the algorithms sharp.</p>
            </div>
            
            <div class="glass-card" style="
                background: white;
                border-radius: 24px;
                padding: 10px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.4), 0 0 20px rgba(121, 75, 196, 0.1);
                overflow: hidden;
            ">
                <iframe id='kofiframe' src='https://ko-fi.com/izyaan/?hidefeed=true&widget=true&embed=true' 
                    style='border:none; width:100%; border-radius: 14px; background: #ffffff;' 
                    height='712' title='izyaan' loading="lazy"></iframe>
            </div>
            
            <div style="text-align: center; margin-top: 25px; opacity: 0.6; font-size: 0.85rem; color: var(--text-secondary);">
                Securely processed via Ko-fi. No data is stored on ConvertRocket servers.
            </div>
        </div>
    </section>
"""

# 2. Refined Hero Support Button (Top Widget)
# This goes right after the <p> in the Hero section
hero_button_code = """
                <!-- Blended Hero Support -->
                <div style="margin-top: 20px; display: flex; justify-content: center; opacity: 0.9;">
                    <script type='text/javascript' src='https://storage.ko-fi.com/cdn/widget/Widget_2.js'></script>
                    <script type='text/javascript'>kofiwidget2.init('Fuel the Chaos 🔥', '#794bc4', 'Q5Q81VCPM3');kofiwidget2.draw();</script>
                </div>
"""

def clean_content(content):
    # Remove old top widget
    content = re.sub(r'<!-- Ko-fi Top Widget -->.*?</div>', '', content, flags=re.DOTALL)
    # Remove old premium support section
    content = re.sub(r'<!-- Premium Support Section -->.*? </section>', '', content, flags=re.DOTALL)
    # Remove any stray kofiwidget2 code if it was outside comments
    return content

for file_path in html_files:
    if 'temp_repo' in file_path or '.git' in file_path:
        continue

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        content = clean_content(content)

        # 1. Place the Hero Button below the main paragraph in the header
        # We look for </p> inside the hero section
        hero_match = re.search(r'(<header class="hero">.*?</p>)', content, re.DOTALL)
        if hero_match:
            content = content.replace(hero_match.group(1), hero_match.group(1) + hero_button_code)
        
        # 2. Place the Tip Panel before footer
        if '<footer' in content:
            content = content.replace('<footer', tip_section_code + "\n    <footer")
        elif '</body>' in content:
            content = content.replace('</body>', tip_section_code + "\n</body>")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed support UI in: {os.path.relpath(file_path, frontend_dir)}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print("Refinement complete.")

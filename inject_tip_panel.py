import os
import glob
import re

frontend_dir = r'c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend'
html_files = glob.glob(os.path.join(frontend_dir, '**/*.html'), recursive=True)

# Premium Support Section HTML (Adblock-friendly names)
tip_section_code = """
    <!-- Protocol Foundation Support -->
    <section class="foundation-bridge" style="margin-top: 80px; margin-bottom: 40px; padding: 20px; font-family: 'Inter', sans-serif;">
        <div class="container" style="max-width: 1000px; margin: 0 auto;">
            <div style="text-align: center; margin-bottom: 40px;">
                <h2 style="font-size: 2.8rem; background: linear-gradient(135deg, #9a93f5, #794bc4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 15px; font-weight: 800;">Fuel the Chaos 🔥</h2>
                <p style="color: var(--text-secondary); font-size: 1.2rem; max-width: 600px; margin: 0 auto;">Your support directly funds the server-side GPU processing and the edge-case algorithms that make ConvertRocket unique.</p>
            </div>

            <div style="display: flex; flex-wrap: wrap; gap: 30px; align-items: flex-start; margin-bottom: 40px;">
                <!-- Content Area -->
                <div style="flex: 1; min-width: 300px; color: var(--text-secondary);">
                    <h3 style="color: #fff; font-size: 1.5rem; margin-bottom: 20px;">Why support the Protocol?</h3>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                            <span style="color: #794bc4; font-size: 1.2rem;">⚡</span>
                            <span><strong>Zero Ads, Ever:</strong> We rely on users, not trackers.</span>
                        </li>
                        <li style="margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                            <span style="color: #794bc4; font-size: 1.2rem;">🛠️</span>
                            <span><strong>Edge-Case Laboratory:</strong> Help us build specialized tools for rare formats.</span>
                        </li>
                        <li style="margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                            <span style="color: #794bc4; font-size: 1.2rem;">🚀</span>
                            <span><strong>Direct Development:</strong> 100% of tips go to server costs and code.</span>
                        </li>
                    </ul>
                    <div style="margin-top: 30px; padding: 20px; background: rgba(121, 75, 196, 0.1); border-radius: 16px; border-left: 4px solid #794bc4;">
                        <p style="margin: 0; font-style: italic; font-size: 0.95rem;">"ConvertRocket is a passion project built for the internet's power users. If it saved you time today, consider dropping a fuel unit in the tank." - Izyaan</p>
                    </div>
                </div>

                <!-- Widget Area with Hover effect -->
                <div class="foundation-hub-wrapper" style="flex: 1.2; min-width: 350px; position: relative;">
                    <style>
                        .foundation-hub-wrapper:hover .foundation-hub {
                            transform: translateY(-5px);
                            box-shadow: 0 30px 60px rgba(0,0,0,0.5), 0 0 30px rgba(121, 75, 196, 0.2);
                        }
                        .foundation-hub {
                            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
                        }
                        .tip-hover-hint {
                            position: absolute;
                            top: -15px;
                            right: 20px;
                            background: #794bc4;
                            color: white;
                            padding: 6px 14px;
                            border-radius: 20px;
                            font-size: 0.75rem;
                            font-weight: 700;
                            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                            opacity: 0;
                            transform: translateY(10px);
                            transition: all 0.3s ease;
                            pointer-events: none;
                            z-index: 10;
                        }
                        .foundation-hub-wrapper:hover .tip-hover-hint {
                            opacity: 1;
                            transform: translateY(0);
                        }
                    </style>
                    <div class="tip-hover-hint">Secure Protocol Checkout</div>
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
                </div>
            </div>

            <div style="text-align: center; opacity: 0.5; font-size: 0.8rem; color: var(--text-secondary);">
                Encrypted via Ko-fi SSL. Standard processing rates apply.
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

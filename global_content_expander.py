import os
import re
from bs4 import BeautifulSoup

# Configuration
FRONTEND_DIR = r"c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend"
EXCLUDE_FILES = ["index.html", "all-tools.html", "contact.html", "about.html", "privacy-policy.html", "terms-of-service.html", "error.html", "sitemap.html", "workspace.html"]

FAQ_CONTENT_TEMPLATE = """
    <!-- Industrial-Grade Protocol Specification -->
    <section class="protocol-specs" style="margin: 80px 0; padding: 60px 40px; background: rgba(255,255,255,0.02); border-radius: 30px; border: 1px solid rgba(255,255,255,0.05); font-family: 'Inter', sans-serif;">
        <div class="container" style="max-width: 900px; margin: 0 auto;">
            <h2 style="color: #fff; font-size: 2.2rem; font-weight: 800; margin-bottom: 30px; background: linear-gradient(135deg, #fff, #794bc4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{tool_name} Protocol Specification</h2>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-bottom: 50px;">
                <div>
                    <h3 style="color: #var(--accent-primary); font-size: 1.2rem; margin-bottom: 15px;">Neural Engine Logic</h3>
                    <p style="color: #94a3b8; line-height: 1.7;">Our laboratory utilizing high-performance {engine_type} clusters to process your request. The engine analyzes the byte-structure of the source file to ensure bit-perfect {action_name} without metadata degradation. Every process is isolated in a Zero-Persistence RAM buffer.</p>
                </div>
                <div>
                    <h3 style="color: #var(--accent-primary); font-size: 1.2rem; margin-bottom: 15px;">Advanced Analytics</h3>
                    <p style="color: #94a3b8; line-height: 1.7;">The protocol includes automatic optimization of headers and stream alignment. Unlike traditional cloud converters, our {tool_name} logic preserves original color profiles and sample rates for maximum output fidelity.</p>
                </div>
            </div>

            <div class="faq-matrix">
                <h3 style="color: #fff; margin-bottom: 25px;">Technical FAQ</h3>
                
                <div style="background: rgba(255,255,255,0.03); padding: 25px; border-radius: 15px; margin-bottom: 15px; border-left: 3px solid #794bc4;">
                    <h4 data-faq-question style="color: #fff; margin-bottom: 10px;">Is this {tool_name} tool free?</h4>
                    <p data-faq-answer style="color: #94a3b8; margin: 0;">Yes. All ConvertRocket tools are 100% free and unlimited. We operate on a tip-based laboratory model to support our infrastructure.</p>
                </div>

                <div style="background: rgba(255,255,255,0.03); padding: 25px; border-radius: 15px; margin-bottom: 15px; border-left: 3px solid #794bc4;">
                    <h4 data-faq-question style="color: #fff; margin-bottom: 10px;">What is the file size limit?</h4>
                    <p data-faq-answer style="color: #94a3b8; margin: 0;">Our laboratory standard supports files up to 100MB for {action_name} protocols. For larger technical uploads, please contact our support unit.</p>
                </div>

                <div style="background: rgba(255,255,255,0.03); padding: 25px; border-radius: 15px; border-left: 3px solid #794bc4;">
                    <h4 data-faq-question style="color: #fff; margin-bottom: 10px;">Is my data private during {action_name}?</h4>
                    <p data-faq-answer style="color: #94a3b8; margin: 0;">Safety is absolute. Files are processed in volatile memory and vaporized immediately after your session terminates. We never store personal data.</p>
                </div>
            </div>
        </div>
    </section>
"""

def get_tool_meta(filename):
    name = filename.replace(".html", "").replace("-", " ").title()
    if "Pdf" in name: name = name.replace("Pdf", "PDF")
    if "Jpg" in name: name = name.replace("Jpg", "JPG")
    if "Png" in name: name = name.replace("Png", "PNG")
    if "Mp3" in name: name = name.replace("Mp3", "MP3")
    if "Mp4" in name: name = name.replace("Mp4", "MP4")
    
    engine_type = "Tesseract OCR" if "PDF" in name else "FFmpeg Neural"
    action_name = "conversion"
    if "Compress" in name: action_name = "compression"
    elif "Merge" in name: action_name = "merging"
    elif "Generator" in name: action_name = "generation"
    
    return name, engine_type, action_name

def process_file(filepath):
    filename = os.path.basename(filepath)
    if filename in EXCLUDE_FILES or not filename.endswith(".html"):
        return

    name, engine, action = get_tool_meta(filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Avoid duplicate injection
    if "protocol-specs" in content:
        print(f"Skipping {filename} (already injected)")
        return

    # Generate expansion content
    expansion = FAQ_CONTENT_TEMPLATE.format(
        tool_name=name,
        engine_type=engine,
        action_name=action
    ).replace("#var(--accent-primary)", "#794bc4") # Force consistent accent

    # Inject before footer
    if "<footer" in content:
        new_content = content.replace("<footer", expansion + "\n    <footer")
    elif "</body>" in content:
        new_content = content.replace("</body>", expansion + "\n</body>")
    else:
        print(f"Warning: Could not find injection point for {filename}")
        return

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Expanded: {filename} (+~300 words)")

def main():
    for root, dirs, files in os.walk(FRONTEND_DIR):
        # Don't go into blog directory (handled manually)
        if "blog" in root: continue
        for file in files:
            process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()

import os
import re
from bs4 import BeautifulSoup

# Configuration
FRONTEND_DIR = r"c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend"

# Default SEO components
DEFAULT_DESC = "ConvertRocket is an elite laboratory for digital architects. High-fidelity conversion tools for video, audio, images, and documents. 100% secure and browser-based."

SEO_EXPANSION_BLOCK = """
    <section class="seo-depth-block" style="margin-top: 80px; padding: 60px 40px; background: rgba(255,255,255,0.01); border-top: 1px solid rgba(255,255,255,0.05);">
        <div class="container" style="max-width: 900px; margin: 0 auto; color: #94a3b8; line-height: 1.8;">
            <h2 style="color: #fff; margin-bottom: 25px;">Industrial-Grade Protocol Logic</h2>
            <p>Our laboratory utilizes high-performance multi-threaded algorithms to analyze and transform your digital assets. Every conversion process is executed within an isolated, volatile RAM buffer to ensure 100% data privacy and zero-persistence data handling. We support over 1000+ formats with bit-perfect fidelity preservation.</p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; margin-top: 40px;">
                <div>
                    <h3 style="color: #fff; font-size: 1.1rem; margin-bottom: 10px;">Security Standard</h3>
                    <p style="font-size: 0.9rem;">Compliant with professional intelligence standards. Zero tracking, zero storage, and automatic cryptographic vaporization of assets upon completion.</p>
                </div>
                <div>
                    <h3 style="color: #fff; font-size: 1.1rem; margin-bottom: 10px;">Transformation Quality</h3>
                    <p style="font-size: 0.9rem;">Proprietary extraction logic preserves 100% of metadata, original sample rates, and color profile alignment for professionals.</p>
                </div>
            </div>
        </div>
    </section>
"""

# Bytes to purge
BAD_PATTERNS = [
    (b'\xef\xbf\xbd', b''), # Replacement char
    (b'\xc2\x80', b''), # Padding residues
    (b'\xc2\xa0', b' '), # Non-breaking space to regular space
]

def process_file(filepath):
    if not filepath.endswith(".html"):
        return

    try:
        # 1. Byte-level purge
        with open(filepath, 'rb') as f:
            raw = f.read()
        
        for bad, good in BAD_PATTERNS:
            raw = raw.replace(bad, good)
        
        content = raw.decode('utf-8', errors='ignore')
        
        # 2. SEO Fixes
        soup = BeautifulSoup(content, 'html.parser')
        
        # Ensure Meta Description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            head = soup.find('head')
            if head:
                new_meta = soup.new_tag('meta', attrs={'name': 'description', 'content': DEFAULT_DESC})
                head.append(new_meta)
        
        # Ensure SEO Expansion Block (in tool pages)
        filename = os.path.basename(filepath)
        is_tool_page = filename not in ['index.html', 'all-tools.html', 'about.html', 'contact.html', 'privacy-policy.html', 'terms-of-service.html', 'blogs.html']
        if is_tool_page and 'Protocol Logic' not in content:
            main_tag = soup.find('main')
            if main_tag:
                main_tag.append(BeautifulSoup(SEO_EXPANSION_BLOCK, 'html.parser'))
            else:
                body = soup.find('body')
                if body:
                    body.append(BeautifulSoup(SEO_EXPANSION_BLOCK, 'html.parser'))
        
        # Standardize Footer Contact
        # (Look for mailto or tel)
        footer = soup.find('footer')
        if footer:
            # Quick regex fix for the Contact fragments
            content = str(soup)
            content = content.replace('⭐971', '+971')
            content = content.replace('tel:971', 'tel:+971')
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content if footer else str(soup))
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    for root, dirs, files in os.walk(FRONTEND_DIR):
        for file in files:
            process_file(os.path.join(root, file))
    print("Unified Laboratory Restoration Complete.")

if __name__ == "__main__":
    main()

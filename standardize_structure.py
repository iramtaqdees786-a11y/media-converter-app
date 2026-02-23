import os
import re

frontend_dir = r"c:\Users\Lenovo-T470-0027\ .gemini\antigravity\scratch\media-converter-app\frontend"
# Handle potential space in path from prompt/copy-paste
frontend_dir = frontend_dir.replace(" .gemini", ".gemini")

footer_standard = """    <footer class="footer-clean">
        <div class="footer-links">
            <a href="/all-tools">All Tools</a>
            <a href="/media-hub">Media Hub</a>
            <a href="/pdf-lab">PDF Lab</a>
            <a href="/blogs">Blog</a>
            <a href="/privacy-policy">Privacy</a>
            <a href="/terms-of-service">Terms</a>
            <a href="/sitemap">Sitemap</a>
            <a href="/contact">Contact</a>
        </div>
        <p class="footer-copyright">© 2026 ConvertRocket.online • Made by Izyaan</p>
    </footer>"""

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Standardize Footer
    # Patterns for different existing footers
    footer_patterns = [
        r'<footer class="footer-clean">.*?</footer>',
        r'<footer class="footer-cosmos">.*?</footer>',
        r'<footer class="resource-footer">.*?</footer>',
        r'<footer class="footer">.*?</footer>',
        r'<footer class="footer-sigma">.*?</footer>'
    ]
    
    new_content = content
    for pattern in footer_patterns:
        new_content = re.sub(pattern, footer_standard, new_content, flags=re.DOTALL)

    # 2. Standardize SEO Section Class
    new_content = re.sub(r'class="seo-pro"', 'class="seo-content"', new_content)
    new_content = re.sub(r'class="seo-slop"', 'class="seo-content"', new_content)
    
    # 3. Remove problematic inline styles in SEO Section
    # Find the seo-content section and remove text-align: left from its immediate children or specific divs
    def remove_seo_inline_styles(match):
        section = match.group(0)
        # Remove text-align: left; but keep display: grid etc if they are doing layout
        # Or better: remove the whole style if it's just doing what CSS should do
        # Most of these are: <div style="... text-align: left;">
        section = re.sub(r'style="([^"]*?)text-align:\s*left;?([^"]*?)"', r'style="\1\2"', section)
        # Clean up empty style attributes or trailing semicolons
        section = re.sub(r'style="\s*;?\s*"', '', section)
        return section

    new_content = re.compile(r'<section class="seo-content">.*?</section>', re.DOTALL).sub(remove_seo_inline_styles, new_content)

    # 4. Standardize Tool Bento Grid (centering fix)
    # Remove inline max-width and margin from bento-grid if it's present
    new_content = re.sub(r'<div class="bento-grid" style="grid-template-columns: 1fr; max-width: 800px; margin: 0 auto;">', 
                         r'<div class="bento-grid" style="grid-template-columns: 1fr;">', new_content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    count = 0
    for root, dirs, files in os.walk(frontend_dir):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                if process_file(path):
                    count += 1
    print(f"Updated {count} files.")

if __name__ == "__main__":
    main()

import os
import re

footer_content = """        <footer class="footer">
            <div class="footer-brand">🚀 <span class="footer-logo">ConvertRocket</span></div>
            <p class="footer-tagline">The World's Fastest All-In-One Converter • 100% Free • No Signup</p>
            <div class="footer-links">
                <a href="/video-converter">Video Downloader</a> •
                <a href="/mp3-converter">MP3 Converter</a> •
                <a href="/pdf-tools">PDF Tools</a> •
                <a href="/media-tools">Media Tools</a> •
                <a href="/sitemap">Sitemap</a>
            </div>

            <div class="footer-divider" style="margin: 20px 0; border-top: 1px solid rgba(255,255,255,0.1);"></div>

            <div class="footer-seo-links"
                style="display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; font-size: 0.85rem; max-width: 900px; margin: 0 auto 20px;">
                <a href="/blogs" style="color: var(--text-muted); text-decoration: none;">Blog</a>
                <span style="color: var(--text-muted);">|</span>
                <a href="/about" style="color: var(--text-muted); text-decoration: none;">About Us</a>
                <span style="color: var(--text-muted);">|</span>
                <a href="/contact" style="color: var(--text-muted); text-decoration: none;">Contact Us</a>
                <span style="color: var(--text-muted);">|</span>
                <a href="/privacy-policy" style="color: var(--text-muted); text-decoration: none;">Privacy Policy</a>
                <span style="color: var(--text-muted);">|</span>
                <a href="/terms-of-service" style="color: var(--text-muted); text-decoration: none;">Terms of Service</a>
            </div>

            <div style="margin: 30px auto; text-align: center;">
                <a href="https://www.producthunt.com/products/convertrocket?embed=true&amp;utm_source=badge-featured&amp;utm_medium=badge&amp;utm_campaign=badge-convertrocket" target="_blank" rel="noopener noreferrer"><img alt="ConvertRocket - All In One Converter And Downloader | Product Hunt" width="250" height="54" src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=1055288&amp;theme=dark&amp;t=1767076017143"></a>
            </div>

            <p class="copyright">© 2025 ConvertRocket.online - Fast & Private File Conversion</p>
        </footer>"""

auto_download_code = """
                    // Automatic download trigger
                    setTimeout(() => {
                        const link = document.createElement('a');
                        link.href = data.download_url;
                        link.download = data.filename || 'converted_file';
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                    }, 500);"""

def update_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update Footer (if not index.html)
    if 'index.html' not in filepath and '/blog/' not in filepath:
        content = re.sub(r'<footer class="footer">.*?</footer>', footer_content, content, flags=re.DOTALL)
        if '<footer' not in content and '</body>' in content:
            content = content.replace('</body>', footer_content + '\n</body>')

    # 2. Add Auto-download to inline scripts
    # Find patterns like: resDiv.innerHTML = `... Success ... <a href="${data.download_url}" ... </div> `;
    # and append auto_download_code after the closing backtick of the innerHTML assignment.
    
    patterns = [
        r'(resDiv\.innerHTML\s*=\s*`[^`]*Success![^`]*`[\s;]*)',
        r'(el\.innerHTML\s*=\s*`[^`]*Success![^`]*`[\s;]*)',
        r'(resultDiv\.innerHTML\s*=\s*`[^`]*Success![^`]*`[\s;]*)'
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            matched_text = match.group(1)
            if 'setTimeout' not in matched_text and 'auto-download-link' not in matched_text:
                new_text = matched_text + auto_download_code
                content = content.replace(matched_text, new_text)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Process frontend
base_dir = r'c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend'
for filename in os.listdir(base_dir):
    if filename.endswith('.html'):
        update_html_file(os.path.join(base_dir, filename))

# Process blog
blog_dir = os.path.join(base_dir, 'blog')
if os.path.exists(blog_dir):
    for filename in os.listdir(blog_dir):
        if filename.endswith('.html'):
            update_html_file(os.path.join(blog_dir, filename))

print("All footers and auto-download logic updated!")

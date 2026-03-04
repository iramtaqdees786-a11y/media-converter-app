import os
import glob
import re

frontend_dir = r'c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend'
html_files = glob.glob(os.path.join(frontend_dir, '*.html'))

ignored = ['index.html', '404.html', 'about.html', 'contact.html', 'privacy-policy.html', 'terms-of-service.html', 'sitemap.html', 'converter.html', 'blogs.html', 'all-tools.html', 'downloader.html', 'media-hub.html', 'utilities.html', 'dev-suite.html', 'pdf-lab.html', 'ai-lab.html']
endpoints = []

for f in html_files:
    basename = os.path.basename(f)
    if basename not in ignored:
        name = basename.replace('.html', '')
        title = name.replace('-', ' ').title()
        endpoints.append({'url': f'/{name}', 'title': title})

# Generate HTML block
new_html = '\n        <!-- COMPLETE TOOLS MATRIX START -->\n'
new_html += '        <div class="container" style="margin-top: 80px; margin-bottom: 50px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 50px;">\n'
new_html += '            <h2 style="margin-bottom: 20px; font-size: 1.5rem; opacity: 0.8; letter-spacing: 1px;">Complete Tools Matrix</h2>\n'
new_html += '            <p style="color: var(--text-secondary); margin-bottom: 30px;">Access every specialized endpoint directly.</p>\n'
new_html += '            <div id="all-endpoints-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px;">\n'

endpoints.sort(key=lambda x: x['title'])

for i, ep in enumerate(endpoints):
    display_style = '' if i < 15 else 'display: none;'
    cls = 'endpoint-btn' + (' extra-endpoint' if i >= 15 else '')
    new_html += f'                <a href="{ep["url"]}" class="{cls}" style="padding: 12px 16px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; color: var(--text-secondary); text-decoration: none; font-size: 0.9rem; transition: 0.2s; text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; {display_style}" onmouseover="this.style.background=\'rgba(255,255,255,0.1)\'; this.style.color=\'#fff\'" onmouseout="this.style.background=\'rgba(255,255,255,0.03)\'; this.style.color=\'var(--text-secondary)\'">{ep["title"]}</a>\n'

new_html += '            </div>\n'
if len(endpoints) > 15:
    new_html += '            <div style="text-align: center; margin-top: 30px;">\n'
    new_html += '                <button id="show-more-endpoints" style="background: var(--accent-primary); color: #000; border: none; padding: 12px 30px; border-radius: 30px; font-weight: 700; cursor: pointer; transition: 0.3s;" onmouseover="this.style.transform=\'scale(1.05)\'" onmouseout="this.style.transform=\'scale(1)\';">Show All Protocols</button>\n'
    new_html += '            </div>\n'
    
    new_html += '''            <script>
                document.getElementById('show-more-endpoints')?.addEventListener('click', function() {
                    const extra = document.querySelectorAll('.extra-endpoint');
                    const isHidden = extra[0].style.display === 'none';
                    extra.forEach(el => el.style.display = isHidden ? 'block' : 'none');
                    this.innerText = isHidden ? 'Show Less' : 'Show All Protocols';
                });
            </script>\n'''
new_html += '        </div>\n'
new_html += '        <!-- COMPLETE TOOLS MATRIX END -->\n'

all_tools_path = os.path.join(frontend_dir, 'all-tools.html')
with open(all_tools_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Insert before </main>
if '</main>' in content:
    content = content.replace('</main>', new_html + '    </main>')
    with open(all_tools_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected Tools Matrix!")
else:
    print("Couldn't find </main>")

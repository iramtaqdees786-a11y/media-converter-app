import os
import glob
import re

frontend_dir = r'c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend'
blog_dir = os.path.join(frontend_dir, 'blog')
blog_files = glob.glob(os.path.join(blog_dir, '*.html'))
blogs_html_path = os.path.join(frontend_dir, 'blogs.html')

def extract_meta(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Get Title (from <title> or <h1>)
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    h1_match = re.search(r'<h1>(.*?)</h1>', content, re.IGNORECASE)
    h1_alt_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE)
    
    title = ""
    # Try to find the h1 inside the article first
    article_h1 = re.search(r'<article.*?>\s*<header.*?>\s*<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    if article_h1:
        title = re.sub(r'<[^>]+>', '', article_h1.group(1)).strip()
    
    if not title or title.lower() == 'convertrocket':
        if title_match:
            title = title_match.group(1).split('-')[0].strip()
        elif h1_match:
            title = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
        elif h1_alt_match:
            title = re.sub(r'<[^>]+>', '', h1_alt_match.group(1)).strip()
            
    if not title or title.lower() == 'convertrocket':
        title = os.path.basename(filepath).replace('.html', '').replace('-', ' ').title()
        
    # Get excerpt (from meta description or first p)
    desc_match = re.search(r'<meta name="description" content="(.*?)">', content, re.IGNORECASE)
    p_match = re.search(r'<p>(.*?)</p>', content, re.IGNORECASE)
    
    desc = ""
    if desc_match:
        desc = desc_match.group(1).strip()
    elif p_match:
        desc = re.sub(r'<[^>]+>', '', p_match.group(1)).strip()
        
    if len(desc) > 120:
        desc = desc[:117] + "..."
        
    # Pick an icon based on title keywords
    icon = "📚"
    t_lower = title.lower()
    if 'pdf' in t_lower: icon = "📄"
    elif 'video' in t_lower or 'mp4' in t_lower or 'youtube' in t_lower or 'tiktok' in t_lower or 'reels' in t_lower: icon = "🎬"
    elif 'image' in t_lower or 'jpg' in t_lower or 'heic' in t_lower or 'png' in t_lower or 'webp' in t_lower: icon = "📸"
    elif 'audio' in t_lower or 'mp3' in t_lower: icon = "🎵"
    elif 'safe' in t_lower: icon = "🔒"
    elif 'fast' in t_lower or 'batch' in t_lower: icon = "⚡"
    
    return {
        'url': f'/blog/{os.path.basename(filepath).replace(".html", "")}',
        'title': title,
        'desc': desc,
        'icon': icon
    }

blog_metadata = []
for f in blog_files:
    blog_metadata.append(extract_meta(f))

# Sort alphabetically
blog_metadata.sort(key=lambda x: x['title'])

# Build new grid HTML
grid_html = '<div class="bento-grid" style="grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px;">\n'

for b in blog_metadata:
    grid_html += f'''
    <a href="{b['url']}" class="bento-card" style="text-decoration: none; display: flex; flex-direction: column; justify-content: flex-start; transition: transform 0.3s ease, border-color 0.3s ease; border: 1px solid rgba(255,255,255,0.05);">
        <div class="shine-overlay"></div>
        <div style="font-size: 2.2rem; margin-bottom: 15px;">{b['icon']}</div>
        <h3 style="font-size: 1.25rem; font-weight: 700; color: #fff; margin-bottom: 10px; line-height: 1.3;">{b['title']}</h3>
        <p style="color: var(--text-secondary); font-size: 0.9rem; line-height: 1.5; flex-grow: 1;">{b['desc']}</p>
        <div style="margin-top: 20px; font-size: 0.8rem; font-weight: 800; color: var(--accent-primary); letter-spacing: 1px; text-transform: uppercase;">
            READ ARTICLE &rarr;
        </div>
    </a>
'''

grid_html += '</div>\n'

# Read blogs.html and replace the bento-grid
with open(blogs_html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace everything from <div class="bento-grid"> to the next </main> tag minus the closing tag
start_marker = 'class="bento-grid"'
end_tag = '</main>'

if start_marker in content and end_tag in content:
    # Find the start of the div containing bento-grid
    start_idx = content.find(start_marker)
    # Move back to the beginning of the <div tag
    div_start = content.rfind('<div', 0, start_idx)
    end_idx = content.find(end_tag, div_start)
    
    new_content = content[:div_start] + grid_html + "        " + content[end_idx:]
    
    with open(blogs_html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Generated blogs.html with {len(blog_metadata)} blog entries.")
else:
    print("Could not find grid tags in blogs.html")

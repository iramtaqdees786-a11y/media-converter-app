"""
Generate individual converter pages with ION V4 PREMIUM THEME
Includes 50+ improvements: Stars, Toasts, SEO Slop, Fixed Select area
"""
import os

CONVERTERS = {
    'image': [
        {'from': 'jpg', 'to': 'png', 'desc': 'Transparent backgrounds & lossless quality', 'accepts': '.jpg,.jpeg'},
        {'from': 'png', 'to': 'jpg', 'desc': 'Small file size with photo quality', 'accepts': '.png'},
        {'from': 'webp', 'to': 'jpg', 'desc': 'Next-gen WebP to universal JPG', 'accepts': '.webp'},
        {'from': 'webp', 'to': 'png', 'desc': 'WebP with transparency to PNG', 'accepts': '.webp'},
        {'from': 'jpg', 'to': 'webp', 'desc': 'Best compression for web images', 'accepts': '.jpg,.jpeg'},
        {'from': 'png', 'to': 'webp', 'desc': 'Lossless conversion to modern WebP', 'accepts': '.png'},
        {'from': 'heic', 'to': 'jpg', 'desc': 'iPhone photos transformed instantly', 'accepts': '.heic,.heif'},
        {'from': 'heic', 'to': 'png', 'desc': 'Convert iPhone photos with transparency', 'accepts': '.heic,.heif'},
        {'from': 'gif', 'to': 'mp4', 'desc': 'Turn GIFs into optimized video files', 'accepts': '.gif'},
        {'from': 'bmp', 'to': 'jpg', 'desc': 'Bitmap to high-quality JPG', 'accepts': '.bmp'},
        {'from': 'bmp', 'to': 'png', 'desc': 'Bitmap to PNG with better compatibility', 'accepts': '.bmp'},
        {'from': 'tiff', 'to': 'jpg', 'desc': 'Convert heavy TIFF to light JPG', 'accepts': '.tiff,.tif'},
        {'from': 'tiff', 'to': 'png', 'desc': 'TIFF to PNG for web and print', 'accepts': '.tiff,.tif'},
    ],
    'pdf': [
        {'from': 'pdf', 'to': 'word', 'desc': 'Editable Word stream from PDF', 'accepts': '.pdf'},
        {'from': 'pdf', 'to': 'excel', 'desc': 'Data extraction to spreadsheets', 'accepts': '.pdf'},
        {'from': 'word', 'to': 'pdf', 'desc': 'Document to PDF/A archive quality', 'accepts': '.doc,.docx'},
        {'from': 'excel', 'to': 'pdf', 'desc': 'Spreadsheet to shareable PDF', 'accepts': '.xls,.xlsx'},
        {'from': 'ppt', 'to': 'pdf', 'desc': 'Presentation to high-res PDF', 'accepts': '.ppt,.pptx'},
        {'from': 'jpg', 'to': 'pdf', 'desc': 'Scan images into one PDF', 'accepts': '.jpg,.jpeg', 'category': 'image'},
        {'from': 'png', 'to': 'pdf', 'desc': 'PNG archive in PDF container', 'accepts': '.png', 'category': 'image'},
    ],
    'media': [
        {'from': 'mp4', 'to': 'mp3', 'desc': 'High bitrate audio extraction', 'accepts': 'video/*'},
        {'from': 'mp4', 'to': 'avi', 'desc': 'MP4 to legacy AVI format', 'accepts': 'video/*'},
        {'from': 'mp4', 'to': 'mov', 'desc': 'MP4 to QuickTime MOV container', 'accepts': 'video/*'},
        {'from': 'avi', 'to': 'mp4', 'desc': 'Modernizing old AVI files', 'accepts': '.avi'},
        {'from': 'mov', 'to': 'mp4', 'desc': 'MOV to universal MP4 stream', 'accepts': '.mov'},
        {'from': 'mkv', 'to': 'mp4', 'desc': 'Lossless MKV to MP4 conversion', 'accepts': '.mkv'},
        {'from': 'webm', 'to': 'mp4', 'desc': 'Browser WebM to universal video', 'accepts': '.webm'},
        {'from': 'flv', 'to': 'mp4', 'desc': 'Legacy Flash video recovery', 'accepts': '.flv'},
        {'from': 'wav', 'to': 'mp3', 'desc': 'Lossless WAV to shareable MP3', 'accepts': '.wav'},
        {'from': 'mp3', 'to': 'wav', 'desc': 'MP3 expansion to studio WAV', 'accepts': '.mp3'},
        {'from': 'flac', 'to': 'mp3', 'desc': 'Ultra-lossless to standard audio', 'accepts': '.flac'},
        {'from': 'aac', 'to': 'mp3', 'desc': 'Extracting AAC to high-res MP3', 'accepts': '.aac'},
        {'from': 'm4a', 'to': 'mp3', 'desc': 'iTunes M4A to universal format', 'accepts': '.m4a'},
    ]
}

def generate_page(from_format, to_format, description, accepts, category=''):
    from_upper = from_format.upper()
    to_upper = to_format.upper()
    title = f"{from_upper} to {to_upper}"
    filename = f"{from_format}-to-{to_format}.html"
    
    icon = '🔄'
    if 'image' in category or any(f in ['jpg','png','webp','heic'] for f in [from_format, to_format]): icon='🖼️'
    elif any(f in ['pdf','word','excel'] for f in [from_format, to_format]): icon='📄'
    elif any(f in ['mp4','avi','mov'] for f in [from_format, to_format]): icon='🎬'
    elif any(f in ['mp3','wav','flac'] for f in [from_format, to_format]): icon='🎵'

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-ZBZSYT7DRY"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-ZBZSYT7DRY');</script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} Converter - Free Online Laboratory | ConvertRocket</title>
    <meta name="description" content="Convert {from_upper} to {to_upper} for free. High-fidelity conversion lab for {from_format} files. Safe, secure, and no signup.">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/ultra-minimalist.css?v=4.0">
    <script src="/static/js/minimalist-search.js" defer></script>
    <script src="/static/js/premium-features.js" defer></script>
</head>
<body>
    <div class="bg-animated"></div>
    <div class="container">
        <nav class="nav-premium">
            <div class="brand-premium" style="font-weight: 950; font-size: 1.5rem;"><a href="/" style="text-decoration:none; color:inherit;">🚀 ConvertRocket</a></div>
        </nav>

        <div class="breadcrumbs">
            <a href="/">Home</a> <span>/</span> <a href="/all-tools">Converters</a> <span>/</span> {title}
        </div>

        <div class="converter-box">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:40px;">
                <h2 style="font-weight: 900; font-size: 2.2rem; margin:0;">{from_upper} <span style="color:var(--neon-cyan)">→</span> {to_upper}</h2>
                <div class="card-star active" style="font-size:2rem; cursor:pointer;" onclick="toggleThisStar(this, '/{from_format}-to-{to_format}')">☆</div>
            </div>
            
            <div class="upload-zone" id="upload-zone">
                <div class="upload-icon">{icon}</div>
                <p style="font-size: 1.4rem; font-weight: 800;">Drop your {from_upper} here</p>
                <p style="opacity: 0.5;">or click to browse your Laboratory</p>
                <input type="file" id="file-input" accept="{accepts}">
            </div>

            <div id="file-info" style="display:none; margin-top:30px; text-align:left; padding:25px; border:1px solid var(--glass-border); border-radius:25px; background:rgba(255,255,255,0.03);"></div>
            
            <div id="progress-container" class="progress-container">
                <div class="progress-fill" id="progress-fill"></div>
                <div style="display:flex; justify-content:space-between; margin-top:15px; font-size:0.9rem; font-weight:700;">
                    <span id="progress-message">Analyzing structure...</span>
                    <span id="progress-percent">0%</span>
                </div>
            </div>

            <div id="result-container" style="display:none; margin-top:40px;">
                <div style="margin-bottom:20px; color:var(--neon-cyan); font-weight:900; letter-spacing:1px;">✅ LABORATORY SUCCESS</div>
                <div style="display: flex; flex-direction: column; gap: 15px; align-items: center;">
                    <a href="#" id="download-link" class="action-btn" style="display:inline-block; text-decoration:none; width: 100%; text-align: center;" download>Save {to_upper} Result</a>
                    
                    <!-- Result Actions (Bookmark/Copy) -->
                    <div style="display: flex; gap: 10px; width: 100%;">
                        <button onclick="copyResultLink()" class="btn-tool" style="flex: 1; background: rgba(0, 242, 255, 0.1); color: var(--neon-cyan); border: 1px solid rgba(0, 242, 255, 0.2); padding: 12px; border-radius: 15px; font-weight: 700; cursor: pointer;">
                            🔗 Copy Link
                        </button>
                        <button onclick="bookmarkTool()" class="btn-tool" style="flex: 1; background: rgba(188, 19, 254, 0.1); color: var(--neon-purple); border: 1px solid rgba(188, 19, 254, 0.2); padding: 12px; border-radius: 15px; font-weight: 700; cursor: pointer;">
                            ⭐ Bookmark
                        </button>
                    </div>
                    <div class="bookmark-badge">🚀 Add tool to your browser lab (Ctrl+D)</div>
                </div>
            </div>

            <div id="status-message" class="status-message"></div>
        </div>

        <section class="seo-slop">
            <h2>Detailed Guide for {from_upper} to {to_upper}</h2>
            <p>Our professional <strong>{from_format} to {to_format} converter</strong> is designed for users who demand the highest possible fidelity. When you convert {from_upper} files in our lab, we use a hybrid processing model that combines browser-side execution for privacy and high-performance server-side engines for complex operations.</p>
            
            <h3>How to convert {from_upper} effectively?</h3>
            <p>Simply drag and drop your file into the secure <strong>upload zone</strong> above. Our system will automatically detect the bitrate, resolution, and metadata of your {from_format} file. Once you click "Process," the magic happens. Your file is converted to {to_upper} format and then automatically downloaded back to your device.</p>
            
            <h3>Is this {title} converter safe?</h3>
            <p>Absolutely. <strong>ConvertRocket.online</strong> operates on a <em>Zero-Persistence</em> policy. Your {from_upper} file is strictly used for the conversion process and is wiped from our volatile memory immediately after you download the {to_upper} result. We use end-to-end SSL encryption to ensure your data is never intercepted.</p>

            <h3>Key Benefits:</h3>
            <ul>
                <li><strong>Lossless Conversion:</strong> We preserve the maximum metadata and quality during the {from_upper} to {to_upper} conversion.</li>
                <li><strong>No Signup:</strong> Start using the professional converter instantly. No email or registration required.</li>
                <li><strong>High Speed:</strong> Powered by our high-frequency clustered servers in the USA and Europe.</li>
                <li><strong>Universal:</strong> Optimized for Chrome, Safari, Firefox, and all mobile browsers.</li>
            </ul>
        </section>

        <footer class="resource-footer">
            <div style="text-align:center; opacity:0.3; font-size:0.8rem; letter-spacing:3px;">
                © 2026 CONVERTROCKET.ONLINE • ION PREMIUM V4.0
            </div>
        </footer>
    </div>

    <script>
        const API_BASE = '';
        const TARGET_FORMAT = '{to_format}';
        
        document.addEventListener('DOMContentLoaded', () => {{
            const zone = document.getElementById('upload-zone');
            const input = document.getElementById('file-input');
            const progress = document.getElementById('progress-container');
            const fill = document.getElementById('progress-fill');
            const perc = document.getElementById('progress-percent');
            const msg = document.getElementById('progress-message');
            const result = document.getElementById('result-container');
            const down = document.getElementById('download-link');
            const info = document.getElementById('file-info');
            
            input.addEventListener('change', async (e) => {{
                if (e.target.files.length === 0) return;
                const file = e.target.files[0];
                info.innerHTML = `<strong>File Identified:</strong> ` + file.name + ` (` + (file.size/1024/1024).toFixed(2) + ` MB)`;
                info.style.display = 'block';
                progress.classList.add('active');
                
                const formData = new FormData();
                formData.append('file', file);
                formData.append('target_format', TARGET_FORMAT);
                
                let p = 0;
                const interval = setInterval(() => {{
                    p = Math.min(p + Math.random() * 10, 96);
                    fill.style.width = p + '%';
                    perc.textContent = Math.round(p) + '%';
                    if(p > 40) msg.textContent = 'Laboratory Conversion...';
                    if(p > 80) msg.textContent = 'Finalizing Result...';
                }}, 400);

                try {{
                    const r = await fetch(API_BASE + '/api/convert/upload', {{ method: 'POST', body: formData }});
                    const d = await r.json();
                    clearInterval(interval);
                    if (d.success) {{
                        fill.style.width = '100%';
                        perc.textContent = '100%';
                        msg.textContent = 'Ready for Save!';
                        setTimeout(() => {{
                            progress.classList.remove('active');
                            result.style.display = 'block';
                            down.href = d.download_url;
                            down.click(); // Auto save
                        }}, 600);
                    }}
                }} catch (err) {{ 
                    alert('Error in Lab: ' + err.message); 
                    clearInterval(interval);
                    progress.classList.remove('active');
                }}
            }});
        
            // Sync Star
            const star = document.querySelector('.card-star');
            const url = '/{from_format}-to-{to_format}';
            const starred = JSON.parse(localStorage.getItem('starredTools') || '[]');
            if (starred.includes(url)) {{ star.textContent = '⭐'; star.classList.add('active'); }}
            else {{ star.textContent = '☆'; star.classList.remove('active'); }}
        }});

        function toggleThisStar(el, url) {{
            let starred = JSON.parse(localStorage.getItem('starredTools') || '[]');
            if (el.classList.contains('active')) {{
                el.classList.remove('active'); el.textContent = '☆';
                starred = starred.filter(u => u !== url);
            }} else {{
                el.classList.add('active'); el.textContent = '⭐';
                if(!starred.includes(url)) starred.push(url);
            }}
            localStorage.setItem('starredTools', JSON.stringify(starred));
        }}

        function copyResultLink() {{
            navigator.clipboard.writeText(window.location.href).then(() => alert('Link copied to laboratory clipboard!'));
        }}

        function bookmarkTool() {{
            alert('Press Ctrl+D to bookmark this tool!');
        }}
    </script>
</body>
</html>'''
    return filename, html

def main():
    output_dir = 'frontend'
    for cat, convs in CONVERTERS.items():
        for conv in convs:
            fname, html = generate_page(conv['from'], conv['to'], conv['desc'], conv['accepts'], conv.get('category', cat))
            with open(os.path.join(output_dir, fname), 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"ION V4 Generated: {{fname}}")

if __name__ == '__main__':
    main()

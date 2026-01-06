import os

# Define the template for specialized tools (ION V6)
TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-ZBZSYT7DRY"></script>
    <script>window.dataLayer = window.dataLayer || []; function gtag() {{ dataLayer.push(arguments); }} gtag('js', new Date()); gtag('config', 'G-ZBZSYT7DRY');</script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - ConvertRocket Laboratory</title>
    <meta name="description" content="{description}">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/ultra-minimalist.css?v=6.0">
    <script src="/static/js/minimalist-search.js" defer></script>
    <script src="/static/js/premium-features.js" defer></script>
</head>
<body>
    <div class="bg-animated"></div>
    <div class="container">
        <nav class="nav-premium">
            <div class="brand-premium" style="font-weight: 950; font-size: 1.5rem;"><a href="/" style="text-decoration:none; color:inherit;">🚀 ConvertRocket</a></div>
             <div class="nav-links" style="display: flex; gap: 20px; opacity: 0.6;">
                <a href="/blogs" style="color:white; text-decoration:none; font-size:0.9rem;">Guides</a>
            </div>
        </nav>

        <!-- Command Hub (Below Hero) -->
        <div class="hub-sticky-container">
            <div class="category-nav">
                <a href="/all-tools" class="cat-link"><span class="icon">🚀</span> All Units</a>
                <a href="/ai-lab" class="cat-link"><span class="icon">🪄</span> AI Lab</a>
                <a href="/media-hub" class="cat-link"><span class="icon">🎬</span> Media Hub</a>
                <a href="/pdf-lab" class="cat-link"><span class="icon">📄</span> PDF Lab</a>
                <a href="/dev-suite" class="cat-link"><span class="icon">💻</span> Dev Suite</a>
                <a href="/utilities" class="cat-link"><span class="icon">🛠️</span> Utilities</a>
                <a href="/downloader" class="cat-link"><span class="icon">⬇️</span> Downloader</a>
                <a href="/converter" class="cat-link"><span class="icon">🔄</span> Converter</a>
            </div>
        </div>

        <div class="converter-box">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:40px;">
                <h2 style="font-weight: 950; font-size: 2.2rem; margin:0;">{title_html}</h2>
                <div class="card-star" style="font-size:2rem; cursor:pointer;" onclick="toggleThisStar(this, '/{slug}')">☆</div>
            </div>

            <div class="upload-zone" id="upload-zone">
                <div class="upload-icon">{icon}</div>
                <p style="font-size: 1.4rem; font-weight: 800;">{action_text}</p>
                <p style="opacity: 0.5;">{sub_text}</p>
                <input type="file" id="file-input" {accept}>
            </div>

            <div id="tool-ui" style="display:none; margin-top:30px; text-align:left;">
                <!-- Dynamic UI injected by tool-specific JS -->
            </div>

            <div id="status-message" class="status-message"></div>
            
            <div id="result-container" style="display:none; margin-top:40px;">
                <div style="margin-bottom:20px; color:var(--neon-cyan); font-weight:900; letter-spacing:1px;">✅ OPERATION COMPLETE</div>
                <div style="display: flex; flex-direction: column; gap: 15px; align-items: center;">
                    <a href="#" id="download-link" class="action-btn" style="display:inline-block; text-decoration:none; width: 100%; text-align: center;" download>Save Result</a>
                    
                    <!-- Result Actions (Bookmark/Copy) -->
                    <div style="display: flex; gap: 10px; width: 100%;">
                        <button onclick="copyResultLink()" class="btn-tool" style="flex: 1; background: rgba(0, 242, 255, 0.1); color: var(--neon-cyan); border: 1px solid rgba(0, 242, 255, 0.2); padding: 12px; border-radius: 15px; font-weight: 700; cursor: pointer;">
                            🔗 Copy Link
                        </button>
                        <button onclick="bookmarkTool()" class="btn-tool" style="flex: 1; background: rgba(188, 19, 254, 0.1); color: var(--neon-purple); border: 1px solid rgba(188, 19, 254, 0.2); padding: 12px; border-radius: 15px; font-weight: 700; cursor: pointer;">
                            ⭐ Bookmark
                        </button>
                    </div>
                </div>
                <div class="bookmark-badge">🚀 Add tool to your browser lab (Ctrl+D)</div>
            </div>
        </div>

        <section class="seo-slop">
            <h2>{seo_title}</h2>
            <p>{seo_text}</p>
        </section>

        <footer class="resource-footer">
            <div style="text-align:center; opacity:0.3; font-size:0.8rem; letter-spacing:3px;">
                © 2026 CONVERTROCKET.ONLINE • LABORATORY MODULE
            </div>
        </footer>
    </div>

    <script>
        // Basic integration for local tools
        const fileInput = document.getElementById('file-input');
        const uploadZone = document.getElementById('upload-zone');
        const toolUi = document.getElementById('tool-ui');
        const status = document.getElementById('status-message');
        const result = document.getElementById('result-container');

        uploadZone.onclick = () => fileInput.click();
        
        fileInput.onchange = (e) => {{
            if (e.target.files.length > 0) {{
                uploadZone.style.display = 'none';
                toolUi.style.display = 'block';
                status.innerHTML = 'File loaded. Initializing {title}...';
                // Mock success for UI demo - backend handles real logic
                setTimeout(() => {{
                   status.innerHTML = '✅ Ready to process';
                }}, 1000);
            }}
        }};

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
        function copyResultLink() {{ navigator.clipboard.writeText(window.location.href).then(() => alert('Link copied!')); }}
        function bookmarkTool() {{ alert('Press Ctrl+D to bookmark!'); }}
    </script>
</body>
</html>'''

TOOLS = [
    {
        "slug": "insta-photo-down",
        "title": "Insta Saver",
        "title_html": "Insta <span style='color:var(--neon-pink)'>Saver</span>",
        "description": "Download Instagram photos and reels in high resolution.",
        "category": "Social Media Hub",
        "icon": "📸",
        "action_text": "Enter Instagram Link",
        "sub_text": "Public media extraction active",
        "accept": 'type="text" class="search-input"',
        "seo_title": "Instagram Media Extraction Laboratory",
        "seo_text": "Save beautiful memories from Instagram. Our tool extracts original resolution media from public links safely and securely."
    },
    {
        "slug": "tiktok-no-watermark",
        "title": "TikTok Pure",
        "title_html": "TikTok <span style='color:var(--neon-cyan)'>Pure</span>",
        "description": "Download TikTok videos without watermark in HD quality.",
        "category": "Social Media Hub",
        "icon": "🎵",
        "action_text": "Enter TikTok Link",
        "sub_text": "Watermark removal engine active",
        "accept": 'type="text" class="search-input"',
        "seo_title": "Pure TikTok Video Downloader",
        "seo_text": "Get TikTok videos without the distracting logo. Save videos directly to your camera roll in crystal clear quality."
    },
    {
        "slug": "pdf-to-text",
        "title": "PDF to Text",
        "title_html": "PDF to <span style='color:var(--neon-purple)'>Text</span>",
        "description": "Extract raw text data from PDF documents using OCR and stream parsing.",
        "category": "PDF Lab",
        "icon": "📄",
        "action_text": "Select PDF for Extraction",
        "sub_text": "Tesseract OCR engine active",
        "accept": 'accept=".pdf"',
        "seo_title": "PDF Text Extraction Laboratory",
        "seo_text": "Convert un-selectable PDF data into plain text instantly. Perfect for research, data entry, and archiving."
    }
]

# Create missing pages
output_dir = 'frontend'
for tool in TOOLS:
    file_path = os.path.join(output_dir, f"{tool['slug']}.html")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(TEMPLATE.format(**tool))
    print(f"Generated: {file_path}")

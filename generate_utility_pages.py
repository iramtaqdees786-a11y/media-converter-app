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

        <div class="breadcrumbs">
            <a href="/">Home</a> <span>/</span> {category} <span>/</span> {title}
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
        "slug": "qr-creator",
        "title": "QR Code Generator",
        "title_html": "QR <span style='color:var(--neon-cyan)'>Generator</span>",
        "description": "Create high-resolution QR codes for websites, WiFi, and business cards.",
        "category": "Utility Lab",
        "icon": "🏁",
        "action_text": "Enter Data for QR",
        "sub_text": "Neural QR generation engine active",
        "accept": 'type="text" placeholder="https://example.com" class="search-input"',
        "seo_title": "Professional QR Generation Engine",
        "seo_text": "Our QR generator creates surgical-grade matrix codes with error correction levels optimized for mobile scanning. Encrypt links, contact info, or plain text into high-fidelity SVG or PNG assets."
    },
    {
        "slug": "pdf-password",
        "title": "PDF Shield",
        "title_html": "PDF <span style='color:var(--neon-purple)'>Shield</span>",
        "description": "Protect your PDF files with military-grade encryption or remove existing passwords.",
        "category": "PDF Lab",
        "icon": "🔐",
        "action_text": "Select PDF to Secure",
        "sub_text": "GhostScript V8 Encryption active",
        "accept": 'accept=".pdf"',
        "seo_title": "Enterprise-Grade PDF Security",
        "seo_text": "Security is paramount. Our PDF Shield utilizes AES-256 bit encryption to lock your documents. We also offer a secure removal laboratory for authorized document unlocking."
    },
    {
        "slug": "base64-converter",
        "title": "Base64 Lab",
        "title_html": "Base64 <span style='color:var(--neon-pink)'>Laboratory</span>",
        "description": "Convert binary data to Base64 strings or decode back to original format.",
        "category": "Dev Lab",
        "icon": "🧬",
        "action_text": "Drop file or enter text",
        "sub_text": "Binary streamer active",
        "accept": '',
        "seo_title": "Advanced Base64 Encoding Engine",
        "seo_text": "Encode images, fonts, or raw data into data-uri strings for web optimization. Our lab handles massive payloads with zero-copy stream processing."
    },
    {
        "slug": "json-formatter",
        "title": "JSON Magician",
        "title_html": "JSON <span style='color:var(--neon-cyan)'>Magician</span>",
        "description": "Prettify, minify, and validate JSON structures instantly.",
        "category": "Dev Lab",
        "icon": "{}",
        "action_text": "Paste your JSON here",
        "sub_text": "Neural validation active",
        "accept": '',
        "seo_title": "Professional JSON Data Lab",
        "seo_text": "Developer efficiency is key. Format messy JSON into beautiful, readable structures or shrink them for production deployment."
    },
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
    },
    {
        "slug": "password-gen",
        "title": "Safe Entropy",
        "title_html": "Safe <span style='color:var(--neon-cyan)'>Entropy</span>",
        "description": "Generate military-grade secure passwords with high entropy.",
        "category": "Dev Lab",
        "icon": "🔑",
        "action_text": "Configure Entropy Settings",
        "sub_text": "Cryptographically secure random engine active",
        "accept": 'type="button" class="action-btn" value="Generate Password"',
        "seo_title": "High-Entropy Password Generator",
        "seo_text": "Protect your digital identity with non-guessable passwords. Custom lengths and character sets available."
    }
]

# Create missing pages
output_dir = 'frontend'
for tool in TOOLS:
    file_path = os.path.join(output_dir, f"{tool['slug']}.html")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(TEMPLATE.format(**tool))
    print(f"Generated: {file_path}")

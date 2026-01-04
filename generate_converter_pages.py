"""
Generate individual converter pages for maximum SEO keyword coverage
"""
import os

# Define all conversion types
CONVERTERS = {
    # Image conversions
    'image': [
        {'from': 'jpg', 'to': 'png', 'desc': 'Perfect for transparent backgrounds and lossless quality', 'accepts': '.jpg,.jpeg'},
        {'from': 'png', 'to': 'jpg', 'desc': 'Reduce file size while maintaining photo quality', 'accepts': '.png'},
        {'from': 'webp', 'to': 'jpg', 'desc': 'Convert modern WebP images to universal JPG format', 'accepts': '.webp'},
        {'from': 'webp', 'to': 'png', 'desc': 'Convert WebP to PNG for transparency support', 'accepts': '.webp'},
        {'from': 'jpg', 'to': 'webp', 'desc': 'Modern format with superior compression', 'accepts': '.jpg,.jpeg'},
        {'from': 'png', 'to': 'webp', 'desc': 'Reduce file size with next-gen WebP format', 'accepts': '.png'},
        {'from': 'heic', 'to': 'jpg', 'desc': 'Convert iPhone photos to universal JPG format', 'accepts': '.heic,.heif'},
        {'from': 'heic', 'to': 'png', 'desc': 'Convert iPhone photos to PNG with transparency', 'accepts': '.heic,.heif'},
        {'from': 'gif', 'to': 'mp4', 'desc': 'Convert animated GIFs to video for better quality', 'accepts': '.gif'},
        {'from': 'bmp', 'to': 'jpg', 'desc': 'Convert bitmap images to compressed JPG', 'accepts': '.bmp'},
        {'from': 'bmp', 'to': 'png', 'desc': 'Convert bitmap to PNG format', 'accepts': '.bmp'},
        {'from': 'tiff', 'to': 'jpg', 'desc': 'Convert high-quality TIFF to web-friendly JPG', 'accepts': '.tiff,.tif'},
        {'from': 'tiff', 'to': 'png', 'desc': 'Convert TIFF to PNG format', 'accepts': '.tiff,.tif'},
    ],
    # PDF conversions
    'pdf': [
        {'from': 'pdf', 'to': 'word', 'desc': 'Edit PDF content in Microsoft Word', 'accepts': '.pdf'},
        {'from': 'pdf', 'to': 'excel', 'desc': 'Extract tables and data to Excel spreadsheets', 'accepts': '.pdf'},
        {'from': 'word', 'to': 'pdf', 'desc': 'Convert Word documents to PDF format', 'accepts': '.doc,.docx'},
        {'from': 'excel', 'to': 'pdf', 'desc': 'Convert Excel spreadsheets to PDF', 'accepts': '.xls,.xlsx'},
        {'from': 'ppt', 'to': 'pdf', 'desc': 'Convert PowerPoint presentations to PDF', 'accepts': '.ppt,.pptx'},
        {'from': 'jpg', 'to': 'pdf', 'desc': 'Create PDF from JPG images', 'accepts': '.jpg,.jpeg', 'category': 'image'},
        {'from': 'png', 'to': 'pdf', 'desc': 'Create PDF from PNG images', 'accepts': '.png', 'category': 'image'},
    ],
    # Audio/Video conversions
    'media': [
        {'from': 'mp4', 'to': 'mp3', 'desc': 'Extract audio from MP4 videos', 'accepts': 'video/*'},
        {'from': 'mp4', 'to': 'avi', 'desc': 'Convert MP4 to AVI format', 'accepts': 'video/*'},
        {'from': 'mp4', 'to': 'mov', 'desc': 'Convert MP4 to QuickTime MOV', 'accepts': 'video/*'},
        {'from': 'avi', 'to': 'mp4', 'desc': 'Convert AVI to modern MP4 format', 'accepts': '.avi'},
        {'from': 'mov', 'to': 'mp4', 'desc': 'Convert QuickTime MOV to MP4', 'accepts': '.mov'},
        {'from': 'mkv', 'to': 'mp4', 'desc': 'Convert MKV to universal MP4', 'accepts': '.mkv'},
        {'from': 'webm', 'to': 'mp4', 'desc': 'Convert WebM to MP4 format', 'accepts': '.webm'},
        {'from': 'flv', 'to': 'mp4', 'desc': 'Convert Flash video to MP4', 'accepts': '.flv'},
        {'from': 'wav', 'to': 'mp3', 'desc': 'Compress WAV audio to MP3', 'accepts': '.wav'},
        {'from': 'mp3', 'to': 'wav', 'desc': 'Convert MP3 to uncompressed WAV', 'accepts': '.mp3'},
        {'from': 'flac', 'to': 'mp3', 'desc': 'Convert lossless FLAC to MP3', 'accepts': '.flac'},
        {'from': 'aac', 'to': 'mp3', 'desc': 'Convert AAC audio to MP3', 'accepts': '.aac'},
        {'from': 'm4a', 'to': 'mp3', 'desc': 'Convert M4A (iTunes) to MP3', 'accepts': '.m4a'},
    ]
}

def generate_page(from_format, to_format, description, accepts, category=''):
    """Generate HTML for a specific converter page"""
    
    from_upper = from_format.upper()
    to_upper = to_format.upper()
    title = f"{from_upper} to {to_upper}"
    filename = f"{from_format}-to-{to_format}.html"
    
    # Icon based on category
    if category == 'image' or any(fmt in ['jpg', 'png', 'webp', 'heic', 'gif', 'bmp', 'tiff'] for fmt in [from_format, to_format]):
        icon = '🖼️'
        cat_name = 'IMAGE'
    elif any(fmt in ['pdf', 'word', 'excel', 'ppt'] for fmt in [from_format, to_format]):
        icon = '📄'
        cat_name = 'DOCUMENT'
    elif any(fmt in ['mp4', 'avi', 'mov', 'mkv', 'webm', 'flv'] for fmt in [from_format, to_format]):
        icon = '🎬'
        cat_name = 'VIDEO'
    elif any(fmt in ['mp3', 'wav', 'flac', 'aac', 'm4a'] for fmt in [from_format, to_format]):
        icon = '🎵'
        cat_name = 'AUDIO'
    else:
        icon = '🔄'
        cat_name = 'CONVERTER'
    
    # Related converters (simple logic)
    related = []
    if from_format == 'jpg':
        related = [('png-to-jpg', 'PNG to JPG'), ('webp-to-jpg', 'WebP to JPG'), ('heic-to-jpg', 'HEIC to JPG')]
    elif from_format == 'png':
        related = [('jpg-to-png', 'JPG to PNG'), ('webp-to-png', 'WebP to PNG'), ('heic-to-png', 'HEIC to PNG')]
    elif from_format == 'webp':
        related = [('jpg-to-webp', 'JPG to WebP'), ('png-to-webp', 'PNG to WebP'), ('webp-to-jpg', 'WebP to JPG')]
    elif from_format == 'pdf':
        related = [('pdf-merge', 'Merge PDF'), ('pdf-compress', 'Compress PDF'), ('pdf-to-excel', 'PDF to Excel')]
    elif from_format == 'mp4':
        related = [('mp4-to-mp3', 'MP4 to MP3'), ('mp4-to-avi', 'MP4 to AVI'), ('mp4-to-mov', 'MP4 to MOV')]
    else:
        related = [('jpg-to-png', 'JPG to PNG'), ('png-to-jpg', 'PNG to JPG'), ('pdf-to-word', 'PDF to Word')]
    
    related_html = '\n'.join([
        f'''<a href="/{url}" style="padding: 15px; background: rgba(102, 126, 234, 0.1); border-radius: 8px; text-decoration: none; color: inherit;">
                    <strong>{name}</strong>
                    <p style="margin: 5px 0 0; font-size: 0.85rem; opacity: 0.8;">Quick convert</p>
                </a>'''
        for url, name in related
    ])
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-ZBZSYT7DRY"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}
        gtag('js', new Date());
        gtag('config', 'G-ZBZSYT7DRY');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <title>{title} Converter - Free Online | ConvertRocket</title>
    <meta name="description" content="Convert {from_upper} to {to_upper} free online. {description}. Fast, secure, and no signup required.">
    <meta name="keywords" content="{from_format} to {to_format}, {from_format} {to_format} converter, free {from_format} to {to_format}, online converter, convertrocket">
    <link rel="canonical" href="https://convertrocket.online/{from_format}-to-{to_format}">
    
    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title} Converter - Free & Fast">
    <meta property="og:description" content="Convert {from_upper} to {to_upper} instantly. 100% free, secure, and no signup needed.">
    
    <!-- Schema.org -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "name": "{title} Converter",
      "applicationCategory": "MultimediaApplication",
      "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "USD" }},
      "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "4.9", "ratingCount": "15000" }}
    }}
    </script>
    
    <link rel="stylesheet" href="/static/css/styles.min.css?v=2.3">
    <link rel="stylesheet" href="/static/css/mobile-optimizations.css?v=2.3">
    <style>
        .bookmark-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 12px;
            padding: 10px 16px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 8px;
            font-size: 0.9rem;
            color: var(--text-primary, #fff);
            transition: all 0.3s ease;
        }}
        .bookmark-badge:hover {{
            transform: translateY(-2px);
            border-color: rgba(102, 126, 234, 0.6);
        }}
        .seo-content {{
            margin-top: 60px;
            padding: 40px 20px;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }}
        @media (max-width: 768px) {{
            .seo-content {{ padding: 30px 15px; }}
            .hero-title {{ font-size: 2rem; }}
        }}
    </style>
</head>
<body>
    <div class="bg-animated"></div>
    
    <div class="top-bar">
        <div class="top-bar-content">
            <a href="/" style="text-decoration: none;">
                <div class="brand-small">🚀 <span>ConvertRocket</span></div>
            </a>
            <nav class="main-nav">
                <a href="/" class="nav-link">Home</a>
                <a href="/pdf-tools" class="nav-link">PDF Tools</a>
                <a href="/media-tools" class="nav-link">Media Tools</a>
                <a href="/blogs" class="nav-link">Blogs</a>
            </nav>
            <div class="top-bar-actions">
                <button class="share-btn" id="share-btn">📤 <span>Share</span></button>
            </div>
        </div>
    </div>
    
    <div class="container">
        <header class="header">
            <div class="free-label">🎉 100% FREE • NO SIGNUP</div>
            <h1 class="hero-title">
                <span class="hero-icon">{icon}</span>
                <span class="title-line1">{from_upper} TO {to_upper}</span>
                <span class="title-line2">{cat_name} CONVERTER</span>
            </h1>
            <p class="hero-subtitle">{description}</p>
        </header>
        
        <!-- Conversion Tool -->
        <div class="card">
            <div class="card-header">
                <div class="card-icon">🔄</div>
                <div>
                    <h2 class="card-title">Convert {from_upper} to {to_upper}</h2>
                    <p class="card-subtitle">Fast, secure, and completely free</p>
                </div>
            </div>
            
            <div class="upload-zone" id="upload-zone">
                <div class="upload-icon">{icon}</div>
                <p class="upload-text">Drop your {from_upper} file here or click to browse</p>
                <p class="upload-subtext">Supported: {from_upper}</p>
                <input type="file" id="file-input" accept="{accepts}" style="display: none;">
            </div>
            
            <div id="file-info" class="result-card" style="display: none;"></div>
            
            <div id="progress-container" class="progress-container" style="display: none;">
                <div class="progress-bar">
                    <div class="progress-fill" id="progress-fill"></div>
                </div>
                <div class="progress-text">
                    <span id="progress-message">Converting...</span>
                    <span class="progress-percent" id="progress-percent">0%</span>
                </div>
            </div>
            
            <div id="result-container" class="result-card" style="display: none;">
                <div class="result-header">
                    <div class="result-icon">✅</div>
                    <div>
                        <strong>Conversion Complete!</strong>
                        <div class="text-muted" id="result-filename"></div>
                    </div>
                </div>
                <a href="#" id="download-link" class="btn btn-success btn-block btn-lg" style="display: none;" download>
                    ⬇️ Download {to_upper}
                </a>
                <div class="bookmark-badge">
                    ⭐ Bookmark this tool – you'll need it again
                </div>
            </div>
            
            <div id="status-message" class="status-message"></div>
        </div>
        
        <!-- SEO Content (Below the tool) -->
        <div class="seo-content">
            <h2>Convert {from_upper} to {to_upper} Online Free</h2>
            <p>
                Our <strong>{from_format} to {to_format} converter</strong> is the fastest and easiest way to convert your files online. 
                {description}. Whether you're a designer, developer, or just need a quick conversion, our tool handles it all.
            </p>
            
            <h3>Why Use Our {title} Converter?</h3>
            <ul>
                <li><strong>100% Free:</strong> No hidden costs, no premium plans, completely free forever</li>
                <li><strong>No Signup Required:</strong> Start converting immediately without creating an account</li>
                <li><strong>Fast Processing:</strong> Lightning-fast conversions powered by optimized servers</li>
                <li><strong>Secure & Private:</strong> Files deleted immediately after conversion (within 1 hour)</li>
                <li><strong>Auto-Download:</strong> Your converted file downloads automatically at 100%</li>
            </ul>
            
            <h3>How to Convert {from_upper} to {to_upper}</h3>
            <ol>
                <li>Click or drag your {from_upper} file to the upload zone above</li>
                <li>Wait a few seconds while we convert it to {to_upper} format</li>
                <li>Your {to_upper} file downloads automatically - that's it!</li>
            </ol>
            
            <h3>Common Questions</h3>
            <p>
                <strong>Is it really free?</strong> Yes! We never charge for conversions. 
                <strong>Are my files safe?</strong> Absolutely. All uploads use HTTPS encryption and files are automatically deleted. 
                <strong>What's the file size limit?</strong> We support files up to 100MB for most formats.
            </p>
            
            <h3>Related Tools</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 20px;">
                {related_html}
            </div>
        </div>
        
        <footer class="footer">
            <div class="footer-brand">🚀 <span class="footer-logo">ConvertRocket</span></div>
            <p class="footer-tagline">The World's Fastest All-In-One Converter • 100% Free • No Signup</p>
            <div class="footer-links">
                <a href="/video-converter">Video Downloader</a> •
                <a href="/mp3-converter">MP3 Converter</a> •
                <a href="/pdf-tools">PDF Tools</a> •
                <a href="/image-converter">Image Tools</a>
            </div>
            <p class="copyright">© 2025 ConvertRocket.online - Fast & Private File Conversion</p>
        </footer>
    </div>
    
    <script>
        // Specific conversion handler
        const API_BASE = '';
        const TARGET_FORMAT = '{to_format}';
        const SOURCE_FORMAT = '{from_format}';
        
        document.addEventListener('DOMContentLoaded', () => {{
            const uploadZone = document.getElementById('upload-zone');
            const fileInput = document.getElementById('file-input');
            const fileInfo = document.getElementById('file-info');
            const progressContainer = document.getElementById('progress-container');
            const progressFill = document.getElementById('progress-fill');
            const progressPercent = document.getElementById('progress-percent');
            const progressMessage = document.getElementById('progress-message');
            const resultContainer = document.getElementById('result-container');
            const downloadLink = document.getElementById('download-link');
            const resultFilename = document.getElementById('result-filename');
            const statusMessage = document.getElementById('status-message');
            
            // Upload zone click
            uploadZone.addEventListener('click', () => fileInput.click());
            
            // Drag and drop
            uploadZone.addEventListener('dragover', (e) => {{
                e.preventDefault();
                uploadZone.classList.add('dragover');
            }});
            
            uploadZone.addEventListener('dragleave', () => {{
                uploadZone.classList.remove('dragover');
            }});
            
            uploadZone.addEventListener('drop', (e) => {{
                e.preventDefault();
                uploadZone.classList.remove('dragover');
                if (e.dataTransfer.files.length > 0) {{
                    handleFile(e.dataTransfer.files[0]);
                }}
            }});
            
            // File input change
            fileInput.addEventListener('change', (e) => {{
                if (e.target.files.length > 0) {{
                    handleFile(e.target.files[0]);
                }}
            }});
            
            // Share button
            const shareBtn = document.getElementById('share-btn');
            if (shareBtn) {{
                shareBtn.addEventListener('click', async () => {{
                    try {{
                        await navigator.clipboard.writeText(window.location.href);
                        shareBtn.innerHTML = '✅ <span>Copied!</span>';
                        setTimeout(() => {{
                            shareBtn.innerHTML = '📤 <span>Share</span>';
                        }}, 2000);
                    }} catch (err) {{
                        console.error('Share failed:', err);
                    }}
                }});
            }}
            
            async function handleFile(file) {{
                // Show file info
                const ext = file.name.split('.').pop().toLowerCase();
                fileInfo.innerHTML = `
                    <div class="result-header">
                        <div class="result-icon">{icon}</div>
                        <div>
                            <strong>${{escapeHtml(file.name)}}</strong>
                            <div class="text-muted">${{formatFileSize(file.size)}} • ${{ext.toUpperCase()}}</div>
                        </div>
                    </div>
                `;
                fileInfo.style.display = 'block';
                
                // Reset UI
                resultContainer.style.display = 'none';
                statusMessage.className = 'status-message';
                
                // Start conversion
                await convertFile(file);
            }}
            
            async function convertFile(file) {{
                progressContainer.style.display = 'block';
                progressMessage.textContent = 'Uploading...';
                
                const formData = new FormData();
                formData.append('file', file);
                formData.append('target_format', TARGET_FORMAT);
                
                // Simulate progress
                let progress = 0;
                const progressInterval = setInterval(() => {{
                    progress = Math.min(progress + Math.random() * 10, 90);
                    updateProgress(progress);
                }}, 300);
                
                try {{
                    const response = await fetch(`${{API_BASE}}/api/convert/upload`, {{
                        method: 'POST',
                        body: formData
                    }});
                    
                    clearInterval(progressInterval);
                    const data = await response.json();
                    
                    if (data.success) {{
                        // Show 100% completion
                        updateProgress(100);
                        progressMessage.textContent = 'Complete!';
                        
                        // Show result
                        setTimeout(() => {{
                            progressContainer.style.display = 'none';
                            resultContainer.style.display = 'block';
                            resultFilename.textContent = data.converted_file;
                            downloadLink.href = data.download_url;
                            downloadLink.download = data.converted_file;
                            downloadLink.style.display = 'block';
                            
                            // AUTO-DOWNLOAD - Downloads automatically without user clicking
                            setTimeout(() => {{
                                downloadLink.click();
                            }}, 500);
                        }}, 800);
                    }} else {{
                        throw new Error(data.message || 'Conversion failed');
                    }}
                }} catch (error) {{
                    clearInterval(progressInterval);
                    progressContainer.style.display = 'none';
                    showStatus(error.message || 'Something went wrong. Please try again!', 'error');
                }}
            }}
            
            function updateProgress(value) {{
                progressFill.style.width = `${{value}}%`;
                progressPercent.textContent = `${{Math.round(value)}}%`;
                if (value > 30) progressMessage.textContent = 'Converting...';
            }}
            
            function showStatus(message, type) {{
                statusMessage.className = `status-message active ${{type}}`;
                statusMessage.innerHTML = `<span>${{message}}</span>`;
                setTimeout(() => {{
                    statusMessage.classList.remove('active');
                }}, 5000);
            }}
            
            function formatFileSize(bytes) {{
                const units = ['B', 'KB', 'MB', 'GB'];
                let size = bytes;
                let unitIndex = 0;
                while (size >= 1024 && unitIndex < units.length - 1) {{
                    size /= 1024;
                    unitIndex++;
                }}
                return `${{size.toFixed(2)}} ${{units[unitIndex]}}`;
            }}
            
            function escapeHtml(text) {{
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }}
        }});
    </script>
</body>
</html>'''
    
    return filename, html

def main():
    """Generate all converter pages"""
    output_dir = 'frontend'
    os.makedirs(output_dir, exist_ok=True)
    
    generated_files = []
    
    for category, converters in CONVERTERS.items():
        for conv in converters:
            filename, html = generate_page(
                conv['from'], 
                conv['to'], 
                conv['desc'], 
                conv['accepts'],
                conv.get('category', category)
            )
            
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            
            generated_files.append(filename)
            print(f"[OK] Generated: {filename}")
    
    print(f"\n[SUCCESS] Generated {len(generated_files)} converter pages!")
    print("\nGenerated files:")
    for f in sorted(generated_files):
        print(f"  - {f}")
    
    # Generate sitemap entry list
    print("\n[SITEMAP] Add these to sitemap.xml:")
    for f in sorted(generated_files):
        url = f.replace('.html', '')
        print(f"    <url><loc>https://convertrocket.online/{url}</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>")

if __name__ == '__main__':
    main()

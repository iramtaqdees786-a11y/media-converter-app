"""
Generate individual converter pages for maximum SEO keyword coverage
WITH THE NEW PREMIUM ION THEME
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
    
    # Related tools logic
    related = []
    if from_format == 'jpg':
        related = [('png-to-jpg', 'PNG to JPG'), ('webp-to-jpg', 'WebP to JPG'), ('heic-to-jpg', 'HEIC to JPG')]
    elif from_format == 'png':
        related = [('jpg-to-png', 'JPG to PNG'), ('webp-to-png', 'WebP to PNG'), ('heic-to-png', 'HEIC to PNG')]
    elif from_format == 'pdf':
        related = [('pdf-to-word', 'PDF to Word'), ('pdf-to-excel', 'PDF to Excel'), ('pdf-compress', 'Compress PDF')]
    else:
        related = [('video-converter', 'Video Downloader'), ('mp3-converter', 'MP3 Converter'), ('ai-image-editor', 'AI Image Editor')]

    related_html = '\n'.join([
        f'''<a href="/{url}" class="tool-card" style="padding:15px; border-radius:15px;">
                    <div class="info"><h3>{name}</h3><p>Fast processing</p></div>
                </a>'''
        for url, name in related
    ])

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-ZBZSYT7DRY"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}
        gtag('js', new Date());
        gtag('config', 'G-ZBZSYT7DRY');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} Converter - Free & Fast | ConvertRocket</title>
    <meta name="description" content="Convert {from_upper} to {to_upper} for free. No signup, fast and secure file conversion laboratory.">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/ultra-minimalist.css?v=3.0">
    <script src="/static/js/minimalist-search.js" defer></script>
</head>
<body>
    <div class="bg-animated"></div>
    
    <section class="hero-minimal" style="padding: 80px 0 40px;">
        <div class="container">
            <h1><a href="/" style="text-decoration:none; color:inherit;">ConvertRocket</a></h1>
            <div class="search-wrapper">
                <input type="text" id="global-search" class="search-input" placeholder="Search other tools...">
                <div id="search-results" class="search-results"></div>
            </div>
        </div>
    </section>

    <div class="container">
        <div class="converter-box">
            <h2 style="margin-bottom: 30px; font-weight: 800; font-size: 2rem;">{from_upper} <span style="color:var(--neon-cyan)">→</span> {to_upper}</h2>
            
            <div class="upload-zone" id="upload-zone">
                <div class="icon">{icon}</div>
                <p style="font-size: 1.2rem; font-weight: 700;">Drop your {from_upper} file here</p>
                <p style="opacity: 0.5;">or click to select from your device</p>
                <input type="file" id="file-input" accept="{accepts}" style="display: none;">
            </div>

            <div id="file-info" style="display: none; margin-top: 30px; text-align: left; padding: 20px; border: 1px solid var(--glass-border); border-radius: 20px; background: rgba(255,255,255,0.02);"></div>
            
            <div id="progress-container" class="progress-container">
                <div class="progress-fill" id="progress-fill"></div>
                <div style="display:flex; justify-content:space-between; margin-top:10px; font-size:0.8rem; font-weight:700;">
                    <span id="progress-message">Preparing...</span>
                    <span id="progress-percent">0%</span>
                </div>
            </div>

            <div id="result-container" style="display: none; margin-top: 30px;">
                <div style="margin-bottom:20px; color:var(--neon-cyan); font-weight:800;">✅ CONVERSION SUCCESSFUL</div>
                <div id="result-filename" style="margin-bottom:20px; opacity:0.7;"></div>
                <a href="#" id="download-link" class="action-btn" style="display: inline-block; text-decoration:none;" download>Download {to_upper}</a>
            </div>

            <div id="status-message" class="status-message"></div>
        </div>

        <div class="tool-section">
            <div class="section-head"><h2>Related Lab Tools</h2></div>
            <div class="grid-tools">
                {related_html}
            </div>
        </div>

        <div class="tool-section" style="opacity:0.6; font-size: 0.9rem;">
            <h2>About {from_upper} to {to_upper} Conversion</h2>
            <p>ConvertRocket provides high-fidelity conversion from {from_upper} to {to_upper}. 
               Our cloud-based laboratory uses enterprise-grade engines to ensure every bit of your data is preserved. 
               100% Privacy - nothing is stored on our servers longer than 60 minutes.</p>
        </div>
    </div>

    <footer class="resource-footer">
        <div class="container">
            <div style="text-align:center; opacity:0.3; font-size:0.8rem; letter-spacing:2px;">
                © 2026 CONVERTROCKET • ALL-IN-ONE LABORATORY
            </div>
        </div>
    </footer>

    <script>
        const API_BASE = '';
        const TARGET_FORMAT = '{to_format}';
        
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
            
            uploadZone.addEventListener('click', () => fileInput.click());
            
            fileInput.addEventListener('change', (e) => {{
                if (e.target.files.length > 0) handleFile(e.target.files[0]);
            }});

            async function handleFile(file) {{
                fileInfo.innerHTML = `<strong>Selected:</strong> ` + file.name + ` (` + (file.size/1024/1024).toFixed(2) + ` MB)`;
                fileInfo.style.display = 'block';
                resultContainer.style.display = 'none';
                
                progressContainer.classList.add('active');
                progressMessage.textContent = 'Uploading...';
                
                const formData = new FormData();
                formData.append('file', file);
                formData.append('target_format', TARGET_FORMAT);
                
                let progress = 0;
                const progressInterval = setInterval(() => {{
                    progress = Math.min(progress + Math.random() * 10, 95);
                    progressFill.style.width = progress + '%';
                    progressPercent.textContent = Math.round(progress) + '%';
                    if(progress > 40) progressMessage.textContent = 'Processing in Lab...';
                }}, 400);
                
                try {{
                    const response = await fetch(API_BASE + '/api/convert/upload', {{
                        method: 'POST',
                        body: formData
                    }});
                    
                    clearInterval(progressInterval);
                    const data = await response.json();
                    
                    if (data.success) {{
                        progressFill.style.width = '100%';
                        progressPercent.textContent = '100%';
                        progressMessage.textContent = 'Ready!';
                        
                        setTimeout(() => {{
                            progressContainer.classList.remove('active');
                            resultContainer.style.display = 'block';
                            resultFilename.textContent = data.converted_file;
                            downloadLink.href = data.download_url;
                            downloadLink.click(); // Auto download
                        }}, 500);
                    }} else {{
                        throw new Error(data.message || 'Error occurred');
                    }}
                }} catch (error) {{
                    clearInterval(progressInterval);
                    statusMessage.textContent = 'Error: ' + error.message;
                    statusMessage.classList.add('active', 'error');
                }}
            }}
        }});
    </script>
</body>
</html>'''
    
    return filename, html

def main():
    output_dir = 'frontend'
    for category, converters in CONVERTERS.items():
        for conv in converters:
            filename, html = generate_page(conv['from'], conv['to'], conv['desc'], conv['accepts'], conv.get('category', category))
            with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Generated: {filename}")

if __name__ == '__main__':
    main()

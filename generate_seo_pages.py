"""
SEO-Optimized Page Generator for ConvertRocket
Generates aggressive SEO pages for all converter tools
"""

import os
import json

# Converter configurations with SEO data
CONVERTERS = [
    {
        "from_format": "pdf",
        "to_format": "word",
        "title": "PDF to Word Converter - Free Online DOCX 2026",
        "description": "Convert PDF to Word instantly. Preserve formatting, no quality loss. Free, no signup. Trusted by 500K+ users.",
        "primary_keyword": "pdf to word converter online free",
        "secondary_keywords": [
            "convert pdf to word without losing format",
            "pdf to docx converter free",
            "pdf to word converter no watermark",
            "free pdf to word 2026"
        ],
        "icon": "📄",
        "faq": [
            {
                "question": "Can I convert PDF to Word for free?",
                "answer": "Yes, 100% free. No hidden fees, no watermarks, no signup required. Convert unlimited PDF files to Word format."
            },
            {
                "question": "Will formatting be preserved?",
                "answer": "Yes, our converter preserves text formatting, images, tables, and layout structure from your PDF."
            },
            {
                "question": "Is it safe to convert PDF online?",
                "answer": "Completely safe. Files are encrypted during upload, processed securely, and automatically deleted after conversion."
            }
        ]
    },
    {
        "from_format": "pdf",
        "to_format": "excel",
        "title": "PDF to Excel Converter - Free Online XLSX 2026",
        "description": "Convert PDF to Excel spreadsheet. Extract tables accurately. Free, fast, no signup. 100K+ conversions daily.",
        "primary_keyword": "pdf to excel converter online free",
        "secondary_keywords": [
            "convert pdf to excel without losing format",
            "pdf to xlsx converter free",
            "extract tables from pdf to excel",
            "free pdf to excel 2026"
        ],
        "icon": "📊",
        "faq": [
            {
                "question": "Can I convert PDF tables to Excel?",
                "answer": "Yes, our converter accurately extracts tables from PDF and converts them to editable Excel spreadsheets."
            },
            {
                "question": "Will formulas be preserved?",
                "answer": "PDF files don't contain formulas, but our converter preserves all numerical data and table structure for you to add formulas in Excel."
            },
            {
                "question": "Is there a file size limit?",
                "answer": "No strict limit. We handle PDF files up to 50MB efficiently. Larger files may take slightly longer to process."
            }
        ]
    },
    {
        "from_format": "png",
        "to_format": "jpg",
        "title": "PNG to JPG Converter - Free Online No Quality Loss",
        "description": "Convert PNG to JPG instantly. Reduce file size, maintain quality. Free, no watermarks. 2M+ conversions monthly.",
        "primary_keyword": "png to jpg converter online free",
        "secondary_keywords": [
            "convert png to jpg without losing quality",
            "png to jpeg converter free",
            "reduce png file size to jpg",
            "batch png to jpg converter"
        ],
        "icon": "🖼️",
        "faq": [
            {
                "question": "Does PNG to JPG reduce quality?",
                "answer": "Our converter maintains maximum quality while reducing file size. JPG uses compression, but quality loss is minimal and imperceptible."
            },
            {
                "question": "Why convert PNG to JPG?",
                "answer": "JPG files are smaller than PNG, making them ideal for web upload, email attachments, and faster loading times."
            },
            {
                "question": "Can I convert transparent PNG?",
                "answer": "Yes, but JPG doesn't support transparency. Transparent areas will be replaced with white background."
            }
        ]
    },
    {
        "from_format": "webp",
        "to_format": "jpg",
        "title": "WebP to JPG Converter - Free Online 2026",
        "description": "Convert WebP to JPG instantly. Universal compatibility. Free, fast, no signup. Works on all devices.",
        "primary_keyword": "webp to jpg converter online free",
        "secondary_keywords": [
            "convert webp to jpg without losing quality",
            "webp to jpeg converter free",
            "batch webp to jpg converter",
            "free webp converter 2026"
        ],
        "icon": "🎨",
        "faq": [
            {
                "question": "What is WebP format?",
                "answer": "WebP is a modern image format developed by Google that provides superior compression. However, it's not universally supported, which is why conversion to JPG is often needed."
            },
            {
                "question": "Does WebP to JPG reduce quality?",
                "answer": "Our converter preserves maximum image quality during conversion. The output JPG will look identical to your original WebP image."
            },
            {
                "question": "Can I convert animated WebP?",
                "answer": "Yes, but JPG doesn't support animation. We'll convert the first frame of animated WebP to JPG."
            }
        ]
    },
    {
        "from_format": "mp4",
        "to_format": "mp3",
        "title": "MP4 to MP3 Converter - Free Audio Extractor 2026",
        "description": "Extract audio from MP4 videos. High-quality MP3 output. Free, fast, no watermarks. 1M+ conversions daily.",
        "primary_keyword": "mp4 to mp3 converter online free",
        "secondary_keywords": [
            "convert mp4 to mp3 high quality",
            "extract audio from mp4 free",
            "video to mp3 converter online",
            "mp4 to mp3 converter no watermark"
        ],
        "icon": "🎵",
        "faq": [
            {
                "question": "Can I extract audio from MP4 for free?",
                "answer": "Yes, 100% free. Upload your MP4 video and we'll extract the audio as high-quality MP3."
            },
            {
                "question": "What bitrate is the MP3?",
                "answer": "We extract audio at the original bitrate, up to 320kbps for maximum quality."
            },
            {
                "question": "Will video quality affect audio?",
                "answer": "No, we extract the original audio stream from your MP4 without re-encoding, preserving perfect quality."
            }
        ]
    }
]

# HTML Template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-ZBZSYT7DRY"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-ZBZSYT7DRY');</script>
    
    <!-- Meta Tags -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- SEO-Optimized Title & Description -->
    <title>{title} | ConvertRocket</title>
    <meta name="description" content="{description}">
    
    <!-- Keywords -->
    <meta name="keywords" content="{keywords}">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="https://www.convertrocket.online/{url_slug}">
    
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    
    <!-- Stylesheets -->
    <link rel="stylesheet" href="/css/seo-optimized.css?v=1.0">
    
    <!-- Structured Data: SoftwareApplication -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "name": "{from_upper} to {to_upper} Converter",
      "applicationCategory": "MultimediaApplication",
      "operatingSystem": "All",
      "offers": {{
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "USD"
      }},
      "aggregateRating": {{
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "ratingCount": "1250"
      }},
      "description": "{description}"
    }}
    </script>
    
    <!-- Structured Data: FAQ -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": {faq_schema}
    }}
    </script>
    
    <!-- Structured Data: HowTo -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "HowTo",
      "name": "How to Convert {from_upper} to {to_upper}",
      "description": "Step-by-step guide to convert {from_upper} to {to_upper} using our free online tool",
      "step": [
        {{
          "@type": "HowToStep",
          "name": "Upload {from_upper} File",
          "text": "Click the upload zone and select your {from_upper} file from your device"
        }},
        {{
          "@type": "HowToStep",
          "name": "Start Conversion",
          "text": "Click 'Convert to {to_upper}' button to begin the conversion process"
        }},
        {{
          "@type": "HowToStep",
          "name": "Download {to_upper}",
          "text": "Once complete, your {to_upper} file will automatically download to your device"
        }}
      ]
    }}
    </script>
</head>

<body>
    <!-- Navigation -->
    <nav class="nav-clean">
        <div class="container">
            <a href="/" class="brand-clean">
                <span class="brand-icon">🚀</span>
                <span>ConvertRocket</span>
            </a>
            <div class="nav-links">
                <a href="/all-tools">Tools</a>
                <a href="/blogs">Guides</a>
                <a href="/contact" class="nav-cta">Support</a>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-clean">
        <h1>{from_upper} to {to_upper} Converter</h1>
        <p class="hero-subtitle">Convert {from_upper} to {to_upper} instantly. Free, fast, no signup required.</p>
        
        <div class="trust-signals">
            <div class="trust-badge">
                <span>✓</span> 100% Free
            </div>
            <div class="trust-badge">
                <span>✓</span> No Watermark
            </div>
            <div class="trust-badge">
                <span>✓</span> Secure & Private
            </div>
            <div class="trust-badge">
                <span>✓</span> High Quality
            </div>
        </div>
    </section>

    <!-- Tool Interface -->
    <div class="tool-container">
        <div class="tool-card">
            <div class="tool-header">
                <h2 class="tool-title">{from_upper} <span class="arrow">→</span> {to_upper}</h2>
            </div>

            <!-- Upload Zone -->
            <div class="upload-zone" id="upload-zone">
                <div class="upload-icon">{icon}</div>
                <p>Click to Upload {from_upper} File</p>
                <small>or drag and drop your file here</small>
                <input type="file" id="file-input" accept=".{from_format}">
            </div>

            <!-- File Info -->
            <div class="file-info" id="file-info" style="display: none;">
                <div class="file-details" id="file-details"></div>
                <button class="action-btn" id="convert-btn">Convert to {to_upper}</button>
            </div>

            <!-- Progress Bar -->
            <div class="progress-container" id="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill" id="progress-fill"></div>
                </div>
                <div class="progress-info">
                    <span class="progress-message" id="progress-message">Initializing...</span>
                    <span class="progress-percent" id="progress-percent">0%</span>
                </div>
            </div>

            <!-- Result Container -->
            <div class="result-container" id="result-container">
                <div class="result-icon">✅</div>
                <h3 class="result-title">Conversion Complete!</h3>
                <p class="result-subtitle">Your {to_upper} file is ready to download</p>
                <a href="#" id="download-link" class="download-btn" download>Download {to_upper}</a>
                
                <div class="secondary-actions">
                    <button class="secondary-btn" onclick="location.reload()">Convert Another</button>
                    <button class="secondary-btn" onclick="copyLink()">📋 Copy Link</button>
                </div>
            </div>
        </div>
    </div>

    <!-- SEO Content Section -->
    <section class="seo-content">
        <h2>How to Convert {from_upper} to {to_upper} Online Free</h2>
        <p>Our <strong>{from_format} to {to_format} converter</strong> provides instant, high-quality conversions. Whether you need to convert files for compatibility, reduce file size, or change formats for specific applications, our tool delivers professional results in seconds.</p>

        <h3>Step 1: Upload Your {from_upper} File</h3>
        <p>Click the upload zone above and select your {from_upper} file from your device. You can also drag and drop files directly into the upload area.</p>

        <h3>Step 2: Start the Conversion</h3>
        <p>Once your file is uploaded, click the "Convert to {to_upper}" button. Our advanced conversion engine will process your file while preserving maximum quality.</p>

        <h3>Step 3: Download Your {to_upper}</h3>
        <p>After conversion completes (usually within seconds), your {to_upper} file will automatically download to your device.</p>

        <h2>Why Use Our {from_upper} to {to_upper} Converter?</h2>
        <ul>
            <li><strong>100% Free:</strong> No hidden fees, no watermarks, no file size limits</li>
            <li><strong>No Signup Required:</strong> Start converting immediately without creating an account</li>
            <li><strong>High Quality:</strong> Preserves maximum quality during conversion</li>
            <li><strong>Fast Processing:</strong> Most conversions complete in under 10 seconds</li>
            <li><strong>Secure & Private:</strong> Files automatically deleted after conversion</li>
            <li><strong>Works Everywhere:</strong> Compatible with all devices and browsers</li>
        </ul>

        <!-- FAQ Section -->
        <div class="faq-section">
            <h2>Frequently Asked Questions</h2>
            {faq_html}
        </div>
    </section>

    <!-- Related Tools -->
    <section class="related-tools">
        <h2>Related Converters</h2>
        <div class="tools-grid">
            {related_tools}
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer-clean">
        <div class="footer-links">
            <a href="/all-tools">All Tools</a>
            <a href="/blogs">Blog</a>
            <a href="/privacy-policy">Privacy</a>
            <a href="/terms-of-service">Terms</a>
            <a href="/sitemap">Sitemap</a>
            <a href="/contact">Contact</a>
        </div>
        <p class="footer-copyright">© 2026 ConvertRocket.online • Made by Izyaan</p>
    </footer>

    <!-- JavaScript -->
    <script>
        const API_BASE = '';
        const TARGET_FORMAT = '{to_format}';

        document.addEventListener('DOMContentLoaded', () => {{
            const uploadZone = document.getElementById('upload-zone');
            const fileInput = document.getElementById('file-input');
            const fileInfo = document.getElementById('file-info');
            const fileDetails = document.getElementById('file-details');
            const convertBtn = document.getElementById('convert-btn');
            const progressContainer = document.getElementById('progress-container');
            const progressFill = document.getElementById('progress-fill');
            const progressPercent = document.getElementById('progress-percent');
            const progressMessage = document.getElementById('progress-message');
            const resultContainer = document.getElementById('result-container');
            const downloadLink = document.getElementById('download-link');

            fileInput.addEventListener('change', (e) => {{
                if (e.target.files.length === 0) return;
                const file = e.target.files[0];
                
                fileDetails.innerHTML = `<strong>File:</strong> ${{file.name}} (${{(file.size/1024/1024).toFixed(2)}} MB)`;
                uploadZone.style.display = 'none';
                fileInfo.style.display = 'block';
            }});

            convertBtn.addEventListener('click', async () => {{
                const file = fileInput.files[0];
                if (!file) return;

                fileInfo.style.display = 'none';
                progressContainer.classList.add('active');

                const formData = new FormData();
                formData.append('file', file);
                formData.append('target_format', TARGET_FORMAT);

                let progress = 0;
                const interval = setInterval(() => {{
                    progress = Math.min(progress + Math.random() * 15, 95);
                    progressFill.style.width = progress + '%';
                    progressPercent.textContent = Math.round(progress) + '%';
                    
                    if (progress > 30) progressMessage.textContent = 'Converting...';
                    if (progress > 70) progressMessage.textContent = 'Finalizing...';
                }}, 300);

                try {{
                    const response = await fetch(API_BASE + '/api/convert/upload', {{
                        method: 'POST',
                        body: formData
                    }});
                    
                    const data = await response.json();
                    clearInterval(interval);

                    if (data.success) {{
                        progressFill.style.width = '100%';
                        progressPercent.textContent = '100%';
                        progressMessage.textContent = 'Complete!';

                        setTimeout(() => {{
                            progressContainer.classList.remove('active');
                            resultContainer.classList.add('active');
                            downloadLink.href = data.download_url;
                            downloadLink.click();
                        }}, 500);
                    }} else {{
                        alert('Conversion failed: ' + (data.message || 'Unknown error'));
                        location.reload();
                    }}
                }} catch (error) {{
                    clearInterval(interval);
                    alert('Error: ' + error.message);
                    location.reload();
                }}
            }});
        }});

        function copyLink() {{
            navigator.clipboard.writeText(window.location.href)
                .then(() => alert('Link copied to clipboard!'));
        }}
    </script>
</body>
</html>
"""

def generate_faq_schema(faq_items):
    """Generate FAQ schema JSON"""
    schema_items = []
    for item in faq_items:
        schema_items.append({
            "@type": "Question",
            "name": item["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": item["answer"]
            }
        })
    return json.dumps(schema_items, indent=6)

def generate_faq_html(faq_items):
    """Generate FAQ HTML"""
    html = ""
    for item in faq_items:
        html += f"""
            <div class="faq-item">
                <h3 class="faq-question">{item["question"]}</h3>
                <p class="faq-answer">{item["answer"]}</p>
            </div>
"""
    return html

def generate_related_tools(current_converter, all_converters):
    """Generate related tools HTML"""
    html = ""
    count = 0
    for conv in all_converters:
        if conv == current_converter or count >= 6:
            continue
        
        url_slug = f"{conv['from_format']}-to-{conv['to_format']}"
        html += f"""
            <a href="/{url_slug}" class="tool-link">
                <div class="tool-link-icon">{conv['icon']}</div>
                <h3 class="tool-link-title">{conv['from_format'].upper()} to {conv['to_format'].upper()}</h3>
                <p class="tool-link-desc">Convert {conv['from_format'].upper()} to {conv['to_format'].upper()} format</p>
            </a>
"""
        count += 1
    
    return html

def generate_page(converter, all_converters):
    """Generate a single converter page"""
    url_slug = f"{converter['from_format']}-to-{converter['to_format']}"
    keywords = f"{converter['primary_keyword']}, " + ", ".join(converter['secondary_keywords'])
    
    faq_schema = generate_faq_schema(converter['faq'])
    faq_html = generate_faq_html(converter['faq'])
    related_tools = generate_related_tools(converter, all_converters)
    
    html = HTML_TEMPLATE.format(
        title=converter['title'],
        description=converter['description'],
        keywords=keywords,
        url_slug=url_slug,
        from_format=converter['from_format'],
        to_format=converter['to_format'],
        from_upper=converter['from_format'].upper(),
        to_upper=converter['to_format'].upper(),
        icon=converter['icon'],
        faq_schema=faq_schema,
        faq_html=faq_html,
        related_tools=related_tools
    )
    
    return url_slug, html

def main():
    """Generate all converter pages"""
    output_dir = "frontend"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("🚀 Generating SEO-Optimized Converter Pages...")
    print("=" * 60)
    
    for converter in CONVERTERS:
        url_slug, html = generate_page(converter, CONVERTERS)
        filename = f"{url_slug}.html"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Generated: {filename}")
        print(f"   Primary Keyword: {converter['primary_keyword']}")
        print(f"   URL: /{url_slug}")
        print()
    
    print("=" * 60)
    print(f"✨ Successfully generated {len(CONVERTERS)} SEO-optimized pages!")
    print("\nNext Steps:")
    print("1. Review generated pages for accuracy")
    print("2. Test conversion functionality")
    print("3. Submit sitemap to Google Search Console")
    print("4. Monitor rankings in Google Analytics")

if __name__ == "__main__":
    main()

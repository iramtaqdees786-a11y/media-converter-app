"""
ConvertRocket SEO Configuration
Domain: convertrocket.online
"""

SEO_METADATA = {
    "/pdf-to-excel": {
        "title": "Convert PDF Table to Excel Online [YEAR] | Fast, Free, No Signup",
        "description": "Extract data tables from PDF to XLSX instantly. Best free tool for accurate PDF table extraction in [YEAR].",
        "keywords": "pdf to excel, pdf to xlsx, extract tables from pdf, convert pdf to excel free",
        "h1": "PDF to EXCEL Converter",
        "quick_guide": [
            "Upload your PDF document to the converter.",
            "Choose Excel (.xlsx) as the target format.",
            "Wait for the neural extraction engine to process the tables.",
            "Download your perfectly formatted Excel spreadsheet."
        ]
    },
    "/video-converter": {
        "title": "Fast Online Video Converter [YEAR] | All Formats Supported",
        "description": "Convert MP4, MOV, AVI, and more in [YEAR]. Lightning-fast browser-based video conversion.",
        "keywords": "video converter, mp4 converter, mov to mp4, avi to mp4, online video converter",
        "h1": "Online Video Converter",
        "quick_guide": [
            "Select your video file from your device.",
            "Pick your desired output format (MP4, MKV, etc.).",
            "Click Initialize Conversion to start the process.",
            "Download your converted video once complete."
        ]
    },
    "/json-formatter": {
        "title": "Best JSON Formatter & Validator Online [YEAR] | Pretty Print JSON",
        "description": "Format, validate, and beautify JSON data instantly in [YEAR]. Pro-grade JSON tool for developers.",
        "keywords": "json formatter, json validator, pretty print json, format json online",
        "h1": "JSON Formatter & Validator",
        "quick_guide": [
            "Paste your JSON code into the editor box.",
            "Click the 'Format' button to beautify the structure.",
            "The validator will highlight any syntax errors instantly.",
            "Copy your clean JSON or download it as a file."
        ]
    },
    "/image-converter": {
        "title": "Bulk Image Converter [YEAR] | JPG, PNG, WebP | Free Online",
        "description": "Convert images between any format in bulk in [YEAR]. Fast, secure, and high-quality image conversion.",
        "keywords": "image converter, jpg to png, png to webp, webp to jpg, bulk image conversion",
        "h1": "Professional Image Converter",
        "quick_guide": [
            "Drop your images into the upload zone.",
            "Select the target image format for conversion.",
            "Adjust quality settings if necessary.",
            "Download your converted images as a ZIP archive."
        ]
    },
    "/mp3-converter": {
        "title": "Fast Audio & MP3 Converter [YEAR] | High Quality",
        "description": "Convert any audio or video file to MP3, WAV, or AAC in [YEAR]. Crystal clear sound quality.",
        "keywords": "mp3 converter, youtube to mp3, wav to mp3, audio converter online",
        "h1": "Audio & MP3 Converter",
        "quick_guide": [
            "Select the audio or video file you want to convert.",
            "Choose MP3 or your preferred audio format.",
            "The extraction engine will process the audio in HQ.",
            "Download your new audio file instantly."
        ]
    },
    "/qr-generator": {
        "title": "Free QR Code Generator [YEAR] | Custom QR Codes Instantly",
        "description": "Generate high-quality QR codes for URLs and text in [YEAR]. Customizable and free to use.",
        "keywords": "qr code generator, create qr code, free qr code, qr generator online",
        "h1": "QR Code Generator",
        "quick_guide": ["Enter text or URL", "Customize style", "Download QR code"]
    },
    "/pdf-merge": {
        "title": "Merge PDF Files Online [YEAR] | Combined PDF Free & Fast",
        "description": "Combine multiple PDF documents into one in [YEAR]. High-speed, secure PDF merging tool.",
        "keywords": "merge pdf, combine pdf files, join pdf, free pdf joiner",
        "h1": "Merge PDF Documents"
    },
    "/pdf-compress": {
        "title": "Compress PDF Online [YEAR] | Reduce PDF File Size High Quality",
        "description": "Shrink PDF file size without losing quality in [YEAR]. Smallest PDF compression tool online.",
        "keywords": "compress pdf, reduce pdf size, shrink pdf, smallpdf alternative",
        "h1": "Compress PDF Files"
    },
    "/heic-to-jpg": {
        "title": "HEIC to JPG Converter Online [YEAR] | Convert iPhone Photos Free",
        "description": "Convert HEIC images to high-quality JPG in [YEAR]. Fast bulk conversion for iPhone HEIF photos.",
        "keywords": "heic to jpg, convert heic to jpg, iphone photo converter, heic to jpeg",
        "h1": "HEIC to JPG Converter"
    },
    "/bg-remover": {
        "title": "AI Background Remover [YEAR] | Remove Image BG Instantly Free",
        "description": "Transparent background maker using AI. Professional edge isolation in [YEAR]. Best free alternative to Adobe Express.",
        "keywords": "background remover, remove bg, transparent background, ai bg remover",
        "h1": "AI Background Remover"
    }
}

FAQ_DATA = {
    "/pdf-to-excel": [
        {"q": "Is this PDF to Excel converter free to use?", "a": "Yes, ConvertRocket provides a 100% free PDF to Excel conversion tool without any hidden costs or signups."},
        {"q": "Will my PDF table formatting be preserved?", "a": "Absolutely. Our neural extraction engine is designed to recognize and preserve complex table structures accurately."},
        {"q": "Are my files safe after conversion?", "a": "Your security is our priority. All files are processed on secure servers and automatically deleted within 60 minutes."}
    ],
    "/video-converter": [
        {"q": "Which video formats are supported?", "a": "We support all major formats including MP4, MKV, WebM, AVI, MOV, and many more."},
        {"q": "Can I convert large video files?", "a": "Yes, our high-speed edge nodes can handle large video files efficiently without quality loss."},
        {"q": "Do I need to install any software?", "a": "No, ConvertRocket is a browser-based tool that works on any device without installation."}
    ],
    "/bg-remover": [
        {"q": "Is the background removal actually free?", "a": "Yes, our AI background remover is 100% free with no watermarks or registrations required."},
        {"q": "How accurate is the AI isolation?", "a": "Our models are trained on millions of images to provide hair-level precision for complex subjects."},
        {"q": "Where are my images processed?", "a": "Processing happens entirely in your browser using WebAssembly. Your photos never leave your computer."}
    ]
}

DEFAULT_METADATA = {
    "title": "ConvertRocket | Ultimate Free Online File Converter [YEAR]",
    "description": "The fastest way to download videos & convert files online in [YEAR]. 100% Free! Supports PDF, Video, Audio, Images, and more.",
    "keywords": "file converter, video downloader, pdf converter, mp3 converter, online tools, free converter 2026",
    "h1": "Fastest Online File Converter"
}

def get_software_schema(path, metadata):
    """Generate SoftwareApplication JSON-LD schema."""
    return {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": metadata.get("h1", "ConvertRocket Tool"),
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "All",
        "url": f"https://www.convertrocket.online{path}",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "ratingCount": "1250"
        },
        "description": metadata.get("description", "").replace("[YEAR]", "2026")
    }

def get_faq_schema(path):
    """Generate FAQPage JSON-LD schema from FAQ_DATA."""
    faqs = FAQ_DATA.get(path, [])
    if not faqs:
        return None
        
    entities = []
    for faq in faqs:
        entities.append({
            "@type": "Question",
            "name": faq["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["a"]
            }
        })
        
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }

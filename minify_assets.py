"""
Minify CSS and JS files for better performance
"""
import re
import os

def minify_css(css_content):
    """Basic CSS minification"""
    # Remove comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    # Remove whitespace
    css_content = re.sub(r'\s+', ' ', css_content)
    # Remove spaces around special characters
    css_content = re.sub(r'\s*([{}:;,>+~])\s*', r'\1', css_content)
    # Remove trailing semicolons
    css_content = re.sub(r';}', '}', css_content)
    return css_content.strip()

def minify_js(js_content):
    """Basic JS minification - removes comments and extra whitespace"""
    # Remove single-line comments (but preserve URLs)
    js_content = re.sub(r'(?<!:)//.*?$', '', js_content, flags=re.MULTILINE)
    # Remove multi-line comments
    js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
    # Remove extra whitespace
    js_content = re.sub(r'\n\s*\n', '\n', js_content)
    js_content = re.sub(r'  +', ' ', js_content)
    return js_content.strip()

# Minify CSS files
css_files = [
    'frontend/css/styles.css',
    'frontend/css/mobile-optimizations.css',
    'frontend/css/styles-append.css',
    'frontend/css/seo-hacks.css'
]

for css_file in css_files:
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        minified = minify_css(content)
        output_file = css_file.replace('.css', '.min.css')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(minified)
        
        original_size = len(content)
        minified_size = len(minified)
        savings = ((original_size - minified_size) / original_size) * 100
        
        print(f"✓ {css_file}")
        print(f"  Original: {original_size:,} bytes")
        print(f"  Minified: {minified_size:,} bytes")
        print(f"  Savings: {savings:.1f}%\n")

# Minify JS files
js_files = [
    'frontend/js/app.js',
    'frontend/js/i18n.js',
    'frontend/js/media-tools.js',
    'frontend/js/pdf-tools.js',
    'frontend/js/seo-hacks.js'
]

for js_file in js_files:
    if os.path.exists(js_file):
        with open(js_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        minified = minify_js(content)
        output_file = js_file.replace('.js', '.min.js')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(minified)
        
        original_size = len(content)
        minified_size = len(minified)
        savings = ((original_size - minified_size) / original_size) * 100
        
        print(f"✓ {js_file}")
        print(f"  Original: {original_size:,} bytes")
        print(f"  Minified: {minified_size:,} bytes")
        print(f"  Savings: {savings:.1f}%\n")

print("✅ All files minified successfully!")

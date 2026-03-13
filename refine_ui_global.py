import os
import glob
import re

frontend_dir = r'c:\Users\Lenovo-T470-0027\.gemini\antigravity\scratch\media-converter-app\frontend'
html_files = glob.glob(os.path.join(frontend_dir, '**/*.html'), recursive=True)

def refine_page(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False

    # 1. Remove YouTube Thumbnail Downloader
    # Pattern for bento-unit cards
    thumbnail_patterns = [
        r'(?s)<a href="/yt-thumbnail".*?</a>',
        r'<li><a href="/yt-thumbnail".*?</li>',
        r'(?s)<div class="interactive-card".*?/yt-thumbnail.*?</div>'
    ]
    for pattern in thumbnail_patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, "", content)
            changed = True

    # 2. Adjust Heading Alignment (Shift Right)
    # Target specific headings
    headings_to_shift = [
        "01. Media Intelligence Lab",
        "01. MEDIA INTELLIGENCE LAB",
        "02. PDF Command Center",
        "02. PDF COMMAND CENTER",
        "03. Image Forge Lab",
        "03. IMAGE FORGE LAB",
        "Complete Tools Matrix"
    ]
    
    for h_text in headings_to_shift:
        # Search for h2 containing this text and add padding-left if not already there
        pattern = f'(<h2[^>]*style="[^"]*)(font-size: 1.5rem;)([^"]*">\\s*{h_text})'
        if re.search(pattern, content):
            content = re.sub(pattern, r'\1padding-left: 20px; \2\3', content)
            changed = True
        elif f">{h_text}</h2>" in content:
            # Case where there's no style tag or different style
            content = content.replace(f">{h_text}</h2>", f' style="padding-left: 20px;">{h_text}</h2>')
            changed = True

    # Subheading for Matrix
    subheading_text = "Access every specialized endpoint directly."
    if subheading_text in content:
        content = content.replace(f">{subheading_text}</p>", f' style="padding-left: 20px; color: var(--text-secondary);">{subheading_text}</p>')
        changed = True

    # 3. Ko-fi Widget Fixes (Positioning & Preload)
    # The white box on the left is the overlay. We need to force it right.
    kofi_css_patch = """
      /* Forced Right Position for Ko-fi Overlay & Container */
      #kofi-widget-overlay, 
      .floatingchat-container,
      .floatingchat-container-wrap,
      .kofichat-container,
      .kofichat-container-small,
      .floating-chat-kofi-popup-iframe,
      .floatingchat-container-wrap-mobi {
          right: 20px !important;
          left: auto !important;
          margin-left: 0 !important;
      }
    """
    
    if "/* Force Right Position for Ko-fi Container */" in content:
        # Update existing patch
        content = content.replace("/* Force Right Position for Ko-fi Container */", "/* Forced Right Position for Ko-fi Overlay & Container */")
        content = content.replace("right: 20px !important;", "right: 20px !important;\n          left: auto !important;\n          margin-left: 0 !important;")
        changed = True
    elif "<!-- Ko-fi Floating Widget -->" in content:
        # Inject into the existing style block if found
        style_pattern = r'(?s)(<!-- Ko-fi Floating Widget -->.*?<style>)(.*?)(</style>)'
        if re.search(style_pattern, content):
            content = re.sub(style_pattern, rf'\1\2{kofi_css_patch}\3', content)
            changed = True

    # Address Preload Warnings
    # Remove any rel="preload" for Ko-fi that might be causing warnings if they don't have 'as' or are unused
    preload_pattern = r'<link rel="preload" [^>]*ko-fi\.com[^>]*>'
    if re.search(preload_pattern, content):
        content = re.sub(preload_pattern, "", content)
        changed = True

    if changed:
        # Cleanup extra whitespace from removals
        content = re.sub(r'\n{3,}', '\n\n', content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Run the refinement
optimized_count = 0
for file in html_files:
    if refine_page(file):
        optimized_count += 1
        print(f"Refined: {os.path.relpath(file, frontend_dir)}")

print(f"Refinement complete. Total pages updated: {optimized_count}")

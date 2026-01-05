/* Global Search Logic for ConvertRocket - Tolerant & Dynamic */

const tools = [
    // Video & Audio
    { name: 'Video Converter', url: '/video-converter', cat: 'Video', icon: '📽️', keywords: 'mp4 mkv avi mov webm download' },
    { name: 'MP3 Converter', url: '/mp3-converter', cat: 'Audio', icon: '🎵', keywords: 'audio music sound extract download' },
    { name: 'MP4 to MP3', url: '/mp4-to-mp3', cat: 'Audio', icon: '🎶', keywords: 'extract audio high quality' },
    { name: 'Video Trimmer', url: '/video-trimmer', cat: 'Video', icon: '✂️', keywords: 'cut clip crop edit' },
    { name: 'YouTube Downloader', url: '/video-converter', cat: 'Video', icon: '▶️', keywords: 'yt download mp3 mp4 4k' },
    { name: 'TikTok Downloader', url: '/video-converter', cat: 'Video', icon: '📱', keywords: 'save video no watermark' },
    { name: 'Instagram Downloader', url: '/video-converter', cat: 'Video', icon: '📸', keywords: 'reels igtv stories' },

    // PDF & Docs
    { name: 'PDF Compressor', url: '/pdf-compress', cat: 'PDF', icon: '📦', keywords: 'shrink small resize optimize' },
    { name: 'PDF to Word', url: '/pdf-to-word', cat: 'PDF', icon: '📄', keywords: 'edit docx document' },
    { name: 'PDF to Excel', url: '/pdf-to-excel', cat: 'PDF', icon: '📊', keywords: 'data spreadsheet xlsx table' },
    { name: 'Merge PDFs', url: '/pdf-merge', cat: 'PDF', icon: '🔗', keywords: 'combine join connect' },
    { name: 'Remove PDF Pages', url: '/pdf-remove-pages', cat: 'PDF', icon: '🗑️', keywords: 'delete extract' },
    { name: 'PDF to Grayscale', url: '/pdf-grayscale', cat: 'PDF', icon: '🌑', keywords: 'black and white b&w' },
    { name: 'PDF to PDF/A', url: '/pdf-pdfa', cat: 'PDF', icon: '🏛️', keywords: 'archive long term' },

    // Images
    { name: 'Image Converter', url: '/image-converter', cat: 'Image', icon: '🖼️', keywords: 'png jpg webp bmp transform' },
    { name: 'Image Compressor', url: '/image-compress', cat: 'Image', icon: '🗜️', keywords: 'shrink small quality resize' },

    // AI Tools (Prominent)
    { name: 'AI Image Editor', url: '/ai-image-editor', cat: 'AI Feature', icon: '🎨', keywords: 'ai rewrite enhance background remove beauty magic edit', ai: true },
    { name: 'AI Face Blur', url: '/ai-image-editor', cat: 'AI Feature', icon: '👤', keywords: 'anonymous privacy hide face', ai: true },
    { name: 'AI Background Remover', url: '/ai-image-editor', cat: 'AI Feature', icon: '🪄', keywords: 'transparency cut out mask', ai: true },

    // Formats
    { name: 'HEIC to JPG', url: '/heic-to-jpg', cat: 'Image', icon: '📸', keywords: 'iphone photo apple' },
    { name: 'WebP to PNG', url: '/webp-to-png', cat: 'Image', icon: '🕸️', keywords: 'google image transparency' },
    { name: 'SVG to PNG', url: '/image-converter', cat: 'Image', icon: '📐', keywords: 'vector vectorization' },

    // Core Utilities (V7 Sync)
    { name: 'PDF Shield', url: '/pdf-password', cat: 'PDF', icon: '🔐', keywords: 'lock security encrypt' },
    { name: 'Base64 Lab', url: '/base64-converter', cat: 'Dev', icon: '🧬', keywords: 'encode decode binary' },
    { name: 'JSON Magician', url: '/json-formatter', cat: 'Dev', icon: '{}', keywords: 'pretty minify validate' },
    { name: 'PDF to Text', url: '/pdf-to-text', cat: 'PDF', icon: '📄', keywords: 'txt extract ocr' }
];

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('global-search');
    const resultsDiv = document.getElementById('search-results');

    if (!searchInput || !resultsDiv) return;

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        if (query.length < 1) {
            resultsDiv.classList.remove('active');
            return;
        }

        const queryWords = query.split(/\s+/);

        const filtered = tools.filter(t => {
            const searchStr = `${t.name} ${t.cat} ${t.keywords}`.toLowerCase();
            return queryWords.every(word => searchStr.includes(word));
        });

        if (filtered.length > 0) {
            resultsDiv.innerHTML = filtered.map(t => `
                <a href="${t.url}" class="search-item">
                    <span class="search-item-icon">${t.icon}</span>
                    <div class="search-item-info">
                        <span class="search-item-name">${t.name} ${t.ai ? '<span class="badge-ai">AI</span>' : ''}</span>
                        <span class="search-item-cat">${t.cat}</span>
                    </div>
                </a>
            `).join('');
            resultsDiv.classList.add('active');
        } else {
            resultsDiv.innerHTML = '<div class="search-item" style="opacity:0.5; padding:30px; text-align:center;">No tools found matching your search. <br>Try different keywords!</div>';
            resultsDiv.classList.add('active');
        }
    });

    // Close on click outside
    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !resultsDiv.contains(e.target)) {
            resultsDiv.classList.remove('active');
        }
    });

    // Hotkey for search
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            searchInput.focus();
        }
    });
});

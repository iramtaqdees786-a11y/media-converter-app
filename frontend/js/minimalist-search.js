/* Global Search Logic for ConvertRocket - Tolerant & Dynamic */

const tools = [
    // Video & Audio
    { name: 'Video Converter', url: '/converter', cat: 'Converter', icon: '📽️', keywords: 'mp4 mkv avi mov webm download' },
    { name: 'MP3 Converter', url: '/converter', cat: 'Converter', icon: '🎵', keywords: 'audio music sound extract download' },
    { name: 'MP4 to MP3', url: '/mp4-to-mp3', cat: 'Audio', icon: '🎶', keywords: 'extract audio high quality' },
    { name: 'Video Trimmer', url: '/video-trimmer', cat: 'Video', icon: '✂️', keywords: 'cut clip crop edit' },
    { name: 'YouTube Downloader', url: '/downloader', cat: 'Downloader', icon: '▶️', keywords: 'yt download mp3 mp4 4k' },
    { name: 'TikTok Downloader', url: '/downloader', cat: 'Downloader', icon: '📱', keywords: 'save video no watermark' },
    { name: 'Instagram Downloader', url: '/downloader', cat: 'Downloader', icon: '📸', keywords: 'reels igtv stories' },

    // PDF & Docs
    { name: 'PDF Compressor', url: '/pdf-compress', cat: 'PDF', icon: '📦', keywords: 'shrink small resize optimize' },
    { name: 'PDF to Word', url: '/pdf-to-word', cat: 'PDF', icon: '📄', keywords: 'edit docx document' },
    { name: 'PDF to Excel', url: '/pdf-to-excel', cat: 'PDF', icon: '📊', keywords: 'data spreadsheet xlsx table' },
    { name: 'Merge PDFs', url: '/pdf-merge', cat: 'PDF', icon: '🔗', keywords: 'combine join connect' },
    { name: 'Remove PDF Pages', url: '/pdf-remove-pages', cat: 'PDF', icon: '🗑️', keywords: 'delete extract' },
    { name: 'PDF to Grayscale', url: '/pdf-grayscale', cat: 'PDF', icon: '🌑', keywords: 'black and white b&w' },
    { name: 'PDF to PDF/A', url: '/pdf-pdfa', cat: 'PDF', icon: '🏛️', keywords: 'archive long term' },
    { name: 'PDF to Text', url: '/pdf-to-text', cat: 'PDF', icon: '📄', keywords: 'txt extract ocr' },

    // Images
    { name: 'Image Converter', url: '/image-converter', cat: 'Image', icon: '🖼️', keywords: 'png jpg webp bmp transform' },
    { name: 'EXIF Strip', url: '/exif-remover', cat: 'Media', icon: '🕵️', keywords: 'privacy metadata remover clean' },

    // AI Tools (Prominent)
    { name: 'AI Image Editor', url: '/ai-image-editor', cat: 'AI Feature', icon: '🎨', keywords: 'ai background remove magic edit', ai: true },
    { name: 'AI Background Remover', url: '/ai-image-editor', cat: 'AI Feature', icon: '🪄', keywords: 'transparency cut out mask', ai: true },

    // Hubs
    { name: 'Cloud Downloader', url: '/downloader', cat: 'Hub', icon: '⬇️', keywords: 'yt tiktok social save' },
    { name: 'Universal Converter', url: '/converter', cat: 'Hub', icon: '🔄', keywords: 'all formats transform' },
    { name: 'Media Hub', url: '/media-hub', cat: 'Hub', icon: '🎬', keywords: 'video image tools' },
    { name: 'PDF Lab', url: '/pdf-lab', cat: 'Hub', icon: '📄', keywords: 'office document tools' }
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

/* Global Search Logic for ConvertRocket */
const tools = [
    { name: 'Video Converter', url: '/video-converter', cat: 'Video', icon: '📽️' },
    { name: 'MP3 Converter', url: '/mp3-converter', cat: 'Audio', icon: '🎵' },
    { name: 'MP4 to MP3', url: '/mp4-to-mp3', cat: 'Audio', icon: '🎶' },
    { name: 'Video Trimmer', url: '/video-trimmer', cat: 'Video', icon: '✂️' },
    { name: 'PDF Compressor', url: '/pdf-compress', cat: 'PDF', icon: '📦' },
    { name: 'PDF to Word', url: '/pdf-to-word', cat: 'PDF', icon: '📄' },
    { name: 'PDF to Excel', url: '/pdf-to-excel', cat: 'PDF', icon: '📊' },
    { name: 'Merge PDFs', url: '/pdf-merge', cat: 'PDF', icon: '🔗' },
    { name: 'Image Converter', url: '/image-converter', cat: 'Image', icon: '🖼️' },
    { name: 'AI Image Editor', url: '/ai-image-editor', cat: 'Image', icon: '🎨' },
    { name: 'Image Compressor', url: '/image-compress', cat: 'Image', icon: '🗜️' },
    { name: 'GIF to MP4', url: '/gif-to-mp4', cat: 'Video', icon: '🎞️' },
    { name: 'YouTube Downloader', url: '/video-converter', cat: 'Video', icon: '▶️' },
    { name: 'TikTok Downloader', url: '/video-converter', cat: 'Video', icon: '🎵' },
    { name: 'YT Thumbnail', url: '/yt-thumbnail', cat: 'Media', icon: '🖼️' }
];

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('global-search');
    const resultsDiv = document.getElementById('search-results');

    if (!searchInput || !resultsDiv) return;

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        if (!query) {
            resultsDiv.classList.remove('active');
            return;
        }

        const filtered = tools.filter(t => t.name.toLowerCase().includes(query) || t.cat.toLowerCase().includes(query));

        if (filtered.length > 0) {
            resultsDiv.innerHTML = filtered.map(t => `
                <a href="${t.url}" class="search-item">
                    <span class="search-item-icon">${t.icon}</span>
                    <div class="search-item-info">
                        <span class="search-item-name">${t.name}</span>
                        <span class="search-item-cat">${t.cat}</span>
                    </div>
                </a>
            `).join('');
            resultsDiv.classList.add('active');
        } else {
            resultsDiv.innerHTML = '<div class="search-item" style="opacity:0.5; cursor:default;">No results found...</div>';
            resultsDiv.classList.add('active');
        }
    });

    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !resultsDiv.contains(e.target)) {
            resultsDiv.classList.remove('active');
        }
    });
});

/* Modern Search Logic for ConvertRocket - Sigma V8 */

const tools = [
    { name: 'Universal Converter', url: '/converter', cat: 'Laboratory', icon: '🔄', keywords: 'file transformation all formats' },
    { name: 'Cloud Downloader', url: '/downloader', cat: 'Extraction', icon: '⬇️', keywords: 'youtube tiktok instagram social' },
    { name: 'Video Trimmer', url: '/video-trimmer', cat: 'Precision', icon: '✂️', keywords: 'cut clip crop edit video' },
    { name: 'PDF Compressor', url: '/pdf-compress', cat: 'Document', icon: '📦', keywords: 'shrink small resize optimize pdf' },
    { name: 'Merge PDF', url: '/pdf-merge', cat: 'Document', icon: '🔗', keywords: 'combine join connect pdf' },
    { name: 'HEIC to JPG', url: '/heic-to-jpg', cat: 'Media', icon: '📸', keywords: 'apple photo transform' },
    { name: 'EXIF Stripper', url: '/exif-remover', cat: 'Privacy', icon: '🕵️', keywords: 'metadata remover clean' },
    { name: 'JSON Lab', url: '/json-formatter', cat: 'Developer', icon: '{ }', keywords: 'format validate minify' },
    { name: 'Color Architect', url: '/color-picker', cat: 'Developer', icon: '🎨', keywords: 'picker extract ui ux' },
    { name: 'PDF to Word', url: '/pdf-to-word', cat: 'Document', icon: '📝', keywords: 'edit docx' },
    { name: 'PDF to Excel', url: '/pdf-to-excel', cat: 'Document', icon: '📊', keywords: 'spreadsheet data' },
    { name: 'Audio Extractor', url: '/mp4-to-mp3', cat: 'Media', icon: '🎵', keywords: 'mp3 sound music' }
];

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('global-search');
    const resultsDiv = document.getElementById('search-results');

    if (!searchInput || !resultsDiv) return;

    // Apply modern result styles dynamically
    const style = document.createElement('style');
    style.textContent = `
        #search-results {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: var(--bg-surface);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            margin-top: 12px;
            max-height: 400px;
            overflow-y: auto;
            z-index: 1000;
            display: none;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            backdrop-filter: blur(20px);
            padding: 12px;
        }
        #search-results.active { display: block; }
        .search-item {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 12px 20px;
            color: white;
            text-decoration: none;
            border-radius: 12px;
            transition: all 0.2s;
        }
        .search-item:hover { background: rgba(255,255,255,0.05); transform: translateX(8px); }
        .search-icon { font-size: 1.5rem; }
        .search-name { font-weight: 700; block; font-size: 0.95rem; }
        .search-cat { font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px; }
    `;
    document.head.appendChild(style);

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        if (query.length < 1) {
            resultsDiv.classList.remove('active');
            return;
        }

        const filtered = tools.filter(t =>
            t.name.toLowerCase().includes(query) ||
            t.keywords.toLowerCase().includes(query) ||
            t.cat.toLowerCase().includes(query)
        );

        if (filtered.length > 0) {
            resultsDiv.innerHTML = filtered.map(t => `
                <a href="${t.url}" class="search-item">
                    <span class="search-icon">${t.icon}</span>
                    <div class="search-info">
                        <div class="search-name">${t.name}</div>
                        <div class="search-cat">${t.cat}</div>
                    </div>
                </a>
            `).join('');
            resultsDiv.classList.add('active');
        } else {
            resultsDiv.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--text-dim);">No protocols found.</div>';
            resultsDiv.classList.add('active');
        }
    });

    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !resultsDiv.contains(e.target)) {
            resultsDiv.classList.remove('active');
        }
    });
});

/**
 * ConvertRocket - Main JavaScript Application
 * Domain: convertrocket.online
 * Handles UI interactions, API calls, and file operations
 */

// API Base URL
const API_BASE = '';

// State management
const state = {
    activeTab: 'download',
    isProcessing: false,
    currentFile: null
};

// DOM Elements
const elements = {
    tabs: null,
    tabContents: null,

    // Download elements
    urlInput: null,
    formatType: null,
    qualitySelect: null,
    downloadBtn: null,
    getInfoBtn: null,
    videoPreview: null,
    downloadStatus: null,
    downloadResult: null,
    downloadProgress: null,

    // Convert elements
    uploadZone: null,
    fileInput: null,
    targetFormat: null,
    convertBtn: null,
    convertStatus: null,
    convertResult: null,
    convertProgress: null,
    selectedFileInfo: null
};

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    initDynamicDates();
    initElements();
    initTabs();
    initDownloadSection();
    initConvertSection();
    initShareButton();
    initQuickConverters();
    initSpecialTabs();
    loadSupportedFormats();

    // Track page view for analytics
    console.log('🚀 ConvertRocket - Industrial Dashboard Active');
    console.log('🌐 Domain: convertrocket.online');

    // Keep service alive
    initKeepAlive();
});

// Replace placeholders [MONTH_YEAR] and [TODAY] with actual dates
function initDynamicDates() {
    const now = new Date();
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const monthYear = `${months[now.getMonth()]} ${now.getFullYear()}`;
    const today = now.toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' });

    // Update title (crucial for SEO display)
    if (document.title.includes('[MONTH_YEAR]')) {
        document.title = document.title.replace('[MONTH_YEAR]', monthYear);
    }

    // Update the entire body for any other placeholders
    const processNode = (node) => {
        if (node.nodeType === 3) { // Text node
            if (node.nodeValue.includes('[MONTH_YEAR]')) {
                node.nodeValue = node.nodeValue.replace(/\[MONTH_YEAR\]/g, monthYear);
            }
            if (node.nodeValue.includes('[TODAY]')) {
                node.nodeValue = node.nodeValue.replace(/\[TODAY\]/g, today);
            }
        } else if (node.nodeType === 1) { // Element node
            for (let child of node.childNodes) {
                processNode(child);
            }
        }
    };

    processNode(document.body);
}

// Keep Alive Mechanism (Pings server every 14 minutes to prevent Render free tier shutdown while tab is open)
function initKeepAlive() {
    const PING_INTERVAL = 14 * 60 * 1000; // 14 minutes

    const ping = () => {
        fetch(`${API_BASE}/api/health`, { method: 'GET', cache: 'no-store' })
            .then(res => console.log('💓 Keep-alive ping:', res.ok ? 'OK' : 'Failed'))
            .catch(err => console.log('💓 Keep-alive ping failed (offline?)'));
    };

    // Initial ping after 30s
    setTimeout(ping, 30000);
    // Recurring ping
    setInterval(ping, PING_INTERVAL);
}

// Initialize DOM elements
function initElements() {
    elements.tabs = document.querySelectorAll('.tab-btn');
    elements.tabContents = document.querySelectorAll('.tab-content');

    // Download elements
    elements.urlInput = document.getElementById('url-input');
    elements.formatType = document.getElementById('format-type');
    elements.qualitySelect = document.getElementById('quality-select');
    elements.downloadBtn = document.getElementById('download-btn');
    elements.getInfoBtn = document.getElementById('get-info-btn');
    elements.videoPreview = document.getElementById('video-preview');
    elements.downloadStatus = document.getElementById('download-status');
    elements.downloadResult = document.getElementById('download-result');
    elements.downloadProgress = document.getElementById('download-progress');

    // Convert elements
    elements.uploadZone = document.getElementById('upload-zone');
    elements.fileInput = document.getElementById('file-input');
    elements.targetFormat = document.getElementById('target-format');
    elements.convertBtn = document.getElementById('convert-btn');
    elements.convertStatus = document.getElementById('convert-status');
    elements.convertResult = document.getElementById('convert-result');
    elements.convertProgress = document.getElementById('convert-progress');
    elements.selectedFileInfo = document.getElementById('selected-file-info');
}

// Tab switching functionality
function initTabs() {
    elements.tabs = document.querySelectorAll('.cat-link');
    if (!elements.tabs) return;
    elements.tabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            const tabId = tab.dataset.filter;
            switchTab(tabId);

            // UI Update
            elements.tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
        });
    });
}

function switchTab(tabId) {
    state.activeTab = tabId;

    // Update tab buttons
    elements.tabs.forEach(tab => {
        const isActive = (tab.dataset.filter === tabId);
        tab.classList.toggle('active', isActive);
        tab.setAttribute('aria-selected', isActive);
    });

    // Update tab contents
    elements.tabContents.forEach(content => {
        content.classList.toggle('active', content.id === `${tabId}-tab`);
    });

    // Update URL hash for SEO
    window.history.replaceState(null, null, `#${tabId}`);
}

// Global exposure for interaction sync
window.switchTab = switchTab;

// Download Section
function initDownloadSection() {
    if (elements.downloadBtn) {
        elements.downloadBtn.addEventListener('click', startDownload);
    }
    if (elements.getInfoBtn) {
        elements.getInfoBtn.addEventListener('click', getVideoInfo);
    }

    // Enter key support
    if (elements.urlInput) {
        elements.urlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                getVideoInfo();
            }
        });
    }

    // Check URL hash on load
    if (window.location.hash) {
        const hash = window.location.hash.substring(1);
        if (['download', 'convert', 'formats'].includes(hash)) {
            switchTab(hash);
        }
    }
}

async function getVideoInfo() {
    const url = elements.urlInput.value.trim();

    if (!url) {
        showStatus('download-status', getTranslation('msg_enter_url', 'Please enter a valid URL'), 'error');
        return;
    }

    showStatus('download-status', getTranslation('msg_fetching', 'Fetching video information...'), 'loading');
    elements.videoPreview.classList.remove('active');

    try {
        const response = await fetch(`${API_BASE}/api/download/info`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            displayVideoInfo(data);
            hideStatus('download-status');
        } else {
            throw new Error(data.detail || 'Failed to fetch video info');
        }
    } catch (error) {
        showStatus('download-status', error.message, 'error');
    }
}

function displayVideoInfo(data) {
    const preview = elements.videoPreview;
    const info = data.info;

    const placeholderSvg = `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 120'%3E%3Crect fill='%231a1a2e' width='200' height='120'/%3E%3Ctext x='100' y='60' text-anchor='middle' fill='%23667eea' font-size='14'%3ENo Preview%3C/text%3E%3C/svg%3E`;

    preview.innerHTML = `
        <img src="${info.thumbnail || placeholderSvg}" 
             class="video-thumbnail" 
             alt="Video thumbnail"
             loading="lazy"
             onerror="this.src='${placeholderSvg}'">
        <div class="video-details">
            <div class="video-title">${escapeHtml(info.title)}</div>
            <div class="video-meta">
                <span>📺 ${data.platform}</span>
                <span>⏱️ ${formatDuration(info.duration)}</span>
                ${info.uploader ? `<span>👤 ${escapeHtml(info.uploader)}</span>` : ''}
            </div>
            ${info.description ? `<p class="text-muted mt-1" style="font-size: 0.85rem;">${escapeHtml(info.description.substring(0, 150))}...</p>` : ''}
        </div>
    `;

    preview.classList.add('active');
}

async function startDownload() {
    const url = elements.urlInput.value.trim();
    const formatType = elements.formatType.value;
    const quality = elements.qualitySelect.value;

    if (!url) {
        showStatus('download-status', getTranslation('msg_enter_url', 'Please enter a valid URL'), 'error');
        return;
    }

    if (state.isProcessing) return;
    state.isProcessing = true;

    elements.downloadBtn.disabled = true;
    showStatus('download-status', getTranslation('msg_downloading', 'Starting download...'), 'loading');
    showProgress('download-progress', 0);
    elements.downloadResult.classList.remove('active');

    // Simulate progress (optimized for performance)
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress = Math.min(progress + Math.random() * 15, 90);
        updateProgress('download-progress', progress);
    }, 800);  // Reduced frequency for better performance

    try {
        const response = await fetch(`${API_BASE}/api/download/start`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url, format_type: formatType, quality })
        });

        clearInterval(progressInterval);
        const data = await response.json();

        if (data.success) {
            updateProgress('download-progress', 100);
            showStatus('download-status', '✅ ' + getTranslation('msg_download_complete', 'Download complete! File saved to your Downloads folder.'), 'success');
            displayDownloadResult(data);
        } else {
            // Show the friendly message from the server
            showStatus('download-status', data.message || 'Download failed. Please try again!', 'error');
            hideProgress('download-progress');
        }
    } catch (error) {
        clearInterval(progressInterval);
        // Show a friendly error message
        const friendlyMsg = error.message.includes('fetch')
            ? 'Connection issue. Please check your internet and try again!'
            : (error.message || 'Something went wrong. Please try again!');
        showStatus('download-status', friendlyMsg, 'error');
        hideProgress('download-progress');
    } finally {
        state.isProcessing = false;
        elements.downloadBtn.disabled = false;
    }
}

function displayDownloadResult(data) {
    const result = elements.downloadResult;
    const downloadText = getTranslation('msg_download_file', 'Download File');

    result.innerHTML = `
        <div class="result-header">
            <div class="result-icon">✅</div>
            <div>
                <strong>Download Complete!</strong>
                <div class="text-muted">${escapeHtml(data.filename)}</div>
                <div style="margin-top: 8px; padding: 8px; background: rgba(56, 239, 125, 0.1); border-radius: 8px; font-size: 0.9rem; color: #38ef7d;">
                    📁 Saved to: <strong>Downloads/ConvertRocket</strong>
                </div>
            </div>
        </div>
        <div class="result-info">
            ${data.title ? `
            <div class="result-info-item">
                <div class="result-info-label">Title</div>
                <div class="result-info-value">${escapeHtml(data.title.substring(0, 50))}...</div>
            </div>
            ` : ''}
            ${data.duration ? `
            <div class="result-info-item">
                <div class="result-info-label">Duration</div>
                <div class="result-info-value">${formatDuration(data.duration)}</div>
            </div>
            ` : ''}
            ${data.filesize ? `
            <div class="result-info-item">
                <div class="result-info-label">File Size</div>
                <div class="result-info-value">${formatFileSize(data.filesize)}</div>
            </div>
            ` : ''}
        </div>
        <a href="${data.download_url}" class="btn btn-success btn-block btn-lg" download>
            ⬇️ ${downloadText}
        </a>
        <div style="display: inline-flex; align-items: center; gap: 8px; margin-top: 12px; padding: 10px 16px; background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15)); border: 1px solid rgba(102, 126, 234, 0.3); border-radius: 8px; font-size: 0.9rem;">
            ⭐ Bookmark this tool – you'll need it again
        </div>
    `;

    result.classList.add('active');

    // Automatic download trigger - downloads automatically at 100%
    setTimeout(() => {
        const link = document.createElement('a');
        link.href = data.download_url;
        link.download = data.filename || 'download';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }, 1000);

    const toolbar = document.getElementById('download-result-toolbar');
    if (toolbar) toolbar.style.display = 'block';
}

// Convert Section
function initConvertSection() {
    const uploadZone = elements.uploadZone;
    const fileInput = elements.fileInput;

    if (!uploadZone || !fileInput) return;

    // Click to upload (Refined to prevent double-trigger)
    uploadZone.addEventListener('click', (e) => {
        if (e.target !== fileInput) fileInput.click();
    });

    // Keyboard accessibility
    uploadZone.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            fileInput.click();
        }
    });

    // Drag and drop
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    // Convert button
    if (elements.convertBtn) {
        elements.convertBtn.addEventListener('click', startConversion);
    }
}

function handleFileSelect(file) {
    state.currentFile = file;
    const fileInfo = elements.selectedFileInfo;
    const ext = file.name.split('.').pop().toLowerCase();
    const category = getFileCategory(ext);

    // ACTIVATE PERFORMANCE BOOST: Freeze animations during selection to prevent lag
    document.body.classList.add('perf-boost');

    // Optimized: Use requestAnimationFrame to prevent UI thread lag on selection
    requestAnimationFrame(() => {
        if (!fileInfo) return;
        fileInfo.innerHTML = `
            <div class="result-header">
                <div class="result-icon">${getCategoryIcon(category)}</div>
                <div style="overflow: hidden;">
                    <strong style="display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${escapeHtml(file.name)}</strong>
                    <div class="text-muted">${formatFileSize(file.size)} • ${ext.toUpperCase()}</div>
                </div>
            </div>
        `;
        fileInfo.style.display = 'block';
        fileInfo.classList.add('active');

        // Update available target formats
        updateTargetFormats(category, ext);
        if (elements.convertBtn) elements.convertBtn.disabled = false;

        // Show controls and hide upload zone for clear 4-step UX
        if (elements.uploadZone) elements.uploadZone.style.display = 'none';
        const controls = document.getElementById('convert-controls');
        if (controls) controls.style.display = 'block';

        // DEACTIVATE PERFORMANCE BOOST after UI update
        setTimeout(() => document.body.classList.remove('perf-boost'), 1000);
    });
}

function updateTargetFormats(category, currentExt) {
    const select = elements.targetFormat;
    const formats = getFormatsForCategory(category);

    select.innerHTML = formats
        .filter(fmt => fmt !== currentExt)
        .map(fmt => `<option value="${fmt}">${fmt.toUpperCase()}</option>`)
        .join('');
}

function getFormatsForCategory(category) {
    const formats = {
        video: ['mp4', 'mkv', 'webm', 'avi', 'mov'],
        audio: ['mp3', 'wav', 'aac', 'ogg', 'flac'],
        image: ['jpg', 'png', 'webp', 'gif', 'bmp'],
        document: ['pdf', 'docx', 'txt', 'xlsx', 'csv'],
        spreadsheet: ['xlsx', 'xls', 'csv', 'pdf']
    };
    return formats[category] || [];
}

function getFileCategory(ext) {
    const categories = {
        video: ['mp4', 'mkv', 'webm', 'avi', 'mov'],
        audio: ['mp3', 'wav', 'aac', 'ogg', 'flac'],
        image: ['jpg', 'jpeg', 'png', 'webp', 'gif', 'bmp'],
        document: ['pdf', 'docx', 'doc', 'txt'],
        spreadsheet: ['xlsx', 'xls', 'csv']
    };

    for (const [category, extensions] of Object.entries(categories)) {
        if (extensions.includes(ext.toLowerCase())) {
            return category;
        }
    }
    return 'unknown';
}

function getCategoryIcon(category) {
    const icons = {
        video: '🎬',
        audio: '🎵',
        image: '🖼️',
        document: '📄',
        spreadsheet: '📊'
    };
    return icons[category] || '📁';
}

async function startConversion() {
    if (!state.currentFile) {
        showStatus('convert-status', getTranslation('msg_select_file', 'Please select a file to convert'), 'error');
        return;
    }

    const targetFormat = elements.targetFormat.value;
    if (!targetFormat) {
        showStatus('convert-status', getTranslation('msg_select_format', 'Please select a target format'), 'error');
        return;
    }

    if (state.isProcessing) return;
    state.isProcessing = true;

    elements.convertBtn.disabled = true;

    // UI Flip: Hide info/controls, show progress
    if (elements.selectedFileInfo) elements.selectedFileInfo.style.display = 'none';
    const controls = document.getElementById('convert-controls');
    if (controls) controls.style.display = 'none';

    showStatus('convert-status', getTranslation('msg_uploading', 'Initializing secure laboratory conversion...'), 'loading');
    showProgress('convert-progress', 0);
    elements.convertResult.classList.remove('active');

    const formData = new FormData();
    formData.append('file', state.currentFile);
    formData.append('target_format', targetFormat);

    // Simulate upload progress
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress = Math.min(progress + Math.random() * 8, 85);
        updateProgress('convert-progress', progress);
    }, 400);

    try {
        const response = await fetch(`${API_BASE}/api/convert/upload`, {
            method: 'POST',
            body: formData
        });

        clearInterval(progressInterval);
        const data = await response.json();

        if (data.success) {
            updateProgress('convert-progress', 100);
            showStatus('convert-status', '✅ ' + getTranslation('msg_conversion_complete', 'Conversion complete! Your file is ready.'), 'success');
            displayConvertResult(data);
        } else {
            // Show the friendly message from the server
            showStatus('convert-status', data.message || 'Conversion failed. Please try again!', 'error');
            hideProgress('convert-progress');
        }
    } catch (error) {
        clearInterval(progressInterval);
        // Show a friendly error message
        const friendlyMsg = error.message.includes('fetch')
            ? 'Connection issue. Please check your internet and try again!'
            : (error.message || 'Something went wrong. Please try again!');
        showStatus('convert-status', friendlyMsg, 'error');
        hideProgress('convert-progress');
    } finally {
        state.isProcessing = false;
        elements.convertBtn.disabled = false;
    }
}

function displayConvertResult(data) {
    const result = elements.convertResult;
    const downloadText = getTranslation('msg_download_converted', 'Download Converted File');

    result.innerHTML = `
        <div class="result-header">
            <div class="result-icon">✅</div>
            <div>
                <strong>Conversion Complete</strong>
                <div class="text-muted">${escapeHtml(data.converted_file)}</div>
            </div>
        </div>
        <div class="result-info">
            <div class="result-info-item">
                <div class="result-info-label">Original</div>
                <div class="result-info-value">${escapeHtml(data.original_file)}</div>
            </div>
            <div class="result-info-item">
                <div class="result-info-label">Original Size</div>
                <div class="result-info-value">${data.original_size || 'N/A'}</div>
            </div>
            <div class="result-info-item">
                <div class="result-info-label">Converted Size</div>
                <div class="result-info-value">${data.converted_size || 'N/A'}</div>
            </div>
        </div>
        <a href="${data.download_url}" class="btn btn-success btn-block btn-lg" download>
            ⬇️ ${downloadText}
        </a>
        <div style="display: inline-flex; align-items: center; gap: 8px; margin-top: 12px; padding: 10px 16px; background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15)); border: 1px solid rgba(102, 126, 234, 0.3); border-radius: 8px; font-size: 0.9rem;">
            ⭐ Bookmark this tool – you'll need it again
        </div>
    `;

    result.classList.add('active');

    // Automatic download trigger - downloads automatically at 100%
    setTimeout(() => {
        const link = document.createElement('a');
        link.href = data.download_url;
        link.download = data.converted_file || 'converted_file';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }, 1000);

    const toolbar = document.getElementById('convert-result-toolbar');
    if (toolbar) toolbar.style.display = 'block';
}

// Load supported formats from API
async function loadSupportedFormats() {
    try {
        const response = await fetch(`${API_BASE}/api/convert/formats`);
        const data = await response.json();

        if (data.formats) {
            // Formats are already displayed in HTML
            console.log('Supported formats loaded:', Object.keys(data.formats));
        }
    } catch (error) {
        console.error('Failed to load formats:', error);
    }
}

// Get translation with fallback
function getTranslation(key, fallback) {
    if (window.ConvertRocketI18n && window.ConvertRocketI18n.t) {
        return window.ConvertRocketI18n.t(key) || fallback;
    }
    return fallback;
}

// Utility Functions
function showStatus(elementId, message, type) {
    const element = document.getElementById(elementId);
    if (!element) return;

    element.className = `status-message active ${type}`;
    element.innerHTML = `
        ${type === 'loading' ? '<div class="spinner"></div>' : ''}
        <span>${message}</span>
    `;
}

function hideStatus(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.remove('active');
    }
}

function showProgress(elementId, value) {
    const container = document.getElementById(elementId);
    if (!container) return;

    container.classList.add('active');
    updateProgress(elementId, value);
}

function updateProgress(elementId, value) {
    const container = document.getElementById(elementId);
    if (!container) return;

    // Industrial Activation
    container.classList.add('active');

    const fill = container.querySelector('.progress-fill');
    const text = container.querySelector('.progress-percent');

    if (fill) fill.style.width = `${value}%`;
    if (text) text.textContent = `${Math.round(value)}%`;
}

function hideProgress(elementId) {
    const container = document.getElementById(elementId);
    if (container) {
        container.classList.remove('active');
    }
}

function formatDuration(seconds) {
    if (!seconds) return 'Unknown';
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    if (hrs > 0) {
        return `${hrs}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function formatFileSize(bytes) {
    if (!bytes) return 'Unknown';
    const units = ['B', 'KB', 'MB', 'GB'];
    let size = bytes;
    let unitIndex = 0;

    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex++;
    }

    return `${size.toFixed(2)} ${units[unitIndex]}`;
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Share Button functionality
function initShareButton() {
    const shareBtn = document.getElementById('share-btn');
    if (shareBtn) {
        shareBtn.addEventListener('click', async () => {
            const url = 'convertrocket.online';
            try {
                await navigator.clipboard.writeText(url);
                shareBtn.innerHTML = '✅ <span>Copied!</span>';
                setTimeout(() => {
                    shareBtn.innerHTML = '📤 <span>Share</span>';
                }, 2000);
            } catch (err) {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = url;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                shareBtn.innerHTML = '✅ <span>Copied!</span>';
                setTimeout(() => {
                    shareBtn.innerHTML = '📤 <span>Share</span>';
                }, 2000);
            }
        });
    }
}

// Quick Converters
function initQuickConverters() {
    const quickBtns = document.querySelectorAll('.quick-convert-btn');
    quickBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const from = btn.dataset.from;
            const to = btn.dataset.to;
            // Switch to convert tab and set up the conversion
            switchTab('convert');
            // Show a message about the conversion type
            showStatus('convert-status',
                `Ready for ${from.toUpperCase()} → ${to.toUpperCase()} conversion. Upload your file!`,
                'loading');
        });
    });
}

// Special Tabs (MP4 to MP3, YouTube to MP3, Image, PDF)
function initSpecialTabs() {
    // MP4 to MP3 upload zone
    const mp4Zone = document.getElementById('mp4-upload-zone');
    if (mp4Zone) {
        const input = mp4Zone.querySelector('input[type="file"]');
        mp4Zone.addEventListener('click', () => input?.click());
        mp4Zone.addEventListener('dragover', (e) => {
            e.preventDefault();
            mp4Zone.classList.add('dragover');
        });
        mp4Zone.addEventListener('dragleave', () => mp4Zone.classList.remove('dragover'));
        mp4Zone.addEventListener('drop', (e) => {
            e.preventDefault();
            mp4Zone.classList.remove('dragover');
            if (e.dataTransfer.files.length > 0) {
                handleSpecialConversion(e.dataTransfer.files[0], 'mp3', mp4Zone);
            }
        });
        if (input) {
            input.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    handleSpecialConversion(e.target.files[0], 'mp3', mp4Zone);
                }
            });
        }
    }

    // YouTube to MP3 button
    const ytBtn = document.querySelector('.youtube-download-btn');
    const ytInput = document.querySelector('.youtube-url-input');
    if (ytBtn && ytInput) {
        ytBtn.addEventListener('click', async () => {
            const url = ytInput.value.trim();
            if (!url) {
                alert('Please enter a YouTube URL');
                return;
            }
            // Use the main download function with audio format
            document.getElementById('url-input').value = url;
            document.getElementById('format-type').value = 'audio';
            switchTab('download');
            startDownload();
        });
    }

    // Image converter zones
    const imageZone = document.querySelector('.image-upload-zone');
    if (imageZone) {
        const input = imageZone.querySelector('input[type="file"]');
        imageZone.addEventListener('click', () => input?.click());
        if (input) {
            input.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    // Switch to main convert tab with the file
                    state.currentFile = e.target.files[0];
                    switchTab('convert');
                    handleFileSelect(e.target.files[0]);
                }
            });
        }
    }

    // PDF converter zone
    const pdfZone = document.querySelector('.pdf-upload-zone');
    if (pdfZone) {
        const input = pdfZone.querySelector('input[type="file"]');
        pdfZone.addEventListener('click', () => input?.click());
        if (input) {
            input.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    state.currentFile = e.target.files[0];
                    switchTab('convert');
                    handleFileSelect(e.target.files[0]);
                }
            });
        }
    }
}

// Handle special conversion (for dedicated converter tabs)
async function handleSpecialConversion(file, targetFormat, zone) {
    const resultDiv = zone.parentElement.querySelector('.converter-result');
    if (resultDiv) {
        resultDiv.innerHTML = '<div class="status-message active loading"><div class="spinner"></div><span>Converting to ' + targetFormat.toUpperCase() + '...</span></div>';
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('target_format', targetFormat);

    try {
        const response = await fetch(`${API_BASE}/api/convert/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.success) {
            if (resultDiv) {
                resultDiv.innerHTML = `
                    <div class="result-card active">
                        <div class="result-header">
                            <div class="result-icon">✅</div>
                            <div>
                                <strong>Conversion Complete!</strong>
                                <div class="text-muted">${escapeHtml(data.converted_file)}</div>
                            </div>
                        </div>
                        <a href="${data.download_url}" class="btn btn-success btn-block btn-lg" download>
                            ⬇️ Download ${targetFormat.toUpperCase()}
                        </a>
                    </div>
                `;
                // Auto-download logic
                setTimeout(() => {
                    const link = document.createElement('a');
                    link.href = data.download_url;
                    link.download = data.converted_file || 'converted_file';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }, 500);
            }
        } else {
            throw new Error(data.detail || 'Conversion failed');
        }
    } catch (error) {
        if (resultDiv) {
            resultDiv.innerHTML = `<div class="status-message active error">${error.message}</div>`;
        }
    }
}

// Export for potential external use
window.ConvertRocket = {
    state,
    switchTab,
    startDownload,
    startConversion
};

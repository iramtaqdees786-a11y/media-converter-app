/* 
   ============================================================
   ConvertRocket - Premium Feature Core
   Handles: Starring tools, History, Notifications, Layout
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
    initParticles();
    initStarring();
    initToasts();
    initSelectionFix();
    updateToolStats();
    initCommandTabs();
    initFlowArrow();
    initToolExplorer(); // NEW: UX Filter
});

// 1. Particle System (Aesthetic Flow)
function initParticles() {
    const container = document.querySelector('.bg-animated');
    if (!container) return;

    // Create particles div if not exists
    let pDiv = document.querySelector('.particles');
    if (!pDiv) {
        pDiv = document.createElement('div');
        pDiv.className = 'particles';
        container.appendChild(pDiv);
    }

    for (let i = 0; i < 20; i++) {
        const p = document.createElement('div');
        p.className = 'particle';
        const size = Math.random() * 4 + 2;
        p.style.width = `${size}px`;
        p.style.height = `${size}px`;
        p.style.left = `${Math.random() * 100}%`;
        p.style.top = `${Math.random() * 100}%`;
        p.style.animationDelay = `${Math.random() * 10}s`;
        p.style.animationDuration = `${Math.random() * 15 + 10}s`;
        pDiv.appendChild(p);
    }
}

// 2. Starring / Favorites System
function initStarring() {
    const stars = document.querySelectorAll('.card-star');
    const favoritesGrid = document.getElementById('favorites-grid');
    const favSection = document.getElementById('favorites-section');

    // Load from local storage
    const starredTools = JSON.parse(localStorage.getItem('starredTools') || '[]');

    // Apply state
    stars.forEach(star => {
        const toolUrl = star.closest('.tool-card').getAttribute('href');
        if (starredTools.includes(toolUrl)) {
            star.classList.add('active');
            star.textContent = '+';
        }

        star.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();

            const card = star.closest('.tool-card');
            const url = card.getAttribute('href');

            if (star.classList.contains('active')) {
                star.classList.remove('active');
                star.textContent = '☆';
                removeStarred(url);
                showToast('Removed from favorites', 'info');
            } else {
                star.classList.add('active');
                star.textContent = '+';
                addStarred(url);
                showToast('Added to favorites!', 'success');
            }
            renderFavorites();
        });
    });

    function addStarred(url) {
        const current = JSON.parse(localStorage.getItem('starredTools') || '[]');
        if (!current.includes(url)) current.push(url);
        localStorage.setItem('starredTools', JSON.stringify(current));
    }

    function removeStarred(url) {
        let current = JSON.parse(localStorage.getItem('starredTools') || '[]');
        current = current.filter(u => u !== url);
        localStorage.setItem('starredTools', JSON.stringify(current));
    }

    function renderFavorites() {
        if (!favoritesGrid) return;
        const current = JSON.parse(localStorage.getItem('starredTools') || '[]');

        if (current.length === 0) {
            if (favSection) favSection.style.display = 'none';
            return;
        }

        if (favSection) favSection.style.display = 'block';
        favoritesGrid.innerHTML = '';

        current.forEach(url => {
            // Find the original card in the document to clone
            const original = document.querySelector(`.tool-card[href="${url}"]`);
            if (original) {
                const clone = original.cloneNode(true);
                // Re-attach star listener to clone
                const newStar = clone.querySelector('.card-star');
                newStar.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    const u = clone.getAttribute('href');
                    removeStarred(u);
                    renderFavorites();
                    // Sync the real card if visible
                    const realStar = document.querySelector(`.tool-card[href="${u}"] .card-star`);
                    if (realStar) { realStar.classList.remove('active'); realStar.textContent = '☆'; }
                });
                favoritesGrid.appendChild(clone);
            }
        });
    }

    renderFavorites();
}

// 3. Selection Area Fix (Absolute Overlay)
function initSelectionFix() {
    const zones = document.querySelectorAll('.upload-zone');
    zones.forEach(zone => {
        const input = zone.querySelector('input[type="file"]');
        if (!input) return;

        // Ensure input covers the zone
        input.style.position = 'absolute';
        input.style.inset = '0';
        input.style.opacity = '0';
        input.style.cursor = 'pointer';
        input.style.width = '100%';
        input.style.height = '100%';
        input.style.zIndex = '5';

        // Fix: Force click if somehow blocked
        zone.addEventListener('click', (e) => {
            if (e.target !== input) {
                input.click();
            }
        });

        // Hover effect for parent
        input.addEventListener('mouseenter', () => zone.style.borderColor = 'var(--neon-cyan)');
        input.addEventListener('mouseleave', () => zone.style.borderColor = '');

        // Drop effect
        input.addEventListener('dragenter', () => zone.classList.add('dragover'));
        input.addEventListener('dragleave', () => zone.classList.remove('dragover'));
        input.addEventListener('drop', () => zone.classList.remove('dragover'));

        // PERFORMANCE SHIELD: Trigger global boost on change
        input.addEventListener('change', () => {
            document.body.classList.add('perf-boost');
            setTimeout(() => document.body.classList.remove('perf-boost'), 2000);
        });
    });
}

// 4. Toast Notifications
function initToasts() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    const icon = type === 'success' ? '✅' : 'ℹ️';
    toast.innerHTML = `${icon} <span>${message}</span>`;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(20px)';
        setTimeout(() => toast.remove(), 500);
    }, 3000);
}

// 5. Tool Stats (Mockup for Aesthetic)
function updateToolStats() {
    const stats = document.querySelectorAll('.stat-badge');
    stats.forEach(stat => {
        const rand = Math.floor(Math.random() * 500) + 100;
        stat.textContent = `${rand} converted today`;
    });
}
// 6. Command Center Tabs
function initCommandTabs() {
    const tabs = document.querySelectorAll('.cmd-tab');
    const panes = document.querySelectorAll('.tab-pane');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const target = tab.getAttribute('data-tab');

            // Sync UI
            tabs.forEach(t => t.classList.remove('active'));
            panes.forEach(p => p.classList.remove('active'));

            tab.classList.add('active');
            const targetPane = document.getElementById(target);
            if (targetPane) targetPane.classList.add('active');

            // Sync with global app state if needed
            if (window.switchTab) {
                const globalTab = target === 'universal-converter' ? 'convert' : 'download';
                window.switchTab(globalTab);
            }
        });
    });
}

// 7. Flow Arrow Logic
function initFlowArrow() {
    const arrow = document.querySelector('.flow-arrow');
    if (arrow) {
        arrow.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = arrow.getAttribute('href').substring(1);
            const target = document.getElementById(targetId);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    }
}

// 8. Result Hub Actions
function copyResultLink() {
    const url = window.location.href;
    navigator.clipboard.writeText(url).then(() => {
        if (window.showToast) window.showToast('Lab link copied to clipboard!', 'success');
    });
}

function bookmarkTool() {
    if (window.showToast) window.showToast('Press Ctrl+D to bookmark this laboratory module!', 'info');
}

// Global exposure
window.copyResultLink = copyResultLink;
window.bookmarkTool = bookmarkTool;
// 9. Tool Category Filtering (Speed & UX)
function initToolExplorer() {
    const pills = document.querySelectorAll('.cat-pill');
    const sections = document.querySelectorAll('.tool-section[data-category]');

    pills.forEach(pill => {
        pill.addEventListener('click', () => {
            const filter = pill.getAttribute('data-filter');

            // Update UI
            pills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');

            // Filter sections
            sections.forEach(section => {
                const category = section.getAttribute('data-category');
                if (filter === 'all' || category === filter) {
                    section.classList.remove('hidden');
                    section.style.opacity = '0';
                    setTimeout(() => section.style.opacity = '1', 10);
                } else {
                    section.classList.add('hidden');
                }
            });

            // Smooth scroll to results
            const explorer = document.getElementById('tool-explorer');
            if (explorer) explorer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });
}

// Global exposure
window.initToolExplorer = initToolExplorer;

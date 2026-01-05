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
            star.textContent = '⭐';
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
                star.textContent = '⭐';
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

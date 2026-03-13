/**
 * ConvertRocket Workspace & Sharing Logic
 * Handles conversion history and dual-email lead capture
 */

const WorkspaceController = {
    init() {
        console.log("🚀 Workspace Controller Initialized");
        this.injectModalStyles();
        this.setupHistoryTracking();
        this.setupShareButtons();
    },

    injectModalStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .cr-modal-overlay {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0,0,0,0.85); backdrop-filter: blur(10px);
                display: flex; align-items: center; justify-content: center;
                opacity: 0; visibility: hidden; transition: 0.3s; z-index: 9999;
            }
            .cr-modal-overlay.active { opacity: 1; visibility: visible; }
            .cr-modal {
                background: #121218; border: 1px solid rgba(255,255,255,0.1);
                border-radius: 24px; padding: 40px; width: 100%; max-width: 450px;
                transform: translateY(20px); transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }
            .cr-modal-overlay.active .cr-modal { transform: translateY(0); }
            .cr-modal h2 { margin-bottom: 8px; font-size: 1.5rem; color: #fff; }
            .cr-modal p { margin-bottom: 24px; color: #94a3b8; font-size: 0.95rem; }
            .cr-form-group { margin-bottom: 20px; }
            .cr-form-group label { display: block; margin-bottom: 8px; font-size: 0.85rem; font-weight: 600; color: #ccc; }
            .cr-input {
                width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
                border-radius: 12px; padding: 14px; color: #fff; font-size: 1rem; outline: none; transition: 0.3s;
            }
            .cr-input:focus { border-color: #00eaff; box-shadow: 0 0 15px rgba(0, 234, 255, 0.2); }
            .cr-btn-share {
                width: 100%; background: linear-gradient(135deg, #00eaff, #0077ff);
                color: #000; border: none; padding: 16px; border-radius: 12px;
                font-weight: 700; font-size: 1rem; cursor: pointer; transition: 0.3s;
            }
            .cr-btn-share:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(0, 234, 255, 0.3); }
            .cr-close-btn { 
                position: absolute; top: 20px; right: 20px; color: #666; 
                cursor: pointer; font-size: 1.5rem; transition: 0.3s;
            }
            .cr-close-btn:hover { color: #fff; }
        `;
        document.head.appendChild(style);
    },

    setupHistoryTracking() {
        // Intercept download clicks or completion events
        // In this app, many tools use a shared 'download-link' ID
        const observer = new MutationObserver((mutations) => {
            const dl = document.getElementById('download-link');
            if (dl && !dl.dataset.tracked) {
                dl.dataset.tracked = "true";
                dl.addEventListener('click', () => {
                    this.saveToHistory({
                        fileName: dl.getAttribute('download') || "Converted File",
                        type: this.detectType(),
                        timestamp: new Date().toISOString(),
                        toolLink: window.location.pathname
                    });
                });
            }
        });
        observer.observe(document.body, { childList: true, subtree: true });
    },

    saveToHistory(item) {
        let history = JSON.parse(localStorage.getItem('conversionHistory') || '[]');
        // Avoid duplicates if clicked multiple times
        if (history.length > 0 && history[history.length-1].fileName === item.fileName) return;
        
        history.push(item);
        if (history.length > 50) history.shift(); // Max 50 items
        localStorage.setItem('conversionHistory', JSON.stringify(history));
        console.log("✅ Conversion saved to workspace");
    },

    detectType() {
        const path = window.location.pathname;
        if (path.includes('pdf')) return 'pdf';
        if (path.includes('video')) return 'video';
        if (path.includes('audio') || path.includes('mp3')) return 'audio';
        if (path.includes('image')) return 'image';
        if (path.includes('json')) return 'json';
        if (path.includes('qr')) return 'qr';
        return 'file';
    },

    setupShareButtons() {
        // Look for buttons that should trigger the "Share via Email" modal
        const shareBtn = document.createElement('button');
        shareBtn.id = "share-email-trigger";
        shareBtn.style.display = "none";
        document.body.appendChild(shareBtn);

        shareBtn.onclick = (e) => {
            const fileData = {
                name: e.detail?.fileName || "your file",
                tool: this.detectType()
            };
            this.showShareModal(fileData);
        };
    },

    showShareModal(fileData) {
        let overlay = document.querySelector('.cr-modal-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.className = 'cr-modal-overlay';
            overlay.innerHTML = `
                <div class="cr-modal">
                    <span class="cr-close-btn">&times;</span>
                    <h2>Email this file</h2>
                    <p>Send a link to "${fileData.name}" directly to an inbox.</p>
                    <div class="cr-form-group">
                        <label>Your Email (Sender)</label>
                        <input type="email" id="cr-sender" class="cr-input" placeholder="you@example.com" required>
                    </div>
                    <div class="cr-form-group">
                        <label>Recipient Email</label>
                        <input type="email" id="cr-recipient" class="cr-input" placeholder="friend@example.com" required>
                    </div>
                    <button id="cr-submit-share" class="cr-btn-share">Share via Email</button>
                    <div id="cr-share-status" style="margin-top: 15px; font-size: 0.85rem; text-align: center;"></div>
                </div>
            `;
            document.body.appendChild(overlay);

            overlay.querySelector('.cr-close-btn').onclick = () => overlay.classList.remove('active');
            overlay.onclick = (e) => { if (e.target === overlay) overlay.classList.remove('active'); };

            document.getElementById('cr-submit-share').onclick = async () => {
                const sender = document.getElementById('cr-sender').value;
                const recipient = document.getElementById('cr-recipient').value;
                const status = document.getElementById('cr-share-status');

                if (!sender || !recipient) {
                    status.innerHTML = '<span style="color: #ff007a;">Please fill both fields.</span>';
                    return;
                }

                status.innerHTML = '<span style="color: #00eaff;">Processing...</span>';

                try {
                    const response = await fetch('/api/share-file', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            sender_email: sender,
                            recipient_email: recipient,
                            tool: fileData.tool,
                            file_name: fileData.name
                        })
                    });
                    const res = await response.json();
                    if (res.success) {
                        status.innerHTML = '<span style="color: #38ef7d;">Success! File shared and emails logged.</span>';
                        setTimeout(() => overlay.classList.remove('active'), 2000);
                    } else {
                        status.innerHTML = '<span style="color: #ff007a;">Error: ' + res.message + '</span>';
                    }
                } catch (err) {
                    status.innerHTML = '<span style="color: #ff007a;">Connection error.</span>';
                }
            };
        }

        overlay.classList.add('active');
    }
};

WorkspaceController.init();

// Global utility to trigger modal from other scripts
window.openShareModal = (fileName) => {
    const trigger = document.getElementById('share-email-trigger');
    if (trigger) {
        const event = new CustomEvent('click', { detail: { fileName } });
        trigger.dispatchEvent(event);
    }
};

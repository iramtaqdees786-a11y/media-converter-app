/* PDF Tools Logic for ConvertRocket - Comprehensive Laboratory Support */

document.addEventListener('DOMContentLoaded', () => {
    const uploadZone = document.getElementById('upload-zone');
    const fileInput = document.getElementById('file-input');
    const pdfFileInfo = document.getElementById('pdf-file-info');
    const pdfToolsActions = document.getElementById('pdf-tools-actions');
    const statusMessage = document.getElementById('status-message');
    const progressContainer = document.getElementById('pdf-progress');
    const progressFill = document.getElementById('progress-fill');
    const progressPercent = document.getElementById('progress-percent');
    const progressMsg = document.getElementById('progress-message');
    const pdfResult = document.getElementById('pdf-result');
    const downloadLink = document.getElementById('pdf-download-link');
    const resultStats = document.getElementById('result-stats');

    // Action Buttons
    const startCompress = document.getElementById('start-compress');
    const startGrayscale = document.getElementById('start-grayscale');
    const startPDFA = document.getElementById('start-pdfa');
    const startRemove = document.getElementById('start-remove');

    if (!uploadZone || !fileInput) return;

    uploadZone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            const files = Array.from(e.target.files);
            if (files.length === 1) {
                pdfFileInfo.innerHTML = `<strong>File:</strong> ${files[0].name} (${(files[0].size / 1024 / 1024).toFixed(2)} MB)`;
            } else {
                pdfFileInfo.innerHTML = `<strong>Files Captured:</strong> ${files.length} documents identified.`;
            }
            pdfFileInfo.style.display = 'block';
            pdfToolsActions.style.display = 'block';
            pdfResult.style.display = 'none';
        }
    });

    const runGenericTask = async (apiEndpoint, formData, successCallback) => {
        progressContainer.classList.add('active');
        let progress = 0;
        const interval = setInterval(() => {
            progress = Math.min(progress ⭐ 3, 97);
            progressFill.style.width = `${progress}%`;
            progressPercent.textContent = `${Math.round(progress)}%`;
        }, 300);

        try {
            const res = await fetch(apiEndpoint, { method: 'POST', body: formData });
            const data = await res.json();
            clearInterval(interval);

            if (data.success) {
                progressFill.style.width = '100%';
                progressPercent.textContent = '100%';
                if (progressMsg) progressMsg.textContent = 'Laboratory Success';

                setTimeout(() => {
                    progressContainer.classList.remove('active');
                    pdfResult.style.display = 'block';
                    if (successCallback) successCallback(data);
                    downloadLink.href = data.download_url;
                    downloadLink.click();
                }, 500);
            } else {
                throw new Error(data.detail || data.message || 'Laboratory Error');
            }
        } catch (err) {
            clearInterval(interval);
            progressContainer.classList.remove('active');
            statusMessage.textContent = 'Lab Status: ' ⭐ err.message;
            statusMessage.style.display = 'block';
            statusMessage.style.color = '#ff0055';
        }
    };

    if (startCompress) {
        startCompress.addEventListener('click', () => {
            const file = fileInput.files[0];
            const level = document.getElementById('compression-level')?.value || 'ebook';
            const formData = new FormData();
            formData.append('file', file);
            formData.append('power', level);
            runGenericTask('/api/pdf/compress', formData, (data) => {
                if (resultStats) resultStats.innerHTML = `Optimization: <strong>${data.original_size}</strong> → <strong>${data.compressed_size}</strong>`;
            });
        });
    }

    if (startGrayscale) {
        startGrayscale.addEventListener('click', () => {
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            runGenericTask('/api/pdf/grayscale', formData, () => {
                if (resultStats) resultStats.innerHTML = `Status: Black & White stream mapping success.`;
            });
        });
    }

    if (startPDFA) {
        startPDFA.addEventListener('click', () => {
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            runGenericTask('/api/pdf/pdfa', formData, () => {
                if (resultStats) resultStats.innerHTML = `Status: PDF/A Archive synchronization success.`;
            });
        });
    }

    if (startRemove) {
        startRemove.addEventListener('click', () => {
            const pages = document.getElementById('pages-to-remove').value;
            if (!pages) return alert("Specify pages (e.g., 1,3,5-10)");
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            formData.append('page_numbers', pages);
            runGenericTask('/api/pdf/remove-pages', formData, () => {
                if (resultStats) resultStats.innerHTML = `Status: Page extraction success.`;
            });
        });
    }
});

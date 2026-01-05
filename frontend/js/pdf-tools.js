/* PDF Tools Logic for ConvertRocket - Individual Page Support */

document.addEventListener('DOMContentLoaded', () => {
    const uploadZone = document.getElementById('upload-zone');
    const fileInput = document.getElementById('file-input');
    const pdfFileInfo = document.getElementById('pdf-file-info');
    const pdfToolsActions = document.getElementById('pdf-tools-actions');
    const startCompress = document.getElementById('start-compress');
    const statusMessage = document.getElementById('status-message');
    const progressContainer = document.getElementById('pdf-progress');
    const progressFill = document.getElementById('progress-fill');
    const progressPercent = document.getElementById('progress-percent');
    const pdfResult = document.getElementById('pdf-result');
    const downloadLink = document.getElementById('pdf-download-link');
    const resultStats = document.getElementById('result-stats');

    if (!uploadZone || !fileInput) return;

    uploadZone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            const file = e.target.files[0];
            pdfFileInfo.innerHTML = `<strong>File:</strong> ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
            pdfFileInfo.style.display = 'block';
            pdfToolsActions.style.display = 'block';
            pdfResult.style.display = 'none';
        }
    });

    if (startCompress) {
        startCompress.addEventListener('click', async () => {
            const file = fileInput.files[0];
            const level = document.getElementById('compression-level')?.value || 'ebook';

            if (!file) return;

            progressContainer.classList.add('active');
            let progress = 0;
            const interval = setInterval(() => {
                progress = Math.min(progress + 5, 95);
                progressFill.style.width = `${progress}%`;
                progressPercent.textContent = `${Math.round(progress)}%`;
            }, 500);

            const formData = new FormData();
            formData.append('file', file);
            formData.append('power', level);

            try {
                const res = await fetch('/api/pdf/compress', {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();
                clearInterval(interval);

                if (data.success) {
                    progressFill.style.width = '100%';
                    progressPercent.textContent = '100%';

                    setTimeout(() => {
                        progressContainer.classList.remove('active');
                        pdfResult.style.display = 'block';
                        resultStats.innerHTML = `File reduced from <strong>${data.original_size}</strong> to <strong>${data.compressed_size}</strong>`;
                        downloadLink.href = data.download_url;
                        downloadLink.click();
                    }, 500);
                } else {
                    throw new Error(data.message);
                }
            } catch (err) {
                clearInterval(interval);
                progressContainer.classList.remove('active');
                statusMessage.textContent = 'Error: ' + err.message;
                statusMessage.classList.add('active', 'error');
            }
        });
    }
});

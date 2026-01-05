/**
 * AI-Powered Image Editor - Core Module
 * Production-ready implementation using MediaPipe, TensorFlow.js (COCO-SSD), and Canvas API
 * 
 * Architecture:
 * 1. AI models detect WHERE to edit (faces, objects, background)
 * 2. Canvas API + pixel math handles HOW to edit (blur, brightness, etc.)
 * 3. Everything runs client-side for 100% privacy
 */

class AIImageEditor {
    constructor() {
        this.originalImage = null;
        this.currentImage = null;
        this.canvas = document.getElementById('main-canvas');
        this.ctx = this.canvas.getContext('2d', { willReadFrequently: true });
        this.maskCanvas = document.createElement('canvas'); // Internal mask
        this.maskCtx = this.maskCanvas.getContext('2d');

        // AI Models
        this.selfieSegmentation = null;
        this.faceDetection = null;
        this.cocoSsd = null;

        // Detection results cache
        this.cachedDetections = {
            faces: null,
            objects: null,
            segmentation: null
        };

        this.init();
    }

    async init() {
        await this.loadModels();
        this.setupEventListeners();
    }

    /**
     * Load all AI models asynchronously
     */
    async loadModels() {
        const statusEl = document.getElementById('status-message');
        if (!statusEl) return;
        statusEl.classList.add('active');
        statusEl.innerHTML = '<div class="loading"><p>Loading AI models...</p></div>';

        try {
            // Load TensorFlow models in parallel
            const [cocoModel] = await Promise.all([
                cocoSsd.load()
            ]);

            this.cocoSsd = cocoModel;

            // Load MediaPipe models
            await this.initMediaPipeModels();

            statusEl.innerHTML = '<p style="color: #38ef7d;">✓ AI models loaded successfully!</p>';
            setTimeout(() => statusEl.classList.remove('active'), 2000);
        } catch (error) {
            console.error('Error loading models:', error);
            statusEl.innerHTML = '<p style="color: #ff6b6b;">⚠️ Error loading models. Some features may not work.</p>';
        }
    }

    /**
     * Initialize MediaPipe models
     */
    async initMediaPipeModels() {
        // Selfie Segmentation
        this.selfieSegmentation = new SelfieSegmentation({
            locateFile: (file) => {
                return `https://cdn.jsdelivr.net/npm/@mediapipe/selfie_segmentation@0.1/${file}`;
            }
        });

        this.selfieSegmentation.setOptions({
            modelSelection: 1, // 0: general, 1: landscape (better quality)
            selfieMode: false,
        });

        await this.selfieSegmentation.initialize();

        // Face Detection
        this.faceDetection = new FaceDetection({
            locateFile: (file) => {
                return `https://cdn.jsdelivr.net/npm/@mediapipe/face_detection@0.4/${file}`;
            }
        });

        this.faceDetection.setOptions({
            model: 'short',
            minDetectionConfidence: 0.5,
        });

        await this.faceDetection.initialize();
    }

    /**
     * Setup all event listeners
     */
    setupEventListeners() {
        const uploadZone = document.getElementById('upload-zone');
        const imageInput = document.getElementById('file-input');
        const downloadBtn = document.getElementById('download-ai-result');

        // Upload events
        uploadZone.addEventListener('click', () => imageInput.click());

        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.style.borderColor = '#667eea';
        });

        uploadZone.addEventListener('dragleave', () => {
            uploadZone.style.borderColor = 'rgba(255, 255, 255, 0.1)';
        });

        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.style.borderColor = 'rgba(255, 255, 255, 0.1)';
            const file = e.dataTransfer.files[0];
            if (file && file.type.startsWith('image/')) {
                this.loadImage(file);
            }
        });

        imageInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                this.loadImage(file);
            }
        });

        // Tool buttons
        document.querySelectorAll('.ai-op-btn').forEach(btn => {
            btn.addEventListener('click', () => this.handleToolClick(btn));
        });

        // Download button
        downloadBtn.addEventListener('click', () => this.downloadImage());
    }

    /**
     * Load and display image
     */
    loadImage(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                this.originalImage = img;
                this.currentImage = img;
                this.displayImage(img);

                // Show canvas, hide upload zone
                document.getElementById('upload-zone').style.display = 'none';
                document.getElementById('ai-workspace').style.display = 'block';
                document.getElementById('canvas-wrapper').style.display = 'block';
                document.getElementById('ai-tools').style.display = 'grid';

                // Clear cached detections
                this.cachedDetections = {
                    faces: null,
                    objects: null,
                    segmentation: null
                };
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }

    /**
     * Display image on canvas
     */
    displayImage(img) {
        // Set canvas size to image size
        this.canvas.width = img.width;
        this.canvas.height = img.height;
        this.maskCanvas.width = img.width;
        this.maskCanvas.height = img.height;

        // Draw image
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.drawImage(img, 0, 0);
    }

    /**
     * Handle tool button clicks
     */
    async handleToolClick(btn) {
        if (!this.originalImage) {
            alert('Please upload an image first!');
            return;
        }

        // Update active state
        document.querySelectorAll('.tool-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const tool = btn.dataset.tool;
        const statusEl = document.getElementById('status-message');
        statusEl.classList.add('active');

        try {
            switch (tool) {
                case 'remove-bg':
                    await this.removeBackground();
                    break;
                case 'blur-bg':
                    await this.blurBackground();
                    break;
                case 'grayscale':
                    this.applyGrayscale();
                    break;
                case 'enhance':
                    this.applyEnhance();
                    break;
                case 'blur-faces':
                    await this.blurFaces();
                    break;
                case 'detect-faces':
                    await this.detectFaces();
                    break;
                case 'detect-objects':
                    await this.detectObjects();
                    break;
                case 'blur-objects':
                    await this.blurObjects();
                    break;
                case 'brightness':
                    this.showBrightnessControl();
                    break;
                case 'contrast':
                    this.showContrastControl();
                    break;
                case 'sharpen':
                    this.applySharpen();
                    break;
                case 'blur':
                    this.showBlurControl();
                    break;
            }
            statusEl.classList.remove('active');
        } catch (error) {
            console.error('Error processing image:', error);
            statusEl.innerHTML = '<p style="color: #ff6b6b;">⚠️ Error processing image</p>';
        }
    }

    /**
     * Remove background using MediaPipe Selfie Segmentation
     */
    async removeBackground() {
        const statusEl = document.getElementById('status-message');
        statusEl.innerHTML = '<div class="loading"><div class="spinner"></div><p>Removing background...</p></div>';

        const mask = await this.getSegmentationMask();
        const imageData = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
        const data = imageData.data;

        // Apply mask: set alpha to 0 for background pixels
        for (let i = 0; i < data.length; i += 4) {
            const maskValue = mask[i / 4];
            if (maskValue < 128) { // Background
                data[i + 3] = 0; // Set alpha to 0
            }
        }

        this.ctx.putImageData(imageData, 0, 0);
        statusEl.innerHTML = '<p style="color: #38ef7d;">✓ Background removed!</p>';
    }

    /**
     * Blur background
     */
    async blurBackground() {
        const statusEl = document.getElementById('status-message');
        statusEl.innerHTML = '<div class="loading"><div class="spinner"></div><p>Blurring background...</p></div>';

        const mask = await this.getSegmentationMask();

        // Create blurred version of entire image
        const blurredData = this.applyGaussianBlur(
            this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height),
            15
        );

        const originalData = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
        const resultData = this.ctx.createImageData(this.canvas.width, this.canvas.height);

        // Blend original and blurred based on mask
        for (let i = 0; i < originalData.data.length; i += 4) {
            const maskValue = mask[i / 4];
            const alpha = maskValue / 255; // Person = 1, Background = 0

            resultData.data[i] = originalData.data[i] * alpha + blurredData.data[i] * (1 - alpha);
            resultData.data[i + 1] = originalData.data[i + 1] * alpha + blurredData.data[i + 1] * (1 - alpha);
            resultData.data[i + 2] = originalData.data[i + 2] * alpha + blurredData.data[i + 2] * (1 - alpha);
            resultData.data[i + 3] = 255;
        }

        this.ctx.putImageData(resultData, 0, 0);
        statusEl.innerHTML = '<p style="color: #38ef7d;">✓ Background blurred!</p>';
    }

    /**
     * Replace background with color/gradient
     */
    async replaceBackground() {
        const statusEl = document.getElementById('status-message');
        statusEl.innerHTML = '<div class="loading"><div class="spinner"></div><p>Replacing background...</p></div>';

        const mask = await this.getSegmentationMask();
        const imageData = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
        const data = imageData.data;

        // Create gradient background
        const gradient = this.ctx.createLinearGradient(0, 0, this.canvas.width, this.canvas.height);
        gradient.addColorStop(0, '#667eea');
        gradient.addColorStop(1, '#f093fb');

        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Get gradient pixel data
        const gradientData = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);

        // Composite: foreground on gradient background
        for (let i = 0; i < data.length; i += 4) {
            const maskValue = mask[i / 4];
            const alpha = maskValue / 255;

            data[i] = data[i] * alpha + gradientData.data[i] * (1 - alpha);
            data[i + 1] = data[i + 1] * alpha + gradientData.data[i + 1] * (1 - alpha);
            data[i + 2] = data[i + 2] * alpha + gradientData.data[i + 2] * (1 - alpha);
        }

        this.ctx.putImageData(imageData, 0, 0);
        statusEl.innerHTML = '<p style="color: #38ef7d;">✓ Background replaced!</p>';
    }

    /**
     * Blur detected faces
     */
    async blurFaces() {
        const statusEl = document.getElementById('status-message');
        statusEl.innerHTML = '<div class="loading"><div class="spinner"></div><p>Detecting and blurring faces...</p></div>';

        const faces = await this.detectFacesInternal();
        const imageData = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);

        // Blur each face region
        faces.forEach(face => {
            const x = Math.floor(face.xMin * this.canvas.width);
            const y = Math.floor(face.yMin * this.canvas.height);
            const width = Math.floor(face.width * this.canvas.width);
            const height = Math.floor(face.height * this.canvas.height);

            const faceData = this.ctx.getImageData(x, y, width, height);
            const blurred = this.applyGaussianBlur(faceData, 20);
            this.ctx.putImageData(blurred, x, y);
        });

        statusEl.innerHTML = `<p style="color: #38ef7d;">✓ ${faces.length} face(s) blurred!</p>`;
    }

    /**
     * Detect and visualize faces
     */
    async detectFaces() {
        const statusEl = document.getElementById('status-message');
        statusEl.innerHTML = '<div class="loading"><div class="spinner"></div><p>Detecting faces...</p></div>';

        const faces = await this.detectFacesInternal();
        this.visualizeDetections(faces, 'face');

        statusEl.innerHTML = `<p style="color: #38ef7d;">✓ Found ${faces.length} face(s)!</p>`;
    }

    /**
     * Detect objects using COCO-SSD
     */
    async detectObjects() {
        const statusEl = document.getElementById('status-message');
        statusEl.innerHTML = '<div class="loading"><div class="spinner"></div><p>Detecting objects...</p></div>';

        const objects = await this.detectObjectsInternal();
        this.visualizeDetections(objects, 'object');

        statusEl.innerHTML = `<p style="color: #38ef7d;">✓ Found ${objects.length} object(s)!</p>`;
    }

    /**
     * Blur detected objects
     */
    async blurObjects() {
        const statusEl = document.getElementById('status-message');
        statusEl.innerHTML = '<div class="loading"><div class="spinner"></div><p>Detecting and blurring objects...</p></div>';

        const objects = await this.detectObjectsInternal();

        objects.forEach(obj => {
            const [x, y, width, height] = obj.bbox;
            const objData = this.ctx.getImageData(x, y, width, height);
            const blurred = this.applyGaussianBlur(objData, 15);
            this.ctx.putImageData(blurred, x, y);
        });

        statusEl.innerHTML = `<p style="color: #38ef7d;">✓ ${objects.length} object(s) blurred!</p>`;
    }

    /**
     * Get segmentation mask from MediaPipe
     */
    async getSegmentationMask() {
        if (this.cachedDetections.segmentation) {
            return this.cachedDetections.segmentation;
        }

        return new Promise((resolve) => {
            this.selfieSegmentation.onResults((results) => {
                const mask = results.segmentationMask;
                const canvas = document.createElement('canvas');
                canvas.width = mask.width;
                canvas.height = mask.height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(mask, 0, 0);

                const maskData = ctx.getImageData(0, 0, mask.width, mask.height);
                const maskArray = new Uint8Array(mask.width * mask.height);

                for (let i = 0; i < maskData.data.length; i += 4) {
                    maskArray[i / 4] = maskData.data[i];
                }

                this.cachedDetections.segmentation = maskArray;
                resolve(maskArray);
            });

            this.selfieSegmentation.send({ image: this.canvas });
        });
    }

    /**
     * Internal face detection
     */
    async detectFacesInternal() {
        if (this.cachedDetections.faces) {
            return this.cachedDetections.faces;
        }

        return new Promise((resolve) => {
            this.faceDetection.onResults((results) => {
                const faces = results.detections.map(det => ({
                    xMin: det.boundingBox.xCenter - det.boundingBox.width / 2,
                    yMin: det.boundingBox.yCenter - det.boundingBox.height / 2,
                    width: det.boundingBox.width,
                    height: det.boundingBox.height,
                    score: det.score[0]
                }));

                this.cachedDetections.faces = faces;
                resolve(faces);
            });

            this.faceDetection.send({ image: this.canvas });
        });
    }

    /**
     * Internal object detection
     */
    async detectObjectsInternal() {
        if (this.cachedDetections.objects) {
            return this.cachedDetections.objects;
        }

        const predictions = await this.cocoSsd.detect(this.canvas);
        this.cachedDetections.objects = predictions;
        return predictions;
    }

    /**
     * Apply high-fidelity grayscale
     */
    applyGrayscale() {
        const imageData = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
        const data = imageData.data;
        for (let i = 0; i < data.length; i += 4) {
            const avg = 0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2];
            data[i] = avg; data[i + 1] = avg; data[i + 2] = avg;
        }
        this.ctx.putImageData(imageData, 0, 0);
    }

    /**
     * Auto-enhance (Contrast + Sharpen boost)
     */
    applyEnhance() {
        // Boost contrast slightly
        this.applyContrast(15);
        // Sharpen once
        this.applySharpen();
    }

    /**
     * Visualize detections with bounding boxes
     */
    visualizeDetections(detections, type) {
        const overlay = document.getElementById('detectionsOverlay');
        overlay.innerHTML = '';
        overlay.style.width = this.canvas.width + 'px';
        overlay.style.height = this.canvas.height + 'px';

        detections.forEach(det => {
            const box = document.createElement('div');
            box.className = 'detection-box';

            if (type === 'face') {
                const x = det.xMin * this.canvas.width;
                const y = det.yMin * this.canvas.height;
                const w = det.width * this.canvas.width;
                const h = det.height * this.canvas.height;

                box.style.left = x + 'px';
                box.style.top = y + 'px';
                box.style.width = w + 'px';
                box.style.height = h + 'px';

                const label = document.createElement('div');
                label.className = 'detection-label';
                label.textContent = `Face (${Math.round(det.score * 100)}%)`;
                box.appendChild(label);
            } else if (type === 'object') {
                const [x, y, w, h] = det.bbox;
                box.style.left = x + 'px';
                box.style.top = y + 'px';
                box.style.width = w + 'px';
                box.style.height = h + 'px';

                const label = document.createElement('div');
                label.className = 'detection-label';
                label.textContent = `${det.class} (${Math.round(det.score * 100)}%)`;
                box.appendChild(label);
            }

            overlay.appendChild(box);
        });
    }

    /**
     * Gaussian blur implementation
     */
    applyGaussianBlur(imageData, radius) {
        const width = imageData.width;
        const height = imageData.height;
        const data = new Uint8ClampedArray(imageData.data);
        const output = new Uint8ClampedArray(data.length);

        const kernel = this.createGaussianKernel(radius);
        const kernelSize = kernel.length;
        const half = Math.floor(kernelSize / 2);

        // Horizontal pass
        for (let y = 0; y < height; y++) {
            for (let x = 0; x < width; x++) {
                let r = 0, g = 0, b = 0, a = 0, weightSum = 0;

                for (let kx = -half; kx <= half; kx++) {
                    const px = Math.min(width - 1, Math.max(0, x + kx));
                    const idx = (y * width + px) * 4;
                    const weight = kernel[kx + half];

                    r += data[idx] * weight;
                    g += data[idx + 1] * weight;
                    b += data[idx + 2] * weight;
                    a += data[idx + 3] * weight;
                    weightSum += weight;
                }

                const outIdx = (y * width + x) * 4;
                output[outIdx] = r / weightSum;
                output[outIdx + 1] = g / weightSum;
                output[outIdx + 2] = b / weightSum;
                output[outIdx + 3] = a / weightSum;
            }
        }

        // Vertical pass
        const output2 = new Uint8ClampedArray(data.length);
        for (let y = 0; y < height; y++) {
            for (let x = 0; x < width; x++) {
                let r = 0, g = 0, b = 0, a = 0, weightSum = 0;

                for (let ky = -half; ky <= half; ky++) {
                    const py = Math.min(height - 1, Math.max(0, y + ky));
                    const idx = (py * width + x) * 4;
                    const weight = kernel[ky + half];

                    r += output[idx] * weight;
                    g += output[idx + 1] * weight;
                    b += output[idx + 2] * weight;
                    a += output[idx + 3] * weight;
                    weightSum += weight;
                }

                const outIdx = (y * width + x) * 4;
                output2[outIdx] = r / weightSum;
                output2[outIdx + 1] = g / weightSum;
                output2[outIdx + 2] = b / weightSum;
                output2[outIdx + 3] = a / weightSum;
            }
        }

        return new ImageData(output2, width, height);
    }

    /**
     * Create Gaussian kernel
     */
    createGaussianKernel(radius) {
        const sigma = radius / 3;
        const size = 2 * radius + 1;
        const kernel = new Float32Array(size);
        let sum = 0;

        for (let i = 0; i < size; i++) {
            const x = i - radius;
            kernel[i] = Math.exp(-(x * x) / (2 * sigma * sigma));
            sum += kernel[i];
        }

        // Normalize
        for (let i = 0; i < size; i++) {
            kernel[i] /= sum;
        }

        return kernel;
    }

    /**
     * Brightness control
     */
    showBrightnessControl() {
        const controlsEl = document.getElementById('controls');
        controlsEl.style.display = 'grid';
        controlsEl.innerHTML = `
            <div class="control-group">
                <label>Brightness</label>
                <input type="range" class="slider" min="-100" max="100" value="0" id="brightnessSlider">
                <p style="margin-top: 0.5rem; font-weight: 600;" id="brightnessValue">0</p>
            </div>
        `;

        const slider = document.getElementById('brightnessSlider');
        const valueEl = document.getElementById('brightnessValue');

        slider.addEventListener('input', (e) => {
            const value = parseInt(e.target.value);
            valueEl.textContent = value;
            this.applyBrightness(value);
        });
    }

    /**
     * Apply brightness adjustment
     */
    applyBrightness(value) {
        this.displayImage(this.originalImage);
        const imageData = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
        const data = imageData.data;

        for (let i = 0; i < data.length; i += 4) {
            data[i] = Math.min(255, Math.max(0, data[i] + value));
            data[i + 1] = Math.min(255, Math.max(0, data[i + 1] + value));
            data[i + 2] = Math.min(255, Math.max(0, data[i + 2] + value));
        }

        this.ctx.putImageData(imageData, 0, 0);
    }

    /**
     * Contrast control
     */
    showContrastControl() {
        const controlsEl = document.getElementById('controls');
        controlsEl.style.display = 'grid';
        controlsEl.innerHTML = `
            <div class="control-group">
                <label>Contrast</label>
                <input type="range" class="slider" min="-100" max="100" value="0" id="contrastSlider">
                <p style="margin-top: 0.5rem; font-weight: 600;" id="contrastValue">0</p>
            </div>
        `;

        const slider = document.getElementById('contrastSlider');
        const valueEl = document.getElementById('contrastValue');

        slider.addEventListener('input', (e) => {
            const value = parseInt(e.target.value);
            valueEl.textContent = value;
            this.applyContrast(value);
        });
    }

    /**
     * Apply contrast adjustment
     */
    applyContrast(value) {
        this.displayImage(this.originalImage);
        const imageData = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
        const data = imageData.data;
        const factor = (259 * (value + 255)) / (255 * (259 - value));

        for (let i = 0; i < data.length; i += 4) {
            data[i] = Math.min(255, Math.max(0, factor * (data[i] - 128) + 128));
            data[i + 1] = Math.min(255, Math.max(0, factor * (data[i + 1] - 128) + 128));
            data[i + 2] = Math.min(255, Math.max(0, factor * (data[i + 2] - 128) + 128));
        }

        this.ctx.putImageData(imageData, 0, 0);
    }

    /**
     * Apply sharpen filter
     */
    applySharpen() {
        const imageData = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
        const sharpened = this.applyConvolution(imageData, [
            0, -1, 0,
            -1, 5, -1,
            0, -1, 0
        ]);
        this.ctx.putImageData(sharpened, 0, 0);
    }

    /**
     * Blur control
     */
    showBlurControl() {
        const controlsEl = document.getElementById('controls');
        controlsEl.style.display = 'grid';
        controlsEl.innerHTML = `
            <div class="control-group">
                <label>Blur Amount</label>
                <input type="range" class="slider" min="0" max="20" value="5" id="blurSlider">
                <p style="margin-top: 0.5rem; font-weight: 600;" id="blurValue">5</p>
            </div>
        `;

        const slider = document.getElementById('blurSlider');
        const valueEl = document.getElementById('blurValue');

        slider.addEventListener('input', (e) => {
            const value = parseInt(e.target.value);
            valueEl.textContent = value;
            this.applyBlurAmount(value);
        });
    }

    /**
     * Apply blur with specific amount
     */
    applyBlurAmount(radius) {
        this.displayImage(this.originalImage);
        if (radius > 0) {
            const imageData = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
            const blurred = this.applyGaussianBlur(imageData, radius);
            this.ctx.putImageData(blurred, 0, 0);
        }
    }

    /**
     * Apply convolution kernel
     */
    applyConvolution(imageData, kernel) {
        const width = imageData.width;
        const height = imageData.height;
        const data = imageData.data;
        const output = new Uint8ClampedArray(data.length);

        for (let y = 0; y < height; y++) {
            for (let x = 0; x < width; x++) {
                let r = 0, g = 0, b = 0;

                for (let ky = -1; ky <= 1; ky++) {
                    for (let kx = -1; kx <= 1; kx++) {
                        const px = Math.min(width - 1, Math.max(0, x + kx));
                        const py = Math.min(height - 1, Math.max(0, y + ky));
                        const idx = (py * width + px) * 4;
                        const weight = kernel[(ky + 1) * 3 + (kx + 1)];

                        r += data[idx] * weight;
                        g += data[idx + 1] * weight;
                        b += data[idx + 2] * weight;
                    }
                }

                const outIdx = (y * width + x) * 4;
                output[outIdx] = Math.min(255, Math.max(0, r));
                output[outIdx + 1] = Math.min(255, Math.max(0, g));
                output[outIdx + 2] = Math.min(255, Math.max(0, b));
                output[outIdx + 3] = data[outIdx + 3];
            }
        }

        return new ImageData(output, width, height);
    }

    /**
     * Download edited image
     */
    downloadImage() {
        this.canvas.toBlob((blob) => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'edited-image-' + Date.now() + '.png';
            a.click();
            URL.revokeObjectURL(url);
        });
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    window.aiEditor = new AIImageEditor();
});

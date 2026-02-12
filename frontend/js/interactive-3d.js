/**
 * Interactive 3D Elements - Performance Optimized
 * ConvertRocket Ultra-Premium Experience
 */

(function () {
    'use strict';

    // Configuration
    const CONFIG = {
        orbSmoothness: 0.08,
        tiltIntensity: 10,
        parallaxIntensity: 20,
        particleCount: 5,
        enableMobileEffects: window.innerWidth > 768
    };

    // Mouse position
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let targetX = mouseX;
    let targetY = mouseY;

    // Track mouse movement with throttling for performance
    let lastMove = 0;
    document.addEventListener('mousemove', (e) => {
        const now = Date.now();
        if (now - lastMove < 16) return; // ~60fps throttle
        lastMove = now;
        mouseX = e.clientX;
        mouseY = e.clientY;

        // Update orb position directly for immediate feedback (better performance than loop)
        const orb = document.getElementById('interactive-orb');
        if (orb) {
            orb.style.left = `${mouseX}px`;
            orb.style.top = `${mouseY}px`;
        }
    });

    /**
     * Interactive Orb - CSS Optimized
     */
    function initInteractiveOrb() {
        const orb = document.getElementById('interactive-orb');
        if (!orb) return;

        // Set initial styles for CSS-based smoothing
        orb.style.position = 'fixed';
        orb.style.pointerEvents = 'none';
        orb.style.zIndex = '-5';
        orb.style.width = '300px';
        orb.style.height = '300px';
        orb.style.borderRadius = '50%';
        orb.style.background = 'radial-gradient(circle, rgba(0, 242, 255, 0.15) 0%, transparent 70%)';
        orb.style.filter = 'blur(40px)';
        orb.style.transform = 'translate(-50%, -50%)';
        orb.style.transition = 'left 0.1s ease-out, top 0.1s ease-out';
    }

    /**
     * 3D Card Tilt Effect
     */
    function init3DCardTilt() {
        const cards = document.querySelectorAll('.tool-card-3d, .glass-panel-3d, .square-item');

        cards.forEach(card => {
            card.addEventListener('mousemove', function (e) {
                if (!CONFIG.enableMobileEffects) return;

                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const centerX = rect.width / 2;
                const centerY = rect.height / 2;

                const rotateX = ((y - centerY) / centerY) * CONFIG.tiltIntensity;
                const rotateY = ((centerX - x) / centerX) * CONFIG.tiltIntensity;

                this.style.transform = `
                    perspective(1000px)
                    rotateX(${rotateX}deg)
                    rotateY(${rotateY}deg)
                    translateZ(10px)
                    scale(1.02)
                `;
            });

            card.addEventListener('mouseleave', function () {
                this.style.transform = '';
            });
        });
    }

    /**
     * Parallax Background Elements
     */
    function initParallax() {
        const parallaxElements = document.querySelectorAll('.orb-3d, .cube-minimal, .ring-3d-container');

        if (parallaxElements.length === 0 || !CONFIG.enableMobileEffects) return;

        let lastUpdate = 0;
        function updateParallax() {
            const now = Date.now();
            if (now - lastUpdate < 32) { // ~30fps for parallax is plenty
                requestAnimationFrame(updateParallax);
                return;
            }
            lastUpdate = now;

            const scrollY = window.scrollY;
            const centerX = window.innerWidth / 2;
            const centerY = window.innerHeight / 2;

            const offsetX = (mouseX - centerX) / centerX;
            const offsetY = (mouseY - centerY) / centerY;

            parallaxElements.forEach((el, index) => {
                const speed = (index + 1) * 0.5;
                const x = offsetX * CONFIG.parallaxIntensity * speed;
                const y = offsetY * CONFIG.parallaxIntensity * speed - scrollY * 0.3;

                el.style.transform = `translate(${x}px, ${y}px)`;
            });

            requestAnimationFrame(updateParallax);
        }

        updateParallax();
    }

    /**
     * Smooth Scroll to Element
     */
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const href = this.getAttribute('href');
                if (href === '#') return;

                e.preventDefault();
                const target = document.querySelector(href);

                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    /**
     * Intersection Observer for Fade-in Animations
     */
    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        document.querySelectorAll('.tool-section, .tool-card, .dashboard-card').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });
    }

    /**
     * Add Ripple Effect to Buttons
     */
    function initRippleEffect() {
        document.querySelectorAll('.cmd-tab, .download-btn, .tap-scale').forEach(button => {
            button.addEventListener('click', function (e) {
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;

                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.classList.add('ripple');

                this.appendChild(ripple);

                setTimeout(() => ripple.remove(), 600);
            });
        });

        // Add CSS for ripple
        if (!document.getElementById('ripple-style')) {
            const style = document.createElement('style');
            style.id = 'ripple-style';
            style.textContent = `
                .ripple {
                    position: absolute;
                    border-radius: 50%;
                    background: rgba(255, 255, 255, 0.3);
                    transform: scale(0);
                    animation: ripple-animation 0.6s ease-out;
                    pointer-events: none;
                }
                @keyframes ripple-animation {
                    to {
                        transform: scale(2);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }

    /**
     * Performance Monitor (Development)
     */
    function monitorPerformance() {
        if (window.location.search.includes('debug=true')) {
            let lastTime = performance.now();
            let frames = 0;

            function checkFPS() {
                frames++;
                const currentTime = performance.now();

                if (currentTime >= lastTime + 1000) {
                    console.log(`FPS: ${frames}`);
                    frames = 0;
                    lastTime = currentTime;
                }

                requestAnimationFrame(checkFPS);
            }

            checkFPS();
        }
    }

    /**
     * Lazy Load Images
     */
    function initLazyLoad() {
        const images = document.querySelectorAll('img[data-src]');

        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    }

    /**
     * Add floating particles dynamically
     */
    function initFloatingParticles() {
        if (!CONFIG.enableMobileEffects) return;

        const container = document.body;
        const colors = ['var(--neon-cyan)', 'var(--neon-purple)', 'var(--neon-pink)'];

        for (let i = 0; i < CONFIG.particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle-float';
            particle.style.left = `${Math.random() * 100}%`;
            particle.style.animationDelay = `${Math.random() * 8}s`;
            particle.style.animationDuration = `${8 + Math.random() * 4}s`;
            particle.style.background = colors[Math.floor(Math.random() * colors.length)];
            container.appendChild(particle);
        }
    }

    /**
     * Initialize all features
     */
    function init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        console.log('🚀 ConvertRocket Interactive 3D - Initialized');

        // Initialize features
        initInteractiveOrb();
        init3DCardTilt();
        initParallax();
        initSmoothScroll();
        initScrollAnimations();
        initRippleEffect();
        initLazyLoad();
        initFloatingParticles();
        monitorPerformance();

        // Reduce animations on low-end devices
        if (navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4) {
            document.body.classList.add('low-power');
            console.log('⚡ Low-power mode activated');
        }
    }

    // Start initialization
    init();

    // Export for testing
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = { init, CONFIG };
    }

})();

/**
 * Priyadharshini E P — Portfolio Website
 * Vanilla JavaScript: Scroll Snap, Progress Bar, Active Nav, Lightbox, Parallax
 */

document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------------------------------------------
    // 1. Initial Page Load Transition
    // -------------------------------------------------------------------------
    const pageContent = document.getElementById('pageContent');
    if (pageContent) {
        pageContent.classList.add('page-transition');
        setTimeout(() => {
            pageContent.classList.add('loaded');
        }, 50);
    }

    // -------------------------------------------------------------------------
    // 2. Responsive Mobile Menu Toggle
    // -------------------------------------------------------------------------
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            navToggle.classList.toggle('active');

            const spans = navToggle.querySelectorAll('span');
            if (navToggle.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(6px, -7px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });

        // Close mobile menu when a nav link is clicked
        navLinks.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                navToggle.classList.remove('active');
                const spans = navToggle.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            });
        });
    }

    // -------------------------------------------------------------------------
    // 3. Scroll Progress Bar
    // -------------------------------------------------------------------------
    const progressBar = document.getElementById('scrollProgressBar');

    function updateScrollProgress() {
        if (!progressBar) return;
        const scrollTop = window.scrollY || document.documentElement.scrollTop;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
        progressBar.style.width = progress + '%';
    }

    window.addEventListener('scroll', updateScrollProgress, { passive: true });
    updateScrollProgress(); // Set initial state

    // -------------------------------------------------------------------------
    // 4. Active Nav Link Highlighting (Intersection Observer)
    // -------------------------------------------------------------------------
    const sections = document.querySelectorAll('.scroll-section');
    const allNavLinks = document.querySelectorAll('.nav-link');

    if ('IntersectionObserver' in window && sections.length > 0 && allNavLinks.length > 0) {
        const activateNav = (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const sectionId = entry.target.getAttribute('id');
                    allNavLinks.forEach(link => {
                        link.classList.remove('active');
                        const href = link.getAttribute('href');
                        if (href === '#' + sectionId) {
                            link.classList.add('active');
                        }
                    });
                }
            });
        };

        const navObserver = new IntersectionObserver(activateNav, {
            root: null,
            threshold: 0,
            rootMargin: '-45% 0px -50% 0px' // Active = the section crossing the middle of the screen
        });

        sections.forEach(sec => navObserver.observe(sec));
    }

    // -------------------------------------------------------------------------
    // 5. Scroll Reveal Animation (Intersection Observer)
    // -------------------------------------------------------------------------
    const revealElements = document.querySelectorAll('.reveal');

    if ('IntersectionObserver' in window && revealElements.length > 0) {
        const revealCallback = (entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    observer.unobserve(entry.target);
                }
            });
        };

        const revealObserver = new IntersectionObserver(revealCallback, {
            root: null,
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        revealElements.forEach(el => {
            revealObserver.observe(el);
        });
    } else {
        revealElements.forEach(el => el.classList.add('revealed'));
    }

    // -------------------------------------------------------------------------
    // 6. Count-up animation for stats and metrics
    // -------------------------------------------------------------------------
    const countEls = document.querySelectorAll('[data-count]');
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const animateCount = (el) => {
        const raw = el.getAttribute('data-count');
        const match = raw.match(/^(\D*)(\d+(?:\.\d+)?)(.*)$/);
        if (!match || reduceMotion) { el.textContent = raw; return; }
        const [, prefix, numStr, suffix] = match;
        const target = parseFloat(numStr);
        const decimals = (numStr.split('.')[1] || '').length;
        const duration = 1400;
        const start = performance.now();
        const tick = (now) => {
            const t = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - t, 3);
            el.textContent = prefix + (target * eased).toFixed(decimals) + suffix;
            if (t < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
    };

    if ('IntersectionObserver' in window && countEls.length) {
        const countObserver = new IntersectionObserver((entries, obs) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCount(entry.target);
                    obs.unobserve(entry.target);
                }
            });
        }, { threshold: 0.6 });
        countEls.forEach(el => countObserver.observe(el));
    }

    // -------------------------------------------------------------------------
    // 6b. Liquid glass: cursor-following light on glass cards
    // -------------------------------------------------------------------------
    const glassCards = document.querySelectorAll(
        '.stat, .skill-category-card, .education-card, .paper-main, .project-card, .courses-card, .cert-card, .contact-form-col'
    );
    const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    if (finePointer && !reduceMotion) {
        glassCards.forEach(card => {
            card.addEventListener('pointermove', (e) => {
                const r = card.getBoundingClientRect();
                card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
                card.style.setProperty('--my', (e.clientY - r.top) + 'px');
            });
            card.addEventListener('pointerenter', () => card.classList.add('is-lit'));
            card.addEventListener('pointerleave', () => card.classList.remove('is-lit'));
        });
    }

    // -------------------------------------------------------------------------
    // 7. Certificate Gallery Lightbox
    // -------------------------------------------------------------------------
    const certCards = document.querySelectorAll('.cert-card');
    const lightbox = document.getElementById('certLightbox');
    const lightboxImg = document.getElementById('lightboxImg');
    const lightboxCaption = document.getElementById('lightboxCaption');
    const lightboxClose = document.getElementById('lightboxClose');

    if (lightbox && lightboxImg && lightboxClose) {
        certCards.forEach(card => {
            card.addEventListener('click', () => {
                const imgUrl = card.getAttribute('data-image');
                const title = card.getAttribute('data-title');

                lightboxImg.src = imgUrl;
                lightboxImg.alt = title;
                lightboxCaption.textContent = title;

                lightbox.classList.add('active');
                lightbox.setAttribute('aria-hidden', 'false');
                document.body.style.overflow = 'hidden';
            });
        });

        const closeLightboxFunc = () => {
            lightbox.classList.remove('active');
            lightbox.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
            setTimeout(() => {
                lightboxImg.src = '';
            }, 300);
        };

        lightboxClose.addEventListener('click', closeLightboxFunc);

        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) {
                closeLightboxFunc();
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && lightbox.classList.contains('active')) {
                closeLightboxFunc();
            }
        });
    }

    // -------------------------------------------------------------------------
    // 8. Smooth Mouse Parallax on Hero Portrait
    // -------------------------------------------------------------------------
    const heroWrapper = document.getElementById('heroPhotoWrapper');
    const heroImg = document.querySelector('.hero-img');

    if (heroWrapper && heroImg && window.innerWidth > 1024) {
        heroWrapper.addEventListener('mousemove', (e) => {
            const rect = heroWrapper.getBoundingClientRect();
            const x = e.clientX - rect.left - (rect.width / 2);
            const y = e.clientY - rect.top - (rect.height / 2);

            const moveX = (x / rect.width) * 15;
            const moveY = (y / rect.height) * 15;

            heroImg.style.transform = `scale(1.05) translate(${moveX}px, ${moveY}px)`;
        });

        heroWrapper.addEventListener('mouseleave', () => {
            heroImg.style.transform = 'none';
        });
    }

    // -------------------------------------------------------------------------
    // 9. Hide Scroll Down Indicator after scrolling past hero
    // -------------------------------------------------------------------------
    const scrollIndicator = document.querySelector('.scroll-down-indicator');
    if (scrollIndicator) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 200) {
                scrollIndicator.style.opacity = '0';
                scrollIndicator.style.pointerEvents = 'none';
            } else {
                scrollIndicator.style.opacity = '1';
                scrollIndicator.style.pointerEvents = 'auto';
            }
        }, { passive: true });
    }
});

/* ============================================
   TENSIX — Main JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {
  const safeInit = (name, initFn) => {
    try {
      if (typeof initFn === 'function') initFn();
    } catch (err) {
      console.warn(`[SafeInit] Failed to load ${name}:`, err);
    }
  };

  // Critical path — runs immediately, needed for layout/UX
  safeInit('initMobileNav', initMobileNav);
  safeInit('initScrollHeader', initScrollHeader);
  safeInit('initReveal', initReveal);
  safeInit('initSmoothScroll', initSmoothScroll);
  safeInit('initContactForm', initContactForm);
  safeInit('initScrollProgress', initScrollProgress);
  safeInit('initParallaxHero', initParallaxHero);
  safeInit('initPageTransition', initPageTransition);

  // Deferred — visual-only enhancements, defer until browser is idle
  const ric = window.requestIdleCallback || (fn => setTimeout(fn, 200));
  ric(() => {
    safeInit('initCursorGlow', initCursorGlow);
    safeInit('initSpotlightCards', initSpotlightCards);
    safeInit('initTiltCards', initTiltCards);
    safeInit('initMagneticDock', initMagneticDock);
    safeInit('initRippleButtons', initRippleButtons);
    safeInit('initGA4Tracking', initGA4Tracking);
  });
});

/* ── Mobile Navigation ──────────────────────── */
function initMobileNav() {
  const toggle = document.querySelector('.nav-toggle');
  const nav    = document.querySelector('.nav');
  if (!toggle || !nav) return;

  toggle.addEventListener('click', function () {
    const open = nav.classList.toggle('open');
    toggle.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });

  // Close on link click
  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      nav.classList.remove('open');
      toggle.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    });
  });

  // Close on outside click
  document.addEventListener('click', function (e) {
    if (nav.classList.contains('open') && !nav.contains(e.target) && !toggle.contains(e.target)) {
      nav.classList.remove('open');
      toggle.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    }
  });
}

/* ── Header Scroll Effect ───────────────────── */
function initScrollHeader() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  let isScrolled = false;
  let ticking = false;

  // Initialize state asynchronously in next frame to prevent forced reflow during page boot
  window.requestAnimationFrame(() => {
    isScrolled = (window.scrollY || 0) > 60;
    if (isScrolled) header.classList.add('scrolled');
  });

  const onScroll = () => {
    const currentScroll = (window.scrollY || 0) > 60;
    if (currentScroll !== isScrolled) {
      isScrolled = currentScroll;
      if (!ticking) {
        window.requestAnimationFrame(() => {
          header.classList.toggle('scrolled', isScrolled);
          ticking = false;
        });
        ticking = true;
      }
    }
  };
  window.addEventListener('scroll', onScroll, { passive: true });
}

/* ── Reveal on Scroll ───────────────────────── */
function initReveal() {
  const elements = document.querySelectorAll(
    '.reveal, .reveal-blur, .reveal-left, .reveal-right, .reveal-scale'
  );
  if (!elements.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  elements.forEach(el => observer.observe(el));
}

/* ── Skill Bar Animations ───────────────────── */
function initSkillBars() {
  const bars = document.querySelectorAll('.skill-fill');
  if (!bars.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const bar = entry.target;
        const width = bar.getAttribute('data-width') || '0%';
        setTimeout(() => { bar.style.width = width; }, 200);
        setTimeout(() => { bar.classList.add('filled'); }, 1900);
        observer.unobserve(bar);
      }
    });
  }, { threshold: 0.5 });

  bars.forEach(bar => observer.observe(bar));
}

/* ── Smooth Scroll (anchor links) ───────────── */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const id = this.getAttribute('href');
      if (id === '#') return;
      const target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        const offset = 80;
        window.scrollTo({
          top: target.getBoundingClientRect().top + window.scrollY - offset,
          behavior: 'smooth'
        });
      }
    });
  });
}

/* ── Typewriter (Typed.js if loaded, fallback if not) ── */
function initTypewriter() {
  const el = document.getElementById('typed-text');
  if (!el) return;

  const strings = [
    'Autonomous AI Agents & Multi-Agent Systems',
    'Enterprise SaaS & FastAPI Backends',
    'Oracle & Plesk VPS CI/CD Infrastructure',
    'GraphRAG & Knowledge Extraction Pipelines',
    'Generative Engine Optimization (GEO & AEO)',
    'High-Velocity Data Scraping & n8n Workflows'
  ];

  if (typeof Typed !== 'undefined') {
    new Typed('#typed-text', {
      strings,
      typeSpeed: 70,
      backSpeed: 45,
      backDelay: 2000,
      startDelay: 500,
      loop: true,
      showCursor: false
    });
  } else {
    // Simple fallback typewriter
    let si = 0, ci = 0, deleting = false;
    function tick() {
      const str = strings[si];
      if (!deleting) {
        el.textContent = str.slice(0, ci + 1);
        ci++;
        if (ci === str.length) {
          deleting = true;
          setTimeout(tick, 2000);
          return;
        }
      } else {
        el.textContent = str.slice(0, ci - 1);
        ci--;
        if (ci === 0) {
          deleting = false;
          si = (si + 1) % strings.length;
        }
      }
      setTimeout(tick, deleting ? 40 : 80);
    }
    setTimeout(tick, 600);
  }
}



/* ── Contact Form ───────────────────────────── */
function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  // Pricing cards link to /contact?plan=<slug>: keep the plan with the inquiry.
  const plan = (new URLSearchParams(location.search).get('plan') || '').toLowerCase().replace(/[^a-z0-9-]/g, '').slice(0, 40);
  const planInput = document.getElementById('cf-plan');
  if (plan && planInput) {
    planInput.value = plan;
    const typeByPrefix = { ai: 'mas', software: 'fullstack', web: 'fullstack', cloud: 'cloud_vps', email: 'cloud_vps', scraper: 'scraping', retainer: 'consultation', geo: 'geo_aeo' };
    const typeSelect = document.getElementById('cf-type');
    const type = typeByPrefix[plan.split('-')[0]];
    if (typeSelect && type) typeSelect.value = type;
    const subjectInput = document.getElementById('cf-subject');
    if (subjectInput && !subjectInput.value) subjectInput.value = 'Inquiry: ' + plan;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Quick validation
    const nameInput = document.getElementById('cf-name');
    const emailInput = document.getElementById('cf-email');
    const messageInput = document.getElementById('cf-message');

    if (!nameInput || !emailInput || !messageInput) return;

    if (!nameInput.value.trim() || !emailInput.value.trim() || !messageInput.value.trim()) {
      showToast('Please fill out all required fields.', 'error');
      return;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(emailInput.value.trim())) {
      showToast('Please enter a valid email address.', 'error');
      return;
    }

    if (messageInput.value.trim().length < 10) {
      showToast('Message must be at least 10 characters long.', 'error');
      return;
    }

    const btn = form.querySelector('[type="submit"]');
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.textContent = 'Sending…';

    const formData = {
      name: nameInput.value,
      email: emailInput.value,
      subject: document.getElementById('cf-subject')?.value || 'General Inquiry',
      project_type: document.getElementById('cf-type')?.value || 'Other',
      message: messageInput.value,
      plan: planInput ? planInput.value : ''
    };

    // Primary path: High-speed Supabase /api/contact endpoint with fallback
    fetch('/api/contact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(formData)
    })
    .then(async response => {
      if (response.ok) {
        return response.json();
      }
      // If /api/contact is unavailable (e.g. static preview), fallback to FormSubmit
      return fetch('https://formsubmit.co/ajax/contact@tensix.in', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(formData)
      }).then(r => r.json());
    })
    .then(data => {
      btn.innerHTML = originalText;
      btn.disabled = false;

      if (data.success === "true" || data.success === true) {
        form.reset();
        showToast('Consultation request transmitted! Saved to TENSIX database.', 'success');
        const successEl = document.getElementById('form-success');
        if (successEl) {
          successEl.style.display = 'block';
          setTimeout(() => { successEl.style.display = 'none'; }, 5000);
        }
        // GA4 Conversion Events
        trackGA4Event('generate_lead', {
          event_category: 'Contact',
          event_label: formData.subject,
          project_type: formData.project_type
        });
        trackGA4Event('contact_form_submit', {
          event_category: 'Form',
          event_label: formData.subject,
          project_type: formData.project_type
        });
      } else {
        showToast(data.error || 'Oops! Something went wrong. Please try again.', 'error');
      }
    })
    .catch(error => {
      // Final resilient fallback: try FormSubmit directly
      fetch('https://formsubmit.co/ajax/contact@tensix.in', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(formData)
      })
      .then(r => r.json())
      .then(() => {
        btn.innerHTML = originalText;
        btn.disabled = false;
        form.reset();
        showToast('Consultation request transmitted!', 'success');
      })
      .catch(() => {
        btn.innerHTML = originalText;
        btn.disabled = false;
        showToast('Connection error. Please check your network.', 'error');
      });
      console.error('Error submitting form:', error);
    });
  });
}

/* ── Toast ──────────────────────── */
function showToast(message, type = 'info') {
  let toast = document.getElementById('site-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'site-toast';
    toast.className = 'toast';
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.className = `toast ${type}`;
  requestAnimationFrame(() => {
    requestAnimationFrame(() => { toast.classList.add('show'); });
  });
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => {
    toast.classList.remove('show');
  }, 4000);
}

/* ── Dock Highlight (active page) ───────────── */
function initDockHighlight() {
  const current = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.dock-btn[data-page]').forEach(btn => {
    if (btn.dataset.page === current) {
      btn.style.color = '#1D4ED8';
      btn.style.background = 'rgba(59,130,246,0.15)';
    }
  });
}

/* ============================================
   3D Animation System — New Functions
   ============================================ */

/* ── Scroll Progress Bar ────────────────────── */
function initScrollProgress() {
  const bar = document.getElementById('scrollProgress');
  if (!bar) return;
  // Use scaleX for better performance
  bar.style.transformOrigin = 'left center';
  
  let maxScroll = 1;
  let currentScroll = 0;
  let ticking = false;

  const update = () => {
    const progress = maxScroll > 0 ? (currentScroll / maxScroll) : 0;
    bar.style.transform = `scaleX(${progress})`;
    ticking = false;
  };

  const updateMax = () => {
    maxScroll = (document.documentElement.scrollHeight || document.body.scrollHeight) - window.innerHeight || 1;
    currentScroll = window.scrollY || 0;
    update();
  };

  // Defer all geometric reads and DOM writes until next frame after initial layout pass
  window.requestAnimationFrame(updateMax);
  window.addEventListener('resize', updateMax, { passive: true });

  window.addEventListener('scroll', () => {
    currentScroll = window.scrollY || 0;
    if (!ticking) {
      window.requestAnimationFrame(update);
      ticking = true;
    }
  }, { passive: true });
}

/* ── Cursor Glow ────────────────────────────── */
function initCursorGlow() {
  const el = document.getElementById('cursorGlow');
  if (!el || window.matchMedia('(pointer: coarse)').matches) return;
  
  // Prepare element for transform
  el.style.left = '0';
  el.style.top = '0';
  
  let raf;
  document.addEventListener('mousemove', e => {
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(() => {
      el.style.transform = `translate(${e.clientX}px, ${e.clientY}px) translate(-50%, -50%)`;
      el.style.opacity = '1';
    });
  }, { passive: true });
  document.addEventListener('mouseleave', () => { el.style.opacity = '0'; });
}

/* ── 3D Tilt Cards ──────────────────────────── */
function initTiltCards() {
  if (window.matchMedia('(pointer: coarse)').matches) return;

  /* Add tilt-card class + card-sheen to qualifying cards */
  document.querySelectorAll('.project-card, .skill-card, .blog-entry').forEach(card => {
    card.classList.add('tilt-card');
    if (!card.querySelector('.card-sheen')) {
      const sheen = document.createElement('div');
      sheen.className = 'card-sheen';
      card.appendChild(sheen);
    }
  });

  document.querySelectorAll('.tilt-card').forEach(card => {
    let r = null;
    let isHovering = false;
    let rafId = null;
    
    card.addEventListener('mouseenter', () => {
      r = card.getBoundingClientRect(); // Cache layout info
      isHovering = true;
    });

    // Invalidate/refresh cached coordinates if page is scrolled during hover
    window.addEventListener('scroll', () => {
      if (isHovering) r = card.getBoundingClientRect();
    }, { passive: true });

    card.addEventListener('mousemove', e => {
      if (!isHovering || !r) return;
      
      const x = (e.clientX - r.left) / r.width  - 0.5;
      const y = (e.clientY - r.top)  / r.height - 0.5;
      const rotY =  x * 10;
      const rotX = -y * 10;
      
      cancelAnimationFrame(rafId);
      rafId = requestAnimationFrame(() => {
        card.style.transform =
          `perspective(var(--perspective)) rotateY(${rotY}deg) rotateX(${rotX}deg) translateZ(6px)`;
      });
    });

    card.addEventListener('mouseleave', () => {
      isHovering = false;
      cancelAnimationFrame(rafId);
      requestAnimationFrame(() => {
        card.style.transform =
          'perspective(var(--perspective)) rotateY(0deg) rotateX(0deg) translateZ(0px)';
      });
    });
  });
}

/* ── Magnetic Dock Buttons ──────────────────── */
function initMagneticDock() {
  if (window.matchMedia('(pointer: coarse)').matches) return;
  document.querySelectorAll('.dock-btn').forEach(btn => {
    let r = null;
    let rafId = null;
    
    btn.addEventListener('mouseenter', () => {
      r = btn.getBoundingClientRect();
    });
    
    btn.addEventListener('mousemove', e => {
      if (!r) return;
      const dx = (e.clientX - (r.left + r.width  / 2)) * 0.38;
      const dy = (e.clientY - (r.top  + r.height / 2)) * 0.38;
      
      cancelAnimationFrame(rafId);
      rafId = requestAnimationFrame(() => {
        btn.style.transform =
          `scale(1.28) translate(${dx}px, ${dy}px) translateY(-4px) rotate(5deg)`;
        btn.style.filter = 'drop-shadow(0 0 8px rgba(59,130,246,0.55))';
      });
    });
    btn.addEventListener('mouseleave', () => {
      cancelAnimationFrame(rafId);
      requestAnimationFrame(() => {
        btn.style.transform = '';
        btn.style.filter    = '';
      });
    });
  });
}

/* ── Parallax Hero ──────────────────────────── */
function initParallaxHero() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const aurora      = document.querySelector('.hero-aurora');
  const heroContent = document.querySelector('.hero .hero-content');

  if (!aurora && !heroContent) return;

  let lastY = 0;
  let ticking = false;
  
  const update = () => {
    const y = window.scrollY;
    if (Math.abs(y - lastY) >= 2) {
      lastY = y;
      if (aurora)      aurora.style.transform      = `translateY(${y * 0.15}px) rotate(${y * 0.02}deg)`;
      if (heroContent) heroContent.style.transform = `translateY(${y * 0.04}px)`;
    }
    ticking = false;
  };
  
  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(update);
      ticking = true;
    }
  }, { passive: true });
}

/* ── Ripple Buttons ─────────────────────────── */
function initRippleButtons() {
  document.querySelectorAll('.hero-grid-btn, .btn, .cta-btn, .cta-hero-btn').forEach(btn => {
    btn.classList.add('ripple-btn');
    btn.addEventListener('click', e => {
      const r      = btn.getBoundingClientRect();
      const size   = 64;
      const ripple = document.createElement('span');
      ripple.style.cssText = [
        'position:absolute',
        `width:${size}px`,
        `height:${size}px`,
        'border-radius:50%',
        'background:rgba(15,23,42,0.15)',
        `top:${e.clientY - r.top  - size / 2}px`,
        `left:${e.clientX - r.left - size / 2}px`,
        'animation:rippleOut 0.55s ease forwards',
        'pointer-events:none',
        'z-index:10'
      ].join(';');
      btn.appendChild(ripple);
      ripple.addEventListener('animationend', () => ripple.remove());
    });
  });
}

/* initPageTransition removed — intercepting native navigation
   breaks browser back/forward, Ctrl+click, and middle-click.
   CSS body { animation: pageFadeIn } handles the entrance fade natively. */
function initPageTransition() {}

/* ── 21st.dev Spotlight Cards Specular Highlight ── */
function initSpotlightCards() {
  if (window.matchMedia('(pointer: coarse)').matches) return;
  const cards = document.querySelectorAll('.spotlight-card, .skill-card, .project-card, .service-item, .about-card, .stat-item');
  
  cards.forEach(card => {
    card.classList.add('spotlight-card');
    let rect = null;
    let rafId = null;

    card.addEventListener('mouseenter', () => {
      rect = card.getBoundingClientRect();
    });

    card.addEventListener('mousemove', (e) => {
      if (!rect) rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      cancelAnimationFrame(rafId);
      rafId = requestAnimationFrame(() => {
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
      });
    }, { passive: true });

    card.addEventListener('mouseleave', () => {
      cancelAnimationFrame(rafId);
    });
  });
}

/* ── GA4 Custom Event & Conversion Tracking ──── */
function trackGA4Event(eventName, params = {}) {
  try {
    if (typeof window.gtag === 'function') {
      window.gtag('event', eventName, params);
    }
  } catch (err) {
    console.debug('[GA4] Event dispatch ignored:', err);
  }
}

function initGA4Tracking() {
  // 1. CTA Button Tracking
  const ctaSelectors = '.cta-button, .cta-hero-btn, .nav-cta, .hero-grid-btn, .hero-buttons a, .form-submit';
  document.querySelectorAll(ctaSelectors).forEach(btn => {
    btn.addEventListener('click', () => {
      const btnText = (btn.innerText || btn.textContent || 'CTA').trim();
      const targetUrl = btn.getAttribute('href') || 'submit';
      trackGA4Event('cta_click', {
        event_category: 'Engagement',
        cta_text: btnText,
        cta_target: targetUrl,
        page_location: window.location.pathname
      });
    });
  });

  // 2. Outbound Links & Social Tracking
  document.querySelectorAll('a[href]').forEach(link => {
    const href = link.getAttribute('href');
    if (!href) return;

    if (href.startsWith('http://') || href.startsWith('https://')) {
      try {
        const url = new URL(href);
        if (url.hostname !== window.location.hostname) {
          link.addEventListener('click', () => {
            trackGA4Event('outbound_click', {
              event_category: 'Outbound Link',
              link_domain: url.hostname,
              link_url: href,
              link_text: (link.innerText || link.getAttribute('aria-label') || url.hostname).trim()
            });
          });
        }
      } catch (e) {}
    } else if (href.startsWith('mailto:')) {
      link.addEventListener('click', () => {
        trackGA4Event('contact_email_click', {
          event_category: 'Lead',
          email_address: href.replace('mailto:', '').split('?')[0]
        });
      });
    }
  });

  // 3. Scroll Depth Milestones (50%, 75%, 90%)
  const scrollMilestones = { 50: false, 75: false, 90: false };
  let scrollTicking = false;
  window.addEventListener('scroll', () => {
    if (!scrollTicking) {
      window.requestAnimationFrame(() => {
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        if (docHeight > 0) {
          const scrollPercent = Math.round((window.scrollY / docHeight) * 100);
          [50, 75, 90].forEach(threshold => {
            if (scrollPercent >= threshold && !scrollMilestones[threshold]) {
              scrollMilestones[threshold] = true;
              trackGA4Event('scroll_depth', {
                event_category: 'Content Engagement',
                percent_scrolled: threshold,
                page_path: window.location.pathname
              });
            }
          });
        }
        scrollTicking = false;
      });
      scrollTicking = true;
    }
  }, { passive: true });
}

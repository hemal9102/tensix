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
  safeInit('initAgentAudit', initAgentAudit);
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
      return fetch('https://formsubmit.co/ajax/hemal.shah2004@gmail.com', {
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
      fetch('https://formsubmit.co/ajax/hemal.shah2004@gmail.com', {
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

/* ── Toast Notification ─────────────────────── */
/* ── Agent Readiness Check (/is-my-site-ai-ready) ──
   Scan data comes from Cloudflare's public scanner. We only read it.
   Triage note: only `core` checks affect an ordinary business site. Labelling
   the rest as losses would be an unverifiable claim (CLAUDE.md §5). */
const AUDIT_CHECKS = {
  robotsTxt: { label: 'robots.txt file', priority: 'core',
    cost: 'Crawlers have to guess what they are allowed to read, and some skip the site rather than guess.' },
  sitemap: { label: 'XML sitemap', priority: 'core',
    cost: 'New and deep pages can go unnoticed for weeks, because nothing tells crawlers they exist.' },
  linkHeaders: { label: 'Link headers', priority: 'core',
    cost: 'Agents cannot find your machine-readable files without downloading and parsing a full page first.' },
  robotsTxtAiRules: { label: 'Rules for AI crawlers', priority: 'core',
    cost: 'You have no stated position on AI crawlers, so each one applies its own default instead of yours.' },
  contentSignals: { label: 'Content signals', priority: 'core',
    cost: 'You are not saying whether your content may be used for training, search or AI answers.' },
  markdownNegotiation: { label: 'Plain-text version of pages', priority: 'core',
    cost: 'AI tools read your layout and scripts along with your words, so they quote you less accurately.' },
  agentSkills: { label: 'Published agent skills', priority: 'core',
    cost: 'Assistants have to guess how to get a quote or make a booking, so they often send people elsewhere.' },

  dnsAid: { label: 'DNS agent discovery', priority: 'advanced',
    cost: 'Only relevant once you run a live agent endpoint for agents to connect to.' },
  webBotAuth: { label: 'Signed bot identity', priority: 'advanced',
    cost: 'Only relevant if your own crawler needs to prove who it is to other websites.' },
  apiCatalog: { label: 'API catalogue', priority: 'advanced',
    cost: 'Only relevant if you publish an API you want machines to discover.' },
  oauthDiscovery: { label: 'OAuth and OpenID discovery', priority: 'advanced',
    cost: 'Only relevant if you run an API that requires a login.' },
  oauthProtectedResource: { label: 'OAuth protected-resource metadata', priority: 'advanced',
    cost: 'Only relevant if you run an API that requires a login.' },
  authMd: { label: 'Agent registration file', priority: 'advanced',
    cost: 'Only relevant if agents need to register for credentials with you.' },
  mcpServerCard: { label: 'MCP server card', priority: 'advanced',
    cost: 'Only relevant if you run an MCP server for agents to call.' },
  a2aAgentCard: { label: 'Agent-to-agent card', priority: 'advanced',
    cost: 'Only relevant if you run an agent that other agents talk to.' },
  webMcp: { label: 'Browser tools for agents', priority: 'advanced',
    cost: 'Only relevant if you want agents to use your forms on the visitor behalf.' },
  ard: { label: 'Agentic resource catalogue', priority: 'advanced',
    cost: 'Only relevant once you have machine-readable resources worth listing.' },

  x402: { label: 'Pay-per-request (x402)', priority: 'commerce',
    cost: 'Only relevant if you want agents to pay you per request.' },
  mpp: { label: 'Machine payment protocol', priority: 'commerce',
    cost: 'Only relevant if your API charges per call.' },
  ucp: { label: 'Universal commerce profile', priority: 'commerce',
    cost: 'Only relevant if you sell a product catalogue to agents.' },
  acp: { label: 'Agentic commerce protocol', priority: 'commerce',
    cost: 'Only relevant if you accept orders placed by agents.' },
  ap2: { label: 'Agent payments (AP2)', priority: 'commerce',
    cost: 'Only relevant if you accept payments made by agents.' }
};

function initAgentAudit() {
  const form = document.getElementById('audit-form');
  if (!form) return;

  const input = document.getElementById('audit-url');
  const statusEl = document.getElementById('audit-status');
  const resultsWrap = document.getElementById('results-section');
  const results = document.getElementById('audit-results');
  const btn = form.querySelector('[type="submit"]');
  const SCAN_API = 'https://isitagentready.com/api/scan';

  const el = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  };

  // AbortSignal.timeout is recent; fall back for older browsers.
  function timeoutSignal(ms) {
    if (AbortSignal.timeout) return AbortSignal.timeout(ms);
    const c = new AbortController();
    setTimeout(() => c.abort(new DOMException('Timeout', 'TimeoutError')), ms);
    return c.signal;
  }

  function normalise(raw) {
    const v = (raw || '').trim();
    if (!v) return '';
    return /^https?:\/\//i.test(v) ? v : 'https://' + v;
  }

  function flatten(checks) {
    const out = [];
    if (!checks || typeof checks !== 'object') return out;
    Object.keys(checks).forEach(cat => {
      const group = checks[cat];
      if (!group || typeof group !== 'object') return;
      Object.keys(group).forEach(name => {
        const c = group[name] || {};
        out.push({ category: cat, name: name, status: c.status,
                   message: c.message, durationMs: c.durationMs });
      });
    });
    return out;
  }

  function renderCheck(c, fixes) {
    const meta = AUDIT_CHECKS[c.name] || { label: c.name, cost: '', priority: 'core' };
    const row = el('div', 'audit-check');
    const head = el('div', 'audit-check-head');
    head.appendChild(el('span', 'audit-check-name', meta.label));

    const st = typeof c.status === 'string' ? c.status : 'neutral';
    const pillClass = (st === 'pass' || st === 'fail') ? st : 'neutral';
    head.appendChild(el('span', 'audit-pill ' + pillClass, st));

    if (c.durationMs != null) head.appendChild(el('span', 'audit-ms', c.durationMs + ' ms'));
    row.appendChild(head);

    // Our plain-language reading, or Cloudflare's own message when we have none.
    const line = meta.cost || c.message;
    if (line) row.appendChild(el('p', 'audit-cost', line));

    const fix = fixes.get(c.name);
    if (fix && (fix.description || (fix.specUrls && fix.specUrls.length))) {
      const p = el('p', 'audit-from');
      p.appendChild(el('b', null, 'From Cloudflare: '));
      if (fix.description) p.appendChild(document.createTextNode(fix.description));
      (fix.specUrls || []).slice(0, 3).forEach(u => {
        p.appendChild(document.createTextNode(' '));
        if (typeof u === 'string' && /^https:\/\//.test(u)) {
          const a = el('a', null, u);
          a.href = u; a.target = '_blank'; a.rel = 'noopener noreferrer';
          p.appendChild(a);
        } else if (typeof u === 'string') {
          p.appendChild(el('span', null, u));
        }
      });
      row.appendChild(p);
    }
    return row;
  }

  function render(data, scannedUrl) {
    results.textContent = '';

    const banner = el('div', 'audit-level');
    banner.appendChild(el('span', 'audit-level-num',
      data.level != null ? String(data.level) : '?'));
    const col = el('div');
    col.appendChild(el('div', 'audit-level-name',
      'Level ' + (data.level != null ? data.level : '?') +
      (data.levelName ? ' — ' + data.levelName : '')));
    col.appendChild(el('div', 'audit-level-url', scannedUrl));
    banner.appendChild(col);
    results.appendChild(banner);

    const fixes = new Map();
    const reqs = (data.nextLevel && data.nextLevel.requirements) || [];
    if (Array.isArray(reqs)) reqs.forEach(r => { if (r && r.check) fixes.set(r.check, r); });

    const all = flatten(data.checks);
    const core = all.filter(c => (AUDIT_CHECKS[c.name] || { priority: 'core' }).priority === 'core');
    const rest = all.filter(c => core.indexOf(c) === -1);

    const main = el('div', 'audit-group');
    main.appendChild(el('h3', null, 'What matters for your site'));
    main.appendChild(el('p', 'audit-group-note',
      core.filter(c => c.status === 'fail').length + ' of ' + core.length +
      ' of these need attention.'));
    core.forEach(c => main.appendChild(renderCheck(c, fixes)));
    results.appendChild(main);

    if (rest.length) {
      const d = el('details', 'audit-advanced');
      d.appendChild(el('summary', null,
        'Advanced and shopping checks (' + rest.length +
        ') — most business sites can ignore these'));
      const box = el('div', 'audit-group');
      rest.forEach(c => box.appendChild(renderCheck(c, fixes)));
      d.appendChild(box);
      results.appendChild(d);
    }

    const h = main.querySelector('h3');
    if (h) { h.setAttribute('tabindex', '-1'); h.focus(); }
  }

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    const url = normalise(input && input.value);
    if (!url) {
      showToast('Enter your website address, like https://example.com', 'error');
      return;
    }

    const original = btn ? btn.innerHTML : '';
    if (btn) { btn.disabled = true; btn.textContent = 'Scanning…'; }
    results.setAttribute('aria-busy', 'true');

    // Static sentence set once so screen readers are not re-interrupted;
    // the ticking number is hidden from them.
    statusEl.textContent = '';
    statusEl.appendChild(document.createTextNode('Scanning. '));
    const ticker = el('span', null, '0.0s');
    ticker.setAttribute('aria-hidden', 'true');
    statusEl.appendChild(ticker);
    statusEl.appendChild(document.createTextNode(
      ' elapsed. Cloudflare runs 22 checks, including one that loads your site in a real ' +
      'browser. This usually takes 10 to 15 seconds.'));

    const t0 = Date.now();
    const tick = setInterval(() => {
      ticker.textContent = ((Date.now() - t0) / 1000).toFixed(1) + 's';
    }, 100);

    try {
      const res = await fetch(SCAN_API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url, format: 'json' }),
        signal: timeoutSignal(30000)
      });
      if (!res.ok) throw new Error('upstream ' + res.status);
      const data = await res.json();
      resultsWrap.hidden = false;
      render(data, data.targetUrl || data.url || url);
      statusEl.textContent = 'Done in ' + ((Date.now() - t0) / 1000).toFixed(1) +
        ' seconds. Results are from Cloudflare.';
    } catch (err) {
      const name = err && err.name;
      let msg;
      if (name === 'TimeoutError' || name === 'AbortError') {
        msg = 'The Cloudflare scanner did not answer in time. Try again in a moment.';
      } else if (err && /^upstream /.test(err.message)) {
        msg = 'The Cloudflare scanner returned an error. This is on their side, not yours.';
      } else {
        msg = 'Could not reach the Cloudflare scanner. Check your connection and try again.';
      }
      statusEl.textContent = msg;
      showToast(msg, 'error');
    } finally {
      clearInterval(tick);
      results.setAttribute('aria-busy', 'false');
      if (btn) { btn.disabled = false; btn.innerHTML = original; }
    }
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
  
  // Defer scrollHeight read to avoid forced reflow at init
  let maxScroll = 1;
  const updateMax = () => { maxScroll = document.body.scrollHeight - window.innerHeight || 1; };
  requestAnimationFrame(updateMax);
  window.addEventListener('resize', updateMax, { passive: true });

  let currentScroll = window.scrollY;
  let ticking = false;

  const update = () => {
    const progress = maxScroll > 0 ? (currentScroll / maxScroll) : 0;
    bar.style.transform = `scaleX(${progress})`;
    ticking = false;
  };

  window.addEventListener('scroll', () => {
    currentScroll = window.scrollY;
    if (!ticking) {
      window.requestAnimationFrame(update);
      ticking = true;
    }
  }, { passive: true });
  
  update();
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

    card.addEventListener('mousemove', e => {
      if (!isHovering || !r) return;
      
      // We don't recalculate getBoundingClientRect on mousemove
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
  window.addEventListener('scroll', () => {
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    if (docHeight <= 0) return;
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
  }, { passive: true });
}

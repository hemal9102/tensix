/* ============================================
   TENSIX — Agent Readiness Diagnostic Controller
   Specifically for /is-my-site-ai-ready
   ============================================ */

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

  function timeoutSignal(ms) {
    if (AbortSignal.timeout) return AbortSignal.timeout(ms);
    const c = new AbortController();
    setTimeout(() => c.abort(new DOMException('Timeout', 'TimeoutError')), ms);
    return c.signal;
  }

  function normalise(raw) {
    const v = (raw || '').trim().replace(/\s+/g, '');
    if (!v) return '';
    let u;
    try { u = new URL(/^https?:\/\//i.test(v) ? v : 'https://' + v); } catch (e) { return null; }
    if (u.protocol !== 'http:' && u.protocol !== 'https:') return null;
    const host = u.hostname;
    if (!/^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)*\.[a-z]{2,}$/i.test(host)) return null;
    return u.href;
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

    const line = (st === 'fail' && meta.cost) ? meta.cost : c.message;
    if (line) row.appendChild(el('p', 'audit-cost', line));

    const fix = fixes.get(c.name);
    if (fix && (fix.description || (fix.specUrls && fix.specUrls.length))) {
      const p = el('p', 'audit-from');
      p.appendChild(el('b', null, 'Specification Fix: '));
      if (fix.description) p.appendChild(document.createTextNode(fix.description));
      (fix.specUrls || []).slice(0, 2).forEach(u => {
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
    const triggerToast = window.showToast || console.log;
    if (url === '') {
      triggerToast('Enter your website address, like example.com', 'error');
      if (input) input.focus();
      return;
    }
    if (url === null) {
      triggerToast('That does not look like a website address. Try something like example.com', 'error');
      if (input) input.focus();
      return;
    }

    const original = btn ? btn.innerHTML : '';
    if (btn) { btn.disabled = true; btn.textContent = 'Scanning…'; }
    results.setAttribute('aria-busy', 'true');

    statusEl.textContent = '';
    statusEl.appendChild(document.createTextNode('Scanning. '));
    const ticker = el('span', null, '0.0s');
    ticker.setAttribute('aria-hidden', 'true');
    statusEl.appendChild(ticker);
    statusEl.appendChild(document.createTextNode(
      ' elapsed. Executing 22 protocol checks across Level 0 to Level 5. ' +
      'Typically completes in 10 to 15 seconds.'));

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
      statusEl.textContent = 'Diagnostic complete in ' + ((Date.now() - t0) / 1000).toFixed(1) +
        ' seconds. 22 protocol specifications evaluated.';
    } catch (err) {
      const name = err && err.name;
      let msg;
      if (name === 'TimeoutError' || name === 'AbortError') {
        msg = 'The diagnostic edge probe timed out. Please retry in a moment.';
      } else if (err && /^upstream /.test(err.message)) {
        msg = 'Diagnostic upstream returned an error. Please retry shortly.';
      } else {
        msg = 'Could not establish connection to diagnostic edge. Check your network connection.';
      }
      statusEl.textContent = msg;
      triggerToast(msg, 'error');
    } finally {
      clearInterval(tick);
      results.setAttribute('aria-busy', 'false');
      if (btn) { btn.disabled = false; btn.innerHTML = original; }
    }
  });
}

document.addEventListener('DOMContentLoaded', initAgentAudit);

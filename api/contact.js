let Pool;
try {
  Pool = require('pg').Pool;
} catch (_) {
  // pg module optional in local static environments
}

let pool;

function getPool() {
  if (!pool && Pool && process.env.DATABASE_URL) {
    const isLocal = /localhost|127\.0\.0\.1/.test(process.env.DATABASE_URL);
    pool = new Pool({
      connectionString: process.env.DATABASE_URL,
      ssl: isLocal
        ? false
        : {
            rejectUnauthorized: process.env.DATABASE_SSL_REJECT_UNAUTHORIZED === 'false' ? false : true
          },
      connectionTimeoutMillis: 5000,
      idleTimeoutMillis: 10000
    });
  }
  return pool;
}

// Input hygiene: strip control characters, null bytes and enforce bounds without corrupting data
function sanitizeInput(str, maxLength = 1000) {
  if (typeof str !== 'string') return '';
  return str
    .slice(0, maxLength)
    .replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, '')
    .trim();
}

const ALLOWED_ORIGINS = [
  'https://tensix.in',
  'https://www.tensix.in',
  'https://tensix.vercel.app',
  'http://localhost:3000',
  'http://localhost:5000',
  'http://localhost:5500',
  'http://127.0.0.1:5500'
];

// In-memory rate limiting per container instance (OWASP API4:2023 Unrestricted Resource Consumption)
const rateLimitMap = new Map();
const RATE_LIMIT_WINDOW_MS = 10 * 60 * 1000; // 10 minutes
const MAX_REQUESTS_PER_WINDOW = 5;

function isRateLimited(ip) {
  if (!ip) return false;
  const now = Date.now();
  const record = rateLimitMap.get(ip) || { count: 0, resetAt: now + RATE_LIMIT_WINDOW_MS };
  if (now > record.resetAt) {
    record.count = 1;
    record.resetAt = now + RATE_LIMIT_WINDOW_MS;
    rateLimitMap.set(ip, record);
    return false;
  }
  record.count += 1;
  rateLimitMap.set(ip, record);
  return record.count > MAX_REQUESTS_PER_WINDOW;
}

module.exports = async function handler(req, res) {
  const origin = req.headers.origin;
  if (origin && ALLOWED_ORIGINS.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
  } else {
    res.setHeader('Access-Control-Allow-Origin', 'https://tensix.in');
  }

  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, error: 'Method not allowed' });
  }

  // OWASP A01: Broken Access Control & Anti-CSRF Guard
  const secFetchSite = req.headers['sec-fetch-site'];
  if (secFetchSite && secFetchSite === 'cross-site') {
    return res.status(403).json({ success: false, error: 'Cross-site form submission forbidden.' });
  }

  // Rate Limiting Guard
  const clientIp = (req.headers['x-forwarded-for'] || '').split(',')[0].trim() ||
                   req.headers['cf-connecting-ip'] ||
                   req.socket?.remoteAddress;
  if (isRateLimited(clientIp)) {
    return res.status(429).json({
      success: false,
      error: 'Too many requests. Please wait a few minutes or reach out via WhatsApp/email directly.'
    });
  }

  try {
    let body = req.body || {};
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch (_) { body = Object.fromEntries(new URLSearchParams(body)); }
    }
    const { name, email, subject, project_type, message, plan, _honey, botcheck, website } = body;

    const wantsHtml = /text\/html/.test(req.headers.accept || '') && !/application\/json/.test(req.headers.accept || '');
    const reply = (status, payload) => (wantsHtml && status === 200)
      ? res.writeHead(303, { Location: '/contact?sent=1' }).end()
      : res.status(status).json(payload);

    // 1. Honeypot Anti-Spam Check (Silently drop bots with 200 OK)
    if (_honey || botcheck || website) {
      console.warn('[TENSIX Bot Shield] Dropped spam submission from bot.');
      return reply(200, {
        success: true,
        message: 'Consultation request received successfully.'
      });
    }

    // 2. Validate required fields
    if (!name || !email || !message) {
      return res.status(400).json({
        success: false,
        error: 'Missing required fields: name, email, and message are required.'
      });
    }

    // 3. Strict Email Validation
    const cleanEmail = String(email).trim().toLowerCase();
    const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;
    if (!emailRegex.test(cleanEmail) || cleanEmail.length > 120) {
      return res.status(400).json({
        success: false,
        error: 'Invalid email address format or length exceeded.'
      });
    }

    // 4. Sanitize and enforce length limits
    const cleanName = sanitizeInput(name, 100);
    const cleanPlan = String(plan || '').toLowerCase().replace(/[^a-z0-9-]/g, '').slice(0, 40);
    const cleanSubject = (cleanPlan ? `[Plan: ${cleanPlan}] ` : '') + sanitizeInput(subject || 'General Architecture Consultation', 150);
    const cleanProjectType = sanitizeInput(project_type || 'Other', 100);
    const cleanMessage = sanitizeInput(message, 5000);

    if (cleanName.length === 0 || cleanMessage.length === 0) {
      return res.status(400).json({
        success: false,
        error: 'Invalid input characters detected in name or message.'
      });
    }

    let dbSaved = false;
    let leadId = null;

    // 5. Parameterized SQL Query (Immune to SQL Injection, hot-path DDL removed)
    const dbPool = getPool();
    if (dbPool) {
      try {
        const insertQuery = `
          INSERT INTO leads (name, email, subject, project_type, message)
          VALUES ($1, $2, $3, $4, $5)
          RETURNING id, created_at;
        `;
        const values = [
          cleanName,
          cleanEmail,
          cleanSubject,
          cleanProjectType,
          cleanMessage
        ];

        const result = await dbPool.query(insertQuery, values);
        if (result.rows && result.rows.length > 0) {
          dbSaved = true;
          leadId = result.rows[0].id;
        }
      } catch (dbErr) {
        console.error('[TENSIX DB Error]', dbErr.message);
      }
    } else {
      console.warn('[TENSIX Warning] DATABASE_URL not configured in environment variables.');
    }

    // 6. Forward sanitized lead to FormSubmit notification service
    let emailSent = false;
    try {
      const emailRes = await fetch('https://formsubmit.co/ajax/contact@tensix.in', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          name: cleanName,
          email: cleanEmail,
          subject: cleanSubject,
          project_type: cleanProjectType,
          message: cleanMessage,
          _database_saved: dbSaved ? `Yes (ID: ${leadId})` : 'Pending DATABASE_URL config'
        })
      });
      if (emailRes.ok) {
        emailSent = true;
      }
    } catch (emailErr) {
      console.error('[TENSIX Email Notify Error]', emailErr.message);
    }

    // If both database persistence and email notification fail, alert the client
    if (!dbSaved && !emailSent && process.env.DATABASE_URL) {
      return res.status(502).json({
        success: false,
        error: 'Unable to deliver message at this time. Please contact Hemal directly on WhatsApp or phone.'
      });
    }

    return reply(200, {
      success: true,
      message: 'Consultation request received successfully.',
      database_saved: dbSaved,
      lead_id: leadId
    });

  } catch (err) {
    console.error('[TENSIX Serverless Error]', err);
    return res.status(500).json({
      success: false,
      error: 'Internal server error processing consultation request.'
    });
  }
};

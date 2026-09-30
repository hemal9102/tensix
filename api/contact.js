let Pool;
try {
  Pool = require('pg').Pool;
} catch (_) {
  // pg module optional in local static environments
}

let pool;

function getPool() {
  if (!pool && Pool && process.env.DATABASE_URL) {
    pool = new Pool({
      connectionString: process.env.DATABASE_URL,
      ssl: {
        rejectUnauthorized: false
      },
      connectionTimeoutMillis: 5000,
      idleTimeoutMillis: 10000
    });
  }
  return pool;
}

// XSS Sanitizer: Escape HTML characters and strip script patterns
function sanitizeInput(str, maxLength = 1000) {
  if (typeof str !== 'string') return '';
  let sanitized = str.slice(0, maxLength);
  // Strip null bytes
  sanitized = sanitized.replace(/\0/g, '');
  // Escape HTML entities to prevent XSS / email HTML injection
  return sanitized
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;')
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

module.exports = async function handler(req, res) {
  const origin = req.headers.origin;
  if (origin && ALLOWED_ORIGINS.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
  } else if (!origin) {
    // Same-origin browser request
    res.setHeader('Access-Control-Allow-Origin', 'https://tensix.in');
  } else {
    // Restrict foreign origins
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

  try {
    const body = req.body || {};
    const { name, email, subject, project_type, message, _honey, botcheck, website } = body;

    // 1. Honeypot Anti-Spam Check (Silently drop bots with 200 OK)
    if (_honey || botcheck || website) {
      console.warn('[TENSIX Bot Shield] Dropped spam submission from bot.');
      return res.status(200).json({
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

    // 4. Sanitize and enforce length limits (Anti-XSS & Anti-DoS)
    const cleanName = sanitizeInput(name, 100);
    const cleanSubject = sanitizeInput(subject || 'General Architecture Consultation', 150);
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

    // 5. Parameterized SQL Query (100% immune to SQL Injection)
    const dbPool = getPool();
    if (dbPool) {
      try {
        await dbPool.query(`
          CREATE TABLE IF NOT EXISTS leads (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT,
            project_type TEXT,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'new'
          );
        `);

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
      console.warn('[TENSIX Warning] DATABASE_URL not set in environment variables.');
    }

    // 6. Forward sanitized lead to FormSubmit for instant email notification
    try {
      await fetch('https://formsubmit.co/ajax/hemal.shah2004@gmail.com', {
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
    } catch (emailErr) {
      console.error('[TENSIX Email Notify Error]', emailErr.message);
    }

    return res.status(200).json({
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

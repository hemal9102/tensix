const { Pool } = require('pg');

let pool;

function getPool() {
  if (!pool && process.env.DATABASE_URL) {
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

module.exports = async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, error: 'Method not allowed' });
  }

  try {
    const { name, email, subject, project_type, message } = req.body || {};

    // 1. Validate required fields
    if (!name || !email || !message) {
      return res.status(400).json({
        success: false,
        error: 'Missing required fields: name, email, and message are required.'
      });
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.trim())) {
      return res.status(400).json({
        success: false,
        error: 'Invalid email address format.'
      });
    }

    let dbSaved = false;
    let leadId = null;

    // 2. Insert into Supabase PostgreSQL (if DATABASE_URL is configured)
    const dbPool = getPool();
    if (dbPool) {
      try {
        // Auto-create table if not exists
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

        // Insert lead record
        const insertQuery = `
          INSERT INTO leads (name, email, subject, project_type, message)
          VALUES ($1, $2, $3, $4, $5)
          RETURNING id, created_at;
        `;
        const values = [
          name.trim(),
          email.trim(),
          (subject || 'General Architecture Consultation').trim(),
          (project_type || 'Other').trim(),
          message.trim()
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

    // 3. Forward to FormSubmit in background for instant email notification
    try {
      await fetch('https://formsubmit.co/ajax/hemal.shah2004@gmail.com', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          name: name.trim(),
          email: email.trim(),
          subject: (subject || 'General Architecture Consultation').trim(),
          project_type: (project_type || 'Other').trim(),
          message: message.trim(),
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

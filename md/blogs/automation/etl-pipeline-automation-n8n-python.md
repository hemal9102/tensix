---
title: "Automated Data Pipelines with Python & n8n | TENSIX"
url: https://www.tensix.in/blogs/automation/etl-pipeline-automation-n8n-python
description: "How to move data between your apps and databases automatically with Python and n8n, so reports and AI search stay current without manual exports."
---

[← Back to Blog](https://www.tensix.in/blogs)

**Hemal Shah (HK)** AI Automation Engineer & Technical SEO

# Reliable Data Pipelines with Python & n8n: From SQL to AI Search

By **[Hemal Shah](https://www.tensix.in/hemal-shah)** • Published July 26, 2026 • 7 min technical read

**In plain words**

Most businesses keep data in many places: a sales tool, a billing system, spreadsheets, a database. A data pipeline (often called ETL: extract, transform, load) copies that data automatically, cleans it, and puts it where you need it, such as reports or an AI assistant that answers from your own documents. This article shows how I build these pipelines with n8n (a visual automation tool) and Python so they run on a schedule, retry on errors, and alert you when something needs attention. If you want this set up for your business, see [data scraping and automation](https://www.tensix.in/services/data-scraping-automation).

An AI assistant is only as good as the data behind it. If your data is out of date, duplicated, or copied across by hand, its answers will be wrong. ETL automation (extract, transform, load) keeps that data fresh without manual exports and without slowing down your main database.

At TENSIX (formerly [HK Engineering](https://www.tensix.in/hk-engineering-ahmedabad)), I combine **n8n** for visual workflows with small **Python services** for the heavy processing. Below is the setup I use to keep a normal SQL database in sync with a vector search engine (the index an AI uses to find relevant text).

#### Need Your Data Workflows Automated?

If you want data moved between apps, APIs connected, or reports updated without manual work, read about [HK Engineering (now TENSIX)](https://www.tensix.in/hk-engineering-ahmedabad) or talk to [Hemal Shah](https://www.tensix.in/hemal-shah) directly.

## 1. The Setup: n8n for Workflows, Python for Heavy Lifting

Teams usually make one of two mistakes. They write one big Python script that runs on a timer, with no easy way to see when it fails. Or they push heavy data processing into a drag-and-drop tool, which can crash on large files.

I split the work into three layers instead:

1. **Orchestration Tier (n8n):** Handles webhook ingestion, cron scheduling, OAuth token refresh loops, rate-limiting backoffs, and error notification routing (Slack / Email alerts).
2. **Processing Tier (Python / FastAPI):** Executes CPU-intensive data normalization, markdown chunking, deduplication hashing, and batch OpenAI embedding generation.
3. **Storage Tier (PostgreSQL + pgvector):** Serves as the transactional source of truth and vector index, utilizing row-level locks and transactional upserts (`ON CONFLICT DO UPDATE`).

## 2. Copy Only What Changed, Without Slowing Your Database

To avoid slowing down the live database, the pipeline only picks up rows that changed since the last run (using timestamps). It also stores a fingerprint (a hash) of each piece of text, so text that has not changed is not processed again.

```
import hashlib
from typing import Dict, Any, List
import psycopg2
from psycopg2.extras import execute_values

def calculate_chunk_hash(text: str, metadata: Dict[str, Any]) -> str:
    """Generate SHA-256 hash of text content and key metadata fields to detect drift."""
    raw_payload = f"{text.strip()}::{metadata.get('updated_at', '')}"
    return hashlib.sha256(raw_payload.encode('utf-8')).hexdigest()

def upsert_vector_batch(conn, chunks: List[Dict[str, Any]]) -> int:
    """Execute high-speed transactional batch upsert into PostgreSQL pgvector table."""
    upsert_sql = """
        INSERT INTO enterprise_vectors (doc_id, chunk_index, content, content_hash, embedding, updated_at)
        VALUES %s
        ON CONFLICT (doc_id, chunk_index) DO UPDATE SET
            content = EXCLUDED.content,
            content_hash = EXCLUDED.content_hash,
            embedding = EXCLUDED.embedding,
            updated_at = NOW()
        WHERE enterprise_vectors.content_hash != EXCLUDED.content_hash;
    """

    # Prepare tuple values for execute_values
    records = [
        (c['doc_id'], c['chunk_index'], c['content'], c['hash'], c['embedding'], c['updated_at'])
        for c in chunks
    ]

    with conn.cursor() as cur:
        execute_values(cur, upsert_sql, records, page_size=500)
        conn.commit()
        return cur.rowcount
```

## 3. When Another App Fails: Retries and a Failure Log

Outside services such as Salesforce, HubSpot, or Stripe sometimes time out or refuse requests for a while (HTTP 429, "too many requests"). In n8n, I retry these calls with growing waits between attempts (exponential backoff), and keep a **Dead Letter Queue** (a failure log table) in PostgreSQL.

If a record still fails after 3 retries, the raw data and the error are saved to the `etl_dead_letter_queue` table and an alert goes out by Slack or email. The rest of the pipeline keeps running, and the failed record can be checked and replayed later.

## 4. What This Means for Your Business

Moving from manual exports to automated pipelines that retry on their own means less time spent fixing data by hand. Your reports and your internal AI search (RAG, an assistant that answers from your own documents) always work from current data.

To discuss custom software or automation for your company, visit the [HK Engineering Ahmedabad page](https://www.tensix.in/hk-engineering-ahmedabad) or read [Hemal Shah's profile](https://www.tensix.in/hemal-shah).

## Want Something Like This for Your Business?

TENSIX is a one-person studio run by Hemal Shah, who uses AI tools to work faster. Tell me what you need and I will reply with a clear plan and price.

[Tell Me About Your Project →](https://www.tensix.in/contact)

[← Previous post](https://www.tensix.in/blogs/n8n-vs-python-scripts-when-to-use-which) No newer posts

---
title: "Guide: AI Document Search with FastAPI & pgvector | TENSIX"
url: https://www.tensix.in/blogs/case-studies/enterprise-rag-pgvector-fastapi-case-study
description: "How to build an AI assistant that answers from your company documents (RAG) on PostgreSQL and FastAPI, with fewer moving parts and faster replies."
---

[← Back to Blog](https://www.tensix.in/blogs)

**Hemal Shah (HK)** AI Automation Engineer & Technical SEO

# Guide: Fast AI Document Search with FastAPI & pgvector

By **[Hemal Shah](https://www.tensix.in/hemal-shah)** • Published July 26, 2026 • 8 min technical read

**In plain words**

RAG is an AI assistant that answers questions from your own documents, such as policies, contracts, or reports, instead of guessing. Many teams buy a separate "vector database" for this, which adds cost and makes answers slower. This article shows how to keep everything inside PostgreSQL, the database many companies already use, and serve answers quickly with FastAPI. If you want an assistant like this for your business, see [AI agent development](https://www.tensix.in/services/ai-agent-development).

When companies grow their AI projects, the usual problem is not how smart the model is. It is how slowly the system finds the right documents, and being locked into a separate paid database. Dedicated vector databases add another service to run, extra network delay, and a monthly bill, even for teams that already run PostgreSQL.

This write-up walks through the architecture [HK Engineering](https://www.tensix.in/hk-engineering-ahmedabad) (now TENSIX) uses for RAG (retrieval-augmented generation: an AI assistant that answers from your own documents), built with **FastAPI**, **PostgreSQL with `pgvector`**, and **LangChain**. It is based on a document-heavy financial services workload of the kind common in Ahmedabad.

## Want an AI Assistant That Knows Your Documents?

I design and build RAG systems for companies in Ahmedabad and beyond. Read about [HK Engineering (now TENSIX)](https://www.tensix.in/hk-engineering-ahmedabad) or talk to [Hemal Shah](https://www.tensix.in/hemal-shah) directly.

## 1. The Problem: Why a Simple RAG Setup Slows Down

A typical starting point is a synchronous Python script (one that handles one request at a time) talking to an external vector database service. When many analysts search documents at the same time, three problems appear:

- **Waiting on the AI model:** A server that handles one request at a time waits on the AI model, so busy periods end in time-out errors.
- **Index Inefficiency:** Without an index, every search compares the question against every document chunk (exact k-NN), so searches get slower as the library grows.
- **Network Hop Latency:** Sending data back and forth between the app server, the main database, and an outside vector service adds delay to every single query.

## 2. The Fix: Keep Search Inside PostgreSQL and Answer Without Blocking

The fix is to keep the normal business data and the vector embeddings (number lists that capture the meaning of text) in one PostgreSQL 16 database, using the open-source `pgvector` extension.

### HNSW Indexing (Fast Approximate Search)

Instead of comparing against every chunk (exact k-NN) or using an `IVFFlat` index, which needs a training step, I build an HNSW index on the 1536-dimension embedding column. HNSW needs no training step and stays fast even while new documents are being added.

```
-- Enable pgvector extension and create enterprise document embeddings table
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE enterprise_chunks (
    chunk_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id VARCHAR(128) NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    embedding vector(1536) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Build high-performance HNSW index for cosine distance retrieval
CREATE INDEX ON enterprise_chunks
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

### Asynchronous Retrieval Pipeline in FastAPI

So that no request waits behind another, the search endpoint is async. It uses `asyncpg` to talk to the database without blocking and server-sent events (SSE) to stream the AI's answer to the user as it is written.

```
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import asyncpg
from typing import List

app = FastAPI(title="HK Engineering RAG Service")

class QueryRequest(BaseModel):
    query_text: str
    top_k: int = 5
    similarity_threshold: float = 0.78

@app.post("/api/v1/retrieve")
async def retrieve_relevant_chunks(request: QueryRequest, db: asyncpg.Connection = Depends(get_db_pool)):
    # 1. Generate query embedding non-blocking
    query_vector = await generate_embedding_async(request.query_text)

    # 2. Execute HNSW vector similarity search in PostgreSQL
    sql_query = """
        SELECT chunk_id, content, metadata,
               1 - (embedding <=> $1) AS cosine_similarity
        FROM enterprise_chunks
        WHERE 1 - (embedding <=> $1) > $2
        ORDER BY embedding <=> $1
        LIMIT $3;
    """
    rows = await db.fetch(sql_query, str(query_vector), request.similarity_threshold, request.top_k)

    return {"results": [dict(row) for row in rows]}
```

## 3. What Changes: Old Setup vs New Setup

Speed and cost depend on your documents, traffic, and hosting, so rather than quote one project's numbers, here is what changes in practice. Before handover, I load-test each build with Locust (a tool that simulates many users at once) so you see real figures for your own data.

| Area | Separate Vector DB + Flask | pgvector + FastAPI |
| --- | --- | --- |
| Many users at once | Requests queue behind each other; timeouts under load | Waiting requests do not block others; answers stream as they are written |
| Growing document library | Exact search slows as documents grow | HNSW index stays fast as data grows |
| Running cost | App server, main database, plus a paid vector service | One PostgreSQL database holds data and search index |
| Backups and permissions | Two systems to back up and keep in sync | One backup; results filtered by user permissions in the same query |

## 4. Key Takeaways for Business and Tech Leaders

For important business systems, do not add a separate vector database just because it is popular. Keeping embeddings inside PostgreSQL gives you reliable transactions (ACID), one simple backup, and fast filtering of search results by who is allowed to see what.

To discuss a similar AI search or automation system for your company, in Ahmedabad or elsewhere, visit the [HK Engineering Ahmedabad page](https://www.tensix.in/hk-engineering-ahmedabad) or send a message through the [contact page](https://www.tensix.in/contact).

## Want Something Like This for Your Business?

TENSIX is a one-person studio run by Hemal Shah, who uses AI tools to work faster. Tell me what you need and I will reply with a clear plan and price.

[Tell Me About Your Project →](https://www.tensix.in/contact)

[← Previous post](https://www.tensix.in/blogs/n8n-vs-python-scripts-when-to-use-which) No newer posts

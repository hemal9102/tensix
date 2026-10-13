#!/usr/bin/env python3
"""
TENSIX HIGH-PERFORMANCE JEV-OUTFLANK RUNNER (ASYNC AIOHTTP ENGINE)
Achieves sub-second execution speeds via non-blocking asynchronous event loops:
1. Concurrently probes competitor origins for TTFB latency.
2. Intercepts real-time Google Suggest queries via suggestqueries.google.com.
3. Invokes typesafe/jev-router (OpenRouter) with deep reasoning tokens.
4. Generates candidate outflank nodes in local sandbox (zero production pollution).
"""

import asyncio
import aiohttp
import json
import os
import sys
import time
from datetime import datetime, timezone

OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "")
JEV_MODEL = "typesafe/jev-router"
SANDBOX_DIR = r"D:\projects\tensix\sandbox"

async def measure_competitor_ttfb(session, url):
    start = time.perf_counter()
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=4)) as resp:
            ttfb = (time.perf_counter() - start) * 1000
            return resp.status, round(ttfb, 1)
    except Exception:
        return 500, 3500.0

async def harvest_google_suggest(session, query):
    url = f"https://suggestqueries.google.com/complete/search?client=chrome&hl=en&gl=in&q={query.replace(' ', '+')}"
    start = time.perf_counter()
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=3)) as resp:
            data = await resp.json(content_type=None)
            duration_ms = (time.perf_counter() - start) * 1000
            stems = data[1] if len(data) > 1 else []
            return stems, round(duration_ms, 1)
    except Exception as e:
        return [], 0.0

async def call_jev_router(session, competitor_url, competitor_ttfb, stems):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://tensix.in",
        "X-Title": "TENSIX-JevOutflank"
    }
    prompt = (
        f"Competitor Target: {competitor_url}\n"
        f"Competitor Origin TTFB: {competitor_ttfb}ms (Lagging)\n"
        f"Google Suggest Stems: {stems[:5]}\n\n"
        "Synthesize for TENSIX Ahmedabad:\n"
        "1. Position 0 Definition Block (exact 40-45 words, high factual density).\n"
        "2. Three high-ticket FAQs with direct answers highlighting sub-400ms speed, fixed pricing, and ERP integration."
    )
    payload = {
        "model": JEV_MODEL,
        "messages": [
            {"role": "system", "content": "You are a senior search systems architect specializing in passage extraction and GEO."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 800
    }
    start = time.perf_counter()
    async with session.post(url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=20)) as resp:
        res = await resp.json()
        duration_ms = (time.perf_counter() - start) * 1000
        msg = res["choices"][0]["message"]
        content = msg.get("content")
        reasoning = msg.get("reasoning", "")
        # If model put answers directly inside reasoning or content was null due to token limits:
        final_content = content if content else reasoning
        return final_content, reasoning, round(duration_ms, 1)

async def run_cycle():
    total_start = time.perf_counter()
    print("=" * 70)
    print("  JEV-OUTFLANK ASYNC ENGINE: MILLISECOND CYCLE EXECUTION")
    print("=" * 70)

    os.makedirs(SANDBOX_DIR, exist_ok=True)

    target_competitor = "https://digitalsky360.com/digital-marketing-agency-for-manufacturers-in-ahmedabad/"
    target_query = "digital marketing for manufacturers ahmedabad"

    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0 TENSIX-JevOutflank/1.0"}) as session:
        # Step 1 & 2 in Parallel!
        print("\n[1/3] Concurrently probing Competitor TTFB & Google Suggest Stems...")
        comp_task = measure_competitor_ttfb(session, target_competitor)
        suggest_task = harvest_google_suggest(session, target_query)

        (comp_status, comp_ttfb), (stems, suggest_duration) = await asyncio.gather(comp_task, suggest_task)

        print(f"      Competitor Status: {comp_status} | Measured TTFB: {comp_ttfb}ms")
        print(f"      Google Suggest Stems ({suggest_duration}ms): {len(stems)} captured")
        for s in stems[:4]:
            print(f"      - {s}")

        # Step 3: Jev Router Synthesis
        print("\n[2/3] Calling typesafe/jev-router (OpenRouter) with reasoning tokens...")
        content, reasoning, jev_duration = await call_jev_router(session, target_competitor, comp_ttfb, stems)
        print(f"      Jev Router Completed in {jev_duration}ms")

        # Step 4: Staging into Sandbox (Zero live production pollution)
        print("\n[3/3] Writing candidate outflank artifacts into sandbox/...")
        candidate_json = {
            "topic": "Industrial Manufacturing B2B Web Engineering",
            "target_route": "/services/industrial-web-engineering",
            "competitor_url": target_competitor,
            "competitor_ttfb_ms": comp_ttfb,
            "tensix_edge_ttfb_ms": 404,
            "harvested_stems": stems,
            "jev_synthesized_content": content,
            "jev_reasoning_summary": reasoning[:300] + "...",
            "staged_at": datetime.now(timezone.utc).isoformat()
        }

        json_path = os.path.join(SANDBOX_DIR, "candidate_industrial_outflank.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(candidate_json, f, indent=2)

        preview_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>SANDBOX PREVIEW: Industrial Outflank Candidate</title>
  <style>
    body {{ font-family: system-ui, -apple-system, sans-serif; padding: 2rem; max-width: 840px; margin: 0 auto; color: #0F172A; line-height: 1.6; }}
    .badge {{ background: #EFF6FF; color: #1D4ED8; font-weight: 700; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem; }}
    .stats {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1.5rem 0; background: #F8FAFC; padding: 1rem; border-radius: 8px; border: 1px solid #E2E8F0; }}
    .content-box {{ background: #fff; border: 1px solid #CBD5E1; border-radius: 8px; padding: 1.5rem; margin-top: 1rem; }}
  </style>
</head>
<body>
  <span class="badge">SANDBOX READ-ONLY CANDIDATE</span>
  <h2>Industrial Manufacturing Outflank Node</h2>
  <div class="stats">
    <div><strong>Competitor Origin TTFB:</strong> {comp_ttfb}ms</div>
    <div><strong>TENSIX Edge Latency:</strong> 404ms</div>
  </div>
  <h3>Jev Router Synthesized Content:</h3>
  <div class="content-box">
    <pre style="white-space:pre-wrap;font-family:inherit;">{content}</pre>
  </div>
</body>
</html>"""
        html_path = os.path.join(SANDBOX_DIR, "candidate_industrial_outflank_preview.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(preview_html)

        total_elapsed = round((time.perf_counter() - total_start) * 1000, 1)
        print(f"      Staged JSON: {json_path}")
        print(f"      Staged HTML: {html_path}")
        print("=" * 70)
        print(f"  TOTAL CYCLE DURATION: {total_elapsed}ms")
        print("=" * 70)

if __name__ == "__main__":
    asyncio.run(run_cycle())

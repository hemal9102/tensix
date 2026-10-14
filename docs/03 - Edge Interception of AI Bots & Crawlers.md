# 03 - Edge Interception of AI Bots & Crawlers

> **Document ID:** `CRAWLER-03`  
> **Tags:** `#bot-detection` `#waf` `#edge-networking` `#cloudflare` `#anti-bot`

---

## 🎯 Executive Summary

When AI platforms (OpenAI, Perplexity, Anthropic, Google) perform real-time retrieval for user prompts, they generate **distinctive network signatures at the web server and reverse-proxy edge**.

By intercepting and logging these bots at the socket / Nginx / Cloudflare layer, systems engineers can observe:
1. **What topics and entities AI engines are actively researching in real time.**
2. **Which pages are being scraped for model training vs. real-time RAG inference.**

---

## 🤖 Major AI Bots & User-Agent Taxonomy

| Bot Name | Operator | Primary Purpose | Verified ASN / Network Range |
| :--- | :--- | :--- | :--- |
| **`GPTBot`** | OpenAI | Foundation Model Training Crawl | Autonomous System IPs published by OpenAI |
| **`ChatGPT-User`** | OpenAI | Real-Time User Browsing / Search RAG | Dispatched live when a user prompts ChatGPT |
| **`PerplexityBot`** | Perplexity AI | Real-Time RAG Search Engine | Amazon AWS / Datacenter ranges |
| **`ClaudeBot`** | Anthropic | Training & Model Ingestion | Anthropic published IP ranges |
| **`Google-Extended`** | Google | Gemini / Vertex AI Training | Google Cloud AS15169 |

---

## 🛡️ Edge Detection & Logging Configuration

### 1. Nginx Reverse Proxy Interception Rule
```nginx
# Map incoming AI User-Agents to dedicated logging channel
map $http_user_agent $ai_bot_type {
    default                     "HUMAN";
    "~*ChatGPT-User"            "OPENAI_LIVE_RAG";
    "~*GPTBot"                  "OPENAI_TRAINING";
    "~*PerplexityBot"           "PERPLEXITY_LIVE_RAG";
    "~*ClaudeBot"               "ANTHROPIC_BOT";
    "~*Google-Extended"         "GOOGLE_GEMINI_INGEST";
}

# Custom JSON access log tailored for AI query mining
log_format ai_intel '{"time":"$time_iso8601","bot":"$ai_bot_type","ip":"$remote_addr","path":"$request_uri","status":$status,"bytes":$body_bytes_sent,"referer":"$http_referer"}';

server {
    access_log /var/log/nginx/ai_traffic.log ai_intel if=$ai_bot_type;
}
```

---

## 🔒 Cloudflare WAF Differentiation: Verified Bots vs Impersonators

Just like Googlebot, AI bots declare their identity in HTTP headers. However, malicious scrapers frequently fake the `User-Agent: ChatGPT-User` header to bypass rate limits.

### How to Verify Real AI Bots:
1. **Reverse DNS Check (FCrDNS):** Look up the incoming IP address via PTR record. For legitimate OpenAI or Google bots, the hostname must resolve back to `.openai.com` or `.google.com`.
2. **ASN Matching:** Compare the incoming connection's Autonomous System Number against the official published IP blocks.

---
**Backlinks:**
* [[06-AI-Search-and-Crawler-Engine/00 - Index|Domain Index]]
* [[06-AI-Search-and-Crawler-Engine/01 - Google Autocomplete & Real-Time Intent Harvesting Engine|01 - Intent Harvesting]]

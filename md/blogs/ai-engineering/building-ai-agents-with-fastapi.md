---
title: "Building AI Agents with FastAPI: A Practical Guide | TENSIX"
url: https://www.tensix.in/blogs/ai-engineering/building-ai-agents-with-fastapi
description: "How to build an AI agent (software that answers and acts for you) with FastAPI and Python: how it fits together, the code, security, and deployment tips."
---

[← Back to Blog](https://www.tensix.in/blogs)

**Hemal Shah (HK)** AI Automation Engineer & Technical SEO

# Building AI Agents with FastAPI: A Production Guide

Published on June 9, 2026 · 8 min read

**In plain words**

An AI agent is software that reads a request, decides what to do, and then does it: answering a customer, looking up an order, or updating a sheet. This guide shows how I build agents on FastAPI (a fast Python web framework) so many people can use them at once without slowing down. The short version for non-technical readers: the right foundation makes an AI assistant reliable, safe, and affordable to run. If you want one built for your business, see [AI agent development](https://www.tensix.in/services/ai-agent-development).

**Hemal Shah (HK)** AI Automation Engineer & Technical SEO • Published June 29, 2026

## 1. The Problem: Simple Scripts Break When Real Users Arrive

Many people build their first AI agent as a simple Python script or notebook. That works for one user. When real customers arrive, it starts to struggle: each request waits for the AI to reply and blocks everyone else, conversation history gets lost, and connecting to tools like Slack or n8n is awkward. Older frameworks like Flask or Django can be heavy for this job or lack built-in async support (the ability to handle many waiting requests at once).

## 2. Why FastAPI Helps

**FastAPI** fixes these problems at the foundation. It is async by default, so while it waits for an OpenAI or Anthropic reply, it keeps serving other users. It also writes its own API documentation (OpenAPI/Swagger) automatically, which makes it easy to describe the "tools" an AI model is allowed to call.

## 3. How the Pieces Fit Together

graph TD Client[Client / Frontend] -->|HTTP POST| FastAPI[FastAPI Server] FastAPI -->|Async Request| LLM[LLM Engine e.g. GPT-4 / Claude] FastAPI -->|Store Context| Redis[(Redis Memory)] LLM -.->|Tool Call| FastAPI FastAPI -->|Execute Function| Tools[External Tools / DB] Tools -.->|Result| FastAPI FastAPI -.->|Final Answer| Client

## 4. What Happens When Someone Sends a Message

Step by step, from the user's message to the final answer:

sequenceDiagram participant User participant FastAPI participant Memory participant LLM User->>FastAPI: POST /chat {message} FastAPI->>Memory: Fetch History FastAPI->>LLM: Send Message + History + Tools LLM-->>FastAPI: ToolCall: fetch_data() FastAPI->>FastAPI: Execute fetch_data() FastAPI->>LLM: Return Tool Result LLM-->>FastAPI: Final Text Response FastAPI->>Memory: Save Interaction FastAPI-->>User: JSON Response

## 5. How the Code Is Organised

```
ai_agent_project/
├── main.py              # FastAPI entry point
├── config.py            # Environment variables
├── agent/
│   ├── core.py          # LLM connection & logic
│   ├── memory.py        # Redis context manager
│   └── tools.py         # Functions LLM can call
├── models/
│   └── schemas.py       # Pydantic data models
└── requirements.txt
```

## 6. The Code: A Minimal Agent Endpoint

Here is a small async AI agent endpoint in FastAPI. Pydantic checks that every request has the right fields before it reaches the AI.

### API Design (main.py)

```
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from agent.core import generate_agent_response

app = FastAPI(title="HK Engineering AI Agent API")

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    tokens_used: int

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Async call to LLM prevents server blocking
    response, tokens = await generate_agent_response(request.user_id, request.message)
    return ChatResponse(reply=response, tokens_used=tokens)

```

## 7. FastAPI vs Flask vs Django

| Framework | Async Support | Type Safety | LLM Tool Integration |
| --- | --- | --- | --- |
| FastAPI | Native (async/await) | Excellent (Pydantic) | Native via OpenAPI |
| Flask | Requires extensions | Manual validation | Requires custom wrappers |
| Django | Partial (ASGI) | Heavy (Django Forms) | Complex overhead |

## 8. Keeping It Safe

- **API Key Rotation:** Never write AI provider keys into the code. Keep them in AWS Secrets Manager or a .env file, and change them regularly.
- **Rate Limiting:** Every AI call costs money, so limit how often one user can call it. `slowapi` does this for FastAPI.
- **Prompt Injection:** Users may try to trick the AI with hidden instructions. Clean user input and keep your own instructions clearly separated from it.

## 9. Connecting the Agent to Your Other Tools

Once the agent sits behind a secure API, your other tools can use it too. For example, an n8n workflow (a visual automation tool) can call it to draft content or answer common customer questions, with a person reviewing the result before it goes live.

## 10. Common Questions

### Why is FastAPI preferred over Flask for AI?

Because an AI reply can take 1 to 10 seconds. In Flask, each waiting call ties up a worker. FastAPI runs on ASGI (an async server standard), so it keeps serving other users while it waits for the AI to answer.

### Can I run local LLMs (like Ollama) with this architecture?

Yes. Instead of pointing the async client to OpenAI, you change the base URL to `http://localhost:11434/v1`, where Ollama is running. Your data then stays on your own machine.

## Want Something Like This for Your Business?

TENSIX is a one-person studio run by Hemal Shah, who uses AI tools to work faster. Tell me what you need and I will reply with a clear plan and price.

[Tell Me About Your Project →](https://www.tensix.in/contact)

[← Previous post](https://www.tensix.in/blogs/n8n-vs-python-scripts-when-to-use-which) No newer posts

"""Step 2: Semantic scoring with TypeSafe Jev via OpenRouter"""
import json, os, urllib.request, urllib.error, time
from pathlib import Path

# Load citation_audit output (Step 1 dependency)
audit_md = Path("../citation_audit.md")
if not audit_md.exists():
    print("ERROR: Run citation_audit.py first"); exit(1)

lines = audit_md.read_text(encoding="utf-8").split("\n")
pages = {}
for line in lines:
    if line.startswith("|") and "FIX" in line or "OK" in line:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 8:
            status = "citation-ready" if "OK" in parts[1] else "needs-work"
            url = parts[2]
            query = parts[3]
            intent = parts[4]
            answers_first = float(parts[5]) if parts[5] else 0
            entity_clear = float(parts[6]) if parts[6] else 0
            specificity = float(parts[7]) if parts[7] else 0
            issues = parts[8] if len(parts) > 8 else ""
            pages[url] = {
                "status": status,
                "query": query,
                "intent": intent,
                "answers_first": answers_first,
                "entity_clear": entity_clear,
                "specificity": specificity,
                "citation_issues": issues
            }

print("=== STEP 2: SEMANTIC SCORING ===\n")

# Use Jev to score pages for: citation readiness, local ranking boost, superlative risk
KEY = os.environ.get("OPENROUTER_API_KEY")
if not KEY:
    print("ERROR: Set OPENROUTER_API_KEY"); exit(1)

scored = []
for url in sorted(pages.keys())[:5]:  # Top 5 pages for demo (full run: all)
    p = pages[url]
    state = json.dumps(p)

    questions = {
        "citation_ready": {
            "type": "noul",
            "instructions": f"Will this page be cited by AI? Query: '{p['query']}'. Intent: {p['intent']}. answers_first={p['answers_first']:.2f}, entity_clear={p['entity_clear']:.2f}, specificity={p['specificity']:.2f}",
            "criteria": {"true": "AI crawlers will quote this page.", "false": "This page won't be cited."}
        },
        "local_rank_help": {
            "type": "score",
            "instructions": f"Does this page help local ranking? It mentions TENSIX/{p['query']}.",
            "criteria": ["Hurts: inconsistent address or no location.", "Neutral: has address but generic content.", "Helps: cited + clear location + high specificity."]
        }
    }

    body = json.dumps({
        "model": "typesafe/jev-router",
        "messages": [{"role": "user", "content": f"Score this page for citation + local ranking.\nState: {state}\nQuestions: {json.dumps(questions)}"}],
        "response_format": {"type": "json_object"},
        "temperature": 0
    }).encode()

    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", body,
                                 {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=30))
        ans = json.loads(r["choices"][0]["message"]["content"])

        citation_prob = ans.get("citation_ready", 0.5)
        local_score = ans.get("local_rank_help", 1)

        scored.append((url, p, citation_prob, local_score))
        print(f"{'OK' if citation_prob >= 0.7 else 'FIX':<5} {url:<50} citation={citation_prob:.2f} local={local_score:.1f}")
        time.sleep(1)
    except Exception as e:
        print(f"ERROR {url}: {e}")

print("\n=== ROOT PATTERNS ===")
# Group failures by root cause
no_query_answer = [u for u, p, c, l in scored if p['answers_first'] < 0.5]
no_entity = [u for u, p, c, l in scored if p['entity_clear'] < 0.5]
too_generic = [u for u, p, c, l in scored if p['specificity'] < 1.0]

print(f"No direct query answer: {len(no_query_answer)} pages → rewrite opening to answer {set(p['query'] for _, p, _, _ in scored)}")
print(f"Missing who/what/where: {len(no_entity)} pages → add 'TENSIX, Navrangpura, Ahmedabad' in first sentence")
print(f"Too generic claims: {len(too_generic)} pages → replace 'best/elite' with checkable facts")

print("\n=== OUTPUT ===")
print(json.dumps({"scored_pages": len(scored), "citation_ready": sum(1 for _, _, c, _ in scored if c >= 0.7), "patterns": {
    "no_query_answer": len(no_query_answer),
    "no_entity": len(no_entity),
    "too_generic": len(too_generic)
}}, indent=2))

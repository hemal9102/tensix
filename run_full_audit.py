"""
Runs structured-data-validator across all HTML files in hemalshah portfolio.
Extracts every JSON-LD block, parses it, and reports all errors.
"""
import os, json, re

ROOT = r"H:\portfolio_website\hemalshah"
HTML_FILES = []
for dirpath, _, filenames in os.walk(ROOT):
    if "node_modules" in dirpath: continue
    for fn in filenames:
        if fn.endswith(".html"):
            HTML_FILES.append(os.path.join(dirpath, fn))

JSONLD_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE
)

errors = []
warnings = []
ok = []
all_ids = {}   # @id → [files]

for filepath in sorted(HTML_FILES):
    rel = os.path.relpath(filepath, ROOT)
    with open(filepath, encoding="utf-8") as f:
        html = f.read()

    blocks = JSONLD_RE.findall(html)
    if not blocks:
        warnings.append(f"[WARN] {rel}: no JSON-LD found")
        continue

    for idx, raw in enumerate(blocks):
        raw = raw.strip()
        # --- 1. Parse JSON ---
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            errors.append(f"[JSON ERROR] {rel} block#{idx+1}: {e}")
            continue

        graph = data.get("@graph", [data])

        for node in graph:
            ntype = node.get("@type", "UNKNOWN")
            nid   = node.get("@id", "")

            # --- 2. Duplicate @id check ---
            if nid:
                if nid not in all_ids:
                    all_ids[nid] = []
                all_ids[nid].append(rel)

            # --- 3. Missing @context ---
            if "@context" not in data:
                errors.append(f"[SCHEMA] {rel}: missing @context")

            # --- 4. Relative URLs ---
            for key in ["url", "image", "logo", "item"]:
                val = node.get(key, "")
                if isinstance(val, str) and val.startswith("/"):
                    errors.append(f"[URL] {rel}: {ntype}.{key} is relative: {val}")

            # --- 5. FAQPage validation ---
            if ntype == "FAQPage":
                entities = node.get("mainEntity", [])
                if not entities:
                    errors.append(f"[FAQ] {rel}: FAQPage has no mainEntity")
                for i, q in enumerate(entities):
                    if q.get("@type") != "Question":
                        errors.append(f"[FAQ] {rel}: mainEntity[{i}] @type is not Question")
                    ans = q.get("acceptedAnswer", {})
                    if ans.get("@type") != "Answer":
                        errors.append(f"[FAQ] {rel}: mainEntity[{i}].acceptedAnswer @type is not Answer")
                    if not ans.get("text", "").strip():
                        errors.append(f"[FAQ] {rel}: mainEntity[{i}].acceptedAnswer.text is empty")
                    if not q.get("name", "").strip():
                        errors.append(f"[FAQ] {rel}: mainEntity[{i}].name (question) is empty")

            # --- 6. Person required fields ---
            if ntype == "Person":
                for req in ["name", "url"]:
                    if not node.get(req):
                        errors.append(f"[PERSON] {rel}: Person missing required '{req}'")
                if not node.get("sameAs"):
                    warnings.append(f"[PERSON] {rel}: Person has no sameAs (recommended)")

            # --- 7. Organization required fields ---
            if ntype == "Organization":
                for req in ["name", "url"]:
                    if not node.get(req):
                        errors.append(f"[ORG] {rel}: Organization missing '{req}'")

            # --- 8. WebPage / BreadcrumbList ---
            if ntype == "BreadcrumbList":
                items = node.get("itemListElement", [])
                if not items:
                    errors.append(f"[BREADCRUMB] {rel}: BreadcrumbList has no itemListElement")
                for i, item in enumerate(items):
                    if not item.get("item") and not item.get("@id"):
                        warnings.append(f"[BREADCRUMB] {rel}: itemListElement[{i}] has no item URL")
                    pos = item.get("position")
                    if pos is None:
                        errors.append(f"[BREADCRUMB] {rel}: itemListElement[{i}] missing position")

            # --- 9. Service ---
            if ntype == "Service":
                if not node.get("name"):
                    errors.append(f"[SERVICE] {rel}: Service missing 'name'")
                if not node.get("provider"):
                    warnings.append(f"[SERVICE] {rel}: Service missing 'provider'")

            # --- 10. WebSite SearchAction ---
            if ntype == "WebSite":
                pa = node.get("potentialAction", {})
                if pa.get("@type") == "SearchAction":
                    target = pa.get("target", "")
                    if "{search_term_string}" not in str(target):
                        errors.append(f"[SEARCH] {rel}: SearchAction target missing {{search_term_string}}")

            # --- 11. Dates ISO8601 ---
            for datefield in ["datePublished", "dateModified", "dateCreated"]:
                val = node.get(datefield, "")
                if val and not re.match(r"\d{4}-\d{2}-\d{2}", val):
                    errors.append(f"[DATE] {rel}: {ntype}.{datefield} not ISO8601: {val}")

            # --- 12. HTML inside JSON values ---
            raw_node = json.dumps(node)
            if re.search(r"<[a-zA-Z][^>]*>", raw_node):
                errors.append(f"[HTML-IN-JSON] {rel}: {ntype} contains HTML tags inside JSON values")

        ok.append(rel)

# --- Duplicate @id report ---
for nid, files in all_ids.items():
    unique = list(dict.fromkeys(files))
    if len(unique) > 1:
        # same @id on different pages is fine (cross-page entity refs)
        pass  # only flag if same file has it twice
    file_counts = {}
    for f in files:
        file_counts[f] = file_counts.get(f, 0) + 1
    for f, count in file_counts.items():
        if count > 1:
            errors.append(f"[DUPLICATE @id] {f}: @id '{nid}' appears {count} times in same file")

# --- Output ---
print("=" * 70)
print("STRUCTURED DATA VALIDATOR — hemalshah.vercel.app")
print("=" * 70)
print(f"Files scanned : {len(HTML_FILES)}")
print(f"Errors        : {len(errors)}")
print(f"Warnings      : {len(warnings)}")
print()

if errors:
    print("-- ERRORS ----------------------------------------------------------")
    for e in errors:
        print(f"  {e}")
    print()

if warnings:
    print("-- WARNINGS --------------------------------------------------------")
    for w in warnings:
        print(f"  {w}")
    print()

if not errors and not warnings:
    print("ALL CLEAN — no structured data errors found.")

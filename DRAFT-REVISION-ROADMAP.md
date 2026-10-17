# Draft Revision Roadmap: draft-shah-agent-readiness-evaluation

How `-00` grows into a citable, data-backed, implementable specification across
`-01`, `-02`, `-03`, and beyond. One revision per milestone, each adding
something concrete that the running code can prove.

- **Current state:** `-00` is live, idnits-clean (0 errors), and defines the
  method, the four pillars, the scoring convention, Security Considerations, and
  IANA Considerations.
- **Source of truth:** `docs/draft-shah-agent-readiness-evaluation-00.xml`
  (the `.txt` is a render). Reference implementation: the `agent-authority`
  repo at `D:\projects\HK\agent-authority`.
- **The rule that drives this roadmap:** never add a claim the running code
  cannot produce. Each revision below lists what the code must do *first*, then
  what text the draft gains. If the code can't back it, it waits.

---

## The through-line

`-00` answered *"what should be measured, and against which standard?"* Every
later revision answers a different, harder question:

| Rev | The question it answers | The artifact it adds |
| :-- | :-- | :-- |
| `-01` | "Is this a real problem?" | Empirical scan data over a public domain fleet |
| `-02` | "Can someone else implement it identically?" | A normative JSON output schema (appendix) |
| `-03` | "Does it survive the messy real web?" | Edge-case handling: challenges, content negotiation, compression |
| `-04+` | "Is it stable enough to be an RFC?" | Consolidation, ISE submission, AUTH48 |

Each revision resets the 6-month expiry clock. You can post a revision any time;
you do not wait for the clock.

---

## `-01` — Empirical grounding (the one that matters most)

**Question:** does the problem the draft describes actually exist in the wild?

**Code to build first (in `agent-authority`):**
- A batch runner: `cli.py --batch <list-file>` that audits many domains
  concurrently with a bounded connection pool and per-host politeness, writing
  one JSON line per domain. (This is also the natural home for the Rust engine
  when you build it — the batch path is where throughput matters.)
- Aggregate stats: for a run of N domains, compute the share that pass each
  individual check (robots allows AI bots, `describedby` present, api-catalog
  served, JSON-LD parses, `sameAs` all-absolute, TLS 1.3, etc.).
- Run it against a public, reproducible list (Tranco top-N is the standard
  choice for research because the list itself is versioned and citable).

**Draft text to add:**
- A new subsection under `scoring` (anchor e.g. `empirical`): "Empirical
  Observations Across Origin Fleets." Report the pass-rates as a table, state
  the list used and its version, the date of the run, and the sample size.
- Keep every number reproducible: name the Tranco list ID and the
  `agent-authority` commit so a reader can re-run it.

**Why first:** hard network data is the single most persuasive thing you can add.
It turns "here is a method" into "here is a measured, widespread gap." It is also
honest leverage — it is your own tool's output, verifiable by anyone.

**Honesty guardrail:** report what you actually measured. If you scanned 5,000
domains, say 5,000, not 10,000. State the vantage point (one scanner, one region,
one point in time) because the draft's own Security Considerations already warn
that observations are point-in-time and vantage-dependent — the empirical section
must live by that same caveat.

---

## `-02` — A normative output schema (makes it implementable)

**Question:** can an independent engineer in another language produce byte-for-byte
comparable results?

**Code to build first:**
- Freeze the JSON shape the engine already emits (score, per-pillar scores,
  per-check `{status, standard, observation, reproduce, fix}`) into a documented
  schema. The current server returns `overall_score` plus telemetry; pin those
  field names and types.
- Add `cli.py --json` output that conforms exactly to that schema, and a schema
  file (JSON Schema draft 2020-12) checked into the repo.

**Draft text to add:**
- A new appendix (anchor e.g. `json-schema`): "Diagnostic Output Schema." Define
  the exact JSON an implementation emits, field by field, so a Rust or Go
  re-implementation is verifiably equivalent to the Python reference.
- Mark it normative for *tools that claim to implement this method* — carefully,
  because `-00` is deliberately Informational. The schema constrains conformant
  tools, not evaluated sites. Keep that distinction explicit, exactly as the
  Requirements Language section already frames keywords.

**Why second:** this is what makes the draft a *standard* people build to, not
just a paper. It is also what lets the German/EU re-implementation you talked
about match your reference output.

---

## `-03` — Real-web edge cases (hardening)

**Question:** does the method hold up against the messy, hostile, inconsistent web?

**Code to build first** (these are real behaviors the scanner hits):
- **Challenge vs. refusal:** distinguish a genuine RFC 9309 `Disallow` from a
  Cloudflare/Akamai bot-challenge or CAPTCHA page returned with status 200. The
  scanner already has a challenge heuristic; make it rigorous and record which
  one fired.
- **Content-negotiation clashes:** servers that return raw Markdown only under
  `Accept: text/markdown`, vs. those that ignore it; servers that serve HTML at
  the `.md` path. Decide and document how each is scored.
- **Compression traps:** handling `Content-Encoding: zstd` (Meta/Zstandard, RFC
  8878) vs. `br` (Brotli, RFC 7932) vs. gzip, so a compressed body is read
  correctly before parsing. (Your `requirements.txt` already lists `zstandard`,
  so this is partly wired.)

**Draft text to add:**
- Expand the `scoring` "not observed vs. non-conformant" discussion with the
  challenge-detection rule.
- Expand `cei` (Content Efficiency) with the content-negotiation rules.
- A short note on transfer-encoding handling where it affects what the scanner
  can read.

**Why third:** these come from *running* the tool. You will discover them by
scanning real domains for `-01`, which is why this revision follows the data, not
precedes it.

---

## Continuous across all revisions: the AI crawler corpus

Pillar 1 (`disc`) checks whether named AI-agent tokens are allowed in robots.txt.
That list of tokens is a moving target and should be refreshed every revision.

**Current engine state (worth noting):** the rewritten engine checks only
`GPTBot`, `ClaudeBot`, and `PerplexityBot`, and does so with a coarse string
match (`"Disallow: /" not in text`), not the longest-match RFC 9309 semantics the
`-00` draft text describes. **Before `-01`, align the code to the draft:** either
implement proper per-token longest-match evaluation, or soften the draft's claim.
The draft and the reference implementation must not disagree — a reviewer will
check exactly this.

**Tokens to track as the corpus grows:**
- `GPTBot`, `OAI-SearchBot` (OpenAI)
- `ClaudeBot`, `anthropic-ai` (Anthropic)
- `PerplexityBot` (Perplexity)
- `Google-Extended` (Google Gemini), `Googlebot`
- `Applebot-Extended` (Apple Intelligence)
- `CCBot` (Common Crawl), `Bytespider`, `Amazonbot`, `meta-externalagent`

Each revision: update the engine's token set and the `disc` section together, and
cite that these are product tokens observed in the wild (they are conventions, not
a registry), consistent with how `-00` already labels conventions vs. standards.

---

## The changelog (every revision carries one)

IETF drafts end with an appendix recording what changed. Add this appendix at
`-01` and append to it each revision. Example after a couple of rounds:

```
Appendix A.  Changes Since -00

   Since -00:
   *  Added empirical scan observations over a Tranco top-N fleet
      (Section on Empirical Observations), with list version and
      reference-implementation commit cited for reproducibility.
   *  Aligned the robots.txt evaluation description in Section on
      Agent Discoverability with the reference implementation's
      longest-match RFC 9309 semantics.

   Since -01:
   *  Added a normative diagnostic output schema (Appendix on Output
      Schema) for conformant implementations.
   *  Expanded the AI user-agent token set in Section on Agent
      Discoverability (OAI-SearchBot, Applebot-Extended, meta-
      externalagent).
```

In xml2rfc v3 this is a `<section>` inside `<back>` (after the references),
rendered as an appendix.

---

## Mechanics of posting a revision

1. Copy `draft-...-00.xml` to `draft-...-01.xml`.
2. Change **both** the filename stem and the `docName=` attribute to end in `-01`.
   They must match or the upload bounces.
3. Update `<date>` to the real upload day.
4. Add the new sections/appendix and bump the changelog.
5. Re-render and re-check (the command that works on this machine):
   ```
   cd D:\projects\HK\tensix\docs
   & "C:\Users\LW-160926-01\AppData\Local\Python\pythoncore-3.14-64\Scripts\xml2rfc.exe" draft-shah-agent-readiness-evaluation-01.xml --text --out draft-shah-agent-readiness-evaluation-01.txt
   ```
6. Upload the `.xml` at https://datatracker.ietf.org/submit/ after confirming
   0 errors at https://author-tools.ietf.org/idnits.
7. The expiry clock resets to 6 months from the new post.

Full submission detail lives in `docs/RFC-SUBMISSION-STEPS.md`.

---

## When to stop revising and request an RFC

Revise while the method is still changing (new data, new edge cases, schema
churn). When the pillars, the scoring convention, and the output schema have gone
a revision or two without substantive change — that is the signal it is stable.
At that point, request publication through the Independent Submissions Editor
(Stage 3 in `RFC-SUBMISSION-STEPS.md`). Stability, not a revision count, is the
trigger; some drafts reach it at `-03`, others take more.

---

## One sequencing note

The roadmap above is deliberately ordered: **data (`-01`) before schema (`-02`)
before edge cases (`-03`)**, because the data run is what surfaces the edge cases,
and the schema is easiest to freeze once you have run the tool at volume. The
Rust engine you deferred fits naturally at `-01`: the batch fleet scan is exactly
the high-throughput workload that justifies it. Build the batch runner once, in
whichever language, and both the empirical section and the performance goal are
served by the same work.

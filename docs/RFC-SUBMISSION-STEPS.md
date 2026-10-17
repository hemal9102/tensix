# RFC Approval: Every Step, Start to Finish

This is the complete path for `draft-shah-agent-readiness-evaluation-00`, from
the files you have now to an actual published RFC. Read it once end-to-end
before you start — the stages are very different in effort and timeline.

Author: Hemal Shah (TENSIX). Datatracker username: `hemal.shah2004`.
Files (already generated and validated): in `D:\projects\HK\tensix\docs\`
- `draft-shah-agent-readiness-evaluation-00.xml`  (the source — this is what you upload)
- `draft-shah-agent-readiness-evaluation-00.txt`  (the rendered text — for your own review)

Current status: the XML renders cleanly with xml2rfc 3.34.1 and passes the
official IETF idnits checker with **0 errors, 0 flaws, 0 comments** (one benign
pre-RFC5378 warning that does not apply to new work). It is ready to upload.

---

## The one thing to understand first: "Internet-Draft" is NOT "RFC"

Uploading a draft is easy and happens in minutes. Becoming an *RFC* is a
separate, much longer process. Do not confuse the two.

- **Posting an Internet-Draft** = publishing a work-in-progress document. Anyone
  with a Datatracker account can do it. It expires in 6 months unless you post a
  new version. It gives you a citable, timestamped, public document. This is
  Stage 1 and you can do it today.
- **Publication as an RFC** = the document is reviewed, approved by a stream's
  authority, edited by the RFC Editor, and assigned an RFC number. This takes
  months to years and is not guaranteed. This is Stages 3–6.

For your stated goal (a citable, authoritative, standards-referencing document
with your name on it, that you can point clients and the `Agent Authority` tool
at), **Stage 1 alone already delivers most of the value.** The RFC number is a
long game on top of that.

---

## Stage 0 — Pre-flight (do this once, now)

1. **Confirm the Datatracker account.** Log in at
   https://datatracker.ietf.org/accounts/profile/ as `hemal.shah2004`. Make sure
   the email on the account is one you read — all process mail goes there.
2. **Re-run idnits yourself** so you see a clean result with your own eyes. Upload
   the `.txt` (or `.xml`) at https://author-tools.ietf.org/idnits and confirm
   "0 errors". (We already did this; this is just so you trust it.)
3. **Optional: render it yourself** to see the formatted document at
   https://author-tools.ietf.org/ — paste or upload the `.xml` and it produces
   text/HTML/PDF. Good for a final read-through.
4. **Pin the date to your real upload day.** The draft is dated `2026-10-17`. If
   you upload on a different day, open the `.xml`, change
   `<date year="2026" month="10" day="17"/>` to the actual day, and re-render.
   A draft dated more than a few days in the past draws a cosmetic "document date
   is older than N days" comment; a future date draws a warning. Neither blocks
   upload, but matching the real day keeps it clean.

**How to re-render after any edit** (the command that works on this machine):

```
cd D:\projects\HK\tensix\docs
& "C:\Users\LW-160926-01\AppData\Local\Python\pythoncore-3.14-64\Scripts\xml2rfc.exe" draft-shah-agent-readiness-evaluation-00.xml --text --out draft-shah-agent-readiness-evaluation-00.txt
```

---

## Stage 1 — Post the Internet-Draft (today; ~10 minutes)

1. Go to https://datatracker.ietf.org/submit/ (logged in).
2. Upload `draft-shah-agent-readiness-evaluation-00.xml`. The submission tool
   runs its own idnits and renders the text/HTML; you'll see a preview.
3. The filename stem must equal the `docName` in the file. Both are
   `draft-shah-agent-readiness-evaluation-00` — already matched, so it won't
   bounce on that.
4. Confirm the metadata the tool extracts (title, author, stream = Independent,
   intended status = Informational). Approve and submit.
5. You'll get a confirmation email. Click the link to finalize the post.
6. Done. The draft is now live at a URL like
   `https://datatracker.ietf.org/doc/draft-shah-agent-readiness-evaluation/` and
   is permanently archived and citable. Update the `Agent Authority` README to
   cite that URL instead of (or alongside) the GitHub repo.

**Keeping it alive:** a draft expires after 6 months. To refresh, bump the
version (`-01`, `-02`, ...) in both the filename and `docName`, update `<date>`,
and re-submit. Each repost resets the 6-month clock.

---

## Stage 2 — Decide the stream (this is the strategic fork)

An RFC is published through one of several "streams." Your draft is currently
tagged **Independent Submission** (`submissionType="independent"`). Here is the
honest trade-off:

- **Independent Submission Stream (ISE).** For documents that are NOT IETF
  consensus work — exactly your case (a one-person diagnostic method). You submit
  to the Independent Submissions Editor, who arranges review and decides. Good
  fit for an Informational document like this. Lower coordination overhead than
  the IETF stream. This is the recommended path for this document.
- **IETF Stream (via a Working Group or AD sponsorship).** For work the IETF
  adopts and builds consensus on. Much heavier: you'd pitch it to a relevant WG
  (e.g. in the Applications/ART area, or httpapi), get it adopted, and iterate
  through WG and IETF-wide review. Only worth it if you want IETF endorsement and
  are ready for a multi-year community process. Not recommended for a first
  document unless that's specifically your aim.

**Recommendation:** stay Independent. The rest of this guide follows the ISE path.

---

## Stage 3 — Request Independent Submission review (weeks to months)

1. Read the ISE's current process page: https://www.rfc-editor.org/about/independent/
2. Email the Independent Submissions Editor (contact on that page; currently the
   `rfc-ise@rfc-editor.org` alias) with a short note: what the document is, why
   it's Independent (not IETF consensus work), and the draft name. Keep it to a
   few sentences.
3. The ISE does a first assessment of whether it's in scope and worth pursuing.
   They may decline, suggest it belongs in the IETF stream, or accept it for
   review. Expect this to take a while and to involve back-and-forth email.

---

## Stage 4 — Independent review + IETF conflict review (months)

1. If the ISE proceeds, they arrange **independent technical review** (reviewers
   they choose). You'll get comments; you revise and post new `-NN` versions.
2. The document goes through **IETF conflict review** (RFC 5742): the IESG checks
   that an Independent-stream document doesn't conflict with or end-run IETF work.
   For a measurement method that explicitly changes no protocol and registers
   nothing, this is normally straightforward, but it is a required gate.
3. Iterate until the ISE is satisfied and conflict review clears.

---

## Stage 5 — RFC Editor queue and editing (months)

1. The ISE approves the document for publication. It enters the **RFC Editor
   queue** (track it at https://www.rfc-editor.org/current_queue.php).
2. The RFC Editor copy-edits for style, expands/clarifies, and sends you
   **AUTH48** — the final author review where you approve the edited text. Respond
   promptly; documents stall here waiting on authors.
3. Any last reference or boilerplate issues get resolved here (e.g. the RFC Editor
   will confirm the normative references, including that TLS 1.3 now points at
   RFC 9846, not the obsoleted RFC 8446).

---

## Stage 6 — Publication

The document is assigned an **RFC number**, published at
`https://www.rfc-editor.org/rfc/rfcNNNN`, and archived permanently. You are now
the author of an RFC. The draft and all its versions remain in the history.

---

## Realistic expectations

- **Stage 1 (post the draft):** today, ~10 minutes, fully in your control.
- **Stages 3–6 (become an RFC):** typically many months to a couple of years,
  depends on reviewer and ISE availability, and publication is not guaranteed.
- **What you control:** document quality (done — it's idnits-clean), responsiveness
  to review, and keeping the draft from expiring.
- **What you don't control:** whether the ISE and reviewers judge it worth
  publishing as an RFC.

Most of the business value you described — an authoritative, citable, timestamped
document under your name that references real RFCs and backs the `Agent Authority`
tool — is captured at **Stage 1**. Treat RFC publication as an optional long-term
upside, not a prerequisite.

---

## If idnits ever complains after an edit

Common causes and fixes (from the validated build of this document):

- **"docName does not match filename"** — the `docName=` attribute and the
  uploaded filename stem must be identical, including the `-NN` version.
- **"Obsolete normative reference"** — a cited RFC was superseded. Verify the
  replacement and update the `<xi:include ... reference.RFC.NNNN.xml>` and every
  in-text `<xref target="RFCNNNN"/>`. (This is how RFC 8446 → RFC 9846 was fixed.)
- **"undefined reference [WORD]"** — a literal bracketed token survived in the
  text instead of becoming an `<xref target="anchor"/>`. Convert it.
- **Over-length line in artwork/sourcecode** — xml2rfc can't reflow `<artwork>`
  or `<sourcecode>`; keep every literal line ≤ 69 chars. (Prose wraps
  automatically; you never hand-wrap body text in v3.)
- **Empty/missing Security or IANA Considerations** — both are mandatory. This
  document has substantive versions of both; don't delete them.

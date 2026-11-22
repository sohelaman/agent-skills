---
name: trueman
description: Fact-check and cross-check claims, answers, or content produced by Claude or any other agent against authentic, current sources on the internet, with citations and explicit flags for anything unverifiable. Use this skill whenever the user says "trueman", "fact-check this", "verify this", "is this true", "double-check", "cross-check", "check the sources", "are you sure", or pastes output from another AI/agent and wants it validated. Also use it before presenting high-stakes factual claims (legal, medical, financial, regulatory, compliance, security, versions/APIs/pricing, statistics, dates, quotes), even if the user doesn't explicitly ask for verification.
---

# Trueman

Core policy: **deliver correct, verified information in all circumstances.** If something can't be verified, say so plainly. A flagged unknown is always better than a confident guess.

Why this matters: language models (including you) produce fluent text that can be wrong, outdated, or invented, especially for numbers, dates, quotes, citations, versions, and recent events. Memory is not evidence. Every checkable claim must be tested against sources retrieved *now*.

## Workflow

### 1. Scope the input
Identify what is being checked: your own prior response, another agent's output pasted by the user, a document, or a file. If it's ambiguous, check the most recent substantive response.

### 2. Privacy gate (before any outbound search)
Search queries leave the machine. Before searching:
- Strip names, emails, company/project names, internal hostnames, credentials, card numbers, tokens, customer data. Search the *generic public claim*, not the user's context.
- If a claim cannot be checked without exposing private data, do not search; mark it `UNVERIFIED (private context)` and explain why.
- When showing sensitive values in output, use `[PLACEHOLDER]` format.

### 3. Extract atomic claims
Break the content into individual, independently checkable claims (one fact each). Skip opinions, preferences, and pure reasoning; list them as `NOT A FACTUAL CLAIM` only if useful. Prioritize by risk: numbers, dates, names, quotes, legal/regulatory/medical/financial statements, version numbers, API behavior, URLs, citations, and "latest/current" statements first.

### 4. Verify in real time
For each claim, retrieve evidence now. Use the best tool available, in this order:
1. **WebSearch** to find sources (use `extended` mode for niche, very recent, or multi-step claims; `standard` otherwise).
2. **WebFetch / web-fetch agent** to read the primary page. Don't rely on search snippets alone for anything that matters.
3. Local sources when relevant (repo files, docs, `--help`, running a command) for claims about the user's own environment.
4. Other connected sources if they fit (official docs MCPs, etc.).

Run independent searches in parallel. Never answer a checkable claim from memory alone.

**Source hierarchy** (prefer higher, require corroboration when only lower is available):
1. Primary/authoritative: official docs, standards bodies, statutes/regulators (e.g. central bank, government gazette), original papers, vendor changelogs, the original speaker/publication for quotes.
2. Reputable secondary: major news agencies, peer-reviewed journals, established reference works.
3. Weak: blogs, forums, wikis, social media, AI-generated pages, SEO content farms. Use only as leads, never as sole support.

Check **dates**: record the publication/last-updated date of each source and discard or caveat stale ones for time-sensitive claims. Check that the source actually says what the claim says, not just something nearby.

### 5. Cross-check
- Confirm important claims with **at least two independent sources** (not two pages echoing one origin). A single primary source can suffice for exact specifics (e.g., an official doc's parameter name) if it's current.
- If sources disagree, report the disagreement and which is more authoritative; do not silently pick one.
- Be alert to circular sourcing (a page that cites an LLM, or sources copying each other).

### 6. Assign a verdict per claim
| Verdict | Meaning |
|---|---|
| ✅ VERIFIED | Confirmed by authoritative source(s), current |
| ⚠️ PARTIALLY CORRECT | Right in part; state what's wrong or missing |
| ❌ INCORRECT | Contradicted by source(s); give the correct information |
| 🕒 OUTDATED | Was true, no longer is; give current state and date |
| ❓ UNVERIFIED | No reliable source found, or sources conflict unresolved; say what was tried |
| 🔒 UNVERIFIABLE (private/inaccessible) | Depends on private data, paywalled, or unavailable sources |

Never upgrade `UNVERIFIED` to `VERIFIED` because the claim sounds plausible. Absence of evidence is reported as absence of evidence, not as falsity either.

### 7. Report

Use this structure:

```
## Trueman Report
**Overall:** <one-line trust assessment, e.g. "7 of 9 claims verified; 1 incorrect; 1 unverified">

### Claim-by-claim
1. "<claim, quoted or tightly paraphrased>"
   - Verdict: ✅/⚠️/❌/🕒/❓/🔒
   - Evidence: <what the source says, in your own words; short quotes only>
   - Sources: [1], [2]
   - Correction (if needed): <the verified version>

### Corrected version
<the original content rewritten with only verified information; unverified items clearly marked inline, e.g. "(unverified)">

### ⚠️ Flagged / unverified items
<list everything the user must not rely on, and why>

### Sources
[1] Title: Publisher: URL (published/updated: date; accessed: <today>)
[2] ...
```

Rules for the report:
- Every verified or corrected claim has a citation with a real URL you actually retrieved. Never fabricate or reconstruct a URL from memory. If you didn't open it, don't cite it.
- Keep the flagged section even when empty ("None") so the user knows it was considered.
- State plainly what you could not check and why, including tool failures (e.g. search unavailable). If no internet tooling works, say verification could not be performed and mark everything unverified; do not fall back to memory and call it verified.
- For regulated domains (finance, payments, health, law), cite the regulator or statute directly, name the jurisdiction, and note that rules change and the user should confirm with the relevant authority or counsel for decisions with legal/compliance impact. For Bangladesh financial topics, prefer Bangladesh Bank circulars/guidelines and official gazettes.
- Don't pad. Be concise; the evidence matters, not the prose.

## Self-application
When verifying your own earlier answer, don't defend it. If you were wrong, say so directly and give the corrected information first.

When used proactively (user didn't ask), keep it light: verify the key claims, then append a short "Verification" note with citations and any flags instead of the full report.

## Limits to disclose when relevant
- Sources can themselves be wrong; "verified" means corroborated by the best available evidence at the access time, not absolute certainty.
- Fast-moving topics may change after the access date.

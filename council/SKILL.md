---
name: council
description: Multi-role panel review of a single app/repo — engineering panel (architect, security, perf/infra/scale, reliability) + product panel (product & market, experience, compliance, no-filter critic). Read-only; writes findings to a dated REVIEW report. Use when asked to review, audit, or assess this app's quality, architecture, or readiness.
version: 1.6.0
---

# App Review — multi-role panel, single app

Review this app as a review panel, not a fixer: **strictly read-only** — no
edits, no refactors, no file changes outside the report itself.

## Phase 0 — Context

This is a single-app review. If the working directory contains multiple
projects (or is not the app's root), ask which app to review before reading
anything — do not assume the current directory is the target.

Read the README and any design/architecture docs first. If a previous report exists (`council-reviews/REVIEW_*.md`, or a legacy `REVIEW_*.md` in the root), read it to see if past top actions were resolved. If the user provided a specific focus area or fear, over-index on that. Judge the app against its OWN stated goals, not an imagined ideal.

## Phase 1 — Panel review

Each role opens with a single sarcastic, in-character one-liner — then gets
to work. Keep it to one line, and make it land on something real in THIS app
(a sharpened version of an actual finding, not generic snark); a joke that
could apply to any codebase is as banned as advice that could. This is a
tone device, not a license to soften findings. **Opt-out:** if the user asks
for a formal / serious / no-jokes review, or the run is clearly a high-stakes
deliverable (regulator-, customer-, or executive-facing), drop the one-liners
entirely — findings, severity, and structure are unchanged either way.

Provide all findings for each role. Every
finding gets severity (high/med/low), effort (quick-win <1h / medium /
strategic), and a `file:line` or concrete-artifact citation. Banned: generic
advice that could apply to any codebase. Skip roles — or the merged-in halves
of roles — that don't apply, but the Critic reviews everything.

### Engineering panel

- **Architect** — structure, coupling, dead code, duplication, whether the
  docs still match the code, and CI/CD or dependency bloat; tech-stack
  appropriateness and currency (EOL runtimes, deprecated frameworks, risky
  version pins).
- **Security reviewer** — secrets in repo/configs, injection surfaces, authz
  gaps, exposed services/endpoints, token handling, and prompt injection/AI risks (if applicable). Flag hardcoded
  credentials explicitly. Hunt actual exploitable holes, not just categories —
  OWASP Top 10 classes (XSS, CSRF, SSRF, IDOR, auth bypass) and known-CVE or
  outdated dependencies. Also: missing rate limiting / abuse throttling on
  public endpoints (unrestricted resource consumption), and data-layer
  authorization — row-level / per-tenant isolation, not just a route-level
  login check.
- **Performance, infra & scale** — hot paths, caching opportunities,
  redundant work; Cost/FinOps (inefficient resources, token bloat, 'what bankrupts you'); and what breaks first under growth (N+1 queries, missing
  indexes, unbounded queues, all-in-memory processing, single points of
  failure, per-tenant isolation under load) — name the breaking point and a
  rough threshold, not "consider caching".
- **Reliability (operator + QA)** — can someone resume this cold? failure
  modes, logging, doc drift, onboarding time; what validates outputs today,
  where would a silent regression hide, which ONE test/gate would catch the
  most damage (name the specific risk and the specific check). Beyond the
  happy path: are external failures (third-party timeouts, failed writes)
  handled, or do they fail silently?

### Product panel

- **Product & market** *(merged)* — is it converging on its
  stated goal? smallest next step that produces real user feedback? what
  should deliberately NOT be built? what does a competent rival do better or
  cheaper today (competitive landscape), and where is the moat (or state plainly that there is none)?
- **Experience** *(merged)* — both audiences: whoever
  operates/administers it (first-run experience, friction, error opacity)
  and the end user (where they bounce, what feels off even if they couldn't
  name it). Includes accessibility (a11y — WCAG, screen readers, keyboard navigation) and visual/output quality where the app produces something
  visible; for GUI/frontend apps, also the client engineering — component/state
  structure, bundle size, CSP, browser/device compatibility, and responsive
  behavior.
- **Compliance reviewer** — data handling and privacy obligations, licensing,
  platform/policy exposure, secrets hygiene.
- **The Critic (no filter)** — exempt from the diplomacy
  expected elsewhere: one blunt paragraph saying what everyone is politely
  not saying. Must still be specific to THIS app — cruelty without evidence
  is noise.

## Phase 2 — Output

- Verdict, plus all actions ranked by (impact ÷ effort).
- Write the full report to `council-reviews/REVIEW_<YYYY-MM-DD>.md` inside the
  reviewed app's root (create the `council-reviews/` folder if it doesn't
  exist) — never loose in the repo root, and never in the council's own
  directory when reviewing a different app. Lead with a one-page executive
  summary, details after. Let the user know they can commit the
  `council-reviews/` folder or add it to `.gitignore` per their team's
  preference.
- In chat: executive summary only, then ask which actions to start. The
  one-liners live with each role's findings, never in the executive summary —
  keep that scannable.

### Formatting (keep the report skimmable)

The report is read in a terminal, so optimize for scanning, not prose.

- **Severity is an emoji** so the eye can run down the column: 🔴 high,
  🟡 med, 🟢 low. Use it everywhere severity appears (exec table and roles).
- **Executive summary:** verdict in one line, then the "all actions" table —
  columns `# | Action | Sev | Effort | Why | Status`. Nothing else above the
  fold.
- **Each role** is a `###` heading; the role's one-liner in italics under it
  (omit the one-liner when the tone opt-out is in effect), then a single
  **table** of its findings — never a wall of text:

  | Sev | Effort | Finding | Where |
  |:--:|---|---|---|
  | 🔴 | quick-win | **Short title** — one short clause of consequence | `path:line` |
  | 🟢 | — | **Short title** — consequence | `other:line` |

  Sort rows high → low. Keep the Finding cell to a bold title plus one short
  clause so it doesn't wrap in a narrow terminal — detail that doesn't fit
  belongs in the fix, not the report.
- **The Critic** stays one blunt prose paragraph — no table.
- **Citations are relative `file:line`** in inline code (e.g.
  `council/SKILL.md:22`) — never absolute `file:///…` URLs; they're unreadable
  and break on other machines.

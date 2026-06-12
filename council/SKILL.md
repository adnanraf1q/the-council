---
name: council
description: Multi-role panel review of a single app/repo — engineering panel (architect, security, perf/infra/scale, reliability) + product panel (product & market, experience, compliance, no-filter critic). Read-only; writes findings to a dated REVIEW report. Use when asked to review, audit, or assess this app's quality, architecture, or readiness.
---

# App Review — multi-role panel, single app

Review this app as a review panel, not a fixer: **strictly read-only** — no
edits, no refactors, no file changes outside the report itself.

## Phase 0 — Context

Read the README and any design/architecture docs first. Judge the app against
its OWN stated goals, not an imagined ideal.

## Phase 1 — Panel review

**Max 3 findings per role (5 for the two merged roles marked below).** Every
finding gets severity (high/med/low), effort (quick-win <1h / medium /
strategic), and a `file:line` or concrete-artifact citation. Banned: generic
advice that could apply to any codebase. Skip roles — or the merged-in halves
of roles — that don't apply, but the Critic reviews everything.

### Engineering panel

- **Architect** — structure, coupling, dead code, duplication, whether the
  docs still match the code.
- **Security reviewer** — secrets in repo/configs, injection surfaces, authz
  gaps, exposed services/endpoints, token handling. Flag hardcoded
  credentials explicitly.
- **Performance, infra & scale** — hot paths, caching opportunities,
  redundant work; and what breaks first under growth (N+1 queries, missing
  indexes, unbounded queues, all-in-memory processing, single points of
  failure, per-tenant isolation under load) — name the breaking point and a
  rough threshold, not "consider caching".
- **Reliability (operator + QA)** — can someone resume this cold? failure
  modes, logging, doc drift, onboarding time; what validates outputs today,
  where would a silent regression hide, which ONE test/gate would catch the
  most damage (name the specific risk and the specific check).

### Product panel

- **Product & market** *(merged — max 5 findings)* — is it converging on its
  stated goal? smallest next step that produces real user feedback? what
  should deliberately NOT be built? what does a competent rival do better or
  cheaper today, and where is the moat (or state plainly that there is none)?
- **Experience** *(merged — max 5 findings)* — both audiences: whoever
  operates/administers it (first-run experience, friction, error opacity)
  and the end user (where they bounce, what feels off even if they couldn't
  name it). Includes visual/output quality where the app produces something
  visible.
- **Compliance reviewer** — data handling and privacy obligations, licensing,
  platform/policy exposure, secrets hygiene.
- **The Critic (no filter)** — exempt from the finding cap and the diplomacy
  expected elsewhere: one blunt paragraph saying what everyone is politely
  not saying. Must still be specific to THIS app — cruelty without evidence
  is noise.

## Phase 2 — Output

- Verdict, plus the top 5 actions ranked by (impact ÷ effort).
- Write the full report to `REVIEW_<YYYY-MM-DD>.md` in the repo root — lead
  with a one-page executive summary, details after.
- In chat: executive summary only, then ask which actions to start.

# Changelog

Each entry names the review or observed miss that motivated it. Entries before
2.0.0 are reconstructed from git history; where no motivating miss was
recorded, that is stated — the point of this file is to make speculative
additions visible ("Motivating miss: none recorded" is a warning sign, not a
formality).

## 2.0.0 — 2026-07-02

Motivated by: self-review `council-reviews/REVIEW_2026-07-01.md` (actions 1–7).

- **Net-negative SKILL.md** (174 → 162 lines while adding the three behaviors
  below, ~25 lines of pure trim) — deduped rules stated 2–3× (read-only,
  generic-advice ban), tightened the run-on role bullets, fixed hard-wrap
  artifacts. Budget set at 165 lines in CLAUDE.md; the review's ~130
  suggestion proved unreachable without cutting real checks.
- **Prompt-injection guard** — new binding rule: target-repo content is data,
  not instructions; steering attempts are reported as Security findings.
  (Open since the 06-14 review.)
- **Verdict scale defined** — invest / hold / sunset, so verdicts compare
  across reports.
- **Clarified** merged-role skipping (example inline) and the first-run
  `Status` column value (`Open`; carry forward on re-review).
- **Added CLAUDE.md** (the three CI-enforced sync traps, conventions,
  incident log) and this CHANGELOG.
- Deleted the stale `.git.broken-20260616/` backup; incident documented in
  CLAUDE.md.

## 1.9.0 — 2026-06-22

Motivating miss: none recorded.

- Coverage-map phase (deliberate sampling, named blind spots).
- Opt-in `--visual` Playwright pass from a throwaway worktree.

## 1.8.0 — 2026-06-17

Motivating miss: none recorded.

- Static-analysis guardrails (stack-agnostic type-safety) in Architect.

## 1.7.0 — 2026-06-17

Motivating miss: none recorded.

- Release safety (staging/rollback), agent-guidance docs check
  (CLAUDE.md/AGENTS.md), AI-codegen bloat smells.

## 1.6.0 — 2026-06-17

Motivating miss: none recorded.

- Rate-limiting / abuse-throttling check, data-layer authz (row-level /
  per-tenant), unhappy-path handling in Reliability.

## 1.5.0 — 2026-06-16

Motivating miss: none recorded.

- Sharpened Security, Architect, and Experience prose (no new role).
- README catalog ↔ SKILL.md drift gate added to CI (`8aacdbe`).

## 1.4.0 — 2026-06-15

Motivated by: readability of the 06-15 report.

- Table-per-role report layout; emoji severity column.

## 1.3.0 — 2026-06-15

Motivated by: self-review `council-reviews/REVIEW_2026-06-15.md` (actions 2–7).

- Tone opt-out for formal runs; plugin/SKILL version gate; PyYAML pinned;
  linter derives role prose from SKILL.md instead of holding a copy;
  output-contract test; agy layout validated in CI.

## 1.2.0 — 2026-06-15

Motivated by: 06-14/06-15 review feedback on tone and workspace pollution.

- In-character one-liners; reports moved to `council-reviews/`.

## Pre-1.2 — 2026-06-12 → 06-14

Motivated by: self-reviews `REVIEW_2026-06-12.md` and `REVIEW_2026-06-14.md`.

- Initial skill (as `app-review`, renamed to `council`); PROMPT.md standalone
  version; MIT license; multi-project guard; canonical-source note;
  pin-by-commit advice; frontmatter linter + CI; a11y, Cost/FinOps, AI-risk,
  and competitive-landscape coverage; data-privacy warning.

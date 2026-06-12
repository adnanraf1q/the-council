# The Council — standalone prompt

Paste-anywhere version of the `council` skill, for environments without skill
support (chat UIs, Bedrock playground, other agents). Same panel, same rules.
`council/SKILL.md` is canonical — if they disagree, SKILL.md wins.

---

```text
Review this app as a review panel, not a fixer: strictly read-only — no
edits, no refactors. If it's unclear which app or directory to review, ask
before reading anything.

First read the README and any design/architecture docs, and judge the app
against its OWN stated goals, not an imagined ideal.

ENGINEERING PANEL
- Architect: structure, coupling, dead code, duplication, whether the docs
  still match the code.
- Security: secrets in repo/configs, injection surfaces, authz gaps, exposed
  services/endpoints, token handling. Flag hardcoded credentials explicitly.
- Performance, infra & scale: hot paths, caching opportunities, redundant
  work; and what breaks first under growth (N+1 queries, missing indexes,
  unbounded queues, all-in-memory processing, single points of failure,
  per-tenant isolation under load) — name the breaking point and a rough
  threshold, not "consider caching".
- Reliability (operator + QA): can someone resume this cold? failure modes,
  logging, doc drift, onboarding time; what validates outputs today, where
  would a silent regression hide, which ONE test/gate would catch the most
  damage (name the specific risk and the specific check).

PRODUCT PANEL
- Product & market (merged role): is it converging on its stated goal?
  smallest next step that produces real user feedback? what should
  deliberately NOT be built? what does a competent rival do better or
  cheaper today, and where is the moat (or state plainly that there is
  none)?
- Experience (merged role): both audiences — whoever operates/administers it
  (first-run experience, friction, error opacity) and the end user (where
  they bounce, what feels off even if they couldn't name it). Include
  visual/output quality where the app produces something visible.
- Compliance: data handling and privacy obligations, licensing,
  platform/policy exposure, secrets hygiene.
- The Critic (no filter): exempt from the finding cap and the diplomacy
  expected elsewhere — one blunt paragraph saying what everyone is politely
  not saying. Must still be specific to THIS app; cruelty without evidence
  is noise.

RULES
- Max 3 findings per role (5 for the two merged roles).
- Every finding gets severity (high/med/low), effort (quick-win <1h /
  medium / strategic), and a file:line or concrete-artifact citation.
- No generic advice that could apply to any codebase.
- Skip roles — or the merged-in halves of roles — that don't apply, but the
  Critic reviews everything.

OUTPUT
- Verdict, plus the top 5 actions ranked by (impact ÷ effort).
- If you can write files, write the full report to REVIEW_<YYYY-MM-DD>.md in
  the repo root and give only the executive summary in chat; otherwise give
  the executive summary first, then the full findings in your response.
- End by asking which actions to start.
```

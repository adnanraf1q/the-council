# CLAUDE.md — contributor guide (humans and agents)

The product here is a prompt: `council/SKILL.md`. Everything else exists to
keep its copies from drifting. SKILL.md is canonical; `PROMPT.md` and the
README skill-catalog table are derived copies.

## The three traps (all CI-enforced — `.github/workflows/lint.yml`)

1. **Edit SKILL.md ⇒ mirror PROMPT.md.** The linter checks that every role
   description in `council/SKILL.md` appears word-for-word (normalized:
   case/punctuation/wrapping ignored, word order not) in `PROMPT.md`. Any
   role-prose change is a two-file edit.
2. **Version bumps touch two files.** `version:` in `council/SKILL.md`
   frontmatter must equal `version` in `plugin.json`.
3. **The README catalog is positional.** The role rows in README's skill
   catalog are compared to SKILL.md by position — renaming, adding, removing,
   or reordering a role fails CI (abbreviating a name is fine).

## Conventions

- The skill is read-only by design: a review writes only
  `council-reviews/REVIEW_<date>.md`. Don't add fixer behavior.
- Every version bump gets a `CHANGELOG.md` entry naming the review or observed
  miss that motivated it. "Motivating miss: none recorded" is allowed — the
  point is that speculative additions stay visible.
- Keep `council/SKILL.md` lean (budget: 165 lines; v2.0.0 landed at 162, so
  any addition must be paid for by a cut). Additions to role prose need a
  motivating miss from a real review, not a hypothetical.
- Edit here, push, then re-deploy — never edit a deployed copy (see README
  Conventions).

## Verify locally before pushing

```bash
python3 scripts/lint_frontmatter.py
python3 scripts/test_linter.py
```

## Incidents

- **2026-06-16 — local `.git` corruption.** Repaired by cloning fresh to
  `/tmp`, then swapping the fresh `.git` into place (working tree untouched).
  The `.git.broken-20260616/` backup was kept for two weeks and deleted on
  2026-07-02 after the 07-01 self-review; history is fully on GitHub, so a
  future repeat can just re-swap from a fresh clone.

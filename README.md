# the-council

Summon a council of advisors to judge your code. Portable, machine-agnostic skills for [Claude Code](https://claude.com/claude-code) — one shareable source of truth across machines, accounts, and teams.

The flagship skill convenes an eight-seat review panel — architect, security, scale, reliability, product, experience, compliance, and one critic with no filter — over any app you point it at.

A *skill* is a reusable instruction set that Claude Code loads on demand. Instead of re-typing (and re-tuning) the same long prompt on every machine, you define it once here, deploy it everywhere, and invoke it with a slash command like `/council`.

## Repository structure

```
the-council/
├── README.md                  ← you are here
└── council/
    └── SKILL.md               ← the skill definition (frontmatter + instructions)
```

Each skill is a folder containing a `SKILL.md`. The frontmatter (`name`, `description`) is what Claude Code reads to decide when the skill is relevant; the body is the instruction set executed when it runs.

## Installation

### Option A — per-repo (recommended for teams)

Commit the skill into a project's `.claude/skills/` directory. Everyone who clones that project gets the skill automatically — no per-person setup:

```bash
cp -r council <your-repo>/.claude/skills/
cd <your-repo> && git add .claude/skills && git commit -m "Add council skill"
```

### Option B — per-machine (all projects, just you)

Clone this repo once and symlink skills into your user-level skills directory:

```bash
# SSH (machines with your GitHub key):
git clone git@github.com:adnanraf1q/the-council.git ~/the-council
# or HTTPS (works anywhere; prompts for auth on private repos):
git clone https://github.com/adnanraf1q/the-council.git ~/the-council

mkdir -p ~/.claude/skills
ln -s ~/the-council/council ~/.claude/skills/council
```

> Windows (no symlinks by default): copy instead of linking —
> `xcopy /E /I the-council\council %USERPROFILE%\.claude\skills\council`

The symlink means `git pull` in `~/the-council` updates every project on that machine at once.

> **Security note for shared/work machines:** skills are executed instructions —
> auto-updating via symlink means whoever can push to this repo can change what
> Claude Code does on your machine. On machines where that matters, pin instead
> of tracking main: `git -C ~/the-council checkout <commit>` and review the diff
> (`git log -p <pinned>..origin/main`) before moving the pin.

### Option C — restricted environments (e.g. work machines without personal GitHub auth)

The skills are plain text. Copy the folder by any means available (paste the file contents, internal file share) into the target repo's `.claude/skills/`. Treat this repo as the master copy and re-sync manually when it changes.

### Option D — no skill support at all

[`PROMPT.md`](PROMPT.md) is a paste-anywhere standalone version of the council — same panel, same rules — for chat UIs, playgrounds, or any tool that takes a prompt but can't install skills.

## Skill catalog

### `council` — multi-role panel review of a single app

Invoke with `/council` (or ask Claude Code to "review this app").

A read-only review panel for one app/repo. It does not edit code — it produces a dated `REVIEW_<date>.md` report plus an executive summary in chat, with a verdict and the top 5 actions ranked by impact ÷ effort.

**Eight consolidated roles** (merged from a 13-role panel to cut overlap and token cost while keeping coverage). *The table below is a summary — `council/SKILL.md` is canonical; if they ever disagree, SKILL.md wins and this table needs updating:*

| Panel | Role | Looks for |
|---|---|---|
| Engineering | Architect | structure, coupling, dead code, doc drift, CI/CD, dependency bloat |
| Engineering | Security | secrets, injection, authz gaps, exposed surfaces, AI safety/prompt injection |
| Engineering | Performance, infra & scale | hot paths, caching, Cost/FinOps, and **what breaks first under growth** — with a named breaking point and rough threshold |
| Engineering | Reliability (operator + QA) | cold-resume, failure modes, where a silent regression hides, the ONE test/gate worth adding |
| Product | Product & market *(merged)* | convergence on stated goal, smallest step to real user feedback, competitive landscape & moat |
| Product | Experience *(merged)* | operator journey AND end-user journey, accessibility (a11y), plus output/visual quality |
| Product | Compliance | data handling, licensing, platform/policy exposure |
| Product | The Critic (no filter) | one blunt paragraph saying what everyone is politely not saying |

**Quality rules baked in** — these four constraints are what keep the output sharp instead of boilerplate:

1. **Read-only** — review panel, not a fixer.
2. **Finding caps** — max 3 per role (5 for the two merged roles); forces selectivity.
3. **Evidence required** — every finding cites `file:line` or a concrete artifact.
4. **No generic advice** — anything that could apply to any codebase is banned.

**Token-cost notes** (relevant on usage-billed platforms like Amazon Bedrock):

- Review a **diff or single module** day-to-day; save whole-app reviews for milestones.
- The skill runs inline — don't add "use parallel subagents per role"; subagent fan-out is the most expensive pattern per unit of work.
- Finding caps limit output tokens, which cost ~5× input tokens.

## Conventions

- **Edit here, push, then re-deploy.** Never edit a deployed copy directly — copies drift and you end up with three slightly different review panels. Improve the skill in this repo, push, then `git pull` / re-copy at the deployment sites.
- **Keep skills machine-agnostic.** No absolute paths, no references to machine-specific config (GPU rules, local registries, personal file layouts). If a skill needs local context, have it read the target repo's own docs (README, CLAUDE.md) at runtime instead.
- **One skill per folder, one job per skill.** A skill that does two things is two skills.

## Adding a new skill

1. Create `<skill-name>/SKILL.md` with frontmatter:

   ```markdown
   ---
   name: skill-name
   description: One line stating what it does AND when to use it — Claude Code uses this to decide relevance.
   ---

   # Instructions the model follows when invoked...
   ```

2. Keep the description trigger-oriented ("Use when asked to…") — it's the matching surface.
3. Add it to the Skill catalog table above.
4. Commit, push, re-deploy on each machine.

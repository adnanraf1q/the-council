# the-council

Summon a council of advisors to judge your code. Portable, machine-agnostic skills for [Claude Code](https://claude.com/claude-code) — one shareable source of truth across machines, accounts, and teams.

The flagship skill convenes an eight-seat review panel — architect, security, scale, reliability, product, experience, compliance, and one critic with no filter — over any app you point it at.

A *skill* is a reusable instruction set that Claude Code loads on demand. Instead of re-typing (and re-tuning) the same long prompt on every machine, you define it once here, deploy it everywhere, and invoke it with a slash command like `/council`.

## Repository structure

```
the-council/
├── README.md                  ← you are here
├── PROMPT.md                  ← standalone paste-anywhere version (Option D)
├── plugin.json                ← Antigravity CLI (agy) plugin manifest (Option E)
├── council/
│   └── SKILL.md               ← the skill definition (frontmatter + instructions)
├── skills/
│   └── council → ../council   ← symlink exposing the skill under the agy plugin layout
├── scripts/                   ← frontmatter linter + tests (run in CI)
├── .github/workflows/         ← CI: lints frontmatter and SKILL.md ↔ PROMPT.md sync
└── council-reviews/           ← dated REVIEW_*.md reports land here (see Skill catalog)
```

Each skill is a folder containing a `SKILL.md`. The frontmatter (`name`, `description`) is what Claude Code reads to decide when the skill is relevant; the body is the instruction set executed when it runs. The same `council/SKILL.md` is the single source of truth for both install paths — Claude Code (`council/`) and the agy plugin (via the `skills/council` symlink) — so updating it updates both at once. The agy plugin's `version` in `plugin.json` is kept in sync with the `version:` in `SKILL.md`.

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



### Option C — restricted environments (e.g. work machines without personal GitHub auth)

The skills are plain text. Copy the folder by any means available (paste the file contents, internal file share) into the target repo's `.claude/skills/`. Treat this repo as the master copy and re-sync manually when it changes. The `SKILL.md` file contains a `version:` field in its frontmatter so you can check if your copied version is stale.

### Option D — no skill support at all

[`PROMPT.md`](PROMPT.md) is a paste-anywhere standalone version of the council — same panel, same rules — for chat UIs, playgrounds, or any tool that takes a prompt but can't install skills.

### Option E — Antigravity CLI (agy)

If you use the Antigravity CLI (`agy`), you can install the council as a plugin directly:

```bash
# Clone the repository
git clone https://github.com/adnanraf1q/the-council.git ~/the-council
cd ~/the-council

# Validate the plugin layout, then install it locally
agy plugin validate .
agy plugin install .
```

This loads the `council` skill (invoked with `/council`) in your `agy` sessions — the plugin exposes it via the `skills/council` symlink. CI validates the same layout on every push (`plugin.json` is well-formed and its `version` matches `council/SKILL.md`), so the agy path can't silently drift from the Claude Code path.

## Security & Privacy

### Data Transmission & Privacy
The council skill operates by reading the files in your target codebase and sending their contents to the AI model's API for analysis. If you are reviewing private, proprietary, or regulated codebases, please ensure that this transmission complies with your organization's data privacy policies and compliance frameworks (such as GDPR, SOC2, or HIPAA). Do not run this tool on codebases containing sensitive personal data or raw production secrets.

### Supply-chain Security (Symlink Updates)
When using Option B (symlinking the skill repository), running `git pull` will automatically update the skill for all linked projects. Because skills are executed instructions, anyone who can push to the upstream repository can modify the behavior of the slash command on your machine.
For shared or high-security environments:
- Clone the repository and check out a specific pinned commit: `git checkout <commit-hash>`.
- Audit new updates using `git log -p <pinned-hash>..origin/main` before updating your pin.

## Skill catalog

### `council` — multi-role panel review of a single app

Invoke with `/council` (or ask Claude Code to "review this app").

**When to use `/council` vs the built-in `/code-review`:** Use `/code-review` and `/security-review` for day-to-day bug-hunting on individual diffs or files. Use `/council` for high-level, holistic architecture and product reviews where you want actionable strategic advice (the "Product Panel" and "The Critic").

A read-only review panel for one app/repo. It does not edit code — it produces a dated `council-reviews/REVIEW_<date>.md` report plus an executive summary in chat, with a verdict and all actions ranked by impact ÷ effort.

**Eight consolidated roles** (merged from a 13-role panel to cut overlap and token cost while keeping coverage). *The table below is a summary — `council/SKILL.md` is canonical; if they ever disagree, SKILL.md wins and this table needs updating. CI enforces this: the linter fails if the roles here drift from SKILL.md (renamed, added, removed, or reordered).*

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
2. **Evidence required** — every finding cites `file:line` or a concrete artifact.
3. **No generic advice** — anything that could apply to any codebase is banned.

**Token-cost notes** (relevant on usage-billed platforms like Amazon Bedrock):

- Review a **diff or single module** day-to-day; save whole-app reviews for milestones.
- The skill runs inline — don't add "use parallel subagents per role"; subagent fan-out is the most expensive pattern per unit of work.

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

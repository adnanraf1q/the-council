# claude-skills

Portable Claude Code skills — one shareable source of truth across machines and accounts.

## Install

Per-repo (team gets it — commit into the project):

    cp -r app-review <your-repo>/.claude/skills/

Per-machine (all projects, just you):

    git clone git@github.com:adnanraf1q/claude-skills.git
    ln -s "$(pwd)/claude-skills/app-review" ~/.claude/skills/app-review

## Skills

- **app-review** — multi-role panel review of a single app/repo (8 consolidated roles: architect, security, perf/infra/scale, reliability + product & market, experience, compliance, no-filter critic). Read-only, writes a dated REVIEW report. Invoke with `/app-review`.

## Conventions

- Edit skills HERE and push — never edit deployed copies, or machines drift.
- Keep skills machine-agnostic: no absolute paths, no machine-specific config references.

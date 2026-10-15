# session-usage-handoff

An agent skill that helps an AI coding assistant check how much token/quota budget is left, save its work to a Markdown handoff file (default `PROGRESS.md`) before limits run out, and resume cleanly in a new session.

## Features

- **Usage check:** uses exact runtime metrics when the environment exposes them; otherwise estimates from session depth and labels the result as an estimate. It never invents exact numbers.
- **Threshold actions:** Safe (>30% remaining), Caution (15–30%), Critical (<15% or a quota warning).
- **Checkpointing:** writes or updates a structured handoff file without blindly overwriting earlier context.
- **Resume:** reads the handoff file first, verifies the workspace, then continues from "Immediate Next Steps".

## Repository layout

```text
.
├── skills/session-usage-handoff/skill.md   # the skill (canonical)
├── skills.md                               # original file, kept unchanged for reference
├── scripts/validate.py                     # lightweight checks
├── .github/workflows/validate.yml          # runs the checks on push / PR
├── GITHUB_REQUIREMENTS.md                  # publication requirements
├── CONTRIBUTING.md
└── .gitignore
```

> `skills.md` is the original, pre-restructuring version. Use `skills/session-usage-handoff/skill.md`, which has small consistency fixes (aligned thresholds and progress-file names).

## Prerequisites

- An AI agent host that can load skills from Markdown files with YAML front matter (`name`, `description`).
- Optional: file-write tools, so the agent can save the handoff file directly. Without them, the skill outputs a copy-pasteable Markdown block.
- Python 3 to run `scripts/validate.py` (development only).

Compatibility with specific hosts has **not** been verified. Check your host's skill-loading documentation for the expected folder and file name. Some hosts expect `SKILL.md` rather than `skill.md`.

## Installation

Copy or reference the `skills/session-usage-handoff/` directory in the location your agent host reads skills from:

```bash
git clone <your-repo-url>
cp -r <your-repo>/skills/session-usage-handoff <your-agent-skills-dir>/
```

## Usage

Example prompts that should activate the skill:

- "How much usage do I have left?"
- "Checkpoint our work into PROGRESS.md before we run out of tokens."
- "Resume from PROGRESS.md."

Typical workflow: the agent checks usage, labels it Exact or Estimated, saves the checkpoint when Caution or Critical, and in the next session reads `PROGRESS.md` and executes its first next step.

## When not to use

- Short tasks with plenty of budget and no need for continuity.
- When you need exact billing figures that the host does not expose. The skill estimates and asks you for the number.

## Limitations

- Most chat hosts hide quotas from the model, so usage is usually an estimate.
- Behavior depends on the host honoring the skill's activation description.

## Validation

```bash
python scripts/validate.py
```

Checks front matter, code fences, relative links, and common secret patterns. The same checks run in GitHub Actions.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Released under the MIT License. See [LICENSE](LICENSE).

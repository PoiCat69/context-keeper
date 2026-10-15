# Contributing

Thanks for helping improve this skill.

## Workflow

1. Fork the repository and create a branch, e.g. `feat/short-description` or `fix/short-description`.
2. Edit `skills/session-usage-handoff/skill.md` (and docs as needed).
3. Run `python scripts/validate.py` and fix any failures.
4. Commit with [Conventional Commits](https://www.conventionalcommits.org/) (`docs:`, `fix:`, `feat:`, `chore:`).
5. Open a pull request describing what changed, why, and your validation results.

## Standards

- Keep `name` (lowercase, hyphen-separated, matching the directory) and `description` in the front matter. The description must say what the skill does and when to use it.
- Keep instructions actionable, with no contradictions or duplicated rules. If you change a threshold or file name, update every mention.
- Distinguish exact metrics from estimates. Never instruct the agent to invent unavailable data.
- Do not claim host compatibility you have not tested.
- Use placeholders in examples. Never commit secrets, tokens, private URLs, or personal data.
- Do not force-push shared branches.

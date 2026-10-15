---
name: session-usage-handoff
description: Monitor remaining token/quota usage, proactively check usage budgets, and save, update, or resume project progress using a markdown handoff file (such as PROGRESS.md or HANDOFF.md) before limits run out. Use when the user asks to check usage left, monitor token/context budget, checkpoint work before tokens run out, update a progress markdown file, create a session handoff summary, or continue from a previous progress checkpoint.
---
# Session Usage & Progress Handoff

Maintain seamless continuity across coding and project sessions by checking remaining token/quota usage, proactively triggering checkpoints when limits run low, capturing the exact state of work into a structured Markdown file (`PROGRESS.md`), and cleanly restoring context after a reset.

## When to Use

- The user asks to check how much token budget, context window, or quota usage is left.
- A long or multi-step task is underway and the agent needs to verify whether enough usage remains before starting another heavy step.
- Token limits, context window space, or rate quotas are running low (e.g., less than 15-20% remaining) and work needs to be saved immediately.
- The user asks to checkpoint, pause, wrap up a session, or update a `.md` tracking file (`PROGRESS.md`, `HANDOFF.md`, `TODO.md`, or `STATE.md`).
- The user starts a new session or returns after a token reset and asks to resume from the saved `.md` file.

## Steps

### Mode 1: Checking Remaining Usage & Proactive Monitoring

Because different agent environments expose token and quota usage differently, check remaining usage using the highest-accuracy method available in the current environment:

1. **Direct Runtime / CLI / System Inspection (When Available):**
   - Check if the system context or tool outputs inject token/budget headers (e.g., `token_budget`, `remaining_tokens`, `context_window`, or API usage headers).
   - If running in a terminal/CLI agent environment with local state or status commands (e.g., usage logs, provider quota endpoints, or CLI status flags), inspect the local usage state if accessible.
2. **Context Window & Turn Heuristic (When Direct Metrics Are Hidden):**
   - If the platform does not expose exact billing/quota numbers to the model, estimate remaining context capacity based on session depth:
     - **Turn count & payload volume:** Count the number of back-and-forth turns, large file reads, and long code outputs generated so far.
     - **Warning signs:** Watch for context truncation, compacted history notices, rate-limit retry warnings, or user mentions of quota warnings.
3. **Report & Threshold Action:**
   - **Status Line:** Always display a concise usage banner at the top or bottom of checkpoints:
     `[Usage Check: ~X% remaining | Status: Safe / Caution / Critical]` (or state whether the value is Exact vs. Estimated from context load).
   - **Safe (greater than 30% remaining):** Continue working normally; briefly note the usage check if requested.
   - **Caution (15% to 30% remaining):** Finish only the current atomic sub-task, avoid starting new large file refactors, and recommend or update `PROGRESS.md`.
   - **Critical (less than 15% remaining or quota warning active):** Immediately halt new feature work and execute **Mode 2** to save state before cut-off.

---

### Mode 2: Saving and Updating Progress (Pre-Limit / Checkpoint)

1. **Prioritize Token Efficiency:** When usage is in the **Caution** or **Critical** zone, skip conversational filler completely. Spend remaining output tokens directly on writing or updating the `.md` file.
2. **Locate or Select the Target File:**
   - Check if a progress file already exists in the workspace (`PROGRESS.md`, `HANDOFF.md`, `STATUS.md`).
   - Default to `PROGRESS.md` in the project root if none exists.
   - Write or update the file directly on disk if file tools are available; otherwise, output a single copy-pasteable Markdown code block.
3. **Update State (Do Not Blindly Overwrite):**
   - Preserve the overarching project goal and architectural constraints from previous checkpoints.
   - Move newly finished items into **Completed Work**.
   - Record the exact stopping point in **Current Stopping Point** (specific file paths, function names, line numbers, uncommitted changes, or failing tests).
4. **Write the Structured Checkpoint:**

```markdown
# Project Progress & Handoff

**Last Updated:** YYYY-MM-DD HH:MM
**Usage / Budget Status:** [Exact metric if available, or Estimated Context Load: Low / Medium / High / Critical]
**Current Phase / Objective:** [1-2 sentence summary of the active goal]

## 1. Completed Work
- [x] [Completed item with key file paths or outcomes]

## 2. Current Stopping Point (In Progress)
- **Active File(s):** `path/to/file`
- **Exact State:** [What was just edited, what is half-finished, or what error/test is currently failing]
- **Unresolved Blockers / Bugs:** [Any edge cases or errors encountered right before stopping]

## 3. Immediate Next Steps (Resume Here)
1. [First concrete action to take when tokens reset]
2. [Second concrete action]
3. [Verification or test command to run]

## 4. Key Context & Decisions
- [Important architectural choices, constraints, or user preferences that a fresh session must not violate]

## 5. Quick Resume Prompt
> "Read `PROGRESS.md` and continue from Section 3 (Immediate Next Steps), starting with [Task 1]."
```

---

### Mode 3: Resuming After Token Reset

1. **Read the Checkpoint First:** Read `PROGRESS.md` (or the specified `.md` file) before scanning the rest of the codebase to save tokens in the new session.
2. **Verify Workspace State:** Check the files listed under **Current Stopping Point** to confirm whether the last session's edits were saved cleanly or cut off mid-edit.
3. **Acknowledge Briefly and Execute:** Confirm the current stopping point in 1-2 sentences, then immediately execute Item 1 under **Immediate Next Steps**.
4. **Keep the File Synced:** Update `PROGRESS.md` after completing major milestones or whenever the usage check enters the **Caution** zone.

## Gotchas

- **Hallucinating exact billing numbers:** Standard chat sandboxes often hide account-level billing quotas from the model's prompt context. Never invent a fake exact token count if no system metric is present. Explicitly label whether the check is based on a **System Metric** or an **Estimated Context Load** (based on turn count and file volume), and ask the user for their UI usage percentage if an exact threshold is needed.
- **Starting a huge task on low budget:** Before beginning a multi-file refactor, check the session depth. If the conversation already contains many large file dumps, proactively suggest updating `PROGRESS.md` and resetting first so the agent doesn't get cut off mid-edit.
- **Burning remaining tokens on explanation:** When usage is critical, output the updated `PROGRESS.md` immediately without long commentary.
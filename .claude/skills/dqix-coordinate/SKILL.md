---
name: dqix-coordinate
description: Coordinate an authorized DQIX matching team with native agent tools, including bounded crack/evolve experiments and promotion of shared findings. Use for Codex or other hosts without Claude's workflow runtime.
---

# Coordinate native DQIX agents

Read `$KIT/AGENTS.md`, `docs/WORKFLOW.md`, `docs/FLEET.md`, and
`docs/IMPROVEMENT_LOOP.md`. Resolve paths through `kitpaths.py`; state belongs outside the kit.
Run `python kit_update.py` at session start and every task finish/stop, rereading `RE-READ`
files. Coordinate updates to a shared checkout at a quiescent boundary; never update beneath
running scripts. Exit 3 means stop and report, with no stash/reset/discard.

Read `$KIT/docs/NATIVE_AGENTS.md` for the native coordination procedure, shared research
record, and bounded adaptations of `.claude/workflows/dqix-crack.js` and `dqix-evolve.js`.
Those JavaScript files require Claude's runtime; this skill does not make them executable
in another host or implement an autonomous background fleet.

Use only the host's available delegation, messaging, status, and stop tools. Delegate within
the user's authorized scope, model choices, concurrency and usage limits. If native delegation
is unavailable, work serially or report the limitation. Never substitute paid `claude -p`
workers for native agents without authorization. A maintenance or review request does not
restart a paused sprint, clear its stop flags, or authorize additional functions.

Before dispatch, resolve ownership, immutable input versions, distinct write paths, the exact
hypothesis or function, and its stopping condition. Return evidence paths and measured results,
not unsupported claims of MATCH. Reuse `dqix-hand-match` for implementation, the existing kit
gates for validation, and the normal staging/integration path for landing.

At handoff, preserve attempts, measure blockers, promote useful findings with their proof,
and send reusable changes upstream in the same session. No new claim while the kit's
freshness, promotion, or blocker checks hold. Keep gate matches, reviewed candidates,
landed bytes, and upstream merges separate in reports.

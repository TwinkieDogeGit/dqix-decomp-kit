---
name: dqix-coordinate
description: Coordinate an authorized DQIX matching team with native agent tools, including bounded crack/evolve experiments and promotion of shared findings. Use for Codex or other hosts without Claude's workflow runtime.
---

# Coordinate native DQIX agents

Read [AGENTS.md](../../../AGENTS.md), [WORKFLOW.md](../../../docs/WORKFLOW.md),
[FLEET.md](../../../docs/FLEET.md), and [IMPROVEMENT_LOOP.md](../../../docs/IMPROVEMENT_LOOP.md).
Resolve paths through `kitpaths.py`. Follow AGENTS.md's Take instructions for maintenance
and [rule 21](../../../AGENTS.md#hard-rules) before publishing a kit or decomp pull request.

Read [NATIVE_AGENTS.md](../../../docs/NATIVE_AGENTS.md) for the native coordination
procedure, shared research record, and bounded adaptations of
`.claude/workflows/dqix-crack.js` and `dqix-evolve.js`. Those JavaScript files require
Claude's runtime; this skill does not make them executable in another host or implement
an autonomous background fleet.

Use only the host's available delegation, messaging, status, and stop tools. Delegate within
the user's authorized scope, model choices, concurrency and usage limits. If native delegation
is unavailable, work serially or report the limitation. Never substitute paid `claude -p`
workers for native agents without authorization. A maintenance or review request does not
restart a paused sprint, clear its stop flags, or authorize additional functions.

Before dispatch, resolve ownership, input versions, distinct write paths, the exact
hypothesis or function, and its stopping condition. Return evidence paths and measured results.
Reuse `dqix-hand-match` for implementation and [WORKFLOW.md](../../../docs/WORKFLOW.md)
for the existing gates and landing procedure.

At handoff, follow [IMPROVEMENT_LOOP.md](../../../docs/IMPROVEMENT_LOOP.md) and
[CONTRIBUTING.md](../../../docs/CONTRIBUTING.md). Keep gate matches, landed bytes,
and upstream merges separate in reports.

# Native agent coordination

This is a coordinator-operated adaptation of the Claude dynamic workflows for Codex and
other hosts with native subagents. It retains the kit's gates and knowledge loop. It is not
a replacement for `pull_all.sh`, a background scheduler, or a port of Claude's JavaScript
workflow runtime. Read `AGENTS.md`, `WORKFLOW.md`, `FLEET.md`, and `IMPROVEMENT_LOOP.md`
first; their pipeline rules still apply. Start with `dqix-coordinate`.

## Session and ownership

Record the authorized scope, model/effort choices, concurrency, budget limits and stop state
in `$SP/OPEN_WORK.md`. Existing stop instructions take precedence over a skill's example
operating mode. Do not copy the historical fleet settings or model spending permissions in
`dqix-plan` into a new host.
Examples that launch background sweeps or automatic resume are not instructions to run them
during an audit or a user pause. Current hard rules override historical recipe examples.

Run `python kit_update.py` at start and every task finish/stop. For a shared checkout, a
designated coordinator serializes these checks with users of that checkout and drains active
scripts before an update. Record deferred checks and complete them at that boundary; do not
declare them done merely because another session previously checked. Read all `RE-READ`
instructions before continuing. On exit 3, stop and tell the user; never stash/reset/discard.
Do not overwrite an immutable reference or mix proofs across kit/repo/compiler versions.

On Windows, verify `python`, `ninja`, and `bash` in the process environment. Use Git Bash,
not the WSL `bash.exe` in System32. For Python subprocess timeout tests, prefer Git's actual
`usr/bin/bash.exe` over its `bin/bash.exe` launcher: killing the launcher may leave the child
holding output pipes open. Keep these path settings process-local.

Before each new function, reconcile current upstream ownership intervals and source, open
decomp PRs, open kit issues, and local claims. `claim.py` only arbitrates its own state;
independent state directories are not a global reservation service. One coordinator owns
the team's public batch issue and the mapping from addresses to workers. Teams can propose
their own next targets; dispatch needs a completed reservation check, not the coordinator
to solve or choose every function personally.

Keep one open kit issue listing the active batch, not an issue per difficult function.
Close it at decomp PR creation with `PR: ZevyaDev/dqix-decomp#N`; the open PR then reserves
its functions. If a subset is submitted, close that issue and create one successor batch
issue for the still-active remainder. If stopping without a PR, close and release the batch.
Recheck ownership before any later retry.

## Roles and evidence flow

The coordinator owns reservations, updates, stop/usage decisions and the final publication.
Delegate bounded queue preparation, blocker triage, and evidence indexing when authorized;
these do not all need to wait on the coordinator's implementation work.

Implementation agents own different functions. Same-function agents are a deliberate crack
experiment with distinct hypotheses under one claim, not independent claims. Each agent gets
an immutable starting source hash and its own writable candidate directory. Shared header
changes are proposals until the designated owner applies and validates them.

Independent reviewers consume frozen candidates and check semantics, declarations, actual
callee contracts, literal/relocation evidence and the real gate results. Review can occur
in parallel per team. The required review count follows the project's current agreement;
this adaptation does not reduce it. Freeze approved source and dependency hashes before
staging; edits invalidate affected reviews.

One integrator owns the shared `staging/` queue and wave lock. Land through `finish_wave.sh`
or `integrate_fast.sh` in the dedicated integration worktree. Other agents can keep gating
and preparing evidence while it runs. Separate per-team review does not require concurrent
integrations into the same worktree. A match is landed only after the resulting commit passes
`ninja check`, plus the repository's other applicable checks.
Before first use or recovery, verify the integration worktree's compiler/build setup, source
branch and publication destination. Do not transplant an old reset/cleanup command to the
main checkout; preserve state and follow the current integration recovery procedure.

Every result carries:

- module/address/size, reservation, owner, kit/repo/compiler identities;
- candidate path and SHA-256, dependency identities, prior source hash;
- precise transformation, gate command/log, measured residue and byte difference;
- semantic findings and uncertainties, reviewer verdicts, next experiment if unresolved;
- promotion destination and evidence, kit PR, staging/landing commit and decomp PR when present.

The source hash binds review to the actual submitted file. A result message is an index to
evidence, not a substitute for it. Managers keep `OPEN_WORK.md` current while work is live.
Workers write per-worker reports; a designated owner merges shared ledgers and boards so
concurrent agents cannot overwrite each other's results.

Refill an available slot with authorized, reserved work while reviewed results queue. Do
not wait for an entire batch to finish just because one worker succeeded. Still honor
freshness, promotion and blocker holds from the kit; resolve their causes rather than
bypassing them or opening a private state directory to claim around them.

## Research records for difficult functions

Use `blocker.py` and `blockercheck.py --verbose` to measure and rank blocker families.
Select a representative by expected reusable benefit and cost. Preserve the best source,
other useful residue shapes, and failed experiments before changing the owner or model.

Keep a concise board under `$SP/handwork/`, linked from `OPEN_WORK.md`. Use the kit's
`<addr>_board.md` convention when adapting a single-function evolve run. Include:

- the research question, representative address and related family members;
- exact baseline source/dependency hashes and measured `RESIDUE`/score;
- owner, experiment IDs and hypotheses, with separate candidate paths;
- one measured result per experiment: source hash, exact change, log, score/signature;
- hypotheses ruled out, winner/stop state, next bounded experiment and remaining uncertainty;
- the generalized finding, proof, delivery check and upstream PR when available.

A score that stopped improving is a stalled approach, not proof that a function is impossible.
Honor `gatelog.py` STOP for that run. A follow-up is a distinct, authorized experiment with
new evidence or a new hypothesis and an explicit cap, not a reset of counters to repeat the
same search. No automatic permanent blacklist or claim of unmatchability.

Public reservation issues are not a backlog of every hard address: listing an address in an
open kit issue reserves it. Keep inactive research locally and submit useful, substantiated
dead ends to the kit. Use upstream tool issues for actionable tool defects when appropriate,
without creating a second function-reservation backlog.

## Bounded crack and evolve

Read `.claude/workflows/dqix-crack.js` or `dqix-evolve.js` for the selected mode. Map their
agent/parallel/phase operations to the native tools actually exposed by the host; do not
invoke their JavaScript through Node and expect Claude's globals to exist.

For a **crack**, measure the baseline with the real gate, then assign a small authorized
round of different source hypotheses to isolated copies. Pass the relevant recipe excerpts,
dead ends, ABI/layout evidence, baseline and concise board digest. Between experiments,
check for a verified winner or stop. A reported MATCH stops new experiments; the coordinator
regates it and obtains independent review before treating it as accepted. If rejected,
record why before continuing within the remaining budget.

For **evolve**, score candidates through `pad/evo_score.py`. Keep a bounded population with
distinct residue signatures; do not retain only the lowest byte count. Plan directed edits
and optional crossover from named parent hashes, and rescore children yourself instead of
trusting reported fitness. The Claude defaults (population 5, width 2, exploration 0,
crossover 1, at most 6 generations, plateau 3) are an example, not spending authorization.
Fitness zero is a candidate for semantic review and normal gating/integration, not proof
of a valid landing. Observe all forbidden-source and compiler-setting rules.

Before dispatch, set finite experiment/compile and wall-time limits, plus the user's model
and usage limits. Record actual model, effort and timing for comparisons. `evocap.py` reads
Claude session accounting; it does not cap native Codex work. Use the host's real usage
telemetry for its limits, and report unavailable cost as unknown, not zero. If a required
usage threshold cannot be checked, stop new dispatch until resolved. Never infer a cheap
run from missing Claude logs.

A stronger model can provide a bounded diagnosis of one family, using the same compact
evidence and a specific question. Use it only within the user's model/budget authorization.
The implementer must test the suggested source change; a persuasive explanation is not
a gate result. This permits a small amount of expensive reasoning to help multiple workers.

## Feed the shared kit

Each result goes through `IMPROVEMENT_LOOP.md`: measure, record, promote, enforce, deliver.
Mirror required outcome records from isolated worker states into the designated shared
state under a single writer, preserving provenance and avoiding duplicate rows. Otherwise
the coordinator's `levercheck.py` and `blockercheck.py` cannot see those workers' findings.
Do not add incompatible fields to the kit's TSV formats; put extra provenance in sidecars.

- MATCH: concrete transformation in `wlog/levers.tsv`, then an automatic rule/repair or a
  concise address-citing `worker_src/core.md` rule with the required proof.
- Miss: measured `blocker.py` record, a handoff for the next attempt, and a substantiated
  `worker_src/deadends.md` row when real experiments ruled forms out.
- Tool fault: fix the shared implementation with a reproducing regression; do not leave a
  private workaround as the only repair.
- Genuine non-reusable result: reasoned decline in the supported ledger. Do not decline
  merely to clear a hold or because promotion takes time.

Run `build_worker_docs.py` after recipe changes and check that the rule reaches the built
worker document. Check the next function's `recipe_select.py` output when changing its
delivery. Run the tests required by the changed files. Check upstream for existing fixes,
then submit reusable changes to the kit in the same session with their proof.

At stop, preserve unfinished research and evidence, release or transfer reservations,
complete the serialized update/reread checks, and report attempted, gate-matched, reviewed,
landed and upstream-merged totals separately. User pauses and budget stops apply to native
agents as well as shell workers; stopping a shell fleet alone does not stop native agents.

## Validation boundary

This procedure can be reviewed and its portable skill mirrored without launching any model
workers. That checks packaging and instructions, not live fleet throughput or native usage
accounting. Record a later authorized pilot separately; never present documentation tests
as measured productivity improvements.

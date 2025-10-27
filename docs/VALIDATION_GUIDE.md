# Narrative Validator Guide — Codewords, Conditions, and Effects

This guide describes how validators should use the **Codeword/Flag Registry** to audit narrative sections
and choices for logical consistency and determinism.

## Inputs
- **/schemas/state/codeword_registry.schema.json** — canonical set of codewords/flags.
- **project_state.schema.json (narrative shard)** — sections, choices, conditions, and effects.
- Optional: **playback_transcript.schema.json** — to replay paths and verify effects during real sessions.

## Core Checks

1. **Referential Integrity**
   - Every `choice.conditions[]` and `section.codewords[]` must reference a known codeword `entries[*].id`.
   - `choice.effects[]` must reference known codewords and be compatible with their `kind`.
   - Conflicts: choices must not set two codewords that appear in `conflicts` within the same step.

2. **Type Compatibility**
   - For `kind=boolean`, effects must only set/unset.
   - For `kind=counter`, effects must increment/decrement within allowed bounds (if specified by policy).
   - For `kind=enum`, effects must set a value found in `enum_values`.

3. **Implication Closure**
   - When a codeword is set, automatically apply `implies[]` to the working set for subsequent condition checks.
   - Detect cycles in implication graph and report as `warning`/`error` depending on policy.

4. **Default State**
   - Validate that paths from the start section remain executable from the `default_state` assignment of all codewords.
   - Optional: compute minimal assignment needed to reach each section (reachability with guards).

5. **Effects Idempotency**
   - Replaying the same path twice with identical inputs must result in the same final codeword state (determinism).
   - Report any non-deterministic effects (e.g., random increments without seed control).

6. **Dead Ends & Dangling Conditions**
   - Any `conditions[]` that are never satisfiable under registry rules should be flagged.
   - Orphaned `effects[]` that never influence any downstream `conditions[]` can be flagged as informational.

## Suggested Validator Output
Emit an **Event.Validation.Report** with `scope=state` and structured `issues[]`:
- `code`: e.g., `CODEWORD.UNKNOWN`, `CONDITION.UNSATISFIABLE`, `EFFECT.TYPE_MISMATCH`, `IMPLIES.CYCLE`.
- `severity`: `error` | `warning` | `info`.
- `path`: JSON Pointer to the offending field in the narrative shard.
- `hint`: remediation suggestion.

## Example — Minimal Registry

```json
{
  "entries": [
    {"id": "CW.ACCESS.ALPHA", "scope":"global", "kind":"boolean", "default_state": false, "implies": ["CW.ACCESS.BASIC"]},
    {"id": "CW.ACCESS.BASIC", "scope":"global", "kind":"boolean", "default_state": true}
  ]
}
```

A choice requiring `CW.ACCESS.ALPHA` is satisfiable if either it is set explicitly by a prior effect, or via an effect that sets `ALPHA` (which also implies `BASIC`).

## Graph-Level Checks (Optional but Recommended)
- Build a graph of sections with guarded edges; compute reachability given registry defaults.
- Report unreachable sections (`GRAPH.UNREACHABLE`) and cycles with monotonic counters that never terminate (`GRAPH.NON_TERMINATING`).

---

For determinism audits during runtime, compare a **playback_transcript** against expected edges and codeword changes; any divergence should emit `Event.Playback.SyncDrift` with `drift_reason`, and a follow-up **Event.Validation.Report** can contain machine-parsable issue details.

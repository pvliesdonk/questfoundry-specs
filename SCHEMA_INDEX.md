# Questfoundry Schema Index (v1)

Domain: <https://questfoundry.liesdonk.nl/v1>

This index lists the canonical JSON Schemas, their purpose, producers/consumers, and typical file locations inside a repo.
All `$id` fields use absolute URLs under the domain above so `$ref`s are resolvable out of tree.

## Conventions
- **Cold SoT**: canonical project state (deterministic, reproducible).
- **Hot SoT**: runtime events/commands/policies.
- All timestamps are RFC3339. IDs use ULIDs. Language tags are BCP47.
- Checksums are **sha256** and content-addressable.

## Schemas

### /schemas/defs
- **common.json** — Reusable types: `ulid`, `semver`, `rfc3339`, `iso_lang`, `checksum`, `toolchain`, `provenance`.
  - Producers: all.
  - Consumers: all.
  - Lower-layer link: determinism and integrity anchors for Cold SoT snapshots and Hot SoT traffic.

### /protocol/schemas/defs
- **envelope.json** — Base envelope for all messages (Event/Command). Adds `continuity_tags` for correlation.
- **command_envelope.json** — Envelope specialization for commands (adds `command_id` for idempotency).

### /protocol/schemas/commands
- **Command.Playback.Start.schema.json** — Start narrator/player at a section with policy mode and optional seed.
- **Command.Playback.Choose.schema.json** — Choose an option and advance.
- **Command.Playback.Jump.schema.json** — Jump to a section (debug/deterministic/recovery).
- **Command.Governance.RequestWaiver.schema.json** — Request a waiver (scope + optional expiry).
- **Command.Governance.RequestSignOff.schema.json** — Request sign-off on scope.
- **Command.Release.Go.schema.json** — Initiate a release (target semver + channel).

### /protocol/schemas/events
- **Event.Validation.Report.schema.json** — Validator outcome with structured issues.
  - (Add’l Event.* schemas should mirror the command/release/governance and playback flows with the same patterns.)

### /schemas/manifest
- **project_manifest.schema.json** — Cold SoT snapshot manifest enumerating artifacts with checksums; links to narrative/codex ids.
  - Producers: release pipeline, snapshot command.
  - Consumers: orchestrator, validators, distribution tools.

### /schemas/policy
- **player_narrator_policy.schema.json** — Hot-side runtime policy for narrator/player (mode, improv, safety, logging, constraints).
  - Producers: orchestrator / config.
  - Consumers: narrator/player agent.

### /protocol/schemas/feedback
- **Feedback.SectionRewrite.Request.schema.json** — Guided rewrite request (section-focused) with constraints and TTL.
- **Feedback.SectionRewrite.Response.schema.json** — Reply including `result_path`, delta metrics, and any violations.
- **feedback.schema.json** — oneOf union of the two above (handy for validators).

### /schemas/state
- **codeword_registry.schema.json** — Canonical registry for codewords/flags, including type (boolean/counter/enum), scope,
  defaults, conflicts, and implication rules.

### /schemas/canon
- **claim_registry.schema.json** — Structured claims about the world with sources, confidence, counters, and merge policy
  so tools can reason about canon vs disputes.

### /schemas/art
- **render_record.schema.json** — Rich render provenance (prompts, model hash, engine params). Intended to be referenced
  from `renders_index` or `artifacts` entries.

### /schemas/audio
- **audio_plan.schema.json** — Timing-focused plan for music/SFX aligned to narrative sections; supports loop regions and ducking.

### /protocol/schemas/playback
- **playback_transcript.schema.json** — Deterministic session log (section→choice→section) with codeword diffs and policy snapshots.

---

## File Layout Suggestions
- `/schemas` — Long-lived, versioned schemas (Cold SoT, policy, manifest, defs).
- `/protocol` — Wire-level contracts for runtime (envelopes, commands, events).

## Backwards Compatibility Notes
- `checksum.algo` is currently restricted to `sha256`. Expansions are a major or controlled minor with negotiation.
- `toolchain.seed` is required; per-stage overrides should still record the global seed for reproducibility.

---

*Keep this index updated when adding new Event.* or Command.*schemas; maintain 1:1 parity between governance flows (request/response) and their event mirrors.*

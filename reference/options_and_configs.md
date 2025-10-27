
# Options & Configs

## Player‑Narrator Policy (`state/player_narrator.policy.json`)
- `mode`: `release` | `debug` | `deterministic`
- `allow_transient_improv`: bool
- `feedback_channel`: bool
- `max_deviation_radius`: float

## Genre Templates (`reference/genre_templates/*.json`)
- Defaults for size, tone, setting, structure.

## Override Cascade
1) CLI flags → 2) env vars → 3) policy files → 4) hard-coded defaults.

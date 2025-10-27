
# Questfoundry — Iteration 3 Checklist (Authoritative)
_Last updated: 2025-10-27 05:20:01Z UTC_

## Status Summary
- Layers **0–5** implemented; **Layer 6** concept in `concepts/`.
- Protocol **harmonized**; goldens validate; docs refreshed; PNG present.

## A) Protocol & Validation
- [ ] Cross-ref validator (choices→sections; assets→media indices)
- [ ] Media indices schema (rights & accessibility)
- [ ] SBOM/hash manifest in packager

## B) Quickstart End-to-End
- [ ] Wire decider/router/spawner (one-shot run)
- [ ] Packager hookup (zip + `manifest.json` hashes)
- [ ] CLI flags (`--pn-mode`, `--genre`, `--size`, `--no-art`)
- [x] Progress teasers (non-spoiler)

## C) Governance & Ops
- [ ] Auto-spawn policy in Orchestrator
- [ ] Sign-off checklist templates per artifact
- [ ] Waiver TTL sweep/report

## D) Templates & Docs
- [ ] Genre templates pack (+6)
- [x] Docs refreshed (Quickstart, Protocol, Architecture + PNG)

## CI & Hygiene
- [ ] CI workflow: run validator + cross-refs on PRs
- [ ] Release packaging rules (no `/bus/`, include `manifest.json`, include PNG)

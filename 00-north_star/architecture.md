
# Architecture Overview

- **Hot SoT:** ephemeral event bus; agents subscribe/emit; PN feedback only in debug.
- **Cold SoT:** canonical project files (JSON + artifacts); reproducible builds.
- **Orchestrator:** policy brain; triggers governance; manages PN mode; snapshots.
- **Agents:** Research → Plotter → Lore → Codex → Art/Audio → Validator → Packager.
- **Governance:** queries, sign‑offs, waivers; router gates releases.
- **Determinism:** given Cold SoT + seeds + tool versions, release reproduces identically.

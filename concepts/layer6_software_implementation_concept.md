# QuestFoundry Toolkit — System & CLI Design Brief

*(Architect / Designer Edition – 2025-10)*

---

## 1. Purpose

QuestFoundry is a **modular, strictly-typed Python library** for creating and orchestrating AI-assisted, deterministic creative projects — narrative, art, and audio — plus a unified **CLI/UI** for human interaction, governance, and publication.

It treats every creative process as a **set of cooperating AI agents** governed by protocol contracts, producing reproducible Cold Sources of Truth (Cold SoT) and ephemeral Hot SoTs for iteration.

---

## 2. Architectural Core

### Library composition

```
questfoundry/
  ai/            → adapters & providers (LLM, image, audio)
  roles/         → creative & deterministic agents
  orchestrator/  → policy, routing, feedback loops
  protocol/      → Pydantic models, schemas, validator
  cli/           → qf command family (Typer/Click)
  state/         → Cold SoT snapshots, manifest, SBOM
```

### Typed interfaces

| Interface      | Purpose                              | Example Providers                                             |
| -------------- | ------------------------------------ | ------------------------------------------------------------- |
| `LLMAdapter`   | structured generation (schema-bound) | OpenAI GPT-5, Gemini 2.5 Pro, Ollama Llama 3                  |
| `ImageAdapter` | prompt→image                         | diffusers SDXL, A1111/Comfy, Imagen 4, 4o-image, Bedrock SDXL |
| `AudioAdapter` | cue→audio                            | Gemini MusicLM, Bedrock TTS, local TTS/music engines          |

Adapters advertise capabilities (`caps()`), rate limits (`limits()`), and determinism levels; the **Orchestrator** chooses the best provider chain via policy and fallback logic.

---

## 3. Roles and Agents (all AI-backed)

| Role                               | Core Function                 | Backed By           |
| ---------------------------------- | ----------------------------- | ------------------- |
| **Researcher**                     | factual background, citations | LLM                 |
| **Plotter**                        | act/beat structure            | LLM                 |
| **Lore Weaver**                    | prose draft                   | LLM                 |
| **Codex Curator**                  | consistency, canon merge      | LLM                 |
| **Art Director & Vision Designer** | briefs, composition specs     | LLM                 |
| **Renderer**                       | image synthesis               | Image Adapter       |
| **Audio Designer**                 | cue sheets                    | LLM                 |
| **Audio Renderer**                 | TTS / composition             | Audio Adapter       |
| **Validator**                      | deterministic checks          | deterministic       |
| **Packager**                       | manifest, SBOM                | deterministic       |
| **Book Binder**                    | manuscript (MD → EPUB/PDF)    | deterministic       |
| **Wiki Exporter**                  | codex → wiki tree             | deterministic       |
| **Player Narrator**                | playback runtime              | AI or deterministic |

All creative roles are AI-backed and schema-validated; deterministic roles handle publishing and QA.

---

## 4. Orchestrator & Feedback Loops

### Feedback cycles

| Loop      | Chain                                      | Purpose               |
| --------- | ------------------------------------------ | --------------------- |
| **lore**  | plot → lore → codex → validate             | prose iteration       |
| **art**   | artdir → vision → renderer → validate      | visual iteration      |
| **audio** | audio designer → audio renderer → validate | sound iteration       |
| **full**  | all creative roles                         | full creative refresh |

Orchestrator manages:

* cycle boundaries (open/snapshot),
* per-role budgets,
* rate limits,
* governance events (sign-off, waiver, query).

---

## 5. Provider Ecosystem (2025-10)

| Domain    | Provider                         | Library / SDK             | Determinism |
| --------- | -------------------------------- | ------------------------- | ----------- |
| **LLM**   | OpenAI GPT-5 / 4.1               | `openai`                  | best-effort |
|           | Google Gemini 2.5 Pro            | `google-generativeai`     | best-effort |
|           | AWS Bedrock Claude/Titan         | `boto3 bedrock-runtime`   | best-effort |
|           | Ollama (Llama3 / Qwen / Mistral) | REST API                  | strict      |
| **Image** | SD/SDXL (diffusers)              | `diffusers`               | strict      |
|           | AUTOMATIC1111 / ComfyUI          | HTTP API                  | strict      |
|           | Google Imagen 4                  | `google-cloud-aiplatform` | best-effort |
|           | OpenAI 4o-image                  | `openai`                  | best-effort |
|           | Bedrock SDXL / Titan Image G1 v2 | `boto3 bedrock-runtime`   | best-effort |
| **Audio** | Gemini MusicLM                   | `google-generativeai`     | best-effort |
|           | Bedrock TTS / Local TTS          | `boto3 bedrock-runtime` / custom | strict      |

All adapters use **provider-native SDKs** for performance, authentication, and billing.
Fallbacks and rate-limit guards are automatic.

---

## 6. Determinism & Provenance

* **Strict determinism**: SD/SDXL renders, Ollama LLMs, local TTS.
* **Best-effort**: hosted LLM/image/audio providers.
* **Provenance hash**: model ID + version + prompt + seed + tool IDs + inputs.
* **Manifest.json**: full record of seeds, versions, hashes, budgets, rights.

Validator enforces deterministic reproducibility for release builds.

---

## 7. Exporters

### Book Binder

* Inputs: validated Cold SoT narrative + media indices.
* Outputs:

  * `manuscript.md`
  * `manuscript.epub`
  * `manuscript.pdf`
* Deterministic conversion (Pandoc / WeasyPrint).
* Rights & accessibility required (alt-text, captions, licenses).

### Wiki Exporter

* Inputs: Codex shards + entity/faction/location taxonomy.
* Output: `docs/wiki/…` (MkDocs-ready).
* Options: `--split-by` taxonomy, `--include-graphs` (Mermaid), auto-crosslinks.

---

## 8. Player Narrator (PN) — Four Operating Modes

| Mode                         | AI? | Feedback                      | Delivery                               |
| ---------------------------- | --- | ----------------------------- | -------------------------------------- |
| **AI-Backed Release**        | Yes | No                            | Toolkit (`qf pn --mode release`)       |
| **AI-Backed Debug**          | Yes | Yes (feedback → orchestrator) | Toolkit (`qf pn --mode debug`)         |
| **Deterministic Toolkit**    | No  | No                            | Toolkit (`qf pn --mode deterministic`) |
| **Deterministic Standalone** | No  | No                            | Separate distributable player app      |

All PN variants read the same manifest and policy; only Debug routes live feedback to the orchestrator.

---

## 9. Command-Line Interface

### Intent groups

**Fast Lane**

```
qf quickstart [--play] [--offline] [--deterministic]
```

**Authoring (First-Class Roles)**

```
qf research | plot | lore | codex | art | render | audio
qf validate | package | binder | wiki | pn
```

**Orchestration**

```
qf loop (lore|art|audio|full)
qf decide (inbox|respond|signoff|waive)
qf status | config | cache
```

### Examples

Quickstart (no PN by default):

```bash
qf quickstart --language en --genre space_opera --size medium --snapshot
```

Targeted authoring:

```bash
qf plot --acts 3 --beats 24 --model gpt5 --snapshot
qf render --scene SCN-013 --provider sdxl_local --seed 42 --quality high
qf audio --scene SCN-013 --kind music --mood tense
```

Book binder:

```bash
qf binder --format all --title "Ecliptic Spire" --cover art/cover.png
```

Wiki export:

```bash
qf wiki export --format mkdocs --split-by entity --include-graphs
```

Feedback loops:

```bash
qf loop art --scenes SCN-010,SCN-013 --open-cycle --snapshot
qf loop audio --scenes SCN-013 --open-cycle --snapshot
```

Player Narrator:

```bash
qf pn --project dist/story.zip --mode release
qf pn --project dist/story.zip --mode debug
qf pn --project dist/story.zip --mode deterministic
```

---

## 10. Governance & Compliance

* Every creative output carries:

  * `rights.license`
  * `rights.source`
  * `rights.scope`
  * `accessibility.alt_text` / `captions`
* Missing or invalid → **validator error**.
* Stakeholder interactions (`Event.Query/SignOff/Waiver`) available in CLI (`qf decide`).

---

## 11. Determinism & Rate-Limit Policy Summary

* **Central rate limiter** per provider (token-bucket + backoff).
* **Per-role budgets** for tokens/images/audio clips per cycle.
* **Automatic rerouting** on provider 429/5xx or capability mismatch.
* **Strict determinism gate** for release and binder export.

---

## 12. Deliverables / Next Steps

1. **Implement strict-typed library skeleton** (interfaces, adapters, orchestrator).
2. **CLI scaffold** with full command family.
3. **Policy config template** (`state/ai_policy.yaml`) with routing, budgets, rate limits.
4. **Provider adapters** (OpenAI, Google, Bedrock, Ollama, SDXL, A1111/Comfy, Imagen 4).
5. **Validator + manifest** finalized for reproducibility.
6. **Binder** and **Wiki exporter** modules.
7. **Standalone PN** packaging pipeline.

---

### Outcome

When complete, the system delivers:

* A reproducible, AI-driven creative pipeline.
* Modular roles, each a specialist model.
* Deterministic builds (manifest-pinned).
* Optional live AI playback or fully standalone deterministic play.
* Clear governance, rights, and accessibility guarantees.

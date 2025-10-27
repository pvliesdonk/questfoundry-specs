
# Layer 6 — Software Implementation with AI Assistance (Concept)

Status: non‑normative outline; implements the process, not just narrative.

## 1) Two Temperatures
Hot Core (bus, live agents, PN improv) and Cold Frame (SoT, provenance).

## 2) Multi‑Agent Environment
Orchestrator, Research, Plotter, Lore, Codex, Art/Audio, Validator, PN, Governance.

## 3) Protocol as Nervous System
Schemas become message contracts; creativity is observable & replayable.

## 4) Runtime Phases
Bootstrap → Production Loop → Release/Play.

## 5) Human–AI Hybridity
Roles can be AI, human, or hybrid; contracts matter, not the actor.

## 6) Persistence & Reproducibility
Cold SoT immutable graph; Hot SoT ephemeral streams; seeds & versions stored.

## 7) Interfaces
APIs (REST/gRPC), events, and a UI for creators and players.

## 8) Ops Intelligence
Orchestrator as AI product manager (scheduling, audits, summaries).

## 9) Deployment Visions (Expanded)

### A. Python‑only Library + Thin CLI
- **Package:** `questfoundry` with modules for orchestrator, protocol, agents, validator, PN.
- **CLI:** `qf` entrypoint (quickstart, validate, package, play).
- **Determinism:** seeds + versions recorded by packager; validator checks.
- **When to choose:** local dev, research, simple pipelines.

### B. LangChain‑based Orchestration
- **Graph:** roles as chains; Orchestrator as a LangGraph controlling flow.
- **Memory/Tools:** LC tool calling for research; memory for Hot SoT context.
- **Persistence:** adapters to Cold SoT schema for outputs.
- **When to choose:** rapid prototyping on LangChain stacks.

### C. MCP Server (Model Context Protocol)
- **Server:** `qf-mcp` exposes tools like `orchestrator.open_cycle`, `validator.check`, `packager.build`.
- **Clients:** IDEs/assistants invoke tools; schemas drive typed inputs/outputs.
- **When to choose:** human-in-the-loop workflows via assistants.

### D. Web‑based Studio (Service Mesh)
- **Services:** Orchestrator, Agents, Validator, PN as microservices; event bus as Hot SoT.
- **UI:** Creator Console + Player Portal.
- **Storage:** S3/Git/DB (Cold SoT); Redis/NATS/Kafka (Hot SoT).
- **When to choose:** collaboration, observability, distribution.

## 10) Outcome
A creative operating system: narrative is output; **process** is a first‑class artifact.

# Determinism Contract (Normative)

**Requirement.** Release mode must be reproducible given Cold SoT + seeds + tool versions + inputs + environment pins.

**Checklist (validator-enforced)**
1. Seeds are fixed and recorded per generation step.
2. Tool versions are pinned (LLMs, renderers, validators, routers).
3. Inputs are captured (prompts, configs, policies).
4. Environment pins are recorded (OS, drivers, fonts, locale).

**Verification.** Validator emits a snapshot manifest and compares hashes for reproducibility.

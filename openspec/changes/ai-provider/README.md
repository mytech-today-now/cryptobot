# AI Provider Layer — Configurable AI Backend for Crypto Trading Bot Platform

## Change ID
`AI-PROVIDER-001`

## Status
📝 **Draft** — Ready for review and implementation

## Quick Links
- [Proposal](./proposal.md) — Problem statement and proposed solution
- [Design](./design.md) — Architecture, flow diagrams, and API signatures
- [Deltas](./deltas.md) — Files to create and modify
- [Tasks](./tasks.md) — Phased implementation task breakdown
- [SUMMARY](./SUMMARY.md) — Bead task series overview
- **Specs**
  - [Provider Abstraction Layer](./specs/provider-abstraction-layer.md)
  - [Configure Subcommand](./specs/configure-subcommand.md)
  - [GUI AI Providers Menu](./specs/gui-menu.md)
  - [.env Integration](./specs/env-integration.md)
  - [Provider Extensibility](./specs/provider-extensibility.md)
- **Tests**
  - [Configure Command Tests](./tests/configure-command.md)
  - [Provider Resolution Tests](./tests/provider-resolution.md)
  - [Secret Masking Tests](./tests/secret-masking.md)
  - [GUI Menu Tests](./tests/gui-menu.md)

---

## Overview

Refactor the Crypto Trading Bot Platform so all AI-powered commands route through a shared provider abstraction instead of a single hard-coded integration. Introduce a dual-mode `configure` subcommand (direct flags for scripting + interactive guided wizard) and an **🤖 AI Providers** menu item in the `--gui` loop. Credentials and active-profile state are stored exclusively in the repo-root `.env` file.

---

## Problem

### Current Issues
- **Hard-coded provider** — AI-powered commands depend on a single integration; switching backends requires source edits
- **No structured configuration** — Users set `.env` keys manually with no guided workflow or validation
- **No multi-profile support** — Cannot maintain separate credentials per client, project, or environment
- **No GUI visibility** — Provider status is not surfaced in the `--gui` interactive loop
- **Fragile cross-runtime state** — Python and TypeScript files may each read credentials differently, risking drift

### Impact
- Non-technical users cannot set up AI providers without developer assistance
- Switching providers mid-project requires manual `.env` edits and risks broken state
- Community/self-hosted providers (Ollama, LocalAI, vLLM) cannot be registered without code changes
- CI/CD pipelines have no scripting-friendly flag API for provider configuration

---

## Solution

### Theme 1 — Provider Abstraction Layer
Route all AI commands through `resolve_active_provider()` (Python) / `resolveActiveProvider()` (TypeScript). Neither helper duplicates business logic; both read `AI_ACTIVE_PROVIDER` and `AI_ACTIVE_PROFILE` from `.env`.

### Theme 2 — Provider Configuration Model
Support Anthropic, OpenAI, and Google AI out of the box. Allow registration of custom or community-hosted adapters (Ollama, LocalAI, vLLM, text-generation-webui, paLM-api). Multiple named profiles per provider persist state in `.env`.

### Theme 3 — `configure` Subcommand (Dual Mode)
- **Mode A (flags)** — Non-interactive; any flag executes a single operation and returns immediately
- **Mode B (wizard)** — No flags; step-by-step guided setup with immediate activation offer

### Theme 4 — GUI AI Providers Menu Item
Add **🤖 AI Providers** to the `--gui` loop with a `rich` status panel and `questionary.select` prompt.

### Theme 5 — `.env` Single Source of Truth
All Python and TypeScript runtimes read and write the same repo-root `.env`; no runtime maintains its own credential store.

### Theme 6 — Secure Credential Handling
API keys masked as `sk-***...***` in all status displays, logs, and terminal output. Raw secrets never printed.

---

## Files to Create

| File | Purpose |
|------|---------|
| `ai_providers.py` | Provider registry, resolution, and management functions |
| `ai_providers.ts` | TypeScript interop wrapper (reads same `.env` keys) |

## Files to Modify

| File | Change |
|------|--------|
| `generate_documentation.py` | Add `configure` subcommand, `--gui` menu item, provider routing |
| `.env` (repo root) | Add `AI_ACTIVE_PROVIDER`, `AI_ACTIVE_PROFILE`, per-provider key conventions |

---

## Success Criteria

- [ ] `--generate` and all AI-powered commands use the active provider/profile automatically
- [ ] `configure --list-providers` and all flags execute without launching the wizard
- [ ] `configure` (no flags) runs the step-by-step guided wizard
- [ ] Community/self-hosted providers can be registered without modifying core abstraction
- [ ] API keys never appear in plain text in any output or log
- [ ] Python and TypeScript helpers read the same `.env` keys; no duplicated business logic
- [ ] All subcommands expose `-h`/`--help` and `-v`/`--version`
- [ ] `KeyboardInterrupt` in the GUI loop exits gracefully without a stack trace

---

## Estimated Effort

| Area | Hours |
|------|-------|
| Design, planning, scaffolding | 10 |
| Provider abstraction layer + runtime routing | 10 |
| `configure` Mode A (direct flags) | 6 |
| `configure` Mode B (interactive wizard) | 4 |
| Custom provider extensibility | 8 |
| GUI AI Providers menu item | 4 |
| `.env` integration (Python + TypeScript) | 4 |
| Provider resolution interop helpers | 4 |
| Testing and documentation | 10 |
| **Total** | **60** |

---

**Last Updated**: 2026-03-16
**Change Owner**: Platform Engineering
**Source**: `ai-prompts/ai-provider-combo-JIRA.md`
**Reviewers**: TBD


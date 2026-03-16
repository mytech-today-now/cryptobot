# Proposal: Configurable AI Provider Layer

## Change ID
`AI-PROVIDER-001`

## Status
Draft

## Created
2026-03-16

## Author
Platform Engineering

---

## Problem Statement

The Crypto Trading Bot Platform's CLI (`generate_documentation.py`) currently has no structured way to select, configure, or switch AI providers. Credentials are either hard-coded or set manually in `.env` without validation, guidance, or multi-profile support.

### 1. No Provider Abstraction
All AI-powered commands depend on a single hard-coded integration. There is no shared provider interface, so:
- Switching backends requires source code edits in every consuming file
- TypeScript and Python runtimes may read credentials differently, creating drift
- Community or self-hosted providers (Ollama, LocalAI, vLLM) cannot be registered without modifying core code

### 2. No Guided Configuration Workflow
Users must manually edit `.env` with no validation, help text, or activation confirmation:
- Non-technical users cannot set up providers without developer assistance
- Mistakes (wrong key names, missing profiles) silently break AI commands at runtime
- There is no scripting-friendly flag API for CI/CD pipelines

### 3. No Multi-Profile Support
A single set of credentials cannot serve multiple clients, projects, or environments:
- No way to maintain `personal`, `work`, `client`, or `testing` profiles per provider
- Switching environments requires full manual overwrite of `.env` keys
- Active provider/profile state is not tracked, making status queries impossible

### 4. No GUI Visibility
The existing `--gui` interactive loop has no entry point for provider management:
- Users cannot check which provider is active without inspecting `.env` directly
- Guided setup is inaccessible from the menu-driven workflow
- `KeyboardInterrupt` during provider tasks can produce unhandled stack traces

---

## Proposed Solution

### Part 1 — Provider Abstraction Layer
Introduce a single import contract for all AI-consuming code:
- Python: `from ai_providers import resolve_active_provider`
- TypeScript: `import { resolveActiveProvider } from './ai_providers'`

Both helpers read `AI_ACTIVE_PROVIDER` and `AI_ACTIVE_PROFILE` from `.env`. Command handlers resolve the active backend through this interface rather than direct integration-specific logic.

### Part 2 — Provider Configuration Model
- Built-in support: **Anthropic**, **OpenAI**, **Google AI**
- Open extension model: users register community/self-hosted adapters using the same interface as built-in providers (Ollama, LocalAI, vLLM, text-generation-webui, paLM-api)
- Multiple named profiles per provider (e.g. `personal`, `work`, `client`, `testing`)
- Active state persisted via `AI_ACTIVE_PROVIDER` and `AI_ACTIVE_PROFILE` in `.env`

### Part 3 — Dual-Mode `configure` Subcommand
**Mode A — Direct flags (non-interactive):**
```
python generate_documentation.py configure --list-providers
python generate_documentation.py configure --list-profiles
python generate_documentation.py configure --create-profile  <provider_id>/<profile_name>
python generate_documentation.py configure --edit-profile    <provider_id>/<profile_name>
python generate_documentation.py configure --delete-profile  <provider_id>/<profile_name>
python generate_documentation.py configure --activate-profile <provider_id>/<profile_name>
```
When any flag is present, execute only that operation and return immediately — the wizard is never launched.

**Mode B — Interactive guided wizard (no flags):**
Print a numbered provider list → prompt for selection → prompt for profile name (default `"default"`) → call `provider_create_command()` interactively → offer immediate activation (`Y/n`).

### Part 4 — GUI AI Providers Menu Item
Add **🤖 AI Providers** to the `--gui` main loop. When selected:
1. Display a `rich` status panel via `provider_status_command()`
2. Present a `questionary.select` prompt: **⚙️ Run guided setup** | **↩ Back**
3. Handle `KeyboardInterrupt` gracefully without a stack trace

### Part 5 — `.env` Single Source of Truth
Key conventions:
- `<PROVIDER_ID>_API_KEY` — e.g. `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_AI_API_KEY`
- `AI_ACTIVE_PROVIDER` — currently selected provider ID
- `AI_ACTIVE_PROFILE` — currently selected profile name

Python writes via `dotenv.set_key()`; TypeScript reads via `dotenv` npm package. No runtime maintains a separate credential store.

### Part 6 — Secure Credential Handling
API keys masked as `sk-***...***` in all status displays, logs, and terminal output. Raw secrets are never printed.

---

## Benefits

1. **Universal provider support** — Any AI backend usable via a single registration step
2. **Non-technical user experience** — Guided wizard + GUI menu make setup accessible
3. **Multi-environment profiles** — Separate credentials per client, project, or environment
4. **Scripting and CI/CD ready** — Non-interactive flags work in automated pipelines
5. **Security** — API keys masked at all output boundaries
6. **Cross-runtime consistency** — Python and TypeScript share the same state via `.env`

---

## Success Criteria

1. `--generate` and all AI-powered commands automatically use the active provider/profile
2. All `configure` flags execute without launching the wizard
3. `configure` (no flags) runs the guided wizard and offers activation on completion
4. Community/self-hosted providers can be registered without modifying the core abstraction
5. API keys never appear in plain text in output or logs
6. Python and TypeScript helpers do not duplicate business logic
7. All subcommands expose `-h`/`--help` and `-v`/`--version`

---

## Non-Goals

- Server-side credential storage (all state remains in repo-root `.env`)
- OAuth or browser-based authentication flows
- Provider billing or usage dashboards
- Automatic provider failover or load balancing (future epic)
- Support for non-`.env` credential backends (e.g., AWS Secrets Manager) in v1

---

## Timeline

| Phase | Description | Duration |
|-------|-------------|----------|
| 1 | Design, scaffolding, and provider abstraction layer | 3 days |
| 2 | `configure` subcommand (Mode A + Mode B) | 3 days |
| 3 | Custom provider extensibility and interop helpers | 2 days |
| 4 | GUI menu item and `.env` integration | 2 days |
| 5 | Testing and documentation | 3 days |
| **Total** | | **~13 days** |

---

## Dependencies

- `python-dotenv` (Python) — already in `requirements.txt`
- `rich` (Python) — terminal panels and styled output
- `questionary` (Python) — interactive prompts
- `dotenv` npm package (TypeScript) — `.env` loading
- `argparse` (Python stdlib) — CLI subcommand registration

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| `.env` write races between Python/TS | Medium | Serialize writes through Python CLI; TS reads only |
| Custom provider authors skip `ensure_providers()` | Medium | Guard in base registration; raise `ProviderNotRegisteredError` |
| Wizard UX confusing for first-time users | Low | Defaults everywhere; clear prompts; Back option always available |
| `KeyboardInterrupt` during wizard leaves partial state | Low | Wrap wizard in try/except; rollback partial profile writes |

---

## Open Questions

1. Should profiles support per-model overrides (e.g. `claude-3-opus` vs `claude-3-haiku`)? → **Yes, as optional `model` field in profile**
2. Should the wizard support editing existing profiles step by step? → **Yes, via `--edit-profile` flag and guided re-prompts**
3. Should TypeScript write-back go through the Python CLI or a shared `dotenv` utility? → **Via Python CLI in v1 for simplicity**
4. Should provider validation ping the API endpoint or just check key format? → **Key format check in v1; live ping as opt-in `--validate` flag**


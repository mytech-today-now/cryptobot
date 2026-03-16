# AI Provider Layer — Summary

## Change ID
`AI-PROVIDER-001`

## Status
Draft

## Generated
2026-03-16

## Source
`ai-prompts/ai-provider-combo-JIRA.md`

---

## Change Overview

**Title**: Configurable AI Provider Layer with `configure` Subcommand and GUI Menu
**Duration**: ~13 days
**Total Tasks**: 21
**Total Estimated Hours**: 60

This change refactors the Crypto Trading Bot Platform CLI so all AI-powered commands route through a shared provider abstraction. It introduces a dual-mode `configure` subcommand, a GUI menu item for provider management, and a TypeScript interop layer — all backed by the repo-root `.env` as the single source of truth.

---

## What Was Generated

### 1. README.md
- Full change overview, problem statement, solution themes
- Files to create and modify
- Success criteria checklist
- Effort estimate table

### 2. proposal.md
- Detailed problem statement (4 problem areas)
- Proposed solution (6 parts)
- Benefits, success criteria, non-goals
- Timeline, dependencies, risks, open questions

### 3. design.md
- Architecture diagram showing all components and data flow
- Python dataclass definitions (`ProviderProfile`, `ProviderDescriptor`, `ConfigureOptions`)
- Full function contract table for `ai_providers.py`
- TypeScript interop function contracts
- `configure` subcommand Mode A and Mode B flow diagrams
- GUI menu integration code sketch
- `.env` key schema table
- Built-in provider registry definition
- Security considerations

### 4. deltas.md
- Files to create: `ai_providers.py`, `ai_providers.ts`
- Files to modify: `generate_documentation.py`, `.env`
- New component APIs (Python import contract, TypeScript import contract)
- Dependencies added (`questionary`, `rich`, `dotenv` npm)
- Rollback plan

### 5. tasks.md
- 21 tasks organized across 5 phases
- Each task: priority, estimated time, dependencies, description, acceptance criteria, deliverables
- Task summary by phase and priority
- Critical path analysis

### 6. specs/ (5 files)
- `provider-abstraction-layer.md` — FR + technical spec for the shared provider interface
- `configure-subcommand.md` — FR + argparse registration + Mode A/B behavior
- `gui-menu.md` — FR + menu integration + KeyboardInterrupt handling
- `env-integration.md` — Key schema, read/write conventions, Python + TypeScript rules
- `provider-extensibility.md` — Registration API, built-in adapter specs, community adapter guide

### 7. tests/ (4 files)
- `configure-command.md` — Tests for Mode A flags, Mode B wizard, slash parsing
- `provider-resolution.md` — Tests for Python + TypeScript resolution, error cases
- `secret-masking.md` — Tests for mask_api_key(), status panel output, log safety
- `gui-menu.md` — Tests for menu entry, status panel, guided setup, KeyboardInterrupt

---

## Implementation Phases

### Phase 1 — Foundation (3 days)
- Task 1.1: Create `ai_providers.py` skeleton and provider registry
- Task 1.2: Implement `ProviderDescriptor`, `ProviderProfile`, `ConfigureOptions` dataclasses
- Task 1.3: Implement `ensure_providers()` and `.env` bootstrap
- Task 1.4: Implement `resolve_active_provider()` and `get_active_profile()`

### Phase 2 — `configure` Subcommand (3 days)
- Task 2.1: Register `configure` subparser in `generate_documentation.py`
- Task 2.2: Implement `configure_command()` dispatch logic
- Task 2.3: Implement `provider_list_command()` with rich table output
- Task 2.4: Implement `provider_create_command()` (interactive + non-interactive)
- Task 2.5: Implement `provider_edit_command()` and `provider_delete_command()`
- Task 2.6: Implement `provider_activate_command()` and `parse_provider_profile_arg()`

### Phase 3 — Provider Extensibility (2 days)
- Task 3.1: Implement `register_provider()` public API
- Task 3.2: Add built-in provider registry (Anthropic, OpenAI, Google AI, Ollama, LocalAI)
- Task 3.3: Add `mask_api_key()` and apply to all output boundaries

### Phase 4 — GUI + TypeScript Interop (2 days)
- Task 4.1: Add 🤖 AI Providers menu entry to `--gui` loop
- Task 4.2: Implement `provider_status_command()` with rich panel
- Task 4.3: Wrap GUI loop in `KeyboardInterrupt` handler
- Task 4.4: Create `ai_providers.ts` TypeScript interop module
- Task 4.5: Route `--generate` and other AI commands through provider abstraction

### Phase 5 — Testing and Documentation (3 days)
- Task 5.1: Write unit tests for `configure` Mode A flags
- Task 5.2: Write unit tests for `configure` Mode B wizard
- Task 5.3: Write unit tests for `resolve_active_provider()` and `get_active_profile()`
- Task 5.4: Write tests for secret masking and GUI menu navigation
- Task 5.5: Update inline docstrings, README, and `.env.example`
- Task 5.6: Run full acceptance criteria checklist

---

## Key Themes and Critical Rules

| Theme | Critical Rule |
|-------|--------------|
| Provider abstraction layer | "Command handlers must resolve the active backend through the provider abstraction rather than direct, integration-specific logic." |
| Provider configuration model | "Separate provider metadata, credentials, and active-profile state so runtime resolution is deterministic." |
| Custom provider extensibility | "Provider registration must not assume a closed list of vendor-owned backends." |
| `configure` Mode A (flags) | "When any flag is present, execute only that operation and return immediately without launching the wizard." |
| `configure` Mode B (wizard) | "The wizard must present a numbered provider list, prompt for profile name with a sensible default, and offer immediate activation." |
| GUI menu item | "The menu item must show a `rich` status panel before presenting choices and must handle `KeyboardInterrupt` without a stack trace." |
| `.env` single source of truth | "No runtime may maintain its own credential store; all reads and writes target the repo-root `.env`." |
| Provider resolution interop | "Python and TypeScript helpers must read the same `AI_ACTIVE_PROVIDER` and `AI_ACTIVE_PROFILE` keys and must not duplicate business logic." |
| Secure credential handling | "Never print secrets in normal output; mask as `sk-***...***` in all status displays and logs." |

---

## Success Metrics

- ✅ `--generate` and all AI commands use active provider/profile automatically
- ✅ All `configure` flags execute without launching wizard
- ✅ `configure` (no flags) runs guided wizard and offers activation
- ✅ Community providers register without modifying core abstraction
- ✅ API keys never appear in plain text in output or logs
- ✅ Python and TypeScript use same `.env` keys, no duplicated logic
- ✅ All subcommands expose `-h`/`--help` and `-v`/`--version`
- ✅ `KeyboardInterrupt` in GUI loop exits gracefully

---

**Generated**: 2026-03-16
**Based on**: `ai-prompts/ai-provider-combo-JIRA.md`
**Ready for**: Review and Beads task decomposition


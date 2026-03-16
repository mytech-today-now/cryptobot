# Tasks: Configurable AI Provider Layer

## Change ID
`AI-PROVIDER-001`

## Version
1.0.0

## Status
Draft

## Last Updated
2026-03-16

---

## Overview

**Total Tasks**: 21
**Estimated Duration**: ~13 days (60 hours)

---

## Phase 1 — Foundation (3 days)

### Task 1.1: Create `ai_providers.py` Skeleton
**Priority**: High | **Estimated Time**: 2 hours | **Dependencies**: None

**Description**: Create the `ai_providers.py` module at repo root with module docstring, imports, and empty function stubs for all public APIs.

**Acceptance Criteria**:
- [ ] File created at repo root
- [ ] All public function stubs present with type hints and docstrings
- [ ] `from ai_providers import resolve_active_provider` importable without error
- [ ] Module passes `python -m py_compile ai_providers.py`

**Deliverables**: `ai_providers.py` (skeleton)

---

### Task 1.2: Implement Dataclasses
**Priority**: High | **Estimated Time**: 2 hours | **Dependencies**: Task 1.1

**Description**: Implement `ProviderDescriptor`, `ProviderProfile`, and `ConfigureOptions` dataclasses with full field definitions and defaults.

**Acceptance Criteria**:
- [ ] All three dataclasses defined with `@dataclass`
- [ ] `ConfigureOptions` fields all default to `False` or `None`
- [ ] `ProviderProfile` includes `extra: dict` for provider-specific settings
- [ ] Unit tests for dataclass instantiation pass

**Deliverables**: Updated `ai_providers.py`

---

### Task 1.3: Implement `ensure_providers()` and `.env` Bootstrap
**Priority**: High | **Estimated Time**: 3 hours | **Dependencies**: Task 1.2

**Description**: Implement `ensure_providers()` to load the provider registry and active state from `.env` at startup. Must be idempotent.

**Acceptance Criteria**:
- [ ] Reads `AI_ACTIVE_PROVIDER` and `AI_ACTIVE_PROFILE` from `.env`
- [ ] Loads all `<PROVIDER_ID>_API_KEY` keys into internal store
- [ ] Idempotent — safe to call multiple times
- [ ] Does not raise if `.env` is missing; logs a warning

**Deliverables**: Updated `ai_providers.py`

---

### Task 1.4: Implement `resolve_active_provider()` and `get_active_profile()`
**Priority**: High | **Estimated Time**: 3 hours | **Dependencies**: Task 1.3

**Description**: Implement the two primary resolution functions consumed by all AI-powered commands.

**Acceptance Criteria**:
- [ ] `resolve_active_provider()` returns `ProviderDescriptor` for `AI_ACTIVE_PROVIDER`
- [ ] Raises `ProviderNotConfiguredError` if `AI_ACTIVE_PROVIDER` is unset or unregistered
- [ ] `get_active_profile()` returns `ProviderProfile` with masked key for display
- [ ] Raises `ProfileNotFoundError` if profile key is missing from `.env`
- [ ] Both call `ensure_providers()` internally

**Deliverables**: Updated `ai_providers.py`, unit tests

---

## Phase 2 — `configure` Subcommand (3 days)

### Task 2.1: Register `configure` Subparser
**Priority**: High | **Estimated Time**: 2 hours | **Dependencies**: Task 1.1

**Description**: Add the `configure` subparser and all 7 flags to `generate_documentation.py`.

**Acceptance Criteria**:
- [ ] `python generate_documentation.py configure -h` prints help without error
- [ ] All 7 flags registered (`--list-providers`, `--list-profiles`, `--list-profiles-for-provider`, `--create-profile`, `--edit-profile`, `--delete-profile`, `--activate-profile`)
- [ ] No breaking changes to existing flags

**Deliverables**: Modified `generate_documentation.py`

---

### Task 2.2: Implement `configure_command()` Dispatch
**Priority**: High | **Estimated Time**: 2 hours | **Dependencies**: Task 2.1, Task 1.4

**Description**: Implement `configure_command(options: ConfigureOptions)` — check each flag in declaration order, delegate to the corresponding function, return after first match, or launch the wizard if no flags set.

**Acceptance Criteria**:
- [ ] Each flag delegates to the correct function
- [ ] `ensure_providers()` called before any registry or store access
- [ ] Returns exit code `0` on success, `1` on error
- [ ] Wizard launched only when no flags present

**Deliverables**: Updated `ai_providers.py`

---

### Task 2.3: Implement `provider_list_command()`
**Priority**: High | **Estimated Time**: 2 hours | **Dependencies**: Task 2.2

**Description**: Print all registered providers as a `rich` table with columns: ID, Display Name, Status (active/inactive), Profile Count.

**Acceptance Criteria**:
- [ ] `configure --list-providers` prints a rich table
- [ ] Active provider row highlighted
- [ ] No API keys visible in output

**Deliverables**: Updated `ai_providers.py`

---

### Task 2.4: Implement `provider_create_command()`
**Priority**: High | **Estimated Time**: 4 hours | **Dependencies**: Task 2.3

**Description**: Interactive and non-interactive profile creation. Interactive mode uses `questionary.text` and `questionary.password` prompts.

**Acceptance Criteria**:
- [ ] `--create-profile anthropic/personal` creates profile non-interactively (prompts for key if not in env)
- [ ] Interactive mode prompts for provider ID, profile name, API key, model (optional)
- [ ] Writes keys to `.env` via `dotenv.set_key()` only
- [ ] Confirms success with `rich` panel

**Deliverables**: Updated `ai_providers.py`

---

### Task 2.5: Implement `provider_edit_command()` and `provider_delete_command()`
**Priority**: High | **Estimated Time**: 3 hours | **Dependencies**: Task 2.4

**Description**: Edit re-prompts only for fields the user wants to change. Delete requires confirmation and removes only the targeted profile keys.

**Acceptance Criteria**:
- [ ] `--edit-profile` re-prompts with current value as default
- [ ] `--delete-profile` asks for confirmation before removing keys
- [ ] Neither command removes unrelated `.env` variables
- [ ] Clear error if profile does not exist

**Deliverables**: Updated `ai_providers.py`

---

### Task 2.6: Implement `provider_activate_command()` and `parse_provider_profile_arg()`
**Priority**: High | **Estimated Time**: 2 hours | **Dependencies**: Task 2.5

**Description**: Write `AI_ACTIVE_PROVIDER` and `AI_ACTIVE_PROFILE` to `.env`. Implement the slash-separator parser used by all profile flags.

**Acceptance Criteria**:
- [ ] `--activate-profile anthropic/personal` sets both env keys
- [ ] `parse_provider_profile_arg("anthropic/personal")` returns `("anthropic", "personal")`
- [ ] Missing `/` separator exits with a clear, actionable error message
- [ ] Validates provider is registered before activating

**Deliverables**: Updated `ai_providers.py`

---

## Phase 3 — Provider Extensibility (2 days)

### Task 3.1: Implement `register_provider()` Public API
**Priority**: High | **Estimated Time**: 2 hours | **Dependencies**: Task 1.3

**Description**: Allow any `.py` or external module to register a custom provider descriptor into the shared registry.

**Acceptance Criteria**:
- [ ] `register_provider(descriptor)` adds to `_provider_registry`
- [ ] Raises `ProviderAlreadyRegisteredError` on duplicate ID (override-safe with `force=True`)
- [ ] Registered provider appears in `--list-providers` output
- [ ] Custom provider can be activated via `--activate-profile`

**Deliverables**: Updated `ai_providers.py`

---

### Task 3.2: Register Built-in Providers
**Priority**: High | **Estimated Time**: 2 hours | **Dependencies**: Task 3.1

**Description**: Register Anthropic, OpenAI, Google AI, Ollama, and LocalAI as built-in providers using the same `register_provider()` API.

**Acceptance Criteria**:
- [ ] All 5 built-in providers registered at module load time
- [ ] Ollama and LocalAI have `requires_api_key=False` and include default `base_url`
- [ ] Built-in providers indistinguishable from custom providers in the registry

**Deliverables**: Updated `ai_providers.py`

---

### Task 3.3: Implement `mask_api_key()` and Apply to All Boundaries
**Priority**: High | **Estimated Time**: 2 hours | **Dependencies**: Task 3.2

**Description**: Implement `mask_api_key()` and apply it at every output boundary (rich panels, table cells, log messages, `provider_status_command()`).

**Acceptance Criteria**:
- [ ] `mask_api_key("sk-ant-abc123")` returns `"sk-***...***"`
- [ ] No raw key value appears in any terminal or log output
- [ ] Applied in `provider_status_command()`, `provider_list_command()`, all edit/create confirmations

**Deliverables**: Updated `ai_providers.py`

---

## Phase 4 — GUI + TypeScript Interop (2 days)

### Task 4.1: Add 🤖 AI Providers Menu Entry to `--gui`
**Priority**: High | **Estimated Time**: 2 hours | **Dependencies**: Task 3.3

**Description**: Add the `🤖 AI Providers` entry to the `questionary.select` choices list in the `--gui` main loop.

**Acceptance Criteria**:
- [ ] Entry appears in `--gui` menu
- [ ] Selection calls `provider_status_command()` then presents setup/back choices
- [ ] `⚙️ Run guided setup` launches `configure_command(ConfigureOptions())`
- [ ] `↩ Back` returns to main menu

**Deliverables**: Modified `generate_documentation.py`

---

### Task 4.2: Implement `provider_status_command()` with Rich Panel
**Priority**: High | **Estimated Time**: 2 hours | **Dependencies**: Task 4.1

**Description**: Display a `rich` panel with active provider ID, display name, profile name, masked API key, and configured model.

**Acceptance Criteria**:
- [ ] Panel shows all fields listed above
- [ ] API key shown as `sk-***...***`
- [ ] "No active provider" message shown if `AI_ACTIVE_PROVIDER` unset
- [ ] Panel renders without error even when `.env` is empty

**Deliverables**: Updated `ai_providers.py`

---

### Task 4.3: Wrap GUI Loop in `KeyboardInterrupt` Handler
**Priority**: High | **Estimated Time**: 1 hour | **Dependencies**: Task 4.1

**Description**: Wrap the entire `--gui` loop and all provider management blocks in `try/except KeyboardInterrupt` so Ctrl+C exits gracefully with a friendly message and no stack trace.

**Acceptance Criteria**:
- [ ] Ctrl+C during main menu exits cleanly with "Goodbye!" or similar
- [ ] Ctrl+C during provider wizard returns to main menu (not crash)
- [ ] No `traceback` output on `KeyboardInterrupt`

**Deliverables**: Modified `generate_documentation.py`

---

### Task 4.4: Create `ai_providers.ts` TypeScript Interop Module
**Priority**: Medium | **Estimated Time**: 4 hours | **Dependencies**: Task 1.4

**Description**: Create a TypeScript module that reads the same `.env` keys and exposes `resolveActiveProvider()`, `getActiveProfile()`, and `maskApiKey()`. Write-back operations delegate to the Python CLI.

**Acceptance Criteria**:
- [ ] `import { resolveActiveProvider } from './ai_providers'` works in any `.ts` file
- [ ] Reads `AI_ACTIVE_PROVIDER` and `AI_ACTIVE_PROFILE` from `process.env`
- [ ] Does not duplicate business logic from `ai_providers.py`
- [ ] `maskApiKey("sk-abc")` returns `"sk-***...***"`

**Deliverables**: `ai_providers.ts`

---

### Task 4.5: Route AI Commands Through Provider Abstraction
**Priority**: High | **Estimated Time**: 3 hours | **Dependencies**: Task 1.4, Task 4.4

**Description**: Update `--generate` and any other AI-powered commands in `generate_documentation.py` so they call `resolve_active_provider()` and `get_active_profile()` instead of direct API logic.

**Acceptance Criteria**:
- [ ] `--generate` uses active provider/profile without user-visible change to invocation
- [ ] Clear error shown if no provider configured (not a raw `KeyError`)
- [ ] Provider routing applies to all AI commands, not just `--generate`

**Deliverables**: Modified `generate_documentation.py`

---

## Phase 5 — Testing and Documentation (3 days)

### Task 5.1: Unit Tests — `configure` Mode A Flags
**Priority**: High | **Estimated Time**: 4 hours | **Dependencies**: Phase 2 complete

**Description**: Write tests for all 7 flags, slash-separator parsing, and `ensure_providers()` guard.

**Acceptance Criteria**: See `tests/configure-command.md`

**Deliverables**: Test file (e.g. `tests/test_ai_providers.py`)

---

### Task 5.2: Unit Tests — `configure` Mode B Wizard
**Priority**: High | **Estimated Time**: 3 hours | **Dependencies**: Task 5.1

**Description**: Write tests for the interactive wizard flow using `questionary` mock/patch.

**Acceptance Criteria**: See `tests/configure-command.md` — Wizard section

**Deliverables**: Updated test file

---

### Task 5.3: Unit Tests — Provider Resolution and Interop
**Priority**: High | **Estimated Time**: 3 hours | **Dependencies**: Task 4.4

**Description**: Write tests for Python and TypeScript provider resolution, error cases, and `.env` read/write behavior.

**Acceptance Criteria**: See `tests/provider-resolution.md`

**Deliverables**: Updated test file; TypeScript test or Jest spec

---

### Task 5.4: Tests — Secret Masking and GUI Navigation
**Priority**: High | **Estimated Time**: 2 hours | **Dependencies**: Task 4.2

**Description**: Write tests for `mask_api_key()`, status panel content, and GUI menu navigation including `KeyboardInterrupt`.

**Acceptance Criteria**: See `tests/secret-masking.md`, `tests/gui-menu.md`

**Deliverables**: Updated test file

---

### Task 5.5: Documentation Updates
**Priority**: Medium | **Estimated Time**: 2 hours | **Dependencies**: All tasks

**Description**: Update inline docstrings, add `.env.example` entries, update project README if needed.

**Acceptance Criteria**:
- [ ] All public functions in `ai_providers.py` have docstrings
- [ ] `.env.example` (if present) includes all new key examples
- [ ] `generate_documentation.py` module docstring updated to mention `configure` subcommand

**Deliverables**: Updated source files

---

### Task 5.6: Acceptance Criteria Sign-Off
**Priority**: High | **Estimated Time**: 2 hours | **Dependencies**: Task 5.5

**Description**: Run the full acceptance criteria checklist from `proposal.md` and `README.md`. File any failing items as new Beads issues.

**Acceptance Criteria**:
- [ ] All checkboxes in README.md "Success Criteria" pass
- [ ] All acceptance criteria in `proposal.md` verified
- [ ] No regressions in existing CLI behavior

**Deliverables**: Completed checklist; any new Beads issues filed

---

## Task Summary

### By Phase
| Phase | Tasks | Duration |
|-------|-------|----------|
| 1 — Foundation | 4 | 3 days |
| 2 — `configure` Subcommand | 6 | 3 days |
| 3 — Provider Extensibility | 3 | 2 days |
| 4 — GUI + TypeScript Interop | 5 | 2 days |
| 5 — Testing and Documentation | 6 | 3 days |
| **Total** | **24** | **~13 days** |

### By Priority
- **High**: 20 tasks
- **Medium**: 1 task

### Critical Path
1. Task 1.1 → 1.2 → 1.3 → 1.4 (core resolution)
2. Task 2.1 → 2.2 → 2.3 → 2.4 → 2.5 → 2.6 (configure flags)
3. Task 3.1 → 3.2 → 3.3 (extensibility + masking)
4. Task 4.1 → 4.2 → 4.3 (GUI); Task 4.4 → 4.5 (interop + routing)
5. Tasks 5.1–5.6 (testing and sign-off)


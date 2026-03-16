# JIRA Ticket: TBD - Add `configure` Subcommand and GUI AI Provider Menu to Crypto Trading Bot Platform

### Summary
Add a `configure` subcommand and an **🤖 AI Providers** menu item to the `--gui` interactive loop in the Crypto Trading Bot Platform CLI (`generate_documentation.py` and any other `.py` or `.ts` files in this repo). Both entry points read and write provider credentials exclusively from the `.env` file at the repo root, which serves as the single source of truth for all Python and TypeScript runtimes. Provider selection supports direct non-interactive flags for scripting and a step-by-step interactive wizard for first-time setup.

> **Note**: Augment Code AI continues to assist with the *development* of this project. The providers configured here power the *runtime* AI features of the trading bot platform (e.g. signal generation, analysis, document generation calls). They are separate from the Augment Code development assistant.

### Description

#### Background
The platform's CLI (`generate_documentation.py`) currently has no structured way for users to select, configure, or switch AI providers. Credentials are either hard-coded or set manually in `.env` without any guided workflow. As more `.py` and `.ts` files are added to the repo and consume AI APIs, this ad-hoc approach becomes fragile and difficult to maintain across environments (personal, client, testing). A formal `configure` subcommand and GUI menu item will give both non-technical users and developers a consistent, safe path to set up and switch providers.

#### Key Requirements
- **Dual-mode `configure` subcommand**:
  - *Mode A — direct flags (non-interactive)*: when any flag is present, execute only that operation and return immediately without launching the wizard:
    ```
    python generate_documentation.py configure --list-providers
    python generate_documentation.py configure --list-profiles
    python generate_documentation.py configure --list-profiles-for-provider <provider_id>
    python generate_documentation.py configure --create-profile <provider_id>/<profile_name>
    python generate_documentation.py configure --edit-profile   <provider_id>/<profile_name>
    python generate_documentation.py configure --delete-profile <provider_id>/<profile_name>
    python generate_documentation.py configure --activate-profile <provider_id>/<profile_name>
    ```
  - *Mode B — interactive guided wizard (no flags)*: print a numbered provider list, prompt for selection, prompt for profile name (default `"default"`), call `provider_create_command` interactively, then offer to activate immediately (`Y/n`).
- **Flag delegation**: each `configure` flag maps to a dedicated Python function — `provider_list_command()`, `provider_create_command()`, `provider_edit_command()`, `provider_delete_command()`, `provider_activate_command()` — all of which call `ensure_providers()` before accessing the registry or store.
- **Slash-separated profile targeting**: profile flags accept `provider_id/profile_name` as a single value; a helper splits on the first `/` and exits with a clear error if the separator is missing.
- **`ConfigureOptions` dataclass**: all flag fields typed as `Optional[str]` or `bool`; `configure_command(options: ConfigureOptions)` checks each field in order and returns early after the first match; all options registered on the `configure` subparser via `argparse` `add_argument()`.
- **🤖 AI Providers GUI menu item**: add to the main `--gui` interactive loop; when selected, display a `rich` status panel via `provider_status_command()` then present a `questionary.select` prompt with ⚙️ Run guided setup and ↩ Back; handle `KeyboardInterrupt` gracefully without a stack trace.
- **`.env` as single source of truth** for both Python and TypeScript runtimes:
  - Key conventions: `<PROVIDER_ID>_API_KEY` (e.g. `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_AI_API_KEY`), `AI_ACTIVE_PROVIDER`, `AI_ACTIVE_PROFILE`.
  - *Python*: load via `dotenv.load_dotenv()` at startup; write via `dotenv.set_key(dotenv_path, key, value)` to avoid overwriting unrelated variables.
  - *TypeScript*: load via `import 'dotenv/config'` or `config({ path: resolve(__dirname, '../../.env') })`; read from `process.env`; write provider state by calling the shared Python CLI or using `dotenv` parse/write utilities — never maintain a separate credential store.
- **Provider resolution interop**:
  - Python: `from ai_providers import resolve_active_provider`
  - TypeScript: `import { resolveActiveProvider } from './ai_providers'` — reads `process.env.AI_ACTIVE_PROVIDER` and `process.env.AI_ACTIVE_PROFILE` after `dotenv` has loaded; must be importable by all `.ts` files in the repo.
- **Security**: mask all secret values as `sk-***...***` in status displays; never log or print raw API keys.
- **Tooling**: use `rich` for panel-style terminal output and `questionary` for interactive prompts (`questionary.select`, `questionary.text`, `questionary.confirm`) in Python files.

This ticket should be suitable for follow-on conversion into an OpenSpec change and subsequent decomposition into Beads tasks.

### Acceptance Criteria
- `python generate_documentation.py configure --list-providers` and all other direct flags execute without launching the interactive wizard.
- `python generate_documentation.py configure` (no flags) runs the step-by-step guided wizard and offers to activate the new profile on completion.
- All `configure` flags parse `provider_id/profile_name` correctly and exit with a clear error when the `/` separator is missing.
- `configure_command()` delegates each flag to the correct provider management function and calls `ensure_providers()` before any registry or store access.
- The `--gui` menu includes an **🤖 AI Providers** entry that displays a `rich` status panel and a `questionary.select` prompt with guided-setup and back options.
- `KeyboardInterrupt` in the GUI loop exits gracefully without a stack trace.
- All provider API keys and active-profile state are stored exclusively in `.env`; no separate credential store exists.
- Python files load `.env` via `python-dotenv` and write changes via `dotenv.set_key()` without overwriting unrelated variables.
- TypeScript files load `.env` via the `dotenv` npm package and read keys from `process.env`; write-back routes through the shared Python CLI or `dotenv` utilities.
- `from ai_providers import resolve_active_provider` works in any `.py` file in the repo.
- `import { resolveActiveProvider } from './ai_providers'` works in any `.ts` file after `dotenv` has loaded.
- API keys are never printed in plain text; all status output masks secrets as `sk-***...***`.
- Tests cover both configure modes, all flags, GUI menu navigation, `.env` read/write, and secret masking.

### Estimated Effort
- Design and subcommand scaffolding: 4 hours
- `configure` Mode A (direct flags) implementation: 6 hours
- `configure` Mode B (interactive wizard) implementation: 4 hours
- GUI AI Providers menu item: 4 hours
- `.env` integration for Python and TypeScript consumers: 4 hours
- Provider resolution interop helpers (`ai_providers.py` / `ai_providers.ts`): 3 hours
- Testing and documentation: 5 hours
- Total: 30 hours

### Attachments
- Implementation detail reference: `ai-prompts/ai-providers-JIRA.md`
- Main CLI entry point: `generate_documentation.py`
- Credential storage: `.env` (repo root) — managed via `python-dotenv` (Python) and `dotenv` npm package (TypeScript)
- Example implementation themes to guide OpenSpec and Beads breakdown:
  - `configure` subcommand — Mode A (direct flags)
    Goal: non-interactive flag execution for scripting and CI use
    Key rule: "When any flag is present, execute only that operation and return immediately without launching the wizard."
  - `configure` subcommand — Mode B (interactive wizard)
    Goal: guided first-time setup for non-technical users
    Key rule: "The wizard must present a numbered provider list, prompt for profile name with a sensible default, and offer immediate activation."
  - GUI AI Providers menu item
    Goal: surface provider status and setup from the existing `--gui` loop
    Key rule: "The menu item must show a `rich` status panel before presenting choices, and must handle `KeyboardInterrupt` without a stack trace."
  - `.env` single source of truth
    Goal: one credential file shared by all Python and TypeScript runtimes
    Key rule: "No runtime may maintain its own credential store; all reads and writes target the repo-root `.env`."
  - Provider resolution interop
    Goal: consistent active-provider lookup across `.py` and `.ts` files
    Key rule: "Python and TypeScript helpers must read the same `AI_ACTIVE_PROVIDER` and `AI_ACTIVE_PROFILE` keys and must not duplicate business logic."
  - Secure credential handling
    Goal: protect API keys at rest and in terminal output
    Key rule: "Never print secrets in normal output; mask as `sk-***...***` in all status displays and logs."


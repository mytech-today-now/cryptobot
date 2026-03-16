# JIRA Ticket: TBD - Add Configurable AI Provider Layer with `configure` Subcommand and GUI Menu to Crypto Trading Bot Platform

### Summary
Refactor the Crypto Trading Bot Platform so AI-powered commands such as `python generate_documentation.py --generate` resolve the active AI backend through a shared provider abstraction instead of a single hard-coded integration. Introduce a dual-mode `configure` subcommand (direct flags for scripting + an interactive guided wizard) and an **🤖 AI Providers** menu item in the `--gui` loop. Initially support Anthropic, OpenAI, and Google AI, while allowing users to add custom or community-hosted providers (Ollama, LocalAI, vLLM, etc.) and maintain multiple named profiles per provider. All credentials and active-profile state are stored exclusively in the `.env` file at the repo root, which serves as the single source of truth for both Python and TypeScript runtimes.

> **Note**: Augment Code AI continues to assist with the *development* of this project. The providers configured here power the *runtime* AI features of the trading bot platform (e.g. signal generation, analysis, document generation). They are separate from the Augment Code development assistant.

---

### Description

#### Background
The platform's CLI (`generate_documentation.py`) has no structured way for users to select, configure, or switch AI providers. Credentials are either hard-coded or set manually in `.env` without any guided workflow. As more `.py` and `.ts` files are added to the repo and consume AI APIs, this ad-hoc approach becomes fragile and difficult to maintain across environments (personal, client, testing). A provider abstraction layer, formal `configure` subcommand, and GUI menu item will give both non-technical users and developers a consistent, safe path to set up, manage, and switch providers — without changing the day-to-day bot workflow.

#### Key Requirements

**1. Provider Abstraction Layer**
- Refactor all AI-dependent functionality so command handlers resolve the active backend through a shared provider interface rather than direct, integration-specific logic.
- Expose a single import contract for Python (`from ai_providers import resolve_active_provider`) and TypeScript (`import { resolveActiveProvider } from './ai_providers'`); both modules read `AI_ACTIVE_PROVIDER` and `AI_ACTIVE_PROFILE` from `.env` and must not duplicate business logic.
- AI-powered commands (`--generate`, etc.) must automatically use the active provider/profile without any change to the user-facing invocation.

**2. Provider Configuration Model**
- Initially support Anthropic, OpenAI, and Google AI.
- Allow users to register and configure their own providers, including community or open-source adapters such as Ollama (`https://github.com/ollama/ollama`), LocalAI (`https://github.com/mudler/LocalAI`), vLLM (`https://github.com/vllm-project/vllm`), text-generation-webui (`https://github.com/oobabooga/text-generation-webui`), and paLM-api (`https://github.com/whitead/paLM-api`).
- Built-in providers must use the same extension model exposed to user-defined providers wherever practical; the architecture must never assume a closed list of vendor-owned backends.
- Allow multiple named profiles per provider (e.g. `personal`, `work`, `client`, `testing`).
- Persist active-profile state via `AI_ACTIVE_PROVIDER` and `AI_ACTIVE_PROFILE` keys in `.env`.

**3. `.env` as Single Source of Truth**
- Key conventions: `<PROVIDER_ID>_API_KEY` (e.g. `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_AI_API_KEY`), `AI_ACTIVE_PROVIDER`, `AI_ACTIVE_PROFILE`.
- Python: load via `dotenv.load_dotenv()` at startup; write via `dotenv.set_key(dotenv_path, key, value)` — never overwrite unrelated variables.
- TypeScript: load via `import 'dotenv/config'` or `config({ path: resolve(__dirname, '../../.env') })`; read from `process.env`; write provider state by calling the shared Python CLI or using `dotenv` parse/write utilities — never maintain a separate credential store.

**4. Dual-Mode `configure` Subcommand**
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
- *Mode B — interactive guided wizard (no flags)*: print a numbered provider list, prompt for selection, prompt for profile name (default `"default"`), call `provider_create_command()` interactively, then offer immediate activation (`Y/n`).
- Implement a `ConfigureOptions` dataclass with all flag fields typed as `Optional[str]` or `bool`; `configure_command(options: ConfigureOptions)` checks each field in order and returns after the first match; all options registered on the `configure` subparser via `argparse.add_argument()`.
- Profile flags accept `provider_id/profile_name` as a single value; a helper splits on the first `/` and exits with a clear error if the separator is missing.
- Each flag delegates to a dedicated function — `provider_list_command()`, `provider_create_command()`, `provider_edit_command()`, `provider_delete_command()`, `provider_activate_command()`, `provider_status_command()` — all of which call `ensure_providers()` before accessing the registry or store.

**5. GUI AI Providers Menu Item**
- Add an **🤖 AI Providers** entry to the main `--gui` interactive loop.
- When selected: display a `rich` status panel via `provider_status_command()`, then present a `questionary.select` prompt with **⚙️ Run guided setup** and **↩ Back** options.
- Handle `KeyboardInterrupt` gracefully in the GUI loop without a stack trace.
- The GUI must always reflect the currently active provider/profile and keep provider-management actions easy to find.

**6. CLI Help and Version Support**
- All new and refactored subcommands must expose `-h` / `--help` for usage guidance and `-v` / `--version` where appropriate.
- Help output must be clear, discoverable, and consistent with existing `argparse`-based CLI conventions in this repo.

**7. Tooling**
- Use `rich` for panel-style terminal output in Python files.
- Use `questionary` (`questionary.select`, `questionary.text`, `questionary.confirm`) for all interactive prompts in Python files.

**8. Validation and Error Handling**
- Validate provider settings before activation or runtime use.
- Surface clear errors for missing credentials, invalid models, unsupported providers, or failed connectivity.
- Provide actionable recovery guidance in both CLI and GUI experiences.

**9. Security**
- Mask all API keys as `sk-***...***` in status displays, logs, and terminal output.
- Never print or log raw secrets anywhere in the codebase.
- Preserve a seamless workflow: users configure once, then use bot commands normally.

**10. Testing and Documentation**
- Add tests covering: both `configure` modes, all flags, slash-separated profile parsing, GUI menu navigation, `.env` read/write, secret masking, provider resolution for Python and TypeScript consumers, custom provider registration, and validation/failure paths.
- Document provider setup, named profiles, switching workflows, GUI behavior, TypeScript interop, and security expectations.

This ticket is suitable for follow-on conversion into an OpenSpec change and subsequent decomposition into Beads tasks.

---

### Acceptance Criteria
- `python generate_documentation.py --generate` and other AI-powered commands automatically use the active configured provider/profile from `.env`.
- Initial provider support includes Anthropic, OpenAI, and Google AI; additional community/self-hosted providers can be registered without modifying the core abstraction.
- `python generate_documentation.py configure --list-providers` and all other direct flags execute without launching the interactive wizard.
- `python generate_documentation.py configure` (no flags) runs the step-by-step guided wizard and offers to activate the new profile on completion.
- All `configure` flags parse `provider_id/profile_name` correctly and exit with a clear error when the `/` separator is missing.
- `configure_command()` delegates each flag to the correct function and calls `ensure_providers()` before any registry or store access.
- Users can add, list, edit, validate, delete, and switch multiple named profiles per provider via the `configure` subcommand.
- The `--gui` menu includes an **🤖 AI Providers** entry that displays a `rich` status panel and a `questionary.select` prompt with guided-setup and back options.
- `KeyboardInterrupt` in the GUI loop exits gracefully without a stack trace.
- All provider API keys and active-profile state are stored exclusively in `.env`; no runtime maintains a separate credential store.
- Python files load `.env` via `python-dotenv` and write changes via `dotenv.set_key()` without overwriting unrelated variables.
- TypeScript files load `.env` via the `dotenv` npm package and read keys from `process.env`; write-back routes through the shared Python CLI or `dotenv` utilities.
- `from ai_providers import resolve_active_provider` works in any `.py` file in the repo.
- `import { resolveActiveProvider } from './ai_providers'` works in any `.ts` file after `dotenv` has loaded; Python and TypeScript helpers read the same keys and do not duplicate business logic.
- All new and refactored subcommands support `-h` / `--help` and `-v` / `--version` consistently with existing CLI conventions.
- API keys are never printed in plain text; all status output masks secrets as `sk-***...***`.
- Adding a new provider requires only a registration step against the shared extension interface.
- Automated tests and documentation cover all core behaviors listed above.

---

### Estimated Effort
| Area | Hours |
|---|---|
| Design, planning, and subcommand scaffolding | 10 |
| Provider abstraction layer and runtime command routing | 10 |
| `configure` Mode A (direct flags) implementation | 6 |
| `configure` Mode B (interactive wizard) implementation | 4 |
| Custom provider extensibility and open-source adapter support | 8 |
| GUI AI Providers menu item | 4 |
| `.env` integration for Python and TypeScript consumers | 4 |
| Provider resolution interop helpers (`ai_providers.py` / `ai_providers.ts`) | 4 |
| Testing and documentation | 10 |
| **Total** | **60** |

---

### Attachments
- Source documents: `ai-prompts/ai-providers-JIRA.md`, `ai-prompts/ai-provider-selection-prompt.md`
- Main CLI entry point: `generate_documentation.py`
- Credential storage: `.env` (repo root) — managed via `python-dotenv` (Python) and `dotenv` npm package (TypeScript)

#### Implementation Themes (for OpenSpec and Beads breakdown)

- **Provider abstraction layer** — Route all AI-powered commands through a shared provider interface. Key rule: "Command handlers must resolve the active backend through the provider abstraction rather than direct, integration-specific logic."
- **Provider configuration model** — Support multiple providers, multiple named profiles per provider, and initial support for Anthropic, OpenAI, and Google AI; persist state in `.env`. Key rule: "Separate provider metadata, credentials, and active-profile state so runtime resolution is deterministic."
- **Custom and open-source provider extensibility** — Allow users to register community or self-hosted adapters using the same extension model as built-in providers. Key rule: "Provider registration must not assume a closed list of vendor-owned backends."
- **`configure` subcommand — Mode A (direct flags)** — Non-interactive flag execution for scripting and CI use. Key rule: "When any flag is present, execute only that operation and return immediately without launching the wizard."
- **`configure` subcommand — Mode B (interactive wizard)** — Guided first-time setup for non-technical users. Key rule: "The wizard must present a numbered provider list, prompt for profile name with a sensible default, and offer immediate activation."
- **GUI AI Providers menu item** — Surface provider status and setup from the existing `--gui` loop. Key rule: "The menu item must show a `rich` status panel before presenting choices and must handle `KeyboardInterrupt` without a stack trace."
- **`.env` single source of truth** — One credential file shared by all Python and TypeScript runtimes. Key rule: "No runtime may maintain its own credential store; all reads and writes target the repo-root `.env`."
- **Provider resolution interop** — Consistent active-provider lookup across `.py` and `.ts` files. Key rule: "Python and TypeScript helpers must read the same `AI_ACTIVE_PROVIDER` and `AI_ACTIVE_PROFILE` keys and must not duplicate business logic."
- **CLI help and version behavior** — Make command discovery easy for all users. Key rule: "All new and refactored subcommands must expose `-h`/`--help` and `-v`/`--version` consistently."
- **Secure credential handling** — Protect API keys at rest and in terminal output. Key rule: "Never print secrets in normal output; mask as `sk-***...***` in all status displays and logs."


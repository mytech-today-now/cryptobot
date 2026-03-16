# Spec Delta: Configurable AI Provider Layer

## Change ID
`AI-PROVIDER-001`

## Change Type
**ADDED + MODIFIED** — New provider abstraction layer added; existing CLI and GUI modified

---

## Files to be Created

### 1. `ai_providers.py`
**Type**: New file
**Purpose**: Python provider registry, resolution, and management functions

**Key Exports**:
```python
resolve_active_provider() -> ProviderDescriptor
get_active_profile() -> ProviderProfile
ensure_providers() -> None
configure_command(options: ConfigureOptions) -> int
provider_list_command() -> None
provider_create_command(provider_id, profile_name, interactive) -> None
provider_edit_command(provider_id, profile_name) -> None
provider_delete_command(provider_id, profile_name) -> None
provider_activate_command(provider_id, profile_name) -> None
provider_status_command() -> None
register_provider(descriptor: ProviderDescriptor) -> None
mask_api_key(key: str) -> str
parse_provider_profile_arg(value: str) -> tuple[str, str]
```

**Dataclasses defined**:
- `ProviderDescriptor`
- `ProviderProfile`
- `ConfigureOptions`

**Dependencies**: `python-dotenv`, `rich`, `questionary`, `dataclasses`, `os`, `pathlib`

**Estimated Lines**: ~350–450

---

### 2. `ai_providers.ts`
**Type**: New file
**Purpose**: TypeScript interop wrapper — resolves active provider from `.env` for `.ts` consumers

**Key Exports**:
```typescript
export interface ProviderDescriptor { ... }
export interface ProviderProfile { ... }
export function resolveActiveProvider(): ProviderDescriptor
export function getActiveProfile(): ProviderProfile
export function maskApiKey(key: string): string
```

**Note**: Write-back operations (activate profile, create profile) delegate to the Python CLI via `spawnSync` rather than duplicating `.env` write logic in TypeScript.

**Dependencies**: `dotenv` npm package, `child_process` (Node.js stdlib)

**Estimated Lines**: ~120–150

---

## Files to be Modified

### 1. `generate_documentation.py`
**Change type**: Modified

**ADDED — `configure` subparser registration** (in `main()`):
```python
subparsers = parser.add_subparsers(dest='subcommand')
configure_parser = subparsers.add_parser('configure', help='Configure AI providers and profiles')
configure_parser.add_argument('--list-providers', action='store_true')
configure_parser.add_argument('--list-profiles', action='store_true')
configure_parser.add_argument('--list-profiles-for-provider', type=str, metavar='PROVIDER_ID')
configure_parser.add_argument('--create-profile', type=str, metavar='PROVIDER_ID/PROFILE_NAME')
configure_parser.add_argument('--edit-profile',   type=str, metavar='PROVIDER_ID/PROFILE_NAME')
configure_parser.add_argument('--delete-profile',  type=str, metavar='PROVIDER_ID/PROFILE_NAME')
configure_parser.add_argument('--activate-profile',type=str, metavar='PROVIDER_ID/PROFILE_NAME')
```

**ADDED — subcommand dispatch** (in `main()` before generator creation):
```python
if args.subcommand == 'configure':
    from ai_providers import configure_command, ConfigureOptions
    options = ConfigureOptions(
        list_providers=args.list_providers,
        ...
    )
    return configure_command(options)
```

**ADDED — `--generate` routing through provider abstraction**:
```python
# Before calling any AI API:
from ai_providers import resolve_active_provider, get_active_profile
provider = resolve_active_provider()
profile  = get_active_profile()
```

**MODIFIED — `--gui` main loop**:
- Add `"🤖 AI Providers"` to the `questionary.select` choices list
- Add handler block for that choice:
  ```python
  elif choice == "🤖 AI Providers":
      try:
          provider_status_command()
          action = questionary.select("AI Providers", choices=["⚙️ Run guided setup", "↩ Back"]).ask()
          if action == "⚙️ Run guided setup":
              configure_command(ConfigureOptions())
      except KeyboardInterrupt:
          pass
  ```
- Wrap main GUI loop in `try/except KeyboardInterrupt` to exit gracefully

**Estimated diff**: +80–120 lines added, 10–20 lines modified

---

### 2. `.env` (repo root)
**Change type**: Schema additions (user-populated, not code-committed)

**ADDED keys** (to be documented in `.env.example` if present):
```dotenv
# AI Provider Configuration
AI_ACTIVE_PROVIDER=anthropic
AI_ACTIVE_PROFILE=default

# Built-in provider API keys
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
GOOGLE_AI_API_KEY=

# Custom/self-hosted provider example
# OLLAMA_BASE_URL=http://localhost:11434
# LOCALAI_BASE_URL=http://localhost:8080
```

---

## New Components / Modules

### Provider Registry (within ai_providers.py)
```python
_provider_registry: dict[str, ProviderDescriptor] = {}

def register_provider(descriptor: ProviderDescriptor) -> None:
    _provider_registry[descriptor.provider_id] = descriptor
```

### Profile Store (within ai_providers.py)
Profiles are persisted as `.env` keys following the convention:
- Key: `<PROVIDER_ID>_API_KEY` (required)
- Key: `<PROVIDER_ID>_MODEL` (optional)
- Key: `<PROVIDER_ID>_BASE_URL` (optional, for self-hosted)

Multiple profiles per provider use the naming convention:
- `<PROVIDER_ID>_<PROFILE_NAME>_API_KEY`
- `AI_ACTIVE_PROVIDER` + `AI_ACTIVE_PROFILE` for active state

---

## API Changes

### argparse Interface
**ADDED** `configure` subcommand with 7 flags (see above).
**No breaking changes** to existing flags (`--phase`, `--category`, `--dry-run`, `--generate`, `--gui`, `--output`).

### Python Import API (new)
```python
from ai_providers import (
    resolve_active_provider,
    get_active_profile,
    ensure_providers,
    configure_command,
    ConfigureOptions,
    register_provider,
    mask_api_key,
)
```

### TypeScript Import API (new)
```typescript
import { resolveActiveProvider, getActiveProfile, maskApiKey } from './ai_providers';
```

---

## Dependencies Added

| Package | Runtime | Purpose |
|---------|---------|---------|
| `questionary` | Python | Interactive wizard prompts |
| `rich` | Python | Status panels and styled tables |
| `dotenv` (npm) | TypeScript | `.env` loading in TS consumers |

`python-dotenv` is already in `requirements.txt`.

---

## Configuration Changes

No changes to `openspec/config.yaml`.

`.env.example` (if present) should be updated with the new key schema documented above.

---

## Migration / Upgrade Path

- Existing users with manually set `.env` keys continue to work; `ensure_providers()` reads existing keys
- Activating a profile writes only `AI_ACTIVE_PROVIDER` and `AI_ACTIVE_PROFILE`; no existing keys are overwritten
- Custom providers can be registered by calling `register_provider()` before any command dispatch

---

## Rollback Plan

1. Remove `ai_providers.py` and `ai_providers.ts`
2. Revert `generate_documentation.py` to remove `configure` subparser and GUI menu entry
3. Remove `AI_ACTIVE_PROVIDER` and `AI_ACTIVE_PROFILE` from `.env`

No impact on existing bot commands or documentation generation behavior.


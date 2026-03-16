# Design: Configurable AI Provider Layer

## Change ID
`AI-PROVIDER-001`

## Version
1.0.0

## Status
Draft

## Last Updated
2026-03-16

---

## Design Overview

This document describes the architecture, data models, and function contracts for implementing the AI provider abstraction layer, `configure` subcommand, GUI menu item, and cross-runtime interop helpers.

---

## Part 1 — Architecture

### Component Diagram

```
┌──────────────────────────────────────────────────────────┐
│                generate_documentation.py                  │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ --generate  │  │  configure   │  │     --gui       │  │
│  │  (and other │  │  subcommand  │  │  (menu loop)    │  │
│  │  AI cmds)   │  │              │  │                 │  │
│  └──────┬──────┘  └──────┬───────┘  └────────┬────────┘  │
│         │                │                    │           │
│         └────────────────┴────────────────────┘           │
│                          │                                │
│              ┌───────────▼───────────┐                    │
│              │     ai_providers.py   │                    │
│              │  resolve_active_      │                    │
│              │  provider()           │                    │
│              │  ensure_providers()   │                    │
│              │  provider_registry    │                    │
│              └───────────┬───────────┘                    │
│                          │                                │
│              ┌───────────▼───────────┐                    │
│              │     .env (repo root)  │                    │
│              │  AI_ACTIVE_PROVIDER   │                    │
│              │  AI_ACTIVE_PROFILE    │                    │
│              │  ANTHROPIC_API_KEY    │                    │
│              │  OPENAI_API_KEY       │                    │
│              │  GOOGLE_AI_API_KEY    │                    │
│              └───────────────────────┘                    │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                   ai_providers.ts                         │
│  resolveActiveProvider() — reads same .env keys          │
│  Write-back: delegates to Python CLI subprocess           │
└──────────────────────────────────────────────────────────┘
```

---

## Part 2 — Data Models

### ProviderProfile Dataclass (Python)
```python
@dataclass
class ProviderProfile:
    provider_id: str        # e.g. "anthropic"
    profile_name: str       # e.g. "personal"
    api_key: str            # raw key (never logged)
    model: Optional[str]    # e.g. "claude-3-5-sonnet-20241022"
    base_url: Optional[str] # for custom/self-hosted providers
    extra: dict             # provider-specific settings
```

### ProviderDescriptor Dataclass (Python)
```python
@dataclass
class ProviderDescriptor:
    provider_id: str        # e.g. "anthropic"
    display_name: str       # e.g. "Anthropic (Claude)"
    env_key_prefix: str     # e.g. "ANTHROPIC"
    default_model: str      # e.g. "claude-3-5-sonnet-20241022"
    base_url: Optional[str] # None for cloud providers
    requires_api_key: bool  # False for some self-hosted
```

### ConfigureOptions Dataclass (Python)
```python
@dataclass
class ConfigureOptions:
    list_providers: bool = False
    list_profiles: bool = False
    list_profiles_for_provider: Optional[str] = None
    create_profile: Optional[str] = None  # "provider_id/profile_name"
    edit_profile: Optional[str] = None
    delete_profile: Optional[str] = None
    activate_profile: Optional[str] = None
```

---

## Part 3 — Function Contracts

### ai_providers.py — Core Functions

```python
def ensure_providers() -> None:
    """Load provider registry and store from .env. Must be called before any registry access."""

def resolve_active_provider() -> ProviderDescriptor:
    """Return the active provider descriptor. Raises ProviderNotConfiguredError if none set."""

def get_active_profile() -> ProviderProfile:
    """Return the active profile. Raises ProfileNotFoundError if missing or misconfigured."""

def provider_list_command() -> None:
    """Print all registered providers as a rich table."""

def provider_create_command(provider_id: str, profile_name: str, interactive: bool = True) -> None:
    """Create a new profile. If interactive=True, prompt for credentials via questionary."""

def provider_edit_command(provider_id: str, profile_name: str) -> None:
    """Edit an existing profile interactively."""

def provider_delete_command(provider_id: str, profile_name: str) -> None:
    """Delete a profile from .env after confirmation."""

def provider_activate_command(provider_id: str, profile_name: str) -> None:
    """Write AI_ACTIVE_PROVIDER and AI_ACTIVE_PROFILE to .env."""

def provider_status_command() -> None:
    """Print a rich panel showing active provider, profile, masked key, and model."""

def configure_command(options: ConfigureOptions) -> int:
    """Dispatch configure flags in declaration order; launch wizard if no flags set."""

def parse_provider_profile_arg(value: str) -> tuple[str, str]:
    """Split 'provider_id/profile_name'; exit with error if '/' separator missing."""

def mask_api_key(key: str) -> str:
    """Return 'sk-***...***' masked representation of any API key string."""
```

### ai_providers.ts — TypeScript Interop

```typescript
export function resolveActiveProvider(): ProviderDescriptor;
export function getActiveProfile(): ProviderProfile;
export function maskApiKey(key: string): string;
// Write-back operations delegate to Python CLI subprocess:
// spawnSync('python', ['generate_documentation.py', 'configure', '--activate-profile', ...])
```

---

## Part 4 — `configure` Subcommand Flow

### Mode A — Direct Flags
```
configure_command(options)
  │
  ├─ options.list_providers?     → provider_list_command()       → return 0
  ├─ options.list_profiles?      → list all profiles             → return 0
  ├─ options.list_profiles_for?  → filter by provider            → return 0
  ├─ options.create_profile?     → provider_create_command()     → return 0
  ├─ options.edit_profile?       → provider_edit_command()       → return 0
  ├─ options.delete_profile?     → provider_delete_command()     → return 0
  └─ options.activate_profile?   → provider_activate_command()   → return 0
       (no flags matched)        → launch Mode B wizard
```

### Mode B — Interactive Wizard
```
1. ensure_providers()
2. questionary.select("Choose a provider", choices=[...registered providers...])
3. questionary.text("Profile name", default="default")
4. provider_create_command(provider_id, profile_name, interactive=True)
5. questionary.confirm("Activate this profile now?", default=True)
   └─ Yes → provider_activate_command(provider_id, profile_name)
6. provider_status_command()   # Show final status
```

---

## Part 5 — GUI Menu Integration

### Updated `--gui` Main Loop (excerpt)
```python
MENU_CHOICES = [
    "📄 Generate documentation",
    "🤖 AI Providers",
    "❌ Exit"
]

choice = questionary.select("Select action:", choices=MENU_CHOICES).ask()

if choice == "🤖 AI Providers":
    try:
        provider_status_command()
        action = questionary.select(
            "AI Providers",
            choices=["⚙️ Run guided setup", "↩ Back"]
        ).ask()
        if action == "⚙️ Run guided setup":
            configure_command(ConfigureOptions())
    except KeyboardInterrupt:
        pass   # Return to main menu silently
```

---

## Part 6 — .env Key Schema

| Key | Example Value | Written By |
|-----|--------------|-----------|
| `AI_ACTIVE_PROVIDER` | `anthropic` | `provider_activate_command()` |
| `AI_ACTIVE_PROFILE` | `personal` | `provider_activate_command()` |
| `ANTHROPIC_API_KEY` | `sk-ant-...` | `provider_create_command()` |
| `OPENAI_API_KEY` | `sk-...` | `provider_create_command()` |
| `GOOGLE_AI_API_KEY` | `AIza...` | `provider_create_command()` |
| `<ID>_API_KEY` | custom | `provider_create_command()` |
| `<ID>_BASE_URL` | `http://localhost:11434` | Custom/self-hosted providers |

All writes use `dotenv.set_key(dotenv_path, key, value)` to avoid overwriting unrelated variables.

---

## Part 7 — Built-in Provider Registry

```python
BUILTIN_PROVIDERS: list[ProviderDescriptor] = [
    ProviderDescriptor("anthropic",  "Anthropic (Claude)",  "ANTHROPIC",  "claude-3-5-sonnet-20241022", None, True),
    ProviderDescriptor("openai",     "OpenAI (GPT)",        "OPENAI",     "gpt-4o",                     None, True),
    ProviderDescriptor("google_ai",  "Google AI (Gemini)",  "GOOGLE_AI",  "gemini-1.5-pro",             None, True),
    ProviderDescriptor("ollama",     "Ollama (local)",      "OLLAMA",     "llama3",  "http://localhost:11434", False),
    ProviderDescriptor("localai",    "LocalAI (local)",     "LOCALAI",    "gpt-4",   "http://localhost:8080",  False),
]
```

Custom providers are appended at runtime via `register_provider(descriptor: ProviderDescriptor)`.

---

## Security Considerations

- `mask_api_key()` applied at every display boundary before any key value reaches terminal, logs, or `rich` panels
- `dotenv.set_key()` used exclusively for writes — no full-file overwrite
- `.env` should be in `.gitignore` (pre-existing project convention)
- TypeScript never receives raw keys; reads only from `process.env` after `dotenv` load


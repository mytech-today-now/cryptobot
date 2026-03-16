# Specification: Provider Extensibility

## Change ID
`AI-PROVIDER-001`

## Section
`specs/provider-extensibility.md`

---

## Overview

The provider system must support both built-in vendors (Anthropic, OpenAI, Google AI) and user-defined community or self-hosted adapters (Ollama, LocalAI, vLLM, text-generation-webui, paLM-api) using the **same** registration model. Adding a new provider must not require changes to the core abstraction.

**Critical Rule**: Provider registration must not assume a closed list of vendor-owned backends.

---

## Functional Requirements

### FR-1: Open Registration API
- `register_provider(descriptor: ProviderDescriptor)` shall be a public function callable by any `.py` file.
- Built-in providers shall be registered using the same `register_provider()` call used by custom providers.
- The registry shall be a flat dictionary keyed by `provider_id`.

### FR-2: No Closed-List Assumptions
- `resolve_active_provider()` shall look up the active provider ID in `_provider_registry` without any hardcoded list of allowed IDs.
- `provider_list_command()` shall display all registered providers, including custom ones.
- `provider_create_command()`, `provider_edit_command()`, and `provider_activate_command()` shall all work for custom providers via the same code paths as built-in providers.

### FR-3: Built-in Providers as First-Class Registrations
The following providers shall be registered at module load time via `_register_builtin_providers()`:

| `provider_id` | `display_name` | `env_key_prefix` | `default_model` | `base_url` | `requires_api_key` |
|--------------|----------------|-----------------|----------------|-----------|-------------------|
| `anthropic` | Anthropic (Claude) | `ANTHROPIC` | `claude-3-5-sonnet-20241022` | None | True |
| `openai` | OpenAI (GPT) | `OPENAI` | `gpt-4o` | None | True |
| `google_ai` | Google AI (Gemini) | `GOOGLE_AI` | `gemini-1.5-pro` | None | True |
| `ollama` | Ollama (local) | `OLLAMA` | `llama3` | `http://localhost:11434` | False |
| `localai` | LocalAI (local) | `LOCALAI` | `gpt-4` | `http://localhost:8080` | False |

### FR-4: Duplicate ID Handling
- `register_provider()` shall raise `ProviderAlreadyRegisteredError` if the `provider_id` is already registered.
- A `force=True` parameter shall allow override (useful for testing and custom forks of built-in providers).

### FR-5: Custom Provider Requirements
A custom provider needs only a valid `ProviderDescriptor`. No subclassing or interface implementation is required.

### FR-6: Community Adapter Guide
Users wishing to add community adapters shall follow the documented pattern:

```python
# my_custom_providers.py — loaded at startup or via configure
from ai_providers import register_provider, ProviderDescriptor

register_provider(ProviderDescriptor(
    provider_id    = "vllm",
    display_name   = "vLLM (self-hosted)",
    env_key_prefix = "VLLM",
    default_model  = "mistral-7b",
    base_url       = "http://localhost:8000",
    requires_api_key = False,
))
```

Then create a profile:
```
python generate_documentation.py configure --create-profile vllm/local
python generate_documentation.py configure --activate-profile vllm/local
```

---

## Technical Specification

### `register_provider()`

```python
def register_provider(descriptor: ProviderDescriptor, force: bool = False) -> None:
    """
    Register a provider descriptor in the global registry.

    Args:
        descriptor: ProviderDescriptor to register.
        force: If True, overwrite an existing registration. Default False.

    Raises:
        ProviderAlreadyRegisteredError: If provider_id already registered and force=False.
    """
    if descriptor.provider_id in _provider_registry and not force:
        raise ProviderAlreadyRegisteredError(
            f"Provider '{descriptor.provider_id}' is already registered. "
            "Use force=True to override."
        )
    _provider_registry[descriptor.provider_id] = descriptor
```

### Built-in Registration

```python
def _register_builtin_providers() -> None:
    _builtins = [
        ProviderDescriptor("anthropic", "Anthropic (Claude)",   "ANTHROPIC",  "claude-3-5-sonnet-20241022", None,                           True),
        ProviderDescriptor("openai",    "OpenAI (GPT)",         "OPENAI",     "gpt-4o",                     None,                           True),
        ProviderDescriptor("google_ai", "Google AI (Gemini)",   "GOOGLE_AI",  "gemini-1.5-pro",             None,                           True),
        ProviderDescriptor("ollama",    "Ollama (local)",       "OLLAMA",     "llama3",                     "http://localhost:11434",        False),
        ProviderDescriptor("localai",   "LocalAI (local)",      "LOCALAI",    "gpt-4",                      "http://localhost:8080",         False),
    ]
    for descriptor in _builtins:
        register_provider(descriptor)
```

### `provider_create_command()` — Custom Provider Handling

For custom providers with `requires_api_key=False`:
- Skip the API key prompt in interactive mode
- Skip API key validation in non-interactive mode
- Still write `<PROVIDER_ID>_BASE_URL` if `base_url` differs from the registered default

```python
def provider_create_command(provider_id: str, profile_name: str, interactive: bool = True) -> None:
    ensure_providers()
    descriptor = _provider_registry.get(provider_id)
    if not descriptor:
        raise ProviderNotRegisteredError(
            f"Provider '{provider_id}' is not registered. "
            "Register it first with register_provider() or choose a built-in provider."
        )

    if descriptor.requires_api_key:
        if interactive:
            api_key = questionary.password(f"API key for {descriptor.display_name}:").ask()
        else:
            api_key = os.getenv(f"{descriptor.env_key_prefix}_API_KEY", "")
        if not api_key:
            print(f"Error: API key required for {descriptor.display_name}", file=sys.stderr)
            sys.exit(1)
        key_var = f"{descriptor.env_key_prefix}_{profile_name.upper()}_API_KEY"
        set_key(str(DOTENV_PATH), key_var, api_key)

    if descriptor.base_url and interactive:
        base_url = questionary.text(
            "Base URL:", default=descriptor.base_url
        ).ask()
        set_key(str(DOTENV_PATH), f"{descriptor.env_key_prefix}_BASE_URL", base_url)
```

---

## Supported Community Adapters (Reference)

| Adapter | `provider_id` | `base_url` | `requires_api_key` | Source |
|---------|--------------|-----------|-------------------|--------|
| Ollama | `ollama` | `http://localhost:11434` | False | https://github.com/ollama/ollama |
| LocalAI | `localai` | `http://localhost:8080` | False | https://github.com/mudler/LocalAI |
| vLLM | `vllm` | `http://localhost:8000` | False | https://github.com/vllm-project/vllm |
| text-generation-webui | `tgwui` | `http://localhost:5000` | False | https://github.com/oobabooga/text-generation-webui |
| paLM-api | `palm_api` | custom | True | https://github.com/whitead/paLM-api |

These adapters can be registered by users following the Community Adapter Guide pattern above.

---

## Acceptance Criteria

- [ ] `register_provider()` adds any `ProviderDescriptor` to the global registry
- [ ] Built-in providers registered via the same `register_provider()` call as custom providers
- [ ] `resolve_active_provider()` works for any registered `provider_id` without hardcoded lists
- [ ] `provider_list_command()` shows all registered providers including custom ones
- [ ] `register_provider()` raises `ProviderAlreadyRegisteredError` on duplicate ID
- [ ] `register_provider(descriptor, force=True)` successfully overrides an existing registration
- [ ] `provider_create_command()` skips API key prompt for `requires_api_key=False` providers
- [ ] Custom provider registered, profiled, and activated without modifying `ai_providers.py` core logic
- [ ] `ProviderNotRegisteredError` raised when `provider_create_command()` called for unknown provider


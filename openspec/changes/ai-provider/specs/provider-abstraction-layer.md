# Specification: Provider Abstraction Layer

## Change ID
`AI-PROVIDER-001`

## Section
`specs/provider-abstraction-layer.md`

---

## Overview

Define the shared provider interface consumed by all AI-powered commands in both Python and TypeScript runtimes. Command handlers must resolve the active backend through this interface rather than direct, integration-specific logic.

---

## Functional Requirements

### FR-1: Single Import Contract
- `from ai_providers import resolve_active_provider` shall work in any `.py` file in the repo without additional setup beyond importing the module.
- `import { resolveActiveProvider } from './ai_providers'` shall work in any `.ts` file after `dotenv` has loaded `.env`.

### FR-2: Active Provider Resolution
- `resolve_active_provider()` shall read `AI_ACTIVE_PROVIDER` from `.env` and return the matching `ProviderDescriptor`.
- If `AI_ACTIVE_PROVIDER` is unset or references an unregistered provider, raise `ProviderNotConfiguredError` with an actionable message directing the user to run `configure`.

### FR-3: Active Profile Resolution
- `get_active_profile()` shall read `AI_ACTIVE_PROFILE` and `<PROVIDER_ID>_<PROFILE_NAME>_API_KEY` from `.env` and return a `ProviderProfile`.
- If the profile key is absent, raise `ProfileNotFoundError` with an actionable message.

### FR-4: No Duplicated Business Logic
- The TypeScript module shall read the same `.env` keys as the Python module.
- Write-back operations (create, edit, delete, activate) shall not be reimplemented in TypeScript; they delegate to the Python CLI.

### FR-5: Automatic `.env` Loading
- Python: call `dotenv.load_dotenv()` at module import time.
- TypeScript: require callers to load `.env` before invoking resolution functions (standard `dotenv/config` import).

---

## Technical Specification

### Python: `ai_providers.py`

```python
from dotenv import load_dotenv, set_key, dotenv_values
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import os

DOTENV_PATH = Path(__file__).parent / ".env"
load_dotenv(DOTENV_PATH)

@dataclass
class ProviderDescriptor:
    provider_id: str
    display_name: str
    env_key_prefix: str
    default_model: str
    base_url: Optional[str]
    requires_api_key: bool

@dataclass
class ProviderProfile:
    provider_id: str
    profile_name: str
    api_key: str            # raw; use mask_api_key() before display
    model: Optional[str]
    base_url: Optional[str]
    extra: dict = field(default_factory=dict)

_provider_registry: dict[str, ProviderDescriptor] = {}
_initialized: bool = False

def ensure_providers() -> None:
    global _initialized
    if _initialized:
        return
    _register_builtin_providers()
    _initialized = True

def resolve_active_provider() -> ProviderDescriptor:
    ensure_providers()
    provider_id = os.getenv("AI_ACTIVE_PROVIDER")
    if not provider_id or provider_id not in _provider_registry:
        raise ProviderNotConfiguredError(
            "No active AI provider configured. "
            "Run: python generate_documentation.py configure"
        )
    return _provider_registry[provider_id]

def get_active_profile() -> ProviderProfile:
    ensure_providers()
    provider_id = os.getenv("AI_ACTIVE_PROVIDER", "")
    profile_name = os.getenv("AI_ACTIVE_PROFILE", "default")
    key_var = f"{provider_id.upper()}_{profile_name.upper()}_API_KEY"
    api_key = os.getenv(key_var) or os.getenv(f"{provider_id.upper()}_API_KEY", "")
    if not api_key and _provider_registry.get(provider_id, ProviderDescriptor("","","","",None,True)).requires_api_key:
        raise ProfileNotFoundError(
            f"No API key found for profile '{profile_name}' of provider '{provider_id}'. "
            f"Expected env var: {key_var}"
        )
    descriptor = _provider_registry.get(provider_id)
    return ProviderProfile(
        provider_id=provider_id,
        profile_name=profile_name,
        api_key=api_key,
        model=os.getenv(f"{provider_id.upper()}_{profile_name.upper()}_MODEL") or
              (descriptor.default_model if descriptor else None),
        base_url=os.getenv(f"{provider_id.upper()}_BASE_URL") or
                 (descriptor.base_url if descriptor else None),
    )
```

### TypeScript: `ai_providers.ts`

```typescript
import * as dotenv from 'dotenv';
import { resolve } from 'path';
import { spawnSync } from 'child_process';

dotenv.config({ path: resolve(__dirname, '../../.env') });

export interface ProviderDescriptor {
  providerId: string;
  displayName: string;
  envKeyPrefix: string;
  defaultModel: string;
  baseUrl: string | null;
  requiresApiKey: boolean;
}

export interface ProviderProfile {
  providerId: string;
  profileName: string;
  apiKey: string;     // raw; use maskApiKey() before display
  model: string | null;
  baseUrl: string | null;
}

export function resolveActiveProvider(): ProviderDescriptor {
  const providerId = process.env.AI_ACTIVE_PROVIDER;
  if (!providerId) {
    throw new Error(
      'No active AI provider configured. Run: python generate_documentation.py configure'
    );
  }
  // Return a minimal descriptor reconstructed from env keys
  return {
    providerId,
    displayName: process.env[`${providerId.toUpperCase()}_DISPLAY_NAME`] ?? providerId,
    envKeyPrefix: providerId.toUpperCase(),
    defaultModel: process.env[`${providerId.toUpperCase()}_DEFAULT_MODEL`] ?? '',
    baseUrl: process.env[`${providerId.toUpperCase()}_BASE_URL`] ?? null,
    requiresApiKey: true,
  };
}

export function getActiveProfile(): ProviderProfile {
  const providerId = process.env.AI_ACTIVE_PROVIDER ?? '';
  const profileName = process.env.AI_ACTIVE_PROFILE ?? 'default';
  const keyVar = `${providerId.toUpperCase()}_${profileName.toUpperCase()}_API_KEY`;
  const apiKey = process.env[keyVar] ?? process.env[`${providerId.toUpperCase()}_API_KEY`] ?? '';
  return {
    providerId,
    profileName,
    apiKey,
    model: process.env[`${providerId.toUpperCase()}_${profileName.toUpperCase()}_MODEL`] ?? null,
    baseUrl: process.env[`${providerId.toUpperCase()}_BASE_URL`] ?? null,
  };
}

export function maskApiKey(key: string): string {
  if (!key || key.length < 8) return '***';
  return `${key.slice(0, 3)}***...***`;
}
```

---

## Error Types

```python
class ProviderNotConfiguredError(RuntimeError): pass
class ProfileNotFoundError(RuntimeError): pass
class ProviderAlreadyRegisteredError(ValueError): pass
class ProviderNotRegisteredError(KeyError): pass
```

---

## Acceptance Criteria

- [ ] `from ai_providers import resolve_active_provider` importable in any `.py` without error
- [ ] `import { resolveActiveProvider } from './ai_providers'` works in `.ts` after `dotenv` loads
- [ ] Both helpers read `AI_ACTIVE_PROVIDER` and `AI_ACTIVE_PROFILE` from the same repo-root `.env`
- [ ] Neither module duplicates credential-write business logic
- [ ] `ProviderNotConfiguredError` raised (not `KeyError`) when provider unset
- [ ] `ProfileNotFoundError` raised (not `KeyError`) when profile key missing
- [ ] `ensure_providers()` is idempotent (safe to call multiple times)


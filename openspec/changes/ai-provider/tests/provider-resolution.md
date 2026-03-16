# Test Specification: Provider Resolution

## Change ID
`AI-PROVIDER-001`

## Section
`tests/provider-resolution.md`

---

## Overview

Tests for `resolve_active_provider()`, `get_active_profile()`, and the TypeScript equivalents `resolveActiveProvider()` and `getActiveProfile()`. Covers happy paths, error cases, and `.env` read behavior.

---

## Test Suite: Python — `resolve_active_provider()`

### TC-RES-PY-01: Returns descriptor for registered active provider
**Preconditions**:
- `AI_ACTIVE_PROVIDER=anthropic` in environment
- `anthropic` registered via `ensure_providers()`
**Steps**:
1. Call `resolve_active_provider()`
**Expected**:
- Returns `ProviderDescriptor` with `provider_id="anthropic"`
- `display_name="Anthropic (Claude)"`
- `requires_api_key=True`

---

### TC-RES-PY-02: Raises `ProviderNotConfiguredError` when `AI_ACTIVE_PROVIDER` unset
**Preconditions**: `AI_ACTIVE_PROVIDER` not in environment
**Steps**:
1. Call `resolve_active_provider()`
**Expected**:
- Raises `ProviderNotConfiguredError`
- Error message contains `"configure"` as a recovery hint
- Does NOT raise `KeyError` or `ValueError`

---

### TC-RES-PY-03: Raises `ProviderNotConfiguredError` for unregistered provider ID
**Preconditions**: `AI_ACTIVE_PROVIDER=unknown_provider` in environment
**Steps**:
1. Call `resolve_active_provider()`
**Expected**:
- Raises `ProviderNotConfiguredError`
- Error message contains the unregistered ID `"unknown_provider"`

---

### TC-RES-PY-04: `resolve_active_provider()` calls `ensure_providers()` internally
**Steps**:
1. Do NOT call `ensure_providers()` manually
2. Set `AI_ACTIVE_PROVIDER=anthropic`
3. Call `resolve_active_provider()`
**Expected**:
- `anthropic` descriptor returned successfully
- `_initialized` set to `True` after call

---

## Test Suite: Python — `get_active_profile()`

### TC-RES-PY-05: Returns profile with named key when `AI_ACTIVE_PROFILE` set
**Preconditions**:
- `AI_ACTIVE_PROVIDER=anthropic`
- `AI_ACTIVE_PROFILE=personal`
- `ANTHROPIC_PERSONAL_API_KEY=sk-ant-test123`
**Steps**:
1. Call `get_active_profile()`
**Expected**:
- Returns `ProviderProfile` with `provider_id="anthropic"`, `profile_name="personal"`
- `api_key="sk-ant-test123"` (raw value internally)

---

### TC-RES-PY-06: Falls back to default key when profile key missing
**Preconditions**:
- `AI_ACTIVE_PROVIDER=anthropic`
- `AI_ACTIVE_PROFILE=personal`
- `ANTHROPIC_PERSONAL_API_KEY` NOT set
- `ANTHROPIC_API_KEY=sk-ant-fallback`
**Steps**:
1. Call `get_active_profile()`
**Expected**:
- Returns profile with `api_key="sk-ant-fallback"`
- No error raised

---

### TC-RES-PY-07: Raises `ProfileNotFoundError` when no key available for key-requiring provider
**Preconditions**:
- `AI_ACTIVE_PROVIDER=anthropic`
- `AI_ACTIVE_PROFILE=personal`
- Neither `ANTHROPIC_PERSONAL_API_KEY` nor `ANTHROPIC_API_KEY` set
**Steps**:
1. Call `get_active_profile()`
**Expected**:
- Raises `ProfileNotFoundError`
- Error message contains the expected env var name `ANTHROPIC_PERSONAL_API_KEY`

---

### TC-RES-PY-08: Returns profile without API key for `requires_api_key=False` provider
**Preconditions**:
- `AI_ACTIVE_PROVIDER=ollama`
- `OLLAMA_API_KEY` NOT set
**Steps**:
1. Call `get_active_profile()`
**Expected**:
- Returns `ProviderProfile` with empty `api_key`
- No `ProfileNotFoundError` raised

---

### TC-RES-PY-09: Profile uses registered default model when model key not in `.env`
**Preconditions**:
- `AI_ACTIVE_PROVIDER=anthropic`, `AI_ACTIVE_PROFILE=default`
- `ANTHROPIC_API_KEY=sk-ant-test`
- `ANTHROPIC_DEFAULT_MODEL` NOT set
**Steps**:
1. Call `get_active_profile()`
**Expected**:
- `profile.model == "claude-3-5-sonnet-20241022"` (from `ProviderDescriptor.default_model`)

---

## Test Suite: Python — `.env` Read Behavior

### TC-RES-PY-10: Missing `.env` logs warning and does not raise
**Preconditions**: `.env` file does not exist
**Steps**:
1. Import `ai_providers`
**Expected**:
- Module imports without error
- Warning logged (not exception)

---

### TC-RES-PY-11: `load_dotenv()` called at module import time
**Steps**:
1. Patch `dotenv.load_dotenv`
2. Import `ai_providers`
**Expected**:
- `load_dotenv` called exactly once during import with `DOTENV_PATH`

---

## Test Suite: TypeScript — `resolveActiveProvider()`

### TC-RES-TS-01: Returns descriptor-like object for set `AI_ACTIVE_PROVIDER`
**Preconditions**: `process.env.AI_ACTIVE_PROVIDER = "openai"`
**Steps**:
1. Call `resolveActiveProvider()`
**Expected**:
- Returns object with `providerId: "openai"`
- `envKeyPrefix: "OPENAI"`

---

### TC-RES-TS-02: Throws `Error` when `AI_ACTIVE_PROVIDER` unset
**Preconditions**: `AI_ACTIVE_PROVIDER` not in `process.env`
**Steps**:
1. Call `resolveActiveProvider()`
**Expected**:
- Throws `Error` with message containing `"configure"` as a recovery hint
- Does NOT return `undefined`

---

### TC-RES-TS-03: `getActiveProfile()` reads named profile key
**Preconditions**:
- `process.env.AI_ACTIVE_PROVIDER = "anthropic"`
- `process.env.AI_ACTIVE_PROFILE = "work"`
- `process.env.ANTHROPIC_WORK_API_KEY = "sk-ant-ts-test"`
**Steps**:
1. Call `getActiveProfile()`
**Expected**:
- Returns `{ providerId: "anthropic", profileName: "work", apiKey: "sk-ant-ts-test" }`

---

### TC-RES-TS-04: TypeScript and Python read same `AI_ACTIVE_PROVIDER` key
**Preconditions**: `.env` contains `AI_ACTIVE_PROVIDER=google_ai`
**Steps**:
1. Load `.env` in Python; call `resolve_active_provider()`
2. Load `.env` in TypeScript; call `resolveActiveProvider()`
**Expected**:
- Both return provider ID `"google_ai"`
- No discrepancy between runtimes

---

## Test Implementation Notes

```python
# pytest example for Python resolution tests
import pytest
import os
from unittest.mock import patch

@pytest.fixture
def anthropic_env(monkeypatch, clean_registry):
    monkeypatch.setenv("AI_ACTIVE_PROVIDER", "anthropic")
    monkeypatch.setenv("AI_ACTIVE_PROFILE", "personal")
    monkeypatch.setenv("ANTHROPIC_PERSONAL_API_KEY", "sk-ant-test123")
    yield

def test_resolve_active_provider_happy_path(anthropic_env):
    from ai_providers import resolve_active_provider
    descriptor = resolve_active_provider()
    assert descriptor.provider_id == "anthropic"
    assert descriptor.requires_api_key is True

def test_resolve_raises_not_configured_when_unset(clean_registry, monkeypatch):
    monkeypatch.delenv("AI_ACTIVE_PROVIDER", raising=False)
    from ai_providers import resolve_active_provider, ProviderNotConfiguredError
    with pytest.raises(ProviderNotConfiguredError):
        resolve_active_provider()
```

```typescript
// Jest example for TypeScript resolution tests
import { resolveActiveProvider, getActiveProfile } from '../ai_providers';

describe('resolveActiveProvider', () => {
  it('returns descriptor for set AI_ACTIVE_PROVIDER', () => {
    process.env.AI_ACTIVE_PROVIDER = 'openai';
    const descriptor = resolveActiveProvider();
    expect(descriptor.providerId).toBe('openai');
  });

  it('throws when AI_ACTIVE_PROVIDER is unset', () => {
    delete process.env.AI_ACTIVE_PROVIDER;
    expect(() => resolveActiveProvider()).toThrow(/configure/i);
  });
});
```


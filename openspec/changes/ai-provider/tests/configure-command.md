# Test Specification: `configure` Command

## Change ID
`AI-PROVIDER-001`

## Section
`tests/configure-command.md`

---

## Overview

Tests for the `configure` subcommand covering Mode A (direct flags) and Mode B (interactive wizard). All tests target `ai_providers.py` functions and the argparse integration in `generate_documentation.py`.

---

## Test Suite: Mode A — Direct Flags

### TC-CFG-A-01: `--list-providers` prints rich table
**Preconditions**: 5 built-in providers registered via `ensure_providers()`
**Steps**:
1. Call `configure_command(ConfigureOptions(list_providers=True))`
**Expected**:
- Rich table printed to stdout with columns: ID, Display Name, Status, Profile Count
- No wizard prompt shown
- Exit code `0`

---

### TC-CFG-A-02: `--list-profiles` prints all profiles
**Preconditions**: `.env` contains `ANTHROPIC_PERSONAL_API_KEY` and `OPENAI_WORK_API_KEY`
**Steps**:
1. Call `configure_command(ConfigureOptions(list_profiles=True))`
**Expected**:
- Both profiles listed in output
- No API key values visible in output
- Exit code `0`

---

### TC-CFG-A-03: `--list-profiles-for-provider` filters by provider
**Preconditions**: Profiles exist for `anthropic` and `openai`
**Steps**:
1. Call `configure_command(ConfigureOptions(list_profiles_for_provider="anthropic"))`
**Expected**:
- Only `anthropic` profiles listed
- `openai` profiles not shown
- Exit code `0`

---

### TC-CFG-A-04: `--create-profile` creates profile non-interactively
**Preconditions**: `ANTHROPIC_API_KEY=sk-ant-test` in environment
**Steps**:
1. Call `configure_command(ConfigureOptions(create_profile="anthropic/work"))`
**Expected**:
- `ANTHROPIC_WORK_API_KEY` written to `.env` via `set_key()`
- Confirmation rich panel displayed
- Exit code `0`

---

### TC-CFG-A-05: `--edit-profile` updates profile field
**Preconditions**: `ANTHROPIC_PERSONAL_API_KEY` exists in `.env`
**Steps**:
1. Mock `questionary.text` to return a new model name
2. Call `configure_command(ConfigureOptions(edit_profile="anthropic/personal"))`
**Expected**:
- `ANTHROPIC_PERSONAL_MODEL` updated in `.env`
- Other `.env` keys unchanged
- Exit code `0`

---

### TC-CFG-A-06: `--delete-profile` removes profile keys after confirmation
**Preconditions**: `ANTHROPIC_PERSONAL_API_KEY` exists in `.env`
**Steps**:
1. Mock `questionary.confirm` to return `True`
2. Call `configure_command(ConfigureOptions(delete_profile="anthropic/personal"))`
**Expected**:
- `ANTHROPIC_PERSONAL_API_KEY` removed from `.env`
- `ANTHROPIC_PERSONAL_MODEL` removed from `.env` (if present)
- No other keys removed
- Exit code `0`

---

### TC-CFG-A-07: `--delete-profile` aborts if user declines confirmation
**Preconditions**: `ANTHROPIC_PERSONAL_API_KEY` exists in `.env`
**Steps**:
1. Mock `questionary.confirm` to return `False`
2. Call `configure_command(ConfigureOptions(delete_profile="anthropic/personal"))`
**Expected**:
- `.env` unchanged
- "Aborted" or similar message printed
- Exit code `0`

---

### TC-CFG-A-08: `--activate-profile` writes both active keys to `.env`
**Preconditions**: `ANTHROPIC_PERSONAL_API_KEY` exists in `.env`
**Steps**:
1. Call `configure_command(ConfigureOptions(activate_profile="anthropic/personal"))`
**Expected**:
- `AI_ACTIVE_PROVIDER=anthropic` written to `.env`
- `AI_ACTIVE_PROFILE=personal` written to `.env`
- Exit code `0`

---

## Test Suite: `parse_provider_profile_arg()`

### TC-CFG-PARSE-01: Valid slash-separated value
**Input**: `"anthropic/personal"`
**Expected**: Returns `("anthropic", "personal")`

---

### TC-CFG-PARSE-02: Multiple slashes — split on first only
**Input**: `"anthropic/personal/extra"`
**Expected**: Returns `("anthropic", "personal/extra")`

---

### TC-CFG-PARSE-03: Missing slash exits with clear error
**Input**: `"anthropicpersonal"`
**Expected**:
- Prints error message containing `"expected 'provider_id/profile_name'"` to stderr
- `sys.exit(1)` called

---

### TC-CFG-PARSE-04: Empty string exits with clear error
**Input**: `""`
**Expected**:
- Prints error message to stderr
- `sys.exit(1)` called

---

## Test Suite: Mode B — Interactive Wizard

### TC-CFG-B-01: Wizard presents provider list
**Preconditions**: 5 built-in providers registered
**Steps**:
1. Mock `questionary.select` to capture choices
2. Call `configure_command(ConfigureOptions())` (no flags)
**Expected**:
- `questionary.select` called with 5 provider choices
- Each choice contains provider ID and display name

---

### TC-CFG-B-02: Wizard defaults profile name to "default"
**Steps**:
1. Mock `questionary.select` to return `"anthropic — Anthropic (Claude)"`
2. Mock `questionary.text` to capture default and return `"default"`
**Expected**:
- `questionary.text` called with `default="default"`

---

### TC-CFG-B-03: Wizard activates profile when user confirms
**Steps**:
1. Mock select → `"anthropic — Anthropic (Claude)"`
2. Mock text → `"personal"`
3. Mock password → `"sk-ant-test"`
4. Mock confirm → `True`
**Expected**:
- `AI_ACTIVE_PROVIDER=anthropic` written to `.env`
- `AI_ACTIVE_PROFILE=personal` written to `.env`
- `provider_status_command()` called at end

---

### TC-CFG-B-04: Wizard skips activation when user declines
**Steps**:
1. Mock select, text, password as above
2. Mock confirm → `False`
**Expected**:
- `AI_ACTIVE_PROVIDER` and `AI_ACTIVE_PROFILE` NOT written to `.env`
- `provider_status_command()` still called at end

---

## Test Suite: `ensure_providers()` Guard

### TC-CFG-ENSURE-01: `ensure_providers()` is idempotent
**Steps**:
1. Call `ensure_providers()` three times in sequence
**Expected**:
- `_register_builtin_providers()` called exactly once
- No `ProviderAlreadyRegisteredError` raised

---

### TC-CFG-ENSURE-02: Registry contains 5 built-in providers after `ensure_providers()`
**Steps**:
1. Call `ensure_providers()`
2. Inspect `_provider_registry`
**Expected**:
- Keys: `anthropic`, `openai`, `google_ai`, `ollama`, `localai`
- Each maps to a valid `ProviderDescriptor`

---

## Test Implementation Notes

```python
# Example test structure (pytest)
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

@pytest.fixture
def clean_registry(monkeypatch):
    """Reset provider registry between tests."""
    import ai_providers
    monkeypatch.setattr(ai_providers, '_provider_registry', {})
    monkeypatch.setattr(ai_providers, '_initialized', False)
    yield

@pytest.fixture
def temp_dotenv(tmp_path, monkeypatch):
    """Provide a temporary .env file."""
    import ai_providers
    env_file = tmp_path / ".env"
    env_file.write_text("")
    monkeypatch.setattr(ai_providers, 'DOTENV_PATH', env_file)
    return env_file

def test_parse_valid_slash(clean_registry):
    from ai_providers import parse_provider_profile_arg
    assert parse_provider_profile_arg("anthropic/personal") == ("anthropic", "personal")

def test_activate_profile_writes_env(clean_registry, temp_dotenv):
    from ai_providers import provider_activate_command
    provider_activate_command("anthropic", "personal")
    content = temp_dotenv.read_text()
    assert "AI_ACTIVE_PROVIDER=anthropic" in content
    assert "AI_ACTIVE_PROFILE=personal" in content
```


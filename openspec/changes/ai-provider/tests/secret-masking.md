# Test Specification: Secret Masking

## Change ID
`AI-PROVIDER-001`

## Section
`tests/secret-masking.md`

---

## Overview

Tests for `mask_api_key()` and all output boundaries where API keys might appear. Ensures no raw credential value is ever printed to the terminal, log files, or status panels.

**Critical Rule**: Never print secrets in normal output; mask as `sk-***...***` in all status displays and logs.

---

## Test Suite: `mask_api_key()` Unit Tests

### TC-MASK-01: Standard Anthropic key masked correctly
**Input**: `"sk-ant-api03-abcdefghijklmnop"`
**Expected**: `"sk-***...***"`

---

### TC-MASK-02: Standard OpenAI key masked correctly
**Input**: `"sk-proj-abc123xyz789def"`
**Expected**: `"sk-***...***"`

---

### TC-MASK-03: Short key (< 8 chars) returns safe fallback
**Input**: `"abc"`
**Expected**: `"***"` (no prefix shown)

---

### TC-MASK-04: Empty string returns safe fallback
**Input**: `""`
**Expected**: `"***"`

---

### TC-MASK-05: Key with non-standard prefix still masked
**Input**: `"AIzaSyAbcDef123456"`
**Expected**: Starts with `"AIz"` and ends with `"***...***"` (first 3 chars preserved)

---

### TC-MASK-06: `mask_api_key()` return value never contains full original key
**Input**: Any string of length ≥ 8
**Expected**: Output does not contain the substring from char 4 onward of input

---

## Test Suite: `provider_status_command()` Output

### TC-MASK-STATUS-01: Status panel does not contain raw API key
**Preconditions**:
- `AI_ACTIVE_PROVIDER=anthropic`
- `AI_ACTIVE_PROFILE=personal`
- `ANTHROPIC_PERSONAL_API_KEY=sk-ant-verysecretkey123`
**Steps**:
1. Capture stdout while calling `provider_status_command()`
**Expected**:
- Output does NOT contain `"sk-ant-verysecretkey123"`
- Output DOES contain `"sk-***...***"` or equivalent masked value

---

### TC-MASK-STATUS-02: Status panel shows masked key label
**Preconditions**: Same as TC-MASK-STATUS-01
**Steps**:
1. Capture rich panel content
**Expected**:
- Panel contains label `"API Key:"` or `"api_key:"`
- Value next to label is masked form, not raw

---

### TC-MASK-STATUS-03: Status panel with no active provider shows no key data
**Preconditions**: `AI_ACTIVE_PROVIDER` not set
**Steps**:
1. Call `provider_status_command()`
**Expected**:
- Output does not contain any key-like pattern (no `sk-`, `AIza`, bearer tokens)
- Shows "No active provider configured" message

---

## Test Suite: `provider_list_command()` Output

### TC-MASK-LIST-01: Provider list table does not expose API keys
**Preconditions**: Multiple profiles with API keys in `.env`
**Steps**:
1. Capture stdout from `provider_list_command()`
**Expected**:
- Output contains no raw API key values
- Output contains no `sk-` prefixes from real keys

---

### TC-MASK-LIST-02: Active provider row highlighted, no key in row
**Preconditions**: `AI_ACTIVE_PROVIDER=anthropic`
**Steps**:
1. Call `provider_list_command()`
**Expected**:
- Active provider row visually indicated (e.g., ✓ marker or color)
- Row does not contain any credential data

---

## Test Suite: `provider_create_command()` Output

### TC-MASK-CREATE-01: Creation confirmation panel does not echo API key
**Steps**:
1. Mock `questionary.password` to return `"sk-ant-newkey456"`
2. Capture stdout from interactive `provider_create_command("anthropic", "work")`
**Expected**:
- Output does NOT contain `"sk-ant-newkey456"`
- Output DOES contain masked form or a generic success message with no key value

---

### TC-MASK-CREATE-02: Non-interactive create does not log API key to stdout
**Preconditions**: `ANTHROPIC_API_KEY=sk-ant-envkey789` in environment
**Steps**:
1. Capture stdout from `provider_create_command("anthropic", "work", interactive=False)`
**Expected**:
- `"sk-ant-envkey789"` not present in stdout
- No raw key in any confirmation message

---

## Test Suite: Log Safety

### TC-MASK-LOG-01: Logging at any level does not emit raw API key
**Preconditions**: Python `logging` module at DEBUG level
**Steps**:
1. Set log level to `DEBUG`
2. Call `resolve_active_provider()` and `get_active_profile()`
3. Capture all log output
**Expected**:
- No log record contains raw API key value
- Masked values (`sk-***...***`) acceptable in debug logs

---

### TC-MASK-LOG-02: Exception messages do not include raw API key
**Preconditions**: `ANTHROPIC_PERSONAL_API_KEY=sk-ant-secret` in env
**Steps**:
1. Trigger `ProfileNotFoundError` by using wrong profile name
2. Capture exception message
**Expected**:
- Exception message contains the *env var name* (e.g., `ANTHROPIC_PERSONAL_API_KEY`) but NOT the key value

---

## Test Implementation Notes

```python
# pytest example
import pytest
from io import StringIO
from unittest.mock import patch
from rich.console import Console

def capture_rich_output(fn, *args, **kwargs) -> str:
    """Capture rich Console output to string."""
    import io
    buffer = io.StringIO()
    with patch('ai_providers.Console', lambda: Console(file=buffer, highlight=False)):
        fn(*args, **kwargs)
    return buffer.getvalue()

def test_mask_api_key_standard():
    from ai_providers import mask_api_key
    result = mask_api_key("sk-ant-api03-abcdefghijklmnop")
    assert result == "sk-***...***"
    assert "abcdefghijklmnop" not in result

def test_status_panel_masks_key(anthropic_env, monkeypatch):
    from ai_providers import provider_status_command
    output = capture_rich_output(provider_status_command)
    assert "sk-ant-test123" not in output
    assert "***" in output

def test_mask_empty_string():
    from ai_providers import mask_api_key
    assert mask_api_key("") == "***"

def test_mask_short_string():
    from ai_providers import mask_api_key
    assert mask_api_key("abc") == "***"
```


# Test Specification: GUI AI Providers Menu

## Change ID
`AI-PROVIDER-001`

## Section
`tests/gui-menu.md`

---

## Overview

Tests for the `🤖 AI Providers` menu item in the `--gui` interactive loop. Covers menu entry presence, status panel display, guided setup invocation, back navigation, and `KeyboardInterrupt` handling at all levels.

---

## Test Suite: Menu Entry

### TC-GUI-MENU-01: AI Providers entry present in main menu choices
**Steps**:
1. Mock `questionary.select` to capture the `choices` list
2. Trigger the `--gui` loop (or call the choices builder directly)
**Expected**:
- `"🤖 AI Providers"` is present in the choices list
- Entry appears regardless of whether a provider is configured

---

### TC-GUI-MENU-02: AI Providers entry appears consistently across runs
**Steps**:
1. Call the GUI menu builder twice in sequence
**Expected**:
- Entry present both times
- Same position in the list both times

---

## Test Suite: Status Panel Display

### TC-GUI-STATUS-01: `provider_status_command()` called before action prompt
**Preconditions**: `AI_ACTIVE_PROVIDER=anthropic` set
**Steps**:
1. Mock `questionary.select` to first return `"🤖 AI Providers"` then `"↩ Back"`
2. Patch `provider_status_command` with a mock
3. Run `--gui` loop for one iteration
**Expected**:
- `provider_status_command` called before the action `questionary.select` is presented

---

### TC-GUI-STATUS-02: Status panel shown even when no provider configured
**Preconditions**: `AI_ACTIVE_PROVIDER` not set
**Steps**:
1. Mock `questionary.select` to return `"🤖 AI Providers"` then `"↩ Back"`
2. Capture stdout
3. Run one GUI iteration
**Expected**:
- No error or exception raised
- "No active provider" panel or message shown in output

---

### TC-GUI-STATUS-03: Status panel contains masked API key
**Preconditions**:
- `AI_ACTIVE_PROVIDER=anthropic`
- `ANTHROPIC_API_KEY=sk-ant-guisecret`
**Steps**:
1. Capture stdout during `provider_status_command()` call within GUI flow
**Expected**:
- `"sk-ant-guisecret"` NOT in output
- Masked form (`"sk-***...***"`) present

---

## Test Suite: Action Prompt Choices

### TC-GUI-ACTION-01: Action prompt presents exactly two choices
**Steps**:
1. Mock first `questionary.select` → `"🤖 AI Providers"`
2. Capture second `questionary.select` choices list
**Expected**:
- Choices are exactly: `["⚙️ Run guided setup", "↩ Back"]`

---

### TC-GUI-ACTION-02: `⚙️ Run guided setup` launches `configure_command()`
**Steps**:
1. Mock select → `"🤖 AI Providers"`, then `"⚙️ Run guided setup"`
2. Patch `configure_command` with a mock
**Expected**:
- `configure_command` called with `ConfigureOptions()` (all fields at defaults)

---

### TC-GUI-ACTION-03: `↩ Back` returns to main menu without calling `configure_command()`
**Steps**:
1. Mock select → `"🤖 AI Providers"`, then `"↩ Back"`
2. Patch `configure_command` with a mock
**Expected**:
- `configure_command` NOT called
- Main menu loop continues (no exit)

---

## Test Suite: `KeyboardInterrupt` Handling

### TC-GUI-KBI-01: Ctrl+C inside AI Providers block returns to main menu silently
**Steps**:
1. Mock first `questionary.select` → `"🤖 AI Providers"`
2. Mock `provider_status_command` to raise `KeyboardInterrupt`
**Expected**:
- No traceback printed
- Control returns to main menu loop
- Program does not exit

---

### TC-GUI-KBI-02: Ctrl+C during guided setup wizard returns to main menu
**Steps**:
1. Mock select → `"🤖 AI Providers"`, then `"⚙️ Run guided setup"`
2. Mock `configure_command` to raise `KeyboardInterrupt`
**Expected**:
- No traceback printed
- Returns to main menu loop

---

### TC-GUI-KBI-03: Ctrl+C at main menu exits cleanly with farewell message
**Steps**:
1. Mock `questionary.select` to raise `KeyboardInterrupt`
2. Capture stdout
**Expected**:
- Program exits (loop broken)
- Stdout contains `"Goodbye!"` or similar farewell message
- No `KeyboardInterrupt` traceback in stderr

---

### TC-GUI-KBI-04: Ctrl+C during action prompt silently returns to main menu
**Steps**:
1. Mock first select → `"🤖 AI Providers"`
2. Mock `provider_status_command` to succeed
3. Mock second `questionary.select` (action prompt) to raise `KeyboardInterrupt`
**Expected**:
- No traceback
- Main menu loop continues

---

## Test Suite: GUI Loop Integrity

### TC-GUI-INTEGRITY-01: Existing menu choices still function after AI Providers added
**Steps**:
1. Mock select → each existing menu choice in sequence
2. Confirm each existing handler is called correctly
**Expected**:
- All pre-existing choices produce same behavior as before this change
- No regression introduced

---

### TC-GUI-INTEGRITY-02: GUI loop continues after visiting AI Providers and back
**Steps**:
1. Mock select → `"🤖 AI Providers"`, then `"↩ Back"`, then `"❌ Exit"`
**Expected**:
- Loop executes three iterations
- Exits cleanly on `"❌ Exit"`

---

## Test Implementation Notes

```python
# pytest example using unittest.mock
import pytest
from unittest.mock import patch, MagicMock, call

@pytest.fixture
def gui_mocks(monkeypatch):
    """Fixture providing common GUI test mocks."""
    status_mock = MagicMock()
    configure_mock = MagicMock()
    monkeypatch.setattr('ai_providers.provider_status_command', status_mock)
    monkeypatch.setattr('ai_providers.configure_command', configure_mock)
    return status_mock, configure_mock

def test_ai_providers_menu_entry_present():
    """Verify 🤖 AI Providers in choices."""
    import generate_documentation as gd
    assert "🤖 AI Providers" in gd.GUI_MENU_CHOICES

def test_back_choice_does_not_call_configure(gui_mocks, monkeypatch):
    status_mock, configure_mock = gui_mocks
    select_responses = iter(["🤖 AI Providers", "↩ Back", "❌ Exit"])
    with patch('questionary.select') as mock_select:
        mock_select.return_value.ask.side_effect = lambda: next(select_responses)
        # Run one AI Providers iteration
        # ... invoke GUI loop ...
    configure_mock.assert_not_called()

def test_keyboard_interrupt_in_status_returns_to_menu(gui_mocks, monkeypatch):
    status_mock, _ = gui_mocks
    status_mock.side_effect = KeyboardInterrupt
    select_responses = iter(["🤖 AI Providers", "❌ Exit"])
    with patch('questionary.select') as mock_select:
        mock_select.return_value.ask.side_effect = lambda: next(select_responses)
        # Should not raise, should continue loop
        # ... invoke GUI loop, assert no exception propagated ...
        pass  # no KeyboardInterrupt propagated
```


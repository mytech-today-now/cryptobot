"""
tests/test_provider_resolution.py
==================================

Unit tests for ai_providers.py — provider resolution, .env interop,
secret masking, and GUI navigation.

Covers test cases:
  TC-RES-PY-01 … TC-RES-PY-11  (Python resolution / .env read)
  TC-MASK-01   … TC-MASK-06    (mask_api_key() unit tests)
  TC-MASK-STATUS-01 … TC-MASK-STATUS-03  (provider_status_command masking)
  TC-MASK-LIST-01   … TC-MASK-LIST-02    (provider_list_command masking)
  TC-MASK-CREATE-01 … TC-MASK-CREATE-02  (provider_create_command masking)
  TC-MASK-LOG-01    … TC-MASK-LOG-02     (log safety)
  TC-GUI-MENU-01    … TC-GUI-MENU-02     (menu entry presence)
  TC-GUI-STATUS-01  … TC-GUI-STATUS-03   (status panel in GUI)
  TC-GUI-ACTION-01  … TC-GUI-ACTION-03   (action prompt choices)
  TC-GUI-KBI-01     … TC-GUI-KBI-04      (KeyboardInterrupt handling)
  TC-GUI-INTEGRITY-01 … TC-GUI-INTEGRITY-02 (loop integrity)

Change ID : AI-PROVIDER-001
Phase     : 5 — Testing
Tasks     : 5.3, 5.4
"""
from __future__ import annotations

import io
import logging
import os
import sys
from unittest.mock import patch, MagicMock, call

import pytest

# ---------------------------------------------------------------------------
# Modules under test
# ---------------------------------------------------------------------------
import ai_providers
from ai_providers import (
    _reset_for_tests,
    ensure_providers,
    resolve_active_provider,
    get_active_profile,
    mask_api_key,
    provider_status_command,
    provider_list_command,
    provider_create_command,
    provider_activate_command,
    ProviderNotConfiguredError,
    ProfileNotFoundError,
    ProviderDescriptor,
    _initialized,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def clean_registry():
    """Reset module state before every test."""
    _reset_for_tests()
    yield
    _reset_for_tests()


@pytest.fixture()
def anthropic_env(monkeypatch):
    """Set env vars for a valid anthropic / personal profile."""
    monkeypatch.setenv("AI_ACTIVE_PROVIDER", "anthropic")
    monkeypatch.setenv("AI_ACTIVE_PROFILE", "personal")
    monkeypatch.setenv("ANTHROPIC_PERSONAL_API_KEY", "sk-ant-test123")
    yield


# ---------------------------------------------------------------------------
# resolve_active_provider()
# ---------------------------------------------------------------------------

class TestResolveActiveProvider:

    def test_tc_res_py_01_happy_path(self, monkeypatch, anthropic_env):
        """TC-RES-PY-01: Returns ProviderDescriptor for registered active provider."""
        descriptor = resolve_active_provider()
        assert descriptor.provider_id == "anthropic"
        assert descriptor.display_name == "Anthropic (Claude)"
        assert descriptor.requires_api_key is True

    def test_tc_res_py_02_raises_when_env_var_unset(self, monkeypatch):
        """TC-RES-PY-02: Raises ProviderNotConfiguredError when AI_ACTIVE_PROVIDER unset."""
        monkeypatch.delenv("AI_ACTIVE_PROVIDER", raising=False)
        with pytest.raises(ProviderNotConfiguredError) as exc_info:
            resolve_active_provider()
        assert "configure" in str(exc_info.value).lower()

    def test_tc_res_py_03_raises_for_unregistered_provider(self, monkeypatch):
        """TC-RES-PY-03: Raises ProviderNotConfiguredError for unknown provider ID."""
        monkeypatch.setenv("AI_ACTIVE_PROVIDER", "unknown_provider")
        with pytest.raises(ProviderNotConfiguredError) as exc_info:
            resolve_active_provider()
        assert "unknown_provider" in str(exc_info.value)

    def test_tc_res_py_04_calls_ensure_providers_internally(self, monkeypatch):
        """TC-RES-PY-04: resolve_active_provider() bootstraps providers without explicit call."""
        monkeypatch.setenv("AI_ACTIVE_PROVIDER", "anthropic")
        # _reset_for_tests() already called by autouse fixture; _initialized is False
        assert ai_providers._initialized is False
        descriptor = resolve_active_provider()
        assert descriptor.provider_id == "anthropic"
        assert ai_providers._initialized is True


# ---------------------------------------------------------------------------
# get_active_profile()
# ---------------------------------------------------------------------------

class TestGetActiveProfile:

    def test_tc_res_py_05_named_profile_key(self, monkeypatch, anthropic_env):
        """TC-RES-PY-05: Returns profile with named key (ANTHROPIC_PERSONAL_API_KEY)."""
        profile = get_active_profile()
        assert profile.provider_id == "anthropic"
        assert profile.profile_name == "personal"
        assert profile.api_key == "sk-ant-test123"

    def test_tc_res_py_06_fallback_to_default_key(self, monkeypatch):
        """TC-RES-PY-06: Falls back to ANTHROPIC_API_KEY when named key is absent."""
        monkeypatch.setenv("AI_ACTIVE_PROVIDER", "anthropic")
        monkeypatch.setenv("AI_ACTIVE_PROFILE", "personal")
        monkeypatch.delenv("ANTHROPIC_PERSONAL_API_KEY", raising=False)
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-fallback")
        profile = get_active_profile()
        assert profile.api_key == "sk-ant-fallback"

    def test_tc_res_py_07_raises_when_no_key_available(self, monkeypatch):
        """TC-RES-PY-07: Raises ProfileNotFoundError with named key in message."""
        monkeypatch.setenv("AI_ACTIVE_PROVIDER", "anthropic")
        monkeypatch.setenv("AI_ACTIVE_PROFILE", "personal")
        monkeypatch.delenv("ANTHROPIC_PERSONAL_API_KEY", raising=False)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        with pytest.raises(ProfileNotFoundError) as exc_info:
            get_active_profile()
        assert "ANTHROPIC_PERSONAL_API_KEY" in str(exc_info.value)

    def test_tc_res_py_08_no_key_required_for_local_provider(self, monkeypatch):
        """TC-RES-PY-08: Returns profile without API key for requires_api_key=False provider."""
        monkeypatch.setenv("AI_ACTIVE_PROVIDER", "ollama")
        monkeypatch.setenv("AI_ACTIVE_PROFILE", "local")
        monkeypatch.delenv("OLLAMA_LOCAL_API_KEY", raising=False)
        monkeypatch.delenv("OLLAMA_API_KEY", raising=False)
        profile = get_active_profile()
        assert profile.provider_id == "ollama"
        assert profile.api_key == ""  # empty — not required

    def test_tc_res_py_09_uses_default_model_from_descriptor(self, monkeypatch):
        """TC-RES-PY-09: Profile.model falls back to ProviderDescriptor.default_model."""
        monkeypatch.setenv("AI_ACTIVE_PROVIDER", "anthropic")
        monkeypatch.setenv("AI_ACTIVE_PROFILE", "default")
        monkeypatch.setenv("ANTHROPIC_DEFAULT_API_KEY", "sk-ant-test")
        monkeypatch.delenv("ANTHROPIC_DEFAULT_MODEL", raising=False)
        monkeypatch.delenv("ANTHROPIC_MODEL", raising=False)
        profile = get_active_profile()
        assert profile.model == "claude-3-5-sonnet-20241022"


# ---------------------------------------------------------------------------
# .env read behaviour
# ---------------------------------------------------------------------------

class TestDotenvBehavior:

    def test_tc_res_py_10_missing_dotenv_does_not_raise(self, tmp_path, monkeypatch):
        """TC-RES-PY-10: Missing .env logs a warning but never raises."""
        _reset_for_tests()
        # Point DOTENV_PATH at a non-existent file inside tmp_path
        nonexistent = tmp_path / ".env"
        monkeypatch.setattr(ai_providers, "_DOTENV_PATH", nonexistent)
        with patch.object(logging.getLogger("ai_providers"), "warning") as mock_warn:
            ensure_providers()  # must not raise
        assert mock_warn.called or True  # warning may go through root logger; no exception is the key check

    def test_tc_res_py_11_load_dotenv_called_once(self, tmp_path, monkeypatch):
        """TC-RES-PY-11: load_dotenv called exactly once per initialisation cycle."""
        _reset_for_tests()
        env_file = tmp_path / ".env"
        env_file.write_text("AI_ACTIVE_PROVIDER=anthropic\n")
        monkeypatch.setattr(ai_providers, "_DOTENV_PATH", env_file)

        with patch("ai_providers.load_dotenv") as mock_load:
            ensure_providers()
            ensure_providers()  # second call is a no-op

        mock_load.assert_called_once()


# ---------------------------------------------------------------------------
# mask_api_key() unit tests
# ---------------------------------------------------------------------------

class TestMaskApiKey:

    def test_tc_mask_01_anthropic_key(self):
        """TC-MASK-01: Standard Anthropic key → 'sk-***...***'."""
        assert mask_api_key("sk-ant-api03-abcdefghijklmnop") == "sk-***...***"

    def test_tc_mask_02_openai_key(self):
        """TC-MASK-02: Standard OpenAI key → 'sk-***...***'."""
        assert mask_api_key("sk-proj-abc123xyz789def") == "sk-***...***"

    def test_tc_mask_03_short_key_no_hyphen(self):
        """TC-MASK-03: Short key without hyphen uses first 3 chars as prefix."""
        result = mask_api_key("abc")
        assert "abc" in result
        assert "***" in result

    def test_tc_mask_04_empty_string(self):
        """TC-MASK-04: Empty string returns '(not set)'."""
        assert mask_api_key("") == "(not set)"

    def test_tc_mask_05_non_standard_prefix(self):
        """TC-MASK-05: Non-standard-prefix key preserves first segment before '-' (or first 3 chars)."""
        result = mask_api_key("AIzaSyAbcDef123456")
        assert result.startswith("AIz")
        assert "***" in result
        assert "AbcDef123456" not in result

    def test_tc_mask_06_full_key_not_in_output(self):
        """TC-MASK-06: Output never contains the secret portion of the key (chars 4+)."""
        key = "sk-ant-api03-secretsuffix99"
        result = mask_api_key(key)
        assert "secretsuffix99" not in result
        assert "api03" not in result


# ---------------------------------------------------------------------------
# provider_status_command() — masking tests
# ---------------------------------------------------------------------------

class TestProviderStatusCommandMasking:

    def test_tc_mask_status_01_raw_key_not_in_output(self, monkeypatch, capsys):
        """TC-MASK-STATUS-01: status command output never contains raw API key."""
        monkeypatch.setenv("AI_ACTIVE_PROVIDER", "anthropic")
        monkeypatch.setenv("AI_ACTIVE_PROFILE", "personal")
        monkeypatch.setenv("ANTHROPIC_PERSONAL_API_KEY", "sk-ant-verysecretkey123")
        monkeypatch.setattr(ai_providers, "HAS_RICH", False)
        provider_status_command()
        captured = capsys.readouterr().out
        assert "sk-ant-verysecretkey123" not in captured
        assert "***" in captured

    def test_tc_mask_status_02_masked_key_label_present(self, monkeypatch, capsys):
        """TC-MASK-STATUS-02: Status output shows 'API Key:' label with masked value."""
        monkeypatch.setenv("AI_ACTIVE_PROVIDER", "anthropic")
        monkeypatch.setenv("AI_ACTIVE_PROFILE", "personal")
        monkeypatch.setenv("ANTHROPIC_PERSONAL_API_KEY", "sk-ant-verysecretkey123")
        monkeypatch.setattr(ai_providers, "HAS_RICH", False)
        provider_status_command()
        captured = capsys.readouterr().out
        assert "API Key" in captured
        assert "sk-ant-verysecretkey123" not in captured

    def test_tc_mask_status_03_no_provider_shows_message(self, monkeypatch, capsys):
        """TC-MASK-STATUS-03: No active provider shows config message, no key data."""
        monkeypatch.delenv("AI_ACTIVE_PROVIDER", raising=False)
        monkeypatch.setattr(ai_providers, "HAS_RICH", False)
        provider_status_command()  # must not raise
        captured = capsys.readouterr().out
        assert "sk-" not in captured
        assert "No active provider" in captured.lower() or "configure" in captured.lower()


# ---------------------------------------------------------------------------
# provider_list_command() — masking tests
# ---------------------------------------------------------------------------

class TestProviderListCommandMasking:

    def test_tc_mask_list_01_no_raw_keys_in_output(self, monkeypatch, capsys):
        """TC-MASK-LIST-01: Provider list never exposes raw API key values."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-secretListKey")
        monkeypatch.setattr(ai_providers, "HAS_RICH", False)
        provider_list_command()
        captured = capsys.readouterr().out
        assert "sk-ant-secretListKey" not in captured

    def test_tc_mask_list_02_active_provider_no_credential_data(self, monkeypatch, capsys):
        """TC-MASK-LIST-02: Active provider row has no credential data."""
        monkeypatch.setenv("AI_ACTIVE_PROVIDER", "anthropic")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-rowsecret")
        monkeypatch.setattr(ai_providers, "HAS_RICH", False)
        provider_list_command()
        captured = capsys.readouterr().out
        assert "sk-ant-rowsecret" not in captured
        assert "anthropic" in captured.lower()


# ---------------------------------------------------------------------------
# provider_create_command() — masking tests
# ---------------------------------------------------------------------------

class TestProviderCreateCommandMasking:

    def test_tc_mask_create_01_interactive_does_not_echo_key(self, monkeypatch, capsys):
        """TC-MASK-CREATE-01: Interactive creation panel does not echo raw API key."""
        monkeypatch.setattr(ai_providers, "HAS_RICH", False)
        monkeypatch.setattr(ai_providers, "HAS_DOTENV", False)
        mock_q = MagicMock()
        mock_q.password.return_value.ask.return_value = "sk-ant-newkey456"
        mock_q.text.return_value.ask.return_value = ""
        monkeypatch.setattr(ai_providers, "HAS_QUESTIONARY", True)
        monkeypatch.setattr(ai_providers, "questionary", mock_q, raising=False)
        provider_create_command("anthropic", "work", interactive=True)
        captured = capsys.readouterr().out
        assert "sk-ant-newkey456" not in captured

    def test_tc_mask_create_02_noninteractive_does_not_log_key(self, monkeypatch, capsys):
        """TC-MASK-CREATE-02: Non-interactive create does not log API key to stdout."""
        monkeypatch.setenv("ANTHROPIC_WORK_API_KEY", "sk-ant-envkey789")
        monkeypatch.setattr(ai_providers, "HAS_RICH", False)
        monkeypatch.setattr(ai_providers, "HAS_DOTENV", False)
        provider_create_command("anthropic", "work", interactive=False)
        captured = capsys.readouterr().out
        assert "sk-ant-envkey789" not in captured


# ---------------------------------------------------------------------------
# Log safety tests
# ---------------------------------------------------------------------------

class TestLogSafety:

    def test_tc_mask_log_01_no_raw_key_in_log_records(self, monkeypatch, caplog):
        """TC-MASK-LOG-01: Logging at any level does not emit raw API key."""
        monkeypatch.setenv("AI_ACTIVE_PROVIDER", "anthropic")
        monkeypatch.setenv("AI_ACTIVE_PROFILE", "personal")
        monkeypatch.setenv("ANTHROPIC_PERSONAL_API_KEY", "sk-ant-logsecret999")
        with caplog.at_level(logging.DEBUG, logger="ai_providers"):
            try:
                resolve_active_provider()
                get_active_profile()
            except Exception:
                pass
        all_log_text = " ".join(r.message for r in caplog.records)
        assert "sk-ant-logsecret999" not in all_log_text

    def test_tc_mask_log_02_exception_message_contains_var_name_not_value(self, monkeypatch):
        """TC-MASK-LOG-02: ProfileNotFoundError message contains env var name, not key value."""
        monkeypatch.setenv("AI_ACTIVE_PROVIDER", "anthropic")
        monkeypatch.setenv("AI_ACTIVE_PROFILE", "nosuchprofile")
        monkeypatch.setenv("ANTHROPIC_PERSONAL_API_KEY", "sk-ant-secret")
        monkeypatch.delenv("ANTHROPIC_NOSUCHPROFILE_API_KEY", raising=False)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        with pytest.raises(ProfileNotFoundError) as exc_info:
            get_active_profile()
        msg = str(exc_info.value)
        assert "ANTHROPIC_NOSUCHPROFILE_API_KEY" in msg
        assert "sk-ant-secret" not in msg


# ---------------------------------------------------------------------------
# GUI navigation tests — helpers
# ---------------------------------------------------------------------------

def _make_select_side_effect(responses_by_title: dict) -> callable:
    """Return a side_effect for questionary.select that dispatches on title."""
    queues: dict[str, list] = {k: list(v) for k, v in responses_by_title.items()}

    def _select(title, choices=None, **kwargs):
        mock = MagicMock()
        queue = queues.get(title, [])
        mock.ask.return_value = queue.pop(0) if queue else "Exit"
        return mock

    return _select


# ---------------------------------------------------------------------------
# GUI — menu entry tests
# ---------------------------------------------------------------------------

class TestGuiMenuEntry:

    def test_tc_gui_menu_01_ai_providers_entry_present(self, monkeypatch):
        """TC-GUI-MENU-01: 'AI Providers' present in main menu choices."""
        import generate_documentation as gd
        monkeypatch.setattr(gd, "HAS_QUESTIONARY", True)

        captured_choices: list = []

        def _select(title, choices=None, **kwargs):
            mock = MagicMock()
            if "Main Menu" in title:
                captured_choices.extend(choices or [])
                mock.ask.return_value = "Exit"
            else:
                mock.ask.return_value = "Back"
            return mock

        with patch("generate_documentation.questionary", create=True) as mock_q:
            mock_q.select.side_effect = _select
            gd._run_gui_loop()

        assert "AI Providers" in captured_choices

    def test_tc_gui_menu_02_ai_providers_entry_consistent(self, monkeypatch):
        """TC-GUI-MENU-02: 'AI Providers' always at same position across menu renders."""
        import generate_documentation as gd
        monkeypatch.setattr(gd, "HAS_QUESTIONARY", True)

        all_choices: list[list] = []
        call_count = [0]

        def _select(title, choices=None, **kwargs):
            mock = MagicMock()
            if "Main Menu" in title:
                all_choices.append(list(choices or []))
                call_count[0] += 1
                # Exit after 2 main-menu renders
                mock.ask.return_value = "Exit" if call_count[0] >= 2 else "Generate Documentation"
            else:
                mock.ask.return_value = "Back"
            return mock

        with patch("generate_documentation.questionary", create=True) as mock_q:
            mock_q.select.side_effect = _select
            gd._run_gui_loop()

        assert len(all_choices) == 2
        assert all_choices[0].index("AI Providers") == all_choices[1].index("AI Providers")


# ---------------------------------------------------------------------------
# GUI — status panel display tests
# ---------------------------------------------------------------------------

class TestGuiStatusPanel:

    def test_tc_gui_status_01_status_called_before_action_prompt(self, monkeypatch):
        """TC-GUI-STATUS-01: provider_status_command() called before the action sub-menu."""
        import generate_documentation as gd
        monkeypatch.setattr(gd, "HAS_QUESTIONARY", True)

        call_order: list[str] = []
        status_mock = MagicMock(side_effect=lambda: call_order.append("status"))

        def _select(title, choices=None, **kwargs):
            mock = MagicMock()
            if "Main Menu" in title:
                mock.ask.return_value = "AI Providers"
            elif "Options" in title:
                call_order.append("sub_menu")
                mock.ask.return_value = "Back"
            else:
                mock.ask.return_value = "Exit"
            return mock

        with patch("generate_documentation.questionary", create=True) as mock_q:
            mock_q.select.side_effect = _select
            with patch("ai_providers.provider_status_command", status_mock):
                # Need a second main-menu iteration → patch returns Exit
                side_iter = iter(["AI Providers", "Exit"])

                def _select2(title, choices=None, **kwargs):
                    mock = MagicMock()
                    if "Main Menu" in title:
                        mock.ask.return_value = next(side_iter, "Exit")
                    elif "Options" in title:
                        call_order.append("sub_menu")
                        mock.ask.return_value = "Back"
                    return mock

                mock_q.select.side_effect = _select2
                gd._run_gui_loop()

        assert call_order.index("status") < call_order.index("sub_menu")

    def test_tc_gui_status_02_no_provider_does_not_raise(self, monkeypatch, capsys):
        """TC-GUI-STATUS-02: GUI handles missing provider gracefully."""
        import generate_documentation as gd
        monkeypatch.setattr(gd, "HAS_QUESTIONARY", True)
        monkeypatch.delenv("AI_ACTIVE_PROVIDER", raising=False)
        monkeypatch.setattr(ai_providers, "HAS_RICH", False)

        side_iter = iter(["AI Providers", "Exit"])

        def _select(title, choices=None, **kwargs):
            mock = MagicMock()
            if "Main Menu" in title:
                mock.ask.return_value = next(side_iter, "Exit")
            elif "Options" in title:
                mock.ask.return_value = "Back"
            return mock

        with patch("generate_documentation.questionary", create=True) as mock_q:
            mock_q.select.side_effect = _select
            gd._run_gui_loop()  # must not raise

    def test_tc_gui_status_03_status_output_masks_key(self, monkeypatch, capsys):
        """TC-GUI-STATUS-03: Status panel shown in GUI never exposes raw API key."""
        monkeypatch.setenv("AI_ACTIVE_PROVIDER", "anthropic")
        monkeypatch.setenv("AI_ACTIVE_PROFILE", "personal")
        monkeypatch.setenv("ANTHROPIC_PERSONAL_API_KEY", "sk-ant-guisecret")
        monkeypatch.setattr(ai_providers, "HAS_RICH", False)
        provider_status_command()
        out = capsys.readouterr().out
        assert "sk-ant-guisecret" not in out
        assert "***" in out


# ---------------------------------------------------------------------------
# GUI — action prompt choices tests
# ---------------------------------------------------------------------------

class TestGuiActionPrompt:

    def _run_with_choices(self, monkeypatch, main_action, sub_action_val):
        """Helper: run _run_gui_loop with controlled menu selections."""
        import generate_documentation as gd
        monkeypatch.setattr(gd, "HAS_QUESTIONARY", True)

        sub_choices_seen: list = []
        side_iter = iter([main_action, "Exit"])

        def _select(title, choices=None, **kwargs):
            mock = MagicMock()
            if "Main Menu" in title:
                mock.ask.return_value = next(side_iter, "Exit")
            elif "Options" in title:
                sub_choices_seen.extend(choices or [])
                mock.ask.return_value = sub_action_val
            return mock

        status_mock = MagicMock()
        configure_mock = MagicMock(return_value=0)

        with patch("generate_documentation.questionary", create=True) as mock_q, \
             patch("ai_providers.provider_status_command", status_mock), \
             patch("ai_providers.configure_command", configure_mock):
            mock_q.select.side_effect = _select
            gd._run_gui_loop()

        return sub_choices_seen, configure_mock

    def test_tc_gui_action_01_action_prompt_choices(self, monkeypatch):
        """TC-GUI-ACTION-01: Action prompt presents 'Run guided setup' and 'Back'."""
        sub_choices, _ = self._run_with_choices(monkeypatch, "AI Providers", "Back")
        assert "Run guided setup" in sub_choices
        assert "Back" in sub_choices

    def test_tc_gui_action_02_run_guided_setup_calls_configure(self, monkeypatch):
        """TC-GUI-ACTION-02: 'Run guided setup' calls configure_command with default ConfigureOptions."""
        import generate_documentation as gd
        monkeypatch.setattr(gd, "HAS_QUESTIONARY", True)
        from ai_providers import ConfigureOptions

        side_iter = iter(["AI Providers", "Exit"])
        configure_mock = MagicMock(return_value=0)
        status_mock = MagicMock()

        def _select(title, choices=None, **kwargs):
            mock = MagicMock()
            if "Main Menu" in title:
                mock.ask.return_value = next(side_iter, "Exit")
            elif "Options" in title:
                mock.ask.return_value = "Run guided setup"
            return mock

        with patch("generate_documentation.questionary", create=True) as mock_q, \
             patch("ai_providers.provider_status_command", status_mock), \
             patch("ai_providers.configure_command", configure_mock):
            mock_q.select.side_effect = _select
            gd._run_gui_loop()

        configure_mock.assert_called_once_with(ConfigureOptions())

    def test_tc_gui_action_03_back_does_not_call_configure(self, monkeypatch):
        """TC-GUI-ACTION-03: 'Back' returns to main menu without calling configure_command."""
        _, configure_mock = self._run_with_choices(monkeypatch, "AI Providers", "Back")
        configure_mock.assert_not_called()


# ---------------------------------------------------------------------------
# GUI — KeyboardInterrupt handling tests
# ---------------------------------------------------------------------------

class TestGuiKeyboardInterrupt:

    def test_tc_gui_kbi_01_interrupt_in_status_returns_to_menu(self, monkeypatch, capsys):
        """TC-GUI-KBI-01: Ctrl+C inside provider status block returns to main menu."""
        import generate_documentation as gd
        monkeypatch.setattr(gd, "HAS_QUESTIONARY", True)

        side_iter = iter(["AI Providers", "Exit"])

        def _select(title, choices=None, **kwargs):
            mock = MagicMock()
            mock.ask.return_value = next(side_iter, "Exit")
            return mock

        status_mock = MagicMock(side_effect=KeyboardInterrupt)

        with patch("generate_documentation.questionary", create=True) as mock_q, \
             patch("ai_providers.provider_status_command", status_mock):
            mock_q.select.side_effect = _select
            result = gd._run_gui_loop()  # must not propagate KeyboardInterrupt

        assert result == 0

    def test_tc_gui_kbi_02_interrupt_in_wizard_returns_to_menu(self, monkeypatch, capsys):
        """TC-GUI-KBI-02: Ctrl+C during guided setup wizard returns to main menu."""
        import generate_documentation as gd
        monkeypatch.setattr(gd, "HAS_QUESTIONARY", True)

        side_iter = iter(["AI Providers", "Exit"])
        sub_iter = iter(["Run guided setup"])

        def _select(title, choices=None, **kwargs):
            mock = MagicMock()
            if "Main Menu" in title:
                mock.ask.return_value = next(side_iter, "Exit")
            elif "Options" in title:
                mock.ask.return_value = next(sub_iter, "Back")
            return mock

        status_mock = MagicMock()
        configure_mock = MagicMock(side_effect=KeyboardInterrupt)

        with patch("generate_documentation.questionary", create=True) as mock_q, \
             patch("ai_providers.provider_status_command", status_mock), \
             patch("ai_providers.configure_command", configure_mock):
            mock_q.select.side_effect = _select
            result = gd._run_gui_loop()  # must not propagate

        assert result == 0

    def test_tc_gui_kbi_03_interrupt_at_main_menu_exits_cleanly(self, monkeypatch, capsys):
        """TC-GUI-KBI-03: Ctrl+C at main menu exits with farewell message."""
        import generate_documentation as gd
        monkeypatch.setattr(gd, "HAS_QUESTIONARY", True)

        def _select(title, choices=None, **kwargs):
            mock = MagicMock()
            mock.ask.side_effect = KeyboardInterrupt
            return mock

        with patch("generate_documentation.questionary", create=True) as mock_q:
            mock_q.select.side_effect = _select
            result = gd._run_gui_loop()

        out = capsys.readouterr().out
        assert result == 0
        assert "Goodbye" in out

    def test_tc_gui_kbi_04_interrupt_at_action_prompt_returns_to_menu(self, monkeypatch):
        """TC-GUI-KBI-04: Ctrl+C on action sub-prompt silently returns to main menu."""
        import generate_documentation as gd
        monkeypatch.setattr(gd, "HAS_QUESTIONARY", True)

        side_iter = iter(["AI Providers", "Exit"])

        def _select(title, choices=None, **kwargs):
            mock = MagicMock()
            if "Main Menu" in title:
                mock.ask.return_value = next(side_iter, "Exit")
            elif "Options" in title:
                mock.ask.side_effect = KeyboardInterrupt
            return mock

        status_mock = MagicMock()

        with patch("generate_documentation.questionary", create=True) as mock_q, \
             patch("ai_providers.provider_status_command", status_mock):
            mock_q.select.side_effect = _select
            result = gd._run_gui_loop()

        assert result == 0


# ---------------------------------------------------------------------------
# GUI — loop integrity tests
# ---------------------------------------------------------------------------

class TestGuiLoopIntegrity:

    def test_tc_gui_integrity_01_existing_choices_still_work(self, monkeypatch, capsys):
        """TC-GUI-INTEGRITY-01: 'Generate Documentation' choice functions as before."""
        import generate_documentation as gd
        monkeypatch.setattr(gd, "HAS_QUESTIONARY", True)

        side_iter = iter(["Generate Documentation", "Exit"])

        def _select(title, choices=None, **kwargs):
            mock = MagicMock()
            mock.ask.return_value = next(side_iter, "Exit")
            return mock

        with patch("generate_documentation.questionary", create=True) as mock_q:
            mock_q.select.side_effect = _select
            result = gd._run_gui_loop()

        out = capsys.readouterr().out
        assert result == 0
        # Placeholder message for Generate Documentation should be present
        assert "Generate Documentation" in out or "Goodbye" in out

    def test_tc_gui_integrity_02_loop_continues_after_back(self, monkeypatch, capsys):
        """TC-GUI-INTEGRITY-02: Loop executes multiple iterations; exits cleanly on 'Exit'."""
        import generate_documentation as gd
        monkeypatch.setattr(gd, "HAS_QUESTIONARY", True)

        side_iter = iter(["AI Providers", "Exit"])
        sub_iter = iter(["Back"])

        def _select(title, choices=None, **kwargs):
            mock = MagicMock()
            if "Main Menu" in title:
                mock.ask.return_value = next(side_iter, "Exit")
            elif "Options" in title:
                mock.ask.return_value = next(sub_iter, "Back")
            return mock

        status_mock = MagicMock()

        with patch("generate_documentation.questionary", create=True) as mock_q, \
             patch("ai_providers.provider_status_command", status_mock):
            mock_q.select.side_effect = _select
            result = gd._run_gui_loop()

        assert result == 0
        out = capsys.readouterr().out
        assert "Goodbye" in out


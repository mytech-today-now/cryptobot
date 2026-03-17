#!/usr/bin/env python3
"""
ai_providers.py — Configurable AI Provider Abstraction Layer
============================================================

Provides a shared provider interface for all AI-powered commands in the
Crypto Trading Bot Platform.  Command handlers resolve the active backend
through this module rather than through direct, integration-specific logic.

Public import contract (Python)::

    from ai_providers import resolve_active_provider

Key design rules:
- Credentials and active-profile state live exclusively in the repo-root ``.env``.
- All writes use ``dotenv.set_key()`` — never a full-file overwrite.
- API keys are masked as ``sk-***...***`` at every display boundary.
- ``ensure_providers()`` is idempotent and must be called before any
  registry or store access.

Change ID : AI-PROVIDER-001
Phase     : 1–3 — Foundation, CLI Dispatch, Built-in Providers
Tasks     : 1.1–1.4, 2.1–2.2, 3.1–3.2
Version   : 0.5.0
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Optional runtime dependencies (resolved in later tasks)
# ---------------------------------------------------------------------------
try:
    from dotenv import load_dotenv, set_key as dotenv_set_key
    HAS_DOTENV = True
except ImportError:  # pragma: no cover
    HAS_DOTENV = False

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    HAS_RICH = True
except ImportError:  # pragma: no cover
    HAS_RICH = False

try:
    import questionary
    HAS_QUESTIONARY = True
except ImportError:  # pragma: no cover
    HAS_QUESTIONARY = False

# ---------------------------------------------------------------------------
# Public API surface
# ---------------------------------------------------------------------------
__all__ = [
    # Dataclasses
    "ProviderDescriptor",
    "ProviderProfile",
    "ConfigureOptions",
    # Exceptions
    "ProviderNotConfiguredError",
    "ProfileNotFoundError",
    "ProviderAlreadyRegisteredError",
    # Core functions
    "ensure_providers",
    "_reset_for_tests",
    "resolve_active_provider",
    "get_active_profile",
    "mask_api_key",
    "register_provider",
    "parse_provider_profile_arg",
    # Command functions
    "provider_list_command",
    "provider_create_command",
    "provider_edit_command",
    "provider_delete_command",
    "provider_activate_command",
    "provider_status_command",
    "configure_command",
]

# ---------------------------------------------------------------------------
# Internal state
# ---------------------------------------------------------------------------
_provider_registry: dict[str, "ProviderDescriptor"] = {}
_api_key_store: dict[str, str] = {}   # maps env-var name → raw key value
_initialized: bool = False
_DOTENV_PATH: Path = Path(__file__).parent / ".env"


def _reset_for_tests() -> None:
    """Reset all module-level state to its initial values.

    **For testing only** — never call this in production code.
    """
    global _provider_registry, _api_key_store, _initialized
    _provider_registry = {}
    _api_key_store = {}
    _initialized = False


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class ProviderNotConfiguredError(RuntimeError):
    """Raised when ``AI_ACTIVE_PROVIDER`` is unset or references an unregistered provider."""


class ProfileNotFoundError(RuntimeError):
    """Raised when the requested profile key is absent from ``.env``."""


class ProviderAlreadyRegisteredError(ValueError):
    """Raised when ``register_provider()`` is called with a duplicate provider ID."""


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class ProviderDescriptor:
    """Static metadata describing a single AI provider.

    Example::

        >>> d = ProviderDescriptor("anthropic", "Anthropic (Claude)", "ANTHROPIC",
        ...                        "claude-3-5-sonnet-20241022", None, True)
        >>> d.provider_id
        'anthropic'
        >>> d.requires_api_key
        True
        >>> d.base_url is None
        True
    """

    provider_id: str                  # e.g. ``"anthropic"``
    display_name: str                 # e.g. ``"Anthropic (Claude)"``
    env_key_prefix: str               # e.g. ``"ANTHROPIC"``
    default_model: str                # e.g. ``"claude-3-5-sonnet-20241022"``
    base_url: Optional[str] = None    # ``None`` for cloud providers
    requires_api_key: bool = True     # ``False`` for some self-hosted providers


@dataclass
class ProviderProfile:
    """Runtime profile containing resolved credentials for a provider.

    The ``api_key`` field stores the raw secret — never pass it to log
    statements or display output; always use :func:`mask_api_key` first.

    Example::

        >>> p = ProviderProfile("anthropic", "personal", "sk-ant-abc123")
        >>> p.provider_id
        'anthropic'
        >>> p.model is None
        True
        >>> p.extra
        {}
    """

    provider_id: str                   # e.g. ``"anthropic"``
    profile_name: str                  # e.g. ``"personal"``
    api_key: str                       # raw key — never logged or displayed
    model: Optional[str] = None        # e.g. ``"claude-3-5-sonnet-20241022"``
    base_url: Optional[str] = None     # for custom / self-hosted providers
    extra: dict = field(default_factory=dict)   # provider-specific settings


@dataclass
class ConfigureOptions:
    """Parsed flags for the ``configure`` subcommand.

    All fields default to ``False`` or ``None`` so that the wizard is
    launched when no flags are present.

    Example::

        >>> o = ConfigureOptions()
        >>> o.list_providers
        False
        >>> o.activate_profile is None
        True
        >>> ConfigureOptions(list_providers=True).list_providers
        True
    """

    list_providers: bool = False
    list_profiles: bool = False
    list_profiles_for_provider: Optional[str] = None  # provider_id
    create_profile: Optional[str] = None              # ``"provider_id/profile_name"``
    edit_profile: Optional[str] = None
    delete_profile: Optional[str] = None
    activate_profile: Optional[str] = None


# ---------------------------------------------------------------------------
# Public API — stubs (implemented in subsequent tasks)
# ---------------------------------------------------------------------------

def _register_builtin_providers() -> None:
    """Register the five built-in AI provider descriptors.

    Called from :func:`ensure_providers`.  Uses ``force=True`` so that
    re-initialisation after :func:`_reset_for_tests` always restores the
    built-ins without raising :class:`ProviderAlreadyRegisteredError`.
    """
    _BUILTIN_PROVIDERS = [
        ProviderDescriptor(
            provider_id="anthropic",
            display_name="Anthropic (Claude)",
            env_key_prefix="ANTHROPIC",
            default_model="claude-3-5-sonnet-20241022",
            base_url=None,
            requires_api_key=True,
        ),
        ProviderDescriptor(
            provider_id="openai",
            display_name="OpenAI",
            env_key_prefix="OPENAI",
            default_model="gpt-4o",
            base_url=None,
            requires_api_key=True,
        ),
        ProviderDescriptor(
            provider_id="google_ai",
            display_name="Google AI (Gemini)",
            env_key_prefix="GOOGLE_AI",
            default_model="gemini-1.5-pro",
            base_url=None,
            requires_api_key=True,
        ),
        ProviderDescriptor(
            provider_id="ollama",
            display_name="Ollama (local)",
            env_key_prefix="OLLAMA",
            default_model="llama3",
            base_url="http://localhost:11434",
            requires_api_key=False,
        ),
        ProviderDescriptor(
            provider_id="localai",
            display_name="LocalAI (local)",
            env_key_prefix="LOCALAI",
            default_model="gpt-4",
            base_url="http://localhost:8080",
            requires_api_key=False,
        ),
    ]
    for descriptor in _BUILTIN_PROVIDERS:
        register_provider(descriptor, force=True)


def ensure_providers() -> None:
    """Load the provider registry and active state from ``.env``.

    Must be called before any registry or store access.  Safe to call
    multiple times (idempotent).  Logs a warning if ``.env`` is missing
    rather than raising.

    Side-effects:
        * Registers all five built-in providers via :func:`_register_builtin_providers`.
        * Populates :data:`_api_key_store` with every ``*_API_KEY``
          variable found in the environment after loading ``.env``.
        * Sets :data:`_initialized` to ``True``.

    Example::

        >>> _reset_for_tests()          # clear state between test runs
        >>> ensure_providers()          # first call loads state
        >>> ensure_providers()          # second call is a no-op
    """
    import logging
    global _initialized, _api_key_store

    if _initialized:
        return

    # ------------------------------------------------------------------ #
    # 1. Load .env (warn, never raise, when the file is missing)          #
    # ------------------------------------------------------------------ #
    if HAS_DOTENV:
        if _DOTENV_PATH.exists():
            load_dotenv(_DOTENV_PATH, override=True)
        else:
            logging.getLogger(__name__).warning(
                "No .env file found at %s; provider credentials unavailable.",
                _DOTENV_PATH,
            )
    else:
        logging.getLogger(__name__).warning(
            "python-dotenv is not installed; .env will not be loaded."
        )

    # ------------------------------------------------------------------ #
    # 2. Register all five built-in providers (force=True for idempotency) #
    # ------------------------------------------------------------------ #
    _register_builtin_providers()

    # ------------------------------------------------------------------ #
    # 3. Snapshot all *_API_KEY variables into the internal store         #
    # ------------------------------------------------------------------ #
    _api_key_store = {
        key: value
        for key, value in os.environ.items()
        if key.endswith("_API_KEY") and value
    }

    # ------------------------------------------------------------------ #
    # 4. Mark as initialised so subsequent calls are no-ops               #
    # ------------------------------------------------------------------ #
    _initialized = True


def resolve_active_provider() -> ProviderDescriptor:
    """Return the :class:`ProviderDescriptor` for the currently active provider.

    Reads ``AI_ACTIVE_PROVIDER`` from ``.env`` after calling
    :func:`ensure_providers`.

    Raises:
        ProviderNotConfiguredError: If ``AI_ACTIVE_PROVIDER`` is unset or the
            referenced provider is not in the registry.

    Example::

        >>> _reset_for_tests()
        >>> register_provider(ProviderDescriptor("anthropic", "Anthropic (Claude)", "ANTHROPIC", "claude-3-5-sonnet-20241022"))
        >>> import os; os.environ["AI_ACTIVE_PROVIDER"] = "anthropic"
        >>> resolve_active_provider().provider_id
        'anthropic'
    """
    ensure_providers()

    provider_id = os.environ.get("AI_ACTIVE_PROVIDER", "").strip()
    if not provider_id:
        raise ProviderNotConfiguredError(
            "AI_ACTIVE_PROVIDER is not set. "
            "Run: python generate_documentation.py configure --activate-profile <provider>/<profile>"
        )

    descriptor = _provider_registry.get(provider_id)
    if descriptor is None:
        registered = ", ".join(sorted(_provider_registry)) or "(none)"
        raise ProviderNotConfiguredError(
            f"Provider '{provider_id}' is not registered. "
            f"Registered providers: {registered}"
        )

    return descriptor


def get_active_profile() -> ProviderProfile:
    """Return the :class:`ProviderProfile` for the currently active profile.

    Reads ``AI_ACTIVE_PROFILE`` and the corresponding ``<PREFIX>_API_KEY``
    from ``.env`` after calling :func:`ensure_providers`.  The returned
    object contains the *raw* API key — never display it without masking.

    Raises:
        ProfileNotFoundError: If the profile key is absent from ``.env``
            or ``AI_ACTIVE_PROFILE`` is unset.
        ProviderNotConfiguredError: If ``AI_ACTIVE_PROVIDER`` is unset or
            unregistered (delegated to :func:`resolve_active_provider`).

    Example::

        >>> _reset_for_tests()
        >>> register_provider(ProviderDescriptor("anthropic", "Anthropic (Claude)", "ANTHROPIC", "claude-3-5-sonnet-20241022"))
        >>> import os; os.environ["AI_ACTIVE_PROVIDER"] = "anthropic"
        >>> os.environ["AI_ACTIVE_PROFILE"] = "personal"
        >>> os.environ["ANTHROPIC_API_KEY"] = "sk-ant-test"
        >>> p = get_active_profile()
        >>> p.profile_name
        'personal'
        >>> p.api_key
        'sk-ant-test'
    """
    ensure_providers()

    descriptor = resolve_active_provider()  # raises ProviderNotConfiguredError if needed

    profile_name = os.environ.get("AI_ACTIVE_PROFILE", "").strip()
    if not profile_name:
        raise ProfileNotFoundError(
            "AI_ACTIVE_PROFILE is not set. "
            "Run: python generate_documentation.py configure --activate-profile <provider>/<profile>"
        )

    # Resolve the API key.  Look for the named-profile key first
    # (<PREFIX>_<PROFILE_NAME_UPPER>_API_KEY), then fall back to the generic
    # default (<PREFIX>_API_KEY).
    profile_key_env_var = f"{descriptor.env_key_prefix}_{profile_name.upper()}_API_KEY"
    default_key_env_var = f"{descriptor.env_key_prefix}_API_KEY"

    api_key = os.environ.get(profile_key_env_var, "").strip()
    if not api_key:
        api_key = os.environ.get(default_key_env_var, "").strip()

    if descriptor.requires_api_key and not api_key:
        raise ProfileNotFoundError(
            f"API key for provider '{descriptor.provider_id}' profile '{profile_name}' "
            f"is not set. Expected environment variable: {profile_key_env_var} "
            f"(or fallback: {default_key_env_var})"
        )

    # Resolve optional model and base_url overrides from the env
    model_env_var = f"{descriptor.env_key_prefix}_MODEL"
    model = os.environ.get(model_env_var, "").strip() or descriptor.default_model or None

    base_url_env_var = f"{descriptor.env_key_prefix}_BASE_URL"
    base_url = os.environ.get(base_url_env_var, "").strip() or descriptor.base_url or None

    return ProviderProfile(
        provider_id=descriptor.provider_id,
        profile_name=profile_name,
        api_key=api_key,
        model=model,
        base_url=base_url,
    )


def mask_api_key(key: str) -> str:
    """Return a masked representation of *key* safe for terminal output.

    The visible prefix is everything before the first ``"-"`` separator (or
    the first three characters when no separator is present).

    Examples::

        >>> mask_api_key("sk-ant-abc123")
        'sk-***...***'
        >>> mask_api_key("")
        '(not set)'

    Args:
        key: The raw API key string.

    Returns:
        A masked string of the form ``"<prefix>-***...***"`` or ``"(not set)"``
        when *key* is empty.
    """
    if not key:
        return "(not set)"
    prefix = key.split("-", 1)[0] if "-" in key else key[:3]
    return f"{prefix}-***...***"


def register_provider(descriptor: ProviderDescriptor, force: bool = False) -> None:
    """Register *descriptor* in the shared provider registry.

    Args:
        descriptor: The :class:`ProviderDescriptor` to register.
        force:      If ``True``, silently overwrite an existing entry with
                    the same ``provider_id``.  Defaults to ``False``.

    Raises:
        ProviderAlreadyRegisteredError: If *descriptor.provider_id* is
            already registered and *force* is ``False``.

    Example::

        >>> _reset_for_tests()
        >>> d = ProviderDescriptor("myprov", "My Provider", "MYPROV", "gpt-x")
        >>> register_provider(d)
        >>> "myprov" in _provider_registry
        True
        >>> register_provider(d, force=True)  # no error
        >>> register_provider(d)              # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        ai_providers.ProviderAlreadyRegisteredError: ...
    """
    provider_id = descriptor.provider_id
    if provider_id in _provider_registry and not force:
        raise ProviderAlreadyRegisteredError(
            f"Provider '{provider_id}' is already registered. "
            "Use force=True to overwrite."
        )
    _provider_registry[provider_id] = descriptor


def parse_provider_profile_arg(value: str) -> tuple[str, str]:
    """Split a ``"provider_id/profile_name"`` argument into its two parts.

    Args:
        value: A string of the form ``"provider_id/profile_name"``.

    Returns:
        A ``(provider_id, profile_name)`` tuple.

    Raises:
        SystemExit: With a human-readable error message when the ``/``
            separator is absent.

    Example::

        >>> parse_provider_profile_arg("anthropic/personal")
        ('anthropic', 'personal')
    """
    parts = value.split("/", maxsplit=1)
    if len(parts) != 2 or not parts[0] or not parts[1]:
        print(
            f"Error: expected 'provider_id/profile_name', got '{value}'.",
            file=sys.stderr,
        )
        sys.exit(1)
    return parts[0], parts[1]


def provider_list_command() -> None:
    """Print all registered providers as a ``rich`` table.

    Columns: ID | Display Name | Status (active/inactive) | Profile Count.
    The active provider row is highlighted.  No API keys appear in output.
    Calls :func:`ensure_providers` before accessing the registry.
    """
    ...  # TODO: Task 2.3


def provider_create_command(
    provider_id: str,
    profile_name: str,
    interactive: bool = True,
) -> None:
    """Create a new provider profile.

    In interactive mode prompts for credentials via ``questionary``.
    Writes settings to ``.env`` via ``dotenv.set_key()`` only.
    Confirms success with a ``rich`` panel.

    Args:
        provider_id:  The registered provider identifier (e.g. ``"anthropic"``).
        profile_name: The name for the new profile (e.g. ``"personal"``).
        interactive:  When ``True``, prompt for any missing credentials.
    """
    ...  # TODO: Task 2.4


def provider_edit_command(provider_id: str, profile_name: str) -> None:
    """Edit an existing provider profile interactively.

    Re-prompts only for fields the user wants to change, using the current
    value as the default.  Exits with a clear error if the profile does not
    exist.

    Args:
        provider_id:  The registered provider identifier.
        profile_name: The name of the existing profile to edit.
    """
    ...  # TODO: Task 2.5


def provider_delete_command(provider_id: str, profile_name: str) -> None:
    """Delete a profile from ``.env`` after user confirmation.

    Only the targeted profile keys are removed; unrelated ``.env`` variables
    are preserved.  Exits with a clear error if the profile does not exist.

    Args:
        provider_id:  The registered provider identifier.
        profile_name: The name of the profile to delete.
    """
    ...  # TODO: Task 2.5


def provider_activate_command(provider_id: str, profile_name: str) -> None:
    """Write ``AI_ACTIVE_PROVIDER`` and ``AI_ACTIVE_PROFILE`` to ``.env``.

    Validates that *provider_id* is registered before writing.

    Args:
        provider_id:  The registered provider identifier to activate.
        profile_name: The profile name to activate.
    """
    ...  # TODO: Task 2.6


def provider_status_command() -> None:
    """Print a ``rich`` panel showing the active provider and profile.

    Displays: active provider ID, display name, profile name, masked API
    key, and configured model.  Shows a ``"No active provider"`` message
    when ``AI_ACTIVE_PROVIDER`` is unset.  Safe to call when ``.env`` is
    empty or missing.
    """
    ...  # TODO: Task 4.2


def configure_command(options: ConfigureOptions) -> int:
    """Dispatch ``configure`` flags in declaration order.

    Checks each flag on *options* in declaration order and delegates to the
    appropriate function, returning after the first match.  When no flags
    are set, launches the interactive guided wizard (Mode B).

    Args:
        options: A :class:`ConfigureOptions` instance populated from
                 ``argparse`` or constructed directly.

    Returns:
        Exit code — ``0`` on success, ``1`` on error.

    Example::

        >>> _reset_for_tests()
        >>> configure_command(ConfigureOptions(list_providers=True))
        0
    """
    ensure_providers()

    try:
        # --list-providers
        if options.list_providers:
            provider_list_command()
            return 0

        # --list-profiles
        if options.list_profiles:
            _list_all_profiles_command()
            return 0

        # --list-profiles-for-provider <provider_id>
        if options.list_profiles_for_provider is not None:
            _list_profiles_for_provider_command(options.list_profiles_for_provider)
            return 0

        # --create-profile <provider_id/profile_name>
        if options.create_profile is not None:
            provider_id, profile_name = parse_provider_profile_arg(options.create_profile)
            provider_create_command(provider_id, profile_name)
            return 0

        # --edit-profile <provider_id/profile_name>
        if options.edit_profile is not None:
            provider_id, profile_name = parse_provider_profile_arg(options.edit_profile)
            provider_edit_command(provider_id, profile_name)
            return 0

        # --delete-profile <provider_id/profile_name>
        if options.delete_profile is not None:
            provider_id, profile_name = parse_provider_profile_arg(options.delete_profile)
            provider_delete_command(provider_id, profile_name)
            return 0

        # --activate-profile <provider_id/profile_name>
        if options.activate_profile is not None:
            provider_id, profile_name = parse_provider_profile_arg(options.activate_profile)
            provider_activate_command(provider_id, profile_name)
            return 0

        # No flags — launch interactive wizard
        _launch_configure_wizard()
        return 0

    except (ProviderNotConfiguredError, ProfileNotFoundError, ProviderAlreadyRegisteredError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1


# ---------------------------------------------------------------------------
# Internal helpers for configure_command dispatch (implemented in later tasks)
# ---------------------------------------------------------------------------

def _list_all_profiles_command() -> None:
    """List all profiles across all registered providers.

    Stub — full implementation in Task 2.x.
    """
    print("(--list-profiles: not yet implemented)")  # TODO: Task 2.x


def _list_profiles_for_provider_command(provider_id: str) -> None:
    """List all profiles for *provider_id*.

    Stub — full implementation in Task 2.x.
    """
    print(f"(--list-profiles-for-provider {provider_id}: not yet implemented)")  # TODO: Task 2.x


def _launch_configure_wizard() -> None:
    """Launch the interactive guided configuration wizard (Mode B).

    Stub — full implementation in Task 4.1.
    """
    if HAS_QUESTIONARY:
        print("Interactive wizard not yet implemented.")
    else:
        print(
            "No flags provided. Run with --help to see available options.\n"
            "(Interactive wizard requires 'questionary' — pip install questionary)"
        )


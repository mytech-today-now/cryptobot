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
Phase     : 1 — Foundation
Task      : 1.1 — Skeleton
Version   : 0.1.0 (skeleton)
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
# Internal state
# ---------------------------------------------------------------------------
_provider_registry: dict[str, "ProviderDescriptor"] = {}
_initialized: bool = False
_DOTENV_PATH: Path = Path(__file__).parent / ".env"


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
    """Static metadata describing a single AI provider."""

    provider_id: str         # e.g. ``"anthropic"``
    display_name: str        # e.g. ``"Anthropic (Claude)"``
    env_key_prefix: str      # e.g. ``"ANTHROPIC"``
    default_model: str       # e.g. ``"claude-3-5-sonnet-20241022"``
    base_url: Optional[str]  # ``None`` for cloud providers
    requires_api_key: bool   # ``False`` for some self-hosted providers


@dataclass
class ProviderProfile:
    """Runtime profile containing resolved credentials for a provider."""

    provider_id: str          # e.g. ``"anthropic"``
    profile_name: str         # e.g. ``"personal"``
    api_key: str              # raw key — never logged or displayed
    model: Optional[str]      # e.g. ``"claude-3-5-sonnet-20241022"``
    base_url: Optional[str]   # for custom / self-hosted providers
    extra: dict = field(default_factory=dict)  # provider-specific settings


@dataclass
class ConfigureOptions:
    """Parsed flags for the ``configure`` subcommand."""

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

def ensure_providers() -> None:
    """Load the provider registry and active state from ``.env``.

    Must be called before any registry or store access.  Safe to call
    multiple times (idempotent).  Logs a warning if ``.env`` is missing
    rather than raising.
    """
    ...  # TODO: Task 1.3


def resolve_active_provider() -> ProviderDescriptor:
    """Return the :class:`ProviderDescriptor` for the currently active provider.

    Reads ``AI_ACTIVE_PROVIDER`` from ``.env`` after calling
    :func:`ensure_providers`.

    Raises:
        ProviderNotConfiguredError: If ``AI_ACTIVE_PROVIDER`` is unset or the
            referenced provider is not in the registry.
    """
    ...  # TODO: Task 1.4


def get_active_profile() -> ProviderProfile:
    """Return the :class:`ProviderProfile` for the currently active profile.

    Reads ``AI_ACTIVE_PROFILE`` and the corresponding ``<PREFIX>_API_KEY``
    from ``.env`` after calling :func:`ensure_providers`.  The returned
    object contains the *raw* API key — never display it without masking.

    Raises:
        ProfileNotFoundError: If the profile key is absent from ``.env``
            or ``AI_ACTIVE_PROFILE`` is unset.
    """
    ...  # TODO: Task 1.4


def mask_api_key(key: str) -> str:
    """Return a masked representation of *key* safe for terminal output.

    Examples::

        >>> mask_api_key("sk-ant-abc123")
        'sk-***...***'
        >>> mask_api_key("")
        '(not set)'

    Args:
        key: The raw API key string.

    Returns:
        A masked string of the form ``"sk-***...***"`` or ``"(not set)"``
        when *key* is empty.
    """
    ...  # TODO: Task 3.3


def register_provider(descriptor: ProviderDescriptor, force: bool = False) -> None:
    """Register *descriptor* in the shared provider registry.

    Args:
        descriptor: The :class:`ProviderDescriptor` to register.
        force:      If ``True``, silently overwrite an existing entry with
                    the same ``provider_id``.  Defaults to ``False``.

    Raises:
        ProviderAlreadyRegisteredError: If *descriptor.provider_id* is
            already registered and *force* is ``False``.
    """
    ...  # TODO: Task 3.1


def parse_provider_profile_arg(value: str) -> tuple[str, str]:
    """Split a ``"provider_id/profile_name"`` argument into its two parts.

    Args:
        value: A string of the form ``"provider_id/profile_name"``.

    Returns:
        A ``(provider_id, profile_name)`` tuple.

    Raises:
        SystemExit: With a human-readable error message when the ``/``
            separator is absent.
    """
    ...  # TODO: Task 2.6


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
    """
    ...  # TODO: Task 2.2


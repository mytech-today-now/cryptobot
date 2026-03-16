# Specification: `configure` Subcommand

## Change ID
`AI-PROVIDER-001`

## Section
`specs/configure-subcommand.md`

---

## Overview

The `configure` subcommand provides two modes of operation for managing AI provider credentials and profiles: a non-interactive flag-based mode for scripting and CI/CD, and a step-by-step guided wizard for first-time users.

**Critical Rule**: When any flag is present, execute only that operation and return immediately without launching the wizard.

---

## Functional Requirements

### FR-1: Subparser Registration
- `configure` shall be registered as an `argparse` subparser on the main parser in `generate_documentation.py`.
- `python generate_documentation.py configure -h` shall print usage and all flag descriptions.

### FR-2: Mode A — Direct Flags (Non-Interactive)
All flags shall execute their single operation and exit with code `0` (success) or `1` (error).

| Flag | Operation | Function |
|------|-----------|----------|
| `--list-providers` | Print registered providers table | `provider_list_command()` |
| `--list-profiles` | Print all profiles across all providers | `list_all_profiles_command()` |
| `--list-profiles-for-provider <ID>` | Print profiles for one provider | `list_profiles_for_provider_command()` |
| `--create-profile <ID/NAME>` | Create a new profile | `provider_create_command()` |
| `--edit-profile <ID/NAME>` | Edit existing profile | `provider_edit_command()` |
| `--delete-profile <ID/NAME>` | Delete a profile | `provider_delete_command()` |
| `--activate-profile <ID/NAME>` | Set as active profile | `provider_activate_command()` |

### FR-3: Profile Flag Format
- Profile flags accept a single value in the format `provider_id/profile_name`.
- `parse_provider_profile_arg()` shall split on the **first** `/` only.
- If `/` is absent, exit with: `Error: expected 'provider_id/profile_name', got '<VALUE>'. Use a slash to separate provider and profile (e.g. anthropic/personal).`

### FR-4: Mode B — Interactive Guided Wizard (No Flags)
When no flags are present, `configure_command()` shall:
1. Call `ensure_providers()`
2. Present a numbered provider list via `questionary.select`
3. Prompt for profile name with default `"default"` via `questionary.text`
4. Call `provider_create_command(provider_id, profile_name, interactive=True)`
5. Prompt for immediate activation via `questionary.confirm(default=True)`
6. If confirmed, call `provider_activate_command(provider_id, profile_name)`
7. Call `provider_status_command()` to display final state

### FR-5: `ensure_providers()` Guard
- Every provider management function (`provider_list_command`, `provider_create_command`, etc.) shall call `ensure_providers()` before accessing the registry or `.env` store.

### FR-6: Help and Version
- `configure` subparser exposes `-h`/`--help`.
- Version flag (`-v`/`--version`) inherited from main parser.

---

## Technical Specification

### argparse Registration

```python
subparsers = parser.add_subparsers(dest='subcommand')

configure_parser = subparsers.add_parser(
    'configure',
    help='Configure AI providers and profiles',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
  %(prog)s --list-providers
  %(prog)s --create-profile anthropic/personal
  %(prog)s --activate-profile anthropic/personal
  %(prog)s                             # Launch guided wizard
    """
)

configure_parser.add_argument('--list-providers', action='store_true',
    help='List all registered AI providers')
configure_parser.add_argument('--list-profiles', action='store_true',
    help='List all configured profiles')
configure_parser.add_argument('--list-profiles-for-provider', type=str, metavar='PROVIDER_ID',
    help='List profiles for a specific provider')
configure_parser.add_argument('--create-profile', type=str, metavar='PROVIDER_ID/PROFILE_NAME',
    help='Create a new provider profile')
configure_parser.add_argument('--edit-profile', type=str, metavar='PROVIDER_ID/PROFILE_NAME',
    help='Edit an existing provider profile')
configure_parser.add_argument('--delete-profile', type=str, metavar='PROVIDER_ID/PROFILE_NAME',
    help='Delete a provider profile')
configure_parser.add_argument('--activate-profile', type=str, metavar='PROVIDER_ID/PROFILE_NAME',
    help='Set the active provider profile')
```

### `configure_command()` Dispatch Logic

```python
def configure_command(options: ConfigureOptions) -> int:
    ensure_providers()

    if options.list_providers:
        provider_list_command(); return 0

    if options.list_profiles:
        list_all_profiles_command(); return 0

    if options.list_profiles_for_provider:
        list_profiles_for_provider_command(options.list_profiles_for_provider); return 0

    if options.create_profile:
        pid, pname = parse_provider_profile_arg(options.create_profile)
        provider_create_command(pid, pname, interactive=False); return 0

    if options.edit_profile:
        pid, pname = parse_provider_profile_arg(options.edit_profile)
        provider_edit_command(pid, pname); return 0

    if options.delete_profile:
        pid, pname = parse_provider_profile_arg(options.delete_profile)
        provider_delete_command(pid, pname); return 0

    if options.activate_profile:
        pid, pname = parse_provider_profile_arg(options.activate_profile)
        provider_activate_command(pid, pname); return 0

    # No flags — launch wizard
    return _run_configure_wizard()
```

### `parse_provider_profile_arg()`

```python
def parse_provider_profile_arg(value: str) -> tuple[str, str]:
    if '/' not in value:
        print(
            f"Error: expected 'provider_id/profile_name', got '{value}'. "
            "Use a slash to separate provider and profile (e.g. anthropic/personal).",
            file=sys.stderr
        )
        sys.exit(1)
    provider_id, profile_name = value.split('/', 1)
    return provider_id.strip(), profile_name.strip()
```

### Interactive Wizard

```python
def _run_configure_wizard() -> int:
    ensure_providers()
    choices = [f"{pid} — {desc.display_name}"
               for pid, desc in _provider_registry.items()]
    selection = questionary.select("Select a provider:", choices=choices).ask()
    provider_id = selection.split(" — ")[0]

    profile_name = questionary.text("Profile name:", default="default").ask()

    provider_create_command(provider_id, profile_name, interactive=True)

    if questionary.confirm("Activate this profile now?", default=True).ask():
        provider_activate_command(provider_id, profile_name)

    provider_status_command()
    return 0
```

---

## Acceptance Criteria

- [ ] `configure -h` prints all 7 flags with descriptions
- [ ] Each flag executes its operation and returns without launching the wizard
- [ ] `parse_provider_profile_arg` splits correctly on first `/`
- [ ] Missing `/` exits with a clear error message (not a Python exception traceback)
- [ ] `configure` (no flags) presents provider list, prompts for profile name, and offers activation
- [ ] `configure_command()` calls `ensure_providers()` before any registry or store access
- [ ] All flag handlers call `ensure_providers()` internally
- [ ] Wizard defaults profile name to `"default"` if user presses Enter


# Specification: GUI AI Providers Menu Item

## Change ID
`AI-PROVIDER-001`

## Section
`specs/gui-menu.md`

---

## Overview

Add an **🤖 AI Providers** entry to the `--gui` interactive loop. The entry displays a `rich` status panel for the currently active provider and profile, then offers a guided setup option. All interactions must handle `KeyboardInterrupt` gracefully.

**Critical Rule**: The menu item must show a `rich` status panel before presenting choices and must handle `KeyboardInterrupt` without a stack trace.

---

## Functional Requirements

### FR-1: Menu Entry
- The `--gui` main loop shall include `"🤖 AI Providers"` as a selectable choice in the `questionary.select` prompt.
- The entry shall appear consistently regardless of whether any provider is configured.

### FR-2: Status Panel
- When **🤖 AI Providers** is selected, `provider_status_command()` shall be called first to display a `rich` panel.
- The panel shall show:
  - Active provider ID and display name
  - Active profile name
  - Masked API key (`sk-***...***`)
  - Configured model name
  - "No active provider configured" if `AI_ACTIVE_PROVIDER` is unset

### FR-3: Action Prompt
- After the status panel, a `questionary.select` prompt shall appear with two choices:
  - `"⚙️ Run guided setup"` — launches `configure_command(ConfigureOptions())`
  - `"↩ Back"` — returns to the main GUI menu without any action

### FR-4: KeyboardInterrupt Handling
- `KeyboardInterrupt` at any point within the AI Providers menu block shall be caught silently (no traceback).
- After catching, the GUI shall return to the main menu loop.
- The main `--gui` loop shall also wrap its top-level iteration in `try/except KeyboardInterrupt` to exit cleanly when Ctrl+C is pressed at the main menu.

### FR-5: GUI Loop Integrity
- Adding the AI Providers entry shall not break any existing `--gui` choices or their handlers.
- All existing GUI menu items shall continue to function identically.

---

## Technical Specification

### Updated `--gui` Menu Choices

```python
GUI_MENU_CHOICES = [
    "📄 Generate documentation",
    "📋 List categories and phases",
    "🤖 AI Providers",
    "❌ Exit",
]
```

### AI Providers Handler Block

```python
# Within the --gui main loop:
try:
    choice = questionary.select(
        "Crypto Trading Bot Platform — Main Menu",
        choices=GUI_MENU_CHOICES
    ).ask()
except KeyboardInterrupt:
    print("\nGoodbye!")
    break

if choice == "🤖 AI Providers":
    try:
        from ai_providers import (
            provider_status_command,
            configure_command,
            ConfigureOptions,
        )
        provider_status_command()   # Always show status panel first

        action = questionary.select(
            "AI Providers",
            choices=["⚙️ Run guided setup", "↩ Back"],
        ).ask()

        if action == "⚙️ Run guided setup":
            configure_command(ConfigureOptions())

    except KeyboardInterrupt:
        pass   # Return to main menu silently
```

### `provider_status_command()` — Rich Panel Specification

```python
from rich.console import Console
from rich.panel import Panel
from rich import box

def provider_status_command() -> None:
    ensure_providers()
    console = Console()

    provider_id  = os.getenv("AI_ACTIVE_PROVIDER")
    profile_name = os.getenv("AI_ACTIVE_PROFILE", "default")

    if not provider_id:
        console.print(Panel(
            "[yellow]No active provider configured.[/yellow]\n"
            "Run [bold]configure[/bold] to set up a provider.",
            title="🤖 AI Providers",
            border_style="yellow",
            box=box.ROUNDED,
        ))
        return

    descriptor = _provider_registry.get(provider_id)
    profile    = get_active_profile()
    masked_key = mask_api_key(profile.api_key)
    model      = profile.model or (descriptor.default_model if descriptor else "—")

    content = (
        f"[bold]Provider:[/bold]  {provider_id} — "
        f"{descriptor.display_name if descriptor else provider_id}\n"
        f"[bold]Profile:[/bold]   {profile_name}\n"
        f"[bold]API Key:[/bold]   {masked_key}\n"
        f"[bold]Model:[/bold]     {model}"
    )

    console.print(Panel(
        content,
        title="🤖 Active AI Provider",
        border_style="green",
        box=box.ROUNDED,
    ))
```

---

## Error Handling

| Scenario | Behavior |
|----------|----------|
| `AI_ACTIVE_PROVIDER` unset | Show yellow "No active provider" panel; still offer guided setup |
| `ProfileNotFoundError` during status | Show orange warning panel with recovery hint |
| `KeyboardInterrupt` in action prompt | Catch silently, return to main menu |
| `KeyboardInterrupt` in guided setup wizard | Catch silently, return to main menu |
| `KeyboardInterrupt` at main menu | Print "Goodbye!" and exit cleanly |
| Unhandled exception in AI Providers block | Show red error panel; do not crash the GUI loop |

---

## Acceptance Criteria

- [ ] `🤖 AI Providers` appears in `--gui` menu choices
- [ ] `provider_status_command()` called before any action prompt
- [ ] Status panel shows provider ID, display name, profile name, masked key, and model
- [ ] "No active provider" panel shown (not an error/crash) when `AI_ACTIVE_PROVIDER` unset
- [ ] `⚙️ Run guided setup` launches `configure_command(ConfigureOptions())`
- [ ] `↩ Back` returns to main menu without any state change
- [ ] `KeyboardInterrupt` inside AI Providers block does not produce a traceback
- [ ] `KeyboardInterrupt` at main menu exits cleanly with a farewell message
- [ ] All existing GUI menu choices continue to function correctly


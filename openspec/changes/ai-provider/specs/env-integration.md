# Specification: .env Integration

## Change ID
`AI-PROVIDER-001`

## Section
`specs/env-integration.md`

---

## Overview

The repo-root `.env` file is the single source of truth for all AI provider credentials, active-profile state, and per-profile settings. No runtime (Python or TypeScript) may maintain a separate credential store.

**Critical Rule**: No runtime may maintain its own credential store; all reads and writes target the repo-root `.env`.

---

## Functional Requirements

### FR-1: Single Credential Store
- All AI provider keys and active-profile state shall be stored exclusively in the `.env` file at the repo root.
- Neither `ai_providers.py` nor `ai_providers.ts` shall write credentials to any other file, database, or in-memory-only store that persists across restarts.

### FR-2: Key Naming Conventions
- Built-in provider API keys: `<PROVIDER_ID_UPPERCASE>_API_KEY`
  - e.g. `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_AI_API_KEY`
- Named profile API keys: `<PROVIDER_ID_UPPERCASE>_<PROFILE_NAME_UPPERCASE>_API_KEY`
  - e.g. `ANTHROPIC_PERSONAL_API_KEY`, `OPENAI_WORK_API_KEY`
- Optional per-profile model override: `<PROVIDER_ID_UPPERCASE>_<PROFILE_NAME_UPPERCASE>_MODEL`
- Optional base URL (custom/self-hosted): `<PROVIDER_ID_UPPERCASE>_BASE_URL`
- Active state: `AI_ACTIVE_PROVIDER`, `AI_ACTIVE_PROFILE`

### FR-3: Python Write Rules
- All `.env` writes shall use `dotenv.set_key(dotenv_path, key, value)`.
- Full-file overwrite of `.env` is strictly prohibited.
- `dotenv.set_key()` shall be the only function used to write or update key/value pairs.
- Reads shall use `os.getenv()` after `dotenv.load_dotenv()` has been called.

### FR-4: TypeScript Read Rules
- TypeScript files shall load `.env` via `dotenv.config({ path: resolve(__dirname, '../../.env') })` or `import 'dotenv/config'`.
- TypeScript files shall read values from `process.env` only.
- TypeScript files shall not write to `.env` directly; all write operations shall delegate to the Python CLI via `spawnSync`.

### FR-5: Idempotent Reads
- `load_dotenv()` and `dotenv.config()` shall be safe to call multiple times without side effects.
- Reading a key that does not exist shall return `undefined` (TS) or `None` (Python), never throw.

### FR-6: `.env` Not Committed
- `.env` shall remain in `.gitignore` per existing project convention.
- A `.env.example` file (committed) shall document all new key names with empty values.

---

## Technical Specification

### `.env` Key Schema

| Key | Example Value | Required | Written By |
|-----|--------------|----------|-----------|
| `AI_ACTIVE_PROVIDER` | `anthropic` | No (until configured) | `provider_activate_command()` |
| `AI_ACTIVE_PROFILE` | `personal` | No (until configured) | `provider_activate_command()` |
| `ANTHROPIC_API_KEY` | `sk-ant-...` | If using Anthropic | `provider_create_command()` |
| `ANTHROPIC_<PROFILE>_API_KEY` | `sk-ant-...` | Named profile | `provider_create_command()` |
| `ANTHROPIC_<PROFILE>_MODEL` | `claude-3-5-sonnet-20241022` | Optional | `provider_create_command()` |
| `OPENAI_API_KEY` | `sk-...` | If using OpenAI | `provider_create_command()` |
| `OPENAI_<PROFILE>_API_KEY` | `sk-...` | Named profile | `provider_create_command()` |
| `GOOGLE_AI_API_KEY` | `AIza...` | If using Google AI | `provider_create_command()` |
| `GOOGLE_AI_<PROFILE>_API_KEY` | `AIza...` | Named profile | `provider_create_command()` |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | If using Ollama | `provider_create_command()` |
| `LOCALAI_BASE_URL` | `http://localhost:8080` | If using LocalAI | `provider_create_command()` |
| `<CUSTOM_ID>_API_KEY` | `...` | Custom provider | `provider_create_command()` |
| `<CUSTOM_ID>_BASE_URL` | `http://...` | Self-hosted | `provider_create_command()` |

### `.env.example` Template

```dotenv
# ============================================================
# AI Provider Configuration — managed by ai_providers.py
# ============================================================

# Active provider and profile (set via 'configure --activate-profile')
AI_ACTIVE_PROVIDER=
AI_ACTIVE_PROFILE=

# Built-in Provider API Keys
# Anthropic (https://console.anthropic.com)
ANTHROPIC_API_KEY=

# OpenAI (https://platform.openai.com)
OPENAI_API_KEY=

# Google AI / Gemini (https://aistudio.google.com)
GOOGLE_AI_API_KEY=

# Self-hosted / Community Providers
# OLLAMA_BASE_URL=http://localhost:11434
# LOCALAI_BASE_URL=http://localhost:8080

# Named profile example (created by 'configure --create-profile anthropic/work')
# ANTHROPIC_WORK_API_KEY=
# ANTHROPIC_WORK_MODEL=claude-3-haiku-20240307
```

### Python Read/Write Pattern

```python
from dotenv import load_dotenv, set_key
from pathlib import Path
import os

DOTENV_PATH = Path(__file__).parent / ".env"
load_dotenv(DOTENV_PATH)

# Read
provider_id = os.getenv("AI_ACTIVE_PROVIDER")

# Write — safe, targeted, never overwrites other vars
set_key(str(DOTENV_PATH), "AI_ACTIVE_PROVIDER", "anthropic")
set_key(str(DOTENV_PATH), "AI_ACTIVE_PROFILE", "personal")
set_key(str(DOTENV_PATH), "ANTHROPIC_PERSONAL_API_KEY", api_key_value)
```

### TypeScript Read + Write-Back Pattern

```typescript
import { config } from 'dotenv';
import { resolve } from 'path';
import { spawnSync } from 'child_process';

config({ path: resolve(__dirname, '../../.env') });

// Read
const providerId = process.env.AI_ACTIVE_PROVIDER;

// Write-back — delegate to Python CLI
function activateProfile(providerId: string, profileName: string): void {
  spawnSync('python', [
    'generate_documentation.py', 'configure',
    '--activate-profile', `${providerId}/${profileName}`,
  ], { stdio: 'inherit' });
}
```

---

## Validation Rules

| Scenario | Behavior |
|----------|----------|
| `.env` file missing at startup | Log warning; do not raise; create on first write |
| `AI_ACTIVE_PROVIDER` set to unregistered ID | Raise `ProviderNotConfiguredError` with helpful message |
| Named profile key missing | Raise `ProfileNotFoundError` with the expected env var name |
| `set_key()` called on read-only `.env` | Raise `IOError` with file path in message |
| TypeScript reads before `dotenv.config()` | `process.env` returns `undefined`; guard with null check |

---

## Acceptance Criteria

- [ ] All reads use `os.getenv()` (Python) or `process.env` (TypeScript)
- [ ] All writes use `dotenv.set_key()` exclusively (Python)
- [ ] No full-file `.env` overwrite occurs anywhere in the codebase
- [ ] TypeScript write-back delegates to Python CLI subprocess
- [ ] `.env.example` committed to repo with all new key templates
- [ ] `.env` remains in `.gitignore`
- [ ] Missing `.env` at startup logs a warning but does not crash
- [ ] `AI_ACTIVE_PROVIDER` set to unknown ID raises `ProviderNotConfiguredError` (not `KeyError`)


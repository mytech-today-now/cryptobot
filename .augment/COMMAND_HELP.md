# Command Help Reference

Auto-generated command-line help for Augment workflow tools.

**Generated**: 2026-03-13T18:11:56.821Z
**Tools**: Augx, Beads, OpenSpec
**Version**: 1.0.0

---

## Augx Commands (augx)

### augx --help

```
Usage: augx [options] [command]

CLI tool for managing Augment Code AI extension modules

Options:
  -V, --version                        output the version number
  -h, --help                           display help for command

Commands:
  init [options]                       Initialize Augment Extensions in current
                                       project (includes Beads integration if
                                       .beads/ exists)
  gui                                  Launch interactive GUI for module
                                       management
  list [options]                       List available or linked extension
                                       modules
  show [options] <module> [file-path]  Display detailed information about a
                                       module (use "completed" to show Beads
                                       completed tasks, "linked" for linked
                                       modules, "all" for all modules)
  use [options] <module>               Select and load a specific module
                                       version
  upgrade [options] <module>           Upgrade module to latest version
  version-info [options] <module>      Show detailed version information
  link [options] <module>              Link an extension module to current
                                       project
  unlink [options] <module>            Unlink an extension module or collection
                                       from current project
  update [options]                     Update CLI and/or linked modules to
                                       latest versions
  search [options] <keyword>           Search for extension modules
  create [options] <name>              Create a new extension module
  validate [options] <module>          Validate module structure and metadata
  pin <module> <version>               Pin module to specific version
  check-updates                        Check for available module updates
  self-remove [options]                Completely remove all Augment Extensions
                                       from the project
  diff <module>                        Show differences between current and
                                       latest version
  catalog [options]                    Update MODULES.md catalog with all
                                       available modules
  catalog-hook [options]               Setup git hook for automatic catalog
                                       updates
  install-rules [options]              Install character count management rule
                                       to .augment/rules
  coord                                Query coordination manifest data
  sync                                 Sync Beads and OpenSpec with
                                       coordination manifest
  migrate                              Migrate existing Beads and OpenSpec data
                                       to coordination system
  skill                                Manage skills
  mcp                                  Manage MCP server integrations
  code-analysis|analyze [options]      Analyze code for quality, complexity,
                                       security, and dependencies
  generate-shot-list [options]         Generate AI-optimized shot lists from
                                       screenplays
  help [command]                       display help for command

```

#### augx init --help

```
Usage: augx init [options] [command]

Initialize Augment Extensions in current project (includes Beads integration if
.beads/ exists)

Options:
  --from-submodule  Initialize from existing submodule
  -h, --help        display help for command

Commands:
  beads             Initialize Beads task tracking in current project

```

##### augx init beads --help

```
Usage: augx init beads [options]

Initialize Beads task tracking in current project

Options:
  -h, --help  display help for command

```

#### augx project --help

```
Usage: augx [options] [command]

CLI tool for managing Augment Code AI extension modules

Options:
  -V, --version                        output the version number
  -h, --help                           display help for command

Commands:
  init [options]                       Initialize Augment Extensions in current
                                       project (includes Beads integration if
                                       .beads/ exists)
  gui                                  Launch interactive GUI for module
                                       management
  list [options]                       List available or linked extension
                                       modules
  show [options] <module> [file-path]  Display detailed information about a
                                       module (use "completed" to show Beads
                                       completed tasks, "linked" for linked
                                       modules, "all" for all modules)
  use [options] <module>               Select and load a specific module
                                       version
  upgrade [options] <module>           Upgrade module to latest version
  version-info [options] <module>      Show detailed version information
  link [options] <module>              Link an extension module to current
                                       project
  unlink [options] <module>            Unlink an extension module or collection
                                       from current project
  update [options]                     Update CLI and/or linked modules to
                                       latest versions
  search [options] <keyword>           Search for extension modules
  create [options] <name>              Create a new extension module
  validate [options] <module>          Validate module structure and metadata
  pin <module> <version>               Pin module to specific version
  check-updates                        Check for available module updates
  self-remove [options]                Completely remove all Augment Extensions
                                       from the project
  diff <module>                        Show differences between current and
                                       latest version
  catalog [options]                    Update MODULES.md catalog with all
                                       available modules
  catalog-hook [options]               Setup git hook for automatic catalog
                                       updates
  install-rules [options]              Install character count management rule
                                       to .augment/rules
  coord                                Query coordination manifest data
  sync                                 Sync Beads and OpenSpec with
                                       coordination manifest
  migrate                              Migrate existing Beads and OpenSpec data
                                       to coordination system
  skill                                Manage skills
  mcp                                  Manage MCP server integrations
  code-analysis|analyze [options]      Analyze code for quality, complexity,
                                       security, and dependencies
  generate-shot-list [options]         Generate AI-optimized shot lists from
                                       screenplays
  help [command]                       display help for command

```

##### augx project init --help

```
Usage: augx [options] [command]

CLI tool for managing Augment Code AI extension modules

Options:
  -V, --version                        output the version number
  -h, --help                           display help for command

Commands:
  init [options]                       Initialize Augment Extensions in current
                                       project (includes Beads integration if
                                       .beads/ exists)
  gui                                  Launch interactive GUI for module
                                       management
  list [options]                       List available or linked extension
                                       modules
  show [options] <module> [file-path]  Display detailed information about a
                                       module (use "completed" to show Beads
                                       completed tasks, "linked" for linked
                                       modules, "all" for all modules)
  use [options] <module>               Select and load a specific module
                                       version
  upgrade [options] <module>           Upgrade module to latest version
  version-info [options] <module>      Show detailed version information
  link [options] <module>              Link an extension module to current
                                       project
  unlink [options] <module>            Unlink an extension module or collection
                                       from current project
  update [options]                     Update CLI and/or linked modules to
                                       latest versions
  search [options] <keyword>           Search for extension modules
  create [options] <name>              Create a new extension module
  validate [options] <module>          Validate module structure and metadata
  pin <module> <version>               Pin module to specific version
  check-updates                        Check for available module updates
  self-remove [options]                Completely remove all Augment Extensions
                                       from the project
  diff <module>                        Show differences between current and
                                       latest version
  catalog [options]                    Update MODULES.md catalog with all
                                       available modules
  catalog-hook [options]               Setup git hook for automatic catalog
                                       updates
  install-rules [options]              Install character count management rule
                                       to .augment/rules
  coord                                Query coordination manifest data
  sync                                 Sync Beads and OpenSpec with
                                       coordination manifest
  migrate                              Migrate existing Beads and OpenSpec data
                                       to coordination system
  skill                                Manage skills
  mcp                                  Manage MCP server integrations
  code-analysis|analyze [options]      Analyze code for quality, complexity,
                                       security, and dependencies
  generate-shot-list [options]         Generate AI-optimized shot lists from
                                       screenplays
  help [command]                       display help for command

```

##### augx project project --help

```
Usage: augx [options] [command]

CLI tool for managing Augment Code AI extension modules

Options:
  -V, --version                        output the version number
  -h, --help                           display help for command

Commands:
  init [options]                       Initialize Augment Extensions in current
                                       project (includes Beads integration if
                                       .beads/ exists)
  gui                                  Launch interactive GUI for module
                                       management
  list [options]                       List available or linked extension
                                       modules
  show [options] <module> [file-path]  Display detailed information about a
                                       module (use "completed" to show Beads
                                       completed tasks, "linked" for linked
                                       modules, "all" for all modules)
  use [options] <module>               Select and load a specific module
                                       version
  upgrade [options] <module>           Upgrade module to latest version
  version-info [options] <module>      Show detailed version information
  link [options] <module>              Link an extension module to current
                                       project
  unlink [options] <module>            Unlink an extension module or collection
                                       from current project
  update [options]                     Update CLI and/or linked modules to
                                       latest versions
  search [options] <keyword>           Search for extension modules
  create [options] <name>              Create a new extension module
  validate [options] <module>          Validate module structure and metadata
  pin <module> <version>               Pin module to specific version
  check-updates                        Check for available module updates
  self-remove [options]                Completely remove all Augment Extensions
                                       from the project
  diff <module>                        Show differences between current and
                                       latest version
  catalog [options]                    Update MODULES.md catalog with all
                                       available modules
  catalog-hook [options]               Setup git hook for automatic catalog
                                       updates
  install-rules [options]              Install character count management rule
                                       to .augment/rules
  coord                                Query coordination manifest data
  sync                                 Sync Beads and OpenSpec with
                                       coordination manifest
  migrate                              Migrate existing Beads and OpenSpec data
                                       to coordination system
  skill                                Manage skills
  mcp                                  Manage MCP server integrations
  code-analysis|analyze [options]      Analyze code for quality, complexity,
                                       security, and dependencies
  generate-shot-list [options]         Generate AI-optimized shot lists from
                                       screenplays
  help [command]                       display help for command

```

---

## Beads Commands (bd)

### bd --help

```
Issues chained together like beads. A lightweight issue tracker with first-class dependency support.

Usage:
  bd [flags]
  bd [command]

Working With Issues:
  children        List child beads of a parent
  close           Close one or more issues
  comments        View or manage comments on an issue
  create          Create a new issue (or multiple issues from markdown file)
  create-form     Create a new issue using an interactive form
  delete          Delete one or more issues and clean up references
  edit            Edit an issue field in $EDITOR
  gate            Manage async coordination gates
  label           Manage issue labels
  list            List issues
  merge-slot      Manage merge-slot gates for serialized conflict resolution
  move            Move an issue to a different rig with dependency remapping
  promote         Promote a wisp to a permanent bead
  q               Quick capture: create issue and output only ID
  query           Query issues using a simple query language
  refile          Move an issue to a different rig
  reopen          Reopen one or more closed issues
  search          Search issues by text query
  set-state       Set operational state (creates event + updates label)
  show            Show issue details
  state           Query the current value of a state dimension
  todo            Manage TODO items (convenience wrapper for task issues)
  update          Update one or more issues

Views & Reports:
  count           Count issues matching filters
  diff            Show changes between two commits or branches (requires Dolt backend)
  find-duplicates Find semantically similar issues using text analysis or AI
  history         Show version history for an issue (requires Dolt backend)
  lint            Check issues for missing template sections
  stale           Show stale issues (not updated recently)
  status          Show issue database overview and statistics
  types           List valid issue types

Dependencies & Structure:
  dep             Manage dependencies
  duplicate       Mark an issue as a duplicate of another
  duplicates      Find and optionally merge duplicate issues
  epic            Epic management commands
  graph           Display issue dependency graph
  supersede       Mark an issue as superseded by a newer one
  swarm           Swarm management for structured epics

Sync & Data:
  backup          Back up your beads database
  branch          List or create branches (requires Dolt backend)
  export          Export issues to JSONL format
  federation      Manage peer-to-peer federation with other Gas Towns
  restore         Restore full history of a compacted issue from Dolt history
  vc              Version control operations (requires Dolt backend)

Setup & Configuration:
  bootstrap       Non-destructive database setup for fresh clones and recovery
  config          Manage configuration settings
  context         Show effective backend identity and repository context
  dolt            Configure Dolt database settings
  forget          Remove a persistent memory
  hooks           Manage git hooks for beads integration
  human           Show essential commands for human users
  info            Show database information
  init            Initialize bd in the current directory
  kv              Key-value store commands
  memories        List or search persistent memories
  onboard         Display minimal snippet for AGENTS.md
  prime           Output AI-optimized workflow context
  quickstart      Quick start guide for bd
  recall          Retrieve a specific memory
  remember        Store a persistent memory
  setup           Setup integration with AI editors
  where           Show active beads location

Maintenance:
  compact         Squash old Dolt commits to reduce history size
  doctor          Check and fix beads installation health (start here)
  flatten         Squash all Dolt history into a single commit
  gc              Garbage collect: decay old issues, compact Dolt commits, run Dolt GC
  migrate         Database migration commands
  preflight       Show PR readiness checklist
  purge           Delete closed ephemeral beads to reclaim space
  rename-prefix   Rename the issue prefix for all issues in the database
  sql             Execute raw SQL against the beads database
  upgrade         Check and manage bd version upgrades
  worktree        Manage git worktrees for parallel development

Integrations & Advanced:
  admin           Administrative commands for database maintenance
  jira            Jira integration commands
  linear          Linear integration commands
  repo            Manage multiple repository configuration

Additional Commands:
  agent           Manage agent bead state
  audit           Record and label agent interactions (append-only JSONL)
  blocked         Show blocked issues
  completion      Generate the autocompletion script for the specified shell
  cook            Compile a formula into a proto (ephemeral by default)
  defer           Defer one or more issues for later
  formula         Manage workflow formulas
  github          GitHub integration commands
  gitlab          GitLab integration commands
  help            Help about any command
  mail            Delegate to mail provider (e.g., gt mail)
  mol             Molecule commands (work templates)
  orphans         Identify orphaned issues (referenced in commits but still open)
  ready           Show ready work (open, no active blockers)
  rename          Rename an issue ID
  ship            Publish a capability for cross-project dependencies
  slot            Manage agent bead slots
  undefer         Undefer one or more issues (restore to open)
  version         Print version information

Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
  -h, --help                      help for bd
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output
  -V, --version                   Print version information

Use "bd [command] --help" for more information about a command.

```

#### bd agent --help

```
Manage state on agent beads for ZFC-compliant state reporting.

Agent beads (labeled gt:agent) can self-report their state using these commands.
This enables the Witness and other monitoring systems to track agent health.

States:
  idle      - Agent is waiting for work
  spawning  - Agent is starting up
  running   - Agent is executing (general)
  working   - Agent is actively working on a task
  stuck     - Agent is blocked and needs help
  done      - Agent completed its current work
  stopped   - Agent has cleanly shut down
  dead      - Agent died without clean shutdown (set by Witness via timeout)

Examples:
  bd agent state gt-emma running     # Set emma's state to running
  bd agent heartbeat gt-emma         # Update emma's last_activity timestamp
  bd agent show gt-emma              # Show emma's agent details

Usage:
  bd agent [command]

Available Commands:
  backfill-labels Backfill role_type/rig labels on existing agent beads
  heartbeat       Update agent last_activity timestamp
  show            Show agent bead details
  state           Set agent state

Flags:
  -h, --help   help for agent

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

Use "bd agent [command] --help" for more information about a command.

```

##### bd agent backfill --help

```
Manage state on agent beads for ZFC-compliant state reporting.

Agent beads (labeled gt:agent) can self-report their state using these commands.
This enables the Witness and other monitoring systems to track agent health.

States:
  idle      - Agent is waiting for work
  spawning  - Agent is starting up
  running   - Agent is executing (general)
  working   - Agent is actively working on a task
  stuck     - Agent is blocked and needs help
  done      - Agent completed its current work
  stopped   - Agent has cleanly shut down
  dead      - Agent died without clean shutdown (set by Witness via timeout)

Examples:
  bd agent state gt-emma running     # Set emma's state to running
  bd agent heartbeat gt-emma         # Update emma's last_activity timestamp
  bd agent show gt-emma              # Show emma's agent details

Usage:
  bd agent [command]

Available Commands:
  backfill-labels Backfill role_type/rig labels on existing agent beads
  heartbeat       Update agent last_activity timestamp
  show            Show agent bead details
  state           Set agent state

Flags:
  -h, --help   help for agent

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

Use "bd agent [command] --help" for more information about a command.

```

##### bd agent heartbeat --help

```
Update the last_activity timestamp of an agent bead without changing state.

Use this for periodic heartbeats to indicate the agent is still alive.
The Witness can use this to detect dead agents via timeout.

Examples:
  bd agent heartbeat gt-emma   # Update emma's last_activity
  bd agent heartbeat gt-mayor  # Update mayor's last_activity

Usage:
  bd agent heartbeat <agent> [flags]

Flags:
  -h, --help   help for heartbeat

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd agent show --help

```
Show detailed information about an agent bead.

Displays agent-specific fields including state, last_activity, hook, and role.

Examples:
  bd agent show gt-emma   # Show emma's agent details
  bd agent show gt-mayor  # Show mayor's agent details

Usage:
  bd agent show <agent> [flags]

Flags:
  -h, --help   help for show

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd agent state --help

```
Set the state of an agent bead.

This updates both the agent_state field and the last_activity timestamp.
Use this for ZFC-compliant state reporting.

Valid states: idle, spawning, running, working, stuck, done, stopped, dead

Examples:
  bd agent state gt-emma running   # Set state to running
  bd agent state gt-mayor idle     # Set state to idle

Usage:
  bd agent state <agent> <state> [flags]

Flags:
  -h, --help   help for state

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

#### bd audit --help

```
Audit log entries are appended to .beads/interactions.jsonl.

Each line is one event. This file is intended to be versioned in git and used for:
- auditing ("why did the agent do that?")
- dataset generation (SFT/RL fine-tuning)

Entries are append-only. Labeling creates a new "label" entry that references a parent entry.

Usage:
  bd audit [command]

Available Commands:
  label       Append a label entry referencing an existing interaction
  record      Append an audit interaction entry

Flags:
  -h, --help   help for audit

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

Use "bd audit [command] --help" for more information about a command.

```

##### bd audit label --help

```
Append a label entry referencing an existing interaction

Usage:
  bd audit label <entry-id> [flags]

Flags:
  -h, --help            help for label
      --label string    Label value (e.g. "good" or "bad")
      --reason string   Reason for label

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd audit record --help

```
Append an audit interaction entry

Usage:
  bd audit record [flags]

Flags:
      --error string       Error string (llm_call/tool_call)
      --exit-code int      Exit code (tool_call) (default -1)
  -h, --help               help for record
      --issue-id string    Related issue id (bd-...)
      --kind string        Entry kind (e.g. llm_call, tool_call, label)
      --model string       Model name (llm_call)
      --prompt string      Prompt text (llm_call)
      --response string    Response text (llm_call)
      --stdin              Read a JSON object from stdin (must match audit.Entry schema)
      --tool-name string   Tool name (tool_call)

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

#### bd blocked --help

```
Show blocked issues

Usage:
  bd blocked [flags]

Flags:
  -h, --help            help for blocked
      --parent string   Filter to descendants of this bead/epic

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

#### bd completion --help

```
Generate the autocompletion script for bd for the specified shell.
See each sub-command's help for details on how to use the generated script.


Usage:
  bd completion [command]

Available Commands:
  bash        Generate the autocompletion script for bash
  fish        Generate the autocompletion script for fish
  powershell  Generate the autocompletion script for powershell
  zsh         Generate the autocompletion script for zsh

Flags:
  -h, --help   help for completion

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

Use "bd completion [command] --help" for more information about a command.

```

##### bd completion bash --help

```
Generate the autocompletion script for the bash shell.

This script depends on the 'bash-completion' package.
If it is not installed already, you can install it via your OS's package manager.

To load completions in your current shell session:
	source <(bd completion bash)

To load completions for every new session, execute once:

#### Linux:

	bd completion bash > /etc/bash_completion.d/bd

#### macOS:

	bd completion bash > $(brew --prefix)/etc/bash_completion.d/bd

You will need to start a new shell for this setup to take effect.


Usage:
  bd completion bash

Flags:
  -h, --help              help for bash
      --no-descriptions   disable completion descriptions

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd completion fish --help

```
Generate the autocompletion script for the fish shell.

To load completions in your current shell session:
	bd completion fish | source

To load completions for every new session, execute once:

	bd completion fish > ~/.config/fish/completions/bd.fish

You will need to start a new shell for this setup to take effect.


Usage:
  bd completion fish [flags]

Flags:
  -h, --help              help for fish
      --no-descriptions   disable completion descriptions

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd completion powershell --help

```
Generate the autocompletion script for powershell.

To load completions in your current shell session:
	bd completion powershell | Out-String | Invoke-Expression

To load completions for every new session, add the output of the above command
to your powershell profile.


Usage:
  bd completion powershell [flags]

Flags:
  -h, --help              help for powershell
      --no-descriptions   disable completion descriptions

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd completion zsh --help

```
Generate the autocompletion script for the zsh shell.

If shell completion is not already enabled in your environment you will need
to enable it.  You can execute the following once:

	echo "autoload -U compinit; compinit" >> ~/.zshrc

To load completions in your current shell session:
	source <(bd completion zsh)

To load completions for every new session, execute once:

#### Linux:

	bd completion zsh > "${fpath[1]}/_bd"

#### macOS:

	bd completion zsh > $(brew --prefix)/share/zsh/site-functions/_bd

You will need to start a new shell for this setup to take effect.


Usage:
  bd completion zsh [flags]

Flags:
  -h, --help              help for zsh
      --no-descriptions   disable completion descriptions

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

#### bd cook --help

```
Cook transforms a .formula.json file into a proto.

By default, cook outputs the resolved formula as JSON to stdout for
ephemeral use. The output can be inspected, piped, or saved to a file.

Two cooking modes are available:
  COMPILE-TIME (default, --mode=compile):
    Produces a proto with {{variable}} placeholders intact.
    Use for: modeling, estimation, contractor handoff, planning.
    Variables are NOT substituted - the output shows the template structure.

  RUNTIME (--mode=runtime or when --var flags provided):
    Produces a fully-resolved proto with variables substituted.
    Use for: final validation before pour, seeing exact output.
    Requires all variables to have values (via --var or defaults).

Formulas are high-level workflow templates that support:
  - Variable definitions with defaults and validation
  - Step definitions that become issue hierarchies
  - Composition rules for bonding formulas together
  - Inheritance via extends

The --persist flag enables the legacy behavior of writing the proto
to the database. This is useful when you want to reuse the same
proto multiple times without re-cooking.

For most workflows, prefer ephemeral protos: pour and wisp commands
accept formula names directly and cook inline.

Examples:
  bd cook mol-feature.formula.json                    # Compile-time: keep {{vars}}
  bd cook mol-feature --var name=auth                 # Runtime: substitute vars
  bd cook mol-feature --mode=runtime --var name=auth  # Explicit runtime mode
  bd cook mol-feature --dry-run                       # Preview steps
  bd cook mol-release.formula.json --persist          # Write to database
  bd cook mol-release.formula.json --persist --force  # Replace existing

Output (default):
  JSON representation of the resolved formula with all steps.

Output (--persist):
  Creates a proto bead in the database with:
  - ID matching the formula name (e.g., mol-feature)
  - The "template" label for proto identification
  - Child issues for each step
  - Dependencies matching depends_on relationships

Usage:
  bd cook <formula-file> [flags]

Flags:
      --dry-run               Preview what would be created
      --force                 Replace existing proto if it exists (requires --persist)
  -h, --help                  help for cook
      --mode string           Cooking mode: compile (keep placeholders) or runtime (substitute vars)
      --persist               Persist proto to database (legacy behavior)
      --prefix string         Prefix to prepend to proto ID (e.g., 'gt-' creates 'gt-mol-feature')
      --search-path strings   Additional paths to search for formula inheritance
      --var stringArray       Variable substitution (key=value), enables runtime mode

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

#### bd defer --help

```
Defer issues to put them on ice for later.

Deferred issues are deliberately set aside - not blocked by anything specific,
just postponed for future consideration. Unlike blocked issues, there's no
dependency keeping them from being worked. Unlike closed issues, they will
be revisited.

Deferred issues don't show in 'bd ready' but remain visible in 'bd list'.

Examples:
  bd defer bd-abc                  # Defer a single issue (status-based)
  bd defer bd-abc --until=tomorrow # Defer until specific time
  bd defer bd-abc bd-def           # Defer multiple issues

Usage:
  bd defer [id...] [flags]

Flags:
  -h, --help           help for defer
      --until string   Defer until specific time (e.g., +1h, tomorrow, next monday)

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

#### bd formula --help

```
Manage workflow formulas - the source layer for molecule templates.

Formulas are YAML/JSON files that define workflows with composition rules.
They are "cooked" into proto beads which can then be poured or wisped.

The Rig → Cook → Run lifecycle:
  - Rig: Compose formulas (extends, compose)
  - Cook: Transform to proto (bd cook expands macros, applies aspects)
  - Run: Agents execute poured mols or wisps

Search paths (in order):
  1. .beads/formulas/ (project)
  2. ~/.beads/formulas/ (user)
  3. $GT_ROOT/.beads/formulas/ (orchestrator, if GT_ROOT set)

Commands:
  list   List available formulas from all search paths
  show   Show formula details, steps, and composition rules

Usage:
  bd formula [command]

Available Commands:
  convert     Convert formula from JSON to TOML
  list        List available formulas
  show        Show formula details

Flags:
  -h, --help   help for formula

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

Use "bd formula [command] --help" for more information about a command.

```

##### bd formula bd --help

```
Manage workflow formulas - the source layer for molecule templates.

Formulas are YAML/JSON files that define workflows with composition rules.
They are "cooked" into proto beads which can then be poured or wisped.

The Rig → Cook → Run lifecycle:
  - Rig: Compose formulas (extends, compose)
  - Cook: Transform to proto (bd cook expands macros, applies aspects)
  - Run: Agents execute poured mols or wisps

Search paths (in order):
  1. .beads/formulas/ (project)
  2. ~/.beads/formulas/ (user)
  3. $GT_ROOT/.beads/formulas/ (orchestrator, if GT_ROOT set)

Commands:
  list   List available formulas from all search paths
  show   Show formula details, steps, and composition rules

Usage:
  bd formula [command]

Available Commands:
  convert     Convert formula from JSON to TOML
  list        List available formulas
  show        Show formula details

Flags:
  -h, --help   help for formula

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

Use "bd formula [command] --help" for more information about a command.

```

##### bd formula convert --help

```
Convert formula files from JSON to TOML format.

TOML format provides better ergonomics:
  - Multi-line strings without \n escaping
  - Human-readable diffs
  - Comments allowed

The convert command reads a .formula.json file and outputs .formula.toml.
The original JSON file is preserved (use --delete to remove it).

Examples:
  bd formula convert shiny              # Convert shiny.formula.json to .toml
  bd formula convert ./my.formula.json  # Convert specific file
  bd formula convert --all              # Convert all JSON formulas
  bd formula convert shiny --delete     # Convert and remove JSON file
  bd formula convert shiny --stdout     # Print TOML to stdout

Usage:
  bd formula convert <formula-name|path> [--all] [flags]

Flags:
      --all      Convert all JSON formulas
      --delete   Delete JSON file after conversion
  -h, --help     help for convert
      --stdout   Print TOML to stdout instead of file

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd formula list --help

```
List all formulas from search paths.

Search paths (in order of priority):
  1. .beads/formulas/ (project - highest priority)
  2. ~/.beads/formulas/ (user)
  3. $GT_ROOT/.beads/formulas/ (orchestrator, if GT_ROOT set)

Formulas in earlier paths shadow those with the same name in later paths.

Examples:
  bd formula list
  bd formula list --json
  bd formula list --type workflow
  bd formula list --type aspect

Usage:
  bd formula list [flags]

Flags:
  -h, --help          help for list
      --type string   Filter by type (workflow, expansion, aspect)

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd formula show --help

```
Show detailed information about a formula.

Displays:
  - Formula metadata (name, type, description)
  - Variables with defaults and constraints
  - Steps with dependencies
  - Composition rules (extends, aspects, expansions)
  - Bond points for external composition

Examples:
  bd formula show shiny
  bd formula show rule-of-five
  bd formula show security-audit --json

Usage:
  bd formula show <formula-name> [flags]

Flags:
  -h, --help   help for show

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

#### bd github --help

```
Commands for syncing issues between beads and GitHub.

Configuration can be set via 'bd config' or environment variables:
  github.token / GITHUB_TOKEN           - Personal access token
  github.owner / GITHUB_OWNER           - Repository owner
  github.repo / GITHUB_REPO             - Repository name
  github.repository / GITHUB_REPOSITORY - Combined "owner/repo" format
  github.url / GITHUB_API_URL           - Custom API URL (GitHub Enterprise)

Usage:
  bd github [command]

Available Commands:
  repos       List accessible GitHub repositories
  status      Show GitHub sync status
  sync        Sync issues with GitHub

Flags:
  -h, --help   help for github

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

Use "bd github [command] --help" for more information about a command.

```

##### bd github repos --help

```
List GitHub repositories that the configured token has access to.

Usage:
  bd github repos [flags]

Flags:
  -h, --help   help for repos

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd github status --help

```
Display current GitHub configuration and sync status.

Usage:
  bd github status [flags]

Flags:
  -h, --help   help for status

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd github sync --help

```
Synchronize issues between beads and GitHub.

By default, performs bidirectional sync:
- Pulls new/updated issues from GitHub to beads
- Pushes local beads issues to GitHub

Use --pull-only or --push-only to limit direction.

Usage:
  bd github sync [flags]

Flags:
      --dry-run         Show what would be synced without making changes
  -h, --help            help for sync
      --prefer-github   On conflict, use GitHub version
      --prefer-local    On conflict, keep local beads version
      --prefer-newer    On conflict, use most recent version (default)
      --pull-only       Only pull issues from GitHub
      --push-only       Only push issues to GitHub

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

#### bd gitlab --help

```
Commands for syncing issues between beads and GitLab.

Configuration can be set via 'bd config' or environment variables:
  gitlab.url / GITLAB_URL         - GitLab instance URL
  gitlab.token / GITLAB_TOKEN     - Personal access token
  gitlab.project_id / GITLAB_PROJECT_ID - Project ID or path

Usage:
  bd gitlab [command]

Available Commands:
  projects    List accessible GitLab projects
  status      Show GitLab sync status
  sync        Sync issues with GitLab

Flags:
  -h, --help   help for gitlab

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

Use "bd gitlab [command] --help" for more information about a command.

```

##### bd gitlab projects --help

```
List GitLab projects that the configured token has access to.

Usage:
  bd gitlab projects [flags]

Flags:
  -h, --help   help for projects

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd gitlab status --help

```
Display current GitLab configuration and sync status.

Usage:
  bd gitlab status [flags]

Flags:
  -h, --help   help for status

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd gitlab sync --help

```
Synchronize issues between beads and GitLab.

By default, performs bidirectional sync:
- Pulls new/updated issues from GitLab to beads
- Pushes local beads issues to GitLab

Use --pull-only or --push-only to limit direction.

Usage:
  bd gitlab sync [flags]

Flags:
      --dry-run         Show what would be synced without making changes
  -h, --help            help for sync
      --prefer-gitlab   On conflict, use GitLab version
      --prefer-local    On conflict, keep local beads version
      --prefer-newer    On conflict, use most recent version (default)
      --pull-only       Only pull issues from GitLab
      --push-only       Only push issues to GitLab

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

#### bd help --help

```
Help provides help for any command in the application.
Simply type bd help [path to command] for full details.

Usage:
  bd help [command] [flags]

Flags:
      --all          Show help for all commands in a single document
      --doc string   Generate markdown docs for a single command (use - for stdout)
  -h, --help         help for help
      --list         List all available commands

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

#### bd mail --help

```
Delegates mail operations to an external mail provider.

Agents often type 'bd mail' when working with beads, but mail functionality
is typically provided by the orchestrator. This command bridges that gap
by delegating to the configured mail provider.

Configuration (checked in order):
  1. BEADS_MAIL_DELEGATE or BD_MAIL_DELEGATE environment variable
  2. 'mail.delegate' config setting (bd config set mail.delegate "gt mail")

Examples:
  # Configure delegation (one-time setup)
  export BEADS_MAIL_DELEGATE="gt mail"
  # or
  bd config set mail.delegate "gt mail"

  # Then use bd mail as if it were gt mail
  bd mail inbox                    # Lists inbox
  bd mail send mayor/ -s "Hi"      # Sends mail
  bd mail read msg-123             # Reads a message

Usage:
  bd mail [subcommand] [args...] [flags]

Flags:
  -h, --help   help for mail

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

#### bd mol --help

```
Manage molecules - work templates for agent workflows.

Protos are template epics with the "template" label. They define a DAG of work
that can be spawned to create real issues (molecules).

The molecule metaphor:
  - A proto is an uninstantiated template (reusable work pattern)
  - Spawning creates a molecule (real issues) from the proto
  - Variables ({{key}}) are substituted during spawning
  - Bonding combines protos or molecules into compounds
  - Distilling extracts a proto from an ad-hoc epic

Commands:
  show       Show proto/molecule structure and variables
  pour       Instantiate proto as persistent mol (liquid phase)
  wisp       Instantiate proto as ephemeral wisp (vapor phase)
  bond       Polymorphic combine: proto+proto, proto+mol, mol+mol
  squash     Condense molecule to digest
  burn       Discard wisp
  distill    Extract proto from ad-hoc epic

Use "bd formula list" to list available formulas.

Usage:
  bd mol [command]

Aliases:
  mol, protomolecule

Available Commands:
  bond          Bond two protos or molecules together
  burn          Delete a molecule without creating a digest
  current       Show current position in molecule workflow
  distill       Extract a formula from an existing epic
  last-activity Show last activity timestamp for a molecule
  pour          Instantiate a proto as a persistent mol (solid -> liquid)
  progress      Show molecule progress summary
  ready         Find molecules ready for gate-resume dispatch
  seed          Verify formula accessibility or seed patrol formulas
  show          Show molecule details
  squash        Compress molecule execution into a digest
  stale         Detect complete-but-unclosed molecules
  wisp          Create or manage wisps (ephemeral molecules)

Flags:
  -h, --help   help for mol

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

Use "bd mol [command] --help" for more information about a command.

```

##### bd mol bd --help

```
Manage molecules - work templates for agent workflows.

Protos are template epics with the "template" label. They define a DAG of work
that can be spawned to create real issues (molecules).

The molecule metaphor:
  - A proto is an uninstantiated template (reusable work pattern)
  - Spawning creates a molecule (real issues) from the proto
  - Variables ({{key}}) are substituted during spawning
  - Bonding combines protos or molecules into compounds
  - Distilling extracts a proto from an ad-hoc epic

Commands:
  show       Show proto/molecule structure and variables
  pour       Instantiate proto as persistent mol (liquid phase)
  wisp       Instantiate proto as ephemeral wisp (vapor phase)
  bond       Polymorphic combine: proto+proto, proto+mol, mol+mol
  squash     Condense molecule to digest
  burn       Discard wisp
  distill    Extract proto from ad-hoc epic

Use "bd formula list" to list available formulas.

Usage:
  bd mol [command]

Aliases:
  mol, protomolecule

Available Commands:
  bond          Bond two protos or molecules together
  burn          Delete a molecule without creating a digest
  current       Show current position in molecule workflow
  distill       Extract a formula from an existing epic
  last-activity Show last activity timestamp for a molecule
  pour          Instantiate a proto as a persistent mol (solid -> liquid)
  progress      Show molecule progress summary
  ready         Find molecules ready for gate-resume dispatch
  seed          Verify formula accessibility or seed patrol formulas
  show          Show molecule details
  squash        Compress molecule execution into a digest
  stale         Detect complete-but-unclosed molecules
  wisp          Create or manage wisps (ephemeral molecules)

Flags:
  -h, --help   help for mol

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

Use "bd mol [command] --help" for more information about a command.

```

##### bd mol bond --help

```
Bond two protos or molecules to create a compound.

The bond command is polymorphic - it handles different operand types:

  formula + formula → cook both, compound proto
  formula + proto   → cook formula, compound proto
  formula + mol     → cook formula, spawn and attach
  proto + proto     → compound proto (reusable template)
  proto + mol       → spawn proto, attach to molecule
  mol + proto       → spawn proto, attach to molecule
  mol + mol         → join into compound molecule

Formula names (e.g., mol-polecat-arm) are cooked inline as ephemeral protos.
This avoids needing pre-cooked proto beads in the database.

Bond types:
  sequential (default) - B runs after A completes
  parallel            - B runs alongside A
  conditional         - B runs only if A fails

Phase control:
  By default, spawned protos follow the target's phase:
  - Attaching to mol (Ephemeral=false) → spawns as persistent (Ephemeral=false)
  - Attaching to ephemeral issue (Ephemeral=true) → spawns as ephemeral (Ephemeral=true)

  Override with:
  --pour  Force spawn as liquid (persistent, Ephemeral=false)
  --ephemeral  Force spawn as vapor (ephemeral, Ephemeral=true, excluded from Dolt sync via dolt_ignore)

Dynamic bonding (Christmas Ornament pattern):
  Use --ref to specify a custom child reference with variable substitution.
  This creates IDs like "parent.child-ref" instead of random hashes.

  Example:
    bd mol bond mol-polecat-arm bd-patrol --ref arm-{{polecat_name}} --var polecat_name=ace
    # Creates: bd-patrol.arm-ace (and children like bd-patrol.arm-ace.capture)

Use cases:
  - Found important bug during patrol? Use --pour to persist it
  - Need ephemeral diagnostic on persistent feature? Use --ephemeral
  - Spawning per-worker arms on a patrol? Use --ref for readable IDs

Examples:
  bd mol bond mol-feature mol-deploy                    # Compound proto
  bd mol bond mol-feature mol-deploy --type parallel    # Run in parallel
  bd mol bond mol-feature bd-abc123                     # Attach proto to molecule
  bd mol bond bd-abc123 bd-def456                       # Join two molecules
  bd mol bond mol-critical-bug wisp-patrol --pour       # Persist found bug
  bd mol bond mol-temp-check bd-feature --ephemeral          # Ephemeral diagnostic
  bd mol bond mol-arm bd-patrol --ref arm-{{name}} --var name=ace  # Dynamic child ID

Usage:
  bd mol bond <A> <B> [flags]

Aliases:
  bond, fart

Flags:
      --as string         Custom title for compound proto (proto+proto only)
      --dry-run           Preview what would be created
      --ephemeral         Force spawn as vapor (ephemeral, Ephemeral=true)
  -h, --help              help for bond
      --pour              Force spawn as liquid (persistent, Ephemeral=false)
      --ref string        Custom child reference with {{var}} substitution (e.g., arm-{{polecat_name}})
      --type string       Bond type: sequential, parallel, or conditional (default "sequential")
      --var stringArray   Variable substitution for spawned protos (key=value)

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd mol burn --help

```
Burn a molecule, deleting it without creating a digest.

Unlike squash (which creates a permanent digest before deletion), burn
completely removes the molecule with no trace. Use this for:
  - Abandoned patrol cycles
  - Crashed or failed workflows
  - Test/debug molecules you don't want to preserve

The burn operation differs based on molecule phase:
  - Wisp (ephemeral): Direct delete
  - Mol (persistent): Cascade delete (syncs to remotes)

CAUTION: This is a destructive operation. The molecule's data will be
permanently lost. If you want to preserve a summary, use 'bd mol squash'.

Example:
  bd mol burn bd-abc123              # Delete molecule with no trace
  bd mol burn bd-abc123 --dry-run    # Preview what would be deleted
  bd mol burn bd-abc123 --force      # Skip confirmation
  bd mol burn bd-a1 bd-b2 bd-c3      # Batch delete multiple wisps

Usage:
  bd mol burn <molecule-id> [molecule-id...] [flags]

Flags:
      --dry-run   Preview what would be deleted
      --force     Skip confirmation prompt
  -h, --help      help for burn

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd mol current --help

```
Show where you are in a molecule workflow.

If molecule-id is given, show status for that molecule.
If not given, infer from in_progress issues assigned to current agent.

The output shows all steps with status indicators:
  [done]     - Step is complete (closed)
  [current]  - Step is in_progress (you are here)
  [ready]    - Step is ready to start (unblocked)
  [blocked]  - Step is blocked by dependencies
  [pending]  - Step is waiting

For large molecules (>100 steps), a summary is shown instead.
Use --limit or --range to view specific steps:
  bd mol current <id> --limit 50       # Show first 50 steps
  bd mol current <id> --range 100-150  # Show steps 100-150

Usage:
  bd mol current [molecule-id] [flags]

Flags:
      --for string     Show molecules for a specific agent/assignee
  -h, --help           help for current
      --limit int      Maximum number of steps to display (0 = auto, use 'all' threshold)
      --range string   Display specific step range (e.g., '1-50', '100-150')

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd mol distill --help

```
Distill a molecule by extracting a reusable formula from an existing epic.

This is the reverse of pour: instead of formula → molecule, it's molecule → formula.

The distill command:
  1. Loads the existing epic and all its children
  2. Converts the structure to a .formula.json file
  3. Replaces concrete values with {{variable}} placeholders (via --var flags)

Use cases:
  - Team develops good workflow organically, wants to reuse it
  - Capture tribal knowledge as executable templates
  - Create starting point for similar future work

Variable syntax (both work - we detect which side is the concrete value):
  --var branch=feature-auth    Spawn-style: variable=value (recommended)
  --var feature-auth=branch    Substitution-style: value=variable

Output locations (first writable wins):
  1. .beads/formulas/       (project-level, default)
  2. ~/.beads/formulas/     (user-level, if project not writable)

Examples:
  bd mol distill bd-o5xe my-workflow
  bd mol distill bd-abc release-workflow --var feature_name=auth-refactor

Usage:
  bd mol distill <epic-id> [formula-name] [flags]

Flags:
      --dry-run           Preview what would be created
  -h, --help              help for distill
      --output string     Output directory for formula file
      --var stringArray   Replace value with {{variable}} placeholder (variable=value)

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd mol last --help

```
Manage molecules - work templates for agent workflows.

Protos are template epics with the "template" label. They define a DAG of work
that can be spawned to create real issues (molecules).

The molecule metaphor:
  - A proto is an uninstantiated template (reusable work pattern)
  - Spawning creates a molecule (real issues) from the proto
  - Variables ({{key}}) are substituted during spawning
  - Bonding combines protos or molecules into compounds
  - Distilling extracts a proto from an ad-hoc epic

Commands:
  show       Show proto/molecule structure and variables
  pour       Instantiate proto as persistent mol (liquid phase)
  wisp       Instantiate proto as ephemeral wisp (vapor phase)
  bond       Polymorphic combine: proto+proto, proto+mol, mol+mol
  squash     Condense molecule to digest
  burn       Discard wisp
  distill    Extract proto from ad-hoc epic

Use "bd formula list" to list available formulas.

Usage:
  bd mol [command]

Aliases:
  mol, protomolecule

Available Commands:
  bond          Bond two protos or molecules together
  burn          Delete a molecule without creating a digest
  current       Show current position in molecule workflow
  distill       Extract a formula from an existing epic
  last-activity Show last activity timestamp for a molecule
  pour          Instantiate a proto as a persistent mol (solid -> liquid)
  progress      Show molecule progress summary
  ready         Find molecules ready for gate-resume dispatch
  seed          Verify formula accessibility or seed patrol formulas
  show          Show molecule details
  squash        Compress molecule execution into a digest
  stale         Detect complete-but-unclosed molecules
  wisp          Create or manage wisps (ephemeral molecules)

Flags:
  -h, --help   help for mol

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

Use "bd mol [command] --help" for more information about a command.

```

##### bd mol mol --help

```
Manage molecules - work templates for agent workflows.

Protos are template epics with the "template" label. They define a DAG of work
that can be spawned to create real issues (molecules).

The molecule metaphor:
  - A proto is an uninstantiated template (reusable work pattern)
  - Spawning creates a molecule (real issues) from the proto
  - Variables ({{key}}) are substituted during spawning
  - Bonding combines protos or molecules into compounds
  - Distilling extracts a proto from an ad-hoc epic

Commands:
  show       Show proto/molecule structure and variables
  pour       Instantiate proto as persistent mol (liquid phase)
  wisp       Instantiate proto as ephemeral wisp (vapor phase)
  bond       Polymorphic combine: proto+proto, proto+mol, mol+mol
  squash     Condense molecule to digest
  burn       Discard wisp
  distill    Extract proto from ad-hoc epic

Use "bd formula list" to list available formulas.

Usage:
  bd mol [command]

Aliases:
  mol, protomolecule

Available Commands:
  bond          Bond two protos or molecules together
  burn          Delete a molecule without creating a digest
  current       Show current position in molecule workflow
  distill       Extract a formula from an existing epic
  last-activity Show last activity timestamp for a molecule
  pour          Instantiate a proto as a persistent mol (solid -> liquid)
  progress      Show molecule progress summary
  ready         Find molecules ready for gate-resume dispatch
  seed          Verify formula accessibility or seed patrol formulas
  show          Show molecule details
  squash        Compress molecule execution into a digest
  stale         Detect complete-but-unclosed molecules
  wisp          Create or manage wisps (ephemeral molecules)

Flags:
  -h, --help   help for mol

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

Use "bd mol [command] --help" for more information about a command.

```

##### bd mol pour --help

```
Pour a proto into a persistent mol - like pouring molten metal into a mold.

This is the chemistry-inspired command for creating PERSISTENT work from templates.
The resulting mol lives in .beads/ (permanent storage) and is synced with git.

Phase transition: Proto (solid) -> pour -> Mol (liquid)

WHEN TO USE POUR vs WISP:
  pour (liquid): Persistent work that needs audit trail
    - Feature implementations spanning multiple sessions
    - Work you may need to reference later
    - Anything worth preserving in git history

  wisp (vapor): Ephemeral work that auto-cleans up
    - Release workflows (one-time execution)
    - Patrol cycles (deacon, witness, refinery)
    - Health checks and diagnostics
    - Any operational workflow without audit value

TIP: Formulas can specify phase:"vapor" to recommend wisp usage.
     If you pour a vapor-phase formula, you'll get a warning.

Examples:
  bd mol pour mol-feature --var name=auth    # Persistent feature work
  bd mol pour mol-review --var pr=123        # Persistent code review

Usage:
  bd mol pour <proto-id> [flags]

Flags:
      --assignee string      Assign the root issue to this agent/user
      --attach strings       Proto to attach after spawning (repeatable)
      --attach-type string   Bond type for attachments: sequential, parallel, or conditional (default "sequential")
      --dry-run              Preview what would be created
  -h, --help                 help for pour
      --var stringArray      Variable substitution (key=value)

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd mol progress --help

```
Show efficient progress summary for a molecule.

This command uses indexed queries to count progress without loading all steps,
making it suitable for very large molecules (millions of steps).

If no molecule-id is given, shows progress for any molecule you're working on.

Output includes:
  - Progress: completed / total (percentage)
  - Current step: the in-progress step (if any)
  - Rate: steps/hour based on closure times
  - ETA: estimated time to completion

Example:
  bd mol progress bd-hanoi-xyz

Usage:
  bd mol progress [molecule-id] [flags]

Flags:
  -h, --help   help for progress

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd mol ready --help

```
Find molecules where a gate has closed and the workflow is ready to resume.

This command discovers molecules waiting at a gate step where:
1. The molecule has a gate bead that blocks a step
2. The gate bead is now closed (condition satisfied)
3. The blocked step is now ready to proceed
4. No agent currently has this molecule hooked

This enables discovery-based resume without explicit waiter tracking.
The Deacon patrol uses this to find and dispatch gate-ready molecules.

Examples:
  bd mol ready --gated           # Find all gate-ready molecules
  bd mol ready --gated --json    # JSON output for automation

Usage:
  bd mol ready --gated [flags]

Flags:
  -h, --help   help for ready

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd mol seed --help

```
Verify that formulas are accessible and can be cooked.

The seed command checks formula search paths to ensure formulas exist
and can be loaded. This is useful for verifying system health before
patrols attempt to spawn work.

WITH --patrol FLAG:
  Verifies all three patrol formulas are accessible:
    - mol-deacon-patrol
    - mol-witness-patrol
    - mol-refinery-patrol

WITHOUT --patrol:
  Verifies the specified formula is accessible.

Formula search paths (checked in order):
  1. .beads/formulas/ (project level)
  2. ~/.beads/formulas/ (user level)
  3. $GT_ROOT/.beads/formulas/ (orchestrator level, if GT_ROOT set)

Examples:
  bd mol seed --patrol                    # Verify all patrol formulas
  bd mol seed mol-feature                 # Verify specific formula
  bd mol seed mol-review --var name=test  # Verify with variable substitution

Usage:
  bd mol seed [formula-name] [flags]

Flags:
  -h, --help              help for seed
      --patrol            Verify all patrol formulas (mol-deacon-patrol, mol-witness-patrol, mol-refinery-patrol)
      --var stringArray   Variable substitution for condition filtering (key=value)

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd mol show --help

```
Show molecule structure and details.

The --parallel flag highlights parallelizable steps:
  - Steps with no blocking dependencies can run in parallel
  - Shows which steps are ready to start now
  - Identifies parallel groups (steps that can run concurrently)

Example:
  bd mol show bd-patrol --parallel

Usage:
  bd mol show <molecule-id> [flags]

Flags:
  -h, --help       help for show
  -p, --parallel   Show parallel step analysis

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd mol squash --help

```
Squash a molecule's ephemeral children into a single digest issue.

This command collects all ephemeral child issues of a molecule (Ephemeral=true),
generates a summary digest, and promotes the wisps to persistent by
clearing their Wisp flag (or optionally deletes them).

The squash operation:
  1. Loads the molecule and all its children
  2. Filters to only wisps (ephemeral issues with Ephemeral=true)
  3. Generates a digest (summary of work done)
  4. Creates a permanent digest issue (Ephemeral=false)
  5. Clears Wisp flag on children (promotes to persistent)
     OR keeps them with --keep-children (default: delete)

AGENT INTEGRATION:
Use --summary to provide an AI-generated summary. This keeps bd as a pure
tool - the calling agent (orchestrator worker, Claude Code, etc.) is responsible
for generating intelligent summaries. Without --summary, a basic concatenation
of child issue content is used.

This is part of the wisp workflow: spawn creates wisps,
execution happens, squash compresses the trace into an outcome (digest).

Example:
  bd mol squash bd-abc123                    # Squash and promote children
  bd mol squash bd-abc123 --dry-run          # Preview what would be squashed
  bd mol squash bd-abc123 --keep-children    # Keep wisps after digest
  bd mol squash bd-abc123 --summary "Agent-generated summary of work done"

Usage:
  bd mol squash <molecule-id> [flags]

Flags:
      --dry-run          Preview what would be squashed
  -h, --help             help for squash
      --keep-children    Don't delete ephemeral children after squash
      --summary string   Agent-provided summary (bypasses auto-generation)

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd mol stale --help

```
Detect molecules (epics with children) that are complete but still open.

A molecule is considered stale if:
  1. All children are closed (Completed == Total)
  2. Root issue is still open
  3. Not assigned to anyone (optional, use --unassigned)
  4. Is blocking other work (optional, use --blocking)

By default, shows all complete-but-unclosed molecules.

Examples:
  bd mol stale              # List all stale molecules
  bd mol stale --json       # Machine-readable output
  bd mol stale --blocking   # Only show those blocking other work
  bd mol stale --unassigned # Only show unassigned molecules
  bd mol stale --all        # Include molecules with 0 children

Usage:
  bd mol stale [flags]

Flags:
      --all          Include molecules with 0 children
      --blocking     Only show molecules blocking other work
  -h, --help         help for stale
      --unassigned   Only show unassigned molecules

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd mol wisp --help

```
Create or manage wisps - EPHEMERAL molecules for operational workflows.

When called with a proto-id argument, creates a wisp from that proto.
When called with a subcommand (list, gc), manages existing wisps.

Wisps are issues with Ephemeral=true in the main database. They're stored
locally but NOT synced via git.

WHEN TO USE WISP vs POUR:
  wisp (vapor): Ephemeral work that auto-cleans up
    - Release workflows (one-time execution)
    - Patrol cycles (deacon, witness, refinery)
    - Health checks and diagnostics
    - Any operational workflow without audit value

  pour (liquid): Persistent work that needs audit trail
    - Feature implementations spanning multiple sessions
    - Work you may need to reference later
    - Anything worth preserving in git history

TIP: Formulas can specify phase:"vapor" to recommend wisp usage.
     If you use pour on a vapor-phase formula, you'll get a warning.

The wisp lifecycle:
  1. Create: bd mol wisp <proto> or bd create --ephemeral
  2. Execute: Normal bd operations work on wisp issues
  3. Squash: bd mol squash <id> (clears Ephemeral flag, promotes to persistent)
  4. Or burn: bd mol burn <id> (deletes without creating digest)

Examples:
  bd mol wisp beads-release --var version=1.0  # Release workflow
  bd mol wisp mol-patrol                       # Ephemeral patrol cycle
  bd mol wisp list                             # List all wisps
  bd mol wisp gc                               # Garbage collect old wisps

Subcommands:
  list  List all wisps in current context
  gc    Garbage collect orphaned wisps

Usage:
  bd mol wisp [proto-id] [flags]
  bd mol wisp [command]

Available Commands:
  create      Instantiate a proto as a wisp (solid -> vapor)
  gc          Garbage collect old/abandoned wisps
  list        List all wisps in current context

Flags:
      --dry-run           Preview what would be created
  -h, --help              help for wisp
      --root-only         Create only the root issue (no child step issues)
      --var stringArray   Variable substitution (key=value)

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

Use "bd mol wisp [command] --help" for more information about a command.

```

#### bd orphans --help

```
Identify orphaned issues - issues that are referenced in commit messages but remain open or in_progress in the database.

This helps identify work that has been implemented but not formally closed.

Examples:
  bd orphans              # Show orphaned issues
  bd orphans --json       # Machine-readable output
  bd orphans --details    # Show full commit information
  bd orphans --fix        # Close orphaned issues with confirmation

Usage:
  bd orphans [flags]

Flags:
      --details   Show full commit information
  -f, --fix       Close orphaned issues with confirmation
  -h, --help      help for orphans

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

#### bd ready --help

```
Show ready work (open issues with no active blockers).

Excludes in_progress, blocked, deferred, and hooked issues. This uses the
GetReadyWork API which applies blocker-aware semantics to find truly claimable work.

Note: 'bd list --ready' is NOT equivalent - it only filters by status=open.

Use --mol to filter to a specific molecule's steps:
  bd ready --mol bd-patrol   # Show ready steps within molecule

Use --gated to find molecules ready for gate-resume dispatch:
  bd ready --gated           # Find molecules where a gate closed

This is useful for agents executing molecules to see which steps can run next.

Usage:
  bd ready [flags]

Flags:
  -a, --assignee string              Filter by assignee
      --gated                        Find molecules ready for gate-resume dispatch
      --has-metadata-key string      Filter issues that have this metadata key set
  -h, --help                         help for ready
      --include-deferred             Include issues with future defer_until timestamps
      --include-ephemeral            Include ephemeral issues (wisps) in results
  -l, --label strings                Filter by labels (AND: must have ALL). Can combine with --label-any
      --label-any strings            Filter by labels (OR: must have AT LEAST ONE). Can combine with --label
  -n, --limit int                    Maximum issues to show (default 10)
      --metadata-field stringArray   Filter by metadata field (key=value, repeatable)
      --mol string                   Filter to steps within a specific molecule
      --mol-type string              Filter by molecule type: swarm, patrol, or work
      --parent string                Filter to descendants of this bead/epic
      --plain                        Display issues as a plain numbered list
      --pretty                       Display issues in a tree format with status/priority symbols (default true)
  -p, --priority int                 Filter by priority
      --rig string                   Query a different rig's database (e.g., --rig gastown, --rig gt-, --rig gt)
  -s, --sort string                  Sort policy: priority (default), hybrid, oldest (default "priority")
  -t, --type string                  Filter by issue type (task, bug, feature, epic, decision, merge-request). Aliases: mr→merge-request, feat→feature, mol→molecule, dec/adr→decision
  -u, --unassigned                   Show only unassigned issues

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

#### bd rename --help

```
Rename an issue from one ID to another.

This updates:
- The issue's primary ID
- All references in other issues (descriptions, titles, notes, etc.)
- Dependencies pointing to/from this issue
- Labels, comments, and events

Examples:
  bd rename bd-w382l bd-dolt     # Rename to memorable ID
  bd rename gt-abc123 gt-auth    # Use descriptive ID

Note: The new ID must use a valid prefix for this database.

Usage:
  bd rename <old-id> <new-id> [flags]

Flags:
  -h, --help   help for rename

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

#### bd ship --help

```
Ship a capability to satisfy cross-project dependencies.

This command:
  1. Finds issue with export:<capability> label
  2. Validates issue is closed (or --force to override)
  3. Adds provides:<capability> label

External projects can depend on this capability using:
  bd dep add <issue> external:<project>:<capability>

The capability is resolved when the external project has a closed issue
with the provides:<capability> label.

Examples:
  bd ship mol-run-assignee              # Ship the mol-run-assignee capability
  bd ship mol-run-assignee --force      # Ship even if issue is not closed
  bd ship mol-run-assignee --dry-run    # Preview without making changes

Usage:
  bd ship <capability> [flags]

Flags:
      --dry-run   Preview without making changes
      --force     Ship even if issue is not closed
  -h, --help      help for ship

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

#### bd slot --help

```
Manage slots on agent beads.

Agent beads have named slots that reference other beads:
  hook  - Current work attached to agent's hook (0..1 cardinality)
  role  - Role definition bead (required for agents)

Slots enforce cardinality constraints - the hook slot can only hold one bead.

Examples:
  bd slot show gt-mayor           # Show all slots for mayor agent
  bd slot set gt-emma hook bd-xyz # Attach work bd-xyz to emma's hook
  bd slot clear gt-emma hook      # Clear emma's hook (detach work)

Usage:
  bd slot [command]

Available Commands:
  clear       Clear a slot on an agent bead
  set         Set a slot on an agent bead
  show        Show all slots on an agent bead

Flags:
  -h, --help   help for slot

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

Use "bd slot [command] --help" for more information about a command.

```

##### bd slot clear --help

```
Clear a slot on an agent bead.

This detaches whatever bead is currently in the slot.

Examples:
  bd slot clear gt-emma hook   # Detach work from emma's hook
  bd slot clear gt-mayor role  # Clear mayor's role (not recommended)

Usage:
  bd slot clear <agent> <slot> [flags]

Flags:
  -h, --help   help for clear

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd slot set --help

```
Set a slot on an agent bead.

The slot command enforces cardinality: if the hook slot is already occupied,
the command will error. Use 'bd slot clear' first to detach existing work.

Examples:
  bd slot set gt-emma hook bd-xyz   # Attach bd-xyz to emma's hook
  bd slot set gt-mayor role gt-role # Set mayor's role bead

Usage:
  bd slot set <agent> <slot> <bead> [flags]

Flags:
  -h, --help   help for set

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

##### bd slot show --help

```
Show all slots on an agent bead.

Displays the current values of all slot fields.

Examples:
  bd slot show gt-emma   # Show emma's slots
  bd slot show gt-mayor  # Show mayor's slots

Usage:
  bd slot show <agent> [flags]

Flags:
  -h, --help   help for show

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

#### bd undefer --help

```
Undefer issues to restore them to open status.

This brings issues back from the icebox so they can be worked on again.
Issues will appear in 'bd ready' if they have no blockers.

Examples:
  bd undefer bd-abc        # Undefer a single issue
  bd undefer bd-abc bd-def # Undefer multiple issues

Usage:
  bd undefer [id...] [flags]

Flags:
  -h, --help   help for undefer

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

#### bd version --help

```
Print version information

Usage:
  bd version [flags]

Flags:
  -h, --help   help for version

Global Flags:
      --actor string              Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --db string                 Database path (default: auto-discover .beads/*.db)
      --dolt-auto-commit string   Dolt auto-commit policy (off|on|batch). 'on': commit after each write. 'batch': defer commits to bd dolt commit; uncommitted changes persist in the working set until then. SIGTERM/SIGHUP flush pending batch commits. Default: off. Override via config key dolt.auto-commit
      --json                      Output in JSON format
      --profile                   Generate CPU profile for performance analysis
  -q, --quiet                     Suppress non-essential output (errors only)
      --readonly                  Read-only mode: block write operations (for worker sandboxes)
      --sandbox                   Sandbox mode: disables auto-sync
  -v, --verbose                   Enable verbose/debug output

```

---

## OpenSpec Commands (openspec)

### openspec --help

```
Usage: openspec [options] [command]

AI-native system for spec-driven development

Options:
  -V, --version                      output the version number
  --no-color                         Disable color output
  -h, --help                         display help for command

Commands:
  init [options] [path]              Initialize OpenSpec in your project
  update [options] [path]            Update OpenSpec instruction files
  list [options]                     List items (changes by default). Use
                                     --specs to list specs.
  view                               Display an interactive dashboard of specs
                                     and changes
  change                             Manage OpenSpec change proposals
  archive [options] [change-name]    Archive a completed change and update main
                                     specs
  spec                               Manage and view OpenSpec specifications
  config [options]                   View and modify global OpenSpec
                                     configuration
  schema                             Manage workflow schemas [experimental]
  validate [options] [item-name]     Validate changes and specs
  show [options] [item-name]         Show a change or spec
  feedback [options] <message>       Submit feedback about OpenSpec
  completion                         Manage shell completions for OpenSpec CLI
  status [options]                   Display artifact completion status for a
                                     change
  instructions [options] [artifact]  Output enriched instructions for creating
                                     an artifact or applying tasks
  templates [options]                Show resolved template paths for all
                                     artifacts in a schema
  schemas [options]                  List available workflow schemas with
                                     descriptions
  new                                Create new items
  help [command]                     display help for command

```

#### openspec init --help

```
Usage: openspec init [options] [path]

Initialize OpenSpec in your project

Options:
  --tools <tools>      Configure AI tools non-interactively. Use "all", "none",
                       or a comma-separated list of: amazon-q, antigravity,
                       auggie, claude, cline, codex, codebuddy, continue,
                       costrict, crush, cursor, factory, gemini, github-copilot,
                       iflow, kilocode, kiro, opencode, pi, qoder, qwen,
                       roocode, trae, windsurf
  --force              Auto-cleanup legacy files without prompting
  --profile <profile>  Override global config profile (core or custom)
  -h, --help           display help for command

```

#### openspec list --help

```
Usage: openspec list [options]

List items (changes by default). Use --specs to list specs.

Options:
  --specs         List specs instead of changes
  --changes       List changes explicitly (default)
  --sort <order>  Sort order: "recent" (default) or "name" (default: "recent")
  --json          Output as JSON (for programmatic use)
  -h, --help      display help for command

```

#### openspec update --help

```
Usage: openspec update [options] [path]

Update OpenSpec instruction files

Options:
  --force     Force update even when tools are up to date
  -h, --help  display help for command

```

---


# JIRA Ticket: TBD - Add Configurable AI Providers to FilmBuff CLI and GUI

### Summary
Refactor FilmBuff AI-powered workflows so commands such as `filmbuff generate-shot-list` use a selectable AI provider instead of relying on a single Augment Code AI integration through the VS Code chatbot. Add CLI and GUI support for configuring providers, initially supporting Anthropic, OpenAI, and Google AI, while also allowing users to add their own custom providers, store multiple named profiles per provider, switch the active provider, and route supported FilmBuff commands through the currently selected AI backend.

### Description

#### Background
FilmBuff currently depends on a tightly coupled AI integration model that makes it difficult for users to choose different providers, manage separate credentials, or switch between environments such as personal, client, and testing setups. This creates friction for both technical and non-technical users and makes future provider expansion more expensive than necessary.

This work should introduce a provider abstraction layer that separates FilmBuff features from any single backend. Users should be able to configure multiple AI providers, with initial configuration support for Anthropic, OpenAI, and Google AI, while also being able to add custom or community-supported providers, maintain multiple named profiles for each provider, select an active provider/profile combination, and run AI-powered FilmBuff commands against that active configuration without changing the user-facing workflow.

FilmBuff should also provide a clear configuration experience through both CLI and GUI entry points. `filmbuff configure` should guide users through provider setup, while `filmbuff gui` should allow users to manage linked modules, search modules, and administer AI provider settings in a unified interface.

#### Key Requirements
- **Provider Abstraction**: Refactor AI-dependent functionality so commands use a shared provider interface rather than directly calling a single hard-coded AI backend.
- **Selectable Provider Execution**: Ensure commands such as `filmbuff generate-shot-list` resolve and use the currently active provider/profile automatically.
- **Multiple Provider Support**:
  - Initially support configuration for Anthropic, OpenAI, and Google AI.
  - Allow the architecture to expand cleanly to additional providers in future releases.
- **User-Added Provider Support**:
  - Allow users to register and configure their own AI providers in addition to the built-in providers.
  - Support extension points or a plugin-style registration mechanism for custom/community providers.
  - Ensure the design can accommodate open-source or self-hosted providers and adapters such as `https://github.com/whitead/paLM-api`, `https://github.com/ollama/ollama`, `https://github.com/mudler/LocalAI`, `https://github.com/vllm-project/vllm`, and `https://github.com/oobabooga/text-generation-webui`.
- **Multiple Named Profiles**:
  - Allow users to save multiple named configurations for the same provider.
  - Support use cases such as personal, work, client, and testing profiles.
- **CLI Provider Management**:
  - Add CLI commands to create, edit, list, validate, delete, and switch AI provider configurations.
  - Make provider/profile selection explicit, persistent, and easy to inspect.
- **CLI Help and Version Support**:
  - Ensure new and refactored CLI commands support `-h` and `--help` for usage guidance.
  - Ensure new and refactored CLI commands support `-v` and `--version` where appropriate so users can inspect the active CLI version consistently.
  - Keep help output clear, discoverable, and aligned with existing FilmBuff CLI conventions.
- **Persistent Configuration Storage**:
  - Store provider settings in a durable user-facing configuration system.
  - Persist the active provider/profile selection across runs.
  - Handle API keys and related secrets securely.
- **GUI Configuration Workflow**:
  - Implement `filmbuff configure` to open a GUI flow for selecting a provider and entering required settings.
  - Allow users to create, edit, validate, save, and activate provider profiles from the GUI.
- **Unified GUI Management Experience**:
  - Implement or extend `filmbuff gui` so users can manage AI provider settings alongside linked-module management and module search.
  - Ensure the GUI reflects the current active provider/profile consistently.
- **Validation and Error Handling**:
  - Validate provider settings before activation or runtime use.
  - Surface clear errors for missing credentials, invalid models, unsupported providers, or failed connectivity.
  - Provide actionable recovery guidance in both CLI and GUI experiences.
- **Security and Professionalism**:
  - Never expose secrets in normal output.
  - Keep command flows intuitive and appropriate for both developers and creative users.
  - Preserve a seamless workflow where users configure once and then use FilmBuff commands normally.
- **Testing and Documentation**:
  - Add tests for provider selection, profile persistence, command routing, validation behavior, and failure paths.
  - Document provider setup, switching workflows, GUI behavior, and security expectations.

This ticket should be suitable for follow-on conversion into an OpenSpec change and subsequent decomposition into Beads tasks.

### Acceptance Criteria
- `filmbuff generate-shot-list` and other supported AI-powered commands use the currently active configured provider/profile.
- Initial provider configuration support includes Anthropic, OpenAI, and Google AI.
- Users can register and use custom AI providers in addition to the built-in providers.
- Users can add, store, list, edit, validate, delete, and switch multiple provider configurations via the CLI.
- Users can maintain multiple named profiles for the same provider.
- New and refactored CLI commands support `-h` / `--help` and `-v` / `--version` consistently.
- `filmbuff configure` provides a GUI-based provider setup and activation flow.
- `filmbuff gui` includes AI provider management alongside existing module-related workflows.
- Provider/profile selection persists across restarts and stays consistent between CLI and GUI.
- Sensitive credentials are handled securely and are not exposed in standard output.
- Adding a new provider requires minimal changes because the implementation uses a reusable provider abstraction.
- The provider model supports community, open-source, or self-hosted integrations through documented extension points.
- Documentation and automated tests cover the core configuration, switching, validation, and command-routing behaviors.

### Estimated Effort
- Design and Planning: 10 hours
- Provider Abstraction and CLI Refactor: 18 hours
- GUI Configuration and Management Flows: 20 hours
- Testing and Documentation: 12 hours
- Total: 60 hours

### Attachments
- Source prompt: `ai-prompts/ai-providers-prompt.md`
- Format reference: `ai-prompts/powershell-prompt.md`
- Example implementation themes to guide OpenSpec and Beads breakdown:
  - Provider abstraction layer
    Goal: route all supported AI-powered commands through a shared provider interface
    Key rule: "Command handlers must resolve the active backend through the provider abstraction rather than direct integration-specific logic."
  - Provider configuration model
    Goal: support multiple providers and multiple named profiles per provider, with initial support for Anthropic, OpenAI, and Google AI
    Key rule: "Separate provider metadata, credentials, and active-profile state so runtime resolution is deterministic."
  - Custom provider extensibility
    Goal: allow users to add their own providers, including community or open-source adapters
    Key rule: "Built-in providers should use the same extension model exposed to user-defined providers wherever practical."
  - CLI management workflow
    Goal: create, inspect, update, validate, delete, and switch provider profiles from the command line
    Key rule: "Provider management commands must be explicit, discoverable, and consistent with FilmBuff CLI conventions."
  - CLI help and version behavior
    Goal: make command discovery easy for all users
    Key rule: "All new and refactored commands must expose `-h`/`--help` and `-v`/`--version` behavior consistently."
  - Secure credential handling
    Goal: protect API keys, tokens, and related settings
    Key rule: "Never print secrets in normal output; validate required credentials before activation or runtime use."
  - GUI provider setup
    Goal: guide users through provider selection, configuration, validation, and activation
    Key rule: "The configuration flow should be clear enough for non-technical users while still supporting advanced provider settings."
  - Unified GUI management
    Goal: manage providers and linked modules in one place
    Key rule: "The main GUI should reflect the active provider/profile and keep provider-management actions easy to find."
  - Open-source provider compatibility
    Goal: support user-added integrations for alternative backends and community projects such as `https://github.com/whitead/paLM-api`
    Key rule: "Provider registration and configuration should not assume a closed list of vendor-owned backends."
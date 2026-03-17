/**
 * ai_providers.ts — TypeScript Interop Module for the AI Provider Abstraction Layer
 * ==================================================================================
 *
 * Mirrors the Python `ai_providers.py` public API without duplicating business
 * logic.  Read operations resolve from `process.env` (same keys as the Python
 * layer reads from `.env`).  Write-back operations delegate to the Python CLI
 * via `spawnSync` so that `.env` mutations remain in one authoritative place.
 *
 * Public API::
 *
 *   import { resolveActiveProvider, getActiveProfile, maskApiKey } from './ai_providers';
 *
 * Change ID : AI-PROVIDER-001
 * Phase     : 4 — TypeScript Interop
 * Task      : 4.4
 * Version   : 0.1.0
 */

import { spawnSync } from "child_process";

// ---------------------------------------------------------------------------
// Types (mirrors ai_providers.py dataclasses)
// ---------------------------------------------------------------------------

/** Static metadata describing a single AI provider. */
export interface ProviderDescriptor {
  providerId: string;
  displayName: string;
  envKeyPrefix: string;
  defaultModel: string;
  baseUrl: string | null;
  requiresApiKey: boolean;
}

/** Runtime profile containing resolved credentials for a provider. */
export interface ProviderProfile {
  providerId: string;
  profileName: string;
  /** Raw API key — never log or display; always pass through {@link maskApiKey} first. */
  apiKey: string;
  model: string | null;
  baseUrl: string | null;
}

// ---------------------------------------------------------------------------
// Built-in provider table (read-only — mirrors ai_providers.py _BUILTIN_PROVIDERS)
// ---------------------------------------------------------------------------

const BUILTIN_PROVIDERS: ReadonlyMap<string, ProviderDescriptor> = new Map([
  ["anthropic", { providerId: "anthropic", displayName: "Anthropic (Claude)", envKeyPrefix: "ANTHROPIC", defaultModel: "claude-3-5-sonnet-20241022", baseUrl: null, requiresApiKey: true }],
  ["openai",    { providerId: "openai",    displayName: "OpenAI",             envKeyPrefix: "OPENAI",    defaultModel: "gpt-4o",                    baseUrl: null, requiresApiKey: true }],
  ["google_ai", { providerId: "google_ai", displayName: "Google AI (Gemini)", envKeyPrefix: "GOOGLE_AI", defaultModel: "gemini-1.5-pro",             baseUrl: null, requiresApiKey: true }],
  ["ollama",    { providerId: "ollama",    displayName: "Ollama (local)",      envKeyPrefix: "OLLAMA",    defaultModel: "llama3",                     baseUrl: "http://localhost:11434", requiresApiKey: false }],
  ["localai",   { providerId: "localai",   displayName: "LocalAI (local)",     envKeyPrefix: "LOCALAI",   defaultModel: "gpt-4",                      baseUrl: "http://localhost:8080",  requiresApiKey: false }],
]);

// ---------------------------------------------------------------------------
// Errors
// ---------------------------------------------------------------------------

export class ProviderNotConfiguredError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ProviderNotConfiguredError";
  }
}

export class ProfileNotFoundError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ProfileNotFoundError";
  }
}

// ---------------------------------------------------------------------------
// Read operations (resolved from process.env — no Python subprocess needed)
// ---------------------------------------------------------------------------

/**
 * Return the {@link ProviderDescriptor} for the active provider.
 *
 * Reads `AI_ACTIVE_PROVIDER` from `process.env`.
 *
 * @throws {ProviderNotConfiguredError} When `AI_ACTIVE_PROVIDER` is unset or unregistered.
 */
export function resolveActiveProvider(): ProviderDescriptor {
  const providerId = (process.env["AI_ACTIVE_PROVIDER"] ?? "").trim();
  if (!providerId) {
    throw new ProviderNotConfiguredError(
      "AI_ACTIVE_PROVIDER is not set. Run: python generate_documentation.py configure --activate-profile <provider>/<profile>"
    );
  }
  const descriptor = BUILTIN_PROVIDERS.get(providerId);
  if (!descriptor) {
    const registered = [...BUILTIN_PROVIDERS.keys()].join(", ") || "(none)";
    throw new ProviderNotConfiguredError(
      `Provider '${providerId}' is not registered. Known providers: ${registered}`
    );
  }
  return descriptor;
}

/**
 * Return the {@link ProviderProfile} for the active profile.
 *
 * Reads `AI_ACTIVE_PROFILE` and `<PREFIX>_API_KEY` from `process.env`.
 *
 * @throws {ProviderNotConfiguredError} When `AI_ACTIVE_PROVIDER` is unset or unregistered.
 * @throws {ProfileNotFoundError} When `AI_ACTIVE_PROFILE` is unset or the API key is missing.
 */
export function getActiveProfile(): ProviderProfile {
  const descriptor = resolveActiveProvider();

  const profileName = (process.env["AI_ACTIVE_PROFILE"] ?? "").trim();
  if (!profileName) {
    throw new ProfileNotFoundError(
      "AI_ACTIVE_PROFILE is not set. Run: python generate_documentation.py configure --activate-profile <provider>/<profile>"
    );
  }

  const apiKeyEnvVar = `${descriptor.envKeyPrefix}_API_KEY`;
  const apiKey = (process.env[apiKeyEnvVar] ?? "").trim();
  if (descriptor.requiresApiKey && !apiKey) {
    throw new ProfileNotFoundError(
      `API key for provider '${descriptor.providerId}' profile '${profileName}' is not set. Expected: ${apiKeyEnvVar}`
    );
  }

  const modelEnvVar = `${descriptor.envKeyPrefix}_MODEL`;
  const model = (process.env[modelEnvVar] ?? "").trim() || descriptor.defaultModel || null;

  const baseUrlEnvVar = `${descriptor.envKeyPrefix}_BASE_URL`;
  const baseUrl = (process.env[baseUrlEnvVar] ?? "").trim() || descriptor.baseUrl || null;

  return { providerId: descriptor.providerId, profileName, apiKey, model, baseUrl };
}

/**
 * Return a masked representation of `key` safe for terminal output.
 *
 * @example
 *   maskApiKey("sk-ant-abc123")  // → "sk-***...***"
 *   maskApiKey("")               // → "(not set)"
 */
export function maskApiKey(key: string): string {
  if (!key) return "(not set)";
  const prefix = key.length > 3 ? key.slice(0, 3) : key;
  return `${prefix}-***...***`;
}

// ---------------------------------------------------------------------------
// Write-back operations (delegate to Python CLI via spawnSync)
// ---------------------------------------------------------------------------

/** Options accepted by {@link activateProfile}. */
export interface ActivateProfileOptions {
  /** Provider identifier, e.g. `"anthropic"`. */
  providerId: string;
  /** Profile name, e.g. `"personal"`. */
  profileName: string;
}

/**
 * Activate a provider profile by delegating to the Python CLI.
 *
 * Runs:
 *   `python generate_documentation.py configure --activate-profile <provider>/<profile>`
 *
 * @throws {Error} When the Python subprocess exits with a non-zero code.
 */
export function activateProfile({ providerId, profileName }: ActivateProfileOptions): void {
  _runPythonCli([
    "generate_documentation.py", "configure",
    "--activate-profile", `${providerId}/${profileName}`,
  ]);
}

/**
 * Create a provider profile by delegating to the Python CLI (non-interactive).
 *
 * @throws {Error} When the Python subprocess exits with a non-zero code.
 */
export function createProfile({ providerId, profileName }: ActivateProfileOptions): void {
  _runPythonCli([
    "generate_documentation.py", "configure",
    "--create-profile", `${providerId}/${profileName}`,
  ]);
}

/**
 * Delete a provider profile by delegating to the Python CLI.
 *
 * @throws {Error} When the Python subprocess exits with a non-zero code.
 */
export function deleteProfile({ providerId, profileName }: ActivateProfileOptions): void {
  _runPythonCli([
    "generate_documentation.py", "configure",
    "--delete-profile", `${providerId}/${profileName}`,
  ]);
}

// ---------------------------------------------------------------------------
// Internal helper
// ---------------------------------------------------------------------------

/**
 * Run `python <args>` synchronously.
 *
 * @internal
 * @throws {Error} When the subprocess exits with a non-zero status.
 */
function _runPythonCli(args: string[]): void {
  const result = spawnSync("python", args, { encoding: "utf8", stdio: "inherit" });
  if (result.status !== 0) {
    throw new Error(
      `Python CLI exited with code ${result.status ?? "unknown"}. ` +
      `Command: python ${args.join(" ")}`
    );
  }
}


/**
 * tests/ai_providers.test.ts
 * ===========================
 *
 * Jest spec for ai_providers.ts — TypeScript provider resolution interop.
 *
 * Covers test cases:
 *   TC-RES-TS-01 … TC-RES-TS-04
 *
 * Run with:
 *   npx jest tests/ai_providers.test.ts
 *
 * Change ID : AI-PROVIDER-001
 * Phase     : 5 — Testing
 * Task      : 5.3
 */

import {
  resolveActiveProvider,
  getActiveProfile,
  maskApiKey,
  ProviderNotConfiguredError,
  ProfileNotFoundError,
} from "../ai_providers";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Snapshot and restore process.env around each test. */
let savedEnv: NodeJS.ProcessEnv;

beforeEach(() => {
  savedEnv = { ...process.env };
  // Clear provider keys that tests set so there is no cross-contamination.
  delete process.env["AI_ACTIVE_PROVIDER"];
  delete process.env["AI_ACTIVE_PROFILE"];
  delete process.env["ANTHROPIC_API_KEY"];
  delete process.env["ANTHROPIC_WORK_API_KEY"];
  delete process.env["OPENAI_API_KEY"];
  delete process.env["GOOGLE_AI_API_KEY"];
});

afterEach(() => {
  // Restore saved env values
  Object.keys(process.env).forEach((k) => delete process.env[k]);
  Object.assign(process.env, savedEnv);
});

// ---------------------------------------------------------------------------
// resolveActiveProvider()
// ---------------------------------------------------------------------------

describe("resolveActiveProvider()", () => {
  /**
   * TC-RES-TS-01: Returns descriptor-like object for set AI_ACTIVE_PROVIDER.
   */
  it("TC-RES-TS-01: returns descriptor for known AI_ACTIVE_PROVIDER", () => {
    process.env["AI_ACTIVE_PROVIDER"] = "openai";
    const descriptor = resolveActiveProvider();
    expect(descriptor.providerId).toBe("openai");
    expect(descriptor.envKeyPrefix).toBe("OPENAI");
  });

  /**
   * TC-RES-TS-02: Throws ProviderNotConfiguredError when AI_ACTIVE_PROVIDER unset.
   */
  it("TC-RES-TS-02: throws when AI_ACTIVE_PROVIDER is unset", () => {
    delete process.env["AI_ACTIVE_PROVIDER"];
    expect(() => resolveActiveProvider()).toThrow(ProviderNotConfiguredError);
    expect(() => resolveActiveProvider()).toThrow(/configure/i);
  });

  it("throws ProviderNotConfiguredError for an unknown provider id", () => {
    process.env["AI_ACTIVE_PROVIDER"] = "totally_unknown";
    expect(() => resolveActiveProvider()).toThrow(ProviderNotConfiguredError);
  });
});

// ---------------------------------------------------------------------------
// getActiveProfile()
// ---------------------------------------------------------------------------

describe("getActiveProfile()", () => {
  /**
   * TC-RES-TS-03: getActiveProfile() reads named profile key.
   */
  it("TC-RES-TS-03: reads named profile API key", () => {
    process.env["AI_ACTIVE_PROVIDER"] = "anthropic";
    process.env["AI_ACTIVE_PROFILE"] = "work";
    process.env["ANTHROPIC_WORK_API_KEY"] = "sk-ant-ts-test";

    const profile = getActiveProfile();
    expect(profile.providerId).toBe("anthropic");
    expect(profile.profileName).toBe("work");
    expect(profile.apiKey).toBe("sk-ant-ts-test");
  });

  it("throws ProfileNotFoundError when AI_ACTIVE_PROFILE is unset", () => {
    process.env["AI_ACTIVE_PROVIDER"] = "anthropic";
    delete process.env["AI_ACTIVE_PROFILE"];
    expect(() => getActiveProfile()).toThrow(ProfileNotFoundError);
  });

  it("throws ProfileNotFoundError when API key is missing for key-requiring provider", () => {
    process.env["AI_ACTIVE_PROVIDER"] = "anthropic";
    process.env["AI_ACTIVE_PROFILE"] = "work";
    delete process.env["ANTHROPIC_WORK_API_KEY"];
    delete process.env["ANTHROPIC_API_KEY"];
    expect(() => getActiveProfile()).toThrow(ProfileNotFoundError);
  });
});

// ---------------------------------------------------------------------------
// TC-RES-TS-04: TypeScript reads same AI_ACTIVE_PROVIDER key as Python
// ---------------------------------------------------------------------------

describe("Interop consistency (TC-RES-TS-04)", () => {
  /**
   * TC-RES-TS-04: TypeScript and Python read the same AI_ACTIVE_PROVIDER key.
   * We verify the TS side here; Python is tested in test_provider_resolution.py.
   */
  it("reads AI_ACTIVE_PROVIDER=google_ai identically to Python", () => {
    process.env["AI_ACTIVE_PROVIDER"] = "google_ai";
    const descriptor = resolveActiveProvider();
    // Must match Python ProviderDescriptor for google_ai
    expect(descriptor.providerId).toBe("google_ai");
    expect(descriptor.defaultModel).toBe("gemini-1.5-pro");
    expect(descriptor.requiresApiKey).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// maskApiKey() — basic coverage (full suite in tests/secret-masking spec)
// ---------------------------------------------------------------------------

describe("maskApiKey()", () => {
  it('returns "(not set)" for empty string', () => {
    expect(maskApiKey("")).toBe("(not set)");
  });

  it("masks a key with a dash-separated prefix", () => {
    const masked = maskApiKey("sk-ant-abc123");
    expect(masked).toMatch(/^\S+-\*\*\*\.\.\.\*\*\*$/);
  });
});


**[日本語](../ja/changelog.md)** | [Back to README](../../README.md)

# Changelog

Per-release changes for the UAIP plugin. Before reading the entries below, please skim the **Versioning Policy** section so you know what each version number means (breaking change vs additive vs fix).

---

## Versioning Policy

UAIP follows [Semantic Versioning 2.0.0](https://semver.org/).

### Reading version numbers

A version number is `MAJOR.MINOR.PATCH`.

| Segment | Meaning |
|---|---|
| **MAJOR** (e.g. `1.x.x` → `2.x.x`) | Breaking changes. May require updating command names, parameter shapes, or config files on upgrade |
| **MINOR** (e.g. `1.0.x` → `1.1.x`) | Backward-compatible additions — new commands, new capabilities, new optional parameters. Existing calls keep working |
| **PATCH** (e.g. `1.0.0` → `1.0.1`) | Bug fixes only. No impact on the public API |

### Current phase: 1.x.y (Fab Pro released)

The current version is **1.0.0**, the first entry of the `1.x.y` series. UAIP is **now released on Fab as the Pro product** ([listing](https://www.fab.com/listings/0eedf909-00ac-4d95-b109-8fda51800fff)).

- Standard SemVer rules now apply strictly: breaking changes require a MAJOR bump (e.g. `2.0.0`)
- New commands / new capabilities ship as MINOR (e.g. `1.0.x` → `1.1.0`)
- Bug fixes ship as PATCH (e.g. `1.0.0` → `1.0.1`)

### Pre-1.0 history: 0.x.y series

Versions `0.9.0` and `0.9.1` were demo-only releases distributed via GitHub Releases ahead of the Fab Pro submission. Their entries are preserved below for historical reference.

### Pre-release tags

Pre-release tags are not used in routine development. The only exception is an optional `1.0.0-rc.1`-style RC (release candidate) build distributed via GitHub Releases immediately before Fab submission. An RC build ships **identical code** to what will be submitted to Fab — if no issues are found, the same code is re-tagged as `1.0.0`.

### Deprecation policy (rarely removed)

UAIP maintains a single source tree across UE versions using version macros (not per-version branches). Because of this, **commands shipped to users are not removed once released**.

- Commands scheduled for retirement are marked `Stability: "Deprecated"` but **keep working**
- `uaip_describe_command` exposes the `DeprecationMessage` and `MigrationTarget` (recommended replacement)
- The only exception: when Epic removes an underlying engine API and UAIP can no longer maintain the implementation, the affected command may be removed during a MAJOR bump

This guarantees that older command names — which may be baked into an AI agent's training data or working memory — keep functioning long-term.

### Demo and Pro share the same version number

The free demo (GitHub Releases) and Pro (Fab) **always share the same version number**. Both are built from the same source with only feature gating differences, so HealthCheck's `UAIPVersion` field returns the same value either way.

---

## Releases

> **You are viewing the `next` branch.** This page tracks development-in-progress content ahead of the next Fab release. For the last released version, see the [`master` branch changelog](https://github.com/Naotsun19B/UnrealAIIntegrationPlatform-Document/blob/master/docs/en/changelog.md).

### Unreleased

Changes that have shipped in the plugin repository but are not yet released on Fab.

#### UAIP Plugin

**Added**

- **Sandbox editing integration** (`UAIPEditorSandbox` module, **Pro only** — requires `FileSandbox` plugin; not available in the demo build): AI agents can now stage asset changes inside a FileSandbox session and commit or revert them after human review. Adds 6 commands under `UAIP.Editor.Sandbox` — `BeginSandboxSession`, `EndSandboxSession`, `GetSandboxStatus`, `GetSandboxChanges`, `CommitSandboxChanges`, `RevertSandboxChanges` — and 4 capabilities: `SandboxObserve` (DefaultAllow), `SandboxSessionControl`, `SandboxPersist`, `SandboxRevert` (all DefaultDenied). All 6 commands — including the read-only observe commands — require the `FileSandbox` plugin and are not included in the demo module whitelist.

**Changed**

- **Niagara module now supports UE 5.7**: All commands under `UAIP.Editor.Niagara` and `UAIP.Runtime.Niagara` (36 UAIP + Toolset bridge commands) are now available on UE 5.7. Previously the entire module was unregistered on UE 5.7 and every command returned `CommandNotFound`.
- **Niagara `default_value` applied**: `AddSetParametersModule` and `AddSetParameterEntry` now parse and apply the `default_value` field for common types (float, int, bool, `UScriptStruct`). Previously entries were always created with type defaults regardless of the supplied value.
- **`script_name` now required for `AddSetParameterEntry` / `RemoveSetParameterEntry`** *(breaking)*: Both commands require a new `script_name` parameter (e.g. `Spawn`, `Update`, `Particle Spawn`, `Particle Update`). This parameter routes the call to the correct script stack and is necessary for the UE 5.8 External Edit API. Existing calls without `script_name` will return `InvalidParams`.

#### MCP Bridge 1.1.1 — released 2026-06-24

**Fixed**

- **Removed `uaip_max_major` upper bound** — `compatibility.json` now sets `uaip_max_major: null`, allowing the bridge to connect to any UAIP plugin version `>= 0.9.1`, including future major versions such as 2.x. Previously the upper bound of `1` required a new bridge release for every plugin major bump, even when no actual incompatibility existed.

---

#### MCP Bridge 1.1.0 — released 2026-06-23

**Added**

- **`uaip_reload_config` tool**: reads `config.json` in-place and, when launch parameters change (`editor_path`, `uproject_path`, `http_port`, or `enable_scenario`), shuts down the running editor and schedules a fresh launch on the next tool call — without disconnecting the MCP session. Optional `EditorPath` / `UProjectPath` arguments override `config.json` for the current session only (not persisted), enabling runtime engine version switching without restarting the MCP client.
- **Version compatibility check on connect**: The bridge validates the running UAIP plugin version against a `compatibility.json` manifest on startup and raises `VersionIncompatibleError` on a major-version mismatch. The check can be bypassed in dev environments with `UAIP_BRIDGE_SKIP_VERSION_CHECK=1`.

**Fixed**

- Bridge now correctly restarts the editor when `enable_scenario` (or other launch parameters) change via `uaip_reload_config`. Previously, `importlib.reload()` was called before checking the running editor state, causing the enum identity comparison to fail and the restart to be silently skipped.
- Bridge now automatically terminates lingering crash dialogs (`WerFault.exe`, `CrashReportClient.exe`) before launching or relaunching the editor. On Windows, a crash dialog holds the per-project named mutex while open, blocking any new editor process from starting until the dialog is dismissed manually.

---

### UAIP Plugin 1.0.0 — 2026-06-18

**UAIP is now available on Fab as the Pro product.** [https://www.fab.com/listings/0eedf909-00ac-4d95-b109-8fda51800fff](https://www.fab.com/listings/0eedf909-00ac-4d95-b109-8fda51800fff)

[![Watch the launch trailer on YouTube](https://markdown-videos-api.jorgenkh.no/youtube/o-33jgYLF0A)](https://youtu.be/o-33jgYLF0A)

This is the first production release of UAIP. The Pro build ships through Fab as a Code Plugin (source included) and provides the full UAIP capability set without the demo's feature gating or watermark. The free demo on GitHub Releases continues to be available for evaluation and non-commercial use.

#### What Pro provides beyond the demo

- **All transports** — HTTP, WebSocket, and CLI in addition to MCP
- **Editor-edit commands** across Blueprint / Level / Asset / Material / Niagara / Sequencer / AnimBlueprint / ControlRig / PCG / MetaSound / BehaviorTree / StateTree / Dataflow / EQS / CommonConversation / UMG / Physics / Skeleton / GameplayTags / GameFeatures / EnhancedInput
- **190+ Toolset bridges** to UE 5.8's official Toolset API, bringing the total to ~730 commands
- **Runtime world edits** — actor spawn, GAS mutations, input injection
- **Python script execution** through `RunEditorPythonScript`
- **No watermark** on captures

#### Compatibility

- UE 5.7 / 5.8 on Windows (Win64)
- The Pro plugin is distributed exclusively on Fab; demo continues on this repository's [Demo Releases](https://github.com/Naotsun19B/UnrealAIIntegrationPlatform-Document/releases?q=Demo)
- MCP Bridge stays at the independent `MCPBridge-v1.0.0` release ([Bridge Releases](https://github.com/Naotsun19B/UnrealAIIntegrationPlatform-Document/releases?q=MCPBridge))

---

### UAIP Plugin 0.9.1 — 2026-06-18

A follow-up demo release that restructures how the MCP Bridge is delivered, in order to comply with Fab packaging rules ahead of the upcoming Pro submission. Other engine-side improvements landed in this version are scoped to the Pro build and have no user-visible effect on the demo.

#### Changed

- **MCP Bridge has been split out of the plugin** to comply with Fab packaging rules — the plugin distribution can no longer bundle a Python toolchain. The bridge is now released as a **separate, independently versioned Release** (`MCPBridge-v<X.Y.Z>` tags) in this repository's [Releases](https://github.com/Naotsun19B/UnrealAIIntegrationPlatform-Document/releases?q=MCPBridge) (UE-version-agnostic, MIT-licensed, shared between Demo and Pro). The installer deploys it to `<UAIP-parent>/UAIPMCPBridge/` (sibling to the UAIP plugin). See [Connection Methods → MCP Bridge](connections.md#mcp-bridge).

---

### UAIP Plugin 0.9.0 — 2026-06-18

**The demo build is now available on GitHub Releases.** The Pro build subsequently shipped on Fab — see the [UAIP Plugin 1.0.0](#uaip-plugin-100--2026-06-18) entry above.

#### Overview

First public release of UAIP, distributed as a demo build. Per the SemVer adoption policy, the version starts at `0.9.0` — the leading entry of the `0.x.y` series that marks the period before the Fab Pro release.

#### Added — what the demo build contains

- **MCP connectivity** — drive the editor from any MCP-capable AI client (Claude Code, Codex CLI, Cursor, Windsurf, GitHub Copilot, …)
- **Observation commands** — JSON dumps of editor state, world state, and Slate widget trees; screenshots of editor tabs and viewports
- **PIE control** — start / stop PIE, load maps
- **Assertion commands** — verify actor properties and world state
- **Scenario execution** — submit an ordered list of steps as a single request, with per-step abort / retry / timeout settings
- **UI automation** — click, key input, and form fill against Slate widgets
- **Extension points** — register your own commands via `ICommandProvider` / `ICommandHandler`

#### Not in the demo (planned for Pro)

- HTTP / WebSocket / CLI transports (demo is MCP-only)
- Editor-edit commands (Blueprint / Level / Asset / Material / Niagara / …)
- Runtime world edits (Spawn / GAS / Input injection)
- Python script execution
- Capture without watermark (the demo composites a "UAIP Demo" watermark into every screenshot)

See the [Demo Version Guide](demo.md) for the full breakdown.

#### Known limitations

- Supported platform: Windows (Win64) only
- Supported UE versions: 5.7 / 5.8
- macOS / Linux support is a future consideration (not in v1.0)

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

- **Editor Toolset bridge commands** (`UAIPEditorAssets`, `UAIPEditorLevel`, `UAIPEditorObservation`, `UAIPEditorWorkspace`, `UAIPEditorEngineManagement`, `UAIPRuntimePIE`, `UAIPRuntimeWorld` modules): AI agents can now call Toolset bridge commands (`Toolset.*`) that delegate to the UE 5.8 official Toolset framework (`EditorAppToolset` + `LogsToolset`). All bridge commands require UE 5.8+ with the relevant Toolset plugin enabled; they are listed as `Available: false` on older versions. Native UAIP commands remain the primary path and continue to work on UE 5.7. Also adds 6 new native commands: `GetVisibleActors`, `ProjectWorldToScreen`, `ProjectScreenToWorld` (under `UAIP.Editor.Level`), `CaptureViewportImageAnnotated` (requires `ViewportAnnotationCapture`; under `UAIP.Editor.Observation`), and `GetLogVerbosity` / `SetLogVerbosity` (requires `LogVerbosityEdit`; under `UAIP.Editor.Engine.Log`). Adds 1 new capability `ViewportAnnotationCapture` (DefaultDenied). Also adds `CVarInspect` capability (DefaultDenied) gating the `Toolset.Editor.Toolset.World.SearchCVars` bridge command.
- **World Partition editing** (`UAIPEditorWorldPartition` module, **Pro only** — not available in the demo build): AI agents can now manage World Partition streaming, Data Layers, and HLOD workflows. Adds 34 commands under `UAIP.Editor.WorldPartition` — 12 World Partition commands (`GetWorldPartitionInfo`, `GetWorldPartitionStreamingGrids`, `GetRuntimeGridSettings`, `SetRuntimeGridSettings`, `GetActorWorldPartitionSettings`, `SetActorIsSpatiallyLoaded`, `SetActorRuntimeGrid`, `SetWorldPartitionStreamingEnabled`, `PinActorInWorldPartition`, `UnpinActorFromWorldPartition`, `DumpWorldPartitionCells`, `ListExternalActors`), 15 Data Layer commands (`ListDataLayers`, `GetDataLayerInfo`, `CreateDataLayerAsset`, `DeleteDataLayerAsset`, `CreateDataLayerInstance`, `DeleteDataLayerInstance`, `SetDataLayerType`, `SetDataLayerInitialRuntimeState`, `SetDataLayerIsLoadedInEditor`, `SetDataLayerVisibility`, `SetParentDataLayerInstance`, `GetActorDataLayers`, `AddActorToDataLayer`, `RemoveActorFromDataLayer`, `GetActorsInDataLayer`), and 7 HLOD commands (`ListHLODLayers`, `CreateHLODLayer`, `DeleteHLODs`, `SetActorHLODLayer`, `BuildHLODs`, `CancelHLODBuild`, `GetHLODBuildStatus`). Adds 3 capabilities: `WorldPartitionEdit`, `DataLayerEdit`, `HLODBuild` (all DefaultDenied). Observation commands (`GetWorldPartitionInfo`, `GetWorldPartitionStreamingGrids`, `DumpWorldPartitionCells`, `ListDataLayers`, `GetDataLayerInfo`, `ListExternalActors`, `GetActorWorldPartitionSettings`, `GetActorDataLayers`, `GetActorsInDataLayer`, `ListHLODLayers`, `GetHLODBuildStatus`) return `Success: true` with `IsWorldPartitionEnabled: false` when the current level does not use World Partition.
- **PCG extended commands and capabilities** (`UAIPEditorPCG` module): Adds 20 commands under `UAIP.Editor.PCG` — asset creation (`CreatePCGGraph`, requires `PCGGraphAssetCreate`), schema / description / parameter read-write (`GetPCGGraphSchema`, `GetPCGGraphDescription`, `SetPCGGraphDescription`, `SetPCGGraphParams`, `RemovePCGGraphParams`), instance management (`ListPCGGraphInstances`, `SpawnPCGGraphInstance`, `GetPCGGraphInstanceParams`, `SetPCGGraphInstanceParams`, `ResetPCGGraphInstanceParams`), subgraph / native-node inspection (`ListPCGAvailableSubgraphs`, `GetPCGNativeNodeSchema`, `AddPCGSubgraphNode`), graph structure editing (`RepositionPCGNode`, `AddPCGCommentBox`, `UpdatePCGCommentBox`, `RemovePCGCommentBox`), and data view / execution (`GetPCGNodeDataView`, `RunPCGInstantGraph`). Adds 5 DefaultDenied capabilities: `PCGGraphAssetCreate`, `PCGGraphExecute`, `PCGVolumeSpawn`, `PCGNodeInspect`, and `PCGToolsetUnsafeNodeAdd`. Do **not** add `PCGVolumeSpawn` or `PCGToolsetUnsafeNodeAdd` to `AllowedCapabilities` in `DefaultUAIP.ini`. `GetPCGNodeDataView` is only functional in builds with `PCG_PROFILING_ENABLED=1`. Also adds 31 Toolset bridge commands under `Toolset.Editor.PCG.*` (requires UE 5.8+ with the `PCGToolset` plugin enabled; listed as `Available: false` on older versions or when the plugin is disabled).
- **Plugin management** (`UAIPRuntimeEngineManagement` and `UAIPEditorEngineManagement` modules): AI agents can now inspect and manage UE plugins without leaving the editor. Adds 5 read-only commands under `UAIP.Runtime.Engine.Plugin` — `ListPlugins`, `GetPluginInfo`, `IsEnabled`, `GetPluginDependencies`, `GetPluginForAsset` — available in both editor and packaged builds. Adds 9 commands under `UAIP.Editor.Engine.Plugin` — 5 inspection commands (`GetPluginDescriptor`, `GetPluginDependents`, `GetPluginTemplateDescriptions`, `IsPluginCreationAllowed`, `IsPluginModificationAllowed`) plus 4 mutation commands (`SetPluginEnabled`, `UpdatePluginDescriptor`, `AddPluginDependency`, `RemovePluginDependency`). On UE 5.8+ with the `PluginToolset` plugin enabled, 15 additional bridge commands are available under `Toolset.Plugin.*` — `ListEnabledPlugins`, `ListDiscoveredPlugins`, `GetPluginInfo`, `IsEnabled`, `GetPluginDependencies`, `GetPluginForAsset`, `GetPluginDescriptor`, `GetPluginDependents`, `GetPluginTemplateDescriptions`, `IsPluginCreationAllowed`, `IsPluginModificationAllowed`, `SetPluginEnabled`, `UpdatePluginDescriptor`, `AddPluginDependency`, `RemovePluginDependency`. Adds 3 DefaultDenied capabilities: `PluginEnableToggle` (gates `SetPluginEnabled`), `PluginDescriptorEdit` (gates `UpdatePluginDescriptor`), `PluginDependencyEdit` (gates `AddPluginDependency` / `RemovePluginDependency`). Inspection commands require only `EditorInspect`. `UAIP.Core.ListPlugins` is deprecated; use `UAIP.Runtime.Engine.Plugin.ListPlugins` instead.
- **Foliage management** (`UAIPEditorFoliage` module): AI agents can now manage foliage types and instances in the editor. Adds 11 commands under `UAIP.Editor.Foliage` — 4 observation commands (`ListFoliageTypes`, `GetFoliageTypeInfo`, `GetFoliageInstanceCount`, `GetFoliageInstances`; require `EditorInspect`; available during PIE), 3 foliage type management commands (`AddFoliageTypeToLevel`, `RemoveFoliageTypeFromLevel`, `SetFoliageTypeSettings`; require `FoliageTypeEdit`), and 4 instance control commands (`AddFoliageInstances`, `RemoveFoliageInstances`, `DeleteAllFoliageInstances`, `ResimulateProceduralFoliage`; require `FoliageInstanceEdit` or `FoliageBulkDelete`). Instance placement is World Partition aware and routes each instance to the correct `AInstancedFoliageActor` cell. Adds 3 new DefaultDenied capabilities: `FoliageTypeEdit`, `FoliageInstanceEdit`, `FoliageBulkDelete`.
- **MVVM editing** (`UAIPEditorMVVM` module, **Pro only** — requires `ModelViewViewModel` plugin; not available in the demo build): AI agents can now drive the full MVVM setup of a WidgetBlueprint — wiring ViewModels, creating and updating View Bindings and View Events, and managing ViewModel properties. Adds 28 commands under `UAIP.Editor.MVVM` and 2 capabilities: `ViewModelBindingEdit` and `ViewModelSourceEdit` (both DefaultDenied). On UE 5.8+ with the `MVVMToolset` plugin enabled, 9 additional bridge commands are available under `Toolset.MVVM.*`.
- **Sound asset editing** (`UAIPEditorSound` module): AI agents can now read and set properties on `USoundClass`, `USoundAttenuation`, and `USoundMix` assets. Adds 13 commands under `UAIP.Editor.SoundSettings` and 3 capabilities: `SoundClassEdit`, `SoundAttenuationEdit`, `SoundMixEdit` (all DefaultDenied).
- **Sandbox editing integration** (`UAIPEditorSandbox` module, **Pro only** — requires `FileSandbox` plugin; not available in the demo build): AI agents can now stage asset changes inside a FileSandbox session and commit or revert them after human review. Adds 6 commands under `UAIP.Editor.Sandbox` — `BeginSandboxSession`, `EndSandboxSession`, `GetSandboxStatus`, `GetSandboxChanges`, `CommitSandboxChanges`, `RevertSandboxChanges` — and 4 capabilities: `SandboxObserve` (DefaultAllow), `SandboxSessionControl`, `SandboxPersist`, `SandboxRevert` (all DefaultDenied). All 6 commands — including the read-only observe commands — require the `FileSandbox` plugin and are not included in the demo module whitelist.
- **Semantic asset search** (`UAIPEditorAssets` module, requires `SemanticSearch` plugin UE 5.8+ and an OpenAI API key): AI agents can now search and compare project assets using natural language queries. Adds 5 commands under `UAIP.Editor.SemanticSearch` — `SearchAssetsSemantic`, `FindSimilarAssets`, `GetIndexStats`, `StartIndexing`, `CancelIndexing` — and 1 capability: `SemanticSearchEdit` (DefaultDenied; gates index rebuild operations). On UE 5.8+ with the `SemanticSearchToolset` plugin enabled, 2 additional bridge commands are available under `Toolset.Editor.SemanticSearch.*` (`Search`, `FindSimilar`). Note: `SearchAssetsSemantic` and `FindSimilarAssets` require an active semantic index; run `StartIndexing` once before using search commands.
- **ConfigSettings commands** (`UAIPEditorEngineManagement` module): AI agents can now inspect and modify Project Settings and Editor Preferences through `ISettingsModule`. Adds 8 commands under `UAIP.Editor.Engine.ConfigSettings` — `ListSettingsContainers`, `ListSettingsCategories`, `ListSettingsSections` (read-only, no capability required), `GetSettingsSchema` (returns a JSON artifact with property names, types, descriptions, defaults, and edit conditions; requires `EditorInspect`), `GetSettingsValues` (returns a JSON artifact with current values; secret fields masked with `***`; requires `EditorInspect`), `SetSettingsValues` (merges a `Properties` map into the settings object via `ImportText`; supports `DryRun`; requires `ConfigSettingsEdit`; blocked during PIE), `SaveSettings` (persists the section to its ini file; blocked during PIE and when `bDisableSave` is set; requires `ConfigSettingsSave`), and `ResetSettingsToDefaults` (reverts to class defaults; blocked during PIE; requires `ConfigSettingsReset`). Write operations are restricted to files under the project `Config/` directory (engine ini files are rejected with `PolicyViolation`). Also adds 2 commands under `UAIP.Runtime.Engine.Config` — `GetConfigValue` (read a raw ini key; no capability required) and `SetConfigValue` (write or delete a raw ini key; blocked in packaged builds; rejects ini injection characters `[` and `]`; requires `ConfigSettingsEdit`). Adds 3 DefaultDenied capabilities: `ConfigSettingsEdit`, `ConfigSettingsSave`, `ConfigSettingsReset`.
- **CVar management** (`UAIPRuntimeEngineManagement` and `UAIPEditorEngineManagement` modules): AI agents can now read, search, set, and reset console variables. Adds 4 commands under `UAIP.Runtime.Engine.CVar` — `GetConsoleVariable` (requires `RuntimeCVarRead`), `SearchConsoleVariables` (requires `RuntimeCVarRead`), `SetConsoleVariable` (requires `RuntimeCVarWrite`), `ResetConsoleVariable` (requires `RuntimeCVarWrite`) — plus 1 Toolset bridge `Toolset.Editor.Toolset.EngineManagement.SearchCVars` (requires `CVarInspect`; UE 5.8+ with EditorToolset plugin). Adds 1 new DefaultDenied capability `RuntimeCVarWrite` (gates `SetConsoleVariable` and `ResetConsoleVariable`). CVars matching sensitive name patterns (`*password*`, `*token*`, `*secret*`, etc.) return `NotFound` to hide their existence. `ECVF_ReadOnly` CVars return `NotAllowed` on set/reset.
- **Log entry retrieval** (`UAIPEditorEngineManagement` and `UAIPRuntimeEngineManagement` modules): Adds `GetLogEntries` under `UAIP.Editor.Engine.Log` (retrieves recent editor output log entries with optional pattern-based filtering; no capability required) and `GetLogCategories` under `UAIP.Runtime.Engine.Log` (lists all registered log category names; no capability required).
- **`CreateAsset` self-description commands** (`UAIPEditorAssets` module): AI agents can now discover valid `CreateAsset` inputs before calling it, instead of trial-and-error via error messages. Adds 2 read-only commands under `UAIP.Editor.Assets` — `ListCreatableAssetClasses` (returns every UClass with at least one creatable factory, plus factory count and default factory class name; heavy call, requires `EditorInspect`) and `ListFactoriesForClass` (returns the factory candidates for a given `ClassName`, each with its `FactoryParams` JSON Schema; requires `EditorInspect`). Also adds `ICreateAssetInterceptor::GetFactoryParamsSchema()` so `DataTable` and `StateTree` asset creation now self-describe their required `FactoryParams` keys (`RowStructPath`, `SchemaClass`).

**Changed**

- **`UAIP.Runtime.World.GetConsoleVariable` and `UAIP.Runtime.World.SearchConsoleVariables` deprecated**: Use `UAIP.Runtime.Engine.CVar.GetConsoleVariable` and `UAIP.Runtime.Engine.CVar.SearchConsoleVariables` instead. Both commands remain functional and return `Success: true` with a `DeprecationWarning` in the response `Data`.
- **`UAIP.Core.ListPlugins` deprecated**: Use `UAIP.Runtime.Engine.Plugin.ListPlugins` instead. The original command remains functional but will be removed in a future release.
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

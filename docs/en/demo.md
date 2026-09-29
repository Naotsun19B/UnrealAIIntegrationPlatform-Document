**[日本語](../ja/demo.md)** | [Back to README](../../README.md)

# Demo Version Guide

The UAIP demo binary is a free, feature-limited build distributed via GitHub Releases. It provides observation, PIE control, assertion, scenario execution, and UI automation, plus read-only inspection of assets, level actors, properties, plugins, settings, logs, console variables and Unreal Insights traces — enough to integrate an AI agent into your review and testing workflow without any cost.

> **License**: the demo is licensed for **personal use and evaluation only**. Commercial use is not covered — see the `EULA.txt` shipped with the release archive. For commercial use, please get the Pro version ([available on Fab](https://www.fab.com/listings/0eedf909-00ac-4d95-b109-8fda51800fff)).

---

## Demo vs Pro

| | Demo | Pro (Fab) |
|---|:---:|:---:|
| **Connection** | | |
| MCP | ✅ | ✅ |
| HTTP API (`/uaip/commands`, …) | — | ✅ |
| WebSocket | — | ✅ |
| CLI | — | ✅ |
| Artifact retrieval (`/uaip/artifacts/*`) | ✅ | ✅ |
| **Commands** | | |
| Core (HealthCheck, ListCommands, …) | ✅ | ✅ |
| Editor observation (screenshots, dumps) | ✅ | ✅ |
| Editor workspace (tab focus, graph framing, editor restart, …) | ✅ | ✅ |
| PIE control (StartPIE, StopPIE, LoadMap, …) | ✅ | ✅ |
| Runtime observation (viewport capture, world dump) | ✅ | ✅ |
| Scenario execution (`uaip_run_scenario`) | ✅ | ✅ |
| UI automation (ClickWidget, PressKey, FillForm, …) | ✅ | ✅ |
| Runtime assertion (WaitSeconds, AssertActorProperty, …) | ✅ | ✅ |
| Read-only editor inspection (assets, level actors and components, properties, plugins, settings, logs, CVars) | ✅ | ✅ |
| Unreal Insights trace inspection (channels, status, captured files) | ✅ | ✅ |
| Unreal Insights trace recording and analysis | — | ✅ |
| Editor editing (Blueprint, Level, Assets, Material, …) | — | ✅ |
| Runtime world editing (SpawnActor, GAS, Input inject, …) | — | ✅ |
| Python script execution (`RunEditorPythonScript`) | — | ✅ |
| **Other** | | |
| Watermark on captured images | ✅ | — |
| User extension points (`ICommandProvider`) | ✅ | ✅ |
| Optional plugin integrations (Toolset, GAS, Niagara, …) | — | ✅ |
| UE version | 5.7 / 5.8 | 5.7 / 5.8 |

---

## Installation

1. Download `UAIP-Demo-UE<version>-Win64.zip` from the [Releases](../../../releases) page
2. Extract the zip into your UE project's `Plugins/` folder — it unpacks as `Plugins/UnrealAIIntegrationPlatform/`, the same folder the Pro plugin uses. If an earlier demo is still under `Plugins/UnrealAIIntegrationPlatformDemo/`, delete that folder first: two copies of the plugin cannot be enabled side by side
3. Copy `Config/DefaultUAIP.ini` from the extracted folder to your project's `Config/` folder — it turns on `AllowLogDump`, `AllowContextMenuMutation`, `AllowKeyboardInput` and `AllowKeyboardModifierInput`, and grants the `RuntimeCVarRead` capability for the console-variable reads. Observation, UI automation and PIE control are allowed by default and need no entry. The few commands marked with a capability in the tables below need one more `+AllowedCapabilities=<Name>` line in `[UAIP.SafetyPolicy]`
4. Register the MCP server in your AI client (see [Connection Methods → MCP Bridge](connections.md#mcp-bridge))

### Upgrading to Pro

`Config/DefaultUAIP.ini` uses the same format in both the demo and Pro. The ini you copied from the demo zip carries over as-is — no replacement is needed. The plugin folder structure and MCP server registration are identical, so no other changes are required.

---

## Available commands

Every command below is registered in the demo build. Where a namespace is marked **read-only subset**, its commands that change the editor exist only in Pro (see [Excluded commands](#excluded-commands)). A capability named in the Note column is deny-by-default: grant it with `+AllowedCapabilities=<Name>` before calling the command.

### `UAIP.Core.*`

| Command | Description | Note |
|---|---|---|
| `UAIP.Core.HealthCheck` | Verify the connection and return the UAIP version | |
| `UAIP.Core.GetSystemInfo` | Return project name, platform, engine version, and build config | |
| `UAIP.Core.ListCommands` | List registered commands (supports `ProviderPrefix` and keyword filter); reports how many commands it left out and why (`HiddenCount` / `HiddenReasons`) | |
| `UAIP.Core.DescribeCommand` | Return full details of one command (description, parameter schema, requirements) | |
| `UAIP.Core.QueryCapabilities` | Return the current session's capability set; `IncludeUnavailable: true` also lists every registered capability | |
| `UAIP.Core.ListIntegrations` | Report the state of every optional-plugin integration (see [Excluded commands](#excluded-commands)) | |
| `UAIP.Core.ListPlugins` | Return UE plugin information (name, version, enabled state) | Deprecated — use `UAIP.Runtime.Engine.Plugin.ListPlugins` |
| `UAIP.Core.EndSession` | End the session, release widget refs, and GC artifacts | |
| `UAIP.Core.ReloadCapabilities` | Reload capabilities from `DefaultUAIP.ini` | Requires `AllowCapabilityReload=True` |
| `UAIP.Core.GetPendingInteractionStatus` | Report the state of a pending interaction | No demo command starts one, so these three always answer `NotFound` |
| `UAIP.Core.WaitForPendingInteraction` | Wait until a pending interaction finishes | Same as above |
| `UAIP.Core.CancelPendingInteraction` | Cancel a pending interaction the session started | Same as above |

### `UAIP.Core.Artifacts.*`

| Command | Description |
|---|---|
| `UAIP.Core.Artifacts.GetArtifact` | Return the stored content of an artifact the calling session produced |

### `UAIP.Editor.Observation.*`

| Command | Description | Note |
|---|---|---|
| `UAIP.Editor.Observation.CaptureActiveWindowImage` | Screenshot of the active editor window | Watermarked |
| `UAIP.Editor.Observation.CaptureEditorTabImage` | Screenshot of a specific editor tab | Watermarked |
| `UAIP.Editor.Observation.CaptureGraphViewportImage` | Screenshot of a graph editor (Blueprint, Material, …) | Watermarked |
| `UAIP.Editor.Observation.CaptureViewportImageAnnotated` | Viewport screenshot with world-coordinate labels drawn on it | Watermarked; `ViewportAnnotationCapture` |
| `UAIP.Editor.Observation.DumpEditorState` | JSON dump of open assets, active tab, window dimensions | |
| `UAIP.Editor.Observation.DumpSelectionState` | JSON dump of the current selection | |
| `UAIP.Editor.Observation.DumpOpenTabs` | JSON list of open tabs | |
| `UAIP.Editor.Observation.DumpOutputLog` | Retrieve the Output Log | |
| `UAIP.Editor.Observation.DumpMessageLog` | Retrieve the Message Log | |
| `UAIP.Editor.Observation.DumpSlateTree` | JSON dump of the Slate widget hierarchy | |
| `UAIP.Editor.Observation.InspectMenu` | Return menu structure information | |
| `UAIP.Editor.Observation.InspectContextMenu` | Return context menu information | |
| `UAIP.Editor.Observation.ObserveWidget` | Register a widget for monitoring (cache) | |
| `UAIP.Editor.Observation.ListGraphNodes` | Return a list of nodes in a graph | |
| `UAIP.Editor.Observation.GetLogCategories` | List registered engine log category names | |

### `UAIP.Editor.Workspace.*`

| Command | Description | Note |
|---|---|---|
| `UAIP.Editor.Workspace.FocusEditorTab` | Bring the editor tab of an asset to the front (by `AssetPath`) | |
| `UAIP.Editor.Workspace.CloseEditorTab` | Close the editor tab of an asset (by `AssetPath`) | |
| `UAIP.Editor.Workspace.ListSpawnableTabs` | List the editor tabs that can be opened, with their Slate layout IDs | `EditorTabSpawn` |
| `UAIP.Editor.Workspace.OpenTabById` | Open an editor tab by its Slate layout ID | `EditorTabSpawn` |
| `UAIP.Editor.Workspace.CloseTabById` | Close an editor tab by its Slate layout ID | `EditorTabSpawn` |
| `UAIP.Editor.Workspace.NormalizeEditorLayout` | Focus the main graph tab and hide transient panels | |
| `UAIP.Editor.Workspace.SetGraphZoom` | Set the graph viewport zoom level | |
| `UAIP.Editor.Workspace.FrameGraphAll` | Fit all nodes in the graph viewport | |
| `UAIP.Editor.Workspace.FrameGraphSelection` | Fit the selected nodes in the graph viewport | |
| `UAIP.Editor.Workspace.SetGraphSelection` | Select graph nodes by ID | |
| `UAIP.Editor.Workspace.GetUndoHistory` | Read the undo/redo history without changing it | |
| `UAIP.Editor.Workspace.Undo` | Undo the last editor operation | `EditorUndoRedo` |
| `UAIP.Editor.Workspace.Redo` | Redo the last undone operation | `EditorUndoRedo` |
| `UAIP.Editor.Workspace.SaveAllPackages` | Save all modified packages | |
| `UAIP.Editor.Workspace.ShutdownEditor` | Shut down the editor | |
| `UAIP.Editor.Workspace.RestartEditor` | Restart the editor | |
| `UAIP.Editor.Workspace.GetLastCrashReport` | Get the most recent crash report | |

### `UAIP.Runtime.PIE.*`

| Command | Description |
|---|---|
| `UAIP.Runtime.PIE.StartPIE` | Start Play in Editor (PIE) |
| `UAIP.Runtime.PIE.StopPIE` | Stop PIE |
| `UAIP.Runtime.PIE.PausePIE` | Pause PIE |
| `UAIP.Runtime.PIE.ResumePIE` | Resume PIE |
| `UAIP.Runtime.PIE.LoadMap` | Load a map |
| `UAIP.Runtime.PIE.GetPIEState` | Return the current PIE state (`Running` / `Stopped` / `Paused` / `Simulating`) |

### `UAIP.Runtime.Observation.*`

| Command | Description | Note |
|---|---|---|
| `UAIP.Runtime.Observation.CaptureViewportImage` | Screenshot of the game viewport | Watermarked |
| `UAIP.Runtime.Observation.DumpWorldState` | JSON dump of all actors, components, and transforms | |
| `UAIP.Runtime.Observation.DumpActorState` | JSON dump of a specific actor | |
| `UAIP.Runtime.Observation.DumpComponentState` | JSON dump of a specific component | |
| `UAIP.Runtime.Observation.DumpRuntimeLog` | Retrieve the runtime log | |
| `UAIP.Runtime.Observation.CapturePerformanceSnapshot` | Capture FPS, memory, and other performance stats | |
| `UAIP.Runtime.Observation.CheckpointCapture` | Screenshot + state dump combined (scenario primitive) | Watermarked |
| `UAIP.Runtime.Observation.SearchLoadedClasses` | Search loaded classes | |

### `UAIP.Runtime.Assertion.*`

| Command | Description |
|---|---|
| `UAIP.Runtime.Assertion.WaitSeconds` | Wait for a specified number of seconds (scenario primitive) |
| `UAIP.Runtime.Assertion.WaitForCondition` | Wait in a condition-evaluation loop (scenario primitive) |
| `UAIP.Runtime.Assertion.AssertActorProperty` | Assert an actor property value (outputs artifact on failure) |
| `UAIP.Runtime.Assertion.AssertWorldState` | Batch-assert multiple properties |

### `UAIP.Editor.UIAutomation.*`

| Command | Description | Note |
|---|---|---|
| `UAIP.Editor.UIAutomation.SnapshotUI` | Take a UI structure snapshot | |
| `UAIP.Editor.UIAutomation.ClickWidget` | Click a widget | |
| `UAIP.Editor.UIAutomation.SelectMenuItem` | Select a menu item | |
| `UAIP.Editor.UIAutomation.InputText` | Input text | |
| `UAIP.Editor.UIAutomation.SetCheckboxState` | Set a checkbox state | |
| `UAIP.Editor.UIAutomation.SetComboSelection` | Select a combo box item | |
| `UAIP.Editor.UIAutomation.DragGraphNode` | Drag a graph node | |
| `UAIP.Editor.UIAutomation.ConnectGraphPins` | Connect graph pins | |
| `UAIP.Editor.UIAutomation.AcceptDialog` | Close a dialog with OK | |
| `UAIP.Editor.UIAutomation.CancelDialog` | Close a dialog with Cancel | |
| `UAIP.Editor.UIAutomation.InvokeContextMenuAction` | Invoke a context menu action | |
| `UAIP.Editor.UIAutomation.HoverWidget` | Hover over a widget | |
| `UAIP.Editor.UIAutomation.PressKey` | Send a key input | `EditorKeyboardInput` |
| `UAIP.Editor.UIAutomation.WaitForWidget` | Wait for a widget to appear | |
| `UAIP.Editor.UIAutomation.FillForm` | Auto-fill a form | |
| `UAIP.Editor.UIAutomation.OpenPasswordTestWindow` | Open a test window with a password field (target for password-field policy tests) | |

### `UAIP.Editor.Assets.*` (read-only subset)

| Command | Description | Note |
|---|---|---|
| `UAIP.Editor.Assets.SearchAssets` | Search assets by path / class / tag | |
| `UAIP.Editor.Assets.GetOpenAssets` | List the assets open in an asset editor | |
| `UAIP.Editor.Assets.GetSelectedAssets` | List the assets selected in the Content Browser | |
| `UAIP.Editor.Assets.GetContentBrowserPath` | Return the folder shown in the Content Browser | |
| `UAIP.Editor.Assets.ListDirtyPackages` | List the packages holding unsaved changes | |
| `UAIP.Editor.Assets.ListAssetRedirectors` | List asset redirectors under a folder | |
| `UAIP.Editor.Assets.ListCreatableAssetClasses` | List the asset classes `CreateAsset` can target | |
| `UAIP.Editor.Assets.ListFactoriesForClass` | List the factory candidates for an asset class | |
| `UAIP.Editor.Assets.GetAssetReferences` | Traverse the reference graph (referencers / dependencies) of an asset | |
| `UAIP.Editor.Assets.GetAssetDependencyPath` | Find the shortest dependency path between two assets | |
| `UAIP.Editor.Assets.GetAssetSizeMap` | Aggregate per-asset size under a folder | |
| `UAIP.Editor.Assets.GetAssetSizeMapByClass` | Aggregate size per asset class under a folder | |
| `UAIP.Editor.Assets.StartAssetAudit` | Start an asset audit as a background job (the editor stays responsive) | |
| `UAIP.Editor.Assets.GetAssetAuditStatus` | Poll an audit job's progress | |
| `UAIP.Editor.Assets.GetAssetAuditResult` | Retrieve the reports of a finished audit job | |
| `UAIP.Editor.Assets.FindUnreferencedAssets` | Find assets with no referencers under a folder | Deprecated — use `StartAssetAudit` |
| `UAIP.Editor.Assets.FindCircularReferences` | Find circular dependency chains under a folder | Deprecated — use `StartAssetAudit` |
| `UAIP.Editor.Assets.FindBrokenReferences` | Find dependencies pointing at missing packages | Deprecated — use `StartAssetAudit` |
| `UAIP.Editor.Assets.RunAssetAudit` | Run a composite audit in one call | Deprecated — use `StartAssetAudit` |
| `UAIP.Editor.Assets.ListPrimaryAssetTypes` | List the registered Primary Asset Types | |
| `UAIP.Editor.Assets.GetPrimaryAssetTypeInfo` | Get the details of one Primary Asset Type | |
| `UAIP.Editor.Assets.ListPrimaryAssets` | List the Primary Assets of a type | |
| `UAIP.Editor.Assets.GetPrimaryAssetIdForPath` | Resolve an asset path to its `PrimaryAssetId` | |
| `UAIP.Editor.Assets.GetPrimaryAssetRules` | Get the effective rules of a Primary Asset | |
| `UAIP.Editor.Assets.GetAssetBundle` | Get the Asset Bundle entries of a Primary Asset | |
| `UAIP.Editor.Assets.GetManagedPackageList` | Get the packages managed by a Primary Asset | |
| `UAIP.Editor.Assets.GetPrimaryAssetLoadList` | Resolve what would load for a Primary Asset | |
| `UAIP.Editor.Assets.GetLoadedPrimaryAssets` | List the currently loaded Primary Assets | |
| `UAIP.Editor.Assets.GetAssetTags` | Get the Asset Registry tags of an asset | |

### `UAIP.Editor.Level.*` (read-only subset)

| Command | Description |
|---|---|
| `UAIP.Editor.Level.ListLevelActors` | List all actors in the open level |
| `UAIP.Editor.Level.ListSelectedActors` | List the actors selected in the editor |
| `UAIP.Editor.Level.GetActorTransform` | Get the transform of an actor |
| `UAIP.Editor.Level.GetVisibleActors` | List the actors visible in the active viewport |
| `UAIP.Editor.Level.GetCameraTransform` | Get the level editor viewport camera location and rotation |
| `UAIP.Editor.Level.ProjectWorldToScreen` | Project a world position to screen coordinates |
| `UAIP.Editor.Level.ProjectScreenToWorld` | Cast a ray from screen coordinates into the world |
| `UAIP.Editor.Level.ListActorComponents` | List every component of an actor placed in the level |
| `UAIP.Editor.Level.GetActorComponentProperty` | Read a property of a placed actor's component |

### `UAIP.Editor.Property.*` (read-only subset)

| Command | Description |
|---|---|
| `UAIP.Editor.Property.GetActorProperty` | Get a property value from an actor |
| `UAIP.Editor.Property.GetAssetProperty` | Get a property value from an asset |
| `UAIP.Editor.Property.GetBlueprintDefault` | Get a property from a Blueprint's class defaults |
| `UAIP.Editor.Property.GetWorldSetting` | Get a World Settings property |
| `UAIP.Editor.Property.GetProjectSetting` | Get a property from a project settings object |
| `UAIP.Editor.Property.GetDataTableRow` | Get a DataTable row property |

Values of secret-looking properties are masked in the responses.

### `UAIP.Editor.Engine.*` (read-only subset)

| Command | Description |
|---|---|
| `UAIP.Editor.Engine.Plugin.GetPluginDescriptor` | Read a plugin's `.uplugin` descriptor |
| `UAIP.Editor.Engine.Plugin.GetPluginDependents` | List the plugins that depend on a plugin |
| `UAIP.Editor.Engine.Plugin.GetPluginTemplateDescriptions` | List the available plugin templates |
| `UAIP.Editor.Engine.Plugin.IsPluginCreationAllowed` | Check whether new plugins can be created |
| `UAIP.Editor.Engine.Plugin.IsPluginModificationAllowed` | Check whether a plugin can be modified |
| `UAIP.Editor.Engine.ConfigSettings.ListSettingsContainers` | List the settings containers (`Project`, `Editor`, …) |
| `UAIP.Editor.Engine.ConfigSettings.ListSettingsCategories` | List the categories of a settings container |
| `UAIP.Editor.Engine.ConfigSettings.ListSettingsSections` | List the sections of a settings category |
| `UAIP.Editor.Engine.ConfigSettings.GetSettingsSchema` | Return the editable properties of a settings section |
| `UAIP.Editor.Engine.ConfigSettings.GetSettingsValues` | Return the current values of a settings section (secrets masked) |
| `UAIP.Editor.Engine.Log.GetLogEntries` | Retrieve recent editor log entries (pattern filter) |

### `UAIP.Runtime.Engine.*` (read-only subset)

| Command | Description | Note |
|---|---|---|
| `UAIP.Runtime.Engine.Plugin.ListPlugins` | List discovered or enabled plugins | |
| `UAIP.Runtime.Engine.Plugin.GetPluginInfo` | Get the details of a plugin | |
| `UAIP.Runtime.Engine.Plugin.IsEnabled` | Check whether a plugin is enabled | |
| `UAIP.Runtime.Engine.Plugin.GetPluginDependencies` | List a plugin's direct dependencies | |
| `UAIP.Runtime.Engine.Plugin.GetPluginForAsset` | Resolve the plugin that owns an asset path | |
| `UAIP.Runtime.Engine.Log.GetLogCategories` | List registered log category names | |
| `UAIP.Runtime.Engine.Log.GetLogVerbosity` | Get the verbosity of a log category | |
| `UAIP.Runtime.Engine.Config.GetConfigValue` | Read an ini value by section and key | |
| `UAIP.Runtime.Engine.CVar.GetConsoleVariable` | Read a console variable's value, type and help text | `RuntimeCVarRead` (granted by the demo ini) |
| `UAIP.Runtime.Engine.CVar.SearchConsoleVariables` | Search console variables by wildcard | `RuntimeCVarRead` (granted by the demo ini) |

### `UAIP.Runtime.Insights.Trace.*` (read-only subset)

| Command | Description |
|---|---|
| `UAIP.Runtime.Insights.Trace.ListTraceChannels` | List the trace channels, whether each is enabled, and what it can disclose |
| `UAIP.Runtime.Insights.Trace.GetTraceStatus` | Report whether a trace is recording and, for a UAIP-started trace, its details |
| `UAIP.Runtime.Insights.Trace.ListTraceFiles` | List the trace files UAIP captured |

---

## Limitations

### Connection

The demo runs in **MCP-only mode**. The HTTP API routes (`/uaip/commands`, etc.) are not registered even if `-uaip-http-enable` is passed — the flag is ignored with a warning in the log. Only `/mcp`, `/uaip/artifacts/*` and `/uaip/instance-proof` are active.

### Watermark on captured images

The following capture commands embed a **"UAIP Demo"** watermark in the output PNG:

- `CaptureActiveWindowImage`
- `CaptureEditorTabImage`
- `CaptureGraphViewportImage`
- `CaptureViewportImageAnnotated`
- `CaptureViewportImage` (and therefore the screenshot `CheckpointCapture` takes)

<p align="center">
  <img src="../../images/demo-watermark-full.png" alt="Demo capture with watermark in the bottom-right corner" width="80%">
</p>

<p align="center">
  <img src="../../images/demo-watermark-zoom.png" alt="Watermark close-up" width="40%">
</p>

The mark makes it clear that a screenshot — when it ends up shared as review or test evidence — was produced by the demo build. The Pro version emits captures without the watermark.

### Excluded commands

Commands that exist in Pro but are not available in the demo:

| Commands | Reason / what the demo answers |
|---|---|
| Commands of modules not included in the demo (Blueprint, Material, Sequencer, runtime world editing, Python execution such as `UAIP.Editor.Execution.RunEditorPythonScript`, …) | Pro only — `CommandNotFound` |
| Commands of optional-plugin integrations (Niagara, StateTree, PCG, GAS, MetaHuman, LiveLink, …) | Pro only — `CommandNotFound`, with a hint that the integration is not included in the free demo edition and is available in Pro on Fab. `UAIP.Core.ListIntegrations` reports these integrations as `NotInThisEdition` |
| Toolset bridge commands (`Toolset.*`) and `UAIP.Editor.Engine.Toolset.DumpToolsetParameterSchemas` | They need the Toolset integration, which the demo does not include. Those belonging to the included modules are registered but always unavailable: hidden from `ListCommands` (listed as `Available: false` with `IncludeUnavailable: true`) and refused when called |
| Commands that change the editor in the included Assets, Level, Property, Engine and Insights namespaces (`CreateAsset`, `SaveAsset`, `PlaceActorInLevel`, `AddActorComponent`, `Set*Property`, `SetPluginEnabled`, `SetSettingsValues`, `SetConsoleVariable`, `StartTrace`, …) | The demo exposes only the read-only subset listed above — `CommandNotFound` |
| `WaitForShaderCompilation`, `RecompileGlobalShaders` and the Live Coding commands in `UAIP.Editor.Workspace` | Shader and Live Coding development — Pro only — `CommandNotFound` |
| Trace analysis (`UAIP.Runtime.Insights.Analysis.*`) | Compiled out of the demo — `CommandNotFound` |

### Where the demo loads

The demo is an editor-only build. It does not load into packaged builds or commandlet runs. If you need UAIP on the runtime side (Gauntlet tests, post-shipping observation, etc.), use the Pro version.

---

## Scenario execution

Scenario execution (`uaip_run_scenario`) is available in the demo. Enable it in `config.json`:

```json
{
  "editor_path":    "...",
  "uproject_path":  "...",
  "enable_scenario": true
}
```

See [Scenario Execution](scenario.md) for full details.

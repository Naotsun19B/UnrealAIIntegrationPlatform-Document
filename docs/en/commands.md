**[日本語](../ja/commands.md)** | [Back to README](../../README.md)

# Commands Reference

UAIP exposes 948 **UAIP commands** (provided directly by the plugin itself) and 420 **Toolset bridge commands** (delegating to the UE 5.8 official Toolset framework), for a combined total of 1368 commands organized by domain. Each command name is fully-qualified — e.g. `UAIP.Editor.Observation.CaptureActiveWindowImage`. This page omits the provider prefix in the tables; the section header tells you what to prepend.

## How to use this reference

- Use `uaip_describe_command(CommandName="...")` to get the full parameter schema for a command
- Use `uaip_list_commands(ProviderPrefix="UAIP.Editor")` to filter by domain at runtime
- For the required Capability per command, see [Safety & Capabilities](safety.md)

## Symbols

| Symbol | Meaning |
|---|---|
| 🆓 | Available in the demo binary (also in Pro) |
| (no mark) | Pro-only command |
| 🧩 | Requires an optional UE plugin (the command is not registered if the plugin is disabled) |

## UAIP commands vs Toolset bridge commands

UAIP exposes two categories of commands:

- **UAIP commands** (`UAIP.*` prefix) — first-party commands provided by the plugin itself. They work regardless of UE version or Toolset plugin availability.
- **Toolset bridge commands** (`Toolset.*` prefix; UE 5.8+ with the relevant Toolset plugin installed) — a delegation layer over the official UE 5.8 Toolset framework. Most mirror an existing UAIP command, while a few surface functionality only available through Toolset.

The domain summary below lists counts only. To enumerate the actual Toolset bridge command names at runtime, use `uaip_list_commands(ProviderPrefix="Toolset")`.

---

## Domain summary

| Domain | Provider prefix | UAIP commands | Toolset bridge | Demo |
|---|---|---:|---:|---:|
| Core | `UAIP.Core` | 8 | — | ✅ |
| Editor Workspace | `UAIP.Editor.Workspace` | 18 | 1 | partial (13/18) |
| Editor Engine Log | `UAIP.Editor.Engine.Log` | 1 | 4 | ✅ |
| Editor Engine Plugin | `UAIP.Editor.Engine.Plugin` | 9 | 15 | partial (5/9) |
| Editor Engine CVar 🧩 | `Toolset.Editor.EngineManagement` | — | 1 | — |
| Editor Engine ConfigSettings | `UAIP.Editor.Engine.ConfigSettings` | 8 | 8 | partial (5/8) |
| Editor Observation | `UAIP.Editor.Observation` | 15 | — | ✅ |
| Editor Execution | `UAIP.Editor.Execution` | 9 | — | — |
| Editor UI Automation | `UAIP.Editor.UIAutomation` | 16 | 10 | ✅ |
| Editor Assets | `UAIP.Editor.Assets` | 46 | 6 | partial (25/46) |
| Editor SemanticSearch 🧩 | `UAIP.Editor.SemanticSearch` | 5 | 2 | — |
| Editor Level | `UAIP.Editor.Level` | 16 | 8 | partial (7/16) |
| Editor Property | `UAIP.Editor.Property` | 12 | — | partial (6/12) |
| Editor Blueprint | `UAIP.Editor.Blueprint` | 20 | — | — |
| Editor UMG | `UAIP.Editor.UMG` | 22 | 13 | — |
| Editor Material | `UAIP.Editor.Material` | 11 | — | — |
| Editor GameplayTags | `UAIP.Editor.GameplayTags` | 7 | 6 | — |
| Editor GameFeatures 🧩 | `UAIP.Editor.GameFeatures` | 5 | 4 | — |
| Editor Niagara 🧩 | `UAIP.Editor.Niagara` | 52 | 45 | — |
| Editor Physics | `UAIP.Editor.Physics` | 31 | 17 | — |
| Editor Dataflow 🧩 | `UAIP.Editor.Dataflow` | 9 | 7 | — |
| Editor ChaosClothAsset 🧩 | `UAIP.Editor.ChaosClothAsset` | 10 | 6 | — |
| Editor Skeleton | `UAIP.Editor.Skeleton` | 8 | — | — |
| Editor MetaHuman 🧩 | `UAIP.Editor.MetaHuman` | 56 | 9 | — |
| Editor DataTable | `UAIP.Editor.DataTable` | 8 | — | — |
| Editor AnimBlueprint | `UAIP.Editor.AnimBlueprint` | 11 | — | — |
| Editor SoundCue | `UAIP.Editor.SoundCue` | 7 | — | — |
| Editor SoundSettings | `UAIP.Editor.SoundSettings` | 13 | — | — |
| Editor MVVM 🧩 | `UAIP.Editor.MVVM` | 26 | 9 | — |
| Editor BehaviorTree | `UAIP.Editor.BehaviorTree` | 17 | 7 | — |
| Editor MetaSound 🧩 | `UAIP.Editor.MetaSound` | 10 | — | — |
| Editor EQS 🧩 | `UAIP.Editor.EQS` | 9 | — | — |
| Editor Sequencer | `UAIP.Editor.Sequencer` | 123 | 61 | — |
| Editor StateTree | `UAIP.Editor.StateTree` | 39 | 8 | — |
| Editor Curve | `UAIP.Editor.Curve` | 6 | — | — |
| Editor PCG 🧩 | `UAIP.Editor.PCG` | 33 | 30 | — |
| Editor WorldConditions 🧩 | `UAIP.Editor.WorldConditions` | 13 | 2 | — |
| Editor Conversation 🧩 | `UAIP.Editor.Conversation` | 7 | 5 | — |
| Editor ControlRig | `UAIP.Editor.ControlRig` | 59 | 107 | — |
| Editor EnhancedInput | `UAIP.Editor.EnhancedInput` | 13 | — | — |
| Editor GAS 🧩 | `UAIP.Editor.GAS` | 8 | 14 | — |
| Editor Python Extension 🧩 | `UAIP.Editor.Python` | 2 | — | — |
| Editor Sandbox 🧩 | `UAIP.Editor.Sandbox` | 6 | — | — |
| Editor WorldPartition | `UAIP.Editor.WorldPartition` | 34 | — | — |
| Editor Foliage | `UAIP.Editor.Foliage` | 11 | — | — |
| Editor DataRegistry 🧩 | `UAIP.Editor.DataRegistry` | 9 | 7 | — |
| Runtime Engine Log | `UAIP.Runtime.Engine.Log` | 3 | — | partial (2/3) |
| Runtime Engine Plugin | `UAIP.Runtime.Engine.Plugin` | 5 | — | ✅ |
| Runtime Engine CVar | `UAIP.Runtime.Engine.CVar` | 4 | — | partial (2/4) |
| Runtime Engine Config | `UAIP.Runtime.Engine.Config` | 2 | — | partial (1/2) |
| Runtime PIE | `UAIP.Runtime.PIE` | 6 | 3 | ✅ |
| Runtime World | `UAIP.Runtime.World` | 9 | 1 | — |
| Runtime Observation | `UAIP.Runtime.Observation` | 8 | — | ✅ |
| Runtime Execution | `UAIP.Runtime.Execution` | 3 | — | — |
| Runtime Assertion | `UAIP.Runtime.Assertion` | 4 | — | ✅ |
| Runtime Input | `UAIP.Runtime.Input` | 11 | — | — |
| Runtime GAS 🧩 | `UAIP.Runtime.GAS` | 17 | — | — |
| Runtime Niagara 🧩 | `UAIP.Runtime.Niagara` | 4 | 4 | — |
| Runtime Insights Trace | `UAIP.Runtime.Insights.Trace` | 11 | — | partial (3/11) |
| Runtime Insights Analysis | `UAIP.Runtime.Insights.Analysis` | 3 | — | — |

---

## UAIP.Core

System-level commands for discovery, health, and session management.

| Command | Description |
|---|---|
| 🆓 `HealthCheck` | Plugin connectivity check — returns `Status`, `UAIPVersion`, `EngineVersion`, `BuildConfig`, `ProjectFilePath` (absolute path of the open `.uproject`, used by the MCP Bridge to verify it is attaching to the right editor instance), `TransportTimeouts` (per-transport async command timeout in seconds, e.g. `{"HTTP": 120, "WS": 12}`), `QueueCongestion` (how busy the deferred-execution queue is, as one of `None` / `Low` / `High` — the exact number waiting is not returned, since it would let one session infer another session's activity) |
| 🆓 `GetSystemInfo` | Returns UE version (Major/Minor/Patch/Changelist), project name, platform, build config, UAIP version |
| 🆓 `QueryCapabilities` | Returns the session's capability set and `OperationalConstraints` (7 policy flags) |
| 🆓 `ListCommands` | Filtered command catalog (filters: `GroupFilter`, `KeywordFilter`, `IncludeUnavailable`) |
| 🆓 `DescribeCommand` | Full metadata for a single command (schema, required capabilities, availability) |
| 🆓 `ListPlugins` | ⚠️ **Deprecated** — use `UAIP.Runtime.Engine.Plugin.ListPlugins` instead. List installed plugins and their enabled state (JSON) |
| 🆓 `EndSession` | End a session explicitly and release its server-side resources; its artifacts become GC candidates |
| 🆓 `ReloadCapabilities` | Reload the capability set from `Config/DefaultUAIP.ini` without restarting the editor (only registered when `AllowCapabilityReload=True`) |

---

## UAIP.Editor.Workspace

Editor lifecycle, tab management, graph layout, shader compilation, Live Coding.

| Command | Description |
|---|---|
| 🆓 `FocusEditorTab` | Bring the editor tab for an asset to the front. The target is addressed by `AssetPath`, **not** by a Slate layout tab identifier — the `ActiveTabId` reported by `DumpEditorState` (`"Viewport"`, `"Inspector"`, …) is rejected here. Use the `TabId` parameter of `CaptureEditorTabImage` when you need to address a tab by its layout identifier |
| 🆓 `CloseEditorTab` | Close the editor tab for an asset. Takes `AssetPath`, addressed the same way as `FocusEditorTab` |
| 🆓 `NormalizeEditorLayout` | Focus the main graph tab and hide transient panels |
| 🆓 `SetGraphZoom` | Set graph viewport zoom level |
| 🆓 `FrameGraphAll` | Zoom the graph viewport to fit all nodes |
| 🆓 `FrameGraphSelection` | Zoom the graph viewport to fit selected nodes |
| 🆓 `SetGraphSelection` | Select graph nodes by ID list |
| 🆓 `ShutdownEditor` | Shut down the UE Editor (optionally save packages) |
| 🆓 `RestartEditor` | Restart the UE Editor (optionally save packages) |
| 🆓 `SaveAllPackages` | Save all modified packages (optionally include maps) |
| 🆓 `Undo` | Undo the last editor operation |
| 🆓 `Redo` | Redo the last undone operation |
| 🆓 `GetLastCrashReport` | Get the most recent crash report |
| `WaitForShaderCompilation` | Wait until shader compilation completes |
| `RecompileGlobalShaders` | Force-recompile all global shaders and wait for completion |
| `CompileLiveCoding` | Trigger Live Coding recompilation |
| `GetLiveCodingStatus` | Get the current Live Coding status |
| `EnableLiveCodingForSession` | Enable Live Coding for the current session |

### Toolset bridges — LiveCoding (1) 🧩

Bridge command via the `LiveCodingToolset` (UE 5.8+). Provider: `Toolset.Editor.LiveCoding.*`.

| Command | Description |
|---|---|
| `Toolset.Editor.LiveCoding.CompileLiveCoding` | Trigger Live Coding recompilation (requires `LiveCodingControl`) |

---

## UAIP.Editor.Engine.Log

Log entry retrieval for the editor output log. Log **verbosity** commands live under [`UAIP.Runtime.Engine.Log`](#uaipruntimeenginelog).

| Command | Description |
|---|---|
| 🆓 `GetLogEntries` | Retrieve recent log entries from the editor output log (supports pattern filtering; no capability required) |

### Toolset bridges — Logs (4) 🧩

Bridge commands via the `LogsToolset` (UE 5.8+, EditorToolset plugin). Provider: `Toolset.Editor.Toolset.Logs.*`.

| Command | Description |
|---|---|
| `Toolset.Editor.Toolset.Logs.GetLogEntries` | Retrieve recent log entries from the editor output log |
| `Toolset.Editor.Toolset.Logs.GetLogCategories` | List registered log category names |
| `Toolset.Editor.Toolset.Logs.GetVerbosity` | Get the verbosity level for a log category |
| `Toolset.Editor.Toolset.Logs.SetVerbosity` | Set the verbosity level for a log category (requires `LogVerbosityEdit`) |

### Toolset bridges — CVar (1) 🧩

Bridge commands via the EditorToolset plugin (UE 5.8+). Provider: `Toolset.Editor.EngineManagement.*`.

| Command | Description |
|---|---|
| `Toolset.Editor.Toolset.EngineManagement.SearchCVars` | Search CVars by name pattern; sensitive patterns are excluded (requires `CVarInspect`) |

---

## UAIP.Editor.Engine.Plugin

Plugin management for the editor — read / write plugin state, descriptor, and dependencies. Requires UE 5.8+ with the `PluginUtils` plugin enabled. Write commands (`SetPluginEnabled`, `UpdatePluginDescriptor`, `AddPluginDependency`, `RemovePluginDependency`) require a restart to take effect.

| Command | Description |
|---|---|
| 🆓 `GetPluginDescriptor` | Read the full `.uplugin` descriptor JSON for a plugin |
| 🆓 `GetPluginDependents` | List plugins that depend on a given plugin (budget-capped scan; `Truncated: true` on limit) |
| 🆓 `GetPluginTemplateDescriptions` | List available plugin scaffold templates |
| 🆓 `IsPluginCreationAllowed` | Check whether new plugin creation is allowed in the current editor state |
| 🆓 `IsPluginModificationAllowed` | Check whether a specific plugin is modifiable (not Engine/Marketplace/GFP) |
| `SetPluginEnabled` | Enable or disable a plugin (`PluginEnableToggle` required; always returns `RestartRequired: true`) |
| `UpdatePluginDescriptor` | Overwrite selected fields of a plugin's `.uplugin` file (`PluginDescriptorEdit` required; supports `DryRun`) |
| `AddPluginDependency` | Add a dependency entry to a plugin's `.uplugin` (`PluginDependencyEdit` required) |
| `RemovePluginDependency` | Remove a dependency entry from a plugin's `.uplugin` (`PluginDependencyEdit` required) |

### Toolset bridges — Plugin (15) 🧩

Bridge commands via the `PluginToolset` (UE 5.8+). Provider: `Toolset.Plugin.*`.

| Command | Description |
|---|---|
| `Toolset.Plugin.ListEnabledPlugins` | List currently enabled plugins |
| `Toolset.Plugin.ListDiscoveredPlugins` | List all discovered plugins (enabled + disabled) |
| `Toolset.Plugin.GetPluginInfo` | Get plugin details by name |
| `Toolset.Plugin.IsEnabled` | Check whether a plugin is currently enabled |
| `Toolset.Plugin.GetPluginDependencies` | Get the direct dependencies declared by a plugin |
| `Toolset.Plugin.GetPluginForAsset` | Resolve the owning plugin for a given asset path |
| `Toolset.Plugin.GetPluginDescriptor` | Read the `.uplugin` descriptor (Toolset variant) |
| `Toolset.Plugin.GetPluginDependents` | List plugins that depend on a given plugin |
| `Toolset.Plugin.GetPluginTemplateDescriptions` | List scaffold templates |
| `Toolset.Plugin.IsPluginCreationAllowed` | Check creation permission |
| `Toolset.Plugin.IsPluginModificationAllowed` | Check modification permission |
| `Toolset.Plugin.SetPluginEnabled` | Enable / disable a plugin (requires `PluginEnableToggle`) |
| `Toolset.Plugin.UpdatePluginDescriptor` | Update descriptor fields (requires `PluginDescriptorEdit`) |
| `Toolset.Plugin.AddPluginDependency` | Add a dependency (requires `PluginDependencyEdit`) |
| `Toolset.Plugin.RemovePluginDependency` | Remove a dependency (requires `PluginDependencyEdit`) |

---

## UAIP.Editor.Engine.ConfigSettings

Project Settings and Editor Preferences management via `ISettingsModule`. Commands use a three-level path `ContainerName / CategoryName / SectionName` to address a settings section. Write operations are restricted to files under the project `Config/` directory — engine ini files are rejected with `PolicyViolation`.

| Command | Description |
|---|---|
| 🆓 `ListSettingsContainers` | List all registered settings containers (e.g. `Project`, `Editor`). No capability required |
| 🆓 `ListSettingsCategories` | List all categories in a settings container. No capability required |
| 🆓 `ListSettingsSections` | List all sections in a settings category. No capability required |
| 🆓 `GetSettingsSchema` | Return a JSON artifact with editable property names, types, descriptions, defaults, and edit conditions for a section (requires `EditorInspect`) |
| 🆓 `GetSettingsValues` | Return a JSON artifact with current property values for a section. Secret fields (name matches a secret pattern, has secret metadata, or is a file path type) are masked with `***` (requires `EditorInspect`) |
| `SetSettingsValues` | Merge a `Properties` map into the settings object via `ImportText`. Supports `DryRun` (validates without applying). Requires `ConfigSettingsEdit`. Blocked during PIE |
| `SaveSettings` | Persist in-memory settings to the section's ini file via `ISettingsSection::Save()`. Requires `ConfigSettingsSave`. Blocked during PIE and when `bDisableSave` is set |
| `ResetSettingsToDefaults` | Revert the settings object to class defaults and save. Requires `ConfigSettingsReset`. Blocked during PIE |

### Toolset bridges — ConfigSettings (8) 🧩

Bridge commands via the `ConfigSettingsToolset` plugin (UE 5.8+). Provider: `Toolset.ConfigSettings.*`.

| Command | Description |
|---|---|
| `Toolset.ConfigSettings.ListContainers` | List all registered settings containers |
| `Toolset.ConfigSettings.ListCategories` | List all categories within a settings container |
| `Toolset.ConfigSettings.ListSections` | List all sections within a settings category |
| `Toolset.ConfigSettings.GetSectionSchema` | Get the property schema for a settings section |
| `Toolset.ConfigSettings.GetSectionPropertyValues` | Get current property values for a settings section |
| `Toolset.ConfigSettings.SetSectionProperties` | Set property values on a settings section and persist them (requires `ConfigSettingsEdit`) |
| `Toolset.ConfigSettings.SaveSection` | Persist the current in-memory settings for a section to its ini file (requires `ConfigSettingsSave`) |
| `Toolset.ConfigSettings.ResetSectionToDefaults` | Reset all property values of a settings section to their compiled defaults (requires `ConfigSettingsReset`) |

---

## UAIP.Editor.Observation

Capture screenshots and dump editor state — all read-only.

| Command | Description |
|---|---|
| 🆓 `CaptureActiveWindowImage` | Screenshot of the active top-level editor window (PNG artifact). The editor does not have to be the foreground application: when no window is active, the main window is captured instead and `Result.CapturedWindow` says which one you got (`"ActiveWindow"` / `"MainWindow"`). The fallback only reaches the main window, so a floating asset editor or modal dialog needs `CaptureEditorTabImage` |
| 🆓 `CaptureEditorTabImage` | Screenshot of a specified editor tab's widget area, addressed by Slate layout identifier — `DumpEditorState`'s `ActiveTabId` can be passed straight through. Works with the editor in the background. ⚠️ Brings the named tab to the front of its stack before capturing (a tab behind a sibling is not drawn and would come back empty), so capturing changes which tab the user sees |
| 🆓 `CaptureGraphViewportImage` | Screenshot of an SGraphEditor viewport |
| 🆓 `DumpEditorState` | Active tab, open assets, window dimensions, etc. (JSON) |
| 🆓 `DumpSelectionState` | Current editor selection — actors, objects, graph nodes (JSON) |
| 🆓 `DumpOpenTabs` | List of open asset editor tabs (JSON) |
| 🆓 `DumpOutputLog` | Buffered Output Log as a text artifact (line count / filter support) |
| 🆓 `DumpMessageLog` | Message Log entries with category filter (JSON artifact) |
| 🆓 `DumpSlateTree` | Slate widget tree (JSON, root path filter support) |
| 🆓 `InspectMenu` | Top-bar menu structure under a path (labels, enabled, checked) |
| 🆓 `InspectContextMenu` | Context menu items for a target (without executing them) |
| 🆓 `ObserveWidget` | Time-series sampling of widget Visibility / Enabled / Hovered / Focused state |
| 🆓 `GetLogCategories` | List all registered engine log category names (optional substring filter) |
| 🆓 `ListGraphNodes` | List every node in a graph editor tab — `NodeId` (GUID), `NodeClass`, `NodeTitle`, `Position`. Works with any `UEdGraph`-based editor |
| 🆓 `CaptureViewportImageAnnotated` | Viewport screenshot with world-coordinate labels drawn on it (requires `ViewportAnnotationCapture`) |

---

## UAIP.Editor.Execution

Run tests, Python scripts, and Editor Utility Blueprints.

| Command | Description |
|---|---|
| `DiscoverAutomationTests` | Load the automation test modules and return summary counts of discovered tests |
| `ListAutomationTests` | Return a filtered list of automation tests as a JSON artifact |
| `RunAutomationTest` | Run a UE Automation Test by name and return Pass/Fail/Error report |
| `RunAutomationSpec` | Run a UE Automation Spec by name and return Pass/Fail/Error report |
| `GetAutomationTestStatus` | Return the current automation test manager status (inline by default) |
| `StopAutomationTests` | Request cancellation of the running automation test batch |
| `RunEditorPythonScript` 🧩 | Run an inline Python script or a `.py` file (requires `PythonScriptPlugin`) |
| `RunEditorUtilityBlueprint` | Run a specified Editor Utility Blueprint |
| `RunNamedEditorCommand` | Run a named editor console command via `GUnrealEd->Exec` |

---

## UAIP.Editor.UIAutomation

Drive the editor UI — click, type, select, drag.

| Command | Description |
|---|---|
| 🆓 `ClickWidget` | Simulate a left click on a widget identified by path |
| 🆓 `SelectMenuItem` | Open and select a menu item by slash-separated label path |
| 🆓 `InputText` | Type text into a widget identified by path |
| 🆓 `SetCheckboxState` | Set the checked state of a checkbox |
| 🆓 `SetComboSelection` | Select a combo box item by label |
| 🆓 `DragGraphNode` | Drag a graph node by a pixel offset on a specified graph editor tab |
| 🆓 `ConnectGraphPins` | Connect two pins on a graph editor tab |
| 🆓 `AcceptDialog` | Accept the active modal dialog (click OK/Yes/Accept) |
| 🆓 `CancelDialog` | Cancel the active modal dialog (click Cancel/No) |
| 🆓 `InvokeContextMenuAction` | Right-click a target and execute an item from the context menu |
| 🆓 `HoverWidget` | Simulate OnMouseEnter on a widget |
| 🆓 `PressKey` | Simulate a key press with modifiers (blacklist for dangerous shortcuts) |
| 🆓 `WaitForWidget` | Poll until a widget reaches an expected state |
| 🆓 `FillForm` | Bulk-fill a form widget using a sequential state machine |
| 🆓 `SnapshotUI` | Capture a structured snapshot of the UI |
| 🆓 `OpenPasswordTestWindow` | Open a floating test window holding a password `SEditableTextBox` — provides a target for password-field policy tests |

### Toolset bridges — SlateInspector (10) 🧩

Bridge commands via the `SlateInspectorToolset` (UE 5.8+). Provider: `Toolset.Editor.SlateInspector.*`. Widgets are addressed by refPath rather than by the widget-path syntax the native commands use.

| Command | Description |
|---|---|
| `Toolset.Editor.SlateInspector.SnapshotUI` | Snapshot the widget tree at the given ref |
| `Toolset.Editor.SlateInspector.ObserveWidget` | Register a widget for observation; returns the observer `Identifier` |
| `Toolset.Editor.SlateInspector.UnobserveWidget` | Stop observing the widget registered under an `Identifier` |
| `Toolset.Editor.SlateInspector.ListObservers` | List every currently active widget observer |
| `Toolset.Editor.SlateInspector.ClickWidget` | Simulate a mouse click on the widget at the given ref |
| `Toolset.Editor.SlateInspector.HoverWidget` | Move the cursor over the widget at the given ref |
| `Toolset.Editor.SlateInspector.InputText` | Type text into the widget at the given ref |
| `Toolset.Editor.SlateInspector.PressKey` | Send a key press; modifier prefixes are supported (e.g. `Ctrl+S`) |
| `Toolset.Editor.SlateInspector.SetComboSelection` | Select an option in a combo box widget |
| `Toolset.Editor.SlateInspector.FillForm` | Fill multiple form fields in a single call |

---

## UAIP.Editor.Assets

Open, search, create, duplicate, rename, delete assets and folders.

| Command | Description |
|---|---|
| `OpenAsset` | Open the specified asset in its editor |
| `CloseAsset` | Close all editors for the specified asset |
| 🆓 `SearchAssets` | Search assets by path / class / tag |
| `CreateAsset` | Create a new asset of the specified class |
| 🆓 `ListCreatableAssetClasses` | Return every UClass that `CreateAsset` can target, with factory count and default factory (heavy call) |
| 🆓 `ListFactoriesForClass` | Return the factory candidates for a `ClassName`, each with its `FactoryParams` schema |
| `DuplicateAsset` | Duplicate an existing asset |
| `CopyAsset` | Copy an asset to a new full package path (fails if the destination exists; requires `AssetCreate`) |
| `RenameAsset` | Rename / move an asset to another path |
| `MoveAsset` | Move an asset to another folder keeping its name; reports whether a redirector was left behind (requires `AssetMutate`) |
| `DeleteAsset` | Delete an asset |
| `CreateFolder` | Create a new folder in the Content Browser |
| `DeleteFolder` | Delete an empty folder (returns `NotEmpty` if not empty) |
| `ForceDeleteFolder` | Delete a folder and its assets (max 50 items, no external-reference check) |
| `MoveFolder` | Move every asset in a folder to a destination folder, preserving sub-folders; partial failures are listed in `FailedAssets` (requires `AssetFolderRefactor`) |
| 🆓 `GetSelectedAssets` | Return the assets currently selected in the Content Browser |
| `SelectAssets` | Select the specified assets in the Content Browser (requires `ContentBrowserNavigate`) |
| 🆓 `GetContentBrowserPath` | Return the current folder path shown in the Content Browser |
| `SetContentBrowserPath` | Navigate the Content Browser to a specified folder (requires `ContentBrowserNavigate`) |
| 🆓 `GetOpenAssets` | Return the list of assets currently open in an asset editor |
| 🆓 `ListAssetRedirectors` | List asset redirectors under a folder (`/Game` project-wide by default) with source/destination paths, without loading any assets |
| `FixAssetRedirectors` (requires `RedirectorFixup`) | Fix up and delete all resolvable asset redirectors under `/Game` (project-wide, recursive, always) |
| `FixUpRedirectorsInFolder` (requires `RedirectorFixup`) | Same fix-up limited to one folder; unresolved entries are returned in `FailedRedirectors` |
| 🆓 `GetAssetReferences` | Traverse the asset reference graph (referencers, dependencies, or both) rooted at an asset up to a given depth |
| 🆓 `GetAssetSizeMap` | Aggregate per-asset disk (and optionally resident memory) size under a folder, sorted descending |
| 🆓 `GetAssetSizeMapByClass` | Aggregate disk size per asset class under a folder, sorted descending |
| 🆓 `FindUnreferencedAssets` | Find assets under a folder with no user (non-Engine/Script) referencers (hard-reference heuristic) |
| 🆓 `FindCircularReferences` | Find circular dependency chains among assets under a folder |
| 🆓 `FindBrokenReferences` | Find dependencies pointing at packages no longer registered in the asset registry |
| 🆓 `GetAssetDependencyPath` | Find the shortest dependency or referencer path between two assets |
| 🆓 `RunAssetAudit` | Run a composite audit (unreferenced assets, circular references, broken references, largest assets) under a folder |
| 🆓 `ListPrimaryAssetTypes` | List all registered `PrimaryAssetType`s (`UAssetManager`) with class/directory/asset-count summary |
| 🆓 `GetPrimaryAssetTypeInfo` | Get the full detail (directories, specific assets, default rules) of a single `PrimaryAssetType` |
| 🆓 `ListPrimaryAssets` | List the `PrimaryAssetId`s and assets belonging to a `PrimaryAssetType` |
| 🆓 `GetAssetBundle` | Get the `AssetBundle` entries of a `PrimaryAssetId` (empty array when none are defined) |
| 🆓 `GetAssetTags` | Get the Asset Registry tag map of an asset |
| 🆓 `GetPrimaryAssetIdForPath` | Resolve an asset path to its `PrimaryAssetId` (`Found:false`, not an error, when unmanaged) |
| 🆓 `GetPrimaryAssetRules` | Get the merged (type default + per-asset override) `PrimaryAssetRules` of a `PrimaryAssetId` |
| 🆓 `GetManagedPackageList` | Get the packages managed by a `PrimaryAssetId` |
| 🆓 `GetPrimaryAssetLoadList` | Resolve the object paths that would actually load for a `PrimaryAssetId` under given bundle conditions |
| 🆓 `GetLoadedPrimaryAssets` | Get the currently loaded / pending `PrimaryAssetId`s and their loaded bundle state |
| `AddPrimaryAssetType` (requires `PrimaryAssetTypeAdd`) | Add a `PrimaryAssetType` to `PrimaryAssetTypesToScan` (persisted to `DefaultGame.ini`) and scan it immediately |
| `RemovePrimaryAssetType` (requires `PrimaryAssetTypeRemove`) | Remove a `PrimaryAssetType` from `PrimaryAssetTypesToScan` (persisted); rejects if assets exist unless `Force` |
| `SetPrimaryAssetRules` (requires `PrimaryAssetRulesOverride`) | Temporarily override a `PrimaryAssetId`'s rules in memory only (not persisted) |
| `LoadPrimaryAsset` (requires `PrimaryAssetLoad`) | Explicitly load `PrimaryAsset`s into memory (non-blocking, allowed during PIE) |
| `UnloadPrimaryAsset` (requires `PrimaryAssetUnload`) | Explicitly unload `PrimaryAsset`s from memory (rejected during PIE) |

### Toolset bridges — Assets (6) 🧩

Bridge commands via the `EditorAppToolset` (UE 5.8+, EditorToolset plugin). Provider: `Toolset.Editor.Toolset.Assets.*`.

| Command | Description |
|---|---|
| `Toolset.Editor.Toolset.Assets.GetSelectedAssets` | Get currently selected assets in the Content Browser |
| `Toolset.Editor.Toolset.Assets.SelectAssets` | Select assets in the Content Browser (requires `ContentBrowserNavigate`) |
| `Toolset.Editor.Toolset.Assets.GetContentBrowserPath` | Get the current Content Browser folder path |
| `Toolset.Editor.Toolset.Assets.SetContentBrowserPath` | Navigate the Content Browser to a folder (requires `ContentBrowserNavigate`) |
| `Toolset.Editor.Toolset.Assets.OpenEditorForAsset` | Open an asset in its editor (requires `AssetWindowControl`) |
| `Toolset.Editor.Toolset.Assets.GetOpenAssets` | List assets currently open in an asset editor |

---

## UAIP.Editor.SemanticSearch 🧩

Semantic asset search and index management. Requires the `SemanticSearch` plugin (UE 5.8+, Experimental) and an OpenAI API key configured in Editor Preferences → Plugins → Semantic Search.

| Command | Description |
|---|---|
| `Search` | Search project assets by natural-language query (hybrid BM25+vector, up to 500 results) |
| `FindSimilar` | Find assets similar to a reference asset via vector similarity |
| `GetIndexStats` | Return current index statistics (asset count, last-built timestamp) |
| `StartIndexing` | Trigger a full semantic index rebuild (long-running; requires `SemanticSearchEdit`) |
| `CancelIndexing` | Cancel an in-progress index build (requires `SemanticSearchEdit`) |

### Toolset bridges (2) 🧩

Bridge commands via the `SemanticSearchToolset` plugin (UE 5.8+). Provider: `Toolset.Editor.SemanticSearch.*`. These commands mirror the native `Search` and `FindSimilar` above and are provided exclusively as a Toolset bridge (no UAIP native equivalent for these two Toolset-side commands; see ADR `2026-06-25-SemanticSearchToolset-BridgeOnly-Exception.md`).

| Command | Description |
|---|---|
| `Toolset.Editor.SemanticSearch.Search` | Hybrid BM25+vector search via SemanticSearchToolset |
| `Toolset.Editor.SemanticSearch.FindSimilar` | Vector similarity search via SemanticSearchToolset |

---

## UAIP.Editor.Level

Editor-side actor placement, transforms, and level loading.

| Command | Description |
|---|---|
| 🆓 `ListLevelActors` | List all actors in the open level |
| `PlaceActorInLevel` | Place an actor in the editor level |
| `DeleteActorFromLevel` | Remove an actor from the editor level |
| 🆓 `GetActorTransform` | Get the transform of an editor actor |
| `SetActorTransform` | Set the transform of an editor actor |
| `OpenLevel` | Open a level in the editor viewport (File > Open Level) |
| `NewLevel` | Create a new level from a template (EmptyLevel / EmptyOpenWorld / Basic / OpenWorld) |
| `SelectActors` | Select the specified actors in the editor level (replace or add to current selection) |
| 🆓 `ListSelectedActors` | Return a list of actors currently selected in the editor |
| `ClearSelection` | Clear the current selection in the editor level |
| `FocusOnActors` | Focus the viewport camera on the specified actors (omit to use the current selection) |
| 🆓 `GetCameraTransform` | Get the camera location and rotation of the active level editor viewport |
| `SetCameraTransform` | Set the camera location and rotation of the active level editor viewport |
| 🆓 `GetVisibleActors` | Return actors currently visible in the active editor viewport (frustum culling) |
| 🆓 `ProjectWorldToScreen` | Project a world-space position to screen coordinates |
| 🆓 `ProjectScreenToWorld` | Cast a ray from screen coordinates into the world (ECC_Visibility line trace) |

### Toolset bridges — Level (8) 🧩

Bridge commands via the `EditorAppToolset` (UE 5.8+, EditorToolset plugin). Provider: `Toolset.Editor.Toolset.Level.*`.

| Command | Description |
|---|---|
| `Toolset.Editor.Toolset.Level.GetSelectedActors` | Return actors currently selected in the level editor viewport |
| `Toolset.Editor.Toolset.Level.SelectActors` | Select the specified actors in the level editor (requires `EditorActorEdit`) |
| `Toolset.Editor.Toolset.Level.GetCameraTransform` | Get the active viewport camera transform |
| `Toolset.Editor.Toolset.Level.SetCameraTransform` | Set the active viewport camera transform (requires `EditorViewportControl`) |
| `Toolset.Editor.Toolset.Level.FocusOnActors` | Focus the viewport on the specified actors (requires `EditorViewportControl`) |
| `Toolset.Editor.Toolset.Level.GetVisibleActors` | List actors visible in the active viewport |
| `Toolset.Editor.Toolset.Level.WorldPosToScreenCoords` | Project a world position to screen space |
| `Toolset.Editor.Toolset.Level.ScreenCoordsToWorld` | Project screen coordinates to world space (requires `EditorInspect`) |

---

## UAIP.Editor.Property

Read and write properties on actors, assets, Blueprint defaults, DataTable rows, World / Project settings. `Get*` commands mask secret-looking property values (name matches a secret pattern, has secret metadata, or is a file path type) with `***`, including nested struct members.

| Command | Description |
|---|---|
| 🆓 `GetActorProperty` | Get a property value from an editor actor |
| `SetActorProperty` | Set a property on an editor actor |
| 🆓 `GetWorldSetting` | Get a WorldSettings property |
| `SetWorldSetting` | Set a WorldSettings property |
| 🆓 `GetAssetProperty` | Get a property from an asset (DataAsset etc.) |
| `SetAssetProperty` | Set a property on an asset and call `MarkPackageDirty` |
| 🆓 `GetBlueprintDefault` | Get a property from a Blueprint CDO |
| `SetBlueprintDefault` | Set a property on a Blueprint CDO |
| 🆓 `GetProjectSetting` | Get a property from a `UDeveloperSettings` CDO |
| `SetProjectSetting` | Set a property on a `UDeveloperSettings` CDO and call `SaveConfig()` |
| 🆓 `GetDataTableRow` | Get a DataTable row property |
| `SetDataTableRow` | Set a DataTable row property |

---

## UAIP.Editor.Blueprint

Edit Blueprint variables, event graph nodes, and SCS components.

### Variables & graph (10)

| Command | Description |
|---|---|
| `AddBlueprintVariable` | Add a member variable to a Blueprint (type, default, tooltip) |
| `DeleteBlueprintVariable` | Remove a member variable |
| `SetBlueprintVariableDefault` | Update a Blueprint variable's CDO default value |
| `AddGraphNode` | Add a node to a Blueprint graph (VariableGet/Set, FunctionCall, Event, ...) |
| `DeleteGraphNode` | Delete a graph node by GUID (EntryNode / Tunnel cannot be deleted) |
| `ConnectBlueprintPins` | Connect two pins in a Blueprint graph |
| `DisconnectBlueprintPins` | Disconnect a pin connection |
| `ListBlueprintPins` | List pins of a Blueprint graph node |
| `SetPinDefaultValue` | Set a default value on a Blueprint graph node pin (auto-selects DefaultValue / DefaultObject / DefaultTextValue based on pin type) |
| `GetPinDefaultValue` | Get the current default value of a Blueprint graph node pin |

### Components — SCS (8)

| Command | Description |
|---|---|
| `ListBlueprintComponents` | List all components visible from a Blueprint (SCS, Inherited, Native) |
| `AddBlueprintComponent` | Add a new SCS component node to a Blueprint |
| `DeleteBlueprintComponent` | Delete an SCS component from a Blueprint |
| `RenameBlueprintComponent` | Rename an SCS component |
| `ReparentBlueprintComponent` | Change an SCS component's parent |
| `DuplicateBlueprintComponent` | Duplicate an SCS component |
| `GetBlueprintComponentProperty` | Get a property value from an SCS component |
| `SetBlueprintComponentProperty` | Set a property on an SCS component |

### Compile (2)

| Command | Description |
|---|---|
| `CompileBlueprint` | Compile a Blueprint and return CompileStatus + structured message log (AnimBlueprint / WidgetBlueprint not supported) |
| `GetBlueprintCompileStatus` | Read the current Blueprint compile status without triggering a compile |

---

## UAIP.Editor.UMG

Widget Blueprint editing — tree, variables, animation, bindings.

### Native (22)

| Command | Description |
|---|---|
| `CreateWidgetBlueprint` | Create a new Widget Blueprint asset |
| `AddWidget` | Add a widget to a Widget Blueprint's tree |
| `RemoveWidget` | Remove a widget from a Widget Blueprint's tree |
| `MoveWidget` | Reorder a widget within a panel or move it to another panel |
| `RenameWidget` | Rename a widget |
| `SetWidgetAsVariable` | Toggle a widget's `bIsVariable` flag |
| `SetNamedSlotContent` | Set the content of a NamedSlot widget |
| `GetNamedSlots` | List NamedSlots in a Widget Blueprint |
| `ReparentWidgetBlueprint` | Change a Widget Blueprint's parent class |
| `GetSlotProperties` | Get a widget's slot properties (JSON, CPF filter, max 64 keys) |
| `SetSlotProperties` | Set a widget's slot properties (32 KiB limit, `/Game/` UObject refs only) |
| `GetWidgets` | Get the full widget tree structure (JSON) |
| `ListWidgetClasses` | List available widget classes (max 500) |
| `CompileWidgetBlueprint` | Compile a Widget Blueprint and return errors / warnings |
| `ListWidgetAnimations` | List animations in a Widget Blueprint |
| `GetWidgetAnimationInfo` | Get track / key info of an animation |
| `CreateWidgetAnimation` | Create a new animation in a Widget Blueprint |
| `AddAnimationTrack` | Add a track to a Widget Animation |
| `ListPropertyBindings` | List property bindings in a Widget Blueprint |
| `AddPropertyBinding` | Add a property binding (same-WBP function / variable only) |
| `RemovePropertyBinding` | Remove a property binding |
| `ExtractWidgetToUserWidget` | Extract a widget subtree into a new UserWidget |

### Toolset bridges (13) 🧩

Mirror of native commands via the `UMGToolSet` plugin. Provider: `Toolset.Editor.UMG.*`. Requires UE 5.8+ and the `UMGToolSet` plugin.

---

## UAIP.Editor.Material

Material graph editing and parameter management.

| Command | Description |
|---|---|
| `GetMaterialInfo` | Basic info (NodeCount, ShadingModel, BlendMode, bHasErrors) |
| `ListMaterialNodes` | List of Material graph nodes (NodeId, ExpressionClass, position, bIsParameter) |
| `AddMaterialNode` | Add a node to the Material graph (ExpressionClass-specified, 6-step allowlist) |
| `DeleteMaterialNode` | Delete a node by NodeId (root deletion returns Conflict) |
| `ConnectMaterialPins` | Connect two pins in a Material graph (cycle / type-mismatch detection) |
| `DisconnectMaterialPins` | Disconnect a pin connection |
| `CompileMaterial` | Compile the material and return errors / warnings |
| `SetMaterialParameterValue` | Set a material parameter value |
| `GetMaterialParameterValue` | Get a material parameter value |
| `ListMaterialExpressionClasses` | List `UMaterialExpression` derived classes (max 500). Use the returned `ClassPath` as the `ExpressionClass` argument for `AddMaterialNode` |
| `RefreshMaterial` | Force-recompile a material (recompiles a saved asset immediately without arguments) |

---

## UAIP.Editor.GameplayTags

Manage project tag tables.

| Command | Description |
|---|---|
| `ListGameplayTags` | List all tags with filters (native inclusion, parent tag, source) — max 2048 |
| `GetGameplayTagInfo` | Tag details (Comment, Source, bIsNative, bIsRestrictedTag, parent / child) |
| `AddGameplayTag` | Add a normal tag to an INI |
| `AddRestrictedGameplayTag` | Add a Restricted tag to RestrictedTagList INI |
| `RemoveGameplayTag` | Remove a tag from an INI (child / native tag protection) |
| `RenameGameplayTag` | Rename a tag (optionally update asset references) |
| `FindGameplayTagReferencers` | Find assets that reference a tag |

### Toolset bridges — GameplayTags (6) 🧩

Bridge commands via the `GameplayTagsToolset` plugin (UE 5.8+, Experimental). Provider: `Toolset.Editor.GameplayTags.*`.

| Command | Description |
|---|---|
| `Toolset.Editor.GameplayTags.ListTags` | List registered tags, optionally restricted to descendants of `ParentTag` (max 2048) |
| `Toolset.Editor.GameplayTags.GetTagInfo` | Detail for a single tag — Comment, Source, Children |
| `Toolset.Editor.GameplayTags.FindReferencersByTag` | Find assets referencing a tag (max 256 paths) |
| `Toolset.Editor.GameplayTags.AddTag` | Add a tag to an existing `.ini` tag source (requires `GameplayTagEdit`) |
| `Toolset.Editor.GameplayTags.RemoveTag` | Remove a tag from the project tag table; asset references are **not** updated (requires `GameplayTagEdit`) |
| `Toolset.Editor.GameplayTags.RenameTag` | Rename a tag in INI only — no reference update and no redirect entry. Prefer the native `RenameGameplayTag` (requires `GameplayTagEdit`) |

---

## UAIP.Editor.GameFeatures 🧩

GameFeature Plugin management. Requires `GameFeatures` + `GameFeaturesEditor` plugins.

| Command | Description |
|---|---|
| `ListGameFeatures` 🧩 | List GameFeature Plugins with a `FilterState` filter (All / Installed / Mounted / Registered / Loaded / Active) |
| `GetGameFeatureInfo` 🧩 | GFP details (State, Actions, dependencies) |
| `GetGameFeatureActions` 🧩 | List the actions declared by a GameFeature Plugin's `UGameFeatureData` |
| `CreateGameFeaturePlugin` 🧩 | Scaffold a new GameFeature Plugin (with name validation) |
| `DeleteGameFeaturePlugin` 🧩 | Delete a GameFeature Plugin and its content from disk |

### Toolset bridges — GameFeatures (4) 🧩

Bridge commands via the `GameFeaturesToolset` (UE 5.8+, Experimental). Provider: `Toolset.Editor.GameFeatures.*`.

| Command | Description |
|---|---|
| `Toolset.Editor.GameFeatures.ListGameFeatures` | List all registered GameFeature Plugins with their current state |
| `Toolset.Editor.GameFeatures.FindGameFeatureData` | Resolve the `UGameFeatureData` asset refPath for a named plugin |
| `Toolset.Editor.GameFeatures.GetActions` | List the action class names of a `UGameFeatureData` (takes `{"refPath": "..."}`) |
| `Toolset.Editor.GameFeatures.CreateGameFeaturePlugin` | Create a content-only GameFeature Plugin (requires `GameFeatureCreate`) |

---

## UAIP.Editor.Niagara 🧩

Niagara VFX system editing. Requires `Niagara` + `NiagaraEditor` plugins and **UE 5.7 or newer**.

### Native (52)

#### Observation (13)

| Command | Description |
|---|---|
| `GetSystemTopology` 🧩 | Niagara system emitter structure. **UE 5.8 note:** `data` and `dynamic_input_children` are absent from the response; only the `is_dynamic` flag is present. Use `GetStackInputData` for resolved values. |
| `GetSystemCompileState` 🧩 | System compilation state |
| `GetAssetDiscoveryInfo` 🧩 | Niagara asset discovery info |
| `GetScriptAssets` 🧩 | Niagara script asset list |
| `GetNiagaraParameterCollections` 🧩 | Niagara parameter collection list |
| `GetUserVariables` 🧩 | User variable list of a system |
| `GetSystemInfo` 🧩 | System detail info (with metadata) |
| `GetSystemData` 🧩 | System data structure |
| `GetEmitterData` 🧩 | Emitter data structure |
| `GetRendererData` 🧩 | Renderer data structure |
| `GetStackInputData` 🧩 | Module stack input value |
| `UEnum_Info` 🧩 | UEnum information |
| `GetAvailableNiagaraRendererClasses` 🧩 | List of `UNiagaraRendererProperties`-derived classes (max 200). Use the returned `ClassPath` as the `RendererClass` argument of `AddRenderer`. |

#### Schema (7)

| Command | Description |
|---|---|
| `GetSystemSchema` 🧩 | JSON Schema of all editable top-level `UNiagaraSystem` properties (constant across systems — cacheable) |
| `GetEmitterSchema` 🧩 | JSON Schema of all editable top-level emitter properties (cacheable) |
| `GetRendererSchema` 🧩 | JSON Schema for one `UNiagaraRendererProperties` class, selected by `RendererClassPath` |
| `GetDataInterfaceSchema` 🧩 | JSON Schema for one `UNiagaraDataInterface` class, selected by `DataInterfaceClassPath` |
| `GetStackInputSchema` 🧩 | Type / category / `SupportsExpressions` for one module input |
| `GetModuleSchema` 🧩 | Inputs and outputs of a module instance in the stack |
| `GetModuleSchemaFromAsset` 🧩 | Inputs and outputs of a `UNiagaraScript` module asset, without an owning system |

#### Topology and dynamic inputs (7)

| Command | Description |
|---|---|
| `GetEmitterTopology` 🧩 | Full module stack topology of an emitter (all script stacks and their modules) |
| `GetScriptStackTopology` 🧩 | Module topology of one script stack |
| `GetModuleTopology` 🧩 | Input topology of one module |
| `GetStackInputTopology` 🧩 | Full topology of one input — type, value mode, current value, recursive dynamic-input children |
| `GetDynamicInputSchema` 🧩 | Inputs and outputs of a dynamic input script instance in the stack |
| `GetDynamicInputSchemaFromAsset` 🧩 | Inputs and outputs of a `UNiagaraScript` dynamic input asset, without an owning system |
| `GetAvailableDynamicInputs` 🧩 | Dynamic input scripts compatible with a specific module input |

#### Stack issues (2)

| Command | Description |
|---|---|
| `GetStackIssues` 🧩 | All stack issues (errors / warnings / info, including dismissed) with the `IssueId` and `FixId` needed below |
| `ApplyStackIssueFix` 🧩 | Apply a Fix-style automated fix by `IssueId` + `FixId` (Link-style fixes are rejected; requires `NiagaraStackAutoFix`) |

#### Editing (21)

| Command | Description |
|---|---|
| `AddEmitter` 🧩 | Add an emitter to a Niagara system |
| `RemoveEmitter` 🧩 | Remove an emitter |
| `DuplicateEmitter` 🧩 | Duplicate an emitter |
| `SetEmitterEnabled` 🧩 | Toggle emitter enabled state |
| `SetEmitterName` 🧩 | Change emitter name |
| `SetEmitterData` 🧩 | Set emitter data |
| `AddRenderer` 🧩 | Add a renderer to an emitter |
| `RemoveRenderer` 🧩 | Remove a renderer |
| `SetRendererData` 🧩 | Set renderer data |
| `AddModule` 🧩 | Add a module to an emitter module stack |
| `RemoveModule` 🧩 | Remove a module |
| `MoveModule` 🧩 | Move a module within the stack |
| `SetModuleEnabled` 🧩 | Toggle module enabled state |
| `SetStackInputData` 🧩 | Set a module stack input value |
| `SetSystemData` 🧩 | Set system data |
| `AddUserVariables` 🧩 | Add user variables to a system |
| `RemoveUserVariables` 🧩 | Remove user variables |
| `CompileNiagaraSystem` 🧩 | Compile the Niagara system |
| `AddSetParametersModule` 🧩 | Add a Set Parameters module to a stack and register initial parameter entries. The `default_value` field is applied for common types (float, int, bool, struct). |
| `AddSetParameterEntry` 🧩 | Add a parameter entry to an existing Set Parameters module. Requires `script_name` (e.g. `Spawn`, `Update`). The `default_value` field is applied for common types (float, int, bool, struct). |
| `RemoveSetParameterEntry` 🧩 | Remove a parameter entry from a Set Parameters module. Requires `script_name` (e.g. `Spawn`, `Update`). |

#### Blueprint wrappers (2)

| Command | Description |
|---|---|
| `ConstructNiagaraBPWrapperFromSystem` 🧩 | Generate an AActor Blueprint whose variables mirror the user variables of a NiagaraSystem asset (Two-Phase Commit) |
| `ConstructNiagaraBPWrapperFromComponent` 🧩 | Generate a Blueprint wrapper from a NiagaraComponent in the editor world, preserving component variable overrides (Two-Phase Commit) |

### Toolset bridges (45) 🧩

Mirror of native commands via the `NiagaraToolsets` plugin (UE 5.8+ Experimental). Provider: `Toolset.Editor.Niagara.*`. Groups: Info (2), Blueprint (2), System Schema (12), Topology (5), Data (5), Edit-1 (8), Edit-2 (8), Diagnostic (3).

---

## UAIP.Editor.Physics

Physics Asset editing — bodies, shapes, constraints.

### Native (31)

#### Asset / observation (3)

| Command | Description |
|---|---|
| `CreatePhysicsAsset` | Generate and link a Physics Asset from a SkeletalMesh |
| `GetPhysicsAssetSummary` | Body / constraint counts and issue summary |
| `ValidatePhysicsAsset` | Detect orphan constraints, shapeless bodies, etc. |

#### Bodies (15)

| Command | Description |
|---|---|
| `GetBodyNames` | List body names in the Physics Asset |
| `AddBody` | Add a body to the specified bone |
| `RemoveBody` | Remove a body (cascades constraint deletion) |
| `GetBodyPhysicsMode` | Get a body's PhysicsMode (Default / Kinematic / Simulated) |
| `SetBodyPhysicsMode` | Set a body's PhysicsMode |
| `SetAllBodiesPhysicsMode` | Bulk-set PhysicsMode for bodies matching a name pattern |
| `GetBodyMassScale` | Get a body's MassScale |
| `SetBodyMassScale` | Set a body's MassScale |
| `GetBodyCollisionProfile` | Get a body's Collision Profile name |
| `SetBodyCollisionProfile` | Set a body's Collision Profile |
| `SetBodyLinearDamping` | Set a body's Linear Damping |
| `SetBodyAngularDamping` | Set a body's Angular Damping |
| `GetBodyOffset` | Get a body's center-of-mass offset (COMNudge) |
| `SetBodyOffset` | Set a body's center-of-mass offset |
| `MirrorBodies` | Mirror-copy left / right bone bodies and shapes by naming convention |

#### Shapes (8)

| Command | Description |
|---|---|
| `GetBodyShapes` | List collision shapes of a body (with ShapeName) |
| `SetSphere` | Set a body's shape to Sphere |
| `SetCapsule` | Set a body's shape to Capsule |
| `SetBox` | Set a body's shape to Box |
| `RemoveShape` | Remove a shape by ShapeName |
| `RegenerateBodyShapes` | Auto-regenerate shapes from bone geometry |
| `CopyBodyShapes` | Copy shapes from one bone to another |
| `SetPhysicalMaterial` | Set Physical Material on a body or all bodies |

#### Constraints (5)

| Command | Description |
|---|---|
| `GetConstraints` | Get all constraints in the asset (max 256) |
| `ListConstraintsForBody` | Get constraints attached to a specific bone (max 256) |
| `AddConstraint` | Add a rigid-body constraint |
| `SetConstraintLimits` | Set a constraint's angular limits |
| `RemoveConstraint` | Remove a constraint |

### Toolset bridges (17) 🧩

Mirror of native commands via the `PhysicsToolsets` plugin (UE 5.8+ Experimental). Provider: `Toolset.Editor.Physics.*`.

---

## UAIP.Editor.Dataflow 🧩

Dataflow graph editing. Requires `DataflowEditor` plugin.

| Command | Description |
|---|---|
| `GetDataflowGraphInfo` 🧩 | Get graph nodes / edges / variables (JSON) |
| `ListDataflowNodeTypes` 🧩 | List available Dataflow node types |
| `AddDataflowNode` 🧩 | Add a node to a Dataflow graph |
| `RemoveDataflowNode` 🧩 | Remove a node from a Dataflow graph |
| `ConnectDataflowPins` 🧩 | Connect two pins |
| `DisconnectDataflowPins` 🧩 | Disconnect a pin connection |
| `ListDataflowVariables` 🧩 | List graph variables |
| `GetDataflowNodeProperty` 🧩 | Read a node's `EditAnywhere` property value (primitives / enum / FName / FString / simple structs) |
| `SetDataflowNodeProperty` 🧩 | Write a node's `EditAnywhere` property value. Domain-agnostic — used by Cloth Weight Map / simulation config nodes among others |

### Toolset bridges — Dataflow (7) 🧩

Bridge commands via the `DataflowAgentToolset` (UE 5.8+). Provider: `Toolset.Editor.DataflowAgent.*`. Editing commands require `DataflowGraphEdit`.

| Command | Description |
|---|---|
| `Toolset.Editor.DataflowAgent.ListDataflowNodeTypes` | List available Dataflow node types (common types only) |
| `Toolset.Editor.DataflowAgent.GetDataflowGraphInfo` | Node and connection structure of a Dataflow asset |
| `Toolset.Editor.DataflowAgent.ListDataflowVariables` | List variables defined in a Dataflow asset |
| `Toolset.Editor.DataflowAgent.AddDataflowNode` | Add a node to a Dataflow graph (requires `DataflowGraphEdit`) |
| `Toolset.Editor.DataflowAgent.RemoveDataflowNode` | Remove a node from a Dataflow graph (requires `DataflowGraphEdit`) |
| `Toolset.Editor.DataflowAgent.ConnectDataflowPins` | Connect two pins (requires `DataflowGraphEdit`) |
| `Toolset.Editor.DataflowAgent.DisconnectDataflowPins` | Disconnect pins (requires `DataflowGraphEdit`) |

---

## UAIP.Editor.ChaosClothAsset 🧩

Chaos Cloth Asset editing and `ChaosClothAssetToolset` bridge (UE 5.8, Experimental). Requires the `ChaosClothAsset` plugin family.

| Command | Description |
|---|---|
| `CreateClothingAsset` | Create a Clothing Asset from a Skeletal Mesh |
| `AssignClothingToSection` | Bind a Clothing Asset to a Skeletal Mesh LOD/section |
| `RemoveClothingFromSection` | Unbind a Clothing Asset from a section (destructive, irreversible) |
| `ListClothingAssets` | List Clothing Assets bound to a Skeletal Mesh |
| `GetSectionClothing` | Get the Clothing Asset bound to a specific LOD/section |
| `ConvertClothingAssetCommonToChaosClothAsset` | Convert a legacy `UClothingAssetCommon` to `UChaosClothAsset` (Experimental, LOD0 only) |
| `GetClothAssetInfo` | Read LOD count, Sim/Render Mesh vertex counts, the referenced `UDataflow` asset path, and Weight Map attribute names |
| `SetClothWeightMapVertexValues` | Directly set a Weight Map node's per-vertex weight array (destructive) |
| `SetClothMeshImportSource` | Set the imported SkeletalMesh/StaticMesh reference on an Import Dataflow node (`SkeletalMeshImport`/`StaticMeshImport`). The node kind is auto-detected; overwriting an existing reference requires `AllowOverwrite` (destructive) |
| `CreateLegacyClothingAsset` | Create a new legacy `UClothingAssetCommon` by extracting the simulation mesh from an existing SkeletalMesh render section |

`GetClothAssetInfo` returns the Cloth Asset's `UDataflow` reference path — feed it to `UAIP.Editor.Dataflow.*` commands to edit Weight Map / simulation config node properties generically.

### Toolset bridge

Mirror of the 6 `ChaosClothAssetToolset` functions. Provider: `Toolset.Editor.ChaosClothAsset.*`. Available only on UE 5.8+ with `ChaosClothAssetToolset` + `ToolsetRegistry` enabled.

| Command | Description |
|---|---|
| `Toolset.Editor.ChaosClothAsset.CreateClothingAsset` | Passthrough to `ChaosClothAssetToolset` |
| `Toolset.Editor.ChaosClothAsset.AssignClothingToSection` | Passthrough to `ChaosClothAssetToolset` |
| `Toolset.Editor.ChaosClothAsset.RemoveClothingFromSection` | Passthrough to `ChaosClothAssetToolset` |
| `Toolset.Editor.ChaosClothAsset.ListClothingAssets` | Passthrough to `ChaosClothAssetToolset` |
| `Toolset.Editor.ChaosClothAsset.GetSectionClothing` | Passthrough to `ChaosClothAssetToolset` |
| `Toolset.Editor.ChaosClothAsset.ConvertClothingAssetCommonToChaosClothAsset` | Passthrough to `ChaosClothAssetToolset` |

---

## UAIP.Editor.Skeleton

Skeleton and SkeletalMesh editing.

| Command | Description |
|---|---|
| `GetSkeletonInfo` | USkeleton bone hierarchy, sockets, virtual bones (JSON, read-only) |
| `AddSocket` | Add a socket to a specified bone |
| `RemoveSocket` | Remove a socket |
| `SetSocketTransform` | Partially update a socket's transform (omitted fields preserve existing values) |
| `AddVirtualBone` | Add a virtual bone (auto-named if name omitted) |
| `RemoveVirtualBone` | Remove a virtual bone |
| `GetSkeletalMeshInfo` | USkeletalMesh LODs, material slots, related Skeleton path (read-only) |
| `SetSkeletalMeshMaterial` | Assign a material to a slot on a SkeletalMesh |

---

## UAIP.Editor.MetaHuman 🧩

MetaHuman character authoring — asset creation, body / skin / eye / makeup settings, face sculpting, conforming and fitting, cloud rigging, texture synthesis, wardrobe, preview, and the asset build pipeline. Requires the `MetaHumanCharacter` plugin; if it is not enabled none of these commands are registered.

Editing commands open a MetaHuman edit session on demand and keep it open, so a run of commands against the same character does not pay the cost of reopening it. Because opening a session is itself an edit-mode entry, **most reads in this domain are not read-only**: they require `MetaHumanEdit` and are refused while the safety policy is in read-only mode. Call `ReleaseEditSession` once a run is finished. The only exception is `GetViewportSettings`, which requires just `EditorInspect`.

**⬆️ = UE 5.8+ only.** 14 of the 56 commands below depend on engine APIs that do not exist on UE 5.7. They are still registered there, so `uaip_list_commands` lists them with `Available: false` and calling one returns `PolicyViolation` (not `CommandNotFound`). Every command without the mark works on both UE 5.7 and UE 5.8. This symbol is used only in this section.

### Native (56)

#### Creation (1)

| Command | Description |
|---|---|
| `CreateMetaHumanCharacter` | Create a new MetaHuman character asset from the default template and write it to disk (package path must be under `/Game/`; requires `MetaHumanAssetCreate`) |

#### Body, skin and eyes (8)

| Command | Description |
|---|---|
| `GetBodyConstraints` | List every body constraint with its target measurement, whether it takes part in the body solve, and its accepted range (JSON artifact). Names are data driven — call this before `SetBodyConstraints` |
| `SetBodyConstraints` | Update named body constraints and re-evaluate the body (unnamed constraints keep their values; every entry is validated before any is applied) |
| `GetBodyShape` | Read the simplified body shape — masculine/feminine, body fat and muscularity as 0..1 values, plus height in cm |
| `SetBodyShape` | Set the simplified body shape and re-evaluate the body (omitted values unchanged; out-of-range values are rejected, not clamped) |
| `GetSkinSettings` | Read the complete skin settings — tone (lightness / redness), texture variant indices, roughness, palms and nails, freckles, per-region tone accents |
| `SetSkinTone` | Set only the two skin tone axes (lightness / redness); every other skin setting is left unchanged |
| `GetEyeSettings` | Read both eyes in full — Iris, Pupil, Cornea and Sclera groups |
| `SetEyeColor` | Write one temperature / brightness pair into the primary and secondary iris colour of both eyes |

#### Appearance detail (8)

| Command | Description |
|---|---|
| `SetSkinSettings` | Partial update of the full skin settings (omitted fields keep their values; out-of-range values are rejected, not clamped) |
| `GetMakeupSettings` | Read the makeup settings — foundation layer, eye makeup, blush, lip makeup |
| `SetMakeupSettings` | Partial update of the makeup settings (style names must match the engine's own names exactly) |
| `GetHeadModelSettings` | Read eyelash style and colouring plus the full set of teeth shape and colour values |
| `SetHeadModelSettings` | Partial update of the head model settings |
| `SetEyeSettings` | Partial update of the eyes, each eye addressed separately across the Iris / Pupil / Cornea / Sclera groups |
| `GetFaceEvaluationSettings` | Read overall face deviation, fine surface detail deviation and uniform head scale |
| `SetFaceEvaluationSettings` | Partial update of the face evaluation settings |

#### Face sculpting (9)

| Command | Description |
|---|---|
| `GetFaceModelCoefficients` ⬆️ | Read the underlying face model coefficients as a flat number array (JSON artifact); pass the same array back to restore the shape |
| `SetFaceModelCoefficients` ⬆️ | Write the face model coefficients (the array length must match `GetFaceModelCoefficients` exactly; any other length is rejected) |
| `GetFaceLandmarks` | Read the face landmark positions as a JSON artifact; an entry's index in the array is what `TranslateFaceLandmarks` expects |
| `TranslateFaceLandmarks` | Move the named face landmarks by matching deltas (all-or-nothing — if any entry is rejected, nothing is applied) |
| `CommitFaceState` | Commit the accumulated sculpting edits onto the asset; the sculpting commands do not commit on their own |
| `ImportFaceFromDna` | Replace the face from a `.dna` file that must live inside the project directory (requires `MetaHumanFileImport`) |
| `ImportFaceFromTemplate` | Fit the face to a template head mesh whose topology matches a MetaHuman head |
| `ImportFaceFromIdentity` | Fit the face to the conformed mesh of a MetaHuman Identity asset (the identity must already be conformed) |
| `CompareFaceState` | Report whether every corresponding vertex and vertex normal of two characters is within `Tolerance` (a single boolean; no per-vertex breakdown) |

#### Conforming and fitting (10)

| Command | Description |
|---|---|
| `GetMeshDataForConforming` ⬆️ | Read a Static / Skeletal Mesh's vertices and triangle indices into a JSON artifact, in the form the conforming commands take as a target |
| `ConformBodyToTarget` | Reshape the body to the supplied vertices, optionally deriving hand and foot joints (target given as `MeshDataArtifactId` or inline `Vertices`) |
| `ConformFaceToTargetMeshes` ⬆️ | Start an asynchronous solve that reshapes the character towards the target meshes; success means it started — poll `GetAsyncConformState` |
| `AlignToTargetMeshes` ⬆️ | Start a rigid alignment (move / rotate / scale, no shape change) onto the target meshes; run before `ConformFaceToTargetMeshes` |
| `RefineVerticesToTarget` ⬆️ | Start a refinement pass that pulls vertices past what the parametric model alone can express; run after the conform has finished |
| `CommitPosedStateAsAPose` ⬆️ | Evaluate the conformed body in the MetaHuman A pose and rebuild the face state from it, so the result can be posed and animated normally |
| `FitStateToTargetVertices` | One-pass fit of the head to target vertices in MetaHuman head topology and vertex order (no iterative solve) |
| `FitFaceFromBodyWithEyesTeethTemplate` ⬆️ | Rebuild the head from the current body shape, taking eyes and teeth from the supplied template meshes |
| `FitFaceFromBodyWithEyesTeethDna` ⬆️ | Same, taking eyes and teeth from a face DNA file — the head shape still comes from the body, so this is not a face import (requires `MetaHumanFileImport`) |
| `GetAsyncConformState` ⬆️ | Report whether a conform / alignment / refinement is still running; the engine offers no completion event, so poll this until `bIsRunning` is false |

#### Build pipeline (6)

| Command | Description |
|---|---|
| `RequestTextureSources` | Start high resolution face texture synthesis and return once the request is in flight; the work runs for minutes in the background (requires `MetaHumanTextureSynthesis`) |
| `GetTextureSourceState` | Poll whether texture synthesis is still running and whether the character already holds synthesized textures |
| `RequestAutoRigging` | Start face rig generation. ⚠️ **Uploads the character's face data to Epic's cloud rigging service** — the rig is produced remotely and downloaded back, so this requires a signed-in Epic account and network access, and the character data leaves the machine. Rigging usually takes minutes; poll `GetRiggingState` (requires `MetaHumanCloudRigging`) |
| `GetRiggingState` | Poll the rigging state — `Unrigged` / `RigPending` / `Rigged`. `Unrigged` once the request has stopped running means it failed (usually sign-in or connectivity) |
| `CanBuildMetaHuman` | Report whether `BuildMetaHuman` would accept this character and, when it would not, the first unmet requirement. Call this before every build |
| `BuildMetaHuman` | Assemble the character into a collection, an instance and a character blueprint under a new subfolder. ⚠️ **Occupies the game thread for the entire build (seconds to minutes).** The engine shows a progress dialog and keeps redrawing, so the editor stays usable to look at rather than going unresponsive, but no other command runs until the build returns. Long builds can exceed the HTTP transport's own async command timeout (120 s); when that happens the call returns `Timeout` even though **the build may still be running inside the editor**. Don't re-issue the command immediately — call `uaip_get_editor_status` first and follow `RecommendedAction` (expect `WAIT`), and expect the build's artifacts to appear only once it actually finishes. Call `CanBuildMetaHuman` first; a build without auto-rigging and synthesized textures always fails. On failure the assets created under the output folder are deleted; the output folder must not already exist. Other MetaHuman commands are refused while a build runs (requires `MetaHumanBuild`) |

#### Preview (3)

| Command | Description |
|---|---|
| `GetViewportSettings` | Read the preview viewport settings — lighting environment, light rotation, background colour, level of detail, hair cards vs strands, preview skin material and camera framing (read-only; requires only `EditorInspect`) |
| `SetViewportSettings` | Partial update of the preview viewport settings (at least one setting must be supplied; out-of-range values are rejected, not clamped). `PreviewMaterial` is named as the editor's viewport toolbar labels it — **pick `Skin` before capturing an image to check a colour**, because `Topology` is a topology visualisation that hides skin, makeup and eye colour entirely, and `Clay` is untextured grey. `CameraFrame` is always recorded on the character, but the preview camera only moves while the character is open in the MetaHuman character editor. A custom lighting environment cannot be selected here — the two supported engine versions describe one differently, so it is set in the editor's viewport toolbar instead |
| `RefreshCharacterPreview` ⬆️ | Propagate pending collection edits back onto the character and re-run the editor pipeline so the preview reflects them |

#### Wardrobe (10)

| Command | Description |
|---|---|
| `ListWardrobeSlots` | List the wardrobe slots the character's collection defines with the number of items in each; names come from the pipeline at runtime, so call this before `AssignWardrobeItem` |
| `ListWardrobeItems` | List the wardrobe items, optionally for one slot; each entry carries the opaque `ItemKey` handle |
| `GetWardrobeItemInfo` | Read one wardrobe item — the slot it occupies, its display name and the package path of the asset it wraps |
| `AssignWardrobeItem` ⬆️ | Assign an asset (groom, garment, …) to a wardrobe slot, select it and rebuild the preview — no separate `RefreshCharacterPreview` needed |
| `RemoveWardrobeItem` ⬆️ | Remove a wardrobe item, clearing the slot selection first when the character is wearing it, then rebuild the preview |
| `ReplaceWardrobeItem` ⬆️ | Replace a wardrobe item with a different asset in the slot the outgoing item occupied, then rebuild the preview |
| `GetWardrobeItem` | Read one wardrobe item asset addressed by package path — the package path of its principal asset, the class path of its pipeline, its thumbnail texture and thumbnail name, and whether it is an asset in its own right. This is the item asset itself, not an item a character is wearing — for that use `GetWardrobeItemInfo`, which takes a character path and an `ItemKey` instead |
| `SetWardrobeItem` | Partial update of a wardrobe item asset's principal asset, thumbnail texture and thumbnail name (omitted fields keep their values, but at least one must be supplied; an empty string in either path field clears that reference rather than naming an asset). The pipeline is not settable here — use `SetWardrobeItemPipeline` |
| `SetWardrobeItemPipeline` | Give a wardrobe item asset a pipeline of the named class, replacing whatever pipeline it had; `PipelineClassPath` is a class path, so take one from `ListItemPipelineClasses` rather than assembling it |
| `ListItemPipelineClasses` | List the item pipeline classes a wardrobe item asset may be built through, with their display names. Which classes exist depends on the plugins the project has loaded; abstract, deprecated and hot-reload superseded classes are left out, so every class listed is one `SetWardrobeItemPipeline` accepts |

#### Session (1)

| Command | Description |
|---|---|
| `ReleaseEditSession` | Release the edit session held open for a character; the call never aborts work that is still in flight |

### Toolset bridges (9) 🧩

Bridge commands via the `MetaHumanGenerator` Python toolset. Provider: `Toolset.Editor.MetaHuman.*`. Available only on UE 5.8+ with `MetaHumanGenerator` + `ToolsetRegistry` enabled — on UE 5.7 the bridge provider is not registered at all, so these names return `CommandNotFound`. Marked `Stability: Experimental` because the underlying engine Python toolset is itself experimental.

Unlike the native commands, every bridge command except `Create` needs an explicit session reference from `BeginEdit`, which also means none of them can run while the safety policy is read-only. All require `MetaHumanEdit`, except `Create` which requires `MetaHumanAssetCreate`.

| Command | Description |
|---|---|
| `Toolset.Editor.MetaHuman.BeginEdit` | Open an edit session on a character and return the session reference the other bridge commands take |
| `Toolset.Editor.MetaHuman.EndEdit` | Close a session opened by `BeginEdit` and take the character out of the editor's edit set |
| `Toolset.Editor.MetaHuman.GetBodyShape` | Return the four simplified body shape values of the session's character |
| `Toolset.Editor.MetaHuman.SetBodyShape` | Set the four simplified body shape values and commit, including the neck region rebuild (out-of-range values are clamped by the toolset rather than refused — the one behavioural difference from the native command) |
| `Toolset.Editor.MetaHuman.GetSkinTone` | Return lightness and redness of the session's character |
| `Toolset.Editor.MetaHuman.SetSkinTone` | Set lightness and redness and commit the skin settings; the rest of the skin settings are left as they are |
| `Toolset.Editor.MetaHuman.GetEyeColor` | Return temperature and brightness, read from the right eye's primary iris colour |
| `Toolset.Editor.MetaHuman.SetEyeColor` | Set one eye colour on both eyes and commit the eye settings, so the two eyes always end up matching |
| `Toolset.Editor.MetaHuman.Create` | Create a new MetaHuman character asset under `/Game/` and return a reference to it (requires `MetaHumanAssetCreate`) |

---

## UAIP.Editor.DataTable

DataTable row management and import / export.

| Command | Description |
|---|---|
| `ListDataTableRows` | List row keys in a DataTable |
| `AddDataTableRow` | Add a new row |
| `DeleteDataTableRow` | Delete a row |
| `DuplicateDataTableRow` | Duplicate a row |
| `ImportDataTableFromCSV` | Bulk-import a CSV string (Replace / Merge modes) |
| `ExportDataTableToCSV` | Export a DataTable as a CSV artifact |
| `GetDataTableRowStruct` | Get the row struct (UScriptStruct) field definitions |
| `ListDataTableRowStructs` | List `FTableRowBase`-derived structs usable as row structs — feed `ClassPath` to `CreateAsset` as `FactoryParams.RowStructPath` |

---

## UAIP.Editor.AnimBlueprint

Anim Blueprint graph and StateMachine editing.

| Command | Description |
|---|---|
| `GetAnimBlueprintInfo` | AnimGraph node list and StateMachine structure (degraded mode during PIE) |
| `GetAvailableAnimGraphNodeClasses` | List `UAnimGraphNode_Base` subclasses — feed `ClassPath` to `AddAnimGraphNode` |
| `AddAnimGraphNode` | Add a `UAnimGraphNode_Base` derived node by NodeClass |
| `RemoveAnimGraphNode` | Remove a node by NodeId |
| `ConnectAnimGraphPins` | Connect two pins (WouldCreateCycle DFS pre-detection) |
| `DisconnectAnimGraphPins` | Disconnect a pin connection |
| `AddAnimState` | Add a State to a StateMachine |
| `RemoveAnimState` | Remove a State by NodeId |
| `AddAnimTransition` | Add a From→To Transition (idempotent on duplicates) |
| `RemoveAnimTransition` | Remove a Transition by NodeId |
| `CompileAnimBlueprint` | Compile and return CompileStatus + error log |

---

## UAIP.Editor.SoundCue

SoundCue graph editing.

| Command | Description |
|---|---|
| `GetSoundCueInfo` | SoundCue graph nodes and connection topology (JSON) |
| `AddSoundCueNode` | Add a node by SoundNodeClass (6-step allowlist) |
| `RemoveSoundCueNode` | Remove a node by NodeId (root deletion returns Conflict) |
| `ConnectSoundCuePins` | Connect two pins (cycle / dynamic input pin auto-add) |
| `DisconnectSoundCuePins` | Disconnect a pin connection (PinIndex=-1 disconnects all) |
| `SetSoundCueNodeProperty` | Set a SoundCue node property (Object / Class / Delegate denylist) |
| `CompileSoundCue` | Rebuild the SoundNode tree from the graph |

---

## UAIP.Editor.SoundSettings

SoundClass hierarchy, SoundAttenuation, and SoundMix asset property editing.

| Command | Description |
|---|---|
| `GetSoundClassInfo` | Return SoundClass Properties (FSoundClassProperties), ChildClasses, ParentClass, and PassiveSoundMixModifiers as JSON |
| `SetSoundClassSettings` | Set one FSoundClassProperties field on a SoundClass asset (changing LoadingBehavior is rejected) |
| `ListSoundClasses` | Enumerate SoundClass assets in the project (AssetPath / ParentClassPath / ChildClassPaths; up to 1000) |
| `AddSoundClassChild` | Add a child class to the SoundClass hierarchy (cycle detection; depth limit 32) |
| `RemoveSoundClassChild` | Remove a child class from the SoundClass hierarchy and clear both directions of the link |
| `GetSoundAttenuationInfo` | Return FSoundAttenuationSettings of a SoundAttenuation asset as JSON |
| `SetSoundAttenuationSettings` | Set one FSoundAttenuationSettings field on a SoundAttenuation asset |
| `ListSoundAttenuations` | Enumerate SoundAttenuation assets in the project (up to 1000) |
| `GetSoundMixInfo` | Return all SoundMix settings (EQ, SoundClassEffects, fade timings) as JSON |
| `SetSoundMixSettings` | Set one top-level SoundMix field (direct write to SoundClassEffects array is rejected) |
| `SetSoundMixAdjuster` | Add or update a SoundClassAdjuster identified by SoundClass path (Upsert; omitted fields keep existing values or use engine defaults) |
| `RemoveSoundMixAdjuster` | Remove the SoundClassAdjuster for the specified SoundClass from a SoundMix |
| `ListSoundMixes` | Enumerate SoundMix assets in the project (up to 1000) |

---

## UAIP.Editor.MVVM 🧩

ViewModel Blueprint property management, View Binding / Event authoring, and Widget ViewModel wiring. Requires the `ModelViewViewModel` plugin (enabled by default since UE 5.5).

### Native (26)

#### ViewModel property management

| Command | Description |
|---|---|
| `ListViewModelClasses` | Enumerate `UMVVMViewModelBase`-derived Blueprint classes via AssetRegistry (optional `SearchPath` filter; up to 1000) |
| `AddViewModelProperty` | Add a property to a ViewModel Blueprint (7 property types; optional `DefaultValue`; optional getter / setter generation) |
| `RemoveViewModelProperty` | Remove a property from a ViewModel Blueprint by name |
| `ListViewModelProperties` | List all properties of a ViewModel Blueprint |

#### Widget ViewModel connection

| Command | Description |
|---|---|
| `AddViewModelToWidget` | Add a ViewModel to a WidgetBlueprint (must be a `/Game/`-rooted `UMVVMViewModelBase` subclass) |
| `RemoveViewModelFromWidget` | Remove a ViewModel entry from a WidgetBlueprint by name |
| `ListWidgetViewModels` | List ViewModels currently wired to a WidgetBlueprint |
| `RenameViewModelInWidget` | Rename a ViewModel entry inside a WidgetBlueprint |
| `ReparentViewModelInWidget` | Change the class of a ViewModel entry inside a WidgetBlueprint |

#### View Binding operations

| Command | Description |
|---|---|
| `AddViewBinding` | Add a View Binding to a WidgetBlueprint |
| `RemoveViewBinding` | Remove a View Binding from a WidgetBlueprint by `BindingId` |
| `ListViewBindings` | List all View Bindings in a WidgetBlueprint |
| `GetViewBinding` | Get details of a single View Binding by `BindingId` |
| `UpdateViewBinding` | Partially update fields of a View Binding |
| `SetViewBindingEnabled` | Enable or disable a View Binding |
| `SetViewBindingConversionFunction` | Set or clear the conversion function for a View Binding |
| `SetViewBindingExecutionMode` | Set the execution mode for a View Binding |
| `ListConversionFunctions` | List available conversion functions for a WidgetBlueprint (expensive on large projects — use `SearchPath` filter) |

#### View Event operations

| Command | Description |
|---|---|
| `AddViewEvent` | Add a View Event to a WidgetBlueprint (returns `EventId`; empty string on failure) |
| `RemoveViewEvent` | Remove a View Event from a WidgetBlueprint |
| `ListViewEvents` | List all View Events in a WidgetBlueprint |

#### ViewModel source settings

| Command | Description |
|---|---|
| `SetViewModelSource` | Change the `CreationType` of a ViewModel entry (Remove + Add round-trip; `Context` type requires UE 5.8+) |
| `GetViewModelSource` | Get the current source configuration of a ViewModel entry |

#### Observation / validation

| Command | Description |
|---|---|
| `GetWidgetBindableProperties` | List bindable properties of a WidgetBlueprint (widget properties and ViewModel properties) |
| `ValidateViewBindings` | Validate all View Bindings in a WidgetBlueprint (expensive on large projects) |
| `GetMVVMViewInfo` | Get the MVVM configuration summary of a WidgetBlueprint (`bMVVMConfigured: false` when MVVM is not configured) |

### Toolset bridges (9) 🧩

Bridge commands via the `MVVMToolset` plugin (UE 5.8+). Provider: `Toolset.MVVM.*`. `CreateViewModel` and `ListViewModels` are unique to this bridge; other commands mirror native equivalents.

| Command | Description |
|---|---|
| `Toolset.MVVM.CreateViewModel` | Create a ViewModel Blueprint asset |
| `Toolset.MVVM.AddViewModelProperty` | Add a property to a ViewModel Blueprint |
| `Toolset.MVVM.ListViewModels` | List ViewModel classes (by class-type filter) |
| `Toolset.MVVM.ListWidgetViewModels` | List ViewModels wired to a WidgetBlueprint |
| `Toolset.MVVM.AddViewModelToWidget` | Add a ViewModel to a WidgetBlueprint |
| `Toolset.MVVM.ListWidgetViewBindings` | List View Bindings of a WidgetBlueprint |
| `Toolset.MVVM.RemoveWidgetViewBinding` | Remove a View Binding from a WidgetBlueprint |
| `Toolset.MVVM.CreateViewBinding` | Create a View Binding in a WidgetBlueprint |
| `Toolset.MVVM.ListConversionFunctions` | List available conversion functions |

---

## UAIP.Editor.BehaviorTree

Behavior Tree graph editing and Blackboard key management.

| Command | Description |
|---|---|
| `GetBehaviorTreeNodeList` | Flat list of every node — `NodeGuid`, `NodeClass`, `DisplayName`, `Depth` (0 = root composite), `ParentNodeGuid` |
| `GetBehaviorTreeSubtree` | Recursive subtree (Composite / Task / Decorator / Service) rooted at a `NodeGuid`, `MaxDepth` 1–32 |
| `GetAvailableBTCompositeClasses` | List `UBTCompositeNode` subclasses — feed `ClassPath` to `AddBehaviorTreeCompositeNode` |
| `GetAvailableBTTaskClasses` | List `UBTTaskNode` subclasses — feed `ClassPath` to `AddBehaviorTreeTaskNode` |
| `GetAvailableBTDecoratorClasses` | List `UBTDecorator` subclasses — feed `ClassPath` to `AddBehaviorTreeDecoratorNode` |
| `GetAvailableBTServiceClasses` | List `UBTService` subclasses — feed `ClassPath` to `AddBehaviorTreeServiceNode` |
| `AddBehaviorTreeCompositeNode` | Add a Composite node (Sequence / Selector / SimpleParallel) |
| `AddBehaviorTreeTaskNode` | Add a Task node by TaskClass |
| `AddBehaviorTreeDecoratorNode` | Attach a Decorator to a parent node |
| `AddBehaviorTreeServiceNode` | Attach a Service to a parent Composite node |
| `RemoveBehaviorTreeNode` | Remove a node by NodeId |
| `SetBehaviorTreeNodeProperty` | Set a node property (FBlackboardKeySelector / generic ImportText_Direct) |
| `ListBlackboardKeys` | List Blackboard asset keys (allowed during PIE) |
| `AddBlackboardKey` | Add a key (KeyType allowlist, duplicate-name check) |
| `RemoveBlackboardKey` | Remove an unreferenced key (returns Conflict + referencers if in use) |
| `SetBehaviorTreeBlackboard` | Change the Blackboard asset a BT references |
| `RequestBehaviorTreeAutoArrange` | Run the AutoArrange pass on an open BT editor |

### Toolset bridges — AIModule (7) 🧩

Bridge commands via the `AIModuleToolset` (UE 5.8+, Experimental). Provider: `Toolset.Editor.AIModule.*`. Observation only.

| Command | Description |
|---|---|
| `Toolset.Editor.AIModule.GetBlackboard` | Blackboard asset associated with a BehaviorTree |
| `Toolset.Editor.AIModule.GetRootDecorators` | Decorators attached to the root composite node |
| `Toolset.Editor.AIModule.ListNodes` | All nodes with their indices and types |
| `Toolset.Editor.AIModule.GetNodeDepth` | Depth of a single node identified by index |
| `Toolset.Editor.AIModule.GetNodeDepths` | Depth of every node as a flat list |
| `Toolset.Editor.AIModule.GetChildren` | Immediate children of a composite node identified by refPath |
| `Toolset.Editor.AIModule.GetSubtree` | Subtree rooted at a node identified by refPath |

---

## UAIP.Editor.MetaSound 🧩

MetaSound graph editing. Requires `Metasound` plugin.

| Command | Description |
|---|---|
| `GetMetaSoundInfo` 🧩 | MetaSoundSource / MetaSoundPatch graph topology (nodes, connections, I/O vertices) |
| `GetAvailableMetaSoundNodeClasses` 🧩 | List frontend-registry node classes (`ClassName`, `Variant`, `MajorVersion`, `DisplayName`) for `AddMetaSoundNode`; filtered to engine-standard namespaces |
| `AddMetaSoundNode` 🧩 | Add a node by `Namespace::Name` (MajorVersion-aware, 5-step policy) |
| `RemoveMetaSoundNode` 🧩 | Remove a node by NodeId |
| `ConnectMetaSoundPins` 🧩 | Connect two pins (idempotent flag on duplicates) |
| `DisconnectMetaSoundPins` 🧩 | Disconnect a pin connection |
| `AddMetaSoundInput` 🧩 | Add an input vertex (single-page assets only) |
| `AddMetaSoundOutput` 🧩 | Add an output vertex (single-page assets only) |
| `SetMetaSoundNodeProperty` 🧩 | Set an input default (Bool / Int / Float / String, NaN / Inf rejected) |
| `CompileMetaSound` 🧩 | Register with Frontend (per-session 1 s rate limit) |

---

## UAIP.Editor.EQS 🧩

EQS query editing. Requires `EnvironmentQueryEditor` plugin.

| Command | Description |
|---|---|
| `GetEQSQueryInfo` 🧩 | EQS Generator Option / Test structure (degraded mode during PIE) |
| `GetAvailableEQSGeneratorClasses` 🧩 | List `UEnvQueryGenerator` subclasses — feed `ClassPath` to `AddEQSGenerator` |
| `GetAvailableEQSTestClasses` 🧩 | List `UEnvQueryTest` subclasses — feed `ClassPath` to `AddEQSTest` |
| `AddEQSGenerator` 🧩 | Add a Generator Option (GeneratorClass, 6-step allowlist) |
| `RemoveEQSGenerator` 🧩 | Remove a Generator Option by NodeId (cascading Test deletion) |
| `AddEQSTest` 🧩 | Add a Test to a Generator Option |
| `RemoveEQSTest` 🧩 | Remove a Test by NodeId |
| `SetEQSGeneratorProperty` 🧩 | Set a Generator property (generic ImportText_Direct) |
| `SetEQSTestProperty` 🧩 | Set a Test property (`param:<Name>` → `UAIDataProvider_QueryParams`) |

---

## UAIP.Editor.Sequencer

LevelSequence editing — tracks, sections, keyframes, playback, bindings.

### Native (123)

#### Structure (15)

| Command | Description |
|---|---|
| `AddTrack` | Add a track to a Level Sequence (TrackClass-specified) |
| `RemoveTrack` | Remove a track by TrackClass / BindingGuid |
| `AddSection` | Add a section to a track (StartFrame / EndFrame in DisplayRate) |
| `RemoveSection` | Remove a section by SectionIndex |
| `SetPlaybackRange` | Set the sequence's playback range |
| `FlushSequencerChanges` | Flush deferred change notifications |
| `GetAvailableSequencerTrackClasses` | List allowed track classes |
| `SetSectionRange` | Set a section's frame range |
| `DuplicateSection` | Duplicate a section |
| `MoveSection` | Move a section by a frame offset |
| `AddCameraCut` | Add a camera-cut section to the CameraCutTrack |
| `SetTrackEnabled` | Toggle a track's enabled state |
| `IsTrackEnabled` | Get a track's enabled state |
| `SetSectionActive` | Toggle a section's active state |
| `IsSectionActive` | Get a section's active state |

#### Keyframes (7)

| Command | Description |
|---|---|
| `AddKeyframe` | Add a keyframe to a channel |
| `RemoveKeyframe` | Remove a keyframe by FrameNumber |
| `SetKeyframeValue` | Update a keyframe's value |
| `SetKeyframeInterpolation` | Change a keyframe's interpolation mode |
| `SetKeyframeTangents` | Set a keyframe's tangents |
| `OffsetKeyframes` | Bulk-shift all keyframes on a channel by a time offset |
| `GetKeyframeTangents` | Get a keyframe's tangents (arrive / leave) |

#### Bindings (4)

| Command | Description |
|---|---|
| `BindActor` | Bind an editor-world actor as a Possessable |
| `UnbindActor` | Remove an actor binding by BindingGuid |
| `GetActorBindingGuid` | Look up BindingGuid by actor name |
| `GetBoundActors` | Get actors bound to a BindingGuid |

#### Observation (12)

| Command | Description |
|---|---|
| `GetSequenceInfo` | Track / section / channel / binding / DisplayRate / playback range |
| `GetBindings` | List Possessable bindings (GUID, name, class) |
| `GetTracks` | List tracks for a BindingGuid |
| `GetSections` | List sections (with frame range) for a track |
| `GetDisplayRate` | Get the sequence's DisplayRate |
| `GetTickResolution` | Get the sequence's TickResolution |
| `GetPlaybackRange` | Get the current playback range |
| `GetKeyframes` | Get keyframes on a channel (time, value, interp) |
| `ValidateSequenceBindings` | Validate all bindings (actor existence, type match) |
| `GetCameraCutSections` | List CameraCutTrack sections |
| `GetCurrentSequence` | Get the currently open LevelSequence |
| `GetFocusedSequence` | Get the focused Sequencer's LevelSequence |

#### Playback (10)

| Command | Description |
|---|---|
| `Play` | Start Sequencer playback |
| `Pause` | Pause playback |
| `IsPlaying` | Get the playback state |
| `SetPlayheadFrame` | Move the playhead to a frame |
| `GetPlayheadFrame` | Get the current playhead position |
| `SetPlaybackSpeed` | Set the playback speed multiplier |
| `GetPlaybackSpeed` | Get the current playback speed multiplier |
| `SetLoopMode` | Set the loop mode (NoLoop / Loop / LoopExactly) |
| `GetLoopMode` | Get the current loop mode |
| `ForceEvaluate` | Force-evaluate the current frame |

#### Section properties (4)

| Command | Description |
|---|---|
| `GetSectionProperty` | Get a UMovieSceneSection property value |
| `SetSectionProperty` | Set a UMovieSceneSection property value |
| `GetSectionWeight` | Get a section's weight |
| `SetSectionWeight` | Set a section's weight |

#### UI / state (10)

| Command | Description |
|---|---|
| `SetCameraLock` | Toggle camera lock |
| `IsCameraLockActive` | Get camera lock state |
| `GetSelectionRange` | Get the selection range |
| `SetSelectionRange` | Set the selection range |
| `ClearSelection` | Clear the selection range |
| `GetTrackFilterNames` | List available track filter names |
| `IsTrackFilterActive` | Get a filter's enabled state |
| `SetTrackFilterActive` | Toggle a filter's enabled state |
| `SetLocked` | Toggle sequence lock |
| `IsLocked` | Get the lock state |

#### Sequence properties (6)

| Command | Description |
|---|---|
| `SetDisplayRate` | Change the sequence's DisplayRate |
| `GetViewRange` | Get the Sequencer timeline view range |
| `SetViewRange` | Set the view range |
| `GetWorkRange` | Get the work range |
| `SetWorkRange` | Set the work range |
| `SetTickResolution` | Change TickResolution (warns if keyframes exist) |

#### Marked frames (5)

| Command | Description |
|---|---|
| `AddMarkedFrame` | Add a labeled marked frame |
| `GetMarkedFrames` | List all marked frames |
| `DeleteMarkedFrame` | Delete a marked frame by index |
| `DeleteAllMarkedFrames` | Delete all marked frames |
| `FindMarkedFrameByLabel` | Find a marked frame by label |

#### Sub-sequences (2)

| Command | Description |
|---|---|
| `GetSubSequences` | List SubSequence track sections |
| `AddSubSequenceTrack` | Add a SubSequence track |

#### AnimMixer (36, optional `MovieSceneAnimMixer`)

| Command | Description |
|---|---|
| `GetAnimMixerTrackInfo` | Get AnimMixer track info |
| `GetMixerLayers` | Compact summary of every AnimMixer layer for a binding |
| `GetMixerLayerCount` | Number of layers in a binding's AnimMixer track |
| `GetLayerName` | Display name of a layer |
| `SetLayerName` | Set the display name of a layer |
| `GetLayerIndex` | Zero-based index of the layer with a given display name (`NotFound` if absent) |
| `GetLayerSections` | Every animation section within a layer |
| `IsLayerEmpty` | Whether a layer holds no animation sections |
| `InsertMixerLayer` | Insert an empty layer at an index, shifting the rest down; returns the new index |
| `GetTransitionsForSection` | Transitions involving a section (`FromSectionIndex`, `ToSectionIndex`, `TransitionClass`) |
| `GetTransitionBetween` | Basic info for the transition between two section indices (`NotFound` if absent) |
| `GetTransitionInfo` | Detailed info for the transition between two sections |
| `GetTransitionName` | Display name of the transition between two sections |
| `ChangeTransitionType` | Replace a transition with one of `NewTransitionClass` (create-then-delete in one transaction) |
| `GetCompatibleDecorations` | Decoration classes compatible with a layer |
| `GetDecorations` | Existing decorations on a layer |
| `FindDecoration` | Find one decoration on a layer (`NotFound` if absent) |
| `AddDecoration` | Add (or retrieve an existing) decoration on a layer |
| `RemoveDecoration` | Remove a decoration from a layer |
| `GetLayerBlendWeight` | Get a layer's blend weight |
| `SetLayerBlendWeight` | Set a layer's blend weight |
| `IsLayerMuted` | Get a layer's mute state |
| `SetLayerMuted` | Toggle a layer's mute state |
| `IsLayerEnabled` | Get a layer's enabled state |
| `SetLayerEnabled` | Toggle a layer's enabled state |
| `ClearMixerLayer` | Clear all sections on a layer |
| `AddMixerLayer` | Add a new AnimMixer layer |
| `RemoveMixerLayer` | Remove an AnimMixer layer |
| `MoveMixerLayer` | Move an AnimMixer layer |
| `AddMixerSection` | Add an AnimMixer section |
| `RemoveMixerSection` | Remove an AnimMixer section |
| `SetMixerSectionRange` | Set an AnimMixer section's frame range (raw FFrameNumber ticks) |
| `SetMixerSectionAnimation` | Set an AnimMixer section's animation |
| `AddMixerTransition` | Add a transition |
| `RemoveMixerTransition` | Remove a transition |
| `GetMixerSectionInfo` | Get AnimMixer section info |

#### ControlRig tracks (12)

ControlRig authoring **inside a LevelSequence**. For editing a ControlRig asset itself see [`UAIP.Editor.ControlRig`](#uaipeditorcontrolrig).

| Command | Description |
|---|---|
| `GetControlRigTracks` | All ControlRig parameter tracks in a LevelSequence |
| `GetControlRigSectionInfo` | Section properties — `IsInfinite`, `StartFrame`, `EndFrame`, `IsActive`, class name |
| `FindOrCreateControlRigTrack` | Find or create a ControlRig parameter track for a binding; reports `TrackCreated` |
| `BakeToControlRig` | Bake a binding's animation onto a ControlRig track (display-rate frames, `Tolerance` 0.0–1.0) |
| `KeyControls` | Key the given controls at one display-rate frame (all visible controls when `ControlNames` is empty) |
| `KeyControlsAtFrames` | Key the given controls at multiple display-rate frames |
| `GetControlsMask` | Per-control visibility mask of a ControlRig section |
| `SetControlsMask` | Set visibility for named controls; unnamed controls keep their state |
| `ShowAllControls` | Make every control in the section visible |
| `HideAllControls` | Hide every control in the section |
| `LoadAnimIntoRig` | ⚠️ Always returns `UnsupportedOperation` — the engine API needs a `USkeletalMeshComponent*` unavailable in static asset editing. Use `Toolset.Editor.SequencerControlRig.LoadAnimIntoRig` instead |
| `GetActorTransformAtFrame` | Evaluate the sequence at a frame and return the named actor's world transform |

### Toolset bridges (61) 🧩

Provider: `Toolset.Editor.AnimationAssistant.*` (41 commands — Lifecycle 6, Playback 10, Property 9, MarkedFrame 5, UI 11) and `Toolset.Editor.SequencerAnimMixer.*` (20 commands — Layers 10, Transitions 5, Decorations 5). Requires UE 5.8+.

> A third Sequencer-module bridge provider, `Toolset.Editor.SequencerControlRig.*` (63 commands), is documented under [`UAIP.Editor.ControlRig`](#uaipeditorcontrolrig) because its commands operate on ControlRig controls.

---

## UAIP.Editor.StateTree

StateTree editing.

### Native (39)

#### State observation (8)

| Command | Description |
|---|---|
| `GetRootStates` | Top-level state descriptors (`StateId`, `Name`, `Type`, `ParentStateId`, `ChildCount`) |
| `GetStateChildren` | Direct child state descriptors of one state |
| `GetStateTasks` | Tasks of one state (class names redacted in degraded mode during PIE) |
| `GetStateTransitions` | Transitions of one state (target state IDs suppressed during PIE) |
| `GetStateEnterConditions` | Enter conditions of one state |
| `GetStateTreeGlobalTasks` | Global tasks of the asset (run regardless of the active state) |
| `GetStateTreeEvaluators` | Evaluators of the asset (run every tick to update shared data) |
| `GetStateNodeDescription` | Class path and display name of a node GUID (searches global tasks, evaluators, all states) |

#### Class / schema discovery (5)

| Command | Description |
|---|---|
| `GetAvailableTaskClasses` | Task classes (native struct + Blueprint) permitted by the active node class policy |
| `GetAvailableConditionClasses` | Condition classes (native struct + Blueprint) |
| `GetAvailableEvaluatorClasses` | Evaluator classes (native struct + Blueprint) |
| `GetAvailableStateTreeSchemaClasses` | `UStateTreeSchema` subclasses — feed `ClassPath` to `CreateAsset` as `FactoryParams.SchemaClass` |
| `GetStateTreeSchema` | Schema class path and root parameter descriptors of an asset |

#### State structure editing (4)

| Command | Description |
|---|---|
| `AddState` | Add a State (State / Group / Subtree / Linked / LinkedAsset — 5 types); returns `StateId` |
| `RemoveState` | Remove a State by `StateId` (recursive child deletion) |
| `SetStateName` | Rename a state |
| `MoveState` | Reparent / reorder a state; rejects moves that would create a cycle |

#### Task / transition / condition editing (9)

| Command | Description |
|---|---|
| `AddStateTask` | Add a Task to a State (8-step allowlist); returns `TaskId` |
| `RemoveStateTask` | Remove a Task by `TaskId` |
| `AddStateTransition` | Add a Transition (`Succeeded` / `Failed` / `NextState` / `NextSelectableState` / GUID target). `OnDelegate` is not supported |
| `RemoveStateTransition` | Remove a Transition by `TransitionId` |
| `AddStateEnterCondition` | Add an enter condition to a state; returns `ConditionId` |
| `RemoveStateEnterCondition` | Remove an enter condition by `ConditionId` |
| `SetEnterConditionProperty` | Set a property on an enter condition node |
| `GetStateNodeProperty` | Read one top-level property of a node GUID as exported text |
| `SetStateNodeProperty` | Set a Task node property (generic `ImportText_Direct`) |

#### Global task / evaluator editing (6)

| Command | Description |
|---|---|
| `AddGlobalTask` | Add a global task; returns `TaskId` |
| `RemoveGlobalTask` | Remove a global task by `TaskId` |
| `SetGlobalTaskProperty` | Set a property on a global task node |
| `AddEvaluator` | Add an evaluator; returns `EvaluatorId` |
| `RemoveEvaluator` | Remove an evaluator by `EvaluatorId` |
| `SetEvaluatorProperty` | Set a property on an evaluator node |

#### Parameters, bindings and compile (7)

| Command | Description |
|---|---|
| `GetStateTreeParameters` | Root parameter descriptors (`Name`, `ParameterType`, current serialized value) |
| `AddStateTreeParameter` | Add a root parameter (Bool / Byte / Int32 / Int64 / Float / Double / Name / String / Text) |
| `RemoveStateTreeParameter` | Remove a root parameter by name |
| `SetStateTreeParameter` | Set a root parameter value from a string-encoded value |
| `AddPropertyBinding` | Bind a source node property to a target node property |
| `RemovePropertyBinding` | Remove a property binding from a target node |
| `CompileStateTree` | Compile the StateTree (per-asset rate limit between successive calls) |

### Toolset bridges (8) 🧩

Bridge commands via the `StateTreeToolset` (UE 5.8+, Experimental). Provider: `Toolset.Editor.StateTree.*`. Observation only.

| Command | Description |
|---|---|
| `Toolset.Editor.StateTree.GetEditorData` | Editor data of a StateTree asset |
| `Toolset.Editor.StateTree.GetRootStates` | Root-level states of a StateTree asset |
| `Toolset.Editor.StateTree.GetGlobalTasks` | Global tasks of a StateTree asset |
| `Toolset.Editor.StateTree.GetEvaluators` | Evaluators of a StateTree asset |
| `Toolset.Editor.StateTree.GetChildren` | Child states of a `UStateTreeState` |
| `Toolset.Editor.StateTree.GetTasks` | Tasks of a `UStateTreeState` |
| `Toolset.Editor.StateTree.GetEnterConditions` | Enter conditions of a `UStateTreeState` |
| `Toolset.Editor.StateTree.GetTransitions` | Transitions of a `UStateTreeState` |

---

## UAIP.Editor.Curve

Curve asset key editing (UCurveFloat / UCurveVector / UCurveLinearColor).

| Command | Description |
|---|---|
| `GetCurveInfo` | Channel list, keys, pre / post extrapolation (per-channel truncated flag) |
| `AddCurveKey` | Add a key on the specified channel |
| `RemoveCurveKey` | Remove a key by time + tolerance |
| `SetCurveKeyValue` | Update an existing key's value and time |
| `SetCurveKeyInterpolation` | Change a key's interpolation mode (Constant / Linear / Cubic / None) |
| `SetCurveKeyTangent` | Set arrive / leave tangents (auto-promote non-Cubic keys with `promoted_to_cubic` flag) |

---

## UAIP.Editor.PCG 🧩

PCG graph editing. Requires `PCG` plugin.

| Command | Description |
|---|---|
| `GetPCGGraphInfo` 🧩 | UPCGGraph nodes / edges / parameters (degraded during PIE) |
| `ListPCGNodeTypes` 🧩 | UPCGSettings subclasses passing the allowlist |
| `AddPCGNode` 🧩 | Add a node by SettingsClassPath (returns NodePath) |
| `RemovePCGNode` 🧩 | Remove a node by NodePath (cascades edge removal) |
| `ConnectPCGPins` 🧩 | Connect pins by NodePath + PinLabel |
| `DisconnectPCGPins` 🧩 | Disconnect pins (specific pair or all from an output pin) |
| `SetPCGNodeProperty` 🧩 | Set a UPCGSettings EditAnywhere property (complex types rejected) |
| `ExecutePCGGraph` 🧩 | Trigger `UPCGComponent::Generate` |
| `ListCustomPCGNodeTypes` 🧩 | List C++ / Blueprint custom PCG node types |
| `GetCustomPCGNodeSchema` 🧩 | JSON schema of C++ UPCGSettings subclass EditAnywhere properties |
| `GetCustomBlueprintPCGNodeSchema` 🧩 | JSON schema of Blueprint UPCGBlueprintSettings subclass properties |
| `SetCustomCppPCGNodeProperty` 🧩 | Set a property on a C++ custom node (`RecompileTriggered` flag) |
| `SetCustomBlueprintPCGNodeProperty` 🧩 | Set a property on a BP custom node (Class CDO / per-Instance modes) |
| `CreatePCGGraph` 🧩 | Create a new UPCGGraph asset in the Content directory (requires `PCGGraphAssetCreate`) |
| `GetPCGGraphSchema` 🧩 | Return the graph's node / pin structure in schema form |
| `GetPCGGraphDescription` 🧩 | Get the graph's Description string |
| `SetPCGGraphDescription` 🧩 | Set the graph's Description (requires `PCGGraphEdit`) |
| `SetPCGGraphParams` 🧩 | Add or update graph parameters (requires `PCGGraphEdit`) |
| `RemovePCGGraphParams` 🧩 | Remove graph parameters (requires `PCGGraphEdit`) |
| `ListPCGGraphInstances` 🧩 | List UPCGComponents in the level |
| `SpawnPCGGraphInstance` 🧩 | Spawn an APCGVolume into the world (requires `PCGVolumeSpawn`) |
| `GetPCGGraphInstanceParams` 🧩 | Get per-instance override parameters |
| `SetPCGGraphInstanceParams` 🧩 | Override instance parameters (requires `PCGGraphEdit`) |
| `ResetPCGGraphInstanceParams` 🧩 | Reset instance parameters to graph defaults (requires `PCGGraphEdit`) |
| `ListPCGAvailableSubgraphs` 🧩 | List subgraph candidates in the project |
| `GetPCGNativeNodeSchema` 🧩 | JSON schema of native PCG node class EditAnywhere properties |
| `AddPCGSubgraphNode` 🧩 | Add a subgraph reference node (requires `PCGGraphEdit`) |
| `RepositionPCGNode` 🧩 | Move a node to a new position (requires `PCGGraphEdit`) |
| `AddPCGCommentBox` 🧩 | Add a comment box (requires `PCGGraphEdit`) |
| `UpdatePCGCommentBox` 🧩 | Update a comment box (requires `PCGGraphEdit`) |
| `RemovePCGCommentBox` 🧩 | Remove a comment box (requires `PCGGraphEdit`) |
| `GetPCGNodeDataView` 🧩 | Get a PCG node's execution data view (requires `PCGNodeInspect`; returns CapabilityNotAvailable when `PCG_PROFILING_ENABLED=0`) |
| `RunPCGInstantGraph` 🧩 | Fire-and-forget PCG graph execution with no actor or component required (requires `PCGGraphExecute`) |

### Toolset bridges — PCG (30) 🧩

Bridge commands via the `PCGToolset` (UE 5.8+). Provider: `Toolset.Editor.PCG.*`. Commands that require an active open PCG editor tab may return `ExecutionFailed` in non-interactive contexts (known PCGToolset constraint).

| Command | Description |
|---|---|
| `Toolset.Editor.PCG.CreateGraph` | Create a PCG graph asset (requires `PCGGraphAssetCreate`) |
| `Toolset.Editor.PCG.GetGraphStructure` | Get the full graph structure (nodes, edges, parameters) |
| `Toolset.Editor.PCG.SetGraphParams` | Set graph parameters (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.RemoveGraphParams` | Remove graph parameters (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.GetGraphSchema` | Get the graph schema |
| `Toolset.Editor.PCG.GetGraphDescription` | Get the graph description |
| `Toolset.Editor.PCG.SetGraphDescription` | Set the graph description (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.ListGraphInstances` | List volume actors referencing the graph |
| `Toolset.Editor.PCG.SpawnGraphInstance` | Spawn a PCG volume actor (requires `PCGVolumeSpawn`) |
| `Toolset.Editor.PCG.ExecuteGraphInstance` | Execute a graph on a PCG volume (requires `PCGGraphExecute`; async, 300 s default) |
| `Toolset.Editor.PCG.GetGraphInstanceParams` | Get per-instance parameter overrides |
| `Toolset.Editor.PCG.SetGraphInstanceParams` | Set per-instance overrides (requires `PCGGraphExecute`) |
| `Toolset.Editor.PCG.ResetGraphInstanceParams` | Reset per-instance overrides (requires `PCGGraphExecute`) |
| `Toolset.Editor.PCG.ListNativeNodes` | List all registered native PCG node classes |
| `Toolset.Editor.PCG.ListAvailableSubgraphs` | List PCG assets available as subgraphs |
| `Toolset.Editor.PCG.GetNativeNodeSchema` | Get the parameter schema for a native node class |
| `Toolset.Editor.PCG.AddNode` | Add a native node (requires `PCGGraphEdit` + `PCGToolsetUnsafeNodeAdd`; bypasses allowlist) |
| `Toolset.Editor.PCG.AddSubgraphNode` | Add a subgraph node (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.UpdateNode` | Update a node's properties (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.SetNodeComment` | Set a node's inline comment (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.GetNodeInfo` | Get info for a specific node |
| `Toolset.Editor.PCG.RepositionNode` | Move a node on the graph canvas (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.RemoveNode` | Remove a node (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.GetNodeDataView` | Get the last-execution data view of a node (requires `PCGNodeInspect`) |
| `Toolset.Editor.PCG.ConnectNodePins` | Connect two node pins (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.DisconnectNodePins` | Disconnect node pins (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.AddCommentBox` | Add a comment box (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.UpdateCommentBox` | Update a comment box (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.RemoveCommentBox` | Remove a comment box (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.RunPCGInstantGraph` | Execute a PCG graph instantly via `UPCGSpatialToolset` (requires `PCGGraphExecute`; async, 300 s default) |

---

## UAIP.Editor.WorldConditions 🧩

WorldConditions editing. Requires `WorldConditions` plugin.

| Command | Description |
|---|---|
| `GetWorldConditionInfo` 🧩 | Condition set structure (Operator / Depth / properties) |
| `AddWorldCondition` 🧩 | Add a condition (`InsertAtIndex=-1` appends) |
| `RemoveWorldCondition` 🧩 | Remove a condition by index |
| `SetWorldConditionProperty` 🧩 | Set a condition USTRUCT property (ImportText value string) |
| `SetWorldConditionOperator` 🧩 | Set Operator (And / Or) and bInvert (Index 0 is fixed Copy) |
| `SetWorldConditionExpressionDepth` 🧩 | Set ExpressionDepth (0–4) |
| `ListWorldConditionClasses` 🧩 | List `FWorldConditionBase`-derived classes accepted by the class policy — use to discover valid `ConditionClass` values |
| `ValidateWorldConditionQuery` 🧩 | Run `Initialize()` + `IsValid()` on a query and return `{IsValid, Errors}` (allowed during PIE) |
| `MoveWorldCondition` 🧩 | Move a condition from `SourceIndex` to `TargetIndex` (index 0 is fixed) |
| `DuplicateWorldCondition` 🧩 | Duplicate the condition at `SourceIndex` and insert the copy at `InsertIndex` |
| `ReplaceWorldCondition` 🧩 | Replace a condition's type with `NewConditionClass` defaults, preserving depth / operator / invert |
| `ClearWorldConditionQuery` 🧩 | Remove every condition, leaving an empty query |
| `SetMultipleWorldConditionProperties` 🧩 | Apply 1–32 property edits in one transaction, reporting per-edit success |

### Toolset bridges — WorldConditions (2) 🧩

Bridge commands via `WorldConditionTools` (UE 5.8+, Experimental). Provider: `Toolset.Editor.WorldConditions.*`. Input JSON is capped at 64 KiB.

| Command | Description |
|---|---|
| `Toolset.Editor.WorldConditions.GetQueryDescription` | Human-readable description of a `FWorldConditionQueryDefinition` |
| `Toolset.Editor.WorldConditions.GetConditionDescription` | Human-readable description of a single condition type |

---

## UAIP.Editor.Conversation 🧩

ConversationDB graph editing. Requires `CommonConversation` plugin.

| Command | Description |
|---|---|
| `ListConversationNodeTypes` 🧩 | List allowed node classes by position (max 256) |
| `AddConversationNode` 🧩 | Add a top-level node (`UConversationNodeWithLinks` derived) |
| `AddConversationSubNode` 🧩 | Attach a SubNode to a parent Task node |
| `RemoveConversationNode` 🧩 | Remove a node by NodeGuid |
| `ConnectConversationNodes` 🧩 | Add a transition edge between nodes |
| `DisconnectConversationNodes` 🧩 | Remove a transition edge |
| `SetConversationNodeProperty` 🧩 | Set a property (FText sanitized — BIDI strip, PUA reject, 4096 char limit) |

### Toolset bridges — Conversation (5) 🧩

Bridge commands via the `ConversationToolset` (UE 5.8+). Provider: `Toolset.Editor.Conversation.*`. These are observation-only; the native commands above cover editing.

| Command | Description |
|---|---|
| `Toolset.Editor.Conversation.ListConversationEntryPoints` | List entry point nodes in a `UConversationDatabase` |
| `Toolset.Editor.Conversation.ListConversationSpeakers` | List speakers defined in a `UConversationDatabase` |
| `Toolset.Editor.Conversation.ListConversationNodes` | List all nodes with the refPath used by the two commands below |
| `Toolset.Editor.Conversation.GetConversationNodeConnections` | Connection graph for a node identified by `NodeRefPath` |
| `Toolset.Editor.Conversation.ListConversationNodeSubNodes` | Sub-nodes (choices, requirements, side-effects) of a node |

---

## UAIP.Editor.ControlRig

ControlRig hierarchy and RigVM graph editing.

### Native (59)

#### Hierarchy observation (10)

| Command | Description |
|---|---|
| `GetElements` | List all hierarchy elements |
| `GetAllBones` | List all bones |
| `GetAllNulls` | List all Null elements |
| `GetAllControls` | List all Control elements |
| `GetGlobalTransform` | Get an element's global transform |
| `GetLocalTransform` | Get an element's local transform |
| `GetParent` | Get an element's parent |
| `GetChildren` | List an element's children |
| `GetModuleInstances` | List ModularRig module instances |
| `GetControlSettings` | Get a Control's `FRigControlSettings` (Gizmo, Limits) |

#### Hierarchy editing (11)

| Command | Description |
|---|---|
| `AddElement` | Add a generic element (ElementType-specified) |
| `AddBone` | Add a bone |
| `AddNull` | Add a Null element |
| `AddControl` | Add a Control element (ControlType allowlist) |
| `RemoveElement` | Remove an element |
| `RemoveBone` | Remove a bone |
| `RemoveNull` | Remove a Null element |
| `RemoveControl` | Remove a Control element |
| `ReparentElement` | Change an element's parent (MaintainGlobalTransform option) |
| `SetControlOffset` | Set a Control's initial local transform |
| `SetControlSettings` | Set a Control's `FRigControlSettings` |

#### Transforms (3)

| Command | Description |
|---|---|
| `SetGlobalTransform` | Set an element's global transform |
| `SetLocalTransform` | Set an element's local transform |
| `ImportBonesFromAsset` | Import bone hierarchy from a SkeletalMesh / Skeleton asset |

#### Graph management (11)

| Command | Description |
|---|---|
| `ListGraphs` | List all RigVM graphs |
| `GetGraph` | Get a graph's info |
| `AddGraph` | Add a custom graph |
| `DeleteGraph` | Delete a custom graph (built-ins rejected) |
| `GetForwardSolveGraph` | Get the ForwardSolve graph |
| `GetBackwardSolveGraph` | Get the BackwardSolve graph |
| `GetInteractionGraph` | Get the Interaction graph |
| `GetEventGraph` | Get the graph for a specified event |
| `AddEventGraph` | Add an event graph |
| `AddBackwardSolveGraph` | Add a BackwardSolve graph |
| `AddInteractionGraph` | Add an Interaction graph |

#### Nodes (10)

| Command | Description |
|---|---|
| `AddGraphNode` | Add a node to the RigVM graph (StructPath + SolveEventName) |
| `RemoveGraphNode` | Remove a node by NodeName |
| `ListNodes` | List nodes in a graph |
| `GetNodeInfo` | Get a node's StructPath, pin types, metadata |
| `FindNodes` | Search nodes by StructPath / NamePattern |
| `GetNodePosition` | Get a node's graph position |
| `SetNodePosition` | Set a node's position |
| `DuplicateNode` | Duplicate a node (returns the duplicate's name) |
| `AddEventNode` | Add an event node |
| `AddVariableNode` | Add a variable node |

#### Pins (7)

| Command | Description |
|---|---|
| `ListPins` | List a node's pins |
| `GetPinValue` | Get a pin's value |
| `SetPinValue` | Set a pin's value |
| `ResetPinValue` | Reset a pin's value to default |
| `GetConnectedPins` | Get a pin's connection info |
| `ConnectControlRigPins` | Connect two pins in the RigVM graph |
| `DisconnectControlRigPins` | Disconnect a pin connection |

#### Variables (5)

| Command | Description |
|---|---|
| `AddVariable` | Add a RigVM variable |
| `ListVariables` | List RigVM variables |
| `GetVariable` | Get a RigVM variable's value |
| `ChangeVariableType` | Change a RigVM variable's type |
| `RemoveVariable` | Remove a RigVM variable |

#### Other (2)

| Command | Description |
|---|---|
| `CompileControlRig` | Compile the ControlRig (per-session 1 s rate limit) |
| `GetAvailableRigVMUnitStructs` | List FRigUnit-derived UScriptStructs (max 1000) |

### Toolset bridges (107) 🧩

Two bridge providers, both delegating to `AnimationAssistantToolset` (UE 5.8+).

**`Toolset.Editor.ControlRig.*` (44)** — mirror of the native asset-editing commands above. Groups: asset creation (1), hierarchy observation (8), hierarchy editing (7), graph management (10), nodes (7), pins (6), variables (5).

**`Toolset.Editor.SequencerControlRig.*` (63)** — animation-time control authoring. Implemented in the Sequencer module (`SequencerControlRigTools`) but documented here because every command acts on ControlRig controls. Requires `MovieSceneAnimMixer` in addition to ControlRig. Groups:

| Group | Count | Commands |
|---|---:|---|
| Control values | 16 | `Get`/`SetFloatValue`, `BoolValue`, `IntValue`, `Vector2DValue`, `PositionValue`, `RotatorValue`, `ScaleValue`, `EulerTransformValue` |
| World transforms | 3 | `GetWorldTransform`, `SetWorldTransform`, `GetActorTransformAtFrame` |
| Layered rigs | 6 | `CollapseAnimLayers`, `IsLayeredControlRig`, `SetLayeredMode`, `Get`/`SetPriorityOrder`, `IsFKControlRig` |
| Anim layers | 6 | `GetControlRigAnimLayers`, `AddControlRigLayerFromSelection`, `Delete`/`Duplicate`/`Reorder`/`MergeControlRigAnimLayers` |
| Spaces | 4 | `Set`/`Move`/`Delete`/`BakeControlRigSpace` |
| Tweening | 3 | `TweenControlRig`, `BlendValuesOnSelected`, `SnapControlRig` |
| Mirroring | 3 | `SelectMirroredControls`, `MirrorSelectedControls`, `ZeroControlRigTransforms` |
| Selection | 4 | `GetSelectedControls`, `SelectControl`, `ClearControlSelection`, `FrameControlSelection` |
| FBX | 2 | `ExportFBXFromRig`, `ImportFBXToRig` |
| Sequencer queries | 4 | `GetSequencerControlRigs`, `GetSequencerControlsInfo`, `Get`/`SetControlRigTransformInSequencer` |
| Anim mode settings | 12 | `Get`/`Set` for `AnimModeGizmoScale`, `AnimModeHierarchy`, `AnimModeNulls`, `AnimModeHideManips`, `AnimModeOnlyRigSel`, `AnimModeLocalSpaces` |

---

## UAIP.Editor.EnhancedInput

Enhanced Input asset editing — Input Actions and Input Mapping Contexts.

| Command | Description |
|---|---|
| `ListInputActions` | List Enhanced Input Action assets in the project |
| `ListMappingContexts` | List Input Mapping Context assets in the project |
| `GetInputActionInfo` | Get an Input Action's details (ValueType, Triggers, Modifiers) |
| `GetMappingContextInfo` | Get a Mapping Context's details (entries, keys, modifiers, triggers) |
| `DeleteInputAction` | Delete an Input Action asset |
| `DeleteMappingContext` | Delete an Input Mapping Context asset |
| `AddInputMapping` | Add a key mapping to an Input Mapping Context |
| `RemoveInputMapping` | Remove a key mapping by index |
| `SetInputMappingKey` | Update a mapping's key |
| `SetInputMappingModifier` | Set / replace modifiers on a mapping |
| `SetInputMappingTrigger` | Set / replace triggers on a mapping |
| `SetInputActionModifier` | Set / replace modifiers on an Input Action |
| `SetInputActionTrigger` | Set / replace triggers on an Input Action |

---

## UAIP.Editor.GAS 🧩

Editor-time GameplayAbilities asset editing — GameplayCue tags and Cue Notify assets. Requires `GameplayAbilities` plugin (plus `GASToolsets` for the bridge variants).

### Native (8)

| Command | Description |
|---|---|
| `AddCueTag` | Add a `GameplayCue.*` tag to the project tag tables |
| `RemoveCueTag` | Remove a `GameplayCue.*` tag |
| `ListCues` | List all GameplayCue tags |
| `GetCueInfo` | Get a GameplayCue tag's details and registered Cue Notify assets |
| `FindCueNotifyAssets` | Find Cue Notify assets that handle a tag |
| `FindCueTagsWithoutNotifies` | Find GameplayCue tags that have no associated Notify asset |
| `CreateCueNotifyAsset` | Create a new GameplayCueNotify asset (Actor / Static / Burst) |
| `ExecuteCueOnSelectedActor` | Execute a GameplayCue on the currently selected actor (testing convenience) |

### Toolset bridges (14) 🧩

Mirror of native commands via the `GASToolsets` plugin (UE 5.8+). Provider: `Toolset.Editor.GAS.*`. Groups: runtime inspection (6) — `GetAttributeValues`, `GetActiveEffects`, `GetGrantedAbilities`, `GetActiveTags`, `FindAttributeSetClasses`, `ListAttributes`; GameplayCue authoring (8) — `ListCues`, `GetCueInfo`, `FindCueNotifyAssets`, `FindCueTagsWithoutNotifies`, `ExecuteCueOnSelectedActor`, `CreateCueNotifyAsset`, `AddCueTag`, `RemoveCueTag`.

---

## UAIP.Editor.Python 🧩

Python command extension. Requires `PythonScriptPlugin`.

| Command | Description |
|---|---|
| `ReloadPythonCommands` 🧩 | Rescan the commands directory and update existing handler descriptors in-place |
| *(dynamic commands)* 🧩 | Commands registered via the `@uaip_command` decorator (names depend on user scripts) |

---

## UAIP.Editor.Sandbox 🧩

Sandbox session lifecycle management. Requires the `FileSandbox` plugin. When `FileSandbox` is not enabled all commands in this section return `CommandNotFound`.

| Command | Description |
|---|---|
| `GetSandboxStatus` 🧩 | Query the current sandbox status — `Active`, `IsStale`, `SessionId`, and `OwnerUAIPSessionId` |
| `GetSandboxChanges` 🧩 | List pending changes inside the active sandbox — `FilePath`, `ChangeKind` (Added / Edited / Removed), `SizeBytes`, and `TotalCount` |
| `BeginSandboxSession` 🧩 | Open a new FileSandbox session; subsequent asset writes are redirected to the sandbox |
| `EndSandboxSession` 🧩 | End the active sandbox session; uncommitted changes are reverted automatically |
| `CommitSandboxChanges` 🧩 | Flush selected (or all) pending sandbox changes to disk; returns `CommittedFiles`, `SkippedFiles`, and `CommittedCount` |
| `RevertSandboxChanges` 🧩 | Discard all pending sandbox changes without committing |

---

## UAIP.Editor.WorldPartition

World Partition, Data Layer, and HLOD management for partitioned worlds (requires `WorldPartition` plugin). All commands in this section return `CommandNotFound` when the project does not have World Partition enabled.

### World Partition (12)

| Command | Description |
|---|---|
| `GetWorldPartitionInfo` | Get World Partition configuration — streaming mode, runtime hash class, and whether WP is enabled for the current level |
| `GetWorldPartitionStreamingGrids` | List runtime streaming grids defined in the World Partition settings |
| `GetRuntimeGridSettings` | Get the settings for a specific runtime grid by name |
| `SetRuntimeGridSettings` | Set the settings for a specific runtime grid (requires `WorldPartitionEdit`) |
| `GetActorWorldPartitionSettings` | Get the World Partition settings for an actor — HLOD Layer, spatially loaded flag, and runtime grid name |
| `SetActorIsSpatiallyLoaded` | Set whether an actor is spatially loaded in World Partition (requires `WorldPartitionEdit`) |
| `SetActorRuntimeGrid` | Assign an actor to a specific runtime streaming grid (requires `WorldPartitionEdit`) |
| `SetWorldPartitionStreamingEnabled` | Enable or disable World Partition streaming for the current level (requires `WorldPartitionEdit`) |
| `PinActorInWorldPartition` | Pin an actor so it is always loaded regardless of streaming state (requires `WorldPartitionEdit`) |
| `UnpinActorFromWorldPartition` | Remove the always-loaded pin from an actor (requires `WorldPartitionEdit`) |
| `DumpWorldPartitionCells` | Dump the current World Partition streaming cell grid as a JSON artifact |
| `ListExternalActors` | List actors stored as external packages (World Partition external actor workflow) |

### Data Layer (15)

| Command | Description |
|---|---|
| `ListDataLayers` | List all Data Layer instances in the current level |
| `GetDataLayerInfo` | Get detailed info for a Data Layer instance — type, runtime state, visibility, and parent hierarchy |
| `CreateDataLayerAsset` | Create a new Data Layer asset in the Content Browser (requires `DataLayerEdit`) |
| `DeleteDataLayerAsset` | Delete a Data Layer asset (requires `DataLayerEdit`) |
| `CreateDataLayerInstance` | Create a new Data Layer instance in the current level from a Data Layer asset (requires `DataLayerEdit`) |
| `DeleteDataLayerInstance` | Delete a Data Layer instance from the current level (requires `DataLayerEdit`) |
| `SetDataLayerType` | Set the type of a Data Layer instance — Editor or Runtime (requires `DataLayerEdit`) |
| `SetDataLayerInitialRuntimeState` | Set the initial runtime state of a Data Layer — Unloaded, Loaded, or Activated (requires `DataLayerEdit`) |
| `SetDataLayerIsLoadedInEditor` | Set whether a Data Layer is loaded in the editor viewport (requires `DataLayerEdit`) |
| `SetDataLayerVisibility` | Set the visibility of a Data Layer in the editor (requires `DataLayerEdit`) |
| `SetParentDataLayerInstance` | Set the parent Data Layer instance, building a hierarchy (max 64 levels; requires `DataLayerEdit`) |
| `GetActorDataLayers` | Get the Data Layer instances assigned to an actor |
| `AddActorToDataLayer` | Add an actor to a Data Layer instance (requires `DataLayerEdit`) |
| `RemoveActorFromDataLayer` | Remove an actor from a Data Layer instance (requires `DataLayerEdit`) |
| `GetActorsInDataLayer` | List all actors assigned to a specific Data Layer instance |

### HLOD (7)

| Command | Description |
|---|---|
| `ListHLODLayers` | List all HLOD Layer assets in the project |
| `CreateHLODLayer` | Create a new HLOD Layer asset under `/Game/` (requires `HLODBuild`) |
| `DeleteHLODs` | Delete built HLOD data for a specified HLOD Layer (requires `HLODBuild`) |
| `SetActorHLODLayer` | Assign an actor to an HLOD Layer asset (requires `HLODBuild`) |
| `BuildHLODs` | Start an HLOD build job for the current world; returns `HLODBuildJobId` (requires `HLODBuild`) |
| `CancelHLODBuild` | Cancel an in-progress HLOD build job by job ID (requires `HLODBuild`) |
| `GetHLODBuildStatus` | Get the current status of an HLOD build job — running, completed, or not found |

---

## UAIP.Editor.Foliage

Foliage type management and instance placement in the editor. Observation commands run during PIE; edit commands require the editor to be stopped (not in PIE or SIE).

### Foliage Observation (4)

| Command | Description |
|---|---|
| `ListFoliageTypes` | List all foliage types registered in the current level's `AInstancedFoliageActor` with instance counts |
| `GetFoliageTypeInfo` | Get detailed settings for a foliage type — mesh path, density, scale range, cull distances, normal alignment, slope angle, and instance count |
| `GetFoliageInstanceCount` | Get the total placed instance count; optionally filtered to a single foliage type with a per-type breakdown |
| `GetFoliageInstances` | List placed instances for a foliage type within a bounding box — returns location, rotation, and scale |

### Foliage Type Management (3)

| Command | Description |
|---|---|
| `AddFoliageTypeToLevel` | Register a foliage type asset with the current level's `AInstancedFoliageActor` (requires `FoliageTypeEdit`) |
| `RemoveFoliageTypeFromLevel` | Unregister a foliage type and delete all its instances from the current level (requires `FoliageTypeEdit`) |
| `SetFoliageTypeSettings` | Update foliage type settings — density, scale range, cull distances, normal alignment, slope angle, and mesh (ISM types only) (requires `FoliageTypeEdit`) |

### Foliage Instance Control (4)

| Command | Description |
|---|---|
| `AddFoliageInstances` | Place foliage instances at the specified transforms. World Partition aware — routes each instance to the correct `AInstancedFoliageActor` cell (requires `FoliageInstanceEdit`) |
| `RemoveFoliageInstances` | Remove foliage instances inside a bounding box or sphere up to `MaxRemoveCount` (requires `FoliageInstanceEdit`) |
| `DeleteAllFoliageInstances` | Delete every placed instance of a foliage type from the current level (requires `FoliageBulkDelete`) |
| `ResimulateProceduralFoliage` 🧩 | Resimulate a `ProceduralFoliageVolume` and place the resulting instances (requires `ProceduralFoliage` plugin and `FoliageInstanceEdit`) |

---

## UAIP.Editor.DataRegistry 🧩

Editor-time observation of UE 5.8 Data Registries — listing, schema inspection, and cached item retrieval with secret-field masking. Requires the `DataRegistry` plugin (plus `DataRegistryToolset` + `ToolsetRegistry` for the bridge variants).

### Native (9)

| Command | Description |
|---|---|
| `ListRegistries` | List all registered Data Registries, optionally filtered by item struct name (`StructFilter`); includes `IsDataRegistrySystemEnabled` / `AreRegistriesInitialized` diagnostics |
| `GetRegistryInfo` | Get item count, lowest source availability, description, and ID format for a registry |
| `GetSchema` | Get the item struct's property schema — name, type, and `IsSecret` flag per property |
| `ListItems` | List registered item IDs for a registry (not necessarily cached) |
| `ListDataSources` | List editor-time defined data sources for a registry |
| `ListRuntimeSources` | List runtime-expanded data sources for a registry |
| `GetItems` | Read cached items by name with secret-field masking; items not yet cached are reported in `MissingItems` with a reason instead of being silently dropped |
| `GetAllCachedItems` | Read every currently cached item without naming items in advance (bounded to 1000 items / 1 MiB; no Toolset equivalent) |
| `AcquireItems` | Trigger an asynchronous cache load for the given items — needed for custom/Remote sources; DataTable sources precache automatically (no Toolset equivalent) |

### Toolset bridges (7) 🧩

Mirror of the first 7 native commands via the `DataRegistryToolset` plugin (UE 5.8+). Provider: `Toolset.Editor.DataRegistry.*`. `GetItems` behaves differently here: missing items are silently omitted and no secret masking is applied — use the native `GetItems` when either matters.

| Command | Description |
|---|---|
| `Toolset.Editor.DataRegistry.ListRegistries` | Passthrough to `DataRegistryToolset` |
| `Toolset.Editor.DataRegistry.GetRegistryInfo` | Passthrough to `DataRegistryToolset` |
| `Toolset.Editor.DataRegistry.GetSchema` | Passthrough to `DataRegistryToolset` (raw JSON string, no `IsSecret` flag) |
| `Toolset.Editor.DataRegistry.ListItems` | Passthrough to `DataRegistryToolset` |
| `Toolset.Editor.DataRegistry.ListDataSources` | Passthrough to `DataRegistryToolset` |
| `Toolset.Editor.DataRegistry.ListRuntimeSources` | Passthrough to `DataRegistryToolset` |
| `Toolset.Editor.DataRegistry.GetItems` | Passthrough to `DataRegistryToolset`; missing items silently omitted, no masking |

---

## UAIP.Runtime.Engine.Log

Log verbosity inspection and log category listing at runtime. These are the Runtime-domain counterparts to `UAIP.Editor.Engine.Log`.

| Command | Description |
|---|---|
| 🆓 `GetLogVerbosity` | Get the current verbosity level of a log category |
| 🆓 `GetLogCategories` | List all registered log category names |
| `SetLogVerbosity` | Set the verbosity level of a log category (requires `LogVerbosityEdit`) |

---

## UAIP.Runtime.Engine.Plugin

Plugin inspection at runtime. Read-only commands available without any special capability. These are the Runtime-domain counterparts to `UAIP.Editor.Engine.Plugin` commands.

| Command | Description |
|---|---|
| 🆓 `ListPlugins` | List discovered or enabled plugins with optional `EnabledOnly` filter and `LoadedFrom` filter |
| 🆓 `GetPluginInfo` | Get detailed info for a plugin (11 fields: Name, FriendlyName, Version, Description, Category, IsEnabled, IsMounted, Type, BaseDir, LoadedFrom, Dependencies) |
| 🆓 `IsEnabled` | Check whether a plugin is currently enabled (note: `.uproject` declaration and actual load state may diverge until restart) |
| 🆓 `GetPluginDependencies` | Get the direct plugin dependencies declared by a plugin |
| 🆓 `GetPluginForAsset` | Resolve the owning plugin for a given asset path |

---

## UAIP.Runtime.Engine.CVar

Read and write engine-wide console variables (CVars). CVars are global engine state — independent of any World or PIE session. Sensitive CVars are automatically excluded.

🔒 requires `RuntimeCVarRead` (DefaultDenied). ✏️ requires `RuntimeCVarWrite` (DefaultDenied). The demo distribution's `Config/DefaultUAIP.ini` pre-grants `RuntimeCVarRead`, so the 🆓 commands below work out of the box in the demo.

| Command | Description |
|---|---|
| 🆓🔒 `GetConsoleVariable` | Get the name, current value, type, and help text for a CVar (sensitive names return `NotFound`) |
| 🆓🔒 `SearchConsoleVariables` | Search CVars using a wildcard (`*`) pattern (default 50 results, max 200) |
| ✏️ `SetConsoleVariable` | Set the value of a CVar (sensitive names and `ECVF_ReadOnly` CVars are rejected; `ECVF_Cheat` CVars are rejected unless `AllowCheatCVarWrite` is enabled) |
| ✏️ `ResetConsoleVariable` | Reset a CVar to its default value (sensitive names and `ECVF_ReadOnly` CVars are rejected; `ECVF_Cheat` CVars are rejected unless `AllowCheatCVarWrite` is enabled) |

> **Note**: The legacy `GetConsoleVariable` and `SearchConsoleVariables` commands under `UAIP.Runtime.PIE` are deprecated and will be removed in v1.2. Use these commands instead.

---

## UAIP.Runtime.Engine.Config

Raw ini key access for runtime and packaged builds. Reads and writes ini keys directly without going through `ISettingsModule`. Write commands are blocked in packaged builds.

| Command | Description |
|---|---|
| 🆓 `GetConfigValue` | Read the string value of an ini key given section and key name. No capability required |
| `SetConfigValue` | Write or delete a raw ini key. Requires `ConfigSettingsEdit`. Blocked in packaged builds. Rejects ini injection characters (`[`, `]`) in key and value fields |

---

## UAIP.Runtime.PIE

PIE session lifecycle. Manipulating the running world is [`UAIP.Runtime.World`](#uaipruntimeworld).

| Command | Description |
|---|---|
| 🆓 `StartPIE` | Start a Play-in-Editor session |
| 🆓 `StopPIE` | Stop the active PIE session |
| 🆓 `PausePIE` | Pause the active PIE session |
| 🆓 `ResumePIE` | Resume a paused PIE session |
| 🆓 `LoadMap` | Load a map in the active PIE session and wait for completion |
| 🆓 `GetPIEState` | Return the current PIE state — `Running`, `Stopped`, `Paused`, or `Simulating` |

### Toolset bridges (3) 🧩

Bridge commands via the `EditorAppToolset` (UE 5.8+, EditorToolset plugin). Provider: `Toolset.Editor.Toolset.PIE.*`.

| Command | Description |
|---|---|
| `Toolset.Editor.Toolset.PIE.StartPIE` | Start a PIE session (async, requires `PIEControl`) |
| `Toolset.Editor.Toolset.PIE.StopPIE` | Stop the active PIE session (async, requires `PIEControl`) |
| `Toolset.Editor.Toolset.PIE.IsPIERunning` | Return whether PIE is currently active |

---

## UAIP.Runtime.World

Manipulate and inspect the **running** game world. These commands were registered under `UAIP.Runtime.PIE` in earlier releases.

| Command | Description |
|---|---|
| `SpawnActor` | Spawn an actor of a class in the active PIE world (requires `RuntimeActorManipulation`) |
| `DestroyActor` | Destroy an actor in the active PIE world (requires `RuntimeActorManipulation`) |
| `TeleportActor` | Teleport an actor to a world-space location / rotation |
| `PossessActor` | Have a player controller possess an actor |
| `SetTimeScale` | Set the global time dilation of the active game world |
| `QuitGame` | Request a graceful quit of the running game process |
| `ExecuteConsoleCommand` | Execute a console command in the active game world (requires `RuntimeExecCommand`) |
| `GetConsoleVariable` | Value, type and help text of a console variable; sensitive names report as not found (requires `RuntimeCVarRead`) |
| `SearchConsoleVariables` | Wildcard (`*`) search over registered console variables — `MaxResults` default 50, max 200; sensitive names are excluded |

### Toolset bridges (1) 🧩

Bridge command via the `EditorAppToolset` (UE 5.8+, EditorToolset plugin). Provider: `Toolset.Editor.Toolset.World.*`.

| Command | Description |
|---|---|
| `Toolset.Editor.Toolset.World.SearchCVars` | Search console variables by name substring; sensitive variables are excluded (requires `CVarInspect`) |

---

## UAIP.Runtime.Observation

Runtime captures and state dumps.

| Command | Description |
|---|---|
| 🆓 `CaptureViewportImage` | PNG screenshot of a specified player's game viewport |
| 🆓 `DumpWorldState` | Snapshot of all actors / components in the active PIE world (JSON) |
| 🆓 `DumpActorState` | State of a specified actor (optionally including components) |
| 🆓 `DumpComponentState` | State of a specified actor component |
| 🆓 `DumpRuntimeLog` | Buffered runtime log as a text artifact |
| 🆓 `CapturePerformanceSnapshot` | CPU / GPU performance snapshot (FPS, memory, draw calls) |
| 🆓 `CheckpointCapture` | Combined screenshot + state dump (scenario primitive) |
| 🆓 `SearchLoadedClasses` | Search loaded classes (used for runtime introspection) |

---

## UAIP.Runtime.Execution

Test execution in PIE / Standalone.

| Command | Description |
|---|---|
| `RunFunctionalTest` | Run an `AFunctionalTest` actor by asset path and return a JSON report |
| `RunRuntimeAutomationTest` | Run a UE Automation Test in PIE context |
| `RunGauntletTest` | Launch a Gauntlet test as an external process via RunUAT |

---

## UAIP.Runtime.Assertion

Scenario primitives — wait and assert.

| Command | Description |
|---|---|
| 🆓 `WaitSeconds` | Wait the specified number of seconds (scenario primitive) |
| 🆓 `WaitForCondition` | Poll a condition until it becomes true |
| 🆓 `AssertActorProperty` | Assert that an actor property equals an expected value |
| 🆓 `AssertWorldState` | Batch-assert multiple properties in one call |

---

## UAIP.Runtime.GAS 🧩

GameplayAbilities state inspection and runtime manipulation. Requires the `GameplayAbilities` plugin. PIE is required except where noted.

#### Inspection (8)

| Command | Description |
|---|---|
| `GetAttributeValues` 🧩 | All AttributeSet attribute values (currentValue / baseValue) for an actor |
| `GetActiveEffects` 🧩 | Active gameplay effects (Level, StackCount, remaining time) on an actor |
| `GetGrantedAbilities` 🧩 | Granted abilities (Class, IsActive, ActiveCount, InputID) on an actor |
| `GetActiveTags` 🧩 | Owned GameplayTags on an actor |
| `FindAttributeSetClasses` 🧩 | Scan PIE world actors and list `UAttributeSet` classes (MaxActors limit) |
| `ListAttributes` 🧩 | List all attribute names defined on an AttributeSet class |
| `GetAbilityAssetInfo` 🧩 | CDO-level metadata for a `UGameplayAbility` class — cost, cooldown, tags. **No PIE required** |
| `GetEffectAssetInfo` 🧩 | CDO-level metadata for a `UGameplayEffect` class — duration policy, modifiers, granted tags. **No PIE required** |

#### Manipulation (9)

All require the `RuntimeGASManipulation` capability and an active PIE session.

| Command | Description |
|---|---|
| `GrantAbility` 🧩 | Grant a GameplayAbility to an actor's AbilitySystemComponent |
| `RemoveAbility` 🧩 | Remove a previously granted GameplayAbility |
| `ClearGrantedAbilities` 🧩 | Remove every granted GameplayAbility from an actor |
| `ApplyEffect` 🧩 | Apply a GameplayEffect to an actor |
| `RemoveEffect` 🧩 | Remove all active instances of a GameplayEffect class |
| `ClearActiveEffects` 🧩 | Remove all active GameplayEffects, optionally narrowed by `TagFilter` |
| `SetAttributeValue` 🧩 | Set an attribute's base value (`AttributeName` format `UMyAttributeSet.Health`) |
| `ResetAttributesToBase` 🧩 | Reset every attribute's current value to its base value |
| `SendGameplayEvent` 🧩 | Send a GameplayEvent with an optional magnitude to an actor |

---

## UAIP.Runtime.Input

Runtime input injection and Enhanced Input state inspection. PIE required.

| Command | Description |
|---|---|
| `InjectInputKey` | Inject a raw key press / release into the active PIE viewport |
| `InjectEnhancedInputAction` | Fire an Enhanced Input Action with a value (Bool / Axis1D / Axis2D / Axis3D) |
| `InjectLegacyAction` | Inject a legacy action mapping event |
| `InjectLegacyAxisInput` | Inject a legacy axis input |
| `InjectLegacySpeechInput` | Inject a legacy speech input |
| `AddMappingContext` | Add an Input Mapping Context to the local player |
| `RemoveMappingContext` | Remove an Input Mapping Context from the local player |
| `SetInputMode` | Set the input mode (GameOnly / UIOnly / GameAndUI) |
| `FlushInput` | Flush pressed-key state at the end of a test |
| `DumpInputState` | Dump current Enhanced Input state (active contexts, mappings, action values) |
| `GetEnhancedInputActionValue` | Get the current value of an Enhanced Input Action |

---

## UAIP.Runtime.Niagara 🧩

Runtime inspection and parameter override for Niagara components in PIE. Requires `Niagara` plugin.

### Native (4)

| Command | Description |
|---|---|
| `GetUserVariables` 🧩 | Get user-exposed variables on a Niagara System Component |
| `GetVariable` 🧩 | Get a specific user variable value |
| `SetVariable` 🧩 | Set a user variable value at runtime |
| `SetSystem` 🧩 | Replace the Niagara System asset on a component at runtime |

### Toolset bridges (4) 🧩

Provider: `Toolset.Runtime.Niagara.*`. Requires UE 5.8+ and `NiagaraToolsets`. Mirrors the native commands above.

---

## UAIP.Runtime.Insights.Trace

Unreal Insights trace capture control. A trace is always written to a file under `Saved/Profiling/UAIP/` — **no command in this module can send a trace to a network destination**. A trace UAIP did not start is never modified: `GetTraceStatus` reports that something else is recording, and every control command except `StopTrace` (which refuses it explicitly) leaves it alone.

The three read-only commands require `RuntimeInsightsInspect` (DefaultAllow). The eight control commands require `RuntimeInsightsControl` (DefaultDenied). Attaching the captured `.utrace` file additionally requires `RuntimeInsightsAttachTraceFile` (DefaultDenied) — see [Safety & Capabilities](safety.md#runtime-insights-trace-capture).

Trace recording is independent of the PIE lifecycle: starting or stopping PIE neither starts nor stops a trace, and a trace keeps recording across PIE sessions.

### Read-only (3)

| Command | Description |
|---|---|
| 🆓 `ListTraceChannels` | List every trace channel this build knows about — description, whether it is currently enabled, whether it can still be toggled, and what it can disclose. Also lists the engine's channel presets, each expanded into its channels and their disclosure classes. Most engine presets include the log channel, so check the expanded classes before passing a preset to `StartTrace` |
| 🆓 `GetTraceStatus` | Report whether the engine is recording, whether recording is suspended, and whether the running trace is one UAIP started. For a UAIP-started trace also reports its label, file name, channels, disclosure classes, elapsed time, file size and self-stop limits. For a trace UAIP did not start, only the kind of activity is reported — the destination, channel set, elapsed time and size are withheld. Elapsed time and size are refreshed once per monitoring interval and can be up to one interval old |
| 🆓 `ListTraceFiles` | List the trace files UAIP captured, newest first, with label, size and the UTC timestamp encoded into the name (`MaxCount` default 50, max 500). A `FileName` from this listing is what `AnalyzeTrace` accepts. When the safety policy enables external trace analysis, `.utrace` files in the configured external directory are listed as well with `Source: External`. Listing never deletes anything — rotation happens when a trace starts |

### Trace control (8)

| Command | Description |
|---|---|
| `StartTrace` | Start recording into UAIP's own trace directory with the given channels or channel presets enabled, and return the file name being written to. `Channels` is required; `Label`, `MaxDurationSeconds` (default 300, range 1–3600) and `MaxFileSizeMB` (default 512, range 1–4096) are optional. A trace UAIP already started is never restarted — the request only adds channels and reports `AlreadyRunning` / `LimitsIgnored`. Rejected with `PolicyViolation` when the *effective* channel set (already enabled ∪ requested) records log text and `AllowLogDump` is false; no channel is ever turned off to make a request pass. When that same set carries something the policy will not let the raw file be handed over for, `Warnings` reports `AttachDisabledByPolicy` naming the channels and the setting, so a capture that is meant to be taken away is not started for nothing. Both limits are checked once per second, so the size limit is not a strict ceiling |
| `StopTrace` | Stop the trace UAIP started and, when `AttachTraceFile` is true, hand the captured `.utrace` over as an artifact. Stopping always succeeds — nothing recording is a successful no-op, a second stop issued right after a first one is the same no-op even though the engine still reports the connection as live while it tears the trace down, and a file that cannot be handed over is skipped with an `AttachSkippedReason` while the stop itself still succeeds. A trace UAIP did not start is never stopped (`NotAllowed`). ⚠️ Attaching the file always discloses the process command line whatever the channel set was. Attaching is refused for a channel set that was mutated while recording, for an unclassified channel, and for a file larger than 64 MB; a set carrying log text needs `AllowLogDump`, and one carrying host paths, screen content or network addresses needs `AllowDisclosingTraceAttachment` (in the editor both are normally required, because the engine enables the log and screenshot channels by itself). Stopping does not close the captured file on its own — the engine's trace writer finishes that on its own thread a moment later — so a request that asks for the file waits up to three seconds for it and reports `AttachSkippedReason: "TraceFileStillOpen"` if it is still being written by then, which is worth asking for again in a moment. A request that did not ask for the file never waits |
| `PauseTrace` | Suspend recording of the trace this module started without stopping it. Idempotent (`WasPaused: false` when already paused), a no-op success when nothing UAIP started is running, and `NotAllowed` for a trace UAIP did not start. The channel monitor keeps running while paused, and the duration limit only counts seconds actually spent recording |
| `ResumeTrace` | Restore recording after `PauseTrace`. Idempotent (`WasResumed: false` when not paused) and `NotAllowed` for a trace UAIP did not start. The engine has a known defect where resuming can fail to restore a channel whose name does not end in `Channel`; such a channel is reported in `Warnings` as `ChannelNotRestoredAfterResume` so it can be re-enabled with `SetTraceChannels` |
| `SetTraceChannels` | Enable and disable channels on the trace this module started while it keeps recording. At least one of `EnableChannels` / `DisableChannels` must be non-empty. `NotAllowed` when no trace is running or the running trace was not started by UAIP, because channel state outlives the trace. The request is judged by the channel set it would leave in effect, so turning a disclosing channel off is never itself rejected. ⚠️ Using this command marks the trace's channel set as externally mutated, which makes `StopTrace` refuse to attach the file |
| `AddTraceBookmark` | Write a point-in-time bookmark (`Text`) into the trace that is recording right now. When the bookmark channel is disabled — which includes every moment nothing is recording — nothing is written and the command still succeeds with `Written: false`. Rejected with `PolicyViolation` when `AllowLogDump` is false, because the text is read back under the same policy that gates log text. Absolute paths in the text are replaced with portable placeholders |
| `BeginTraceRegion` | Open a named span (`Name`, optional `Category`) in the running trace and return the `RegionId` that closes it. Regions are matched by id, never by name, so nested regions and same-named regions stay apart. A `RegionId` is returned even when the region channel is disabled (`Written: false`). Any span still open is closed automatically when the trace stops or the module shuts down. Gated by `AllowLogDump` the same way `AddTraceBookmark` is |
| `EndTraceRegion` | Close the region `BeginTraceRegion` opened, matched by `RegionId` (`NotFound` for an id that names no open region, including one already closed by the automatic sweep). `DurationSeconds` is measured in-process and is reported even when the region channel was disabled. Never rejected by the log dump policy — it carries no text of its own |

---

## UAIP.Runtime.Insights.Analysis

Offline analysis of a captured `.utrace` file. This provider is only registered in builds where trace analysis is supported; elsewhere (including the demo build) the commands are absent and return `CommandNotFound` rather than failing on every call.

All three commands require `RuntimeInsightsAnalyze` (DefaultDenied) — including the status command, because the progress of an analysis is of no use to a caller that may not analyse a trace.

Analysis is asynchronous: call `AnalyzeTrace` to get an `AnalysisId`, poll `GetTraceAnalysisStatus` until `State` is `Completed`, then read `GetTraceAnalysisResult`. Only one run is ever under way — a request that arrives while another run is parsing or extracting is rejected with `TooManyRequests`, and the error message names the `AnalysisId` of the run holding the slot, so it can be watched through `GetTraceAnalysisStatus` instead of blind-polling. There is no way to cancel a run. A finished run does not hold the slot: it stays readable for its time to live and does not stop the next run from starting.

| Command | Description |
|---|---|
| `AnalyzeTrace` | Start analysing a trace file and return the `AnalysisId`. `FileName` must be a name `ListTraceFiles` reported (not a path); a trace captured outside UAIP is analysed by passing `ExternalTracePath` instead, which requires the external-analysis policy. Optional `Sections`, `StartTimeSeconds` / `EndTimeSeconds`, `TopN` (default 32), `MaxSeries` (default 256), `MaxSamplesPerSeries` (default 1024), `NameFilter`, `HitchThresholdMs` (default 33.3). A trace larger than 512 MB is rejected. Each requested section is written out as its own JSON artifact as it finishes, which is why the command is not read-only. A section whose channel was not recorded, or whose content the safety policy withholds, is reported as unavailable with a reason rather than failing the run |
| `GetTraceAnalysisStatus` | Report how far one run has got — `Running` (parsing), `Extracting`, `Completed` or `Failed` — with elapsed time, `CompletedSections`, `AvailableSections` and `UnavailableSections` (each with its reason). `FailureReason` is one of a fixed set of values and is only meaningful once `State` is `Failed`; what the analysis engine itself reported goes to the output log instead, because those messages can carry absolute paths. Read-only |
| `GetTraceAnalysisResult` | Return the artifacts a finished run produced, one per section, with `TotalCount` / `ReturnedCount` per section and `Truncated` when any of them hit a limit. Only a run whose `State` is `Completed` can be read. The command hands back references and reads nothing, so pick only the sections worth fetching; a section the original `AnalyzeTrace` call did not request is rejected rather than analysed now. Reading a result restarts the time the run is kept for (15 minutes per read, one hour absolute) |

Section names accepted by `Sections`: `Frames`, `Counters`, `Timers`, `Threads`, `StackSamples`, `LoadTime`, `Memory`, `Allocations`, `Tasks`, `FileActivity`, `NetProfiler`, `CsvProfiler`, `ContextSwitches`, `CookProfiler`, `Bookmarks`, `Regions`, `Diagnostics`, `Channels`, `Log`, `Screenshots`, and `Objects` (UE 5.8+ only — the underlying provider does not exist on UE 5.7).

Three per-section details worth knowing before reading a result:

- **`Frames`** counts only frames that both began and ended. A capture stops in the middle of a frame, so the last frame of each frame type is almost always still open and has no duration to report; such a frame is left out of the statistics and out of `TotalCount` alike. `TotalCount` and `ReturnedCount` therefore differ only when a time window was requested, and this section never truncates.
- **`Screenshots`** reports metadata only — the identifier, name, time, width and height of each screenshot, alongside `ImageDataIncluded: false` — and never the encoded image bytes. No image ever arrives from it, so there is nothing to wait for beyond that metadata.
- **`Diagnostics`** omits its `EngineVersion` key on UE 5.7. That version's trace format does not carry an engine version at all, so the key is left out rather than reported as an empty string, which would be indistinguishable from a capture that genuinely recorded none.

---

## Scenario execution route

Scenarios are not a single command — they are a separate route that submits an ordered list of commands as one request. See [Scenario Execution](scenario.md). Available entry points:

| Transport | Entry point |
|---|---|
| MCP | `uaip_run_scenario` |
| HTTP | `POST /uaip/scenarios` (requires `-uaip-enable-scenario`) |
| WebSocket | Frame `Type: "ScenarioRequest"` |
| CLI | `-uaip-scenario=<json>` / `-uaip-scenario-file=<path>` |

Any step in a scenario is dispatched through the same `CommandDispatcher` as `uaip_execute`, so the same Capability + SafetyPolicy rules apply.

---

> Schemas and parameter details are intentionally omitted from this page. Use `uaip_describe_command(CommandName="...")` to get the full schema for any command.

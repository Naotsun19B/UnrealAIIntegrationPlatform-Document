**[日本語](../ja/commands.md)** | [Back to README](../../README.md)

# Commands Reference

UAIP exposes 632+ **UAIP commands** (provided directly by the plugin itself) and 260+ **Toolset bridge commands** (delegating to the UE 5.8 official Toolset framework), for a combined total of about 892+ commands organized by domain. Each command name is fully-qualified — e.g. `UAIP.Editor.Observation.CaptureActiveWindowImage`. This page omits the provider prefix in the tables; the section header tells you what to prepend.

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
| Core | `UAIP.Core` | 7 | — | ✅ |
| Editor Workspace | `UAIP.Editor.Workspace` | 18 | — | partial (13/18) |
| Editor Engine Log | `UAIP.Editor.Engine.Log` | 3 | 4 | — |
| Editor Engine Plugin | `UAIP.Editor.Engine.Plugin` | 9 | 15 | — |
| Editor Engine CVar 🧩 | `Toolset.Editor.EngineManagement` | — | 1 | — |
| Editor Engine ConfigSettings | `UAIP.Editor.Engine.ConfigSettings` | 8 | — | — |
| Editor Observation | `UAIP.Editor.Observation` | 15 | — | ✅ (1 excluded) |
| Editor Execution | `UAIP.Editor.Execution` | 5 | — | — |
| Editor UI Automation | `UAIP.Editor.UIAutomation` | 15 | — | ✅ |
| Editor Assets | `UAIP.Editor.Assets` | 17 | 6 | — |
| Editor SemanticSearch 🧩 | `UAIP.Editor.SemanticSearch` | 5 | 2 | — |
| Editor Level | `UAIP.Editor.Level` | 16 | 8 | — |
| Editor Property | `UAIP.Editor.Property` | 12 | — | — |
| Editor Blueprint | `UAIP.Editor.Blueprint` | 20 | — | — |
| Editor UMG | `UAIP.Editor.UMG` | 22 | 13 | — |
| Editor Material | `UAIP.Editor.Material` | 11 | — | — |
| Editor GameplayTags | `UAIP.Editor.GameplayTags` | 7 | — | — |
| Editor GameFeatures 🧩 | `UAIP.Editor.GameFeatures` | 3 | — | — |
| Editor Niagara 🧩 | `UAIP.Editor.Niagara` | 36 | 45 | — |
| Editor Physics | `UAIP.Editor.Physics` | 31 | 17 | — |
| Editor Dataflow 🧩 | `UAIP.Editor.Dataflow` | 7 | — | — |
| Editor Skeleton | `UAIP.Editor.Skeleton` | 8 | — | — |
| Editor DataTable | `UAIP.Editor.DataTable` | 7 | — | — |
| Editor AnimBlueprint | `UAIP.Editor.AnimBlueprint` | 10 | — | — |
| Editor SoundCue | `UAIP.Editor.SoundCue` | 7 | — | — |
| Editor SoundSettings | `UAIP.Editor.SoundSettings` | 13 | — | — |
| Editor MVVM 🧩 | `UAIP.Editor.MVVM` | 26 | 9 | — |
| Editor BehaviorTree | `UAIP.Editor.BehaviorTree` | 12 | — | — |
| Editor MetaSound 🧩 | `UAIP.Editor.MetaSound` | 9 | — | — |
| Editor EQS 🧩 | `UAIP.Editor.EQS` | 7 | — | — |
| Editor Sequencer | `UAIP.Editor.Sequencer` | 92 | 61 | — |
| Editor StateTree | `UAIP.Editor.StateTree` | 9 | — | — |
| Editor Curve | `UAIP.Editor.Curve` | 6 | — | — |
| Editor PCG 🧩 | `UAIP.Editor.PCG` | 33 | 31 | — |
| Editor WorldConditions 🧩 | `UAIP.Editor.WorldConditions` | 6 | — | — |
| Editor Conversation 🧩 | `UAIP.Editor.Conversation` | 12 | — | — |
| Editor ControlRig | `UAIP.Editor.ControlRig` | 59 | 44 | — |
| Editor EnhancedInput | `UAIP.Editor.EnhancedInput` | 13 | — | — |
| Editor GAS 🧩 | `UAIP.Editor.GAS` | 11 | 11 | — |
| Editor Python Extension 🧩 | `UAIP.Editor.PythonExtension` | 2 | — | — |
| Editor Sandbox 🧩 | `UAIP.Editor.Sandbox` | 6 | — | — |
| Editor WorldPartition | `UAIP.Editor.WorldPartition` | 34 | — | — |
| Editor Foliage | `UAIP.Editor.Foliage` | 11 | — | — |
| Runtime Engine Log | `UAIP.Runtime.Engine.Log` | 1 | — | — |
| Runtime Engine Plugin | `UAIP.Runtime.Engine.Plugin` | 5 | — | — |
| Runtime Engine CVar | `UAIP.Runtime.Engine.CVar` | 4 | — | partial (2/4) |
| Runtime Engine Config | `UAIP.Runtime.Engine.Config` | 2 | — | — |
| Runtime PIE | `UAIP.Runtime.PIE` | 11 ⁺² | 3 | partial (6/11) |
| Runtime Observation | `UAIP.Runtime.Observation` | 8 | — | ✅ |
| Runtime Execution | `UAIP.Runtime.Execution` | 3 | — | — |
| Runtime Assertion | `UAIP.Runtime.Assertion` | 4 | — | ✅ |
| Runtime Input | `UAIP.Runtime.Input` | 11 | — | — |
| Runtime GAS 🧩 | `UAIP.Runtime.GAS` | 6 | — | — |
| Runtime Niagara 🧩 | `UAIP.Runtime.Niagara` | 4 | 4 | — |

---

## UAIP.Core

System-level commands for discovery, health, and session management.

| Command | Description |
|---|---|
| 🆓 `HealthCheck` | Plugin connectivity check — returns `Status`, `UAIPVersion`, `EngineVersion`, `BuildConfig` |
| 🆓 `GetSystemInfo` | Returns UE version (Major/Minor/Patch/Changelist), project name, platform, build config, UAIP version |
| 🆓 `QueryCapabilities` | Returns the session's capability set and `OperationalConstraints` (7 policy flags) |
| 🆓 `ListCommands` | Filtered command catalog (filters: `GroupFilter`, `KeywordFilter`, `IncludeUnavailable`) |
| 🆓 `DescribeCommand` | Full metadata for a single command (schema, required capabilities, availability) |
| 🆓 `ListCommandGroups` | All group paths with intermediate path completion |
| 🆓 `ListPlugins` | ⚠️ **Deprecated** — use `UAIP.Runtime.Engine.Plugin.ListPlugins` instead. List installed plugins and their enabled state (JSON) |

---

## UAIP.Editor.Workspace

Editor lifecycle, tab management, graph layout, shader compilation, Live Coding.

| Command | Description |
|---|---|
| 🆓 `FocusEditorTab` | Bring the editor tab for an asset to the front |
| 🆓 `CloseEditorTab` | Close the editor tab for an asset |
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
---

## UAIP.Editor.Engine.Log

Log verbosity management and log entry retrieval.

| Command | Description |
|---|---|
| `GetLogVerbosity` | Get the current verbosity level of a log category |
| `SetLogVerbosity` | Set the verbosity level of a log category (requires `LogVerbosityEdit`) |
| `GetLogEntries` | Retrieve recent log entries from the editor output log (supports pattern filtering; no capability required) |

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
| `GetPluginDescriptor` | Read the full `.uplugin` descriptor JSON for a plugin |
| `GetPluginDependents` | List plugins that depend on a given plugin (budget-capped scan; `Truncated: true` on limit) |
| `GetPluginTemplateDescriptions` | List available plugin scaffold templates |
| `IsPluginCreationAllowed` | Check whether new plugin creation is allowed in the current editor state |
| `IsPluginModificationAllowed` | Check whether a specific plugin is modifiable (not Engine/Marketplace/GFP) |
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
| `ListSettingsContainers` | List all registered settings containers (e.g. `Project`, `Editor`). No capability required |
| `ListSettingsCategories` | List all categories in a settings container. No capability required |
| `ListSettingsSections` | List all sections in a settings category. No capability required |
| `GetSettingsSchema` | Return a JSON artifact with editable property names, types, descriptions, defaults, and edit conditions for a section (requires `EditorInspect`) |
| `GetSettingsValues` | Return a JSON artifact with current property values for a section. Secret fields (name matches a secret pattern, has secret metadata, or is a file path type) are masked with `***` (requires `EditorInspect`) |
| `SetSettingsValues` | Merge a `Properties` map into the settings object via `ImportText`. Supports `DryRun` (validates without applying). Requires `ConfigSettingsEdit`. Blocked during PIE |
| `SaveSettings` | Persist in-memory settings to the section's ini file via `ISettingsSection::Save()`. Requires `ConfigSettingsSave`. Blocked during PIE and when `bDisableSave` is set |
| `ResetSettingsToDefaults` | Revert the settings object to class defaults and save. Requires `ConfigSettingsReset`. Blocked during PIE |

---

## UAIP.Editor.Observation

Capture screenshots and dump editor state — all read-only.

| Command | Description |
|---|---|
| 🆓 `CaptureActiveWindowImage` | Screenshot of the active top-level editor window (PNG artifact) |
| 🆓 `CaptureEditorTabImage` | Screenshot of a specified editor tab's widget area |
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
| `CaptureViewportImageAnnotated` | Viewport screenshot with world-coordinate labels drawn on it (requires `ViewportAnnotationCapture`) |

---

## UAIP.Editor.Execution

Run tests, Python scripts, and Editor Utility Blueprints.

| Command | Description |
|---|---|
| `RunAutomationTest` | Run a UE Automation Test by name and return Pass/Fail/Error report |
| `RunAutomationSpec` | Run a UE Automation Spec by name and return Pass/Fail/Error report |
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

---

## UAIP.Editor.Assets

Open, search, create, duplicate, rename, delete assets and folders.

| Command | Description |
|---|---|
| `OpenAsset` | Open the specified asset in its editor |
| `CloseAsset` | Close all editors for the specified asset |
| `SearchAssets` | Search assets by path / class / tag |
| `CreateAsset` | Create a new asset of the specified class |
| `ListCreatableAssetClasses` | Return every UClass that `CreateAsset` can target, with factory count and default factory (heavy call) |
| `ListFactoriesForClass` | Return the factory candidates for a `ClassName`, each with its `FactoryParams` schema |
| `DuplicateAsset` | Duplicate an existing asset |
| `RenameAsset` | Rename / move an asset to another path |
| `DeleteAsset` | Delete an asset |
| `CreateFolder` | Create a new folder in the Content Browser |
| `DeleteFolder` | Delete an empty folder (returns `NotEmpty` if not empty) |
| `ForceDeleteFolder` | Delete a folder and its assets (max 50 items, no external-reference check) |
| 🆓 `GetSelectedAssets` | Return the assets currently selected in the Content Browser |
| `SelectAssets` | Select the specified assets in the Content Browser (requires `ContentBrowserNavigate`) |
| 🆓 `GetContentBrowserPath` | Return the current folder path shown in the Content Browser |
| `SetContentBrowserPath` | Navigate the Content Browser to a specified folder (requires `ContentBrowserNavigate`) |
| 🆓 `GetOpenAssets` | Return the list of assets currently open in an asset editor |

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
| `SearchAssetsSemantic` | Search project assets by natural-language query (hybrid BM25+vector, up to 500 results) |
| `FindSimilarAssets` | Find assets similar to a reference asset via vector similarity |
| `GetIndexStats` | Return current index statistics (asset count, last-built timestamp) |
| `StartIndexing` | Trigger a full semantic index rebuild (long-running; requires `SemanticSearchEdit`) |
| `CancelIndexing` | Cancel an in-progress index build (requires `SemanticSearchEdit`) |

### Toolset bridges (2) 🧩

Bridge commands via the `SemanticSearchToolset` plugin (UE 5.8+). Provider: `Toolset.Editor.SemanticSearch.*`. These commands mirror `SearchAssetsSemantic` and `FindSimilarAssets` above and are provided exclusively as a Toolset bridge (no UAIP native equivalent for these two Toolset-side commands; see ADR `2026-06-25-SemanticSearchToolset-BridgeOnly-Exception.md`).

| Command | Description |
|---|---|
| `Toolset.Editor.SemanticSearch.Search` | Hybrid BM25+vector search via SemanticSearchToolset |
| `Toolset.Editor.SemanticSearch.FindSimilar` | Vector similarity search via SemanticSearchToolset |

---

## UAIP.Editor.Level

Editor-side actor placement, transforms, and level loading.

| Command | Description |
|---|---|
| `ListLevelActors` | List all actors in the open level |
| `PlaceActorInLevel` | Place an actor in the editor level |
| `DeleteActorFromLevel` | Remove an actor from the editor level |
| `GetActorTransform` | Get the transform of an editor actor |
| `SetActorTransform` | Set the transform of an editor actor |
| `OpenLevel` | Open a level in the editor viewport (File > Open Level) |
| `NewLevel` | Create a new level from a template (EmptyLevel / EmptyOpenWorld / Basic / OpenWorld) |
| `SelectActors` | Select the specified actors in the editor level (replace or add to current selection) |
| `ListSelectedActors` | Return a list of actors currently selected in the editor |
| `ClearSelection` | Clear the current selection in the editor level |
| `FocusOnActors` | Focus the viewport camera on the specified actors (omit to use the current selection) |
| `GetCameraTransform` | Get the camera location and rotation of the active level editor viewport |
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

Read and write properties on actors, assets, Blueprint defaults, DataTable rows, World / Project settings.

| Command | Description |
|---|---|
| `GetActorProperty` | Get a property value from an editor actor |
| `SetActorProperty` | Set a property on an editor actor |
| `GetWorldSetting` | Get a WorldSettings property |
| `SetWorldSetting` | Set a WorldSettings property |
| `GetAssetProperty` | Get a property from an asset (DataAsset etc.) |
| `SetAssetProperty` | Set a property on an asset and call `MarkPackageDirty` |
| `GetBlueprintDefault` | Get a property from a Blueprint CDO |
| `SetBlueprintDefault` | Set a property on a Blueprint CDO |
| `GetProjectSetting` | Get a property from a `UDeveloperSettings` CDO |
| `SetProjectSetting` | Set a property on a `UDeveloperSettings` CDO and call `SaveConfig()` |
| `GetDataTableRow` | Get a DataTable row property |
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

---

## UAIP.Editor.GameFeatures 🧩

GameFeature Plugin management. Requires `GameFeatures` + `GameFeaturesEditor` plugins.

| Command | Description |
|---|---|
| `ListGameFeatures` 🧩 | List GameFeature Plugins with state filter (All / Installed / Mounted / Registered / Loaded / Active) |
| `GetGameFeatureInfo` 🧩 | GFP details (State, Actions, dependencies) |
| `CreateGameFeaturePlugin` 🧩 | Scaffold a new GameFeature Plugin (with name validation) |

---

## UAIP.Editor.Niagara 🧩

Niagara VFX system editing. Requires `Niagara` + `NiagaraEditor` plugins and **UE 5.7 or newer**.

### Native (36)

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

---

## UAIP.Editor.AnimBlueprint

Anim Blueprint graph and StateMachine editing.

| Command | Description |
|---|---|
| `GetAnimBlueprintInfo` | AnimGraph node list and StateMachine structure (degraded mode during PIE) |
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
| `GetBehaviorTreeInfo` | BT graph tree structure (Composite / Task / Decorator / Service) — recursive JSON |
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

---

## UAIP.Editor.MetaSound 🧩

MetaSound graph editing. Requires `Metasound` plugin.

| Command | Description |
|---|---|
| `GetMetaSoundInfo` 🧩 | MetaSoundSource / MetaSoundPatch graph topology (nodes, connections, I/O vertices) |
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
| `AddEQSGenerator` 🧩 | Add a Generator Option (GeneratorClass, 6-step allowlist) |
| `RemoveEQSGenerator` 🧩 | Remove a Generator Option by NodeId (cascading Test deletion) |
| `AddEQSTest` 🧩 | Add a Test to a Generator Option |
| `RemoveEQSTest` 🧩 | Remove a Test by NodeId |
| `SetEQSGeneratorProperty` 🧩 | Set a Generator property (generic ImportText_Direct) |
| `SetEQSTestProperty` 🧩 | Set a Test property (`param:<Name>` → `UAIDataProvider_QueryParams`) |

---

## UAIP.Editor.Sequencer

LevelSequence editing — tracks, sections, keyframes, playback, bindings.

### Native (92)

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

#### AnimMixer (17, optional `MovieSceneAnimMixer`)

| Command | Description |
|---|---|
| `GetAnimMixerTrackInfo` | Get AnimMixer track info |
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

### Toolset bridges (61) 🧩

Provider: `Toolset.AnimationAssistant.*` (41 commands — Lifecycle 6, Playback 10, Property 9, MarkedFrame 5, UI 11) and `Toolset.SequencerAnimMixer.*` (20 commands — Layers 10, Transitions 5, Decorations 5). Requires UE 5.8+.

---

## UAIP.Editor.StateTree

StateTree editing.

| Command | Description |
|---|---|
| `GetStateTreeInfo` | State tree, Task list, Transition list, Schema info (degraded mode during PIE) |
| `AddState` | Add a State (State / Group / Subtree / Linked / LinkedAsset — 5 types) |
| `RemoveState` | Remove a State by StateId (recursive child deletion) |
| `AddStateTask` | Add a Task to a State (8-step allowlist) |
| `RemoveStateTask` | Remove a Task by TaskId |
| `AddStateTransition` | Add a Transition (Succeeded / Failed / NextState / NextSelectableState / GotoState) |
| `RemoveStateTransition` | Remove a Transition by TransitionId |
| `SetStateNodeProperty` | Set a Task node property (generic ImportText_Direct) |
| `CompileStateTree` | Compile the StateTree (per-session 1 s rate limit) |

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

### Toolset bridges — PCG (31) 🧩

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

---

## UAIP.Editor.Conversation 🧩

ConversationDB graph editing. Requires `CommonConversation` plugin.

| Command | Description |
|---|---|
| `ListConversationEntryPoints` 🧩 | List entry points |
| `ListConversationSpeakers` 🧩 | List speakers |
| `ListConversationNodes` 🧩 | List all nodes with refPath |
| `GetConversationNodeConnections` 🧩 | Get connection info for a node |
| `ListConversationNodeSubNodes` 🧩 | List SubNodes of a node |
| `ListConversationNodeTypes` 🧩 | List allowed node classes by position (max 256) |
| `AddConversationNode` 🧩 | Add a top-level node (`UConversationNodeWithLinks` derived) |
| `AddConversationSubNode` 🧩 | Attach a SubNode to a parent Task node |
| `RemoveConversationNode` 🧩 | Remove a node by NodeGuid |
| `ConnectConversationNodes` 🧩 | Add a transition edge between nodes |
| `DisconnectConversationNodes` 🧩 | Remove a transition edge |
| `SetConversationNodeProperty` 🧩 | Set a property (FText sanitized — BIDI strip, PUA reject, 4096 char limit) |

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

### Toolset bridges (44) 🧩

Mirror of native commands via `AnimationAssistantToolset` (UE 5.8+). Provider: `Toolset.Editor.ControlRig.*`. Groups: asset creation (1), hierarchy observation (8), hierarchy editing (7), graph management (10), nodes (7), pins (6), variables (5).

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

### Native (11)

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

### Toolset bridges (11) 🧩

Mirror of native commands via the `GASToolsets` plugin (UE 5.8+). Provider: `Toolset.Editor.GAS.*`. Also bridges runtime inspection helpers: `GetAttributeValuesToolset`, `GetActiveEffectsToolset`, `GetGrantedAbilitiesToolset`, `GetActiveTagsToolset`, `FindAttributeSetClassesToolset`, `ListAttributesToolset`.

---

## UAIP.Editor.PythonExtension 🧩

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

## UAIP.Runtime.Engine.Log

Log category inspection at runtime. Read-only; no capability required.

| Command | Description |
|---|---|
| `GetLogCategories` | List all registered log category names |

---

## UAIP.Runtime.Engine.Plugin

Plugin inspection at runtime. Read-only commands available without any special capability. These are the Runtime-domain counterparts to `UAIP.Editor.Engine.Plugin` commands.

| Command | Description |
|---|---|
| `ListPlugins` | List discovered or enabled plugins with optional `EnabledOnly` filter and `LoadedFrom` filter |
| `GetPluginInfo` | Get detailed info for a plugin (11 fields: Name, FriendlyName, Version, Description, Category, IsEnabled, IsMounted, Type, BaseDir, LoadedFrom, Dependencies) |
| `IsEnabled` | Check whether a plugin is currently enabled (note: `.uproject` declaration and actual load state may diverge until restart) |
| `GetPluginDependencies` | Get the direct plugin dependencies declared by a plugin |
| `GetPluginForAsset` | Resolve the owning plugin for a given asset path |

---

## UAIP.Runtime.Engine.CVar

Read and write engine-wide console variables (CVars). CVars are global engine state — independent of any World or PIE session. Sensitive CVars are automatically excluded.

🔒 requires `RuntimeCVarRead` (DefaultDenied). ✏️ requires `RuntimeCVarWrite` (DefaultDenied).

| Command | Description |
|---|---|
| 🔒 `GetConsoleVariable` | Get the name, current value, type, and help text for a CVar (sensitive names return `NotFound`) |
| 🔒 `SearchConsoleVariables` | Search CVars using a wildcard (`*`) pattern (default 50 results, max 200) |
| ✏️ `SetConsoleVariable` | Set the value of a CVar (sensitive names and `ECVF_ReadOnly` CVars are rejected; `ECVF_Cheat` CVars are rejected unless `AllowCheatCVarWrite` is enabled) |
| ✏️ `ResetConsoleVariable` | Reset a CVar to its default value (sensitive names and `ECVF_ReadOnly` CVars are rejected; `ECVF_Cheat` CVars are rejected unless `AllowCheatCVarWrite` is enabled) |

> **Note**: The legacy `GetConsoleVariable` and `SearchConsoleVariables` commands under `UAIP.Runtime.PIE` are deprecated and will be removed in v1.2. Use these commands instead.

---

## UAIP.Runtime.Engine.Config

Raw ini key access for runtime and packaged builds. Reads and writes ini keys directly without going through `ISettingsModule`. Write commands are blocked in packaged builds.

| Command | Description |
|---|---|
| `GetConfigValue` | Read the string value of an ini key given section and key name. No capability required |
| `SetConfigValue` | Write or delete a raw ini key. Requires `ConfigSettingsEdit`. Blocked in packaged builds. Rejects ini injection characters (`[`, `]`) in key and value fields |

---

## UAIP.Runtime.PIE

PIE session control and runtime world manipulation.

| Command | Description |
|---|---|
| 🆓 `StartPIE` | Start a Play-in-Editor session |
| 🆓 `StopPIE` | Stop the active PIE session |
| 🆓 `PausePIE` | Pause the active PIE session |
| 🆓 `ResumePIE` | Resume a paused PIE session |
| 🆓 `LoadMap` | Load a map in the active PIE session and wait for completion |
| `ExecuteConsoleCommand` | Execute a console command in the active PIE session |
| `TeleportActor` | Teleport an actor to a world-space location / rotation |
| `PossessActor` | Have a player controller possess an actor |
| `SetTimeScale` | Set the global time scale of the active PIE session |
| `QuitGame` | Request the running game process to quit |
| ~~`GetConsoleVariable`~~ | ⚠️ **Deprecated** — use `UAIP.Runtime.Engine.CVar.GetConsoleVariable` instead |
| ~~`SearchConsoleVariables`~~ | ⚠️ **Deprecated** — use `UAIP.Runtime.Engine.CVar.SearchConsoleVariables` instead |
| 🆓 `GetPIEState` | Return the current PIE state — `Running`, `Stopped`, `Paused`, or `Simulating` |

### Toolset bridges (4) 🧩

Bridge commands via the EditorToolset plugin (UE 5.8+).

| Command | Provider | Description |
|---|---|---|
| `Toolset.Editor.Toolset.PIE.StartPIE` | `Toolset.Editor.Toolset.PIE.*` | Start a PIE session (async, requires `PIEControl`) |
| `Toolset.Editor.Toolset.PIE.StopPIE` | `Toolset.Editor.Toolset.PIE.*` | Stop the active PIE session (async, requires `PIEControl`) |
| `Toolset.Editor.Toolset.PIE.IsPIERunning` | `Toolset.Editor.Toolset.PIE.*` | Return whether PIE is currently active |

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

GameplayAbilities state inspection. Requires `GameplayAbilities` plugin. PIE required.

| Command | Description |
|---|---|
| `GetAttributeValues` 🧩 | All AttributeSet attribute values (currentValue / baseValue) for an actor |
| `GetActiveEffects` 🧩 | Active gameplay effects (Level, StackCount, remaining time) on an actor |
| `GetGrantedAbilities` 🧩 | Granted abilities (Class, IsActive, ActiveCount, InputID) on an actor |
| `GetActiveTags` 🧩 | Owned GameplayTags on an actor |
| `FindAttributeSetClasses` 🧩 | Scan PIE world actors and list UAttributeSet classes (MaxActors limit) |
| `ListAttributes` 🧩 | List all attribute names defined on an AttributeSet class |

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

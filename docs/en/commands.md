**[日本語](../ja/commands.md)** | [Back to README](../../README.md)

# Commands Reference

UAIP exposes 600+ commands organized by domain. Each command name is fully-qualified — e.g. `UAIP.Editor.Observation.CaptureActiveWindowImage`. This page omits the provider prefix in the tables; the section header tells you what to prepend.

## How to use this reference

- Use `uaip_describe_command(CommandName="...")` to get the full parameter schema for a command
- Use `uaip_list_commands(ProviderPrefix="UAIP.Editor")` to filter by domain at runtime
- For the required Capability per command, see [Safety & Capabilities](safety.md)

## Symbols

| Symbol | Meaning |
|---|---|
| 🆓 | Available in the demo binary (also in Pro) |
| (no mark) | Pro-only command |
| **†** | Requires an optional UE plugin (the command is not registered if the plugin is disabled) |

## Toolset bridges (UE 5.8+)

In addition to UAIP-native commands, the Pro version exposes **Toolset bridge** commands (under the `Toolset.*` prefix) that delegate to the official UE 5.8 Toolset framework. They mirror UAIP-native commands and provide an alternative API path. This page summarizes them per domain rather than enumerating each one — use `uaip_list_commands(ProviderPrefix="Toolset")` to enumerate them at runtime.

---

## Domain summary

| Domain | Provider prefix | Native | Toolset bridge | Demo |
|---|---|---:|---:|---:|
| Core | `UAIP.Core` | 6 | — | ✅ |
| Editor Workspace | `UAIP.Editor.Workspace` | 18 | — | partial (13/18) |
| Editor Observation | `UAIP.Editor.Observation` | 13 | — | ✅ (1 excluded) |
| Editor Execution | `UAIP.Editor.Execution` | 5 | — | — |
| Editor UI Automation | `UAIP.Editor.UIAutomation` | 15 | — | ✅ |
| Editor Assets | `UAIP.Editor.Assets` | 10 | — | — |
| Editor Level | `UAIP.Editor.Level` | 7 | — | — |
| Editor Property | `UAIP.Editor.Property` | 13 | — | — |
| Editor Blueprint | `UAIP.Editor.Blueprint` | 8 | — | — |
| Editor UMG | `UAIP.Editor.UMG` | 23 | 13 | — |
| Editor Material | `UAIP.Editor.Material` | 9 | — | — |
| Editor GameplayTags | `UAIP.Editor.GameplayTags` | 7 | — | — |
| Editor GameFeatures **†** | `UAIP.Editor.GameFeatures` | 3 | — | — |
| Editor Niagara **†** | `UAIP.Editor.Niagara` | 30 | 45 | — |
| Editor Physics | `UAIP.Editor.Physics` | 31 | 17 | — |
| Editor Dataflow **†** | `UAIP.Editor.Dataflow` | 7 | — | — |
| Editor Skeleton | `UAIP.Editor.Skeleton` | 8 | — | — |
| Editor DataTable | `UAIP.Editor.DataTable` | 7 | — | — |
| Editor AnimBlueprint | `UAIP.Editor.AnimBlueprint` | 10 | — | — |
| Editor SoundCue | `UAIP.Editor.SoundCue` | 7 | — | — |
| Editor BehaviorTree | `UAIP.Editor.BehaviorTree` | 12 | — | — |
| Editor MetaSound **†** | `UAIP.Editor.MetaSound` | 9 | — | — |
| Editor EQS **†** | `UAIP.Editor.EQS` | 7 | — | — |
| Editor Sequencer | `UAIP.Editor.Sequencer` | 93 | 61 | — |
| Editor StateTree | `UAIP.Editor.StateTree` | 9 | — | — |
| Editor Curve | `UAIP.Editor.Curve` | 6 | — | — |
| Editor PCG **†** | `UAIP.Editor.PCG` | 13 | — | — |
| Editor WorldConditions **†** | `UAIP.Editor.WorldConditions` | 6 | — | — |
| Editor Conversation **†** | `UAIP.Editor.Conversation` | 12 | — | — |
| Editor ControlRig | `UAIP.Editor.ControlRig` | 59 | 44 | — |
| Editor Python Extension **†** | `UAIP.Editor.PythonExtension` | 2 | — | — |
| Runtime PIE | `UAIP.Runtime.PIE` | 10 | — | partial (5/10) |
| Runtime Observation | `UAIP.Runtime.Observation` | 8 | — | ✅ |
| Runtime Execution | `UAIP.Runtime.Execution` | 3 | — | — |
| Runtime Assertion | `UAIP.Runtime.Assertion` | 4 | — | ✅ |
| Runtime GAS **†** | `UAIP.Runtime.GAS` | 6 | — | — |

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

## UAIP.Editor.Observation

Capture screenshots and dump editor state — all read-only.

| Command | Description |
|---|---|
| 🆓 `CaptureActiveWindowImage` | Screenshot of the active top-level editor window (PNG artifact) |
| 🆓 `CaptureEditorTabImage` | Screenshot of a specified editor tab's widget area |
| 🆓 `CaptureGraphViewportImage` | Screenshot of an SGraphEditor viewport |
| `CaptureCanonicalGraphImage` **†** | Full canonical graph image via a registered external capture provider |
| 🆓 `DumpEditorState` | Active tab, open assets, window dimensions, etc. (JSON) |
| 🆓 `DumpSelectionState` | Current editor selection — actors, objects, graph nodes (JSON) |
| 🆓 `DumpOpenTabs` | List of open asset editor tabs (JSON) |
| 🆓 `DumpOutputLog` | Buffered Output Log as a text artifact (line count / filter support) |
| 🆓 `DumpMessageLog` | Message Log entries with category filter (JSON artifact) |
| 🆓 `DumpSlateTree` | Slate widget tree (JSON, root path filter support) |
| 🆓 `InspectMenu` | Top-bar menu structure under a path (labels, enabled, checked) |
| 🆓 `InspectContextMenu` | Context menu items for a target (without executing them) |
| 🆓 `ObserveWidget` | Time-series sampling of widget Visibility / Enabled / Hovered / Focused state |

---

## UAIP.Editor.Execution

Run tests, Python scripts, and Editor Utility Blueprints.

| Command | Description |
|---|---|
| `RunAutomationTest` | Run a UE Automation Test by name and return Pass/Fail/Error report |
| `RunAutomationSpec` | Run a UE Automation Spec by name and return Pass/Fail/Error report |
| `RunEditorPythonScript` **†** | Run an inline Python script or a `.py` file (requires `PythonScriptPlugin`) |
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
| `DuplicateAsset` | Duplicate an existing asset |
| `RenameAsset` | Rename / move an asset to another path |
| `DeleteAsset` | Delete an asset |
| `CreateFolder` | Create a new folder in the Content Browser |
| `DeleteFolder` | Delete an empty folder (returns `NotEmpty` if not empty) |
| `ForceDeleteFolder` | Delete a folder and its assets (max 50 items, no external-reference check) |

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
| `ListPlugins` | List installed plugins and their enabled state (JSON) |

---

## UAIP.Editor.Blueprint

Edit Blueprint variables and event graph nodes.

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

---

## UAIP.Editor.UMG

Widget Blueprint editing — tree, variables, animation, bindings.

### Native (23)

| Command | Description |
|---|---|
| `CreateWidgetBlueprint` | Create a new Widget Blueprint asset |
| `ListWidgetBlueprints` | List Widget Blueprints from AssetRegistry (max 500) |
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

### Toolset bridges (13) **†**

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

## UAIP.Editor.GameFeatures **†**

GameFeature Plugin management. Requires `GameFeatures` + `GameFeaturesEditor` plugins.

| Command | Description |
|---|---|
| `ListGameFeatures` **†** | List GameFeature Plugins with state filter (All / Installed / Mounted / Registered / Loaded / Active) |
| `GetGameFeatureInfo` **†** | GFP details (State, Actions, dependencies) |
| `CreateGameFeaturePlugin` **†** | Scaffold a new GameFeature Plugin (with name validation) |

---

## UAIP.Editor.Niagara **†**

Niagara VFX system editing. Requires `Niagara` + `NiagaraEditor` plugins.

### Native (30)

#### Observation (12)

| Command | Description |
|---|---|
| `GetSystemTopology` **†** | Niagara system emitter structure |
| `GetSystemCompileState` **†** | System compilation state |
| `GetAssetDiscoveryInfo` **†** | Niagara asset discovery info |
| `GetScriptAssets` **†** | Niagara script asset list |
| `GetNiagaraParameterCollections` **†** | Niagara parameter collection list |
| `GetUserVariables` **†** | User variable list of a system |
| `GetSystemInfo` **†** | System detail info (with metadata) |
| `GetSystemData` **†** | System data structure |
| `GetEmitterData` **†** | Emitter data structure |
| `GetRendererData` **†** | Renderer data structure |
| `GetStackInputData` **†** | Module stack input value |
| `UEnum_Info` **†** | UEnum information |

#### Editing (18)

| Command | Description |
|---|---|
| `AddEmitter` **†** | Add an emitter to a Niagara system |
| `RemoveEmitter` **†** | Remove an emitter |
| `DuplicateEmitter` **†** | Duplicate an emitter |
| `SetEmitterEnabled` **†** | Toggle emitter enabled state |
| `SetEmitterName` **†** | Change emitter name |
| `SetEmitterData` **†** | Set emitter data |
| `AddRenderer` **†** | Add a renderer to an emitter |
| `RemoveRenderer` **†** | Remove a renderer |
| `SetRendererData` **†** | Set renderer data |
| `AddModule` **†** | Add a module to an emitter module stack |
| `RemoveModule` **†** | Remove a module |
| `MoveModule` **†** | Move a module within the stack |
| `SetModuleEnabled` **†** | Toggle module enabled state |
| `SetStackInputData` **†** | Set a module stack input value |
| `SetSystemData` **†** | Set system data |
| `AddUserVariables` **†** | Add user variables to a system |
| `RemoveUserVariables` **†** | Remove user variables |
| `CompileNiagaraSystem` **†** | Compile the Niagara system |

### Toolset bridges (45) **†**

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

### Toolset bridges (17) **†**

Mirror of native commands via the `PhysicsToolsets` plugin (UE 5.8+ Experimental). Provider: `Toolset.Editor.Physics.*`.

---

## UAIP.Editor.Dataflow **†**

Dataflow graph editing. Requires `DataflowEditor` plugin.

| Command | Description |
|---|---|
| `GetDataflowGraphInfo` **†** | Get graph nodes / edges / variables (JSON) |
| `ListDataflowNodeTypes` **†** | List available Dataflow node types |
| `AddDataflowNode` **†** | Add a node to a Dataflow graph |
| `RemoveDataflowNode` **†** | Remove a node from a Dataflow graph |
| `ConnectDataflowPins` **†** | Connect two pins |
| `DisconnectDataflowPins` **†** | Disconnect a pin connection |
| `ListDataflowVariables` **†** | List graph variables |

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

## UAIP.Editor.MetaSound **†**

MetaSound graph editing. Requires `Metasound` plugin.

| Command | Description |
|---|---|
| `GetMetaSoundInfo` **†** | MetaSoundSource / MetaSoundPatch graph topology (nodes, connections, I/O vertices) |
| `AddMetaSoundNode` **†** | Add a node by `Namespace::Name` (MajorVersion-aware, 5-step policy) |
| `RemoveMetaSoundNode` **†** | Remove a node by NodeId |
| `ConnectMetaSoundPins` **†** | Connect two pins (idempotent flag on duplicates) |
| `DisconnectMetaSoundPins` **†** | Disconnect a pin connection |
| `AddMetaSoundInput` **†** | Add an input vertex (single-page assets only) |
| `AddMetaSoundOutput` **†** | Add an output vertex (single-page assets only) |
| `SetMetaSoundNodeProperty` **†** | Set an input default (Bool / Int / Float / String, NaN / Inf rejected) |
| `CompileMetaSound` **†** | Register with Frontend (per-session 1 s rate limit) |

---

## UAIP.Editor.EQS **†**

EQS query editing. Requires `EnvironmentQueryEditor` plugin.

| Command | Description |
|---|---|
| `GetEQSQueryInfo` **†** | EQS Generator Option / Test structure (degraded mode during PIE) |
| `AddEQSGenerator` **†** | Add a Generator Option (GeneratorClass, 6-step allowlist) |
| `RemoveEQSGenerator` **†** | Remove a Generator Option by NodeId (cascading Test deletion) |
| `AddEQSTest` **†** | Add a Test to a Generator Option |
| `RemoveEQSTest` **†** | Remove a Test by NodeId |
| `SetEQSGeneratorProperty` **†** | Set a Generator property (generic ImportText_Direct) |
| `SetEQSTestProperty` **†** | Set a Test property (`param:<Name>` → `UAIDataProvider_QueryParams`) |

---

## UAIP.Editor.Sequencer

LevelSequence editing — tracks, sections, keyframes, playback, bindings.

### Native (93)

#### Structure (16)

| Command | Description |
|---|---|
| `AddTrack` | Add a track to a Level Sequence (TrackClass-specified) |
| `RemoveTrack` | Remove a track by TrackClass / BindingGuid |
| `AddSection` | Add a section to a track (StartFrame / EndFrame in DisplayRate) |
| `RemoveSection` | Remove a section by SectionIndex |
| `SetPlaybackRange` | Set the sequence's playback range |
| `FlushSequencerChanges` | Flush deferred change notifications |
| `CreateLevelSequence` | Create a new LevelSequence asset |
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

### Toolset bridges (61) **†**

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

## UAIP.Editor.PCG **†**

PCG graph editing. Requires `PCG` plugin.

| Command | Description |
|---|---|
| `GetPCGGraphInfo` **†** | UPCGGraph nodes / edges / parameters (degraded during PIE) |
| `ListPCGNodeTypes` **†** | UPCGSettings subclasses passing the allowlist |
| `AddPCGNode` **†** | Add a node by SettingsClassPath (returns NodePath) |
| `RemovePCGNode` **†** | Remove a node by NodePath (cascades edge removal) |
| `ConnectPCGPins` **†** | Connect pins by NodePath + PinLabel |
| `DisconnectPCGPins` **†** | Disconnect pins (specific pair or all from an output pin) |
| `SetPCGNodeProperty` **†** | Set a UPCGSettings EditAnywhere property (complex types rejected) |
| `ExecutePCGGraph` **†** | Trigger `UPCGComponent::Generate` |
| `ListCustomPCGNodeTypes` **†** | List C++ / Blueprint custom PCG node types |
| `GetCustomPCGNodeSchema` **†** | JSON schema of C++ UPCGSettings subclass EditAnywhere properties |
| `GetCustomBlueprintPCGNodeSchema` **†** | JSON schema of Blueprint UPCGBlueprintSettings subclass properties |
| `SetCustomCppPCGNodeProperty` **†** | Set a property on a C++ custom node (`RecompileTriggered` flag) |
| `SetCustomBlueprintPCGNodeProperty` **†** | Set a property on a BP custom node (Class CDO / per-Instance modes) |

---

## UAIP.Editor.WorldConditions **†**

WorldConditions editing. Requires `WorldConditions` plugin.

| Command | Description |
|---|---|
| `GetWorldConditionInfo` **†** | Condition set structure (Operator / Depth / properties) |
| `AddWorldCondition` **†** | Add a condition (`InsertAtIndex=-1` appends) |
| `RemoveWorldCondition` **†** | Remove a condition by index |
| `SetWorldConditionProperty` **†** | Set a condition USTRUCT property (ImportText value string) |
| `SetWorldConditionOperator` **†** | Set Operator (And / Or) and bInvert (Index 0 is fixed Copy) |
| `SetWorldConditionExpressionDepth` **†** | Set ExpressionDepth (0–4) |

---

## UAIP.Editor.Conversation **†**

ConversationDB graph editing. Requires `CommonConversation` plugin.

| Command | Description |
|---|---|
| `ListConversationEntryPoints` **†** | List entry points |
| `ListConversationSpeakers` **†** | List speakers |
| `ListConversationNodes` **†** | List all nodes with refPath |
| `GetConversationNodeConnections` **†** | Get connection info for a node |
| `ListConversationNodeSubNodes` **†** | List SubNodes of a node |
| `ListConversationNodeTypes` **†** | List allowed node classes by position (max 256) |
| `AddConversationNode` **†** | Add a top-level node (`UConversationNodeWithLinks` derived) |
| `AddConversationSubNode` **†** | Attach a SubNode to a parent Task node |
| `RemoveConversationNode` **†** | Remove a node by NodeGuid |
| `ConnectConversationNodes` **†** | Add a transition edge between nodes |
| `DisconnectConversationNodes` **†** | Remove a transition edge |
| `SetConversationNodeProperty` **†** | Set a property (FText sanitized — BIDI strip, PUA reject, 4096 char limit) |

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

### Toolset bridges (44) **†**

Mirror of native commands via `AnimationAssistantToolset` (UE 5.8+). Provider: `Toolset.Editor.ControlRig.*`. Groups: asset creation (1), hierarchy observation (8), hierarchy editing (7), graph management (10), nodes (7), pins (6), variables (5).

---

## UAIP.Editor.PythonExtension **†**

Python command extension. Requires `PythonScriptPlugin`.

| Command | Description |
|---|---|
| `ReloadPythonCommands` **†** | Rescan the commands directory and update existing handler descriptors in-place |
| *(dynamic commands)* **†** | Commands registered via the `@uaip_command` decorator (names depend on user scripts) |

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

## UAIP.Runtime.GAS **†**

GameplayAbilities state inspection. Requires `GameplayAbilities` plugin. PIE required.

| Command | Description |
|---|---|
| `GetAttributeValues` **†** | All AttributeSet attribute values (currentValue / baseValue) for an actor |
| `GetActiveEffects` **†** | Active gameplay effects (Level, StackCount, remaining time) on an actor |
| `GetGrantedAbilities` **†** | Granted abilities (Class, IsActive, ActiveCount, InputID) on an actor |
| `GetActiveTags` **†** | Owned GameplayTags on an actor |
| `FindAttributeSetClasses` **†** | Scan PIE world actors and list UAttributeSet classes (MaxActors limit) |
| `ListAttributes` **†** | List all attribute names defined on an AttributeSet class |

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

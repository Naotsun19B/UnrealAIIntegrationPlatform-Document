**[日本語](../ja/commands.md)** | [Back to README](../../README.md)

# Commands Reference

UAIP exposes 200+ commands organized by domain. All command names are fully-qualified (e.g. `UAIP.Editor.Assets.CreateAsset`).

---

## Discovering commands

Use the three discovery tools before calling a command:

| Tool | Purpose |
|---|---|
| `uaip_query_capabilities` | Return the capability set available to the current session |
| `uaip_list_commands` | List registered commands — filter with `ProviderPrefix` |
| `uaip_describe_command` | Get the parameter schema and required capabilities for one command |

### Common discovery patterns

```
# List all editor commands
uaip_list_commands(ProviderPrefix="UAIP.Editor")

# List only stable commands
uaip_list_commands(ProviderPrefix="UAIP.Editor", Stability="Stable")

# Inspect parameters before calling
uaip_describe_command(CommandName="UAIP.Editor.Assets.CreateAsset")
```

---

## Core commands

| Command | Description |
|---|---|
| `UAIP.Core.HealthCheck` | Verify the connection is alive |
| `UAIP.Core.ListCommands` | List registered commands |
| `UAIP.Core.DescribeCommand` | Describe one command |
| `UAIP.Core.QueryCapabilities` | Return current session capabilities |
| `UAIP.Core.EndSession` | End the current session and release artifacts |
| `UAIP.Core.ReloadCapabilities` | Reload capabilities from ini (requires `AllowCapabilityReload=True`) |

---

## Editor domain — `UAIP.Editor.*`

### Workspace

| Provider | Coverage |
|---|---|
| `UAIP.Editor.Workspace` | Tab management, graph editor focus, LiveCoding trigger, Undo-Redo, ShutdownEditor, RestartEditor |

### Assets

| Provider | Coverage |
|---|---|
| `UAIP.Editor.Assets` | CreateAsset, DeleteAsset, DuplicateAsset, OpenAsset, CloseAsset, SaveAll, SearchAssets, RenameAsset |

### Level

| Provider | Coverage |
|---|---|
| `UAIP.Editor.Level` | OpenLevel, PlaceActorInLevel, DeleteActor, SetActorTransform, ListLevelActors |

### Blueprint

| Provider | Coverage |
|---|---|
| `UAIP.Editor.Blueprint` | AddVariable, SetVariableDefault, AddFunction, AddGraphNode, ConnectPins, ListGraphNodes, DeleteNode, CompileBlueprint |

### Property

| Provider | Coverage |
|---|---|
| `UAIP.Editor.Property` | GetActorProperty, SetActorProperty |

### UMG

| Provider | Coverage |
|---|---|
| `UAIP.Editor.UMG` | AddWidget, SetWidgetProperty, ListWidgets |

### Material

| Provider | Coverage |
|---|---|
| `UAIP.Editor.Material` | AddMaterialNode, ConnectMaterialPins, SetMaterialProperty, ListMaterialNodes |

### Niagara

| Provider | Coverage |
|---|---|
| `UAIP.Editor.Niagara` | AddNiagaraModule, SetNiagaraParameter, ListNiagaraEmitters |

### Physics

| Provider | Coverage |
|---|---|
| `UAIP.Editor.Physics` | AddPhysicsBody, SetPhysicsConstraint, ListPhysicsBodies |

### Dataflow

| Provider | Coverage |
|---|---|
| `UAIP.Editor.Dataflow` | AddDataflowNode, ConnectDataflowPins, ListDataflowNodes |

### Skeleton

| Provider | Coverage |
|---|---|
| `UAIP.Editor.Skeleton` | ListBones, AddSocket, SetSocketTransform |

### Anim Blueprint

| Provider | Coverage |
|---|---|
| `UAIP.Editor.AnimBlueprint` | AddAnimNode, ConnectAnimPins, AddStateMachineState, AddStateMachineTransition |

### Behavior Tree

| Provider | Coverage |
|---|---|
| `UAIP.Editor.BehaviorTree` | AddBTNode, SetBTNodeProperty, AddBlackboardKey |

### EQS

| Provider | Coverage |
|---|---|
| `UAIP.Editor.EQS` | AddEQSGenerator, AddEQSTest, SetEQSTestProperty |

### MetaSound

| Provider | Coverage |
|---|---|
| `UAIP.Editor.MetaSound` | AddMetaSoundNode, ConnectMetaSoundPins, ListMetaSoundNodes |

### Sequencer

| Provider | Coverage |
|---|---|
| `UAIP.Editor.Sequencer` | AddTrack, AddSection, SetSectionRange, AddKeyframe, BindActor |

### StateTree

| Provider | Coverage |
|---|---|
| `UAIP.Editor.StateTree` | AddState, AddTransition, AddTask, SetStateProperty |

### ControlRig

| Provider | Coverage |
|---|---|
| `UAIP.Editor.ControlRig` | AddControl, SetControlTransform, AddRigVMNode, ConnectRigVMPins |

### Gameplay Tags

| Provider | Coverage |
|---|---|
| `UAIP.Editor.GameplayTags` | AddGameplayTag, RemoveGameplayTag, ListGameplayTags |

### Game Features

| Provider | Coverage |
|---|---|
| `UAIP.Editor.GameFeatures` | ListGameFeaturePlugins, ActivateGameFeaturePlugin, DeactivateGameFeaturePlugin |

### Enhanced Input

| Provider | Coverage |
|---|---|
| `UAIP.Editor.EnhancedInput` | AddInputAction, AddMappingContext, AddActionMapping |

### PCG

| Provider | Coverage |
|---|---|
| `UAIP.Editor.PCG` | AddPCGNode, ConnectPCGPins, ListPCGNodes |

### Observation

| Provider | Coverage |
|---|---|
| `UAIP.Editor.Observation` | CaptureActiveWindowImage, CaptureEditorTabImage, CaptureGraphViewportImage, CaptureCanonicalGraphImage, DumpEditorState, DumpSlateTree, DumpSelectionState |

### Execution

| Provider | Coverage |
|---|---|
| `UAIP.Editor.Execution` | RunAutomationTest, RunEditorPythonScript, RunEditorUtilityWidget |

### UI Automation

| Provider | Coverage |
|---|---|
| `UAIP.Editor.UIAutomation` | ClickWidget, FillForm, PressKey, WaitForWidget, InvokeContextMenuAction, FocusEditorTab |

---

## Runtime domain — `UAIP.Runtime.*`

### PIE

| Provider | Coverage |
|---|---|
| `UAIP.Runtime.PIE` | StartPIE, StopPIE, LoadMap |

### World

| Provider | Coverage |
|---|---|
| `UAIP.Runtime.World` | SpawnActor, DestroyActor, TeleportActor, ExecuteConsoleCommand, ListWorldActors |

### Observation

| Provider | Coverage |
|---|---|
| `UAIP.Runtime.Observation` | DumpWorldState, CaptureViewportImage, CapturePerformanceSnapshot, CheckpointCapture |

### GAS (Gameplay Ability System)

| Provider | Coverage |
|---|---|
| `UAIP.Runtime.GAS` | GetAttributeValues, FindAttributeSetClasses, ListGrantedAbilities |

### Input

| Provider | Coverage |
|---|---|
| `UAIP.Runtime.Input` | InjectInputKey, InjectEnhancedInputAction |

### Assertion (Scenario primitives)

| Provider | Coverage |
|---|---|
| `UAIP.Runtime.Assertion` | WaitSeconds, WaitForCondition, AssertActorProperty, AssertWorldActorExists |

### Execution

| Provider | Coverage |
|---|---|
| `UAIP.Runtime.Execution` | RunGauntletTest, RunRuntimeAutomationTest |

---

## Toolset bridge — `Toolset.*`

When optional Toolset plugins are enabled, additional commands are available under the `Toolset.*` prefix. These commands are enhancements — every Toolset bridge command has a corresponding `UAIP.*` native command that works without Toolset plugins.

| Provider | Requires |
|---|---|
| `Toolset.AutomationTest` | AutomationTestToolset plugin |
| `Toolset.SlateInspector` | SlateInspectorToolset plugin |
| `Toolset.AIModule` | AIModuleToolset plugin |
| `Toolset.AnimationAssistant` | AnimationAssistantToolset plugin |

---

## Error codes

| ErrorCode | Cause | Fix |
|---|---|---|
| `CommandNotFound` | Wrong command name | Use `uaip_list_commands` to find the correct name |
| `CapabilityNotAvailable` | Session lacks the required capability | See [Safety & Capabilities](safety.md) |
| `PolicyViolation` | Denied by SafetyPolicy or missing opt-in | See [Safety & Capabilities](safety.md) |
| `InvalidParams` | Missing or wrong parameter | Re-read schema with `uaip_describe_command` |
| `NotFound` | Asset / actor path mismatch | Check the path or name |
| `ExecutionFailed` | Runtime failure | Rebuild params; use `RetryCount` in scenarios |
| `NotAllowed` | Forbidden path or PIE-time edit | Reconsider the path or timing |
| `Timeout` | Step exceeded wall-clock cap | Split work or increase `TimeoutSeconds` |

# Live Demo: AI Builds a Blueprint Line Trace in Unreal Engine

**Engine:** UE 5.8 — ThirdPerson template  
**AI client:** Claude Code via MCP

---

This page is a full transcript of the UAIP demo session recorded for the
[official trailer](https://www.youtube.com/watch?v=TODO).
Claude was given a single prompt spanning three phases and completed everything
autonomously — no human intervention during execution.

The session illustrates:

- discovering assets and parameters with search commands instead of hard-coded paths
- correcting a property-set syntax error on the fly
- building an 11-node Blueprint graph (variables, wiring, compile) entirely through UAIP commands
- bundling a PIE timing-sensitive verification inside `uaip_run_scenario` to stay within a 5-second effect window

---

## Prompt given to the AI

The full prompt is reproduced below.

<details>
<summary>Click to expand</summary>

```
This is a live demonstration being recorded for an audience. Follow these rules strictly:

- Every editor operation must produce a visible change on screen before you move to the next step.
- During Blueprint graph editing: after placing each node or group of nodes, call FrameGraphAll
  to keep all nodes in the visible canvas area.
- If a command requires discovering an asset name or parameter name, use the appropriate
  search or list command first — do not hard-code guesses.

IMPLEMENTATION CONSTRAINTS (NON-NEGOTIABLE):

[L1] Use "Line Trace By Channel" to determine the ground location. Do not substitute it
     with GetActorLocation wired directly to the spawn node.
[L2] The "Hit Location" output of "Break Hit Result" MUST be wired to the spawn node's Location.
[L3] Line Trace inputs:
       Start = GetActorLocation (Self)
       End   = GetActorLocation + (GetActorUpVector × −500)
[L4] Cleanup chain: Spawn → Delay(5.0) → DestroyComponent.
     Use a Blueprint variable "DelayDuration = 5.0" because the API does not expose
     direct pin-default writes and the Delay node's built-in default is 0.2.

PHASE 1 — Map and Material
  1. Open Lvl_ThirdPerson.
  2. Open MI_ThirdPersonColWay.
  3. Find the floor color parameter and change it to red (R=1, G=0, B=0, A=1). Save.
  4. Capture a screenshot confirming the change.

PHASE 2 — Blueprint Graph
  5. Open BP_ThirdPersonCharacter, focus the Event Graph.
  6. Implement: Jump (Pressed) → LineTraceByChannel → SpawnSystemAtLocation(NS_JumpPad)
                             → Delay(DelayDuration) → DestroyComponent
     - Capture a reference image of the chosen Niagara effect before wiring.
  7. Compile and save.

PHASE 3 — PIE Verification
  8–10. Close BP, focus Level Viewport, start PIE.
  11. Use uaip_run_scenario (NOT individual uaip_execute calls) to bundle:
        WaitSeconds → InjectInputKey(Jump Pressed) → InjectInputKey(Released)
        → WaitSeconds → CaptureImage
      Iterate up to 3 scenario submissions until the Niagara effect is clearly
      visible at the hit location.
  12. Stop PIE.
  13. Report all yes/no checks, scenario count, and both reference + final images.
```

</details>

---

## Phase 1 — Map and Material

### Asset discovery

Rather than guessing paths, the AI ran `SearchAssets` first:

```
SearchAssets(PackagePath="/Game/", Filter="Lvl_ThirdPerson")
→ /Game/ThirdPersonTemplate/ThirdPerson/Lvl_ThirdPerson

SearchAssets(Filter="MI_ThirdPersonColWay")
→ /Game/ThirdPersonTemplate/ThirdPerson/MI_ThirdPersonColWay (MaterialInstanceConstant)
```

### Parameter discovery and color change

```
Property.GetAssetProperty(PropertyPath="VectorParameterValues")
→ Base Color: (R=0.051, G=0.527, B=0.051, A=1.0)  ← green-ish
```

First attempt with a wrong path format failed:

```
Property.SetAssetProperty(PropertyPath="VectorParameterValues(0).ParameterValue", ...)
→ InvalidParams: invalid character at index 21
```

Corrected to bracket notation:

```
Property.SetAssetProperty(
  PropertyPath="VectorParameterValues[0].ParameterValue",
  Value="(R=1.0,G=0.0,B=0.0,A=1.0)"
)
→ Success. Previous=(R=0.051,...) New=(R=1.0,G=0.0,B=0.0,A=1.0)
```

### Visual confirmation

After save, the first viewport capture still showed the old color — the render had not
propagated yet. The AI reopened the asset, waited for shader compilation, then recaptured:

> **Screenshot 2** — floor is red. Phase 1 complete.

---

## Phase 2 — Blueprint Graph Construction

### Graph layout

The AI listed existing Event Graph nodes to find the `IA_Jump` event, then planned
new node positions to its right.

```
ListGraphNodes(TabId="BP_ThirdPersonCharacter", GraphName="EventGraph")
→ 19 nodes. IA_Jump event at (−2800, −480).
```

### Variable-driven workaround for pin literals

Because the current UAIP API does not expose a `SetPinDefaultValue` command, the AI
created Blueprint variables for all numeric and object literals:

| Variable | Type | Default |
|---|---|---|
| `DelayDuration` | Float | `5.0` |
| `TraceDistance` | Float | `−500.0` |
| `EffectSystem` | Object (NiagaraSystem) | `NS_JumpPad` |

### Niagara system search and reference image

```
SearchAssets(ClassNames=["/Script/Niagara.NiagaraSystem"])
→ /Game/ThirdPersonTemplate/LevelPrototyping/.../NS_JumpPad
```

The Niagara asset was opened and captured as a reference image before wiring:

> **Screenshot 3 (reference)** — NS_JumpPad editor: Steam_Burst + Sparks emitters visible.

### Nodes placed (11 total)

| Node | Class | NodeId (prefix) |
|---|---|---|
| LineTraceSingle | KismetSystemLibrary | `CE12A040` |
| GetActorLocation (Start) | Actor | `A7DF0506` |
| GetActorLocation (End) | Actor | `84EADC4C` |
| GetActorUpVector | Actor | `FACA3B49` |
| Multiply\_VectorFloat | KismetMathLibrary | `C2C04124` |
| Add\_VectorVector | KismetMathLibrary | `0BFBAF78` |
| BreakHitResult | GameplayStatics | `438C8D8D` |
| SpawnSystemAtLocation | NiagaraFunctionLibrary | `80CCDE67` |
| Delay | KismetSystemLibrary | `683BA07B` |
| DestroyComponent | ActorComponent | `CFF1771B` |
| VariableGet DelayDuration | — | `11381A40` |

### Wiring

Execution chain:
```
Jump.then → LineTrace.execute → SpawnSystem.execute → Delay.execute → DestroyComponent.execute
```

Data wires (15 connections):
```
GetActorLocation_Start.ReturnValue  → LineTrace.Start
GetActorLocation_End.ReturnValue    → Add.A
GetActorUpVector.ReturnValue        → Multiply.A
TraceDistance(get)                  → Multiply.B
Multiply.ReturnValue                → Add.B
Add.ReturnValue                     → LineTrace.End
LineTrace.OutHit                    → BreakHitResult.Hit
BreakHitResult.Location             → SpawnSystem.Location   ← [L2]
EffectSystem(get)                   → SpawnSystem.SystemTemplate
DelayDuration(get)                  → Delay.Duration
SpawnSystem.ReturnValue             → DestroyComponent.Object
SpawnSystem.ReturnValue             → DestroyComponent.self   ← added after first compile error
```

### Compile

First compile returned:

```
Error: "This blueprint (self) is not an ActorComponent,
        therefore 'Target' must have a connection."
```

The AI connected `SpawnSystem.ReturnValue → DestroyComponent.self`. Second compile:

```
CompileBlueprint → CompileStatus: Success
```

> **Screenshot 4** — BP editor showing the full graph after compile.

---

## Phase 3 — PIE Verification

### Why `uaip_run_scenario` was required

The Niagara effect's visible window is ~5 seconds (the `DelayDuration` variable).
Between separate `uaip_execute` calls there is unavoidable command-pipeline latency
that frequently exceeds several seconds, making it nearly impossible to catch the
effect with individual calls. Bundling all steps inside one `uaip_run_scenario`
submission removes that inter-call gap.

### Scenario shape

```
Steps:
  Settle      — WaitSeconds(1.0)
  JumpPress   — InjectInputKey(SpaceBar, Pressed)
  JumpRelease — InjectInputKey(SpaceBar, Released)
  WaitForSpawn— WaitSeconds(0.7)
  Capture     — CaptureActiveWindowImage
                (Runtime.Observation.CaptureViewportImage was tried first
                 but returned "Splitscreen is not active")
```

One scenario submission produced a clean frame.

### Visual feature match

| Feature | Reference (NS_JumpPad editor) | Final PIE screenshot |
|---|---|---|
| Steam burst ring | Visible at base | Circular ring of bright streaks at ground |
| Spark streams | Vertical streaks | Vertical spark streaks rising from the ring |
| Additive glow | Bright core | Bright core distinct from matte red floor |
| Location | Emitter origin | Spawn point at line trace hit (character's feet) |

Conclusion: effect confirmed at the trace hit point, not just floor color.

> **Screenshot 5 (final)** — character mid-jump, NS_JumpPad effect visible at feet on red floor.

---

## Final report (AI's own summary)

| Check | Result |
|---|---|
| Line Trace By Channel node implemented? | ✅ Yes |
| End = GetActorLocation + (GetActorUpVector × −500)? | ✅ Yes |
| Spawn.Location wired from BreakHitResult.Hit Location? | ✅ Yes |
| Spawn → Delay(5.0) → DestroyComponent present? | ✅ Yes |
| Delay.Duration = 5.0 via variable (not 0.2 default)? | ✅ Yes |
| `uaip_run_scenario` used for Phase 3? | ✅ Yes |
| Scenario submissions to capture clean frame | 1 (first succeeded) |

---

## Appendix: UAIP command surface overview

After Phase 3, the AI was asked to walk through the full command surface.

> *"I just ran `uaip_query_capabilities` and `uaip_list_commands` against the running editor.
> Here's what's actually exposed."*

### Numbers on this build

- **Total commands registered**: ~430 across all domains
- **Capabilities granted**: 41 (`BlueprintGraphEdit`, `MaterialParameterEdit`, `PIEControl`,
  `RuntimeInputInjection`, …)
- **Toolset bridge**: 0 in this session (requires `ToolsetRegistry` plugin)

### Domain breakdown

| Domain | Count | Examples |
|---|---|---|
| Core | 8 | HealthCheck, ListCommands, QueryCapabilities, EndSession |
| Editor.Assets | 11 | CreateAsset, OpenAsset, SearchAssets, DeleteAsset |
| Editor.Level | 7 | OpenLevel, ListLevelActors, PlaceActor, DeleteActor |
| Editor.Workspace | 17 | FocusEditorTab, SaveAllPackages, RestartEditor, Undo/Redo |
| Editor.Property | 11 | GetAssetProperty, SetAssetProperty, GetActorProperty |
| Editor.Blueprint | 18 | AddGraphNode, ConnectBlueprintPins, CompileBlueprint |
| Editor.Observation | 13 | CaptureActiveWindowImage, DumpEditorState, DumpWorldState |
| Editor.UIAutomation | 15 | ClickWidget, FillForm, InvokeContextMenuAction |
| Editor.Material | 10 | Graph editing for Material / MaterialFunction assets |
| Editor.Niagara | ~38 | Emitter / module / parameter editing |
| Editor.Sequencer | ~100 | Track / section / binding editing |
| Editor.ControlRig | ~59 | Hierarchy + RigVM graph editing |
| Editor.AnimBlueprint | 2 | State machine / anim graph editing |
| Editor.BehaviorTree | 7 | BT / Blackboard editing |
| Editor.StateTree | 14 | StateTree editing |
| Editor.PCG | 12 | PCG graph editing |
| … (more) | — | GameplayTags, GameFeatures, UMG, MetaSound, … |
| Runtime.PIE | 5 | StartPIE, StopPIE, PausePIE, LoadMap |
| Runtime.Input | 7 | InjectInputKey, InjectInputAxis, SetInputMode |
| Runtime.Observation | 7 | CaptureViewportImage, DumpWorldState, DumpActorState |
| Runtime.Assertion | 4 | WaitSeconds, WaitForCondition, AssertActorProperty |
| Runtime.GAS | 8 | Observe abilities, attributes, cues |
| Toolset.* | 0 (here) | 190+ when ToolsetRegistry is loaded |

### Safety layer

Two layers gate every call:

1. **Capabilities** (per-session) — observation commands are default-allow; mutations
   (`BlueprintGraphEdit`, `RuntimeInputInjection`, etc.) are default-deny and must be
   explicitly listed in `Config/DefaultUAIP.ini`:
   ```ini
   [UAIP.SafetyPolicy]
   +AllowedCapabilities=BlueprintGraphEdit
   ```
2. **SafetyPolicy** (process-wide) — bool switches like `ReadOnly`, `DisableSave`,
   `AllowKeyboardInput`, `DisablePIEStart` in the same ini. The AI cannot override either layer.

### Transports

| Transport | Opt-in flag | Use case |
|---|---|---|
| MCP | `-uaip-mcp-enable` | AI assistant clients (Claude Code, Cursor, …) |
| HTTP | `-uaip-http-enable` | Scripts, CI pipelines |
| WebSocket | `-uaip-ws-enable` | Long-lived / streaming sessions |
| CLI | (always available) | Headless and cooked builds |

The scenario route (`uaip_run_scenario`) requires the additional flag `-uaip-enable-scenario`.

---

*This session used approximately 20 of the ~430 available commands across Assets, Level,
Property, Blueprint, Workspace, Observation, Runtime.Input, Runtime.PIE, Runtime.Observation,
and Runtime.Assertion.*

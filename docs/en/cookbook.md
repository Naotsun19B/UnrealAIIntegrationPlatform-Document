**[日本語](../ja/cookbook.md)** | [Back to README](../../README.md)

# Examples / Cookbook

Recipes for the most common UAIP workflows. Each recipe is self-contained, names the commands and capabilities involved, and shows what to ask the AI client.

> Most recipes use **scenarios** so that a multi-step procedure runs as one request with abort-on-failure semantics and one bundled response. If you're new to scenarios, see [Scenario Execution](scenario.md).

---

## Quick index

| Recipe | Use case | Demo OK |
|---|---|:---:|
| [1. PIE smoke test](#1-pie-smoke-test) | "Did this map at least start without crashing?" | ✅ |
| [2. AI code / Blueprint review](#2-ai-code--blueprint-review) | Have the AI judge a Blueprint visually + structurally | ✅ |
| [3. Asset audit & naming check](#3-asset-audit--naming-check) | Sweep folders for naming / class violations | ✅ |
| [4. Blueprint edit-verify loop](#4-blueprint-edit-verify-loop) | Add nodes, compile, fix errors | — |
| [5. UI automation test](#5-ui-automation-test) | Drive editor menus / buttons end-to-end | ✅ |
| [6. PIE playtest with captures](#6-pie-playtest-with-captures) | Run, screenshot at checkpoints, assert state | ✅ |
| [7. Run automation tests from CI](#7-run-automation-tests-from-ci-pro) | Headless test execution (Pro only) | — |

Demo OK = works on the demo binary. Others require Pro.

---

## 1. PIE smoke test

**Ask the AI**: "Run a PIE smoke test on `/Game/Maps/MainMenu`."

**Scenario**:

```json
{
  "ScenarioName": "PIE_Smoke_MainMenu",
  "Steps": [
    { "StepName": "Load",   "CommandName": "UAIP.Runtime.PIE.LoadMap",
      "Params": { "MapPath": "/Game/Maps/MainMenu" } },
    { "StepName": "Start",  "CommandName": "UAIP.Runtime.PIE.StartPIE" },
    { "StepName": "Settle", "CommandName": "UAIP.Runtime.Assertion.WaitSeconds",
      "Params": { "Seconds": 3 } },
    { "StepName": "Shot",   "CommandName": "UAIP.Runtime.Observation.CheckpointCapture",
      "Params": { "Label": "after-load" } },
    { "StepName": "Stop",   "CommandName": "UAIP.Runtime.PIE.StopPIE",
      "AbortOnFailure": false }
  ]
}
```

**What you get**: a checkpoint artifact (screenshot + JSON dump) you can `Read` after the run. If any step before `Stop` fails, the scenario aborts but `Stop` still runs (`AbortOnFailure: false` on the cleanup step) so PIE isn't left running.

**Capabilities**: `PIEControl`, `RuntimeCapture` — both DefaultAllow.

---

## 2. AI code / Blueprint review

**Goal**: have the AI evaluate a Blueprint's logic flow and visual state.

**Single-call workflow**:

1. Open the asset:
   `uaip_execute(CommandName="UAIP.Editor.Assets.OpenAsset", Params={"AssetPath": "/Game/Blueprints/BP_PlayerCharacter"})`
2. Normalize the layout so the screenshot is reproducible:
   `uaip_execute(CommandName="UAIP.Editor.Workspace.NormalizeEditorLayout")`
3. Capture the graph:
   `uaip_execute(CommandName="UAIP.Editor.Observation.CaptureGraphViewportImage", Params={"TabId": "/Game/Blueprints/BP_PlayerCharacter"})`
4. Dump the graph structurally:
   `uaip_execute(CommandName="UAIP.Editor.Blueprint.ListBlueprintPins", Params={...})`

Then ask the AI: "Review this Blueprint — look for unconnected execution pins, missing null checks on the cast nodes, and any dangling event nodes."

**Demo note**: capture commands embed a `UAIP Demo` watermark in the output PNG. The AI can still see the layout and evaluate it.

**Capabilities**: `EditorObservation`, `EditorInspect` — DefaultAllow.

---

## 3. Asset audit & naming check

**Goal**: find all `BP_*` Blueprints under a folder and confirm they match a naming convention.

**Single-call workflow**:

```
uaip_execute(
  CommandName="UAIP.Editor.Assets.SearchAssets",
  Params={
    "Path": "/Game/Characters",
    "ClassNames": ["Blueprint"],
    "Recursive": true
  }
)
```

The JSON artifact lists all matching assets. Hand it to the AI: "Find Blueprints whose name doesn't start with `BP_`, doesn't end with `_Character`, or has a path component that isn't PascalCase."

For dependency-style audits (unused assets, circular references, size maps), see [Roadmap → Asset Audit](roadmap.md#asset-audit--dependency-analysis) — these are planned but not yet implemented.

**Capabilities**: `EditorInspect` — DefaultAllow.

---

## 4. Blueprint edit-verify loop

**Goal**: add a member variable to a Blueprint, wire up a node graph, save, and verify.

**Scenario**:

```json
{
  "ScenarioName": "BP_AddHealth",
  "Steps": [
    { "StepName": "AddVar", "CommandName": "UAIP.Editor.Blueprint.AddBlueprintVariable",
      "Params": {
        "BlueprintPath": "/Game/Blueprints/BP_PlayerCharacter",
        "VariableName":  "Health",
        "PinCategory":   "real",
        "PinSubCategory":"double",
        "DefaultValue":  "100.0"
      } },
    { "StepName": "AddGet", "CommandName": "UAIP.Editor.Blueprint.AddGraphNode",
      "Params": {
        "BlueprintPath": "/Game/Blueprints/BP_PlayerCharacter",
        "NodeKind":      "VariableGet",
        "VariableName":  "Health",
        "NodeX": 0, "NodeY": 200
      } },
    { "StepName": "Inspect", "CommandName": "UAIP.Editor.Blueprint.ListBlueprintPins",
      "Params": {
        "BlueprintPath": "/Game/Blueprints/BP_PlayerCharacter",
        "NodeId":        "${AddGet.Data.NodeId}"
      } },
    { "StepName": "Save",   "CommandName": "UAIP.Editor.Workspace.SaveAllPackages" }
  ]
}
```

After save, ask the AI to inspect the Blueprint graph visually with `CaptureGraphViewportImage` and confirm the wiring matches intent. A dedicated `CompileBlueprint` command with structured error retrieval is planned — see [Roadmap → Blueprint Compile & Error Retrieval](roadmap.md#blueprint-compile--error-retrieval).

**Capabilities**: `BlueprintEdit`, `BlueprintVariableEdit`, `BlueprintGraphEdit` — all **DefaultDenied**. Add to `Config/DefaultUAIP.ini`:

```ini
[UAIP.SafetyPolicy]
+AllowedCapabilities=BlueprintEdit
+AllowedCapabilities=BlueprintVariableEdit
+AllowedCapabilities=BlueprintGraphEdit
```

Pro only — Blueprint editing modules are not in the demo binary.

---

## 5. UI automation test

**Goal**: open the Project Settings dialog from the menu and confirm a specific tab appears.

```json
{
  "ScenarioName": "OpenProjectSettings",
  "Steps": [
    { "StepName": "Menu",  "CommandName": "UAIP.Editor.UIAutomation.SelectMenuItem",
      "Params": { "MenuPath": "Edit/Project Settings" } },
    { "StepName": "Wait",  "CommandName": "UAIP.Editor.UIAutomation.WaitForWidget",
      "Params": { "WidgetPath": "Window:Project Settings", "TimeoutSeconds": 10 } },
    { "StepName": "Shot",  "CommandName": "UAIP.Editor.Observation.CaptureActiveWindowImage" }
  ]
}
```

The AI can `Read` the screenshot to verify the dialog actually appeared. For interactive flows, chain `ClickWidget`, `InputText`, `SetComboSelection`, and `AcceptDialog`.

**Capabilities**: `EditorUIAutomation` — DefaultAllow. Some sub-features need explicit opt-in: `EditorKeyboardInput` for `PressKey`, `AllowContextMenuMutation` for `InvokeContextMenuAction`. See [Safety & Capabilities](safety.md).

---

## 6. PIE playtest with captures

**Goal**: load a level, start PIE, take screenshots at fixed time intervals, and assert on a property.

```json
{
  "ScenarioName": "PlaytestCharacterMove",
  "Variables": { "ExpectedHealth": 100 },
  "Steps": [
    { "StepName": "Load",  "CommandName": "UAIP.Runtime.PIE.LoadMap",
      "Params": { "MapPath": "/Game/Maps/TestArena" } },
    { "StepName": "Play",  "CommandName": "UAIP.Runtime.PIE.StartPIE" },
    { "StepName": "T0",    "CommandName": "UAIP.Runtime.Observation.CheckpointCapture",
      "Params": { "Label": "t0" } },
    { "StepName": "Wait1", "CommandName": "UAIP.Runtime.Assertion.WaitSeconds",
      "Params": { "Seconds": 5 } },
    { "StepName": "T5",    "CommandName": "UAIP.Runtime.Observation.CheckpointCapture",
      "Params": { "Label": "t5" } },
    { "StepName": "Check", "CommandName": "UAIP.Runtime.Assertion.AssertActorProperty",
      "Params": {
        "ActorIdentifier": "PlayerCharacter",
        "PropertyName":    "Health",
        "ExpectedValue":   "${Variables.ExpectedHealth}"
      } },
    { "StepName": "Stop",  "CommandName": "UAIP.Runtime.PIE.StopPIE", "AbortOnFailure": false }
  ]
}
```

Compare the two CheckpointCapture artifacts — different position / lighting / state at the two times — so the AI can describe what changed.

**Capabilities**: `PIEControl`, `RuntimeCapture`, `RuntimeInspect` — DefaultAllow.

---

## 7. Run automation tests from CI (Pro)

UAIP can be invoked from CI / CD pipelines via the **CLI transport** (Pro only). The editor processes one request and exits, which works for headless test execution.

### Example (PowerShell on a Windows GitHub Actions runner)

```powershell
# 1. Write the request as JSON
@'
{
  "CommandName": "UAIP.Editor.Execution.RunAutomationTest",
  "Params": {
    "TestName": "MyGame.Smoke.MainMenu",
    "RunAllMatching": false
  }
}
'@ | Set-Content cmd.json

# 2. Run the editor with the CLI transport
& "C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe" `
    "$pwd/MyGame.uproject" `
    "-uaip-request-file=$pwd/cmd.json" `
    "-uaip-response-file=$pwd/result.json"

# 3. Inspect the JSON result, fail the CI step if not Success
$r = Get-Content result.json | ConvertFrom-Json
if (-not $r.Success) { exit 1 }
```

The same pattern works for `RunAutomationSpec`, `RunFunctionalTest`, and `RunGauntletTest`.

### Caveats

- **Editor startup is slow** (often 30–90 s in CI). Plan for it.
- **Demo doesn't support CLI** — the demo binary is MCP-only. CI needs Pro.
- **Headless / `-nullrhi`** disables capture commands. If you need screenshots in CI, plan for a real GPU runner.
- See [Roadmap → Build & Package Pipeline](roadmap.md#build--package-pipeline) for richer CI integration that's planned but not yet shipped.

---

## Patterns worth knowing

- **Scenario templates** (`${StepName.Data.x}`, `${Variables.y}`) let later steps consume earlier-step output. See [Scenario Execution → Templates](scenario.md#4-templates---splice-earlier-results-into-later-steps).
- **Default `AbortOnFailure: true`** stops the scenario at the first failed step. Override to `false` on cleanup steps so they run even if PIE / asset operations fail mid-flight.
- **Capture commands return artifact IDs, not file paths**. Use `Read` on the artifact's `FilePath` (returned in the response) to view PNG / JSON output. See [Artifacts](artifacts.md).
- **Sessions isolate work**. Pass `SessionId="my-test"` to keep artifacts grouped per task — they're stored under `Saved/UAIP/<session>/`.
- **Self-verify before asking the user** — if you wonder "did this work?", call a Capture or Dump command before pinging the user.

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
      "Params": { "MapPath": "/Game/Maps/MainMenu" }, "AbortOnFailure": false },
    { "StepName": "Start",  "CommandName": "UAIP.Runtime.PIE.StartPIE",
      "AbortOnFailure": false },
    { "StepName": "Settle", "CommandName": "UAIP.Runtime.Assertion.WaitSeconds",
      "Params": { "Seconds": 3 }, "AbortOnFailure": false },
    { "StepName": "Shot",   "CommandName": "UAIP.Runtime.Observation.CheckpointCapture",
      "Params": { "Label": "after_load" }, "AbortOnFailure": false },
    { "StepName": "Stop",   "CommandName": "UAIP.Runtime.PIE.StopPIE" }
  ]
}
```

**What you get**: a checkpoint artifact (screenshot + JSON dump) you can `Read` after the run.

**Why every step carries `AbortOnFailure: false`**: the flag is evaluated on the step that **failed**, not on the steps after it. If `Load` … `Shot` kept the default `true`, the first failure would finalize the scenario and `Stop` would never be dispatched — PIE left running. Marking the earlier steps `false` is what makes `Stop` reachable; the price is that the scenario no longer stops at the first failure, so read `StepResults` to find it. See [Scenario Execution → Failure handling and cleanup](scenario.md#failure-handling-and-cleanup).

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
   `uaip_execute(CommandName="UAIP.Editor.Observation.CaptureGraphViewportImage", Params={"TabId": "BP_PlayerCharacter"})`
4. List the graph's nodes, and read the `NodeId` (the NodeGuid) of the node you want from the artifact. Each entry also carries `NodeClass`, `NodeTitle`, and `Position`:
   `uaip_execute(CommandName="UAIP.Editor.Observation.ListGraphNodes", Params={"TabId": "BP_PlayerCharacter"})`
5. Dump the pins of that node:
   `uaip_execute(CommandName="UAIP.Editor.Blueprint.ListBlueprintPins", Params={"BlueprintPath": "/Game/Blueprints/BP_PlayerCharacter", "NodeId": "<NodeId read from the ListGraphNodes artifact>"})`

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
    "PackagePath": "/Game/Characters",
    "ClassNames": ["/Script/Engine.Blueprint"],
    "Recursive": true
  }
)
```

The JSON artifact lists all matching assets. Hand it to the AI: "Find Blueprints whose name doesn't start with `BP_`, doesn't end with `_Character`, or has a path component that isn't PascalCase."

For dependency-style audits (unused assets, circular references, broken references, size maps), see the audit commands under [Commands → `UAIP.Editor.Assets`](commands.md#uaipeditorassets). The folder-wide audit runs as a job: `StartAssetAudit` returns an id straight away and the scan advances between editor frames, `GetAssetAuditStatus` reports how far it has got, and `GetAssetAuditResult` returns one artifact per report. All three need the same explicit `SessionId`.

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
        "VarName":       "Health",
        "VarType":       "Float",
        "DefaultValue":  "100.0"
      } },
    { "StepName": "AddGet", "CommandName": "UAIP.Editor.Blueprint.AddGraphNode",
      "Params": {
        "BlueprintPath": "/Game/Blueprints/BP_PlayerCharacter",
        "NodeType":      "VariableGet",
        "VarName":       "Health",
        "NodeX": 0, "NodeY": 200
      } },
    { "StepName": "Save",   "CommandName": "UAIP.Editor.Workspace.SaveAllPackages" }
  ]
}
```

`AddGraphNode` writes the new node's `NodeId` to its artifact only, not to the step's `Data`, so a `${AddGet.Data.NodeId}` template cannot carry it into a later step. Verify in two stages instead:

1. Read the `NodeId` of the new node from the artifact of the `AddGet` step.
2. In a separate call, pass it on:
   `uaip_execute(CommandName="UAIP.Editor.Blueprint.ListBlueprintPins", Params={"BlueprintPath": "/Game/Blueprints/BP_PlayerCharacter", "NodeId": "<NodeId read from the artifact>"})`

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

**Goal**: open the Project Settings dialog from the menu, capture the screen so the AI can check that it appeared, and take a snapshot of the UI that yields the `WidgetRef` of each widget.

```json
{
  "ScenarioName": "OpenProjectSettings",
  "Steps": [
    { "StepName": "Menu",   "CommandName": "UAIP.Editor.UIAutomation.SelectMenuItem",
      "Params": { "MenuPath": "Edit/Project Settings..." } },
    { "StepName": "Settle", "CommandName": "UAIP.Runtime.Assertion.WaitSeconds",
      "Params": { "Seconds": 2 } },
    { "StepName": "Snap",   "CommandName": "UAIP.Editor.UIAutomation.SnapshotUI" },
    { "StepName": "Shot",   "CommandName": "UAIP.Editor.Observation.CaptureActiveWindowImage" }
  ]
}
```

The AI can `Read` the screenshot to verify the dialog actually appeared.

**Waiting for a widget** takes two separate calls, because a `WidgetRef` is issued by `SnapshotUI` and cannot be spliced into the same scenario. A ref is scoped to the session (pass the same `SessionId` to both calls) and expires after 60 seconds, so make the second call soon after the first.

1. Call `SnapshotUI` and read the `WidgetRef` of the widget you want from its artifact — it is the `Ref` field of that widget's entry (the `Snap` step above does this).
2. In a separate call, pass that ref to `WaitForWidget`:

```json
{
  "WidgetRef":          "<ref read from the SnapshotUI artifact>",
  "ExpectedState":      "Visible",
  "WaitTimeoutSeconds": 10
}
```

If the ref has expired, call `SnapshotUI` again to get a fresh one.

For interactive flows, chain `ClickWidget`, `InputText`, `SetComboSelection`, and `AcceptDialog`.

**Capabilities**: `EditorUIAutomation` — DefaultAllow. Some sub-features need explicit opt-in: `EditorKeyboardInput` for `PressKey`, `AllowContextMenuMutation` for `InvokeContextMenuAction`. See [Safety & Capabilities](safety.md).

---

## 6. PIE playtest with captures

**Goal**: load a level, start PIE, take screenshots at fixed time intervals, and assert on a property.

```json
{
  "ScenarioName": "PlaytestCharacterMove",
  "Variables": { "ExpectedHealth": "100" },
  "Steps": [
    { "StepName": "Load",  "CommandName": "UAIP.Runtime.PIE.LoadMap",
      "Params": { "MapPath": "/Game/Maps/TestArena" }, "AbortOnFailure": false },
    { "StepName": "Play",  "CommandName": "UAIP.Runtime.PIE.StartPIE",
      "AbortOnFailure": false },
    { "StepName": "T0",    "CommandName": "UAIP.Runtime.Observation.CheckpointCapture",
      "Params": { "Label": "t0" }, "AbortOnFailure": false },
    { "StepName": "Wait1", "CommandName": "UAIP.Runtime.Assertion.WaitSeconds",
      "Params": { "Seconds": 5 }, "AbortOnFailure": false },
    { "StepName": "T5",    "CommandName": "UAIP.Runtime.Observation.CheckpointCapture",
      "Params": { "Label": "t5" }, "AbortOnFailure": false },
    { "StepName": "Check", "CommandName": "UAIP.Runtime.Assertion.AssertActorProperty",
      "Params": {
        "ActorIdentifier": "PlayerCharacter",
        "PropertyName":    "Health",
        "ExpectedValue":   "${Variables.ExpectedHealth}"
      }, "AbortOnFailure": false },
    { "StepName": "Stop",  "CommandName": "UAIP.Runtime.PIE.StopPIE" }
  ]
}
```

Compare the two CheckpointCapture artifacts — different position / lighting / state at the two times — so the AI can describe what changed.

Every step before `Stop` is marked `AbortOnFailure: false` for the same reason as recipe 1: without it, the first failure ends the scenario and `Stop` never runs. The assertion result is still visible in `StepResults[].Success` for the `Check` step.

**Capabilities**: `PIEControl`, `RuntimeCapture`, `RuntimeInspect` — DefaultAllow.

---

## 7. Run automation tests from CI (Pro)

UAIP can be invoked from CI / CD pipelines via the **CLI transport** (Pro only). The editor processes one request and exits, which works for headless test execution.

### Example (PowerShell on a Windows GitHub Actions runner)

Run it from the project root.

```powershell
# 1. Write the request as JSON (requests are only read from under Saved/UAIP/Requests/)
New-Item -ItemType Directory -Force Saved/UAIP/Requests, Saved/UAIP/Responses | Out-Null
@'
{
  "Command": "UAIP.Editor.Execution.RunAutomationTest",
  "Params": {
    "TestName": "MyGame.Smoke.MainMenu",
    "RunAllMatching": false
  }
}
'@ | Set-Content Saved/UAIP/Requests/cmd.json

# 2. Run the editor with the CLI transport and wait for it to exit
Start-Process -Wait -FilePath "C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe" -ArgumentList @(
    "`"$pwd/MyGame.uproject`"",
    "-uaip-request-file=Saved/UAIP/Requests/cmd.json",
    "-uaip-response-file=Saved/UAIP/Responses/result.json"
)

# 3. Inspect the JSON result, fail the CI step if not Success
$r = Get-Content Saved/UAIP/Responses/result.json | ConvertFrom-Json
if (-not $r.Success) { exit 1 }
```

- The request names the command under the key `Command` (not `CommandName`, which is the argument name of the MCP tool `uaip_execute`).
- The request file must be under `Saved/UAIP/Requests/` and the response file under `Saved/UAIP/Responses/`, passed as paths relative to the project root.
- `UnrealEditor.exe` is a GUI application, so calling it with PowerShell's `&` returns without waiting for it to exit. `Start-Process -Wait` waits before the result is read.

The same pattern works for `RunAutomationSpec`, `RunFunctionalTest`, and `RunGauntletTest`.

### Caveats

- **Editor startup is slow** (often 30–90 s in CI). Plan for it.
- **Demo doesn't support CLI** — the demo binary is MCP-only. CI needs Pro.
- **Headless / `-nullrhi`** disables capture commands. If you need screenshots in CI, plan for a real GPU runner.
- See [Roadmap → Build & Package Pipeline](roadmap.md#build--package-pipeline) for richer CI integration that's planned but not yet shipped.

---

## Patterns worth knowing

- **Scenario templates** (`${StepName.Data.x}`, `${Variables.y}`) let later steps consume earlier-step output. See [Scenario Execution → Templates](scenario.md#4-templates---splice-earlier-results-into-later-steps).
- **Default `AbortOnFailure: true`** stops the scenario at the first failed step. The flag is read on the step that **failed**, so setting it to `false` only on a trailing cleanup step does nothing — that step is skipped too. To reach the cleanup step, mark every step before it `false`; otherwise clean up with a separate call after the scenario returns. See [Scenario Execution → Failure handling and cleanup](scenario.md#failure-handling-and-cleanup).
- **Capture commands return artifact IDs, not file paths**. Use `Read` on the artifact's `FilePath` (returned in the response) to view PNG / JSON output. See [Artifacts](artifacts.md).
- **Sessions isolate work**. Pass `SessionId="my-test"` to keep artifacts grouped per task — they're stored under `Saved/UAIP/<session>/`.
- **Self-verify before asking the user** — if you wonder "did this work?", call a Capture or Dump command before pinging the user.

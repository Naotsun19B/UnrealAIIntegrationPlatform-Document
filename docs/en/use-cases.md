**[日本語](../ja/use-cases.md)** | [Back to README](../../README.md)

# Use Cases

Who uses UAIP, for what, and why. Each scenario links to the relevant Cookbook recipe and the capabilities you'll need.

> If you're looking for copy-pasteable JSON, jump to [Cookbook](cookbook.md). This page is the "why and when" side.

---

## 1. AI pair programming on the editor side

**Who**: solo devs and small teams using Claude Code / Cursor / Copilot as their primary IDE. This is the main use case UAIP is built for.

**Problem**: the AI is great at producing C++ patches, but for the Blueprint side of UE projects it goes blind. "Hook this widget up to that event" can't be done in source — the BP graph is the source.

**What UAIP gives them**:
- `UAIP.Editor.Blueprint.*` to add variables, nodes, and wire pins
- `UAIP.Editor.UMG.*` to edit widget trees, animations, bindings
- `UAIP.Editor.Level.*` to place actors and tweak transforms
- `UAIP.Editor.Property.*` for setting fields on assets and actors
- `CompileBlueprint` + error retrieval (planned, see [Roadmap → Blueprint Compile](roadmap.md#blueprint-compile--error-retrieval)) to close the edit-verify loop

**Capabilities**: `BlueprintEdit`, `BlueprintGraphEdit`, `BlueprintVariableEdit`, `WidgetTreeEdit`, `EditorActorEdit`, `PropertyEdit` — all DefaultDenied. Enable only what your workflow actually needs (see [Security → Full editing profile](security.md#recommended-hardening-profiles)).

**Pro only** — editing modules are not in the demo binary.

**Cookbook**: [Blueprint edit-verify loop](cookbook.md#4-blueprint-edit-verify-loop).

---

## 2. AI-driven test authoring & QA

**Who**: QA / test automation engineers, gameplay programmers who own playtest scripts.

**Problem**: writing every PIE smoke test by hand is slow, and the tests rot fast as level layouts shift. AI agents are good at "given this map, drive the player around and report anomalies", but only if they can actually drive the game.

**What UAIP gives them**:
- `UAIP.Runtime.PIE.*` to start / stop / load maps
- `UAIP.Runtime.Input` and `UAIP.Editor.UIAutomation.*` for actual controls
- `UAIP.Runtime.Observation.CheckpointCapture` to leave screenshot + state evidence at fixed points
- `UAIP.Runtime.Assertion.AssertActorProperty` / `AssertWorldState` for declarative postconditions
- Scenarios so the whole thing is one auditable record

**Capabilities**: `PIEControl`, `RuntimeCapture`, `RuntimeInspect` (all DefaultAllow), `RuntimeActorManipulation` and `RuntimeInputInjection` if you need to drive characters.

**Cookbook**: [PIE smoke test](cookbook.md#1-pie-smoke-test), [PIE playtest with captures](cookbook.md#6-pie-playtest-with-captures).

---

## 3. AI code review & Blueprint review

**Who**: lead programmers, anyone running an LLM as the first reviewer on a PR.

**Problem**: code review on a Blueprint-heavy project is hard — graphs are visual, diff tools don't help much, and "did anything important change?" requires opening the editor. Asking a human to open every changed BP is wasteful for simple PRs.

**What UAIP gives them**:
- `UAIP.Editor.Assets.OpenAsset` to bring the BP into focus
- `UAIP.Editor.Workspace.NormalizeEditorLayout` so screenshots are reproducible
- `UAIP.Editor.Observation.CaptureGraphViewportImage` so the AI sees the graph
- `UAIP.Editor.Blueprint.ListBlueprintPins` so the AI can reason structurally instead of pixel-by-pixel
- `UAIP.Editor.Observation.DumpEditorState` so the AI knows what else is open

**Capabilities**: `EditorInspect`, `EditorObservation`, `EditorWorkspaceControl` — all DefaultAllow. **No write capabilities needed** — the demo binary is enough.

**Cookbook**: [AI code / Blueprint review](cookbook.md#2-ai-code--blueprint-review).

---

## 4. Asset audit & cleanup

**Who**: tech artists, content leads, anyone enforcing project conventions.

**Problem**: at scale, "BP_FooBar should be in `/Characters/Heroes/`, not `/Misc/`" rules drift constantly. Identifying violations across a 5000-asset project is a script-writing job. The script keeps breaking when the editor changes.

**What UAIP gives them**:
- `UAIP.Editor.Assets.SearchAssets` to enumerate by path / class / tag
- `UAIP.Editor.Property.GetAssetProperty` to inspect specific fields
- `UAIP.Editor.GameplayTags.FindGameplayTagReferencers` to walk tag usage
- A semantic command surface that survives editor UI changes

**Capabilities**: `EditorInspect` (DefaultAllow). Add `AssetDelete` / `AssetFolderRefactor` if you want the AI to also fix violations, not just report them.

**Cookbook**: [Asset audit & naming check](cookbook.md#3-asset-audit--naming-check).

**Roadmap-adjacent**: deeper dependency analysis (unused-asset detection, circular references, size maps) is planned but not yet implemented. See [Roadmap → Asset Audit](roadmap.md#asset-audit--dependency-analysis).

---

## 5. UI automation tests for editor extensions

**Who**: plugin authors, tools programmers building editor utilities.

**Problem**: testing custom editor tools means clicking menus, filling forms, and verifying dialogs come up. Manual every release; brittle if scripted with screen coordinates.

**What UAIP gives them**:
- `SelectMenuItem`, `ClickWidget`, `InputText`, `SetCheckboxState`, `SetComboSelection` for input
- `WaitForWidget` for synchronization (no `Sleep` hacks)
- `AcceptDialog` / `CancelDialog` for modal handling
- `CaptureActiveWindowImage` for visual regression evidence

**Capabilities**: `EditorUIAutomation` (DefaultAllow). `EditorKeyboardInput` for `PressKey`. `AllowContextMenuMutation` for `InvokeContextMenuAction`.

**Cookbook**: [UI automation test](cookbook.md#5-ui-automation-test).

---

## 6. Procedural content workflows

**Who**: PCG users, procedural artists, technical designers.

**Problem**: tweaking PCG node parameters is iterative — change a value, regenerate, check the result, repeat. Doing this from the editor by hand is fine for one node; doing it across a graph of dozens is tedious.

**What UAIP gives them**:
- `UAIP.Editor.PCG.GetPCGGraphInfo` to read graph structure
- `UAIP.Editor.PCG.SetPCGNodeProperty` to change parameters
- `UAIP.Editor.PCG.ExecutePCGGraph` to regenerate
- `CaptureViewportImage` / `DumpWorldState` to verify the result
- Scenarios to parameter-sweep across a value range with screenshots at each step

**Capabilities**: `PCGGraphEdit` (DefaultDenied, requires `PCG` plugin). `PCGCustomNodeEdit` / `PCGBlueprintNodeEdit` for custom node properties.

**Pro only** — PCG editing is not in the demo.

---

## 7. Animation pipeline integration

**Who**: animation tech artists, AnimBlueprint owners, ControlRig users.

**Problem**: complex anim trees are big and the relationships between AnimGraph states, State Machine transitions, ControlRig rigs, and Sequencer cinematics are easy to break. Visual verification is necessary, but doing it for every change is impractical.

**What UAIP gives them**:
- `UAIP.Editor.AnimBlueprint.*` for AnimGraph + StateMachine editing
- `UAIP.Editor.ControlRig.*` for hierarchy and RigVM graph editing (59 native + 44 Toolset commands)
- `UAIP.Editor.Sequencer.*` for LevelSequence editing (93 native + 61 Toolset commands)
- `UAIP.Editor.Skeleton.*` for socket / virtual bone management
- `UAIP.Editor.Physics.*` for physics asset tuning
- Runtime checks via `UAIP.Runtime.PIE.*` and Anim observation (planned, see [Roadmap → AnimInstance Runtime State](roadmap.md#animinstance-runtime-state))

**Capabilities**: `AnimBlueprintGraphEdit`, `AnimStateMachineEdit`, `ControlRigGraphEdit`, `ControlRigHierarchyEdit`, `SequencerStructureEdit`, `SequencerKeyframeEdit`, `SkeletonAssetEdit`, `PhysicsAssetEdit`, `PhysicsBodyEdit` — all DefaultDenied.

**Pro only**.

---

## 8. Multiplayer & gameplay-systems debugging

**Who**: gameplay programmers chasing PIE-only bugs.

**Problem**: "this works in standalone but breaks in multiplayer" or "AI doesn't perceive the player when X happens". Repro requires PIE; bug analysis requires reading replicated state, AI perception state, BehaviorTree active nodes, GameplayAbility state, etc. Doing it through the editor's debug UIs is one perspective at a time.

**What UAIP gives them**:
- `UAIP.Runtime.Observation.DumpWorldState` for the global picture
- `UAIP.Runtime.GAS.*` for ability / attribute / effect inspection
- Planned: AI Perception, BT / StateTree runtime state, AnimInstance state, Network / Replication state ([Roadmap → Runtime Inspection](roadmap.md#runtime--inspection--debugging))
- Scenarios to reproduce the bad state and capture evidence in one shot

**Capabilities**: `PIEControl`, `RuntimeInspect`, `RuntimeGASInspect` (all DefaultAllow). Editing requires `RuntimeActorManipulation`.

---

## 9. Content compliance / pre-submit gates

**Who**: build engineers, internal tools maintainers.

**Problem**: "did anyone commit a Blueprint that fails to compile" or "did anyone add an asset to `/Game/Tests/`" — should be a pre-submit gate, but writing the gate in C++ means cooking a custom commandlet. Slow to iterate, slow to roll out.

**What UAIP gives them**:
- CLI transport (Pro) for headless one-shot runs in pre-submit hooks / CI
- `UAIP.Editor.Execution.RunAutomationTest` for the test side
- Planned: `ValidateAsset` / `ValidateFolder` ([Roadmap → Asset Validation](roadmap.md#asset-validation))
- Planned: Build & Package pipeline ([Roadmap → Build & Package Pipeline](roadmap.md#build--package-pipeline))

**Capabilities**: `EditorInspect`, `EditorExecution` (DefaultAllow).

**Cookbook**: [Run automation tests from CI (Pro)](cookbook.md#7-run-automation-tests-from-ci-pro).

**Reality check**: CI integration today is workable but rough (slow editor startup, demo doesn't support CLI, validation primitives are still on the roadmap). Use this for build-validation style use cases, not for sub-second per-commit linting.

---

## 10. Live ops / data-driven balancing

**Who**: gameplay designers, live-ops engineers.

**Problem**: gameplay constants live in DataTables, Blueprint defaults, and project settings. Iterating on balance requires the engineer to either edit each by hand or write one-off tools.

**What UAIP gives them**:
- `UAIP.Editor.DataTable.*` for row CRUD and CSV import / export
- `UAIP.Editor.Property.GetBlueprintDefault` / `SetBlueprintDefault` for CDO tweaks
- `UAIP.Editor.Property.GetProjectSetting` / `SetProjectSetting` for `UDeveloperSettings`-backed configs
- `UAIP.Runtime.GAS.*` for verifying the effect on attribute / ability state in PIE

**Capabilities**: `DataTableRowEdit`, `DataTableImport`, `BlueprintEdit`, `ProjectConfigEdit` — DefaultDenied.

**Pro only**.

---

## When **not** to use UAIP

- **Production user-facing automation** — UAIP is built for dev / CI, not for steering shipped games. Use the engine's own subsystems (Gameplay Abilities, online services, etc.) for runtime gameplay.
- **Sub-second iteration loops** — editor startup is slow. If you need 10 ms response, write a UE plugin directly.
- **Replacing your IDE** — UAIP doesn't edit C++ source. Keep using your IDE for code changes; use UAIP for the parts of the project that live inside the editor.
- **Multi-tenant deployment** — UAIP is single-editor-per-project. Don't try to share one bridge across many concurrent users.
- **Bare public-network exposure** — HTTP FullHTTP is intentionally reachable from another machine via Bearer token + firewall, but UAIP is designed for developer machines and trusted internal CI, not direct internet exposure. If you need cross-network access, put it behind a VPN, reverse proxy, or IP allowlist at the operator level. See [Security → Threat model](security.md#threat-model).

---

## Related reading

- [Quickstart](quickstart.md) — set up in 5 minutes
- [Cookbook](cookbook.md) — copy-pasteable recipes
- [Demo Version Guide](demo.md) — what's available without Pro
- [Roadmap](roadmap.md) — what's planned
- [Security](security.md) — how to harden a deployment

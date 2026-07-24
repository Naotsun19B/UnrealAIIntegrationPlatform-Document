**[日本語](../ja/roadmap.md)** | [Back to README](../../README.md)

# Roadmap

Items below are planned or under investigation. No specific release dates are committed and the list is subject to change based on user demand and API stability in upstream UE versions.

> **Shipped in 1.1.0.** Several features previously listed here — Foliage, World Partition / DataLayer / HLOD, MVVM, Sound architecture, Config Settings, Data Registry, Plugin management, extended PCG, Chaos Cloth, asset audit / Asset Manager / redirector fixup, console variable management, viewport coordinate conversion, visible actor query, and log verbosity control (plus Semantic Search, partially — its embedding pipeline is still Epic-internal) — have shipped and moved to the [Changelog](changelog.md). They are no longer listed below.

---

## Engine Version Support

### Backward compatibility to UE 5.6 and earlier
UAIP currently targets UE 5.7 and 5.8. Support for UE 5.6 and older versions is under evaluation for a future release. Demand for UE 5.5 and earlier will be assessed separately.

### Linux / macOS Support
UAIP currently supports Windows (Win64) only. Linux and macOS support is under evaluation and will be considered when sufficient demand and a suitable test environment are available.

---

## Editor — Asset & Project Management

### Asset Validation
Run registered `UEditorValidatorSubsystem` validators on individual assets or folders. Results are returned as structured JSON artifacts.

### Localization Pipeline
Automate the full localization workflow: gather source text, compile localization data, manage cultures, add/edit/remove string table entries, and switch editor display language for verification.

### Build & Package Pipeline
Cook content, package projects, and run Project Launcher profiles through AI commands. Long-running operations include progress reporting and cancellation.

---

## Editor — Editing Domain Extensions

### MetaHuman Editing
Edit MetaHuman body, face, skin, eye, and hair parameters through `MetaHumanCharacterEditorSubsystem` — for projects using the MetaHuman Character plugin. Long-running operations include progress reporting. Requires the `MetaHuman Character` plugin and **UE 5.8 or newer**.

### Material Validation & Templates
Validate materials against project rules, find similar materials to prevent duplication, and create materials from workflow templates.

### Mixed Control Rig Tracks
Add Mixed Control Rig tracks to Level Sequences (the AnimMixer pieces are already shipped; this covers the remaining `MovieSceneMixedControlRig` native commands).

### Motion Matching (PoseSearch)
Manage PoseSearchDatabase contents, schema settings, and normalization parameters for projects adopting UE's Motion Matching system.

### Chaos Destruction (Geometry Collection)
Edit Geometry Collection assets — fracture meshes, configure damage thresholds, and inspect cluster structures.

### Groom (Strand-Based Hair)
Configure Groom Assets — simulation parameters, LOD settings, and SkeletalMesh bindings.

### Additional Optional Graph Editors
- **Subsonic for MetaSound** (UE 5.8): event-driven audio integration
- **ControlRig Dynamics** (UE 5.8): simple physics simulation nodes inside ControlRig graphs
- **AnimationLayering / UAF** (UE 5.8): bone-mask layers and Unified Animation Framework node operations
- **MeshPartition (MegaMesh)** (UE 5.8): spatial partition and non-destructive modifiers on large meshes
- **Enhanced Input Debugging** (UE 5.8): dump the current Enhanced Input / CommonUI input state and fire Input Actions programmatically — powered by the `PlayerInputDebugger` plugin
- **CustomizableSequencerTracks**: Blueprint-defined custom Sequencer track type support
- **DataPrep Asset**: execute and inspect DataPrep import-pipeline assets

---

## Runtime — Inspection & Debugging

### BehaviorTree / StateTree Runtime State
Dump the currently active node, transition history, and Blackboard values during PIE — pairs with the existing editor-side BT / StateTree commands to close the design → playtest → debug loop.

### AnimInstance Runtime State
Dump the active state-machine state, blend weights, currently playing montages, and anim curve values for an actor during PIE.

### AI Perception Observation
Dump `UAIPerceptionComponent` sensor states, currently perceived actors, and stimuli emitted by an actor — answers "why didn't the enemy notice?" debugging questions.

### Navigation Runtime Queries
Compute paths between two points, test reachability, dump NavMesh tile coverage, and inspect NavModifier zones — observation-only, no NavMesh editing.

### GameViewport Widget Observation
Dump the widget tree rooted at `UGameViewportClient` (HUD / menus / runtime UI) — narrower and less noisy than the editor-wide `DumpSlateTree`.

### CommonUI Stack Observation
Dump the `UCommonUISubsystem` activatable widget stack — active widget, focus state, current input mode. For CommonUI-based projects only.

### Subsystem Enumeration & State
List registered `UGameInstanceSubsystem` / `UWorldSubsystem` / `ULocalPlayerSubsystem` and dump their `UPROPERTY` values — fills the discovery gap in the current Subsystem inspection workflow.

### Network / Replication Observation
NetConnection stats (RTT, packet loss, bandwidth), NetDriver info, replicated property dump per actor — supports multiplayer debugging.

### Chaos Runtime State
Dump `UGeometryCollectionComponent` cluster state, destruction event log, and Chaos Field System state during PIE — pairs with the editor-side Geometry Collection editing.

### Mass Entity Observation
Dump Mass Entity archetypes, entity counts, and processor execution graphs during PIE — for debugging crowd AI and large-scale entity simulations. Requires the `MassEntity` / `MassGameplay` plugins.

### Performance Insights Tracing
Start and stop UE Trace sessions with channel selection, query frame stats and hitch summaries, and inspect domain-specific traces (HTTP events, Niagara timings, render commands).

### GameplayMessage Subsystem
Listen to and inject `UGameplayMessageSubsystem` messages for event-driven architectures — useful for testing decoupled gameplay systems.

### SaveGame Operations
List, load, save, and delete `USaveGame` slots — enables tests to start from a specific save state and reset to a known baseline.

---

## Infrastructure

### Human-facing Editor GUI
Optional editor tabs for monitoring AI activity: Command History (timeline of commands and responses) and Artifact Viewer (inline preview of screenshots, JSON dumps, and reports).

### EDA Transport
Optional transport for connecting UAIP to Epic's Epic Developer Assistant (EDA), alongside the existing MCP, HTTP, WebSocket, and CLI transports. Depends on Epic publishing a stable `window.eda.*` JavaScript API.

---

> Feature requests and bug reports: open an [Issue](../../issues) in this repository.

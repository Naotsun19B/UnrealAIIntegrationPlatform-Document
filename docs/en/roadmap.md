**[日本語](../ja/roadmap.md)** | [Back to README](../../README.md)

# Roadmap

Items below are planned or under investigation. No specific release dates are committed and the list is subject to change based on user demand and API stability in upstream UE versions.

---

## Engine Version Support

### Backward compatibility to UE 5.5
UAIP currently targets UE 5.7 and 5.8. Support down to approximately UE 5.5 is being actively pursued. Versions below 5.4 will be evaluated based on demand.

---

## Editor — Asset & Project Management

### Sandbox feature
AI-proposed edits are staged in a sandbox and require human approval before being written to disk. All changes can be inspected and selectively accepted or rejected without relying on Undo. Implemented on top of UE 5.8's `FileSandboxCore`, so this feature will be **UE 5.8+ only** even after it ships.

### Asset Audit & Dependency Analysis
Get asset reference graphs, detect unused assets, identify circular references, and generate size maps across the entire content tree.

### Asset Validation
Run registered `UEditorValidatorSubsystem` validators on individual assets or folders. Results are returned as structured JSON artifacts.

### Asset Manager Configuration
Manage PrimaryAssetType definitions, asset bundles, and asset tags programmatically. Designed for DLC, content-bundle, and cooking-rule workflows.

### Asset Redirector Fixup
Bulk-fix asset redirectors created by renames or moves — list all redirectors, fix them in selected folders, and clean up references in a single AI-driven refactoring flow.

### Localization Pipeline
Automate the full localization workflow: gather source text, compile localization data, manage cultures, add/edit/remove string table entries, and switch editor display language for verification.

### Build & Package Pipeline
Cook content, package projects, and run Project Launcher profiles through AI commands. Long-running operations include progress reporting and cancellation.

---

## Editor — Editing Domain Extensions

### Blueprint Compile & Error Retrieval
Force-compile a Blueprint and retrieve the resulting error / warning list. Closes the AI's edit → verify → fix loop for Blueprint editing.

### World Partition / DataLayer
Manage DataLayers on World Partition maps — create, delete, set initial state, and bind actors. Includes HLOD layer assignment and external actor listing.

### Foliage Editing
List foliage types in a level, add instances by coordinates, bulk-remove instances by area, and tune FoliageType settings (density, scale, culling).

### Material Validation & Templates
Validate materials against project rules, find similar materials to prevent duplication, and create materials from workflow templates.

### MVVM Support
Create ViewModel classes and add, remove, and configure View Bindings from AI agents — for projects using the `ModelViewViewModel` plugin.

### Mixed Control Rig Tracks
Add Mixed Control Rig tracks to Level Sequences (the AnimMixer pieces are already shipped; this covers the remaining `MovieSceneMixedControlRig` native commands).

### Motion Matching (PoseSearch)
Manage PoseSearchDatabase contents, schema settings, and normalization parameters for projects adopting UE's Motion Matching system.

### Sound Architecture (SoundClass / Attenuation / Mix)
Extend the existing SoundCue commands to cover SoundClass volume hierarchy, SoundAttenuation spatial settings, and SoundMix EQ / pitch modulation.

### Chaos Destruction (Geometry Collection)
Edit Geometry Collection assets — fracture meshes, configure damage thresholds, and inspect cluster structures.

### Groom (Strand-Based Hair)
Configure Groom Assets — simulation parameters, LOD settings, and SkeletalMesh bindings.

### Additional Optional Graph Editors
- **Subsonic for MetaSound** (UE 5.8): event-driven audio integration
- **ControlRig Dynamics** (UE 5.8): simple physics simulation nodes inside ControlRig graphs
- **AnimationLayering / UAF** (UE 5.8): bone-mask layers and Unified Animation Framework node operations
- **MeshPartition (MegaMesh)** (UE 5.8): spatial partition and non-destructive modifiers on large meshes
- **ChaosCloth Asset** (UE 5.8): weight map, Sim/Render mesh, and cloth simulation config
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

### Performance Insights Tracing
Start and stop UE Trace sessions with channel selection, query frame stats and hitch summaries, and inspect domain-specific traces (HTTP events, Niagara timings, render commands).

### GameplayMessage Subsystem
Listen to and inject `UGameplayMessageSubsystem` messages for event-driven architectures — useful for testing decoupled gameplay systems.

### SaveGame Operations
List, load, save, and delete `USaveGame` slots — enables tests to start from a specific save state and reset to a known baseline.

### Semantic Asset Search (Frozen)
AI-powered semantic search across the Content Browser. Built on UE 5.8's `SemanticSearch` plugin, so this feature will be **UE 5.8+ only** even after it ships. Additionally, in UE 5.8 the `SemanticSearch` embedding pipeline only runs inside Epic's internal environment, so this item is **frozen** until the pipeline becomes available in the public build.

---

## Infrastructure

### Human-facing Editor GUI
Optional editor tabs for monitoring AI activity: Command History (timeline of commands and responses) and Artifact Viewer (inline preview of screenshots, JSON dumps, and reports).

### EDA Transport
Optional transport for connecting UAIP to Epic's Epic Developer Assistant (EDA), alongside the existing MCP, HTTP, WebSocket, and CLI transports. Depends on Epic publishing a stable `window.eda.*` JavaScript API.

---

> Feature requests and bug reports: open an [Issue](../../issues) in this repository.

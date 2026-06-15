**[日本語](../ja/roadmap.md)** | [Back to README](../../README.md)

# Roadmap

The items below are planned or under investigation. No specific release dates are committed and the list is subject to change.

---

### Sandbox Editing
AI-proposed edits are staged in a sandbox and require human approval before being written to disk. All changes can be inspected and selectively accepted or rejected without relying on Undo.

### Asset Audit & Dependency Analysis
Get asset reference graphs, detect unused assets, identify circular references, and generate size maps across the entire content tree.

### Asset Validation
Run registered `UEditorValidatorSubsystem` validators on individual assets or folders. Results are returned as structured JSON artifacts, making them suitable for CI/CD gate checks.

### Asset Manager Configuration
Manage PrimaryAssetType definitions, asset bundles, and asset tags programmatically. Designed for DLC, content-bundle, and cooking-rule workflows.

### Localization Pipeline Automation
Automate the full localization workflow: gather source text, compile localization data, manage cultures, add/edit/remove string table entries, and switch editor display language for verification.

### Build & Package Pipeline
Cook content, package projects, and run Project Launcher profiles through AI commands. Long-running operations include progress reporting and cancellation. Designed for CI/CD pipeline integration.

### Performance Insights Tracing
Start and stop UE Trace sessions with channel selection, query frame stats and hitch summaries, and inspect domain-specific traces (HTTP events, Niagara timings, render commands). Results are returned as JSON artifacts.

### Material Validation & Templates
Validate materials against project rules, find similar materials to prevent duplication, and create materials from workflow templates.

### Semantic Asset Search
AI-powered semantic search across the Content Browser — find assets by meaning rather than by filename. Currently suspended pending stability improvements in the underlying embedding pipeline.

### Additional Graph Editor Integrations
- **Niagara Subsonic**: Audio event nodes in MetaSound and Niagara graphs (UE 5.8 Subsonic system)
- **ControlRig Dynamics**: Simple physics simulation nodes inside ControlRig graphs
- **Mixed Control Rig tracks**: Add Mixed Control Rig tracks to Level Sequences
- **AnimationLayering / UAF**: Bone-mask layers and Unified Animation Framework node operations in Anim Blueprints
- **MeshPartition (MegaMesh)**: Spatial partition and non-destructive modifiers on large meshes
- **ChaosCloth Asset**: Weight map, Sim/Render mesh, and cloth simulation config commands
- **CustomizableSequencerTracks**: Blueprint-defined custom Sequencer track type support
- **DataPrep Asset**: Execute and inspect DataPrep import-pipeline assets

### Human-facing Editor GUI
Optional editor tabs for monitoring AI activity: Command History (timeline of commands and responses), Artifact Viewer (inline preview of screenshots, JSON dumps, and reports), and Scenario Builder (visually assemble and run scenarios without writing JSON by hand).

### EDA Transport
Optional transport for connecting UAIP to Epic's Epic Developer Assistant (EDA), alongside the existing MCP, HTTP, WebSocket, and CLI transports.

---

> Feature requests and bug reports: open an [Issue](../../issues) in this repository.

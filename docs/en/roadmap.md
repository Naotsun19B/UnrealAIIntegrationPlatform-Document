**[日本語](../ja/roadmap.md)** | [Back to README](../../README.md)

# Roadmap

The items below are planned features that are not yet available. No specific release dates are committed. The list reflects current planning and is subject to change.

---

## Near-term

### Sandbox Editing
AI-proposed edits are staged in a temporary sandbox and require human approval before being written to disk. Enables a **review-before-commit** safety workflow — all changes can be inspected and selectively accepted or rejected without ever touching Undo.

### Asset Audit & Dependency Analysis
Analyze asset dependencies from AI agents: get reference graphs (depth-limited), detect unused assets, identify circular references, and generate size maps across the content tree. Designed for AI-driven asset optimization loops.

### Asset Validation
Run registered `UEditorValidatorSubsystem` validators on individual assets or entire content folders. Results are returned as structured JSON artifacts — designed to serve as a CI/CD gate check.

### Asset Manager Configuration
Manage PrimaryAssetType definitions, asset bundles, and asset tags programmatically. Covers the DLC, content-bundle, and cooking-rule workflows that depend on `DefaultGame.ini` and the Asset Manager.

---

## Medium-term

### Localization Pipeline Automation
Automate the full localization workflow: gather source text, compile localization data, manage cultures, add/edit/remove string table entries, and switch editor display language for verification. Designed for teams that want AI to drive translation pass reviews.

### Build & Package Pipeline
Cook content, package projects, and run Project Launcher profiles through AI commands. Long-running operations report progress and support cancellation. Designed for CI/CD pipelines where an AI agent monitors and drives the build.

### Performance Insights Tracing
Start and stop UE Trace sessions with channel selection, query frame stats and hitch summaries, and inspect domain-specific traces (HTTP events, Niagara timings, render commands). Results are returned as JSON artifacts for AI analysis.

### Material Validation & Templates
Validate materials against project rules, find similar materials to prevent duplication, and create new materials from workflow templates.

---

## Exploratory

### Human-facing Editor GUI
Optional editor tabs for humans to monitor AI activity: **Command History** (timeline of commands and responses), **Artifact Viewer** (preview screenshots, JSON dumps, and test reports inline), and **Scenario Builder** (visually assemble and run scenarios without writing JSON by hand). Implemented as an optional module that does not affect the core.

### Semantic Asset Search
AI-powered semantic search across the Content Browser — find assets by meaning rather than by filename. Currently suspended pending stability improvements in the underlying embedding pipeline.

### Additional Graph Editor Integrations
- **Niagara Subsonic**: Audio event nodes in MetaSound and Niagara graphs (UE 5.8 Subsonic system)
- **ControlRig Dynamics**: Set up simple physics simulation nodes inside ControlRig graphs
- **Mixed Control Rig tracks**: Add Mixed Control Rig tracks to Level Sequences
- **AnimationLayering / UAF**: Bone-mask layers and Unified Animation Framework node operations in Anim Blueprints
- **MeshPartition (MegaMesh)**: Spatial partition and non-destructive modifiers on large meshes
- **ChaosCloth Asset**: Domain-specific commands for weight maps, Sim/Render mesh assignment, and cloth simulation config
- **CustomizableSequencerTracks**: Blueprint-defined custom Sequencer track type support
- **DataPrep Asset**: Execute and inspect DataPrep import-pipeline assets

### EDA Transport
Optional additional transport for connecting UAIP to Epic's Epic Developer Assistant (EDA) inside the editor — alongside the existing MCP, HTTP, WebSocket, and CLI transports.

---

> Feature requests and bug reports: open an [Issue](../../issues) in this repository.

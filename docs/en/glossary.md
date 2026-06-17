**[日本語](../ja/glossary.md)** | [Back to README](../../README.md)

# Glossary

Terms that appear repeatedly across the UAIP documentation. Sorted alphabetically.

---

### Artifact
A file produced by a command (PNG screenshot, JSON dump, text log, report bundle). Returned by reference (`ArtifactId`) rather than by path. Stored under `Saved/UAIP/<SessionId>/`. See [Artifacts](artifacts.md).

### Bearer Token
The 32-character random token UAIP writes at startup to authenticate HTTP and WebSocket requests. Stored at `Saved/UAIP/EditorHttpAuthToken.txt` and `EditorWsAuthToken.txt`. Passed in the `Authorization: Bearer <token>` header (HTTP) or in the first handshake frame (WebSocket). See [Connection Methods](connections.md).

### Capability
A per-command, per-session authorization tag (e.g., `BlueprintEdit`, `PIEControl`). Each command handler declares its required capabilities; a session can run a command only if it owns every required capability. Two classes: **DefaultAllow** (granted automatically) and **DefaultDenied** (must be enabled in `Config/DefaultUAIP.ini`). See [Safety & Capabilities](safety.md).

### Capability Set
The collection of capabilities owned by a session, computed at spawn time from the project's SafetyPolicy. Queried via `UAIP.Core.QueryCapabilities`.

### CommandDispatcher
The Core component that receives a `CommandRequest`, checks capability + policy, resolves the handler, runs it on the game thread, and returns the `CommandResponse`. Shared by all four transports and by the scenario route.

### CommandRegistry
The Core component that maps a fully-qualified command name (e.g., `UAIP.Editor.Blueprint.CompileBlueprint`) to the handler that implements it. Populated at module startup. Queried by `uaip_list_commands` / `uaip_describe_command`.

### DefaultAllow / DefaultDenied
The two classes of capability. **DefaultAllow** capabilities are granted to every new session automatically (e.g., `EditorInspect`, `PIEControl`). **DefaultDenied** capabilities require an explicit `+AllowedCapabilities=<name>` line in `Config/DefaultUAIP.ini`. The distinction roughly maps to read vs write.

### Demo / Pro
Two distribution forms of UAIP. **Demo** is the free, feature-limited binary on GitHub Releases (MCP transport only, observation + PIE + assertions + UI automation, capture watermarked). **Pro** is the full product (all transports, full editor + runtime editing, no watermark) — coming soon on Fab. See [Demo Version Guide](demo.md).

### ErrorCode
The machine-readable error category in a failed response (`CommandNotFound`, `CapabilityNotAvailable`, `PolicyViolation`, `InvalidParams`, `NotFound`, `ExecutionFailed`, `NotAllowed`, `Timeout`, `TooManyRequests`, `InternalError`). The `ErrorMessage` field carries the human-readable detail. See [Troubleshooting](troubleshooting.md).

### Fully-Qualified Command Name
The complete dot-separated name used to invoke a command (e.g., `UAIP.Editor.Observation.CaptureActiveWindowImage`). Short names (`CaptureActiveWindowImage` alone) return `CommandNotFound`. The first segment is `UAIP`, `Toolset`, or a project-defined prefix.

### Handler
The C++ class that implements one command (e.g., `FCaptureActiveWindowImageHandler`). Registered with `CommandRegistry` by its parent module at startup. Lives in the corresponding `UAIPEditor*` / `UAIPRuntime*` module.

### MCP (Model Context Protocol)
The open protocol used by AI clients (Claude Code, Codex CLI, Cursor, Windsurf, Copilot) to discover and invoke tools. UAIP exposes itself as an MCP server through the **MCP Bridge** (`thin_proxy.py`). See [Connection Methods](connections.md).

### MCP Bridge
The thin Python proxy (`Scripts/MCPBridge/thin_proxy.py`) that connects an AI client to the UE Editor. Translates MCP tool calls into UAIP HTTP requests internally, manages editor lifecycle (auto-launch, crash/hang recovery), and handles artifact inlining.

### Operational Constraints
A snapshot of the SafetyPolicy flags returned by `UAIP.Core.QueryCapabilities` — used by the AI to know in advance whether a given action will be permitted (e.g., `ReadOnly=True` means all writes will fail).

### PIE (Play in Editor)
UE's mode for running the game inside the editor. UAIP exposes start / stop / pause / resume / map-load through `UAIP.Runtime.PIE.*` and runtime observation / assertion / input commands during PIE.

### Provider
A namespace that groups related commands (e.g., `UAIP.Editor.Observation`, `Toolset.AnimationAssistant`). Each provider is registered by a module at startup. Filter `uaip_list_commands` with `ProviderPrefix` to enumerate one provider's commands.

### SafetyPolicy
A process-wide configuration (in `Config/DefaultUAIP.ini` under `[UAIP.SafetyPolicy]`) that gates entire categories of operations regardless of capability set — read-only mode, log dump permission, keyboard input permission, scenario opt-in, etc. The AI cannot lift SafetyPolicy at runtime; only the operator can change it (and an editor restart is usually required). See [Safety & Capabilities](safety.md).

### Scenario
An ordered list of commands submitted as one request via `uaip_run_scenario`, `POST /uaip/scenarios`, the WebSocket `ScenarioRequest` frame, or the `-uaip-scenario-file=…` CLI flag. Supports per-step `AbortOnFailure`, `RetryCount`, `TimeoutSeconds`, and template expressions (`${StepName.Data.x}`) to pipe earlier-step output into later steps. See [Scenario Execution](scenario.md).

### Session
A per-task scope on the server side. Owns a capability set, an artifact subfolder (`Saved/UAIP/<SessionId>/`), an observed-widget cache, and rate limiters. Created on the first request with a new `SessionId`. Cleaned up on `EndSession` or TTL expiry. Use a fresh `SessionId` per logical task to keep artifacts organized.

### Stability
A descriptor on each command (`Stable`, `Experimental`, `Deprecated`) returned by `uaip_describe_command`. Experimental commands may change without notice. Deprecated commands include a `MigrationTarget` field pointing at the replacement.

### Toolset / Toolset Bridge
**Toolset** refers to UE 5.8's first-party Toolset framework — a separate engine-side surface that some plugins expose. **Toolset bridge** commands (UAIP commands under the `Toolset.*` prefix) adapt that surface to UAIP's request/response shape, mirroring a corresponding UAIP-native command in most cases. Requires UE 5.8+ and the relevant Toolset plugin (e.g., `NiagaraToolsets`, `PhysicsToolsets`, `AnimationAssistantToolset`).

### Transport
A communication channel between an external client and the UAIP Core. Four are supported: **MCP** (via the Bridge), **HTTP**, **WebSocket**, **CLI**. All four feed the same `CommandDispatcher`; capability + policy decisions are identical regardless of transport. See [Connection Methods](connections.md).

### UAIP
**Unreal AI Integration Platform** — the plugin documented by this repository.

### Watermark
The `UAIP Demo` marker the demo binary adds to capture outputs (`CaptureActiveWindowImage`, `CaptureEditorTabImage`, `CaptureGraphViewportImage`, `CaptureViewportImage`). Its purpose is to make screenshots — which are commonly shared as review or test evidence — identifiable as having come from the demo build. The Pro version does not add it.

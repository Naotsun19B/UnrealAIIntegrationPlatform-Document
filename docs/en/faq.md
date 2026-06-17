**[日本語](../ja/faq.md)** | [Back to README](../../README.md)

# FAQ

## General

### What is UAIP for, in one sentence?

It lets AI agents drive, observe, and verify the UE Editor and Runtime over a structured, capability-gated API — instead of brittle coordinate-clicking or scripting against private UI internals.

### Who is the typical user?

- **AI-first developers** who want their Claude Code / Codex CLI / Cursor / Windsurf / Copilot session to actually touch the editor (open assets, edit Blueprints, run PIE, take screenshots).
- **QA / test automation engineers** who want LLM-driven smoke tests, PIE assertions, and capture-based regression evidence without writing every test by hand.
- **Tools programmers** building higher-level workflows on top of a stable command surface instead of reverse-engineering UE editor menus.

### How is this different from Python scripting in UE?

Python is just one automation surface. UAIP exposes **semantic commands** with declared parameter schemas, required capabilities, and uniform artifact output — across MCP, HTTP, WebSocket, and CLI. Python scripting (via `RunEditorPythonScript`) is also available but bypasses the capability/policy layer, so it's only recommended when no registered command covers your need.

### Is the demo limited in time?

No — the demo is feature-limited (no editor editing, no HTTP/WS/CLI, capture watermark), not time-limited. Use it indefinitely.

---

## Demo vs Pro

### Which should I start with?

Start with the **demo**. It covers observation, PIE control, scenarios, UI automation, and assertions — enough to evaluate whether the integration model works for you.

Upgrade to **Pro** when you need: editor editing (Blueprint / Level / Assets / Material / …), runtime world editing (Spawn / GAS / Input injection / …), HTTP / WebSocket / CLI transports, or Python script execution.

See [Demo Version Guide](demo.md) for the full comparison table.

### Can I run both in one project?

No — they share the same plugin path. Replace one with the other; the `DefaultUAIP.ini` capability set is what differs.

### Why does demo capture have a watermark?

To make demo-version screenshots clearly identifiable as such. Captures are commonly shared as review or test evidence, so the origin needs to be obvious. The watermark is not present in the Pro version.

---

## Setup & connection

### Does the bridge keep the editor running between calls?

Yes. The MCP Bridge starts the editor on the first call, keeps the connection alive, and detects crashes / hangs to auto-restart (up to 3 restarts per 60 s, then it bubbles the error to the AI). You don't manage the editor lifecycle manually — see [usage.md §2](../../README.md#editor-lifecycle).

### Why doesn't `-uaip-http-enable` work in the demo?

The demo binary is **MCP-only**. The HTTP / WebSocket / CLI flags are silently ignored. This is enforced at module-load time, not by stripping the flag handlers. Pro removes the restriction.

### Can I run UAIP on macOS / Linux?

UAIP v1.0 is **Windows (Win64) only** — the `.uplugin`'s `PlatformAllowList` is locked to `Win64`. macOS / Linux support is on the roadmap as a future consideration but is low priority, with Linux scheduled even later than macOS.

### How do I authenticate?

- **MCP**: no auth (the bridge runs locally).
- **HTTP / WebSocket (Pro)**: a 32-char Bearer token is generated at startup and saved to `Saved/UAIP/EditorHttpAuthToken.txt` / `EditorWsAuthToken.txt`. Pass it in the `Authorization` header (HTTP) or in the first frame (WebSocket). Use `-uaip-http-no-auth` / `-uaip-ws-no-auth` for dev only. Connections are localhost-only by design.

---

## Capabilities & safety

### Why is `AddBlueprintVariable` returning `CapabilityNotAvailable`?

Editing capabilities (`BlueprintEdit`, `BlueprintVariableEdit`, etc.) are **DefaultDenied**. Add them to `Config/DefaultUAIP.ini`:

```ini
[UAIP.SafetyPolicy]
+AllowedCapabilities=BlueprintEdit
+AllowedCapabilities=BlueprintVariableEdit
+AllowedCapabilities=BlueprintGraphEdit
```

Then restart the editor, or — if `AllowCapabilityReload=True` is set — call `UAIP.Core.ReloadCapabilities`.

### What's the difference between Capability and SafetyPolicy?

- **Capability** is per-command, per-session authorisation (e.g., this session can edit Blueprints).
- **SafetyPolicy** is a process-wide gate that can deny entire categories regardless of capability (e.g., read-only mode rejects every write). SafetyPolicy is configured by the operator and cannot be lifted by the AI at runtime.

Full reference: [Safety & Capabilities](safety.md).

### Why is `PressKey` rejected even after I added `EditorKeyboardInput`?

`PressKey` also requires the SafetyPolicy switch `AllowKeyboardInput=True` (deny-by-default at process level). Modifier keys (Ctrl/Alt/Shift/Cmd) additionally require `AllowKeyboardModifierInput=True`. The capability gates *which sessions can ask*; SafetyPolicy gates *whether the request is accepted at all*.

### Can I make the editor effectively read-only for the AI?

Yes. Set `ReadOnly=True` in `[UAIP.SafetyPolicy]`. All mutating commands return `PolicyViolation` regardless of capability set. Useful for evaluation / sandbox environments.

---

## Workflow

### Should I call `uaip_execute` repeatedly or build a scenario?

If you'd call `uaip_execute` two or more times to do one logical thing, switch to `uaip_run_scenario`. Scenarios give you:
- Ordered execution on the game thread (no interleaving)
- Abort-on-failure / retry / per-step timeout as declarative options
- All artifacts bundled in one response
- A wall-clock watchdog per scenario (up to 1800 s)

See [Scenario Execution](scenario.md) for the full spec and [Cookbook](cookbook.md) for templates.

### Where are screenshots / dumps saved?

Under `<YourProject>/Saved/UAIP/<SessionId>/` — split into `Screenshots/`, `Dumps/`, `Logs/`, `Reports/`. The exact path is internal to the server; AI clients receive artifact IDs and read files via the bridge or the editor's HTTP artifact endpoint. See [Artifacts](artifacts.md).

### How do I get the AI to verify a UI state without me looking?

Use a capture command (`CaptureActiveWindowImage`, `CaptureGraphViewportImage`, `CaptureEditorTabImage`) followed by reading the resulting PNG. The AI client's file-read tool can display the image in context. For structural state, prefer `DumpEditorState` / `DumpSlateTree` — JSON is cheaper than pixel inspection.

### Do I need to write `UAIP.` prefixes when calling commands?

Yes, command names are fully-qualified. `HealthCheck` returns `CommandNotFound`; you need `UAIP.Core.HealthCheck`. Use `uaip_list_commands(ProviderPrefix="UAIP.Core")` if you're unsure of the full name.

---

## CI / production usage

### Can I run UAIP in CI?

Technically yes, via the CLI transport (Pro). See [Cookbook recipe 7](cookbook.md#7-run-automation-tests-from-ci-pro). Practically: editor startup is slow (30–90 s in CI), the demo doesn't support CLI, and richer CI primitives (cook, package, validation) are still on the roadmap.

### Can multiple AI agents share one editor?

The MCP Bridge currently assumes one editor per project. Concurrent commands within one editor are serialized at the dispatcher; concurrent scenarios are rejected with `TooManyRequests`. Use separate editors / projects if you need parallel agent work.

### Does UAIP affect packaged builds?

The demo and Pro plugins both load only in editor configurations by default. The runtime modules (`UAIPRuntime*`) can be opted into packaged builds for Gauntlet / runtime observation, but the editor modules (`UAIPEditor*`) are not packaged.

---

## Reporting bugs / contributing

### Where do I report issues?

Open an [issue](../../issues) on this repository with:
- UE version (5.7 / 5.8 + minor)
- Demo or Pro
- Command + parameters that failed
- `ErrorCode` and `ErrorMessage` from the response
- Editor crash log if applicable (`Saved/Crashes/`)

### How do I propose a new command?

File an issue describing the use case. Roadmap candidates are tracked in the [Roadmap](roadmap.md).

### Are pull requests accepted?

Yes. The author reviews PRs and may modify them for code style or implementation details before merging. Opening an Issue beforehand to align on direction is encouraged.

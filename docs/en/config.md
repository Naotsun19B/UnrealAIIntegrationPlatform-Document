**[日本語](../ja/config.md)** | [Back to README](../../README.md)

# Configuration Reference

This page enumerates every configuration knob exposed by UAIP outside of the SafetyPolicy / Capability layer.
SafetyPolicy and Capability settings have their own reference — see [Safety & Capabilities](safety.md).

---

## Configuration sources

UAIP reads its configuration from four locations, merged in this priority order (later sources override earlier ones):

| Priority | Source | Scope | Reload |
|---|---|---|---|
| 1 | `Plugins/UnrealAIIntegrationPlatform/Config/DefaultUAIP.ini` | Plugin defaults shipped with the build | Editor restart |
| 2 | `<Project>/Config/DefaultUAIP.ini` | Per-project overrides committed to source control | Editor restart |
| 3 | `<Project>/Saved/UAIP/UAIPOverride.ini` | **Packaged builds only** — user-editable override created on first launch | Editor restart |
| 4 | CLI launch flags (`-uaip-*`) | Per-process, transient | Re-launch the editor |

`UAIP.Core.ReloadCapabilities` can reload `AllowedCapabilities` and `DeniedCapabilities` at runtime without restarting (see [Safety & Capabilities](safety.md#enabling-defaultdenied-capabilities)). All other keys require an editor restart.

> The MCP Bridge (`Plugins/UAIPMCPBridge/` after install) has its own configuration layer (`config.json` + environment variables). The bridge is distributed separately from the plugin — see [MCP Bridge config.json](#mcp-bridge-configjson) below.

---

## ini sections (other than SafetyPolicy)

All sections live in `Config/DefaultUAIP.ini` under their `[UAIP.*]` headers. Every key is opt-in — commented-out keys use the built-in default shown below.

### `[UAIP.CommandNotification]` — Editor toast notifications

Displays a Slate toast notification each time a command runs. Intended for development and live-demo sessions only. **Disable in CI / automation** because the toast can be captured by screenshots / recordings.

| Key | Type | Default | Range | Description |
|---|---|---|---|---|
| `Enabled` | bool | `False` | — | Master switch for toast notifications |
| `DurationSeconds` | float | `4.0` | `[1.0, 30.0]` | How long each toast stays on screen. Failure toasts add +2.0 seconds |
| `MaxConcurrentNotifications` | int32 | `5` | `[1, 20]` | Hard cap on simultaneously visible toasts |
| `ThrottleWindowSeconds` | float | `2.0` | `[0.1, 60.0]` | Identical-command coalescing window |

No CLI equivalents.

### `[UAIP.CommandPump]` — Running commands while a modal dialog is up (off by default)

While the editor shows a modal dialog, UAIP normally cannot answer at all. Commands run inside a ticker callback, and the dialog stops the game thread with that ticker on it. From the AI's side this is indistinguishable from a frozen editor.

Turning this on moves execution away from the moment a command is accepted, to the end of the frame. Commands that only **read** state can then be answered while the dialog is up. Commands that change the editor are not failed; they wait their turn and run once the dialog closes.

> **Off by default.** Enabling it changes when every command runs, so treat it as something to adopt deliberately. It disables itself for commandlet runs, where the end-of-frame delegate may never fire.

| Key | Type | Default | Description |
|---|---|---|---|
| `StarvedTickAllowList` | string | `UAIP.Core.HealthCheck,UAIP.Core.QueryCapabilities` | Comma-separated fully-qualified names of the commands that may run while a modal dialog is up. Anything not listed is **not rejected — it stays queued** until the dialog closes |

The default list is deliberately two commands: a modal dialog means the editor is halfway through someone else's operation. `ListCommands` and `DescribeCommand` are read-only, but they ask every registered handler for its availability and schema, which would run code from every domain module in exactly that situation. They are left out for that reason.

Matching CLI flag: `-uaip-command-pump-starved-tick-allow-list=...`

The effective list is resolved at startup and written to the Output Log as a single line (`Starved tick allowlist: ...`). If an ini edit does not appear to take effect, or an entry was dropped for being malformed, **the startup log is where to look**. Note that reading the `uaip.Command.StarvedTickAllowList` console variable only ever returns the default — the ini and the command line layer on top of it rather than writing back to it.

#### Console variables

| CVar | Default | Changeable at runtime | Description |
|---|---|---|---|
| `uaip.Command.PumpedExecution` | `0` | Yes | Master switch; `1` enables it |
| `uaip.Command.MaxQueuedCommands` | `32` | Yes | How many commands may be waiting at once. Anything over is answered with `TooManyRequests` — it never ran, so resending is safe. The per-session limit is derived from this value |
| `uaip.Command.MaxCommandsPerDrain` | `8` | Yes | Most commands to run in a single frame |
| `uaip.Command.StarvedTickAllowList` | as above | **No** | Read-only; set it from an ini file or the command line |

`StarvedTickAllowList` is read-only because the console is reachable through the very interface this list exists to constrain. A boundary that can be widened from inside is not a boundary.

### `[UAIP.Jobs]` — Per-frame budget for job-style commands

`UAIP.Editor.Assets.StartAssetAudit` returns as soon as the job is registered and advances its scan between editor frames instead of holding the game thread until the whole audit is done. This key sets how much of each frame that scan may take.

| Key | Type | Default | Range | Description |
|---|---|---|---|---|
| `AuditStepBudgetMs` | float | `10.0` | `[1.0, 100.0]` | Milliseconds of each frame the audit job may spend scanning. A larger value finishes audits sooner and makes the editor heavier while one runs; a smaller value does the opposite. A value outside the range is clamped rather than rejected |

The value is read once when the module starts, so an edit takes effect the next time the editor starts.

It is a target rather than a guarantee. A step that cannot be cut in half will overrun it — the initial asset-list query that `Preparing` issues, and the disk-size lookup for a single asset, are both indivisible.

No CLI equivalents.

### `[UAIP.Session]` — Session persistence

Controls whether session metadata (id, command log, capability set) is persisted to disk so sessions survive editor restarts.

| Key | Type | Default | Range | Description |
|---|---|---|---|---|
| `Enabled` | bool | `True` | — | Master switch for session persistence |
| `SubDirectory` | string | `Sessions` | — | Subdirectory under the artifact root where session files live |
| `MaxCommandLogEntries` | int32 | `100` | `[1, 10000]` | Maximum command-log entries retained per session file |
| `SessionLifetimeHours` | float | `24.0` | `[1.0, 8760.0]` | Idle hours before a session is considered expired |
| `MaxAllowedLifetimeHours` | float | `168.0` | `[1.0, 87600.0]` | Hard upper bound on total session lifetime even with renewals |
| `MaxScanFiles` | int32 | `1000` | `[1, 100000]` | Max files scanned on startup when rehydrating persisted sessions |

CLI equivalents: `-uaip-session-enabled` / `-uaip-session-sub-directory=...` / `-uaip-session-max-command-log-entries=N` / `-uaip-session-lifetime-hours=N` / `-uaip-session-max-allowed-lifetime-hours=N` / `-uaip-session-max-scan-files=N`.

### `[UAIP.ArtifactGC]` — Artifact garbage collection

Periodic cleanup of old artifact files under the artifact root. Keeps `Saved/UAIP/` from growing unbounded over long-running sessions.

| Key | Type | Default | Range | Description |
|---|---|---|---|---|
| `Enabled` | bool | `True` | — | Master switch for periodic GC |
| `MaxAgeHours` | int32 | `24` | `[1, 8760]` | Artifacts older than this are eligible for collection |
| `MaxSessionCount` | int32 | `50` | `[1, 100000]` | When session count exceeds this, the oldest sessions are purged first |
| `CleanupIntervalSeconds` | float | `3600.0` | `[60.0, 86400.0]` | Interval between GC passes |

CLI equivalents: `-uaip-gc-enabled` / `-uaip-gc-max-age-hours=N` / `-uaip-gc-max-session-count=N` / `-uaip-gc-cleanup-interval-seconds=N`.

### `[UAIP.PythonExtension]` — Python command extension (🧩 `PythonScriptPlugin`)

Controls where the scanner looks for `@uaip_command`-decorated Python files. Only registered when the `PythonScriptPlugin` is enabled in your `.uproject`.

| Key | Type | Default | Description |
|---|---|---|---|
| `CommandsDir` | string | `<Project>/Scripts/UAIPCommands` | Directory scanned for Python command definition files. Relative paths are resolved against the project root |

No CLI equivalents.

> `[UAIP.SafetyPolicy]` is intentionally not listed here — see [Safety & Capabilities](safety.md) for the full SafetyPolicy reference, including `AllowedCapabilities`, `DeniedCapabilities`, `DeniedCommands`, and `AllowCapabilityReload`.

### `AllowedArtifactDirectory` override

Although declared under `[UAIP.SafetyPolicy]` (the sandbox boundary is a safety concern), this key is referenced by every artifact-producing command:

```ini
[UAIP.SafetyPolicy]
AllowedArtifactDirectory=Saved/MyCustomUAIPStorage
```

- Default: `<Project>/Saved/UAIP/`
- ini-only (no CLI equivalent — the sandbox root is fixed at process start)
- The path is resolved relative to the project root if not absolute

---

## CLI launch flags

CLI flags are read from the editor process command line (`UnrealEditor.exe MyProject.uproject <flags>`). They override ini-derived values for the lifetime of the process.

### Transport opt-ins

Every transport is disabled by default and must be opted in at launch.

| Flag | Description |
|---|---|
| `-uaip-http-enable` | Enable HTTP API mode (FullHTTP). Binds `0.0.0.0:<port>` and exposes `/uaip/*` + `/mcp`. Requires Bearer token unless `-uaip-http-no-auth` is set |
| `-uaip-mcp-enable` | Enable MCP-only mode. Implies `-uaip-http-enable` but only exposes `/mcp` and `/uaip/artifacts/*`. Enforces 5-stage localhost check (PeerAddress / Host / Origin). No auth required |
| `-uaip-ws-enable` | Enable WebSocket transport. Binds `127.0.0.1:<port>` (hard-coded). Requires Bearer token in the first frame unless `-uaip-ws-no-auth` is set |
| `-uaip-enable-scenario` | Enable the `uaip_run_scenario` route. Without this, scenario submissions return `PolicyViolation: Scenario execution is not enabled` |

If both `-uaip-http-enable` and `-uaip-mcp-enable` are set, **MCP mode takes precedence** (HTTP API mode is not started).

### Port overrides

| Flag | Default | Description |
|---|---|---|
| `-uaip-http-port=N` | `8765` | TCP port for HTTP / MCP transport |
| `-uaip-ws-port=N` | `8766` | TCP port for WebSocket transport |

### Auth bypass (CI / sandbox only)

| Flag | Description |
|---|---|
| `-uaip-http-no-auth` | Disable Bearer token validation on HTTP API. Use **only** in isolated CI environments — see [Security](security.md) |
| `-uaip-ws-no-auth` | Disable Bearer token validation on WebSocket. Same caveat. When set, the OutputLog forwarding channel is also disabled |

### WebSocket logging

| Flag | Description |
|---|---|
| `-uaip-ws-log-verbose` | Lower the OutputLog forwarding threshold from `Display` to `Verbose` |
| `-uaip-ws-no-output-log` | Skip OutputLog forwarding entirely (also disables forwarding when `-uaip-ws-no-auth` is set) |

### CLI transport (one-shot execution)

The CLI transport runs a single command (or scenario) from the editor command line, writes the JSON response, and exits. Useful for shell scripts and CI hooks.

| Flag | Description |
|---|---|
| `-uaip-request=<json>` | Inline `uaip_execute` request JSON (escape quotes per your shell) |
| `-uaip-request-file=<path>` | Read the request JSON from a file |
| `-uaip-scenario=<json>` | Inline `uaip_run_scenario` payload |
| `-uaip-scenario-file=<path>` | Read the scenario JSON from a file |
| `-uaip-response-file=<path>` | Where to write the response. Defaults to stdout when omitted |
| `-uaip-stdin` | Read the request JSON from standard input |

Examples:

```bash
# Run HealthCheck once and write the JSON response to ./result.json
UnrealEditor-Cmd.exe MyProject.uproject \
  -uaip-request='{"CommandName":"UAIP.Core.HealthCheck","Params":{}}' \
  -uaip-response-file=./result.json

# Run a saved scenario
UnrealEditor-Cmd.exe MyProject.uproject \
  -uaip-scenario-file=./scenarios/pie-smoke.json \
  -uaip-response-file=./scenarios/pie-smoke.result.json
```

### SafetyPolicy CLI flags

Every `[UAIP.SafetyPolicy]` bool flag has a matching `-uaip-policy-*` CLI flag (the ini keys themselves are documented in [Safety & Capabilities](safety.md#safetypolicy-settings)):

| ini key | CLI flag |
|---|---|
| `ReadOnly` | `-uaip-policy-read-only` |
| `DisableSave` | `-uaip-policy-disable-save` |
| `AllowLogDump` | `-uaip-policy-allow-log-dump` |
| `AllowContextMenuMutation` | `-uaip-policy-allow-context-menu-mutation` |
| `AllowKeyboardInput` | `-uaip-policy-allow-keyboard-input` |
| `AllowKeyboardModifierInput` | `-uaip-policy-allow-keyboard-modifier-input` |
| `AllowPasswordFieldWrite` | `-uaip-policy-allow-password-field-write` |
| `AllowInputModeBypass` | `-uaip-policy-allow-input-mode-bypass` |
| `DisablePIEStart` | `-uaip-policy-disable-pie-start` |
| `AllowCheatCVarWrite` | `-uaip-policy-allow-cheat-cvar-write` |
| `AllowExternalTraceAnalysis` | `-uaip-policy-allow-external-trace-analysis` |
| `AllowDisclosingTraceAttachment` | `-uaip-policy-allow-disclosing-trace-attachment` |

`AllowCapabilityReload`, `AllowedCapabilities`, `DeniedCapabilities`, `DeniedCommands`, `AllowedArtifactDirectory`, and `ExternalTraceDirectory` are **ini-only** (no CLI equivalents — they control capability escalation and sandbox boundaries that must not be alterable via the process command line).

---

## Runtime override mechanism (packaged builds)

In packaged builds (`!WITH_EDITOR`), UAIP automatically creates and reads `<Project>/Saved/UAIP/UAIPOverride.ini` on first launch:

```ini
; UAIP Runtime Configuration Override
; Settings placed here override the defaults packaged in Config/DefaultUAIP.ini.
; Call UAIP.Core.ReloadCapabilities to apply AllowedCapabilities changes without restarting.
;
; Example:
;   [UAIP.SafetyPolicy]
;   +AllowedCapabilities=RuntimeExecCommand
```

- The file is created from a commented template if absent
- Any keys present here are merged on top of the pak'd `DefaultUAIP.ini` defaults
- Edit it freely to adjust runtime behavior without rebuilding the game
- `AllowedCapabilities` and `DeniedCapabilities` changes can be applied with `UAIP.Core.ReloadCapabilities` (no relaunch needed); other keys still require relaunch

This file does not exist in editor builds — use `Config/DefaultUAIP.ini` directly there.

---

## MCP Bridge `config.json`

When connecting via the MCP Bridge (deployed at `<UAIP-parent>/UAIPMCPBridge/` — typically `<Project>/Plugins/UAIPMCPBridge/`), an additional JSON config layer applies. It is consumed by the Python proxy, not by the editor. The bridge is distributed as `UAIP-MCPBridge-<version>.zip` in the documentation repository's [Releases](../../../releases).

| Key | Type | Default | Description |
|---|---|---|---|
| `editor_path` | string | `""` | Absolute path to `UnrealEditor.exe`. Falls back to env override `UAIP_UE_EDITOR_PATH` (env takes precedence) |
| `uproject_path` | string | `""` | Absolute path to the `.uproject` file. Falls back to env override `UAIP_UPROJECT_PATH` (env takes precedence) |
| `http_port` | int | `8765` | HTTP port for the editor's MCP endpoint. Must match `-uaip-http-port` when set |
| `http_startup_timeout_seconds` | int | `120` | How long the bridge waits for the editor to become ready after launch |
| `command_timeout_seconds` | int | `180` | Per-request HTTP timeout for forwarded commands. **Cannot be set lower than the HTTP transport's own async command timeout (120 s)** — see the invariant note below |
| `unresponsive_timeout_seconds` | int | `30` | How long a port that is listening but not answering health pings is tolerated before the bridge marks the editor `UNRESPONSIVE`. In this state the bridge neither auto-launches nor auto-restarts — see [Connection Methods → Check editor status](connections.md#check-editor-status-uaip_get_editor_status) |
| `health_poll_interval_seconds` | int | `15` | Interval between background health pings while the editor is believed to be running |
| `handshake_timeout_seconds` | int | `10` | Timeout for the `HealthCheck` call used for project-identity verification, and for the `ShutdownEditor` call issued during a config reload |
| `scenario_timeout_seconds` | int | `1800` | Wall-clock cap applied to `uaip_run_scenario` submissions forwarded through the bridge, matching the route's own 30-minute limit |
| `artifact_timeout_seconds` | int | `60` | Timeout for artifact downloads, tracked independently of command execution time |
| `probe_tcp_timeout_seconds` | float | `1.0` | TCP connect timeout used to check whether the editor's port is listening at all |
| `probe_ping_timeout_seconds` | float | `5.0` | HTTP ping timeout used to check whether a listening editor actually responds |
| `process_exit_wait_seconds` | int | `10` | How long the bridge waits for a spawned editor process to exit before giving up |
| `allow_unverified_attach` | bool | `false` | Opt-in to allow attaching to an existing editor whose `HealthCheck` response lacks `ProjectFilePath` (older plugin versions that predate this field). **Denied by default** — a peer that cannot be identity-verified is refused rather than silently attached |
| `log_level` | string | `"INFO"` | Python logger verbosity — `DEBUG` / `INFO` / `WARNING` / `ERROR` |
| `enable_scenario` | bool | `false` | When `true`, the bridge launches the editor with `-uaip-enable-scenario`. Env override: `UAIP_ENABLE_SCENARIO=1` |
| `inline_artifacts.image` | bool | `false` | Inline PNG artifacts as base64 in MCP responses. **Off by default** to avoid `"Could not process image"` API errors when PNGs accumulate across a long session — use the `Read` tool with the artifact path instead |
| `inline_artifacts.json` | bool | `true` | Inline JSON artifacts as base64 in MCP responses |
| `inline_artifacts.text` | bool | `true` | Inline text artifacts as base64 in MCP responses |

Environment variables (`UAIP_UE_EDITOR_PATH`, `UAIP_UPROJECT_PATH`, `UAIP_ENABLE_SCENARIO`) override the corresponding JSON values when set. See `config.json.example` (shipped inside the bridge zip; after install, at `<bridge-root>/config.json.example`) for a fully-commented template.

### Timeout invariants

The bridge validates its timeout settings and reacts differently depending on which invariant is broken:

- `health_poll_interval_seconds` < `unresponsive_timeout_seconds` < `command_timeout_seconds`, and `unresponsive_timeout_seconds` < `http_startup_timeout_seconds`. These four values are treated as one profile — violating any single comparison resets **all four** to their defaults (with a warning in the bridge log) rather than starting with an inconsistent profile.
- `handshake_timeout_seconds` < `command_timeout_seconds`, validated independently — a violation resets only `handshake_timeout_seconds`.
- `TransportTimeouts.HTTP` (the editor's own async command timeout, `120` by default) `<` `command_timeout_seconds` — this one is checked against the **actual value reported by the editor's `HealthCheck` response** right after startup/attach, not against a hardcoded constant. A violation only logs a warning; it does not block startup or reset the value, because the editor process is already live by the time this check runs. Setting `command_timeout_seconds` below the editor's real async timeout means the bridge would give up on a command the editor is still allowed to keep running — see [Connection Methods → Long-running commands](connections.md#long-running-commands-and-the-120-s-async-timeout).

There is no separate `inflight_suppression_max_seconds` key — it is derived as `scenario_timeout_seconds + 60` to avoid racing the scenario route's own timeout at the boundary.

### Reloading config at runtime (`uaip_reload_config`)

Use `uaip_reload_config` to apply config changes **without restarting the MCP client**. The tool reads `config.json` in-place and, when launch parameters differ from the current session, shuts down the running editor and schedules a fresh launch on the next tool call.

```
uaip_reload_config()
→ { "EditorRestartScheduled": true/false, "EditorPath": "...", ... }
```

**Optional arguments** (session-only override; not persisted to `config.json`):

| Argument | Effect |
|---|---|
| `EditorPath` | Switch engine version at runtime without editing `config.json` |
| `UProjectPath` | Point at a different `.uproject` for this session |

Typical flow after editing `config.json`:

1. Edit `config.json` (e.g. set `enable_scenario: true`)
2. Call `uaip_reload_config()` — the bridge detects the change and schedules an editor restart
3. The next `uaip_execute` call launches the editor with the new parameters

---

## Where to look when something is misconfigured

| Symptom | First config to inspect |
|---|---|
| `PolicyViolation: Scenario execution is not enabled` | `-uaip-enable-scenario` flag (or `enable_scenario: true` in the bridge `config.json`) |
| HTTP / MCP / WS server did not start | Matching `-uaip-<transport>-enable` flag is missing |
| Artifacts accumulate on disk | `[UAIP.ArtifactGC]` — `Enabled` / `MaxAgeHours` / `MaxSessionCount` |
| Sessions vanish after restart | `[UAIP.Session].Enabled=True` and `MaxScanFiles` large enough |
| `"Could not process image"` API error | `inline_artifacts.image` in the bridge `config.json` is `true` — set to `false` |
| Editor toast spam during recording | `[UAIP.CommandNotification].Enabled=False` |
| Bearer token rejected | Check the token value matches the one written to `Saved/UAIP/Auth/http_token.txt` (HTTP) or `ws_token.txt` (WS). See [Security](security.md) |
| `CapabilityNotAvailable: <name>` | Add `+AllowedCapabilities=<name>` under `[UAIP.SafetyPolicy]` and call `UAIP.Core.ReloadCapabilities` (or restart) |

For everything else, see [Troubleshooting](troubleshooting.md).

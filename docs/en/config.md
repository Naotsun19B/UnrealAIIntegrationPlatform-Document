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

> The MCP Bridge (`Tools/MCPBridge/`) has its own configuration layer (`config.json` + environment variables). See [MCP Bridge config.json](#mcp-bridge-configjson) below.

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

`AllowCapabilityReload`, `AllowedCapabilities`, `DeniedCapabilities`, `DeniedCommands`, and `AllowedArtifactDirectory` are **ini-only** (no CLI equivalents — they control capability escalation and sandbox boundaries that must not be alterable via the process command line).

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

When connecting via the MCP Bridge (`Tools/MCPBridge/`), an additional JSON config layer applies. It is consumed by the Python proxy, not by the editor.

| Key | Type | Default | Description |
|---|---|---|---|
| `ue_editor_path` | string | — | Absolute path to `UnrealEditor.exe`. Env override: `UAIP_UE_EDITOR_PATH` |
| `uproject_path` | string | — | Absolute path to the `.uproject` file. Env override: `UAIP_UPROJECT_PATH` |
| `subprocess_timeout_seconds` | int | `300` | Timeout for individual UE subprocess calls |
| `log_level` | string | `"INFO"` | Python logger verbosity — `DEBUG` / `INFO` / `WARNING` / `ERROR` |
| `enable_scenario` | bool | `false` | When `true`, the bridge launches the editor with `-uaip-enable-scenario`. Env override: `UAIP_ENABLE_SCENARIO=1` |
| `inline_artifacts.image` | bool | `false` | Inline PNG artifacts as base64 in MCP responses. **Off by default** to avoid `"Could not process image"` API errors when PNGs accumulate across a long session — use the `Read` tool with the artifact path instead |
| `inline_artifacts.json` | bool | `true` | Inline JSON artifacts as base64 in MCP responses |
| `inline_artifacts.text` | bool | `true` | Inline text artifacts as base64 in MCP responses |

Environment variables override the JSON values when set. See `Tools/MCPBridge/config.json.example` (shipped with the plugin) for a fully-commented template.

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

**[日本語](../ja/troubleshooting.md)** | [Back to README](../../README.md)

# Troubleshooting

When something fails, the response includes an `ErrorCode` and `ErrorMessage`. This page maps those codes to fixes, and lists the most common environmental issues.

> Symbols used on this page: **🆓** = available in the demo binary / **🧩** = requires an optional plugin (same legend as [Commands Reference](commands.md#symbols)).

---

## Error code reference

| ErrorCode | What it means | Likely fix |
|---|---|---|
| `CommandNotFound` | The fully-qualified command name isn't registered | Verify spelling with `uaip_list_commands(ProviderPrefix="UAIP.Core")`. Optional-plugin commands (marked 🧩) require the plugin to be enabled |
| `CapabilityNotAvailable` | The session lacks the required capability | Read the missing capability name from `ErrorMessage`, add it to `[UAIP.SafetyPolicy] +AllowedCapabilities=<name>` in `Config/DefaultUAIP.ini`, then restart or call `UAIP.Core.ReloadCapabilities` |
| `PolicyViolation` | A SafetyPolicy gate rejected the call | `"is denied by SafetyPolicy"` → an ini flag is off; `"is not enabled"` → a CLI opt-in flag (`-uaip-enable-scenario`, `-uaip-http-enable`, etc.) is missing at launch |
| `InvalidParams` | Wrong / missing parameters, or (in a scenario) a `${...}` template reference that couldn't be resolved | Re-read the schema with `uaip_describe_command(CommandName="...")`. For template failures, see [Scenario Execution → Template resolution failures](scenario.md#template-resolution-failures) — this is **not** retried by `RetryCount` |
| `NotFound` | Target asset / actor / object doesn't exist | Verify the path or name; `SearchAssets` or `ListLevelActors` to confirm |
| `ExecutionFailed` | Runtime failure inside the command | Read `ErrorMessage` for details. In scenarios, set `RetryCount` on the step |
| `NotAllowed` | Forbidden path (`/Engine/`) or forbidden timing (editor edits during PIE) | Pick a different target path, or wait until PIE has stopped |
| `Timeout` | Wall-clock cap exceeded | Increase `TimeoutSeconds` on the scenario step, or split the scenario |
| `TooManyRequests` | Concurrency limit (1 scenario at a time) | Wait for the previous submission to complete |
| `InternalError` | Process-fault level | Try `UAIP.Workspace.RestartEditor` first; if it persists, capture the crash log under `Saved/Crashes/` and file an issue |

---

## Common situations

### "The editor won't start when I run a command"

The MCP Bridge launches the editor on the first call. If it doesn't come up:

1. Check the bridge config: `Plugins/UAIPMCPBridge/config.json` — `ue_editor_path` and `uproject_path` must be absolute and correct. Or, more commonly, the MCP client `env` block (`UAIP_UE_EDITOR_PATH` / `UAIP_UPROJECT_PATH`) which takes precedence.
2. Try launching the editor manually with the same `uproject` to confirm UE itself opens. If it doesn't, that's an engine issue, not UAIP.
3. Check Python is on `PATH` and `python --version` reports 3.10+.
4. If you see "Editor restart limit exceeded", you hit the 3-restarts-per-60-s guard. Wait 60 s and retry.

### "The first call times out, but subsequent calls work"

Initial editor startup can take 30–90 s (shader recompile, plugin load). The default MCP timeout for the first call is generous, but very heavy projects can still exceed it. Either pre-warm by launching the editor yourself before the first AI call, or retry — the bridge keeps the editor alive after a timeout.

### "My screenshot is a black frame"

Most often:
- The capture target window isn't focused. Run `FocusEditorTab` first for tab-based captures.
- The editor was launched with `-nullrhi` or `-RenderOffscreen`. Capture commands need a real RHI.
- For PIE captures (`CaptureViewportImage`), PIE isn't actually running. Confirm with `DumpEditorState`.

### "I asked for an asset edit and got `PolicyViolation: Capability '...' is denied by SafetyPolicy`"

The capability is listed in `[UAIP.SafetyPolicy] DeniedCapabilities=...`, which has deny-wins precedence over `AllowedCapabilities`. Remove it from `DeniedCapabilities` and restart the editor.

### "Scenarios always reject with `PolicyViolation: Scenario execution is not enabled in this environment`"

The scenario route is **off by default** for safety. Re-launch the editor with `-uaip-enable-scenario`, or — when starting through the MCP Bridge — add `"enable_scenario": true` to `Plugins/UAIPMCPBridge/config.json` and restart the bridge.

### "Capture / dump returns `ExecutionFailed`, no obvious reason"

Check `Saved/UAIP/<session>/Logs/` for the latest log lines from the command — they usually contain the exact UE-side failure. Common causes:

- Demo capture: watermark composition failed (corrupt font cache, blocked `Saved/UAIP/`); the command fails-closed.
- Slate tree dump: the root widget path filter didn't match anything. Try without `RootWidgetPath`.
- World dump during async load: world isn't ready. Wait for `LoadMap` to complete via the scenario flow.

### "I can't tell whether the AI's edit actually changed the file"

UAIP edits do call `MarkPackageDirty` (or the equivalent), but the file on disk only changes when you save. Either:

- Add a final `UAIP.Editor.Workspace.SaveAllPackages` step to the scenario.
- Inspect with `git status` after the operation (if your project is under version control).
- Use `DumpEditorState` — its `OpenAssets` field includes dirty flags.

### "Live Coding rebuild is blocked"

When Live Coding is mid-build and the editor refuses other commands, ask the AI to call `UAIP.Workspace.GetLiveCodingStatus` first; if a build is in progress, wait. Forcing other operations during a Live Coding build leads to undefined behavior. If you need to shut down for a full rebuild, prefer `UAIP.Workspace.ShutdownEditor` over `taskkill` — `taskkill` leaves `mcp_proxy.lock` behind and causes the next session to disconnect.

### "I got `CommandNotFound` for a command listed in the docs"

Most likely:
- The command's optional plugin isn't enabled in `.uproject` (see the 🧩 marker in [Commands Reference](commands.md)).
- You're on the demo and the command requires Pro (no 🆓 marker).
- The Toolset bridge command (e.g., `Toolset.Editor.UMG.GetWidgets`) requires UE 5.8+ and the matching Toolset plugin.

Confirm with `uaip_describe_command(CommandName="...")` — `Available: false` tells you which prerequisite is missing.

### "No response at all while the editor is showing a dialog"

Commands run inside the editor's ticker callback, and a modal dialog stops the game thread with that ticker on it. **Nothing is answered for as long as the dialog is up.** The dialog is sometimes behind another window, so from the AI's side this looks like a frozen editor.

Look at the editor and close the dialog; responses resume.

There is a feature that softens this (`[UAIP.CommandPump]`). With it enabled, commands that only read state — `HealthCheck` and the like — are answered while the dialog is up, and commands that change the editor wait their turn instead of failing, running once the dialog closes. **It is off by default**; see the [configuration reference](config.md).

A progress bar (slow task) is different: nothing is answered there even with the feature on. Cutting into an operation that is halfway through would corrupt state, so that case is refused on purpose.

### "MCP appears stuck — should I kill the editor?"

**No, don't `taskkill` the editor**, and don't assume it needs restarting just because a call didn't come back. That terminates every UE editor instance on the host (including other projects) and leaves `mcp_proxy.lock` behind. The right sequence:

1. **Call `uaip_get_editor_status()` first** — it probes the connection without triggering auto-launch and returns `State` + `RecommendedAction`. See [Connection Methods → Check editor status](connections.md#check-editor-status-uaip_get_editor_status).
2. If `State` is `UNRESPONSIVE` (port open, game thread not answering), `RecommendedAction` starts with `WAIT:` — **do not restart or kill anything.** A long-running command (see [Long-running commands and the 120 s async timeout](connections.md#long-running-commands-and-the-120-s-async-timeout)) is most likely still executing. Re-check periodically instead.
3. Only when `RecommendedAction` actually suggests recovering — e.g. `State` is `CRASHED` (`RETRY:`) or `PORT_OCCUPIED` (`CHECK CONFIGURATION:`) — act on it: `uaip_execute(CommandName="UAIP.Editor.Workspace.RestartEditor")` handles a clean restart for you.
4. If MCP itself is unresponsive (not just the editor), restart only the bridge process; the editor can stay running.
5. Only as an absolute last resort, manually `Stop-Process` the specific editor PID after closing the AI client — and only after `uaip_get_editor_status` has ruled out `UNRESPONSIVE`.

---

## Performance & resource usage

### "Artifacts are eating disk space"

`Saved/UAIP/` grows over time. Manual cleanup is fine — artifacts are not referenced after a session ends. For per-session bounded retention, end sessions explicitly with `UAIP.Core.EndSession`.

### "Editor memory usage is climbing across many commands"

Long-lived AI sessions can accumulate widget observation registrations, cached Slate trees, etc. Call `UAIP.Core.EndSession` periodically to GC artifacts and release widget refs. Combine with a fresh `SessionId` per major task.

### "Commands are slow"

Most "slow" cases are real editor cost (shader compile, asset load, PIE startup). Check with `uaip_describe_command` — read-only commands are usually <100 ms; capture commands depend on frame budget; PIE start can take seconds.

---

## Still stuck?

1. Capture the relevant `ErrorCode` + `ErrorMessage`.
2. Look at `Saved/UAIP/<session>/Logs/` for the corresponding command log.
3. Confirm UE version, plugin version (`UAIP.Core.GetSystemInfo`), demo / Pro.
4. File an [issue](../../issues) with the above details. Attach an `Saved/Crashes/` dump if the editor crashed.

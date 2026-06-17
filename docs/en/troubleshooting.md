**[日本語](../ja/troubleshooting.md)** | [Back to README](../../README.md)

# Troubleshooting

When something fails, the response includes an `ErrorCode` and `ErrorMessage`. This page maps those codes to fixes, and lists the most common environmental issues.

---

## Error code reference

| ErrorCode | What it means | Likely fix |
|---|---|---|
| `CommandNotFound` | The fully-qualified command name isn't registered | Verify spelling with `uaip_list_commands(ProviderPrefix="UAIP.Core")`. Optional-plugin commands (marked 🧩) require the plugin to be enabled |
| `CapabilityNotAvailable` | The session lacks the required capability | Read the missing capability name from `ErrorMessage`, add it to `[UAIP.SafetyPolicy] +AllowedCapabilities=<name>` in `Config/DefaultUAIP.ini`, then restart or call `UAIP.Core.ReloadCapabilities` |
| `PolicyViolation` | A SafetyPolicy gate rejected the call | `"is denied by SafetyPolicy"` → an ini flag is off; `"is not enabled"` → a CLI opt-in flag (`-uaip-enable-scenario`, `-uaip-http-enable`, etc.) is missing at launch |
| `InvalidParams` | Wrong / missing parameters | Re-read the schema with `uaip_describe_command(CommandName="...")` |
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

1. Check the bridge config: `Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/config.json` — `editor_path` and `uproject_path` must be absolute and correct.
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

The scenario route is **off by default** for safety. Re-launch the editor with `-uaip-enable-scenario`, or — when starting through the MCP Bridge — add `"enable_scenario": true` to `Scripts/MCPBridge/config.json` and restart the bridge.

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

### "MCP appears stuck — should I kill the editor?"

**No, don't `taskkill` the editor.** That terminates every UE editor instance on the host (including other projects) and leaves `mcp_proxy.lock`. The right sequence:

1. Try `uaip_execute(CommandName="UAIP.Workspace.RestartEditor")` — the bridge handles the restart cleanly.
2. If MCP itself is unresponsive, restart only the bridge process (the editor stays running).
3. Only as a last resort, manually `Stop-Process` the specific editor PID after closing the AI client.

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

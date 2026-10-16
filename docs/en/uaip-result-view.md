**[日本語](../ja/uaip-result-view.md)** | [Back to README](../../README.md)

# uaip-result-view (Claude Code Mod)

A Claude Code Mod that redraws the transcript rows of UAIP MCP tool calls. By default, Claude Code
shows only the first characters of the response JSON for each call, so a person following the
session cannot tell which command ran or how it ended. This Mod draws a summary instead.
**Only the drawing changes: the result the model reads is left exactly as the bridge returned it.**

It is for sessions that reach UAIP through the [MCP Bridge](connections.md#mcp-bridge) in Claude
Code. It does not need, and is not part of, the [Claude Code Plugin](claude-code-plugin.md)
(the `/uaip:*` skills that use the HTTP API); the two only share a marketplace.

---

## What it shows

```
UAIP ▸ Execute  UAIP.Editor.Observation.CaptureActiveWindowImage
  ✓ Success
    📎 Image  MCP-…/Captures/CaptureActiveWindowImage-….png
    ▸ Details          ← opens the main fields of Result (already open when the call failed)
```

| Tool | Headline | Lines always shown below it |
|---|---|---|
| `uaip_execute` | `✓ Success`, or `✗ <ErrorCode>: <ErrorMessage>` in red | Artifacts (type and path) |
| `uaip_run_scenario` | `✓ Completed (n/n steps)` / `✗ Failed (n/m steps)` | One line per step and the artifact count |
| `uaip_get_editor_status` | `✓ Success · <State>` | `RecommendedAction` |
| Other bridge tools | Success or failure | Artifacts, if any |

- **Details** lists the fields of `Result` (or `Data`, for tools the bridge answers itself) as
  `Key: value`. Nested objects open one level, arrays show only their length, and at most 16
  lines are shown.
- The call line shows the command (or scenario) name and its arguments as `Key=Value`.
- When a result cannot be read, its first line of text is shown as is.

In the VS Code extension and the desktop app, the summary is drawn in the call's own row. In the
terminal, the call row is one line and the summary is drawn in the result row below it.

---

## Requirements

- **Claude Code with Mod support.** The Mod API is marked **EARLY ACCESS** by Claude Code and may
  change between Claude Code releases; this is why the Mod is versioned `0.x`. If UAIP rows go back
  to raw JSON after a Claude Code update, start Claude Code with `claude --debug` and look for the
  `ui.render (ToolUse)` lines in the log: they say why the drawing was rejected.
- **The UAIP MCP Bridge**, registered in Claude Code by its installer (the server name starts with
  `uaip-`). See [Claude Code](clients/claude-code.md) for the bridge setup.

---

## Installing

The Mod ships in its own zip but belongs to the same `uaip-tools` marketplace as the
[Claude Code Plugin](claude-code-plugin.md). Both zips extract into the same
`UAIPClaudeCodePlugin` folder and carry the same marketplace file, so you can install either one
or both.

1. Download `UAIP-ResultView-<X.Y.Z>.zip` together with its `.sha256` file from this repository's
   [Releases](../../../releases) (tag `UAIPResultView-v<X.Y.Z>`), and check it — see
   [Verifying the download](#verifying-the-download) below.
2. Extract it into a permanent folder only you can write to, outside any UE project folder and
   outside Claude Code's working directory. If you already use the Claude Code Plugin, extract it
   into the folder you extracted that zip to.
3. If the `uaip-tools` marketplace is not registered yet, run
   `/plugin marketplace add <path to the extracted UAIPClaudeCodePlugin folder>`.
   Otherwise run `/plugin marketplace update uaip-tools`.
4. Run `/plugin install uaip-result-view@uaip-tools`, then restart Claude Code.

The marketplace lists both plugins whichever zip you extracted. Installing the one whose zip you
did not extract fails with "Source path does not exist"; nothing else is affected.

---

## Verifying the download

Each release publishes a `.sha256` file next to the zip, with two lines:

```
<sha-256 hex, lowercase>  UAIP-ResultView-<version>.zip
commit <the commit the release was built from>
```

The same SHA-256 is also recorded on this page (see [Release checksums](#release-checksums)
below), as a second, independent source. Compare both before trusting the zip:

```powershell
Get-FileHash UAIP-ResultView-<version>.zip -Algorithm SHA256
```

---

## Updating, or rolling back

1. Delete the `plugins/uaip-result-view` folder inside the extracted `UAIPClaudeCodePlugin`
   folder. Leave the rest of the folder alone: `plugins/uaip` belongs to the Claude Code Plugin.
2. Extract the zip for the version you want.
3. Run `/plugin marketplace update uaip-tools`, then `/plugin update uaip-result-view@uaip-tools`,
   then restart Claude Code.

---

## Release checksums

| Version | SHA-256 (`UAIP-ResultView-<version>.zip`) |
|---|---|
| 0.1.0 | `8c30b0a40bc525e62bdbabdaf28ac629718fb9622c432ec0b59a9a6ea74cc39b` |

---

## License

MIT. The license text ships inside the release archive as `LICENSE`.

**[日本語](../ja/claude-code-plugin.md)** | [Back to README](../../README.md)

# Claude Code Plugin

Eight Claude Code skills (`/uaip:*`) that let Claude Code drive, observe, and test a UE Editor
project through UAIP's HTTP API directly — **no MCP server configured, no MCP Bridge install**.
Each skill runs one bundled, pre-approved Python script that finds the right command, reads its
parameter schema, and executes it against this project's editor: never a guess at parameter names,
and never a shell command typed by the model.

This page covers installing, verifying, and running the plugin, and how it compares to the
[MCP Bridge](connections.md#mcp-bridge). For the transport it talks to underneath, see
[Connection Methods → HTTP API](connections.md#http-api-pro).

---

## Requirements

- **Windows (Win64) only.**
- **Python 3.10 or later**, available on `PATH` as `python`. On Windows, if no real Python
  install is on `PATH`, running `python` can silently open the Microsoft Store's placeholder
  ("app execution alias") instead of running anything — if a skill's first command seems to do
  nothing, run `python --version` yourself and confirm it prints `Python 3.10` or later.
- **UAIP 1.2.0 or later**, running with its HTTP API enabled (not MCP-only mode, and not the demo
  build — see [This plugin vs. the MCP Bridge](#this-plugin-vs-the-mcp-bridge) below).

---

## Installing

1. Download the release zip together with its `.sha256` file from this repository's
   [Releases](../../../releases) (tag `ClaudeCodePlugin-v<X.Y.Z>`, asset
   `UAIP-ClaudeCodePlugin-<X.Y.Z>.zip`), and check it — see
   [Verifying the download](#verifying-the-download) below.
2. Extract the zip somewhere **outside** any UE project folder, outside Claude Code's working
   directory, and outside anything listed in your `additionalDirectories` setting — a permanent
   folder only you can write to and do not plan to delete, for example
   `%USERPROFILE%\ClaudePlugins\`. This matters: the extracted `UAIPClaudeCodePlugin` folder is
   where Claude Code actually runs the pre-approved scripts from, so anyone who can write to it
   can change what those pre-approved commands do. Treat write access to this folder as
   equivalent to approval to run code.
3. In Claude Code, run `/plugin marketplace add <path to the extracted UAIPClaudeCodePlugin folder>`.
4. Run `/plugin install uaip@uaip-tools`.
5. Restart Claude Code. Eight `/uaip:*` skills should now be listed.

## Verifying the download

Each release publishes a `.sha256` file next to the zip, with two lines:

```
<sha-256 hex, lowercase>  UAIP-ClaudeCodePlugin-<version>.zip
commit <the commit the release was built from>
```

The same SHA-256 is also recorded on this page (see [Release checksums](#release-checksums)
below), as a second, independent source. Compare both before trusting the zip:

```powershell
Get-FileHash UAIP-ClaudeCodePlugin-<version>.zip -Algorithm SHA256
```

The printed hash must match the first line of the `.sha256` file (case-insensitively) and the
value recorded in the table below.

## Updating, or rolling back to an older release

1. Delete **everything** inside the folder you extracted to. An update that only overwrites files
   in place can leave behind files an older version shipped that the new one removed.
2. Extract the zip for the version you want — the newest release to update, an older release to
   roll back.
3. In Claude Code, run `/plugin marketplace update uaip-tools`, then `/plugin update uaip@uaip-tools`,
   then restart Claude Code. Updating the marketplace alone only re-reads the folder: the installed copy
   stays at the old version until `/plugin update` replaces it (this is also what rolls back).

If you started the editor with the watchdog option (see [Starting the editor](#starting-the-editor)
below), the watchdog is a separate background process running against the old scripts. It exits on
its own a few minutes after the editor it was watching stops answering — no crash marker, nothing
listening — so an update just has to wait that out; you do not have to find and close it by hand.
If you would rather not wait, closing the editor first and then ending the watchdog process
yourself has the same effect.

## Migrating from an earlier release

Earlier, unreleased copies of this plugin installed under the name `uaip@local-plugins`. If you
have one:

1. In Claude Code, disable and remove the `uaip` plugin and the `local-plugins` marketplace entry.
2. Delete the copy it made on disk — normally under `~/.claude/local-marketplace/plugins/uaip`
   (`%USERPROFILE%\.claude\local-marketplace\plugins\uaip` on Windows).
3. Follow [Installing](#installing) above for this release. Leaving the old copy in place alongside
   this one causes the same skill names to be registered twice.

---

## Starting the editor

Ask for it in chat, or run the skill directly:

```
/uaip:launch
/uaip:launch --port 9000
/uaip:launch --enable-scenario
```

- `--port <N>`: start (or, if it is already running, attach to) the editor on a specific port
  instead of the default. Once the editor has started, the other skills recall that port
  automatically for as long as it stays up; you only name the port again if you want a different
  one.
- `--enable-scenario`: let the editor accept scenario submissions (see
  [Scenario Execution](scenario.md) and the `/uaip:scenario` skill below). An editor that is
  already running cannot be switched on remotely — close it and run
  `/uaip:launch --enable-scenario` again.

This plugin needs the editor's HTTP API mode. **MCP-only startups, including the demo build, are
not supported by this plugin** — see [This plugin vs. the MCP Bridge](#this-plugin-vs-the-mcp-bridge)
below.

---

## Security boundary

- **What runs without asking you first**: each skill pre-approves only the one bundled script it
  calls, plus narrow permissions to read `Saved/UAIP/temp/` and write `Saved/UAIP/Requests/` in
  the current project. Because the script that sends commands is pre-approved, it can send *any*
  UAIP command name without a separate Claude Code prompt for each one. The boundary that actually
  decides what a command may do is the editor's own [Capability grants and SafetyPolicy](safety.md),
  not Claude Code's approval prompts. A command the editor does not allow comes back as
  `CapabilityNotAvailable` or `PolicyViolation`; the skills report this and ask whether you want
  to allow it, rather than changing the editor's configuration themselves.
- **Where credentials go**: before sending its authentication token anywhere, this plugin (and
  the MCP Bridge, when it is configured with a credential) asks the program on the target port to
  prove it is this project's UAIP editor, using a per-launch secret that only the real editor can
  read — see [Security → Instance proof](security.md#instance-proof) for the full mechanism. A
  program that cannot prove that — a different project's editor, an unrelated program that happens
  to use the same port, a port-forwarding relay, or an editor build older than 1.2.0 — never
  receives the token. The affected skill reports this as a connection failure with a message
  telling you what to check: pick another port, start the editor, or update it.
- **If your Claude Code settings prompt for approval anyway**: some environments turn off the
  default working-directory read access, or otherwise require every rule to be listed explicitly.
  Add one rule per script a skill calls, plus the two directory rules, for example (replace the
  path with where you extracted this plugin):

  ```
  Bash(python "<extracted-folder>/plugins/uaip/scripts/exec.py":*)
  Read(Saved/UAIP/temp/**)
  Edit(Saved/UAIP/Requests/**)
  ```

---

## Skills

| Skill | What it does |
|---|---|
| `/uaip:uaip` | Entry point: takes a natural-language request or a command name, finds the matching command, and routes to the skill below that handles it |
| `/uaip:launch` | Starts the editor with the HTTP API enabled, optionally on a specific port, with scenarios enabled, or with the crash/freeze watchdog |
| `/uaip:health` | Quick health check: confirms the editor answers and reports its version and load |
| `/uaip:diag` | Diagnoses an unreachable or crashed editor (reachability, TCP port, crash marker, crash log) without sending any credential |
| `/uaip:exec` | Runs any single UAIP command: looks it up, reads its parameter schema, executes it, and reports the result and artifacts |
| `/uaip:capture` | Screenshots and state dumps (active window, a graph editor tab, an editor tab, the output log, and similar) |
| `/uaip:test` | Runs an Automation Test or Automation Spec and reports Pass / Fail / Error |
| `/uaip:scenario` | Builds and submits an ordered batch of commands as one [scenario](scenario.md), and reports every step's result |

---

## Running a command that takes a long time

By default, the bundled `exec.py` script waits up to 130 seconds for a command's answer — the editor's own HTTP async command timeout is 120 seconds, and the script adds 10 seconds of margin. A command that legitimately runs longer than that — a large Automation Test run is the common case — needs a larger wait raised on **both** ends at once, or the call comes back as a timeout while the editor keeps working on it:

- **The editor's own wait**: add `--timeout N` (an integer from 1 to 1800) to the `exec.py` call. This sets the request's top-level `TimeoutSeconds` field, so the editor waits up to `N` seconds before giving up on an answer, instead of the 120-second default; `exec.py` itself then waits `N + 10` seconds for the response. `--timeout` cannot be combined with a scenario submission (`/uaip:scenario`), which has its own 1800-second wall-clock limit instead — see [API Reference → Request format](api.md#2-request-format) (§2.1) for the underlying HTTP field.
- **The Bash tool's own limit**: give the Bash tool a `timeout` of `--timeout` plus 60 seconds, in milliseconds. Its ceiling is 600000 ms (10 minutes); for a run that can take close to that or more, start the command in the background instead and read its output once it finishes.

For `/uaip:test`, also raise the command's own `TimeoutSec` parameter (1–600, default 60) — the limit the editor gives the *test run itself*, independent of `--timeout`, which only governs how long the HTTP transport waits for the answer. Set `TimeoutSec` to how long the tests need and `--timeout` to somewhat more than that (about 30 seconds more), for example:

```bash
python "<extracted-folder>/plugins/uaip/scripts/exec.py" "UAIP.Editor.Execution.RunAutomationTest" '{"TestName": "UAIP.Core.", "TimeoutSec": 300}' --timeout 330
```

If the editor still has not answered by then, exit code 4 means **the result is unknown** — the tests may still be running. Do not resend the same request; check again (a larger `--timeout` next time, or `/uaip:diag`) rather than assuming failure.

---

## This plugin vs. the MCP Bridge

This plugin's skills call the bundled Python scripts directly over HTTP; they do not need any MCP
server configured in Claude Code. Use these skills when you want Claude Code to drive the editor
directly, with each script pre-approved individually, and you would rather not deploy and maintain
a separate [MCP Bridge](connections.md#mcp-bridge) install.

Separately, UAIP's MCP Bridge exposes the same underlying commands as MCP tools, for AI clients
that talk MCP instead of calling scripts directly — including Claude Code itself, via
[its own MCP client page](clients/claude-code.md). If your session also has the MCP Bridge
configured for UAIP, its tools reach the same editor and can be used instead of these skills for
the same operations — the two are alternatives, not something you run together against the same
editor session.

|  | This plugin | MCP Bridge |
|---|---|---|
| Setup | `/plugin marketplace add` + `/plugin install` | Extract, run installer, edit an MCP config file |
| Transport it uses | UAIP HTTP API directly | MCP over stdio → the bridge process → UAIP HTTP API |
| Works with clients other than Claude Code | No | Yes (Codex CLI, Claude Desktop, Cursor, Windsurf, Copilot — see [Connection Methods](connections.md#mcp-bridge)) |
| Demo build support | No — HTTP API is Pro-only | Yes — MCP transport is available in the demo |
| Distribution | This repository's Releases, `uaip-tools` marketplace | This repository's Releases, `UAIP-MCPBridge-<version>.zip` |

---

## Exit codes

Every skill that runs the command script (directly, or through a sub-skill) reports one of:

| Code | Meaning |
|---|---|
| 0 | Success, and every artifact was saved |
| 1 | The editor reported a failure (`Success: false`, or an error such as `CapabilityNotAvailable`, `PolicyViolation`, `InvalidParams`, `NotFound`, `CommandNotFound`, `TooManyRequests`) |
| 2 | Bad arguments or input (wrong argument combination, not a UE project folder, a request file outside `Saved/UAIP/Requests/`, invalid JSON, input over 64 KiB). Nothing was sent |
| 3 | The program on the target port could not be reached, verified as this project's UAIP editor, or authenticated with. Nothing was carried out |
| 4 | Timed out. **The result is unknown** — the editor may still be working on it. Do not resend |
| 5 | The command (or every scenario step) succeeded, but one or more artifacts could not be fetched or saved |
| 6 | The response could not be interpreted. **The result is unknown** |

For a scenario submitted with `/uaip:scenario`, the same codes describe the whole submission
(whether every step succeeded, in place of a single command's success), and exit code 4 also
covers the editor stopping a scenario at its 1800-second limit (see
[Scenario Execution → Response shape](scenario.md#response-shape)).

---

## Files this plugin writes under `Saved/UAIP/`

- **`Requests/`** — where a skill writes a parameters or scenario file before handing it to the
  command script. The script deletes a request file once it has read it, unless the skill asked
  it to keep the file.
- **`temp/`** — saved copies of responses and artifacts (images, JSON, logs) that a skill has
  already shown you, kept so you can re-read them afterwards. **Safe to delete at any time** to
  reclaim space; nothing in this plugin depends on its contents surviving.
- **`raw/`** — used only when a text artifact contained an authentication token's value: the
  unmodified original goes here, while the copy under `temp/` has the value masked. **Safe to
  delete at any time**, same as `temp/`; it exists only so a token value does not sit in the copy
  the skills normally show you.
- **`EditorHttpAuthToken.txt`** and the per-port files under `InstanceSecrets/` — the editor's own
  credential and identity-verification files (see [Security → Instance proof](security.md#instance-proof)).
  This plugin does not write these and does not delete them; anything that can read them can act
  as this plugin does, so treat them like any other local secret.
- **`ClaudePluginLaunch.json`** — records the port and scenario setting from the last successful
  launch, purely so later commands can reuse them without you naming them again. It is never used
  to decide whether to trust a connection — that is always the per-command verification described
  under [Security boundary](#security-boundary) above. Deleting it just resets the next launch to
  the default port.

---

## Release checksums

Each release's SHA-256 is recorded here as a second, independent source — compare it against the
`.sha256` file that ships with the download (see [Verifying the download](#verifying-the-download)
above). Filled in at release time; the plugin's own version and the minimum UAIP version it
requires are also recorded here.

| Version | Requires | SHA-256 (`UAIP-ClaudeCodePlugin-<version>.zip`) |
|---|---|---|
| _(recorded at release time)_ | UAIP 1.2.0 or later | |

---

## License

MIT. The license text ships inside the release archive as `LICENSE`.

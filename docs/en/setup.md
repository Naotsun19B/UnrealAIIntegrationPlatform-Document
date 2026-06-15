**[日本語](../ja/setup.md)** | [Back to README](../../README.md)

# Setup Guide

This guide walks you through connecting your AI client to the UE Editor via the UAIP MCP Bridge.

---

## Prerequisites

- The `Plugins/UnrealAIIntegrationPlatform` folder is placed in your project's `Plugins` folder and the plugin is enabled
- Python 3.10 or newer is installed

---

## Step 1 — Install Python dependencies

Run the install script from the `Scripts/MCPBridge/install/` directory inside the plugin:

| Platform | Command |
|---|---|
| Windows | `install.ps1` |
| macOS / Linux | `install.sh` |

This installs Python dependencies and creates `config.json` next to `thin_proxy.py`.

---

## Step 2 — Determine the MCP server key

The server key identifies the bridge in your AI client's config.

| Plugin location | Key format | Example |
|---|---|---|
| Project plugin | `uaip-<ProjectName>` | `uaip-MyGame` |
| Engine plugin | `uaip-<version>` | `uaip-5.8` |

---

## Step 3 — Register the MCP server

Add the following entry to your AI client's MCP config file. Fill in the key from Step 2 and the paths from `config.json`.

```json
{
  "mcpServers": {
    "uaip-<ProjectName>": {
      "command": "python",
      "args": ["<absolute-path-to-bridge-root>/thin_proxy.py"],
      "env": {
        "UAIP_UE_EDITOR_PATH": "<absolute-path-to-UnrealEditor.exe>",
        "UAIP_UPROJECT_PATH":  "<absolute-path-to/MyProject.uproject>"
      }
    }
  }
}
```

### Config file location by client

| Client | Config file |
|---|---|
| **Claude Desktop** (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Claude Desktop** (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Claude Code** — user-wide | `~/.claude.json` |
| **Claude Code** — project | `.mcp.json` next to the `.uproject` file |
| **Cursor** | `~/.cursor/mcp.json` (user-wide) or `.cursor/mcp.json` (project) |
| **Windsurf** | `~/.codeium/windsurf/mcp_config.json` |
| **VS Code (GitHub Copilot)** | `.vscode/mcp.json` (workspace) |

Restart the AI client after saving.

---

## Step 4 — Deploy AI usage guides (Recommended)

The `Scripts/MCPBridge/install/guides/` directory contains Markdown guides that teach the AI how to use UAIP effectively. Deploying them means every future conversation automatically has the UAIP context loaded.

| Client | Action |
|---|---|
| **Claude Code** | Copy all `.md` files to `~/.claude/rules/uaip/` and add `@rules/uaip/usage.md` to `~/.claude/CLAUDE.md` |
| **Cursor** | Copy the `.md` files to `.cursor/rules/` with the `.mdc` extension |
| **Windsurf** | Append the content of `usage.md` to `.windsurfrules` |
| **GitHub Copilot** | Append a summary of `usage.md` to `.github/copilot-instructions.md` |

---

## Step 5 — Verify the setup

1. Restart the AI client
2. Ask the AI: **"Run a UAIP HealthCheck"**
3. The AI should call `uaip_execute(CommandName="UAIP.Core.HealthCheck")` via the registered MCP server
4. On success the editor launches (if not already running) and returns `{"Success": true}`

---

## Enable scenario execution (Optional)

`uaip_run_scenario` is disabled by default. To enable it, add `"enable_scenario": true` to `config.json` and reconnect the MCP client:

```json
{
  "editor_path":    "...",
  "uproject_path":  "...",
  "enable_scenario": true
}
```

See [Scenario Execution](scenario.md) for details.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Tool not found in AI client | MCP server not connected | Verify the server key and config file path; restart the client |
| Timeout after ~120 s | Editor failed to start | Check `config.json` — editor path and `.uproject` path must be valid |
| Python error on startup | Missing dependencies | Re-run `install.ps1` (or `install.sh`) |
| `PolicyViolation` on first command | Capability not granted | See [Safety & Capabilities](safety.md) |
| `CommandNotFound` | Wrong command name | Use `uaip_list_commands` to find the correct fully-qualified name |

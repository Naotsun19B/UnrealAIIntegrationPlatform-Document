**[日本語](../ja/setup.md)** | [Back to README](../../README.md)

# Setup Guide

This guide walks you through connecting your AI client to the UE Editor via the UAIP MCP Bridge.

---

## Prerequisites

- The `Plugins/UnrealAIIntegrationPlatform` folder is placed in your project's `Plugins` folder and the plugin is enabled
- Python 3.10 or newer is installed and available on `PATH`

---

## Step 1 — Run the install script

Open a terminal in your UE project root and run the install script. The script checks your Python version, installs dependencies, and **interactively asks you for two paths** to generate `config.json`.

**Windows (PowerShell):**
```powershell
.\Plugins\UnrealAIIntegrationPlatform\Scripts\MCPBridge\install\install.ps1
```

**macOS / Linux:**
```bash
bash Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/install/install.sh
```

The script runs three internal steps:

| Step | What it does |
|---|---|
| 1/3 | Verifies Python 3.10+ is available |
| 2/3 | Runs `pip install -r requirements.txt` (installs the `mcp` package) |
| 3/3 | Prompts for two paths, then writes `config.json` |

### Paths you will be asked to enter

**UE Editor executable**

| Platform | Example |
|---|---|
| Windows | `E:\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe` |
| macOS | `/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor` |
| Linux | `/home/user/UnrealEngine/Engine/Binaries/Linux/UnrealEditor` |

**`.uproject` file**

```
E:\MyProjects\MyGame\MyGame.uproject
```

When the script finishes, `config.json` is created next to `thin_proxy.py` at:

```
Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/config.json
```

---

## Step 2 — Determine the MCP server key

The server key identifies this bridge instance in your AI client's config.

| Plugin location | Key format | Example |
|---|---|---|
| Project plugin | `uaip-<ProjectName>` | `uaip-MyGame` |
| Engine plugin | `uaip-<version>` | `uaip-5.8` |

Derive the project name from your `.uproject` filename (without the extension).

---

## Step 3 — Register the MCP server

Add the following entry to your AI client's MCP config file. Use the key from Step 2 and the paths stored in `config.json`.

```json
{
  "mcpServers": {
    "uaip-<ProjectName>": {
      "command": "python",
      "args": ["<absolute-path-to>/Scripts/MCPBridge/thin_proxy.py"],
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
3. The AI calls `uaip_execute(CommandName="UAIP.Core.HealthCheck")` via the MCP server
4. On success, the editor launches (if not already running) and returns `{"Success": true}`

---

## Enable scenario execution (Optional)

`uaip_run_scenario` is disabled by default. Open `config.json` and add `"enable_scenario": true`, then reconnect the MCP client:

```json
{
  "editor_path":                  "...",
  "uproject_path":                "...",
  "http_startup_timeout_seconds": 120,
  "command_timeout_seconds":      60,
  "log_level":                    "INFO",
  "enable_scenario":              true
}
```

See [Scenario Execution](scenario.md) for details.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `install.ps1` is blocked by execution policy | PowerShell execution policy | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` first |
| Tool not found in AI client | MCP server not connected | Verify the key and `thin_proxy.py` path; restart the client |
| Timeout after ~120 s on first command | Editor failed to start | Check `editor_path` and `uproject_path` in `config.json` |
| Python error on startup | Missing dependencies | Re-run the install script |
| `PolicyViolation` on a command | Capability not granted | See [Safety & Capabilities](safety.md) |
| `CommandNotFound` | Wrong command name | Use `uaip_list_commands` to find the correct fully-qualified name |

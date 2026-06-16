**[日本語](../ja/setup.md)** | [Back to README](../../README.md)

# Setup Guide

This is the hub page for installing UAIP and registering the MCP Bridge with an AI client. For a 5-minute path, see [Quickstart](quickstart.md) first. For HTTP API, WebSocket, and CLI connections, see [Connection Methods](connections.md).

---

## Prerequisites

- The `Plugins/UnrealAIIntegrationPlatform` folder is placed in your project's `Plugins` folder and the plugin is enabled
- Python 3.10 or newer is installed and available on `PATH`
- One of the supported AI clients (Claude Code, Claude Desktop, Cursor, Windsurf, GitHub Copilot)

---

## Step 1 — Run the install script

Open a terminal in your UE project root and run the install script. It checks Python, installs dependencies, and **interactively asks you for two paths** to generate `config.json`.

**Windows (PowerShell):**
```powershell
.\Plugins\UnrealAIIntegrationPlatform\Scripts\MCPBridge\install\install.ps1
```

**macOS / Linux (Pro):**
```bash
bash Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/install/install.sh
```

What the script does:

| Step | Action |
|---|---|
| 1/3 | Verifies Python 3.10+ is available |
| 2/3 | `pip install -r requirements.txt` (installs the `mcp` package) |
| 3/3 | Prompts for `editor_path` + `uproject_path`, writes `config.json` |

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

`config.json` is created at `Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/config.json`.

---

## Step 2 — Determine the MCP server key

The server key identifies this bridge instance in your AI client's config.

| Plugin location | Key format | Example |
|---|---|---|
| Project plugin | `uaip-<ProjectName>` | `uaip-MyGame` |
| Engine plugin | `uaip-<version>` | `uaip-5.8` |

Derive the project name from your `.uproject` filename (without the extension). The key only affects how the client lists the server — it doesn't have to match anything in the bridge.

---

## Step 3 — Register the MCP server in your AI client

Pick your client and follow its dedicated page:

| Client | Page | Notes |
|---|---|---|
| **Claude Code** (CLI / VS Code extension) | [claude-code.md](clients/claude-code.md) | Best support; `.mcp.json` per project or `~/.claude.json` global |
| **Claude Desktop** | [claude-desktop.md](clients/claude-desktop.md) | `claude_desktop_config.json` |
| **Cursor** | [cursor.md](clients/cursor.md) | `~/.cursor/mcp.json` or `.cursor/mcp.json` |
| **Windsurf** | [windsurf.md](clients/windsurf.md) | `~/.codeium/windsurf/mcp_config.json` |
| **GitHub Copilot (VS Code)** | [copilot.md](clients/copilot.md) | `.vscode/mcp.json` |

Each per-client page has the exact config JSON, the deployment of the AI usage guides under `Scripts/MCPBridge/install/guides/`, and the verification step ("ask the AI to run HealthCheck").

---

## Step 4 — Enable scenario execution (optional)

`uaip_run_scenario` is disabled by default. To enable, edit `config.json`:

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

Reconnect the MCP client after the change. See [Scenario Execution](scenario.md) for what scenarios enable.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `install.ps1` is blocked by execution policy | PowerShell execution policy | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` then re-run |
| Tool not found in AI client | MCP server not connected | Check the key and `thin_proxy.py` path; restart the client |
| Timeout after ~120 s on first command | Editor failed to start | Verify `editor_path` and `uproject_path` in `config.json` |
| Python error on startup | Missing dependencies | Re-run the install script |
| `PolicyViolation` on a command | Capability not granted, or SafetyPolicy flag off | See [Safety & Capabilities](safety.md) |
| `CommandNotFound` | Wrong command name | `uaip_list_commands(ProviderPrefix="UAIP.Core")` |

For deeper diagnostics see [Troubleshooting](troubleshooting.md).

**[日本語](../../ja/clients/claude-desktop.md)** | [Back to Connection Methods](../connections.md#mcp-bridge)

# Claude Desktop

Claude Desktop is the standalone desktop chat app. MCP support is via `claude_desktop_config.json`.

---

## Config file location

| OS | Path |
|---|---|
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |

If the file doesn't exist, create it.

---

## Configuration

Paste the snippet the installer printed:

```json
{
  "mcpServers": {
    "uaip-MyGame": {
      "command": "E:/MyProjects/MyGame/Plugins/UAIPMCPBridge/.venv/Scripts/python.exe",
      "args": [
        "E:/MyProjects/MyGame/Plugins/UAIPMCPBridge/thin_proxy.py"
      ],
      "env": {
        "UAIP_UE_EDITOR_PATH": "E:/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe",
        "UAIP_UPROJECT_PATH":  "E:/MyProjects/MyGame/MyGame.uproject"
      }
    }
  }
}
```

- Replace `uaip-MyGame` with your own server key
- Use **absolute paths with forward slashes** in JSON
- `command` points at the venv Python the installer created, so a system-wide Python on `PATH` is not required

Save the file and **quit Claude Desktop completely** (system tray → Quit), then relaunch.

---

## AI usage guides

Claude Desktop doesn't have a per-project rules system. You have two options:

- **Inline**: paste the content of `Plugins/UAIPMCPBridge/install/guides/usage.md` at the start of each conversation
- **System prompt** (Claude Pro / Team): set a project-wide custom instruction containing the usage guidelines

The CLI-based [Claude Code](claude-code.md) handles this better. Consider it if you do a lot of UAIP work.

---

## Verification

1. Quit and relaunch Claude Desktop
2. In a new chat, the bottom of the input box should show **🔌 1 MCP server connected**
3. Ask: **"Run a UAIP HealthCheck."**
4. First call launches the editor (30–60 s); subsequent calls are fast

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| 🔌 shows 0 servers | Config file path or JSON syntax error. Validate JSON, restart Claude Desktop |
| Server icon is red | Click it to see the stderr from `thin_proxy.py`. Common cause: Python not on `PATH` — use the absolute `python.exe` path |
| AI doesn't know about UAIP commands | The usage guides aren't loaded. Paste `usage.md` inline at the start of the conversation |

See [Troubleshooting](../troubleshooting.md) for the full error code reference.

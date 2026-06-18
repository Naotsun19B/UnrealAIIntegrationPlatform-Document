**[日本語](../../ja/clients/copilot.md)** | [Back to Connection Methods](../connections.md#mcp-bridge)

# GitHub Copilot (VS Code)

[GitHub Copilot Chat](https://docs.github.com/en/copilot) in VS Code supports MCP servers from VS Code 1.99+. UAIP integrates as a workspace-local server.

---

## Config file location

| Scope | Path |
|---|---|
| Workspace | `.vscode/mcp.json` (next to `.vscode/settings.json`) |

---

## Configuration

Adapt the installer's snippet to Copilot's `servers` shape (add `type: "stdio"`, rename `mcpServers` → `servers`):

```json
{
  "servers": {
    "uaip-MyGame": {
      "type": "stdio",
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

> **Note**: Copilot's schema uses `servers` (not `mcpServers`) and requires the `type: "stdio"` field — different from Claude / Cursor / Windsurf. Don't reuse the JSON from those clients verbatim.

- Replace `uaip-MyGame` with your own server key
- Use absolute paths with forward slashes
- `command` points at the venv Python the installer created, so a system-wide Python on `PATH` is not required

After saving, VS Code prompts to start the MCP server. Approve it, or run **Command Palette → MCP: Restart Server**.

---

## AI usage guides (`.github/copilot-instructions.md`)

Copilot reads `.github/copilot-instructions.md` for repo-wide custom instructions. Append a summary of the UAIP guides:

```powershell
mkdir -Force .github
Get-Content Plugins/UAIPMCPBridge/install/guides/usage.md | Add-Content .github/copilot-instructions.md
```

Copilot has a smaller context budget than the other clients for custom instructions — paste only `usage.md` plus the most relevant guide for your workflow (e.g., `scenario.md` if you use scenarios heavily). Don't dump all guides at once.

---

## Verification

1. Reload the VS Code window (Command Palette → "Reload Window")
2. Open the Copilot Chat panel
3. Check the server status: Command Palette → **MCP: List Servers** → `uaip-MyGame` should be `Running`
4. Ask Copilot: **"Run a UAIP HealthCheck."**

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| MCP commands not in Command Palette | VS Code version too old. Update to 1.99+ |
| `MCP: List Servers` shows the server as Failed | Click the server name → **View Logs**. Common: `mcp` package not installed in the chosen Python |
| Copilot ignores the UAIP context | `.github/copilot-instructions.md` not loaded. Check **GitHub Copilot Chat: Use Instruction Files** is enabled |
| Tool calls don't get suggested | Phrase requests more concretely: "Use the UAIP HealthCheck tool" rather than "check UAIP" |

See [Troubleshooting](../troubleshooting.md) for the full error code reference.

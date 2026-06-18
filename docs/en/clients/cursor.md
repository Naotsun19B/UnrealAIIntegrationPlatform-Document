**[日本語](../../ja/clients/cursor.md)** | [Back to Connection Methods](../connections.md#mcp-bridge)

# Cursor

[Cursor](https://cursor.sh/) is an AI-first IDE based on VS Code. MCP support is enabled via `mcp.json`.

---

## Config file location

| Scope | Path |
|---|---|
| User-wide | `~/.cursor/mcp.json` |
| Project | `.cursor/mcp.json` (next to the `.uproject`) |

Project-scope is recommended so multiple UE projects don't collide.

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

After saving, **Cursor → Settings → Cursor Settings → Features → MCP** should list `uaip-MyGame`. Click the refresh icon or restart Cursor if it doesn't appear.

---

## AI usage guides (.cursor/rules)

Copy the guide files to `.cursor/rules/` and rename them with the `.mdc` extension:

```powershell
mkdir -Force .cursor/rules
Get-ChildItem Plugins/UAIPMCPBridge/install/guides/*.md | ForEach-Object {
    Copy-Item $_.FullName -Destination ".cursor/rules/$($_.BaseName).mdc"
}
```

The `.mdc` extension is required for Cursor to load them as rules. Cursor reads `.mdc` files in this folder automatically per project — no manual `@include` needed.

---

## Verification

1. Restart Cursor (or click the refresh icon next to the server)
2. Open the Cursor chat panel
3. Ask: **"Run a UAIP HealthCheck."**
4. The chat shows tool-use indicators when Cursor calls UAIP

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Server doesn't appear in Settings → MCP | JSON syntax error or wrong path. Validate JSON, restart Cursor |
| Server appears but "Failed to start" | Click the server name to see stderr. Common: wrong Python path or missing `mcp` package |
| Tool calls succeed but rules aren't applied | `.mdc` extension missing on guide files. Rename them and restart |
| Editor doesn't launch on first call | Verify `UAIP_UE_EDITOR_PATH` and `UAIP_UPROJECT_PATH` in the `env` block |

See [Troubleshooting](../troubleshooting.md) for the full error code reference.

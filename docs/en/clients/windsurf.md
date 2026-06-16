**[日本語](../../ja/clients/windsurf.md)** | [Back to Setup](../setup.md)

# Windsurf

[Windsurf](https://codeium.com/windsurf) is Codeium's AI-first IDE. MCP support is enabled via `mcp_config.json`.

---

## Config file location

| Scope | Path |
|---|---|
| User-wide | `~/.codeium/windsurf/mcp_config.json` |

Windsurf currently only supports a single user-wide config — multiple UE projects share the same MCP server entries.

---

## Configuration

```json
{
  "mcpServers": {
    "uaip-MyGame": {
      "command": "python",
      "args": [
        "E:/MyProjects/MyGame/Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/thin_proxy.py"
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
- Replace `python` with the full Python interpreter path if not on `PATH`

For multiple projects, add an entry per project under `mcpServers` with distinct keys (`uaip-GameA`, `uaip-GameB`, …).

---

## AI usage guides (`.windsurfrules`)

Windsurf reads `.windsurfrules` at the workspace root. Append the content of `usage.md`:

```powershell
Get-Content Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/install/guides/usage.md | Add-Content .windsurfrules
```

For more context (scenarios, capabilities, etc.), repeat for the other `.md` files in the `guides/` folder.

---

## Verification

1. Restart Windsurf
2. Open the Cascade panel
3. Look for the MCP server status at the top of the panel — it should show `uaip-MyGame ✓`
4. Ask: **"Run a UAIP HealthCheck."**

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Server doesn't appear in Cascade | JSON syntax error or wrong path. Validate JSON, restart Windsurf |
| Server appears in red | Check the Windsurf logs (`~/.codeium/windsurf/logs/`) for stderr from `thin_proxy.py` |
| Tool calls succeed but the AI ignores UAIP context | `.windsurfrules` not in the workspace root, or content not appended. Re-run the `Add-Content` command |
| Editor doesn't launch | Verify `UAIP_UE_EDITOR_PATH` and `UAIP_UPROJECT_PATH` |

See [Troubleshooting](../troubleshooting.md) for the full error code reference.

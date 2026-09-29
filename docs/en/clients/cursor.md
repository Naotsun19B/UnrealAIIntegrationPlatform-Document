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

## AI usage guides

Copy the guide files, unchanged, to `.cursor/uaip/guides/` — **not** into `.cursor/rules/`:

```powershell
mkdir -Force .cursor/uaip/guides
cp Plugins/UAIPMCPBridge/install/guides/*.md .cursor/uaip/guides/
```

Then create a single rule, `.cursor/rules/uaip.mdc`, that points at them:

```markdown
---
description: UAIP — driving and observing the Unreal Editor through the uaip_* MCP tools
alwaysApply: true
---
The UAIP usage guides are in `.cursor/uaip/guides/` at the project root.
Before the first uaip_* tool call in a conversation, read `.cursor/uaip/guides/index.md`,
then open only the guides it points to for the task at hand. Do not read every guide.
```

Why not `.cursor/rules/`: a rule with `alwaysApply: true` is included in every chat, so turning every guide into a rule puts the whole guide set — over 150k characters — into every conversation. This pointer costs a few lines, and the guides are read only when a task needs them. Write the path as plain text: an `@file` reference inside a rule inlines the referenced file.

After upgrading the bridge, check the copy with `python Plugins/UAIPMCPBridge/install/check_guides.py --deployed .cursor/uaip/guides` (add `--apply` to update it).

### Upgrading from the old layout

Earlier versions of this page had you copy every guide into `.cursor/rules/` as a `.mdc` file. Remove those before adding `uaip.mdc`:

```powershell
Get-ChildItem Plugins/UAIPMCPBridge/install/guides/*.md | ForEach-Object {
    Remove-Item -ErrorAction SilentlyContinue ".cursor/rules/$($_.BaseName).mdc"
}
```

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
| Tool calls succeed but the AI ignores the guides | `.cursor/rules/uaip.mdc` is missing, lacks the `.mdc` extension, or lacks `alwaysApply: true`. Fix it and restart |
| Editor doesn't launch on first call | Verify `UAIP_UE_EDITOR_PATH` and `UAIP_UPROJECT_PATH` in the `env` block |

See [Troubleshooting](../troubleshooting.md) for the full error code reference.

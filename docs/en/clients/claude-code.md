**[日本語](../../ja/clients/claude-code.md)** | [Back to Connection Methods](../connections.md#mcp-bridge)

# Claude Code

[Claude Code](https://claude.com/claude-code) is Anthropic's CLI / IDE-extension. It has the most mature MCP support of the listed clients and reads project-local `.mcp.json` files automatically.

---

## Prerequisites

You have already completed [Connection Methods → MCP Bridge Step 1](../connections.md#step-1--run-the-install-script). `config.json` is at:

```
Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/config.json
```

---

## Option A — Per-project (recommended)

Create `.mcp.json` next to your `.uproject`:

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

- Replace `uaip-MyGame` with your own server key (see [Connection Methods → MCP Bridge Step 2](../connections.md#step-2--pick-an-mcp-server-key))
- Use **absolute paths with forward slashes** (Windows accepts forward slashes in JSON)
- Replace `python` with the full path to your Python interpreter if `python` isn't on `PATH`

Claude Code picks this up the next time you start it from the project directory.

---

## Option B — Global (one server reused across projects)

Edit `~/.claude.json` and add the same `mcpServers` block at the top level. Use this only if your `editor_path` and `uproject_path` don't change between projects — usually not the case.

---

## Step — Deploy the AI usage guides (recommended)

`Scripts/MCPBridge/install/guides/` ships with Markdown documents that teach Claude how to use UAIP idiomatically (scenarios, capabilities, artifacts, graph editing, safety). Without them, Claude figures it out per-conversation, which wastes turns.

```powershell
# Copy all guide files to your global Claude rules folder
mkdir -Force ~/.claude/rules/uaip
cp Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/install/guides/*.md ~/.claude/rules/uaip/
```

Then reference them from `~/.claude/CLAUDE.md` so they load on every conversation:

```markdown
@rules/uaip/usage.md
@rules/uaip/scenario.md
@rules/uaip/safety-and-capabilities.md
@rules/uaip/command-discovery.md
@rules/uaip/artifacts.md
@rules/uaip/graph-editing.md
```

---

## Verification

1. Open a new Claude Code session in your project directory
2. Confirm the server shows up: `claude mcp list` should include `uaip-MyGame: ✔ connected`
3. Ask Claude: **"Run a UAIP HealthCheck."**
4. The first call launches the editor (30–60 s); subsequent calls are fast

Expected response shape:

```json
{
  "Success": true,
  "Data": {
    "Status": "Healthy",
    "UAIPVersion": "1.0.0",
    "EngineVersion": "5.8.0"
  }
}
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `claude mcp list` shows the server as failed | Run `python <path-to>/thin_proxy.py` directly — the error appears in stderr |
| `TypeError: ...` from `thin_proxy.py` startup | Wrong Python version. Confirm `python --version` is 3.10+ |
| `HealthCheck` works once, then later calls hang | The editor crashed and the bridge is reconnecting. Wait 60 s or check `Saved/Crashes/` |
| "Couldn't reach MCP" after editor restart | `mcp_proxy.lock` left over from a previous `taskkill`. Delete it from `Saved/UAIP/` and restart |

See [Troubleshooting](../troubleshooting.md) for the full error code reference.

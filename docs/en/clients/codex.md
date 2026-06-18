**[日本語](../../ja/clients/codex.md)** | [Back to Connection Methods](../connections.md#mcp-bridge)

# OpenAI Codex CLI

[Codex CLI](https://github.com/openai/codex) is OpenAI's official coding CLI. MCP servers are registered through `~/.codex/config.toml` (TOML, not JSON).

---

## Config file location

| Scope | Path |
|---|---|
| User-wide | `~/.codex/config.toml` |

Codex applies the same `mcp_servers` block to every project. If you want different bridges per project, use distinct server keys (e.g. `uaip-GameA`, `uaip-GameB`).

---

## Configuration

Translate the JSON snippet the installer printed into TOML:

```toml
[mcp_servers.uaip-MyGame]
command = "E:/MyProjects/MyGame/Plugins/UAIPMCPBridge/.venv/Scripts/python.exe"
args = [
    "E:/MyProjects/MyGame/Plugins/UAIPMCPBridge/thin_proxy.py",
]

[mcp_servers.uaip-MyGame.env]
UAIP_UE_EDITOR_PATH = "E:/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe"
UAIP_UPROJECT_PATH  = "E:/MyProjects/MyGame/MyGame.uproject"
```

> **Note**: Codex uses TOML, with the section header `[mcp_servers.<server-key>]` — different from Claude / Cursor / Windsurf (`"mcpServers"` JSON object) and from GitHub Copilot (`"servers"` JSON object). Don't reuse those clients' snippets verbatim.

- Replace `uaip-MyGame` with your own server key
- Use absolute paths with forward slashes (Windows accepts forward slashes in TOML strings)
- `command` points at the venv Python the installer created, so a system-wide Python on `PATH` is not required

Restart Codex CLI after saving so it picks up the new server.

---

## AI usage guides (`AGENTS.md`)

Codex reads `AGENTS.md` from the project root for project-specific instructions, and `~/.codex/AGENTS.md` for user-wide instructions. Deploy the UAIP usage guides as instruction files:

```powershell
# Per-project (recommended): paste the usage guide into the project's AGENTS.md
Get-Content Plugins/UAIPMCPBridge/install/guides/usage.md `
    | Add-Content AGENTS.md

# Or user-wide: applies to every Codex session on this machine
mkdir -Force ~/.codex
Get-Content Plugins/UAIPMCPBridge/install/guides/usage.md `
    | Add-Content ~/.codex/AGENTS.md
```

For deeper coverage (scenarios, capabilities, artifacts) append the matching `.md` files from `guides/` to the same `AGENTS.md`.

---

## Verification

1. Restart Codex CLI in your project directory
2. Confirm the server is registered — Codex's MCP listing command should show `uaip-MyGame` as connected
3. Ask Codex: **"Run a UAIP HealthCheck."**
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
| Codex shows the server as failed | Run `python <path-to>/thin_proxy.py` directly — the error appears in stderr |
| Codex doesn't surface MCP at all | Confirm your Codex CLI version supports MCP servers (`codex --version`); upgrade if needed |
| TOML parse error on Codex startup | Section headers must be exactly `[mcp_servers.<key>]` and `[mcp_servers.<key>.env]`. Strings need double quotes |
| Editor doesn't launch | Verify `UAIP_UE_EDITOR_PATH` and `UAIP_UPROJECT_PATH` in the `[mcp_servers.<key>.env]` block |
| Codex ignores the UAIP guidance | `AGENTS.md` isn't in the working directory or `~/.codex/`; confirm Codex is reading from where you wrote it |

See [Troubleshooting](../troubleshooting.md) for the full error code reference.

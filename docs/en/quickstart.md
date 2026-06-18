**[日本語](../ja/quickstart.md)** | [Back to README](../../README.md)

# Quickstart — 5 minutes to your first AI command

This page gets you from a fresh checkout to running your first UAIP command from an AI client in about five minutes. For detailed installation options, troubleshooting, and per-client configuration, see the [Connection Methods → MCP Bridge](connections.md#mcp-bridge).

---

## What you need

- **UE 5.7 or 5.8** project on Windows
- **Python 3.10+** on your `PATH` (used by the MCP Bridge)
- One of: **Claude Code**, **Codex CLI**, **Cursor**, **Windsurf**, or **GitHub Copilot Chat** (any MCP-capable client works)

---

## 1. Install the plugin (30 s)

### Demo (free)

Download the latest `UAIP-Demo-UE<version>-Win64.zip` from [Releases](../../../releases) and extract it as:

```
<YourProject>/Plugins/UnrealAIIntegrationPlatform/
```

### Pro

The Pro version is **coming soon on Fab**. Once published, install and place the plugin under the same path.

---

## 2. Enable the plugin (30 s)

Open your `.uproject` in UE and confirm **UnrealAIIntegrationPlatform** is enabled under **Edit > Plugins**. If you just dropped the folder in, restart the editor once.

For the demo, also copy `Config/DefaultUAIP.ini` from the release zip into your project's `Config/` folder — this pre-enables the demo capabilities (`PIEControl`, `SlateUIAutomation`, `ObservationCapture`).

---

## 3. Install the MCP Bridge (1 min)

The bridge is a thin Python proxy that connects your AI client to the UE Editor. It also handles starting the editor when it isn't running yet. **The bridge is distributed separately from the plugin** — download `UAIP-MCPBridge-<version>.zip` from this repository's [Releases](../../../releases) (one zip works for every UE version) and extract it anywhere, then run the installer:

```powershell
cd <wherever-you-extracted>/UAIPMCPBridge
./install/install.ps1
```

> **Supported platform**: UAIP v1.0 targets **Windows (Win64) only**. macOS / Linux support is a future consideration.

The installer is interactive — it asks for your `.uproject` path (or engine path), deploys the bridge to `<YourProject>/Plugins/UAIPMCPBridge/` (sibling to the UAIP plugin), creates a Python venv, and prints a copy-pasteable MCP client registration snippet at the end.

---

## 4. Register the MCP server in your AI client (1 min)

Paste the snippet the installer printed into your AI client's MCP config file. The exact file path differs per client — see [Connection Methods → MCP Bridge](connections.md#mcp-bridge) for the locations. The shape is:

```json
{
  "mcpServers": {
    "uaip": {
      "command": "<YourProject>/Plugins/UAIPMCPBridge/.venv/Scripts/python.exe",
      "args":    ["<YourProject>/Plugins/UAIPMCPBridge/thin_proxy.py"],
      "env": {
        "UAIP_UE_EDITOR_PATH": "<absolute path to UnrealEditor.exe>",
        "UAIP_UPROJECT_PATH":  "<absolute path to your.uproject>"
      }
    }
  }
}
```

Restart your AI client so it picks up the new server.

> **Tip**: the installer auto-detects the paths and prints the snippet with real values filled in — paste it as-is.

---

## 5. Verify it works (30 s)

Open a chat with your AI client and ask:

> "Run a UAIP HealthCheck."

The agent should call `uaip_execute(CommandName="UAIP.Core.HealthCheck")` and report back something like:

```json
{
  "Success": true,
  "Data": {
    "Status": "Healthy",
    "UAIPVersion": "1.0.0",
    "EngineVersion": "5.8.0",
    "BuildConfig": "Development"
  }
}
```

The editor will launch automatically on this first call — give it 30–60 s the first time.

---

## You're in. What's next?

| Goal | Where to go |
|---|---|
| See what kinds of things UAIP can do | [Examples / Cookbook](cookbook.md) |
| Drive Editor / PIE from AI through real scenarios | [Scenario Execution](scenario.md) |
| Look up a specific command | [Commands Reference](commands.md) |
| Use HTTP / WebSocket / CLI instead of MCP (Pro) | [Connection Methods](connections.md) |
| Understand the safety model before granting edit capabilities | [Safety & Capabilities](safety.md) |
| Something went wrong | [Troubleshooting](troubleshooting.md) |

---

> **Demo vs Pro**: the demo binary supports MCP transport, observation, PIE control, scenario execution, UI automation, and assertions — enough to integrate an AI agent into your review and testing workflow. For editor editing (Blueprint, Level, Assets, …), runtime world editing (Spawn, GAS, Input injection, …), HTTP / WebSocket / CLI transports, and Python script execution, see the [Demo Version Guide](demo.md) and consider the Pro version (coming soon on Fab).

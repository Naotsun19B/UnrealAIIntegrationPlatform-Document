![UE Version](https://img.shields.io/badge/Unreal%20Engine-5.7%20%2F%205.8-0e1128?logo=unrealengine&logoColor=white)
[![License: Fab Standard License (Fab EULA)](https://img.shields.io/badge/License-Fab%20Standard%20License%20%28Fab%20EULA%29-blue)](https://www.fab.com/eula)
[![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/Naotsun_UE?style=social)](https://twitter.com/Naotsun_UE)

**[日本語](docs/ja/overview.md)**

# UnrealAIIntegrationPlatform

<!--ts-->
   * [Description](#Description)
   * [Requirement](#Requirement)
   * [Installation](#Installation)
   * [Setup](#Setup)
   * [Demo Version](#Demo-Version)
   * [Documentation](#Documentation)
   * [License](#License)
   * [Author](#Author)
   * [History](#History)
<!--te-->

## Description

**UnrealAIIntegrationPlatform (UAIP)** is an Unreal Engine plugin that lets AI agents **drive, observe, execute, and verify** the UE Editor and Runtime over a structured API.

AI tools such as Claude Code, Cursor, Windsurf, and GitHub Copilot can connect via the **Model Context Protocol (MCP)** and issue semantic commands — no coordinate clicks, no brittle UI scripting.

Key capabilities:
- **Editor control** — open/save assets, edit Blueprints, manipulate actors, run Automation Tests, drive the Sequencer, and much more through 200+ registered commands
- **Visual & structural observation** — capture screenshots of any editor tab or viewport, dump JSON state of the world, Slate widget tree, editor state, and so on
- **Runtime / PIE control** — start/stop PIE, spawn actors, inject input, run Gauntlet tests, assert actor properties
- **Scenario execution** — submit an ordered list of commands as one request with abort-on-failure, retry, and per-step timeouts
- **Multi-transport** — reachable over MCP, HTTP, WebSocket, or CLI from within the same process
- **Safety & capability policy** — per-session capability gates and process-wide SafetyPolicy switches

## Requirement

Target version : UE 5.7 / 5.8  
Target platform : Windows  
Python : 3.10 or newer (required for the MCP Bridge)

## Installation

Put the `Plugins/UnrealAIIntegrationPlatform` folder in your project's `Plugins` folder.  
If the feature is not available after installing the plugin, check that the plugin is enabled from **Edit > Plugins**.

## Setup

The MCP Bridge (`Scripts/MCPBridge/`) is a thin Python proxy that connects your AI client to the UE Editor over HTTP.

1. Run `Scripts/MCPBridge/install/install.ps1` (Windows) or `install.sh` (macOS / Linux)
2. Register the MCP server in your AI client's config file
3. Deploy the AI usage guides from `Scripts/MCPBridge/install/guides/` (recommended)
4. Ask the AI: **"Run a UAIP HealthCheck"** to verify

For the full setup walkthrough, see [Setup Guide](docs/en/setup.md).

## Demo Version

A free demo binary is available in the [Releases](../../releases) of this repository.

The demo provides observation, PIE control, assertion, scenario execution, and UI automation commands — enough to integrate an AI agent into your review and testing workflow.

| | Demo | Pro (Fab) |
|---|:---:|:---:|
| MCP connection | ✅ | ✅ |
| HTTP / WebSocket / CLI | — | ✅ |
| Observation commands | ✅ | ✅ |
| PIE control | ✅ | ✅ |
| Scenario execution | ✅ | ✅ |
| UI automation | ✅ | ✅ |
| Editor editing (Blueprint, Level, Assets, …) | — | ✅ |
| Runtime world editing (Spawn, GAS, Input, …) | — | ✅ |
| Python script execution | — | ✅ |
| Watermark on captured images | ✅ | — |
| User extension points (`ICommandProvider`) | ✅ | ✅ |
| UE version | 5.7 / 5.8 | 5.7 / 5.8 |

See [Demo Version Guide](docs/en/demo.md) for the full command list, limitations, and installation steps.

## Documentation

| Document | Description |
|---|---|
| [Setup Guide](docs/en/setup.md) | MCP Bridge installation, client config, troubleshooting |
| [Connection Methods](docs/en/connections.md) | HTTP API, WebSocket, and CLI transport options (Pro) |
| [Commands Reference](docs/en/commands.md) | All 200+ commands organized by domain |
| [Scenario Execution](docs/en/scenario.md) | Multi-step ordered command batches |
| [Artifacts](docs/en/artifacts.md) | Screenshots, JSON dumps, logs — how to read them |
| [Safety & Capabilities](docs/en/safety.md) | SafetyPolicy and Capability configuration reference |
| [Demo Version Guide](docs/en/demo.md) | Demo command list, limitations, and installation |
| [Roadmap](docs/en/roadmap.md) | Planned features and future direction |

## License

The demo binary available in the Releases of this repository is provided under the terms of `EULA.txt` included in the release archive.  
The full product distributed on Fab is provided under the [Fab Standard License (Fab EULA)](https://www.fab.com/eula).  
Unless explicitly stated otherwise, all documentation content in this repository is © 2026 Naotsun. All rights reserved.

## Author

[Naotsun](https://twitter.com/Naotsun_UE)

## History

- (2026/06/16) v1.0  
  Initial release

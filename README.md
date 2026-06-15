![UE Version](https://img.shields.io/badge/Unreal%20Engine-5.8-0e1128?logo=unrealengine&logoColor=white)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/Naotsun_UE?style=social)](https://twitter.com/Naotsun_UE)

# UnrealAIIntegrationPlatform

<!--ts-->
   * [Description](#Description)
   * [Requirement](#Requirement)
   * [Installation](#Installation)
   * [Setup](#Setup)
      * [Step 1 — Install Python dependencies](#step-1--install-python-dependencies)
      * [Step 2 — Register the MCP server](#step-2--register-the-mcp-server)
      * [Step 3 — Deploy AI usage guides (Recommended)](#step-3--deploy-ai-usage-guides-recommended)
      * [Step 4 — Verify the setup](#step-4--verify-the-setup)
   * [Features](#Features)
      * [Editor Domain Commands](#editor-domain-commands)
      * [Runtime Domain Commands](#runtime-domain-commands)
      * [Scenario Execution](#scenario-execution)
      * [Artifacts](#artifacts)
   * [Settings](#Settings)
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

Target version : UE 5.8  
Target platform : Windows  
Python : 3.10 or newer (required for the MCP Bridge)

## Installation

Put the `Plugins/UnrealAIIntegrationPlatform` folder in your project's `Plugins` folder.  
If the feature is not available after installing the plugin, check that the plugin is enabled from **Edit > Plugins**.

## Setup

The MCP Bridge (`Scripts/MCPBridge/`) is a thin Python proxy that connects your AI client to the UE Editor over HTTP. The full setup guide is available at `Scripts/MCPBridge/install/SETUP.md` inside the plugin — open that file and ask your AI tool to complete the steps.

The short version is below.

### Step 1 — Install Python dependencies

Run the install script from the `Scripts/MCPBridge/install/` directory:

| Platform | Command |
|---|---|
| Windows | `install.ps1` |
| macOS / Linux | `install.sh` |

This installs Python dependencies and creates `config.json` next to `thin_proxy.py`.

### Step 2 — Register the MCP server

Add the following entry to your AI client's MCP config file:

```json
{
  "mcpServers": {
    "uaip-<ProjectName>": {
      "command": "python",
      "args": ["<absolute-path-to-bridge-root>/thin_proxy.py"],
      "env": {
        "UAIP_UE_EDITOR_PATH": "<absolute-path-to-UnrealEditor.exe>",
        "UAIP_UPROJECT_PATH":  "<absolute-path-to/MyProject.uproject>"
      }
    }
  }
}
```

| Client | Config file |
|---|---|
| **Claude Desktop** (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Claude Desktop** (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Claude Code** — user-wide | `~/.claude.json` |
| **Claude Code** — project | `.mcp.json` next to the `.uproject` file |
| **Cursor** | `~/.cursor/mcp.json` (user-wide) or `.cursor/mcp.json` (project) |
| **Windsurf** | `~/.codeium/windsurf/mcp_config.json` |
| **VS Code (GitHub Copilot)** | `.vscode/mcp.json` (workspace) |

Restart the AI client after saving.

### Step 3 — Deploy AI usage guides (Recommended)

The `Scripts/MCPBridge/install/guides/` directory contains Markdown guides that teach the AI how to use UAIP effectively. Deploying them means every future conversation automatically has the UAIP context loaded.

| Client | Action |
|---|---|
| **Claude Code** | Copy all `.md` files to `~/.claude/rules/uaip/` and add `@rules/uaip/usage.md` to `~/.claude/CLAUDE.md` |
| **Cursor** | Copy the `.md` files to `.cursor/rules/` with the `.mdc` extension |
| **Windsurf** | Append the content of `usage.md` to `.windsurfrules` |
| **GitHub Copilot** | Append a summary of `usage.md` to `.github/copilot-instructions.md` |

### Step 4 — Verify the setup

1. Restart the AI client
2. Ask the AI: **"Run a UAIP HealthCheck"**
3. The AI should call `uaip_execute(CommandName="UAIP.Core.HealthCheck")` via the registered MCP server
4. On success the editor launches (if not already running) and returns `{"Success": true}`

## Features

### Editor Domain Commands

Commands in the `UAIP.Editor.*` namespace cover the full editor surface:

| Provider prefix | Coverage |
|---|---|
| `UAIP.Editor.Workspace` | Tab management, graph editor focus, LiveCoding, Undo-Redo |
| `UAIP.Editor.Assets` | CreateAsset, DeleteAsset, OpenAsset, SaveAll, SearchAssets, … |
| `UAIP.Editor.Level` | PlaceActorInLevel, SetActorTransform, OpenLevel, … |
| `UAIP.Editor.Blueprint` | Blueprint variable / function / graph editing |
| `UAIP.Editor.Property` | Get/SetActorProperty |
| `UAIP.Editor.UMG` | Widget tree editing |
| `UAIP.Editor.Material` | Material graph editing |
| `UAIP.Editor.Niagara` | Niagara VFX editing |
| `UAIP.Editor.Physics` | Physics Asset editing |
| `UAIP.Editor.Dataflow` | Dataflow graph editing |
| `UAIP.Editor.Skeleton` | Skeleton / SkeletalMesh editing |
| `UAIP.Editor.AnimBlueprint` | Anim Blueprint / StateMachine editing |
| `UAIP.Editor.BehaviorTree` | Behavior Tree / Blackboard editing |
| `UAIP.Editor.EQS` | EQS query editing |
| `UAIP.Editor.MetaSound` | MetaSound graph editing |
| `UAIP.Editor.Sequencer` | Level Sequence editing |
| `UAIP.Editor.StateTree` | StateTree editing |
| `UAIP.Editor.ControlRig` | ControlRig hierarchy / RigVM graph |
| `UAIP.Editor.GameplayTags` | GameplayTag management |
| `UAIP.Editor.GameFeatures` | GameFeature Plugin management |
| `UAIP.Editor.EnhancedInput` | Input Action / Mapping Context editing |
| `UAIP.Editor.PCG` | PCG graph editing |
| `UAIP.Editor.Observation` | CaptureActiveWindowImage, DumpEditorState, DumpSlateTree, … |
| `UAIP.Editor.Execution` | RunAutomationTest, RunEditorPythonScript, RunEditorUtility |
| `UAIP.Editor.UIAutomation` | ClickWidget, PressKey, FillForm, WaitForWidget, … |

### Runtime Domain Commands

Commands in the `UAIP.Runtime.*` namespace control the running game:

| Provider prefix | Coverage |
|---|---|
| `UAIP.Runtime.PIE` | StartPIE, StopPIE, LoadMap |
| `UAIP.Runtime.World` | SpawnActor, TeleportActor, ExecuteConsoleCommand |
| `UAIP.Runtime.Observation` | DumpWorldState, CaptureViewportImage, CapturePerformanceSnapshot |
| `UAIP.Runtime.GAS` | GetAttributeValues, FindAttributeSetClasses, … |
| `UAIP.Runtime.Input` | InjectInputKey, InjectEnhancedInputAction |
| `UAIP.Runtime.Assertion` | WaitSeconds, WaitForCondition, AssertActorProperty (scenario primitives) |
| `UAIP.Runtime.Execution` | RunGauntletTest, RunRuntimeAutomationTest |

### Scenario Execution

`uaip_run_scenario` submits an ordered list of commands as one request. Steps run in order on the game thread with per-step abort, retry, and timeout controls.

Example — full PIE validation flow:

```json
{
  "ScenarioName": "PIE_HealthCheck",
  "Steps": [
    { "StepName": "Load",   "CommandName": "UAIP.Runtime.PIE.LoadMap",    "Params": { "MapPath": "/Game/Maps/TestMap" } },
    { "StepName": "Start",  "CommandName": "UAIP.Runtime.PIE.StartPIE",   "Params": {} },
    { "StepName": "Settle", "CommandName": "UAIP.Runtime.Assertion.WaitSeconds", "Params": { "Seconds": 2 } },
    { "StepName": "Cap",    "CommandName": "UAIP.Runtime.Observation.CaptureViewportImage", "Params": {} },
    { "StepName": "Stop",   "CommandName": "UAIP.Runtime.PIE.StopPIE",    "Params": {}, "AbortOnFailure": false }
  ]
}
```

Enable scenario execution by adding `"enable_scenario": true` to `config.json`.

### Artifacts

Every command returns artifacts — PNG screenshots, JSON state dumps, logs, and reports — stored under `Saved/UAIP/<SessionId>/`. The AI can read them directly without asking the user.

## Settings

Safety and capability controls are configured in `Config/DefaultUAIP.ini`:

```ini
[UAIP.SafetyPolicy]
ReadOnly=False
DisableSave=False
AllowLogDump=True
AllowContextMenuMutation=True
AllowKeyboardInput=True
AllowKeyboardModifierInput=True

; Lift specific DefaultDenied capabilities:
; +AllowedCapabilities=BlueprintEdit
; +AllowedCapabilities=SkeletonAssetEdit
```

| Key | Default | Effect |
|---|---|---|
| `ReadOnly` | `False` | Reject every mutating command |
| `DisableSave` | `False` | Reject disk-writing commands |
| `AllowLogDump` | `False` | Allow `DumpOutputLog` / `DumpMessageLog` |
| `AllowContextMenuMutation` | `False` | Allow `InvokeContextMenuAction` |
| `AllowKeyboardInput` | `False` | Allow `PressKey` |
| `AllowKeyboardModifierInput` | `False` | Allow Ctrl/Alt/Shift inside `PressKey` |
| `AllowPasswordFieldWrite` | `False` | Allow `FillForm` to write into password fields |
| `DisablePIEStart` | `False` | Reject PIE startup |
| `AllowedCapabilities` | empty | DefaultDenied capabilities to lift (one per line) |
| `DeniedCommands` | empty | Fully-qualified command names to block |

## License

Source code is available under the [MIT License](https://opensource.org/licenses/MIT).  
Unless explicitly stated otherwise, all documentation content in this repository is © 2026 Naotsun. All rights reserved.

## Author

[Naotsun](https://twitter.com/Naotsun_UE)

## History

- (2026/06/16) v1.0  
  Initial release

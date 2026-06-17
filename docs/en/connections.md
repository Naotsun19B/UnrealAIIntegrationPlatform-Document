**[日本語](../ja/connections.md)** | [Back to README](../../README.md)

# Connection Methods

UAIP supports four transport options. Choose the one that fits your integration scenario.

| Transport | Port (Editor) | Port (Packaged) | Best for |
|---|---|---|---|
| **MCP Bridge** | — | — | AI clients (Claude Code, Cursor, Windsurf, Copilot) |
| **HTTP API** | 8765 | 8767 | Custom integrations, REST clients, CI/CD pipelines |
| **WebSocket** | 8766 | 8768 | Real-time streaming, persistent connections |
| **CLI** | — | — | One-shot automation, shell scripts |

> **Demo limitation**: the demo binary supports the **MCP transport only**. HTTP, WebSocket, and CLI require the Pro version.

---

## Transport comparison

```mermaid
flowchart LR
    AI["AI client<br/>Claude / Cursor / …"] -->|stdio| MCP[MCP Bridge]
    MCP -->|"HTTP /mcp"| Ed[(UE Editor)]
    Tool[CI / scripts] -->|"HTTP POST"| Ed
    WSC[WebSocket client] -->|"WS frames"| Ed
    Shell[Shell / batch] -->|"-uaip-request / stdin-stream"| Ed
    Ed -->|writes| Artifacts[(Saved/UAIP/&lt;Session&gt;)]

    style MCP fill:#dfe
    style Ed fill:#eef
```

All four transports terminate at the same dispatch core inside the editor (see [Architecture](architecture.md)) so capability + policy semantics are identical regardless of which transport you use.

---

## MCP Bridge

The MCP Bridge is the recommended transport for AI client integration. A thin Python proxy (`thin_proxy.py`) sits between the AI client and the UE Editor, translating MCP tool calls into UAIP HTTP requests internally. The AI client ↔ Bridge link is MCP over stdio; the Bridge ↔ UE Editor link is loopback HTTP.

If you only want the shortest path to a working setup, see [Quickstart](quickstart.md).

### Prerequisites

- The `Plugins/UnrealAIIntegrationPlatform` folder is placed in your project's `Plugins` folder
- The **UnrealAIIntegrationPlatform** plugin is enabled in the UE project
- Python 3.10 or newer is installed and available on `PATH`
- One of the supported AI clients (Claude Code, Codex CLI, Claude Desktop, Cursor, Windsurf, GitHub Copilot)

### Step 1 — Run the install script

Open a terminal in your UE project root and run the install script. It verifies Python, installs dependencies, and prompts you for the two paths it needs to generate `config.json`.

```powershell
.\Plugins\UnrealAIIntegrationPlatform\Scripts\MCPBridge\install\install.ps1
```

What the script does:

| Step | Action |
|---|---|
| 1/3 | Verify Python 3.10+ is available |
| 2/3 | `pip install -r requirements.txt` (installs the `mcp` package) |
| 3/3 | Prompt for the UE Editor executable path and `.uproject` path, then write `config.json` |

Example inputs:

- UE Editor executable — `E:\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe`
- `.uproject` file — `E:\MyProjects\MyGame\MyGame.uproject`

`config.json` is created at `Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/config.json`.

### Step 2 — Pick an MCP server key

The server key is how this bridge instance is identified in your AI client's config.

| Plugin location | Key format | Example |
|---|---|---|
| Project plugin | `uaip-<ProjectName>` | `uaip-MyGame` |
| Engine plugin | `uaip-<version>` | `uaip-5.8` |

Derive the project name from your `.uproject` filename (without the extension). It only affects how the client lists the server, so any unique name works.

### Step 3 — Register the MCP server in your AI client

Pick your client and follow its dedicated page:

| Client | Page | Notes |
|---|---|---|
| **Claude Code** (CLI / VS Code extension) | [claude-code.md](clients/claude-code.md) | Best support; `.mcp.json` per project or `~/.claude.json` global |
| **Codex CLI** | [codex.md](clients/codex.md) | OpenAI's official CLI. `~/.codex/config.toml` (TOML) |
| **Claude Desktop** | [claude-desktop.md](clients/claude-desktop.md) | `claude_desktop_config.json` |
| **Cursor** | [cursor.md](clients/cursor.md) | `~/.cursor/mcp.json` or `.cursor/mcp.json` |
| **Windsurf** | [windsurf.md](clients/windsurf.md) | `~/.codeium/windsurf/mcp_config.json` |
| **GitHub Copilot (VS Code)** | [copilot.md](clients/copilot.md) | `.vscode/mcp.json` |

Each per-client page has the exact config JSON, the deployment of the AI usage guides under `Scripts/MCPBridge/install/guides/`, and the verification step ("ask the AI to run HealthCheck").

### Enable scenario execution (optional)

`uaip_run_scenario` is disabled by default. To enable, add `enable_scenario` to `config.json`:

```json
{
  "editor_path":                  "...",
  "uproject_path":                "...",
  "http_startup_timeout_seconds": 120,
  "command_timeout_seconds":      60,
  "log_level":                    "INFO",
  "enable_scenario":              true
}
```

Reconnect the MCP client after the change. See [Scenario Execution](scenario.md) for what scenarios enable.

### MCP setup troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `install.ps1` is blocked by execution policy | PowerShell execution policy | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` then re-run |
| Tool not found in AI client | MCP server not connected | Check the key and `thin_proxy.py` path; restart the client |
| Timeout after ~120 s on first command | Editor failed to start | Verify `editor_path` and `uproject_path` in `config.json` |
| Python error on startup | Missing dependencies | Re-run the install script |
| `PolicyViolation` on a command | Capability not granted, or SafetyPolicy flag off | See [Safety & Capabilities](safety.md) |
| `CommandNotFound` | Wrong command name | `uaip_list_commands(ProviderPrefix="UAIP.Core")` |

For broader diagnostics, see [Troubleshooting](troubleshooting.md).

---

## HTTP API (Pro)

The HTTP API exposes a REST interface. It's suited for custom scripts, CI/CD pipelines, and any integration where an AI client isn't involved. The socket binds to `0.0.0.0`, so with the Bearer token and a firewall allowance the editor can be reached from another machine (FullHTTP mode). Access control is the responsibility of the token and your network setup — see [Security → Network surface](security.md#network-surface) for the detailed model.

### Enable

Launch the editor with `-uaip-http-enable`:

```
UnrealEditor.exe MyProject.uproject -uaip-http-enable
```

To change the port (default: `8765` for editor, `8767` for packaged):

```
UnrealEditor.exe MyProject.uproject -uaip-http-enable -uaip-http-port=9000
```

### Authentication

On startup, UAIP writes a random 32-character Bearer token to:

```
Saved/UAIP/EditorHttpAuthToken.txt
```

Include this token in every request:

```http
Authorization: Bearer <token>
```

For development or CI environments where authentication is not needed:

```
-uaip-http-no-auth
```

### Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/uaip/health` | Health check — returns `{"status":"ok"}` |
| GET | `/uaip/capabilities` | Available capabilities for the current session |
| POST | `/uaip/sessions` | Create a session — returns `{"SessionId":"..."}` |
| DELETE | `/uaip/sessions/:sessionId` | End a session |
| POST | `/uaip/commands` | Execute a command |
| POST | `/uaip/scenarios` | Execute a scenario (waits for completion) |
| GET | `/uaip/artifacts/:artifactId` | Download an artifact |
| GET | `/uaip/sessions/:sessionId/artifacts` | List artifacts for a session |

### Executing a command

```http
POST /uaip/commands
Content-Type: application/json
Authorization: Bearer <token>

{
  "CommandName": "UAIP.Core.HealthCheck",
  "Params": {},
  "SessionId": "my-session"
}
```

Response:

```json
{
  "Success": true,
  "Data": { ... },
  "Artifacts": [...],
  "ErrorCode": null,
  "ErrorMessage": null
}
```

### Limits

| Item | Limit |
|---|---|
| Max request body | 64 KiB |
| Max artifact response | 100 MiB |
| Max concurrent commands | 1 |
| Command timeout | 120 s |

---

## WebSocket (Pro)

The WebSocket transport provides persistent bidirectional connections with real-time log streaming.

### Enable

```
UnrealEditor.exe MyProject.uproject -uaip-ws-enable
```

Custom port (default: `8766` for editor, `8768` for packaged):

```
UnrealEditor.exe MyProject.uproject -uaip-ws-enable -uaip-ws-port=9001
```

### Connection URL

```
ws://127.0.0.1:8766/
```

Connections are restricted to localhost (`127.0.0.1` and `::1`).

### Authentication

On startup, UAIP writes a token to:

```
Saved/UAIP/EditorWsAuthToken.txt
```

Include it in the first request frame:

```json
{
  "Type": "CommandRequest",
  "ClientProtocolVersion": "1.0",
  "Token": "<token>",
  "RequestId": "req-001",
  "SessionId": "my-session",
  "CommandName": "UAIP.Core.HealthCheck",
  "Params": {}
}
```

To disable authentication (development / CI only):

```
-uaip-ws-no-auth
```

### Handshake & message flow

```mermaid
sequenceDiagram
    autonumber
    participant C as WS client
    participant S as Editor WS server

    C->>S: WebSocket upgrade (ws://127.0.0.1:8766/)
    S-->>C: AuthChallenge
    C->>S: First frame { Type: "CommandRequest", Token, SessionId, ... }
    alt auth ok
        S-->>C: Welcome { SessionId, Capabilities }
        loop while connected
            C->>S: CommandRequest / ScenarioRequest
            S-->>C: CommandResponse / ScenarioResponse
            S-->>C: OutputLogEntry (streamed, async)
        end
    else auth failed
        S-->>C: close 1008
    end
```

**Inbound (client → server):**

| `Type` | Purpose |
|---|---|
| `CommandRequest` | Execute a command |
| `ScenarioRequest` | Execute a scenario |

**Outbound (server → client):**

| `Event` | Purpose |
|---|---|
| `AuthChallenge` | Authentication required |
| `Welcome` | Connection established — includes `SessionId` and `Capabilities` |
| `CommandResponse` | Command result |
| `ScenarioResponse` | Scenario result |
| `OutputLogEntry` | Streamed log line (real-time) |

### Output log streaming

The server pushes `OutputLogEntry` events for all UE log output in real time. To disable:

```
-uaip-ws-no-output-log
```

### Limits

| Item | Limit |
|---|---|
| Max receive message | 64 KiB |
| Max scenario payload | 1 MiB |
| Max concurrent connections | 4 |
| Handshake timeout | 5 s |
| Command timeout | 12 s |

---

## CLI (Pro)

The CLI transport runs commands by launching the editor with specific arguments. It is suited for shell scripts and CI pipelines that need tight one-shot automation without a persistent server.

### One-shot execution

The editor executes the command, writes the result, and exits.

**Inline JSON:**

```
UnrealEditor.exe MyProject.uproject -uaip-request="{\"CommandName\":\"UAIP.Core.HealthCheck\",\"Params\":{}}"
```

**From a JSON file:**

```
UnrealEditor.exe MyProject.uproject -uaip-request-file="Saved/UAIP/Requests/cmd.json"
```

**Write the response to a file:**

```
UnrealEditor.exe MyProject.uproject -uaip-request-file="..." -uaip-response-file="Saved/UAIP/Responses/result.json"
```

**Scenario from a file:**

```
UnrealEditor.exe MyProject.uproject -uaip-scenario-file="path/to/scenario.json"
```

### Stream mode

In stream mode the editor reads JSON requests from stdin and writes responses to stdout. This is the mode used internally by the MCP Bridge.

```mermaid
sequenceDiagram
    autonumber
    participant Br as Bridge / wrapper
    participant Ed as UnrealEditor.exe

    Br->>Ed: spawn (-uaip-stdin-stream)
    Ed-->>Br: stdout: __UAIP_STREAM_READY__
    loop while editor alive
        Br->>Ed: stdin: { "CommandName": "...", ... }\n
        Ed-->>Br: stdout: __UAIP_RESPONSE_BEGIN__
        Ed-->>Br: stdout: { "Success": true, ... }
        Ed-->>Br: stdout: __UAIP_RESPONSE_END__
    end
    Br->>Ed: stdin EOF (or kill)
    Ed-->>Br: process exit
```

The markers (`__UAIP_*__`) make it possible to mix request/response with normal UE log output on stdout.

```
UnrealEditor.exe MyProject.uproject -uaip-stdin-stream
```

**stdout markers:**

| Marker | Meaning |
|---|---|
| `__UAIP_STREAM_READY__` | Editor is ready to receive requests |
| `__UAIP_RESPONSE_BEGIN__` | Start of a JSON response |
| `__UAIP_RESPONSE_END__` | End of a JSON response |

### CLI flags reference

| Flag | Description |
|---|---|
| `-uaip-request=<json>` | Execute a command from inline JSON |
| `-uaip-stdin` | Read a single request from stdin |
| `-uaip-request-file=<path>` | Read a command from a JSON file |
| `-uaip-response-file=<path>` | Write the response to a file |
| `-uaip-scenario=<json>` | Execute a scenario from inline JSON |
| `-uaip-scenario-file=<path>` | Read a scenario from a JSON file |
| `-uaip-stdin-stream` | Enable persistent stream mode |

### Limits

| Item | Limit |
|---|---|
| Max request body | 1 MiB |
| Command timeout | 120 s |

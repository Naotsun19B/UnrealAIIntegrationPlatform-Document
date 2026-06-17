**[日本語](../ja/api.md)** | [Back to README](../../README.md)

# API Reference

This is the **machine-oriented reference** for UAIP — request / response shapes, error codes, artifact contracts, scenario primitives, and the per-command JSON schema dump. If you're integrating UAIP from your own tooling (LLM agents, CI scripts, code generators), this is the page to bookmark.

For human-oriented browsing of what commands exist, use [Commands Reference](commands.md).

---

## Table of contents

1. [Transport endpoints](#1-transport-endpoints)
2. [Request format](#2-request-format)
3. [Response format](#3-response-format)
4. [Error codes](#4-error-codes)
5. [Artifact contract](#5-artifact-contract)
6. [Session API](#6-session-api)
7. [Scenario API](#7-scenario-api)
8. [Type mapping (UE → JSON)](#8-type-mapping-ue--json)
9. [Per-command schema dump](#9-per-command-schema-dump)
10. [Client examples](#10-client-examples)
11. [Versioning policy](#11-versioning-policy)

---

## 1. Transport endpoints

Every transport eventually lands on the same `CommandDispatcher`, so capability, policy, and ErrorCode semantics are identical no matter which transport you use.

| Transport | Format | Editor port | Packaged port | Bind layer | Auth |
|---|---|---|---|---|---|
| HTTP (Pro) | REST + JSON | 8765 | 8767 | `0.0.0.0` — FullHTTP is reachable from another machine; MCPOnly mode enforces localhost at the app layer | `Authorization: Bearer <token>` |
| WebSocket (Pro) | JSON frames | 8766 | 8768 | `127.0.0.1` (hard-coded) | First frame `Token` field |
| CLI (Pro) | stdin/stdout + CLI flags | n/a | n/a | — | none (in-process) |
| MCP | stdio child of AI client | n/a | n/a | — | none (child process) |

Token files (auto-generated at editor startup):

```
<YourProject>/Saved/UAIP/EditorHttpAuthToken.txt
<YourProject>/Saved/UAIP/EditorWsAuthToken.txt
```

See [Security → Network surface](security.md#network-surface) for the detailed bind / auth layering.

---

## 2. Request format

### 2.1 `CommandRequest` (HTTP `POST /uaip/commands`)

```json
{
  "CommandName": "UAIP.Editor.Observation.CaptureActiveWindowImage",
  "Params":      { ... },
  "SessionId":   "my-task-001"
}
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `CommandName` | string | yes | Fully-qualified name (e.g. `UAIP.Core.HealthCheck`) |
| `Params` | object | no | Command-specific parameters (default `{}`); validated against the command's `ParameterSchema` |
| `SessionId` | string | no | `[A-Za-z0-9_-]{1,128}`. Omitting creates an anonymous session |

### 2.2 `CommandRequest` (WebSocket frame)

```json
{
  "Type":                  "CommandRequest",
  "ClientProtocolVersion": "1.0",
  "Token":                 "<32-char-bearer>",
  "RequestId":             "req-001",
  "SessionId":             "my-task-001",
  "CommandName":           "UAIP.Core.HealthCheck",
  "Params":                {}
}
```

- `Token` is required only in the first frame; the connection is then trusted for its lifetime
- `RequestId` is echoed back in the corresponding `CommandResponse`, so the client can correlate
- `ClientProtocolVersion` lets the server negotiate compatibility

### 2.3 `CommandRequest` (CLI inline)

```
UnrealEditor.exe MyProject.uproject -uaip-request="{\"CommandName\":\"UAIP.Core.HealthCheck\",\"Params\":{}}"
```

Or, for repeat use:

```
UnrealEditor.exe MyProject.uproject -uaip-request-file=path/to/cmd.json
```

CLI requests get an auto-generated `SessionId` and the editor exits after the response is written.

### 2.4 `CommandRequest` (MCP)

The MCP Bridge wraps the same `CommandRequest` shape into a tool call:

```python
uaip_execute(
    CommandName="UAIP.Editor.Observation.CaptureActiveWindowImage",
    Params={"TabId": "/Game/Maps/Main"},
    SessionId="my-task-001"
)
```

The bridge sets `SessionId` automatically if omitted (`MCP-Anonymous-<guid>`).

---

## 3. Response format

### 3.1 `CommandResponse` (uniform across transports)

```json
{
  "Success":      true,
  "Data":         { ... },
  "Artifacts":    [ { "ArtifactId": "...", "FilePath": "...", "Type": "Image" } ],
  "ErrorCode":    "Success",
  "ErrorMessage": ""
}
```

| Field | Type | Notes |
|---|---|---|
| `Success` | bool | True if `ErrorCode == "Success"` |
| `Data` | object | Command-specific result data (shape defined by each command) |
| `Artifacts` | array | One entry per produced artifact; see [§5](#5-artifact-contract) |
| `ErrorCode` | string | One of the codes in [§4](#4-error-codes), or `"Success"` |
| `ErrorMessage` | string | Human-readable detail; empty on success |

### 3.2 WebSocket envelope

```json
{
  "Event":     "CommandResponse",
  "RequestId": "req-001",
  "Response":  { /* CommandResponse */ }
}
```

The server may also push unprompted events:

| `Event` | Direction | Purpose |
|---|---|---|
| `AuthChallenge` | server → client | Request authentication on a fresh connection |
| `Welcome` | server → client | Sent after successful auth; carries `SessionId` + `Capabilities` |
| `CommandResponse` | server → client | Reply to a `CommandRequest` |
| `ScenarioResponse` | server → client | Reply to a `ScenarioRequest` |
| `OutputLogEntry` | server → client | UE log streaming (suppressible with `-uaip-ws-no-output-log`) |

### 3.3 CLI response

When `-uaip-response-file=<path>` is supplied the JSON is written there. Without it, the response is bracketed by stdout markers:

```
__UAIP_RESPONSE_BEGIN__
{ "Success": true, ... }
__UAIP_RESPONSE_END__
```

In stdin-stream mode the same markers appear per request.

---

## 4. Error codes

| ErrorCode | HTTP status | When | How to recover |
|---|---|---|---|
| `Success` | 200 | Command completed | — |
| `CommandNotFound` | 404 | `CommandName` not registered | Verify with `UAIP.Core.ListCommands`; optional-plugin commands need the plugin loaded |
| `InvalidParams` | 400 | Missing required / wrong type / unknown field (with `AdditionalProperties:false`) | Re-fetch the schema via `UAIP.Core.DescribeCommand` |
| `CapabilityNotAvailable` | 403 | Session lacks a required Capability | `ErrorMessage` names the missing capability; enable it via `Config/DefaultUAIP.ini` and restart or call `UAIP.Core.ReloadCapabilities` |
| `PolicyViolation` | 403 | SafetyPolicy gate or missing route opt-in | `ErrorMessage` distinguishes "denied by SafetyPolicy" vs "not enabled in this environment" |
| `NotFound` | 404 | Asset / actor / object referenced by params doesn't exist | Verify path / GUID with a `Search*` or `List*` command |
| `NotAllowed` | 409 | Forbidden path (e.g. `/Engine/`) or forbidden timing (editor edit during PIE) | Choose a different path or wait for PIE to stop |
| `ExecutionFailed` | 500 | Runtime failure inside the handler | `ErrorMessage` carries detail; inside a scenario use `RetryCount` |
| `Timeout` | 408 | Per-step or per-scenario wall-clock cap exceeded | Increase `TimeoutSeconds` or split the scenario |
| `TooManyRequests` | 429 | Concurrency limit hit (1 scenario at a time, etc.) | Wait for the in-flight request to finish |
| `InternalError` | 500 | Process-fault level (handler threw, dispatcher invariant broken) | `RestartEditor`; if it persists, capture `Saved/Crashes/` and file an issue |

HTTP status codes are advisory — always rely on `ErrorCode` for branching. WebSocket and CLI don't carry HTTP statuses.

---

## 5. Artifact contract

### 5.1 `Artifact` object

```json
{
  "ArtifactId":   "8D1403DB4896B4742E423CBD9F535F19",
  "FilePath":     "MCP-Anonymous-7b8e/Screenshots/CaptureActiveWindowImage-8D14....png",
  "Type":         "Image",
  "ContentType":  "image/png",
  "SizeBytes":    524288,
  "CreatedAt":    "2026-06-17T05:34:12Z"
}
```

| Field | Type | Notes |
|---|---|---|
| `ArtifactId` | string | 32-char hex; primary key for fetch |
| `FilePath` | string | Server-internal **relative** path under `Saved/UAIP/`. Don't reconstruct it on the client side — use `ArtifactId` |
| `Type` | enum | `Image` / `Json` / `Log` / `Report` / `Bundle` |
| `ContentType` | string | MIME type for fetch |
| `SizeBytes` | int | Useful for streaming budget decisions |
| `CreatedAt` | string | ISO 8601, UTC |

### 5.2 Fetching artifact bytes

```http
GET /uaip/artifacts/{artifactId}
Authorization: Bearer <token>
```

Response: the raw bytes, with `Content-Type` from the artifact's metadata. 404 if the artifact has been GC'd (session ended or TTL expired).

For sessions, listing is available:

```http
GET /uaip/sessions/{sessionId}/artifacts
Authorization: Bearer <token>
```

### 5.3 Inline embedding (MCP bridge only)

The MCP bridge can base64-inline small artifacts into the response:

```json
{
  "Success": true,
  "Artifacts": [ { "ArtifactId": "...", "Type": "Json", ... } ],
  "_inlined_artifacts": [
    {
      "artifact_id":   "...",
      "content_type":  "application/json",
      "data_base64":   "eyJTdGF0dXMiOiJIZWFsdGh5In0="
    }
  ]
}
```

See [Artifacts → Inline-vs-fetch decision](artifacts.md#inline-vs-fetch-decision) for the inline policy. HTTP / WebSocket / CLI never inline — they always require the fetch round-trip.

---

## 6. Session API

### 6.1 Create / use a session

Sessions are created implicitly on the first command using a new `SessionId`. There is no separate create call — just pass `SessionId="my-task"` in the first request.

Explicit creation (HTTP, optional):

```http
POST /uaip/sessions
Authorization: Bearer <token>
Content-Type: application/json

{ "Hint": "my-task" }
```

Response:

```json
{ "SessionId": "my-task-1718601234" }
```

### 6.2 Query a session

```http
GET /uaip/sessions/{sessionId}
Authorization: Bearer <token>
```

Returns the session's Capabilities, OperationalConstraints (SafetyPolicy snapshot), and artifact count.

### 6.3 End a session

```
uaip_execute(CommandName="UAIP.Core.EndSession", Params={"SessionId":"my-task"})
```

Or HTTP:

```http
DELETE /uaip/sessions/{sessionId}
Authorization: Bearer <token>
```

Ending a session releases observed-widget caches and marks artifacts for GC.

### 6.4 Capability discovery

```
uaip_execute(CommandName="UAIP.Core.QueryCapabilities")
```

Response `Data`:

```json
{
  "Capabilities": ["EditorInspect", "PIEControl", "RuntimeCapture", ...],
  "OperationalConstraints": {
    "ReadOnly":              false,
    "DisableSave":           false,
    "AllowLogDump":          true,
    "AllowContextMenuMutation": false,
    "AllowKeyboardInput":    true,
    "AllowKeyboardModifierInput": false,
    "DisablePIEStart":       false
  }
}
```

Use `OperationalConstraints` as a forward-looking gate: if `ReadOnly:true`, don't attempt mutating commands.

---

## 7. Scenario API

Scenarios run an ordered list of commands as one request. See [Scenario Execution](scenario.md) for the conceptual guide.

### 7.1 `ScenarioRequest`

```json
{
  "ScenarioName": "MyScenario",
  "SessionId":    "scenario-001",
  "Variables":    { "TargetHp": 100 },
  "Steps": [
    {
      "StepName":       "Load",
      "CommandName":    "UAIP.Runtime.PIE.LoadMap",
      "Params":         { "MapPath": "/Game/Maps/Foo" },
      "AbortOnFailure": true,
      "RetryCount":     0,
      "TimeoutSeconds": 60
    }
  ]
}
```

| Step field | Type | Default | Notes |
|---|---|---|---|
| `StepName` | string | — | `[A-Za-z0-9_]{1,64}`, unique per scenario |
| `CommandName` | string | — | Same as `uaip_execute` |
| `Params` | object | `{}` | After template resolution |
| `AbortOnFailure` | bool | `true` | If false, scenario continues even if this step fails |
| `RetryCount` | int | `0` | Retry on `ExecutionFailed` only — never on `CapabilityNotAvailable` / `PolicyViolation` |
| `TimeoutSeconds` | int | `60` | Per-step wall-clock cap |

### 7.2 Template expressions

| Expression | Resolves to |
|---|---|
| `${StepName.Success}` | bool |
| `${StepName.ErrorCode}` | string |
| `${StepName.Data.<JSON Pointer>}` | Any JSON value at that pointer in the step's `Data` |
| `${StepName.Artifacts[<index>]}` | Artifact id string |
| `${StepName.Artifacts.<ArtifactId>}` | Artifact id string |
| `${Variables.<key>}` | Value from the request's `Variables` map |

**Type preservation**: if a string field is exactly one `${...}` expression, the resolved JSON value replaces it verbatim. Mixed strings stringify and concatenate.

**Single-pass invariant**: a template result is never re-evaluated. A `${...}` stored inside `Variables` is passed as a literal string to downstream steps.

### 7.3 `ScenarioResponse`

```json
{
  "ScenarioId":         "fc2a1c2e-...-7e9c",
  "ScenarioName":       "MyScenario",
  "Status":             "Completed",
  "StartedAt":          "2026-06-17T05:34:10Z",
  "CompletedAt":        "2026-06-17T05:34:18Z",
  "AllStepsSucceeded":  true,
  "StepResults": [
    {
      "StepName":     "Load",
      "Success":      true,
      "ErrorCode":    "Success",
      "ErrorMessage": "",
      "Data":         { ... },
      "ArtifactIds":  ["8D14..."],
      "AttemptCount": 1,
      "DurationMs":   1234
    }
  ],
  "ArtifactIds": ["8D14...", "F521..."]
}
```

| `Status` | Meaning |
|---|---|
| `Completed` | Every step succeeded |
| `Failed` | At least one step returned `Success:false` |
| `Aborted` | Scenario-wide 1800-second cap exceeded |

### 7.4 Hard limits

| Limit | Value |
|---|---|
| Max steps | 100 |
| Per-scenario wall-clock cap | 1800 s |
| Concurrent scenarios | 1 (`TooManyRequests` otherwise) |
| Per-step `Params` string | 8 KiB |
| Total `Params` payload | 256 KiB |
| Total `ScenarioRequest` size | 1 MiB |

---

## 8. Type mapping (UE → JSON)

When generating clients or LLM prompts, you need to know how UE C++ types appear in the JSON wire format.

| UE C++ type | JSON | Example |
|---|---|---|
| `bool` | bool | `true` |
| `int32` / `int64` | number (integer) | `42` |
| `float` / `double` | number | `3.14` |
| `FString` / `FName` / `FText` | string | `"PlayerCharacter"` |
| `FGuid` | string (32-char hex, no braces / hyphens) | `"8D1403DB4896B4742E423CBD9F535F19"` |
| `FVector` | object `{X,Y,Z}` | `{"X":0,"Y":0,"Z":100}` |
| `FRotator` | object `{Pitch,Yaw,Roll}` | `{"Pitch":0,"Yaw":90,"Roll":0}` |
| `FTransform` | object `{Location,Rotation,Scale}` | nested |
| `FLinearColor` | object `{R,G,B,A}` (0.0–1.0) | `{"R":1,"G":0,"B":0,"A":1}` |
| `FColor` | object `{R,G,B,A}` (0–255 int) | `{"R":255,"G":0,"B":0,"A":255}` |
| `TArray<T>` | array of `T` | `[1,2,3]` |
| `TMap<FString,T>` | object | `{"k":v}` |
| `UObject*` reference | string (asset path or actor identifier) | `"/Game/Blueprints/BP_Foo"` |
| `TSubclassOf<T>` | string (class path) | `"/Script/Engine.StaticMeshActor"` |
| `enum class` | string (enum value name) | `"Default"` |
| `FInstancedStruct` | object `{StructType, Value:{...}}` | `{"StructType":"/Script/Foo.FBar","Value":{...}}` |

NaN / Inf are rejected for `Number` fields — the dispatcher returns `InvalidParams`.

---

## 9. Per-command schema dump

For programmatic use — tooling, code generation, LLM-side validation — fetch the full schema for every command as a single JSON.

### 9.1 Three sources

| Source | Use when | Caveat |
|---|---|---|
| `UAIP.Core.DescribeCommand` at runtime | One command at a time, reflects the running editor exactly | Requires a live editor |
| Pre-generated `commands-schema.json` (shipped with releases) | Build-time tools, offline codegen | Stable snapshot of a known UAIP version |
| Generate locally via `docs/scripts/generate_command_schema.py` | Includes project-specific commands registered via `ICommandProvider` | Requires running editor + HTTP transport |

### 9.2 Generating locally

```powershell
$Token = Get-Content "<YourProject>/Saved/UAIP/EditorHttpAuthToken.txt"
$env:UAIP_HTTP_TOKEN = $Token

python docs/scripts/generate_command_schema.py `
    --host http://127.0.0.1:8765 `
    --out  commands-schema.json
```

Add `--no-auth` if launched with `-uaip-http-no-auth`. Add `--split-by-provider` for one JSON per provider under `by-provider/`.

Expected runtime: 10–60 s for ~730 commands depending on optional plugin set.

### 9.3 Output shape

```json
{
  "generatedAt":     "2026-06-17T05:34:12Z",
  "uaipVersion":     "1.0.0",
  "engineVersion":   "5.8.0",
  "commandCount":    735,
  "commands": [
    {
      "Name":                 "UAIP.Editor.Blueprint.AddBlueprintVariable",
      "ProviderName":         "UAIP.Editor.Blueprint",
      "Description":          "Add a member variable to a Blueprint (type, default, tooltip).",
      "RequiredCapabilities": ["BlueprintEdit", "BlueprintVariableEdit"],
      "IsReadOnly":           false,
      "Available":            true,
      "Stability":            "Stable",
      "DeprecationMessage":   null,
      "MigrationTarget":      null,
      "ParameterSchema": {
        "Type":                 "Object",
        "AdditionalProperties": false,
        "Properties": {
          "BlueprintPath":   { "Type": "String",  "Description": "Path of the Blueprint asset (e.g. /Game/Blueprints/BP_Foo)" },
          "VariableName":    { "Type": "String",  "Description": "Variable name; must be a valid identifier" },
          "PinCategory":     { "Type": "String",  "Description": "Pin category (bool / int / real / object / struct / …)" },
          "PinSubCategory":  { "Type": "String",  "Description": "Sub-category (e.g. double for real)" },
          "DefaultValue":    { "Type": "String",  "Description": "ImportText-format default value" }
        },
        "Required": ["BlueprintPath", "VariableName", "PinCategory"]
      }
    }
  ]
}
```

### 9.4 Three representative schemas

#### Simple, no params

```json
{
  "Name": "UAIP.Core.HealthCheck",
  "RequiredCapabilities": [],
  "IsReadOnly": true,
  "ParameterSchema": {
    "Type": "Object", "AdditionalProperties": false,
    "Properties": {}, "Required": []
  }
}
```

#### Nested objects

```json
{
  "Name": "UAIP.Editor.Level.SetActorTransform",
  "RequiredCapabilities": ["EditorActorEdit"],
  "IsReadOnly": false,
  "ParameterSchema": {
    "Type": "Object", "AdditionalProperties": false,
    "Properties": {
      "ActorIdentifier": { "Type": "String" },
      "Location": { "Type": "Object", "Properties": {
        "X": {"Type":"Number"}, "Y": {"Type":"Number"}, "Z": {"Type":"Number"}
      } },
      "Rotation": { "Type": "Object", "Properties": {
        "Pitch": {"Type":"Number"}, "Yaw": {"Type":"Number"}, "Roll": {"Type":"Number"}
      } },
      "Scale":    { "Type": "Object", "Properties": {
        "X": {"Type":"Number"}, "Y": {"Type":"Number"}, "Z": {"Type":"Number"}
      } }
    },
    "Required": ["ActorIdentifier"]
  }
}
```

#### Array + enum-string

```json
{
  "Name": "UAIP.Editor.Assets.SearchAssets",
  "RequiredCapabilities": ["EditorInspect"],
  "IsReadOnly": true,
  "ParameterSchema": {
    "Type": "Object", "AdditionalProperties": false,
    "Properties": {
      "Path":       { "Type": "String", "Description": "Content path prefix (e.g. /Game/Characters)" },
      "ClassNames": { "Type": "Array",  "Description": "Asset class names; one of Blueprint / Material / DataAsset / ..." },
      "Recursive":  { "Type": "Boolean" }
    },
    "Required": ["Path"]
  }
}
```

---

## 10. Client examples

### 10.1 HTTP — curl

```bash
TOKEN=$(cat /path/to/Saved/UAIP/EditorHttpAuthToken.txt)

curl -s -X POST http://127.0.0.1:8765/uaip/commands \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "CommandName": "UAIP.Core.HealthCheck",
    "Params": {},
    "SessionId": "smoke-test"
  }' | jq .
```

Fetch an artifact:

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8765/uaip/artifacts/8D1403DB4896B4742E423CBD9F535F19 \
  -o capture.png
```

### 10.2 HTTP — Python

```python
import requests

class UAIPClient:
    def __init__(self, host="http://127.0.0.1:8765", token=None):
        self.host = host
        self.session = requests.Session()
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
        self.session.headers["Content-Type"] = "application/json"

    def execute(self, command, params=None, session_id=None):
        body = {"CommandName": command, "Params": params or {}}
        if session_id:
            body["SessionId"] = session_id
        r = self.session.post(f"{self.host}/uaip/commands", json=body, timeout=120)
        r.raise_for_status()
        data = r.json()
        if not data["Success"]:
            raise RuntimeError(f'{data["ErrorCode"]}: {data["ErrorMessage"]}')
        return data

    def fetch_artifact(self, artifact_id):
        r = self.session.get(f"{self.host}/uaip/artifacts/{artifact_id}", timeout=60)
        r.raise_for_status()
        return r.content

client = UAIPClient(token=open("...EditorHttpAuthToken.txt").read().strip())
print(client.execute("UAIP.Core.HealthCheck")["Data"])
```

### 10.3 WebSocket — JavaScript

```javascript
import WebSocket from "ws";
import { readFileSync } from "fs";

const token = readFileSync(".../EditorWsAuthToken.txt", "utf-8").trim();
const ws = new WebSocket("ws://127.0.0.1:8766/");

const pending = new Map();
let nextId = 1;

ws.on("open", () => {
  ws.send(JSON.stringify({
    Type: "CommandRequest",
    ClientProtocolVersion: "1.0",
    Token: token,
    RequestId: "init",
    SessionId: "ws-session",
    CommandName: "UAIP.Core.HealthCheck",
    Params: {}
  }));
});

ws.on("message", (raw) => {
  const msg = JSON.parse(raw);
  if (msg.Event === "CommandResponse") {
    const cb = pending.get(msg.RequestId);
    if (cb) { pending.delete(msg.RequestId); cb(msg.Response); }
    else    { console.log("init:", msg.Response); }
  }
});

function execute(command, params, sessionId) {
  return new Promise((resolve) => {
    const id = `req-${nextId++}`;
    pending.set(id, resolve);
    ws.send(JSON.stringify({
      Type: "CommandRequest",
      RequestId: id,
      SessionId: sessionId,
      CommandName: command,
      Params: params
    }));
  });
}
```

### 10.4 CLI — PowerShell one-shot

```powershell
@'
{
  "CommandName": "UAIP.Editor.Execution.RunAutomationTest",
  "Params":      { "TestName": "MyGame.Smoke.MainMenu" }
}
'@ | Set-Content cmd.json

& "C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe" `
    "$pwd/MyGame.uproject" `
    "-uaip-request-file=$pwd/cmd.json" `
    "-uaip-response-file=$pwd/result.json"

$result = Get-Content result.json | ConvertFrom-Json
if (-not $result.Success) {
    Write-Error "$($result.ErrorCode): $($result.ErrorMessage)"
    exit 1
}
```

### 10.5 CLI — stdin-stream wrapper (Python)

```python
import subprocess, json, threading

proc = subprocess.Popen(
    ["UnrealEditor.exe", "MyGame.uproject", "-uaip-stdin-stream"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    text=True, bufsize=1
)

def read_responses():
    buffer, capturing = [], False
    for line in proc.stdout:
        if "__UAIP_STREAM_READY__" in line:
            print("editor ready")
        elif "__UAIP_RESPONSE_BEGIN__" in line:
            capturing, buffer = True, []
        elif "__UAIP_RESPONSE_END__" in line:
            capturing = False
            yield json.loads("".join(buffer))
        elif capturing:
            buffer.append(line)

threading.Thread(target=lambda: list(read_responses()), daemon=True).start()

proc.stdin.write(json.dumps({"CommandName":"UAIP.Core.HealthCheck","Params":{}}) + "\n")
proc.stdin.flush()
```

---

## 11. Versioning policy

UAIP follows **semantic versioning** at the command level:

- **Major (1.x → 2.x)**: breaking changes allowed — renamed commands, changed parameter shapes, capability renames
- **Minor (1.0 → 1.1)**: additive only — new commands, new optional parameters, new fields in `Data`. Existing fields stay
- **Patch (1.0.0 → 1.0.1)**: bug fixes only, no schema change

### Stability tiers per command

| `Stability` | Contract |
|---|---|
| `Stable` | Schema is fixed across minor versions. Renames / removals only on major bumps |
| `Experimental` | Schema may change in any release. Treat the schema dump as a snapshot, not a contract |
| `Deprecated` | Will be removed in the next major. `DeprecationMessage` + `MigrationTarget` are populated |

### Capability renames

When a `RequiredCapabilities` entry is renamed, the old name remains a deny-default alias for one minor version cycle (e.g. renamed in 1.2, old alias still recognized in 1.2 and 1.3, removed in 2.0).

### Reading the version

```
uaip_execute(CommandName="UAIP.Core.GetSystemInfo")
```

Returns `UAIPVersion`, `EngineVersion`, `BuildConfig`, plus the `commandCount` reflected by the running editor.

---

## See also

- [Commands Reference](commands.md) — one-line-per-command browsable index
- [Safety & Capabilities](safety.md) — Capability and SafetyPolicy reference
- [Architecture](architecture.md) — internal dispatch path
- [Connection Methods](connections.md) — transport-by-transport setup
- [Scenario Execution](scenario.md) — scenario route conceptual guide
- [Artifacts](artifacts.md) — artifact lifecycle and inline policy

**[日本語](../ja/api.md)** | [Back to README](../../README.md)

# API Reference — Full Command Schemas

The [Commands Reference](commands.md) lists every command with a one-line description. For programmatic use — tooling, code generation, LLM-side validation — you need the **full schema** for each command (parameter types, required fields, default values, capability requirements).

This page describes how to produce that full schema as JSON and how to consume it.

---

## Three ways to fetch a command's full schema

| Source | Use when | Notes |
|---|---|---|
| `uaip_describe_command(CommandName="...")` | At runtime, one command at a time | Reflects what the running editor actually has. Best for "is this command available with my plugin set?" |
| Pre-generated JSON dump (this page) | Building tools / generators offline | Stable snapshot of a known UAIP version. No editor required at consumption time |
| Reading source headers | Last resort | Authoritative but harder to parse mechanically |

---

## Generating the dump yourself

A standalone script is included in this repo at [`docs/scripts/generate_command_schema.py`](../scripts/generate_command_schema.py).

### Prerequisites

- A UE editor with the UAIP plugin enabled
- The editor launched with the HTTP transport: `-uaip-http-enable`
- Python 3.10+ with `requests` (`pip install requests`)

### Run

```powershell
# Find the auth token the editor wrote at startup
$Token = Get-Content "<YourProject>/Saved/UAIP/EditorHttpAuthToken.txt"
$env:UAIP_HTTP_TOKEN = $Token

# Generate the schema dump
python docs/scripts/generate_command_schema.py `
    --host http://127.0.0.1:8765 `
    --out  commands-schema.json
```

Add `--no-auth` if the editor was launched with `-uaip-http-no-auth`. Add `--split-by-provider` to also emit one JSON per provider under `by-provider/`.

### Runtime

Expect 10–60 seconds for the ~730 commands depending on optional plugins.

---

## Output format

```json
{
  "generatedAt": "2026-06-17T05:34:12Z",
  "uaipVersion": "1.0.0",
  "engineVersion": "5.8.0",
  "commandCount": 735,
  "commands": [
    {
      "Name": "UAIP.Core.HealthCheck",
      "ProviderName": "UAIP.Core",
      "Description": "Plugin connectivity check — returns Status, UAIPVersion, EngineVersion, BuildConfig.",
      "RequiredCapabilities": [],
      "IsReadOnly": true,
      "Available": true,
      "Stability": "Stable",
      "ParameterSchema": {
        "Type": "Object",
        "AdditionalProperties": false,
        "Properties": {},
        "Required": []
      }
    },
    ...
  ]
}
```

### Per-command descriptor fields

| Field | Type | Notes |
|---|---|---|
| `Name` | string | Fully-qualified command name |
| `ProviderName` | string | Owning provider (`UAIP.Editor.Blueprint`, `Toolset.AnimationAssistant`, …) |
| `Description` | string | Human-readable one-line summary |
| `RequiredCapabilities` | array of string | All must be present in the session |
| `IsReadOnly` | bool | If true, never blocked by `ReadOnly=True` SafetyPolicy |
| `Available` | bool | False when an optional plugin isn't loaded |
| `Stability` | enum | `Stable` / `Experimental` / `Deprecated` |
| `DeprecationMessage` | string? | Present when `Stability=Deprecated` |
| `MigrationTarget` | string? | Replacement command name for deprecated entries |
| `ParameterSchema` | object | JSON-Schema-like description of `Params` |

### ParameterSchema shape

The parameter schema is a lightweight JSON-Schema dialect:

```json
{
  "Type": "Object",
  "AdditionalProperties": false,
  "Properties": {
    "ActorIdentifier": { "Type": "String", "Description": "..." },
    "Location":        { "Type": "Object", "Properties": {
                          "X": { "Type": "Number" },
                          "Y": { "Type": "Number" },
                          "Z": { "Type": "Number" }
                        } },
    "Rotation":        { "Type": "Object", "Properties": { ... } }
  },
  "Required": ["ActorIdentifier", "Location"]
}
```

- `Type`: `String` / `Number` / `Integer` / `Boolean` / `Object` / `Array`
- `Required`: fields that may not be omitted
- `AdditionalProperties: false`: extra fields trigger `InvalidParams`
- For enums, the candidate list usually appears in the `Description` text

---

## Example consumers

### Generate TypeScript types from the schema

```typescript
import schema from './commands-schema.json' assert { type: 'json' };

type CommandName = (typeof schema.commands)[number]['Name'];
// → "UAIP.Core.HealthCheck" | "UAIP.Editor.Blueprint.AddGraphNode" | ...
```

### LLM-side validation prompt

> System: When invoking a UAIP command, validate the parameters against the schema below before issuing the call. Reject calls that omit a Required field or contain a field not in Properties.
>
> Schema for `<CommandName>`: { ... }

### Capability-aware command picker

Filter the dump to commands a given session can actually run:

```python
import json
with open("commands-schema.json", "r", encoding="utf-8") as f:
    payload = json.load(f)

granted_capabilities = {"EditorInspect", "EditorObservation", "PIEControl"}
available = [
    cmd for cmd in payload["commands"]
    if cmd["Available"]
       and all(cap in granted_capabilities for cap in cmd["RequiredCapabilities"])
]
print(f"{len(available)} commands callable with current capabilities")
```

---

## Where to get a pre-built dump

Bundled in each plugin release archive as `commands-schema.json`. If you only need a current snapshot for a specific UE version + UAIP version combination, look in the [Releases](../../../releases) — no editor launch required.

For project-specific custom commands (registered via `ICommandProvider` from your own modules), only the locally generated dump captures them.

---

## Schema stability

- **Within a UAIP minor version**, `Name`, `RequiredCapabilities`, and `ParameterSchema` fields are stable.
- **Across major versions**, breaking changes are listed in the [Roadmap](roadmap.md) and announced in release notes.
- **`Stability: Experimental`** commands may change in any release. Treat their schema as informational only.
- **`Stability: Deprecated`** commands include `DeprecationMessage` and `MigrationTarget`. Plan a migration.

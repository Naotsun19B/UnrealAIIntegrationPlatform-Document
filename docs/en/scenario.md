**[日本語](../ja/scenario.md)** | [Back to README](../../README.md)

# Scenario Execution

`uaip_run_scenario` submits an ordered list of commands as one request. Steps run in order on the game thread with per-step abort, retry, and timeout controls.

---

## Enabling scenarios

Scenario execution is disabled by default. Enable it by adding `"enable_scenario": true` to `config.json`:

```json
{
  "editor_path":    "...",
  "uproject_path":  "...",
  "enable_scenario": true
}
```

Reconnect the MCP client after saving.

---

## When to use a scenario

| Use single `uaip_execute` | Use `uaip_run_scenario` |
|---|---|
| One operation (screenshot, open asset) | Ordered procedure (LoadMap → PIE → capture → assert) |
| Read-only, no state transition | Later steps depend on earlier step output |
| Exploration — check result then decide | Need abort-on-failure, retry, or per-step timeout |

**Rule of thumb**: if you are about to call `uaip_execute` two or more times in a row, use a scenario instead.

---

## Execution flow

```mermaid
sequenceDiagram
    autonumber
    participant Cli as Client
    participant Sc as Scenario route
    participant Di as CommandDispatcher
    participant Hd as Step handler
    participant Ar as ArtifactManager

    Cli->>Sc: uaip_run_scenario(Steps[])
    Sc->>Sc: validate (opt-in / size / shape)

    loop for each Step in order
        Sc->>Sc: resolve ${...} templates
        Sc->>Di: DispatchAsync(StepCommand)
        Di->>Hd: Execute(params)
        Hd->>Ar: WriteArtifact(...)
        Ar-->>Hd: ArtifactId
        Hd-->>Di: StepResult
        Di-->>Sc: StepResult
        alt StepResult.Success == false
            alt AbortOnFailure of the failed step == true
                Note over Sc: skip every remaining step
            else AbortOnFailure of the failed step == false
                Note over Sc: continue
            end
        end
    end

    Sc-->>Cli: ScenarioResponse(StepResults[], ArtifactIds[])
```

The scenario route never bypasses authorization — each step goes through the same `CommandDispatcher` and same capability + policy check as a direct `uaip_execute` call. See [Architecture](architecture.md) for the dispatch path.

---

## Invocation shape

```
uaip_run_scenario(
  ScenarioName="MyScenario",          # [A-Za-z0-9_]{1,128}
  SessionId="scenario-<purpose>",      # optional
  Variables={ "Key": "Value", ... },   # optional initial values
  Steps=[
    {
      "StepName":        "Load",        # [A-Za-z0-9_]{1,64}, unique
      "CommandName":     "UAIP.Runtime.PIE.LoadMap",
      "Params":          { "MapPath": "/Game/Maps/TestMap" },
      "AbortOnFailure":  true,          # default: true — see "Failure handling and cleanup"
      "RetryCount":      0,             # default: 0
      "TimeoutSeconds":  60             # default: 60
    },
    ...
  ]
)
```

---

## Template splicing `${...}`

Use `${StepName.Data.<pointer>}` to pass output from an earlier step into a later step's params.

| Expression | Meaning |
|---|---|
| `${StepName.Success}` | bool — true if the step succeeded |
| `${StepName.ErrorCode}` | string error code |
| `${StepName.Data.<pointer>}` | Value inside the step's response data — see notation below |
| `${StepName.Data}` | The whole `Data` object |
| `${StepName.Artifacts[0]}` | First artifact id of the step |
| `${Variables.<key>}` | Value from the `Variables` map |

### JSON Pointer notation

The pointer body has **two accepted notations**, told apart by its first character:

| Notation | Trigger | Behaviour |
|---|---|---|
| **Strict** | Body starts with `/` | Read verbatim as an RFC 6901 JSON Pointer — `.` is never treated as a separator, so a key that itself contains `.` becomes addressable |
| **Lenient** | Body starts with anything else | `.` and `/` are both accepted as segment separators — this is how most existing scenarios are written |

Examples:

| Expression | Notation | Pointer | Result |
|---|---|---|---|
| `${S.Data.Result}` | lenient | `/Result` | The top-level `Result` field |
| `${S.Data.Result/0/refPath}` | lenient | `/Result/0/refPath` | Array element 0's `refPath` field |
| `${S.Data./refPath}` | strict | `/refPath` | Same field, written strictly |
| `${S.Data./a.b/0}` | strict | `/a.b/0` | Array element 0 under the key `a.b` — only reachable in strict notation, since lenient would split on the `.` |
| `${S.Data}` | — | *(empty)* | The whole `Data` object |
| `${S.Data./With~1Slash}` | strict | `/With~1Slash` | A field literally named `With/Slash` (`/` escaped as `~1`) |
| `${S.Data.With~0Tilde}` | lenient | `/With~0Tilde` | A field literally named `With~Tilde` (`~` escaped as `~0`) |

The `~1` / `~0` escapes are part of JSON Pointer semantics, not of the surface notation, so they apply the same way in **both** strict and lenient form. A key that itself contains `~` must be written as `~0`.

Additional constraints:

- **Object key matching is case-sensitive, exact match.** `refPath` does not match a field named `RefPath` or `REFPATH`.
- **Array indices** must be `0` or `[1-9][0-9]*` — no leading zeros (`01`), no sign (`+1`), no trailing characters (`1abc`), no leading whitespace.
- **Objects and arrays can only be spliced as a whole field.** Embedding one inside a larger string (e.g. `"prefix-${S.Data.SomeObject}"`) fails the step instead of silently rendering as an empty string.

Templates are resolved once before the step runs. They are **not** re-evaluated — a template inside `Variables` is passed as a literal string, not re-expanded.

### Template resolution failures

A malformed reference — unknown sub-identifier, empty pointer, invalid `~` escape, a pointer that doesn't match anything in the step's data, an oversized value, an object/array embedded in a mixed string, and so on — fails the step with `ErrorCode: InvalidParams`. This is **not retried**: `RetryCount` only applies to `ExecutionFailed`.

### Template size limits

| Limit | What it bounds | Enforced at |
|---|---|---|
| 64 KiB | One `Variables` entry's value | When the variable is stored |
| 8 KiB | One value spliced from `Step.Data` | Template resolution |
| 256 KiB | One step's whole Params payload, and the total resolved expansion | Submission, and again at resolution |

### Single-pass resolution

```mermaid
flowchart LR
    A["Variables &nbsp;{Hop: '${B.Data.x}'}"] --> R[Resolver]
    B["Step B output<br/>Data.x = 42"] --> R
    R --> C["Step C params<br/>Field: '${Variables.Hop}'"]
    C --> Result["Field = '${B.Data.x}'<br/>(literal — not re-expanded)"]
    style Result fill:#fee,stroke:#c66
```

If you want `Field` to actually receive `42`, reference `${B.Data.x}` directly from Step C's params instead of hopping through `Variables`.

---

## Response shape

```json
{
  "ScenarioId": "<uuid>",
  "Status": "Completed",
  "AllStepsSucceeded": true,
  "StepResults": [
    {
      "StepName": "Load",
      "Success": true,
      "ErrorCode": "Success",
      "ArtifactIds": ["..."]
    }
  ],
  "ArtifactIds": ["...", "..."]
}
```

| Status | Meaning |
|---|---|
| `Completed` | All steps succeeded |
| `Failed` | At least one step failed |
| `Aborted` | Scenario exceeded the 1800-second wall-clock cap |

---

## Hard limits

| Limit | Value |
|---|---|
| Max steps | 100 |
| Scenario wall-clock cap | 1800 seconds |
| Concurrent scenarios | 1 (returns `TooManyRequests` if another is running) |
| Payload size | 1 MiB total, 8 KiB per Params string |

---

## Exclusivity with single commands

A scenario's exclusivity is not limited to other scenarios — it also excludes single commands submitted through `uaip_execute`, in both directions, across **every transport** (HTTP, MCP, and WebSocket alike):

- **While a scenario is running**, a single command submitted by any session — including the session that submitted the scenario — is refused with `TooManyRequests`. This holds for the whole run, up to the 1800-second wall-clock cap; if the wall-clock watchdog fires without the runner actually finishing, the gate stays closed until it does. The one exception is a passive-wait command (see [Configuration → `[UAIP.Transport]` concurrency](config.md#uaiptransport--passive-wait-concurrency-off-by-default)): those are still admitted while a scenario runs, provided `AllowConcurrentPassiveWaits=True` is set — they don't change editor state, so they can't interleave with a scenario's steps.
- **The reverse also holds**: submitting a scenario is refused with `TooManyRequests` while a non-passive command is still executing anywhere in the editor — even one that has already timed out its own response (the HTTP/MCP 120-second async timeout) but is still running server-side, such as a map load or a shader recompile still in progress. Passive waits don't count toward this check, so a long-running wait never blocks starting a scenario.
- If the same command stays in flight for far longer than a scenario's own wall-clock cap would allow, the rejection changes from `TooManyRequests` to `InternalError` with a message indicating the editor needs to be restarted — this distinguishes ordinary congestion (worth retrying) from a wedged handler (not worth retrying).
- Neither direction reveals *what* is currently running, only that something is.

This is a correctness fix, not a new restriction you opt into: earlier releases only excluded other scenarios, so a single command could interleave mid-scenario. If your scenario-based workflow relied on being able to slip a single command in between two scenario submissions from the same session, that no longer works — split the work into two scenarios instead, or issue the single command before or after the scenario, not during.

---

## Example — full PIE validation flow

```json
{
  "ScenarioName": "PIE_HealthCheck",
  "Variables": { "ExpectedHp": "100" },
  "Steps": [
    { "StepName": "Load",   "CommandName": "UAIP.Runtime.PIE.LoadMap",
      "Params": { "MapPath": "/Game/Maps/TestMap" } },
    { "StepName": "Start",  "CommandName": "UAIP.Runtime.PIE.StartPIE", "Params": {} },
    { "StepName": "Settle", "CommandName": "UAIP.Runtime.Assertion.WaitSeconds",
      "Params": { "Seconds": 2 } },
    { "StepName": "Cap",    "CommandName": "UAIP.Runtime.Observation.CaptureViewportImage",
      "Params": {} },
    { "StepName": "Assert", "CommandName": "UAIP.Runtime.Assertion.AssertActorProperty",
      "Params": { "ActorIdentifier": "PlayerCharacter",
                  "PropertyName": "Health",
                  "ExpectedValue": "${Variables.ExpectedHp}" } },
    { "StepName": "Stop",   "CommandName": "UAIP.Runtime.PIE.StopPIE",
      "Params": {} }
  ]
}
```

As written, a failure in `Load` … `Assert` finalizes the scenario at that step and `Stop` is never dispatched — PIE stays running. See the next section for why, and what to do about it.

---

## Failure handling and cleanup

`AbortOnFailure` is evaluated on **the step that just failed**, never on the steps that come after it:

- The failed step's own `AbortOnFailure` is `true` (the default) → the scenario finalizes immediately. Every later step is never dispatched and never appears in `StepResults`.
- The failed step's own `AbortOnFailure` is `false` → execution continues with the next step; the failure is still recorded in `StepResults`.

`AbortOnFailure: false` therefore means "a failure of **this** step is not fatal", not "run this step even after an earlier failure". Putting it only on a trailing cleanup step (`StopPIE`, delete-temp-asset, close-tab, …) does **not** make that step run — it is skipped along with everything else after the failure.

The same rule applies when a step fails template resolution (`InvalidParams`): that step's own flag decides.

### Making a cleanup step actually run

| Approach | What to do | Trade-off |
|---|---|---|
| Give up fail-fast | Set `AbortOnFailure: false` on **every step that precedes the cleanup steps**, not only on the cleanup steps | The scenario never stops early, so steps after a failure run against a broken precondition and usually fail too. Read `StepResults` to find the first failure |
| Clean up outside the scenario | Keep fail-fast and run the cleanup afterwards — a `uaip_execute` call, or a second cleanup-only scenario, issued once the first scenario returns | Extra round trips, but the cleanup is driven by the client, so it also covers the cases below |
| Leave nothing to clean | Order the scenario so the failure-prone steps come before anything that leaves a trace | Not always possible |

### What no in-scenario pattern can cover

- **Submit-time rejects** (opt-in missing, malformed payload, `TooManyRequests`) — no step runs at all.
- **The scenario wall-clock watchdog** — when the whole-scenario budget expires, the route responds immediately with a result that carries **no `StepResults`**, while the runner keeps going in the background. The response cannot tell you whether the cleanup step ran, and a new submission is refused until the runner finishes.
- **An editor crash or hang mid-scenario** — nothing after it runs.

Whichever approach you take, confirm the traces are gone (PIE stopped, temp assets deleted) with a state dump after the scenario returns instead of inferring it from `StepResults`.

---

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| `PolicyViolation: Scenario execution is not enabled` | `enable_scenario` not set | Add `"enable_scenario": true` to `config.json` |
| Steps 2+ missing from `StepResults` | Step 1 failed with default `AbortOnFailure: true` | Set `"AbortOnFailure": false` on **the failing step**, not on the steps you want to keep running |
| A cleanup step marked `AbortOnFailure: false` never ran | An earlier step failed with the default `AbortOnFailure: true`, so the scenario finalized before reaching it | See [Failure handling and cleanup](#failure-handling-and-cleanup) — mark every preceding step `false`, or clean up outside the scenario |
| Template left as literal `"${...}"` | Single-pass resolver — `Variables` are not re-expanded | Pass the value directly via `Variables` or split into two steps |
| Step fails with `InvalidParams` and a template-related message | Malformed `${...}` reference (wrong notation, bad escape, pointer miss, oversized value, object/array in a mixed string) | Re-read [JSON Pointer notation](#json-pointer-notation) above; this is not retried by `RetryCount` |
| `TooManyRequests` | Another scenario is running | Wait for it to finish |

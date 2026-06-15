**[日本語](../ja/safety.md)** | [Back to README](../../README.md)

# Safety & Capabilities

UAIP applies per-command authorization in three layers. Understanding the layers helps you diagnose errors quickly.

---

## Authorization layers

| Layer | Mechanism | Error on failure |
|---|---|---|
| 1 | Session's `FCapabilitySet` — per-session × per-command | `CapabilityNotAvailable` |
| 2 | `FSafetyPolicy` bool switches / DeniedCapabilities — process-wide | `PolicyViolation` |
| 3 | Route-specific opt-in (e.g. scenario route) — process-wide | `PolicyViolation` |

---

## Capabilities

Every command declares `RequiredCapabilities`. The command runs only when the session owns every required capability.

- **DefaultAllow** — granted automatically to new sessions
- **DefaultDenied** — not granted by default; must be explicitly enabled in `Config/DefaultUAIP.ini`

```
# Discover what a command requires
uaip_describe_command(CommandName="UAIP.Editor.Blueprint.CompileBlueprint")
→ RequiredCapabilities: ["BlueprintEdit"]

# Check what the current session has
uaip_query_capabilities()
→ Capabilities: ["...", ...]
```

When a capability is missing:

```json
{ "ErrorCode": "CapabilityNotAvailable",
  "ErrorMessage": "Required capability is not available: BlueprintEdit" }
```

Lift DefaultDenied capabilities by adding them to `Config/DefaultUAIP.ini` (see below).

---

## SafetyPolicy configuration

Edit `Config/DefaultUAIP.ini` in your project:

```ini
[UAIP.SafetyPolicy]
ReadOnly=False
DisableSave=False
AllowLogDump=False
AllowContextMenuMutation=False
AllowKeyboardInput=False
AllowKeyboardModifierInput=False
AllowPasswordFieldWrite=False
AllowInputModeBypass=False
DisablePIEStart=False

; Lift DefaultDenied capabilities (one entry per line):
; +AllowedCapabilities=BlueprintEdit
; +AllowedCapabilities=SkeletonAssetEdit

; Block specific commands:
; +DeniedCommands=UAIP.Editor.Level.PlaceActorInLevel
```

### All settings reference

| Key | Default | Effect |
|---|---|---|
| `ReadOnly` | `False` | Reject every mutating command |
| `DisableSave` | `False` | Reject disk-writing commands |
| `AllowLogDump` | `False` | Allow `DumpOutputLog` / `DumpMessageLog` |
| `AllowContextMenuMutation` | `False` | Allow `InvokeContextMenuAction` |
| `AllowKeyboardInput` | `False` | Allow `PressKey` |
| `AllowKeyboardModifierInput` | `False` | Allow Ctrl/Alt/Shift inside `PressKey` |
| `AllowPasswordFieldWrite` | `False` | Allow `FillForm` to write into password fields |
| `AllowInputModeBypass` | `False` | Allow `BypassInputMode=true` in Inject commands |
| `DisablePIEStart` | `False` | Reject PIE startup |
| `AllowedCapabilities` | empty | DefaultDenied capabilities to grant (one per line) |
| `DeniedCapabilities` | empty | Remove DefaultAllow capabilities from sessions |
| `DeniedCommands` | empty | Block specific commands by fully-qualified name |
| `AllowCapabilityReload` | `False` | Enable `UAIP.Core.ReloadCapabilities` command |

---

## Lifting DefaultDenied capabilities

Add `+AllowedCapabilities=<name>` entries to `[UAIP.SafetyPolicy]`:

```ini
[UAIP.SafetyPolicy]
+AllowedCapabilities=BlueprintEdit
+AllowedCapabilities=SkeletonAssetEdit
```

After editing the ini, either restart the editor or (if `AllowCapabilityReload=True` is set) call:

```
uaip_execute(CommandName="UAIP.Core.ReloadCapabilities")
```

---

## Diagnosing errors

| ErrorCode | Diagnosis | Action |
|---|---|---|
| `CapabilityNotAvailable` | Session lacks the capability | Read the name from `ErrorMessage`; add it to `AllowedCapabilities` in the ini |
| `PolicyViolation: ... denied by SafetyPolicy` | SafetyPolicy ini flag | Set the corresponding flag to `True` in `[UAIP.SafetyPolicy]` and restart |
| `PolicyViolation: Scenario execution is not enabled` | Scenario route opt-in missing | Add `"enable_scenario": true` to `config.json` |
| `PolicyViolation: Command is denied` | Command is in `DeniedCommands` | Remove it from `DeniedCommands` in the ini |

---

## Common DefaultDenied capabilities

| Capability | Required for |
|---|---|
| `BlueprintEdit` | Blueprint graph / variable / function editing |
| `SkeletonAssetEdit` | Skeleton and SkeletalMesh editing |
| `EditorLifecycle` | `ShutdownEditor`, `RestartEditor` |
| `LogDump` | `DumpOutputLog`, `DumpMessageLog` |

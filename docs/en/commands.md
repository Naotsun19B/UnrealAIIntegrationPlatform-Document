**[日本語](../ja/commands.md)** | [Back to README](../../README.md)

# Commands Reference

UAIP exposes 1314 **UAIP commands** (provided directly by the plugin itself) and 421 **Toolset bridge commands** (delegating to the UE 5.8 official Toolset framework), for a combined total of 1735 commands organized by domain. These totals count every command the plugin defines for the UE 5.8 editor on Win64, including commands listed with `Available: false` because a plugin they need is disabled. Each command name is fully-qualified — e.g. `UAIP.Editor.Observation.CaptureActiveWindowImage`. This page omits the provider prefix in the tables; the section header tells you what to prepend.

## How to use this reference

- Get the full parameter schema for a command with `{"Command": "UAIP.Core.DescribeCommand", "Params": {"Name": "<command name>"}}` over HTTP / WebSocket / CLI, or `uaip_describe_command(CommandName="<command name>")` over MCP (the argument is `Name` in the first form and `CommandName` in the second)
- Use `uaip_list_commands(ProviderPrefix="UAIP.Editor")` to filter by domain at runtime
- For the required Capability per command, see [Safety & Capabilities](safety.md)
- These commands delete, move or rename files on disk, so they are refused with `PolicyViolation` — before anything else is checked, PIE included — when the safety policy sets `DisableSave` ("Disk write operations are disabled by the current safety policy."): `DeleteAsset`, `DeleteFolder`, `ForceDeleteFolder`, `RenameAsset`, `MoveAsset`, `MoveFolder`, `FixAssetRedirectors`, `FixUpRedirectorsInFolder`, `DeleteInputAction`, `DeleteMappingContext`, `DeleteDataLayerAsset`, `DeleteHLODs` and `DeleteGameFeaturePlugin`. Commands that already refused under `DisableSave` are unchanged. See [Safety & Capabilities](safety.md#disablesave-and-the-commands-that-delete-move-or-rename)

## Symbols

| Symbol | Meaning |
|---|---|
| 🆓 | Available in the demo binary (also in Pro) |
| (no mark) | Pro-only command |
| 🧩 | Requires an optional UE plugin (the command is not registered if the plugin is disabled). On an editor build, if the plugin exists in your engine but is merely disabled, enabling it and restarting the editor is enough — no `.uproject` edit or rebuild required. If the plugin isn't part of this engine version at all, no toggle helps; see `UnavailableDetail: OptionalPluginDisabled` under [UnavailableDetail](#unavailabledetail--the-eight-reasons-behind-a-handlerunavailable-refusal). Either way, `UAIP.Core.ListIntegrations` reports the exact state |
| ⚠️ | Experimental — the behaviour or the contract may change, or a known limitation prevents it from working as documented |

## UAIP commands vs Toolset bridge commands

UAIP exposes two categories of commands:

- **UAIP commands** (`UAIP.*` prefix) — first-party commands provided by the plugin itself. They work regardless of UE version or Toolset plugin availability.
- **Toolset bridge commands** (`Toolset.*` prefix; UE 5.8+ with the relevant Toolset plugin installed) — a delegation layer over the official UE 5.8 Toolset framework. Most mirror an existing UAIP command, while a few surface functionality only available through Toolset.

The domain summary below lists counts only. To enumerate the actual Toolset bridge command names at runtime, use `uaip_list_commands(ProviderPrefix="Toolset")`.

When a Toolset bridge command cannot run because the Toolset integration it goes through is not ready, the error message starts by naming that integration and its state, then says what to do about it. For example, in the free demo build, which does not include the Toolset integration: `This command runs through the Toolset integration 'UAIPCoreToolsetRegistry', which is not loaded (state: NotInThisEdition). The integration is not included in the free demo edition of UAIP. Its commands are available in the Pro edition on Fab.` While the integration is still loading (state `Pending` or `Loading`) the first sentence says `has not finished loading yet` instead of `is not loaded`. `UAIP.Core.ListIntegrations` reports the same state.

### Toolset bridge commands are gaining declared, validated parameter schemas

Historically, most Toolset bridge commands declared **no parameters at all** — `uaip_describe_command` returned an empty `Properties` object regardless of what the command actually accepted, and any JSON you sent was passed straight through to the underlying Toolset call unchecked. A malformed call still reached the engine and typically failed there with a generic `ExecutionFailed`, giving no indication of which key was wrong.

This is being migrated one command at a time to a declared, strictly-validated schema (`AdditionalProperties: false`, real `Required` flags, real types). **As of this update, 161 Toolset bridge commands have completed the migration** — concentrated in `Toolset.Editor.Niagara.*`, `Toolset.Editor.PCG.*`, `Toolset.Editor.Sequencer.*` (plus its `SequencerAnimMixer` / `AnimationAssistant` sibling providers), `Toolset.Editor.Physics.*`, `Toolset.Editor.UMG.*` and `Toolset.MVVM.*`, with a handful of individual commands elsewhere. The migration is ongoing — whether a given command has been migrated is visible directly from its schema: a non-empty `Properties` with `AdditionalProperties: false` means it validates strictly now; an empty `Properties` with `AdditionalProperties: true` means it is not migrated yet and still passes parameters through unchecked. Always check the live schema with `uaip_describe_command` rather than assuming from this reference.

**This is a breaking change for calls that previously "worked by accident"**: a call that sent an extra or misspelled key used to be silently accepted (and simply ignored, or forwarded and rejected deep inside the engine) — on a migrated command it is now refused up front with `InvalidParams`, naming the offending key.

Five `Toolset.Editor.Niagara.*` commands (`DuplicateEmitter`, `GetScriptAssets`, `MoveModule`, `SetEmitterEnabled`, `SetEmitterName`) still declare no parameters as of this update, and that is no longer an open question: none of the five has a matching function in any Niagara toolset this plugin supports, so instead of being migrated to a real schema, all five now report `Available: false` (`UnavailableReason: "HandlerUnavailable"`, `UnavailableDetail: "DelegationTargetMissing"`) — there is nothing left for a schema to describe. See the note under [UAIP.Editor.Niagara → Toolset bridges](#uaipeditorniagara-) for what each one refuses with and which ones have a working native alternative. The same "the toolset declares no matching function" shape also applies to `Toolset.Editor.GameFeatures.ListGameFeatures` and `Toolset.Editor.Niagara.GetNiagaraParameterCollections`, which were already declaring a proper empty schema and so are not counted among these five — see [UAIP.Editor.GameFeatures → Toolset bridges](#uaipeditorgamefeatures-). **This update establishes the full set of commands in this state.** Of the 421 bridge commands, the 419 built on the shared bridge handler have had their delegation pair — (toolset name, tool name) — checked statically against what the engine actually registers: **404 reach a target and 15 do not**. The other two (`CompileLiveCoding` and `DrawPCGSpline`) are not built on that handler and are outside this check. All 15 report `Available: false` with `UnavailableDetail: "DelegationTargetMissing"` (7 in Niagara, 4 in GameFeatures, 2 in SlateInspector, 2 in UMG). The same pass also found **16 commands whose delegation target was misspelled, which now reach it** (7 in Dataflow, 8 in SlateInspector, 1 in Niagara) — until now this reference described them as working while they failed at run time. `uaip_describe_command` remains the authoritative answer for any specific command.

---

## UnavailableDetail — the eight reasons behind a HandlerUnavailable refusal

Several notes throughout this page cite `UnavailableDetail` next to `UnavailableReason: "HandlerUnavailable"`. `HandlerUnavailable` on its own only says a command's `IsAvailable()` reported `false` — it does not say why. `UnavailableDetail` narrows that down to one of eight values.

It is visible from `uaip_describe_command` on any command, whether or not it is currently available. It is **not** part of `uaip_list_commands`'s `HiddenReasons` object, which stays at the five fixed `UnavailableReason` keys (`DeniedCommand` / `MissingCapability` / `RoleRestricted` / `ReadOnlyPolicy` / `HandlerUnavailable`) regardless — call `uaip_describe_command` by name to see the detail behind a specific `HandlerUnavailable` entry, or pass `IncludeUnavailable: true` to `uaip_list_commands`, whose hidden rows now carry the same per-command `UnavailableDetail` string (never `UnavailableDetailMessage`, which stays a `describe_command`-only field so list responses stay bounded). When a handler reports one of the seven non-`Unspecified` values below, a matching `UnavailableDetailMessage` string is usually present alongside it — the handler's own free-text elaboration; quote it back to the user rather than re-deriving your own wording.

| `UnavailableDetail` | Meaning | What resolves it |
|---|---|---|
| `Unspecified` | No detail beyond `HandlerUnavailable` itself — the default for a handler that predates this field, and also what every handler reports once `Available` is `true` again | — |
| `EngineVersion` | The command needs an engine version other than the one currently running (an API only introduced in, or only surviving up to, a specific release) | Raising or lowering the engine version |
| `BuildConfiguration` | The command needs a build configuration this process was not built with (e.g. Developer Tools, an Editor target) | Rebuilding with the required configuration |
| `ExecutionEnvironment` | The command needs infrastructure this execution environment does not provide (e.g. a render hardware interface, an interactive session, a modular-feature client an optional runtime plugin registers) | Running under a different execution environment |
| `OptionalPluginDisabled` | The command depends on an optional plugin this binary has no compiled-in support for at all — the plugin was absent from the engine this UAIP build was compiled against | **Enabling the plugin and restarting fixes nothing here.** On an editor build, the fix is a UAIP build for an engine version that includes the plugin (for a source build: add the plugin to that engine and rebuild). On a packaged game, enable the plugin in the `.uproject` and package again. A plugin that is merely *disabled*, not absent, never produces this value — that shows up as `CommandNotFound` (with a remedy) or, for a Toolset bridge, `ExecutionEnvironment` instead — see [`UAIP.Core.ListIntegrations`](#uaipcore) |
| `EngineApiNotExported` | The command depends on an engine-side API that is never exported to a plugin, on any supported engine version | Nothing an engine-version change or a plugin toggle fixes — look for a different code path (e.g. a Toolset bridge command reaching the same effect through editor scripting) |
| `DelegationTargetMissing` | The command forwards to a function on an external surface (a Toolset bridge target) that no supported engine version actually declares, so the call could never reach an implementation | Nothing here either — the plugin owning that surface may already be enabled; use a native command covering the same operation, where one exists |
| `SafetyPolicyDisabled` | Nothing about the environment or the build is missing: the command is gated behind a deny-by-default SafetyPolicy flag that is off in this process | Setting that flag in `Config/DefaultUAIP.ini` and restarting — the `ErrorMessage` names the flag. Where `AllowCapabilityReload=True`, `UAIP.Core.ReloadCapabilities` applies the edit without a restart |

`EngineVersion` / `BuildConfiguration` / `ExecutionEnvironment` / `OptionalPluginDisabled` all name something a human can change. `EngineApiNotExported` and `DelegationTargetMissing` do not — no ini flag, capability grant, engine version, or plugin toggle changes either of them; the only way forward is a different code path. `SafetyPolicyDisabled` is the odd one out: it is the one value that *is* an ini question, and the only one an `AllowedCapabilities` / `DeniedCapabilities`-style edit to `Config/DefaultUAIP.ini` resolves.

Calling a command by name while it is `Available: false` fails, and **which error code comes back depends on the detail**. The six values that name something about the environment or the build — `EngineVersion` / `BuildConfiguration` / `ExecutionEnvironment` / `OptionalPluginDisabled` / `EngineApiNotExported` / `DelegationTargetMissing` — fail with `AbilityUnavailable` (HTTP 501, "this cannot be done here"). `SafetyPolicyDisabled` and `Unspecified` fail with `PolicyViolation` (HTTP 403), because those are the two cases where flipping a setting really is the answer. `ErrorMessage` restates the same information either way: `"Command '<name>' is not available (<UnavailableDetail>): <UnavailableDetailMessage>"` — or, when `UnavailableDetail` is `Unspecified`, the older generic sentence `"... is not available in the current SafetyPolicy configuration."`.

### Commands that newly report a detail

- **`UAIP.Runtime.LiveLink.*` — all 14 commands in the domain** report `UnavailableDetail: "ExecutionEnvironment"` when no `ILiveLinkClient` is registered as a modular feature in this process (the `LiveLink` plugin not enabled, or not yet loaded). Nothing in the module is compiled out — see [UAIP.Runtime.LiveLink](#uaipruntimelivelink).
- **`UAIP.Editor.AnimSequence.SelectAnimNotify`** is UE 5.8+ only; it reports `UnavailableDetail: "EngineVersion"` on UE 5.7, because the notify widget type and its node-object interface are private to the Persona module before 5.8. See [UAIP.Editor.AnimSequence](#uaipeditoranimsequence).
- **`UAIP.Core.ReloadCapabilities`** now reports `UnavailableDetail: "SafetyPolicyDisabled"`, naming the ini key to set, while `AllowCapabilityReload` is left at its default `False` — instead of only the older generic sentence. This is the one detail value that keeps `PolicyViolation` as its error code rather than `AbilityUnavailable`, because setting the flag really does resolve it. See [UAIP.Core](#uaipcore).

---

## Domain summary

| Domain | Provider prefix | UAIP commands | Toolset bridge | Demo |
|---|---|---:|---:|---:|
| Core | `UAIP.Core` | 12 | — | ✅ |
| Core Artifacts | `UAIP.Core.Artifacts` | 1 | — | ✅ |
| Editor Workspace | `UAIP.Editor.Workspace` | 24 | 1 | partial (19/24) |
| Editor Engine Log | `UAIP.Editor.Engine.Log` | 1 | 4 | ✅ |
| Editor Engine Plugin | `UAIP.Editor.Engine.Plugin` | 9 | 15 | partial (5/9) |
| Editor Engine CVar 🧩 | `Toolset.Editor.Toolset.EngineManagement` | — | 1 | — |
| Editor Engine ConfigSettings | `UAIP.Editor.Engine.ConfigSettings` | 8 | 8 | partial (5/8) |
| Editor Engine Toolset 🧩 | `UAIP.Editor.Engine.Toolset` | 1 | — | — |
| Editor Observation | `UAIP.Editor.Observation` | 15 | — | ✅ |
| Editor Execution | `UAIP.Editor.Execution` | 9 | — | — |
| Editor UI Automation | `UAIP.Editor.UIAutomation` | 16 | 10 | ✅ |
| Editor Assets | `UAIP.Editor.Assets` | 51 | 6 | partial (29/51) |
| Editor SemanticSearch 🧩 | `UAIP.Editor.SemanticSearch` | 5 | 2 | — |
| Editor Level | `UAIP.Editor.Level` | 22 | 8 | partial (9/22) |
| Editor Property | `UAIP.Editor.Property` | 12 | — | partial (6/12) |
| Editor Blueprint | `UAIP.Editor.Blueprint` | 20 | — | — |
| Editor UMG | `UAIP.Editor.UMG` | 22 | 13 | — |
| Editor Material | `UAIP.Editor.Material` | 11 | — | — |
| Editor GameplayTags | `UAIP.Editor.GameplayTags` | 7 | 6 | — |
| Editor GameFeatures 🧩 | `UAIP.Editor.GameFeatures` | 5 | 4 | — |
| Editor Niagara 🧩 | `UAIP.Editor.Niagara` | 52 | 45 | — |
| Editor Physics | `UAIP.Editor.Physics` | 31 | 17 | — |
| Editor Dataflow 🧩 | `UAIP.Editor.Dataflow` | 9 | 7 | — |
| Editor ChaosClothAsset 🧩 | `UAIP.Editor.ChaosClothAsset` | 10 | 6 | — |
| Editor Skeleton | `UAIP.Editor.Skeleton` | 11 | — | — |
| Editor MetaHuman 🧩 | `UAIP.Editor.MetaHuman` | 56 | 9 | — |
| Editor DataTable | `UAIP.Editor.DataTable` | 8 | — | — |
| Editor AnimBlueprint | `UAIP.Editor.AnimBlueprint` | 19 | — | — |
| Editor AnimBlueprint UAF 🧩 | `UAIP.Editor.AnimBlueprint.UAF` | 1 | — | — |
| Editor UAF 🧩 | `UAIP.Editor.UAF` | 19 | — | — |
| Editor UAF AnimGraph 🧩 | `UAIP.Editor.UAF.AnimGraph` | 1 | — | — |
| Editor SoundCue | `UAIP.Editor.SoundCue` | 8 | — | — |
| Editor SoundSettings | `UAIP.Editor.SoundSettings` | 13 | — | — |
| Editor MVVM 🧩 | `UAIP.Editor.MVVM` | 26 | 9 | — |
| Editor BehaviorTree | `UAIP.Editor.BehaviorTree` | 18 | 7 | — |
| Editor MetaSound 🧩 | `UAIP.Editor.MetaSound` | 10 | — | — |
| Editor EQS 🧩 | `UAIP.Editor.EQS` | 9 | — | — |
| Editor Sequencer | `UAIP.Editor.Sequencer` | 129 | 61 | — |
| Editor StateTree | `UAIP.Editor.StateTree` | 39 | 8 | — |
| Editor Curve | `UAIP.Editor.Curve` | 6 | — | — |
| Editor PCG 🧩 | `UAIP.Editor.PCG` | 34 | 31 | — |
| Editor WorldConditions 🧩 | `UAIP.Editor.WorldConditions` | 13 | 2 | — |
| Editor Conversation 🧩 | `UAIP.Editor.Conversation` | 7 | 5 | — |
| Editor ControlRig | `UAIP.Editor.ControlRig` | 68 | 107 | — |
| Editor ControlRig Dynamics 🧩 | `UAIP.Editor.ControlRig.Dynamics` | 17 | — | — |
| Editor ControlRig Physics 🧩 | `UAIP.Editor.ControlRig.Physics` | 8 | — | — |
| Editor EnhancedInput | `UAIP.Editor.EnhancedInput` | 15 | — | — |
| Editor GAS 🧩 | `UAIP.Editor.GAS` | 8 | 14 | — |
| Editor Python Extension 🧩 | `UAIP.Editor.Python` | 1 | — | — |
| Editor Sandbox 🧩 | `UAIP.Editor.Sandbox` | 6 | — | — |
| Editor WorldPartition | `UAIP.Editor.WorldPartition` | 34 | — | — |
| Editor Foliage | `UAIP.Editor.Foliage` | 11 | — | — |
| Editor DataRegistry 🧩 | `UAIP.Editor.DataRegistry` | 9 | 7 | — |
| Editor MotionMatching 🧩 | `UAIP.Editor.MotionMatching` | 23 | — | — |
| Editor Chooser 🧩 | `UAIP.Editor.Chooser` | 20 | — | — |
| Editor AnimSequence | `UAIP.Editor.AnimSequence` | 13 | — | — |
| Editor ChaosDestruction | `UAIP.Editor.ChaosDestruction` | 29 | — | — |
| Editor Subsonic 🧩 | `UAIP.Editor.Subsonic` | 22 | — | — |
| Editor GroomAsset 🧩 | `UAIP.Editor.GroomAsset` | 35 | — | — |
| Editor Validation 🧩 | `UAIP.Editor.Validation` | 7 | — | — |
| Editor LiveLink 🧩 | `UAIP.Editor.LiveLink` | 11 | — | — |
| Editor Mass 🧩 | `UAIP.Editor.Mass` | 7 | — | — |
| Runtime Engine Log | `UAIP.Runtime.Engine.Log` | 3 | — | partial (2/3) |
| Runtime Engine Plugin | `UAIP.Runtime.Engine.Plugin` | 5 | — | ✅ |
| Runtime Engine CVar | `UAIP.Runtime.Engine.CVar` | 4 | — | partial (2/4) |
| Runtime Engine Config | `UAIP.Runtime.Engine.Config` | 2 | — | partial (1/2) |
| Runtime PIE | `UAIP.Runtime.PIE` | 6 | 3 | ✅ |
| Runtime World | `UAIP.Runtime.World` | 14 | 1 | — |
| Runtime Observation | `UAIP.Runtime.Observation` | 14 | — | ✅ |
| Runtime Execution | `UAIP.Runtime.Execution` | 3 | — | — |
| Runtime Assertion | `UAIP.Runtime.Assertion` | 4 | — | ✅ |
| Runtime Input | `UAIP.Runtime.Input` | 15 | — | partial (2/15) |
| Runtime GAS 🧩 | `UAIP.Runtime.GAS` | 17 | — | — |
| Runtime Niagara 🧩 | `UAIP.Runtime.Niagara` | 4 | 4 | — |
| Runtime LiveLink | `UAIP.Runtime.LiveLink` | 14 | — | — |
| Runtime Insights Trace | `UAIP.Runtime.Insights.Trace` | 11 | — | partial (3/11) |
| Runtime Insights Analysis | `UAIP.Runtime.Insights.Analysis` | 3 | — | — |
| Runtime SaveGame | `UAIP.Runtime.SaveGame` | 10 | — | — |
| Runtime AI | `UAIP.Runtime.AI` | 14 | — | partial (13/14) |
| Runtime StateTree 🧩 | `UAIP.Runtime.StateTree` | 7 | — | — |
| Runtime CommonUI 🧩 | `UAIP.Runtime.CommonUI` | 4 | — | — |
| Runtime Chaos Destruction | `UAIP.Runtime.ChaosDestruction` | 8 | — | partial (7/8) |
| Runtime Navigation | `UAIP.Runtime.Navigation` | 8 | — | partial (7/8) |
| Runtime Animation | `UAIP.Runtime.Animation` | 7 | — | partial (6/7) |
| Runtime Network | `UAIP.Runtime.Network` | 7 | — | partial (3/7) |
| Runtime Mass | `UAIP.Runtime.Mass` | 6 | — | — |

---

## Writing references, structs and containers

The property-writing commands listed below take the value in either of two forms, and can operate on a single container element instead of replacing the whole value. Which capability a write needs is decided from the property's type while the write runs, so it never appears in the command's declared `RequiredCapabilities` — read the property first (see [Finding out what a write needs](#finding-out-what-a-write-needs)) or take the missing name out of the refusal.

### Capabilities

| Capability | Required when |
|---|---|
| `PropertyReferenceEdit` | the value being written is — or contains, at any depth — an object / class / soft / weak / lazy / interface reference, a delegate, or a field path. Clearing a reference needs it too: attaching and detaching a dependency are the same kind of change |
| `PropertyStructuredEdit` | the property is a struct outside the built-in value catalogue, an array, a set, a map, an optional, or a fixed-size array |

Both are DefaultDenied — enable them in `Config/DefaultUAIP.ini`, see [Safety & Capabilities](safety.md). Writing a struct that contains a reference needs both, so the structured capability alone is not a way around the reference gate.

A module that already governs reference writes through a capability of its own keeps using that name for the reference half: `SetAnimNotifyProperty` reads `AnimNotifyReferenceEdit`, `SetDataflowNodeProperty` reads `DataflowReferenceEdit`, the Subsonic commands read `SubsonicEventEdit`, `SetSlotProperties` reads `WidgetSlotReferenceEdit`, the four Enhanced Input trigger / modifier setters read `EnhancedInputReferenceEdit`, and `SetStateTreeParameter` reads `StateTreeParameterReferenceEdit`. The struct / container half is always `PropertyStructuredEdit`. The same pattern holds outside this list: `AddSetParameterEntry` and `AddSetParametersModule` read `NiagaraReferenceEdit` when the `DefaultValue` they are given belongs to a data interface or object parameter. A refusal names the capability that command's own write path actually reads, so the name you are handed is always the one worth asking an operator for.

### Parameters

| Parameter | Type | Meaning |
|---|---|---|
| `ValueJson` | any JSON value | The value as a JSON document instead of engine text. Carries the whole new value for a `Replace`, the element for an array `Insert`, and the value half of the pair for a map `Insert` |
| `Operation` | string | `Replace` (default) / `Insert` / `Remove` / `Clear`. Omitting it leaves the command behaving exactly as it did before element operations existed |
| `ElementIndex` | integer | The position an array element is inserted at or removed from. An `Insert` may name the position one past the last element, to append. Must be a whole number that fits in a 32-bit signed integer — `1.5` is refused rather than rounded |
| `ElementKeyJson` | any JSON value | The element a set operation names, or the key half of the pair a map operation names |

`ValueJson` is mutually exclusive with the command's text value parameter — `Value` on every command below except `SetSectionProperty`, which spells it `PropertyValue`. Supplying both is `InvalidParams`.

| Operation | Array | Set | Map |
|---|---|---|---|
| `Replace` | replaces the whole container | replaces the whole container | replaces the whole container |
| `Insert` | inserts `ValueJson` at `ElementIndex` | adds `ElementKeyJson` if it is not already present | stores `ValueJson` under `ElementKeyJson`, overwriting any value that key already had |
| `Remove` | removes the element at `ElementIndex` | removes `ElementKeyJson` | removes the entry keyed by `ElementKeyJson` |
| `Clear` | empties the container | empties the container | empties the container |

Which parameters each operation accepts:

- `Replace` takes exactly one of the text value or `ValueJson`, and neither `ElementIndex` nor `ElementKeyJson`
- `Insert` and `Remove` take exactly one of `ElementIndex` or `ElementKeyJson`, and never the text value
- `Clear` takes none of `ElementIndex` / `ElementKeyJson` / `ValueJson`

Every violation is refused with `InvalidParams` **before** the property path is resolved, so the answer never depends on which property was named.

A JSON `null` in `ValueJson` is a value, not an omission — it is how a reference is cleared.

### `Value` is no longer a required parameter

On every command in the table below, the text value parameter — `Value`, or `PropertyValue` on `SetSectionProperty` — moved from `Required` to `Optional` in the schema. A schema cannot say "exactly one of these two", and leaving the parameter required would have made `Remove`, `Clear` and every `ValueJson` write unreachable. The Subsonic commands' `Value` changed the same way.

**The set of requests that get refused is unchanged, but the refusal moved and its wording changed.** A `Replace` supplying no value at all used to be rejected by schema validation with a message naming `Value` as a required parameter. It is now rejected by the command itself, with:

- `Invalid parameters: operation 'Replace' requires either 'Value' or 'ValueJson'.` on the fifteen commands that accept both forms
- `Invalid parameters: operation 'Replace' requires 'Value'.` on the three Subsonic commands, which have no `ValueJson`

`ErrorCode` is `InvalidParams` either way. If your tooling matches on the old message text, update the match.

Other things worth knowing about element operations:

- They are idempotent where the container makes them so. Adding an element a set already holds, or removing one it never held, succeeds. `Success` on its own therefore does not tell you whether anything moved — the artifact carries a `Changed` field next to `Operation` for exactly that, and it is written for a `Replace` too.
- A container already holding more than 4096 elements is refused whatever the operation, `Remove` and `Clear` included. The whole container is copied and validated before anything is committed, so the ceiling is about the cost of reading it rather than about what the operation would do to it.
- A key whose type is a reference cannot be rewritten in place — remove the entry and insert it again.
- Replacing a map wholesale with a document that repeats a key keeps the last occurrence, matching what `Insert` does.
- An optional value distinguishes three states: absent, present but empty, and present with a value. It takes `Replace` only — the three states already express what `Insert` / `Remove` / `Clear` would say.
- A fixed-size array (`int32 Values[3]` and the like) also takes `Replace` only, and the JSON array supplied must have exactly as many elements as the property declares.
- **Replacing one array element in place is expressed in `PropertyPath`, not in `Operation`.** Write `Arr[3]` with the default `Replace`; `Insert` means "put a new element in", never "overwrite the one at this position".

### Commands that accept these parameters

| Command | Domain | Text value parameter | `ValueJson` | Capability for the reference half |
|---|---|---|---|---|
| `SetActorProperty` | `UAIP.Editor.Property` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetAssetProperty` | `UAIP.Editor.Property` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetBlueprintDefault` | `UAIP.Editor.Property` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetWorldSetting` | `UAIP.Editor.Property` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetProjectSetting` | `UAIP.Editor.Property` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetDataTableRow` | `UAIP.Editor.Property` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetBlueprintComponentProperty` | `UAIP.Editor.Blueprint` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetActorComponentProperty` | `UAIP.Editor.Level` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetSectionProperty` | `UAIP.Editor.Sequencer` | `PropertyValue` | ✅ | `PropertyReferenceEdit` |
| `SetSoundClassSettings` | `UAIP.Editor.SoundSettings` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetSoundAttenuationSettings` | `UAIP.Editor.SoundSettings` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetSoundMixSettings` | `UAIP.Editor.SoundSettings` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetSoundCueNodeProperty` | `UAIP.Editor.SoundCue` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetAnimGraphNodeProperty` | `UAIP.Editor.AnimBlueprint` | `Value` | ✅ | `AnimBlueprintReferenceEdit` |
| `SetDataflowNodeProperty` 🧩 | `UAIP.Editor.Dataflow` | `Value` | ✅ | `DataflowReferenceEdit` |
| `SetAnimNotifyProperty` | `UAIP.Editor.AnimSequence` | `Value` | ✅ | `AnimNotifyReferenceEdit` |
| `SetPoseSearchSchemaChannelProperty` 🧩 | `UAIP.Editor.MotionMatching` | `Value` | ✅ | — (references are refused outright) |
| `SetSubsonicEventActionProperty` 🧩 | `UAIP.Editor.Subsonic` | `Value` (already a JSON value) | — | `SubsonicEventEdit` |
| `SetSubsonicActionModifierProperty` 🧩 | `UAIP.Editor.Subsonic` | `Value` (already a JSON value) | — | `SubsonicEventEdit` |
| `SetSubsonicParameterValue` 🧩 | `UAIP.Editor.Subsonic` | `Value` (already a JSON value) | — | `SubsonicEventEdit` |

The three Subsonic commands **do not** take `ValueJson`. Their existing `Value` parameter is already a JSON value rather than engine text, so it carries the structured value directly; a second parameter with the same meaning would only leave callers guessing which one to use. They take `Operation` / `ElementIndex` / `ElementKeyJson` like the rest. Their refusals name `Value` alone and never mention a parameter they do not declare: a `Replace` requires `Value`, and a `Clear` refuses it.

`SetPCGNodeProperty`, `SetCustomCppPCGNodeProperty`, `SetCustomBlueprintPCGNodeProperty` and `SetConversationNodeProperty` already took their value as a JSON document and do not take element operations. What changed for them is that references, structs and containers are no longer refused permanently — those writes are now gated by the two capabilities above, like everywhere else.

### Finding out what a write needs

The matching `Get*` command attaches a `WriteRequirements` object to the value it read:

| Field | Meaning |
|---|---|
| `RequiredCapabilities` | the capability names that command's own write path looks up, so granting them actually unblocks the write |
| `HeldCapabilities` / `MissingCapabilities` | the same names split by whether the session that issued the read holds them |
| `IsWritable` / `RefusalReason` | whether the property's type and flags permit a write at all, whatever the session holds |
| `WriteInputForm` | `TextOrJson`, `JsonOnly` or `None` — which input field the value has to be supplied in. `None` accompanies `IsWritable: false`: no input form is accepted and no capability changes that |

A few commands decide writability on their own terms and do not attach this report. For those, attempt the write: the refusal names the capability that is missing. The guidance is what is absent, not the way forward.

Ten further read commands now carry the report, in one of two shapes depending on how each already returns its values:

| Command | Where the report sits |
|---|---|
| `GetSlotProperties` (`UAIP.Editor.UMG`) | a `PropertyWriteRequirements` map beside `Properties`, keyed by property name |
| `GetInputActionInfo` / `GetMappingContextInfo` (`UAIP.Editor.EnhancedInput`) | a `PropertyWriteRequirements` map inside each trigger / modifier entry, beside its `Params` |
| `GetStateTreeParameters` (`UAIP.Editor.StateTree`) | a `WriteRequirements` object nested in each parameter entry |
| `GetWorldConditionInfo` (`UAIP.Editor.WorldConditions`) | a `WriteRequirements` object nested in each condition property entry |
| `GetAnimNotifyClassSchema` (`UAIP.Editor.AnimSequence`) | a `WriteRequirements` object nested in each property entry |
| `GetAnimNotifyProperty` (`UAIP.Editor.AnimSequence`) | a `WriteRequirements` object nested in each property entry — and directly in `Data`, beside `PropertyName` and `Value`, when a single property was requested |
| `GetPoseSearchChannelClassSchema` (`UAIP.Editor.MotionMatching`) | a `WriteRequirements` object nested in each property entry |
| `GetBehaviorTreeNodeProperties` (`UAIP.Editor.BehaviorTree`) | a `WriteRequirements` object nested in each property entry |
| `GetStackInputData` (`UAIP.Editor.Niagara`) | a `WriteRequirements` object nested in each stack input entry |

The value maps themselves (`Properties`, `Params`) did not change shape, so a caller that only reads values is unaffected. On the two Enhanced Input getters the report covers **every** editable property, including the references and containers the value map used to skip — those are precisely the ones a capability is needed for. `GetWorldConditionInfo` reports an empty `RequiredCapabilities` throughout: that path accepts no reference or container at all, so there is no capability to ask an operator for, and naming one would point at a permission that unlocks nothing. `GetAnimNotifyProperty` uses the same field names and the same nesting as `GetAnimNotifyClassSchema`, so the two are read the same way; the difference is that its verdict is resolved against the actual notify instance addressed by `NotifyGuid` — the object `SetAnimNotifyProperty` writes to — rather than against the class default. `GetBehaviorTreeNodeProperties` reports and accepts a `FBlackboardKeySelector` property as the bare key name in plain text rather than the struct's own fields — that property never reaches the shared write model, so its `WriteRequirements` names only `BehaviorTreeNodeReferenceEdit`, the one capability `SetBehaviorTreeNodeProperty`'s own write path actually checks for it. `GetStackInputData`'s `WriteRequirements` describes what `AddSetParameterEntry` would need to replace an input's default value; an input already holding a plain object reference still reports `ValueMode: "Unknown"` and an empty `Value`, because `AddSetParameterEntry`'s own type allow-list has no route to create that kind of entry in the first place — the gap is in what can be written, not in what this command can read.

> ⚠️ **Breaking change**: `GetAnimNotifyClassSchema` and `GetPoseSearchChannelClassSchema` used to report this per property directly on the property entry, under their own names — `bIsWritable`, `NotWritableReason`, `WriteInputForm` and `RequiredCapabilities` — with no `HeldCapabilities` / `MissingCapabilities` at all. Both now attach the identical nested `WriteRequirements` object shown above instead, so a caller still reading the old flat names finds nothing there. Read `WriteRequirements.IsWritable`, `.RefusalReason`, `.WriteInputForm` and `.RequiredCapabilities`; `.HeldCapabilities` / `.MissingCapabilities` are new information, not a renamed field. Nothing about which properties are writable, or what a write needs, changed — only where the answer is reported. With this, every UAIP read command that reports what a write would take now uses the same shape.

### Things that catch people out

- **A hard reference can only point at an asset that is already loaded.** A property write never loads an asset as a side effect, so an object path resolves only if something already has that asset open. "Does not exist" and "exists but is not loaded" come back as the same refusal, because resolving without loading cannot tell them apart — open the asset first, then write. Soft references (`TSoftObjectPtr` / `TSoftClassPtr` / `FSoftObjectPath` / `FSoftClassPath`) are exempt: those are validated against the asset registry and never need the target loaded. This rule now holds for **every** UAIP command that writes a reference, including the Subsonic ones, which used to load the target implicitly — a write that used to succeed may now need the asset opened first.
- **References and composite values cannot be written as text.** Their `WriteInputForm` is `JsonOnly`: passing an object path in `Value` is refused even with the capability granted, because the text import path would resolve and load the reference behind the capability gate. Use `ValueJson` (or, on the Subsonic commands, the JSON `Value` they already take). A small number of value types go the other way and accept only the text form; `WriteInputForm` is what tells the two apart.
- **A few commands refuse references outright, capability or not.** `SetPoseSearchSchemaChannelProperty` will not write a reference-bearing type at all: a channel's sub-channel array is how channels are created, and writing it directly would sidestep the class allowlist `AddPoseSearchSchemaChannel` enforces. Use the dedicated channel commands instead. The refusal is a `PolicyViolation` rather than something a permission fixes.
- **On user-authored PCG nodes, a session without the capabilities sees a narrowed set of types.** `GetCustomPCGNodeSchema`, `GetCustomBlueprintPCGNodeSchema` and `GetPCGNativeNodeSchema` list only the curated types for such a session, and the matching setter's refusal deliberately does not name the type it refused. The response still says that something was left out: `HiddenCount`, `HiddenCapabilities` (which permissions would reveal them) and a `HiddenReasons` object whose `MissingCapability` and `Unwritable` keys are always present and always sum to `HiddenCount`. Grant the named capabilities and the hidden entries appear, with `HiddenCount` back to 0. Property *names* were never hidden — a misspelt name still comes back as "no such property", so a typo stays distinguishable from a missing permission.
- **Intermediate path segments are checked, not just the last one.** `Struct.Inner` is refused when `Struct` itself is read-only, deprecated, or absent from the Details panel; naming an inner member no longer walks past a read-only level. The same check applies through a container index (`Array[0].Inner`), where it is the container that is inspected.
- **Values that hold an asset path are written whole.** `FSoftObjectPath`, `FSoftClassPath` and `FTopLevelAssetPath` cannot be addressed member by member — writing their internals would be a way past the reference gate.
- **The class being written into a reference can itself need a domain's own capability, on top of `PropertyReferenceEdit`.** Holding `PropertyEdit` + `PropertyReferenceEdit` used to be enough to write any already-loaded class into a hard reference or an instanced subobject property, through `SetAssetProperty` and the same-shaped commands, regardless of what that class was. Constructing an instanced subobject from a caller-named class goes through the identical check. A session with nothing beyond those two capabilities is unaffected either way — it could never reach a reference write at all. Today this is wired up for `UAIP.Editor.Material`: writing a `UMaterialExpression`-derived class into a reference or instanced-subobject property needs `MaterialCustomTypeEdit` / `MaterialCustomNodeEdit` in addition, the same as `AddMaterialNode` would ask for it — see [Capability-gated custom types](#capability-gated-custom-types). Other domains have not registered this check yet, so writing one of their own gated classes through the generic property commands is not yet caught by it.

---

## Capability-gated custom types

Several domains only let a project- or plugin-defined type through once a capability is granted for it — see the domain's own note, for example [UAIP.Editor.Material](#uaipeditormaterial), [UAIP.Editor.AnimBlueprint](#uaipeditoranimblueprint), [UAIP.Editor.ControlRig](#uaipeditorcontrolrig), [UAIP.Editor.EnhancedInput](#uaipeditorenhancedinput), [UAIP.Editor.UAF](#uaipeditoruaf-), [UAIP.Editor.BehaviorTree](#uaipeditorbehaviortree), [UAIP.Editor.MetaSound](#uaipeditormetasound-), [UAIP.Editor.EQS](#uaipeditoreqs-), [UAIP.Editor.StateTree](#uaipeditorstatetree), [UAIP.Editor.WorldConditions](#uaipeditorworldconditions-), [UAIP.Editor.Sequencer](#uaipeditorsequencer), [UAIP.Editor.SoundCue](#uaipeditorsoundcue), [UAIP.Editor.MotionMatching](#uaipeditormotionmatching-) and [UAIP.Editor.Conversation](#uaipeditorconversation-). What follows applies the same way in every one of them and is not repeated per domain.

Component classes are gated the same way but by a rule of their own, described in [UAIP.Editor.Blueprint — Components — SCS](#components--scs-8): the capability is `ComponentCustomTypeEdit`, it is shared by every command that increases how many instances of a component class exist (`AddActorComponent`, `AddBlueprintComponent`, `DuplicateBlueprintComponent`), and — unlike the domains above — deleting, renaming or reparenting a component is **not** gated by it.

- **The check runs on every operation that touches the type, not only `Add*`.** Once a node of a gated type exists in a graph, the same capability is re-evaluated whenever that node is edited, connected, disconnected, compiled, or deleted — and whenever its effective type is changed (reparenting) or a reference to it is created or replaced. Holding the capability when the node was added does not carry forward to later calls: if the session subsequently loses it (a role change, a narrower `AllowedCapabilities`), those later operations are refused too, exactly as `Add*` would have refused them.
- **⚠️ Breaking change — delete and disconnect used to be ungated.** Before this change, only each domain's `Add*` command checked the type being added; deleting a node or disconnecting its pins went through unconditionally, whatever type the node was. That is no longer the case: deleting or disconnecting a node of a gated type now needs the same capability `Add*` would have required to create it in the first place.
- **A type that can no longer be added can still be cleaned up.** A node whose class fails to load, or whose class an engine upgrade dropped support for, cannot be re-added — that is a structural refusal no capability grant changes. By itself, that is not a reason the existing node can't be deleted or disconnected: as long as the session holds whatever capability that type would require, removing it still works.
- **Compiling checks only the dangerous kind, not "custom" by itself.** In a domain that separates "project-/plugin-defined" from "dangerous" (Material does; see its own note for a domain where the distinction doesn't exist), compiling an asset only requires a capability for the dangerous kinds of type it contains — an ordinary project-defined type that isn't also a dangerous kind does not block compilation. Otherwise, a project containing any custom type at all would never compile without a capability grant, for every session, every time.
- **A missing capability on the asset-creation path is reported as `CapabilityNotAvailable`, the same as everywhere else.** A type named in `CreateAsset`'s `FactoryParams` — StateTree's `SchemaClass`, ControlRig's `ParentClass` — is admitted by the same policy as everywhere else, and a capability shortfall for that type arrives as `CapabilityNotAvailable`, naming every missing capability in full (`Required capability is not available: <names>`), exactly like `Add*`'s own refusal would. A structural refusal for the same field — the class did not resolve, is the wrong base type, is abstract, or is deprecated — is still `InvalidParams`, because that is a statement about the parameter rather than about a missing permission. ⚠️ This corrects an earlier state of this page: `ICreateAssetInterceptor`'s interception point originally answered with only a success flag and a message, with no way to carry an error classification out — every refusal it produced, capability shortfalls included, arrived as `InvalidParams` regardless of cause. It now carries the classification through, so the code you branch on matches the other capability-gated domains.

---

## Choosing which play world a Runtime command acts on

A networked Play-in-Editor session runs **more than one world inside the same editor process** — a server and one or more clients. 112 Runtime commands therefore take two optional parameters saying which of those worlds to act on. Both are optional, and omitting both gives exactly the behaviour these commands had before the parameters existed, so **no existing call changes meaning**.

| Parameter | Type | Meaning |
|---|---|---|
| `TargetNetRole` | string | `"Standalone"`, `"Server"` or `"Client"`, matched case-insensitively. `"Server"` matches a dedicated server **and** a listen server — a caller reasons about authority, not about which flavour of server PIE happened to start |
| `TargetPIEInstance` | integer | The instance index `ListPlayWorlds` reports. Use it when a role alone does not identify exactly one world |

Start from [`ListPlayWorlds`](#uaipruntimeworld): it reports every play world the engine currently holds, with the `PIEInstance`, `NetMode`, `MapName` and `bIsPrimaryPIEInstance` of each — and `PIEInstance` is the value `TargetPIEInstance` takes.

### How a target is resolved

| What you send | What happens |
|---|---|
| Neither parameter | The world the command would have used before these parameters existed — the primary play session |
| `TargetNetRole` alone, one world in that role | That world |
| `TargetNetRole` alone, several worlds in that role | `InvalidParams`. The message lists every candidate as `TargetPIEInstance <n> (TargetNetRole "...", NetMode ..., map ...)`, so the retry is the same call with one of those numbers added |
| `TargetPIEInstance` alone | That instance |
| Both, and they agree | That instance |
| Both, and they disagree | `InvalidParams`, naming the role that instance actually runs as |
| A role or an instance matching nothing | `NotAllowed` — play worlds exist, but none is the one you named. The message lists the ones that do |
| Nothing running at all | `NotAllowed` with `PIE is not running.` (`No active game world.` in a packaged build) |

`InvalidParams` means the request named a target that cannot be honoured; `NotAllowed` means the editor is not in a state the command can act on. Which of the two comes back is what tells "fix the call" apart from "start a play session".

Two limits worth knowing:

- **Only play sessions inside this editor process can be selected.** A dedicated server launched as a separate process is never a candidate and never appears in `ListPlayWorlds`.
- **Toolset bridge commands (`Toolset.*`) do not accept these parameters.** A bridge forwards the engine toolset's own inputs unchanged and its schema is generated from what the toolset declares, so there is nowhere to add a UAIP-specific parameter. Where you need to pick a session, use the native command covering the same operation.

### Commands that accept these parameters

| Domain | Commands |
|---|---|
| `UAIP.Runtime.World` | `SpawnActor`, `DestroyActor`, `TeleportActor`, `PossessActor`, `SetTimeScale`, `ExecuteConsoleCommand`, `SetDataLayerRuntimeState`, `GetDataLayerRuntimeState`, `ListDataLayerRuntimeStates`, `WaitForDataLayerStreaming` |
| `UAIP.Runtime.Observation` | `CaptureViewportImage`, `DumpWorldState`, `DumpActorState`, `DumpComponentState`, `CheckpointCapture`, `DumpGameViewportWidgets`, `FindGameViewportWidgets`, `DumpGameViewportWidgetTexts`, `DumpHUDState`, `ListSubsystems`, `DumpSubsystemState` |
| `UAIP.Runtime.Execution` | `RunFunctionalTest`, `RunRuntimeAutomationTest` |
| `UAIP.Runtime.Assertion` | `WaitForCondition`, `AssertActorProperty`, `AssertWorldState` |
| `UAIP.Runtime.Input` | `InjectInputKey`, `InjectEnhancedInputAction`, `InjectLegacyAction`, `InjectLegacyAxisInput`, `InjectLegacySpeechInput`, `AddMappingContext`, `RemoveMappingContext`, `SetInputMode`, `FlushInput`, `DumpInputState`, `GetEnhancedInputActionValue`, `ClickGameViewportWidget`, `PressGameViewportUIKey`, `TypeGameViewportText`, `EvaluateInputGateWithProjectCode` |
| `UAIP.Runtime.GAS` 🧩 | `GetAttributeValues`, `GetActiveEffects`, `GetGrantedAbilities`, `GetActiveTags`, `FindAttributeSetClasses`, `GrantAbility`, `RemoveAbility`, `ClearGrantedAbilities`, `ApplyEffect`, `RemoveEffect`, `ClearActiveEffects`, `SetAttributeValue`, `ResetAttributesToBase`, `SendGameplayEvent` |
| `UAIP.Runtime.Niagara` 🧩 | `GetUserVariables`, `GetVariable`, `SetVariable`, `SetSystem` |
| `UAIP.Runtime.AI` | `DumpAIPerceptionState`, `GetPerceivedActors`, `GetActorPerceivers`, `DumpAIPerceptionSystemState`, `ExplainSightPerception`, `DumpAIPerceptionSenseConfigs`, `DumpBehaviorTreeState`, `GetActiveBehaviorTreeNode`, `ListBehaviorTreeAgents`, `GetBlackboardValues`, `DescribeBehaviorTreeWithProjectCode`, `StartBehaviorTreeCapture` |
| `UAIP.Runtime.StateTree` 🧩 | `DumpStateTreeState`, `GetActiveStateTreeState`, `ListStateTreeComponents`, `DumpStateTreeInstanceData`, `StartStateTreeCapture` |
| `UAIP.Runtime.CommonUI` 🧩 | `DumpActivatableStacks`, `GetInputState`, `GetActionDisplayNames`, `DescribeActivatableWidgetsWithProjectCode` |
| `UAIP.Runtime.ChaosDestruction` | `ListGeometryCollections`, `DumpGeometryCollectionState`, `DumpChaosFieldState`, `StartDestructionCapture`, `CaptureGeometryCollectionStrain` |
| `UAIP.Runtime.Navigation` | `DumpNavigationSystemState`, `FindPath`, `IsLocationReachable`, `DumpNavMeshTiles`, `QueryNavModifiers`, `GetPathFollowingState`, `WaitForNavigationBuild`, `RebuildNavigation` |
| `UAIP.Runtime.Animation` | `DumpAnimInstanceState`, `GetAnimStateMachineStates`, `GetAnimBlendWeights`, `GetActiveMontages`, `GetAnimCurveValues`, `DumpAnimInstanceVariables`, `GetMotionMatchingState` |
| `UAIP.Runtime.Network` | `GetNetDriverState`, `ListNetConnections`, `DumpActorReplication`, `DumpReplicatedPropertyValues`, `CompareReplicatedProperties`, `SetNetworkEmulation`, `ResetNetworkEmulation` |
| `UAIP.Runtime.Mass` | `GetMassEntityCount`, `DumpMassEntityArchetypes`, `DumpMassProcessorGraph`, `DescribeMassEntity`, `GetMassEntityFragments` |

`CheckpointCapture` is the one entry above that does not resolve a world of its own: it is composed of `CaptureViewportImage` and `DumpWorldState`, and hands whatever target you name to both of them. That is what keeps the screenshot and the state dump inside one checkpoint describing the same world, instead of two worlds the engine happened to pick separately.

`QuitGame`, `ListPlayWorlds` and the CVar commands take neither: the first two are not addressed to a single world, and CVars are engine-global rather than per-world.

### Compatibility: what changed for commands that already existed

The game viewport UI commands ([`UAIP.Runtime.Observation`](#uaipruntimeobservation), [`UAIP.Runtime.Input`](#uaipruntimeinput)) came with a clean-up of how the existing Runtime commands report that there is no play world. While a play world exists nothing changes; the differences below show only when none does, or when a capability is denied.

**No play world: the error code is now `NotAllowed`.** Every Runtime command that needs a play world now refuses with the same `NotAllowed`, through one shared mapping. A scenario retries a step by itself only after `ExecutionFailed` or `PreconditionFailed`, so **these commands are no longer retried when there is no play world**. A scenario that relied on retries to wait for PIE to start must wait explicitly instead.

| Module | Commands | Before | Now |
|---|---|---|---|
| Observation | `DumpWorldState`, `DumpActorState`, `DumpComponentState`, `CaptureViewportImage`, `CheckpointCapture` | `ExecutionFailed` | `NotAllowed` |
| Input | the 11 existing commands | `ExecutionFailed` | `NotAllowed` |
| World | `SpawnActor`, `DestroyActor` (the other eight World commands already returned `NotAllowed`) | `ExecutionFailed` | `NotAllowed` |
| GAS 🧩 | all 14 commands | `ExecutionFailed` | `NotAllowed` |
| Assertion | `AssertActorProperty`, `AssertWorldState`, `WaitForCondition` | `ExecutionFailed` | `NotAllowed` |
| Execution | `RunFunctionalTest`, `RunRuntimeAutomationTest` | `ExecutionFailed` | `NotAllowed` |
| Niagara 🧩 — **the other way round** | `GetUserVariables`, `GetVariable`, `SetSystem`, `SetVariable`, also through the Toolset bridge | `PreconditionFailed` | `NotAllowed` |

- The five read commands of GAS (`GetActiveEffects`, `GetActiveTags`, `GetAttributeValues`, `GetGrantedAbilities`, `FindAttributeSetClasses`) still read the level being edited when no play world exists, **as long as you name no world** (`TargetNetRole` / `TargetPIEInstance` omitted). `NotAllowed` comes only when you named a world and none is running.
- `WaitForCondition` returns `NotAllowed` when there is no play world at its first check. If the world is found and then disappears while it waits, it still ends with `ExecutionFailed`, which a scenario retries.
- If the play world disappears **during** `RunFunctionalTest` or `RunRuntimeAutomationTest`, the result is still a timeout or a test failure, not `NotAllowed`.

**Capabilities.** `DumpWorldState`, `DumpActorState`, `DumpComponentState`, `DumpRuntimeLog`, `CapturePerformanceSnapshot` and `SearchLoadedClasses` now require `RuntimeInspect`; `CaptureViewportImage` requires `RuntimeCapture`; `CheckpointCapture` requires `RuntimeInspect` in addition to what it required before, because it dumps the world state internally. All are DefaultAllow, so only a configuration that denies one of them in `DeniedCapabilities` notices: the command is then refused with `PolicyViolation` when the request is accepted, and no artifact is produced. A capability that is merely not granted is `CapabilityNotAvailable`.

**Read-only.** Those commands and `CaptureViewportImage` now count as read-only: they run when the safety policy sets `ReadOnly`, and while a modal dialog is open.

**`CaptureViewportImage` captures the chosen world.** It now captures the game viewport of the world that `TargetNetRole` / `TargetPIEInstance` select, so with several PIE instances it no longer captures another instance's screen.

**`PlayerIndex` does not mean the same in every command.** The existing input commands (`InjectInputKey` and the others) take the number of the **player controller**. `PressGameViewportUIKey`, `TypeGameViewportText` and `DumpHUDState` take the number of the **local player** in the game instance's list. The parameter descriptions say which.

---

## UAIP.Core

System-level commands for discovery, health, and session management.

| Command | Description |
|---|---|
| 🆓 `HealthCheck` | Plugin connectivity check — returns `Status`, `UAIPVersion`, `EngineVersion`, `BuildConfig`, `ProjectFilePath` (absolute path of the open `.uproject`, used by the MCP Bridge to verify it is attaching to the right editor instance), `TransportTimeouts` (per-transport async command timeout in seconds, e.g. `{"HTTP": 120, "WS": 12}`), `QueueCongestion` (how busy the deferred-execution queue is, as one of `None` / `Low` / `High` — the exact number waiting is not returned, since it would let one session infer another session's activity), `MinBridgeVersion` (the oldest MCP Bridge version this plugin accepts — the bridge reads it from this response and refuses to run below it) |
| 🆓 `GetSystemInfo` | Returns UE version (Major/Minor/Patch/Changelist), project name, platform, build config, UAIP version |
| 🆓 `QueryCapabilities` | Returns `Capabilities` (the session's effective set), `RegisteredCapabilityCount` / `UngrantedCapabilityCount` (always) and `OperationalConstraints` (9 policy flags). Pass `IncludeUnavailable: true` to also get `RegisteredCapabilities` — every capability the loaded modules declare, each with `Name` / `DefaultPolicy` / `IsGranted`, so one this session does not hold can still be found by name; the deny-by-default ones are the entries whose `DefaultPolicy` is `Denied`. In the free demo build, an entry for a capability that only the Pro edition uses also carries `UnavailableReason: "NotInThisEdition"`; its `IsGranted` is always `false`, and naming it in `AllowedCapabilities` does not change that (see [Safety & Capabilities](safety.md#capabilities-the-demo-build-does-not-ship)). An entry without `UnavailableReason` is not blocked for that reason. Pro builds never carry it |
| 🆓 `ListCommands` | Filtered command catalog (filters: `ProviderPrefix`, `KeywordFilter`, `IncludeUnavailable`, `Stability`; `ResultMode` — `Commands` (default) or `Providers` to list providers instead of commands; `Limit` — max results returned (1–1000); `IncludeDescription` — include each command's description text in the listing) |
| 🆓 `DescribeCommand` | Full metadata for a single command (schema, required capabilities, availability) |
| 🆓 `ListPlugins` | ⚠️ **Deprecated** — use `UAIP.Runtime.Engine.Plugin.ListPlugins` instead. List installed plugins and their enabled state (JSON) |
| 🆓 `EndSession` | End a session explicitly and release its server-side resources; its artifacts become GC candidates |
| 🆓 `ReloadCapabilities` | Reload the capability set from `Config/DefaultUAIP.ini` without restarting the editor. Hidden from the default `ListCommands` response, and reports `Available: false` with `UnavailableDetail: "SafetyPolicyDisabled"` naming the ini key to set, until `AllowCapabilityReload=True` — see [UnavailableDetail](#unavailabledetail--the-eight-reasons-behind-a-handlerunavailable-refusal) |
| 🆓 `ListIntegrations` | Reports every optional-plugin integration UAIP knows about — a UAIP module (or part of one) that needs a plugin which can be disabled or absent at run time. Each entry carries `Name`, `State` (`Pending` / `Loading` / `Loaded` / `CompiledOut` / `PluginDisabled` / `PluginNotInstalled` / `DependencyNotLoaded` / `NotApplicable` / `LoadFailed`, plus `NotInThisEdition` in the free demo build for an integration only the Pro edition includes), `RequiredPlugins`, `MissingPlugins`, `DependsOn`, `CommandMatchers`, a plain-language `Remedy` — the same wording a `CommandNotFound` hint gives for one of its commands — and, only when `State` is `LoadFailed`, `FailureKind` / `FailureReason`. `CompiledOut` means the integration's code is not built into this binary: the build did not find the plugins it integrates with enabled, or the engine version is older than the integration supports. `MissingPlugins` lists the plugins that enabling would fix — the ones the build did not find enabled; it is empty when the reason is the engine version (the `Remedy` then names the minimum engine version) and for `NotInThisEdition`. The plugins an integration needs are always listed in `RequiredPlugins`. Packaged games built from a Fab-distributed UAIP installed in the engine cannot include these integrations; place UAIP in the project's `Plugins` folder so it is compiled with the project. An optional `State` parameter narrows the returned `Integrations` array to that state; `IntegrationCount` / `LoadedCount` / `NotLoadedCount` always cover every integration regardless of the filter. An unrecognised `State` value is refused with `InvalidParams`. Requires no capability |
| 🆓 `GetPendingInteractionStatus` | Reports where one pending interaction stands — `State`, `Cause`, `ElapsedSeconds`, `Prompt`, `Reason`, `Result` — without waiting for it to change. Requires the same explicitly given `SessionId` that started the interaction (an interactive command such as `DrawPCGSpline`); unknown, expired, and other-session all report `NotFound` identically |
| 🆓 `WaitForPendingInteraction` | Blocks until a pending interaction leaves `AwaitingUser`, or until this call's own `TimeoutSeconds` ceiling is reached (default 30, range [1, 600]), whichever comes first; on timeout the interaction itself is unaffected and keeps waiting for the human. Up to 4 concurrent calls may watch the same interaction, but reaching more than one requires `[UAIP.Transport] AllowConcurrentPassiveWaits` — see [Configuration](config.md) |
| 🆓 `CancelPendingInteraction` | Cancels a pending interaction the calling session started, without waiting for the human to act. An interaction already `Completed` is answered with `Success` rather than an error; the capabilities the starting command declared are re-checked against the session's current capability set; one the session no longer holds is refused with `CapabilityNotAvailable`, or with `PolicyViolation` when the operator has denied it explicitly in `DeniedCapabilities` |

### Sensitive values and where they are masked

`DescribeCommand` reports, for each command, the values UAIP keeps out of its own records:

- `SensitiveParams` — top-level parameter names, for example `Text` for `TypeGameViewportText`.
- `SensitiveResponseData` — positions in the response `Data`, written as dot paths in which `[]` stands for every element of an array: `PasswordFieldValues` (a top-level field of `DumpGameViewportWidgetTexts`), `Connections[].RemoteAddress` (`ListNetConnections`), and `Properties[].Value` and `Components[].Properties[].Value` (`DumpReplicatedPropertyValues`). A plain name is a top-level field, so a list written before nested paths existed reads the same.

**Path syntax.** Segments are separated by `.`; each segment is a non-empty field name followed by zero or more `[]`. A field name may not contain `.`, `[` or `]`, and there is no index syntax (`[0]`). Field names are matched ignoring case. A path that reaches a field the response does not have, a `null`, or an empty array masks nothing there and adds nothing.

**Where values are masked.** In the completion notification the editor raises after every command, which the editor's own notifications and any code that records commands (audit records, logs) receive. Each value at a declared position becomes the string `"<redacted>"`, whatever its type (`null`, an object or an array included) and without its length. When the response does not have the shape the path describes, the value is masked rather than skipped: something other than an array (and not `null`) at a `[]` position, or something other than an object (and not `null`) where the path reads a field — for example a string or an array at `A` of `A.B` — is masked whole. When the declaration cannot be relied on, the whole `Data` is masked instead, keeping the top-level field names: when a declared path is malformed (the editor also logs an error when the command is registered), and when the command cannot be resolved at all (an unknown name, or a command unregistered while it ran). In a [scenario](scenario.md), a step that takes a masked value — or the array or object holding it — from an earlier step's response with a `${...}` template is recorded with all of its parameters and response `Data` masked, and so is every step that value is passed on to; the step itself still receives the real value.

**Where values are not masked.** The response returned to the caller (MCP, HTTP, WebSocket, CLI, and each step of a scenario result) and the artifacts a command saves keep the original values: the caller asked for them, behind whatever capability the command requires. An artifact stays on disk until artifact garbage collection removes it.

---

## UAIP.Core.Artifacts

Reading back the content of an artifact a previous command produced. See [Artifacts](artifacts.md) for the artifact model itself.

| Command | Description |
|---|---|
| 🆓 `GetArtifact` | Returns the stored content of an artifact by `ArtifactId`, for artifacts the calling session owns. Text-shaped artifacts (`Json` / `Log` / `Report` / `Bundle`) come back in `Content`, at most `MaxBytes` at a time (default and ceiling 65536, floor 4); binary ones (`Image` / `Trace`) come back as metadata and `TotalBytes` only and are meant to be opened as files instead. Pass the previous call's `NextOffset` as `Offset` to read on — the returned window always ends on a character boundary, so paging never splits a character, duplicates text or loses any. An `Offset` past the end succeeds with `ReturnedBytes` 0, which is how the end of a paged read is detected. `MetaIsPartial` true means the metadata was rebuilt from the file on disk after the store's index was lost, so `Sequence` / `Description` are absent and `CreatedAt` is the file's modification time; `CommandNameVerified` false means nothing corroborates the command name the artifact's filename carries. An artifact belonging to another session reports `NotFound`, indistinguishable from one that never existed. Requires `ArtifactContentRead` |

---

## UAIP.Editor.Workspace

Editor lifecycle, tab management, graph layout, shader compilation, Live Coding.

| Command | Description |
|---|---|
| 🆓 `FocusEditorTab` | Bring the editor tab for an asset to the front. The target is addressed by `AssetPath`, **not** by a Slate layout tab identifier — the `ActiveTabId` reported by `DumpEditorState` (`"Viewport"`, `"Inspector"`, …) is rejected here. Use the `TabId` parameter of `CaptureEditorTabImage` when you need to address a tab by its layout identifier. An optional `GraphName` additionally brings that named sub-graph's tab to the front, for any currently open editor that supports Blueprint graph navigation (plain Blueprint, AnimBlueprint, WidgetBlueprint/UMG, GameplayAbility Blueprint, ControlRig, and others) — an empty string is treated the same as omitting it. See the note below the table for the `Result` contract and a breaking change on two of its error codes |
| 🆓 `CloseEditorTab` | Close the editor tab for an asset. Takes `AssetPath`, addressed the same way as `FocusEditorTab` |
| 🆓 `ListSpawnableTabs` | List editor tabs that can currently be opened, each row giving `TabId` / `OwnerMajorTabId` / `OwnerInstanceId` to pass straight into `OpenTabById` / `CloseTabById` as `TabId` / `OwnerTabId` / `OwnerInstanceId`, plus display name, tooltip, and whether the tab is already open. That last flag is read against the same owner the row names: a `MajorTabLocal` row answers for its own window alone, while a `Global` row answers for the whole editor, because a tab registered editor-wide docks wherever the layout puts it and stays reachable through `"Global"` regardless. Not exhaustive — every response repeats `EnumerationScope: "MenuVisible"`: a `TabId` missing from the list may still open (it may just be excluded from generated menus), or may be permanently refused by configuration, so treat an absence as unlisted, never as nonexistent. Read-only, but still requires `EditorTabSpawn` because reading display names and tooltips can evaluate third-party delegates |
| 🆓 `OpenTabById` | Open the editor tab named by its Slate layout identifier (`TabId`) — a different identifier space from `FocusEditorTab`'s `AssetPath` — reaching tabs neither `FocusEditorTab` nor menu-driven navigation can, including tabs registered only through legacy menus never wired into ToolMenus, and tabs whose owning window is not currently in front. Pass `OwnerTabId` `"Global"` for tabs registered editor-wide (Output Log and similar), or a major tab's own `TabId` (plus `OwnerInstanceId` to disambiguate) to reach a panel that lives inside it; opens that owning window first when it is not already open. An owner that is already open is used as it stands, so every row `ListSpawnableTabs` returns can be passed straight back in — the spawner and permission checks on the owner apply only when this call would have to open it. The response reports the `InstanceId` of the tab actually opened — the only place that value can be obtained — plus `WasAlreadyOpen` and `OwnerOpenedByThisCall`, so callers know what to close afterward (target tab first, then the owning window). On failure, everything this call opened is closed again. Run `ListSpawnableTabs` to discover valid combinations (requires `EditorTabSpawn`) |
| 🆓 `CloseTabById` | Close a currently live editor tab addressed the same way as `OpenTabById` (`TabId` / `OwnerTabId` / `InstanceId` / `OwnerInstanceId`), never by asset path. Unlike `OpenTabById`, it never opens `OwnerTabId` to reach something inside it — an owner that is not already open reports `NotFound` instead of being spawned — and it skips the tab permission check, since refusing to clean up a tab this call is meant to close, purely because policy tightened at runtime, would defeat the purpose. As a result its target is any tab that happens to be live right now, including one a person opened by hand, not only tabs this session opened itself (requires `EditorTabSpawn`) |
| 🆓 `NormalizeEditorLayout` | Focus the main graph tab and hide transient panels. Saves the same editor-state artifact as `OpenAsset`, including the deprecated `ActiveTabId` field — read `ActiveAssetPath` instead (see [`OpenAsset`](#uaipeditorassets)) |
| 🆓 `SetEditorWindowState` | Minimize the editor main window, or restore it from the minimized state, and return once the window has settled in the requested state. Takes one required parameter, `State`: `Restored` or `Minimized` (anything else is `InvalidParams`). `Restored` undoes the minimization. Windows lets only the foreground application bring a window to the front, so while the user works in another application the editor is restored **behind it**: the keyboard focus stays in that application and the editor's taskbar button may flash. The window can be captured all the same. A window that was maximized before it was minimized is maximized again, because `Restored` does not undo maximization. Only the main window is affected. Requires `EditorWindowStateControl` (DefaultDenied; see the note below the table) |
| 🆓 `SetGraphZoom` | Set graph viewport zoom level |
| 🆓 `FrameGraphAll` | Zoom the graph viewport to fit all nodes |
| 🆓 `FrameGraphSelection` | Zoom the graph viewport to fit selected nodes |
| 🆓 `SetGraphSelection` | Select graph nodes by ID list |
| 🆓 `ShutdownEditor` | Shut down the UE Editor (optionally save packages). Cancels a `RestartEditor` attempt that is still in progress, so the exit is not turned into a restart |
| 🆓 `RestartEditor` | Restart the UE Editor (optionally save packages). `Success` means the request was **accepted**, not that the editor has restarted — the outcome is read with `GetRestartStatus`, and the MCP Bridge waits for it automatically. See the note below the table |
| 🆓 `GetRestartStatus` | Report the state of a `RestartEditor` attempt (`Scheduled` / `CloseRetrying` / `Declined` / `ExitStarted`). Read-only; requires `EditorLifecycle` |
| 🆓 `SaveAllPackages` | Save all modified packages (optionally include maps) |
| 🆓 `Undo` | Undo the last editor operation |
| 🆓 `Redo` | Redo the last undone operation |
| 🆓 `GetUndoHistory` | Read the undo history without executing anything. Returns how many steps can be undone or redone, and their names |
| 🆓 `GetLastCrashReport` | Get the most recent crash report |
| `WaitForShaderCompilation` | Wait until shader compilation completes |
| `RecompileGlobalShaders` | Force-recompile all global shaders and wait for completion |
| `CompileLiveCoding` | Trigger Live Coding recompilation |
| `GetLiveCodingStatus` | Get the current Live Coding status |
| `EnableLiveCodingForSession` | Enable Live Coding for the current session |

> **`SetEditorWindowState` — result and refusals.** `Result` carries `PreviousState`, `State` (each `Normal`, `Minimized` or `Maximized`; `NoWindow` if the window was destroyed while the command waited), `Changed` (bool) and `Size` (`Width` / `Height` in screen pixels); the same content is stored as a JSON artifact. A request for the state the window is already in returns at once with `Changed: false` and waits for nothing. Otherwise the command waits up to 2 seconds for the window to settle; if it does not settle, or the window is destroyed meanwhile, the answer is `ExecutionFailed` with the state that was observed. Because the command changes the window while it waits, it counts as a running command and holds the transport slot for up to those 2 seconds.
>
> It is refused, with a `Reason` from the same vocabulary as the [capture commands](#capture-refusals), when there is nothing to act on: `Headless`, `BlockedByModal` and `Hidden` answer `NotAllowed`, and `NoWindow` (the main window does not exist yet) answers `PreconditionFailed`. A window that is `Minimized`, or that Slate cannot draw right now (`DebuggerPaused`, `NotInVisibleTree`, `NotRenderable`), is **not** refused, since changing the window is what the command is for.
>
> **Size synchronization after `Restored`.** After a restore (and also when the window is already in the requested `Restored` state, in which case `Changed: false` is kept), the command synchronizes the size Slate holds for the window with the size the operating system reports. If that cannot be fixed, it answers `NotAllowed` with `Reason: WindowSizeMismatch`; the result still carries `PreviousState`, `State`, `Changed` and `Size` (after the synchronization), plus `OsClientSize` and `SlateSize` (each `Width` / `Height`), and the same content is stored as a JSON artifact. Minimize and restore the window again, or ask the user to change its size by hand. Requesting `Minimized` does not compare sizes.
>
> `EditorWindowStateControl` is **DefaultDenied** and is registered in the demo build too, where it is not marked as unavailable. Without it the command is refused with `CapabilityNotAvailable`, and under `ReadOnly` with `PolicyViolation`, like any other write. To allow it, add `+AllowedCapabilities=EditorWindowStateControl` to `[UAIP.SafetyPolicy]` in `Config/DefaultUAIP.ini` (the demo's `DefaultUAIP.ini` carries the line as a comment).

> **`RestartEditor` and `GetRestartStatus` — what `Success` means and how to learn the outcome.** Both require `EditorLifecycle`. `RestartEditor` takes one optional parameter, `SaveAll`. When omitted, it saves unsaved changes first unless `DisableSave` is in force (then it does not save); an explicit `SaveAll: true` under `DisableSave` is refused with `PolicyViolation`. `Success` means the request was **accepted**. `Data` carries `AttemptId`, `State` (`Scheduled`), `RestartScheduled: true`, `CloseDeadlineSeconds` and `ProcessId` (the id of the editor process that accepted the request).
>
> - **Through the MCP Bridge**, the call does not return at acceptance. The bridge waits for the outcome, keeps sending progress to the client, and answers once the new editor is connected, the restart was declined (the editor's reason and remedy are returned as the error), or the outcome could not be confirmed within the time limit. There are two limits: until the editor closes, the deadline the editor reported plus about 30 seconds (and up to 60 more seconds once shutdown has begun); after it closes, the bridge's editor-startup wait (default 120 seconds). When the bridge reports that it could not confirm the outcome, check `GetRestartStatus` and `uaip_get_editor_status`.
> - **Over any other transport** (HTTP and so on), `Success` is only the acceptance. Call `GetRestartStatus` with the `AttemptId`, or without it for the most recent attempt. It answers only while the editor that accepted the request is still running: a restarted editor has no record of earlier attempts, and an unknown `AttemptId` — or one that has aged out (the latest 8 attempts are kept) — returns `NotFound`. Every `GetRestartStatus` answer, `NotFound` included, carries `ProcessId`, so a caller can tell the editor it asked from its successor.
> - **`GetRestartStatus` data**: `AttemptId`, `State`, `RequestedAt`, `ElapsedSeconds`, `CloseDeadlineSeconds`, `ProcessId`. `State` is `Scheduled`, `CloseRetrying` (the editor is busy saving or loading and keeps trying to close), `Declined` or `ExitStarted`. A `Declined` attempt also carries `DeclineReason`, `DeclineDetail`, `Remedy`, `OutcomeErrorCode` (`ExecutionFailed`), `OutcomeErrorMessage`, `RestoredDirtyPackageCount` and `LostDirtyPackageCount`.
> - **Refused up front (nothing is saved, discarded or changed)**: `PreconditionFailed` while a lighting build (`LightingBuildRunning`), an Interchange import (`InterchangeActive`) or a main window recreation (`MainFrameRecreating`) is running, or while a modal dialog is open (`ModalWindowOpen`; only in an editor a person operates, not in the unattended editor the bridge launches) — `Data` carries `DeclineReason` and `Remedy`, and the message ends with the remedy. `NotAllowed` when the editor is already exiting. `Conflict` while another attempt is in progress (`Data.AttemptId` names it; this is decided before the conditions above). `ExecutionFailed` when saving was requested and some packages failed to save (`Data.FailedPackages` lists them); the editor does not restart.
> - **Declined after acceptance**: the editor logs a warning, restores the settings it changed for the restart, and puts unsaved changes it was about to discard back into the unsaved state (`RestoredDirtyPackageCount` / `LostDirtyPackageCount` give the counts). `DeclineReason` is one of `LightingBuildRunning`, `InterchangeActive`, `CloseRequestDeclined`, `CloseTimedOut` or `SupersededByShutdown`. The editor keeps running.
> - **Close deadline**: if the editor cannot close within `CloseDeadlineSeconds` (default 60) of acceptance, the attempt is declined with `CloseTimedOut`; in an editor a person operates, it is not declined while a modal dialog is open (the restart itself does not show a save prompt; such a dialog comes from something else). Change it in `DefaultUAIP.ini` with `[UAIP.EditorRestart]` `CloseDeadlineSeconds` (10 to 600; see [Configuration](config.md#uaipeditorrestart--closing-deadline-for-restarteditor)) — raise it if you often restart right after a heavy save or shader compilation.
> - **Shutting down during an attempt**: `ShutdownEditor`, or `QuitGame` when it ends up asking the editor itself to exit, cancels the attempt and the editor exits without starting a new one. A `ShutdownEditor` refused by the safety policy (`PolicyViolation`) cancels nothing. Before the editor exits, `GetRestartStatus` reports the attempt as `Declined` with `SupersededByShutdown`. A person closing the window, or an exit that does not come from UAIP, during an attempt still ends in a restart.
> - **Older components**: an older MCP Bridge still returns at acceptance, and an older editor returns no `AttemptId`, so a newer bridge behaves as before. Either way, a restart declined after acceptance is only visible through `GetRestartStatus` on a newer editor.

> **`FocusEditorTab`'s `GraphName` — response contract.** When `GraphName` is a non-empty string, `Result` carries four fields: `WindowFocusRequested` (bool — records that bringing the editor window to front was *requested*; it does not guarantee the OS actually put it in the foreground), `GraphNameRequested` (bool), `GraphNameApplied` (bool), and `Reason` — a closed set of three strings, `Applied` / `BlueprintEditorInterfaceUnavailable` / `OpenFailed`. Read `GraphNameApplied` and `Reason` rather than `Success` alone: a `BlueprintEditorInterfaceUnavailable` reason still reports `Success: true`, because the open editor genuinely has no Blueprint graph-navigation entry point (for example a ControlRig editor with `RigVM.UseNewEditor` enabled) and retrying the same input cannot change that. None of these four fields are set when `GraphName` is omitted or empty — callers must handle both "`Result` absent" and "`Result.GraphNameRequested` is `false`". Applying a graph move clears the editor's current UI selection, and for a Widget Blueprint opened in Designer mode, switches it to Graph mode first (needed to display the graph at all); both happen before the graph itself is opened, so they can already have taken effect even when the open subsequently fails with `OpenFailed`.
>
> ⚠️ **Breaking change** — two of `GraphName`'s error codes changed from `ExecutionFailed` to a non-retryable code, because a scenario's `RetryCount` retries only `ExecutionFailed` and `PreconditionFailed`, and retrying either of these can never succeed on the same input: naming a graph that does not exist in the asset now answers `NotFound` (previously `ExecutionFailed`); naming `GraphName` on an asset that is not Blueprint-derived now answers `InvalidParams` (previously `ExecutionFailed`). `OpenFailed` — a genuine failure to open the graph after its navigation entry point was found — is unchanged and remains `ExecutionFailed`, since that one is still worth retrying.
>
> **When `GraphName` matches more than one graph in the asset, one of them is opened and which one is chosen is not defined by this contract** — do not build any behavior around a particular one being picked, since nothing here is guaranteed to keep picking it on a later call. This does not read a caller's mind about which one was intended, and it does not change what is returned: `GraphNameApplied` and `Reason` describe whether opening succeeded, not which graph was opened. In practice a name collision is rare: sibling graphs at the same nesting level (functions, macros, the event graph, an interface's implementation graphs) can never carry the same name — the editor offers no way to create that. A name can only be shared when a collapsed graph is involved: a graph nested inside a collapsed graph can end up sharing a name with a graph outside it.

### Toolset bridges — LiveCoding (1) 🧩

Bridge command via the `LiveCodingToolset` (UE 5.8+). Provider: `Toolset.Editor.LiveCoding.*`.

| Command | Description |
|---|---|
| `Toolset.Editor.LiveCoding.CompileLiveCoding` | Trigger Live Coding recompilation (requires `LiveCodingControl`) |

---

## UAIP.Editor.Engine.Log

Log entry retrieval for the editor output log. Log **verbosity** commands live under [`UAIP.Runtime.Engine.Log`](#uaipruntimeenginelog).

| Command | Description |
|---|---|
| 🆓 `GetLogEntries` | Retrieve recent log entries from the editor output log (supports pattern filtering; no capability required) |

### Toolset bridges — Logs (4) 🧩

Bridge commands via the `LogsToolset` (UE 5.8+, EditorToolset plugin). Provider: `Toolset.Editor.Toolset.Logs.*`.

| Command | Description |
|---|---|
| `Toolset.Editor.Toolset.Logs.GetLogEntries` | Retrieve recent log entries from the editor output log |
| `Toolset.Editor.Toolset.Logs.GetLogCategories` | List registered log category names |
| `Toolset.Editor.Toolset.Logs.GetVerbosity` | Get the verbosity level for a log category |
| `Toolset.Editor.Toolset.Logs.SetVerbosity` | Set the verbosity level for a log category (requires `LogVerbosityEdit`) |

### Toolset bridges — CVar (1) 🧩

Bridge commands via the EditorToolset plugin (UE 5.8+). Provider: `Toolset.Editor.Toolset.EngineManagement.*`.

| Command | Description |
|---|---|
| `Toolset.Editor.Toolset.EngineManagement.SearchCVars` | Search CVars by name pattern; sensitive patterns are excluded (requires `CVarInspect`) |

---

## UAIP.Editor.Engine.Plugin

Plugin management for the editor — read / write plugin state, descriptor, and dependencies. Requires UE 5.8+ with the `PluginUtils` plugin enabled. Write commands (`SetPluginEnabled`, `UpdatePluginDescriptor`, `AddPluginDependency`, `RemovePluginDependency`) require a restart to take effect.

| Command | Description |
|---|---|
| 🆓 `GetPluginDescriptor` | Read the full `.uplugin` descriptor JSON for a plugin |
| 🆓 `GetPluginDependents` | List plugins that depend on a given plugin (budget-capped scan; `Truncated: true` on limit) |
| 🆓 `GetPluginTemplateDescriptions` | List available plugin scaffold templates |
| 🆓 `IsPluginCreationAllowed` | Check whether new plugin creation is allowed in the current editor state |
| 🆓 `IsPluginModificationAllowed` | Check whether a specific plugin is modifiable (not Engine/Marketplace/GFP) |
| `SetPluginEnabled` | Enable or disable a plugin (`PluginEnableToggle` required; always returns `RestartRequired: true`) |
| `UpdatePluginDescriptor` | Overwrite selected fields of a plugin's `.uplugin` file (`PluginDescriptorEdit` required; supports `DryRun`) |
| `AddPluginDependency` | Add a dependency entry to a plugin's `.uplugin` (`PluginDependencyEdit` required) |
| `RemovePluginDependency` | Remove a dependency entry from a plugin's `.uplugin` (`PluginDependencyEdit` required) |

### Toolset bridges — Plugin (15) 🧩

Bridge commands via the `PluginToolset` (UE 5.8+). Provider: `Toolset.Plugin.*`.

| Command | Description |
|---|---|
| `Toolset.Plugin.ListEnabledPlugins` | List currently enabled plugins |
| `Toolset.Plugin.ListDiscoveredPlugins` | List all discovered plugins (enabled + disabled) |
| `Toolset.Plugin.GetPluginInfo` | Get plugin details by name |
| `Toolset.Plugin.IsEnabled` | Check whether a plugin is currently enabled |
| `Toolset.Plugin.GetPluginDependencies` | Get the direct dependencies declared by a plugin |
| `Toolset.Plugin.GetPluginForAsset` | Resolve the owning plugin for a given asset path |
| `Toolset.Plugin.GetPluginDescriptor` | Read the `.uplugin` descriptor (Toolset variant) |
| `Toolset.Plugin.GetPluginDependents` | List plugins that depend on a given plugin |
| `Toolset.Plugin.GetPluginTemplateDescriptions` | List scaffold templates |
| `Toolset.Plugin.IsPluginCreationAllowed` | Check creation permission |
| `Toolset.Plugin.IsPluginModificationAllowed` | Check modification permission |
| `Toolset.Plugin.SetPluginEnabled` | Enable / disable a plugin (requires `PluginEnableToggle`) |
| `Toolset.Plugin.UpdatePluginDescriptor` | Update descriptor fields (requires `PluginDescriptorEdit`) |
| `Toolset.Plugin.AddPluginDependency` | Add a dependency (requires `PluginDependencyEdit`) |
| `Toolset.Plugin.RemovePluginDependency` | Remove a dependency (requires `PluginDependencyEdit`) |

---

## UAIP.Editor.Engine.ConfigSettings

Project Settings and Editor Preferences management via `ISettingsModule`. Commands use a three-level path `ContainerName / CategoryName / SectionName` to address a settings section. Write operations are restricted to files under the project `Config/` directory — engine ini files are rejected with `PolicyViolation`.

| Command | Description |
|---|---|
| 🆓 `ListSettingsContainers` | List all registered settings containers (e.g. `Project`, `Editor`). No capability required |
| 🆓 `ListSettingsCategories` | List all categories in a settings container. No capability required |
| 🆓 `ListSettingsSections` | List all sections in a settings category. No capability required |
| 🆓 `GetSettingsSchema` | Return a JSON artifact with editable property names, types, descriptions, defaults, and edit conditions for a section (requires `EditorInspect`) |
| 🆓 `GetSettingsValues` | Return a JSON artifact with current property values for a section. Secret fields (name matches a secret pattern, has secret metadata, or is a file path type) are masked with `***` (requires `EditorInspect`) |
| `SetSettingsValues` | Merge a `Properties` map into the settings object via `ImportText`. Supports `DryRun` (validates without applying). Requires `ConfigSettingsEdit`. Blocked during PIE. Values are engine text only, so a reference, a container or a struct outside the built-in value catalogue is refused **whatever capabilities the session holds** — write those through `SetProjectSetting`, which reaches the same settings object and takes `ValueJson`. A value that only parses part-way is now refused with `InvalidParams` instead of being applied as a fragment |
| `SaveSettings` | Persist in-memory settings to the section's ini file via `ISettingsSection::Save()`. Requires `ConfigSettingsSave`. Blocked during PIE and when `bDisableSave` is set |
| `ResetSettingsToDefaults` | Revert the settings object to class defaults and save. Requires `ConfigSettingsReset`. Blocked during PIE |

### Toolset bridges — ConfigSettings (8) 🧩

Bridge commands via the `ConfigSettingsToolset` plugin (UE 5.8+). Provider: `Toolset.ConfigSettings.*`.

| Command | Description |
|---|---|
| `Toolset.ConfigSettings.ListContainers` | List all registered settings containers |
| `Toolset.ConfigSettings.ListCategories` | List all categories within a settings container |
| `Toolset.ConfigSettings.ListSections` | List all sections within a settings category |
| `Toolset.ConfigSettings.GetSectionSchema` | Get the property schema for a settings section |
| `Toolset.ConfigSettings.GetSectionPropertyValues` | Get current property values for a settings section |
| `Toolset.ConfigSettings.SetSectionProperties` | Set property values on a settings section and persist them (requires `ConfigSettingsEdit`) |
| `Toolset.ConfigSettings.SaveSection` | Persist the current in-memory settings for a section to its ini file (requires `ConfigSettingsSave`) |
| `Toolset.ConfigSettings.ResetSectionToDefaults` | Reset all property values of a settings section to their compiled defaults (requires `ConfigSettingsReset`) |

---

## UAIP.Editor.Engine.Toolset 🧩

An investigation aid for authoring Toolset bridge commands, not a command you would reach for in ordinary use. Requires the `ToolsetRegistry` plugin (UE 5.8+); reports `Available: false` with `UnavailableDetail: OptionalPluginDisabled` when it is not present, and does not appear in `uaip_list_commands`' default output on such an environment — name it explicitly with `uaip_describe_command` to see why.

| Command | Description |
|---|---|
| `DumpToolsetParameterSchemas` | Dump the raw JSON Schema (parameter names, types, `Required` flags) that `ToolsetRegistry` reports for every currently-registered Toolset, as a `Json` artifact. `{}` returns every registered toolset; the optional `ToolsetName` narrows the dump to one, by an exact, case-sensitive match against its full `<Module>.<Toolset>` name (e.g. `PCGToolset.PCGToolset` — the module name alone matches nothing). A name that matches nothing returns `Success: true` with an empty array, not `NotFound`. No capability required; read-only |

---

## UAIP.Editor.Observation

Capture screenshots and dump editor state — all read-only.

| Command | Description |
|---|---|
| 🆓 `CaptureActiveWindowImage` | Screenshot of the active top-level editor window (PNG artifact). The editor does not have to be the foreground application: when no window is active, the main window is captured instead and `Result.CapturedWindow` says which one you got (`"ActiveWindow"` / `"MainWindow"`). The fallback only reaches the main window, so a floating asset editor or modal dialog needs `CaptureEditorTabImage`. When the target is not drawn (the window is minimized or hidden, a modal window is open, and so on), the command is refused with `NotAllowed` or `PreconditionFailed` and a `Reason`, instead of returning an empty capture — see [Capture refusals](#capture-refusals) |
| 🆓 `CaptureEditorTabImage` | Screenshot of a specified editor tab's widget area, addressed by Slate layout identifier — `DumpEditorState`'s `ActiveTabId` can be passed straight through. Works with the editor in the background. ⚠️ Brings the named tab to the front before capturing (a tab behind a sibling is not drawn and would come back empty), together with the outer editor tab that holds it (for example the level editor tab when a Blueprint editor is in front of it), so capturing changes which tab the user sees and the tab flashes. The editor's OS window is not raised above other applications. When a tab was brought forward, the command waits up to 2 seconds for it to be drawn before it captures; a tab already in front is captured immediately. If the tab is still not drawn after that, the message asks the user to bring it to the front. When the target is not drawn (the window is minimized or hidden, a modal window is open, and so on), the command is refused with `NotAllowed` or `PreconditionFailed` and a `Reason`, instead of returning an empty capture — see [Capture refusals](#capture-refusals) |
| 🆓 `CaptureGraphViewportImage` | Screenshot of an SGraphEditor viewport. When the target is not drawn (the window is minimized or hidden, a modal window is open, and so on), the command is refused with `NotAllowed` or `PreconditionFailed` and a `Reason`, instead of returning an empty capture — see [Capture refusals](#capture-refusals) |
| 🆓 `DumpEditorState` | Active tab, open assets, window dimensions, etc. (JSON). Also reports the play session as three booleans — `IsPIERunning`, `IsPIEPaused` and `IsSimulatingInEditor` — which is what to read before mutating, since most editor edits are refused while a session is running and a world dump taken then describes the play world rather than the editor world. All three are always present, so "nothing is playing" stays distinguishable from "not reported". `MainWindowSize` is the size of the first top-level window, which is not always the main frame; read `MainWindowState` for the main frame itself. `MainWindowState` carries `State` (`Normal` / `Minimized` / `Maximized` / `Hidden` / `NoWindow`; a window that has never been shown reports `Hidden`), `Size` and `RestoredSize` (each an object with `Width` and `Height`; both are 0 when there is no window) and `CaptureBlocker` — `None` when a capture can be taken, otherwise the [`Reason`](#capture-refusals) a capture would be refused with. The command only reads and never synchronizes anything, so `CaptureBlocker` can be `WindowSizeMismatch` for a mismatch that a capture or `SetEditorWindowState` would have fixed by itself. `MainWindowState` also carries `SizeCheck` (`NotQueryable` / `Minimized` / `Matched` / `Mismatched`), `SizeMismatched` (bool or null), and `OsClientSize` and `SlateSize` (each `Width` / `Height`, null unless `SizeCheck` is `Matched` or `Mismatched`). The root carries `WindowMessageRecording`: `RecordingEnabled`, `RecordingActive`, `RecordingStatus` (`Disabled` / `NotRegistered` / `WaitingForMessages` / `Recording`), `TotalRecordedCount`, `Capacity` (64, the capacity of the ring the non-priority windows share), `PriorityWindowCapacity` (64, per priority window), `MaxPriorityWindowCount` (8), `PriorityMessageCount`, `SharedMessageCount` (the two add up to the length of `RecentMessages`) and `RecentMessages` (oldest first; each has `Kind`, `WindowHandle`, `IsPriorityWindow`, `SizeType`, `MessageSize`, `MessageSizeMeaning`, `WindowPosFlags`, `ClientStateAtArrival`, `TimeSeconds` and `SequenceNumber`). The messages of a regular Slate window — the main window, a floating tab or an asset editor in its own window, a modal dialog — are priority messages: each such window keeps its own last 64 messages (up to 8 windows; when a ninth sends a message, the window whose last message is oldest is dropped with its messages), so notification toasts and menus, which send hundreds of messages and are not priority windows, cannot push them out. The messages of all other windows are still recorded, in one ring they share (the last 64), and the list can hold up to 576 messages in total. `IsPriorityWindow` tells which kind a message came from. `MessageSizeMeaning` says what `MessageSize` measures for the message: `ClientArea` (`WM_SIZE`), `WholeWindow` (`WM_WINDOWPOSCHANGED`, which reports the whole window rather than its client area, so do not compare it with `ClientArea` directly) or `ProposedWholeWindow` (`WM_NCCALCSIZE`). `MessageSize` is null when the message carried no size, `SizeType` is null unless the message is `WM_SIZE`, and `ClientStateAtArrival` is null when the operating system could not be asked about the window. See [`RecordWindowMessages`](config.md#uaipruntimeobservation--window-size-message-log-and-hud-draw-statistics) |
| 🆓 `DumpSelectionState` | Current editor selection (JSON): `SelectedActors` / `SelectedObjects` are always reported. `SelectedNodes` (`NodeId` / `NodeClass` / `NodeTitle` / `Position` per node) is additionally populated when `TabId` names an open graph editor tab — resolved the same way as `CaptureGraphViewportImage`'s `TabId` (an exact Slate tab match, then a case-insensitive substring match against an open asset's name; a `/`-bearing content-browser path is rejected with `InvalidParams`). A `TabId` that resolves no tab answers `NotFound` rather than falling back to an empty `SelectedNodes`. Omitting `TabId` is unchanged from before: `SelectedNodes` stays empty and actor/object selection is reported regardless |
| 🆓 `DumpOpenTabs` | List of open asset editor tabs (JSON) |
| 🆓 `DumpOutputLog` | Buffered Output Log as a text artifact (line count / filter support) |
| 🆓 `DumpMessageLog` | Message Log entries with category filter (JSON artifact) |
| 🆓 `DumpSlateTree` | Slate widget tree (JSON, root path filter support) |
| 🆓 `InspectMenu` | Top-bar menu structure under a path (labels, enabled, checked) |
| 🆓 `InspectContextMenu` | Context menu items for a target (without executing them) |
| 🆓 `ObserveWidget` | Time-series sampling of widget Visibility / Enabled / Hovered / Focused state |
| 🆓 `GetLogCategories` | List all registered engine log category names (optional substring filter) |
| 🆓 `ListGraphNodes` | List every node in a graph editor tab — `NodeId` (GUID), `NodeClass`, `NodeTitle`, `Position`. Works with any `UEdGraph`-based editor |
| 🆓 `CaptureViewportImageAnnotated` | Viewport screenshot with world-coordinate labels drawn on it (requires `ViewportAnnotationCapture`). When the window that holds the viewport is not drawn (for example minimized), the command is refused with `NotAllowed` or `PreconditionFailed` and a `Reason` instead of returning a stale frame — see [Capture refusals](#capture-refusals) |

### Capture refusals

`CaptureActiveWindowImage`, `CaptureEditorTabImage`, `CaptureGraphViewportImage` and `CaptureViewportImageAnnotated` check that the target will be drawn before they take anything. When it will not be, they refuse without capturing — they no longer return an empty image, and `CaptureViewportImageAnnotated` no longer returns a stale frame — and the response carries a `Reason` plus an error message that says what to do. The checks run in the order of the table; the first one that fails names the `Reason`. `DumpEditorState` reports the same vocabulary for the main window as `MainWindowState.CaptureBlocker`, and `SetEditorWindowState` uses it for its refusals.

| `Reason` | ErrorCode | Meaning | What to do |
|---|---|---|---|
| `NoWindow` | `PreconditionFailed` | Slate is not initialized, the target has no window, or the window has no native window yet | Wait until the window appears, then call again. If the target is inside a tab that is behind another tab (the check cannot always tell), waiting does not help: bring the tab to the front with `OpenTabById` (needs `EditorTabSpawn`) or ask the user |
| `Headless` | `NotAllowed` | Slate does not draw widgets in this process (no rendering device, a commandlet, a dedicated server). With no rendering device the message says so | Start the editor with a rendering device |
| `DebuggerPaused` | `NotAllowed` | A Blueprint debugger breakpoint has paused the game thread in the middle of a frame | Resume execution, then capture again |
| `NotInVisibleTree` | `NotAllowed` | There is no path from the window to the widget — the widget or an ancestor is collapsed or hidden | Make that part visible, then capture again |
| `BlockedByModal` | `NotAllowed` | A modal window is open, and only the modal window, its children, tooltips and notifications are drawn | Close the modal window, then capture again |
| `Minimized` | `NotAllowed` | The window, or an ancestor window that has to be drawn first, is minimized | Restore it. If it is the editor main window, call `SetEditorWindowState` with `State: Restored` (needs `EditorWindowStateControl`) or ask the user to restore it |
| `Hidden` | `NotAllowed` | The window, or an ancestor window, has a native window that is not visible. A window that was created but has never been shown is reported the same way, because the engine does not say which of the two it is | Show the window, or — right after startup — call again once it has been shown |
| `NotRenderable` | `PreconditionFailed` | The renderer has no viewport for the window, or the viewport has no size | Wait until the window has finished appearing, then call again |
| `InBackgroundTab` | `NotAllowed` | The target is inside a docked tab that is behind another tab, or inside an editor tab that is behind another one (for example the level editor viewport after a Blueprint editor was opened), so it is not drawn. The check runs right after `NoWindow` for Slate being uninitialized | Bring the tab to the front: `OpenTabById` (needs `EditorTabSpawn`; an open tab is brought forward together with its editor tab) or ask the user. `OpenTabById` takes both `TabId` and `OwnerTabId` — `OwnerTabId` is the editor tab that holds the target (`LevelEditor` for the level editor), and `ListSpawnableTabs` lists the valid combinations. Waiting does not change it. `CaptureEditorTabImage` does this itself |
| `WindowSizeMismatch` | `NotAllowed` | The size Slate holds for the window differs from the size the operating system reports for it, and the synchronization the capture tries before it takes anything did not fix it, so the capture would be a broken image. Every capture command compares the two sizes first. A minimized window is not compared; the check runs after `Minimized` / `Hidden` and before `NotRenderable` | For the editor main window, call `SetEditorWindowState` with `Minimized` and then `Restored` again (needs `EditorWindowStateControl`), then capture again; if it persists, ask the user to change the window size by hand. For any other window, ask the user to change its size |

- **`InBackgroundTab` is the exception to the table order**: it is checked after `Headless` and the Slate-not-initialized `NoWindow`, before the other window checks, and it is in the last rows only because it was added late. `WindowSizeMismatch` is checked after `Minimized` / `Hidden` and before `NotRenderable`.
- **`NoWindow` and `NotRenderable` answer `PreconditionFailed`**: the foundation is not there yet, and waiting fixes it. A scenario step with `RetryCount` retries it.
- **Every other `Reason` answers `NotAllowed`**: the state of an existing window forbids the capture. A scenario's `RetryCount` does **not** retry `NotAllowed`, so a step that used to be retried after a minimized window answered `ExecutionFailed` now fails at once. Change the state first, as the table says.
- A child window is not drawn when its parent is not, so a floating window whose parent is minimized or hidden is refused with the parent's state (`Minimized` or `Hidden`), even though the child itself is not minimized. When a modal window is open, only the modal window, its children, tooltips and notifications can be captured.
- A capture that was allowed but failed afterwards — the engine returned no image or an empty one, or the PNG could not be encoded — answers `ExecutionFailed` with no `Reason`; the message says which step failed.

**The game viewport commands refuse the same way.** `CaptureViewportImage` (`UAIP.Runtime.Observation`) checks that the game viewport will be drawn before it captures. When it will not be (the window that holds it is minimized or hidden, a modal window is open, and so on), it is refused without capturing, with the same `Reason`, error codes and `Result.Reason` as the table above. The message says what to do. A minimized window that is the editor main window (the Play In Editor window docked in it) is answered with the `SetEditorWindowState` remedy; for a separate PIE window or a standalone game, the message asks the user to restore that window. A capture that was allowed but failed afterwards stays `ExecutionFailed` with no `Reason`.

- **`CheckpointCapture` passes the refusal through.** It captures with `CaptureViewportImage` first, so when that is refused, the checkpoint is refused with the same `NotAllowed` or `PreconditionFailed` and copies the `Reason` into its own `Result.Reason`. The message is `CheckpointCapture: CaptureViewportImage failed: ` followed by the message of `CaptureViewportImage`. Every other failure of the two commands it is composed of stays `ExecutionFailed`.
- **The game viewport UI operations are refused by the state of the host window.** `ClickGameViewportWidget`, `PressGameViewportUIKey` and `TypeGameViewportText` check the window that hosts the game before they send anything, and answer with `Reason: HostWindowUnavailable`: `NoWindow` (the game viewport has no window yet) is `PreconditionFailed` (`The game viewport has no window yet. Retry after the game window has been created.`), while `Hidden` and `Minimized` are `NotAllowed` (`The window that hosts the game is not visible, so nothing in it is laid out.` / `The window that hosts the game is minimized, so nothing in it is laid out.`). A minimized window is `NotAllowed`, not `PreconditionFailed`, so a scenario's `RetryCount` does not retry it; restore the window first.

---

## UAIP.Editor.Execution

Run tests, Python scripts, and Editor Utility Blueprints.

| Command | Description |
|---|---|
| `DiscoverAutomationTests` | Load the automation test modules and return summary counts of discovered tests |
| `ListAutomationTests` | Return a filtered list of automation tests as a JSON artifact |
| `RunAutomationTest` | Run a UE Automation Test by name and return a per-test report (Pass / Fail / Skipped / Error / Cancelled; see [the report contract](#automation-test-report-contract)) |
| `RunAutomationSpec` | Run a UE Automation Spec by name and return a per-test report (same contract as `RunAutomationTest`) |
| `GetAutomationTestStatus` | Return the current automation test manager status (inline by default) |
| `StopAutomationTests` | Request cancellation of the running automation test batch |
| `RunEditorPythonScript` 🧩 | Run an inline Python script or a `.py` file (requires `PythonScriptPlugin`) |
| `RunEditorUtilityBlueprint` | Run a specified Editor Utility Blueprint |
| `RunNamedEditorCommand` | Run a named editor console command via `GUnrealEd->Exec` |

> **`RunEditorPythonScript` can interrupt a script that runs too long.** The optional `AbortAfterSeconds` parameter is an integer from `0` to `1800`. `0` means never interrupt; omitting it or passing `null` uses the ini default (`[UAIP.Python] DefaultAbortAfterSeconds`, itself `0` by default — see [Configuration](config.md#uaippython--default-abort-deadline-for-runeditorpythonscript)). Once the deadline passes, an exception is raised inside the script on the game thread, and raised again every second until the script stops.
>
> **This is best effort.** The exception arrives only between Python bytecode instructions, so a script blocked inside a native call (`time.sleep`, a long engine call) is interrupted only when that call returns. Edits made before the interruption **remain**. A script that catches the exception is not stopped — it is sent again every second — and the repeated exception can also interrupt the script's own cleanup. After the deadline the exception can reach other Python running on the same thread. Threads the script started are not stopped. The abort works only on Python 3.11 builds; on another version a call that asks for one is refused with `AbilityUnavailable`.
>
> **An interrupted call** answers `Timeout` with `Data.Aborted: true` and `Data.NotExecuted: false` (the script ran partially — check the editor state before running it again). `Data` carries `AbortAfterSeconds`, `AbortSource` (`Argument` or `Config`), `DeadlineExceeded`, `Aborted`, `AbortSignalsSent` and `ElapsedSeconds`, plus `NotExecuted`, `AbortDrainFailed` and `AbortInjectionFailed` when they apply. An explicit `0` in the argument answers with only `AbortAfterSeconds` and `AbortSource`; a `0` that came from the ini adds no `Data` at all.
>
> **Refusals:** a call made from inside another Python execution on the game thread is `NotAllowed`; before Python has initialized, or while it is shutting down, it is `PreconditionFailed`.
>
> **Recommendations:** keep the call's `TimeoutSeconds` (how long the MCP / HTTP request waits) longer than `AbortAfterSeconds`, or the request gives up before the script's answer arrives. Pass `0` explicitly while debugging Python. `TimeoutSec` is accepted but has no effect — use `AbortAfterSeconds` to cut a script short.

> **Note**: `RunAutomationTest` (and its runtime counterpart `RunRuntimeAutomationTest`) runs **every matching test** when `RunAllMatching=true`, which is the default. To bound the run, pass `MaxMatchingTests` (1 or greater; omit it for no bound). `0` is rejected rather than read as "no bound" — they are opposite requests, and quietly turning one into the other is how a bounded run starts claiming full coverage.
>
> The report always carries `Summary.Matched` (how many tests matched the filter) and `Summary.Selected` (how many were actually run). **Both are stated whether or not they differ** — a line that appears only on truncation is one the reader has to already know about, since its absence would otherwise be indistinguishable from a build that never emitted it. The human-readable report and the Output Log carry the same pair.
>
> `TimeoutSec` bounds **each individual test**, not the batch (60 seconds by default). A larger match set still runs in full as long as every test finishes within that time. Separately, the runtime `RunRuntimeAutomationTest` bounds the whole bulk run at 600 seconds of wall clock; reaching it adds a `(bulk execution time limit reached)` entry to the report as an `Error`.
>
> **Changed in v1.1.0**: earlier releases stopped at a hundred matches and **gave the caller no way to tell** — `Pass=100 Fail=0` reads exactly like a clean run over the whole set. If you relied on that ceiling, pass `MaxMatchingTests=100` explicitly.

> **Changed in v1.2.0**: `RunAutomationSpec` now declares a parameter schema and rejects anything outside it — it accepts `TestName` (required), `TimeoutSec`, `RunAllMatching`, and `MaxMatchingTests` (the same four keys `RunAutomationTest` reads, since both share a parser), with `AdditionalProperties: false`. **A call naming `SpecName`, or any other key outside this set, now fails with `InvalidParams` instead of being silently ignored** — earlier releases declared no schema at all, so an unrecognized key passed through unchecked and simply had no effect. `RunAllMatching` and `MaxMatchingTests` are accepted for schema symmetry with `RunAutomationTest`, but have **no effect on a Spec run**: `Execute()` always forces a single exact-name match regardless of what either parameter is set to.

#### Automation test report contract

`RunAutomationTest`, `RunAutomationSpec` and `RunRuntimeAutomationTest` return the same report shape.

**Each `Tests[]` entry** carries `Name`, `Result` and `TimeSec`, plus three message lists that are written **only when non-empty**, in this order: `FailMessages`, `SkipMessages`, `WarningMessages`.

**`Result` is one of five values:**

| Value | Meaning |
|---|---|
| `Pass` | The test succeeded and wrote no skip line |
| `Fail` | The test recorded at least one error. The errors are in `FailMessages` |
| `Skipped` | The test succeeded and wrote at least one skip line (`TEST-SKIP[<Reason>]: <Detail>`). The lines are in `SkipMessages` |
| `Error` | The test failed without recording any error (or the runner could not run it, for example on a timeout). When the test recorded no error, `FailMessages` holds a synthesized message, `The test reported failure without recording an error.`, so a failed result always carries a reason |
| `Cancelled` | The test was cancelled before it finished |

A test that recorded an error is `Fail` even when one of its messages looks like a skip line. Warnings never change `Result`: they go to `WarningMessages` and do not fail the test.

**`Summary`** counts `Pass`, `Fail` (both `Fail` and `Error` results), `Skip` (the `Skipped` results) and `Cancelled`, together with `Matched`, `Selected` and `TotalTimeSec`. A skipped test is counted in `Summary.Skip`, **not** in `Summary.Pass`.

**The log artifact** lists each test's entries in the order `FAIL:` (from `FailMessages`), `SKIP:` (from `SkipMessages`), `WARN:` (from `WarningMessages`), then `LOG:` (other output).

**`ReportErrors`** at the root of the report holds problems of the whole run that belong to no single test. It is written only when there is at least one, and its entries are not counted in `Summary`.

---

## UAIP.Editor.UIAutomation

Drive the editor UI — click, type, select, drag.

| Command | Description |
|---|---|
| 🆓 `ClickWidget` | Simulate a left click on a widget identified by the `WidgetRef` that `SnapshotUI` returns |
| 🆓 `SelectMenuItem` | Open and select a menu item by slash-separated label path |
| 🆓 `InputText` | Type text into a widget identified by the `WidgetRef` that `SnapshotUI` returns |
| 🆓 `SetCheckboxState` | Set the checked state of a checkbox |
| 🆓 `SetComboSelection` | Select a combo box item by label |
| 🆓 `DragGraphNode` | Drag a graph node by a pixel offset on a specified graph editor tab |
| 🆓 `ConnectGraphPins` | Connect two pins on a graph editor tab |
| 🆓 `AcceptDialog` | Accept the active modal dialog (click OK/Yes/Accept) |
| 🆓 `CancelDialog` | Cancel the active modal dialog (click Cancel/No) |
| 🆓 `InvokeContextMenuAction` | Right-click a target and execute an item from the context menu |
| 🆓 `HoverWidget` | Simulate OnMouseEnter on a widget |
| 🆓 `PressKey` | Simulate a key press with modifiers (blacklist for dangerous shortcuts) |
| 🆓 `WaitForWidget` | Poll until a widget, identified by a `WidgetRef` from `SnapshotUI`, reaches an expected state |
| 🆓 `FillForm` | Bulk-fill a form widget using a sequential state machine |
| 🆓 `SnapshotUI` | Capture a structured, scope-filterable snapshot of the UI and report what was left out |
| 🆓 `OpenPasswordTestWindow` | Open a small standalone test window holding a password `SEditableTextBox`, as a target for checking how `InputText` and the password-field policy treat a password field. It changes no asset, setting or saved state. It is in the demo build as well as Pro, because it only opens a window |

> **Note**: Commands that act on a widget take the `WidgetRef` that `SnapshotUI` returns, not a widget path. Call `SnapshotUI` first and pass the `WidgetRef` of the widget you want.
>
> **`SelectMenuItem`** takes one required parameter, `MenuPath`: a slash-separated list of menu labels, for example `Edit/Project Settings...`.
>
> - The first element is the menu name. Each later element matches a menu name or a display label, ignoring case, and must match it completely.
> - A label that contains `/` cannot be specified.
> - A label that contains `...` can be used, as in `Project Settings...`.
> - These are refused with `InvalidParams`: a segment that is only `..`, an empty segment, a control character, a path longer than 256 characters, and a path nested deeper than 10 levels.
>
> **`WaitForWidget`** takes `WidgetRef` (required) and `ExpectedState` (required; one of `Exists`, `Absent`, `Visible`, `Hidden`, `Enabled`, `Disabled`, `Focused`). `WaitTimeoutSeconds` is optional (default 5.0, at most 30). `PollIntervalSeconds` (default 0.1, at least 0.05) and `ConfirmTickCount` (default 3, at most 10) are also optional.

> **Note — input path and `PartialDelivery`.** `ClickWidget`, `HoverWidget`, `PressKey`, `AcceptDialog`, `CancelDialog`, `SetComboSelection` and `FillForm` now build their input the same way the runtime UI commands ([`ClickGameViewportWidget`](#game-viewport-ui-input-3) and the others) do. Their parameters, errors and refusal conditions (menus, modals) are unchanged, and `HoverWidget` still succeeds as before: it checks afterwards that the hover took hold and only logs the result. Because the hover, combo and key input now reach the widget as the real mouse and keyboard user, a UI that sorts input by user number may respond where it did not before. The combo operation of `SetComboSelection` and `FillForm` now moves the cursor first and checks that the target (or something inside it) is under the cursor before pressing; if something covers it, that field fails before anything is pressed.
>
> One behaviour changes. When the press of `ClickWidget`, `AcceptDialog` or `CancelDialog` itself opens a modal window, the release used to be delivered after the modal had been closed, after the response was sent. It is no longer sent: the response reports the press as delivered with `ModalOpened` and `PartialDelivery: DownOnly`, the same as a click on the game viewport UI.
>

> **Note**: `SnapshotUI` takes an optional scope — `RootWidgetRef` or `RootWidgetPath` (mutually exclusive; neither combines with `WindowTitle`) to pick a starting widget, `MaxDepth` (default 30) and `MaxNodes` (default 50000, shared across every root the call visits) to bound the walk, `WidgetTypes` + `WidgetTypeMode` (`"Add"` layers extra types on top of the usual roster, `"Only"` restricts to just the listed types) and `LabelContains` to filter, and `bIncludeInvisible` / `bIncludeUnclassified` to opt into widgets the default scan skips. The response always carries `EmittedCount`, `FilteredCount`, `FilteredReasons` (six reason keys present even at zero — `InvisibleSubtreeRoot`, `StructuralContainer`, `TypeFilterMismatch`, `LabelFilterMismatch`, `Unclassified`, `RegistrationFailed`), `UnclassifiedTypes` (up to 200 entries of `Type` + `Count`, sorted by count then name — each `Type` can be passed straight back into `WidgetTypes`), `Traversal` (`Complete` / `NodeLimitReached` / `DepthLimitReached` / `VisitedNodeCount`), `MatchedRootCount`, and `EffectiveParams` (the clamped/normalized values actually applied).
>
> A response can only ever say "not in the set that passed the current filters." Reading that as "does not exist anywhere in the UI" requires all of: the walk was not cut off (`Traversal.Complete == true`); the unclassified-type list is complete and every entry is addressable (`UnclassifiedTypesComplete == true` and `UnaddressableUnclassifiedCount == 0`); invisible widgets were not pruned (`FilteredReasons.InvisibleSubtreeRoot == 0`, or `bIncludeInvisible` was set); `WidgetTypeMode` was `"Add"` (no type restriction); `LabelContains` was empty; no widget failed ref registration (`FilteredReasons.RegistrationFailed == 0`); and no `WindowTitle` / `RootWidgetRef` / `RootWidgetPath` scoped the call (otherwise the conclusion only holds within that scope). Even when all of those hold, a **structural container** type (below) never appears in `Widgets` or `UnclassifiedTypes` — name it explicitly via `WidgetTypes` to check for one.
>
> Structural containers — widgets that exist purely to compose layout — are traversed but never emitted and never listed as an unclassified type; they are folded into `FilteredReasons.StructuralContainer` instead: `SBox`, `SBorder`, `SOverlay`, `SSpacer`, `SConstraintCanvas`, `SHorizontalBox`, `SVerticalBox`, `SGridPanel`, `SWrapBox`, `SWidgetSwitcher`, `SCanvas`, `SScaleBox`, `SSizeBox`, `SNullWidget`, `SInvalidationPanel`, `SRetainerWidget`. Naming one of these in `WidgetTypes` still emits it — an explicit type name always wins over classification.
>
> Type names come from `SWidget::GetTypeAsString()` — the identifier passed to `SNew(...)` at the widget's construction site, not a dynamic type. A widget built as `SNew(TBaseClass)` reports the base class name even where the concrete type differs, and a widget constructed without `SNew` (e.g. `MakeShared<SFoo>()`) reports the literal type name `"None"`.
>
> `RootWidgetRef` is single-use: once the call completes, **every** `WidgetRef` from that session is invalidated, not just the one passed in — each `SnapshotUI` call starts a fresh generation. Use `RootWidgetPath` instead when narrowing down step by step while keeping earlier refs alive. `SnapshotUI` still declares `IsReadOnly() == true` and runs under `bReadOnly`; only the UAIP-side ref cache is reset, no persistent editor state changes. Every `WidgetRef` — from any UI Automation command — expires 60 seconds after the snapshot that produced it.

### Toolset bridges — SlateInspector (10) 🧩

Bridge commands via the `SlateInspectorToolset` (UE 5.8+). Provider: `Toolset.Editor.SlateInspector.*`. Widgets are addressed by refPath, whereas the native commands address a widget by the `WidgetRef` that `SnapshotUI` returns. Every bridge command in this section now requires the same capability as its native counterpart (see [Safety & Capabilities](safety.md)) — earlier releases dispatched these without a capability check.

| Command | Description |
|---|---|
| `Toolset.Editor.SlateInspector.SnapshotUI` | Snapshot the widget tree at the given ref |
| `Toolset.Editor.SlateInspector.ObserveWidget` | ⚠️ **Not callable** — no delegation target exists. See the note below |
| `Toolset.Editor.SlateInspector.UnobserveWidget` | ⚠️ **Not callable** — no delegation target exists. See the note below |
| `Toolset.Editor.SlateInspector.ListObservers` | List every currently active widget observer |
| `Toolset.Editor.SlateInspector.ClickWidget` | Simulate a mouse click on the widget at the given ref |
| `Toolset.Editor.SlateInspector.HoverWidget` | Move the cursor over the widget at the given ref |
| `Toolset.Editor.SlateInspector.InputText` | Type text into the widget at the given ref |
| `Toolset.Editor.SlateInspector.PressKey` | Send a key press; modifier prefixes are supported (e.g. `Ctrl+S`) |
| `Toolset.Editor.SlateInspector.SetComboSelection` | Select an option in a combo box widget |
| `Toolset.Editor.SlateInspector.FillForm` | Fill multiple form fields in a single call |

> **Note**: `Toolset.Editor.SlateInspector.PressKey` applies the same blocked-shortcut list as the native `PressKey` command, but it has no way to resolve which widget currently has focus, so it blocks **Backspace unconditionally** — the native command's exemption for a focused text-input widget does not carry over to the bridge.

> **⚠️ Breaking change — none of the 10 commands in this section worked until now.** They passed the toolset name **unqualified, as `SlateInspectorToolset`**, and the ToolsetRegistry resolves a call with one exact lookup and no fallback of any kind (no prefix match, no suffix match), so nothing matched the registered `SlateInspectorToolset.SlateInspectorToolset` and every command failed at run time with "no such toolset". **Eight of them now work**: `SnapshotUI`, `ListObservers`, `ClickWidget`, `HoverWidget`, `InputText`, `PressKey`, `SetComboSelection` and `FillForm`.
>
> The remaining two, `ObserveWidget` and `UnobserveWidget`, **do not reach a target even with the name corrected**. The toolset declares `Observe` and `Unobserve`, whose parameters differ: `Observe` takes a widget ref and a traversal depth rather than the observer name this command accepts, and `Unobserve` cancels an observer by the identifier `Observe` returned — an identifier a caller of this bridge never receives. Pointing them at the nearest name would make them reach something and do the wrong thing, so both report `Available: false` with `UnavailableDetail: "DelegationTargetMissing"`. For `ObserveWidget`, use **`UAIP.Editor.Observation.ObserveWidget`**, which performs the same operation natively. `UnobserveWidget` has no native counterpart.

---

## UAIP.Editor.Assets

Open, search, create, duplicate, rename, delete assets and folders.

| Command | Description |
|---|---|
| `OpenAsset` | Open the specified asset in its editor. The editor-state artifact names the asset whose editor has focus as `ActiveAssetPath`. ⚠️ **Deprecated field:** the same artifact's `ActiveTabId` holds that asset path too — not the Slate layout identifier `DumpEditorState` reports under the same name — and switches to the layout identifier in the next major version. Read `ActiveAssetPath` instead; the artifact's `DeprecatedFields` array states this in machine-readable form. Start the editor with `-uaip-active-tab-id-as-layout-id` to try the new meaning now (provided for the 1.x releases only) |
| `CloseAsset` | Close all editors for the specified asset |
| `SaveAsset` | Write only the named assets to disk (requires `AssetMutate`). Shows no dialog, so it completes unattended |
| 🆓 `ListDirtyPackages` | List the packages holding unsaved changes (pre-flight check before saving) |
| 🆓 `SearchAssets` | Search assets by path / class / tag |
| `CreateAsset` | Create a new asset of the specified class. Fails with `InvalidParams` when an asset already exists at `AssetPath` (saved or not, of any class): nothing is created, the existing asset is not touched, and no overwrite dialog appears — delete it first or pick another path. When the registry knows the existing asset, the response `Result` carries its class as `ExistingClassName`. If the factory produced an asset of a different class than `ClassName`, or the asset-type-specific post-processing fails, the asset just created is discarded before the error is returned; if it cannot be discarded, the error says so and `Result.RemainingAssetPath` names where it remains. The generic Blueprint factory, which ignores the requested kind and always makes a plain Blueprint, is not a candidate for specific Blueprint kinds (it is still used for `/Script/Engine.Blueprint` itself). Two requests that name `/Script/Engine.Blueprint` are refused with `InvalidParams` before anything is created, because that factory would otherwise produce a different kind of asset without the checks that kind has: a `FactoryParams.ParentClass` that the engine maps to a dedicated Blueprint kind (an Animation Instance subclass becomes an Animation Blueprint, a User Widget subclass a Widget Blueprint, and so on) is answered with the class to use instead, in the message and as `Result.RequiredClassName` (for example `/Script/Engine.AnimBlueprint`; `ListFactoriesForClass` lists the factories for that class and the `FactoryParams` they accept); and a `ParentClass` that derives from `UControlRig` is answered with a message naming the Control Rig class to use (no `Result.RequiredClassName`). A parent that needs no dedicated kind, such as an Actor, and an omitted `ParentClass` are created as before. For Control Rig see [Control Rig asset formats](#control-rig-asset-formats) |
| 🆓 `ListCreatableAssetClasses` | Return every UClass that `CreateAsset` can target, with factory count and default factory (heavy call) |
| 🆓 `ListFactoriesForClass` | Return the factory candidates for a `ClassName`, each with its `FactoryParams` schema. The generic Blueprint factory is no longer listed for specific Blueprint kinds (see `CreateAsset`) |
| `DuplicateAsset` | Duplicate an existing asset |
| `CopyAsset` | Copy an asset to a new full package path (fails if the destination exists; requires `AssetCreate`) |
| `RenameAsset` | Rename / move an asset to another path. Refused with `PolicyViolation` while `DisableSave` is in force |
| `MoveAsset` | Move an asset to another folder keeping its name; reports whether a redirector was left behind (requires `AssetMutate`). Refused with `PolicyViolation` while `DisableSave` is in force |
| `DeleteAsset` | Delete an asset. Refused with `PolicyViolation` while `DisableSave` is in force |
| `CreateFolder` | Create a new folder in the Content Browser |
| `DeleteFolder` | Delete an empty folder (returns `NotEmpty` if not empty). Refused with `PolicyViolation` while `DisableSave` is in force |
| `ForceDeleteFolder` | Delete a folder and its assets (max 50 items, no external-reference check). Refused with `PolicyViolation` while `DisableSave` is in force |
| `MoveFolder` | Move every asset in a folder to a destination folder, preserving sub-folders; partial failures are listed in `FailedAssets` (requires `AssetFolderRefactor`). Refused with `PolicyViolation` while `DisableSave` is in force |
| 🆓 `GetSelectedAssets` | Return the assets currently selected in the Content Browser |
| `SelectAssets` | Select the specified assets in the Content Browser (requires `ContentBrowserNavigate`) |
| 🆓 `GetContentBrowserPath` | Return the current folder path shown in the Content Browser |
| `SetContentBrowserPath` | Navigate the Content Browser to a specified folder (requires `ContentBrowserNavigate`) |
| 🆓 `GetOpenAssets` | Return the list of assets currently open in an asset editor |
| 🆓 `ListAssetRedirectors` | List asset redirectors under a folder (`/Game` project-wide by default) with source/destination paths, without loading any assets |
| `FixAssetRedirectors` (requires `RedirectorFixup`) | Fix up and delete all resolvable asset redirectors under `/Game` (project-wide, recursive, always). Refused with `PolicyViolation` while `DisableSave` is in force |
| `FixUpRedirectorsInFolder` (requires `RedirectorFixup`) | Same fix-up limited to one folder; unresolved entries are returned in `FailedRedirectors`. Refused with `PolicyViolation` while `DisableSave` is in force |
| 🆓 `GetAssetReferences` | Traverse the asset reference graph (referencers, dependencies, or both) rooted at an asset up to a given depth |
| 🆓 `GetAssetSizeMap` | Aggregate per-asset disk (and optionally resident memory) size under a folder, sorted descending |
| 🆓 `GetAssetSizeMapByClass` | Aggregate disk size per asset class under a folder, sorted descending |
| 🆓 `FindUnreferencedAssets` | ⚠️ **Deprecated** — use `StartAssetAudit` instead. Find assets under a folder with no user (non-Engine/Script) referencers (hard-reference heuristic); behavior and progress firing are unchanged |
| 🆓 `FindCircularReferences` | ⚠️ **Deprecated** — use `StartAssetAudit` instead. Find circular dependency chains among assets under a folder; behavior and progress firing are unchanged |
| 🆓 `FindBrokenReferences` | ⚠️ **Deprecated** — use `StartAssetAudit` instead. Find dependencies pointing at packages no longer registered in the asset registry; behavior and progress firing are unchanged |
| 🆓 `GetAssetDependencyPath` | Find the shortest dependency or referencer path between two assets |
| 🆓 `RunAssetAudit` | ⚠️ **Deprecated** — use `StartAssetAudit` instead. Run a composite audit (unreferenced assets, circular references, broken references, largest assets) under a folder; behavior and progress firing are unchanged. Runs synchronously and occupies the game thread until it completes — on a large project this can freeze the editor, and every other UAIP command, for tens of seconds to minutes |
| 🆓 `StartAssetAudit` | Start an asset audit job and return an `AuditId` immediately; the scan then advances a little at a time between editor frames instead of blocking the game thread, so the editor and other UAIP commands stay responsive while it runs. Params: `PackagePath` (required), `Recursive` (default `true`), `Reports` (array of `UnreferencedAssets` / `CircularReferences` / `BrokenReferences` / `TopLargestAssets`; default: all four — an explicit empty array is rejected with `InvalidParams`), `MaxUnreferenced` (default `200`, range `[1, 2000]`), `MaxCycles` / `MaxBroken` / `MaxTopLargest` (same defaults as `RunAssetAudit`). Rejected with `TooManyRequests` while another audit job is already running, and with `NotAllowed` while the editor is showing a modal dialog or a slow-task progress bar. **Requires an explicit `SessionId`** — an anonymous session (auto-generated by the transport) is rejected with `InvalidParams`, since a job started anonymously could never be polled or retrieved afterward |
| 🆓 `GetAssetAuditStatus` | Poll an audit job by `AuditId` — returns `State` (`Preparing` / `Running` / `Completed` / `Failed`), the report currently being scanned, processed/total item counts, elapsed seconds, and a failure reason if the job failed. Cost does not scale with job size (O(1)). **Requires the same `SessionId`** used to start the job; an unknown, expired, or other-session `AuditId` all return `NotFound` without distinguishing which case it is |
| 🆓 `GetAssetAuditResult` | Retrieve the artifact references produced by a completed audit job by `AuditId`, optionally narrowed to a subset of `Reports` (defaults to every report requested at start; requesting a report that was not part of the original job is reported back as unavailable rather than an error). O(1). Returns `ExecutionFailed` with the current `State` if the job has not reached `Completed` yet. **Requires the same `SessionId`** used to start the job |
| 🆓 `ListPrimaryAssetTypes` | List all registered `PrimaryAssetType`s (`UAssetManager`) with class/directory/asset-count summary |
| 🆓 `GetPrimaryAssetTypeInfo` | Get the full detail (directories, specific assets, default rules) of a single `PrimaryAssetType` |
| 🆓 `ListPrimaryAssets` | List the `PrimaryAssetId`s and assets belonging to a `PrimaryAssetType` |
| 🆓 `GetAssetBundle` | Get the `AssetBundle` entries of a `PrimaryAssetId` (empty array when none are defined) |
| 🆓 `GetAssetTags` | Get the Asset Registry tag map of an asset |
| 🆓 `GetPrimaryAssetIdForPath` | Resolve an asset path to its `PrimaryAssetId` (`Found:false`, not an error, when unmanaged) |
| 🆓 `GetPrimaryAssetRules` | Get the merged (type default + per-asset override) `PrimaryAssetRules` of a `PrimaryAssetId` |
| 🆓 `GetManagedPackageList` | Get the packages managed by a `PrimaryAssetId` |
| 🆓 `GetPrimaryAssetLoadList` | Resolve the object paths that would actually load for a `PrimaryAssetId` under given bundle conditions |
| 🆓 `GetLoadedPrimaryAssets` | Get the currently loaded / pending `PrimaryAssetId`s and their loaded bundle state |
| `AddPrimaryAssetType` (requires `PrimaryAssetTypeAdd`) | Add a `PrimaryAssetType` to `PrimaryAssetTypesToScan` (persisted to `DefaultGame.ini`) and scan it immediately |
| `RemovePrimaryAssetType` (requires `PrimaryAssetTypeRemove`) | Remove a `PrimaryAssetType` from `PrimaryAssetTypesToScan` (persisted); rejects if assets exist unless `Force` |
| `SetPrimaryAssetRules` (requires `PrimaryAssetRulesOverride`) | Temporarily override a `PrimaryAssetId`'s rules in memory only (not persisted) |
| `LoadPrimaryAsset` (requires `PrimaryAssetLoad`) | Explicitly load `PrimaryAsset`s into memory (non-blocking, allowed during PIE) |
| `UnloadPrimaryAsset` (requires `PrimaryAssetUnload`) | Explicitly unload `PrimaryAsset`s from memory (rejected during PIE) |

> **A folder parameter accepts the content root itself.** `SearchAssets`, `ListAssetRedirectors`, `GetAssetSizeMap`, `GetAssetSizeMapByClass`, `StartAssetAudit`, `RunAssetAudit`, `FindUnreferencedAssets`, `FindCircularReferences` and `FindBrokenReferences` take `/Game` (or the content root of a plugin, such as `/MyPlugin`) as `PackagePath` / `FolderPath` just as they take `/Game/` or a folder beneath it. A trailing `/` is dropped, so the folder is handled — and, for `ListAssetRedirectors`, echoed back in `FolderPath` — without it. A path that is neither a mounted root nor beneath one, or an empty string, is `InvalidParams`, and the message names the parameter and the value it was given (`'PackagePath' value '…': <reason>`). `StartValidationJob` accepts a content root in `PackagePath` the same way. Commands that expect a single asset path are unchanged: a bare root is still refused there.
>
> **The Content Browser commands report whether the Content Browser is there.** `GetSelectedAssets`, `SelectAssets`, `GetContentBrowserPath` and `SetContentBrowserPath` are listed as unavailable (`Available: false`, `UnavailableReason: HandlerUnavailable`, `UnavailableDetail: ExecutionEnvironment`) when the Content Browser module is not loaded, so the absence is visible before the call. Before, they were listed as available and refused the call. The Toolset bridge counterparts (`Toolset.Editor.Toolset.Assets.GetContentBrowserPath` and so on) are not affected; their availability follows the Toolset integration.

> **Note**: `StartAssetAudit` is a **job-style command** — it returns immediately and the work continues across editor frames rather than blocking the call. If your `uaip_execute` call includes an MCP `_meta.progressToken`, the bridge sends a `notifications/progress` update roughly every 5 seconds while the call is pending, carrying only the elapsed time and the editor's own state (`STARTING` / `RUNNING` / `UNRESPONSIVE`) — it never carries the job's internal progress; poll `GetAssetAuditStatus` for that. This applies to `uaip_execute` only (not `uaip_run_scenario`), only when the client sends a progress token, and whether the notification is actually surfaced to you depends on the MCP client. The per-frame time budget the audit job spends on each scan step is configurable via `Config/DefaultUAIP.ini` → `[UAIP.Jobs] AuditStepBudgetMs` (default `10.0`, clamped to `[1.0, 100.0]`; a value outside that range is silently clamped rather than rejected).


> **Note**: There are two ways to save, and they differ in blast radius. `SaveAllPackages` writes **every** package holding unsaved changes, so work a person left in progress is committed alongside yours. When you know what you changed, name it with `SaveAsset` instead. To find out what a save would write, call `ListDirtyPackages` first: it reads the same source the editor-wide save consults (`GetDirtyContentPackages` / `GetDirtyWorldPackages`), so its list and the set `SaveAllPackages` would write are the same.
>
> `SaveAsset` only ever writes packages that are **loaded and dirty**. An asset that was never loaded cannot hold unsaved changes, so it is returned under `Skipped` with `Reason: "NotLoaded"` rather than being loaded just to write it back; one that is already saved comes back as `NotDirty`. Neither is an error. Paths under `/Engine/` and `/Script/` are refused as `Failed` with `WriteForbidden` because they reach outside the project, but the call itself still succeeds and the remaining assets are saved. Only `DisableSave=True` in the safety policy rejects the whole call, with `PolicyViolation`.
>
> **Relationship to `ApplyValidationFix`**: when a validator wraps its fix in `FAutoSavingFixer`, applying it through UAIP does **not** write to disk. The engine performs that auto-save through a modal confirmation dialog, which cannot complete when nobody is there to answer it. `ApplyValidationFix` reports `Applied: true` together with `AssetSaved: false` in that case, so **treat `AssetSaved: false` as the signal to persist the change yourself with `SaveAsset`**.

> **Note — a class named in `FactoryParams` can need a capability of its own.** Some domains admit a class named there through the same policy that gates their editing commands — StateTree's `FactoryParams.SchemaClass` and ControlRig's `FactoryParams.ParentClass` today. Blueprint's own `FactoryParams.ParentClass` (optional, defaults to `AActor`) and Anim Blueprint's `FactoryParams.TargetSkeleton` (required) are **not** gated this way and need no capability beyond `AssetCreate`. Neither is loaded on demand any more: a class that is not already in memory is refused rather than loaded in order to decide whether the caller was allowed to name it. When the session does not hold what the named class requires, `CreateAsset` answers **`CapabilityNotAvailable`**, with the missing capability names in the message — the same as everywhere else — see [Capability-gated custom types](#capability-gated-custom-types).

### Toolset bridges — Assets (6) 🧩

Bridge commands via the `EditorAppToolset` (UE 5.8+, EditorToolset plugin). Provider: `Toolset.Editor.Toolset.Assets.*`.

| Command | Description |
|---|---|
| `Toolset.Editor.Toolset.Assets.GetSelectedAssets` | Get currently selected assets in the Content Browser |
| `Toolset.Editor.Toolset.Assets.SelectAssets` | Select assets in the Content Browser (requires `ContentBrowserNavigate`) |
| `Toolset.Editor.Toolset.Assets.GetContentBrowserPath` | Get the current Content Browser folder path |
| `Toolset.Editor.Toolset.Assets.SetContentBrowserPath` | Navigate the Content Browser to a folder (requires `ContentBrowserNavigate`) |
| `Toolset.Editor.Toolset.Assets.OpenEditorForAsset` | Open an asset in its editor (requires `AssetWindowControl`) |
| `Toolset.Editor.Toolset.Assets.GetOpenAssets` | List assets currently open in an asset editor |

---

## UAIP.Editor.SemanticSearch 🧩

Semantic asset search and index management. Requires the `SemanticSearch` plugin (UE 5.8+, Experimental) and an OpenAI API key configured in Editor Preferences → Plugins → Semantic Search.

| Command | Description |
|---|---|
| `Search` | Search project assets by natural-language query (hybrid BM25+vector, up to 500 results) |
| `FindSimilar` | Find assets similar to a reference asset via vector similarity |
| `GetIndexStats` | Return current index statistics (asset count, last-built timestamp) |
| `StartIndexing` | Trigger a full semantic index rebuild (long-running; requires `SemanticSearchEdit`) |
| `CancelIndexing` | Cancel an in-progress index build (requires `SemanticSearchEdit`) |

### Toolset bridges (2) 🧩

Bridge commands via the `SemanticSearchToolset` plugin (UE 5.8+). Provider: `Toolset.Editor.SemanticSearch.*`. These commands mirror the native `Search` and `FindSimilar` above and are provided exclusively as a Toolset bridge (no UAIP native equivalent for these two Toolset-side commands; see ADR `2026-06-25-SemanticSearchToolset-BridgeOnly-Exception.md`).

| Command | Description |
|---|---|
| `Toolset.Editor.SemanticSearch.Search` | Hybrid BM25+vector search via SemanticSearchToolset |
| `Toolset.Editor.SemanticSearch.FindSimilar` | Vector similarity search via SemanticSearchToolset |

---

## UAIP.Editor.Level

Editor-side actor placement, transforms, and level loading.

| Command | Description |
|---|---|
| 🆓 `ListLevelActors` | List all actors in the open level |
| `PlaceActorInLevel` | Place an actor in the editor level |
| `DeleteActorFromLevel` | Remove an actor from the editor level |
| 🆓 `GetActorTransform` | Get the transform of an editor actor |
| `SetActorTransform` | Set the transform of an editor actor |
| `OpenLevel` | Open a level in the editor viewport (File > Open Level) |
| `NewLevel` | Create a new level from a template (EmptyLevel / EmptyOpenWorld / Basic / OpenWorld) |
| `SelectActors` | Select the specified actors in the editor level (replace or add to current selection) |
| 🆓 `ListSelectedActors` | Return a list of actors currently selected in the editor |
| `ClearSelection` | Clear the current selection in the editor level |
| `FocusOnActors` | Focus the viewport camera on the specified actors (omit to use the current selection) |
| 🆓 `GetCameraTransform` | Get the camera location and rotation of the active level editor viewport |
| `SetCameraTransform` | Set the camera location and rotation of the active level editor viewport |
| 🆓 `GetVisibleActors` | Return actors currently visible in the active editor viewport (frustum culling) |
| 🆓 `ProjectWorldToScreen` | Project a world-space position to screen coordinates |
| 🆓 `ProjectScreenToWorld` | Cast a ray from screen coordinates into the world (ECC_Visibility line trace) |
| 🆓 `ListActorComponents` | List every component of an actor placed in the level. Each entry carries the `ComponentId` the three commands below take, plus `ComponentClassPath`, `Origin` (`Instance` / `SimpleConstructionScript` / `UserConstructionScript` / `Native`), `IsEditableInstance`, `IsSceneComponent`, `IsRootComponent`, `AttachParentComponentName` and `AttachSocketName`. Each entry also reports what **adding** a component of that class would take — `Admission` (`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`) with `RequiredCapabilities` and `MissingCapabilities` — which is how a caller learns about `ComponentCustomTypeEdit` before attempting a write. Reads the editor world, so it stays answerable during PIE. Requires `EditorInspect`. `ComponentId` is opaque and already escaped: pass it unchanged to the other component commands, and never build it or edit it by hand |
| `AddActorComponent` | Add a component to an actor placed in the level — what the Details panel's *Add Component* button does, as one undo step. Returns the new component's `ComponentId`. `ComponentName` may be omitted to let the engine generate one; `AttachParentComponentName` / `AttachSocketName` apply only to a `USceneComponent` subclass, and the new component becomes the root when the actor has none. The class is resolved against what is already loaded and is never loaded on request (an unloaded class is `NotFound`). Requires `ActorComponentEdit`, plus `ComponentCustomTypeEdit` for a class outside `/Script/Engine` and `/Script/LiveLinkComponents` — see [Capability-gated custom types](#capability-gated-custom-types). Refused during PIE |
| `DeleteActorComponent` | Remove an instance component from an actor placed in the level, as one undo step. Only `Origin: Instance` components can be removed — an SCS one belongs to the Blueprint component commands, a construction-script one is rebuilt by the script, and a native one exists on every instance of the class; each refusal names the route that does own it, and the actor's `DefaultSceneRoot` is refused too. Children of a removed scene component are re-attached to its parent, keeping their world transforms. `ExpectedComponentClass` is required (pass back the `ComponentClassPath` from the listing) so a stale identifier is refused with `NotFound` rather than followed. Requires `ActorComponentEdit`. Refused during PIE |
| `ReparentActorComponent` | Attach a scene component of a placed actor beneath a different component of the same actor, keeping its world transform, as one undo step. Both must be `USceneComponent` subclasses on that actor and the moved one must be `Origin: Instance`. There is no "attached to nothing" — detaching is expressed by naming the actor's root as `NewParentComponentName` — and the root itself cannot be moved. A cycle, or a socket the new parent does not have, is refused before anything is written. `ExpectedComponentClass` is required, same as above. Requires `ActorComponentEdit`. Refused during PIE |
| 🆓 `GetActorComponentProperty` | Read a property value from a component of an actor placed in the level, addressed by the `ComponentId` from `ListActorComponents` / `AddActorComponent` — `GetActorProperty` refuses a path that traverses the object reference an actor holds its components through, so this is the only way to reach one. Returns `Value`, `PropertyType`, `Origin`, and `WriteRequirements` — what a write of that property would additionally require beyond `ActorComponentEdit`, split into what this session already holds and what it is missing, plus whether the write is possible at all and which of `SetActorComponentProperty`'s two value parameters it must arrive in. `ExpectedComponentClass` is required, so a stale `ComponentId` is refused rather than followed. A component of any `Origin` can be read. Reads the editor world, so it stays answerable during PIE. Requires `EditorInspect`. The `ComponentId` is opaque and already escaped — pass it unchanged, as `ListActorComponents` returned it |
| `SetActorComponentProperty` | Write a property value onto a component of an actor placed in the level, addressed the same way as `GetActorComponentProperty`, as one undo step. The value arrives as UE import text in `Value` or as JSON in `ValueJson`, and `Operation` / `ElementIndex` / `ElementKeyJson` address a single container element instead of replacing the whole value — see [Writing references, structs and containers](#writing-references-structs-and-containers) for those parameters and the capabilities a reference or composite value additionally needs (call `GetActorComponentProperty` first to find out which). `ExpectedComponentClass` is required, same as above. Refused when the component's `Origin` is `UserConstructionScript`, since the next run of that script would discard the write. Requires `ActorComponentEdit`. Refused during PIE |

> **Note — instance components only.** These six commands operate on components of an actor **placed in the level** (`GetActorComponentProperty` can also read a component of any `Origin`, including one owned by the Blueprint's construction script — only writing to that one is refused). Components declared on the actor's Blueprint go through [UAIP.Editor.Blueprint — Components — SCS](#components--scs-8) instead. Renaming and duplicating an instance component have no counterpart here; add the component again under the name you want.

> **Note — writing `RestCollection` on a GeometryCollection component.** When `SetActorComponentProperty` writes `RestCollection` on a GeometryCollection component and the value actually changes, the write is committed through the engine's `SetRestCollection`, not by a plain property assignment. The asset's own defaults (damage settings and the like) are therefore taken into the component. Order matters: write `RestCollection` first and the damage settings after, and the settings you wrote stay; write them in the other order and the damage settings are overwritten by the asset's values. A write that does not change the value (writing the same asset again) does not take the defaults in.

### Toolset bridges — Level (8) 🧩

Bridge commands via the `EditorAppToolset` (UE 5.8+, EditorToolset plugin). Provider: `Toolset.Editor.Toolset.Level.*`.

| Command | Description |
|---|---|
| `Toolset.Editor.Toolset.Level.GetSelectedActors` | Return actors currently selected in the level editor viewport |
| `Toolset.Editor.Toolset.Level.SelectActors` | Select the specified actors in the level editor (requires `EditorActorEdit`) |
| `Toolset.Editor.Toolset.Level.GetCameraTransform` | Get the active viewport camera transform |
| `Toolset.Editor.Toolset.Level.SetCameraTransform` | Set the active viewport camera transform (requires `EditorViewportControl`) |
| `Toolset.Editor.Toolset.Level.FocusOnActors` | Focus the viewport on the specified actors (requires `EditorViewportControl`) |
| `Toolset.Editor.Toolset.Level.GetVisibleActors` | List actors visible in the active viewport |
| `Toolset.Editor.Toolset.Level.WorldPosToScreenCoords` | Project a world position to screen space |
| `Toolset.Editor.Toolset.Level.ScreenCoordsToWorld` | Project screen coordinates to world space (requires `EditorInspect`) |

---

## UAIP.Editor.Property

Read and write properties on actors, assets, Blueprint defaults, DataTable rows, World / Project settings. `Get*` commands mask secret-looking property values (name matches a secret pattern, has secret metadata, or is a file path type) with `***` — a compound value (e.g. a struct) containing a secret member is masked as a whole, not just the secret sub-field. `Set*` commands accept 17 struct types (vectors, rotators, transforms, colors, `FGuid`, intervals, `FGameplayTag` / `FGameplayTagContainer` / `FGameplayCueTag`, `FBoneReference`, …) and every integer width from `int8` through `uint64` in the text `Value`. Arrays, maps, sets, optionals, other structs and object references go in `ValueJson` instead, and a single container element can be addressed with `Operation` / `ElementIndex` / `ElementKeyJson` — see [Writing references, structs and containers](#writing-references-structs-and-containers) for those parameters and the two capabilities (`PropertyReferenceEdit` / `PropertyStructuredEdit`) that gate them.

| Command | Description |
|---|---|
| 🆓 `GetActorProperty` | Get a property value from an editor actor |
| `SetActorProperty` | Set a property on an editor actor |
| 🆓 `GetWorldSetting` | Get a WorldSettings property |
| `SetWorldSetting` | Set a WorldSettings property |
| 🆓 `GetAssetProperty` | Get a property from an asset (DataAsset etc.) |
| `SetAssetProperty` | Set a property on an asset and call `MarkPackageDirty` |
| 🆓 `GetBlueprintDefault` | Get a property from a Blueprint CDO |
| `SetBlueprintDefault` | Set a property on a Blueprint CDO |
| 🆓 `GetProjectSetting` | Get a property from a `UDeveloperSettings` CDO |
| `SetProjectSetting` | Set a property on a `UDeveloperSettings` CDO and call `SaveConfig()` |
| 🆓 `GetDataTableRow` | Get a DataTable row property |
| `SetDataTableRow` | Set a DataTable row property |

---

## UAIP.Editor.Blueprint

Edit Blueprint variables, event graph nodes, and SCS components.

### Asset creation (1)

| Command | Description |
|---|---|

### Variables & graph (11)

| Command | Description |
|---|---|
| `AddBlueprintVariable` | Add a member variable to a Blueprint (type, default, tooltip). A type that Blueprints cannot use as a variable type is refused with `InvalidParams`, using the same rule as the editor's variable type menu: a class needs `BlueprintType` (or `BlueprintSpawnableComponent`) on itself or an ancestor and must not be `NotBlueprintType`; a struct needs `BlueprintType` and must not be `BlueprintInternalUseOnly`. A refused call leaves the Blueprint unchanged (no variable is added and the asset is not marked dirty). The default is now validated once the variable's type has resolved, and a refused default **removes the variable again** rather than leaving it behind with an empty value. The default is engine text only — a reference or container default is refused whatever the session holds; set those afterwards with `SetBlueprintDefault`, which takes `ValueJson` |
| `DeleteBlueprintVariable` | Remove a member variable |
| `SetBlueprintVariableDefault` | Update a Blueprint variable's CDO default value |
| `AddGraphNode` | Add a node to any graph in a Blueprint asset (VariableGet/Set, FunctionCall, EventBeginPlay/EventTick, or `Event` to override any parent or interface event) — not just the event graph and function graphs. `GraphName` or `GraphGuid` selects the target; see the note below the table for graph selection, ambiguity, and the two-stage acceptance check |
| `AddFunctionOverride` | Override a parent class or interface function that returns a value, has output parameters or is const as a function graph, the way the Override menu does. Returns the graph and its entry / result node GUIDs |
| `DeleteGraphNode` | Delete a graph node by GUID (EntryNode / Tunnel cannot be deleted) |
| `ConnectBlueprintPins` | Connect two pins in a Blueprint graph |
| `DisconnectBlueprintPins` | Disconnect a pin connection |
| `ListBlueprintPins` | List pins of a Blueprint graph node |
| `SetPinDefaultValue` | Set a default value on a Blueprint graph node pin (auto-selects DefaultValue / DefaultObject / DefaultTextValue based on pin type) |
| `GetPinDefaultValue` | Get the current default value of a Blueprint graph node pin |

> **New — `AddGraphNode` with `NodeType: "Event"` overrides any event of the parent classes or of an implemented interface, named by `FunctionName`** (for example `ReceiveDestroyed` or `ReceiveActorBeginOverlap`), the way the Override menu of the My Blueprint panel adds an event node. `EventBeginPlay` and `EventTick` keep working as before. A Blueprint can override an event only once: when the override already exists anywhere in the Blueprint, the existing node is returned instead of a second one. A function that returns a value, has output parameters or is const cannot be an event node and is refused with `InvalidParams` naming `AddFunctionOverride`; a name that no parent class or interface declares as a `BlueprintImplementableEvent` / `BlueprintNativeEvent` is refused with `InvalidParams` as well.
>
> **New — `AddFunctionOverride` overrides such a function as a function graph** (for example `ACharacter::CanJumpInternal`). The graph gets the entry and result nodes of the parent's signature and a call to the parent implementation, and is compiled unless `SkipCompile` is `true`. The artifact reports `GraphName`, `GraphGuid`, `EntryNodeId`, `ResultNodeId` (absent when the function returns nothing), `OverriddenClass` and `AlreadyExisted`; wire the graph with `AddGraphNode` and `ConnectBlueprintPins`. Asking again returns the existing graph with `AlreadyExisted: true`. A function that can be an event node is refused with `InvalidParams` naming `AddGraphNode`, and so is one already overridden as an event node. Requires `BlueprintGraphEdit`.

> **`AddGraphNode` now looks at every graph in the asset, not just the event graph and function graphs.** Macros, interface-implementation graphs, and graphs nested inside a collapsed graph are now reachable by `GraphName` — previously naming one of those answered `NotFound` (before this change, `ExecutionFailed`) even though the graph existed.
>
> ⚠️ **Breaking change — `GraphName` matching is now case-insensitive.** It used to require an exact-case match; a name differing only in case now matches. If the asset holds two graphs whose names differ only in case, a call that used to succeed by matching the one graph with the exact case now hits both and is rejected as ambiguous (see below) instead of succeeding.
>
> **`GraphGuid` (optional string) selects a graph by `UEdGraph::GraphGuid` instead of by name, and is mutually exclusive with `GraphName`** — supplying both is `InvalidParams`. Omit it unless a prior call already rejected the same `GraphName` as ambiguous.
>
> **When `GraphName` matches more than one graph, nothing is added.** The command answers `InvalidParams` and `Result.MatchedGraphGuids` carries every candidate's `GraphGuid` as a string. Pass one of those values back as `GraphGuid` to target exactly one of them — no other formatting is needed. Empty `GraphName` and the literal `"EventGraph"` are unaffected: both still select the event graph directly and never enter this ambiguity check.
>
> **Two separate checks decide whether the node can go where `GraphName` / `GraphGuid` points, and only `AddGraphNode` runs them** — the other commands in this table do not, because they act on a node or pin that already exists rather than deciding where a new one may go:
> - *Does the graph accept edits at all?* An event dispatcher's own definition graph, a graph belonging to the interface asset itself (as opposed to a Blueprint that implements the interface — that one is editable), a math-expression graph, and graphs the editor generates internally all refuse with `NotAllowed`.
> - *Does this kind of node belong in this kind of graph?* A state machine's top-level graph (the one showing states and transitions) and a Blend Space graph refuse the combination with `InvalidParams` — the graph accepts editing in general, but not this node type. Passing the schema check here means the editor's own graph schema accepts the combination; it says nothing about whether the resulting graph makes sense at runtime (e.g. a generic node placed inside a state's pose-evaluation graph passes this check but may not do anything useful there).
>
> **Naming a graph that does not exist now answers `NotFound`** (previously `ExecutionFailed`) — repeating the same request cannot succeed, so a scenario's `RetryCount` no longer wastes a retry on it.

> ⚠️ **Breaking change — `ConnectBlueprintPins`, `DisconnectBlueprintPins`, `DeleteGraphNode`, `GetPinDefaultValue`, `ListBlueprintPins`, and `SetPinDefaultValue` now answer `NotFound` when the node or pin they were asked for does not exist** (previously `ExecutionFailed`). A scenario's `RetryCount` retries only `ExecutionFailed` and `PreconditionFailed`, so before this change a request naming a nonexistent `NodeId` or `PinName` was retried anyway, even though repeating it can never succeed.
>
> `GetPinDefaultValue` additionally had a defect fixed here: when `PinName` named no pin on the target node, the handler had no branch for that case at all and fell through to reading a pin that was never found, an unchecked access with undefined behavior. It now reports `NotFound` for a `PinName` that does not match any pin on the node, the same as the other commands in this list.

### Components — SCS (8)

| Command | Description |
|---|---|
| `ListBlueprintComponents` | List all components visible from a Blueprint (SCS, Inherited, Native) |
| `AddBlueprintComponent` | Add a new SCS component node to a Blueprint. ⚠️ Now additionally requires `ComponentCustomTypeEdit` for a project- or plugin-defined component class — see the note below |
| `DeleteBlueprintComponent` | Delete an SCS component from a Blueprint |
| `RenameBlueprintComponent` | Rename an SCS component |
| `ReparentBlueprintComponent` | Change an SCS component's parent. Naming a parent requires the component and the parent to each be a `USceneComponent` subclass; moving to the root level (an empty `NewParentVariableName`) works for any component class |
| `DuplicateBlueprintComponent` | Duplicate an SCS component. ⚠️ Now additionally requires `ComponentCustomTypeEdit` for a project- or plugin-defined component class — see the note below |
| `GetBlueprintComponentProperty` | Get a property value from an SCS component |
| `SetBlueprintComponentProperty` | Set a property on an SCS component. The value goes in `Value` as engine text or in `ValueJson` as JSON, and `Operation` / `ElementIndex` / `ElementKeyJson` address a single container element — see [Writing references, structs and containers](#writing-references-structs-and-containers) |

> ⚠️ **Breaking change — `AddBlueprintComponent` and `DuplicateBlueprintComponent` now gate the component class.**
>
> Every route that **increases how many instances of a component class exist** now asks the same question under the same capability name: the new instance-side `AddActorComponent`, and these two Blueprint / SCS commands. A component class declared by `/Script/Engine` or `/Script/LiveLinkComponents` is admitted on `BlueprintComponentEdit` alone, exactly as before. **Any other class — one your project's C++ declares, one another plugin declares (including engine plugins such as Niagara), or a Blueprint-generated component class — now additionally requires `ComponentCustomTypeEdit`**, and is refused with `CapabilityNotAvailable` naming it when the session does not hold it.
>
> **What this means on upgrade**: a session that used to add or duplicate a project-defined component with only `BlueprintComponentEdit` granted will start being refused. Add `+AllowedCapabilities=ComponentCustomTypeEdit` to `[UAIP.SafetyPolicy]` in `Config/DefaultUAIP.ini` to restore it — see [Safety & Capabilities](safety.md#level--actor--property-editing).
>
> **Why both routes**: gating only one of them leaves the other as a way to reach the same class. **Delete, rename, reparent and property writes are unaffected** — none of them increases the number of instances of a class, so none of them is gated by this. The requirement is decided from the class while the command runs, so it does not appear in either command's declared `RequiredCapabilities`; `ListActorComponents` reports per class what an add would take, and the refusal itself always names what is missing.

### Compile (2)

| Command | Description |
|---|---|
| `CompileBlueprint` | Compile a Blueprint and return CompileStatus + structured message log (AnimBlueprint / WidgetBlueprint not supported) |
| `GetBlueprintCompileStatus` | Read the current Blueprint compile status without triggering a compile |

---

## UAIP.Editor.UMG

Widget Blueprint editing — tree, variables, animation, bindings.

### Native (22)

| Command | Description |
|---|---|
| `CreateWidgetBlueprint` | Create a new Widget Blueprint asset |
| `AddWidget` | Add a widget to a Widget Blueprint's tree |
| `RemoveWidget` | Remove a widget from a Widget Blueprint's tree |
| `MoveWidget` | Reorder a widget within a panel or move it to another panel |
| `RenameWidget` | Rename a widget |
| `SetWidgetAsVariable` | Toggle a widget's `bIsVariable` flag |
| `SetNamedSlotContent` | Set the content of a NamedSlot widget |
| `GetNamedSlots` | List NamedSlots in a Widget Blueprint |
| `ReparentWidgetBlueprint` | Change a Widget Blueprint's parent class |
| `GetSlotProperties` | Get a widget's slot properties (JSON, CPF filter, max 64 keys), plus a `PropertyWriteRequirements` map saying what a write to each property would need and which input form it takes |
| `SetSlotProperties` | Set a widget's slot properties (32 KiB limit, `/Game/` UObject refs only). A reference now requires `WidgetSlotReferenceEdit` and a struct or container `PropertyStructuredEdit`, and those values are supplied as a JSON document rather than engine bracket text — read the property first for its `WriteInputForm`. A refused write leaves no undo entry and does not mark the asset dirty. A successful write compiles the Widget Blueprint so the change reaches widgets created at runtime; pass `bSkipCompile: true` to only mark it modified (the response then reports `bRequiresFollowupCompile: true`) and compile once with `CompileWidgetBlueprint` after a batch of edits |
| `GetWidgets` | Get the full widget tree structure (JSON) |
| `ListWidgetClasses` | List available widget classes (max 500) |
| `CompileWidgetBlueprint` | Compile a Widget Blueprint and return errors / warnings |
| `ListWidgetAnimations` | List animations in a Widget Blueprint |
| `GetWidgetAnimationInfo` | Get track / key info of an animation |
| `CreateWidgetAnimation` | Create a new animation in a Widget Blueprint |
| `AddAnimationTrack` | Add a track to a Widget Animation |
| `ListPropertyBindings` | List property bindings in a Widget Blueprint |
| `AddPropertyBinding` | Add a property binding (same-WBP function / variable only) |
| `RemovePropertyBinding` | Remove a property binding |
| `ExtractWidgetToUserWidget` | Extract a widget subtree into a new UserWidget |

### Toolset bridges (13) 🧩

Mirror of native commands via the `UMGToolSet` plugin. Provider: `Toolset.Editor.UMG.*`. Requires UE 5.8+ and the `UMGToolSet` plugin.

> **⚠️ Breaking change — two of these are not callable: `Toolset.Editor.UMG.ReparentWidgetBlueprint` and `Toolset.Editor.UMG.SetWidgetAsVariable`.** `UMGToolSet` declares no tool under either name. For `SetWidgetAsVariable`, the `ToggleWidgetAsVariable` the toolset does declare **flips the flag rather than setting it to a requested value**, so pointing the bridge there would make it reach something and do the wrong thing. Both now report `Available: false` with `UnavailableDetail: "DelegationTargetMissing"`. **Enabling the `UMGToolSet` plugin does not resolve this.** The native **`UAIP.Editor.UMG.ReparentWidgetBlueprint`** and **`UAIP.Editor.UMG.SetWidgetAsVariable`** perform the same operations without the plugin.

---

## UAIP.Editor.Material

Material graph editing and parameter management.

| Command | Description |
|---|---|
| `GetMaterialInfo` | Basic info (NodeCount, ShadingModel, BlendMode, bHasErrors) |
| `ListMaterialNodes` | List of Material graph nodes (NodeId, ExpressionClass, position, bIsParameter) |
| `AddMaterialNode` | Add a node to the Material graph (`ExpressionClass`-specified) — a project-defined or custom-HLSL class needs a capability, see the note below |
| `DeleteMaterialNode` | Delete a node by NodeId (root deletion returns Conflict) |
| `ConnectMaterialPins` | Connect two pins in a Material graph (cycle / type-mismatch detection) |
| `DisconnectMaterialPins` | Disconnect a pin connection |
| `CompileMaterial` | Compile the material and return errors / warnings |
| `SetMaterialParameterValue` | Set a material parameter value |
| `GetMaterialParameterValue` | Get a material parameter value |
| `ListMaterialExpressionClasses` | List `UMaterialExpression` derived classes (max 500), each with `Admission` (`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`) plus `RequiredCapabilities` / `MissingCapabilities` from the same policy `AddMaterialNode` validates against. Use the returned `ClassPath` as the `ExpressionClass` argument. Reports `TotalCount`, `ReturnedCount`, `Truncated` — see the note below |
| `RefreshMaterial` | Force-recompile a material (recompiles a saved asset immediately without arguments) |

> **Note — project-defined and custom-HLSL expression classes are capability-gated**: an `ExpressionClass` from one of the engine's built-in modules (`Engine`, `RenderCore`, `MaterialEditor`, `Landscape`) is added the same way as before. A class outside those modules — a project- or plugin-defined `UMaterialExpression` subclass — now requires `MaterialCustomTypeEdit`. `UMaterialExpressionCustom`, `UMaterialExpressionCustomOutput` and their subclasses (arbitrary HLSL) require `MaterialCustomNodeEdit` regardless of which module they come from — this capability was already registered, but no command enforced it until now. A class that is both needs both capabilities together, and the refusal names whichever ones are missing. Neither is granted by default; see [Safety & Capabilities](safety.md#material-editing).
>
> These checks are not limited to `AddMaterialNode` — see [Capability-gated custom types](#capability-gated-custom-types) for how the same capabilities are re-checked when an existing node of one of these classes is edited, connected, disconnected, compiled, reparented, or deleted, and for the breaking change on delete / disconnect specifically.
>
> ⚠️ **Breaking change**: these classes used to be refused outright — `PolicyViolation` for one the type policy rejected, `InvalidParams` when the class could not be resolved at all. `AddMaterialNode` now answers `CapabilityNotAvailable` and names the missing capabilities once the class is loaded. There is no compatibility window for the old codes: they meant "no permission would have helped", so keeping them would describe a permission system that did not exist.
>
> `ExpressionClass` must already be loaded — `AddMaterialNode` no longer loads it as a side effect, and answers `NotFound` for a class it cannot resolve, whether or not it is one of the classes above.
>
> **Note — `ListMaterialExpressionClasses` now reports admission per class**: every entry carries `Admission`, one of four values — `Allowed` (usable by this session right now), `RequiresCapabilities` (usable once an operator grants the capabilities named in `MissingCapabilities`, itself a subset of `RequiredCapabilities`), `NotAddable` (refused for a structural reason no capability grant can fix — wrong base type, abstract, deprecated, or hidden from the class picker), or `CompatibilityUnknownUntilAuthorized` (the session already holds every required capability, but the engine's own compatibility check has not run — a listing must not execute a class's own code for a session it has not authorized, so the final answer only comes from actually adding the node). The response also reports `TotalCount`, `ReturnedCount` and `Truncated` — the 500-class cap this listing has always had was never reported before this. The set of classes returned is also wider than before: abstract, deprecated, `NewerVersionExists`, and class-picker-hidden classes used to be silently dropped from the response; they now appear with `Admission: NotAddable` instead of being omitted, so a class this command cannot place is described rather than hidden. This report is a snapshot, not an authorization: capabilities and roles can change between the listing and the mutation, so `AddMaterialNode` re-evaluates admission on its own request rather than trusting anything reported here.

---

## UAIP.Editor.GameplayTags

Manage project tag tables.

| Command | Description |
|---|---|
| `ListGameplayTags` | List all tags with filters (native inclusion, parent tag, source) — max 2048 |
| `GetGameplayTagInfo` | Tag details (Comment, Source, bIsNative, bIsRestrictedTag, parent / child) |
| `AddGameplayTag` | Add a normal tag to an INI |
| `AddRestrictedGameplayTag` | Add a Restricted tag to RestrictedTagList INI |
| `RemoveGameplayTag` | Remove a tag from an INI (child / native tag protection) |
| `RenameGameplayTag` | Rename a tag (optionally update asset references) |
| `FindGameplayTagReferencers` | Find assets that reference a tag |

### Toolset bridges — GameplayTags (6) 🧩

Bridge commands via the `GameplayTagsToolset` plugin (UE 5.8+, Experimental). Provider: `Toolset.Editor.GameplayTags.*`.

| Command | Description |
|---|---|
| `Toolset.Editor.GameplayTags.ListTags` | List registered tags, optionally restricted to descendants of `ParentTag` (max 2048) |
| `Toolset.Editor.GameplayTags.GetTagInfo` | Detail for a single tag — Comment, Source, Children |
| `Toolset.Editor.GameplayTags.FindReferencersByTag` | Find assets referencing a tag (max 256 paths) |
| `Toolset.Editor.GameplayTags.AddTag` | Add a tag to an existing `.ini` tag source (requires `GameplayTagEdit`) |
| `Toolset.Editor.GameplayTags.RemoveTag` | Remove a tag from the project tag table; asset references are **not** updated (requires `GameplayTagEdit`, and `GameplayTagRestrictedEdit` for a Restricted tag) |
| `Toolset.Editor.GameplayTags.RenameTag` | Rename a tag in INI only — no reference update and no redirect entry. Prefer the native `RenameGameplayTag` (requires `GameplayTagEdit`, and `GameplayTagRestrictedEdit` for a Restricted tag) |

> **Note — a write outside the project's own `Config/` directory needs `GameplayTagExternalSourceEdit`**: `AddGameplayTag`, `AddRestrictedGameplayTag`, `RemoveGameplayTag`, `RenameGameplayTag`, and the Toolset `AddTag` / `RemoveTag` / `RenameTag` bridges resolve where a tag would actually be written before touching anything. A destination outside the project's own `Config/` directory — an engine plugin, a Fab / third-party plugin, or **the project's own game plugin or Game Feature plugin** — now needs the DefaultDenied `GameplayTagExternalSourceEdit` capability in addition to `GameplayTagEdit` / `GameplayTagRestrictedEdit`, and is otherwise refused with `CapabilityNotAvailable` naming it. ⚠️ **Behavior change**: adding or renaming a tag in a plugin-owned source used to work with `GameplayTagEdit` alone; it now also needs `GameplayTagExternalSourceEdit`. A Restricted source reached through a plugin's search path whose write destination does not match where it is actually read from is refused outright with `NotAllowed` instead — no capability lifts that refusal, since the write would land somewhere other than where the source is read from. The boundary is checked by path text alone; a symbolic link or junction placed inside `Config/` that points outside it is still treated as inside. See [Safety & Capabilities — Gameplay systems](safety.md#gameplay-systems).
>
> **Note — deleting or renaming a Restricted tag needs `GameplayTagRestrictedEdit`**: adding a Restricted tag has always required this capability; `RemoveGameplayTag` / `RenameGameplayTag` and the Toolset `RemoveTag` / `RenameTag` bridges now require it too whenever the tag removed or renamed — or, for a forced removal or a rename that carries children, any of its descendants — is Restricted. A session holding only `GameplayTagEdit` is refused with `CapabilityNotAvailable` naming the missing capability.
>
> **Note — renaming a Restricted tag does not remove the old one**: this is an engine limitation, not a UAIP choice. The engine's rename implementation adds the new tag to the old tag's own source but leaves the old tag in place, and writes the redirect entry to the project's default tag file rather than to the Restricted source. `RenameGameplayTag` and the Toolset `RenameTag` bridge pass this through unchanged; the capability and source checks above are evaluated against what the engine actually writes (the old tag's source, plus the default source for the redirect).
>
> **Note — `AddGameplayTag` / Toolset `AddTag` refuse a Restricted source name up front**: naming a Restricted-tag source to an unrestricted add is refused with `InvalidParams` before any capability is checked, naming `AddRestrictedGameplayTag` as the command to use instead. The reverse — naming a non-Restricted source to `AddRestrictedGameplayTag` — is refused the same way.

---

## UAIP.Editor.GameFeatures 🧩

GameFeature Plugin management. Requires `GameFeatures` + `GameFeaturesEditor` plugins.

| Command | Description |
|---|---|
| `ListGameFeatures` 🧩 | List GameFeature Plugins with a `FilterState` filter (All / Installed / Mounted / Registered / Loaded / Active) |
| `GetGameFeatureInfo` 🧩 | GFP details (State, Actions, dependencies) |
| `GetGameFeatureActions` 🧩 | List the actions declared by a GameFeature Plugin's `UGameFeatureData` |
| `CreateGameFeaturePlugin` 🧩 | Create a new GameFeature Plugin under the project's `Plugins/GameFeatures/` folder, register it with the Game Feature subsystem and take it to `InitialState`. See the note below the table |
| `DeleteGameFeaturePlugin` 🧩 | Delete a content-only GameFeature Plugin from the project's `Plugins/GameFeatures/` folder. Requires `GameFeatureDelete`. Refused with `PolicyViolation` while `DisableSave` is in force. See the note below the table |

> **`CreateGameFeaturePlugin`** requires `GameFeatureCreate` and `PluginName` (a letter followed by up to 63 letters, digits or `_`). The optional `OutputPath` defaults to the project's `Plugins/GameFeatures/`; a relative path is taken from the project root, so `Plugins/GameFeatures/Combat` creates the plugin in `Plugins/GameFeatures/Combat/<PluginName>/`. The optional `InitialState` (`Installed`, `Registered`, `Loaded` or `Active`; default `Active`) is the state the plugin is taken to, and it is the state it starts from after a restart. The plugin gets a GameFeature data asset with the same name, is registered as a GameFeature in the session that created it (usually within a few seconds), and is registered again after an editor restart. The `.uproject` file is not changed.
>
> - **Success**: `Data` carries `PluginPath` (relative to the project root; the real location), `PluginUrl`, `State` and `Warnings`. When the project has no asset-manager setting for GameFeature data, `Warnings` explains that a packaged build may leave this GameFeature's data out and gives the `DefaultGame.ini` lines to add. The command never edits project settings itself.
> - **`InvalidParams`**: `OutputPath` outside the project's `Plugins/GameFeatures/` folder (for example directly under `Plugins/`, or outside the project), inside an existing plugin, or reaching outside the project through a junction; an invalid name; an invalid `InitialState`. Nothing is created. `Conflict` when a folder or plugin with the name already exists. `NotAllowed` while the editor is shutting down, in PIE or running as a commandlet. `PolicyViolation` when the safety policy disables disk writes.
> - **`ExecutionFailed`** when a step fails partway (plugin creation, data asset creation or save, registration), registration does not finish within 30 seconds, the editor starts shutting down, or the location turns out to be outside the project when it is checked again after creation. What was already created is left in place, and `Data` reports how far it got (`CreatedOnDisk`, `Mounted`, `DataAssetCreated`, `DataAssetSaved`, `Registered`), the reached `State` and `PluginPath`; the same report is attached as a JSON artifact, with a copy of the `.uplugin` when one exists. Use `DeleteGameFeaturePlugin` to clean up — except when the location check failed: the plugin is then detached from the editor but its files stay and `DeleteGameFeaturePlugin` also refuses it, so inspect and delete it by hand.
>
> **`DeleteGameFeaturePlugin`** takes `PluginName`. It unregisters the GameFeature (a plugin that never got registered, as after a failed create, skips this), unloads its assets, checks again that the target may be deleted, removes the plugin and deletes the folder. It refuses, and deletes nothing, when: the plugin does not exist (`NotFound`); the target is not a GameFeature — a plugin outside `Plugins/GameFeatures/`, or one an older version created directly under `Plugins/` — or it is the `GameFeatures` folder itself, contains other plugins, has code modules or contains a link such as a junction (`NotAllowed`); the GameFeature is changing state (`PreconditionFailed`; wait and retry); unloading the assets failed, unregistering did not finish within 30 seconds, or the editor began shutting down (`ExecutionFailed`).

### Toolset bridges — GameFeatures (4) 🧩

Bridge commands via the `GameFeaturesToolset` (UE 5.8+, Experimental). Provider: `Toolset.Editor.GameFeatures.*`.

| Command | Description |
|---|---|
| `Toolset.Editor.GameFeatures.ListGameFeatures` | Not available through this bridge command — use `UAIP.Editor.GameFeatures.ListGameFeatures` instead (see the note below) |
| `Toolset.Editor.GameFeatures.FindGameFeatureData` | ⚠️ **Not callable** — no delegation target exists and there is no native counterpart (see the note below) |
| `Toolset.Editor.GameFeatures.GetActions` | ⚠️ **Not callable** — no delegation target exists and there is no native counterpart (see the note below) |
| `Toolset.Editor.GameFeatures.CreateGameFeaturePlugin` | ⚠️ **Not callable** — use `UAIP.Editor.GameFeatures.CreateGameFeaturePlugin` instead (see the note below) |

> **⚠️ Breaking change — `Toolset.Editor.GameFeatures.ListGameFeatures` is no longer reachable through this bridge command, on any engine version.** The `GameFeaturesToolset` this handler forwards to declares no function named `ListGameFeatures`, so the forwarded call could never reach an implementation — it used to fail at execution time with a generic `ExecutionFailed` no matter what was asked. It now reports `Available: false` from `UAIP.Core.DescribeCommand` and `uaip_list_commands`, with `UnavailableReason: "HandlerUnavailable"` and `UnavailableDetail: "DelegationTargetMissing"`. Calling it by name still fails, now with `PolicyViolation` and the same explanation in `ErrorMessage`. **Use `UAIP.Editor.GameFeatures.ListGameFeatures` instead** — the native command performs the same operation without delegating, and is unaffected by this change.

> **⚠️ Breaking change — the same state applies to the other three commands in this section.** Checking every bridge command's delegation pair found that `FindGameFeatureData`, `GetActions` and `CreateGameFeaturePlugin` also delegate to names `GameFeaturesToolset` does not declare (the seven it does declare are `GetGameFeatureState`, `IsGameFeatureActive`, `IsGameFeaturePlugin`, `ListDiscoveredGameFeaturePlugins`, `ListEnabledGameFeaturePlugins`, `RequestActivateGameFeature` and `RequestDeactivateGameFeature`). All three now report `Available: false` with `UnavailableDetail: "DelegationTargetMissing"`. **Enabling the `GameFeaturesToolset` plugin does not resolve this.** For `CreateGameFeaturePlugin`, **`UAIP.Editor.GameFeatures.CreateGameFeaturePlugin`** performs the same operation natively. `FindGameFeatureData` and `GetActions` have no native counterpart, so as of this update neither operation has a working path in this plugin.

---

## UAIP.Editor.Niagara 🧩

Niagara VFX system editing. Requires `Niagara` + `NiagaraEditor` plugins and **UE 5.7 or newer**.

### Native (52)

#### Observation (13)

| Command | Description |
|---|---|
| `GetSystemTopology` 🧩 | Niagara system emitter structure — each emitter's `Spawn` / `Update` / `Event` module lists, each entry now carrying `ModuleId` alongside `ModuleName` (feeds straight into `GetStackInputData`). Module entries here never carry an `Inputs` array — use `GetModuleTopology` or `GetStackInputTopology` to inspect a module's inputs. ⚠️ `Spawn`/`Update` are the *emitter*-level Spawn/Update stacks and `Event` is the event handler stack — a system's Particle Spawn / Particle Update modules are never listed here; use `GetEmitterTopology` for those. |
| `GetSystemCompileState` 🧩 | System compilation state |
| `GetAssetDiscoveryInfo` 🧩 | Niagara asset discovery info |
| `GetScriptAssets` 🧩 | Niagara script asset list |
| `GetNiagaraParameterCollections` 🧩 | Niagara parameter collection list |
| `GetUserVariables` 🧩 | User variable list of a system |
| `GetSystemInfo` 🧩 | System detail info (with metadata) |
| `GetSystemData` 🧩 | System data structure |
| `GetEmitterData` 🧩 | Emitter data structure |
| `GetRendererData` 🧩 | Renderer data structure |
| `GetStackInputData` 🧩 | Module stack input value — name, type, value mode (Local/Linked/Dynamic/DataInterface/Expression), the current value in the form `AddSetParameterEntry` accepts back, and a nested `WriteRequirements` object. Its required `ModuleId` parameter comes from `GetSystemTopology`, `GetEmitterTopology`, `GetScriptStackTopology`, `GetModuleTopology`, or `AddModule`'s own response — all four reads and the write return it in the same lowercase-hyphenated form, so a module on an asset nobody used UAIP to build can be read without ever having added one. |
| `UEnum_Info` 🧩 | UEnum information |
| `GetAvailableNiagaraRendererClasses` 🧩 | List of `UNiagaraRendererProperties`-derived classes (max 200). Use the returned `ClassPath` as the `RendererClass` argument of `AddRenderer`. |

#### Schema (7)

| Command | Description |
|---|---|
| `GetSystemSchema` 🧩 | JSON Schema of all editable top-level `UNiagaraSystem` properties (constant across systems — cacheable). UE 5.8+ only; reports `Available: false` on UE 5.7 |
| `GetEmitterSchema` 🧩 | JSON Schema of all editable top-level emitter properties (cacheable). UE 5.8+ only; reports `Available: false` on UE 5.7 |
| `GetRendererSchema` 🧩 | JSON Schema for one `UNiagaraRendererProperties` class, selected by `RendererClassPath`. UE 5.8+ only; reports `Available: false` on UE 5.7 |
| `GetDataInterfaceSchema` 🧩 | JSON Schema for one `UNiagaraDataInterface` class, selected by `DataInterfaceClassPath`. UE 5.8+ only; reports `Available: false` on UE 5.7 |
| `GetStackInputSchema` 🧩 | Type / category / `SupportsExpressions` for one module input |
| `GetModuleSchema` 🧩 | Inputs and outputs of a module instance in the stack |
| `GetModuleSchemaFromAsset` 🧩 | Inputs and outputs of a `UNiagaraScript` module asset, without an owning system |

#### Topology and dynamic inputs (7)

| Command | Description |
|---|---|
| `GetEmitterTopology` 🧩 | Full module stack topology of an emitter (all script stacks and their modules), each module entry carrying `ModuleId` |
| `GetScriptStackTopology` 🧩 | Module topology of one script stack, each module entry carrying `ModuleId` |
| `GetModuleTopology` 🧩 | Input topology of one module, including that module's own `ModuleId` |
| `GetStackInputTopology` 🧩 | Topology of one input — name, type, `IsVisible`/`IsEditable`/`IsDynamic`. No resolved value is included, and `DynamicInputChildren` is always returned as an empty array on every engine version rather than a walked chain — use `GetDynamicInputSchema` to read an actual dynamic input's own inputs and outputs, and `GetStackInputData` for the current value. The same `Name`/`Type`/`IsVisible`/`IsEditable`/`IsDynamic`/`DynamicInputChildren` shape, and the same always-empty `DynamicInputChildren`, is also what `GetModuleTopology`, `GetEmitterTopology` and `GetScriptStackTopology` use for each module's own `Inputs[]` entries |
| `GetDynamicInputSchema` 🧩 | Inputs and outputs of a dynamic input script instance in the stack |
| `GetDynamicInputSchemaFromAsset` 🧩 | Inputs and outputs of a `UNiagaraScript` dynamic input asset, without an owning system |
| `GetAvailableDynamicInputs` 🧩 | Dynamic input scripts compatible with a specific module input. UE 5.8+ only; reports `Available: false` on UE 5.7 |

> **⚠️ Note — `GetStackInputSchema`, `GetModuleSchema` and `GetDynamicInputSchema` now also read ordinary modules on their pre-5.8 fallback, and that fallback's key names now match UE 5.8+**: each of these three commands used to succeed on UE 5.7 only against a "Set Parameters" (assignment) module — `GetStackInputSchema` and `GetDynamicInputSchema` failed the whole call with `ExecutionFailed` against anything else, and `GetModuleSchema` answered success with `Inputs` as an empty array instead of failing. All three now also read an ordinary function-call module directly from the graph (no view model). `GetModuleSchema` now fails, rather than answering an empty array, when the target module has no valid script or graph to read. `GetDynamicInputSchema` still fails when the addressed input is not actually driven by a dynamic input — that refusal is intentional, since there is nothing to describe, not a bug. Separately, this fallback's JSON keys for an input entry changed from `InputName`/`InputType` to `Name`/`Type` — for `GetStackInputSchema`'s own entries, and for each element of the `Inputs` array `GetModuleSchema` and `GetDynamicInputSchema` return — so all three now use the same key names UE 5.8+ always did. `GetDynamicInputSchema`'s own Set Parameters branch also changed its envelope to match its own ordinary-module branch: it now returns `{ModuleAssetPath, Inputs: [{Name, Type}], Outputs: []}` instead of the previous bespoke `{InputName, InputType, Inputs: [], Outputs: []}`. None of this touches `GetStackInputData`, which keeps returning `InputName`/`InputType` on every engine version.
>
> **⚠️ Note — `GetStackInputTopology`'s pre-5.8 fallback now also reads ordinary modules, not only Set Parameters**: the response shape has matched UE 5.8+ (`Name`/`Type`/`IsVisible`/`IsEditable`/`IsDynamic`/`DynamicInputChildren`) since the two branches were unified; what changed here is which modules the command can read. It used to succeed only against a "Set Parameters" (assignment) module and fail the whole call with `ExecutionFailed` against anything else. It now also succeeds against an ordinary function-call module, reading its inputs directly from the graph (no view model). How this fallback walks a multi-element `InputNameStack` changed since then — see the note below. A static switch input still cannot be targeted through this branch, on either kind of module.
>
> How much of `IsVisible`/`IsEditable`/`IsDynamic` is actually measured now depends on which kind of module was matched:
> - Against a **Set Parameters** module, nothing changed: `IsVisible` and `IsEditable` are still always reported as `true` — not measured from the module (an assignment target carries no visibility/editability metadata of its own), but true because reaching this outcome already means the target's whole purpose is exposing its assignment targets for editing. `IsDynamic` is still always reported as `false` as a conservative default, since this path still has no way to detect an actual dynamic input chain on an assignment target.
> - Against an **ordinary module**, `IsDynamic` is now genuinely measured: it reports `true` only when the input's override pin connects to a Dynamic Input script's function-call node — the same condition UE 5.8+ calls value mode `Dynamic`. `IsVisible` is measured too, from the module's own current hidden-input set, but a `VisibleCondition` expression is not evaluated, so an input hidden only by a false condition is still reported visible. `IsEditable` reuses that same measured visibility and is therefore only half-measured: an `EditCondition` expression — which needs a sibling input's current value and cannot be resolved from the graph alone — is not evaluated either, so an input made read-only only by a false edit condition is still reported editable.
>
> **⚠️ Breaking change — `GetStackInputTopology`, `GetStackInputSchema` and `GetDynamicInputSchema`'s pre-5.8 fallback now walks every element of `InputNameStack`, not only the first one**: all three used to consult only `InputNameStack[0]` and silently ignore the rest — a caller targeting a nested dynamic input's own input (e.g. `[TopLevelInput, NestedInput]`) got back `TopLevelInput`'s own data, reported as a normal success, with nothing indicating the nested element was never read. **This means a prior nested-stack answer was not merely incomplete — it described the wrong input while reporting success.** The fallback now walks the whole stack the same way UE 5.8+ already does: `InputNameStack[0]` resolves against the module's own input, and each further element resolves against the input on the Dynamic Input script instance currently driving the previous element. When an element along the way is not actually driven by a dynamic input, or its name does not resolve, the call now fails instead of silently answering a different input than the one addressed. `GetDynamicInputSchema` now describes the dynamic input instance driving the *resolved leaf*, not the one driving `InputNameStack[0]`. Against a **Set Parameters** (assignment) module specifically, a stack of more than one element is now refused outright — an assignment target carries no dynamic input of its own to walk into, so previously it silently answered the assignment target's own data regardless of how many elements were addressed. **UE 5.8+ is unaffected** — it already walked the full stack. A single-element `InputNameStack`, the common case, resolves exactly as before on every engine version.
>
> **⚠️ Breaking change — `GetModuleTopology`'s pre-5.8 fallback returns a different shape, now honors `ScriptName`, and can target a system-level script**: the fallback used to walk a system view model across the whole emitter stack and answer `{ModuleName, ModuleAssetPath, Inputs: [{InputName, InputType}], Outputs: []}`, ignoring the `ScriptName` argument entirely — the module was matched anywhere in the emitter's stacks, never against the one stack `ScriptName` named. An empty `EmitterName` never matched any stack, so a system-level module could not be read through this branch at all. The fallback now reads the addressed script's graph directly, the same crash-safe way UE 5.8+ already does, and `ScriptName` is genuinely consulted; an empty `EmitterName` now resolves the system's own spawn/update script, matching what `GetEmitterTopology` and `GetScriptStackTopology` already accepted. The response shape changed to match: `ModuleAssetPath` is renamed to `ModuleScript`; `Outputs` is gone — a module's topology carries no output concept on either engine version, and the fallback's own `Outputs` was always an empty array anyway, so nothing is actually lost; `Enabled` and `IsSetParametersModule` are new; and each `Inputs[]` entry now carries `Name`/`Type`/`IsVisible`/`IsEditable`/`IsDynamic`/`DynamicInputChildren` (see the `GetStackInputTopology` row above, including its `DynamicInputChildren` limitation) instead of `InputName`/`InputType` alone. Module-name matching is also now case-sensitive, where it used to ignore case. `Enabled` is read off the module's own function-call node; a module whose sub-nodes were disabled independently of the node itself can report a different `Enabled` than what UE 5.8+'s own stack view would show for the same abnormal state.
>
> **⚠️ Breaking change — `GetEmitterTopology`'s pre-5.8 fallback drops `IsEnabled`, wraps each script stack in the same `{ScriptName, Modules}` shape UE 5.8+ has always used, and each `Modules[]` entry gains five fields**: the fallback used to answer `{EmitterName, IsEnabled, EmitterSpawn: [{ModuleName}], EmitterUpdate: [...], ParticleSpawn: [...], ParticleUpdate: [...], Renderers: [{RendererClass}]}` — `EmitterSpawn`/`EmitterUpdate`/`ParticleSpawn`/`ParticleUpdate` were bare arrays of modules, and each module carried only `ModuleName`. `IsEnabled` is gone: UE 5.8+'s own emitter topology never carried it either, so a field that only ever existed on one engine version was worse than no field at all. The emitter's enabled state stays readable on every engine version, from `GetSystemTopology`'s per-emitter entries or from `GetEmitterData`. Each of the four script stacks is now wrapped as `{ScriptName, Modules}`, the same object shape UE 5.8+ has always returned — a caller that iterated `EmitterSpawn` etc. as a bare array of modules must switch to reading its `Modules` field instead. Each `Modules[]` entry grows from a single `ModuleName` field to the same six fields `GetModuleTopology` and `GetScriptStackTopology`'s module entries carry (see above and below): `ModuleName`, `ModuleId`, `Enabled`, `IsSetParametersModule`, `ModuleScript`, and `Inputs`. Each `Renderers[]` entry also gains `RendererIndex` alongside the existing `RendererClass`, matching UE 5.8+ — pass the reported index back into `RemoveRenderer`. `RendererClass`'s own value also changes on this fallback, from a full class path (e.g. `/Script/Niagara.NiagaraSpriteRendererProperties`) to the bare class name (e.g. `NiagaraSpriteRendererProperties`) UE 5.8+ has always reported — the same bare name `GetRendererSchema` now also accepts directly (see below).
>
> **Note — `GetScriptStackTopology`'s pre-5.8 fallback adds fields to each `Modules[]` entry; nothing is removed**: each entry used to carry only `ModuleName`. It now carries the same six fields `GetModuleTopology` and `GetEmitterTopology`'s module entries carry — `ModuleName`, `ModuleId`, `Enabled`, `IsSetParametersModule`, `ModuleScript`, and `Inputs` (in the `GetStackInputTopology` shape, see above) — but `ModuleName` keeps meaning what it always meant, and the surrounding `{ScriptName, Modules}` envelope is unchanged, so code that only ever read `ModuleName` off each entry keeps working unmodified.
>
> **⚠️ Breaking change — `GetScriptStackTopology`'s pre-5.8 fallback now reports the canonical `ScriptName`, not the spelling the caller passed in**: the response's `ScriptName` field used to echo back the exact string passed as the `ScriptName` argument, whatever its spelling or case — a caller that requested `"particlespawn"` or even `"whatever"` got that same string reflected back, indistinguishable from a genuine answer. It now reports the same canonical name (`EmitterSpawnScript`, `ParticleUpdateScript`, `SystemSpawnScript`, and so on) that `GetEmitterTopology`'s own script-stack entries already reported on this fallback — the two commands used to answer differently for the same stack within the same engine session; they no longer do. **UE 5.8+ is unaffected** — it already reported the canonical name.
>
> **Note — on UE 5.8+, a `Modules[]` entry's `ModuleId` is best-effort and can be missing; on UE 5.7 and earlier it is always present**: `GetEmitterTopology`, `GetScriptStackTopology` and `GetModuleTopology` all get `ModuleId` the same way on UE 5.8+. `UNiagaraExternalEditUtilities`' topology structs identify a module by display name only and carry no guid field at all, so `ModuleId` has to be backfilled afterward, by walking the script's graph and matching each entry's `ModuleName` against a `UNiagaraNodeFunctionCall` node — case-sensitively. When no node matches, the entry is left without a `ModuleId` key rather than an empty string, so it carries one field fewer than a sibling entry that did match. On UE 5.7 and earlier, the fallback reads the node's guid directly while it is already walking the same graph to build the rest of the entry, so `ModuleId` is always present there. Code that reads `Modules[].ModuleId` unconditionally should account for its occasional absence on UE 5.8+.
>
> **⚠️ Breaking change (UE 5.8+ only) — an enum-typed input's `Type` field now reports the enum's own name instead of `NiagaraInt32`.** Every `Type` field goes through one serialization function, and it used to test `FNiagaraTypeDefinition::GetStruct()` before `GetEnum()`. Niagara stores an enum's value in an `int32` struct, so `GetStruct()` never returned null for an enum type, and every enum-typed input was reported as `"NiagaraInt32"` with its enum identity lost. This is a bug fix, not a new capability: the check order now tries `GetEnum()` first, so an enum-typed input now reports its own enum name instead — e.g. `"ENiagaraCoordinateSpace"`. A struct-typed input (`"NiagaraFloat"`, or `"NiagaraInt32"` on a genuine integer input) and a class-typed input are unaffected. This touches the `Type` field everywhere it appears on UE 5.8+: `GetModuleTopology`, `GetEmitterTopology` and `GetScriptStackTopology`'s per-input entries, `GetStackInputTopology`, `GetStackInputSchema`, `GetModuleSchema`, `GetDynamicInputSchema`, `GetDynamicInputSchemaFromAsset`, and `GetModuleSchemaFromAsset` (which delegates to `GetDynamicInputSchemaFromAsset`). **UE 5.7 and earlier are unaffected** — their fallback already read the enum's own name off `FNiagaraTypeDefinition::GetName()`, so this change brings UE 5.8+ in line with what UE 5.7 and earlier always reported.
>
> **Note — `GetRendererSchema` now also accepts a bare class name for `RendererClassPath`, on every engine version.** The parameter used to resolve only a full class path (e.g. `/Script/Niagara.NiagaraSpriteRendererProperties`). It now also resolves the bare class name (e.g. `NiagaraSpriteRendererProperties`) that `GetEmitterTopology`'s `Renderers[].RendererClass` (see above) and `GetRendererData` already report — the parameter name `RendererClassPath` is unchanged, and the existing path form still works. A bare name that matches more than one renderer class is refused rather than guessed at. `AddRenderer` and `SetRendererData` accept the same two forms for their own `RendererClassPath` argument.
>
> **Note — `GetDataInterfaceSchema` now also accepts a bare class name for `DataInterfaceClassPath`, on every engine version.** Previously this parameter resolved only a full class path. It now also resolves the bare class name (e.g. `NiagaraDataInterfaceCurve`) that this command's own `TypeName` field, and a data-interface-typed `Type` field anywhere in a topology or schema read, already report — so a type name read from one of those fields can now be handed straight back into this command. The parameter name `DataInterfaceClassPath` is unchanged, and the existing path form still works.
>
> **Note — `GetModuleSchema` and `GetDynamicInputSchema`'s pre-5.8 fallback now reports the same four `Inputs[]` keys UE 5.8+ always has.** Each `Inputs[]` entry used to carry only `Name`/`Type`; it now also carries `Category` and `SupportsExpressions`, matching the shape UE 5.8+ already uses. On this fallback, though, neither new field is actually measured: `Category` is always an empty string and `SupportsExpressions` is always `false`, because both are normally read off the stack view model and neither has an equivalent on the graph-only path this fallback uses. `Name` and `Type` are unaffected, and `Outputs[]` stays empty on this fallback as before.
>
> **⚠️ Breaking change — `GetDynamicInputSchemaFromAsset`'s pre-5.8 fallback now returns the asset's actual declared inputs instead of always answering an empty array.** The fallback used to answer `{ModuleAssetPath, Inputs: [], Outputs: []}` for every asset regardless of what it declared, and always reported success — a caller could only read that as "this asset declares no inputs", when the truth was that nothing had been read at all. It now reads the same `Module.`-namespace declarations UE 5.8+ already reads off the asset's graph (`Name`/`Type`/`Category`/`SupportsExpressions` per entry, static switches excluded), so a successful call's `Inputs` is populated whenever the asset declares any. **A call that used to always succeed can now fail**: when the asset carries no readable graph, the command now answers `ExecutionFailed` instead of the previous empty-but-successful response. `Outputs` stays an empty array on this fallback, as it always was. Because the asset is read directly rather than through a call site inside a stack, the reported set is a superset of what the same script would report when read from inside a stack: an input hidden behind a static-switch branch a particular call site never takes is still listed, and stack-side hidden-input narrowing does not apply here. `GetModuleSchemaFromAsset` delegates to this same read and changes identically. **UE 5.8+ is unaffected** — its own branch already could fail on an asset with no graph to read, and keeps doing so unchanged.
>
> **⚠️ Breaking change — `GetAvailableDynamicInputs` is no longer available at all on UE 5.7; it used to fail with `ExecutionFailed`, it now doesn't appear in `uaip_list_commands`'s default listing.** Which dynamic input scripts a stack input accepts is decided by the same engine surface that offers them inside the stack UI, and UE 5.7 has no graph-level equivalent to read it from. The command used to report `Available: true` on every engine version and let the call reach the handler, where the pre-5.8 fallback answered `{DynamicInputs: []}` with `Success: true` — reading as "no dynamic input fits this input", indistinguishable from the question never having been asked. A later revision changed that fallback to answer `ExecutionFailed` instead, with `ErrorMessage` explaining the UE 5.8 engine-API requirement. **The refusal has now moved again, from execution time to discovery time**: `UAIP.Core.DescribeCommand` and `uaip_list_commands` report `Available: false` on UE 5.7 from the start, with `UnavailableReason: "HandlerUnavailable"` and `UnavailableDetail: "EngineVersion"`. Calling it by name on UE 5.7 still fails, but now with `PolicyViolation` rather than `ExecutionFailed`, and the same explanation appears in `ErrorMessage`. **UE 5.8+ is unaffected** — its own branch already could fail (an unresolved system, emitter, script or module) and keeps doing so unchanged.
>
> **⚠️ Breaking change — `GetEmitterSchema`, `GetSystemSchema`, `GetRendererSchema` and `GetDataInterfaceSchema` are no longer available at all on UE 5.7; they used to fail with `ExecutionFailed`, they now don't appear in `uaip_list_commands`'s default listing.** `PropertySchema` is built by an engine API introduced in UE 5.8, and UE 5.7 has no equivalent to build it from. All four used to report `Available: true` on every engine version and let each call reach the handler, where an earlier revision answered success with `PropertySchema` fixed at an empty string, and a later one changed that to `ExecutionFailed` with an explanatory `ErrorMessage`. **The refusal has now moved again, from execution time to discovery time**: `UAIP.Core.DescribeCommand` and `uaip_list_commands` report `Available: false` on UE 5.7 for all four from the start, with `UnavailableReason: "HandlerUnavailable"` and `UnavailableDetail: "EngineVersion"`. Calling one of the four by name on UE 5.7 still fails, but now with `PolicyViolation` rather than `ExecutionFailed`, and the same explanation appears in `ErrorMessage`. **UE 5.8+ is unaffected** — its own branch already could fail (an unresolved system or class) and keeps doing so unchanged. Read `GetRendererData` / `GetEmitterData` / `GetSystemData` for the actual property values on every engine version, as before.
>
> **Note — a failed `GetDynamicInputSchema` classifies why into one of six `FailureReason` values, and rebuilds its own sentence instead of forwarding the engine's.** `ErrorCode` stays `ExecutionFailed` either way — only `Result.FailureReason` tells the six apart: `NestedStackOnAssignmentModule` (the target is a Set Parameters module, which only accepts a single-element `InputNameStack`, but more than one element was given), `AssignmentTargetNotFound` (the Set Parameters module has no assignment target under this name), `InputNotFound` (the name does not resolve to an input on this module or dynamic input script at all), `NoOverridePin` (the input exists but carries no override — it is still at its own default value), `OverrideIsNotDynamicInput` (the input's override exists but drives a script that is not itself a dynamic input), and `InputIsNotDynamic` (the input exists and is not in Dynamic mode). `FailureReason` is absent from the response when the failure falls outside this vocabulary — for example, the system, script or module itself could not be resolved. **On UE 5.8+, `NoOverridePin` and `OverrideIsNotDynamicInput` cannot be told apart from a genuinely non-Dynamic input**: the engine's own public topology surface reports all three as `InputIsNotDynamic` there. UE 5.7 reads the graph directly and keeps all six distinct. When this aggregation applies, the response also carries `Result.AmbiguousFailureReasons: ["NoOverridePin", "OverrideIsNotDynamicInput"]` alongside `FailureReason: "InputIsNotDynamic"`, so a caller can tell "determined to be exactly this" apart from "could not tell which of these it is" — the field is absent whenever the running engine version can distinguish the two. `ErrorMessage` is always UAIP's own wording, never a forwarded engine string.
>
> **Note — `GetStackInputSchema`, `GetStackInputTopology`, `GetDynamicInputSchema` and `GetAvailableDynamicInputs` now widen the spelling their `InputNameStack` parameter accepts, without widening which input it can reach.** `GetStackIssues`' `Location.InputNameStack` (see below) can include a leading run of conditional / static-switch structure that is not itself a Dynamic-mode input — structure these four commands' own flat, single-element lookup already reaches through on its own. Previously, handing that stack straight back to one of these four could fail on such a leading element even though the leaf it named was reachable through a shorter stack. These four now try the stack exactly as given first; when that does not resolve, they drop the leading run up to and including the first element that is not itself reported Dynamic-mode, then resolve the remainder as a single-element lookup — only when that shortened form matches exactly one input under the addressed module. **The set of inputs reachable is unchanged; only how many elements are needed to name the same input widens.** A shortened form matching more than one input under the module (the same name reused under different parents) is refused rather than guessed at, and a name that does not resolve under any spelling is still refused, whichever form was used to ask for it. This is what makes `GetStackIssues`' `Location.InputNameStack` usable unchanged as input to any of these four commands, without the caller reconstructing a shorter path by hand.

#### Stack issues (2)

| Command | Description |
|---|---|
| `GetStackIssues` 🧩 | All stack issues (errors / warnings / info, including dismissed) with the `IssueId` and `FixId` needed below. UE 5.8+ only; reports `Available: false` on UE 5.7 |
| `ApplyStackIssueFix` 🧩 | Apply a Fix-style automated fix by `IssueId` + `FixId` (Link-style fixes are rejected; requires `NiagaraStackAutoFix`). UE 5.8+ only; reports `Available: false` on UE 5.7 |

> **Note — each `GetStackIssues` issue's `Location` object carries `InputNameStack` or `RendererIndex`, whichever applies, and neither when the issue targets a module or the system as a whole.** Every `Location` always carries `EmitterName`, `ScriptName` and `ModuleName`. When the issue names a specific stack input, `Location` also carries `InputNameStack` — the same ordered array of names, from module-level to leaf, that `GetStackInputSchema`, `GetStackInputTopology`, `GetDynamicInputSchema` and `SetStackInputData` accept as their own `InputNameStack` parameter. When it names a renderer instead, `Location` carries `RendererIndex` in its place. The two fields are mutually exclusive, and neither is padded in with an empty array or `-1` when it doesn't apply — the field's presence, not its value, is what says whether it applies. Pass a populated `InputNameStack` from `GetStackIssues` straight into any of the four input commands above to inspect or fix the exact input an issue names, without reconstructing the path by hand. Because `GetStackIssues` itself is UE 5.8+ only (see above), `Location` — and this round trip — only exists there.

> **⚠️ Breaking change — `GetStackIssues` and `ApplyStackIssueFix` are no longer available at all on UE 5.7; both used to fail with `ExecutionFailed`, they now don't appear in `uaip_list_commands`'s default listing.** Both used to report `Available: true` on every engine version and let each call reach the handler, where an earlier revision answered success unconditionally (`GetStackIssues` with an empty `Issues` array, `ApplyStackIssueFix` with `{Applied: false}`), and a later one changed that to `ExecutionFailed` with an explanatory `ErrorMessage` — reading either outcome as "no issues exist" / "this fix could not be applied" would have been indistinguishable from the check never having run. **The refusal has now moved again, from execution time to discovery time**: `UAIP.Core.DescribeCommand` and `uaip_list_commands` report `Available: false` on UE 5.7 for both from the start, with `UnavailableReason: "HandlerUnavailable"` and `UnavailableDetail: "EngineVersion"`. Calling either by name on UE 5.7 still fails, but now with `PolicyViolation` rather than `ExecutionFailed`, and the same explanation appears in `ErrorMessage`. **On UE 5.7 the whole call path that used to distinguish "engine-version refusal" from "this Fix genuinely could not be applied" is gone**, since `ApplyStackIssueFix` cannot be reached there at all anymore. **UE 5.8+ is unaffected for both commands**, including `ApplyStackIssueFix`'s ordinary `{Success: true, Applied: false}` outcome for a fix that legitimately does not apply, which was already reported this way and stays that way.

#### Editing (21)

| Command | Description |
|---|---|
| `AddEmitter` 🧩 | Add an emitter to a Niagara system |
| `RemoveEmitter` 🧩 | Remove an emitter |
| `DuplicateEmitter` 🧩 | Duplicate an emitter. Not available through this native command, and the Toolset bridge equivalent has no working target either — see the note below |
| `SetEmitterEnabled` 🧩 | Toggle emitter enabled state |
| `SetEmitterName` 🧩 | Change emitter name |
| `SetEmitterData` 🧩 | Set emitter data |
| `AddRenderer` 🧩 | Add a renderer to an emitter |
| `RemoveRenderer` 🧩 | Remove a renderer |
| `SetRendererData` 🧩 | Set renderer data (requires `NiagaraStackEdit`). When the emitter has no renderer of the named class the command now answers `NotFound` — it no longer falls back to writing whichever renderer came first. A property the write path cannot handle fails the whole request with `PolicyViolation` instead of being ignored, a struct default that only parses part-way is refused with `InvalidParams` instead of being taken as the default, and a successful write raises `PostEditChangeProperty` so the editor reflects it immediately |
| `AddModule` 🧩 | Add a module to an emitter module stack |
| `RemoveModule` 🧩 | Remove a module |
| `MoveModule` 🧩 | Move a module within the stack. Not available through this native command, and the Toolset bridge equivalent has no working target either — see the note below |
| `SetModuleEnabled` 🧩 | Toggle module enabled state |
| `SetStackInputData` 🧩 | Set a module stack input value |
| `SetSystemData` 🧩 | Set system data |
| `AddUserVariables` 🧩 | Add user variables to a system |
| `RemoveUserVariables` 🧩 | Remove user variables |
| `CompileNiagaraSystem` 🧩 | Compile the Niagara system |
| `AddSetParametersModule` 🧩 | Add a Set Parameters module to a stack and register initial parameter entries. The `DefaultValue` field is applied for common types (float, int, bool, struct) and, with `NiagaraReferenceEdit`, for a data interface or object parameter given as an object path — see the note below. |
| `AddSetParameterEntry` 🧩 | Add a parameter entry to an existing Set Parameters module. Requires `ScriptName` (e.g. `Spawn`, `Update`). The `DefaultValue` field is applied for common types (float, int, bool, struct) and, with `NiagaraReferenceEdit`, for a data interface or object parameter given as an object path — see the note below. |
| `RemoveSetParameterEntry` 🧩 | Remove a parameter entry from a Set Parameters module. Requires `ScriptName` (e.g. `Spawn`, `Update`). |

> **⚠️ Breaking change — `DuplicateEmitter` and `MoveModule` are no longer reachable through these native commands, on any engine version.** The engine-side APIs they call (`FNiagaraSystemViewModel::DuplicateEmitters` and `FNiagaraStackGraphUtilities::MoveModule`) are not exported outside the engine module, so neither could ever actually run — both used to fail at execution time with `NotAllowed` no matter what was asked. Both now report `Available: false` from `UAIP.Core.DescribeCommand` and `uaip_list_commands` on every engine version, with `UnavailableReason: "HandlerUnavailable"` and `UnavailableDetail: "EngineApiNotExported"`. **No engine upgrade fixes this** — the export is missing on every version, not just an older one. Calling either by name still fails, now with `PolicyViolation` and the same explanation in `ErrorMessage`.
>
> **⚠️ Update — the Toolset bridge equivalents do not fill this gap either.** `Toolset.Editor.Niagara.DuplicateEmitter` and `Toolset.Editor.Niagara.MoveModule` were expected to reach the same operations through the engine's own toolset, but the `NiagaraToolsets` plugin declares no function under either name, in any engine version this plugin supports. Both bridge commands now report `Available: false` too, with `UnavailableDetail: "DelegationTargetMissing"` (see the note under Toolset bridges, below). **As of this update, neither operation has a working path anywhere in this plugin.**
>
> **⚠️ Behavior change — a reference-typed `DefaultValue` is written now instead of being dropped.** When the parameter's type is a data interface or an object reference, `AddSetParameterEntry` and `AddSetParametersModule` used to **silently ignore** `DefaultValue`: the request succeeded and the entry was created with no default. Pass the value as an object path and it is now stored in the dedicated data-interface / object slot of `FNiagaraVariant`, where the reference is retained properly rather than packed into the byte payload the other parameter types use. What can come back instead of a success:
>
> - `CapabilityNotAvailable` — the session does not hold `NiagaraReferenceEdit` (granted in addition to `NiagaraStackEdit`, which both commands require anyway). The refusal names it.
> - `NotFound` — the object path names an asset nothing has loaded. A write never loads an asset as a side effect, so open the asset first; "does not exist" and "exists but is not loaded" are the same refusal.
> - `InvalidParams` — the object resolved, but it is not of the parameter type's class.
>
> With the capability granted and the target loaded, the write succeeds and the reference is kept. **Leaving `DefaultValue` unset behaves exactly as before** — no extra capability, and the entry is created with no default.
>
> ⚠️ **Only data interface types are reachable in practice.** The parameter type name is checked against a type allowlist before the value is ever looked at, so an ordinary object type such as `UTexture2D` is refused at that stage with `InvalidParams` naming the type, and `NiagaraReferenceEdit` never comes into play for it. Niagara *user* parameters (`AddUserVariables`) are a different store and take no default value at all.
>
> **⚠️ Behavior change — an unresolvable parameter type is refused instead of quietly becoming a float.** Both commands used to answer a type they could not resolve by creating the entry as a `float` and reporting success, so the only way to notice was to read the entry back and find a type you never asked for. They now return `InvalidParams` with the rejected type named. `AddSetParametersModule` refuses before the module is created, so a request whose second parameter is unresolvable no longer leaves a module holding only the entries that happened to resolve. The `ParsedAsDefault` / `ParsedAsDefaultArray` flags no longer fold in "the type did not resolve" — they report only that a value fell back to its type's default.
>
> A written default value **can** now be read back: `GetStackInputData` returns each input's current value, so a write to a Set Parameters entry can be confirmed.
>
> **Note — `AddSetParameterEntry` and `AddSetParametersModule` now also accept the bare type name a read reports for `TypePath`, on every engine version.** `TypePath` used to resolve only a short form (`float`, `Vector3f`) or a full object path (`/Script/Niagara.NiagaraFloat`). It now also resolves the bare name that a read's own `Type` field already reports — `NiagaraFloat`, `ENiagaraCoordinateSpace`, `NiagaraDataInterfaceCurve`, `Quat4f`, and so on — closing a round trip that did not exist before: a type name read from `GetModuleTopology`, `GetEmitterTopology`, `GetScriptStackTopology`, `GetStackInputTopology`, `GetStackInputSchema`, `GetModuleSchema`, `GetDynamicInputSchema`, `GetDynamicInputSchemaFromAsset` or `GetModuleSchemaFromAsset` can now be handed straight back into `TypePath`. **The set of types `TypePath` accepts is unchanged** — a bare name resolves through the registered Niagara type list and then the same allowlist the other two spellings already went through, so nothing that was unreachable before becomes writable; only the spelling widened. Both previous spellings keep resolving exactly as before, and a name that still does not resolve is still refused with `InvalidParams` naming it.

#### Blueprint wrappers (2)

| Command | Description |
|---|---|
| `ConstructNiagaraBPWrapperFromSystem` 🧩 | Generate an AActor Blueprint whose variables mirror the user variables of a NiagaraSystem asset (Two-Phase Commit) |
| `ConstructNiagaraBPWrapperFromComponent` 🧩 | Generate a Blueprint wrapper from a NiagaraComponent in the editor world, preserving component variable overrides (Two-Phase Commit) |

### Toolset bridges (45) 🧩

Mirror of native commands via the `NiagaraToolsets` plugin (UE 5.8+ Experimental). Provider: `Toolset.Editor.Niagara.*`. Groups: Info (2), Blueprint (2), System Schema (12), Topology (5), Data (5), Edit-1 (8), Edit-2 (8), Diagnostic (3).

> **⚠️ Breaking — `Toolset.Editor.Niagara.SetRendererData` now requires `NiagaraStackEdit`**, the capability its native counterpart reads. It used to require `NiagaraEmitterEdit`, so an operator who had closed `NiagaraStackEdit` could still perform the same write through the bridge. **A session granted only `NiagaraEmitterEdit` loses access to this command** — add `NiagaraStackEdit` instead.
>
> **The bridge does not run UAIP's value checks.** A bridge write happens inside the engine's toolset, so the type gate, the part-way-parse check and the all-or-nothing batching the native command applies do not reach it. Use the native `SetRendererData` when you want those checks.
>
> **⚠️ Breaking change — six of these bridge commands are no longer reachable, on any engine version: `GetScriptAssets`, `GetNiagaraParameterCollections`, `SetEmitterEnabled`, `SetEmitterName`, `DuplicateEmitter` and `MoveModule`.** The Niagara toolset these commands forward to declares no function under any of the six names, in any engine version this plugin supports, so the forwarded call could never reach an implementation — each used to fail at execution time with a generic `ExecutionFailed` no matter what was asked. All six now report `Available: false` from `UAIP.Core.DescribeCommand` and `uaip_list_commands`, with `UnavailableReason: "HandlerUnavailable"` and `UnavailableDetail: "DelegationTargetMissing"`. Calling any of them by name still fails, now with `PolicyViolation` and the same explanation in `ErrorMessage`.
>
> **Four of the six have a working native alternative**: `UAIP.Editor.Niagara.GetScriptAssets`, `GetNiagaraParameterCollections`, `SetEmitterEnabled` and `SetEmitterName` perform the same operations without delegating, and are unaffected by this change.
>
> **`DuplicateEmitter` and `MoveModule` do not.** Their native counterparts are themselves unavailable, for an unrelated reason (see the breaking-change note under [Editing](#editing-21) above): the engine-side APIs they need are never exported to a plugin, on any engine version. **As of this update, neither operation has a working path anywhere in this plugin** — not through the native command, and not through this bridge.
>
> **`GetSystemInfo` joins them as a seventh.** Checking every bridge command's delegation pair found that `Toolset.Editor.Niagara.GetSystemInfo` has no target either: the toolset declares `GetSystemSummary` and `GetSystemData`, neither of which returns the shape this command's callers are promised. It now reports `Available: false` with `UnavailableDetail: "DelegationTargetMissing"`. **`UAIP.Editor.Niagara.GetSystemInfo`** performs the same operation natively.
>
> **`GetAssetDiscoveryInfo`, by contrast, now works.** It delegated to `NiagaraToolset_Info` while the tool itself lives on `NiagaraToolset_Assets`, and the ToolsetRegistry resolves a call with one exact lookup, so it never arrived. The target has been corrected.

---

## UAIP.Editor.Physics

Physics Asset editing — bodies, shapes, constraints.

### Native (31)

#### Asset / observation (3)

| Command | Description |
|---|---|
| `CreatePhysicsAsset` | Generate and link a Physics Asset from a SkeletalMesh |
| `GetPhysicsAssetSummary` | Body / constraint counts and issue summary |
| `ValidatePhysicsAsset` | Detect orphan constraints, shapeless bodies, etc. |

#### Bodies (15)

| Command | Description |
|---|---|
| `GetBodyNames` | List body names in the Physics Asset |
| `AddBody` | Add a body to the specified bone |
| `RemoveBody` | Remove a body (cascades constraint deletion) |
| `GetBodyPhysicsMode` | Get a body's PhysicsMode (Default / Kinematic / Simulated) |
| `SetBodyPhysicsMode` | Set a body's PhysicsMode |
| `SetAllBodiesPhysicsMode` | Bulk-set PhysicsMode for bodies matching a name pattern |
| `GetBodyMassScale` | Get a body's MassScale |
| `SetBodyMassScale` | Set a body's MassScale |
| `GetBodyCollisionProfile` | Get a body's Collision Profile name |
| `SetBodyCollisionProfile` | Set a body's Collision Profile |
| `SetBodyLinearDamping` | Set a body's Linear Damping |
| `SetBodyAngularDamping` | Set a body's Angular Damping |
| `GetBodyOffset` | Get a body's center-of-mass offset (COMNudge) |
| `SetBodyOffset` | Set a body's center-of-mass offset |
| `MirrorBodies` | Mirror-copy left / right bone bodies and shapes by naming convention |

#### Shapes (8)

| Command | Description |
|---|---|
| `GetBodyShapes` | List collision shapes of a body (with ShapeName) |
| `SetSphere` | Set a body's shape to Sphere |
| `SetCapsule` | Set a body's shape to Capsule |
| `SetBox` | Set a body's shape to Box |
| `RemoveShape` | Remove a shape by ShapeName |
| `RegenerateBodyShapes` | Auto-regenerate shapes from bone geometry |
| `CopyBodyShapes` | Copy shapes from one bone to another |
| `SetPhysicalMaterial` | Set Physical Material on a body or all bodies |

#### Constraints (5)

| Command | Description |
|---|---|
| `GetConstraints` | Get all constraints in the asset (max 256) |
| `ListConstraintsForBody` | Get constraints attached to a specific bone (max 256) |
| `AddConstraint` | Add a rigid-body constraint |
| `SetConstraintLimits` | Set a constraint's angular limits |
| `RemoveConstraint` | Remove a constraint |

### Toolset bridges (17) 🧩

Mirror of native commands via the `PhysicsToolsets` plugin (UE 5.8+ Experimental). Provider: `Toolset.Editor.Physics.*`.

---

## UAIP.Editor.Dataflow 🧩

Dataflow graph editing. Requires `DataflowEditor` plugin.

| Command | Description |
|---|---|
| `GetDataflowGraphInfo` 🧩 | Get graph nodes / edges / variables (JSON). Each node reports both `NodeName` (its actual name within the graph — this is what `SetGroomDataflowAsset`'s `TerminalNodeName` and similar fields expect) and `DisplayName` (the node type's display name) |
| `ListDataflowNodeTypes` 🧩 | List available Dataflow node types |
| `AddDataflowNode` 🧩 | Add a node to a Dataflow graph. An optional `NodeName` sets its name within the graph; when omitted, a unique name is derived from the node type. The resulting name is reported back in the response's `NodeName` |
| `RemoveDataflowNode` 🧩 | Remove a node from a Dataflow graph |
| `ConnectDataflowPins` 🧩 | Connect two pins |
| `DisconnectDataflowPins` 🧩 | Disconnect a pin connection |
| `ListDataflowVariables` 🧩 | List graph variables |
| `GetDataflowNodeProperty` 🧩 | Read a node's `EditAnywhere` property value (primitives / enum / FName / FString / simple structs) |
| `SetDataflowNodeProperty` 🧩 | Write a node's `EditAnywhere` property value. Domain-agnostic — used by Cloth Weight Map / simulation config nodes among others. References, structs and containers are written through `ValueJson`, with a single container element addressed by `Operation` / `ElementIndex` / `ElementKeyJson` — see [Writing references, structs and containers](#writing-references-structs-and-containers). A write that touches a reference requires `DataflowReferenceEdit` on top of `DataflowGraphEdit`; a struct or container requires `PropertyStructuredEdit` as well. A hard reference (e.g. `TObjectPtr<UGroomAsset>`) is the object path of an **already-loaded** asset, since a property write never loads an asset as a side effect; soft references are validated against the asset registry and do not need the target loaded |

### Toolset bridges — Dataflow (7) 🧩

Bridge commands via the `DataflowAgentToolset` (UE 5.8+). Provider: `Toolset.Editor.DataflowAgent.*`. Editing commands require `DataflowGraphEdit`.

> **None of the 7 commands in this section worked until this update.** They passed the toolset name **unqualified, as `DataflowAgentToolset`**, which does not match the registered `DataflowAgent.DataflowAgentToolset` (the ToolsetRegistry resolves a call with one exact lookup). `ConnectDataflowPins` and `DisconnectDataflowPins` also had the wrong tool name — the toolset declares them as `ConnectNodePins` and `DisconnectNodePins`. **All seven have been corrected and now work.**

| Command | Description |
|---|---|
| `Toolset.Editor.DataflowAgent.ListDataflowNodeTypes` | List available Dataflow node types (common types only) |
| `Toolset.Editor.DataflowAgent.GetDataflowGraphInfo` | Node and connection structure of a Dataflow asset |
| `Toolset.Editor.DataflowAgent.ListDataflowVariables` | List variables defined in a Dataflow asset |
| `Toolset.Editor.DataflowAgent.AddDataflowNode` | Add a node to a Dataflow graph (requires `DataflowGraphEdit`) |
| `Toolset.Editor.DataflowAgent.RemoveDataflowNode` | Remove a node from a Dataflow graph (requires `DataflowGraphEdit`) |
| `Toolset.Editor.DataflowAgent.ConnectDataflowPins` | Connect two pins (requires `DataflowGraphEdit`) |
| `Toolset.Editor.DataflowAgent.DisconnectDataflowPins` | Disconnect pins (requires `DataflowGraphEdit`) |

---

## UAIP.Editor.ChaosClothAsset 🧩

Chaos Cloth Asset editing and `ChaosClothAssetToolset` bridge (UE 5.8, Experimental). Requires the `ChaosClothAsset` plugin family.

| Command | Description |
|---|---|
| `CreateClothingAsset` | Create a Clothing Asset from a Skeletal Mesh |
| `AssignClothingToSection` | Bind a Clothing Asset to a Skeletal Mesh LOD/section |
| `RemoveClothingFromSection` | Unbind a Clothing Asset from a section (destructive, irreversible) |
| `ListClothingAssets` | List Clothing Assets bound to a Skeletal Mesh |
| `GetSectionClothing` | Get the Clothing Asset bound to a specific LOD/section |
| `ConvertClothingAssetCommonToChaosClothAsset` | Convert a legacy `UClothingAssetCommon` to `UChaosClothAsset` (Experimental, LOD0 only) |
| `GetClothAssetInfo` | Read LOD count, Sim/Render Mesh vertex counts, the referenced `UDataflow` asset path, and Weight Map attribute names |
| `SetClothWeightMapVertexValues` | Directly set a Weight Map node's per-vertex weight array (destructive) |
| `SetClothMeshImportSource` | Set the imported SkeletalMesh/StaticMesh reference on an Import Dataflow node (`SkeletalMeshImport`/`StaticMeshImport`). The node kind is auto-detected; overwriting an existing reference requires `AllowOverwrite` (destructive) |
| `CreateLegacyClothingAsset` | Create a new legacy `UClothingAssetCommon` by extracting the simulation mesh from an existing SkeletalMesh render section |

`GetClothAssetInfo` returns the Cloth Asset's `UDataflow` reference path — feed it to `UAIP.Editor.Dataflow.*` commands to edit Weight Map / simulation config node properties generically.

### Toolset bridge

Mirror of the 6 `ChaosClothAssetToolset` functions. Provider: `Toolset.Editor.ChaosClothAsset.*`. Available only on UE 5.8+ with `ChaosClothAssetToolset` + `ToolsetRegistry` enabled.

| Command | Description |
|---|---|
| `Toolset.Editor.ChaosClothAsset.CreateClothingAsset` | Passthrough to `ChaosClothAssetToolset` |
| `Toolset.Editor.ChaosClothAsset.AssignClothingToSection` | Passthrough to `ChaosClothAssetToolset` |
| `Toolset.Editor.ChaosClothAsset.RemoveClothingFromSection` | Passthrough to `ChaosClothAssetToolset` |
| `Toolset.Editor.ChaosClothAsset.ListClothingAssets` | Passthrough to `ChaosClothAssetToolset` |
| `Toolset.Editor.ChaosClothAsset.GetSectionClothing` | Passthrough to `ChaosClothAssetToolset` |
| `Toolset.Editor.ChaosClothAsset.ConvertClothingAssetCommonToChaosClothAsset` | Passthrough to `ChaosClothAssetToolset` |

---

## UAIP.Editor.Skeleton

Skeleton and SkeletalMesh editing.

| Command | Description |
|---|---|
| `GetSkeletonInfo` | USkeleton bone hierarchy, sockets, virtual bones (JSON, read-only) |
| `AddSocket` | Add a socket to a specified bone |
| `RemoveSocket` | Remove a socket |
| `SetSocketTransform` | Partially update a socket's transform (omitted fields preserve existing values) |
| `AddVirtualBone` | Add a virtual bone (auto-named if name omitted) |
| `RemoveVirtualBone` | Remove a virtual bone |
| `GetSkeletalMeshInfo` | USkeletalMesh LODs, material slots, related Skeleton path (read-only) |
| `SetSkeletalMeshMaterial` | Assign a material to a slot on a SkeletalMesh |
| `CreateBlendProfile` | Create a BlendProfile on a Skeleton — `Mode` is `TimeFactor`, `WeightFactor`, or `BlendMask` (use `BlendMask` when the profile will be assigned to a `LayeredBoneBlend` node's `BlendMasks`; the other two modes are silently ineffective there) |
| `SetBlendProfileBoneScale` | Set the blend scale of one bone within an existing BlendProfile |
| `ListBlendProfiles` | List every BlendProfile currently registered on a Skeleton (read-only) |

> **Note**: for every write command in this domain, a path that satisfies the `/Game/` prefix check but fails deeper validation (`..` path traversal, over 512 characters, an invisible control character, or a malformed package name) answers `NotAllowed` rather than `NotFound`. This is not a breaking change — such paths never succeeded before either, and the previous error code for this specific edge case was never documented — but note it if your tooling matches on `ErrorCode` for path rejections.

---

## UAIP.Editor.MetaHuman 🧩

MetaHuman character authoring — asset creation, body / skin / eye / makeup settings, face sculpting, conforming and fitting, cloud rigging, texture synthesis, wardrobe, preview, and the asset build pipeline. Requires the `MetaHumanCharacter` plugin; if it is not enabled none of these commands are registered.

Editing commands open a MetaHuman edit session on demand and keep it open, so a run of commands against the same character does not pay the cost of reopening it. Because opening a session is itself an edit-mode entry, **most reads in this domain are not read-only**: they require `MetaHumanEdit` and are refused while the safety policy is in read-only mode. Call `ReleaseEditSession` once a run is finished. The only exception is `GetViewportSettings`, which requires just `EditorInspect`.

**⬆️ = UE 5.8+ only.** 14 of the 56 commands below depend on engine APIs that do not exist on UE 5.7. They are still registered there, but the default `uaip_list_commands` response omits them — they are counted in `HiddenCount` and `HiddenReasons.HandlerUnavailable` instead. Pass `IncludeUnavailable=true` to list them explicitly (each entry shows `Available: false`). `uaip_describe_command` continues to show them regardless of this filter. Calling one returns `PolicyViolation` (not `CommandNotFound`). Every command without the mark works on both UE 5.7 and UE 5.8. This symbol is used only in this section.

### Native (56)

#### Creation (1)

| Command | Description |
|---|---|
| `CreateMetaHumanCharacter` | Create a new MetaHuman character asset from the default template and write it to disk (package path must be under `/Game/`; requires `MetaHumanAssetCreate`) |

#### Body, skin and eyes (8)

| Command | Description |
|---|---|
| `GetBodyConstraints` | List every body constraint with its target measurement, whether it takes part in the body solve, and its accepted range (JSON artifact). Names are data driven — call this before `SetBodyConstraints` |
| `SetBodyConstraints` | Update named body constraints and re-evaluate the body (unnamed constraints keep their values; every entry is validated before any is applied) |
| `GetBodyShape` | Read the simplified body shape — masculine/feminine, body fat and muscularity as 0..1 values, plus height in cm |
| `SetBodyShape` | Set the simplified body shape and re-evaluate the body (omitted values unchanged; out-of-range values are rejected, not clamped) |
| `GetSkinSettings` | Read the complete skin settings — tone (lightness / redness), texture variant indices, roughness, palms and nails, freckles, per-region tone accents |
| `SetSkinTone` | Set only the two skin tone axes (lightness / redness); every other skin setting is left unchanged |
| `GetEyeSettings` | Read both eyes in full — Iris, Pupil, Cornea and Sclera groups |
| `SetEyeColor` | Write one temperature / brightness pair into the primary and secondary iris colour of both eyes |

#### Appearance detail (8)

| Command | Description |
|---|---|
| `SetSkinSettings` | Partial update of the full skin settings (omitted fields keep their values; out-of-range values are rejected, not clamped) |
| `GetMakeupSettings` | Read the makeup settings — foundation layer, eye makeup, blush, lip makeup |
| `SetMakeupSettings` | Partial update of the makeup settings (style names must match the engine's own names exactly) |
| `GetHeadModelSettings` | Read eyelash style and colouring plus the full set of teeth shape and colour values |
| `SetHeadModelSettings` | Partial update of the head model settings |
| `SetEyeSettings` | Partial update of the eyes, each eye addressed separately across the Iris / Pupil / Cornea / Sclera groups |
| `GetFaceEvaluationSettings` | Read overall face deviation, fine surface detail deviation and uniform head scale |
| `SetFaceEvaluationSettings` | Partial update of the face evaluation settings |

#### Face sculpting (9)

| Command | Description |
|---|---|
| `GetFaceModelCoefficients` ⬆️ | Read the underlying face model coefficients as a flat number array (JSON artifact); pass the same array back to restore the shape |
| `SetFaceModelCoefficients` ⬆️ | Write the face model coefficients (the array length must match `GetFaceModelCoefficients` exactly; any other length is rejected) |
| `GetFaceLandmarks` | Read the face landmark positions as a JSON artifact; an entry's index in the array is what `TranslateFaceLandmarks` expects |
| `TranslateFaceLandmarks` | Move the named face landmarks by matching deltas (all-or-nothing — if any entry is rejected, nothing is applied) |
| `CommitFaceState` | Commit the accumulated sculpting edits onto the asset; the sculpting commands do not commit on their own |
| `ImportFaceFromDna` | Replace the face from a `.dna` file that must live inside the project directory (requires `MetaHumanFileImport`) |
| `ImportFaceFromTemplate` | Fit the face to a template head mesh whose topology matches a MetaHuman head |
| `ImportFaceFromIdentity` | Fit the face to the conformed mesh of a MetaHuman Identity asset (the identity must already be conformed) |
| `CompareFaceState` | Report whether every corresponding vertex and vertex normal of two characters is within `Tolerance` (a single boolean; no per-vertex breakdown) |

#### Conforming and fitting (10)

| Command | Description |
|---|---|
| `GetMeshDataForConforming` ⬆️ | Read a Static / Skeletal Mesh's vertices and triangle indices into a JSON artifact, in the form the conforming commands take as a target |
| `ConformBodyToTarget` | Reshape the body to the supplied vertices, optionally deriving hand and foot joints (target given as `MeshDataArtifactId` or inline `Vertices`) |
| `ConformFaceToTargetMeshes` ⬆️ | Start an asynchronous solve that reshapes the character towards the target meshes; success means it started — poll `GetAsyncConformState` |
| `AlignToTargetMeshes` ⬆️ | Start a rigid alignment (move / rotate / scale, no shape change) onto the target meshes; run before `ConformFaceToTargetMeshes` |
| `RefineVerticesToTarget` ⬆️ | Start a refinement pass that pulls vertices past what the parametric model alone can express; run after the conform has finished |
| `CommitPosedStateAsAPose` ⬆️ | Evaluate the conformed body in the MetaHuman A pose and rebuild the face state from it, so the result can be posed and animated normally |
| `FitStateToTargetVertices` | One-pass fit of the head to target vertices in MetaHuman head topology and vertex order (no iterative solve) |
| `FitFaceFromBodyWithEyesTeethTemplate` ⬆️ | Rebuild the head from the current body shape, taking eyes and teeth from the supplied template meshes |
| `FitFaceFromBodyWithEyesTeethDna` ⬆️ | Same, taking eyes and teeth from a face DNA file — the head shape still comes from the body, so this is not a face import (requires `MetaHumanFileImport`) |
| `GetAsyncConformState` ⬆️ | Report whether a conform / alignment / refinement is still running; the engine offers no completion event, so poll this until `bIsRunning` is false |

#### Build pipeline (6)

| Command | Description |
|---|---|
| `RequestTextureSources` | Start high resolution face texture synthesis and return once the request is in flight; the work runs for minutes in the background (requires `MetaHumanTextureSynthesis`) |
| `GetTextureSourceState` | Poll whether texture synthesis is still running and whether the character already holds synthesized textures |
| `RequestAutoRigging` | Start face rig generation. ⚠️ **Uploads the character's face data to Epic's cloud rigging service** — the rig is produced remotely and downloaded back, so this requires a signed-in Epic account and network access, and the character data leaves the machine. Rigging usually takes minutes; poll `GetRiggingState` (requires `MetaHumanCloudRigging`) |
| `GetRiggingState` | Poll the rigging state — `Unrigged` / `RigPending` / `Rigged`. `Unrigged` once the request has stopped running means it failed (usually sign-in or connectivity) |
| `CanBuildMetaHuman` | Report whether `BuildMetaHuman` would accept this character and, when it would not, the first unmet requirement. Call this before every build |
| `BuildMetaHuman` | Assemble the character into a collection, an instance and a character blueprint under a new subfolder. ⚠️ **Occupies the game thread for the entire build (seconds to minutes).** The engine shows a progress dialog and keeps redrawing, so the editor stays usable to look at rather than going unresponsive, but no other command runs until the build returns. Long builds can exceed the HTTP transport's own async command timeout (120 s); when that happens the call returns `Timeout` even though **the build may still be running inside the editor**. Don't re-issue the command immediately — call `uaip_get_editor_status` first and follow `RecommendedAction` (expect `WAIT`), and expect the build's artifacts to appear only once it actually finishes. Call `CanBuildMetaHuman` first; a build without auto-rigging and synthesized textures always fails. On failure the assets created under the output folder are deleted; the output folder must not already exist. Other MetaHuman commands are refused while a build runs (requires `MetaHumanBuild`) |

#### Preview (3)

| Command | Description |
|---|---|
| `GetViewportSettings` | Read the preview viewport settings — lighting environment, light rotation, background colour, level of detail, hair cards vs strands, preview skin material and camera framing (read-only; requires only `EditorInspect`) |
| `SetViewportSettings` | Partial update of the preview viewport settings (at least one setting must be supplied; out-of-range values are rejected, not clamped). `PreviewMaterial` is named as the editor's viewport toolbar labels it — **pick `Skin` before capturing an image to check a colour**, because `Topology` is a topology visualisation that hides skin, makeup and eye colour entirely, and `Clay` is untextured grey. `CameraFrame` is always recorded on the character, but the preview camera only moves while the character is open in the MetaHuman character editor. A custom lighting environment cannot be selected here — the two supported engine versions describe one differently, so it is set in the editor's viewport toolbar instead |
| `RefreshCharacterPreview` ⬆️ | Propagate pending collection edits back onto the character and re-run the editor pipeline so the preview reflects them |

#### Wardrobe (10)

| Command | Description |
|---|---|
| `ListWardrobeSlots` | List the wardrobe slots the character's collection defines with the number of items in each; names come from the pipeline at runtime, so call this before `AssignWardrobeItem` |
| `ListWardrobeItems` | List the wardrobe items, optionally for one slot; each entry carries the opaque `ItemKey` handle |
| `GetWardrobeItemInfo` | Read one wardrobe item — the slot it occupies, its display name and the package path of the asset it wraps |
| `AssignWardrobeItem` ⬆️ | Assign an asset (groom, garment, …) to a wardrobe slot, select it and rebuild the preview — no separate `RefreshCharacterPreview` needed |
| `RemoveWardrobeItem` ⬆️ | Remove a wardrobe item, clearing the slot selection first when the character is wearing it, then rebuild the preview |
| `ReplaceWardrobeItem` ⬆️ | Replace a wardrobe item with a different asset in the slot the outgoing item occupied, then rebuild the preview |
| `GetWardrobeItem` | Read one wardrobe item asset addressed by package path — the package path of its principal asset, the class path of its pipeline, its thumbnail texture and thumbnail name, and whether it is an asset in its own right. This is the item asset itself, not an item a character is wearing — for that use `GetWardrobeItemInfo`, which takes a character path and an `ItemKey` instead |
| `SetWardrobeItem` | Partial update of a wardrobe item asset's principal asset, thumbnail texture and thumbnail name (omitted fields keep their values, but at least one must be supplied; an empty string in either path field clears that reference rather than naming an asset). The pipeline is not settable here — use `SetWardrobeItemPipeline` |
| `SetWardrobeItemPipeline` | Give a wardrobe item asset a pipeline of the named class, replacing whatever pipeline it had; `PipelineClassPath` is a class path, so take one from `ListItemPipelineClasses` rather than assembling it |
| `ListItemPipelineClasses` | List the item pipeline classes a wardrobe item asset may be built through, with their display names. Which classes exist depends on the plugins the project has loaded; abstract, deprecated and hot-reload superseded classes are left out, so every class listed is one `SetWardrobeItemPipeline` accepts |

#### Session (1)

| Command | Description |
|---|---|
| `ReleaseEditSession` | Release the edit session held open for a character; the call never aborts work that is still in flight |

### Toolset bridges (9) 🧩

Bridge commands via the `MetaHumanGenerator` Python toolset. Provider: `Toolset.Editor.MetaHuman.*`. Available only on UE 5.8+ with `MetaHumanGenerator` + `ToolsetRegistry` enabled — on UE 5.7 the bridge provider is not registered at all, so these names return `CommandNotFound`. Marked `Stability: Experimental` because the underlying engine Python toolset is itself experimental.

Unlike the native commands, every bridge command except `Create` needs an explicit session reference from `BeginEdit`, which also means none of them can run while the safety policy is read-only. All require `MetaHumanEdit`, except `Create` which requires `MetaHumanAssetCreate`.

| Command | Description |
|---|---|
| `Toolset.Editor.MetaHuman.BeginEdit` | Open an edit session on a character and return the session reference the other bridge commands take |
| `Toolset.Editor.MetaHuman.EndEdit` | Close a session opened by `BeginEdit` and take the character out of the editor's edit set |
| `Toolset.Editor.MetaHuman.GetBodyShape` | Return the four simplified body shape values of the session's character |
| `Toolset.Editor.MetaHuman.SetBodyShape` | Set the four simplified body shape values and commit, including the neck region rebuild (out-of-range values are clamped by the toolset rather than refused — the one behavioural difference from the native command) |
| `Toolset.Editor.MetaHuman.GetSkinTone` | Return lightness and redness of the session's character |
| `Toolset.Editor.MetaHuman.SetSkinTone` | Set lightness and redness and commit the skin settings; the rest of the skin settings are left as they are |
| `Toolset.Editor.MetaHuman.GetEyeColor` | Return temperature and brightness, read from the right eye's primary iris colour |
| `Toolset.Editor.MetaHuman.SetEyeColor` | Set one eye colour on both eyes and commit the eye settings, so the two eyes always end up matching |
| `Toolset.Editor.MetaHuman.Create` | Create a new MetaHuman character asset under `/Game/` and return a reference to it (requires `MetaHumanAssetCreate`) |

---

## UAIP.Editor.DataTable

DataTable row management and import / export.

| Command | Description |
|---|---|
| `ListDataTableRows` | List row keys in a DataTable |
| `AddDataTableRow` | Add a new row |
| `DeleteDataTableRow` | Delete a row |
| `DuplicateDataTableRow` | Duplicate a row |
| `ImportDataTableFromCSV` | Bulk-import a CSV string (Replace / Merge modes) |
| `ExportDataTableToCSV` | Export a DataTable as a CSV artifact |
| `GetDataTableRowStruct` | Get the row struct (UScriptStruct) field definitions |
| `ListDataTableRowStructs` | List `FTableRowBase`-derived structs usable as row structs — feed `ClassPath` to `CreateAsset` as `FactoryParams.RowStructPath` |

---

## UAIP.Editor.AnimBlueprint

Anim Blueprint graph and StateMachine editing.

| Command | Description |
|---|---|
| `GetAnimBlueprintInfo` | AnimGraph node list and StateMachine structure (degraded mode during PIE). Optional `IncludePins` (default false) adds a `Pins[]` array to each node entry; omitting it leaves the output unchanged from before |
| `GetAvailableAnimGraphNodeClasses` | List `UAnimGraphNode_Base` subclasses — feed `ClassPath` to `AddAnimGraphNode` |
| `AddAnimGraphNode` | Add a `UAnimGraphNode_Base` derived node by NodeClass — a project- or plugin-defined class needs a capability, see the note below |
| `RemoveAnimGraphNode` | Remove a node by NodeId |
| `ConnectAnimGraphPins` | Connect two pins (WouldCreateCycle DFS pre-detection) |
| `DisconnectAnimGraphPins` | Disconnect a pin connection |
| `AddAnimState` | Add a State to a StateMachine |
| `RemoveAnimState` | Remove a State by NodeId |
| `AddAnimTransition` | Add a From→To Transition (idempotent on duplicates) |
| `RemoveAnimTransition` | Remove a Transition by NodeId |
| `CompileAnimBlueprint` | Compile and return CompileStatus + error log |
| `SetAnimGraphNodeProperty` | Write an `EditAnywhere` property on an AnimGraph node by dot-notation `PropertyPath`. References go through `ValueJson` and `AnimBlueprintReferenceEdit`, structs / containers through `PropertyStructuredEdit` — see [Writing references, structs and containers](#writing-references-structs-and-containers). When the property is exposed as a pin and nothing is connected to it, the pin's default is brought in step with the write, so the value survives the next compile; a connected pin is left alone |
| `GetAnimGraphNodeDetails` | Pin and property details for a single AnimGraph node (read-only; secret values report `IsSecret: true` with `Value` omitted) |
| `AddAnimGraphNodePosePin` | Add one dynamic pose input pin to a node that supports it (currently only `UAnimGraphNode_LayeredBoneBlend`); non-idempotent |
| `RemoveAnimGraphNodePosePin` | Remove one dynamic pose input pin by `PinIndex`; removing a pin renumbers the rest |
| `AddAnimLayerGraph` | Create a new self-contained Anim Layer graph on a root AnimBlueprint; refused on a derived AnimBlueprint |
| `RemoveAnimLayerGraph` | Remove a self-contained Anim Layer graph, and every `LinkedAnimLayer` node still referencing it when `RemoveReferencingNodes` is true |
| `ImplementAnimLayerInterface` | Implement a `UAnimLayerInterface`-derived interface, generating one layer graph per anim-layer function it declares. Requires `AnimBlueprintReferenceEdit` (writes a class reference into the implemented interface list) |
| `AddLinkedAnimLayerNode` | Place a `LinkedAnimLayer` node pointing at a self-contained layer, or (with `InterfacePath` set) at one of an already-implemented interface's layer functions — the latter additionally requires `AnimBlueprintReferenceEdit`. `TargetGraph` (name) or `GraphGuid` selects which graph the node lands in; see the note below the table |

> **Note — `AddLinkedAnimLayerNode`'s `TargetGraph` / `GraphGuid` (which graph the node lands in)**: `TargetGraph` (optional string; unset defaults to the first AnimGraph) and `GraphGuid` (optional string, `UEdGraph::GraphGuid`) are mutually exclusive — supplying both is `InvalidParams`. `TargetGraph` is looked up first among the AnimBlueprint's own AnimGraphs (the root graph plus its self-contained layers); only when nothing matches there does the lookup fall back to the layer graphs of already-implemented interfaces — so a self-contained layer never loses to an interface layer of the same name, and this fallback itself cannot report ambiguity against the self set (self graphs are checked exhaustively first). A name matching more than one graph within whichever set actually produced the match answers `InvalidParams` with `Result.MatchedGraphGuids` carrying every candidate's `GraphGuid`; pass one of those back as `GraphGuid` to disambiguate. Naming a graph that exists nowhere answers `NotFound`.
>
> **Note — `LayerName` / `InterfacePath` (which layer the node points at) is a separate resolution from `TargetGraph`**: `InterfacePath` unset searches only the AnimBlueprint's own self-contained layers for `LayerName`; `InterfacePath` set searches only that interface's own layer functions — never both, so this resolution has no self-vs-interface priority to apply. A `LayerName` matching more than one graph within that one set (self-contained layers are expected to be uniquely named, as are one interface's own layer functions) is `InvalidParams` with `Result.MatchedGraphGuids`, same as above; this is a defensive check for a name collision the engine is not expected to allow, not a routine occurrence.
>
> **Note — project- and plugin-defined AnimGraph node classes are capability-gated**: a `NodeClass` from one of the three modules this domain has always trusted (`AnimGraph`, `AnimGraphRuntime`, `Engine`) is added the same way as before. A class outside those modules — a project- or plugin-defined `UAnimGraphNode_Base` subclass — now requires `AnimBlueprintCustomTypeEdit`. Unlike Material, there is no companion "dangerous node" capability here: eight node kinds (`UAnimGraphNode_StateResult`, `TransitionResult`, `TransitionPoseEvaluator`, `Root`, `StateMachineBase`, `LinkedAnimGraph`, `LinkedAnimLayer`, `CustomProperty`) cannot be placed at the AnimGraph root **regardless of any capability held** — they are internal- or sub-graph-only node kinds the graph does not accept from that direction, not a danger a capability grant unlocks. Neither `AnimBlueprintCustomTypeEdit` nor any other capability changes this outcome; see [Safety & Capabilities](safety.md#blueprint--anim-blueprint-editing).
>
> This check is not limited to `AddAnimGraphNode` — see [Capability-gated custom types](#capability-gated-custom-types) for how `AnimBlueprintCustomTypeEdit` is re-checked when an existing node of a gated class is edited, connected, disconnected, compiled, or deleted, and for the breaking change on delete / disconnect specifically.
>
> ⚠️ **Breaking change**: a project- or plugin-defined `NodeClass` used to be refused outright with `PolicyViolation`. `AddAnimGraphNode` now answers `CapabilityNotAvailable` and names `AnimBlueprintCustomTypeEdit` once the class is loaded. There is no compatibility window for the old code: it meant "no permission would have helped", so keeping it would describe a permission system that did not exist. The eight internal/sub-graph-only kinds above are unaffected by this change and keep returning `PolicyViolation`.
>
> `NodeClass` must already be loaded — `AddAnimGraphNode` no longer loads it as a side effect, and answers `NotFound` for a class it cannot resolve.

---

## UAIP.Editor.AnimBlueprint.UAF 🧩

The one command that embeds a Unified Animation Framework graph into an AnimBlueprint. Requires the Engine's `UAFAnimGraph` plugin (which itself requires `UAF`); if either is disabled this command is not registered.

**`Stability: Experimental`**, for the same reason as [UAIP.Editor.UAF](#uaipeditoruaf-).

| Command | Description |
|---|---|
| `AddUAFGraphNodeToAnimBlueprint` | Place a `UAnimGraphNode_AnimNextGraph` node into `TargetGraph` (defaulting to the first AnimGraph), or the graph named by `GraphGuid` instead — the two are mutually exclusive — pointing at a `UUAFAnimGraph` asset given by `UAFGraphPath`. `UAFGraphPath` must already be loaded in this editor — it is never force-loaded, and only resolved after every required capability is confirmed. Requires `AnimBlueprintGraphEdit`, `AnimBlueprintReferenceEdit`, and `AnimBlueprintCustomTypeEdit` (the node class comes from a module this domain does not ship). Not allowed during Play-in-Editor |

> **Note — `TargetGraph` / `GraphGuid` ambiguity**: `TargetGraph` is looked up only among the AnimBlueprint's own AnimGraphs (the root AnimGraph and its self-contained layers) — unlike `AddLinkedAnimLayerNode`, it never falls back to an implemented interface's layer graphs. A name matching more than one of the AnimBlueprint's own graphs answers `InvalidParams` with `Result.MatchedGraphGuids` carrying every candidate's `GraphGuid`; pass one of those back as `GraphGuid` to disambiguate. Naming a graph that does not exist answers `NotFound`.

---

## UAIP.Editor.UAF 🧩

Editing and inspection of Unified Animation Framework assets (`UUAFAnimGraph` / `UUAFSystem`) — RigVM graph nodes, pins, variables, and event graphs. Requires the Engine's own `UAF` plugin; if it is disabled none of these commands are registered.

**Every command in this section is `Stability: Experimental`**, because the underlying UAF plugin is itself an Experimental engine feature and its API may change without notice in a future engine release.

| Command | Description |
|---|---|
| `GetUAFAssetInfo` | Summary information about a UAF asset — asset class, entry count, degraded flag (read-only) |
| `ListUAFEntries` | List every entry (graphs, variables, shared variables, categories, …) stored in a UAF asset's editor data (read-only) |
| `ListUAFGraphs` | List every entry that carries a RigVM graph — animation graph entries, event graph entries, etc. (read-only) |
| `ListUAFNodes` | List all node names in the RigVM graph owned by a UAF asset entry (read-only) |
| `GetUAFNodeInfo` | Struct path and pin descriptions for a node in a UAF asset entry's RigVM graph (read-only) |
| `ListUAFPins` | All pin descriptions for a node in a UAF asset entry's RigVM graph (read-only) |
| `GetUAFPinValue` | The default value of a pin, addressed as `NodeName.PinName` (read-only) |
| `ListUAFVariables` | List every member variable of a UAF asset (read-only) |
| `GetUAFVariable` | Description of one named member variable (read-only) |
| `GetAvailableUAFUnitStructs` | List available `FRigUnit_AnimNextBase` substructs — feed `ClassPath` to `AddUAFGraphNode` as `StructPath`. Each entry carries `Admission` plus `RequiredCapabilities` / `MissingCapabilities`, so a struct that cannot be added yet still says what it would take |
| `AddUAFGraphNode` | Add a RigVM unit node via `StructPath` (resolved against structs already loaded, never loaded on demand); a struct outside the modules this domain ships requires `UAFCustomTypeEdit` |
| `RemoveUAFGraphNode` | Remove a RigVM node by name; requires `UAFCustomTypeEdit` when the removed node's struct is not one this domain ships |
| `ConnectUAFPins` | Connect an output pin to an input pin (`NodeName.PinName` format); requires `UAFCustomTypeEdit` when either endpoint's struct is not one this domain ships |
| `DisconnectUAFPins` | Disconnect an output pin from an input pin; same `UAFCustomTypeEdit` condition as `ConnectUAFPins` |
| `SetUAFPinValue` | Set the default value of a pin (UE text import notation). Requires `UAFCustomTypeEdit` when the owning node's struct is not one this domain ships, and `UAFReferenceEdit` when the pin's declared type is — or contains — an object / class reference |
| `AddUAFVariable` | Create a new member variable; `ValueType` / `ContainerType` name `EPropertyBagPropertyType` / `EPropertyBagContainerType` enumerators. Requires `UAFReferenceEdit` for a reference-typed variable |
| `RemoveUAFVariable` | Remove a member variable by name (`VariableNotFound` both when nothing of that name exists and when it exists but is not a variable) |
| `AddUAFEventGraph` | Add a new event graph entry rooted at the RigVM unit struct named by `StructPath`. `UUAFSystem` only — refused with `UnsupportedOperation` on `UUAFAnimGraph`, which has a single fixed animation graph entry and no room for one |
| `CompileUAFAsset` | Trigger a synchronous compile via `RequestAssetCompilation`, subject to per-session rate limiting (`MinCompileIntervalSeconds` between calls per asset) |

All nine mutating commands above require `UAFGraphEdit` as their static capability.

---

## UAIP.Editor.UAF.AnimGraph 🧩

One read-only command specific to UAF animation graph assets. Requires the Engine's `UAFAnimGraph` plugin (which itself requires `UAF`).

**`Stability: Experimental`**, for the same reason as [UAIP.Editor.UAF](#uaipeditoruaf-).

| Command | Description |
|---|---|
| `GetAvailableUAFTraits` | List available `FAnimNextTraitSharedData` substructs (UAF animation traits) — feed `ClassPath` to `AddUAFGraphNode` as `StructPath`. Same `Admission` / capability-preview shape as `GetAvailableUAFUnitStructs` |

---

## UAIP.Editor.SoundCue

SoundCue graph editing.

| Command | Description |
|---|---|
| `GetSoundCueInfo` | SoundCue graph nodes and connection topology (JSON) |
| `GetAvailableSoundCueNodeClasses` | Every `USoundNode` subclass this editor has loaded, whether or not this session may currently add one — feed a `NodeClass` value from the result as `AddSoundCueNode`'s `SoundNodeClass`. Each entry carries `Admission` (`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`) plus `RequiredCapabilities` / `MissingCapabilities`, from the same policy `AddSoundCueNode` validates against — a class from outside `/Script/Engine` is listed and names `SoundCueCustomTypeEdit` rather than being left out. Ordered by `NodeClass`; reports `TotalCount`, `ReturnedCount`, `Truncated` (max 200). `SchemaVersion` is `1`. Requires `EditorInspect` |
| `AddSoundCueNode` | Add a node by SoundNodeClass. Requires `SoundCueCustomTypeEdit` in addition to `SoundCueGraphEdit` when `SoundNodeClass` comes from outside `/Script/Engine` — see [Capability-gated custom types](#capability-gated-custom-types). ⚠️ **Changed** — `SoundNodeClass` is resolved against what this editor already has loaded and is never force loaded; an unresolvable path is `NotFound` where it used to be `InvalidParams` |
| `RemoveSoundCueNode` | Remove a node by NodeId (root deletion returns Conflict). Requires `SoundCueCustomTypeEdit` when the removed node's class is from outside `/Script/Engine` |
| `ConnectSoundCuePins` | Connect two pins (cycle / dynamic input pin auto-add). Requires `SoundCueCustomTypeEdit` when either endpoint's class is from outside `/Script/Engine`; the root output node owns no node class of its own and contributes nothing to this check |
| `DisconnectSoundCuePins` | Disconnect a pin connection (PinIndex=-1 disconnects all). Requires `SoundCueCustomTypeEdit` when the target node's class is from outside `/Script/Engine` |
| `SetSoundCueNodeProperty` | Set a SoundCue node property. Object / class / delegate references, structs and containers are no longer refused outright — they go in `ValueJson` and are gated by `PropertyReferenceEdit` / `PropertyStructuredEdit`, see [Writing references, structs and containers](#writing-references-structs-and-containers). Requires `SoundCueCustomTypeEdit` in addition when the target node's class is from outside `/Script/Engine` |
| `CompileSoundCue` | Rebuild the SoundNode tree from the graph. Never requires `SoundCueCustomTypeEdit`: it names no node class of its own, and the classes a cue already holds are judged by a separate, permission-free question this domain always answers the same way — a cue containing a project's own node stays compilable without it |

> ⚠️ **Breaking change — delete, connect, disconnect and property edits used to be ungated.** Before this capability existed, only `AddSoundCueNode` checked the node class being added; the other four mutating commands went through unconditionally, whatever class the node was. See [Capability-gated custom types](#capability-gated-custom-types) for the general rule this follows.

---

## UAIP.Editor.SoundSettings

SoundClass hierarchy, SoundAttenuation, and SoundMix asset property editing.

The three `Set*Settings` commands take the value in `Value` as engine text or in `ValueJson` as JSON, and address a single container element with `Operation` / `ElementIndex` / `ElementKeyJson` — see [Writing references, structs and containers](#writing-references-structs-and-containers).

| Command | Description |
|---|---|
| `GetSoundClassInfo` | Return SoundClass Properties (FSoundClassProperties), ChildClasses, ParentClass, and PassiveSoundMixModifiers as JSON |
| `SetSoundClassSettings` | Set one FSoundClassProperties field on a SoundClass asset (changing LoadingBehavior is rejected) |
| `ListSoundClasses` | Enumerate SoundClass assets in the project (AssetPath / ParentClassPath / ChildClassPaths; up to 1000) |
| `AddSoundClassChild` | Add a child class to the SoundClass hierarchy (cycle detection; depth limit 32) |
| `RemoveSoundClassChild` | Remove a child class from the SoundClass hierarchy and clear both directions of the link |
| `GetSoundAttenuationInfo` | Return FSoundAttenuationSettings of a SoundAttenuation asset as JSON |
| `SetSoundAttenuationSettings` | Set one FSoundAttenuationSettings field on a SoundAttenuation asset |
| `ListSoundAttenuations` | Enumerate SoundAttenuation assets in the project (up to 1000) |
| `GetSoundMixInfo` | Return all SoundMix settings (EQ, SoundClassEffects, fade timings) as JSON |
| `SetSoundMixSettings` | Set one top-level SoundMix field (direct write to SoundClassEffects array is rejected) |
| `SetSoundMixAdjuster` | Add or update a SoundClassAdjuster identified by SoundClass path (Upsert; omitted fields keep existing values or use engine defaults) |
| `RemoveSoundMixAdjuster` | Remove the SoundClassAdjuster for the specified SoundClass from a SoundMix |
| `ListSoundMixes` | Enumerate SoundMix assets in the project (up to 1000) |

---

## UAIP.Editor.MVVM 🧩

ViewModel Blueprint property management, View Binding / Event authoring, and Widget ViewModel wiring. Requires the `ModelViewViewModel` plugin (enabled by default since UE 5.5).

### Native (26)

#### ViewModel property management

| Command | Description |
|---|---|
| `ListViewModelClasses` | Enumerate `UMVVMViewModelBase`-derived Blueprint classes via AssetRegistry (optional `SearchPath` filter; up to 1000) |
| `AddViewModelProperty` | Add a property to a ViewModel Blueprint (7 property types; optional `DefaultValue`; optional getter / setter generation) |
| `RemoveViewModelProperty` | Remove a property from a ViewModel Blueprint by name |
| `ListViewModelProperties` | List all properties of a ViewModel Blueprint |

#### Widget ViewModel connection

| Command | Description |
|---|---|
| `AddViewModelToWidget` | Add a ViewModel to a WidgetBlueprint (must be a `/Game/`-rooted `UMVVMViewModelBase` subclass) |
| `RemoveViewModelFromWidget` | Remove a ViewModel entry from a WidgetBlueprint by name |
| `ListWidgetViewModels` | List ViewModels currently wired to a WidgetBlueprint |
| `RenameViewModelInWidget` | Rename a ViewModel entry inside a WidgetBlueprint |
| `ReparentViewModelInWidget` | Change the class of a ViewModel entry inside a WidgetBlueprint |

#### View Binding operations

| Command | Description |
|---|---|
| `AddViewBinding` | Add a View Binding to a WidgetBlueprint |
| `RemoveViewBinding` | Remove a View Binding from a WidgetBlueprint by `BindingId` |
| `ListViewBindings` | List all View Bindings in a WidgetBlueprint |
| `GetViewBinding` | Get details of a single View Binding by `BindingId` |
| `UpdateViewBinding` | Partially update fields of a View Binding |
| `SetViewBindingEnabled` | Enable or disable a View Binding |
| `SetViewBindingConversionFunction` | Set or clear the conversion function for a View Binding |
| `SetViewBindingExecutionMode` | Set the execution mode for a View Binding |
| `ListConversionFunctions` | List available conversion functions for a WidgetBlueprint (expensive on large projects — use `SearchPath` filter) |

#### View Event operations

| Command | Description |
|---|---|
| `AddViewEvent` | Add a View Event to a WidgetBlueprint (returns `EventId`; empty string on failure) |
| `RemoveViewEvent` | Remove a View Event from a WidgetBlueprint |
| `ListViewEvents` | List all View Events in a WidgetBlueprint |

#### ViewModel source settings

| Command | Description |
|---|---|
| `SetViewModelSource` | Change the `CreationType` of a ViewModel entry (Remove + Add round-trip; `Context` type requires UE 5.8+) |
| `GetViewModelSource` | Get the current source configuration of a ViewModel entry |

#### Observation / validation

| Command | Description |
|---|---|
| `GetWidgetBindableProperties` | List bindable properties of a WidgetBlueprint (widget properties and ViewModel properties) |
| `ValidateViewBindings` | Validate all View Bindings in a WidgetBlueprint (expensive on large projects) |
| `GetMVVMViewInfo` | Get the MVVM configuration summary of a WidgetBlueprint (`bMVVMConfigured: false` when MVVM is not configured) |

### Toolset bridges (9) 🧩

Bridge commands via the `MVVMToolset` plugin (UE 5.8+). Provider: `Toolset.MVVM.*`. `CreateViewModel` and `ListViewModels` are unique to this bridge; other commands mirror native equivalents.

| Command | Description |
|---|---|
| `Toolset.MVVM.CreateViewModel` | Create a ViewModel Blueprint asset |
| `Toolset.MVVM.AddViewModelProperty` | Add a property to a ViewModel Blueprint |
| `Toolset.MVVM.ListViewModels` | List ViewModel classes (by class-type filter) |
| `Toolset.MVVM.ListWidgetViewModels` | List ViewModels wired to a WidgetBlueprint |
| `Toolset.MVVM.AddViewModelToWidget` | Add a ViewModel to a WidgetBlueprint |
| `Toolset.MVVM.ListWidgetViewBindings` | List View Bindings of a WidgetBlueprint |
| `Toolset.MVVM.RemoveWidgetViewBinding` | Remove a View Binding from a WidgetBlueprint |
| `Toolset.MVVM.CreateViewBinding` | Create a View Binding in a WidgetBlueprint |
| `Toolset.MVVM.ListConversionFunctions` | List available conversion functions |

---

## UAIP.Editor.BehaviorTree

Behavior Tree graph editing and Blackboard key management.

| Command | Description |
|---|---|
| `GetBehaviorTreeNodeList` | Flat list of every node — `NodeGuid`, `NodeClass`, `DisplayName`, `Depth` (0 = root composite), `ParentNodeGuid`. Every node now also carries `ExecutionIndex` (the number the node has when the asset runs as the top-level tree, the same number a runtime response reports for it), or `null` with `ExecutionIndexUnavailableReason`. See [Matching a runtime node to the editor asset](#matching-a-runtime-node-to-the-editor-asset) |
| `GetBehaviorTreeSubtree` | Recursive subtree (Composite / Task / Decorator / Service) rooted at a `NodeGuid`, `MaxDepth` 1–32. Every node now also carries `ExecutionIndex` (the number the node has when the asset runs as the top-level tree, the same number a runtime response reports for it), or `null` with `ExecutionIndexUnavailableReason`. See [Matching a runtime node to the editor asset](#matching-a-runtime-node-to-the-editor-asset) |
| `GetAvailableBTCompositeClasses` | List `UBTCompositeNode` subclasses — feed `ClassPath` to `AddBehaviorTreeCompositeNode`. Each entry now carries `Admission` (`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`) plus `RequiredCapabilities` / `MissingCapabilities`, from the same policy the add command validates against. No longer filtered to the modules this domain ships. Ordered by `ClassPath`; reports `TotalCount`, `ReturnedCount`, `Truncated` (max 200). `SchemaVersion` is now `2` — see the note below |
| `GetAvailableBTTaskClasses` | List `UBTTaskNode` subclasses — feed `ClassPath` to `AddBehaviorTreeTaskNode`. Reports the same admission and count fields as above |
| `GetAvailableBTDecoratorClasses` | List `UBTDecorator` subclasses — feed `ClassPath` to `AddBehaviorTreeDecoratorNode`. Reports the same admission and count fields as above |
| `GetAvailableBTServiceClasses` | List `UBTService` subclasses — feed `ClassPath` to `AddBehaviorTreeServiceNode`. Reports the same admission and count fields as above |
| `AddBehaviorTreeCompositeNode` | Add a Composite node (Sequence / Selector / SimpleParallel) — a class from outside the modules this domain ships needs a capability, see the note below |
| `AddBehaviorTreeTaskNode` | Add a Task node by TaskClass — sub-tree runners and Blueprint-backed tasks additionally need their own capability, see the note below |
| `AddBehaviorTreeDecoratorNode` | Attach a Decorator to a parent node — same checks as above |
| `AddBehaviorTreeServiceNode` | Attach a Service to a parent Composite node — same checks as above |
| `RemoveBehaviorTreeNode` | Remove a node by NodeId — needs the same capabilities the node's own class asks for |
| `GetBehaviorTreeNodeProperties` | Every property a node's `NodeInstance` declares — `PropertyName`, `PropertyType` (the C++ type name), `PropertyValue` in the exact form `SetBehaviorTreeNodeProperty` accepts back for it, and a nested `WriteRequirements` object. A `FBlackboardKeySelector` property is reported as the bare key name, matching the write command's special-cased handling of it. The `ExecutionIndex` property it lists is a transient engine value that is never saved with the asset: it is filled in only after the tree has been opened in the BehaviorTree editor and reads 0 right after the asset is loaded, so to match runtime responses use the `ExecutionIndex` of `GetBehaviorTreeNodeList` / `GetBehaviorTreeSubtree` instead. Read-only; permitted during PIE (degraded mode). Requires `EditorInspect` |
| `SetBehaviorTreeNodeProperty` | Set a node property (FBlackboardKeySelector / generic ImportText_Direct). Needs the capabilities asked for by the class of the node being written **and** by the class that declares the property. A key-selector write is now refused when the tree has no Blackboard asset assigned — the key name cannot be validated without one, and the write used to leave a name and a type that did not match. A refused write no longer marks the asset dirty or leaves an empty undo entry |
| `ListBlackboardKeys` | List Blackboard asset keys (allowed during PIE) |
| `AddBlackboardKey` | Add a key (duplicate-name check). A key type outside `/Script/AIModule`, and the two key kinds that hold a reference the writer chooses, each need a capability — see the note below |
| `RemoveBlackboardKey` | Remove an unreferenced key (returns Conflict + referencers if in use) — needs the same capabilities the key's own type asks for |
| `SetBehaviorTreeBlackboard` | Change the Blackboard asset a BT references |
| `RequestBehaviorTreeAutoArrange` | Run the AutoArrange pass on an open BT editor |

> **Note — this domain gates types at three separate places, behind three capabilities**: the class of a node being placed or worked on, the class that declares a node property being written, and the class of a Blackboard key type being declared or removed. Each place has its own set of modules it has always accepted, and those sets are deliberately not the same.
>
> - **`BehaviorTreeCustomTypeEdit`** — required when the type comes from outside what this domain ships: `/Script/AIModule` or `/Script/AITestSuite` for a node class, `/Script/AIModule` or `/Script/Engine` for the class declaring a node property, and `/Script/AIModule` alone for a Blackboard key type. A project module, a plugin module (including an engine plugin such as `GameplayBehaviorSmartObjects`), or a Blueprint generated class all fall outside. One name covers all three places on purpose: it stands for a single permission — work with types this domain does not ship — and which place a project's own type is reached through is not something an operator granting that permission would want to decide separately.
> - **`BehaviorTreeExternalBehaviorNodeEdit`** — required for the five node kinds whose body is defined somewhere other than the class itself: `UBTTask_RunBehavior` and `UBTTask_RunBehaviorDynamic`, which execute a whole other Behavior Tree asset, and `UBTTask_BlueprintBase` / `UBTDecorator_BlueprintBase` / `UBTService_BlueprintBase`, whose subclasses carry a graph authored in the editor. Matched by inheritance, not by name.
> - **`BlackboardReferenceKeyTypeEdit`** — required for the two key kinds whose stored value is a reference the writer gets to choose: `UBlackboardKeyType_Object`, which accepts any object in the project, and `UBlackboardKeyType_Class`, which names a class and has the engine resolve it. Also matched by inheritance.
>
> None is granted by default; see [Safety & Capabilities](safety.md#ai-systems).
>
> ⚠️ **A Blueprint-authored Behavior Tree node needs two capabilities, not one.** It is both a class this domain does not ship and a class whose body is a graph, so `BehaviorTreeCustomTypeEdit` and `BehaviorTreeExternalBehaviorNodeEdit` are required **together**; holding one leaves the request refused, naming the other as still missing. The same applies to a project-defined subclass of `UBlackboardKeyType_Object`, which needs `BehaviorTreeCustomTypeEdit` and `BlackboardReferenceKeyTypeEdit`. This domain is the second after Material where two capabilities can apply to one type, and it is the case most likely to surprise: an operator who grants only the custom-type capability will still be refused for every Blueprint node the project defines.
>
> **Rebuilding a tree is never gated by the classes it already contains.** Adding or removing a main node rewrites the tree's node template chain afterwards, and that rewrite asks nothing for the classes already sitting in the asset — otherwise a tree holding one node class of the project's own could never be edited without a grant. Only the class a request *names*, and the nodes a request *acts on*, are gated. The same holds for Blackboard key types: declaring a key describes the shape of a slot, so a Behavior Tree naming a Blackboard that has an object key stays editable without `BlackboardReferenceKeyTypeEdit`.
>
> **Nothing here is refused by the engine after authorization.** Unlike Material and ControlRig, this domain has no per-class engine predicate to consult: the Behavior Tree editor answers whether a graph is a Behavior Tree graph rather than whether a class belongs in one, and a Blackboard imposes no schema on the key types it accepts. A type whose only remaining requirement is a capability is therefore accepted once that capability is held.
>
> These checks are not limited to the `Add*` commands — see [Capability-gated custom types](#capability-gated-custom-types) for how the same capabilities are re-checked when an existing node is edited or deleted, or an existing key removed, and for the breaking change on delete specifically.
>
> ⚠️ **Breaking change**: such a class used to be refused with `PolicyViolation`. The four `Add*` commands and `AddBlackboardKey` now answer `CapabilityNotAvailable` and name every missing capability at once. Two other codes moved with them: a class path nothing currently loaded answers to is now `NotFound` rather than `InvalidParams`, and a class that is abstract, deprecated, superseded, or not a Behavior Tree node at all is now `InvalidParams` rather than `PolicyViolation`. There is no compatibility window for the old codes: they meant "no permission would have helped", so keeping them would describe a permission system that did not exist. **Nothing is loaded to resolve a class path** — the four `Add*` commands and `AddBlackboardKey` used to fall back to loading the named class when it was not already in memory, and no longer do.
>
> **Note — the four listings no longer hide anything, and say what each class would take**: they used to return only classes that were concrete, not deprecated, not superseded, and not marked as hidden in the editor's own drop-down, without ever consulting the policy the add path uses. That produced disagreements in both directions — a sub-tree runner or a project's own node was offered and then refused, while a class carrying the hidden-drop-down marker was accepted by the add path yet absent from the one place it could have been discovered. All four now answer from the same policy, report `Admission` per entry, and include the classes that cannot be placed at all as `NotAddable` rather than dropping them. They are ordered by `ClassPath` and report `TotalCount` / `ReturnedCount` / `Truncated`, so a capped answer always carries the same leading classes instead of whichever ones the class walk reached first. A listing is a snapshot, not an authorization: capabilities and roles can change between the listing and the mutation, so each command re-evaluates on its own request.
>
> **There is no listing for Blackboard key types.** The three gated places are not equally discoverable: node classes have the four listings above, while the key types a Blackboard will accept, and the properties a node exposes, have no command that enumerates them with their admission. An operator granting `BlackboardReferenceKeyTypeEdit` or `BehaviorTreeCustomTypeEdit` for a key type has to know the class path in advance.

### Toolset bridges — AIModule (7) 🧩

Bridge commands via the `AIModuleToolset` (UE 5.8+, Experimental). Provider: `Toolset.Editor.AIModule.*`. Observation only.

| Command | Description |
|---|---|
| `Toolset.Editor.AIModule.GetBlackboard` | Blackboard asset associated with a BehaviorTree |
| `Toolset.Editor.AIModule.GetRootDecorators` | Decorators attached to the root composite node |
| `Toolset.Editor.AIModule.ListNodes` | All nodes with their indices and types |
| `Toolset.Editor.AIModule.GetNodeDepth` | Depth of a single node identified by index |
| `Toolset.Editor.AIModule.GetNodeDepths` | Depth of every node as a flat list |
| `Toolset.Editor.AIModule.GetChildren` | Immediate children of a composite node identified by refPath |
| `Toolset.Editor.AIModule.GetSubtree` | Subtree rooted at a node identified by refPath |

---

## UAIP.Editor.MetaSound 🧩

MetaSound graph editing. Requires `Metasound` plugin.

| Command | Description |
|---|---|
| `GetMetaSoundInfo` 🧩 | MetaSoundSource / MetaSoundPatch graph topology (nodes, connections, I/O vertices). Every node reports its real `ClassName` plus `Admission` / `RequiredCapabilities` / `MissingCapabilities` for working on it — see the note below |
| `GetAvailableMetaSoundNodeClasses` 🧩 | List frontend-registry node classes (`ClassName`, `Variant`, `MajorVersion`, `DisplayName`) for `AddMetaSoundNode`, each with `Admission` (`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`) plus `RequiredCapabilities` / `MissingCapabilities` from the same policy `AddMetaSoundNode` validates against. No longer filtered to engine-standard namespaces. Ordered by `ClassName`; reports `TotalCount`, `ReturnedCount`, `Truncated` (max 1000) — see the note below |
| `AddMetaSoundNode` 🧩 | Add a node by `Namespace::Name` (MajorVersion-aware) — a class from outside the four engine namespaces needs a capability, see the note below |
| `RemoveMetaSoundNode` 🧩 | Remove a node by NodeId — needs the same capability when the node is one of those classes |
| `ConnectMetaSoundPins` 🧩 | Connect two pins (idempotent flag on duplicates) — both ends are checked |
| `DisconnectMetaSoundPins` 🧩 | Disconnect a pin connection — both ends are checked |
| `AddMetaSoundInput` 🧩 | Add an input vertex (single-page assets only) |
| `AddMetaSoundOutput` 🧩 | Add an output vertex (single-page assets only) |
| `SetMetaSoundNodeProperty` 🧩 | Set an input default (Bool / Int / Float / String, NaN / Inf rejected) — needs the same capability when the node is one of those classes |
| `CompileMetaSound` 🧩 | Register with Frontend (per-session 1 s rate limit) — never gated by the custom-type capability |

> **Note — node classes outside the four engine namespaces are capability-gated**: a `ClassName` whose namespace is `UE`, `Metasound`, `MetasoundStandardNodes` or `MetasoundEditor` is added the same way as before. A class from any other namespace — one a project or plugin module registered under its own — now requires `MetaSoundCustomTypeEdit` instead of being refused outright. Not granted by default; see [Safety & Capabilities](safety.md#optional-graph-editors). There is no companion "dangerous type" capability for this domain, as in AnimBlueprint, ControlRig and Enhanced Input and unlike Material: a MetaSound node evaluates the fixed signal operation its registry entry describes and runs nothing the caller supplied.
>
> ⚠️ **This affects ordinary graphs more here than in the other gated domains — read this before granting or withholding the capability.** MetaSound registers **every MetaSound asset's own graph class without a namespace**, and that is exactly what a node referencing another MetaSound asset is: a subgraph, or the target of a preset. Such a node therefore always falls outside the four namespaces, so a session without `MetaSoundCustomTypeEdit` **cannot connect, disconnect, remove, or write an input default on any node of a subgraph or preset**, even though nothing about the graph is unusual. Subgraph reuse is normal practice in MetaSound in a way it is not in the other domains this gate covers, so expect to grant this capability for most real authoring work. It is not exempted, because a graph class registered by an asset of the project's own *is* a type of the project's own, and exempting it would empty the capability of most of its meaning in this domain.
>
> **Compiling is never gated by it.** `CompileMetaSound`, and the implicit re-registration every mutating command performs after its own change, ask nothing for the classes an asset merely contains — otherwise a MetaSound referencing one asset of the project's own could never be compiled without a grant. Only the class a request *names*, and the nodes a request *acts on*, are gated.
>
> These checks are not limited to `AddMetaSoundNode` — see [Capability-gated custom types](#capability-gated-custom-types) for how the same capability is re-checked when an existing node is edited, connected, disconnected, or deleted, and for the breaking change on delete / disconnect specifically.
>
> ⚠️ **Breaking change**: such a class used to be refused with `PolicyViolation`. `AddMetaSoundNode` now answers `CapabilityNotAvailable` and names the missing capability. Two other codes moved with it: a `ClassName` nothing in the frontend registry answers to is now `NotFound` rather than `PolicyViolation`, and a deprecated class is now `InvalidParams` rather than `PolicyViolation`. A template class (`Reroute` and the like) keeps returning `PolicyViolation`. There is no compatibility window for the old codes: they meant "no permission would have helped", so keeping them would describe a permission system that did not exist. Nothing is loaded to resolve a class name — the registry is read as it stands.
>
> **Note — the two listings now report admission and no longer hide anything**: `GetAvailableMetaSoundNodeClasses` used to drop every class outside the four namespaces from its response, so a project's own nodes were invisible to it even for an operator who had granted access to them. It now returns the registry's external classes in full, ordered by `ClassName`, each with `Admission` — `Allowed`, `RequiresCapabilities` (grant what `MissingCapabilities` names, itself a subset of `RequiredCapabilities`), `NotAddable` (a structural refusal no grant fixes — deprecated, a template class, or nothing registered answers to it), or `CompatibilityUnknownUntilAuthorized` — plus `TotalCount` / `ReturnedCount` / `Truncated` for a new 1000-entry cap. ⚠️ `GetMetaSoundInfo` changed the same way and more sharply: it used to report any node outside those namespaces as `ClassName: "<Unknown>"` **and drop every edge touching one**, so the returned topology did not match the asset. It now reports real class names and all edges, and attaches `Admission` / `RequiredCapabilities` / `MissingCapabilities` to each node from the same question the editing routes ask. A caller that treated `"<Unknown>"` as a sentinel, or that relied on the edge list being pre-filtered, must stop. Both reports are snapshots, not authorizations: capabilities and roles can change between the listing and the mutation, so each command re-evaluates on its own request.

---

## UAIP.Editor.EQS 🧩

EQS query editing. Requires `EnvironmentQueryEditor` plugin.

| Command | Description |
|---|---|
| `GetEQSQueryInfo` 🧩 | EQS Generator Option / Test structure. Every Option and Test now reports its real class name — no longer redacted during degraded (PIE) reads — plus `Admission` / `RequiredCapabilities` / `MissingCapabilities` for it, see the note below. Degraded mode still omits `NodeX` / `NodeY` and `GeneratorProperties`. `SchemaVersion` is now `2` |
| `GetAvailableEQSGeneratorClasses` 🧩 | List `UEnvQueryGenerator` subclasses — feed `ClassPath` to `AddEQSGenerator`. Each entry now carries `Admission` (`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`) plus `RequiredCapabilities` / `MissingCapabilities`, from the same policy the add command validates against. No longer filtered to the module this domain ships. Ordered by `ClassPath`; reports `TotalCount`, `ReturnedCount`, `Truncated` (max 200). `SchemaVersion` is now `2` — see the note below |
| `GetAvailableEQSTestClasses` 🧩 | List `UEnvQueryTest` subclasses — feed `ClassPath` to `AddEQSTest`. Reports the same admission and count fields as above |
| `AddEQSGenerator` 🧩 | Add a Generator Option — a class from outside the module this domain ships needs a capability, see the note below |
| `RemoveEQSGenerator` 🧩 | Remove a Generator Option by NodeId (cascading Test deletion) — needs the same capabilities the Generator's own class asks for |
| `AddEQSTest` 🧩 | Add a Test to a Generator Option — same checks as `AddEQSGenerator` |
| `RemoveEQSTest` 🧩 | Remove a Test by NodeId — needs the same capabilities the Test's own class asks for |
| `SetEQSGeneratorProperty` 🧩 | Set a Generator property (generic ImportText_Direct) — needs the capabilities asked for by the class of the Generator being written **and** by the class that declares the property |
| `SetEQSTestProperty` 🧩 | Set a Test property (`param:<Name>` → `UAIDataProvider_QueryParams`) — same checks as above; toggling `bTestEnabled` (`PropertyName: "TestEnabled"`) is gated by the Test's own class too, even though the flag itself lives on the graph node rather than on the Test instance — this route was previously ungated entirely, see the note below |

> **Note — this domain gates types at three separate places, behind two capabilities**: the class of a Generator being placed or worked on, the class of a Test being placed or worked on, and the class that declares a node property being written. All three places have always accepted the same single module, `/Script/AIModule`.
>
> - **`EQSCustomTypeEdit`** — required when the type comes from outside `/Script/AIModule`: a project module, a plugin module (including an engine plugin such as `SmartObjects` or `MassEQS`), or a Blueprint generated Test class. One name covers all three places on purpose, for the same reason as the other gated domains: which place a project's own type is reached through — as a Generator, a Test, or the declarer of a property — is not something an operator granting this permission would want to decide separately.
> - **`EQSDelegatedGeneratorEdit`** — required for a Generator kind whose item production is not its own compiled code: `UEnvQueryGenerator_Composite`, which runs a set of nested Generator instances held inside it, and `UEnvQueryGenerator_BlueprintBase`, whose subclasses carry a graph authored in the editor. Matched by inheritance, not by name, and required independently of where the class came from — `/Script/AIModule` ships both kinds itself, so the module a class comes from says nothing about what it will run. Also required for a property such a Generator declares (a Composite Generator's own properties describe the child Generators it runs).
>
> Neither is granted by default; see [Safety & Capabilities](safety.md#optional-graph-editors).
>
> ⚠️ **A project-defined Composite-derived Generator needs both capabilities, not one.** It is both a class this domain does not ship and a class whose item production runs elsewhere, so `EQSCustomTypeEdit` and `EQSDelegatedGeneratorEdit` are required **together**; holding one leaves the request refused, naming the other as still missing. The same applies to a property such a class declares.
>
> **The Test surface has no companion "dangerous type" capability.** Unlike the Generator surface, nothing this domain accepts as a Test runs code somewhere other than its own compiled class — a Blueprint-authored Test's graph is answered by origin, the same as any other project-defined class, rather than by a second finding.
>
> **Rebuilding a query is never gated by the classes it already contains.** Adding or removing a Generator or Test writes the graph back into the query's Option list afterward, and that rewrite asks nothing for the classes already sitting in the asset — otherwise a query holding one Generator or Test class of the project's own could never be edited without a grant. Only the class a request *names*, and the nodes a request *acts on*, are gated.
>
> **Nothing here is refused by the engine after authorization.** This domain has no per-class engine predicate to consult: the environment query editor builds its class menus by enumerating subclasses and dropping the abstract, deprecated and hidden ones, and the graph schema answers whether a graph is a query graph rather than whether a given Generator or Test belongs in one. A type whose only remaining requirement is a capability is therefore accepted once that capability is held.
>
> These checks are not limited to the `Add*` commands — see [Capability-gated custom types](#capability-gated-custom-types) for how the same capabilities are re-checked when an existing Generator or Test is edited or deleted, and for the breaking change on delete specifically. ⚠️ **Toggling `bTestEnabled` used to be entirely ungated**, along with delete and disconnect — before this change, only the `Add*` and `Set*` (for the property it writes to the node instance) commands consulted the type policy, so this route reached the asset regardless of what the Test's class was.
>
> ⚠️ **Breaking change**: such a class used to be refused with `PolicyViolation`. `AddEQSGenerator`, `AddEQSTest`, `SetEQSGeneratorProperty` and `SetEQSTestProperty` now answer `CapabilityNotAvailable` and name every missing capability at once. A class path nothing currently loaded answers to is now `NotFound` rather than `InvalidParams`; this domain never fell back to loading an unresolved class as a side effect, so nothing changes there. There is no compatibility window for the old codes: they meant "no permission would have helped", so keeping them would describe a permission system that did not exist.
>
> **Note — the two listings no longer hide anything, and say what each class would take**: they used to enumerate classes by base type and class flags alone, without consulting the policy the add path uses, and dropped every class outside `/Script/AIModule` from the response. That produced disagreements in both directions — a Composite Generator or a project's own class was offered and then refused, while an abstract class such as `UEnvQueryGenerator_BlueprintBase` was correctly refused yet absent from the one place it could have been discovered. Both listings now answer from the same policy, report `Admission` per entry, and include the classes that cannot be placed at all as `NotAddable` rather than dropping them. They are ordered by `ClassPath` and report `TotalCount` / `ReturnedCount` / `Truncated` (max 200), so a capped answer always carries the same leading classes instead of whichever ones the class walk reached first. A listing is a snapshot, not an authorization: capabilities and roles can change between the listing and the mutation, so each command re-evaluates on its own request.
>
> **`GetEQSQueryInfo` no longer withholds a class name.** Every Option and Test used to report `<redacted>` in place of the class name during a degraded (PIE) read for a type the domain would not accept outright, which told the caller neither what the node was nor what would make it usable. It now always reports the real class name, alongside `Admission` / `RequiredCapabilities` / `MissingCapabilities` for the same question `SetEQSGeneratorProperty` / `SetEQSTestProperty` / `RemoveEQSGenerator` / `RemoveEQSTest` would ask about it.

---

## UAIP.Editor.Sequencer

LevelSequence editing — tracks, sections, keyframes, playback, bindings.

### Native (129)

#### Structure (15)

| Command | Description |
|---|---|
| `AddTrack` | Add a track to a Level Sequence (TrackClass-specified). Requires `SequencerCustomTypeEdit` in addition to `SequencerStructureEdit` when `TrackClass` comes from outside the four modules this domain ships tracks from — see [Capability-gated custom types](#capability-gated-custom-types) |
| `RemoveTrack` | Remove a track by TrackClass / BindingGuid. Requires `SequencerCustomTypeEdit` when the removed track's class is from outside the four trusted modules, **except** for `UMovieSceneSubTrack` / `UMovieSceneCinematicShotTrack` / `UMovieSceneEventTrack` — those three can never be added through `AddTrack`, but removing one already in the sequence needs no capability at all as long as it comes from a trusted module |
| `AddSection` | Add a section to a track (StartFrame / EndFrame in DisplayRate). Requires `SequencerCustomTypeEdit` when the owning track's class is untrusted |
| `RemoveSection` | Remove a section by SectionIndex. Requires `SequencerCustomTypeEdit` when the owning track's class is untrusted |
| `SetPlaybackRange` | Set the sequence's playback range |
| `FlushSequencerChanges` | Flush deferred change notifications |
| `GetAvailableSequencerTrackClasses` | List every `UMovieSceneTrack` subclass this editor has loaded, whether or not this session may currently add one. `SchemaVersion` is `2`; each entry carries `Admission` (`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`) plus `RequiredCapabilities` / `MissingCapabilities`, and the response carries `TotalCount` / `ReturnedCount` / `Truncated`. ⚠️ **Changed** — the listing used to silently exclude every `Deprecated`, `NewerVersionExists` or `HideDropDown` class; it now includes them with `Admission` describing what each would take, matching what `AddTrack` itself would do with the same class |
| `SetSectionRange` | Set a section's frame range |
| `DuplicateSection` | Duplicate a section |
| `MoveSection` | Move a section by a frame offset |
| `AddCameraCut` | Add a camera-cut section to the CameraCutTrack |
| `SetTrackEnabled` | Toggle a track's enabled state |
| `IsTrackEnabled` | Get a track's enabled state |
| `SetSectionActive` | Toggle a section's active state |
| `IsSectionActive` | Get a section's active state |

#### Keyframes (7)

| Command | Description |
|---|---|
| `AddKeyframe` | Add a keyframe to a channel. Requires `SequencerCustomTypeEdit` when the owning track's class is untrusted |
| `RemoveKeyframe` | Remove a keyframe by FrameNumber. Requires `SequencerCustomTypeEdit` when the owning track's class is untrusted |
| `SetKeyframeValue` | Update a keyframe's value. Requires `SequencerCustomTypeEdit` when the owning track's class is untrusted |
| `SetKeyframeInterpolation` | Change a keyframe's interpolation mode |
| `SetKeyframeTangents` | Set a keyframe's tangents |
| `OffsetKeyframes` | Bulk-shift all keyframes on a channel by a time offset |
| `GetKeyframeTangents` | Get a keyframe's tangents (arrive / leave) |

> These checks are not limited to `AddTrack` — see [Capability-gated custom types](#capability-gated-custom-types) for how the same capability is re-checked when an existing track's section or keyframe is edited or removed, and for the breaking change on delete specifically. ⚠️ **The three internal-only track classes are the one exception**: `UMovieSceneSubTrack`, `UMovieSceneCinematicShotTrack` (each reachable only through its own dedicated command) and `UMovieSceneEventTrack` (which this domain has no command to add at all) can never be added through `AddTrack` regardless of any capability held, but `RemoveTrack` needs no capability at all to remove one already in the sequence, as long as it comes from a trusted module — removing authors no content, so the restriction that keeps the class off the generic add path does not carry over to taking an existing instance back out.

#### Bindings (4)

| Command | Description |
|---|---|
| `BindActor` | Bind an editor-world actor as a Possessable |
| `UnbindActor` | Remove an actor binding by BindingGuid |
| `GetActorBindingGuid` | Look up BindingGuid by actor name |
| `GetBoundActors` | Get actors bound to a BindingGuid |

#### Observation (12)

| Command | Description |
|---|---|
| `GetSequenceInfo` | Track / section / channel / binding / DisplayRate / playback range |
| `GetBindings` | List Possessable bindings (GUID, name, class) |
| `GetTracks` | List tracks for a BindingGuid |
| `GetSections` | List sections (with frame range) for a track |
| `GetDisplayRate` | Get the sequence's DisplayRate |
| `GetTickResolution` | Get the sequence's TickResolution |
| `GetPlaybackRange` | Get the current playback range |
| `GetKeyframes` | Get keyframes on a channel (time, value, interp) |
| `ValidateSequenceBindings` | Validate all bindings (actor existence, type match) |
| `GetCameraCutSections` | List CameraCutTrack sections |
| `GetCurrentSequence` | Get the currently open LevelSequence |
| `GetFocusedSequence` | Get the focused Sequencer's LevelSequence |

#### Playback (10)

| Command | Description |
|---|---|
| `Play` | Start Sequencer playback |
| `Pause` | Pause playback |
| `IsPlaying` | Get the playback state |
| `SetPlayheadFrame` | Move the playhead to a frame |
| `GetPlayheadFrame` | Get the current playhead position |
| `SetPlaybackSpeed` | Set the playback speed multiplier |
| `GetPlaybackSpeed` | Get the current playback speed multiplier |
| `SetLoopMode` | Set the loop mode (NoLoop / Loop / LoopExactly) |
| `GetLoopMode` | Get the current loop mode |
| `ForceEvaluate` | Force-evaluate the current frame |

#### Section properties (4)

| Command | Description |
|---|---|
| `GetSectionProperty` | Get a UMovieSceneSection property value |
| `SetSectionProperty` | Set a UMovieSceneSection property value. The value goes in `PropertyValue` as engine text or in `ValueJson` as JSON, and `Operation` / `ElementIndex` / `ElementKeyJson` address a single container element — see [Writing references, structs and containers](#writing-references-structs-and-containers) |
| `GetSectionWeight` | Get a section's weight |
| `SetSectionWeight` | Set a section's weight |

#### UI / state (10)

| Command | Description |
|---|---|
| `SetCameraLock` | Toggle camera lock |
| `IsCameraLockActive` | Get camera lock state |
| `GetSelectionRange` | Get the selection range |
| `SetSelectionRange` | Set the selection range |
| `ClearSelection` | Clear the selection range |
| `GetTrackFilterNames` | List available track filter names |
| `IsTrackFilterActive` | Get a filter's enabled state |
| `SetTrackFilterActive` | Toggle a filter's enabled state |
| `SetLocked` | Toggle sequence lock |
| `IsLocked` | Get the lock state |

#### Sequence properties (6)

| Command | Description |
|---|---|
| `SetDisplayRate` | Change the sequence's DisplayRate |
| `GetViewRange` | Get the Sequencer timeline view range |
| `SetViewRange` | Set the view range |
| `GetWorkRange` | Get the work range |
| `SetWorkRange` | Set the work range |
| `SetTickResolution` | Change TickResolution (warns if keyframes exist) |

#### Marked frames (5)

| Command | Description |
|---|---|
| `AddMarkedFrame` | Add a labeled marked frame |
| `GetMarkedFrames` | List all marked frames |
| `DeleteMarkedFrame` | Delete a marked frame by index |
| `DeleteAllMarkedFrames` | Delete all marked frames |
| `FindMarkedFrameByLabel` | Find a marked frame by label |

#### Sub-sequences (2)

| Command | Description |
|---|---|
| `GetSubSequences` | List SubSequence track sections |
| `AddSubSequenceTrack` | Add a SubSequence track |

#### AnimMixer (42, optional `MovieSceneAnimMixer`)

| Command | Description |
|---|---|
| `GetAnimMixerTrackInfo` | Get AnimMixer track info |
| `GetMixerLayers` | Compact summary of every AnimMixer layer for a binding |
| `GetMixerLayerCount` | Number of layers in a binding's AnimMixer track |
| `GetLayerName` | Display name of a layer |
| `SetLayerName` | Set the display name of a layer |
| `GetLayerIndex` | Zero-based index of the layer with a given display name (`NotFound` if absent) |
| `GetLayerSections` | Every animation section within a layer |
| `IsLayerEmpty` | Whether a layer holds no animation sections |
| `InsertMixerLayer` | Insert an empty layer at an index, shifting the rest down; returns the new index |
| `GetTransitionsForSection` | Transitions involving a section (`FromSectionIndex`, `ToSectionIndex`, `TransitionClass`) |
| `GetTransitionBetween` | Basic info for the transition between two section indices (`NotFound` if absent) |
| `GetTransitionInfo` | Detailed info for the transition between two sections |
| `GetTransitionName` | Display name of the transition between two sections |
| `ChangeTransitionType` | Replace a transition with one of `NewTransitionClass` (create-then-delete in one transaction) |
| `GetCompatibleDecorations` | Decoration classes compatible with a layer. Optional `Target` (`"Layer"` default or `"ChildTrack"`) selects the layer or its child track. ⚠️ **Changed** — `CompatibleDecorations` array elements are now objects (`DecorationClass` plus `Admission` / `RequiredCapabilities` / `MissingCapabilities`), not plain class-path strings |
| `GetDecorations` | Existing decorations on a layer. Optional `Target` (`"Layer"` default or `"ChildTrack"`) selects the layer or its child track. ⚠️ **Changed** — `Decorations` array elements are now objects (`DecorationClass` plus `Admission` / `RequiredCapabilities` / `MissingCapabilities`), not plain class-path strings |
| `FindDecoration` | Find one decoration on a layer (`NotFound` if absent). Optional `Target` (`"Layer"` default or `"ChildTrack"`) selects the layer or its child track; `NotFound` is also returned when `Target` is `"ChildTrack"` but the layer has no child track. An unresolvable `DecorationClass` is never force loaded |
| `AddDecoration` | Add (or retrieve an existing) decoration on a layer. Optional `Target` (`"Layer"` default or `"ChildTrack"`) selects the resolution target; the compatibility check runs against whichever container `Target` resolves to. Requires `SequencerCustomTypeEdit` in addition to `SequencerStructureEdit` when `DecorationClass` comes from outside the five modules this domain ships decorations from — see [Capability-gated custom types](#capability-gated-custom-types). ⚠️ **Changed** — `DecorationClass` is resolved against what this editor already has loaded and is never force loaded; an unresolvable path is `NotFound` where it used to be loaded on demand |
| `RemoveDecoration` | Remove a decoration from a layer. Optional `Target` (`"Layer"` default or `"ChildTrack"`) selects the layer or its child track; `NotFound` is also returned when `Target` is `"ChildTrack"` but the layer has no child track. Requires `SequencerCustomTypeEdit` when the removed decoration's class is untrusted |
| `GetLayerBlendWeight` | Get a layer's blend weight |
| `SetLayerBlendWeight` | Set a layer's blend weight |
| `IsLayerMuted` | Get a layer's mute state |
| `SetLayerMuted` | Toggle a layer's mute state |
| `IsLayerEnabled` | Get a layer's enabled state |
| `SetLayerEnabled` | Toggle a layer's enabled state |
| `ClearMixerLayer` | Clear all sections on a layer |
| `AddMixerLayer` | Add a new AnimMixer layer |
| `RemoveMixerLayer` | Remove an AnimMixer layer |
| `MoveMixerLayer` | Move an AnimMixer layer |
| `AddMixerSection` | Add an AnimMixer section |
| `RemoveMixerSection` | Remove an AnimMixer section |
| `SetMixerSectionRange` | Set an AnimMixer section's frame range (raw FFrameNumber ticks) |
| `SetMixerSectionAnimation` | Set an AnimMixer section's animation |
| `AddMixerTransition` | Add a transition |
| `RemoveMixerTransition` | Remove a transition |
| `GetMixerSectionInfo` | Get AnimMixer section info |
| `AddMixerChildTrack` | Add a ControlRig child track parented to the layer at `LayerIndex`, creating a ControlRig instance of `ControlRigPath` (must derive from `UControlRig`) and attaching its parameter section. `LayerIndex` may equal the current layer count to append a new row. Optional `IsLayered` (default false) configures the new ControlRig as additive. Fails with `Conflict` (no side effects) when the target layer already has a child track or animation sections. `ControlRigPath` accepts a Control Rig asset in either format (on UE 5.8, the asset itself, e.g. `/Game/X.X`; an inner part path such as `/Game/X.X:X_EditorOnly` is not found); a path that is not a Control Rig is `NotFound` |
| `RemoveMixerChildTrack` | Remove the child track parented to the layer at `LayerIndex`, tearing down the layer reference, the child-track bookkeeping, its decorations, and the binding together. `NotFound` if the layer has no child track |
| `GetMixerChildTracks` | List every child track across all layers of a binding's AnimMixer track. Each entry carries `LayerIndex`, `TrackName`, `TrackClass` |
| `MoveMixerChildTrack` | Move the child track parented to `LayerIndex` to `NewLayerIndex`. Succeeds as a no-op when the two indices are equal. Fails with `Conflict` (no side effects) when the destination layer already has a child track or animation sections |
| `SetMixerSectionBlendType` | Set the blend type of the animation section at `SectionIndex` on the child track parented to `LayerIndex`. `BlendType` is matched case-insensitively against Absolute / Additive / Relative / Override and must be supported by the target section |
| `GetMixerSectionBlendType` | Get the current blend type and the set of supported blend types of the animation section at `SectionIndex` on the child track parented to `LayerIndex` |

#### ControlRig tracks (12)

ControlRig authoring **inside a LevelSequence**. For editing a ControlRig asset itself see [`UAIP.Editor.ControlRig`](#uaipeditorcontrolrig).

| Command | Description |
|---|---|
| `GetControlRigTracks` | All ControlRig parameter tracks in a LevelSequence. Each entry now carries `IsChildTrack`, with `LayerIndex` present only when it is `true` |
| `GetControlRigSectionInfo` | Section properties — `IsInfinite`, `StartFrame`, `EndFrame`, `IsActive`, class name |
| `FindOrCreateControlRigTrack` | Find or create a ControlRig parameter track for a binding; reports `TrackCreated`. Optional `IsLayered` (default false) configures a newly created ControlRig as additive; ignored when an existing track is found. Accepts a Control Rig asset in either format (on UE 5.8, pass the asset itself, e.g. `/Game/X.X`, not an inner part path); a path that does not name a Control Rig is `NotFound`, and a track of a different Control Rig is never mistaken for the requested one |
| `BakeToControlRig` | Bake a binding's animation onto a ControlRig track (display-rate frames, `Tolerance` 0.0–1.0). Accepts either Control Rig format; a path that does not name a Control Rig is `NotFound`. **Key reduction differs for a UE 5.8 runtime-asset Control Rig:** `Tolerance` greater than 0 still turns reduction on, but it is read as a fraction of the value range (`0.1` = 10%) instead of the absolute value difference the legacy format uses, so the default `0.1` reduces more strongly than the engine's own UI default (5%). Reduction requires the sequence to be open in the Level Sequence editor; if it is not (another sequence being open does not count), the call is refused with `PreconditionFailed` and the tracks and keys are left unchanged — open the sequence, or pass `Tolerance: 0` to bake without reduction. After the bake, every animation track of the binding is disabled (the legacy format disables only the first) |
| `KeyControls` | Key the given controls at one display-rate frame (all visible controls when `ControlNames` is empty) |
| `KeyControlsAtFrames` | Key the given controls at multiple display-rate frames. UE 5.8+ only; reports `Available: false` on UE 5.7 (`UnavailableDetail: "EngineVersion"`) |
| `GetControlsMask` | Per-control visibility mask of a ControlRig section |
| `SetControlsMask` | Set visibility for named controls; unnamed controls keep their state |
| `ShowAllControls` | Make every control in the section visible |
| `HideAllControls` | Hide every control in the section |
| `LoadAnimIntoRig` | Bakes an AnimSequence onto the controls of a ControlRig section. The animation is sampled through the skeletal mesh the track's binding resolves to, so the level holding the bound actor must be open; otherwise the command fails with `NotFound` |
| `GetActorTransformAtFrame` | Evaluate the sequence at a frame and return the named actor's world transform |

### Toolset bridges (61) 🧩

Provider: `Toolset.Editor.AnimationAssistant.*` (41 commands — Lifecycle 6, Playback 10, Property 9, MarkedFrame 5, UI 11) and `Toolset.Editor.SequencerAnimMixer.*` (20 commands — Layers 10, Transitions 5, Decorations 5). Requires UE 5.8+.

> A third Sequencer-module bridge provider, `Toolset.Editor.SequencerControlRig.*` (63 commands), is documented under [`UAIP.Editor.ControlRig`](#uaipeditorcontrolrig) because its commands operate on ControlRig controls.

> The two Decorations mutating commands (`AddDecoration` / `RemoveDecoration`) are gated by `SequencerCustomTypeEdit` exactly the same way their native counterparts are — closing only the native route would leave the identical class reachable through the bridge. The two Decorations listing commands (`GetCompatibleDecorations` / `GetDecorations`) pass the external Toolset registry's response through unchanged, so they do not carry the `Admission` / `RequiredCapabilities` / `MissingCapabilities` fields the native listing commands now report; use the native commands when that information is needed.

---

## UAIP.Editor.StateTree

StateTree editing.

### Native (39)

#### State observation (8)

| Command | Description |
|---|---|
| `GetRootStates` | Top-level state descriptors (`StateId`, `Name`, `Type`, `ParentStateId`, `ChildCount`) |
| `GetStateChildren` | Direct child state descriptors of one state |
| `GetStateTasks` | Tasks of one state (class names redacted in degraded mode during PIE). Each entry carries `Admission` / `RequiredCapabilities` / `MissingCapabilities` for the task's own class — see the note below. `SchemaVersion` is now `2` |
| `GetStateTransitions` | Transitions of one state (target state IDs suppressed during PIE) |
| `GetStateEnterConditions` | Enter conditions of one state. Reports the same admission fields as `GetStateTasks`. `SchemaVersion` is now `2` |
| `GetStateTreeGlobalTasks` | Global tasks of the asset (run regardless of the active state). Reports the same admission fields as `GetStateTasks`. `SchemaVersion` is now `2` |
| `GetStateTreeEvaluators` | Evaluators of the asset (run every tick to update shared data). Reports the same admission fields as `GetStateTasks`. `SchemaVersion` is now `2` |
| `GetStateNodeDescription` | Class path and display name of a node GUID (searches global tasks, evaluators, all states) |

> **Note — the four node listings above no longer mask a class this domain does not ship.** They used to replace `TaskClass` / `ConditionClass` / `EvaluatorClass` with `"<redacted>"` and set `MaskedDueToPolicy: true` for a node whose class the add path would refuse. All four now name the real class and instead attach `Admission` / `RequiredCapabilities` / `MissingCapabilities`, matching how `GetAvailableTaskClasses` / `GetAvailableConditionClasses` / `GetAvailableEvaluatorClasses` below already report classes not yet placed. `MaskedDueToPolicy` is still present in the response for compatibility but is now always `false`. **This is unrelated to the redaction that still applies during a degraded (PIE) read** (the `TaskClass` / `ConditionClass` / `EvaluatorClass` field itself, not `MaskedDueToPolicy`) — which continues to replace every class name with `"<redacted>"` regardless of capability, for reasons that predate this feature.
>
> ⚠️ Two node kinds were also affected by two unrelated fixes made alongside the above. Global task, evaluator and enter condition nodes backed by a native struct (as opposed to a Blueprint instance) previously bypassed the node class policy entirely and were never reported with any admission fields at all; they now are. Evaluator and enter condition nodes were previously judged as though they were Task nodes, which could report `WrongBaseType`-style refusals for classes the add path accepts; they are now judged against their own base.

#### Class / schema discovery (5)

| Command | Description |
|---|---|
| `GetAvailableTaskClasses` | `FStateTreeTaskBase` fields (native struct + Blueprint) — feed `ClassPath` to `AddStateTask` / `AddGlobalTask`. Each entry now carries `Admission` (`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`) plus `RequiredCapabilities` / `MissingCapabilities`, from the same policy the add commands validate against — including the native struct hierarchy, which the previous filter never consulted at all. Ordered by `ClassPath`; reports `TotalCount`, `ReturnedCount`, `Truncated` (max 200, applied once to the struct and class hierarchies combined). `SchemaVersion` is now `2` — see the note below |
| `GetAvailableConditionClasses` | `FStateTreeConditionBase` fields (native struct + Blueprint) — feed `ClassPath` to `AddStateEnterCondition`. Reports the same admission and count fields as above |
| `GetAvailableEvaluatorClasses` | `FStateTreeEvaluatorBase` fields (native struct + Blueprint) — feed `ClassPath` to `AddEvaluator`. Reports the same admission and count fields as above |
| `GetAvailableStateTreeSchemaClasses` | `UStateTreeSchema` subclasses — feed `ClassPath` to `CreateAsset` as `FactoryParams.SchemaClass`. Each entry now carries `Admission` (`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`) plus `RequiredCapabilities` / `MissingCapabilities`, from the same policy `CreateAsset` admits a named schema class through — so a schema class this domain does not ship is listed with what it would take rather than being left out. Classes the editor's own schema picker hides are listed too, as `NotAddable`. Ordered by `ClassPath`; reports `TotalCount`, `ReturnedCount`, `Truncated`. `SchemaVersion` is now `2` — see the note below |
| `GetStateTreeSchema` | Schema class path and root parameter descriptors of an asset |

#### State structure editing (4)

| Command | Description |
|---|---|
| `AddState` | Add a State (State / Group / Subtree / Linked / LinkedAsset — 5 types); returns `StateId` |
| `RemoveState` | Remove a State by `StateId` (recursive child deletion) |
| `SetStateName` | Rename a state |
| `MoveState` | Reparent / reorder a state; rejects moves that would create a cycle |

#### Task / transition / condition editing (9)

| Command | Description |
|---|---|
| `AddStateTask` | Add a Task to a State — a class from outside the modules this domain ships needs a capability, see the note below; returns `TaskId` |
| `RemoveStateTask` | Remove a Task by `TaskId` — needs the same capability the removed task's own class asks for |
| `AddStateTransition` | Add a Transition (`Succeeded` / `Failed` / `NextState` / `NextSelectableState` / GUID target). `OnDelegate` is not supported |
| `RemoveStateTransition` | Remove a Transition by `TransitionId` |
| `AddStateEnterCondition` | Add an enter condition to a state — same capability check as `AddStateTask`; returns `ConditionId` |
| `RemoveStateEnterCondition` | Remove an enter condition by `ConditionId` — needs the same capability the removed condition's own class asks for |
| `SetEnterConditionProperty` | Set a property on an enter condition node — needs the capabilities asked for by the condition's own class **and** by the class that declares the property |
| `GetStateNodeProperty` | Read one top-level property of a node GUID as exported text |
| `SetStateNodeProperty` | Set a Task node property (generic `ImportText_Direct`) — needs the capabilities asked for by the task's own class **and** by the class that declares the property |

#### Global task / evaluator editing (6)

| Command | Description |
|---|---|
| `AddGlobalTask` | Add a global task — same capability check as `AddStateTask`; returns `TaskId` |
| `RemoveGlobalTask` | Remove a global task by `TaskId` — needs the same capability the removed task's own class asks for |
| `SetGlobalTaskProperty` | Set a property on a global task node — needs the capabilities asked for by the task's own class **and** by the class that declares the property |
| `AddEvaluator` | Add an evaluator — same capability check as `AddStateTask`; returns `EvaluatorId` |
| `RemoveEvaluator` | Remove an evaluator by `EvaluatorId` — needs the same capability the removed evaluator's own class asks for |
| `SetEvaluatorProperty` | Set a property on an evaluator node — needs the capabilities asked for by the evaluator's own class **and** by the class that declares the property |

> **Note — a project's own task, evaluator or enter condition class is capability-gated, not refused outright**: a class or struct from outside `/Script/StateTreeModule`, `/Script/AIModule` and `/Script/GameplayStateTreeModule` — a project module, a plugin module, or a Blueprint generated class — needs `StateTreeCustomTypeEdit`. Not granted by default; see [Safety & Capabilities](safety.md#statetree-editing). There is no companion "dangerous type" capability for this domain, as in MetaSound and Enhanced Input and unlike Material: a task, evaluator or enter condition field is a compiled function the tree calls with values from its own instance data, and a node property is a plain data member — neither carries code the caller wrote.
>
> **A property write checks two classes independently, not one.** `SetStateNodeProperty`, `SetGlobalTaskProperty`, `SetEvaluatorProperty` and `SetEnterConditionProperty` each admit the node's own class and the struct or class declaring the property being written as two separate questions; either one asking for a capability the session lacks refuses the whole write, and the refusal names every missing capability from both at once.
>
> **Compiling is never gated by it.** `CompileStateTree` asks nothing about the classes an asset merely contains — otherwise a StateTree holding one task of the project's own could never be compiled without a grant. Only the class a request *names*, and the nodes a request *acts on*, are gated.
>
> These checks are not limited to the `Add*` commands — see [Capability-gated custom types](#capability-gated-custom-types) for how the same capability is re-checked when an existing node is edited or deleted.
>
> ⚠️ **Breaking change**: such a class used to be refused with `PolicyViolation`. `AddStateTask`, `AddGlobalTask`, `AddEvaluator`, `AddStateEnterCondition` and the four `Set*Property` commands now answer `CapabilityNotAvailable` and name every missing capability at once. A class path nothing currently loaded answers to is `NotFound`; a class that is abstract, deprecated, superseded, or not a StateTree node at all is `InvalidParams`. **`RemoveStateTask`, `RemoveGlobalTask`, `RemoveEvaluator` and `RemoveStateEnterCondition` now check a capability at all** — previously none of the four consulted any policy, so removing a node was never refused regardless of its class. Nothing is loaded to resolve a class path; class resolution has always used `FindObject` rather than a loading fallback.
>
> **Note — the three class listings no longer hide the native struct hierarchy, and say what each class would take**: `GetAvailableTaskClasses`, `GetAvailableConditionClasses` and `GetAvailableEvaluatorClasses` used to run the native `FStateTree*Base` struct hierarchy through no policy at all, and ran the Blueprint class hierarchy through it only for `GetAvailableTaskClasses` — so a project's own struct-based task was listed exactly as freely as an engine-shipped one, and a Blueprint-backed condition or evaluator was listed without regard to where it came from either. All three now answer both hierarchies from the same policy the add commands validate against, report `Admission` per entry, and include classes that cannot be placed at all as `NotAddable` rather than dropping them. The two hierarchies are combined into one ordered, capped set — previously each hierarchy was capped independently, so a response could in principle carry up to twice the stated limit. A listing is a snapshot, not an authorization: capabilities and roles can change between the listing and the mutation, so each command re-evaluates on its own request.
>
> **⚠️ A schema class named at asset creation is gated too, engine-shipped ones included.** `CreateAsset`'s `FactoryParams.SchemaClass` used to be accepted on two conditions alone — it resolved, and it derived from `UStateTreeSchema` — with nothing asked about where the class came from. It now goes through the same origin rule as the node classes above, so a schema class from outside `/Script/StateTreeModule`, `/Script/AIModule` and `/Script/GameplayStateTreeModule` needs `StateTreeCustomTypeEdit`. That is not limited to a project's own classes: `/Script/MassAIBehavior`, `/Script/GameplayCameras`, `/Script/GameplayInteractionsModule`, `/Script/AvalancheTransition` and `/Script/UAFStateTree` all ship with the engine and all sit outside those three modules, so their schemas now require the capability; `/Script/GameplayStateTreeModule` schemas continue to need nothing. A class that is abstract, deprecated, superseded, or hidden from the editor's schema dropdown is refused whatever is held — previously only an abstract class was refused and a deprecated one was merely logged. The class is no longer loaded on demand either: one that is not already in memory is refused instead of being loaded in order to decide whether the caller was allowed to name it. A missing `StateTreeCustomTypeEdit` for a schema class is reported as `CapabilityNotAvailable`, naming the capability, the same as everywhere else — see [Capability-gated custom types](#capability-gated-custom-types). A structural refusal (abstract, deprecated, superseded, hidden, or not loaded) is `InvalidParams`.

| Command | Description |
|---|---|
| `GetStateTreeParameters` | Root parameter descriptors (`Name`, `ParameterType`, current serialized value) plus a nested `WriteRequirements` object per parameter. `ParameterType` now names enum, struct, object, soft-object, class, soft-class and the remaining integer widths instead of reporting every non-scalar as `Unknown` |
| `AddStateTreeParameter` | Add a root parameter (Bool / Byte / Int32 / Int64 / Float / Double / Name / String / Text) |
| `RemoveStateTreeParameter` | Remove a root parameter by name |
| `SetStateTreeParameter` | Set a root parameter value. A reference requires `StateTreeParameterReferenceEdit` and a struct or container `PropertyStructuredEdit`, and those values are supplied as JSON rather than bracket text. Refusals are now `CapabilityNotAvailable` / `PolicyViolation` / `InvalidParams` / `NotFound` as appropriate instead of a blanket `NotFound`, a refused write does not mark the asset dirty, and a successful one is undoable |
| `AddPropertyBinding` | Bind a source node property to a target node property |
| `RemovePropertyBinding` | Remove a property binding from a target node |
| `CompileStateTree` | Compile the StateTree (per-asset rate limit between successive calls) |

### Toolset bridges (8) 🧩

Bridge commands via the `StateTreeToolset` (UE 5.8+, Experimental). Provider: `Toolset.Editor.StateTree.*`. Observation only.

| Command | Description |
|---|---|
| `Toolset.Editor.StateTree.GetEditorData` | Editor data of a StateTree asset |
| `Toolset.Editor.StateTree.GetRootStates` | Root-level states of a StateTree asset |
| `Toolset.Editor.StateTree.GetGlobalTasks` | Global tasks of a StateTree asset |
| `Toolset.Editor.StateTree.GetEvaluators` | Evaluators of a StateTree asset |
| `Toolset.Editor.StateTree.GetChildren` | Child states of a `UStateTreeState` |
| `Toolset.Editor.StateTree.GetTasks` | Tasks of a `UStateTreeState` |
| `Toolset.Editor.StateTree.GetEnterConditions` | Enter conditions of a `UStateTreeState` |
| `Toolset.Editor.StateTree.GetTransitions` | Transitions of a `UStateTreeState` |

---

## UAIP.Editor.Curve

Curve asset key editing (UCurveFloat / UCurveVector / UCurveLinearColor).

| Command | Description |
|---|---|
| `GetCurveInfo` | Channel list, keys, pre / post extrapolation (per-channel truncated flag) |
| `AddCurveKey` | Add a key on the specified channel |
| `RemoveCurveKey` | Remove a key by time + tolerance |
| `SetCurveKeyValue` | Update an existing key's value and time |
| `SetCurveKeyInterpolation` | Change a key's interpolation mode (Constant / Linear / Cubic / None) |
| `SetCurveKeyTangent` | Set arrive / leave tangents (auto-promote non-Cubic keys with `promoted_to_cubic` flag) |

---

## UAIP.Editor.PCG 🧩

PCG graph editing. Requires `PCG` plugin.

| Command | Description |
|---|---|
| `GetPCGGraphInfo` 🧩 | UPCGGraph nodes / edges / parameters (degraded during PIE) |
| `ListPCGNodeTypes` 🧩 | UPCGSettings subclasses passing the allowlist |
| `AddPCGNode` 🧩 | Add a node by SettingsClassPath (returns NodePath) |
| `RemovePCGNode` 🧩 | Remove a node by NodePath (cascades edge removal) |
| `ConnectPCGPins` 🧩 | Connect pins by NodePath + PinLabel |
| `DisconnectPCGPins` 🧩 | Disconnect pins (specific pair or all from an output pin) |
| `SetPCGNodeProperty` 🧩 | Set a UPCGSettings EditAnywhere property. The value is a JSON document; references, structs and containers are no longer refused permanently but gated by `PropertyReferenceEdit` / `PropertyStructuredEdit` — see [Writing references, structs and containers](#writing-references-structs-and-containers) |
| `ExecutePCGGraph` 🧩 | Trigger `UPCGComponent::Generate` |
| `ListCustomPCGNodeTypes` 🧩 | List C++ / Blueprint custom PCG node types |
| `GetCustomPCGNodeSchema` 🧩 | JSON schema of C++ UPCGSettings subclass EditAnywhere properties. A session holding neither `PropertyReferenceEdit` nor `PropertyStructuredEdit` sees a narrowed set of types; what was left out is reported as `HiddenCount` / `HiddenCapabilities` / `HiddenReasons` rather than silently omitted |
| `GetCustomBlueprintPCGNodeSchema` 🧩 | JSON schema of Blueprint UPCGBlueprintSettings subclass properties. Narrowed the same way as `GetCustomPCGNodeSchema`, with one `HiddenCount` / `HiddenCapabilities` / `HiddenReasons` accounting covering both classes it enumerates |
| `SetCustomCppPCGNodeProperty` 🧩 | Set a property on a C++ custom node (`RecompileTriggered` flag). References, structs and containers are gated by `PropertyReferenceEdit` / `PropertyStructuredEdit`; the refusal deliberately does not name the property's type — see [Writing references, structs and containers](#writing-references-structs-and-containers) |
| `SetCustomBlueprintPCGNodeProperty` 🧩 | Set a property on a BP custom node (Class CDO / per-Instance modes). Gated the same way as `SetCustomCppPCGNodeProperty` |
| `CreatePCGGraph` 🧩 | Create a new UPCGGraph asset in the Content directory (requires `PCGGraphAssetCreate`) |
| `GetPCGGraphSchema` 🧩 | Return the graph's node / pin structure in schema form |
| `GetPCGGraphDescription` 🧩 | Get the graph's Description string |
| `SetPCGGraphDescription` 🧩 | Set the graph's Description (requires `PCGGraphEdit`) |
| `SetPCGGraphParams` 🧩 | Add or update graph parameters (requires `PCGGraphEdit`). Values are range- and NaN-checked and a bad one is refused with `InvalidParams`; the batch is applied to a copy first, so a refusal leaves no partial write, no undo entry and no dirty flag |
| `RemovePCGGraphParams` 🧩 | Remove graph parameters (requires `PCGGraphEdit`) |
| `ListPCGGraphInstances` 🧩 | List UPCGComponents in the level |
| `SpawnPCGGraphInstance` 🧩 | Spawn an APCGVolume into the world (requires `PCGVolumeSpawn`) |
| `GetPCGGraphInstanceParams` 🧩 | Get per-instance override parameters |
| `SetPCGGraphInstanceParams` 🧩 | Override instance parameters (requires `PCGGraphEdit`). Same range / NaN checking and same all-or-nothing application as `SetPCGGraphParams` |
| `ResetPCGGraphInstanceParams` 🧩 | Reset instance parameters to graph defaults (requires `PCGGraphEdit`). A call with nothing to reset still succeeds, but no longer opens a transaction or marks the asset dirty |
| `ListPCGAvailableSubgraphs` 🧩 | List subgraph candidates in the project |
| `GetPCGNativeNodeSchema` 🧩 | JSON schema of native PCG node class EditAnywhere properties. Narrowed the same way as `GetCustomPCGNodeSchema`, and reports `HiddenCount` / `HiddenCapabilities` / `HiddenReasons` |
| `AddPCGSubgraphNode` 🧩 | Add a subgraph reference node (requires `PCGGraphEdit`) |
| `RepositionPCGNode` 🧩 | Move a node to a new position (requires `PCGGraphEdit`) |
| `AddPCGCommentBox` 🧩 | Add a comment box (requires `PCGGraphEdit`) |
| `UpdatePCGCommentBox` 🧩 | Update a comment box (requires `PCGGraphEdit`) |
| `RemovePCGCommentBox` 🧩 | Remove a comment box (requires `PCGGraphEdit`) |
| `GetPCGNodeDataView` 🧩 | Get a PCG node's execution data view (requires `PCGNodeInspect`; returns CapabilityNotAvailable when `PCG_PROFILING_ENABLED=0`) |
| `RunPCGInstantGraph` 🧩 | Fire-and-forget PCG graph execution with no actor or component required (requires `PCGGraphExecute`) |
| `DrawPCGSpline` 🧩 | Starts an interactive spline draw the human finishes in the level viewport and returns an `InteractionId` right away (`IsInteractive: true`) — poll with `GetPendingInteractionStatus`, block briefly with `WaitForPendingInteraction`, or cancel with `CancelPendingInteraction`. Requires `PCGSplineDraw` and `SafetyPolicy.AllowUserInteractionPrompt` (a separate gate); one interaction may hold the level viewport at a time |

### Toolset bridges — PCG (31) 🧩

Bridge commands via the `PCGToolset` (UE 5.8+). Provider: `Toolset.Editor.PCG.*`. Commands that require an active open PCG editor tab may return `ExecutionFailed` in non-interactive contexts (known PCGToolset constraint).

> **⚠️ Breaking — `SetGraphInstanceParams` and `ResetGraphInstanceParams` now require `PCGGraphEdit`** instead of `PCGGraphExecute`, matching their native counterparts. Both rewrite the same parameter bag, so requiring the execute capability let an operator who had closed `PCGGraphEdit` change instance overrides through the bridge anyway. **A session granted only `PCGGraphExecute` loses access to these two commands** — add `PCGGraphEdit`.
>
> **The bridge does not run UAIP's value checks.** `SetGraphParams`, `SetGraphInstanceParams` and `ResetGraphInstanceParams` write inside `UPCGToolset`, so the type gate, the range / NaN checks, the part-way-parse check and the all-or-nothing batching the native commands apply do not reach them. Use `SetPCGGraphParams` / `SetPCGGraphInstanceParams` / `ResetPCGGraphInstanceParams` when you want those checks.

| Command | Description |
|---|---|
| `Toolset.Editor.PCG.CreateGraph` | Create a PCG graph asset (requires `PCGGraphAssetCreate`) |
| `Toolset.Editor.PCG.GetGraphStructure` | Get the full graph structure (nodes, edges, parameters) |
| `Toolset.Editor.PCG.SetGraphParams` | Set graph parameters (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.RemoveGraphParams` | Remove graph parameters (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.GetGraphSchema` | Get the graph schema |
| `Toolset.Editor.PCG.GetGraphDescription` | Get the graph description |
| `Toolset.Editor.PCG.SetGraphDescription` | Set the graph description (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.ListGraphInstances` | List volume actors referencing the graph |
| `Toolset.Editor.PCG.SpawnGraphInstance` | Spawn a PCG volume actor (requires `PCGVolumeSpawn`) |
| `Toolset.Editor.PCG.ExecuteGraphInstance` | Execute a graph on a PCG volume (requires `PCGGraphExecute`; async, 300 s default) |
| `Toolset.Editor.PCG.GetGraphInstanceParams` | Get per-instance parameter overrides |
| `Toolset.Editor.PCG.SetGraphInstanceParams` | Set per-instance overrides (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.ResetGraphInstanceParams` | Reset per-instance overrides (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.ListNativeNodes` | List all registered native PCG node classes |
| `Toolset.Editor.PCG.ListAvailableSubgraphs` | List PCG assets available as subgraphs |
| `Toolset.Editor.PCG.GetNativeNodeSchema` | Get the parameter schema for a native node class |
| `Toolset.Editor.PCG.AddNode` | Add a native node (requires `PCGGraphEdit` + `PCGToolsetUnsafeNodeAdd`; bypasses allowlist) |
| `Toolset.Editor.PCG.AddSubgraphNode` | Add a subgraph node (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.UpdateNode` | Update a node's properties (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.SetNodeComment` | Set a node's inline comment (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.GetNodeInfo` | Get info for a specific node |
| `Toolset.Editor.PCG.RepositionNode` | Move a node on the graph canvas (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.RemoveNode` | Remove a node (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.GetNodeDataView` | Get the last-execution data view of a node (requires `PCGNodeInspect`) |
| `Toolset.Editor.PCG.ConnectNodePins` | Connect two node pins (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.DisconnectNodePins` | Disconnect node pins (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.AddCommentBox` | Add a comment box (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.UpdateCommentBox` | Update a comment box (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.RemoveCommentBox` | Remove a comment box (requires `PCGGraphEdit`) |
| `Toolset.Editor.PCG.RunPCGInstantGraph` | Execute a PCG graph instantly via `UPCGSpatialToolset` (requires `PCGGraphExecute`; async, 300 s default) |
| `Toolset.Editor.PCG.DrawSpline` | Bridge equivalent of `UAIP.Editor.PCG.DrawPCGSpline`, delegating to `UPCGToolset::DrawSpline` (Experimental). Same admission rules and capability gates as the native command, but the wait it registers is capped at 600 s (the toolset dispatch's own hard clamp) rather than the native command's full 1800 s default |

---

## UAIP.Editor.WorldConditions 🧩

WorldConditions editing. Requires `WorldConditions` plugin.

| Command | Description |
|---|---|
| `GetWorldConditionInfo` 🧩 | Condition set structure (Operator / Depth / properties), with a `WriteRequirements` object nested in each property entry. Its `RequiredCapabilities` is always empty — this path accepts no reference or container at all, so no capability unlocks one. Every condition also now reports `Admission` / `RequiredCapabilities` / `MissingCapabilities` for its own struct, see the note below |
| `AddWorldCondition` 🧩 | Add a condition (`InsertAtIndex=-1` appends) — a struct from outside the module this domain ships needs a capability, see the note below |
| `RemoveWorldCondition` 🧩 | Remove a condition by index — needs the same capability the removed condition's struct asks for |
| `SetWorldConditionProperty` 🧩 | Set a condition USTRUCT property (ImportText value string) — needs the capability asked for by the struct being written **and** by the struct that declares the property |
| `SetWorldConditionOperator` 🧩 | Set Operator (And / Or) and bInvert (Index 0 is fixed Copy) — needs the same capability the condition's own struct asks for |
| `SetWorldConditionExpressionDepth` 🧩 | Set ExpressionDepth (0–4) — same check as above |
| `ListWorldConditionClasses` 🧩 | List `FWorldConditionBase`-derived classes — use to discover valid `ConditionClass` values. Each entry now carries `Admission` (`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`) plus `RequiredCapabilities` / `MissingCapabilities`, from the same policy `AddWorldCondition` validates against. No longer filtered to the module this domain ships. Ordered by full path (`/Script/<Module>.<Class>`); reports `TotalCount`, `ReturnedCount`, `Truncated` (max 200) |
| `ValidateWorldConditionQuery` 🧩 | Run `Initialize()` + `IsValid()` on a query and return `{IsValid, Errors}` (allowed during PIE) |
| `MoveWorldCondition` 🧩 | Move a condition from `SourceIndex` to `TargetIndex` (index 0 is fixed) — needs the same capability the moved condition's struct asks for |
| `DuplicateWorldCondition` 🧩 | Duplicate the condition at `SourceIndex` and insert the copy at `InsertIndex` — same checks as `AddWorldCondition` |
| `ReplaceWorldCondition` 🧩 | Replace a condition's type with `NewConditionClass` defaults, preserving depth / operator / invert — same checks as `AddWorldCondition` |
| `ClearWorldConditionQuery` 🧩 | Remove every condition, leaving an empty query — needs the capability asked for by every condition it removes |
| `SetMultipleWorldConditionProperties` 🧩 | Apply 1–32 property edits in one transaction, all-or-nothing — same checks as `SetWorldConditionProperty`, per edit |

> **⚠️ Breaking — `SetMultipleWorldConditionProperties` returns a different success payload.** The command is now all-or-nothing: every edit is staged and checked — domain gate, text import, part-way-parse detection, validation — and only when all of them pass is the transaction opened and the whole batch committed. A single failure fails the request with a top-level `ErrorCode` / `ErrorMessage` and writes nothing, so the old per-edit `Results[]` and `AllSucceeded` no longer describe anything. The success payload is now `AppliedEdits` (the `{ConditionIndex, SubPropertyName}` pairs actually committed) and `SkippedEdits` (the same shape, for names that matched no property — an unmatched name still does not fail the batch). Update any caller that reads `Results[]` or `AllSucceeded`.
>
> **Note — this domain gates condition structs at one place, behind one capability: `WorldConditionsCustomTypeEdit`.** A condition struct being placed, replaced, or acted on, and the struct declaring a property being written, are judged the same way and share the one name — a project's own condition declares its own properties, so a second permission for the property face would not make sense. Required when the struct comes from outside `/Script/WorldConditions`: a project module, a plugin module (including an engine plugin such as `SmartObjects`), or a Blueprint generated struct. Not granted by default; see [Safety & Capabilities](safety.md#optional-graph-editors).
>
> **Writing a property already sitting in an asset now needs this capability too — this is a new restriction, not a preserved one.** Before this change, `SetWorldConditionProperty` / `SetMultipleWorldConditionProperties` checked only the property's write flags and value kind; a project-defined condition's own properties were writable without any capability at all. They now also need `WorldConditionsCustomTypeEdit` when the declaring struct is not `/Script/WorldConditions`'s own.
>
> **Deleting, moving or duplicating a condition — not only adding one — is gated.** `RemoveWorldCondition`, `ClearWorldConditionQuery`, `MoveWorldCondition`, `DuplicateWorldCondition`, `SetWorldConditionOperator`, `SetWorldConditionExpressionDepth` used to reach the asset regardless of what the condition's struct was; they now re-check the same capability on the condition being acted on. Removing or moving a struct the capability check would refuse for placement is still allowed once the capability itself is held — only a struct that cannot be instantiated at all stays refused outright, and only for the commands that would place a fresh one.
>
> **Engine compatibility is consulted too, but only for a struct that needed the capability, and only once the session holds it.** `AddWorldCondition` and `DuplicateWorldCondition` additionally ask the query definition's own schema (`UWorldConditionSchema::IsStructAllowed`) once the capability check clears — a schema that declines a struct refuses it with `PolicyViolation` even though the capability was held. `ReplaceWorldCondition` does not reach this step: it validates `NewConditionClass` before the asset (and its schema) are resolved, so a struct accepted there is judged on the capability alone. A query definition with no schema attached is unaffected either way.
>
> ⚠️ **Breaking change**: a struct outside this domain's own module used to be refused with `PolicyViolation` unconditionally. `AddWorldCondition` / `ReplaceWorldCondition` / `SetWorldConditionProperty` / `SetMultipleWorldConditionProperties` now answer `CapabilityNotAvailable` and name the missing capability — and actually succeed once the capability is granted, which the previous implementation did not. A class path nothing currently loaded answers to is `NotFound`; this domain never fell back to loading an unresolved class as a side effect.
>
> **Note — `ListWorldConditionClasses` no longer hides a gated struct.** It used to filter classes by base type and module membership alone, silently dropping every struct outside `/Script/WorldConditions` from the response. It now answers from the same policy `AddWorldCondition` validates against and reports `Admission` per entry instead of dropping anything outside the family's own module — only a struct that is not a `FWorldConditionBase` descendant at all, or that never resolved, is excluded. A listing is a snapshot, not an authorization: capabilities and roles can change between the listing and the mutation, so each command re-evaluates on its own request.
>
> **`GetWorldConditionInfo` never withheld a class name and still does not** — the only redaction it performs is on the value of a `FWorldConditionContextDataRef` property, unrelated to which struct a condition instances. It now additionally reports `Admission` / `RequiredCapabilities` / `MissingCapabilities` for each condition's own struct, the same question `SetWorldConditionProperty` / `RemoveWorldCondition` would ask about it.

### Toolset bridges — WorldConditions (2) 🧩

Bridge commands via `WorldConditionTools` (UE 5.8+, Experimental). Provider: `Toolset.Editor.WorldConditions.*`. Input JSON is capped at 64 KiB.

| Command | Description |
|---|---|
| `Toolset.Editor.WorldConditions.GetQueryDescription` | Human-readable description of a `FWorldConditionQueryDefinition` |
| `Toolset.Editor.WorldConditions.GetConditionDescription` | Human-readable description of a single condition type |

---

## UAIP.Editor.Conversation 🧩

ConversationDB graph editing. Requires `CommonConversation` plugin.

| Command | Description |
|---|---|
| `ListConversationNodeTypes` 🧩 | List node classes by position (`TopLevel` / `SubNode`, omit for both). Each entry carries `Admission` (`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`) plus `RequiredCapabilities` / `MissingCapabilities` from the same policy the mutating commands below validate against. No longer filtered to `/Script/CommonConversationRuntime` — a project or plugin class, or a Blueprint generated one, is described with `Admission: RequiresCapabilities` rather than omitted. Ordered by `ClassPath`; reports `TotalCount`, `ReturnedCount`, `Truncated` (max 256 per position) — see the note below |
| `AddConversationNode` 🧩 | Add a top-level node (`UConversationNodeWithLinks` derived). Requires `ConversationCustomTypeEdit` in addition to `ConversationGraphEdit` when `NodeClass` comes from outside `/Script/CommonConversationRuntime` — see [Capability-gated custom types](#capability-gated-custom-types) |
| `AddConversationSubNode` 🧩 | Attach a SubNode to a parent Task node. Requires `ConversationCustomTypeEdit` in addition when `NodeClass` comes from outside `/Script/CommonConversationRuntime` |
| `RemoveConversationNode` 🧩 | Remove a node by NodeGuid. Requires `ConversationCustomTypeEdit` when the removed node's class is from outside `/Script/CommonConversationRuntime` — removing a top-level node also judges every SubNode removed along with it |
| `ConnectConversationNodes` 🧩 | Add a transition edge between nodes. Requires `ConversationCustomTypeEdit` when either endpoint's class is from outside `/Script/CommonConversationRuntime` |
| `DisconnectConversationNodes` 🧩 | Remove a transition edge. Requires `ConversationCustomTypeEdit` when either endpoint's class is from outside `/Script/CommonConversationRuntime` |
| `SetConversationNodeProperty` 🧩 | Set a property (FText sanitized — BIDI strip, PUA reject, 4096 char limit). The value is a JSON document; references, structs and containers are no longer refused permanently but gated by `PropertyReferenceEdit` / `PropertyStructuredEdit` — see [Writing references, structs and containers](#writing-references-structs-and-containers). Requires `ConversationCustomTypeEdit` in addition when the target node's class is from outside `/Script/CommonConversationRuntime` |

> ⚠️ **Breaking change — delete, connect, disconnect and property edits used to be ungated.** Before this capability existed, only `AddConversationNode` / `AddConversationSubNode` checked the node class being added; the other four mutating commands went through unconditionally, whatever class the node was. See [Capability-gated custom types](#capability-gated-custom-types) for the general rule this follows. Every mutation also rebuilds the database's compiled bank, which judges every node class the database already holds the same way — a database that already contains a project's own node stays compilable and repairable without a grant, since nothing about compiling or removing an existing node runs code the request itself supplies.

> **A Blueprint generated task or sub-node class is no longer refused outright.** Before this capability existed, a Blueprint subclass of `UConversationTaskNode` / `UConversationRequirementNode` / `UConversationSideEffectNode` / `UConversationChoiceNode` — which the stock graph editor's own "Add Node" menu offers alongside the native classes — was always refused by `AddConversationNode` / `AddConversationSubNode`, with no way to grant access to it. It is judged the same way any project- or plugin-defined class is: reachable once the session holds `ConversationCustomTypeEdit`.

> ⚠️ **Changed — `ListConversationNodeTypes` no longer reports `NodeTypesTruncated`.** The response now carries the shared `Truncated` field (alongside `TotalCount` / `ReturnedCount`) that every capped UAIP listing reports; a caller still reading `NodeTypesTruncated` finds nothing there.

### Toolset bridges — Conversation (5) 🧩

Bridge commands via the `ConversationToolset` (UE 5.8+). Provider: `Toolset.Editor.Conversation.*`. These are observation-only; the native commands above cover editing.

| Command | Description |
|---|---|
| `Toolset.Editor.Conversation.ListConversationEntryPoints` | List entry point nodes in a `UConversationDatabase` |
| `Toolset.Editor.Conversation.ListConversationSpeakers` | List speakers defined in a `UConversationDatabase` |
| `Toolset.Editor.Conversation.ListConversationNodes` | List all nodes with the refPath used by the two commands below |
| `Toolset.Editor.Conversation.GetConversationNodeConnections` | Connection graph for a node identified by `NodeRefPath` |
| `Toolset.Editor.Conversation.ListConversationNodeSubNodes` | Sub-nodes (choices, requirements, side-effects) of a node |

---

## UAIP.Editor.ControlRig

ControlRig hierarchy and RigVM graph editing.

#### Control Rig asset formats

UE 5.8 has two Control Rig asset formats, and every native command here accepts both with the same parameters (undo / redo, the dirty mark and the ModularRig protection work the same way):

| Format | Class path | Note |
|---|---|---|
| Runtime asset (UE 5.8 default) | `/Script/ControlRig.ControlRigRuntimeAsset` | Does not exist on UE 5.7 |
| Legacy Blueprint | `/Script/ControlRigDeveloper.ControlRigBlueprint` | |

Which format a new asset gets is decided by the project's console variable `RigVM.BlueprintIndependentAssets` (on by default in UE 5.8; `RigVM.BlueprintIndependentAssets=0` under `[ConsoleVariables]` in the project's `DefaultEngine.ini` selects the legacy format). The variable affects the whole project, including the editor's own Create menu; UAIP never changes it.

- **`CreateAsset` follows the setting.** The class path must match it: asking for the legacy class while the project creates runtime assets (or the other way around) is refused with `InvalidParams`, nothing is created, and the message names the right class and the variable to change. A missing `ControlRigBlueprintCreate` capability is reported first, and an existing asset at `AssetPath` is reported before a factory mistake. With the project set to the legacy format, `FactoryClassName` is not needed for the legacy class.
- **The earlier `/Script/ControlRig.ControlRigBlueprint` class path was wrong** — it does not resolve on UE 5.8 ("class could not be resolved"). Use one of the two paths above.
- **Asset paths in responses** are always the asset itself (`/Game/X.X`). A runtime asset's inner part path (`/Game/X.X:X_EditorOnly`) is accepted as input by these native commands and answered with the asset path.
- **`AddVariable` returns the name actually given**, recompiles the rig, and keeps the initial value across save and reopen. On a runtime-asset Control Rig, `IsReadOnly` is accepted but has no effect: the engine does not apply it, and the variable stays readable and writable.
- **`Toolset.Editor.ControlRig.*` rejects the runtime-asset format** with `UnsupportedOperation`, before anything is delegated, and names the equivalent `UAIP.Editor.ControlRig.*` command (or points at this domain when there is none). This is checked before the ModularRig protection. Legacy assets and unreadable assets are handled by the Toolset as before. `Toolset.Editor.ControlRig.Create` always creates the **legacy** format regardless of the project setting, and an existing asset at the destination is handled as it always was.
- **`CreateAsset` with `ClassName=/Script/Engine.Blueprint` and a Control Rig `FactoryParams.ParentClass` is refused** with `InvalidParams` before anything is created (the parent is `UControlRig` or a subclass: a Modular Rig, a project-defined subclass, a Control Rig generated class). The generic Blueprint factory would have produced a plain Blueprint of that class, not a Control Rig asset, without checking the `ControlRigBlueprintCreate` capability, and the Control Rig commands cannot edit it. The message names the class to use in `ClassName` (the runtime-asset class or the legacy class, whichever the project creates) and says to keep the parent class in `FactoryParams.ParentClass` (for example `/Script/ControlRig.ModularRig`). A missing capability, an occupied `AssetPath` and a wrong `FactoryClassName` are reported before this.
- On UE 5.7 only the legacy format exists; a request for the runtime-asset class is `InvalidParams` ("class could not be resolved").

### Native (68)

#### Hierarchy observation (10)

| Command | Description |
|---|---|
| `GetElements` | List all hierarchy elements |
| `GetAllBones` | List all bones |
| `GetAllNulls` | List all Null elements |
| `GetAllControls` | List all Control elements |
| `GetGlobalTransform` | Get an element's global transform |
| `GetLocalTransform` | Get an element's local transform |
| `GetParent` | Get an element's parent |
| `GetChildren` | List an element's children |
| `GetModuleInstances` | List ModularRig module instances |
| `GetControlSettings` | Get a Control's `FRigControlSettings` (Gizmo, Limits) |

#### Hierarchy editing (11)

| Command | Description |
|---|---|
| `AddElement` | Add a generic element (ElementType-specified) |
| `AddBone` | Add a bone |
| `AddNull` | Add a Null element |
| `AddControl` | Add a Control element (ControlType allowlist) |
| `RemoveElement` | Remove an element |
| `RemoveBone` | Remove a bone |
| `RemoveNull` | Remove a Null element |
| `RemoveControl` | Remove a Control element |
| `ReparentElement` | Change an element's parent (MaintainGlobalTransform option) |
| `SetControlOffset` | Set a Control's initial local transform |
| `SetControlSettings` | Set a Control's `FRigControlSettings` |

#### Transforms (3)

| Command | Description |
|---|---|
| `SetGlobalTransform` | Set an element's global transform |
| `SetLocalTransform` | Set an element's local transform |
| `ImportBonesFromAsset` | Import bone hierarchy from a SkeletalMesh / Skeleton asset |

#### Graph management (11)

| Command | Description |
|---|---|
| `ListGraphs` | List all RigVM graphs |
| `GetGraph` | Get a graph's info |
| `AddGraph` | Add a custom graph |
| `DeleteGraph` | Delete a custom graph (built-ins rejected) |
| `GetForwardSolveGraph` | Get the ForwardSolve graph |
| `GetBackwardSolveGraph` | Get the BackwardSolve graph |
| `GetInteractionGraph` | Get the Interaction graph |
| `GetEventGraph` | Get the graph for a specified event |
| `AddEventGraph` | Add an event graph |
| `AddBackwardSolveGraph` | Add a BackwardSolve graph |
| `AddInteractionGraph` | Add an Interaction graph |

#### Nodes (10)

| Command | Description |
|---|---|
| `AddGraphNode` | Add a node to the RigVM graph (StructPath + SolveEventName) |
| `RemoveGraphNode` | Remove a node by NodeName |
| `ListNodes` | List nodes in a graph |
| `GetNodeInfo` | Get a node's StructPath, pin types, metadata |
| `FindNodes` | Search nodes by StructPath / NamePattern |
| `GetNodePosition` | Get a node's graph position |
| `SetNodePosition` | Set a node's position |
| `DuplicateNode` | Duplicate a node (returns the duplicate's name) |
| `AddEventNode` | Add an event node |
| `AddVariableNode` | Add a variable node |

#### Pins (7)

| Command | Description |
|---|---|
| `ListPins` | List a node's pins |
| `GetPinValue` | Get a pin's value |
| `SetPinValue` | Set a pin's value |
| `ResetPinValue` | Reset a pin's value to default |
| `GetConnectedPins` | Get a pin's connection info |
| `ConnectControlRigPins` | Connect two pins in the RigVM graph |
| `DisconnectControlRigPins` | Disconnect a pin connection |

> **Fixed — a missing graph and an unreadable asset now answer different error codes.** Every command below that resolves a model by `GraphName` (`GetGraph`, `AddGraph`, `DeleteGraph`, `AddGraphNode`, `AddEventNode`, `AddVariableNode`, `FindNodes`, `GetConnectedPins`, `GetNodeInfo`, `GetNodePosition`, `GetPinValue`, `ListNodes`, `ListPins`, `SetNodePosition`, `SetPinValue`, `ResetPinValue`, `DuplicateNode`) used to answer `ExecutionFailed` with "Graph is null." both when `GraphName` matched no model and when the asset's own ControlRigBlueprint reference was itself invalid — the dedicated "not found" response existed in the code but was never actually reached, because both situations were reported the same way internally. The two are now told apart: `GraphName` matching no model in an otherwise valid asset answers `NotFound`; the asset's own ControlRigBlueprint being unreadable still answers `ExecutionFailed`. A caller can now tell "a different `GraphName` might work" apart from "retrying is pointless until the asset itself loads."
>
> ⚠️ **Breaking change — `GraphName`'s short-form match is common, and the commands that write to the asset now refuse an ambiguous one instead of picking a graph.** `GraphName` accepts a prefix — a caller may pass a short name and the command matches whichever full RigVM model name starts with it, an intentional abbreviation rather than an edge case. Matching more than one model this way used to resolve silently to one of them everywhere. It still does for the eight read-only commands above and in the sections below — `FindNodes`, `GetConnectedPins`, `GetGraph`, `GetNodeInfo`, `GetNodePosition`, `GetPinValue`, `ListNodes`, `ListPins` — since inspecting the wrong graph has no side effect to correct. The seven commands that write to the asset no longer do: `AddEventNode`, `AddVariableNode`, `DeleteGraph`, `DuplicateNode`, `ResetPinValue`, `SetNodePosition`, `SetPinValue` now answer `InvalidParams` without changing anything when `GraphName` matches more than one model, and report every candidate's full model name under `Result.MatchedFullGraphNames`. Re-issue the call with one of those full names as `GraphName` to resolve to exactly one graph — no new parameter was added for this, unlike the `GraphGuid` / `MatchedGraphGuids` contract Blueprint and AnimBlueprint use, because ControlRig's own short-form lookup already gives an unambiguous full name to fall back to.

#### Variables (5)

| Command | Description |
|---|---|
| `AddVariable` | Add a RigVM variable. The default value is validated once the variable's type has resolved, and a refused default **removes the variable again**, matching `AddBlueprintVariable`. The default is engine text only — set a reference or container default afterwards with `SetBlueprintDefault`. A refused call does not mark the asset dirty. Returns the name the variable actually received (the engine may normalize names, e.g. ones with spaces) and recompiles the rig. On a UE 5.8 runtime-asset Control Rig, `IsReadOnly` is accepted but has no effect — the variable stays readable and writable |
| `ListVariables` | List RigVM variables |
| `GetVariable` | Get a RigVM variable's value |
| `ChangeVariableType` | Change a RigVM variable's type |
| `RemoveVariable` | Remove a RigVM variable |

#### Rig hierarchy components (9)

Components (`FRigBaseComponent` substructs) attached to a hierarchy element. These are the generic commands: they work for every component type the module allowlist covers, including the ControlRigDynamics and ControlRigPhysics types that the two domains below give typed commands for. A component is addressed by `ElementName` plus `ElementType` (`Bone`, `Null`, or `Control` — `All` is not accepted) plus `ComponentName`. The four read commands require `EditorInspect`; the five write commands require `ControlRigComponentEdit` (denied by default) and are rejected while PIE is running.

| Command | Description |
|---|---|
| `ListComponents` | List one element's components, or the whole hierarchy's when neither `ElementName` nor `ElementType` is given. Each entry carries the owning element, the type path, and `IsProcedural`; the response reports `TotalCount` / `ReturnedCount` / `Truncated` |
| `GetComponent` | Type and content of one component. `ContentText` (the engine export form) is always present; `Content` (JSON) is an explicit `null` with a `ContentConversion` reason when the type cannot be expressed as JSON, so an unconvertible component is never mistaken for an empty one |
| `ListAddableComponentTypes` | Every `FRigBaseComponent` substruct the running editor knows, whether or not the target hierarchy holds any components yet. Each entry carries `Admission` (`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`) plus `RequiredCapabilities` / `MissingCapabilities` from the same policy `AddComponent` validates against, and `TotalCount` / `ReturnedCount` / `Truncated` on the response — see the note below |
| `CanAddComponent` | Whether a type could be attached to an element, without attaching it. Reports `Admission` plus `RequiredCapabilities` / `MissingCapabilities` the same way the listing above does, and — only for a type this session is already entitled to use — also asks the engine and reports its answer as `CanAdd` / `FailureReason`; see the note below |
| `AddComponent` | Attach a new component, optionally with initial content — `Content` (JSON) **or** `ContentText` (export form), not both. Validated in full before anything is created, so a rejected request leaves nothing behind |
| `RemoveComponent` | Remove a component. `ReferenceHandling` decides what happens to components that hold its key — `Reject` (default), `Detach`, or `Force`. Every reference found is reported under `References` with what happened to it |
| `RenameComponent` | Rename a component to `NewName` and repoint the references to it |
| `ReparentComponent` | Move a component to the element named by `NewParentName` plus `NewParentType`, and repoint the references to it. A destination element that does not exist is refused before anything changes |
| `SetComponentContent` | Replace a component's content — `Content` **or** `ContentText`, exactly one required — then read the component back and report what was actually written |

> **⚠️ Changed — `ListAddableComponentTypes` and `CanAddComponent` report `Admission`, not a plain `Addable` flag**: each entry carries `Admission` — one of `Allowed` (usable by this session right now), `RequiresCapabilities` (usable once an operator grants the capabilities named in `MissingCapabilities`, itself a subset of `RequiredCapabilities`), `NotAddable` (refused for a structural reason no capability grant fixes — wrong base type, `Deprecated`, or `Hidden`), or `CompatibilityUnknownUntilAuthorized` (the session already holds `ControlRigCustomTypeEdit` for this struct, but the engine's own compatibility check has not run for it — see [Capability-gated custom types](#capability-gated-custom-types)) — plus `RequiredCapabilities` / `MissingCapabilities`. `CanAddComponent` additionally asks the engine — `URigHierarchy::CanAddComponent` — but **only for a type whose `Admission` is `Allowed` or `CompatibilityUnknownUntilAuthorized`**: a type reported `NotAddable` or `RequiresCapabilities` is answered without touching the engine at all, so a session that does not hold the capability never runs that type's own code. The engine's answer never overwrites `Admission` — it lands in `CanAdd` / `FailureReason` instead, so the two can be read together (`Admission: CompatibilityUnknownUntilAuthorized` with `CanAdd: false` means the session is authorized but the engine still refuses the combination). ⚠️ **Breaking — the boolean `Addable` and the string `NotAddableReason` these two commands used to report are gone**; a caller that branched on either must switch to `Admission`. A `ComponentStructPath` that is malformed is now `InvalidParams` on `CanAddComponent` rather than a `CanAdd: false` response, matching `AddComponent`.
>
> **Note — the name you asked for is not always the name you get**: `AddComponent`, `RenameComponent` and `ReparentComponent` do not fail on a name collision. The engine assigns a free name instead, and the result reports the key the component actually carries (`RenameComponent` and `ReparentComponent` also set `NameChanged`). Use the reported key from then on. Renaming to the name a component already has, or reparenting to the element it already hangs off, succeeds and changes nothing.
>
> **Note — properties that are not written are listed, not reset**: object references, delegates and runtime-only state are never written from outside. `AddComponent`, `SetComponentContent` and the typed `Set*` commands of the two domains below report them under `FilteredProperties`, and each of them keeps the value it already had rather than falling back to a default.
>
> **Note — an empty `ReferenceWarnings` does not on its own mean nothing broke**: `RemoveComponent` with `Detach` or `Force` reports under `ReferenceWarnings` every component left with an end that resolves to nothing, because neither the engine nor the simulation says anything when that happens — a dynamics constraint that loses one of its particles is skipped without a message, and a physics body or joint that loses its solver or its parent body silently attaches itself to whatever the engine's automatic search finds instead. Those components are left in place; nothing is removed on their behalf. A component whose type this command does not understand cannot be warned about, so read `References` as well. `Reject` and `Detach` both refuse rather than leave such a reference behind — `Force` is the mode that removes that safeguard.
>
> **Note — components the rig created for itself cannot be edited**: an entry reported with `IsProcedural: true` is rebuilt by rig execution rather than authored, and every write command here refuses it.

#### Other (2)

| Command | Description |
|---|---|
| `CompileControlRig` | Compile the ControlRig (per-session 1 s rate limit) |
| `GetAvailableRigVMUnitStructs` | List FRigUnit-derived UScriptStructs (max 1000), each with `Admission` (`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`) plus `RequiredCapabilities` / `MissingCapabilities` from the same policy `AddGraphNode` validates against. Reports `SchemaVersion` (3), `TotalCount`, `ReturnedCount`, `Truncated` |

> **⚠️ Changed — `GetAvailableRigVMUnitStructs` now answers with `SchemaVersion: 3`**: each entry carries `Admission` — the same four values `ListAddableComponentTypes` and `CanAddComponent` report in the note above — plus `RequiredCapabilities` / `MissingCapabilities`, sourced from the same policy `AddGraphNode` validates against. This replaces the boolean `Addable` and the string `NotAddableReason` that `SchemaVersion: 2` used to report; a caller that branched on either must switch to `Admission`. `ClassPath` and `ClassDisplayName` are unchanged, so an existing reader that only used those keeps working. The response also reports `TotalCount` (the full count before the entry cap), `ReturnedCount`, and `Truncated`, listed in `ClassPath` order so a response cut short by the entry cap always cuts the same tail.
>
> **⚠️ Breaking — the module allowlist behind `AddGraphNode` is now an exact match**: a `StructPath`'s owning package used to be accepted whenever it merely **began with** `/Script/ControlRig`, `/Script/AnimationCore`, or `/Script/Engine`. It is now compared for equality against a list of seven modules — `/Script/ControlRig`, `/Script/ControlRigDynamics`, `/Script/ControlRigPhysics`, `/Script/ControlRigSpline`, `/Script/ControlRigModules`, `/Script/AnimationCore`, `/Script/Engine`. A package that only shared a prefix — `/Script/ControlRigDeveloper`, `/Script/ControlRigEditor`, `/Script/EngineMessages` and the like — was accepted before and is now rejected with `ModuleNotAllowed`. A call that relied on that stops working, and there is no opt-out: the list was never meant to reach those modules.
>
> **Note — the ControlRig sibling modules are on that list on purpose now**: `/Script/ControlRigDynamics`, `/Script/ControlRigPhysics`, `/Script/ControlRigSpline` and `/Script/ControlRigModules` used to be reachable only incidentally, as a side effect of the `/Script/ControlRig` prefix. They are named explicitly, so the roughly 73 physics rig units (`FRigUnit_SpawnPhysicsSolver`, `FRigUnit_AddPhysicsBody`, `FRigUnit_AddPhysicsJoint`, and so on) stay addable under the stricter rule rather than being caught by it. The node allowlist and the component allowlist cover the same set of modules, so a type you can create a component of is also a type you can place as a node.

> **Note — project- and plugin-defined RigVM unit structs and rig hierarchy component structs are capability-gated**: a `StructPath` naming a struct from one of the seven modules this domain has always accepted is used the same way as before. A struct outside those modules — one a project or a plugin declares — now requires `ControlRigCustomTypeEdit`. This applies to both families of type this domain admits: `FRigUnit` descendants placed as graph nodes by `AddGraphNode`, and `FRigBaseComponent` descendants attached by `AddComponent`. Control types (`AddControl`, `SetControlSettings`) are not gated at all — the set of control types is fixed by the engine, so there is no control type of a project's own for a capability to guard.
>
> Unlike Material, there is no companion "dangerous type" capability here: a unit struct is a compiled function the VM calls with values from pins, and a component struct is data hanging off a hierarchy element — neither carries code the caller supplied. Structs marked `Deprecated` or `Hidden`, and structs that do not derive from the expected base at all, stay refused **regardless of any capability held**; those are types that cannot be used at all, not a danger a grant unlocks.
>
> This check is not limited to `AddGraphNode` and `AddComponent` — see [Capability-gated custom types](#capability-gated-custom-types) for the general rule, and the breaking change immediately below for what it means in this domain specifically.
>
> ⚠️ **Breaking change — operations on an existing node or component of a gated type now require the capability too.** Before this change only `AddGraphNode` and `AddComponent` consulted the type policy at all; every other route into the same rig went through unconditionally. A session that does not hold `ControlRigCustomTypeEdit` can no longer: delete a node whose unit struct is project- or plugin-defined (`RemoveGraphNode`), connect or disconnect its pins (`ConnectControlRigPins`, `DisconnectControlRigPins`), write or reset one of its pin defaults (`SetPinValue`, `ResetPinValue`), move it (`SetNodePosition`), duplicate it (`DuplicateNode`), or remove, rename, reparent or rewrite the content of a component whose struct is project- or plugin-defined (`RemoveComponent`, `RenameComponent`, `ReparentComponent`, `SetComponentContent`, and every typed `Set*` command of the Dynamics and Physics domains below).
>
> `CompileControlRig` is **not** affected: this domain has no dangerous kind of type, so compiling a rig that merely contains a project-defined unit struct or component struct requires nothing extra. The same holds for the graph-level commands that name no type of their own — `AddGraph`, `DeleteGraph`, `AddEventGraph`, `AddBackwardSolveGraph`, `AddInteractionGraph`, `AddEventNode`, `AddVariableNode`.
>
> ⚠️ **Breaking change — a struct that is not loaded is answered `NotFound`, not `InvalidParams`.** `AddGraphNode` and `AddComponent` no longer load the struct named by `StructPath` as a side effect; loading it would run its module's code in order to decide whether the caller was allowed to name it. A struct that is not already in memory is refused with `NotFound` and a sentence saying nothing is loaded on demand to answer the question. A `StructPath` that is malformed — empty, longer than 256 characters, or holding a character an object path is never built from — is still `InvalidParams`, because that is a statement about the parameter rather than about a type.
>
> The order two refusals arrive in also changed: the struct used to be judged before the asset was looked for, so a request that got both the struct and the asset path wrong was answered about the struct. It is judged with the asset in hand now — the same judgement has to be able to take in what the rig already holds — so such a request is answered about the asset instead. The shape of `StructPath` is still checked first, so an obvious typo still answers `InvalidParams` before anything is loaded.
>
> **⚠️ The parent class named at asset creation is gated too.** `CreateAsset`'s `FactoryParams.ParentClass` — the `UControlRig` subclass a new Control Rig asset is built from — used to be accepted on the factory's own conditions alone: it resolved, it derived from `UControlRig`, and (for the blueprint-based factory) it could serve as a Blueprint base. It now goes through the same origin rule as the unit and component structs above, so a class from outside the seven modules listed there needs `ControlRigCustomTypeEdit`. **Every parent class the engine ships stays free**, since they all live in those modules; what needs the capability is a class of the project's own — a native `UControlRig` subclass declared by the project or a third-party plugin, and the generated class of a Control Rig Blueprint in the project (`/Game/….CR_Foo_C`). Omitting `ParentClass` still produces a plain `UControlRig` and asks for nothing. The class is no longer loaded on demand: one that is not already in memory is refused rather than loaded to answer the question. A missing `ControlRigCustomTypeEdit` for a parent class is reported as `CapabilityNotAvailable`, naming the capability, the same as everywhere else — see [Capability-gated custom types](#capability-gated-custom-types). A structural refusal (unresolved, wrong base type) is `InvalidParams`. Separately, the `ControlRigBlueprintCreate` check that guards the command as a whole is now asked of the calling session rather than of the process, so a session bound to a role that denies it is refused where it used to be allowed; that refusal is still `PolicyViolation`.

### Toolset bridges (107) 🧩

Two bridge providers, both delegating to `AnimationAssistantToolset` (UE 5.8+).

**`Toolset.Editor.ControlRig.*` (44)** — mirror of the native asset-editing commands above. Groups: asset creation (1; `Create` always makes a legacy-format Control Rig, whatever the project's `RigVM.BlueprintIndependentAssets` setting — unlike `CreateAsset`; see [Control Rig asset formats](#control-rig-asset-formats)), hierarchy observation (8), hierarchy editing (7), graph management (10), nodes (7), pins (6), variables (5).

**`Toolset.Editor.SequencerControlRig.*` (63)** — animation-time control authoring. Implemented in the Sequencer module (`SequencerControlRigTools`) but documented here because every command acts on ControlRig controls. Requires `MovieSceneAnimMixer` in addition to ControlRig. On UE 5.8, the 38 commands that take a `ControlRigPath` (the other 25 do not, and are unaffected) refuse a runtime-asset Control Rig with `UnsupportedOperation` before anything is delegated, because the delegated toolset finds a rig in the sequence by its Blueprint class, which a runtime asset does not have, and would either fail to find it or act on a different legacy rig whose path happens to overlap. Read-only commands (`Get...` / `Is...`) are refused the same way. The message names the command and the asset path, whether given as an object path (`/Game/Rigs/CR_X.CR_X`) or a package path (`/Game/Rigs/CR_X`). There is no native equivalent to point at. A missing `AssetPath` or `ControlRigPath` is still `InvalidParams` first; a legacy rig, a path that names no asset and a value that is not an asset path are delegated as before. Groups:

| Group | Count | Commands |
|---|---:|---|
| Control values | 16 | `Get`/`SetFloatValue`, `BoolValue`, `IntValue`, `Vector2DValue`, `PositionValue`, `RotatorValue`, `ScaleValue`, `EulerTransformValue` |
| World transforms | 3 | `GetWorldTransform`, `SetWorldTransform`, `GetActorTransformAtFrame` |
| Layered rigs | 6 | `CollapseAnimLayers`, `IsLayeredControlRig`, `SetLayeredMode`, `Get`/`SetPriorityOrder`, `IsFKControlRig` |
| Anim layers | 6 | `GetControlRigAnimLayers`, `AddControlRigLayerFromSelection`, `Delete`/`Duplicate`/`Reorder`/`MergeControlRigAnimLayers` |
| Spaces | 4 | `Set`/`Move`/`Delete`/`BakeControlRigSpace` |
| Tweening | 3 | `TweenControlRig`, `BlendValuesOnSelected`, `SnapControlRig` |
| Mirroring | 3 | `SelectMirroredControls`, `MirrorSelectedControls`, `ZeroControlRigTransforms` |
| Selection | 4 | `GetSelectedControls`, `SelectControl`, `ClearControlSelection`, `FrameControlSelection` |
| FBX | 2 | `ExportFBXFromRig`, `ImportFBXToRig` |
| Sequencer queries | 4 | `GetSequencerControlRigs`, `GetSequencerControlsInfo`, `Get`/`SetControlRigTransformInSequencer` |
| Anim mode settings | 12 | `Get`/`Set` for `AnimModeGizmoScale`, `AnimModeHierarchy`, `AnimModeNulls`, `AnimModeHideManips`, `AnimModeOnlyRigSel`, `AnimModeLocalSpaces` |

---

## UAIP.Editor.ControlRig.Dynamics 🧩

Typed editing of the `ControlRigDynamics` component types on a ControlRig hierarchy — solver, particle, collider, constraint, cone limit and confiner — plus four commands that build or rewire a whole setup in one call. Requires UE 5.8+ and the `ControlRigDynamics` plugin (Experimental); the whole domain is unavailable on UE 5.7 or with the plugin disabled. The generic component commands under [`UAIP.Editor.ControlRig`](#uaipeditorcontrolrig) reach the very same components without this plugin — what these commands add is a named, range-checked schema per type. No Toolset bridge exists for this domain.

Every command here reports `Stability: Experimental`, because `ControlRigDynamics` is an Experimental engine plugin and its structs may change across engine minor versions. Reads require `EditorInspect`; every write requires `ControlRigComponentEdit` (denied by default) and is rejected while PIE is running. This domain and `UAIP.Editor.ControlRig.Physics` are independent of each other — a project can have either one without the other, and each appears on its own.

> **Prerequisite — enable the plugin and restart the editor**: on an editor build, UAIP compiles in support for `ControlRigDynamics` automatically whenever the engine you're building against has it — you no longer need to add it to the `Plugins` array of your `.uproject` or rebuild. What's left is enabling the plugin itself (`ControlRigDynamics` is Experimental and off by default, so most projects do need this step): enable it from **Edit → Plugins** (or add `{ "Name": "ControlRigDynamics", "Enabled": true }` to `.uproject` yourself) and restart the editor. While the plugin is disabled, the whole domain is missing from `uaip_list_commands`, and calling one of these commands returns `CommandNotFound` naming the plugin to enable; `UAIP.Core.ListIntegrations` reports the domain's state directly.

#### Typed reads (6) — requires `EditorInspect`

| Command | Description |
|---|---|
| `GetDynamicsSolverSettings` | `Settings`, `SpaceMotion` and `TeleportDetection` of a `FRigDynamicsSolverComponent`. Its `Particles` / `Colliders` / `Constraints` / `ConeLimits` / `Confiners` reference arrays are not reported here — read them with `GetComponent` |
| `GetDynamicsParticleProperties` | `ParticleProperties` of a `FRigDynamicsParticleComponent` |
| `GetDynamicsColliderShapes` | `Shapes` (`Boxes`, `Capsules`, `Planes`) of a `FRigDynamicsColliderComponent`, shaped the same way `SetDynamicsColliderShapes` accepts them back |
| `GetDynamicsConstraintSettings` | `ConstraintType`, `Strength`, `DampingRatio`, `ExtraDamping`, `bAccelerationMode`, `LengthMultiplier` and `ExtraLength` of a `FRigDynamicsConstraintComponent`. The topology keys are not reported here |
| `GetDynamicsConeLimitSettings` | `Strength`, `DampingRatio` and `Angle` of a `FRigDynamicsConeLimitComponent`. The topology keys are not reported here |
| `GetDynamicsConfinerSettings` | `Shapes` and `Strength` of a `FRigDynamicsConfinerComponent` |

#### Typed writes (6) — requires `ControlRigComponentEdit`

| Command | Description |
|---|---|
| `SetDynamicsSolverSettings` | Replace `Settings`, `SpaceMotion` and/or `TeleportDetection`. The solver's reference arrays cannot be changed here — use `AddComponentToDynamicsSolver` / `RemoveComponentFromDynamicsSolver` |
| `SetDynamicsParticleProperties` | Replace one or more `ParticleProperties` fields. `Radius` and `Mass` must be strictly positive; `Strength`, `DampingRatio`, `ExtraDamping`, `AngleLimit`, `AngleLimitStrength` and `Damping` must not be negative; `TargetMode` is 0.0–1.0; `MovementType` is `Kinematic` or `Simulated` |
| `SetDynamicsColliderShapes` | Replace the whole `Shapes` collection. Every transform must be finite, box and plane extents positive on every axis, capsule radius positive, capsule length not negative |
| `SetDynamicsConstraintSettings` | Replace one or more settings. `ConstraintType` is `Hard` or `Soft`; `Strength`, `DampingRatio`, `ExtraDamping` and `LengthMultiplier` must not be negative; `ExtraLength` may be any finite number. The topology keys are carried through unchanged |
| `SetDynamicsConeLimitSettings` | Replace `Strength`, `DampingRatio` and/or `Angle`; all three are refused when negative or non-finite. The topology keys cannot be changed here — use `SetComponentContent` |
| `SetDynamicsConfinerSettings` | Replace `Shapes` and/or `Strength`. Shape validation matches `SetDynamicsColliderShapes`; `Strength` must be finite and not negative |

#### Orchestration (5) — requires `ControlRigComponentEdit`

| Command | Description |
|---|---|
| `AddDynamicsChain` | Build a whole chain in one call: a particle on every element from `StartElementName` down to `EndElementName`, a constraint between every adjacent pair, and one registration of all of them with the named solver. `StartElementName` must be an ancestor of `EndElementName` and the two may not be the same element. Optional `ParticleContent` / `ConstraintContent` are applied to every component of that kind; `ConstraintContent` may not name the topology keys, since the chain decides which particles each constraint joins |
| `ImportDynamicsCollidersFromPhysicsAsset` | Create one collider per body of a PhysicsAsset whose bone exists on the rig, converting box, sphere and capsule shapes (a sphere becomes a zero-length capsule). Reports what it created and, under `SkippedBodies`, what it skipped and why |
| `AddComponentToDynamicsSolver` | Register a dynamics component with a solver. Which of the solver's arrays it goes into follows from the component's type and cannot be chosen; the array used is reported as `SolverArray`. Registering something the solver already names changes nothing and reports `Added: false` |
| `RemoveComponentFromDynamicsSolver` | Take a component out of every reference array of a solver. Removing something the solver does not refer to changes nothing and reports `Removed: false` |
| `RemoveDynamicsChain` | Tear down a whole chain in one call: identify it either the way `AddDynamicsChain` built it (`StartElementName` / `EndElementName` / `ElementType`) or by the exact `Particles[]` / `Constraints[]` it returned, then unregister it from the solver, delete the constraints, and delete the particles. Refuses **without changing anything** when the match is ambiguous or incomplete; `DryRun` reports the target and any external references instead of removing them |

> **Note — every typed `Set*` is a partial write, but never an empty one**: each field is independently optional and at least one is required. A field left out keeps the value the component already holds rather than falling back to the type default. Values outside the range the simulation accepts — a non-finite number, a negative mass or strength, a ratio outside 0–1, a timestep or iteration count of zero or less — are refused and leave the component unchanged. The generic `SetComponentContent` applies the same checks, so routing around a typed command does not get a rejected value in.
>
> **Note — naming a component of the wrong type answers `NotFound`, not a policy error**: passing a constraint's name to a collider command reports `NotFound`, because a mismatched type is almost always a mix-up about *which* component was meant rather than a question of which types are allowed.
>
> **Note — `ImportDynamicsCollidersFromPhysicsAsset` tells two kinds of mismatch apart**: a body whose bone is missing from the rig, whose element will not host a collider, or whose shapes are all of a kind that is not converted (convex hulls, tapered capsules, level sets) is **skipped**, and reported under `SkippedBodies` with the reason — the rest of the import goes ahead. A body whose bone does exist but whose shape values cannot be used is **refused outright**: nothing at all is created, rather than a silently partial result. The colliders it creates are not registered with any solver; do that explicitly with `AddComponentToDynamicsSolver`.
>
> **Note — `RemoveComponentFromDynamicsSolver` unregisters, it does not delete**: the component stays in the hierarchy (use `RemoveComponent` to delete it), it does not even have to still exist — a key left behind by an already-deleted component can be cleaned up this way — and it is taken out of every one of the solver's arrays rather than a chosen one. Constraints and cone limits the solver still simulates that name it are reported under `ReferenceWarnings` and left in place, because the solver skips a constraint whose particle it cannot resolve without an error or a warning.
>
> **Note — `RemoveDynamicsChain` takes exactly one way of pointing at the chain**: either the same `StartElementName` / `EndElementName` / `ElementType` (plus the solver) that `AddDynamicsChain` was given, or the exact `Particles[]` / `Constraints[]` it returned. Passing both, or neither, is `InvalidParams`. Either way the match has to be exact — a single unbroken run of particles and constraints, no branch, no loop, no gap. Anything else is refused without changing the asset: more than one candidate reports `AmbiguousElements[]`, a missing piece reports `IncompleteElements[]`. "Nothing there" reads differently by mode — a range with no chain on it is treated as already done (`Status: AlreadyAbsent`, a no-op success safe to repeat), while an exact key that does not exist is `NotFound`, since naming an individual key that is missing is a real error rather than nothing to do.
>
> **Note — `ReferenceHandling` decides what happens to references from outside the chain**, the same three values as `RemoveComponent` above (case-sensitive): `Reject` (default) refuses and reports every external reference under `References`; `Detach` removes them first, refusing upfront instead if even one cannot be detached; `Force` leaves them in place, and any left pointing at nothing are reported under `ReferenceWarnings` the same way `RemoveComponent`'s does. `DryRun` runs every check, including this one, and reports the target and any external references without touching the asset (`Status: Previewed`, `RemovedCount: 0`) — repeating the same call without `DryRun` removes exactly what was previewed.
>
> **Note — a pre-flight refusal guarantees no change; a mid-removal failure does not guarantee full recovery**: `Status` can also come back `RolledBack` or `RollbackFailed` when something fails after every check already passed. A rollback restores what it can and reports the achieved extent — `RemovedBeforeFailure[]`, `RestoredComponents[]`, `MissingAfterRollback[]`, `UnrestoredReferrers[]`, `SolverRestored` — rather than claiming full recovery, because recreating a deleted component does not reliably reproduce the same key. ⚠️ If the removal itself succeeds but the response record fails to save, the command answers `ExecutionFailed` even though the chain is already gone — `ErrorMessage` says so explicitly; this is the one command in this domain that checks the artifact save.

---

## UAIP.Editor.ControlRig.Physics 🧩

Typed editing of the `ControlRigPhysics` component types on a ControlRig hierarchy — solver, body, joint and control. Requires the `ControlRigPhysics` plugin (Beta), which is available on UE 5.7 as well as UE 5.8, unlike the Dynamics domain above. The generic component commands under [`UAIP.Editor.ControlRig`](#uaipeditorcontrolrig) reach the very same components without this plugin. No Toolset bridge exists for this domain.

Reads require `EditorInspect`; every write requires `ControlRigComponentEdit` (denied by default), is rejected while PIE is running, and is rejected against a ModularRig asset. This domain and `UAIP.Editor.ControlRig.Dynamics` are independent of each other — a project can have either one without the other, and each appears on its own.

> **Prerequisite**: on an editor build, UAIP compiles in support for `ControlRigPhysics` automatically whenever the engine you're building against has it — you no longer need to add it to the `Plugins` array of your `.uproject` or rebuild. `ControlRigPhysics` is enabled by default by the engine, so most projects already have it on and these commands work out of the box; if a project has explicitly disabled it, enable it from **Edit → Plugins** and restart the editor. While the plugin is disabled, the whole domain is missing from `uaip_list_commands`, and calling one of these commands returns `CommandNotFound` naming the plugin to enable; `UAIP.Core.ListIntegrations` reports the domain's state directly.

#### Typed reads (4) — requires `EditorInspect`

| Command | Description |
|---|---|
| `GetPhysicsSolverSettings` | `SolverSettings`, `SpaceMotion` and `TeleportDetection` of a `FRigPhysicsSolverComponent` on UE 5.8 (`SolverSettings` and `SimulationSpaceSettings` on UE 5.7). `SolverSettings.SpaceBone` is not reported here — read it with `GetComponent` |
| `GetPhysicsBodySettings` | The tunable settings of a `FRigPhysicsBodyComponent` — mass and inertia overrides, damping, `MovementType`, `CollisionType`, `KinematicTargetSpace`, gravity multiplier, blend weight, CCD, and the rest — reported at the top level. Topology, collision shapes and the kinematic target are not reported here |
| `GetPhysicsJointSettings` | `JointData` and `DriveData` of a `FRigPhysicsJointComponent`, as whole JSON objects. The parent / child body keys are not reported here |
| `GetPhysicsControlSettings` | `ControlData`, `ControlMultiplier`, `ControlTarget` and `UseParentBodyAsDefault` of a `FRigPhysicsControlComponent`. The parent / child body keys are not reported here |

#### Typed writes (4) — requires `ControlRigComponentEdit`

| Command | Description |
|---|---|
| `SetPhysicsSolverSettings` | Replace `SolverSettings`, `SpaceMotion` and/or `TeleportDetection` on UE 5.8 (`SolverSettings` and/or `SimulationSpaceSettings` on UE 5.7). A `SolverSettings` object that names `SpaceBone` is refused |
| `SetPhysicsBodySettings` | Replace one or more body settings. `MovementType` is `Static`, `Kinematic`, `Simulated` or `Default`; `CollisionType` is `NoCollision`, `QueryOnly`, `PhysicsOnly`, `QueryAndPhysics`, `ProbeOnly` or `QueryAndProbe`; `KinematicTargetSpace` is `World`, `Component`, `OffsetInBoneSpace` or `OffsetInWorldSpace`. `LinearDamping` and `AngularDamping` must not be negative. Topology, collision shapes and the kinematic target are carried through unchanged |
| `SetPhysicsJointSettings` | Replace `JointData` and/or `DriveData`. `LinearProjectionAmount` and `AngularProjectionAmount` must fall within 0.0–1.0 and `ParentInverseMassScale` must not be negative. The parent / child body keys cannot be changed here — use `SetComponentContent` |
| `SetPhysicsControlSettings` | Replace `ControlData`, `ControlMultiplier`, `ControlTarget` and/or `UseParentBodyAsDefault`. A negative strength, damping or multiplier is refused. The parent / child body keys cannot be changed here — use `SetComponentContent` |

> **⚠️ Note — the solver commands have a different schema on UE 5.7 and UE 5.8**: on UE 5.8 `GetPhysicsSolverSettings` / `SetPhysicsSolverSettings` work in terms of `SolverSettings`, `SpaceMotion` and `TeleportDetection`; on UE 5.7 the same two commands work in terms of `SolverSettings` and `SimulationSpaceSettings`. This follows the engine plugin's own struct layout. Read the command's `Description` through `uaip_describe_command` at runtime rather than assuming one shape. The other six commands have the same schema on both versions.
>
> **Note — every typed `Set*` is a partial write, but never an empty one**: each field is independently optional and at least one is required. A field left out keeps the value the component already holds rather than falling back to the type default. Values outside the range the solver accepts — a non-finite number, an iteration or step count below its minimum, a negative threshold, a ratio outside 0–1 — are refused and leave the component unchanged. The generic `SetComponentContent` applies the same checks.
>
> **Note — naming a component of the wrong type answers `NotFound`, not a policy error**: passing a joint's name to a body command reports `NotFound`, for the same reason as in the Dynamics domain.

---

## UAIP.Editor.EnhancedInput

Enhanced Input asset editing — Input Actions and Input Mapping Contexts.

| Command | Description |
|---|---|
| `ListInputActions` | List Enhanced Input Action assets in the project |
| `ListMappingContexts` | List Input Mapping Context assets in the project |
| `GetInputActionInfo` | Get an Input Action's details (ValueType, Triggers, Modifiers). Each trigger / modifier's `Params` now carries reference, container and struct values too — in the same form the setters accept — and gains a `PropertyWriteRequirements` map |
| `GetMappingContextInfo` | Get a Mapping Context's details (entries, keys, modifiers, triggers), with the same structured `Params` values and `PropertyWriteRequirements` map |
| `DeleteInputAction` | Delete an Input Action asset. Refused with `PolicyViolation` while `DisableSave` is in force |
| `DeleteMappingContext` | Delete an Input Mapping Context asset. Refused with `PolicyViolation` while `DisableSave` is in force |
| `AddInputMapping` | Add a key mapping to an Input Mapping Context |
| `RemoveInputMapping` | Remove a key mapping by index |
| `SetInputMappingKey` | Update a mapping's key |
| `SetInputMappingModifier` | Set / replace modifiers on a mapping |
| `SetInputMappingTrigger` | Set / replace triggers on a mapping |
| `SetInputActionModifier` | Set / replace modifiers on an Input Action |
| `SetInputActionTrigger` | Set / replace triggers on an Input Action |
| `GetAvailableInputTriggerClasses` | Every `UInputTrigger` subclass this editor has loaded, whether or not this session may currently name one — feed a `ClassPath` value from the result as the `Class` field of a `Triggers` entry when calling `SetInputActionTrigger` / `SetInputMappingTrigger`. Each entry carries `Admission` (`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`) plus `RequiredCapabilities` / `MissingCapabilities`, from the same policy those setters validate against — a class from outside `/Script/EnhancedInput` is listed and names `EnhancedInputCustomTypeEdit` rather than being left out, and `UInputTriggerChordAction` / `UInputTriggerChordBlocker` are listed as `NotAddable` since no capability opens them. Ordered by `ClassPath`; reports `TotalCount`, `ReturnedCount`, `Truncated` (max 200). Requires `EditorInspect` |
| `GetAvailableInputModifierClasses` | Every `UInputModifier` subclass this editor has loaded, whether or not this session may currently name one — feed a `ClassPath` value from the result as the `Class` field of a `Modifiers` entry when calling `SetInputActionModifier` / `SetInputMappingModifier`. Reports the same `Admission` / `RequiredCapabilities` / `MissingCapabilities` fields as `GetAvailableInputTriggerClasses`, from the same policy those setters validate against — a class from outside `/Script/EnhancedInput` is listed and names `EnhancedInputCustomTypeEdit` rather than being left out. Ordered by `ClassPath`; reports `TotalCount`, `ReturnedCount`, `Truncated` (max 200). Requires `EditorInspect` |

> The four trigger / modifier setters — `SetInputMappingModifier`, `SetInputMappingTrigger`, `SetInputActionModifier`, `SetInputActionTrigger` — no longer refuse references and containers outright. A reference requires `EnhancedInputReferenceEdit` on top of `EnhancedInputEdit`, a struct or container requires `PropertyStructuredEdit`, and such values are supplied as JSON rather than engine bracket text — the two getters above report the required form per property. Unlike most property writers, a `Params` key naming no property still fails the whole request: these responses have nowhere to report a skipped key.

> **Note — project- and plugin-defined Trigger and Modifier classes are capability-gated**: a `Class` from the `/Script/EnhancedInput` module is accepted the same way as before. A class from anywhere else — a project module, a plugin module, or a Blueprint subclass of `UInputTrigger` / `UInputModifier` — now requires `EnhancedInputCustomTypeEdit`. Unlike Material, there is no companion "dangerous type" capability here: a trigger evaluates key state and a modifier rescales an input value, and neither runs anything the caller supplied with the request. Two trigger kinds — `UInputTriggerChordAction` and `UInputTriggerChordBlocker`, plus anything derived from either — are refused **regardless of any capability held**: Enhanced Input builds and configures them as part of a chord rather than offering them to an author, and the engine's own class picker hides them for the same reason. `UInputTrigger` and `UInputModifier` themselves are abstract and equally unreachable. See [Safety & Capabilities](safety.md#gameplay-systems).
>
> **`Class` now accepts a full object path.** A name with no path separator is still looked up in `/Script/EnhancedInput` exactly as before (`Pressed` continues to resolve the way it always did, and `InputTriggerPressed` likewise). A class from anywhere else is named by its full object path — `/Script/MyGame.MyGameInputTrigger`, or `/Game/Input/BPT_Hold.BPT_Hold_C` for a Blueprint. Without this there was no spelling that reached such a class at all. The class must already be loaded: nothing is loaded in order to decide whether it was allowed to be, and a name that resolves to nothing answers `NotFound`.
>
> This check is not limited to the four setters — see [Capability-gated custom types](#capability-gated-custom-types) for the general rule. In this domain it additionally covers `RemoveInputMapping`, `DeleteInputAction` and `DeleteMappingContext`: removing a mapping entry, or deleting an asset, discards every Trigger and Modifier instance it holds, and a class this domain does not ship needs the same capability on the way out as on the way in. Nothing else changes about those three commands, and a target holding only Enhanced Input classes — including a chord trigger set up from the editor — is removed and deleted exactly as before, with no capability required.
>
> ⚠️ **Breaking change**: a Trigger or Modifier `Class` that failed the previous check was refused with `PolicyViolation` or `InvalidParams`. The four setters now answer `CapabilityNotAvailable` and name `EnhancedInputCustomTypeEdit` for a class that is merely from another module, `NotFound` for one that is not loaded, and `InvalidParams` for one that does not derive from `UInputTrigger` / `UInputModifier` at all. The two chord trigger kinds keep returning `PolicyViolation`. There is no compatibility window for the old codes: they meant "no permission would have helped", so keeping them would describe a permission system that did not exist.
>
> ⚠️ **Breaking change — a class of the wrong family is now refused.** The previous check never asked what a class derived from, so naming an Enhanced Input class that is neither a trigger nor a modifier — an `InputAction`, say — passed it and reached the call that instanced it into the list. That combination now answers `InvalidParams`. It never produced a usable asset.

---

## UAIP.Editor.GAS 🧩

Editor-time GameplayAbilities asset editing — GameplayCue tags and Cue Notify assets. Requires `GameplayAbilities` plugin (plus `GASToolsets` for the bridge variants).

### Native (8)

| Command | Description |
|---|---|
| `AddCueTag` | Add a `GameplayCue.*` tag to the project tag tables |
| `RemoveCueTag` | Remove a `GameplayCue.*` tag |
| `ListCues` | List all GameplayCue tags |
| `GetCueInfo` | Get a GameplayCue tag's details and registered Cue Notify assets |
| `FindCueNotifyAssets` | Find Cue Notify assets that handle a tag |
| `FindCueTagsWithoutNotifies` | Find GameplayCue tags that have no associated Notify asset |
| `CreateCueNotifyAsset` | Create a new GameplayCueNotify asset (Actor / Static / Burst) |
| `ExecuteCueOnSelectedActor` | Execute a GameplayCue on the currently selected actor (testing convenience) |

### Toolset bridges (14) 🧩

Mirror of native commands via the `GASToolsets` plugin (UE 5.8+). Provider: `Toolset.Editor.GAS.*`. Groups: runtime inspection (6) — `GetAttributeValues`, `GetActiveEffects`, `GetGrantedAbilities`, `GetActiveTags`, `FindAttributeSetClasses`, `ListAttributes`; GameplayCue authoring (8) — `ListCues`, `GetCueInfo`, `FindCueNotifyAssets`, `FindCueTagsWithoutNotifies`, `ExecuteCueOnSelectedActor`, `CreateCueNotifyAsset`, `AddCueTag`, `RemoveCueTag`.

---

## UAIP.Editor.Python 🧩

Python command extension. Requires `PythonScriptPlugin`.

| Command | Description |
|---|---|
| `ReloadPythonCommands` 🧩 | Rescan the commands directory and update existing handler descriptors in-place |
| *(dynamic commands)* 🧩 | Commands registered via the `@uaip_command` decorator (names depend on user scripts) |

---

## UAIP.Editor.Sandbox 🧩

Sandbox session lifecycle management. Requires the `FileSandbox` plugin. When `FileSandbox` is not enabled all commands in this section return `CommandNotFound`.

| Command | Description |
|---|---|
| `GetSandboxStatus` 🧩 | Query the current sandbox status — `Active`, `IsStale`, `SessionId`, and `OwnerUAIPSessionId` |
| `GetSandboxChanges` 🧩 | List pending changes inside the active sandbox — `FilePath`, `ChangeKind` (Added / Edited / Removed), `SizeBytes`, and `TotalCount` |
| `BeginSandboxSession` 🧩 | Open a new FileSandbox session; subsequent asset writes are redirected to the sandbox |
| `EndSandboxSession` 🧩 | End the active sandbox session; uncommitted changes are reverted automatically |
| `CommitSandboxChanges` 🧩 | Flush selected (or all) pending sandbox changes to disk; returns `CommittedFiles`, `SkippedFiles`, and `CommittedCount` |
| `RevertSandboxChanges` 🧩 | Discard all pending sandbox changes without committing |

---

## UAIP.Editor.WorldPartition

World Partition, Data Layer, and HLOD management for partitioned worlds (requires `WorldPartition` plugin). All commands in this section return `CommandNotFound` when the project does not have World Partition enabled.

### World Partition (12)

| Command | Description |
|---|---|
| `GetWorldPartitionInfo` | Get World Partition configuration — streaming mode, runtime hash class, and whether WP is enabled for the current level |
| `GetWorldPartitionStreamingGrids` | List runtime streaming grids defined in the World Partition settings |
| `GetRuntimeGridSettings` | Get the settings for a specific runtime grid by name |
| `SetRuntimeGridSettings` | Set the settings for a specific runtime grid (requires `WorldPartitionEdit`) |
| `GetActorWorldPartitionSettings` | Get the World Partition settings for an actor — HLOD Layer, spatially loaded flag, and runtime grid name |
| `SetActorIsSpatiallyLoaded` | Set whether an actor is spatially loaded in World Partition (requires `WorldPartitionEdit`) |
| `SetActorRuntimeGrid` | Assign an actor to a specific runtime streaming grid (requires `WorldPartitionEdit`) |
| `SetWorldPartitionStreamingEnabled` | Enable or disable World Partition streaming for the current level (requires `WorldPartitionEdit`) |
| `PinActorInWorldPartition` | Pin an actor so it is always loaded regardless of streaming state (requires `WorldPartitionEdit`) |
| `UnpinActorFromWorldPartition` | Remove the always-loaded pin from an actor (requires `WorldPartitionEdit`) |
| `DumpWorldPartitionCells` | Dump the current World Partition streaming cell grid as a JSON artifact |
| `ListExternalActors` | List actors stored as external packages (World Partition external actor workflow) |

### Data Layer (15)

| Command | Description |
|---|---|
| `ListDataLayers` | List all Data Layer instances in the current level |
| `GetDataLayerInfo` | Get detailed info for a Data Layer instance — type, load filter, runtime state, visibility, and parent hierarchy |
| `CreateDataLayerAsset` | Create a new Data Layer asset in the Content Browser (requires `DataLayerEdit`) |
| `DeleteDataLayerAsset` | Delete a Data Layer asset (requires `DataLayerEdit`). Refused with `PolicyViolation` while `DisableSave` is in force |
| `CreateDataLayerInstance` | Create a new Data Layer instance in the current level from a Data Layer asset (requires `DataLayerEdit`) |
| `DeleteDataLayerInstance` | Delete a Data Layer instance from the current level (requires `DataLayerEdit`) |
| `SetDataLayerType` | Set the type of a Data Layer instance — Editor or Runtime (requires `DataLayerEdit`) |
| `SetDataLayerInitialRuntimeState` | Set the initial runtime state of a Data Layer — Unloaded, Loaded, or Activated (requires `DataLayerEdit`) |
| `SetDataLayerIsLoadedInEditor` | Set whether a Data Layer is loaded in the editor viewport (requires `DataLayerEdit`) |
| `SetDataLayerVisibility` | Set the visibility of a Data Layer in the editor (requires `DataLayerEdit`) |
| `SetParentDataLayerInstance` | Set the parent Data Layer instance, building a hierarchy (max 64 levels; requires `DataLayerEdit`). A pairing that cannot be parented is refused with the reason |
| `GetActorDataLayers` | Get the Data Layer instances assigned to an actor |
| `AddActorToDataLayer` | Add an actor to a Data Layer instance (requires `DataLayerEdit`) |
| `RemoveActorFromDataLayer` | Remove an actor from a Data Layer instance (requires `DataLayerEdit`) |
| `GetActorsInDataLayer` | List all actors assigned to a specific Data Layer instance |

### HLOD (7)

| Command | Description |
|---|---|
| `ListHLODLayers` | List all HLOD Layer assets in the project |
| `CreateHLODLayer` | Create a new HLOD Layer asset under `/Game/` (requires `HLODBuild`) |
| `DeleteHLODs` | Delete built HLOD data for a specified HLOD Layer (requires `HLODBuild`). Refused with `PolicyViolation` while `DisableSave` is in force |
| `SetActorHLODLayer` | Assign an actor to an HLOD Layer asset (requires `HLODBuild`) |
| `BuildHLODs` | Start an HLOD build job for the current world; returns `HLODBuildJobId` (requires `HLODBuild`) |
| `CancelHLODBuild` | Cancel an in-progress HLOD build job by job ID (requires `HLODBuild`) |
| `GetHLODBuildStatus` | Get the current status of an HLOD build job — running, completed, or not found |

---

## UAIP.Editor.Foliage

Foliage type management and instance placement in the editor. Observation commands run during PIE; edit commands require the editor to be stopped (not in PIE or SIE).

### Foliage Observation (4)

| Command | Description |
|---|---|
| `ListFoliageTypes` | List all foliage types registered in the current level's `AInstancedFoliageActor` with instance counts |
| `GetFoliageTypeInfo` | Get detailed settings for a foliage type — mesh path, density, scale range, cull distances, normal alignment, slope angle, and instance count |
| `GetFoliageInstanceCount` | Get the total placed instance count; optionally filtered to a single foliage type with a per-type breakdown |
| `GetFoliageInstances` | List placed instances for a foliage type within a bounding box — returns location, rotation, and scale |

### Foliage Type Management (3)

| Command | Description |
|---|---|
| `AddFoliageTypeToLevel` | Register a foliage type asset with the current level's `AInstancedFoliageActor` (requires `FoliageTypeEdit`) |
| `RemoveFoliageTypeFromLevel` | Unregister a foliage type and delete all its instances from the current level (requires `FoliageTypeEdit`) |
| `SetFoliageTypeSettings` | Update foliage type settings — density, scale range, cull distances, normal alignment, slope angle, and mesh (ISM types only) (requires `FoliageTypeEdit`) |

### Foliage Instance Control (4)

| Command | Description |
|---|---|
| `AddFoliageInstances` | Place foliage instances at the specified transforms. World Partition aware — routes each instance to the correct `AInstancedFoliageActor` cell (requires `FoliageInstanceEdit`) |
| `RemoveFoliageInstances` | Remove foliage instances inside a bounding box or sphere up to `MaxRemoveCount` (requires `FoliageInstanceEdit`) |
| `DeleteAllFoliageInstances` | Delete every placed instance of a foliage type from the current level (requires `FoliageBulkDelete`) |
| `ResimulateProceduralFoliage` 🧩 | Resimulate a `ProceduralFoliageVolume` and place the resulting instances (requires `ProceduralFoliage` plugin and `FoliageInstanceEdit`) |

---

## UAIP.Editor.DataRegistry 🧩

Editor-time observation of UE 5.8 Data Registries — listing, schema inspection, and cached item retrieval with secret-field masking. Requires the `DataRegistry` plugin (plus `DataRegistryToolset` + `ToolsetRegistry` for the bridge variants).

### Native (9)

| Command | Description |
|---|---|
| `ListRegistries` | List all registered Data Registries, optionally filtered by item struct name (`StructFilter`); includes `IsDataRegistrySystemEnabled` / `AreRegistriesInitialized` diagnostics |
| `GetRegistryInfo` | Get item count, lowest source availability, description, and ID format for a registry |
| `GetSchema` | Get the item struct's property schema — name, type, and `IsSecret` flag per property |
| `ListItems` | List registered item IDs for a registry (not necessarily cached) |
| `ListDataSources` | List editor-time defined data sources for a registry |
| `ListRuntimeSources` | List runtime-expanded data sources for a registry |
| `GetItems` | Read cached items by name with secret-field masking; items not yet cached are reported in `MissingItems` with a reason instead of being silently dropped |
| `GetAllCachedItems` | Read every currently cached item without naming items in advance (bounded to 1000 items / 1 MiB; no Toolset equivalent) |
| `AcquireItems` | Trigger an asynchronous cache load for the given items — needed for custom/Remote sources; DataTable sources precache automatically (no Toolset equivalent) |

### Toolset bridges (7) 🧩

Mirror of the first 7 native commands via the `DataRegistryToolset` plugin (UE 5.8+). Provider: `Toolset.Editor.DataRegistry.*`. `GetItems` behaves differently here: missing items are silently omitted and no secret masking is applied — use the native `GetItems` when either matters.

| Command | Description |
|---|---|
| `Toolset.Editor.DataRegistry.ListRegistries` | Passthrough to `DataRegistryToolset` |
| `Toolset.Editor.DataRegistry.GetRegistryInfo` | Passthrough to `DataRegistryToolset` |
| `Toolset.Editor.DataRegistry.GetSchema` | Passthrough to `DataRegistryToolset` (raw JSON string, no `IsSecret` flag) |
| `Toolset.Editor.DataRegistry.ListItems` | Passthrough to `DataRegistryToolset` |
| `Toolset.Editor.DataRegistry.ListDataSources` | Passthrough to `DataRegistryToolset` |
| `Toolset.Editor.DataRegistry.ListRuntimeSources` | Passthrough to `DataRegistryToolset` |
| `Toolset.Editor.DataRegistry.GetItems` | Passthrough to `DataRegistryToolset`; missing items silently omitted, no masking |

---

## UAIP.Editor.MotionMatching 🧩

Motion Matching editing for the Pose Search plugin — `UPoseSearchDatabase` animation registration, `UPoseSearchSchema` structure (roled skeletons and the feature channel tree), `UPoseSearchNormalizationSet` membership, and asynchronous index builds. Requires the `PoseSearch` plugin.

> **Note**: Every edit command in this domain reports `Success: true` once its own mutation lands, even when the schema's `Finalize()` step subsequently rolls back (e.g. no skeleton assigned yet, or a `UPoseSearchFeatureChannel_Group` left empty). Check the response's `bSchemaReadyForIndexBuild` rather than `Success` alone before assuming a schema can build an index — a schema with zero roled skeletons stays `bSchemaReadyForIndexBuild: false` no matter how many channels are added; add one with `AddSkeletonToPoseSearchSchema` first. `bSchemaReadyForIndexBuild` only guarantees this schema's own preconditions are met — an actual index build also requires a `UPoseSearchDatabase` to reference the schema (`SetPoseSearchDatabaseSchema`) and have animations registered (`AddAnimationToPoseSearchDatabase`).

### Database (6)

| Command | Description |
|---|---|
| `GetPoseSearchDatabaseInfo` | Structural info for a `UPoseSearchDatabase` — Schema/NormalizationSet references, PoseSearchMode, PCA/KDTree settings, and every `AnimationAssets` entry (path, class, enabled, mirror option, sampling range/grid). Rejects Chooser-owned databases |
| `AddAnimationToPoseSearchDatabase` (requires `PoseSearchAssetEdit`) | Add an animation asset at `InsertAt` with optional per-entry settings (enabled, mirror option, sampling range/grid). Idempotent by default for an animation already registered as a normal (non-BranchIn) entry; set `bAllowDuplicate: true` to bypass that check and always insert a new entry |
| `RemoveAnimationFromPoseSearchDatabase` (requires `PoseSearchAssetEdit`) | Remove every entry referencing an animation asset. All-or-nothing: fails if any matching entry was created by the PoseSearchBranchIn animation notify |
| `SetPoseSearchDatabaseAnimationSettings` (requires `PoseSearchAssetEdit`) | Partially update one existing `AnimationAssets` entry's settings, resolved by animation path (disambiguated by `Index` when needed). UE 5.8 only; reports `Available: false` on UE 5.7 |
| `SetPoseSearchDatabaseSchema` (requires `PoseSearchAssetEdit`) | Set a database's `Schema` reference; replacing an already-assigned one requires `bAllowOverwrite` |
| `SynchronizePoseSearchDatabase` (requires `PoseSearchAssetEdit`) | Explicitly merge every `UAnimSequenceBase`'s `PoseSearchBranchIn` notify entries (`BranchInId != 0`) into the database's `AnimationAssets`, since the engine has no reliable event to observe that merge happening on its own — call it after adding/editing a `PoseSearchBranchIn` notify and saving the animation asset, before reading `GetPoseSearchDatabaseInfo`. ⚠️ Calling it in the same request as that save can report zero merged entries: the asset registry's referencer index rebuilds asynchronously after a save, so re-issue the call once the save has settled. Idempotent — nothing new to merge leaves the database untouched. Rejects Chooser-owned databases with `NotAllowed` |

### Schema (11)

| Command | Description |
|---|---|
| `GetPoseSearchSchemaInfo` | Structural info for a `UPoseSearchSchema` — SampleRate, DataPreprocessor, SchemaCardinality, the roled `Skeletons` array, the `Finalize()`-expanded `Channels` array, and the pre-finalize `RawChannels` tree (`ChannelPath` / `ClassPath`) the editing commands below actually address. Each `RawChannels[]` entry (nested ones included) now also reports `Admission` / `RequiredCapabilities` / `MissingCapabilities`, read as they apply to editing that channel's properties — see the note below |
| `SetPoseSearchSchemaDataPreprocessor` (requires `PoseSearchAssetEdit`) | Change `DataPreprocessor` (`None` / `Normalize` / `NormalizeOnlyByDeviation` / `NormalizeWithCommonSchema`); response lists every database found to reference the schema (best-effort) |
| `AddPoseSearchSchemaChannel` (requires `PoseSearchAssetEdit`) | Create a channel of `ChannelClass` and insert it into the channel tree, optionally nested under `ParentChannelPath` at `InsertAt`. Not idempotent — calling it twice creates two channels. A class from outside `/Script/PoseSearch` additionally needs `MotionMatchingCustomTypeEdit`, see the note below |
| `RemovePoseSearchSchemaChannel` (requires `PoseSearchAssetEdit`) | Remove the channel at `ChannelPath` together with every nested descendant; optional `ExpectedChannelClass` guards against removing the wrong channel after a stale path. Needs `MotionMatchingCustomTypeEdit` when the removed channel's class, or any nested descendant's class, is one this domain does not ship |
| `MovePoseSearchSchemaChannel` (requires `PoseSearchAssetEdit`) | Reorder the channel at `SourceChannelPath` to `TargetIndex` within its own parent. Moving to a different parent is not supported — remove and re-add instead. Needs `MotionMatchingCustomTypeEdit` when the moved channel's own class is one this domain does not ship — nested descendants are not re-checked, since a reorder does not disturb them. Checked even when `TargetIndex` names the channel's current position, so a session cannot use a no-op move to probe a gated channel's position for free |
| `SetPoseSearchSchemaChannelProperty` (requires `PoseSearchAssetEdit`) | Write into a top-level property of the channel at `ChannelPath` — `Value` in UE text-import syntax (max 4 KiB), or `ValueJson` as JSON with `Operation` / `ElementIndex` / `ElementKeyJson` for a single container element (see [Writing references, structs and containers](#writing-references-structs-and-containers)). A struct or container additionally requires `PropertyStructuredEdit`. A reference-bearing type is refused with `PolicyViolation` whatever the session holds, because writing a channel's sub-channel array directly would sidestep the class allowlist `AddPoseSearchSchemaChannel` enforces — add channels with that command instead. A post-write validation failure rolls the write back. Needs `MotionMatchingCustomTypeEdit` when the channel's own class, or the class declaring the property being written, is one this domain does not ship — see the note below for why this is a new restriction |
| `AddDefaultPoseSearchSchemaChannels` (requires `PoseSearchAssetEdit`) | Add the same default trajectory + pose channel pair the editor's schema factory creates. Existing channels are kept, not replaced — calling it twice appends a duplicate pair. Never needs `MotionMatchingCustomTypeEdit`: the two channels it adds are always the engine's own, with no caller-supplied class |
| `GetAvailablePoseSearchChannelClasses` | List every `UPoseSearchFeatureChannel` subclass the structural checks alone recognise as a channel — the same set `AddPoseSearchSchemaChannel` resolves `ChannelClass` against — whether or not this session may currently place one. Each entry carries `Admission` (`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`) plus `RequiredCapabilities` / `MissingCapabilities`, and `bCanHostSubChannels` marking valid `ParentChannelPath` targets. Entries are ordered by full class path (`/Script/<Module>.<Class>`); the artifact reports `TotalCount`, `ReturnedCount`, `Truncated` (max 500). Heavy — walks every loaded `UClass`; cache the result |
| `GetPoseSearchChannelClassSchema` | List a channel class's Details-panel properties, each with a nested `WriteRequirements` object reporting `IsWritable` / `RefusalReason` for `SetPoseSearchSchemaChannelProperty`, `WriteInputForm` (`TextOrJson` / `JsonOnly` / `None`), and `RequiredCapabilities` / `HeldCapabilities` / `MissingCapabilities` naming what a structured write would need — see [Finding out what a write needs](#finding-out-what-a-write-needs) — and `DefaultValueText` as a working text-import example for each |
| `AddSkeletonToPoseSearchSchema` (requires `PoseSearchAssetEdit`) | Add or replace the roled skeleton entry for `Role`, with an optional `MirrorDataTablePath`. Replacing an existing `Role` requires `bAllowOverwrite` |
| `RemoveSkeletonFromPoseSearchSchema` (requires `PoseSearchAssetEdit`) | Remove the roled skeleton entry for `Role` from the `Skeletons` array |

> **Note**: `AddPoseSearchSchemaChannel`'s `ChannelClass` and every editing command's `ExpectedChannelClass` need the **fully qualified class path** (e.g. `/Script/PoseSearch.PoseSearchFeatureChannel_Position`) — use `GetPoseSearchSchemaInfo`'s `RawChannels[].ClassPath` or `GetAvailablePoseSearchChannelClasses`' `ClassPath`, not the shorter `ChannelClass` field reported alongside them. `ChannelPath` is a `/`-separated index path (e.g. `"0"`, `"2/0"`) into `RawChannels[]`, **not** into the `Finalize()`-expanded `Channels[]`; an edit can shift the `ChannelPath` of later siblings, so re-read `RawChannels` after each call rather than reusing paths obtained before it.
>
> **Note — this domain gates channel classes at one place, behind one capability: `MotionMatchingCustomTypeEdit`.** A channel class being placed, removed, or acted on, and the class declaring a channel property being written, are judged the same way and share the one name — a project's own channel declares its own properties, so a second permission for the property face would not make sense. Required when the class comes from outside `/Script/PoseSearch`: a project module, a plugin module, or a Blueprint generated class (a Blueprint generated channel class stays refused outright, whatever the session holds — it is not the kind of custom type this capability opens). There is no companion "dangerous type" capability for this domain: a channel class's `Finalize` / `BuildQuery` / `IndexAsset` is its own author's compiled code, never something a request supplies, and a channel property is a plain data member. Not granted by default; see [Safety & Capabilities](safety.md#motion-matching--pose-search-editing).
>
> **Writing a property already sitting in a schema now needs this capability too — this is a new restriction, not a preserved one.** Before this change, `SetPoseSearchSchemaChannelProperty` checked only the property's write flags and value kind; a project-defined channel's own properties were writable without any capability at all. It now also needs `MotionMatchingCustomTypeEdit` when the declaring class is not `/Script/PoseSearch`'s own.
>
> **Removing or moving a channel — not only adding one — is gated, and starting an index build is too.** `RemovePoseSearchSchemaChannel` and `MovePoseSearchSchemaChannel` used to reach the asset regardless of what the channel's class was; they now re-check the same capability. Removal is judged over the whole nested subtree it takes with it, since every descendant disappears along with it; a move only judges the moved channel's own class, since nothing nested is disturbed by a reorder. `StartPoseSearchDatabaseIndexBuild` is gated for the same reason: the engine's own build pipeline runs every distinct channel class the target schema holds, so starting a build is judged the same way adding one of those classes would be — every class the schema holds is checked, not only the ones a caller named when they were added.
>
> ⚠️ **Breaking change**: a channel class outside this domain's own module used to be refused with `PolicyViolation` unconditionally, and `RemovePoseSearchSchemaChannel` / `MovePoseSearchSchemaChannel` / `SetPoseSearchSchemaChannelProperty` never refused one on origin grounds at all. `AddPoseSearchSchemaChannel` / `RemovePoseSearchSchemaChannel` / `MovePoseSearchSchemaChannel` / `SetPoseSearchSchemaChannelProperty` / `StartPoseSearchDatabaseIndexBuild` now answer `CapabilityNotAvailable` and name the missing capability — and actually succeed once it is granted, which the previous implementation did not for `AddPoseSearchSchemaChannel`. A class path nothing currently loaded answers to is still `NotFound`; this domain never falls back to loading an unresolved class as a side effect.
>
> ⚠️ **Breaking change — `GetAvailablePoseSearchChannelClasses`'s response shape changed.** The `NumClasses` field (both on the artifact and on `CommandResponse.Result`) is gone; `CommandResponse.Result` is no longer set at all. Read `TotalCount` / `ReturnedCount` / `Truncated` on the artifact instead. The listing also no longer silently drops a class gated behind `MotionMatchingCustomTypeEdit` — it is now listed with `Admission: RequiresCapabilities` and the capability named, the same way `AddPoseSearchSchemaChannel` would answer about it. A new 500-entry cap applies after sorting by full class path, where none applied before.
>
> **`GetPoseSearchSchemaInfo`'s `RawChannels[]` entries now additionally report `Admission` / `RequiredCapabilities` / `MissingCapabilities`** for each channel's own class, including nested ones — the same question `SetPoseSearchSchemaChannelProperty` / `RemovePoseSearchSchemaChannel` would ask about it. Additive only; every existing field on an entry is unchanged.

### NormalizationSet (4)

| Command | Description |
|---|---|
| `GetPoseSearchNormalizationSetInfo` | List a `UPoseSearchNormalizationSet`'s `Databases` array (`Index` / `DatabasePath` / `bIsNull`) in storage order |
| `SetPoseSearchDatabaseNormalizationSet` (requires `PoseSearchAssetEdit`) | Set or clear a database's `NormalizationSet` reference (`NormalizationSetPath` and `bClearNormalizationSet` are mutually exclusive). Only edits the database side — pair with `AddDatabaseToPoseSearchNormalizationSet` if both sides need to agree |
| `AddDatabaseToPoseSearchNormalizationSet` (requires `PoseSearchAssetEdit`) | Add a database to a `UPoseSearchNormalizationSet`'s `Databases` array. Idempotent; only edits the normalization set side — pair with `SetPoseSearchDatabaseNormalizationSet` |
| `RemoveDatabaseFromPoseSearchNormalizationSet` (requires `PoseSearchAssetEdit`) | Remove every slot referencing a database. Matched slots are cleared to null rather than compacted, so every other `Index` stays stable |

### Index Build (2)

| Command | Description |
|---|---|
| `StartPoseSearchDatabaseIndexBuild` (requires `PoseSearchAssetEdit`) | Start a database index build asynchronously and return a `BuildId` to poll. Only one build runs at a time across the whole editor, whichever database it targets |
| `GetPoseSearchDatabaseIndexBuildStatus` | Poll one build's `State` (`Running` / `Succeeded` / `Failed`) and `ElapsedSeconds`; once `Succeeded`, also reports `NumPoses` / `SchemaCardinality` |

> **Note**: `StartPoseSearchDatabaseIndexBuild` and `GetPoseSearchDatabaseIndexBuildStatus` must both be called with an explicit `SessionId` — the **same** one for both. An automatically generated session differs on every call, so a build started under one could never be polled afterward; both commands reject an anonymous or omitted `SessionId` with `InvalidParams`.

---

## UAIP.Editor.Chooser 🧩

Authoring `UChooserTable` assets — rows, columns, the cell each row holds in each column, the result object a row selects, and the input binding that decides what a column looks at. Requires the **Chooser** plugin.

Addressing is positional: `ColumnIndex` and `RowIndex` are the current zero-based indices the read commands report, and an index that names nothing is refused with `InvalidParams` carrying the table's current counts. Values round-trip — what a read reports under a cell's `Value`, a row's `ResultType` / `ResultValue`, or a column's input binding is exactly what the matching write accepts, so anything read from one row, column or table can be written to another unchanged.

> **Note**: every edit command below takes an optional `Fingerprint` — the structural fingerprint the read commands report. When it no longer matches the table's current structure the edit is refused with `Conflict`, and the response carries the current value to reissue against. `CompileChooserTable` is the exception: it accepts no `Fingerprint`, since it touches no row or column. Every edit is rejected while a play session is in progress, and for an asset outside `/Game/`.
>
> Beyond `ChooserTableEdit`, an edit is judged per call against what it actually names: **`ChooserCustomTypeEdit`** when a column type, result type or input binding type comes from outside the modules this domain ships those types from (asked about the type already in the table as well as the one being written), **`ChooserReferenceEdit`** when a value is supplied for a type that can hold an object reference, and **`ChooserFunctionBindingEdit`** when a property chain resolves to a function the evaluation path would call rather than to plain properties. A chain reaching a function through a binding the chooser editor offers no functions for is refused with `NotAllowed` instead, which no capability lifts. The `Admission` field on the listing commands below reports, per type, which of these a call naming it would need.

| Command | Description |
|---|---|
| `GetChooserTableInfo` | The table-wide summary: row and column counts, the output kind and the class constraining it, the context parameter count, whether a fallback result is assigned and what it holds, and the structural fingerprint. Structural only — no row, column or cell value is reported here. Read-only, requires `EditorInspect` |
| `GetChooserTableRow` | One row: its result object, its disabled flag, and one cell entry per column, alongside the table's current counts and fingerprint. A cell whose column keeps no per-row data, or cannot round-trip as a plain value, is reported with a null `Value` and `bCellValueUnavailable` set rather than omitted. Read-only, requires `EditorInspect` |
| `ListChooserTableRows` | One page of rows — each row's result object, disabled flag and one cell per column — as a JSON artifact. `StartIndex` / `Count` page through the table; an out-of-range `StartIndex` yields an empty or shortened page rather than an error, so a caller can walk pages until an empty one signals the end. Read-only, requires `EditorInspect` |
| `ListChooserColumns` | Every column as a JSON artifact — its index, its own type, the input binding deciding what it looks at, whether it is disabled, and whether its cells round-trip as plain values — plus the table's counts and fingerprint. The `ColumnIndex` reported here is the one every column-targeting edit expects. Read-only, requires `EditorInspect` |
| `ListChooserContextData` | Every context parameter the table's evaluation context declares — the candidates a column's input binding can be pointed at — each with its index, the type it exposes, and whether it is read from, written to, or both. A nested table resolves this from the root of the chooser chain. Read-only, requires `EditorInspect` |
| `ListChooserColumnTypes` | Every `FChooserColumnBase`-derived struct currently discovered — the same set the Chooser editor's own Add Column menu offers. Pass a `ClassPath` from the result as `ColumnType` to `AddChooserColumn`. Each entry carries `Admission` (`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`) plus `RequiredCapabilities` / `MissingCapabilities`, and `TotalCount` / `ReturnedCount` / `Truncated` report whether the result cap cut anything off. Ordered by `ClassPath`, so a truncated result always carries the same leading types. `AssetPath` is optional and never narrows the listing, but is still resolved and refused with `NotFound` when it names no real chooser table. Read-only, requires `EditorInspect` |
| `ListChooserResultTypes` | Every `FObjectChooserBase`-derived struct `AddChooserTableRow` / `SetChooserTableResult` / `SetChooserFallbackResult` accept as a `ResultType`, whether or not this session may currently use one. `AssetPath` is accepted but never resolved — the result type family is the same for every table. Same `Admission` / count / ordering contract as `ListChooserColumnTypes`. Read-only, requires `EditorInspect` |
| `ListChooserInputTypes` | Every input binding type the column named by `ColumnIndex` may be bound to — the same candidates the editor's own binding widget offers. Pass a `ClassPath` from the result to `SetChooserColumnInput`. Unlike the two listings above the candidates depend entirely on which column is named, so both `AssetPath` and `ColumnIndex` are required. A column presenting no primary input — one an author cannot bind from the editor either — is described with an empty listing rather than refused. Same `Admission` / count / ordering contract. Read-only, requires `EditorInspect` |
| `AddChooserColumn` (requires `ChooserTableEdit`) | Add one column of the named type and report the index it ended up at, the counts afterwards, and the new fingerprint. The new column is given one cell per existing row, so the table keeps answering for every row it already had. `ColumnType` must be one of the types `ListChooserColumnTypes` reports; `InsertAt` places the column, and omitting it appends |
| `RemoveChooserColumn` (requires `ChooserTableEdit`) | Remove one column together with the cells it owns. No other column is affected, since each column owns its own cells |
| `MoveChooserColumn` (requires `ChooserTableEdit`) | Move one column so that it ends up at `ToIndex`, taking every cell it owns with it. `ToIndex` is the position the column occupies **after** the move, not before; moving a column onto its own current index is a successful no-op |
| `SetChooserColumnInput` (requires `ChooserTableEdit`) | Install a column's input binding — the parameter deciding what the column looks at. `InputType` / `InputValue` take exactly what `ListChooserColumns` reported for a column; a null `InputValue` writes the named type's own defaults, which is the unbound binding a column is given when its parameter type is picked in the editor. `InputType` has to name one of the types `ListChooserInputTypes` reports for *this* column — a type of a family the column cannot read a value as is refused with `InvalidParams`, as is every type for a column that presents no input binding at all |
| `AddChooserTableRow` (requires `ChooserTableEdit`) | Add one row and report the index it ended up at. `InsertAt` places the row, and omitting it appends. `ResultType` / `ResultValue` give the new row its result object in the same shape the read commands report one, so a row read from one table can be added to another; omitting both adds a row whose result is empty |
| `RemoveChooserTableRows` (requires `ChooserTableEdit`) | Remove one or more rows as a single change. `RowIndices` names every row by its current index; order does not matter, but every entry has to be distinct and in range or the whole request is refused. Removing several rows is one change, so a single Undo restores all of them |
| `MoveChooserTableRow` (requires `ChooserTableEdit`) | Move one row so that it ends up at `ToIndex`, taking its result, its disabled flag and its cell in every column with it. Same after-the-move `ToIndex` semantics as `MoveChooserColumn` |
| `SetChooserTableCell` (requires `ChooserTableEdit`) | Write one cell — the value one row holds in one column. A column that keeps no per-row data, or whose cell cannot round-trip as a plain value (the columns a read reports with `bCellValueUnavailable` set), is refused rather than written |
| `SetChooserTableResult` (requires `ChooserTableEdit`) | Replace the result object one row selects. Omitting `ResultType`, or passing it empty, empties the row's result instead of rebuilding it — the state the editor's own result picker puts a row back into — in which case `ResultValue` has to be omitted or null. A nested chooser the row used to hold is unregistered from the table before the new result is written, and one being written is registered afterwards, so ownership follows the replacement |
| `SetChooserFallbackResult` (requires `ChooserTableEdit`) | Replace the result the table produces when no row matched — the Fallback Result in the editor. The fallback belongs to the table rather than to a row, so this command takes no index. Same empty-by-omitting-`ResultType` and nested-chooser ownership rules as `SetChooserTableResult` |
| `SetChooserRowDisabled` (requires `ChooserTableEdit`) | Take one row out of evaluation or put it back in, without moving it, changing its result, or touching any of its cells. The fingerprint does not change either, since a row's disabled flag is not one of the things it describes. Requires `ChooserTableEdit` and no other capability, since this command names no column, result or input binding type |
| `CompileChooserTable` (requires `ChooserTableEdit`) | Compile the table explicitly. Compiling is not forced when the asset is saved, so an edit made through the other commands here can leave a column's input binding resolved against a stale offset until something asks for a recompile — which is what this command is for. No column, result or binding type already in the table is re-judged for where it came from; only every input binding the table already holds is put through the same binding chain resolver every write in this domain uses, which is why it additionally requires `ChooserFunctionBindingEdit` when one of them resolves to a function the evaluation path would call |

---

## UAIP.Editor.AnimSequence

Add, remove, and edit AnimNotify / AnimNotifyState entries and notify tracks on `UAnimSequence` / `UAnimMontage` / `UAnimComposite` assets. Built entirely on engine-shipped types — no optional plugin required.

> **Note**: `NotifyGuid` is 32 hex digits with no hyphens (`FGuid::ToString(EGuidFormats::Digits)`) — the form `GetAnimNotifyInfo` reports and every other command in this domain expects back. `SetAnimNotifyProperty` requires `AnimNotifyEdit` for every write, additionally requires `AnimNotifyReferenceEdit` when the property being written is — or contains — a reference (`GetAnimNotifyClassSchema` reports this per property as `bIsObjectReference`), and additionally requires `PropertyStructuredEdit` when it is a struct outside the value catalogue, an array, a set, a map or an optional. `GetAnimNotifyClassSchema` names both per property under `WriteRequirements.RequiredCapabilities` and says which input field the value belongs in under `WriteRequirements.WriteInputForm`; `GetAnimNotifyProperty` reports the same thing in the same shape, resolved against the notify instance itself. `GetAnimNotifyProperty` is the read-only counterpart — same `NotifyGuid` / `PropertyName` addressing and the same text format as `SetAnimNotifyProperty`'s `Value` and `GetAnimNotifyClassSchema`'s `DefaultValueText`, so all three round-trip byte-for-byte, including a zero-valued property ("0" / "False" / "None" rather than an empty string). Every edit command in this domain is rejected while PIE or SIE is active.

| Command | Description |
|---|---|
| `GetAnimNotifyInfo` | Every notify track (`TrackIndex` / `TrackName` / `TrackColor`) and every notify / notify state entry (guid, class, timing, montage-specific fields) on the asset, plus asset-level scalars (`AssetKind` / `PlayLength` / `NumTracks` / `NumNotifies` / `NumInvalidGuids`). For a `UAnimComposite` this only covers the asset's own `Notifies` array, not the notifies carried by its segments' `AnimSequence`s. Read-only, requires `EditorInspect` |
| `GetAvailableAnimNotifyClasses` | List every `UAnimNotify` / `UAnimNotifyState` subclass `AddAnimNotify` / `AddAnimNotifyState` would accept as `ClassPath`, with `bIsNotifyState` / `bCanBePlaced` / `NotPlaceableReason`. Only currently loaded classes are visible. Heavy — walks every loaded `UClass`; cache the result. Read-only, requires `EditorInspect` |
| `GetAnimNotifyClassSchema` | List the Details-panel properties of a `UAnimNotify` / `UAnimNotifyState` subclass, each with a nested `WriteRequirements` object reporting `IsWritable` / `RefusalReason` for `SetAnimNotifyProperty`, `WriteInputForm` (`TextOrJson` / `JsonOnly` / `None`), and `RequiredCapabilities` / `HeldCapabilities` / `MissingCapabilities` — see [Finding out what a write needs](#finding-out-what-a-write-needs) — plus `bIsObjectReference` and `DefaultValueText` as a working text-import example. Read-only, requires `EditorInspect` |
| `GetAnimNotifyProperty` | Read one property (`PropertyName`) or, when it is omitted or empty, every property `GetAnimNotifyClassSchema` would enumerate for the notify instance identified by `NotifyGuid`. All-properties reads report `NumProperties` / `bTruncated` in place of `PropertyName` / `Value` and truncate on overflow; a single-property read instead fails with `InvalidParams` rather than being cut short. Secret-looking values are masked the same way `GetAnimNotifyClassSchema`'s `DefaultValueText` and `SetAnimNotifyProperty`'s `AppliedValue` are. Each property also carries a nested `WriteRequirements` object — same field names and same nesting as `GetAnimNotifyClassSchema`, resolved against the notify instance rather than the class default — reporting `IsWritable` / `RefusalReason`, `WriteInputForm` (`TextOrJson` / `JsonOnly` / `None`) and `RequiredCapabilities` / `HeldCapabilities` / `MissingCapabilities`; on a single-property read it sits directly in `Data`. See [Finding out what a write needs](#finding-out-what-a-write-needs). Never mutates the asset. Read-only and Idempotent, requires `EditorInspect` |
| `AddAnimNotifyTrack` (requires `AnimNotifyEdit`) | Ensure a notify track named `TrackName` exists, creating it (optional `TrackColor`, default white) when it does not. Idempotent-on-existence — an existing track's `TrackIndex` is returned as-is and `TrackColor` is ignored. Rejected while PIE/SIE is active |
| `RemoveAnimNotifyTrack` (requires `AnimNotifyEdit`) | Remove the notify track named `TrackName`, deleting every notify placed on it and shifting later tracks' indices down by one; the response's `RemovedNotifyGuids` / `ReindexedNotifies` report the full blast radius. Fails with `NotFound` on an already-removed track. Rejected while PIE/SIE is active |
| `AddAnimNotify` (requires `AnimNotifyEdit`) | Add a single point notify to `TrackName` at `StartTime`. Exactly one of `ClassPath` (a `UAnimNotify` subclass) / `NotifyName` (class-less, optionally registered on the Skeleton via `bRegisterOnSkeleton`) is required. Not idempotent — repeated calls create independent notifies with new `NotifyGuid`s. Rejected while PIE/SIE is active |
| `AddAnimNotifyState` (requires `AnimNotifyEdit`) | Add a single notify state spanning `[StartTime, StartTime + Duration]` to `TrackName`; `ClassPath` must resolve to a `UAnimNotifyState` subclass. Not idempotent — repeated calls create independent notify states with new `NotifyGuid`s. Rejected while PIE/SIE is active |
| `RemoveAnimNotify` (requires `AnimNotifyEdit`) | Remove exactly one notify identified by `NotifyGuid`. Optional `ExpectedNotifyClassPath` / `ExpectedNotifyName` is an optimistic-concurrency guard. Fails with `NotFound` rather than a no-op success once the guid no longer resolves. Rejected with `NotAllowed` while PIE/SIE is active |
| `SetAnimNotifyEvent` (requires `AnimNotifyEdit`) | Partially update one notify's event fields (`StartTime` / `Duration` / `TrackName` / `NotifyName` / `MontageTickType` / trigger and filter settings) identified by `NotifyGuid` — only the supplied fields change. `Duration` is rejected on a point notify; `MontageTickType` is rejected outside `UAnimMontage`. Rejected with `NotAllowed` while PIE/SIE is active |
| `SetAnimNotifyProperty` (requires `AnimNotifyEdit`; hard object/class reference writes additionally require `AnimNotifyReferenceEdit`) | Write one top-level property on the notify instance identified by `NotifyGuid`, in the same text-import format `GetAnimNotifyClassSchema` reports as `DefaultValueText`. Also writable now: `FGameplayTag` / `FGameplayTagContainer` / `FGameplayCueTag` (rejected as `InvalidParams` for an unregistered tag, a tag outside a `Categories` / `GameplayTagFilter` scope, or a duplicate tag inside a container) and `FBoneReference` (rejected as `InvalidParams` for a bone the target skeleton does not have, or when no skeleton can be resolved to validate against). Soft / weak / lazy references, maps, sets, optionals and other structs or arrays — reference-containing ones included — are written through `ValueJson`, with a single container element addressed by `Operation` / `ElementIndex` / `ElementKeyJson` (see [Writing references, structs and containers](#writing-references-structs-and-containers)); a hard reference names an **already-loaded** asset, since a write never loads one as a side effect. Rejected with `NotAllowed` while PIE/SIE is active |
| `FixupAnimNotifyGuids` (requires `AnimNotifyEdit`) | Assign a fresh guid to every notify whose guid is currently invalid; legacy notifies otherwise get an unstable guid on every reload until this is run and the asset is saved. Idempotent — nothing to repair succeeds with `NumFixed: 0`. Rejected while PIE/SIE is active |
| `SelectAnimNotify` (requires `EditorUIAutomation`) | Select the notify identified by `NotifyGuid` inside the animation asset editor already open for it, so its properties appear in that editor's Details panel — simulating the click a human would make on the notify's timeline widget, since the engine exposes no API for it. Never modifies the asset. UE 5.8+ only: on UE 5.7 the notify widget type and its node-object interface are private to the Persona module, so rather than picking an arbitrary notify the command reports `Available: false` with `UnavailableDetail: "EngineVersion"` — see [UnavailableDetail](#unavailabledetail--the-eight-reasons-behind-a-handlerunavailable-refusal). Idempotent |

---

## UAIP.Editor.ChaosDestruction

Geometry Collection (Chaos Destruction) editing — inspect structure, hierarchy, and damage settings; create and merge `UGeometryCollection` assets; fracture them (Uniform / Voronoi / Plane / Slice / Brick / Mesh / Mesh Array); edit the bone cluster hierarchy; clean up and edit geometry attributes; and configure the damage model and clustering settings. Mirrors the tools available in Fracture Editor Mode. No Toolset bridge exists for this domain.

Three DefaultDenied capabilities gate the write commands — `GeometryCollectionCreate` (2 commands), `GeometryCollectionFracture` (12 commands), and `GeometryCollectionEdit` (11 commands); see [Safety & Capabilities](safety.md). 20 of the 29 commands (marked 🧩) additionally require the `Fracture` plugin, and one (marked 🧩) requires the `GeometryCollectionPlugin`; commands without either mark have no plugin dependency. Every write command is rejected while PIE or SIE is active, and — except the settings and merge commands, which use `bAllowOverwrite` — is rejected when the target asset references a Dataflow graph unless `AllowOverwrite` is set.

#### Observation (4) — requires `EditorInspect`

| Command | Description |
|---|---|
| `GetGeometryCollectionInfo` | Structural summary — `TransformCount`, `GeometryCount`, `HierarchyDepth`, `MaterialCount`, the Dataflow graph asset path, whether the asset has unsaved changes, and a destruction-settings summary |
| `GetGeometryCollectionClusterInfo` | Bone-level hierarchy as an array of entries (`BoneIndex`, `Parent`, `Children`, `SimulationType`, `BoneName`, `Level`, `BoundingBox`), capped at 256 entries with `bTruncated` |
| `GetGeometryCollectionDestructionSettings` | Full damage-model and clustering configuration — `DamageModel`, the per-level `DamageThreshold` array, `SizeSpecificData`, and clustering settings |
| `SelectGeometryCollectionBones` 🧩 | Run one bone selection query (`Root` / `Parent` / `Children` / `Siblings` / `Level` / `Contact` / `Leaf` / `Cluster` / `BySize` / `ByVolume` / `ByPercentage`) and return the resulting bone index array, ready to feed into other commands' `BoneIndices` parameter. Requires the `Fracture` plugin even though it is read-only |

#### Creation (2) — requires `GeometryCollectionCreate`

| Command | Description |
|---|---|
| `CreateGeometryCollectionFromStaticMesh` 🧩 | Create a new `UGeometryCollection` asset by converting a `UStaticMesh`. Applies the project's Fracture Mode default settings when the `ChaosEditor` plugin is available. Rejects an output path that already resolves to an existing asset. Requires the `GeometryCollectionPlugin`; leaves the new asset unsaved |
| `MergeGeometryCollectionAssets` | Append one Geometry Collection's geometry into another (`UGeometryCollection::AppendGeometry`) without losing existing data on either asset; the two assets must be different. Leaves the target asset unsaved |

#### Fracture (7) — requires `GeometryCollectionFracture`, all 🧩

Each command fractures the selected bones (or every bone under the root, when `BoneIndices` is omitted), replacing each cut bone with its fractured pieces.

| Command | Description |
|---|---|
| `FractureGeometryCollectionUniform` 🧩 | Fracture using a Voronoi diagram where every selected bone shares one random site placement. Mirrors Fracture Editor Mode's Uniform tool |
| `FractureGeometryCollectionVoronoi` 🧩 | Fracture using caller-supplied Voronoi sites, shared by every selected bone |
| `FractureGeometryCollectionPlane` 🧩 | Fracture against one or more cutting planes — explicit (`CutPlaneTransforms`) and/or randomly-placed (`NumPlanes`), additive |
| `FractureGeometryCollectionSlice` 🧩 | Fracture with an axis-aligned grid of slicing planes (`SlicesX` × `SlicesY` × `SlicesZ`). Mirrors the Slice tool |
| `FractureGeometryCollectionBrick` 🧩 | Fracture with a brick-patterned grid of cutting cells. Mirrors the Brick tool |
| `FractureGeometryCollectionWithMesh` 🧩 | Fracture by cutting against one `UStaticMesh`, once per `CutterMeshTransforms` entry. Mirrors the Mesh Cut tool |
| `FractureGeometryCollectionWithMeshArray` 🧩 | Fracture by cutting against one or more `UStaticMesh` assets, extending `FractureGeometryCollectionWithMesh` to more than one cutting mesh |

#### Cluster hierarchy (4) — requires `GeometryCollectionEdit`

These only re-parent, rename, or group bones — geometry and topology are unchanged.

| Command | Description |
|---|---|
| `ClusterGeometryCollectionBones` | Re-parent the selected bones under a new cluster node (`NewNodeAtIndex` / `NewNodeWithParent` / `AllBonesUnderNewRoot`) |
| `AutoClusterGeometryCollection` 🧩 | Automatically group the selected bones into new cluster nodes (`AutoCluster` / `ConvexityBasedCluster` / `ClusterMagnet`). Requires the `Fracture` plugin |
| `UnclusterGeometryCollectionBones` | Remove intermediate cluster nodes or move bones toward the root (5 modes: `MoveUpOneHierarchyLevel` / `CollapseHierarchyOneLevel` / `CollapseLevelHierarchy` / `RemoveDanglingClusters` / `RemoveClustersOfOnlyOneChild`); never deletes a bone that carries geometry |
| `RenameGeometryCollectionBone` | Rename a single bone; optionally cascades the new name to every descendant (`UpdateChildren`, default true) |

#### Geometry editing & clean-up (11)

| Command | Description |
|---|---|
| `MergeGeometryCollectionBones` 🧩 | Merge at least two selected bones — geometrically into one surviving bone (`MergeAllSelectedBones`) or by re-parenting under a shared cluster without touching geometry (`MergeSelectedClusters`). Requires `GeometryCollectionFracture` and the `Fracture` plugin |
| `DeleteGeometryCollectionBranch` 🧩 | Delete the selected bones and every descendant. Mirrors the Prune tool; a selected bone that is itself the collection's root is never deleted. Requires `GeometryCollectionFracture` and the `Fracture` plugin |
| `FixGeometryCollectionTinyGeometry` 🧩 | Merge geometry (`MergeGeometry`) or clusters (`MergeClusters`) below a size threshold into a neighboring bone. Mirrors the Geometry Merge tool. `NeighborSelection` value `LargestContactArea` requires UE 5.8+. Requires `GeometryCollectionFracture` and the `Fracture` plugin |
| `SplitGeometryCollectionIslands` 🧩 | Split the selected bones into their disconnected components. Mirrors the Split Islands tool; finding nothing to split is a successful no-op. Requires `GeometryCollectionFracture` and the `Fracture` plugin |
| `ValidateGeometryCollection` 🧩 | Clean up unreferenced geometry, single-child clusters, and/or dangling clusters across the entire collection (at least one flag required); finding nothing to clean up is a successful no-op. Requires `GeometryCollectionFracture` and the `Fracture` plugin |
| `SetGeometryCollectionBoneVisibility` 🧩 | Toggle the `Visible` flag of faces, by bone selection (`SelectionMode: Transform`) or explicit face selection (`SelectionMode: Face`). Requires `GeometryCollectionEdit` and the `Fracture` plugin |
| `SetGeometryCollectionBoneMaterial` 🧩 | Assign a `MaterialID` to the internal / external / all faces (`TargetFaces`) of a bone selection — useful for pointing newly-exposed fracture faces at a dedicated interior material. Requires `GeometryCollectionEdit` and the `Fracture` plugin |
| `RecomputeGeometryCollectionNormals` 🧩 | Recompute normals (and, unless `OnlyTangents` is set, tangents) of a bone selection — safe to run after any operation that leaves them stale. Requires `GeometryCollectionEdit` and the `Fracture` plugin |
| `SimplifyGeometryCollectionConvexHulls` 🧩 | Reduce the triangle count of convex collision hulls (`MeshQSlim` or `AngleTolerance`); fails with `ExecutionFailed` when the collection has no convex hull data. Requires `GeometryCollectionEdit` and the `Fracture` plugin |
| `GenerateGeometryCollectionExplodedView` 🧩 | Write the exploded-view display attribute driven by the Fracture Mode viewport's "View Exploded Amount" slider. Display-only. Requires `GeometryCollectionEdit` and the `Fracture` plugin |
| `SetGeometryCollectionBoneColors` 🧩 | Assign the bone-coloring display attribute using one of seven algorithms (`ByParent` / `ByLevel` / `ByCluster` / `ByLeafLevel` / `ByLeaf` / `ByAttr` / `Random`); optionally transfers the result onto vertex colors. Display-only. Requires `GeometryCollectionEdit` and the `Fracture` plugin |

#### Settings (1) — requires `GeometryCollectionEdit`

| Command | Description |
|---|---|
| `SetGeometryCollectionDestructionSettings` | Atomically replace the damage-model and clustering configuration — `DamageModel`, the per-level `DamageThreshold` array, `SizeSpecificData`, and clustering settings. No partial-update mode; read the current settings with `GetGeometryCollectionDestructionSettings` first |

---

## UAIP.Editor.Subsonic 🧩

Structural editing of `USubsonicEventCollection` assets for the Subsonic audio event system — events, their action sequences, per-action modifiers, Collection/Event-scoped parameters, and property-to-parameter bindings — plus auditioning an event without leaving the editor. Requires UE 5.8+ and the `Subsonic` plugin (Experimental); the whole domain is unavailable on UE 5.7 or with the plugin disabled. No Toolset bridge exists for this domain.

> **Note**: Every index-based write on an action or modifier (`RemoveSubsonicEventAction`, `MoveSubsonicEventAction`, `SetSubsonicEventActionProperty`, `AddSubsonicActionModifier`, `RemoveSubsonicActionModifier`, `MoveSubsonicActionModifier`, `SetSubsonicActionModifierProperty`, and inserting `AddSubsonicEventAction` at an explicit `InsertIndex`) requires an `ExpectedActionFingerprint` (and, for the `Move*` commands and insert-at-index calls, `ExpectedActionsFingerprint`) matching what the caller last observed. This is optimistic concurrency, not a permission check — index-based addressing is otherwise unsafe against a concurrent edit silently corrupting the wrong action. Re-read the collection, or use the `ActionsFingerprint` / `Actions[]` a prior write already returned, to get a current value after a rejection.
>
> `AuditionSubsonicEvent`'s response field is `EventDispatched`, not "played": it is `true` once the event resolved, was public, and had `Execute()` called on its actions — it does not guarantee anything was actually audible. `StopSubsonicAudition` only releases sound owned by that executor's own scope; it does **not** stop anything started in the `Global` execution scope. Before dispatching, audition statically walks the event's reachable `FGameplayTag` references and refuses with `ExecutionFailed` (`CyclePath` in the response) if they cycle or exceed the chain-depth / reachable-action-count limits — a project-defined action type that assembles a tag at runtime is invisible to this check.
>
> Property-to-parameter bindings (`AddSubsonicPropertyBinding`) have no `ParameterScope` argument: the target `ParameterName` is resolved by name alone, and an event-scoped parameter shadows a collection-scoped parameter of the same name.

#### Observation (4) — requires `EditorInspect`

| Command | Description |
|---|---|
| `ListSubsonicEventCollections` | List `USubsonicEventCollection` assets via the AssetRegistry, sorted by `AssetPath`. Each entry has `AssetPath` only — use `GetSubsonicEventCollectionInfo` for details. Paged with `PageIndex` / `PageSize`; `PathFilter` narrows by content-browser path prefix |
| `GetSubsonicEventCollectionInfo` | Full event/action/modifier/parameter/binding breakdown of one collection. `EventTagFilter` narrows by an `EventTag` prefix match. Bounded by `MaxEvents` / `MaxTotalItems` / `MaxResponseBytes` / `MaxContainerElements` / `MaxRecursionDepth` (may be lowered but never raised past their hard limits). The response body is saved as an artifact; `Data` only carries a summary. Legal to call while PIE is running |
| `ListSubsonicActionTypes` | List every discoverable Subsonic action struct type (non-`Abstract` / non-`Hidden` / non-`Deprecated`), with the property schema `SetSubsonicEventActionProperty` would accept for each. Takes no required input. Bounded by `MaxTotalItems` / `MaxResponseBytes` |
| `ListSubsonicModifierTypes` | List every discoverable derived type of the nested instanced-struct array named by `ActionStructPath` / `PropertyName`, with the property schema `SetSubsonicActionModifierProperty` would accept for each. The base type is resolved from the property's `BaseStruct` metadata, so this works for any `TArray<TInstancedStruct<...>>` property |

#### Event & Action editing (7) — requires `SubsonicEventEdit`

| Command | Description |
|---|---|
| `AddSubsonicEvent` | Add an event tagged `EventTag`. Idempotent — an already-existing tag reports `AlreadyExisted: true` and mutates nothing. `EventTag` must be a registered GameplayTag. Rejected while a play session is in progress |
| `RemoveSubsonicEvent` | Remove the event tagged `EventTag`, along with every action, event-scoped parameter, and property binding it owns; reports how many of each were removed. Fails with `NotFound` when no event carries `EventTag`. `AffectedEvents` is always empty — removing an event only deletes state scoped to that event. Rejected while a play session is in progress |
| `SetSubsonicEventSettings` | Update settings on the event tagged `EventTag`. Currently the only settable field is `IsPublic`. At least one setting must be specified — a request that changes nothing is rejected with `InvalidParams` rather than silently doing nothing. Rejected while a play session is in progress |
| `AddSubsonicEventAction` | Instantiate `ActionStructPath` and insert it into `EventTag`'s action sequence at `InsertIndex`, or append when omitted. `ExpectedActionsFingerprint` is required only when `InsertIndex` is set. Returns the updated `ActionsFingerprint` and a bounded `Actions[]` list. Rejected while a play session is in progress |
| `RemoveSubsonicEventAction` | Remove the action at `Index` (together with its property bindings) from `EventTag`'s action sequence. `ExpectedActionFingerprint` is always required. Returns the updated `ActionsFingerprint` and `Actions[]`. Rejected while a play session is in progress |
| `MoveSubsonicEventAction` | Relocate the action at `FromIndex` so it ends up at `ToIndex` (the position in the resulting array with the moved element already taken out). `FromIndex == ToIndex` succeeds as a no-op. `ExpectedActionFingerprint` and `ExpectedActionsFingerprint` are both always required. Rejected while a play session is in progress |
| `SetSubsonicEventActionProperty` | Write `Value` into the top-level `PropertyName` property of the action at `Index`. `Value` is already a JSON value and carries structured values directly, so this command has no `ValueJson`; `Operation` / `ElementIndex` / `ElementKeyJson` address a single container element (see [Writing references, structs and containers](#writing-references-structs-and-containers)). A struct or container additionally requires `PropertyStructuredEdit`. A reference names an **already-loaded** asset — this command no longer loads the target implicitly, so a write that used to succeed may now need the asset opened first. A nested `TArray<TInstancedStruct<...>>` (`Modifiers`) property is rejected — use the dedicated `AddSubsonicActionModifier` / `RemoveSubsonicActionModifier` / `MoveSubsonicActionModifier` / `SetSubsonicActionModifierProperty` commands instead. `ExpectedActionFingerprint` is always required. Rejected while a play session is in progress |

#### Action Modifier editing (4) — requires `SubsonicEventEdit`

| Command | Description |
|---|---|
| `AddSubsonicActionModifier` | Instantiate `ModifierStructPath` and insert it into the `ModifiersPropertyName` array of the action at `Index`, at `InsertIndex` or appended. Not idempotent — repeated calls with the same arguments add multiple modifiers. Always requires `ExpectedActionFingerprint`, because a modifier array is part of its owning action's fingerprint. Rejected while a play session is in progress |
| `RemoveSubsonicActionModifier` | Remove the modifier at `ModifierIndex` from the `ModifiersPropertyName` array of the action at `Index`. Always requires `ExpectedActionFingerprint`. Rejected while a play session is in progress |
| `MoveSubsonicActionModifier` | Relocate the modifier at `ModifierFromIndex` so it ends up at `ModifierToIndex`, within the `ModifiersPropertyName` array of the action at `Index`. Equal indices succeed as a no-op that opens no transaction. Always requires `ExpectedActionFingerprint`. Rejected while a play session is in progress |
| `SetSubsonicActionModifierProperty` | Write `Value` into the top-level `PropertyName` property of the modifier at `ModifierIndex`. `Value` is already a JSON value and there is no `ValueJson`; `Operation` / `ElementIndex` / `ElementKeyJson` address a single container element (see [Writing references, structs and containers](#writing-references-structs-and-containers)). A struct or container additionally requires `PropertyStructuredEdit`, and a reference names an **already-loaded** asset — the target is no longer loaded implicitly. Always requires `ExpectedActionFingerprint`. Rejected while a play session is in progress |

#### Parameter editing (3) — requires `SubsonicEventEdit`

| Command | Description |
|---|---|
| `AddSubsonicParameter` | Add a parameter named `ParameterName` to the `FInstancedPropertyBag` selected by `Scope` (`Collection` or `Event`; `EventTag` required for `Event`). `ParameterType` is an `EPropertyBagPropertyType` enumerator name (`Bool` / `Int32` / `Int64` / `Float` / `Double` / `Name` / `String` / `Enum` / `Object` / `Struct`); `ValueTypePath` is required for `Enum` / `Object` / `Struct` and must be omitted for every other type — a struct `ValueTypePath` is additionally limited to `FGameplayTag`, the only currently writable struct type. Re-adding an existing parameter name is rejected rather than overwritten, so an existing binding's type can never change silently. Rejected while a play session is in progress |
| `RemoveSubsonicParameter` | Remove the parameter named `ParameterName` from the selected `Scope`'s bag. `UnboundPropertyCount` / `ReboundPropertyCount` classify what happened to every action property that was bound to it — rebound properties kept resolving because a same-named, type-compatible collection-level parameter took over (only possible for `Scope: "Event"`). Fails with `NotFound` when no parameter named `ParameterName` exists in the selected scope. Rejected while a play session is in progress |
| `SetSubsonicParameterValue` | Set the default value of the existing parameter named `ParameterName` in the selected `Scope`'s bag. `Value` is validated through the same allowlist the action-property setters use, including NaN/Inf rejection for `Float` / `Double`. `Value` is already a JSON value and there is no `ValueJson`; `Operation` / `ElementIndex` / `ElementKeyJson` address a single container element (see [Writing references, structs and containers](#writing-references-structs-and-containers)). A struct or container additionally requires `PropertyStructuredEdit`, and a reference names an **already-loaded** asset — the target is no longer loaded implicitly. Fails with `NotFound` when no parameter named `ParameterName` exists in the selected scope. Rejected while a play session is in progress |

#### Property Binding editing (2) — requires `SubsonicEventEdit`

| Command | Description |
|---|---|
| `AddSubsonicPropertyBinding` | Bind the action property named `PropertyName` on the action at `Index` of event `EventTag` to the parameter named `ParameterName`, replacing any previous binding of that property. Rejected when the property carries the `NoBinding` metadata, is outside the value allowlist, or is not type-compatible with the parameter. `ExpectedActionFingerprint` is always required. Rejected while a play session is in progress |
| `RemoveSubsonicPropertyBinding` | Remove the binding of the action property named `PropertyName` on the action at `Index` of event `EventTag`. A property that is not currently bound is reported as `NotFound` rather than succeeding as a no-op. `ExpectedActionFingerprint` is always required. Rejected while a play session is in progress |

#### Audition (2) — requires `SubsonicEventAudition`

| Command | Description |
|---|---|
| `AuditionSubsonicEvent` | Audition the event tagged `EventTag` in a `USubsonicEventCollection` asset. Replaces this session's previously held audition, if any. See the note above for what `EventDispatched` means and how the reachability-cycle check works. Rejected while a play session is in progress |
| `StopSubsonicAudition` | Stop whatever this session is currently auditioning, by unregistering and releasing its held executor. Takes no input — the session to stop is always the request's own `SessionId`. Idempotent: a session holding no audition still succeeds, with `AuditionWasActive: false` instead of the command failing. Does **not** stop sound started in the `Global` execution scope — only sources owned by the executor's own scope are cleared |

---

## UAIP.Editor.GroomAsset 🧩

Structural editing of `UGroomAsset` (Strand-Based Hair) assets — group/LOD/simulation/interpolation/rendering settings, Cards/Meshes source configuration and derived-data builds, guide/strand curve control points, Dataflow graph assignment and evaluation, follicle-mask/strands texture generation, binding creation to a target mesh, reimport, and RBF deformation baking. Requires the `HairStrands` plugin (Optional, disabled by default); the whole domain is unavailable when the plugin is disabled. No Toolset bridge exists for this domain — the engine ships no Groom-domain Toolset.

Four DefaultDenied capabilities gate the write commands — `GroomAssetEdit` (12 commands), `GroomAssetCreate` (3 commands), `GroomCurveEdit` (4 commands), and `GroomBindingEdit` (3 commands); see [Safety & Capabilities](safety.md). Every write command is rejected while PIE or SIE is active. Most write commands leave the target asset unsaved (its own description says so); persist with `UAIP.Editor.Workspace.SaveAllPackages`. The four commands that create a brand-new asset (`GenerateGroomFollicleMaskTexture`, `GenerateGroomStrandsTextures`, `CreateGroomBinding`, `CreateGeometryCacheGroomBinding`, `BakeGroomRBFDeformation`) save it before responding instead.

#### Observation (13) — requires `EditorInspect`

| Command | Description |
|---|---|
| `GetGroomAssetInfo` | Group count, per-group `FHairGroupInfo` fields (curve/guide/vertex counts, max curve length), each group's own LOD slot count (never the cross-group maximum), and asset-wide settings (material slot count, Dataflow asset path, unsaved-changes flag, global interpolation / simulation cache / hair interpolation type) |
| `GetGroomLODSettings` | Every group's `AutoLODBias` plus the full `FHairLODSettings` of every LOD slot. Output shape mirrors `SetGroomLODSettings`'s input |
| `GetGroomSimulationSettings` | Every group's full `FHairGroupsPhysics` (solver, external forces, bend/stretch/collision constraints, strands parameters), including the four scalar curves serialized key by key. Output shape mirrors `SetGroomSimulationSettings`'s input |
| `GetGroomInterpolationSettings` | Every group's full `FHairGroupsInterpolation` (decimation and interpolation settings). Output shape mirrors `SetGroomInterpolationSettings`'s input |
| `GetGroomRenderingSettings` | Every group's full `FHairGroupsRendering` (geometry/shadow/advanced settings). Output shape mirrors `SetGroomRenderingSettings`'s input |
| `GetGroomCardsInfo` | Every `FHairGroupsCardsSourceDescription` entry (source mesh, guide type, texture layout and paths, card/vertex counts) plus whether a `"HairCardGenerator"` implementation is currently registered |
| `GetGroomMeshesInfo` | Every `FHairGroupsMeshesSourceDescription` entry (source mesh, texture layout and paths) |
| `GetGroomGuideCurves` | Guide curve control points for one group, over one or more caller-supplied ranges (no "dump everything" mode). Truncates rather than rejects when a range exceeds the per-response cap, reporting `bTruncated` and the actually-returned range |
| `GetGroomStrandCurves` | Strand curve control points, same range/truncation contract as `GetGroomGuideCurves`, plus per-vertex color/roughness/AO and per-curve guide-weight fields |
| `GetGroomDataflowInfo` | The `UDataflow` asset currently assigned (empty when none) and the configured terminal node name. Unassigned is a normal result, not an error |
| `GetGroomBindingInfo` | Properties of a `UGroomBindingAsset` directly — binding type, source/target mesh paths, interpolation point count, per-group `GroupInfos`, whether it is currently compiling, validity |
| `ListGroomBindings` | Every `UGroomBindingAsset` that references the target `UGroomAsset`, answered entirely from Asset Registry tags — no candidate binding is loaded |
| `GetGroomCacheInfo` | Contents of a `UGroomCache` directly — type (Strands/Guides), frame range, duration, and stored animation-info attribute flags |

#### Settings & LOD writes (7) — requires `GroomAssetEdit`

| Command | Description |
|---|---|
| `SetGroomSimulationSettings` | Partial patch to one group's physics settings, including full-curve replacement for the four scalar curves. Accepts the shape `GetGroomSimulationSettings` returns, so a caller can round-trip Get → edit → Set |
| `SetGroomLODSettings` | Partial patch to one existing LOD slot's fields plus the owning group's `AutoLODBias`. Does not add or remove slots |
| `SetGroomInterpolationSettings` | Partial patch to one group's decimation/interpolation settings. Rejected when the target references a Dataflow asset unless `bAllowOverwrite` is set, because `GuideType` is exactly what Dataflow evaluation overwrites |
| `SetGroomRenderingSettings` | Partial patch to one group's geometry/shadow/advanced rendering settings |
| `SetGroomAssetSettings` | Partial patch to the three asset-wide fields (`EnableGlobalInterpolation`, `EnableSimulationCache`, `HairInterpolationType`) — no `GroupIndex`, unlike the group-scoped writes above |
| `AddGroomLOD` | Append one default-constructed LOD slot to a group; returns the new slot's index. Configure it afterward with `SetGroomLODSettings` |
| `RemoveGroomLOD` | Remove one LOD slot. Only the slot's own settings are lost — the group's curve data is untouched — but restoring it afterward means reapplying every field via `AddGroomLOD` + `SetGroomLODSettings` |

#### Cards / Meshes (4) — requires `GroomAssetEdit`

| Command | Description |
|---|---|
| `SetGroomCardsSource` | Upsert one `FHairGroupsCardsSourceDescription` entry (guide type, imported mesh, texture layout/paths) — patches an existing (group, LOD) entry or appends a new one. Does not build cards derived data |
| `SetGroomMeshesSource` | Upsert one `FHairGroupsMeshesSourceDescription` entry, same patch/append contract. Does not build meshes derived data |
| `BuildGroomCardsData` | Force `UGroomAsset::BuildCardsData()` (Derived Data Cache lookup/build, Heavy, no upper time bound). Rejects up front with `NotAllowed` when a source description asks for `GuideType == Generated` and no `"HairCardGenerator"` implementation is registered |
| `BuildGroomMeshesData` | Force `UGroomAsset::BuildMeshesData()` (Derived Data Cache lookup/build, Heavy, no upper time bound) |

#### Texture generation (2) — requires `GroomAssetCreate`

| Command | Description |
|---|---|
| `GenerateGroomFollicleMaskTexture` | Create a new follicle-mask `UTexture2D` next to the source Groom's own package and submit its pixel generation. Only submission is guaranteed — GPU generation/readback completes over the following frames with no completion signal the engine exposes. Does not link the texture to the Groom; use `SetGroomCardsSource`/`SetGroomMeshesSource` for that |
| `GenerateGroomStrandsTextures` | Create one new strands `UTexture2D` per slot the chosen layout requires, tracing strand geometry against a SkeletalMesh or StaticMesh. Same submission-only guarantee and no-auto-link behavior as `GenerateGroomFollicleMaskTexture` |

#### Curve editing & Dataflow (4)

| Command | Capability | Description |
|---|---|---|
| `SetGroomGuideCurves` | `GroomCurveEdit` | Replace guide curve control points for one or more ranges within a group, via a single `ConvertFromGroomAsset` → `ConvertToGroomAsset` round trip. Accepts exactly the shape `GetGroomGuideCurves` returns; a write never adds/removes curves, and an out-of-range write is rejected rather than truncated. Rejected when the target references a Dataflow asset unless `bAllowOverwrite` is set |
| `SetGroomStrandCurves` | `GroomCurveEdit` | Same contract as `SetGroomGuideCurves`, for strand curves |
| `SetGroomDataflowAsset` | `GroomAssetEdit` | Partial patch to the Dataflow assignment (asset path / terminal node name). Non-destructive — only changes the assignment, does not evaluate the graph or touch curve data |
| `EvaluateGroomDataflow` ⚠️ | `GroomCurveEdit` | **Experimental — cannot currently produce a useful result.** Evaluate the assigned Dataflow graph (`FDataflowInstance::UpdateOwnerAsset()`). Overwrites every group's guide/strand curve geometry and `GuideType` with the graph's output — the prior curves are not recoverable through this command. Returns `NotFound` when no Dataflow asset is assigned. **Known engine limitation**: the Groom terminal nodes implement only `FDataflowTerminalNode`'s two-argument `Evaluate()`, while `UpdateOwnerAsset()` calls the single-argument overload whose base implementation is `ensure(false)`. The graph is therefore never evaluated, yet the terminal still writes an empty result and **clears the target's hair groups**. The same happens through the engine's own paths (the Content Browser's Re-evaluate Dataflow action, `RegenerateAssetFromDataflow` / `EvaluateTerminalNodeByName`), so it is not specific to this command. Verified on UE 5.8. Treat a success response as "the request reached the engine", not as "the curves were rebuilt", and check the group count afterwards |

#### Bindings (3) — requires `GroomBindingEdit`

| Command | Description |
|---|---|
| `CreateGroomBinding` | Create a new `UGroomBindingAsset` binding a Groom to a target `USkeletalMesh`, wait for the build to finish, and save the result before responding. Omitting the source SkeletalMesh produces a binding `BakeGroomRBFDeformation` cannot later use. A path collision creates the binding under a different (numbered) name instead of overwriting — the response reports the actual path |
| `CreateGeometryCacheGroomBinding` | Same contract as `CreateGroomBinding`, binding to a `UGeometryCache` instead (synchronous build for this binding type) |
| `RebuildGroomBinding` | Rebuild an existing binding's derived data in place and wait for the build to finish. Returns `TooManyRequests` immediately (does not wait) when another request is already building the same binding. A failed rebuild cannot be undone — the engine discards the prior derived data before regenerating |

#### Import / Bake (2)

| Command | Capability | Description |
|---|---|---|
| `ReimportGroom` | `GroomCurveEdit` | Replace a Groom's hair description with a fresh translation of a source file (or the asset's own existing import file) and rebuild its derived data in place. If the source-file translation itself fails, the asset is left unmodified; if translation succeeds but the subsequent import/rebuild step fails, the asset's prior content is not guaranteed to survive. Set `bAllowOverwrite` to reimport a target that references a Dataflow asset |
| `BakeGroomRBFDeformation` | `GroomAssetCreate` | Bake a binding's RBF deformation into a brand-new `UGroomAsset`, duplicated from the binding's source Groom (including Cards/Meshes geometry). Never modifies the source Groom or the binding. Requires the binding to have both a source and target SkeletalMesh, and every group's decimation disabled (`VertexDecimation=1`, `CurveDecimation=1`) — rejected up front otherwise. **Even with every checkable precondition satisfied, the engine's own RBF root-data generation can still fail in a way that crashes the editor process** — this command is gated behind `GroomAssetCreate` (denied by default) specifically because of this residual risk |

---

## UAIP.Editor.Validation 🧩

Run the asset validators a project has registered — over a handful of named assets or over a whole content folder — read what they found, and apply the fixes they offered. UAIP never decides what "correct" means here: every judgement comes from `UEditorValidatorSubsystem` and the validators the engine and the project registered with it. Requires the `DataValidation` plugin. No Toolset bridge exists for this domain.

> **Prerequisite**: `DataValidation` ships with the engine and is enabled by default. On an editor build, UAIP compiles in support for it automatically — you no longer need to add it to the `Plugins` array of your `.uproject` or rebuild. If a project has explicitly disabled it, enable it from **Edit → Plugins** and restart the editor. While the plugin is disabled, the whole domain is missing from `uaip_list_commands`, and calling one of these commands returns `CommandNotFound` naming the plugin to enable; `UAIP.Core.ListIntegrations` reports the domain's state directly.

> **Note — material validation needs one more setting**: the engine's material validator skips every material while the project's `MaterialValidationPlatforms` setting is empty. That platform list is built once when the validator's class default object is constructed, so **changing the setting takes effect only after the editor is restarted**. `ListValidators` reports what can be observed about this under `MaterialValidation`; its `EffectivelyRunnable` is an estimate rather than an answer, because the list the validator actually holds cannot be read from outside — materials may still be skipped while every flag reads true.
>
> **Note — that setting cannot be written through UAIP**: `UAIP.Editor.Engine.ConfigSettings.SetSettingsValues` accepts `MaterialValidationPlatforms` and answers `ChangedCount: 1`, the following `SaveSettings` succeeds, and `ListValidators` then reads `PlatformsConfigured: true` — yet the value reaches only the in-memory settings object. It is written to no `.ini` file, and it is gone once the editor restarts. Set it instead from **Project Settings → Editor → Data Validation → Material Validation Platforms**, or by editing `Config/DefaultEditor.ini` (section `[/Script/DataValidation.DataValidationSettings]`) directly, and restart the editor afterwards.
>
> **Note — a job's result is not promised to equal a single call's**: `StartValidationJob` validates a few assets at a time so that the editor stays usable, and the engine raises its per-batch validation hooks once per chunk. A project validator that aggregates across a batch therefore sees several batches instead of one. Use `ValidateAssets` when that matters; it validates in a single call, for up to 8 assets.
>
> **Note — fixes come from the project, not from the engine**: no validator the engine ships offers a fix, so an empty `Assets[].Fixes[]` is the ordinary outcome rather than a sign of trouble. Fixes appear only where a project has written a validator that offers them. Validation and repair also reach different distances on purpose: validation reads from every mounted content root, engine and plugin content included, while `ApplyValidationFix` refuses with `NotAllowed` for an asset under a root UAIP will not write to (`/Engine/` and the like) — copy such an asset into project content and fix the copy.
>
> **Note — every command but `ListValidators` requires an explicitly given `SessionId`**, because a validation is followed, read and repaired after the call that started it, and only the session that started one can reach it. An identifier that names nothing the calling session may reach answers `NotFound` whatever the reason — unknown, expired, another session's, or a `ResultId` handed to a job command. Separately, `ListValidators` can only enumerate the validators the engine considers **enabled**; how many exist but are switched off is not observable.

#### Validator observation (1) — requires `EditorInspect`

| Command | Description |
|---|---|
| `ListValidators` | List the validators the editor currently considers enabled, each with `ClassPath` / `ClassName` / `IsEnabled`, plus `EnabledCount` and a `MaterialValidation` block (`ValidatorPresent`, `SettingsEnabled`, `PlatformsConfigured`, `EffectivelyRunnable`, `Note`). Use it to tell "nothing was wrong" apart from "nothing was inspected" — a result with no findings means little while it is unknown whether any validator was enabled at all. The one command in this domain callable without an explicit `SessionId` |

#### Validation (2) — requires `AssetValidation`

| Command | Description |
|---|---|
| `ValidateAssets` | Validate 1–8 assets synchronously and answer with the result. Assets that came back invalid, that carry a warning, or that were not inspected at all are listed individually; the ones nothing was found on are counted in `Summary` and listed only when `IncludeValid` is true. The result JSON is answered inline while it stays under 64 KiB and is written as an artifact either way. ⚠️ The call has no time budget, no interruption point and no progress to poll — validating a single material compiles shaders and can take seconds on its own, so a call carrying heavy assets can leave the editor unresponsive for seconds to tens of seconds. A `ResultId` is answered only when the result carries at least one fix. A path repeated inside `AssetPaths` is rejected with `InvalidParams` rather than silently de-duplicated — an explicit list of 8 paths that validates 7 assets would be a confusing answer |
| `StartValidationJob` | Validate a folder (`PackagePath` + `Recursive`) or an explicit `AssetPaths` list — one or the other, never both and never neither — in steps across many frames, and answer with a `JobId` rather than a result. `MaxAssets` bounds what is kept after redirectors are resolved and external objects are folded into their owners; anything dropped raises `Summary.AssetLimitReached`. A folder so wide that enumeration alone exceeds the internal ceiling fails outright with `EnumerationLimitExceeded` rather than validating an arbitrary prefix of it, so narrow the folder rather than lowering `MaxAssets`. Starting a second job while one of the same session is still running stops the earlier one and reports `ReplacedPreviousJob`; starting again too soon after the last one answers `TooManyRequests`. `Recursive` is meaningful only alongside `PackagePath`; passing it with `AssetPaths` is rejected rather than ignored, as is an `AssetPaths` list longer than 20,000. `PackagePath` accepts a content root such as `/Game` as well as a folder beneath it (a trailing `/` is dropped); a refused path is `InvalidParams` with a message of the form `'PackagePath' value '…': <reason>` |

#### Job observation & control (3) — requires `EditorInspect`

| Command | Description |
|---|---|
| `GetValidationJobStatus` | Poll one job: `State` (`Preparing` / `Enumerating` / `Normalizing` / `Validating` / `Finalizing` / `Completed` / `Failed` / `Aborted`), `PhaseLabel`, `ProcessedCount` / `TotalCount`, `ElapsedSeconds`, `FailureReason` (one of a fixed set of values, reading `None` until the job fails), and the running totals `NumInvalid` / `NumWarnings`. Counts, states and durations are the whole of what is reported — no message a validator produced and no asset path appears here. Answering costs the same whatever the size of the job, so polling does not slow the validation down |
| `GetValidationJobResult` | Fetch what a job produced: the job-wide counts inline, plus the full result as a JSON artifact listing every asset that came back invalid, carried a warning, or was not inspected. Nothing is validated or scanned again. Answered for a job that failed or was cancelled as well as for one that completed — whatever had been validated before it stopped is in the artifact, and `Truncation` explains what was left out. A job that has not finished yet is not answered with a partial result; poll the status first. A successful read restarts the job's retention countdown |
| `CancelValidationJob` | Stop a job at its next chunk boundary — **not immediately**: the engine's validation call cannot be broken into once entered, so the chunk in flight runs to completion and what it produced is still kept. Polling right afterwards may therefore still show the job working. The job keeps its identifier and its result and reads `Aborted` from then on, which is usually the point of stopping a long run rather than abandoning it. Cancelling an already-finished job succeeds and does nothing, reporting `WasRunning: false`. ⚠️ Declared read-only and gated by `EditorInspect` alongside the observing commands even though it moves a job to `Aborted`; what bounds it is ownership of the job |

#### Fix application (1) — requires `AssetValidationFix`

| Command | Description |
|---|---|
| `ApplyValidationFix` | Apply one fix a validator offered alongside a message it produced, named by `ResultId` (the `JobId` `StartValidationJob` returned, or the `ResultId` `ValidateAssets` returned) and the `FixId` quoted from that result's `Assets[].Fixes[]`. Fixes are applied one at a time, and applying one can rule out the alternatives it was mutually exclusive with, so the answer carries `UpdatedFixes`: the applicability of every fix still held for that result, re-queried afterwards. A fix is reachable only through the result that produced it — an identifier that result does not hold reports `NotFound`, and the identifier's own text is never used to find an asset, so a result cannot be used as a ticket for repairing something it never validated. `AssetSaved` reports whether the asset was left written to disk. The one command in this domain that is not read-only, and it is refused outright while `DisableSave` is in force, because a fixer cannot be asked whether it will save what it repairs |

---

## UAIP.Editor.LiveLink 🧩

Editor-side LiveLink work: preset assets, binding a Subject to a placed actor's LiveLink controller component, MessageBus discovery and connection, and Take Recorder driven recording. **Requires both the `LiveLink` and the `Takes` plugins.** On an editor build, UAIP compiles in support for both automatically whenever they exist in the engine (in practice always, since both ship with the engine) — no `.uproject` declaration needed. What has to be true is that both are **enabled** for the project: if either is disabled, the whole domain is not registered and these commands return `CommandNotFound`, naming the plugin to enable — enabling both and restarting the editor is the fix, no rebuild involved. (If a plugin were genuinely absent from this engine version, no toggle would help; that reports `UnavailableDetail: "OptionalPluginDisabled"` instead — see [UnavailableDetail](#unavailabledetail--the-eight-reasons-behind-a-handlerunavailable-refusal).) Once the domain is registered, the four recording commands (`StartLiveLinkRecording`, `StopLiveLinkRecording`, `CancelLiveLinkRecording`, `GetLiveLinkRecordingStatus`) can still individually report `Available: false` with `UnavailableDetail: "ExecutionEnvironment"` if the `TakeRecorder` module has not actually finished loading into this process yet — relaunching, not rebuilding, resolves that too.

The observation half of LiveLink lives in [UAIP.Runtime.LiveLink](#uaipruntimelivelink), which carries no plugin requirement at all.

Only one LiveLink-configuration operation runs at a time. While a preset apply is in flight, and while a recording is in progress, the mutating commands here and in `UAIP.Runtime.LiveLink` are refused; **reads are never refused**, so `GetLiveLinkPresetInfo` and `GetLiveLinkRecordingStatus` stay answerable throughout. A refusal that will clear on its own is reported as `TooManyRequests`; one that needs the other operation ended first is `NotAllowed`.

### Presets (4)

| Command | Description |
|---|---|
| `GetLiveLinkPresetInfo` | Report the Sources and Subjects a `ULiveLinkPreset` asset stores, without touching the live client. The pre-snapshot to take before `ApplyLiveLinkPreset`. Each stored settings object is reported by class path only — its values, the connection string included, are never returned. Read-only (`EditorInspect`); permitted during PIE and while an apply or a recording is in flight |
| `ApplyLiveLinkPreset` | ⚠️ **Destructive.** Replace the client's whole configuration with the preset's. **Every existing Source is removed before the preset is rebuilt, and a run that does not finish leaves a partially removed configuration** — not the previous one. The engine keeps no copy to roll back to, so UAIP cannot restore it either. Asynchronous; the response arrives when the engine's apply concludes. `TooManyRequests` while another apply is in flight (waiting helps), `NotAllowed` while a recording is in flight (stop it first); either refusal leaves the client untouched. Requires `LiveLinkPresetApply` |
| `AddLiveLinkPresetToClient` | Add the preset's Sources and Subjects to the current configuration, synchronously. Additive by default and non-destructive. Setting `RecreateExisting` removes and rebuilds every Source and Subject the preset names, which **is** destructive and additionally requires `LiveLinkPresetApply` — the name is echoed under `RecreateExistingRequiredCapability` on every response. Requires `LiveLinkPresetAdd` |
| `SaveLiveLinkPreset` | Write the client's current configuration to a preset asset at `PresetPath`, creating it or overwriting an existing preset; the response says which of the two happened. **A path already holding an asset that is not a LiveLink preset is refused rather than replaced.** Project content paths only. Refused during PIE / SIE. Requires `LiveLinkPresetSave` |

### Component binding (1)

| Command | Description |
|---|---|
| `SetLiveLinkComponentSubject` | Bind a LiveLink Subject to a LiveLink controller component on a placed actor, and name the component on that actor the controller drives. `ComponentId` and `ExpectedComponentClass` come from `ListActorComponents` or `AddActorComponent` (see [UAIP.Editor.Level](#uaipeditorlevel)); the expected class is re-checked so a stale identifier is refused rather than followed. `SubjectName` is resolved against the currently enabled Subjects and refused with `InvalidParams` listing `Candidates` when more than one carries the name; the key it resolved to is reported back. Only components on that one actor are accepted — Blueprint-owned ones go through the Blueprint component commands. Refused during PIE / SIE. Undoable. Requires `LiveLinkComponentEdit` |

### MessageBus discovery and connection (2)

| Command | Description |
|---|---|
| `DiscoverLiveLinkMessageBusProviders` | Broadcast a discovery ping and report every provider that replies within `DurationSeconds` (clamped to [1, 30]; the applied value comes back as `EffectiveDurationSeconds`). Each reply is returned as an opaque `Token` plus `ProviderName` — **never the underlying network address**. A token resolves only for the session that ran the discovery and only within a short TTL; it is invisible to and unusable by any other session. `IncludeSensitiveDetails: true` adds each provider's `MachineName` and requires `LiveLinkSourceInspectSensitive` **in addition** to `LiveLinkNetworkDiscovery`; the name is echoed under `SensitiveDetailsRequiredCapability` whether or not it was asked for. At most one discovery runs at a time (`TooManyRequests`). Asynchronous. Requires `LiveLinkNetworkDiscovery` |
| `ConnectLiveLinkMessageBusSource` | Connect a discovered provider to the client as a new Source, addressed by the `Token` discovery returned. The token's ownership, TTL and provider validity are re-verified before anything is built; a failed verification is `InvalidParams` whichever of the three it was. Returns the new `SourceGuid` and `ProviderName` only — it does **not** wait for or report on any Subject appearing, since a healthy connection can legitimately show none for a while. Watch `ListLiveLinkSources` / `ListLiveLinkSubjects` for that. Requires `LiveLinkSourceConnect` |

### Recording (4)

| Command | Description |
|---|---|
| `StartLiveLinkRecording` | Record one or more LiveLink Subjects into a new LevelSequence through `UTakeRecorderSubsystem`, **without opening Sequencer and without any modal dialog**. Each entry of `SubjectNames` is resolved against whichever Subject with that name is presently enabled; a name matching none is `NotFound`, one matching more than one is `InvalidParams` listing every candidate under `ResolvedSubjects`. `NotAllowed` / `TooManyRequests` when a preset apply or another recording is in flight, `ExecutionFailed` when a Take Recorder recording is already running outside UAIP's bookkeeping — in every case with no side effect. **The destination follows `UTakeRecorderProjectSettings`; this command accepts no arbitrary save path.** Allowed during PIE. Requires `LiveLinkRecording` |
| `StopLiveLinkRecording` | Stop the recording UAIP itself started and report the package path of the LevelSequence it produced. `NotAllowed` when no UAIP-owned recording is in progress — whether nothing is recording at all, or the recording in progress was started elsewhere (the Take Recorder panel, another plugin). Allowed during PIE. Requires `LiveLinkRecording` |
| `CancelLiveLinkRecording` | Cancel the recording UAIP itself started, **discarding what it captured** rather than finalizing it into a usable LevelSequence. Same `NotAllowed` rule as `StopLiveLinkRecording`. Allowed during PIE. Requires `LiveLinkRecording` |
| `GetLiveLinkRecordingStatus` | Report `IsRecording` (a Take Recorder recording is in progress, whoever started it) and `StartedByUAIP`. Only when `StartedByUAIP` is true does the response also carry `ResolvedSubjects`, `ElapsedSeconds` and `TargetSequencePath` — nothing observes when an externally started recording began or what it targets, so those fields are absent rather than guessed. Read-only (`EditorInspect`) |

> **A recording UAIP started but a human stopped is detected, not left stuck.** If someone stops or finishes a UAIP-started recording from the Take Recorder panel, UAIP notices and clears its own "recording in progress" state, so the mutating commands it was blocking do not stay blocked. The reverse is also enforced: a recording UAIP did not start is never stopped or cancelled by these commands.

---

## UAIP.Editor.Mass 🧩

Reading and assembling the data a Mass simulation is built from: the trait classes a session can choose from, Mass entity config assets (what they declare, what they inherit and whether they are valid) and the spawners that place entities. Requires the **MassGameplay** plugin; a build made without it still lists the seven commands, with `Available: false` (`UnavailableDetail: OptionalPluginDisabled`). Not provided in the demo build. To watch the entities of a running game, use [`UAIP.Runtime.Mass`](#uaipruntimemass).

**Capabilities.** The three reading commands require `EditorInspect` (DefaultAllow). The four writing commands require `MassAssetEdit` (DefaultDenied), and some calls need more, judged per call from what the request names: `MassCustomTypeEdit` for a trait or spawn data generator class from outside the engine's own Mass modules, and `MassProjectCodeExecution` wherever a call makes project code run. A refusal for a missing capability is `CapabilityNotAvailable` and lists `RequiredCapabilities` and `MissingCapabilities`; nothing is changed. See [Safety & Capabilities](safety.md#mass-observation-and-editing), which also says what granting `MassProjectCodeExecution` exposes you to.

**Reading never changes the editor world.** `DumpMassEntityConfig`, `ValidateMassEntityConfig` and `ListMassEntityTraits` work out what a config builds by building each trait in a private world that exists only for the call, so neither the editor world nor the asset is touched. The result is for the execution mode `EditorWorld` (`EvaluatedExecutionMode`): a trait that decides by the execution mode of its world may build something else in a running game, which `Limitations` says. A trait from outside the engine's Mass modules is neither built nor has its property values read unless the session holds `MassProjectCodeExecution`; it is listed under `SkippedTraits` (or with `ElementsOmittedReason`) instead, and `ValidateMassEntityConfig` then reports `IsComplete: false` and a `Verdict` of `Inconclusive` unless an error that no skipped trait could undo already makes it `Invalid`. Reading is permitted during PIE.

**Ambiguous element names.** When the `AddsElement` of `ListMassEntityTraits` is a short name that matches more than one element type, the command refuses with `InvalidParams`, and the failed response's `Result` carries `AmbiguousName` (the name as given), `Candidates` (the full type paths, sorted, at most 10) and `TotalCandidateCount` (how many types matched). Pass one of the candidate paths to remove the ambiguity.

**Writing.** A write is one undoable step. A refused request changes nothing — not the asset, not the dirty flag of its package and not the undo history. Writes are refused with `NotAllowed` while a play session is in progress, and for an asset in a place that is read-only (for example under `/Engine`). After a successful write to a config, the editor world's cached templates of that config and of its loaded descendants are dropped; the response reports `RemovedEditorWorldTemplates`, `UnloadedDescendantCount` and `TemplateRegistryUnavailable`. Writes made through the generic property commands, by hand or by Undo / Redo do not drop them.

> **Mass Debugger tab.** While a Mass Debugger tab is open, creating the temporary world makes an engine-internal check (an `ensure`) fail once and print a call stack in the log (a debugger attached to the editor stops there). The engine does the same for the temporary world it creates to list traits. The commands still succeed, and the temporary world does not appear in the Mass Debugger's list of environments. Close the tab first if you want to avoid the message.

| Command | Description |
|---|---|
| `ListMassEntityTraits` | Lists the Mass trait classes a session can choose from. Each entry has `ClassPath`, `DisplayName`, `Admission` (`Allowed`, `RequiresCapabilities`, `NotAddable` or `CompatibilityUnknownUntilAuthorized`), `RequiredCapabilities` / `MissingCapabilities` for adding it, `EvaluationRequiredCapabilities` for reading its elements, `Deprecated`, and the elements it adds or requires (`AddedElements` / `RequiredElements`). A class the session cannot place is listed with its refusal, not dropped. `AddsElement` lists only the traits that add that element (`UnevaluatedTraitCount` counts those that might have and could not be read), `NameFilter` matches the class path or display name without regard to case, and `MaxClasses` (1–1000, default 200) caps the list (`TotalCount` / `Truncated`). Ordered by class path. Data holds the leading entries and the artifact holds the rest up to a size budget. Read-only, requires `EditorInspect`, and `MassProjectCodeExecution` only to read the elements of project traits |
| `DumpMassEntityConfig` | Reads a Mass entity config asset (`AssetPath`) and saves what it declares: `OwnTraits`, `ParentChain` (nearest first), `InheritanceCycle`, `CombinedTraits` (every trait along the parent chain, with `OverriddenBy` and `Effective`), `Composition` (the elements of the template the effective traits build), `PerTrait` (what each effective trait added, required and removed) and `SkippedTraits`. A parent chain that loops back on itself leaves `CombinedTraits`, `Composition` and `PerTrait` empty and `Limitations` says `CompositionNotComputedDueToCycle`. Read-only, requires `EditorInspect`, and `MassProjectCodeExecution` only to evaluate project traits |
| `ValidateMassEntityConfig` | Validates a config (`AssetPath`) the way the engine validates the entity template its traits build. `Verdict` is `Valid`, `Invalid` or `Inconclusive`, `IsComplete` says whether every trait was evaluated (when true, `Verdict` agrees with the engine's own validation), and each entry of `Issues` has a `Kind` (`MissingElement`, `DuplicateElement`, `TraitValidationFailed`, `InheritanceCycle` or `TraitOverridden`), a `Severity` and — for a missing element — `SuggestedTraits`. `SuggestionsComplete` and `UnevaluatedTraitCount` say whether the suggestions rest on every trait class. The reason a trait's own validation failed is only in the engine log (`TraitValidationReasonOnlyInLog`). Read-only, requires `EditorInspect`, and `MassProjectCodeExecution` only to evaluate project traits |
| `AddMassEntityConfigTrait` (requires `MassAssetEdit`) | Adds a trait to a config. `TraitClass` is the path of a trait class that is already loaded, as `ListMassEntityTraits` reports it (an unloaded class is `NotFound`, not loaded). `InitialProperties` (optional, at most 64 entries) are written into the new trait before it is added, and a refused value cancels the whole addition. `ValidTargetConfig` (optional) names target flags (`Standalone`, `Server`, `Client`, `Editor`, `EditorWorld`, comma separated, or `None`); UE 5.7 has none and accepts only `NotApplicable`. A trait the config already declares for the same targets is `InvalidParams` with `CandidateIndices`; a trait a parent declares is replaced and `OverridesParentTrait` says so. Also requires `MassCustomTypeEdit` when the class comes from outside the engine's Mass modules, and `MassProjectCodeExecution` whenever `InitialProperties` are passed, whatever the class |
| `RemoveMassEntityConfigTrait` (requires `MassAssetEdit`) | Removes a trait the config declares itself. Name it with exactly one of `Index` (its position in the config's own traits, as `DumpMassEntityConfig` reports under `OwnTraits`) or `TraitClass`. A class that matches several of the config's own traits is `InvalidParams` with `CandidateIndices`; a trait only a parent declares is `InvalidParams` with `ParentAssetPaths` (the configs to edit instead). Requires no other capability, because removing a trait runs none of its code |
| `SetMassEntityConfigTraitProperty` (requires `MassAssetEdit` and `MassProjectCodeExecution`) | Sets one property of a trait the config declares itself. The trait is named as in `RemoveMassEntityConfigTrait`; `PropertyPath` (at most 1024 characters) and `Value` (null is not accepted) name what to write. A string is written as text when the property accepts text, and any other JSON value is written as a structured document. A value that would make the trait duplicate another of the config's traits is `InvalidParams`; a value the property write path refuses is reported with its own error code. Needs both capabilities **whatever the trait class**, because every member of a trait is written through the shared property write path, and for a trait from outside the engine's Mass modules the write runs the project's own code. A value that holds a reference or a nested object can also need `PropertyReferenceEdit` or `PropertyStructuredEdit` |
| `ConfigureMassSpawner` (requires `MassAssetEdit`) | Sets the `Count`, `EntityTypes`, `SpawnDataGenerators` and `AutoSpawnOnBeginPlay` of a Mass spawner in the editor world (`ActorIdentifier` is its label or object path). At least one is required and only the ones given are replaced; a list that is given replaces the whole list (at most 64 entries, `Proportion` defaults to 1), and a new generator is created for each entry. A generator class must be already loaded. Also requires `MassCustomTypeEdit` when a generator class comes from outside the engine's Mass modules, and `MassProjectCodeExecution` when replacing the entity types makes the editor world register a template that resolves to such a trait (inherited traits included) — a config whose template already exists is reused and needs neither. The response says what was built and what was reused (`TemplatesBuiltInEditorWorld`, `ExistingTemplatesReused`); a non-zero `ExistingTemplatesReused` can mean an old template is in use (`ExistingEditorWorldTemplateReused`) |

**Errors.**

| ErrorCode | When |
|---|---|
| `NotAllowed` | A write while a play session is in progress, or on an asset in a read-only place |
| `NotFound` | The asset, the trait, the class (not loaded) or the spawner does not exist; a spawner label that more than one actor carries is `NotFound` listing them in `CandidateActorPaths` |
| `InvalidParams` | A duplicate trait, an ambiguous or parent-only trait, an asset that is not a config, a class that is not a trait or generator, a malformed or out-of-range parameter |
| `CapabilityNotAvailable` / `PolicyViolation` | A required capability is not granted / is denied by the safety policy |

**Using the generic commands with Mass assets.** Creating an entity config asset, placing a spawner and setting a config's parent are done with the existing generic commands. Since this domain was added, a generic property write to a Mass asset (a config, a spawner, a trait, a generator, or the structs that carry their settings) additionally requires `MassAssetEdit` and `MassProjectCodeExecution`. See [Safety & Capabilities](safety.md#mass-observation-and-editing).

---

## UAIP.Runtime.Engine.Log

Log verbosity inspection and log category listing at runtime. These are the Runtime-domain counterparts to `UAIP.Editor.Engine.Log`.

| Command | Description |
|---|---|
| 🆓 `GetLogVerbosity` | Get the current verbosity level of a log category |
| 🆓 `GetLogCategories` | List all registered log category names |
| `SetLogVerbosity` | Set the verbosity level of a log category (requires `LogVerbosityEdit`) |

---

## UAIP.Runtime.Engine.Plugin

Plugin inspection at runtime. Read-only commands available without any special capability. These are the Runtime-domain counterparts to `UAIP.Editor.Engine.Plugin` commands.

| Command | Description |
|---|---|
| 🆓 `ListPlugins` | List discovered or enabled plugins with optional `EnabledOnly` filter and `LoadedFrom` filter |
| 🆓 `GetPluginInfo` | Get detailed info for a plugin (11 fields: Name, FriendlyName, Version, Description, Category, IsEnabled, IsMounted, Type, BaseDir, LoadedFrom, Dependencies) |
| 🆓 `IsEnabled` | Check whether a plugin is currently enabled (note: `.uproject` declaration and actual load state may diverge until restart) |
| 🆓 `GetPluginDependencies` | Get the direct plugin dependencies declared by a plugin |
| 🆓 `GetPluginForAsset` | Resolve the owning plugin for a given asset path |

---

## UAIP.Runtime.Engine.CVar

Read and write engine-wide console variables (CVars). CVars are global engine state — independent of any World or PIE session. Sensitive CVars are automatically excluded.

🔒 requires `RuntimeCVarRead` (DefaultDenied). ✏️ requires `RuntimeCVarWrite` (DefaultDenied). The demo distribution's `Config/DefaultUAIP.ini` pre-grants `RuntimeCVarRead`, so the 🆓 commands below work out of the box in the demo.

| Command | Description |
|---|---|
| 🆓🔒 `GetConsoleVariable` | Get the name, current value, type, and help text for a CVar (sensitive names return `NotFound`) |
| 🆓🔒 `SearchConsoleVariables` | Search CVars using a wildcard (`*`) pattern (default 50 results, max 200) |
| ✏️ `SetConsoleVariable` | Set the value of a CVar (sensitive names and `ECVF_ReadOnly` CVars are rejected; `ECVF_Cheat` CVars are rejected unless `AllowCheatCVarWrite` is enabled) |
| ✏️ `ResetConsoleVariable` | Reset a CVar to its default value (sensitive names and `ECVF_ReadOnly` CVars are rejected; `ECVF_Cheat` CVars are rejected unless `AllowCheatCVarWrite` is enabled) |

> **Note**: The legacy `GetConsoleVariable` and `SearchConsoleVariables` commands under `UAIP.Runtime.PIE` are deprecated and will be removed in v1.2. Use these commands instead.

---

## UAIP.Runtime.Engine.Config

Raw ini key access for runtime and packaged builds. Reads and writes ini keys directly without going through `ISettingsModule`. Write commands are blocked in packaged builds.

| Command | Description |
|---|---|
| 🆓 `GetConfigValue` | Read the string value of an ini key given section and key name. No capability required |
| `SetConfigValue` | Write or delete a raw ini key. Requires `ConfigSettingsEdit`. Blocked in packaged builds. Rejects ini injection characters (`[`, `]`) in key and value fields |

---

## UAIP.Runtime.PIE

PIE session lifecycle. Manipulating the running world is [`UAIP.Runtime.World`](#uaipruntimeworld).

| Command | Description |
|---|---|
| 🆓 `StartPIE` | Start a Play-in-Editor session |
| 🆓 `StopPIE` | Stop the active PIE session |
| 🆓 `PausePIE` | Pause the active PIE session |
| 🆓 `ResumePIE` | Resume a paused PIE session |
| 🆓 `LoadMap` | Load a map in the active PIE session and wait for completion |
| 🆓 `GetPIEState` | Return the current PIE state — `Running`, `Stopped`, `Paused`, or `Simulating` |

### Toolset bridges (3) 🧩

Bridge commands via the `EditorAppToolset` (UE 5.8+, EditorToolset plugin). Provider: `Toolset.Editor.Toolset.PIE.*`.

| Command | Description |
|---|---|
| `Toolset.Editor.Toolset.PIE.StartPIE` | Start a PIE session (async, requires `PIEControl`) |
| `Toolset.Editor.Toolset.PIE.StopPIE` | Stop the active PIE session (async, requires `PIEControl`) |
| `Toolset.Editor.Toolset.PIE.IsPIERunning` | Return whether PIE is currently active |

---

## UAIP.Runtime.World

Manipulate and inspect the **running** game world. These commands were registered under `UAIP.Runtime.PIE` in earlier releases.

Every command in this domain except `QuitGame`, `ListPlayWorlds` and the two CVar commands accepts the optional `TargetNetRole` / `TargetPIEInstance` parameters — see [Choosing which play world a Runtime command acts on](#choosing-which-play-world-a-runtime-command-acts-on).

| Command | Description |
|---|---|
| `SpawnActor` | Spawn an actor of a class in the active PIE world (requires `RuntimeActorManipulation`) |
| `DestroyActor` | Destroy an actor in the active PIE world (requires `RuntimeActorManipulation`) |
| `TeleportActor` | Teleport an actor to a world-space location / rotation |
| `PossessActor` | Have a player controller possess an actor |
| `SetTimeScale` | Set the global time dilation of the active game world |
| `QuitGame` | Request a graceful quit of the running game process (requires `RuntimeActorManipulation`). During PIE it stops the PIE session. In an editor where no game is running it answers `ExecutionFailed` and the editor stays open — `QuitGame` quits the running game, not the editor; use [`ShutdownEditor`](#uaipeditorworkspace) (`UAIP.Editor.Workspace.ShutdownEditor`) to close the editor. It used to answer `Success: true` without doing anything in that case |
| `ExecuteConsoleCommand` | Execute a console command in the active game world (requires `RuntimeExecCommand`) |
| 🆓 `GetConsoleVariable` | Value, type and help text of a console variable; sensitive names report as not found (requires `RuntimeCVarRead`) |
| 🆓 `SearchConsoleVariables` | Wildcard (`*`) search over registered console variables — `MaxResults` default 50, max 200; sensitive names are excluded |
| `ListPlayWorlds` | Every play world the engine currently holds — `PIEInstance`, `NetMode` (`Standalone` / `DedicatedServer` / `ListenServer` / `Client`), `MapName`, `bIsPrimaryPIEInstance` — plus `Count`. Returns an empty list rather than an error when nothing is playing, so it is safe to call before starting play, and it takes no parameters at all. What it reports is exactly what `TargetNetRole` / `TargetPIEInstance` accept. Requires no capability |

> ⚠️ **Breaking change — `SetTimeScale`, `TeleportActor`, `PossessActor` and `ExecuteConsoleCommand` no longer act on the level open in the editor.** These four used to resolve their world without filtering by world type, so with no play session running they picked up the first world they found — **the level being edited** — and really did apply the change there. They no longer do: outside a play session they now fail and change nothing. The refusal also changed shape, from `ExecutionFailed` with `No active game world found.` to **`NotAllowed` with `PIE is not running.`** These four are addressed to a running game; to change the level being edited, use the matching `UAIP.Editor.*` commands. Update anything that pattern-matches the old error code or the old message text.

> ⚠️ **`TeleportActor` no longer reports success for an actor it could not move.** `AActor::TeleportTo` returns `true` even when nothing moved: with a root component that is not a `UPrimitiveComponent`, and on the paths that skip the collision check, the result of the move is never read back. An actor whose root component mobility is not `Movable` cannot be moved during play, so the command used to report success while the actor stood still. It now compares the location and rotation before and against after the call, and answers **`ExecutionFailed`** when nothing changed. The refusal message also names which cause applies, where it used to report all of them as one sentence: the root component's mobility, an actor with no root component at all, or a destination the actor could not be placed at. A move that collision nudged to a nearby spot still succeeds, as before. For the same reason `UAIP.Editor.Level.SetActorTransform` now answers `ExecutionFailed` when the transform could not be applied, which is the case for an actor with no root component.

> **A game world that is not an editor play session reports `PIEInstance: -1`** — a packaged build's single world, for instance. That `-1` is a real index here and **can be passed to `TargetPIEInstance` as is**; it is not a "no instance" sentinel to be filtered out.

### Data Layer runtime state (4)

World Partition Data Layer state **in a running play world**. Authoring Data Layers — creating them, reparenting them, choosing the state a level starts in — is [`UAIP.Editor.WorldPartition`](#uaipeditorworldpartition); nothing in this group writes anything to disk. `DataLayerInstanceId` is the same identifier those editor commands use, so one looked up before play starts can be passed straight in.

| Command | Description |
|---|---|
| `SetDataLayerRuntimeState` | Set one runtime Data Layer instance's state — `RuntimeState` is `Activated`, `Loaded` or `Unloaded` (case-insensitive; any other spelling is `InvalidParams` listing the three accepted values). `bIsRecursive: true` applies the same state to every descendant and adds `AffectedCount`, `bPartialSuccess` and `RejectedDescendants[]`, each entry naming a `DataLayerInstanceId` and a short `RejectionReason` token (`NotRuntime`, `ClientOnlyFromServer`, `ServerOnlyFromClient`, `AuthoritativeFromClient`, `Unknown`) — a refusal of the *requested* instance itself fails the whole call instead. Reports `PreviousRuntimeState`, `RequestedRuntimeState`, `EffectiveRuntimeState`, `bStateChanged`, `bEffectiveStateDiffers`, `LimitingAncestorId` (only when an ancestor was actually identified), both streaming flags and the world acted on. `NotFound` for an unknown identifier — **and for a Data Layer that has no runtime state at all** (an editor-only or private one), because the engine removes those from a world the moment it starts playing, so from a play world they were never there. `ExecutionFailed` for a world without World Partition, `NotAllowed` when the world's net role is not allowed to make the change. Requires `RuntimeDataLayerControl` |
| `ListDataLayerRuntimeStates` | Every Data Layer instance in the target play world with its `DataLayerInstanceName`, `DataLayerType`, `RuntimeState`, `EffectiveRuntimeState`, `ParentInstanceId` (omitted at the root), `bIsClientOnly` and `bIsServerOnly`. **The array itself lives in the JSON artifact**; the response carries `Count` — how many entries that array holds — alongside `bIsWorldPartitionEnabled`, `NetMode`, `WorldContext` and `PIEInstance`, so a caller can branch without fetching the artifact first. Only Data Layers that have a runtime state appear; editor-only and private ones are removed from a world when play starts, so they are absent here and the editor-side [`ListDataLayers`](#uaipeditorworldpartition) is where you see them with their type. A level without World Partition answers an empty list with `bIsWorldPartitionEnabled: false`, not an error. Requires no capability |
| `GetDataLayerRuntimeState` | One instance's full description: the same per-instance fields `ListDataLayerRuntimeStates` reports, plus `bEffectiveStateDiffers`, `LimitingAncestorId` and both streaming flags. Small enough that the whole payload is mirrored into the response as well as the artifact. A level without World Partition answers `bIsWorldPartitionEnabled: false` rather than `NotFound`, which is what distinguishes "this level has no Data Layers at all" from "no Data Layer by that identifier". Requires no capability |
| `WaitForDataLayerStreaming` | Poll until streaming settles for the instances named in `DataLayerInstanceIds`, or — when that is omitted or empty — for every runtime Data Layer instance in the target world. Returns `Success` with `ElapsedSeconds` and an empty `IncompleteDataLayerInstanceIds[]` once everything settles, `Timeout` with the same fields listing what had not. `ExecutionFailed` if the play world is destroyed mid-wait, so a wait never outlives the session it was watching. A level without World Partition completes immediately with `bIsWorldPartitionEnabled: false`. Requires no capability |

> **`WaitForDataLayerStreaming`'s limits are checked before the wait starts, and a violation is `InvalidParams`, never `Timeout`.** `TimeoutSeconds` defaults to 30 and must be a finite number greater than 0 and **at most 60** — the same ceiling `WaitForCondition` carries, so the wait commands share one contract. `PollIntervalSeconds` defaults to 0.1 and must be between 0.05 and 1.0. `DataLayerInstanceIds` takes **at most 64 entries**; needing more is the signal to omit the parameter and wait on the whole world instead. An identifier in the list that names no Data Layer is `NotFound`, again before any waiting happens.

> **The two streaming flags answer different questions, and neither covers the other.** `bStreamingCompleted` is scoped to the Data Layers the call is about, but does not see spatially loaded cells. `bWorldStreamingCompleted` covers the whole world, but cannot be narrowed to those Data Layers. `SetDataLayerRuntimeState`, `GetDataLayerRuntimeState` and `WaitForDataLayerStreaming` all report both for exactly that reason — **wait for both when it has to be certain**.

> **`bStateChanged` is not a success flag.** It answers "is the state different from what it was", so a Data Layer that already held the requested state comes back with `bStateChanged: false` on a call that fully succeeded. Judge whether the request took effect by comparing `RequestedRuntimeState` with `EffectiveRuntimeState`. When those two differ, `bEffectiveStateDiffers` is `true` and `LimitingAncestorId` names the ancestor holding the effective state down — an unloaded parent caps what a child can reach, and the request is recorded rather than lost.

### Toolset bridges (1) 🧩

Bridge command via the `EditorAppToolset` (UE 5.8+, EditorToolset plugin). Provider: `Toolset.Editor.Toolset.World.*`.

| Command | Description |
|---|---|
| `Toolset.Editor.Toolset.World.SearchCVars` | Search console variables by name substring; sensitive variables are excluded (requires `CVarInspect`) |

---

## UAIP.Runtime.Observation

Runtime captures and state dumps.

| Command | Description |
|---|---|
| 🆓 `CaptureViewportImage` | PNG screenshot of a specified player's game viewport |
| 🆓 `DumpWorldState` | Snapshot of all actors / components in the active PIE world (JSON) |
| 🆓 `DumpActorState` | State of a specified actor (optionally including components). An actor that cannot be found is `NotFound`, not `ExecutionFailed`, so a scenario's `RetryCount` no longer retries it |
| 🆓 `DumpComponentState` | State of a specified actor component. A component that cannot be found is `NotFound`, not `ExecutionFailed`, so a scenario's `RetryCount` no longer retries it |
| 🆓 `DumpRuntimeLog` | Buffered runtime log as a text artifact |
| 🆓 `CapturePerformanceSnapshot` | CPU / GPU performance snapshot (FPS, memory, draw calls) |
| 🆓 `CheckpointCapture` | Combined screenshot + state dump (scenario primitive) |
| 🆓 `SearchLoadedClasses` | Search loaded classes (used for runtime introspection) |
| 🆓 `DumpGameViewportWidgets` | The widget tree of the game viewport of the play world — the game's own UI, with none of the editor's toolbars or tabs. The whole tree is saved as a JSON artifact; the response carries the node count, whether and where the walk was cut by `MaxDepth` / `MaxNodes`, the first 50 top level user widgets, the keyboard and gamepad focus and the screen area of each local player, and `Limitations`. Each node gives its Slate type, the UMG name and class, its rectangle, whether it is effectively visible and which layer it sits in. Text is read only with `IncludeText: true`. See [Game viewport UI and HUD](#game-viewport-ui-and-hud-4) |
| 🆓 `FindGameViewportWidgets` | Searches the same tree for the nodes that meet every condition given (`WidgetClass`, `SlateType`, `WidgetName` / `WidgetNameContains`, `OwningPlayerIndex`; at least one is required). `WithinWidgetPath` narrows the search to the subtree of one widget, such as a CommonUI screen. Each match carries the `TypePath` and the `Fingerprint` that `ClickGameViewportWidget`, `PressGameViewportUIKey` and `TypeGameViewportText` take back. A search that finds nothing is a success; `ResultLimitReached` and the `SearchIncomplete` limitation say whether the list was cut or the walk stopped early. Text is never read |
| 🆓 `DumpGameViewportWidgetTexts` | The text of **every** text widget of the game viewport, on screen or not, and editable text with its value, as a JSON artifact. Each entry says whether its text is on screen. Requires `RuntimeWidgetTextRead` (DefaultDenied). The plain value of a password field is never written to the artifact; it appears in the response (`PasswordFieldValues`) only when the session also holds `RuntimeWidgetPasswordTextRead` |
| 🆓 `DumpHUDState` | The HUD state of each local player as a JSON artifact: the HUD class, the display flags, the `ShowDebug` state, the debug texts, the names of the hit boxes, the widgets the HUD references and the widgets the player controller keeps on screen. What the HUD drew (lines, text, boxes) and hit box positions cannot be read and are reported in `Limitations` |
| 🆓 `ListSubsystems` | The subsystems alive in the engine, the game instance, the play world and the local players, one row per instance (class, class path, object path, owner, status), sorted into one fixed order and cut into pages with `StartIndex` / `MaxEntries`. With `IncludeNotCreated: true` the loaded classes that have no instance under an owner are listed too. The `Engine` scope alone works without a play world. No property value is read |
| 🆓 `DumpSubsystemState` | The property values of one subsystem instance, saved as a JSON artifact. Requires `RuntimeInspect` and `SubsystemStateDump` (DefaultDenied). The response carries only a summary; the values are in the artifact. ⚠️ The artifact stays after `SubsystemStateDump` is taken away — see [Safety & Capabilities](safety.md#runtime-subsystems) |

### Game viewport UI and HUD (4)

Read the UI of a running game: which widgets are in the game viewport, where they are, whether they can be seen, and what the HUD shows. Only the game's own UI is returned — the editor's toolbars and tabs are not mixed in, which is what separates these commands from the editor-wide `DumpSlateTree`. The same commands work in PIE and in `-game` and packaged builds. All four accept [`TargetNetRole` / `TargetPIEInstance`](#choosing-which-play-world-a-runtime-command-acts-on) and are read-only: they run when the safety policy sets `ReadOnly` and while a modal dialog is open. A world with no game viewport (a server world) is refused with `NotAllowed`, and the response lists the client play worlds to retry against.

**Capabilities.** `DumpGameViewportWidgets`, `FindGameViewportWidgets` and `DumpHUDState` require `RuntimeInspect` (DefaultAllow). `DumpGameViewportWidgetTexts` requires `RuntimeWidgetTextRead` (DefaultDenied), and the plain value of a password field in its response additionally requires `RuntimeWidgetPasswordTextRead` (DefaultDenied). A missing capability is `CapabilityNotAvailable` naming it; one denied explicitly in `DeniedCapabilities` is `PolicyViolation`. See [Safety & Capabilities](safety.md#runtime-game-viewport-ui).

**To operate what you found**, take the `TypePath` and `Fingerprint` of a match to [`ClickGameViewportWidget`, `PressGameViewportUIKey` or `TypeGameViewportText`](#game-viewport-ui-input-3), then read the tree again to see the effect.

#### What a reading is

- **Rectangles** are in physical pixels from the top left corner of the game viewport, as of the last frame that was drawn. Right after an operation they can still be the old positions. In an environment that does not render (`-nullrhi`) the tree is returned without rectangles and `Limitations` says why.
- **Text.** `DumpGameViewportWidgets` with `IncludeText: true` gives the plain text only of text that is **on screen**, cut at 256 characters with control characters removed. A text is treated as not on screen when it is hidden, fully transparent through the UI opacity or colour settings (a text made transparent by a material or another non-colour means is not detected), clipped out of view (outside a scroll area or the viewport, or of size zero), or when the environment cannot render. Whether another widget **covers** a text is not judged: a covered text is given as plain text, and a note says so. An editable text reports only a length class — `Empty`, `NonEmpty` (1 to 127 characters) or `Long` (128 or more) — and whether it is a password field. A field whose password state cannot be determined counts as a password field.
- **`DumpGameViewportWidgetTexts` returns everything**, on screen or not, each entry marked with whether it is on screen. Its result is saved as an artifact, which by default is kept for 24 hours and, with the default HTTP settings, can be fetched by anyone who knows its ID. A password field's plain value is never written to the artifact; it is in the response only, as `PasswordFieldValues` (at most 16 values of at most 256 characters, the rest counted), and only with `RuntimeWidgetPasswordTextRead`. Without it, the `PasswordTextWithheld` limitation says how many fields were withheld.
- **Blueprint bindings may run.** Working out what a widget shows can call the game's Blueprint binding functions. Every widget observation says so in `Limitations`.
- **`FindGameViewportWidgets` looks at visible widgets by default** (`VisibleOnly: true`). "Visible" here means the visibility settings of the widget and its parents do not hide it; a widget with opacity 0 or outside the screen still counts, which is wider than "on screen" for text. A search that finds nothing is a success; the response says whether the list was cut (`ResultLimitReached`), whether the walk stopped early (`SearchIncomplete`) or whether the visibility filter produced the empty result, so "none exists" and "not looked at" can be told apart.
- **The open drop-downs** of the game's own menus are part of the tree.
- **Focus.** The response gives, for each local player, where the focus is: on the UI, on the game viewport itself, outside the game viewport, or nowhere.

#### Parameters

| Parameter | Commands | Meaning |
|---|---|---|
| `MaxDepth` | `DumpGameViewportWidgets`, `FindGameViewportWidgets`, `DumpGameViewportWidgetTexts` | Deepest level walked, 1 to 128 (the root is level 0). Default 64. A value out of range is refused with `InvalidParams`, not clamped |
| `MaxNodes` | the same three | Budget of nodes walked, 1 to 20000. Default 5000. Refused when out of range |
| `IncludeDebugLayer` | the same three | Also walk the debug layer below the window overlay. Default `false` |
| `IncludeCollapsed` | the same three | Also walk branches whose own visibility is `Collapsed`. Default `true` |
| `IncludeText` | `DumpGameViewportWidgets` | Include the text that is on screen (see above). Default `false` |
| `WidgetClass` | `FindGameViewportWidgets` | Class name of the UMG widget, compared ignoring case. Classes are never loaded, so a match through a parent class works only for classes that are already loaded |
| `IncludeSubclasses` | `FindGameViewportWidgets` | Also compare the parent classes of the UMG widget with `WidgetClass`. Default `true` |
| `SlateType` | `FindGameViewportWidgets` | Slate type name, compared exactly (for example `STextBlock`) |
| `WidgetName`, `WidgetNameContains` | `FindGameViewportWidgets` | Name of the UMG widget, whole or in part, ignoring case. Cannot be given together |
| `OwningPlayerIndex` | `FindGameViewportWidgets` | Local player number (0 or more) that owns the user widget the node belongs to. A player who owns none, or does not exist, gives no match — still a success |
| `VisibleOnly` | `FindGameViewportWidgets` | Match only widgets that are effectively visible. Default `true` |
| `MaxResults` | `FindGameViewportWidgets` | Most matches returned, 1 to 500. Default 50. The rest are counted, not returned |
| `WithinWidgetPath` | `FindGameViewportWidgets` | Object path of a UMG widget (at most 4096 characters) to search inside — for example the `WidgetPath` that [`UAIP.Runtime.CommonUI.DumpActivatableStacks`](#uaipruntimecommonui-) returns for a screen. Narrows the search; it is not a condition by itself. The whole game layer is walked all the same, so `MaxDepth` and `MaxNodes` count from the root of the game layer and `TypePath` stays relative to that root. A path that does not lead to a widget below the game layer is `NotFound`, naming the parameter. When the walk never reaches the widget (hidden, collapsed, a page that is not shown, or beyond the limits), the result has no match and the `ScopeRootNotTraversed` limitation. The value given is echoed back in `Result` and in the artifact |
| `RootTypePath` | `DumpGameViewportWidgetTexts` | `TypePath` of the widget whose subtree is dumped. The whole game layer is walked all the same, so `MaxDepth` and `MaxNodes` count from its root. A path that leads to no widget is `NotFound`. Default: the whole game layer |
| `PlayerIndex` | `DumpHUDState` | Number of the **local player** to inspect (0 is the first local player). Omit for every local player. A number no local player has is `NotFound` |
| `TargetNetRole`, `TargetPIEInstance` | all four | Which play world; see [Choosing which play world](#choosing-which-play-world-a-runtime-command-acts-on) |

At least one of `WidgetClass`, `SlateType`, `WidgetName`, `WidgetNameContains` and `OwningPlayerIndex` is required by `FindGameViewportWidgets`; none at all, or `WidgetName` together with `WidgetNameContains`, is `InvalidParams`. `WithinWidgetPath` does not count as a condition, so giving it alone is `InvalidParams` too.

#### Refusals

| Situation | Result |
|---|---|
| No play world, no world matching `TargetPIEInstance`, or a server world | `NotAllowed` (a server world comes with the client worlds to choose from) |
| `TargetNetRole` / `TargetPIEInstance` contradict each other or match several worlds | `InvalidParams` |
| The game layer does not exist yet (just after start) | `PreconditionFailed`; retry shortly (a scenario retries by itself) |
| The game layer cannot be located (a project replaced the standard UI layer) | `NotAllowed`. Only the standard game layer is supported |
| `PlayerIndex` of `DumpHUDState` names a player who is not there | `NotFound` |
| `WithinWidgetPath` of `FindGameViewportWidgets` does not lead to a widget below the game layer | `NotFound`, naming `WithinWidgetPath` |

#### The HUD

`DumpHUDState` returns, per local player, the HUD class and display flags, the `ShowDebug` state, the debug texts (also when the HUD is not being drawn, which the result then says), the names of the hit boxes, the widgets the HUD references (at most 64) and the widgets the player has on screen. Each of those lists has a limit, and a cut list says so. Fields the engine version cannot provide are left out with the reason. Canvas draw-batch statistics for the game viewport are added only when `EnableHUDCanvasStats=True` under `[UAIP.RuntimeObservation]` in `DefaultUAIP.ini` (read at startup, so a restart is required); otherwise `Limitations` explains how to enable it. The statistics describe the most recent frame in which a HUD was drawn into that game viewport and do not add up across frames; with split screen they cover every HUD that drew into the viewport in that frame. A game viewport that has not drawn a HUD yet has no statistics, and the result says so. See [Safety & Capabilities](safety.md#runtime-game-viewport-ui).

### Subsystems (2)

Read the subsystems of a running game: which ones are alive under which owner and — when you allow it — the values inside one of them. A subsystem lives under one of four kinds of owner: `Engine`, `GameInstance`, `World` (the play world) or `LocalPlayer`. Both commands only read: they run when the safety policy sets `ReadOnly`.

**Capabilities.** `ListSubsystems` requires `RuntimeInspect` (DefaultAllow). `DumpSubsystemState` requires `RuntimeInspect` and `SubsystemStateDump` (DefaultDenied), because the values are whatever the project stores, secrets included. A missing capability is `CapabilityNotAvailable` naming it; one denied explicitly in `DeniedCapabilities` is `PolicyViolation`. See [Safety & Capabilities](safety.md#runtime-subsystems).

**Play world.** A request for the `Engine` scope alone needs no play world and takes neither `TargetNetRole` nor `TargetPIEInstance`; its response carries no world information (net mode, PIE instance). Every other scope needs a play world, which [`TargetNetRole` / `TargetPIEInstance`](#choosing-which-play-world-a-runtime-command-acts-on) choose. With no play world such a request is `NotAllowed` — the `Engine` result is not returned in its place.

**Demo build.** Both commands are in the demo binary. `SubsystemStateDump` is not granted by the demo's default configuration; add `+AllowedCapabilities=SubsystemStateDump` yourself to use `DumpSubsystemState`.

#### What a reading is

- **A row** of `ListSubsystems` gives `Scope`, `ClassName`, `ClassPath`, `ObjectPath`, `Owner` (the parts the owner has: `PIEInstance`, `PlayerIndex`), `Status` and `IsTickableWorldSubsystem`. `Status` is `Created` (a live instance), `NonAuthoritativeClass` (a live instance whose class was replaced by a newer version through hot reload, Live Coding or a Blueprint recompile, and which still carries the renamed old class) or `NotCreated` (a loaded class with no instance under the owner; only with `IncludeNotCreated: true`).
- **Order.** Rows are sorted by scope (`Engine`, `GameInstance`, `World`, `LocalPlayer`), PIE instance, player index, status, class path and object path, so the same state always gives the same rows in the same order.
- **Pages.** The response carries the first 50 rows of the page; the JSON artifact carries the whole page. `Truncated: true` means more pages follow: call again with `NextStartIndex` as `StartIndex` (`NextStartIndex` is left out when nothing remains). `DataEntriesTruncated` says the response holds fewer rows than the page. A `StartIndex` at or beyond the total gives an empty page, which is a success.
- **Counts.** `TotalCount`, `CreatedCount`, `NonAuthoritativeCount` and `NotCreatedCount` are counted after `ClassNameContains` and before paging. `Scopes[]` has one entry per requested scope with `Scope`, `Availability` (`Available` or `Unavailable`), `Count` and, when unavailable, `Reason`.
- **`IncludeNotCreated`** compares the loaded classes with the instances under each owner. A class that is not loaded is never listed, the `Engine` scope has no `NotCreated` rows, and the reason a subsystem was not created is not returned. An owner that has not created its subsystems yet (just after a game instance or a player is added) simply has no rows. `Limitations` says which of these apply to the result.
- **`DumpSubsystemState`** selects exactly the class you name; naming a base class does not select an instance of a derived class. The response Data holds the identity (`Scope`, `ClassName`, `ClassPath`, `ObjectPath`), `Owner`, `Status`, `PropertyCount`, `IncludedCount`, `Truncated`, `StopReason` (only when the dump stopped) and `Limitations`. The properties are in the artifact only, in `Properties[]`, each with `Name`, `DeclaredBy`, `Type`, `Flags` (those of Transient, Config, BlueprintVisible, BlueprintReadOnly, Net and SaveGame that are set) and `Value`, base class first in declaration order. The properties of the common subsystem base class and editor-only properties are not listed.
- **Size.** A dump is cut at about 256 KiB: it still succeeds, with `Truncated: true` and a `StopReason` (in practice `TotalBudget`), and `PropertyCount` still counts the properties that were left out. A container keeps its first 32 elements, a string is cut at 1024 characters, a struct is expanded one level, and a reference is written as the path of what it refers to, never followed.
- **After a reload.** A subsystem left over from before a hot reload or Live Coding shows in the list as `NonAuthoritativeClass` under its renamed class name; to dump it, give that renamed name or its path. When the current class has no instance but an old one remains under the same owner, the `NotFound` result lists the renamed class names in `Candidates` (at most 16).

#### Parameters

| Parameter | Commands | Meaning |
|---|---|---|
| `Scopes` | `ListSubsystems` | One to four distinct names out of `Engine`, `GameInstance`, `World` and `LocalPlayer`, compared ignoring case. Default: all four. Only `Engine` works without a play world |
| `PlayerIndex` | both | Number of the **local player** (0 is the first local player of the game instance). For `ListSubsystems`, allowed only when `Scopes` includes `LocalPlayer`; omit it to list every local player. For `DumpSubsystemState`, only with `Scope: LocalPlayer`, and it may be omitted only while exactly one local player exists |
| `ClassNameContains` | `ListSubsystems` | Text the class name must contain, 1 to 256 characters, ignoring case. Applied while the rows are collected |
| `IncludeNotCreated` | `ListSubsystems` | Also list loaded classes that have no instance under an owner, with status `NotCreated`. Default `false`. Does not apply to the `Engine` scope |
| `StartIndex` | `ListSubsystems` | Index of the first row of the page in the sorted list, 0 or more. Default 0 |
| `MaxEntries` | `ListSubsystems` | Most rows one page holds, 1 to 4096. Default 256. A value out of range is refused with `InvalidParams`, not clamped |
| `Scope` (required) | `DumpSubsystemState` | `Engine`, `GameInstance`, `World` or `LocalPlayer`, ignoring case |
| `SubsystemClass` (required) | `DumpSubsystemState` | Class of the subsystem, 1 to 1024 characters of `A-Z a-z 0-9 _ . / : -`. A value with a slash is a class path; otherwise it is a short class name compared exactly with the object name of the class, ignoring case. A leading `U` of a C++ type name may be left off or kept. A Blueprint class needs its `_C` name. Only classes that are already loaded can be targeted |
| `TargetNetRole`, `TargetPIEInstance` | both | Which play world; see [Choosing which play world](#choosing-which-play-world-a-runtime-command-acts-on). Not accepted when only the `Engine` scope is asked for |

#### Errors

| ErrorCode | When |
|---|---|
| `InvalidParams` | A parameter is missing, of the wrong type, out of range or unknown; an unknown or repeated scope; `PlayerIndex` with a scope other than `LocalPlayer`; a play world selector with the `Engine` scope only; `TargetNetRole` / `TargetPIEInstance` contradict each other or match several worlds. For `ListSubsystems`, a request that still matches more than 65536 rows after `ClassNameContains` (drop `IncludeNotCreated` or narrow the request). For `DumpSubsystemState`, a short `SubsystemClass` that matches classes in more than one place (the class paths are in `Candidates`; repeat the request with one of them), and `Scope: LocalPlayer` without `PlayerIndex` while more than one local player exists |
| `NotAllowed` | A scope other than `Engine` was asked for and no play world is running, or none matches `TargetNetRole` / `TargetPIEInstance` |
| `NotFound` | `DumpSubsystemState`: the target does not exist; the `Reason` in the result says why (below). `ListSubsystems`: a `PlayerIndex` that no local player has (`Reason` is `PlayerNotFound`, or `NoGameInstance` when the play world has no game instance) |
| `CapabilityNotAvailable` | `RuntimeInspect`, or for `DumpSubsystemState` `SubsystemStateDump`, is not granted |
| `PolicyViolation` | The capability is denied by the safety policy |

`NotFound` carries a machine readable `Reason` in its result:

| `Reason` | Meaning |
|---|---|
| `NotInstantiated` | The class is loaded, but the scope and owner hold no instance of it. `Candidates` may name renamed instances left from before a reload |
| `ClassNotFound` | No loaded class matches the name or path. `Candidates` lists class names that exist under that scope and owner (at most 16). A class that is not loaded cannot be targeted |
| `NoGameInstance` | The play world has no game instance, so neither the game instance nor any local player exists |
| `NoLocalPlayer` | The game instance has no local player (a dedicated server, for example) and no `PlayerIndex` was given |
| `PlayerNotFound` | A `PlayerIndex` was given and no local player has it |

The same five values appear as `Reason` in a `Scopes[]` entry of `ListSubsystems` that is `Unavailable`. A `ListSubsystems` request without `PlayerIndex` does not fail for these: that scope is reported `Unavailable` with the reason, and the other scopes are returned as usual.

Every successful call saves exactly one JSON artifact; a failed call saves none.

---

## UAIP.Runtime.Execution

Test execution in PIE / Standalone.

| Command | Description |
|---|---|
| `RunFunctionalTest` | Run an `AFunctionalTest` actor in the PIE world, found by its display name (actor label), and return a JSON report |
| `RunRuntimeAutomationTest` | Run a UE Automation Test in PIE context and return a per-test report (Pass / Fail / Skipped / Error / Cancelled; see [the report contract](#automation-test-report-contract)) |
| `RunGauntletTest` | Launch a Gauntlet test as an external process via RunUAT |

> **`RunFunctionalTest`** runs the `AFunctionalTest` actor in the PIE world whose display name (actor label) equals `TestPath`, ignoring case; the whole name must match. The name is not a file path, so a name that contains `..` can be used.
>
> **`RunGauntletTest`** takes `TestName` (required), `TestParams` (optional) and `TimeoutSec` (optional, 1 to 1800, default 600). It requires the `GauntletExecution` capability. Anything outside the formats below is refused with `InvalidParams` and nothing is launched.
>
> **`TestName`** is at most 512 characters: a comma-separated list of test specs, for example `UE.BootTest`.
>
> - Each spec is a dotted name. Every part starts with an ASCII letter or `_`, followed by ASCII letters, digits or `_`.
> - A spec may be followed by one per-test parameter list in parentheses. The list may hold ASCII letters, digits and `_ . , = + - '`, but no `..` and no nested parentheses.
> - Characters such as `/`, `\`, `:`, spaces and quotes are refused.
>
> **`TestParams`** is an object with at most 32 entries, and every value is a string. The parameters reach Gauntlet in the form `-Key="Value"`.
>
> - **Key**: 1 to 128 characters matching `[A-Za-z][A-Za-z0-9_]*`. Write it without a leading `-`; `.` is not allowed.
> - **Value**: up to 1024 characters from `[A-Za-z0-9_.:/+-]`, without `..`. An empty value is allowed.
>
> Some arguments that are well-formed still change what the test or its child process does. They need the `GauntletUnrestrictedArguments` capability, which is denied by default (see [Safety & Capabilities](safety.md)). Without it the call fails with `CapabilityNotAvailable`. All matching below ignores case.
>
> - A per-test parameter list in parentheses in `TestName`.
> - A key that ends with one of: `Args`, `ExecCmds`, `Cmds`, `CommandLine`, `Cmdline`, `Platform`, `Configuration`, `Flavor`, `Dir`, `Directory`, `Path`, `Root`, `File`, `URL`.
> - A key that starts with one of: `Skip`, `Editor`, `Script`, `Automation`, `Horde`, `Telemetry`, `Device`, `P4`.
> - A key that is exactly one of: `NoCompileUAT`, `noturnkeyvariables`, `profile`, `ScriptsForProject`, `Bootstrap`, `Build`, `Builds`, `Project`, `ProjectName`, `Target`, `CustomModuleRoles`, `Sandbox`, `Clean`, `FullClean`, `cleardevices`, `Reboot`, `FirmwareVersion`, `UpdateFirmware`, `TryUpdateFirmware`, `VerifyLogin`, `test`, `tests`, `Namespaces`, `RunTest`, `TestFilter`, `TagFilter`, `Map`, `Controller`, `EnablePlugins`, `DDC`, `RHI`, `UseEditor`, `CookedEditor`, `packaged`, `staged`, `bulk`, `notbulk`, `devices`, `PerfSpec`, `PrefSpec`, `PerfModel`, `PrefModel`, `RequiredDeviceTags`, `PreferredDeviceTags`, `UndesiredDeviceTags`, `BlockedDeviceTags`, `WorkerJobID`, `LocalDeviceIndex`, `MaxLocalDevices`, `MaxVirtualDevices`, `username`, `password`, `JobDetails`, `PublishTelemetryTo`, `PerfReportServer`, `uploadreport`, `UseAgentTag`, `EnableHordeDeviceReservations`, `clientip`, `serverip`, `hostip`, `EpicApp`, `McpRegion`, `McpSubRegion`, `BuildIDOverride`, `NoMCP`, `RemoteServer`, `RequiresLogin`, `PreAssignAccount`, `ArtifactName`, `ArtifactPostfix`, `PgcFilenamePrefix`, `LocalReplay`, `MemPro`, `EditorTraces`, `ClientTraces`, `ServerTraces`, `VerboseLogCategories`, `Compile`, `NoCompile`, `CompileOnly`, `Submit`, `NoSubmit`, `NoKill`, `BuildMachine`, `UseLocalBuildStorage`, `WaitForDebugger`, `List`, `Help`, `forcestepfail`, `listargs`, `listallargs`.
> - A key that Gauntlet forwards to the child process: a key that starts with the text before the first `test` in any dot-separated part of `TestName` or of the default namespaces (`Gauntlet`, `UnrealTest`, `UnrealGame`, `UnrealEditor`), or with the whole part when it has no `test`. For `UE.BootTest` these include `UE` and `Boot`. When a part starts with `test`, every key is forwarded.
> - A value that contains `:`, or that has a `+`-separated element starting with `/` (an absolute path, a UNC path or a URL).
> - A value that starts with `-` followed by an ASCII letter, which RunUAT.bat reads as one of its own switches.
>
> Shell and batch special characters stay refused even with the capability.
>
> Parameter values and the contents of a per-test parameter list never appear in logs, errors or artifacts. A parameter list is shown as `(<redacted>)`; only parameter keys are recorded.
>
> Errors: a refused argument is `InvalidParams`; a request that needs `GauntletUnrestrictedArguments` without holding it is `CapabilityNotAvailable` (`PolicyViolation` when that capability is denied explicitly in `DeniedCapabilities`); a launch that could not start (another Gauntlet test is running, RunUAT or the shell was not found, a path RunUAT.bat cannot carry, or the process failed to start) is `ExecutionFailed`.

---

## UAIP.Runtime.Assertion

Scenario primitives — wait and assert.

| Command | Description |
|---|---|
| 🆓 `WaitSeconds` | Wait the specified number of seconds (scenario primitive) |
| 🆓 `WaitForCondition` | Poll a condition until it becomes true |
| 🆓 `AssertActorProperty` | Assert that an actor property equals an expected value |
| 🆓 `AssertWorldState` | Batch-assert multiple properties in one call |

---

## UAIP.Runtime.GAS 🧩

GameplayAbilities state inspection and runtime manipulation. Requires the `GameplayAbilities` plugin. PIE is required except where noted.

#### Inspection (8)

| Command | Description |
|---|---|
| `GetAttributeValues` 🧩 | All AttributeSet attribute values (currentValue / baseValue) for an actor |
| `GetActiveEffects` 🧩 | Active gameplay effects (Level, StackCount, remaining time) on an actor |
| `GetGrantedAbilities` 🧩 | Granted abilities (Class, IsActive, ActiveCount, InputID) on an actor |
| `GetActiveTags` 🧩 | Owned GameplayTags on an actor |
| `FindAttributeSetClasses` 🧩 | Scan PIE world actors and list `UAttributeSet` classes (MaxActors limit) |
| `ListAttributes` 🧩 | List all attribute names defined on an AttributeSet class |
| `GetAbilityAssetInfo` 🧩 | CDO-level metadata for a `UGameplayAbility` class — cost, cooldown, tags. **No PIE required** |
| `GetEffectAssetInfo` 🧩 | CDO-level metadata for a `UGameplayEffect` class — duration policy, modifiers, granted tags. **No PIE required** |

#### Manipulation (9)

All require the `RuntimeGASManipulation` capability and an active PIE session.

| Command | Description |
|---|---|
| `GrantAbility` 🧩 | Grant a GameplayAbility to an actor's AbilitySystemComponent |
| `RemoveAbility` 🧩 | Remove a previously granted GameplayAbility |
| `ClearGrantedAbilities` 🧩 | Remove every granted GameplayAbility from an actor |
| `ApplyEffect` 🧩 | Apply a GameplayEffect to an actor |
| `RemoveEffect` 🧩 | Remove all active instances of a GameplayEffect class |
| `ClearActiveEffects` 🧩 | Remove all active GameplayEffects, optionally narrowed by `TagFilter` |
| `SetAttributeValue` 🧩 | Set an attribute's base value (`AttributeName` takes either `Health` or `MyAttributeSet.Health`, the form `GetAttributeValues` reports) |
| `ResetAttributesToBase` 🧩 | Reset every attribute's current value to its base value |
| `SendGameplayEvent` 🧩 | Send a GameplayEvent with an optional magnitude to an actor |

---

## UAIP.Runtime.Input

Runtime input injection and Enhanced Input state inspection. PIE required.

| Command | Description |
|---|---|
| `InjectInputKey` | Inject a raw key press / release into the active PIE viewport |
| `InjectEnhancedInputAction` | Fire an Enhanced Input Action with a value (Bool / Axis1D / Axis2D / Axis3D) |
| `InjectLegacyAction` | Inject a legacy action mapping event |
| `InjectLegacyAxisInput` | Inject a legacy axis input |
| `InjectLegacySpeechInput` | Inject a legacy speech input |
| `AddMappingContext` | Add an Input Mapping Context to the local player |
| `RemoveMappingContext` | Remove an Input Mapping Context from the local player |
| `SetInputMode` | Set the input mode (GameOnly / UIOnly / GameAndUI) |
| `FlushInput` | Flush pressed-key state at the end of a test |
| 🆓 `DumpInputState` | Dump current input state (pressed keys, axis values, active mapping contexts with priority, the evidence behind the inferred input mode, the verdict of the injection gate, and — with `IncludeActionStates=true` — per-action trigger state). Runs no project code. See [The injection gate](#the-injection-gate) |
| 🆓 `GetEnhancedInputActionValue` | Get the current value of an Enhanced Input Action |
| `EvaluateInputGateWithProjectCode` | Evaluate the injection gate exactly as an injection would, **running the project's overrides** of the game viewport client, and report the verdict without injecting anything. `PlayerIndex`: number of the player controller (default 0). Succeeds when the gate blocks too (`Decision: "Blocked"`). Requires `RuntimeInspect` + `InputProjectCodeExecution` (DefaultDenied). Not a read-only command: refused under the read-only safety mode. Not in the Demo edition |
| `ClickGameViewportWidget` | Click a widget of the UI of a running game with the mouse: moves the pointer to the press point, confirms that the widget under it is the target or inside it, then presses and releases the button. The target is given as a UMG `WidgetPath`, a `ViewportPosition`, or a `TypePath` with its `Fingerprint` from `FindGameViewportWidgets`. Requires `RuntimeUIInputInjection`. See [Game viewport UI input](#game-viewport-ui-input-3) |
| `PressGameViewportUIKey` | Press a UI key (arrows, Tab, Enter, Space, Escape, the gamepad buttons) as the Slate user of a local player: key down, a safety re-check, key up. Without a target the key goes to the widget that has the player's focus; with one, the focus is moved to it first. Requires `RuntimeUIInputInjection` |
| `TypeGameViewportText` | Type text into an input field of the UI of a running game, one character event at a time, as the Slate user of a local player. Does not confirm the text (send Enter with `PressGameViewportUIKey`) and never sets the field's value directly. The text is not logged, returned or recorded. Requires `RuntimeUIInputInjection`; a password field also needs the `AllowRuntimePasswordFieldWrite` safety setting |

---

> **Note**: `DumpInputState` always reports `ActiveMappingContexts` (sorted by `Priority` descending, then `Path` ascending) and `EnhancedInputState` (`"Available"` / `"Unavailable"`, telling apart "queried and found none" from "could not query"). Pass `IncludeActionStates=true` to additionally get `ActionStates[]` — one entry per action reachable from the active mapping contexts, each carrying `Trigger` (one of the six `ETriggerEvent` values, including `"None"` for an action that was evaluated but is not currently firing), `ValueX`/`ValueY`/`ValueZ`, `SourceContexts[]` (which active context configured it) and `ConfiguredKeys[]` (deduplicated, sorted) — plus `ActionStatesTotalCount` and `ActionStatesTruncated` (capped at 256, sorted by `ActionPath`). Leaving `IncludeActionStates` at its default `false` keeps the call cheap; the flag is opt-in specifically because its cost scales with the number of mapped actions rather than the number of loaded mapping contexts.

### `DumpInputState` output

`DumpInputState` never runs project code. The mapping contexts are read from the data the Enhanced Input evaluation itself uses, not through the subsystem's overridable functions, so a project that overrides those functions sees the contexts input processing really applies. `PlayerIndex` is resolved the same way: from the game instance's local player list and the game state's player array, not through a function a project can override. When that data cannot be read on the running engine version, `EnhancedInputState` is `"Unavailable"` and `EnhancedInputUnavailableReason` names why (for example `"ReflectedFieldUnavailable:AppliedInputContextData"`); the field is present only then.

| Field | Meaning |
|---|---|
| `InputModeEvidence` | What the inferred input mode was derived from. `Viewport` (`IgnoreInput`, `MouseCaptureMode`, `MouseLockMode`, `HideCursorDuringCapture`; `null` with no game viewport), `PlayerController` (`IgnoreMoveInput`, `IgnoreLookInput`, `ShowMouseCursor`) and `LastSetInputModeDebugString` (development builds only) |
| `PlayerControllerPath` | Object path of the player controller `PlayerIndex` resolved to. `PlayerIndex` is a position in a numbering that shifts as players join and leave, so use the path to tell which player controller a dump describes, or whether two dumps describe the same one. Written for local and remote player controllers alike |
| `ViewportClientClass` | Class of the game viewport client |
| `ViewportClientIsVerifiedEngineClass` | `true` when that class is exactly an engine class (or one a gate contributor has verified). When `false`, the viewport values above are the engine's implementation, not the project's overrides — see `GameInputGate` |
| `GameInputGate` | The verdict the injection gate would reach: `Decision` (`Allowed` / `Blocked`), `Source` (`Bypass` / `ViewportInference` / `Contributor`), `InferredInputMode`, `ViewportReadStatus` (`Read` / `NoViewport` / `ChangedDuringProjectCode` / `OutOfRangeValue`), `ContributorInstalled`, and `Contributor` (`Name`, `Applicability`, `AllowsGameInput`, `Reason`, `Evidence`; `null` when none is installed). With an unverified viewport client class it adds `RequiresCapabilities: ["InputProjectCodeExecution"]` and `SeeCommand: "UAIP.Runtime.Input.EvaluateInputGateWithProjectCode"` (in the Demo edition `RequiresCapabilities: ["NotInThisEdition"]` and no `SeeCommand`) |
| `Limitations[]` | `{Code}`: `ViewportClientOverridesNotEvaluated`, `ViewportInputStateOutOfRange`, `ViewportChangedDuringProjectCode`, `InputModeDebugStringUnavailableInThisBuild`, `ReflectedFieldUnavailable:<field>` |

`Result` is `{PlayerIndex, InferredInputMode, GameInputGate: {Decision, Source}}`.

Arguments are checked before the play world is looked up: a negative `PlayerIndex` or a non-boolean `IncludeActionStates` is `InvalidParams`. A `PlayerIndex` no player controller has is `NotFound`, listing the indices that exist.

### The injection gate

The five injection commands (`InjectInputKey`, `InjectEnhancedInputAction`, `InjectLegacyAction`, `InjectLegacyAxisInput`, `InjectLegacySpeechInput`) refuse to inject while the game is not taking game input. The gate combines two judges, and blocks when either blocks:

- **ViewportInference** — the input mode inferred from the game viewport client and the player controller.
- **A contributor** — an optional integration that knows about a UI framework's own input routing. The [CommonUI integration](#uaipruntimecommonui-) installs one named `CommonUIRouter`; it blocks game input while the CommonUI action router is in menu mode, for example. At most one contributor is installed.

An injection reads the viewport client the way real input does, including the project's overrides of `IgnoreInput`, `GetMouseCaptureMode` and `HideCursorDuringCapture`. `DumpInputState` reads only the engine's implementation, so for a project viewport client that overrides these its `GameInputGate` can differ from what an injection decides; `EvaluateInputGateWithProjectCode` reports the injection's own verdict. If the project code run during the read replaces the player controller, local player, world or viewport client, the gate blocks with `ViewportReadStatus: "ChangedDuringProjectCode"`.

A refusal is `NotAllowed` and its message names the judge that blocked (`ViewportInference` or the contributor's name) with its reason. The `PolicyViolation` returned for `BypassInputMode=true` without the bypass safety setting is unchanged. Every injection's audit record carries `GateSource`, `GateContributorReason` and `GateViewportReadStatus`.

The gate does not model everything: a key a person presses can be consumed by a UI action binding (CommonUI's, for example) before it reaches game input, and the gate does not reproduce that. In a build with the console enabled and no viewport console object, the gate is stricter than the engine.

`EvaluateInputGateWithProjectCode` does not wait for a safe point in the frame — it evaluates where an injection evaluates, so it returns what an injection would get. Because it runs project code it is refused with `PolicyViolation` in read-only mode and with `NotAllowed` while a modal dialog is open or the engine tick is starved.

### Game viewport UI input (3)

Operate the UI of a running game by the same input path a person uses. The pointer moves over the target, the press goes through Slate's input routing, and the focus moves the way the game's own UI moves it; nothing calls a button's handler and nothing sets a field's value directly, so the game's input handling (CommonUI, a project's own input processing) takes part. The operating system's cursor does not move, and Unreal Editor may be in the background. Works in PIE and in `-game` and packaged builds (a packaged build needs `-uaip-http-enable` to use HTTP). All three accept [`TargetNetRole` / `TargetPIEInstance`](#choosing-which-play-world-a-runtime-command-acts-on) and send only into the game viewport of the world they select.

**Capabilities.** All three require `RuntimeUIInputInjection` (DefaultDenied). It is **separate from `RuntimeInputInjection`**: allowing the latter does not let you operate the UI. In PIE inside the editor, a key that the editor binds to its own PIE shortcuts (by default Escape, which stops PIE) additionally requires `RuntimeUIEditorReservedKeyInput` (DefaultDenied); Standalone and packaged builds are not restricted. The capability is checked when the request is accepted and again just before the input is sent. See [Safety & Capabilities](safety.md#runtime-game-viewport-ui).

#### Naming the target

`ClickGameViewportWidget` needs exactly one target; `PressGameViewportUIKey` and `TypeGameViewportText` may omit it (the input then goes to whatever widget the player's focus is on).

| Parameter | Meaning |
|---|---|
| `WidgetPath` | Object path of a UMG widget that is on screen. The most reliable way when the widget has a name |
| `ViewportPosition` | `{X, Y}` in physical pixels from the top left corner of the game viewport. The target is the widget in front at that point |
| `TypePath` + `Fingerprint` | The values `FindGameViewportWidgets` returned for a match. If the widget at `TypePath` is no longer the one the fingerprint describes (the screen was rebuilt), the command is refused with `Conflict` — search again. Widgets of the same type with no name and no tag cannot always be told apart after a swap |
| `LocalX` + `LocalY` | `ClickGameViewportWidget` only. Where to press, as an offset from the top left of the target's rectangle; both or neither, inside the rectangle, not with `ViewportPosition`. Default: the centre |
| `MouseButton` | `ClickGameViewportWidget` only. `Left` (default) or `Right` |
| `Key` (required) | `PressGameViewportUIKey` only. One of the UI allow list: the arrow keys, `Tab`, `Enter`, `SpaceBar`, `Escape`, the gamepad directional pad, face buttons, shoulders, triggers and special buttons, and `Virtual_Gamepad_Accept` / `Virtual_Gamepad_Back`. Any other key, every modifier key included, is refused with the allowed names in `AllowedKeys`. No modifier key is ever added |
| `Text` (required) | `TypeGameViewportText` only. 1 to 1024 code points (a combined emoji or flag is several), with no control characters — a line break cannot be typed |
| `PlayerIndex` | `PressGameViewportUIKey` and `TypeGameViewportText`. Number of the **local player** to act as; default 0 |

**`PlayerIndex` is not the player controller number.** The existing input commands (`InjectInputKey` and the others) number the **player controllers** of the world; these two number the **local players** of the game instance (0 is the first). A negative number is `InvalidParams`; a number no local player has is `NotFound`. A click is always sent as the user that owns the mouse (normally the first local player), so it can press the UI of another local player's screen; the response notes it.

#### How an operation goes

1. **Click.** The pointer is moved onto the press point and the command checks that the widget directly under it is the target or inside it — if not, nothing is pressed (`ExecutionFailed`, naming the widget in front). Then the button is pressed and released.
2. **Key.** With a target, the focus is moved there first and the move is checked. The key goes down, a safety re-check runs, then it goes up. `ReachedGameViewport` tells whether the UI let the key through to the game: `true`, `false` or `Unknown`. With `false`, `ReachedGameViewportReason` is `HandledBeforeGameViewport`: the focused widget, or a widget that contains it, handled the key, so nothing that reads input at the game viewport saw it (the player controller's input, and input actions the game binds through the viewport client). The command still succeeds — check `FocusAfter` and whether that screen binds the key itself. `Unknown` (the key may have gone to another viewport) carries no reason.
3. **Text.** With a target, the focus is moved to it first. Characters are sent one at a time as a person typing would; no IME composition is sent. Before each character the command checks that the focus is still on the same field and that its password state has not changed, and stops if not. Whether the field is a password field is judged at the time of sending; one that cannot be judged counts as a password field.

The response is sent after the input has been delivered. It reports what was hit (`HitWidget`, `HitWidgetIsTarget`), where the focus is afterwards (`FocusAfter`), whether the input reached the game (`ReachedGameViewport`), whether a modal window opened (`ModalOpened`) and `Limitations`; `TypeGameViewportText` reports `CharactersDelivered`, the reason it stopped, and the length class of the field before and after (`Empty`, `NonEmpty`, `Long`) — never the text.

#### What `Success` means

`Success` means **the input was delivered by the path a person's input takes**. It does not promise that the button's handler ran or that the screen changed: input on the way (CommonUI, a project's own handling, the editor's input monitoring) may consume or change it, as it may a person's. Read the tree again (`DumpGameViewportWidgets`) to confirm the effect. An input the UI did not handle can become game input (movement, attack) — as with a person — and every operation's response says so. Between accepting a request and sending it the command checks that the caller is still waiting and that the world, session, capability and target are unchanged; a caller that has given up gets nothing sent, which reduces double presses but cannot rule out a timeout that lands just after the check.

#### Refusals

Nothing is sent in any of these unless stated.

| Situation | Result |
|---|---|
| No play world, a server world, or no world matching the selector | `NotAllowed` (a server world comes with the client worlds to choose from). A contradictory or ambiguous selector is `InvalidParams`. In a dedicated server process these commands are not available at all, and the refusal names the reason |
| Game layer does not exist yet | `PreconditionFailed`; retry. A layer that cannot be located: `NotAllowed` |
| Capability not granted | `CapabilityNotAvailable` naming it (for an editor-reserved key, also the shortcut that matched, with a hint to use the gamepad Back button). Denied explicitly: `PolicyViolation` |
| The game viewport holds the mouse (input mode is game only) for a click; the focus is on the game viewport itself for a key or text with no target; a drag is in progress; any modal window or a menu outside the game viewport is open | `NotAllowed`, with the focus and mouse capture state. The input mode is never changed for you — use `SetInputMode`. A drop-down that is part of the game's own UI does not block |
| The window that hosts the game is minimized or hidden (`Reason: HostWindowUnavailable`; see [Capture refusals](#capture-refusals)) | `NotAllowed`. The host window not existing yet is `PreconditionFailed` |
| Target missing or not added to the viewport | `NotFound` |
| The screen was rebuilt after the search | `Conflict` — search again |
| Target hidden or disabled | `NotAllowed` |
| Another widget is in front of the target (also the editor's viewport toolbar or messages in PIE) | `ExecutionFailed` naming the widget in front; hover reactions such as tooltips have already happened |
| A coordinate target whose front-most widget belongs to the editor or another window; a key or text whose focus is outside the game viewport | `NotAllowed` |
| A key or text with no target when no widget of that player has focus at all | `NotFound` |
| The focus could not be moved to the target | `NotAllowed`, with the focus afterwards |
| The state changed between press and release (the screen, the world or a modal changed) | `NotAllowed` with `PartialDelivery` (`DownOnly` for a click, `KeyDownOnly` for a key). The release is not sent and the pressed state is cleared |
| The press itself opened a modal window | **Success** with `ModalOpened` and `PartialDelivery`; the release is not sent |
| Text into a password field, or a field whose password state cannot be determined, without `AllowRuntimePasswordFieldWrite` | `PolicyViolation`, before the focus is moved. The message says which of the two it was |
| Text into something that is not an input field, or is read-only or disabled | `NotAllowed` |
| Text interrupted (focus moved, password state changed, the application state changed) | `NotAllowed` with the number of characters already sent in `CharactersDelivered` when at least one was; when none was sent yet, the refusal of the matching situation above. A character that would be split (an emoji sent as two halves) reports it. If a character opens a modal window the call **succeeds** with `ModalOpened` and the count, and the field's length class after is not reported |
| `PlayerIndex` names no local player | `NotFound` |
| A key outside the allow list, an empty or too long text, a control character, a position outside the target, one of `LocalX` / `LocalY` alone, `LocalX` / `LocalY` with `ViewportPosition`, no target or more than one for a click, a `TypePath` without a `Fingerprint`, a negative `PlayerIndex` | `InvalidParams` naming the field and the allowed range |
| Unreal Engine began shutting down | `ExecutionFailed` (cancelled by shutdown) |

A scenario retries a step by itself only after `ExecutionFailed` or `PreconditionFailed`. The partially delivered cases return `NotAllowed` for that reason: a retry would otherwise press twice or repeat characters.

When a key was pressed and the game saw it go down before the press stopped, the game-side pressed state of that player is cleared too, which also clears keys the person at the keyboard is physically holding. If it cannot be told whether the game saw the key, or the player is gone, nothing is cleared and the response notes it.

#### Things to know

- **Split screen.** The tree and the focus report the screen area of each local player. Keys and text go as the player you name; clicks always go as the mouse user.
- **Several PIE instances in one process.** The input is sent only into the selected world's viewport, but part of the input path (CommonUI's global handling) is shared across PIE instances. With "route gamepad to second window" on, a gamepad key can reach another PIE; `ReachedGameViewport` is then `Unknown`. Two game menus open in different PIE instances at once may not be told apart.
- **No rendering (`-nullrhi`).** The tree has no rectangles and operations are refused with `NotAllowed` (waiting does not help); right after start, before anything has been drawn, it is `PreconditionFailed`.
- **Sensitive values.** `DescribeCommand` lists the parameters that are masked in notifications and audit records (`SensitiveParams`; `Text` for `TypeGameViewportText`) and the response fields masked likewise (`SensitiveResponseData`; the password field values of `DumpGameViewportWidgetTexts`). Subscribers and audit records receive `"<redacted>"`, without even the length; if the parameters to mask cannot be determined, the whole parameter set is masked, and if the response fields to mask cannot be determined, the whole response `Data` is masked, keeping its top-level field names. In a scenario, a step that embeds such a value taken from an earlier step's response is masked in full, and so are the steps it is passed on to; a file the target command saves as its result is not covered. See [Sensitive values and where they are masked](#sensitive-values-and-where-they-are-masked).
- **The CLI keeps what you pass it.** A text given on the command line (`-uaip-request=`) or in a request file (`-uaip-request-file=`), and a response file, stays there: UAIP does not mask a file or command line that the caller chose. Keep secrets out of those, or use HTTP / MCP.

## UAIP.Runtime.Niagara 🧩

Runtime inspection and parameter override for Niagara components in PIE. Requires `Niagara` plugin.

### Native (4)

| Command | Description |
|---|---|
| `GetUserVariables` 🧩 | Get user-exposed variables on a Niagara System Component |
| `GetVariable` 🧩 | Get a specific user variable value |
| `SetVariable` 🧩 | Set a user variable value at runtime |
| `SetSystem` 🧩 | Replace the Niagara System asset on a component at runtime |

### Toolset bridges (4) 🧩

Provider: `Toolset.Runtime.Niagara.*`. Requires UE 5.8+ and `NiagaraToolsets`. Mirrors the native commands above.

---

## UAIP.Runtime.LiveLink

LiveLink Source / Subject observation, client-state control, and UAIP-owned synthetic Sources. Works in the editor and at runtime alike, and does not require PIE.

**No plugin requirement, and no 🧩.** The client interface these commands use ships in the engine's own always-present `LiveLinkInterface` module, not in the optional `LiveLink` plugin, so the commands are **always registered**. When no LiveLink client is present — the `LiveLink` plugin disabled — they report `Available: false` in `uaip_list_commands` / `uaip_describe_command` rather than vanishing, and `ListLiveLinkSources` answers `LiveLinkAvailable`, so **one call tells you whether LiveLink is usable in this environment**. `uaip_describe_command` additionally reports `UnavailableDetail: "ExecutionEnvironment"` for all 14 commands in this domain in that state — nothing here is compiled out; what's missing is the running process's `ILiveLinkClient` — see [UnavailableDetail](#unavailabledetail--the-eight-reasons-behind-a-handlerunavailable-refusal). Preset, connection and recording commands live in [UAIP.Editor.LiveLink](#uaipeditorlivelink-), which does require plugins.

**Naming a Subject.** Two different Sources may publish a Subject of the same name. Reads accept a bare `SubjectName` and resolve it, but a name matching more than one is refused with `InvalidParams` listing every match under `Candidates` — never silently resolved to one of them. Mutations take the full `SubjectKey` (`SourceGuid` + `SubjectName`) instead. The three places where the engine itself only accepts a name — a virtual Subject's member list, `StartLiveLinkRecording`'s targets, and `SetLiveLinkComponentSubject` — resolve against whichever Subject with that name is presently *enabled*, refuse an ambiguous one, and report back what they resolved to.

**Mutual exclusion.** The mutating commands below are refused while a preset apply or a recording is in flight (see [UAIP.Editor.LiveLink](#uaipeditorlivelink-)). `PushLiveLinkSyntheticFrame` is the deliberate exception and is never refused for that reason; reads never are either.

### Observation (6) — requires `RuntimeInspect`

| Command | Description |
|---|---|
| `ListLiveLinkSources` | Every Source registered with the client, real and virtual-subject container alike — `Guid`, human-readable `Type`, `IsStillValid`, `IsVirtual`, `FactoryClassPath`. `LiveLinkAvailable` reports whether a client implementation is registered at all, which is what makes this the one call to start from. ⚠️ `IncludeSensitiveDetails: true` adds `ConnectionString` / `StatusText` / `MachineName` — free-form fields a Source controls that can carry host addresses or credentials — and requires `LiveLinkSourceInspectSensitive`; every response echoes the name under `SensitiveDetailsRequiredCapability` whether or not it was asked for |
| `ListLiveLinkSubjects` | Every Subject the client knows about, filtered by `IncludeDisabled` / `IncludeVirtual`. Each entry carries `SubjectKey`, `RoleClassPath`, `EnabledConfigured` (the persistent configured flag) and `IsSubjectValid`. `State` is included only when `EnabledConfigured` is true, because the engine's own state query is keyed by name and answers for whichever same-named Subject is enabled — reporting it for a disabled row would describe a different Subject |
| `GetLiveLinkSubjectFrame` | Evaluate a Subject's current static and frame data for a role and return both as role-structured JSON (`SubjectKey`, `RoleClassPath`, `StaticData`, `FrameData`, `CapturedAt`). Narrow by `SourceGuid` to evaluate against that exact Source; omit it to evaluate by name, which answers for whichever same-named Subject is enabled. `Role` defaults to the Subject's own. Engine-shipped roles are decoded field by field; a project- or plugin-defined role falls back to the fields common to every role (curve values, times, timecode) — `ListLiveLinkRoles` says which is which |
| `GetLiveLinkSubjectStatus` | A Subject's connection status: `State` (only when the resolved Subject is the enabled one sharing its name, for the reason above), `IsSubjectTimeSynchronized`, `SceneTime` (the most recent frame's, when any frame has arrived), `FrameArrivalTimes` and `CapturedAt`. ⚠️ **No frame rate is computed.** `FrameArrivalTimes` is the raw arrival history exactly as the engine exposes it — the engine documents it as debugging-only and offers no frame-rate query — so any rate is yours to derive |
| `GetLiveLinkSubjectSettings` | A Subject's `ULiveLinkSubjectSettings`-level configuration, currently just `InterpolationProcessorClassPath` — the class path of the `ULiveLinkFrameInterpolationProcessor` configured on the Subject, or `null` when none is set. Resolves a bare `SubjectName` the same way as `GetLiveLinkSubjectStatus` (optionally narrowed by `SourceGuid`; `InvalidParams` listing `Candidates` when the name is ambiguous, never silently resolved to one of them). **`null` is also the answer for a Subject that has no settings object to configure in the first place** — a virtual Subject, for instance — so it does not by itself distinguish "configurable but unset" from "not configurable at all"; attempting `SetLiveLinkSubjectInterpolationProcessor` against the same Subject is what tells the two apart (it answers `NotAllowed` for the latter) |
| `ListLiveLinkRoles` | Every registered `ULiveLinkRole` subclass — `RoleClassPath`, `DisplayName`, `StaticDataStructPath`, `FrameDataStructPath`, and `IsFullySupported` (whether frames of that role are decoded field by field or only through the common base fields). Also lists every **concrete** `ULiveLinkVirtualSubject` subclass under `VirtualSubjectClasses`; `AddLiveLinkVirtualSubject` requires one of these, since the abstract base cannot be instantiated |

### Client state (5)

| Command | Description |
|---|---|
| `SetLiveLinkSubjectEnabled` | Set a Subject's configured enabled flag, addressed by `SubjectKey`. **Only one Subject sharing a name may be enabled at a time**, so enabling one can implicitly disable another; that Subject's key comes back under `ImplicitlyDisabledSubjectKey` (`null` when none was affected). `EnabledConfigured` reflects the change immediately, while `EnabledThisFrame` — the snapshot the client evaluates against — only picks it up on the client's next tick, which is why the two are reported separately. Requires `LiveLinkClientControl` |
| `RemoveLiveLinkSource` | ⚠️ **Cannot be undone.** Remove a Source by `Guid`, taking every Subject it owns with it; a removed Source cannot be recreated under the same `Guid`. When the Source is one UAIP created, its ledger entry is dropped too (`WasSyntheticSource`). `NotFound` for a `SourceGuid` that names no registered Source. Requires `LiveLinkSourceDelete` — held apart from `LiveLinkClientControl` precisely because it is the one irreversible mutation in this group |
| `AddLiveLinkVirtualSubject` | Add a virtual Subject — a combination of one or more existing Subjects — to the shared UAIP virtual-subject container Source. `VirtualSubjectClass` must be a concrete `ULiveLinkVirtualSubject` subclass path (`ListLiveLinkRoles` lists them). Each `MemberSubjectNames` entry resolves against whichever same-named Subject is enabled, `NotFound` when none matches and `InvalidParams` listing candidates when more than one does; the resolved keys come back under `Members`. Up to 64 members, names up to 256 characters. **Virtual Subjects are real client configuration and survive the session that made them** — remove them explicitly. Requires `LiveLinkClientControl` |
| `RemoveLiveLinkVirtualSubject` | Remove a virtual Subject by `SubjectKey`. Idempotent: a key that names no virtual Subject succeeds with `WasPresent: false`. When the container Source is left holding none, the Source is removed too (`WasContainerSourceRemoved`) — **unless that would leave the client with no virtual Source at all**, which the editor's LiveLink panel assumes exists. `InvalidParams` when `SubjectKey` names a real Subject; use `RemoveLiveLinkSource` for those. Requires `LiveLinkClientControl` |
| `SetLiveLinkSubjectInterpolationProcessor` | Set or clear the `ULiveLinkFrameInterpolationProcessor` configured on a Subject's settings, addressed by the full `SubjectKey` (`SourceGuid` + `SubjectName` — no bare-name resolution here). **Omitting `InterpolationProcessorClassPath` clears interpolation; an empty string is refused with `InvalidParams` rather than treated the same as omission**, so a class path built from an empty variable cannot silently clear the setting instead of failing loudly. When a path is given, the class is resolved with `FindObject` only (never loaded) and must be a concrete, non-abstract subclass of `ULiveLinkFrameInterpolationProcessor`, up to 512 characters — anything else is `InvalidParams`. `NotFound` when `SubjectKey` names no registered Subject; `NotAllowed` when the resolved Subject has no settings object to configure (see `GetLiveLinkSubjectSettings` above). Refused, with no change made, while a preset apply or a recording is in flight. Requires `LiveLinkClientControl` |

### Synthetic Sources (3)

A synthetic Source is a minimal Source UAIP registers itself, so an agent can stand a Subject up **entirely in process — no capture hardware, no LiveLink Hub, no network** — and verify the whole LiveLink path end to end. Synthetic Sources are owned by the session that created them and are cleaned up when it ends; nothing else in this domain is.

| Command | Description |
|---|---|
| `CreateLiveLinkSyntheticSource` | Register a UAIP-owned Source with the client and return its `SourceGuid`. The Source is recorded against the requesting session: **only that session may push into it or remove it**. `TooManyRequests` once the session holds the maximum number of synthetic Sources. Requires `LiveLinkSyntheticSource` |
| `PushLiveLinkSyntheticFrame` | Push `StaticData` and `FrameData` for one role into a synthetic Source this session created, creating the named Subject on first use. ⚠️ **Both pushes only enqueue** — the client drains the queue on its own next tick — so `IsSubjectValidImmediately` reads `false` on nearly every successful call. Wait at least one more client tick (e.g. `WaitForCondition`) before evaluating the Subject. `NotAllowed` when the `SourceGuid` was not created by this session; pushing to a Source that does not exist is discarded silently by the engine, which is why the response reports whether the Subject actually stood up. Bounded per session by distinct Subject count and push rate (`TooManyRequests`), and per payload by array length, name length and non-finite (`NaN` / `Inf`) numbers (`InvalidParams`). Never refused by an in-flight preset apply or recording. Requires `LiveLinkFrameInjection` — deliberately separate from `LiveLinkSyntheticSource`, so a session can be allowed to inject test data without being allowed to create or remove Sources |
| `RemoveLiveLinkSyntheticSource` | Remove a synthetic Source this session created. Idempotent: a `SourceGuid` never registered, or already removed, succeeds with `Removed: false`. `NotAllowed` when it belongs to a different session. Requires `LiveLinkSyntheticSource` |

---

## UAIP.Runtime.Insights.Trace

Unreal Insights trace capture control. A trace is always written to a file under `Saved/Profiling/UAIP/` — **no command in this module can send a trace to a network destination**. A trace UAIP did not start is never modified: `GetTraceStatus` reports that something else is recording, and every control command except `StopTrace` (which refuses it explicitly) leaves it alone.

The three read-only commands require `RuntimeInsightsInspect` (DefaultAllow). The eight control commands require `RuntimeInsightsControl` (DefaultDenied). Attaching the captured `.utrace` file additionally requires `RuntimeInsightsAttachTraceFile` (DefaultDenied) — see [Safety & Capabilities](safety.md#runtime-insights-trace-capture).

Trace recording is independent of the PIE lifecycle: starting or stopping PIE neither starts nor stops a trace, and a trace keeps recording across PIE sessions.

### Read-only (3)

| Command | Description |
|---|---|
| 🆓 `ListTraceChannels` | List every trace channel this build knows about — description, whether it is currently enabled, whether it can still be toggled, and what it can disclose. Also lists the engine's channel presets, each expanded into its channels and their disclosure classes. Most engine presets include the log channel, so check the expanded classes before passing a preset to `StartTrace` |
| 🆓 `GetTraceStatus` | Report whether the engine is recording, whether recording is suspended, and whether the running trace is one UAIP started. For a UAIP-started trace also reports its label, file name, channels, disclosure classes, elapsed time, file size and self-stop limits. For a trace UAIP did not start, only the kind of activity is reported — the destination, channel set, elapsed time and size are withheld. Elapsed time and size are refreshed once per monitoring interval and can be up to one interval old |
| 🆓 `ListTraceFiles` | List the trace files UAIP captured, newest first, with label, size and the UTC timestamp encoded into the name (`MaxCount` default 50, max 500). A `FileName` from this listing is what `AnalyzeTrace` accepts. When the safety policy enables external trace analysis, `.utrace` files in the configured external directory are listed as well with `Source: External`. Listing never deletes anything — rotation happens when a trace starts |

### Trace control (8)

| Command | Description |
|---|---|
| `StartTrace` | Start recording into UAIP's own trace directory with the given channels or channel presets enabled, and return the file name being written to. `Channels` is required; `Label`, `MaxDurationSeconds` (default 300, range 1–3600) and `MaxFileSizeMB` (default 448, range 1–4096) are optional. A trace UAIP already started is never restarted — the request only adds channels and reports `AlreadyRunning` / `LimitsIgnored`. Rejected with `PolicyViolation` when the *effective* channel set (already enabled ∪ requested) records log text and `AllowLogDump` is false; no channel is ever turned off to make a request pass. When that same set carries something the policy will not let the raw file be handed over for, `Warnings` reports `AttachDisabledByPolicy` naming the channels and the setting, so a capture that is meant to be taken away is not started for nothing. Both limits are checked once per second, so the size limit is not a strict ceiling — the default leaves room for that overshoot so a trace recorded without a size limit stays within the 512 MB `AnalyzeTrace` accepts, and a larger limit is reported back as a `TraceTooLargeToAnalyze` warning |
| `StopTrace` | Stop the trace UAIP started and, when `AttachTraceFile` is true, hand the captured `.utrace` over as an artifact. Stopping always succeeds — nothing recording is a successful no-op, a second stop issued right after a first one is the same no-op even though the engine still reports the connection as live while it tears the trace down, and a file that cannot be handed over is skipped with an `AttachSkippedReason` while the stop itself still succeeds. A trace UAIP did not start is never stopped (`NotAllowed`). ⚠️ Attaching the file always discloses the process command line whatever the channel set was. Attaching is refused for a channel set that was mutated while recording, for an unclassified channel, and for a file larger than 64 MB; a set carrying log text needs `AllowLogDump`, and one carrying host paths, screen content or network addresses needs `AllowDisclosingTraceAttachment` (in the editor both are normally required, because the engine enables the log and screenshot channels by itself). Stopping does not close the captured file on its own — the engine's trace writer finishes that on its own thread a moment later — so a request that asks for the file waits up to three seconds for it and reports `AttachSkippedReason: "TraceFileStillOpen"` if it is still being written by then, which is worth asking for again in a moment. A request that did not ask for the file never waits |
| `PauseTrace` | Suspend recording of the trace this module started without stopping it. Idempotent (`WasPaused: false` when already paused), a no-op success when nothing UAIP started is running, and `NotAllowed` for a trace UAIP did not start. The channel monitor keeps running while paused, and the duration limit only counts seconds actually spent recording |
| `ResumeTrace` | Restore recording after `PauseTrace`. Idempotent (`WasResumed: false` when not paused) and `NotAllowed` for a trace UAIP did not start. The engine has a known defect where resuming can fail to restore a channel whose name does not end in `Channel`; such a channel is reported in `Warnings` as `ChannelNotRestoredAfterResume` so it can be re-enabled with `SetTraceChannels` |
| `SetTraceChannels` | Enable and disable channels on the trace this module started while it keeps recording. At least one of `EnableChannels` / `DisableChannels` must be non-empty. `NotAllowed` when no trace is running or the running trace was not started by UAIP, because channel state outlives the trace. The request is judged by the channel set it would leave in effect, so turning a disclosing channel off is never itself rejected. ⚠️ Using this command marks the trace's channel set as externally mutated, which makes `StopTrace` refuse to attach the file |
| `AddTraceBookmark` | Write a point-in-time bookmark (`Text`) into the trace that is recording right now. When the bookmark channel is disabled — which includes every moment nothing is recording — nothing is written and the command still succeeds with `Written: false`. Rejected with `PolicyViolation` when `AllowLogDump` is false, because the text is read back under the same policy that gates log text. Absolute paths in the text are replaced with portable placeholders |
| `BeginTraceRegion` | Open a named span (`Name`, optional `Category`) in the running trace and return the `RegionId` that closes it. Regions are matched by id, never by name, so nested regions and same-named regions stay apart. A `RegionId` is returned even when the region channel is disabled (`Written: false`). Any span still open is closed automatically when the trace stops or the module shuts down. Gated by `AllowLogDump` the same way `AddTraceBookmark` is |
| `EndTraceRegion` | Close the region `BeginTraceRegion` opened, matched by `RegionId` (`NotFound` for an id that names no open region, including one already closed by the automatic sweep). `DurationSeconds` is measured in-process and is reported even when the region channel was disabled. Never rejected by the log dump policy — it carries no text of its own |

---

## UAIP.Runtime.Insights.Analysis

Offline analysis of a captured `.utrace` file. This provider is only registered in builds where trace analysis is supported; elsewhere (including the demo build) the commands are absent and return `CommandNotFound` rather than failing on every call.

All three commands require `RuntimeInsightsAnalyze` (DefaultDenied) — including the status command, because the progress of an analysis is of no use to a caller that may not analyse a trace.

Analysis is asynchronous: call `AnalyzeTrace` to get an `AnalysisId`, poll `GetTraceAnalysisStatus` until `State` is `Completed`, then read `GetTraceAnalysisResult`. Only one run is ever under way — a request that arrives while another run is parsing or extracting is rejected with `TooManyRequests`, and the error message names the `AnalysisId` of the run holding the slot, so it can be watched through `GetTraceAnalysisStatus` instead of blind-polling. There is no way to cancel a run. A finished run does not hold the slot: it stays readable for its time to live and does not stop the next run from starting.

A run also belongs to the session that started it. `GetTraceAnalysisStatus` and `GetTraceAnalysisResult` find an `AnalysisId` only when they are called with the same `SessionId` that `AnalyzeTrace` was called with; from any other session that identifier reads as `NotFound`. That is deliberately the same answer as for an identifier that never existed — an unknown `AnalysisId`, one whose time to live has run out, and one owned by another session are not told apart, so neither command can be used to find out whether some other caller's identifier exists. Keep using one `SessionId` and nothing about how you call these commands changes. Omitting `SessionId` does break it: the transport then makes a fresh anonymous session per call, so a run started that way can never be looked up again. This is the same requirement the asset audit job commands carry.

| Command | Description |
|---|---|
| `AnalyzeTrace` | Start analysing a trace file and return the `AnalysisId`. **The run is bound to the `SessionId` of this call**, and only that same `SessionId` can poll or read it afterwards. `FileName` must be a name `ListTraceFiles` reported (not a path); a trace captured outside UAIP is analysed by passing `ExternalTracePath` instead, which requires the external-analysis policy. Optional `Sections`, `StartTimeSeconds` / `EndTimeSeconds`, `TopN` (default 32), `MaxSeries` (default 256), `MaxSamplesPerSeries` (default 1024), `NameFilter`, `HitchThresholdMs` (default 33.3). A trace larger than 512 MB is rejected. Each requested section is written out as its own JSON artifact as it finishes, which is why the command is not read-only. A section whose channel was not recorded, or whose content the safety policy withholds, is reported as unavailable with a reason rather than failing the run |
| `GetTraceAnalysisStatus` | Report how far one run has got — `Running` (parsing), `Extracting`, `Completed` or `Failed` — with elapsed time, `CompletedSections`, `AvailableSections` and `UnavailableSections` (each with its reason). `FailureReason` is one of a fixed set of values and is only meaningful once `State` is `Failed`; what the analysis engine itself reported goes to the output log instead, because those messages can carry absolute paths. **Requires the same `SessionId`** used to start the run; an unknown, expired, or other-session `AnalysisId` all return `NotFound` without distinguishing which case it is. Read-only |
| `GetTraceAnalysisResult` | Return the artifacts a finished run produced, one per section, with `TotalCount` / `ReturnedCount` per section and `Truncated` when any of them hit a limit. Only a run whose `State` is `Completed` can be read, and **only with the same `SessionId`** that started it — from any other session the `AnalysisId` returns `NotFound`, the same as an unknown one. The command hands back references and reads nothing, so pick only the sections worth fetching; a section the original `AnalyzeTrace` call did not request is rejected rather than analysed now. Reading a result restarts the time the run is kept for (15 minutes per read, one hour absolute) |

Section names accepted by `Sections`: `Frames`, `Counters`, `Timers`, `Threads`, `StackSamples`, `LoadTime`, `Memory`, `Allocations`, `Tasks`, `FileActivity`, `NetProfiler`, `CsvProfiler`, `ContextSwitches`, `CookProfiler`, `Bookmarks`, `Regions`, `Diagnostics`, `Channels`, `Log`, `Screenshots`, and `Objects` (UE 5.8+ only — the underlying provider does not exist on UE 5.7).

Three per-section details worth knowing before reading a result:

- **`Frames`** counts only frames that both began and ended. A capture stops in the middle of a frame, so the last frame of each frame type is almost always still open and has no duration to report; such a frame is left out of the statistics and out of `TotalCount` alike. `TotalCount` and `ReturnedCount` therefore differ only when a time window was requested, and this section never truncates.
- **`Screenshots`** reports metadata only — the identifier, name, time, width and height of each screenshot, alongside `ImageDataIncluded: false` — and never the encoded image bytes. No image ever arrives from it, so there is nothing to wait for beyond that metadata.
- **`Diagnostics`** omits its `EngineVersion` key on UE 5.7. That version's trace format does not carry an engine version at all, so the key is left out rather than reported as an empty string, which would be indistinguishable from a capture that genuinely recorded none.

---

## UAIP.Runtime.SaveGame

List, inspect, read, back up, prepare, delete and restore the game's save slots — the `USaveGame` objects the engine's save game system stores under a slot name. Built for tests that have to start from a particular save, or from no save at all, and put things back afterwards. Works in the editor with or without PIE, and in `-game` and packaged builds; no plugin requirement.

**Nothing is ever loaded.** Reading a slot never loads a class or an asset: the SaveGame class a slot names, and every object a hard reference in it points at, must already be loaded in the process. A C++ class is normally loaded whenever the project is open in the editor; a Blueprint class may not be until its asset has been opened. Reading or writing a slot also never changes the state of a running game — UAIP reads and writes slots, and how a game applies a slot it loads is up to the game.

**Capabilities.** `ListSaveGameSlots`, `GetSaveGameInfo` and `ListSaveGameSnapshots` require `RuntimeSaveGameInspect` (DefaultAllow). `DumpSaveGame` requires `RuntimeSaveGameContentRead` (DefaultDenied). Every command that changes a slot or a snapshot requires `RuntimeSaveGameWrite` (DefaultDenied) — `SnapshotSaveGame` included, because it copies the raw bytes of a slot into the UAIP working directory. Two arguments add a capability on top: `WriteSaveGame` with `BaseSlotName` also requires `RuntimeSaveGameContentRead`, and `SkipValidation: true` on `CopySaveGameSlot` / `RestoreSaveGame` requires `RuntimeSaveGameUnvalidatedWrite` (DefaultDenied). A missing one is `CapabilityNotAvailable`. See [Safety & Capabilities](safety.md#runtime-savegame-slots).

**Names.** A slot name or a snapshot name passed to a command is 1 to 64 characters from `A-Z`, `a-z`, `0-9`, `_` and `-`, and not a Windows reserved device name (`CON`, `PRN`, `AUX`, `NUL`, `COM0`-`COM9`, `LPT0`-`LPT9`); anything else is `InvalidParams`. Slot names and snapshot names are separate, so a snapshot may have the same name as its slot. `UserIndex` is a whole number from 0 (default 0); the default save game system on Windows ignores it and keeps every user index in the same file.

**A typical round.** `SnapshotSaveGame` the slot → change it (`DeleteSaveGame`, `WriteSaveGame` or `CopySaveGameSlot`) → run the test and stop PIE → `RestoreSaveGame` the snapshot (`Overwrite: true` when the slot exists) → `DeleteSaveGameSnapshot` once it is no longer needed. When the slot did not exist beforehand there is nothing to snapshot; clean up by deleting the slot you created.

### Inspection (3) — requires `RuntimeSaveGameInspect`

| Command | Description |
|---|---|
| `ListSaveGameSlots` | Slot names of the configured save game system in ascending name order (ignoring case). `MaxResults` 1–1024 (default 256); `Truncated` is `true` when slots were left out. Each entry of `Slots[]` carries `Name`, `Addressable` (`false` for a name the other commands cannot take — such a slot is listed but never gets details) and `NameTruncated` (names that come from the files are sanitized and cut to 256 characters). `IncludeDetails: true` adds `Status`, `ByteCount`, `ModifiedAt`, `Format`, `SaveGameClassName`, `ClassNameIsGuess` and `SaveGameClassNameTruncated` to each addressable slot, reading only the leading part of it (the first 1 MiB with the default save game system); once 256 MiB have been read in total, the remaining slots are listed without details and `DetailsTruncated` is `true`. `SaveGameSystem` reports `ConfiguredSaveGameSystemModule` and `GenericPathsAvailable` — whether the project uses the default save game system, which is when sizes and modification times are available. An abnormal slot never fails the command. A project whose save game system cannot list its slots answers `UnsupportedOperation`; the other commands still work with a known slot name |
| `GetSaveGameInfo` | Metadata of one slot, without loading any class: `Status`, `Format`, `StoppedAtStage`, `FileVersion`, `PackageFileUEVersion`, `EngineVersion`, `CustomVersionFormat`, `UnregisteredCustomVersionCount`, `SaveGameClassName`, `ClassNameIsGuess`, `SaveGameClassNameTruncated`, `ClassLoaded` (whether that class is loaded right now — looked up, never loaded), `ByteCount`, `ModifiedAt` and `ContentHash` (SHA-1 as 40 hexadecimal digits — the value `ExpectedHash` takes). A damaged, oversized or unreadable slot does not fail the command: `Status` says so and whatever could be read is returned. `ContentHash` is returned only when the whole slot was read, so never for `TooLarge` or `Unreadable`; `ModifiedAt` only with the default save game system. A slot that does not exist is `NotFound` |
| `ListSaveGameSnapshots` | Snapshots taken by `SnapshotSaveGame`, in ascending name order (ignoring case). `MaxResults` 1–1024 (default 256), with `Truncated`. Only the metadata is read, never the slot bytes. Each entry of `Snapshots[]` carries `Name`, `NameTruncated` and `Status` — `OK`, or `Corrupt` for a snapshot file whose metadata cannot be read. An `OK` entry adds `SourceSlotName`, `UserIndex`, `CreatedAt` (UTC), `ByteCount`, `ContentHash`, `Format` and, when the header named one, `SaveGameClassName` (with `SaveGameClassNameTruncated` when it was cut). A `Corrupt` entry carries only those three keys; it is listed so that it can be found and deleted |

### Content read (1) — requires `RuntimeSaveGameContentRead`

| Command | Description |
|---|---|
| `DumpSaveGame` | Read one slot and return its property values as a JSON artifact holding `Properties` (property name → value), `PropertyCount`, and `UnresolvedReferences` / `ClearedSoftReferences` with their counts. The response carries `PropertyCount`, `UnresolvedReferenceCount` and `ClearedSoftReferenceCount`. A hard reference to an object that is not loaded becomes `null` and its path is listed in `UnresolvedReferences`; a soft reference normally stays as a path, and the few that had to be emptied are listed in `ClearedSoftReferences`. Both lists are deduplicated and hold at most 64 paths (the counts cover all of them), and a path longer than 1023 characters is cut and ends with `...`. A text that refers to a string table is dumped without loading the table. Refused before the body is read: a header this command cannot use (`ExecutionFailed`), a SaveGame class that is not loaded (`NotFound`) or is not a usable SaveGame class, and a slot larger than `MaxSaveFileBytes` (`NotAllowed`). ⚠️ The artifact holds the contents of the save as they are — see [the note on dump artifacts](#the-dumpsavegame-artifact-and-snapshots-hold-the-save-as-it-is) below |

### Slot changes (3) — requires `RuntimeSaveGameWrite`

| Command | Description |
|---|---|
| `DeleteSaveGame` | Delete one slot. A slot that does not exist is `NotFound`, with or without `ExpectedHash`. With `ExpectedHash` the whole slot is read once and compared first, and a mismatch is `Conflict`. A deleted slot cannot be recovered — snapshot it first when the data matters. Reports `Deleted`, `PreviousContentHash` (only when the slot was read) and `PlayWorldActive` |
| `CopySaveGameSlot` | Copy the bytes of `SourceSlotName` to `TargetSlotName` unchanged. The two must not name the same slot (compared ignoring case). The copied bytes are validated up to the SaveGame header (layout, versions and class), and the class it names must be loaded; the body after the header is never checked, so a slot whose body is damaged can be copied and can stop the game that later loads it. `SkipValidation: true` skips the header check — see [SkipValidation](#skipvalidation) below. Reports `ByteCount`, `Overwritten`, `ContentHash`, `PreviousContentHash` (only when the target was read for `ExpectedHash`), `ValidationSkipped`, `ValidationSkipReason` (`RequestedByCaller` when skipped) and `PlayWorldActive` |
| `WriteSaveGame` | Write a slot from the JSON object `Values`. Give exactly one of **`SaveGameClass`** — create a new object of that class with the class defaults and apply `Values` to it; the class is a full path, `/Script/<Module>.<Class>` or `/Game/<Path>/<Blueprint>.<Blueprint>_C`, and short names are refused — or **`BaseSlotName`** — read and restore that slot, apply `Values` on top, and save the result to `SlotName`, which may be the same slot (then `Overwrite: true` is required) or another one. Patching reads the contents of the base slot, so it also requires `RuntimeSaveGameContentRead`. Every key and value is checked before anything is written, and a single refused value writes nothing. Arrays, sets and maps are replaced as a whole (give one element and the others are gone); structs are merged field by field. The bytes about to be saved are validated up to the SaveGame header; the body is not checked. Reports `ByteCount`, `Overwritten`, `ContentHash`, `PreviousContentHash` (only when the target was read), `ValidationSkipped` (always `false`) and `PlayWorldActive`. See [Values of WriteSaveGame](#values-of-writesavegame) below for what `Values` accepts |

### Snapshots (3) — requires `RuntimeSaveGameWrite`

| Command | Description |
|---|---|
| `SnapshotSaveGame` | Copy the bytes of a slot unchanged into a named snapshot — a file in the `SaveGameSnapshots` folder of the UAIP working directory (`Saved/UAIP/SaveGameSnapshots/` unless [`AllowedArtifactDirectory`](config.md#allowedartifactdirectory-override) moves it). The bytes are not validated, so a damaged slot or a slot in a game's own format can be taken as well; only a slot larger than `MaxSaveFileBytes` is refused (`NotAllowed`). The snapshot records the source slot, the user index, the time it was taken (UTC), the size, the content hash, the `Format` and, when the header names it, the SaveGame class. An existing snapshot of the same name is replaced only with `Overwrite: true`; the replacement is not atomic, but wherever it stops, either the old or the new snapshot is left in place. The slot is only read, so this is allowed while the editor is playing and under `DisableSave`. Reports `ByteCount`, `ContentHash`, `Format` (`SaveGameHeader`, `Legacy` or `Unknown`), `Overwritten` and `PlayWorldActive` (when `true`, a running game may also be writing the slot, so the snapshot may not match what it saves next) |
| `RestoreSaveGame` | Write the bytes of a snapshot back to a slot. The snapshot is checked before any slot is touched, and a damaged one fails with `ExecutionFailed` (reason `SnapshotCorrupt`). `SlotName` and `UserIndex` each default to the value recorded in the snapshot, so omitting them restores the slot it was taken from. The header check is skipped on its own — `ValidationSkipReason: "SameSourceSlot"`, with no extra capability — when the bytes go back to the slot and user index they were taken from (slot names compared ignoring case) and still have the content hash recorded in the snapshot: that only brings back what was there, so a game with its own save format can still use snapshots. Restoring to another slot, or bytes whose hash no longer matches, is validated as usual and fails for a game's own format unless `SkipValidation: true` is given. The snapshot is kept, so a restore can be repeated. Reports the same keys as `CopySaveGameSlot`, with `ValidationSkipReason` `SameSourceSlot` or `RequestedByCaller` when the check was skipped |
| `DeleteSaveGameSnapshot` | Delete one snapshot together with its backup copy and any temporary file an interrupted snapshot left behind. A snapshot that does not exist is `NotFound`; a damaged one can be deleted. It touches no slot, so it is allowed while the editor is playing and under `DisableSave`. Reports `Deleted` |

#### Status of a slot

| `Status` | Meaning |
|---|---|
| `OK` | The header was read in full and every check passed |
| `LegacyOrUnknown` | The bytes do not start with the SaveGame header — a game's own format, or a layout from an old engine. A class name reported for it is a guess (`ClassNameIsGuess: true`) |
| `UnsupportedVersion` | The header declares a layout newer than this engine, or an old one (UE4, UE 5.0 and so on) that is deliberately not read |
| `Corrupt` | The header is truncated, malformed or holds values out of range |
| `TooLarge` | The file is larger than `MaxSaveFileBytes` and was not read |
| `Unreadable` | The save game system failed to load the slot |

**Only the leading part of the file is examined**, so `OK` does not promise that the rest of the file can be restored. Slots are not saved atomically either, so a slot the game is writing at that moment can read as `Corrupt` — snapshot it first when you need a stable copy.

**`PackageFileUEVersion` is a string, not a number**: `"UE4=<n>"`, or `"UE4=<n> UE5=<m>"` when the header also carries a UE5 version. It is omitted when the header reader stopped before reaching it. `StoppedAtStage` names the step the reader reached — `ByteCount`, `Tag`, `FileVersion`, `EngineVersion`, `CustomVersionFormat`, `CustomVersions`, `ClassName` or `Completed` — which tells how far a `Corrupt` header could be read.

**`SaveGameClassNameTruncated`.** A class name comes from the file, so it is sanitized and cut to 256 characters before it is returned. When a name was cut, `SaveGameClassNameTruncated: true` is present next to it — in `GetSaveGameInfo`, in `ListSaveGameSlots` with `IncludeDetails`, and in `ListSaveGameSnapshots`. The key is absent when the name was not cut. A cut name is not the real path of the class, so do not pass it on as `SaveGameClass`.

#### The DumpSaveGame artifact and snapshots hold the save as it is

> ⚠️ **A `DumpSaveGame` artifact is the contents of the save in plain JSON.** A save file can hold personal data — player names, account identifiers, anything the game stores — and the runtime has **no secret masking**: at run time there is no information that tells which values are secret. That is why `RuntimeSaveGameContentRead` is denied by default. The artifact stays in the artifact store until artifact garbage collection removes it (`[UAIP.ArtifactGC]` in [Configuration](config.md)), and anyone who can read the UAIP working directory can read it.
>
> **Snapshots hold the same thing as raw bytes**, and they stay until `DeleteSaveGameSnapshot` removes them: there is no limit on their number or total size, and nothing deletes them automatically. Delete the snapshots you no longer need.

#### Values of WriteSaveGame

- Keys match the property names ignoring case, also inside nested structs. An unknown key, or a property that is transient, deprecated or skipped by serialization, is refused rather than ignored.
- At most 49152 bytes of JSON, 16 levels of nesting and 4096 values. Names, enum names and reference paths are at most 1023 characters.
- Numbers have to fit the property. 64-bit integers are accepted up to ±2^53 — the range a JSON number represents exactly; a larger value would be rounded, so it is refused. Floats also accept the strings `"NaN"`, `"Infinity"` and `"-Infinity"`. Enums take an entry name or a declared value.
- Texts are stored as the given string. A string written in the form of a string table reference is not kept as a reference, and no string table is loaded.
- Object, class and soft references take a full path starting with `/` (the `Class'/Path.Obj'` form `DumpSaveGame` writes is accepted as is). A hard reference has to resolve to a loaded object, otherwise `NotFound`. An empty string `""` sets a reference to nothing.
- Structs take a JSON object, not a string. A set must not contain the same element twice, nor a map the same key.
- Not writable: interface, lazy, delegate and field path properties, and nested objects the save owns (an object carrying `_ClassName`) — creating them would load arbitrary classes.
- A refused value fails the whole request with `InvalidParams`. The failure diagnostics artifact lists where and why (`RejectedValues`, `RejectedValueCount`), never the values themselves.

> ⚠️ **`null` works one way only.** A reference that points at nothing comes out of `DumpSaveGame` as `null`, but `WriteSaveGame` refuses `null` everywhere. So a dump cannot always be sent back as it is. To clear a reference, pass `""`. When patching with `BaseSlotName`, leave the key out of `Values` instead, and the value in the base slot stays as it was.

> ⚠️ **Keys that differ only in case are not refused as duplicates.** `Values` is read with keys compared ignoring case, so `{"Score": 1, "score": 2}` is accepted and only the one written later is kept. A map keyed by strings ends up the same, because the game side compares those keys ignoring case as well, so the saved result would not differ. Check your keys for case-only collisions before sending them.

**What a dump cannot write back as it is.** Besides `null`: 64-bit integers beyond ±2^53 come out of `DumpSaveGame` rounded and are refused here; texts are written as plain strings (a string table reference or localization data is not kept); and nested objects (`_ClassName`) and interface, lazy, delegate and field path properties cannot be written.

**Patching a slot that holds references that would be lost.** When the base slot has any entry that `DumpSaveGame` would list in `UnresolvedReferences` or `ClearedSoftReferences`, `WriteSaveGame` refuses it with `NotFound` and lists the paths in the failure artifact, because saving it again would drop references you did not touch. Load the referenced assets first.

#### Refused before the body is read

`DumpSaveGame` and `WriteSaveGame` with `BaseSlotName` restore the slot into an object of its class. Before doing so they scan the stored property layout and refuse, with `ExecutionFailed`, a slot that would stop the editor while loading. The error names the location of the property and the reason, never the value:

- a string of 1024 characters or more stored for a property the class has since changed to a type other than a string or a text (container elements included), or no longer has
- a text stored for a property that is now a name (`FName`), whatever its length
- an object reference stored for a property that is now a field path
- a layout that is broken (a size out of range, a negative element count and so on)

The game itself may read some of these without trouble — notably a long string left in a property that was removed — but UAIP does not read them. Structs that serialize themselves (such as `InstancedStruct`) are not looked into; see [what remains a risk](safety.md#runtime-savegame-slots).

#### Overwriting and ExpectedHash

`CopySaveGameSlot`, `WriteSaveGame`, `RestoreSaveGame`, and `SnapshotSaveGame` for an existing snapshot, refuse to replace something that exists unless `Overwrite: true` is given (`NotAllowed`); patching a slot in place always needs it. The response reports `Overwritten: true` when something was replaced.

`ExpectedHash` on `DeleteSaveGame`, `CopySaveGameSlot`, `WriteSaveGame` and `RestoreSaveGame` is the content hash that the slot being written — not the source slot, the base slot or the snapshot — must have right before the write: 40 hexadecimal digits, compared ignoring case, as `GetSaveGameInfo` returns. A different hash, or a target that does not exist, is `Conflict` and nothing is written (for `DeleteSaveGame` a missing slot is `NotFound`). With `ExpectedHash` the target is read in full, so the read limit applies to it; without it the target is not read, so even a slot larger than the limit can be replaced or deleted. The check happens once, right before the write: a game saving in the background or another process can still write the slot in between.

#### During PIE and under DisableSave

`DeleteSaveGame`, `CopySaveGameSlot`, `WriteSaveGame` and `RestoreSaveGame` are refused with `NotAllowed` while the editor is playing, because the running game may read or overwrite the same slots; the message names `bAllowWritesDuringPIE` in `[UAIP.SaveGame]`, the setting that allows it. Stop PIE and run the command again. A `-game` or packaged build has no such refusal, although the game can still overwrite the same slot later. The same four are refused with `PolicyViolation` while the safety policy sets `DisableSave`.

`ListSaveGameSlots`, `GetSaveGameInfo`, `DumpSaveGame`, `SnapshotSaveGame`, `ListSaveGameSnapshots` and `DeleteSaveGameSnapshot` are allowed in both cases. `PlayWorldActive` in the response of the four slot-changing commands and of `SnapshotSaveGame` reports whether a game could be writing the same slots at that moment — an editor play session, or a `-game` or packaged run.

**Writes are not atomic.** A failure while writing (a full disk, a locked file) can leave the target slot damaged. Snapshot a slot worth keeping before you replace it; the snapshot brings it back.

#### SkipValidation

`CopySaveGameSlot` and `RestoreSaveGame` accept `SkipValidation: true`, which skips the header check so that a slot in a game's own format, a damaged one, one of an unsupported version or one whose class is not loaded can be copied or restored to any slot. It requires `RuntimeSaveGameUnvalidatedWrite` (DefaultDenied); without it the request fails with `CapabilityNotAvailable` (`PolicyViolation` when it is denied explicitly in `DeniedCapabilities`), even when a restore would have qualified for `SameSourceSlot`. The response reports `ValidationSkipped: true` with `ValidationSkipReason: "RequestedByCaller"`, or `"SameSourceSlot"` when that also applies. The size limit still applies. ⚠️ **A slot written this way can stop the game that loads it.**

#### Errors

| ErrorCode | When |
|---|---|
| `InvalidParams` | A name, `UserIndex`, `MaxResults`, hash, class path or value is not valid; `SourceSlotName` and `TargetSlotName` name the same slot; `WriteSaveGame` gets both or neither of `SaveGameClass` and `BaseSlotName`; the class is not a concrete, current subclass of `USaveGame` |
| `NotFound` | The slot or the snapshot does not exist; the SaveGame class or an object a value refers to is not loaded; the base slot of a patch holds references that would be lost |
| `NotAllowed` | The target exists and `Overwrite` is not `true`; the editor is playing; the file is larger than `MaxSaveFileBytes` (the message names the setting) |
| `Conflict` | `ExpectedHash` does not match, or the target it was given for does not exist |
| `PolicyViolation` | The safety policy sets `DisableSave` (slot changes only); or a required capability is denied explicitly in `DeniedCapabilities` (checked before `CapabilityNotAvailable`, so it wins) |
| `CapabilityNotAvailable` | A required capability — including one an argument adds — is not granted; the message names it |
| `ExecutionFailed` | The header cannot be used, the class named by the data cannot be used, the body could not be read (including the refusals above), the snapshot is damaged, or reading or writing a slot or a snapshot failed |
| `UnsupportedOperation` | `ListSaveGameSlots` on a save game system that cannot list its slots |

A failed command attaches a failure diagnostics artifact carrying `Command`, `FailedStage`, `Reason` (the cause, e.g. `SnapshotCorrupt`), `ErrorMessage` and what the failing step reported — the header fields for a header that could not be used, the reference paths for references that do not resolve, `RejectedValues` / `RejectedValueCount` for refused `Values`. Values stored in a save are never part of it.

---

## UAIP.Runtime.AI

This domain observes the AI of a running game: its perception system, and its behavior trees and Blackboards (see [Behavior tree and Blackboard observation](#behavior-tree-and-blackboard-observation) further down). The text up to that section is about the six perception commands.

Observe the AI perception system of a running game: what one AI currently senses, which AIs sense a given actor, the state of the perception system itself, why sight does or does not see a target, and the values of the sense configurations. Every perception command only reads — nothing here changes what an AI perceives. Works in the editor while PIE is running, and in `-game` and packaged builds; no plugin requirement. All six perception commands accept [`TargetNetRole` / `TargetPIEInstance`](#choosing-which-play-world-a-runtime-command-acts-on).

**Capabilities.** All six perception commands require `RuntimeInspect` (DefaultAllow). `DumpAIPerceptionSenseConfigs` also requires `AIPerceptionConfigDump` (DefaultDenied), because it writes out the values of every sense configuration, including those of a project's own sense classes. A missing one is `CapabilityNotAvailable`. See [Safety & Capabilities](safety.md#runtime-ai-perception).

**Perception exists only on the server.** AI controllers and the perception system live in a standalone or server world. In a networked PIE session, point these commands at the server with `TargetNetRole: "Server"` or `TargetPIEInstance`. Observing a client world still succeeds, but reports `Availability.State: "Unavailable"` with `Reason: "ClientWorld"` and lists the server side play worlds to retry against — see [When the perception system is unavailable](#when-the-perception-system-is-unavailable).

### Perception state (5) — requires `RuntimeInspect`

| Command | Description |
|---|---|
| 🆓 `DumpAIPerceptionState` | Everything one AI's perception component holds. `ActorIdentifier` names a pawn, an AI controller or another actor carrying a perception component (see [Finding the perception component](#finding-the-perception-component)). The artifact holds the configured senses (`Senses[]`), the `ListenerId` (when registered), the `TeamId` (`255` means no team), the `DominantSense`, every perceived actor with its stimuli (`Targets[]`) and `AgeUnitNote`. `MaxTargets` 1–4096 (default 256). Expired stimuli are left out unless `IncludeInactiveStimuli: true`; an actor whose stimuli are all expired is then neither listed nor counted. The response carries `ListenerRegistered`, `TargetCount`, `TargetsTotalCount` and `TargetsTruncated` |
| 🆓 `GetPerceivedActors` | The actors one AI senses right now (`Mode: "Current"`, the default) or senses and still remembers after losing them (`Mode: "Known"`), matched ignoring case. `Sense` restricts the result to one sense configured on the component, given by its short name (`Sight`, ignoring case) or its class path (exact); the state is then judged from that sense alone. A name that matches none of the configured senses, or more than one, is `InvalidParams`, and the message lists the senses that are configured. `HostileOnly: true` keeps only the actors the engine recorded as hostile. `MaxActors` 1–4096 (default 256). The response carries the first 50 entries of `Actors[]` (`Name`, `Label`, `Path`, `Senses[]`, `IsHostile`), `ActorsTotalCount`, `ActorsTruncated`, `Mode` and, when given, `Sense`; the artifact holds every actor. A returned `Name` can be passed back as `ActorIdentifier`, unless another actor's label happens to be the same string |
| 🆓 `GetActorPerceivers` | The other way round: which AIs sense the actor `ActorIdentifier`. The actor needs no perception component of its own. `Perceivers[]` lists each perceiving component (`ComponentOwner`) with the stimuli it holds for this actor; expired stimuli are always left out. `Source` describes the actor as a stimulus source: `ConfiguredOnSourceComponent[]` (the stimuli source components on it, with `AutoRegister` and the senses they register as), `ObservedBySight[]` (per sight implementation running in the world, whether the actor is registered as a sight target; omitted while the perception system is unavailable) and `OtherSenses: "Unknown"` (whether the actor is registered with other senses is not readable). `MaxPerceivers` 1–4096 (default 256). The response carries the first 50 perceivers, `PerceiversTotalCount` and `PerceiversTruncated`; the artifact holds every one |
| 🆓 `DumpAIPerceptionSystemState` | The perception system of the world as a whole. The response carries `HasBegunPlay`, `HasAuthGameMode`, `ComponentsWithValidListenerId` (an approximation: components that hold a listener id), `SightStatistics[]` (per sight implementation: `ObservedTargetCount`, `QueriesInRangeCount`, `QueriesOutOfRangeCount`, `QueriesPendingCount`), `ComponentCount`, `ComponentsTotalCount` and `ComponentsTruncated`. The artifact adds `PerceptionAgingRate`, `Senses[]` (each sense with `IsInstantiated` — configured senses that were never instantiated are listed too) and `Components[]` (each perception component with `ListenerRegistered` and `EnabledSenses[]`). `MaxComponents` 1–4096 (default 256) |
| 🆓 `ExplainSightPerception` | Why sight does or does not see `TargetIdentifier` from `ObserverIdentifier`, as 14 ordered steps. The target needs no perception component. The response and the artifact carry the same object. The explanation is recomputed from the current state and is **not authoritative** — see [Reading ExplainSightPerception](#reading-explainsightperception) |

### Sense configuration values (1) — requires `RuntimeInspect` and `AIPerceptionConfigDump`

| Command | Description |
|---|---|
| `DumpAIPerceptionSenseConfigs` | The value of every property of every sense configuration on one AI's perception component, the configurations of a project's own sense classes included. The response carries `SenseCount` and `Truncated`; the values are in the artifact's `Senses[]` — see [Values in DumpAIPerceptionSenseConfigs](#values-in-dumpaiperceptionsenseconfigs). Not affected by whether the perception system is available. ⚠️ The artifact stays after `AIPerceptionConfigDump` is taken away — see [Safety & Capabilities](safety.md#runtime-ai-perception) |

#### Parameters

| Parameter | Commands | Meaning |
|---|---|---|
| `ActorIdentifier` (required) | `DumpAIPerceptionState`, `GetPerceivedActors`, `DumpAIPerceptionSenseConfigs` | Label or object name of the pawn, AI controller or other actor whose perception component is read |
| `ActorIdentifier` (required) | `GetActorPerceivers` | Label or object name of the perceived actor |
| `ObserverIdentifier`, `TargetIdentifier` (both required) | `ExplainSightPerception` | Label or object name of the observing actor (found like `ActorIdentifier`) and of the actor whose visibility is explained |
| `MaxTargets` / `MaxActors` / `MaxPerceivers` / `MaxComponents` | one each | Upper bound on the main list. An integer from 1 to 4096; default 256 |
| `IncludeInactiveStimuli` | `DumpAIPerceptionState` | Boolean, default `false`. `true` also lists expired stimuli |
| `Mode` | `GetPerceivedActors` | `"Current"` (default) or `"Known"`, ignoring case |
| `Sense` | `GetPerceivedActors` | Short name of a sense or its class path. Up to 256 characters from `A-Z`, `a-z`, `0-9` and `_ . / : -` |
| `HostileOnly` | `GetPerceivedActors` | Boolean, default `false` |

Identifiers are 1 to 256 characters without control characters. Booleans must be JSON booleans and the limits JSON integers; anything else, an unknown key, or a limit outside 1–4096 is `InvalidParams`. Parameters are checked before the play world is looked up, so a malformed request is refused even when PIE is not running.

#### Finding the perception component

`DumpAIPerceptionState`, `GetPerceivedActors`, `ExplainSightPerception` (observer) and `DumpAIPerceptionSenseConfigs` accept the pawn, its AI controller, or any other actor that carries a perception component. The component is looked for on the named actor and on the controller or pawn it is paired with; when both carry one, the controller's component is used. The response reports the one used in `ComponentOwner` (`Name`, `Path`, `ComponentPath`) and lists any others in `OtherComponentsFound[]`, with `OtherComponentsFoundTotalCount` and `OtherComponentsFoundTruncated`. An actor whose pair has no perception component at all is `NotFound`.

#### Fields in every response

| Field | Meaning |
|---|---|
| `CapturedAt` | When the state was read (ISO 8601, UTC) |
| `Frame` | The engine frame number at that moment |
| `NetMode` | Net mode of the observed world |
| `WorldContext` | The world context the command read |
| `PIEInstance` | PIE instance of the observed world; omitted outside PIE |
| `Availability` | `State`: `Available` or `Unavailable`. When unavailable, `Reason`, and for `ClientWorld` also `ServerCandidates[]` (`PIEInstance`, `NetMode`, `MapName`, `IsPrimaryPIEInstance` of each server side play world) |
| `DegradedSections[]` | Parts of the result that could not be filled, each with `Section` and `Cause` (`PerceptionSystemUnavailable` or `UnreadableField`). An empty array means nothing was left out |
| `Limitations[]` | Caveats about what was returned, each with `Code` and sometimes `Detail` |

`Limitations[].Code` takes one of:

| `Code` | Meaning |
|---|---|
| `UnreadableField` | An engine value could not be read on this engine version. `Detail` names the field; the part that depends on it is left out |
| `UnknownStimulusExcludedFromMode` | A stimulus whose state could not be classified exists; `GetPerceivedActors` never matches it to a `Mode` |
| `StaleTargetsSkipped` | Entries for actors that no longer exist were skipped. `Detail` is the number skipped |
| `CustomSightImplementation` | Sight is not implemented by the engine's own sight class. `Detail` names the class in use |
| `RecomputedFromCurrentState` | `ExplainSightPerception` only, always present: the explanation is recomputed from the current state |

#### When the perception system is unavailable

A world without a usable perception system is not an error. The command succeeds, `Availability.State` is `Unavailable` and `Availability.Reason` says why:

| `Reason` | Meaning |
|---|---|
| `ClientWorld` | The world is a client; AI exists only on the server. `ServerCandidates[]` lists the server side play worlds |
| `AISystemDisabled` | The world settings disable AI, so the world has no AI system |
| `CustomAISystem` | The world's AI system is not the engine's standard one, so its perception system cannot be reached |
| `Unknown` | No AI system or no perception system, for a reason not listed above |

The parts that need the perception system are then listed in `DegradedSections[]` and left out of the result:

| Command | `Section` (cause `PerceptionSystemUnavailable`) | `Section` (cause `UnreadableField`) |
|---|---|---|
| `DumpAIPerceptionState` | `Targets`, `Senses` | `Targets` |
| `GetPerceivedActors` | `Actors` | `Actors` |
| `GetActorPerceivers` | `Perceivers`, `Source.ObservedBySight` | `Perceivers` |
| `DumpAIPerceptionSystemState` | `Senses`, `SightStatistics`, `ComponentsWithValidListenerId` | — |
| `ExplainSightPerception` | — (always empty; the first step fails instead) | — |
| `DumpAIPerceptionSenseConfigs` | — (always empty; not affected) | — |

`ListenerRegistered` and the `IsInstantiated` of each sense are written only while the perception system is available. The actor and component checks come first, so a missing actor is still `NotFound` in a world without a perception system.

#### Lists, counts and missing values

- **A value that is not there is left out, not written as `null`.** That includes the engine's "never" sentinels (for example a location that was never set) and non-finite numbers. The one `null` in this domain is `Diverged` in `ExplainSightPerception`.
- **Lists are ordered** by `Name` (ignoring case) and then `Path`; components by owner name and then `ComponentPath`. Sense configurations keep the order they are configured in.
- **Inner lists** (stimuli of a target, senses of an actor, other components and so on) hold at most 64 entries and come with `<Key>TotalCount` and `<Key>Truncated`.
- **`<Key>Truncated` means the `Max*` limit cut the list**, nothing else. `GetPerceivedActors` and `GetActorPerceivers` return only the first 50 entries in the response even when nothing was cut; the artifact holds every captured entry. So `ActorsTruncated: false` with 50 entries in `Actors[]` and `ActorsTotalCount: 120` means: compare the count with the array length, and read the artifact for the rest.

#### Stimuli

Each stimulus carries `SenseClass` (and `SenseName` when the sense is instantiated), `StimulusState`, `Strength`, `Age`, `ExpirationAge`, `StimulusLocation`, `ReceiverLocation`, `Tag`, `WasSuccessfullySensed` and `IsExpired`, each left out when there is no value.

| `StimulusState` | Meaning |
|---|---|
| `Sensing` | Sensed right now |
| `LostButRemembered` | Lost, but not expired yet |
| `Expired` | Past its maximum age. Listed only with `IncludeInactiveStimuli: true` |
| `Unknown` | Could not be classified. Kept and counted, never matched by `Mode`, and flagged with `UnknownStimulusExcludedFromMode` |

Things that look like bugs but are how the engine works:

- **A sense that reports events (hearing, for example) stays `Sensing` until the stimulus expires.** Such a sense never reports "lost" on its own.
- **A maximum age of 0 — the default for a sense configuration — never expires**, so the stimulus stays `LostButRemembered` indefinitely.
- **Ages advance in steps.** The perception system ages stimuli once every `PerceptionAgingRate` seconds (0.3 by default), so `Age` and `ExpirationAge` (game time seconds) can lag the real time since the stimulus by up to that interval. `AgeUnitNote` in the artifact says the same.
- **With the AI system's forget-stale-actors option enabled, `Expired` never appears**: the engine removes an actor whose stimuli have all expired instead of keeping it as expired.

#### Reading ExplainSightPerception

The response is built from **the current state**: steps 1–9 read what the engine holds now, and steps 10–14 recompute the sight checks from the current configuration, positions and teams. It is **not the engine's own decision log** and can differ from what the engine decided at its last update — when the observer has moved since then, when the query has not been re-evaluated yet, when the trace runs asynchronously, or when the configuration was changed at run time. It is a diagnosis aid, not a verdict. `Limitations` always carries `RecomputedFromCurrentState`.

`AlgorithmRevision` (an integer, currently `1`) identifies the way the steps are evaluated. It goes up whenever their meaning changes, so compare explanations only when it is the same. `EvaluationBasis` is always `"CurrentState"`.

Each entry of `Steps[]` carries `Step`, `Basis` (`EngineState` or `Recomputed`), `Result` and, sometimes, `Detail`. All 14 steps are always present, in this order:

| # | `Step` | `Basis` | Checks |
|---:|---|---|---|
| 1 | `PerceptionSystemAvailable` | `EngineState` | The world has a usable perception system |
| 2 | `ListenerRegistered` | `EngineState` | The observer's perception component is registered as a listener |
| 3 | `SightConfigured` | `EngineState` | The component has a sight configuration |
| 4 | `SightEnabled` | `EngineState` | Sight is enabled on the component |
| 5 | `SightInstantiated` | `EngineState` | The sight sense exists in the perception system |
| 6 | `TargetIsNotSelf` | `EngineState` | The target is not the observer itself |
| 7 | `DigestAvailable` | `EngineState` | The sight sense holds the observer's digested configuration |
| 8 | `ObservedBySight` | `EngineState` | The target is registered as a sight target |
| 9 | `QueryExists` | `EngineState` | A sight query for this observer and target exists |
| 10 | `Affiliation` | `Recomputed` | The team attitude allows sensing the target |
| 11 | `AutoSuccess` | `Recomputed` | The target is within the auto-success range of where it was last seen |
| 12 | `Distance` | `Recomputed` | The target is within sight range |
| 13 | `PeripheralAngle` | `Recomputed` | The target is within the peripheral vision angle |
| 14 | `Occlusion` | `Recomputed` | Nothing blocks the line of sight |

`Result` is `Pass`, `Fail`, `Skipped` (not evaluated because of an earlier result), `NotApplied` (the step does not apply) or `Delegated` (the target decides for itself). How the steps depend on each other:

- Steps 1–8 stop at the first `Fail`; every step after it is `Skipped`.
- When `QueryExists` fails, only `Affiliation` is still evaluated, as a candidate reason (team attitude is the usual reason a query is never created); the rest are `Skipped`.
- When `QueryExists` passes, `Affiliation` is `Skipped` — the query exists, so the team attitude already let it be created — and steps 11–14 are evaluated.
- `AutoSuccess` never fails. `Pass` makes the remaining steps `Skipped`; otherwise it is `NotApplied` (always, with the default configuration).
- `Distance` uses the lose-sight radius when the engine last saw the target, the sight radius otherwise.
- A `Fail` in `Distance` or `PeripheralAngle` makes `Occlusion` `Skipped`.
- A target that implements the sight target interface decides its own visibility, so `Occlusion` is `Delegated` and its visibility function is not called.

`QueryExists` adds `QueryList` (`SightQueriesInRange`, `SightQueriesOutOfRange` or `SightQueriesPending`), `Pending`, `LastSeenLocation`, `LastResult` (only when the query is not pending) and `AsynchronousTrace`. `Affiliation` adds `TeamAgent` (`Owner`, `BodyActor` or `None` — whose team was used). `Occlusion` adds `HitActor` when something blocks the line.

Which fields are present:

| Field | Present |
|---|---|
| `Observer`, `Target` (`Name`, `Label`, `Path`), `ComponentOwner`, `OtherComponentsFound[]` | Always |
| `EvaluationBasis`, `AlgorithmRevision`, `Steps[]` | Always |
| `Diverged` | Always. `true` or `false` when the recomputed result can be compared with the engine's last result; `null` when it cannot — an engine state step failed, the query is pending, or `Occlusion` is `Delegated` |
| `DivergenceCandidates[]` | Always; has items only when `Diverged` is `true`. Possible items: `StaleListenerLocation`, `QueryNotYetReevaluated`, `AsynchronousTrace`, `ConfigChangedAtRuntime`, `CustomSightImplementation` |
| `ConfigDigestMismatch[]` | Always; one `{Field, FromConfig, Digested}` per value that differs between the sight configuration and what the sight sense digested from it (`SightRadiusSq`, `LoseSightRadiusSq`, `NearClippingRadiusSq`, `PeripheralVisionAngleCos`, `PointOfViewBackwardOffset`, `AutoSuccessRangeSqFromLastSeenLocation`, `AffiliationFlags`) |
| `ListenerRegistered` | When `ListenerRegistered` was evaluated |
| `FirstFailingStep` | When a step failed. After a failed `QueryExists` it is `QueryExists`, and `Affiliation` is the candidate reason |
| `SightConfigUsed` (`ConfigClass`, `ImplementationClass`, `OtherSightConfigs[]`) | When `SightConfigured` passed. The first sight configuration is used; the others are listed |
| `EngineLastResult` | When `QueryExists` passed and the query is not pending |
| `EngineConeCheck` | When `DigestAvailable` passed |

When sight is not implemented by the engine's own sight class, `Limitations` carries `CustomSightImplementation` and the recomputed steps are only indicative. **A target whose sight target interface completes a pending visibility check on another thread is not supported**; what this command reports for such a target is not guaranteed.

#### Values in DumpAIPerceptionSenseConfigs

Each entry of `Senses[]` carries `SenseName` (when instantiated), `SenseClass`, `ConfigClass`, `IsEnabled`, `IsInstantiated` (only while the perception system is available), `Properties[]` (`Name`, `Type`, `Value`) and `Truncated`. Base class properties come first, each class in declaration order; editor-only properties are never listed. A value is written as:

| Property | Written as |
|---|---|
| Number, boolean | The value. Floats that are not finite become the strings `"NaN"`, `"Infinity"` or `"-Infinity"` |
| Enum | The entry name; the number when the value has no name |
| Name, string, text | A string, cut at 1024 characters |
| Struct | An object, one level deep. A struct nested further, or a struct inside a container, becomes `{"Type": "<type>"}` |
| Array, set, map, fixed-size array | `{"Value": [...], "TotalCount": N, "Truncated": bool}` holding the first 32 elements; a map element is `[key, value]`; sets and maps keep their storage order |
| Object, class, soft, weak, lazy or interface reference | The path as a string, `"None"` when empty. Nothing is ever loaded |
| Delegate and other unsupported types | `{"Unsupported": "<type>"}` |

At most 64 senses, 64 KiB per sense and 256 KiB in total. A sense that reaches its own budget keeps what fits and reports `Truncated: true`; once the total budget is used, the remaining senses are written as `Omitted: true` with only their identity. `SenseCount` in the response is the number of sense entries written, omitted ones included, and `Truncated` is `true` when any of these limits cut the dump.

`DumpAIPerceptionState` lists the same configurations in its `Senses[]` with less detail: the values of engine-declared properties are shown (also on a project's own configuration class derived from one), while a property the project declared shows only `Name` and `Type`, without the `Value` key. Use `DumpAIPerceptionSenseConfigs` for those values.

#### Errors

| ErrorCode | When |
|---|---|
| `InvalidParams` | A parameter is missing, of the wrong type, out of range or unknown; `Sense` matches no configured sense or more than one; `TargetNetRole` / `TargetPIEInstance` cannot be honoured |
| `NotAllowed` | No play world is running (`PIE is not running.`), or none matches `TargetNetRole` / `TargetPIEInstance` |
| `NotFound` | No actor matches the identifier; the actor and the controller or pawn it is paired with have no perception component ("The actor has no AI perception component, and neither does the controller or pawn it is paired with."). For `ExplainSightPerception` the message starts with `The observer actor could not be resolved.` or `The target actor could not be resolved.`, and the component message names the observer actor |
| `ExecutionFailed` | More than one actor matches the identifier; the artifact could not be written |
| `CapabilityNotAvailable` | `RuntimeInspect`, or for `DumpAIPerceptionSenseConfigs` `AIPerceptionConfigDump`, is not granted |
| `PolicyViolation` | The capability is denied by the safety policy |

When the observed world is a client, an error message after the world was found ends with a note that AI exists only on the server and names the server side play worlds to retry with `TargetPIEInstance`.

Every successful call saves exactly one JSON artifact; a failed call saves none.

### Behavior tree and Blackboard observation

Observe the behavior tree an AI runs and the Blackboard it reads: which node is active, which decorators pass, what the Blackboard holds, and how the tree moved over time. Seven of the eight commands only read. `DescribeBehaviorTreeWithProjectCode` is the exception: it runs project code, and is described separately below. The commands act on one actor of a play world (PIE is what is verified; `-game` and packaged builds are not) and accept [`TargetNetRole` / `TargetPIEInstance`](#choosing-which-play-world-a-runtime-command-acts-on) — except `GetBehaviorTreeEventLog` and `StopBehaviorTreeCapture`, which take a `CaptureId` instead and never look up a play world, so they still work after the play session ended. The actor is given as `ActorIdentifier`: the label or object name of the AI controller, its pawn, or any other actor that owns the component. When a name is not known, `ListBehaviorTreeAgents` returns the names to use.

**Capabilities.** All eight require `RuntimeInspect` (DefaultAllow). `GetBlackboardValues` also requires `BlackboardValueRead` (DefaultDenied), because Blackboard values are project data. `DescribeBehaviorTreeWithProjectCode` requires `BlackboardValueRead` and `AIBehaviorProjectCodeExecution` (DefaultDenied) in addition. A missing one is `CapabilityNotAvailable`. See [Safety & Capabilities](safety.md#runtime-ai-behavior-trees-and-blackboards).

**Demo build.** `DescribeBehaviorTreeWithProjectCode` and the `AIBehaviorProjectCodeExecution` capability are not provided in the demo binary: the command is absent and returns `CommandNotFound`. The other seven commands are provided. `BlackboardValueRead` is registered in the demo too, but the demo's ini does not grant it, so reading values there needs an ini line of your own. Where a response of the demo would name `AIBehaviorProjectCodeExecution` as the permission an omitted description needs, it says `NotInThisEdition` instead.

#### Current state (3) — requires `RuntimeInspect`

| Command | Description |
|---|---|
| 🆓 `ListBehaviorTreeAgents` | Lists the actors of the target play world that are running a behavior tree, with the behavior tree component of each and whether its tree is paused. A paused tree is listed; a tree that was stopped or never started is not. `MaxEntries` 1–4096 (default 256). The response carries `AgentCount`, `AgentsTotalCount` and `AgentsTruncated`; the artifact holds every agent. A world with no AI system, such as a client side play world, answers with an empty list. While the engine state may be half updated (a modal dialog or a long running task holds the game loop, or the world is in the middle of its tick) nothing is read and `Availability` is `NotAtSafePoint`. Use the names it returns as `ActorIdentifier` of the other commands |
| 🆓 `GetActiveBehaviorTreeNode` | The active node of one actor's behavior tree and the path from it to the root, with `IsRunning` and `IsPaused`. The light form of `DumpBehaviorTreeState`: no description, no verdict and no Blackboard is read or returned. The response and the artifact hold the same result |
| 🆓 `DumpBehaviorTreeState` | Everything the default observation may say about one actor's behavior tree. `IsRunning`, `IsPaused`, `IsRestartPending` and `IsAbortPending`; the stack of tree instances (a subtree is a further instance), each with its `TreeAsset`, the active node and its path to the root, `ActiveNodeType` (`Composite`, `ActiveTask`, `AbortingTask` or `InactiveTask`), the active auxiliary nodes (decorators and services) and the parallel tasks with their `Status`; and the Blackboard key definitions, which are returned whenever the Blackboard can be reached, also when the tree is not running. Every node carries `InstanceIndex`, `TreeAsset`, `ExecutionIndex`, `NodeName`, `ClassPath` and `NodeRole`. For a node the default observation may describe it adds `StaticDescription`, `RuntimeDescription` and, for a decorator on the path from the active node to the root and for an active auxiliary decorator, `Verdict` (`Passed`, `Failed` or `Unknown`). For every other node it says why they are left out — `DescriptionOmittedReason` / `VerdictUnknownReason` — and which capabilities would produce them (`RequiresCapabilities[]`); see [What the default observation leaves out](#what-the-default-observation-leaves-out). `MaxEntries` 1–4096 (default 256) bounds the described nodes. Data holds the leading entries of each list and the artifact holds all of them. Returns a degraded result, not an error, when the tree has not been started (`Availability: NotRunning`) or the engine state may be half updated and was not read (`NotAtSafePoint`) |

#### Blackboard values (1) — requires `RuntimeInspect` and `BlackboardValueRead`

| Command | Description |
|---|---|
| 🆓 `GetBlackboardValues` | The value of every key of one actor's Blackboard, together with the full descriptions of the running nodes that print Blackboard values. Standard key types come back as typed values (`Bool`, `Int`, `Float`, `Name`, `String`, `Vector`, `Rotator`, `Enum`, `NativeEnum`, `Object`, `Class`, `Struct`); an `Object` or `Class` key tells an empty reference (`Empty`) from a live one (`Live`) and a destroyed one (`Destroyed`); a `Struct` key is rendered field by field within fixed bounds, without calling any export function of the struct. A key of a type the project defines is reported by type name only, with `RequiresCapabilities: ["AIBehaviorProjectCodeExecution"]` (`NotInThisEdition` in the demo). A node whose description cannot be produced here is listed with the reason and the capability that would produce it. `MaxEntries` 1–4096 (default 256) bounds the keys. A Blackboard component that runs with no Blackboard asset answers with no keys and `BlackboardAvailability: NoAsset`; an actor with no Blackboard component is `NotFound`. See [Reading Blackboard values](#reading-blackboard-values) |

#### Project code (1) — requires `RuntimeInspect`, `BlackboardValueRead` and `AIBehaviorProjectCodeExecution`

Not provided in the demo build.

| Command | Description |
|---|---|
| `DescribeBehaviorTreeWithProjectCode` | Describes what the other commands leave out because producing it runs project code, for one actor: the static and runtime descriptions of project and Blueprint nodes, the verdicts of engine decorators that reach project code, the runtime descriptions and verdicts of a behavior tree component class the project derived, and the values of the Blackboard keys whose type the project defines. Only running nodes that one of those outputs applies to are listed. Outputs that no command produces, because the engine code behind them has not been verified, are never called and are listed with the reason (`EngineCallNotVerified`). `MaxEntries` 1–4096 (default 256) bounds the described nodes; a node past the bound is not called. ⚠️ **It runs project code, which may change the tree while it runs.** The tree is checked again before every call; a node that stops running is skipped and reported with `NodeDeactivatedDuringProjectCode`, and a tree or Blackboard that changes (the tree is stopped, the Blackboard asset is replaced, a key is retyped, an actor key now points at another actor) stops the description with `TreeChangedDuringProjectCode`, returning what was produced until then. A Blackboard value that is merely rewritten does not stop it; the descriptions that follow use the new value. Not read-only: it is refused with `PolicyViolation` under the safety policy's read-only mode, and with `NotAllowed` while a modal dialog or a long running task holds the game loop (if the operator's starved-tick allow list lets it run then anyway, it reads nothing and reports `NotAtSafePoint`). An actor with no behavior tree component is `NotFound` |

#### Recording (3) — requires `RuntimeInspect`

A recording belongs to the session that started it: another session sees `NotFound` for its id, without being told whether it exists. A recording reads the tree once per world tick, after every actor has ticked, and keeps what changed — not Blackboard values.

| Command | Description |
|---|---|
| 🆓 `StartBehaviorTreeCapture` | Starts recording how one actor's behavior tree changes over time, into a capture owned by the calling session, and returns its `CaptureId`. The tree may be stopped or not started yet: its start is recorded when it happens. `MaxDurationSeconds` (1–600, default 120), `BufferCapacity` (64–16384, default 4096; the number of entries kept before the oldest are dropped and counted) and `ReplaceExisting` (default `false`, which refuses a second recording of the same component and names the first; `true` stops that capture and starts a new one). A session records at most 8 behavior trees at once, a world holds at most 32 recording captures across all sessions, and a stopped capture is kept for 30 minutes. The first entry is the `Baseline`, the state when the recording started. If the engine state may be half updated at that moment, the recording still starts, the Baseline is taken at the first read after the game ticks and the response says `BaselinePending: true`. A recording stops by itself at `MaxDurationSeconds`, when the play session ends or when the component is destroyed. Fails with `NotFound` when the actor has no behavior tree component |
| 🆓 `GetBehaviorTreeEventLog` | Reads the entries of a capture, oldest first, from `SinceSequence` on (default 0). `CaptureId` (required) is the id `StartBehaviorTreeCapture` returned. `MaxEntries` 1–4096 (default 256). Data holds the first 50 entries of the read; the artifact holds every entry of it, and `NextSequence` is the `SinceSequence` that continues after the artifact's last entry. `bGap` is true when entries at or after `SinceSequence` were dropped before they could be read; `DroppedCount` counts the entries dropped by the capacity of the capture or by the bound on the entries one read of the tree may produce. The response also carries the capture's `State`, why it stopped (`EndReason`), `OldestAvailableSequence`, `BaselinePending`, `RecordingSeconds` and `Limitations[]`. Works after the play session ended. Fails with `NotFound` for an unknown, expired or foreign `CaptureId`, without telling which |
| 🆓 `StopBehaviorTreeCapture` | Stops a capture and returns its final state: why it stopped, whether the Baseline was taken, the recording seconds and the sequence bookkeeping. Stopping a capture that already stopped succeeds and keeps the reason it first stopped with (`Stopped`, `DurationLimit`, `WorldTornDown`, `Replaced` or `TargetDestroyed`). Works after the play session ended; a session keeps at most 4 stopped captures and drops the oldest first. Fails with `NotFound` for an unknown, expired or foreign `CaptureId`, without telling which |

#### What the default observation leaves out

`DumpBehaviorTreeState` and the recording describe a node only when it is known to be safe: the node class must be one the plugin has checked, and every Blackboard key it refers to must be of a standard type. For every other node the description is left empty, its verdict is `Unknown`, and the response gives the reason and the permission that would produce it:

| Reason (`DescriptionOmittedReason` / `VerdictUnknownReason`) | Meaning | Where to read it |
|---|---|---|
| `BlackboardValueReadRequired` | The description would print a Blackboard value — an engine node that shows a key's value, or a parameter bound to a Blackboard key whose remaining time or similar is derived from the value | `GetBlackboardValues` (needs `BlackboardValueRead`) |
| `ProjectCodeExecutionRequired` | Producing it runs project code — a node the project or a Blueprint defined; a node that refers to a key of a project-defined type, struct or enum; an engine decorator whose verdict calls into a project object (for example one that asks the actor a Blackboard key points at for its gameplay tags) | `DescribeBehaviorTreeWithProjectCode` (needs `AIBehaviorProjectCodeExecution`) |
| `ProjectDerivedComponent` | The tree runs in a behavior tree component class the project derived, whose runtime descriptions and verdicts cannot be trusted to be the engine's | `DescribeBehaviorTreeWithProjectCode` |
| `EngineCallNotVerified` | An engine node whose description or verdict has not been checked to be safe to call, or is known to be unsafe (for example the runtime description of a loop decorator). No command calls it | None |
| `NodeMemoryUnavailable` | The memory the node keeps for the running tree could not be reached, so the node was not asked | None |

A node bound to a Blackboard key whose type cannot be confirmed — the behavior tree component has no Blackboard asset, the key is missing from the asset, or the type the node expects differs from the key's type — is `EngineCallNotVerified` rather than a permission reason, because granting a permission would not make it readable. In the demo build, `RequiresCapabilities` never names `AIBehaviorProjectCodeExecution`; it says `NotInThisEdition`.

#### Reading Blackboard values

- **`IsSet` in the key definitions** (`DumpBehaviorTreeState`, `GetBlackboardValues`) is `true` or `false` for `Vector`, `Rotator`, `Object` and `Class` keys, and `null` (unknown) for every other type, because a zero or empty value cannot be told from an unset one. For `Object` and `Class`, a reference that points at a destroyed object counts as not set; `GetBlackboardValues` tells an empty reference from a destroyed one. The `Limitations` entry `IsSetNotDeterminable` says so.
- **Struct keys** are rendered field by field. A nested struct is expanded one level further; a deeper one is written as its type name. A struct of a kind chosen at run time (an instanced struct or property bag) nested in a struct is not expanded, and `NestedInstancedStructNotExpanded` says so.
- **Enum keys** carry the number and the name of the entry. For an enum defined in Blueprint, the name is the internal name, not the display name set in the editor (`UserDefinedEnumNamesAreInternal`). An obsolete native enum key (deprecated by the engine) holds no value area, so it is reported with a `ValueOmittedReason` instead of a value.
- **Bounds.** A container inside a struct key keeps its first 32 elements, a string is cut at 1024 characters, a key's value is limited to 64 KiB and one response to 256 KiB; what does not fit is cut or left out and marked. A reference is written as a path and never followed.
- **A Blackboard component with no asset** answers `BlackboardAvailability: NoAsset` with no keys; **no Blackboard component** is `NoComponent` in `DumpBehaviorTreeState` and `NotFound` in `GetBlackboardValues`.

#### Matching a runtime node to the editor asset

A node in a runtime response is identified by its `TreeAsset` and its `ExecutionIndex`. The same number is reported by the Editor commands `GetBehaviorTreeNodeList` and `GetBehaviorTreeSubtree` ([`UAIP.Editor.BehaviorTree`](#uaipeditorbehaviortree)), for the asset as it would run as a top-level tree, without opening PIE and without saving the asset. Look the runtime pair up there to find the node in the asset. The number of `GetBehaviorTreeNodeProperties` is a different value and is not for matching.

A node without a number carries `ExecutionIndex: null` and `ExecutionIndexUnavailableReason`, which is one of:

| `ExecutionIndexUnavailableReason` | Meaning |
|---|---|
| `ContextDependentInjectedDecorator` | A decorator on the root of the asset. It runs only when another tree calls this one, and its number depends on the calling tree, so look it up on the calling asset instead |
| `NotInCompiledTree` | The node is in the graph but not yet in the tree the asset runs, for example right after it was added |

#### Fields in every behavior tree response

| Field | Meaning |
|---|---|
| `CapturedAt`, `Frame`, `NetMode`, `WorldContext`, `PIEInstance`, `WorldTimeSeconds` | When and where the state was read: ISO 8601 UTC time, the engine frame number, the net mode and world context, the PIE instance (omitted outside PIE) and the world time |
| `Actor`, `Component` | The actor and the behavior tree component that were observed |
| `Availability` | `Running`, `NotRunning` (the tree has not been started or was stopped; the instances and nodes are empty, the Blackboard key definitions are still returned) or `NotAtSafePoint` (the engine state may be half updated, so nothing was read; call again once dialogs and loading have finished). A paused tree is `Running` with `IsPaused: true`. `AvailabilityReason` says why in words |
| `BlackboardAvailability` | `Available`, `NoAsset`, `NoComponent` or `NotAtSafePoint` |
| `Limitations[]` | Caveats about what was returned, each with `Code` and sometimes `Detail` |

`Limitations[].Code` takes one of:

| `Code` | Meaning |
|---|---|
| `InstanceWithoutTasksNotVisible` | A tree instance (subtree level) that holds no task is not visible. Reported when it can be detected; not every such arrangement can |
| `SubTickTransitionsNotVisible` | A recording reads the tree once per tick, so when the tree moves several times within one frame only the last state is seen |
| `ReasonNotRecorded` | A recording says what changed, not why |
| `NotPolledWhileWorldPaused` | A recording is not read while the game is paused; what changed meanwhile shows up together after it resumes |
| `BaselineNotTaken` | The recording stopped before its first read, so it has no `Baseline` entry |
| `NodeDeactivatedDuringProjectCode` | `DescribeBehaviorTreeWithProjectCode` skipped a node that stopped running while project code ran |
| `TreeChangedDuringProjectCode` | `DescribeBehaviorTreeWithProjectCode` stopped because project code changed the tree or the Blackboard; the response holds what was produced until then |
| `NotAtSafePoint` | The engine state may have been half updated, so it was not read |
| `NestedInstancedStructNotExpanded` | A struct of a kind chosen at run time inside a struct value is not expanded |
| `IsSetNotDeterminable` | `IsSet` is `null` for key types whose unset state cannot be told from a zero value |
| `UserDefinedEnumNamesAreInternal` | The name of a Blueprint-defined enum entry is its internal name |

A recording entry carries `Sequence`, the frame, the time and a `Kind`: `Baseline`, `TreeStarted`, `TreeStopped`, `Paused`, `Resumed`, `InstancePushed`, `InstancePopped`, `ActiveNodeChanged`, `ActiveNodeTypeChanged`, `AuxNodeActivated`, `AuxNodeDeactivated`, `ParallelTaskChanged`, `RestartPendingChanged` and `AbortPendingChanged`. A `Baseline` entry holds the tree state in `Snapshot`; a `Baseline` taken at the first read after the start, rather than at the start itself, is marked `Deferred`.

#### Errors

| ErrorCode | When |
|---|---|
| `InvalidParams` | A parameter is missing, of the wrong type, out of range or unknown; `TargetNetRole` / `TargetPIEInstance` cannot be honoured. Out-of-range recording durations, capacities and limits are refused, never rounded |
| `NotAllowed` | No play world is running (`PIE is not running.`), or none matches `TargetNetRole` / `TargetPIEInstance`; a recording limit (per session or per world) is reached, or the component is already recorded and `ReplaceExisting` is not set; `DescribeBehaviorTreeWithProjectCode` while a modal dialog or a long running task holds the game loop |
| `NotFound` | No actor matches the identifier (in a client side world, the server candidates are named in the message); the actor and the controller or pawn it is paired with have no behavior tree or Blackboard component; an unknown, expired, malformed or foreign `CaptureId` |
| `ExecutionFailed` | More than one actor matches the identifier; the artifact could not be written (for `StartBehaviorTreeCapture` and `StopBehaviorTreeCapture` only when the save location itself cannot be resolved) |
| `CapabilityNotAvailable` | `RuntimeInspect`, `BlackboardValueRead` or `AIBehaviorProjectCodeExecution` is not granted. The message names the missing ones |
| `PolicyViolation` | A required capability is denied by the safety policy, or `DescribeBehaviorTreeWithProjectCode` is called in read-only mode |

Every successful call saves exactly one JSON artifact (the recording commands `StartBehaviorTreeCapture` and `StopBehaviorTreeCapture` save a supporting one); a failed call saves none.

---

## UAIP.Runtime.StateTree 🧩

Observe the StateTree an AI runs: which states are active, which tasks run, which delayed transitions are waiting, how the tree moved over time and — when you allow it — the values it holds. Requires the `StateTree` and `GameplayStateTree` plugins. If either is disabled the commands are not registered, and calling one returns `CommandNotFound` naming the plugin; `UAIP.Core.ListIntegrations` reports the state. Not provided in the demo build. Every command only reads. The commands act on the `UStateTreeComponent` family (including `UStateTreeAIComponent`) of an actor in a play world and accept [`TargetNetRole` / `TargetPIEInstance`](#choosing-which-play-world-a-runtime-command-acts-on) — except `GetStateTreeEventLog` and `StopStateTreeCapture`, which take a `CaptureId` and never look up a play world, so they still work after the play session ended.

**Capabilities.** All seven require `RuntimeInspect` (DefaultAllow). `DumpStateTreeInstanceData` also requires `StateTreeInstanceDataDump` (DefaultDenied), because the values of a tree's parameters and nodes are project data. A missing one is `CapabilityNotAvailable`. See [Safety & Capabilities](safety.md#runtime-statetree-observation).

**Finding the component.** `ActorIdentifier` is the label or object name of the actor. The component is looked for on that actor; if it has none, on the AI controller of a pawn, or the pawn of an AI controller (a `UStateTreeAIComponent` usually sits on the controller and a `UStateTreeComponent` on the pawn). When several components are found, `ComponentName` (the component's object name) must choose one: without it the command fails with `InvalidParams` and lists the candidates, and a name that matches none is `NotFound` with the candidates. `ListStateTreeComponents` returns the names to use.

**A component class the project derived is not read.** The engine offers no way to verify that such a class runs its tree the way the engine component does, and reading it wrongly would switch off the engine's own validation. The observation commands succeed without reading it and say so (`Availability: ProjectDerivedComponent`, and `ProjectDerivedComponentNotVerified` in `Limitations`); `ListStateTreeComponents` lists it with `RunStatus: null` and the reason. `StartStateTreeCapture` can record it, but if the class runs the tree under another owner or tree, nothing is recorded.

#### Current state (3) — requires `RuntimeInspect`

| Command | Description |
|---|---|
| `ListStateTreeComponents` 🧩 | Lists the StateTree components of the actors of the target play world: the actor, the component, its class, the tree asset it is set to run and its `RunStatus`. The run status of a component that is not read (a class the project derived, or a tree that is not linked) is `null`, with `RunStatusUnavailableReason`. `MaxEntries` 1–4096 (default 256). Data holds the leading components and the artifact holds all of them. While the engine state may be half updated (a modal dialog or a long running task holds the game loop, or the world is in the middle of its tick) the actors are not walked at all, no list is returned and `Availability` is `NotAtSafePoint` |
| `GetActiveStateTreeState` 🧩 | The active states of one component's StateTree: the `RunStatus` and, for each frame of the active frame stack, the tree asset and the path from the root to each active state. The light form of `DumpStateTreeState`: no tasks, delayed transitions or next tick. Data and the artifact hold the same content |
| `DumpStateTreeState` 🧩 | One component's StateTree in full: `RunStatus` (`Running`, `Stopped`, `Succeeded`, `Failed` or `Unset`) and `LastTickStatus`; the `Frames[]` of the active frame stack, each with the tree asset and the active states (name, tag, `StateType` — `State`, `Group`, `Linked`, `LinkedAsset` or `Subtree` — and path); the tasks of the active states with their `Status`; the delayed transitions that are waiting, with the target state and the `RemainingSeconds`; and `NextScheduledTickSeconds`. Data holds the leading frames and the artifact holds all of them. Returns a degraded result, not an error, when the tree has not been started, the component has no tree or is not ready to run, the component is of a class the project derived, or the engine state may be half updated and was not read |

#### Instance data (1) — requires `RuntimeInspect` and `StateTreeInstanceDataDump`

| Command | Description |
|---|---|
| `DumpStateTreeInstanceData` 🧩 | The values one component holds: the parameters of the tree, the parameters of each active state and the instance data of each active node, as blocks of properties with their values (`Blocks[]`, each with a `BlockKind`). The values are read by reflection and no function of a node or other project type runs. A struct is expanded one level, an array, set or map keeps its leading elements, a long string is cut and a value that does not fit the byte budgets is cut or left out (`bOmitted`); each cut is reported beside the count before it. A struct of a kind chosen at run time nested in a struct is not expanded (`NestedInstancedStructNotExpanded`). `MaxEntries` 1–4096 (default 256) bounds the blocks. Data holds the leading blocks and the artifact holds all of them. Degrades like `DumpStateTreeState`. See [Safety & Capabilities](safety.md#runtime-statetree-observation) for what comes out |

#### Recording (3) — requires `RuntimeInspect`

A recording belongs to the session that started it: another session sees `NotFound` for its id, without being told whether it exists.

| Command | Description |
|---|---|
| `StartStateTreeCapture` 🧩 | Starts recording what one component's StateTree does over time, into a capture owned by the calling session, and returns its `CaptureId`. A recording is made from the engine's StateTree debug notifications. `Kinds` keeps only some of the entry kinds (default: all; an empty list or an unknown kind is `InvalidParams`); the kinds are `StateEntered`, `StateExited`, `StateCompleted`, `StateSelected`, `Transition` and `EventSent`. `MaxDurationSeconds` (1–600, default 120), `BufferCapacity` (64–16384, default 4096) and `ReplaceExisting` (default `false`) work as in `StartBehaviorTreeCapture`; a session records at most 8 StateTree components at once, a world holds at most 32 recording captures across all sessions, and a stopped capture is kept for 30 minutes. A tree that has not been started, or whose instance data is not initialized yet, can be recorded, and what it does once it starts is recorded. A recording stops by itself at `MaxDurationSeconds`, when the play session ends, when the component is destroyed or when it is set to run another tree (`TargetChanged`). **Fails with `NotAllowed`** at a moment that is not a safe point (call again once dialogs and loading have finished), when the component has no StateTree set (set one, then start again), and in a build whose engine provides no StateTree debug notifications (use an editor build, Development or DebugGame; the other commands are not affected). Fails with `NotFound` when the actor has no StateTree component |
| `GetStateTreeEventLog` 🧩 | Reads the entries of a capture, oldest first, from `SinceSequence` on (default 0). `CaptureId` (required) is the id `StartStateTreeCapture` returned. `MaxEntries` 1–4096 (default 256). Data holds the first 50 entries of the read; the artifact holds every entry of it, and `NextSequence` is the `SinceSequence` that continues after the artifact's last entry. `bGap` and `DroppedCount` work as in `GetBehaviorTreeEventLog`. The response also carries the capture's state, why it stopped, the recording seconds and `Limitations[]`. Works after the play session ended, and in a build whose engine provides no debug notifications. Fails with `NotFound` for an unknown, expired or foreign `CaptureId`, without telling which |
| `StopStateTreeCapture` 🧩 | Stops a capture and returns its final state: why it stopped, the recording seconds and the sequence bookkeeping. Stopping a capture that already stopped succeeds and keeps the reason it first stopped with (`Stopped`, `DurationLimit`, `WorldTornDown`, `Replaced`, `TargetDestroyed` or `TargetChanged`). Works after the play session ended; a session keeps at most 4 stopped captures and drops the oldest first. Fails with `NotFound` for an unknown, expired or foreign `CaptureId`, without telling which |

What the entry kinds mean — some differ from what their names suggest:

| `Kind` | Meaning |
|---|---|
| `StateEntered` / `StateExited` | A state was entered or left. Also recorded when the same state is selected again and nothing actually changes |
| `StateCompleted` | A state completed. One completion is recorded for every state on the active path |
| `StateSelected` | A state was selected. This is the notification at the time the selection was tried, and the selection may be cancelled afterwards. The state is named from the tree of the frame it was selected in; when that tree cannot be told for certain, or is a linked asset the recording did not register, the entry carries only the state's number and no name |
| `Transition` | A transition was taken: the source state (when known, `SourceState`), the target state, the `Trigger` kind (`OnStateCompleted`, `OnStateSucceeded`, `OnStateFailed`, `OnTick`, `OnEvent` or `OnDelegate`), the `RequiredEventTag` the transition is set up to wait for, the `Priority`, the `DelaySeconds`, and the `SourceType` (`Asset`, `ExternalRequest` or `Internal`). Starting or stopping the tree and a forced transition change the state without being recorded as a transition; only the entered and exited entries remain |
| `EventSent` | An event was sent to the tree: its `EventTag` and the type name of its payload (`EventPayloadType`). The payload value is never recorded |

The time a state has been active is not stored anywhere; compute it from the time of its `StateEntered` entry.

#### Fields in every StateTree response

| Field | Meaning |
|---|---|
| `CapturedAt`, `Frame`, `NetMode`, `WorldContext`, `PIEInstance`, `WorldTimeSeconds` | When and where the state was read, as for the behavior tree commands |
| `Actor`, `Component`, `TreeAssetPath` | The actor, the StateTree component and the tree asset that were observed |
| `Availability` | `Running`, `NotRunning` (the tree has not been started), `NoTree` (the component has no tree), `NotInitialized` (the instance data is not initialized), `Unreadable` (the component could not be read — no owner, being destroyed, or an internal engine item that is no longer there; not the same as `NotInitialized`), `ProjectDerivedComponent` or `NotAtSafePoint`. `AvailabilityReason` says why in words |
| `Limitations[]` | Caveats about what was returned, each with `Code` and sometimes `Detail` |

`Limitations[].Code` takes one of:

| `Code` | Meaning |
|---|---|
| `ProjectDerivedComponentNotVerified` | The component class is derived by the project. For an observation the state was not read; for a recording, nothing may be recorded if the class runs its tree under another owner or tree |
| `NotAtSafePoint` | The engine state may have been half updated, so it was not read |
| `EventSentMatchedByOwnerAndTree` | An event is matched to a recording by its owner and tree only, so an event sent to another run of the same tree on the same owner (several components, or the same tree run inside a behavior tree task) is recorded as well |
| `TriggeringEventNotRecorded` | The event that actually fired a transition is not recorded; a transition names only the event it is set up to wait for. The `EventSent` entry just before it is the clue |
| `NestedInstancedStructNotExpanded` | A struct of a kind chosen at run time inside a struct value is not expanded |
| `TreeNotStarted` | The tree has not been started, so there is no state to report |

While a StateTree recording runs, every StateTree debug notification in the process costs a small amount of work, so the StateTree runs that much slower, and the notifications of StateTrees running on several threads are handled one at a time. Record only what you need and stop the recording when it is done.

#### Errors

| ErrorCode | When |
|---|---|
| `InvalidParams` | A parameter is missing, of the wrong type, out of range or unknown; `Kinds` is empty or names an unknown kind; the actor has several StateTree components and `ComponentName` is missing (the candidates are listed) |
| `NotAllowed` | No play world is running, or none matches `TargetNetRole` / `TargetPIEInstance`; `StartStateTreeCapture` at a moment that is not a safe point, on a component with no tree, or in a build without StateTree debug notifications; a recording limit is reached, or the component is already recorded and `ReplaceExisting` is not set |
| `NotFound` | No actor matches the identifier; the actor and the controller or pawn it is paired with have no StateTree component; `ComponentName` matches none of the candidates; an unknown, expired, malformed or foreign `CaptureId` |
| `ExecutionFailed` | More than one actor matches the identifier; the artifact could not be written |
| `CapabilityNotAvailable` | `RuntimeInspect` or, for `DumpStateTreeInstanceData`, `StateTreeInstanceDataDump` is not granted |
| `PolicyViolation` | A required capability is denied by the safety policy |

Every successful call saves exactly one JSON artifact (the recording commands `StartStateTreeCapture` and `StopStateTreeCapture` save a supporting one); a failed call saves none.

---

## UAIP.Runtime.CommonUI 🧩

Observe the CommonUI state of a running game: the activatable widget containers (stacks and queues) and which widget each one shows, the input state CommonUI keeps for each local player (the input mode its action router applies, the front activated widget, the focus, the input type and the bound actions), and the texts the actions are displayed with. Requires the `CommonUI` plugin (and `EnhancedInput`, which CommonUI itself requires). If it is disabled the commands are not registered, and calling one returns `CommandNotFound` naming the plugin; `UAIP.Core.ListIntegrations` reports the state. A UAIP build made without CommonUI keeps the commands listed and refuses them with `UnavailableDetail: OptionalPluginDisabled`. Not provided in the demo build. All four accept [`TargetNetRole` / `TargetPIEInstance`](#choosing-which-play-world-a-runtime-command-acts-on) and reject unknown parameters. Works in PIE and in `-game` and packaged builds.

**Capabilities.** All four require `RuntimeInspect` (DefaultAllow). `GetActionDisplayNames` also requires `RuntimeWidgetTextRead` (DefaultDenied), because the texts are what the game shows — the same capability that gates the text of [game viewport widgets](#game-viewport-ui-and-hud-4). `DescribeActivatableWidgetsWithProjectCode` also requires `CommonUIProjectCodeExecution` (DefaultDenied). See [Safety & Capabilities](safety.md#runtime-commonui-observation).

**No project code by default.** The first three commands do not call functions a project may override: the getters of an activatable widget (the input configuration and the focus target it asks for) are left out, and every response names them in `ProjectCodeFields` (`Omitted`, `OmittedReason: "ProjectCodeExecutionRequired"`, `RequiresCapabilities: ["CommonUIProjectCodeExecution"]`, `Command`). The router's verdict is CommonUI's own check, even when the project derived the router. Two engine paths may still reach project code through a virtual function: the walk of the widget tree (a project widget that overrides how it lists its children) and the lookup of the activatable widget that owns a Slate widget (a project's own Slate metadata type). Only `DescribeActivatableWidgetsWithProjectCode` calls the overridable getters.

**`PlayerIndex` is the local player number.** `GetInputState` and `GetActionDisplayNames` number the **local players** of the game instance (0 is the first), as `PressGameViewportUIKey` does. `DumpInputState` and `EvaluateInputGateWithProjectCode` number the **player controllers** of the world instead, in this order: the players of this machine first (in the order of the game's local players), then the other players (in the order the game state lists them), and the world's own list of player controllers only when there are neither. A negative number is `InvalidParams`; a number no local player has is `NotFound`, and the message lists the numbers that exist. Left out, every local player is read.

| Command | Description |
|---|---|
| `DumpActivatableStacks` 🧩 | For each container: its kind and order, the local player that owns it (`OwningPlayerIndex`, `null` when unknown), whether its Slate widget is built and lies in the game layer, the activatable widget that holds it (`ParentActivatable`), the widget it shows (`ActiveWidget`, `ActiveWidgetIsActivated`), whether it is between two widgets (`IsTransitioning`, and `ActiveWidgetIsOutgoing` in the first half of a transition), the root content of a stack, and its entries in the order they were added (`IsDisplayed`, `IsActivated`, `IsModal`, `SupportsActivationFocus`, `AutoRestoresFocus`, `IsBackHandler`, `AutoActivate`). Activated widgets in no container are in `UncontainedActivatedWidgets`. Widgets and containers left out are counted by reason in `ExcludedCounts` (`PendingKill`, `DesignTime`, `NoWorld`, `OtherWorld`, and `Unconstructed` for a container not built yet). `IncludeUnconstructed` (default `false`) lists those containers too. Bounds: 64 containers, 256 entries per container (the displayed entry is always kept), 64 widgets in no container. `Result` holds the counts, `ExcludedCounts`, `Limitations` and the widget each of the first 16 containers shows |
| `GetInputState` 🧩 | For each local player: the action router's class (`RouterClass`, `RouterIsEngineBaseClass`), the input mode it applies (`InputMode`: `Menu`, `Game`, `All` or `NotApplied`), the mouse capture it applies, whether it is rebuilding its tree of activated widgets, `RouterAllowsGameInput` with the values it was decided from (`GameInputDecisionEvidence`), the activated widget CommonUI treats as the front one (`Leafmost`, UE 5.8 and later), the Slate user's actual focus (`Focus`) and whether it lies inside `Leafmost`, the input type (`InputType`, `RawInputType`, `GamepadName`, `IsUsingPointerInput`) and what the player controller ignores and shows. Once for the world: the game viewport's input state (`ViewportState`), its class, whether it derives from CommonUI's game viewport client, whether it is a verified engine class, and whether CommonUI's verdict is installed in the [injection gate](#the-injection-gate) (`GameInputGateContributorInstalled`). `IncludeActions` (default `false`) adds the actions bound for each player — name, identifier, input event, input mode, keys and the widget they are bound to — without display text. Bounds: 128 actions per player and 8 keys per action, counted separately for the normal and the hold keys. `Result` holds each player's index, status, input mode, `RouterAllowsGameInput` and the path of `Leafmost`, plus `ViewportClientIsCommonUIBased` and `Limitations` |
| `GetActionDisplayNames` 🧩 | The texts the bound actions are displayed with. Each action carries three texts, one per source: `ActionDisplayName` (the display name the binding carries), `LegacyRowDisplayName` (the display name of the data table row the action is defined by) and `InputActionDescription` (the description of the Enhanced Input action it is defined by); a source that has none is `null`. Which one the screen shows depends on the game, so the command does not choose. A row held by a data table whose class the project derived is not read (`LegacyRowNotReadFromProjectDataTable`). `ActionName`, `ActionIdentifier`, `InputEvent`, `InputMode` and `BoundWidget.WidgetPath` together match an action with the same action in `GetInputState`'s `Actions`; the two commands read at different moments, so an action can be in one and not the other. A player with no action router has `Status: "Unavailable"`. The texts are written to the artifact only: `Result` holds, for each player, its index, status and number of actions, and the limitations. Requires `RuntimeWidgetTextRead` |
| `DescribeActivatableWidgetsWithProjectCode` 🧩 | **Runs project code.** Calls the getters an activatable widget may override and returns `DesiredInputConfig` (`InputMode`, `MouseCaptureMode`, `MouseLockMode`, `HideCursorDuringViewportCapture`, `IgnoreMoveInput`, `IgnoreLookInput`; `null` when the widget asks for none) and `DesiredFocusTarget` (`null` when it names none; a target that is being destroyed or belongs to another world is left out with `DesiredFocusTargetExcludedReason`). `WidgetPaths` names the widgets by the `WidgetPath` `DumpActivatableStacks` returns: 1 to 32 entries, each a full object path that starts with `/`, holds no single quote or control character and is at most 1023 characters (otherwise the whole request is `InvalidParams`); repeats are kept, and a named widget is evaluated whether it is activated or not. Left out, every activated widget of the world is evaluated, the ones in the game layer first. Each target has `Status`: `Evaluated`, `NotEvaluated` (the command stopped before it), `NotFound`, or `Excluded` with `ExcludedReason` (`PendingKill`, `DesignTime`, `NoWorld`, `OtherWorld`). The world and the widget are checked again around every call: a widget that stops being activated is marked `DeactivatedDuringProjectCode` and still evaluated; a change of the world or the widget stops the command, which still succeeds with what it evaluated, `StoppedAt` naming the widget and the getter, and `ScreenChangedDuringProjectCode` (or `NotAtSafePoint`) in `Limitations`. Bound: 32 targets. Not a read-only command: refused under the read-only safety mode. Requires `CommonUIProjectCodeExecution`. Not in the Demo edition |

#### Fields in every CommonUI response

| Field | Meaning |
|---|---|
| `CapturedAt`, `Frame`, `NetMode`, `WorldContext`, `PIEInstance` | When and where the state was read |
| `Availability` | `NotAtSafePoint` when the engine state may be half updated (a modal dialog or a long task holds the game loop, or the world is in the middle of its tick): nothing is read, the command succeeds and no lists are returned. Call again |
| `WidgetPath` | On every widget. `FindGameViewportWidgets` takes it as `WithinWidgetPath` to search inside that widget |
| `TypePath`, `Fingerprint` | On a built widget in the game layer. The [game viewport UI input](#game-viewport-ui-input-3) commands take them as a target. Left out, with `InGameLayer`, when the root of the game layer cannot be resolved (`GameLayerRootUnresolved`) |
| `ProjectCodeFields` | The fields only project code can produce and the capability and command that produce them |
| `XTruncated`, `XTotalCount` | Present only on a list that was cut, with the count before the cut |
| `ActionDisplayNameTruncated`, `LegacyRowDisplayNameTruncated`, `InputActionDescriptionTruncated` | A text was cut. Texts are cleaned of control characters and cut to 256 characters |
| `Limitations[]` | Caveats about what was returned, each with `Code` and sometimes `Detail` |

`Limitations[].Code` takes one of:

| `Code` | Meaning |
|---|---|
| `NotAtSafePoint` | The engine state may have been half updated, so it was not read (or, for `DescribeActivatableWidgetsWithProjectCode`, the engine left its safe point while project code ran) |
| `GeometryFromPreviousFrame` | Positions and sizes come from the last frame that was laid out |
| `GameLayerRootUnresolved` | The root of the game layer could not be resolved; `InGameLayer`, `TypePath` and `Fingerprint` are left out |
| `TransitionStateUnavailable` | Whether a container is between two widgets could not be read |
| `ReflectedFieldUnavailable:<field>` | An engine field read by name was not found on this engine version; what depends on it is left out |
| `NoLocalPlayers` | The world has no local player |
| `SlateUnavailable` | Slate is not initialized (for example in a process without rendering) |
| `LeafmostUnavailableOnThisEngineVersion` | UE 5.7: the engine does not expose the front activated widget, so `Leafmost` is left out |
| `InputModeNotEnforced` | The game viewport client does not derive from CommonUI's, so CommonUI's input mode is not applied on the path game input takes |
| `GameInputGateContributorNotInstalled` | CommonUI's verdict is not part of the injection gate in this process |
| `ViewportClientOverridesNotEvaluated` | The game viewport client is a project class; its overrides were not run, so the viewport values are the engine's implementation |
| `ScreenChangedDuringProjectCode` | The world or a widget changed while project code ran, and the command stopped |
| `LegacyRowNotReadFromProjectDataTable` | A data table row was not read because the table's class is derived by the project |

#### Errors

| ErrorCode | When |
|---|---|
| `InvalidParams` | A parameter is of the wrong type, out of range or unknown; an entry of `WidgetPaths` breaks the rules above |
| `NotAllowed` | No play world is running, or none matches `TargetNetRole` / `TargetPIEInstance`; for `DescribeActivatableWidgetsWithProjectCode`, a modal dialog is open or the engine tick is starved |
| `NotFound` | `PlayerIndex` names no local player (the message lists the numbers that exist) |
| `CapabilityNotAvailable` | A required capability is not granted |
| `PolicyViolation` | A required capability is denied by the safety policy; `DescribeActivatableWidgetsWithProjectCode` under the read-only safety mode |
| `CommandNotFound` | The `CommonUI` plugin is disabled; in the Demo edition |

In a packaged game from a Fab-distributed UAIP installed in the engine, the optional integrations are never built in, and the four commands are listed and refused with `OptionalPluginDisabled`, as for the other optional integrations; place UAIP in the project's `Plugins` folder so it is compiled with the project. See [Capability reference](safety.md#capability-reference).

---

## UAIP.Runtime.ChaosDestruction

Observe the Chaos destruction of a running game: which Geometry Collection components the world holds and how broken each one is, the state of every piece, the physics fields that act on the world, a time series of destruction events, and the strain each piece carries. Nothing here changes what is destroyed: the observation commands only read, and the one command that turns a game notification on (`EnableForcedDestructionNotify`) is described separately below. Works in the editor while PIE is running, and in `-game` and packaged builds; no plugin requirement.

**Capabilities.** All commands require `RuntimeInspect` (DefaultAllow). `EnableForcedDestructionNotify` also requires `ChaosDestructionForceNotify` (DefaultDenied). A missing one is `CapabilityNotAvailable`. See [Safety & Capabilities](safety.md#runtime-chaos-destruction).

**Demo build.** `EnableForcedDestructionNotify` and the `ChaosDestructionForceNotify` capability are not provided in the demo binary; the other seven commands are. In the demo the command is absent and returns `CommandNotFound`.

**Play world.** `ListGeometryCollections`, `DumpGeometryCollectionState`, `DumpChaosFieldState`, `StartDestructionCapture` and `CaptureGeometryCollectionStrain` accept [`TargetNetRole` / `TargetPIEInstance`](#choosing-which-play-world-a-runtime-command-acts-on). The three capture commands that take a `CaptureId` (`GetDestructionEventLog`, `StopDestructionCapture`, `EnableForcedDestructionNotify`) address a capture, not a world.

**A destruction notification may be off in the game.** Geometry Collection components report breaks, crumblings, collisions and removals only when the game turned the matching notification on, and the engine default is off. The state commands (`ListGeometryCollections`, `DumpGeometryCollectionState`) read the pieces directly and are not affected. A capture still records the piece-level events it detects by sampling, and reports in each response's `Coverage` which event kinds it could and could not record and why. To record the engine's own event data without changing the game, see `EnableForcedDestructionNotify`.

### Current state (3) — requires `RuntimeInspect`

| Command | Description |
|---|---|
| 🆓 `ListGeometryCollections` | Lists the Geometry Collection components of the target play world, one entry per component, ordered by actor path and then component name. Each entry holds the actor, the component, the rest collection asset, the number of transforms, whether the root broke and for how long, the piece counts per state, the notification flags as the game set them and the availability of the component. `StartIndex` (default 0) and `MaxEntries` 1–4096 (default 256) select the page; `IncludeClassification: false` leaves the piece counts out (default `true`). Data holds the first 50 entries of the page; the artifact holds the whole page, and `NextStartIndex` points past it while more components remain. At most 262144 transforms are classified per command; components beyond that are listed with `ClassificationSkipped` and no counts. A component without a physics state is listed with the reason it cannot be read, not as an error |
| 🆓 `DumpGeometryCollectionState` | Dumps one Geometry Collection component: the component summary with the other components of the same actor, the piece counts per hierarchy level, the pieces with state (Active, Broken, Decayed, ClusterReleased), dynamic state, location, rotation and velocity, the damage settings, the transforms the asset anchors and the fields that initialize the component. `ActorIdentifier` (required) names the actor by label or object name, and `ComponentName` the component when the actor holds more than one. `Indices` (1–4096 transform indices) and `States` (any of `Sleeping`, `Kinematic`, `Static`, `Dynamic`, `Broken`, `Decayed`, `ClusterReleased`, `Active`, `Inactive`, ignoring case) restrict the pieces; `StartIndex` and `MaxEntries` 1–4096 (default 256) select the page; `IncludeTransforms` and `IncludeVelocities` (default `true`) leave the location and rotation, or the velocities, out. Data holds the first 50 pieces of the page; the artifact holds the whole page, and `NextStartIndex` points past it while more pieces remain. Why a piece is kinematic or static (asset, field or script) cannot be told apart. A component without a physics state is dumped with the reason it cannot be read, not as an error |
| 🆓 `DumpChaosFieldState` | Dumps the fields that act on the target play world: the persistent, construction and last-tick transient commands of the world's physics field with their physics type, target attribute, source actor name, bounds, magnitude, center, meta data and node tree, and the field system actors placed in the level with the commands they hold. Each kind is bounded by `MaxEntries` 1–4096 (default 256) on its own and reported with its total count and whether it was cut; `IncludeNodeTrees: false` leaves the node trees out (default `true`). Data holds the first 50 entries of each list and the artifact holds all that `MaxEntries` allows. A world whose physics field is disabled returns success with empty command lists and the reason, and still lists the field system actors. Fields that exist only on the GPU are not observable |

### Event capture (3) — requires `RuntimeInspect`

A capture belongs to the session that started it: another session sees `NotFound` for its id, without being told whether it exists.

| Command | Description |
|---|---|
| 🆓 `StartDestructionCapture` | Starts recording the destruction of the target play world into a capture owned by the calling session, and returns its `CaptureId`. The capture records the Geometry Collection components named in `Targets` (1–64 objects, each with `ActorIdentifier` and optionally `ComponentName`), or every component of the world — including the ones that appear later — when `Targets` is left out, until `StopDestructionCapture` is called, `MaxDurationSeconds` of wall clock time pass (1–600, default 120), or the play session ends. `Kinds` picks the event kinds to record, from `RootBroken`, `ClusterReleased`, `PieceBrokenOff`, `PieceDecayed`, `AnchorReleased`, `PieceStateChanged`, `CollectionReset`, `Break`, `Crumble`, `Removal`, `Collision` and `FieldApplied`; the default is every kind except `PieceStateChanged`. `BufferCapacity` (64–16384, default 4096) is the number of events kept before the oldest are dropped and counted. A world holds at most 8 recording captures and 65536 tracked transforms across all sessions, and a session records at most one capture per world; `ReplaceExisting: true` stops that capture and starts a new one (default `false`, which refuses the start and names the capture). Collections beyond the transform budget are left untracked and reported in `Coverage` and `Limitations`. Fails with `PreconditionFailed` when the world has no physics scene or solver |
| 🆓 `GetDestructionEventLog` | Reads the events of a capture, oldest first, from `SinceSequence` on (default 0). `CaptureId` (required) is the id `StartDestructionCapture` returned. Works after the play session ended: a stopped capture keeps its events for 30 minutes, and a session keeps its four most recent stopped captures. `MaxEntries` 1–4096 (default 256) bounds the events read. Data holds the first 50 events of the read; the artifact holds every event of it, and `NextSequence` is the `SinceSequence` that continues after the artifact's last event. `Gap` is true when events at or after `SinceSequence` were dropped before they could be read. The response also carries the state of the capture, why it stopped, the tracked collections and transforms, the sampled frames, the recording seconds and the coverage of each event kind. Events from different sources are not guaranteed to be in causal order. Fails with `NotFound` for an unknown, expired or foreign `CaptureId`, without telling which |
| 🆓 `StopDestructionCapture` | Stops a capture and returns its final state: why it stopped, the tracked collections and transforms, the sampled frames, the recording seconds, the sequence bookkeeping and the coverage of each event kind. Stopping a capture that already stopped succeeds and keeps the reason it first stopped with (`Stopped`, `DurationLimit`, `WorldTornDown` or `Replaced`). Works after the play session ended; the stopped capture keeps its events for 30 minutes, during which `GetDestructionEventLog` can still read them. Fails with `NotFound` for an unknown, expired or foreign `CaptureId`, without telling which |

A capture that is left running stops by itself at `MaxDurationSeconds`, and when the play world is torn down.

### Strain snapshot (1) — requires `RuntimeInspect`

| Command | Description |
|---|---|
| 🆓 `CaptureGeometryCollectionStrain` | Captures the strain of the pieces of one Geometry Collection component on the next physics step: for each piece, the internal strain (the strength it has left before it breaks off its parent, or `Unbreakable`), the collision impulse of the previous step (or `ForcedBreakMarker`), the external strain, the largest applied value, the margin and whether the piece would break, next to the damage settings of the component. `ActorIdentifier` (required) and `ComponentName` name the component as in `DumpGeometryCollectionState`; `Indices` (1–4096), `StartIndex` and `MaxEntries` 1–4096 (default 256) select the pieces. The command waits for the physics step for up to `TimeoutSeconds` (above 0, up to 60, default 5), checking every `PollIntervalSeconds` (0.05–1, default 0.05), and is refused with `NotAllowed` while the game is paused. Data holds the first 50 pieces of the page; the artifact holds the whole page. Internal clusters, which have no transform index, are not reported. A component that has no physics proxy or simulates in a solver other than the default one is reported with the reason and its damage settings, not as an error. On timeout the response carries `Result` with `Executed` false and whether the game was paused |

### Forcing a destruction notification on (1) — requires `RuntimeInspect` and `ChaosDestructionForceNotify`

Not provided in the demo build.

| Command | Description |
|---|---|
| `EnableForcedDestructionNotify` | Turns on the destruction notifications named in `Kinds` (`Breaks`, `Crumblings`, `Collisions`, `Removals`; ignoring case; each at most once) of the Geometry Collection components that a recording capture of the calling session tracks on the default physics solver, including the components the capture starts tracking later, until that capture stops. `CaptureId` (required) names the capture. The events those notifications produce (mass, velocity and bounds of broken pieces, the children a crumbling released, collision partners and impulses) are recorded by that capture only; other captures of the same world see the game's own settings. Only a notification whose event kind the capture records can be forced (`Breaks` as `Break`, `Crumblings` as `Crumble`, `Collisions` as `Collision`, `Removals` as `Removal`); any other is refused with `InvalidParams` and nothing is forced. Calling it again for the same capture adds kinds. A notification the game already has on is left untouched. Returns the capture's status: `Coverage` marks the cells this capture forced with `ForcedByUAIP`, and `Limitations` carry `ForceNotifySideEffects`. Refused in read-only mode. Fails with `NotFound` for an unknown, expired or foreign `CaptureId`, and with `NotAllowed` for a capture that already stopped. ⚠️ Side effects and what cannot be undone — see [Forced destruction notifications](#forced-destruction-notifications) |

#### Forced destruction notifications

- **The game's own listeners receive the events too.** While a notification is forced, every listener the game registered for it gets its events, not only the capture. The engine also unregisters and re-registers every Chaos event of the component each time a notification is turned on and when it is restored, so a listener registered through a different path can be affected.
- **Part of it cannot be undone.** Turning a notification on raises the solver's event filters, which the engine has no way to lower. The solver keeps producing that event data until the play session ends, even after the capture stops.
- **Restoring.** When the capture stops (by `StopDestructionCapture`, its duration limit, a replacement or the end of the session), each notification no capture forces any more is restored if it still carries the forced value. A notification the game turned off in the meantime is left as the game set it; one the game wrote back on cannot be told apart and is restored as well. Nothing is restored when the play world is torn down.
- **Collisions are not forced on components with collision profiles of their own** (per-particle or per-level collision profiles, or the abandoned-particle profile of a replicated component). Forcing would overwrite those profiles until the physics state is recreated, so for such a component `Collisions` is accepted but its coverage reads `NotGenerated` with `ForceNotSupported`, and its collision setup is left alone. Other components of the same capture, and the other notification kinds, are still forced.

See [Safety & Capabilities](safety.md#runtime-chaos-destruction) for how the capability is granted.

#### Fields in every response

Each response says when and where it was read: the capture or play world that was observed, the frame and the time. Anything that could not be filled is listed rather than left out silently: `Limitations[]` carries caveats about what was returned, each with a `Code`, and capture responses carry `Coverage[]`, one cell per event kind and collection, saying whether the events of that kind could be recorded.

Parameters are checked before the play world is looked up, so a malformed request is refused with `InvalidParams` even when PIE is not running. An unknown key, a wrong JSON type, an out-of-range value or an empty array is `InvalidParams`.

Every successful call saves exactly one JSON artifact; a failed call saves none.

---

## UAIP.Runtime.Navigation

Observe the navigation mesh and path finding of a world: whether the navigation system exists and how it is set up, whether one point can be reached from another and why not, the path itself with its cost per area, the tiles of the mesh, the modifiers that shape it, what an AI is doing on its path, and whether a rebuild of the mesh has settled. Seven commands only observe; the eighth (`RebuildNavigation`) queues a regeneration of the mesh and is described separately below. Works in the editor (with or without PIE running), and in `-game` and packaged builds; no plugin requirement.

**Capabilities.** Seven commands require `RuntimeInspect` (DefaultAllow). `RebuildNavigation` requires `RuntimeNavigationRebuild` (DefaultDenied). `FindPath` and `IsLocationReachable` additionally need `RuntimeNavigationExtendedSearch` (DefaultDenied) **only when `MaxSearchNodes` is above 8192**; that capability is checked per request and does not appear in the command's declared `RequiredCapabilities`. A missing one is `CapabilityNotAvailable` naming it. See [Safety & Capabilities](safety.md#runtime-navigation).

**Demo build.** `RebuildNavigation` and the `RuntimeNavigationRebuild` capability are not provided in the demo binary; the other seven commands are. In the demo the command is absent and returns `CommandNotFound`.

**Which world is read.** `DumpNavigationSystemState`, `FindPath`, `IsLocationReachable`, `DumpNavMeshTiles`, `QueryNavModifiers` and `WaitForNavigationBuild` read the play world when one is running and the editor world otherwise — a navigation mesh is generated and saved in the editor, so it can be checked without starting PIE. `GetPathFollowingState` (AI controllers exist only in a play world) and `RebuildNavigation` (it never changes the editor level) act on a play world only. All eight accept [`TargetNetRole` / `TargetPIEInstance`](#choosing-which-play-world-a-runtime-command-acts-on); naming a play world that does not exist is `NotAllowed`, it never falls back to the editor world.

### Observation (6) — requires `RuntimeInspect`

| Command | Description |
|---|---|
| 🆓 `DumpNavigationSystemState` | The state of the navigation system of the target world. Takes no parameters besides the play world selector. The response carries `NavDataCount` and `NavData[]` (at most 64: `Name`, `IsMain`, `IsRecast`, `HasValidNavMesh`, `AgentName`, `AgentRadius`, `AgentHeight`, `StepHeight`, `MaxSlopeDegrees`, `RuntimeGeneration` (`Static`, `DynamicModifiersOnly` or `Dynamic`), `ActiveTilesOnly`, `TileCount`, `TilePoolCapacity` and `GenerationParameters` such as `CellSize`, `CellHeight`, `TileSizeUU`, `TilePoolSize`), the three kinds of bounds — `NavigationBounds[]` (the volumes registered with the system, at most 256), `NavigableBounds` (what each navigation data is meant to cover) and `NavMeshBounds` (what the generated mesh covers) —, `Areas[]` (at most 64, with `DefaultCost` and `FixedAreaEnteringCost`), `BuildState` and `SearchLimits`. `SearchLimits` tells how far a path query may search: `DefaultCeiling` (8192), `ExtendedCeiling` (65534), `ExtendedSearchCapability` (the name of the capability that raises the ceiling), `ExtendedSearchGranted` (whether the calling session holds it) and `EngineDefaultMaxSearchNodes`. The artifact holds every item |
| 🆓 `FindPath` | A path between two points and whether the end point can be reached. Each point is a location (`StartLocation` / `EndLocation`) or an actor (`StartActor` / `EndActor`); `AgentActor` (a pawn or its controller) lends the query its owner, its navigation data and its default filter, and stands in for a missing start point. The response carries `Reachable` (`true`, `false`, or `null` when it cannot be told), `Reason` (see [Reading a reachability answer](#reading-a-reachability-answer)), `Result`, `QueryConditions` (what the query actually used: `Owner`, `NavData`, `Filter{Class, Source, QuerierPresent}`, `StartSource`, `EndSource`, `RequireNavigableEndLocation`, `AllowPartialPath`, `MaxSearchNodes{Value, Source, Ceiling}`), and, for the reasons that produce a path, `IsPartial`, `Length`, `Cost`, the first 50 `PathPoints` with `PathPointsTotalCount`, and `AreaBreakdown[]` (cost and length contributed by each area along the path, `Traversable: false` with an `ExclusionSource` for an area that is excluded). When a point could not be projected onto the mesh, `StartProjection` / `EndProjection` say which one failed and, in `TileExistsAtLocation`, whether a tile exists there. The artifact holds up to `MaxPathPoints` points and the corridor |
| 🆓 `IsLocationReachable` | The same question as `FindPath` with the same parameters (except `MaxPathPoints`) and the same answer for `Reachable`, `Reason`, `QueryConditions` and the projection of a point that failed to land, but without the path, its length, cost and area breakdown |
| 🆓 `DumpNavMeshTiles` | The tiles of one navigation mesh in (X, Y, Layer) order: `X`, `Y`, `Layer`, `Bounds`, `Resolution` and `PolygonCount` of each. `Box` limits the list to the tiles that overlap it; `NavDataName` picks the navigation data (default: the main one); `MaxTiles` is 1–4096 (default 256). The response carries the first 50 `Tiles[]` and `TotalCount` (exact, counted before `MaxTiles` was applied); the artifact holds every listed tile. The polygon count is read only for the tiles that are listed |
| 🆓 `QueryNavModifiers` | The navigation modifiers that touch the required `Box`, and how the polygons of the mesh in that region are divided among areas. Each modifier carries its source (`Name`, `Path`, `Label`), its `Bounds`, its area class, the area class it replaces, its `Shape` and `ApplyMode`; a modifier the engine has not gathered yet is marked `PendingLazyGathering` and carries the `DeclaredAreaClass` its component declares. `AreaBreakdown` counts polygons per area, up to `MaxPolygons` (1–16384, default 4096); `AreaBreakdown.CountComplete: false` means the counts are lower bounds. `MaxModifiers` is 1–4096 (default 256). The response carries the first 50 modifiers and `TotalCount`; the artifact holds every captured modifier |
| 🆓 `GetPathFollowingState` | What the path following component of one AI is doing, in a play world only: `Status` (`Idle`, `Waiting`, `Paused` or `Moving`), `HasPath`, `RequestId`, the goal (`GoalLocation` is the end of the path it follows, even when `PathPoints` is cut short, and is left out when it holds no path; `MoveGoal` is the actor it moves to, when it moves to one), the end of the segment it is heading to (`CurrentTargetLocation`), the segment it is on (`CurrentPathIndex`, `NextPathIndex`), `AcceptanceRadius`, `HasPartialPath`, the navigation data the path was made with (`NavDataUsed`), the first 50 `PathPoints` and the `AreaBreakdown[]` of the path. `ActorIdentifier` (required) names the pawn or its AI controller. `MaxPathPoints` is 1–4096 (default 256) and bounds the points written to the artifact. While the navigation system or the mesh is unavailable the follow state is still returned and only the area breakdown is left out |

### Waiting (1) — requires `RuntimeInspect`

| Command | Description |
|---|---|
| 🆓 `WaitForNavigationBuild` | Waits until the navigation system of the target world is quiescent: no generation task remains and no dirty area waits to be processed. The command only observes — it polls and never drives the world — and it is a passive wait, so it does not hold the transport's single command slot. `TimeoutSeconds` is greater than 0 and at most 60 (default 30); `PollIntervalSeconds` is 0.05–1.0 (default 0.1). `WaitOutcome` is `NotApplicable` (the world has no navigation system or no valid navigation data), `AlreadyQuiescent` (nothing was being built), or `Quiescent` (it settled while waiting); when `TimeoutSeconds` passes first the command fails with `Timeout` and still returns the result and the artifact. The response carries `CompletionScope: "NavigationSystemQuiescent"`, `ElapsedSeconds`, `BuildStateAtStart`, `BuildStateAtEnd` and `World`. **What a finished wait guarantees** is that the whole navigation system is quiescent, never that a particular region is finished; the engine also holds back some updates that cannot be observed (`Limitations: UnobservablePendingUpdates`), so generation may start right after the check |

### Queuing a rebuild (1) — requires `RuntimeNavigationRebuild`

Not provided in the demo build.

| Command | Description |
|---|---|
| `RebuildNavigation` | Queues a regeneration of the navigation mesh of the target **play** world and answers at once, without waiting for it (`IsReadOnly` is false). Without `Box` every registered navigation bounds is queued; with `Box` only that region is. The response carries `Queued`, `Scope` (`Full` or `Box`), `QueuedAreaCount`, `NextStep: "WaitForNavigationBuild"` — run that command afterwards and query again once it reports the system quiescent —, `BuildState` and, for every navigation data, `Eligible` (whether the rebuild covers it), `GeometryRebuild` (whether its geometry is rebuilt; `DynamicModifiersOnly` reapplies the modifiers only) and `ActiveTilesOnly` (whether only the active tiles around invokers or loaded World Partition cells are rebuilt). Fails with `PreconditionFailed`, queuing nothing, when the world has no navigation system, has nowhere to build, or has no navigation data that regenerates while the game runs (`Static`); the `ErrorMessage` starts with the reason (`NavigationSystemMissing`, `NothingToBuild` or `NoRuntimeGeneration`) and explains it, and the failure carries no `Data`. A build lock, a paused world, a region outside every navigation bounds and a queue the build state does not show are reported in `Limitations[]`, not as failures. The artifact repeats the response; a failed save leaves the command successful |

#### Parameters

| Parameter | Commands | Meaning |
|---|---|---|
| `StartLocation` / `EndLocation` | `FindPath`, `IsLocationReachable` | `{X, Y, Z}` world location. Exclusive with `StartActor` / `EndActor` respectively. Coordinates must be finite and within ±2097152 |
| `StartActor` / `EndActor` | `FindPath`, `IsLocationReachable` | Label or object name of the actor the path starts or ends at (1–256 characters, no control characters): its navigation agent location when it is a navigation agent, its location otherwise |
| `AgentActor` | `FindPath`, `IsLocationReachable` | Label or object name of a pawn, or the controller of one. Lends the query its owner, its navigation data and its default filter, and stands in for a missing `StartLocation` / `StartActor`. Exclusive with `NavDataName`. A controller without a pawn, or a pawn that is not a navigation agent, is `InvalidParams` |
| `NavDataName` | `FindPath`, `IsLocationReachable`, `DumpNavMeshTiles`, `QueryNavModifiers` | Object name of the navigation data to use (1–256 characters). Left out, the main navigation data is used. A name that matches none is `InvalidParams` and lists the names that exist |
| `FilterClass` | `FindPath`, `IsLocationReachable` | Full class path of the navigation query filter, for example `/Script/MyGame.MyQueryFilter`. Only an already loaded class is accepted; nothing is loaded. Left out, the default filter of the agent (or of the navigation data) is used |
| `RequireNavigableEndLocation` | `FindPath`, `IsLocationReachable` | Boolean, default `true`. Whether an end point outside the mesh fails the query |
| `AllowPartialPath` | `FindPath`, `IsLocationReachable` | Boolean, default `true`. Whether a path that stops short of the end point is accepted |
| `MaxSearchNodes` | `FindPath`, `IsLocationReachable` | Integer 4–65534. Left out, the filter's own count is used, capped at 8192 without `RuntimeNavigationExtendedSearch` and raised to 4 when it is lower (both reported as `Limitations: SearchNodesClamped`). A value above 8192 needs the capability; a value above 65534, or below 4, is `InvalidParams` whatever the session holds. Fewer than 4 nodes would make the navigation mesh write outside its search node pool. `QueryConditions.MaxSearchNodes.Value` reports the count the query actually ran with |
| `MaxPathPoints` | `FindPath`, `GetPathFollowingState` | Integer 1–4096, default 256. Path points written to the artifact |
| `Box` | `DumpNavMeshTiles` (optional), `QueryNavModifiers` (required), `RebuildNavigation` (optional) | `{Min: {X, Y, Z}, Max: {X, Y, Z}}`. `Min` must not exceed `Max` on any axis (the corners are never swapped for you) and the box needs a width on X and Y; a zero height is allowed |
| `MaxTiles` | `DumpNavMeshTiles` | Integer 1–4096, default 256 |
| `MaxModifiers` | `QueryNavModifiers` | Integer 1–4096, default 256 |
| `MaxPolygons` | `QueryNavModifiers` | Integer 1–16384, default 4096. Polygons counted for the area breakdown |
| `ActorIdentifier` (required) | `GetPathFollowingState` | Label or object name of the pawn or AI controller |
| `TimeoutSeconds` / `PollIntervalSeconds` | `WaitForNavigationBuild` | Numbers; see the command above |

A start point is exactly one of `StartLocation`, `StartActor`, or — when neither is given — the pawn of `AgentActor`; an end point is exactly one of `EndLocation` and `EndActor` (`AgentActor` never stands in for it). Giving both forms of a point, none at all, or both `AgentActor` and `NavDataName` is `InvalidParams`. Booleans must be JSON booleans, limits JSON integers; anything else, an unknown key or a value out of range is `InvalidParams`. Parameters are checked before the play world is looked up, so a malformed request is refused even when PIE is not running.

#### Fields in every response

| Field | Meaning |
|---|---|
| `CapturedAt` / `Frame` | When the state was read (ISO 8601, UTC) and the engine frame number at that moment |
| `NetMode` / `WorldContext` / `PIEInstance` | The world that was read. `WorldContext` is `PIE`, `Editor` or `Game`; `PIEInstance` is omitted outside PIE |
| `WorldPartitioned` | Whether the observed world uses World Partition |
| `Availability` | `State`: `Available`, `Degraded` or `Unavailable`. `Reason` is one of `NavigationSystemMissing` (with `Detail`: `ClientWorld` and the server side play worlds in `ServerCandidates[]` to retry against, `NoNavigationSystemConfig`, or `Unknown`), `NoNavigationData`, `NoNavigationDataForAgent`, `NavMeshNotBuilt`, or — `DumpNavigationSystemState` only, when some but not all navigation data has a mesh — `SomeNavDataNotBuilt` (`Degraded`) |
| `BuildState` | `RemainingTasks`, `RunningTasks`, `DirtyAreasQueued`, `Locks[]` (`NoUpdateInEditor`, `NoUpdateInPIE`, `InitialLock`, `Custom`, and `AsyncLoadLock` on UE 5.8), `AutoUpdateEnabled`, `WorldPaused`, `Quiescent`. Left out when there is no navigation system |
| `DegradedSections[]` | Parts of the result that could not be filled, each with `Section` and `Cause` (`NavigationUnavailable`, `SomeNavDataNotBuilt` or `UnreadableField`) |
| `Limitations[]` | Caveats about what was returned, each with a `Code` and a `Detail` (see below) |

A world without a navigation system, or whose navigation data has no generated mesh, is **not** an error for the observation commands: they succeed, leave out the items that come from the navigation system and say why in `Availability`. A name given in `NavDataName` or `FilterClass` is then not compared with anything (`Limitations: SelectionNotEvaluated`), so it is never reported as wrong input there. A value that cannot be determined is left out rather than filled with a default.

#### Reading a reachability answer

`Reachable` is three-valued, and `null` is not "no": `SearchLimitReached`, `Unknown`, `NavigationUnavailable` and `NavMeshNotBuilt` mean the question could not be settled. `Reason` is the first row that applies:

| `Reason` | `Reachable` | Meaning |
|---|---|---|
| `NavigationUnavailable` | `null` | The world has no navigation system or no valid navigation data. No path was computed |
| `NavMeshNotBuilt` | `null` | The selected navigation data has no generated mesh. No path was computed |
| `StartNotOnNavMesh` | `false` | The start point could not be projected onto the mesh |
| `EndNotOnNavMesh` | `false` | The end point could not be projected onto the mesh (not with `RequireNavigableEndLocation: false`) |
| `Reachable` | `true` | A complete path exists. When start and end are almost the same point the path is one point of length 0 |
| `SearchLimitReached` | `null` | The search ran out of nodes. `IsPartial` is true and the path is what was explored; raise `MaxSearchNodes` (needs `RuntimeNavigationExtendedSearch` above 8192) |
| `PartialPathOnly` | `false` | Only a path that stops short exists and `AllowPartialPath` is true. The partial path is returned |
| `NoPath` | `false` | No path, or only a partial one while `AllowPartialPath` is false. No path is returned |
| `Unknown` | `null` | The path finder gave an answer that fits none of the above |

`StartNotOnNavMesh` / `EndNotOnNavMesh` report in `StartProjection` / `EndProjection` which point failed (`Projected: false`) and, in `TileExistsAtLocation`, whether a tile exists there — a missing tile points at a World Partition region that is not loaded rather than at a bad coordinate.

Without `AgentActor` the query has no querier, so a filter other than the default of the navigation data is initialised without one and meta filters are not resolved; the response then carries `Limitations: QuerierlessFilter`. Pass `AgentActor` to see the result an AI would get. An area an AI cannot enter is shown as `Traversable: false` with `ExclusionSource` `AreaCost`, `AreaFlags` or `NullArea`, never as a huge cost.

#### Limitations codes

| Code | Meaning |
|---|---|
| `UnreadableField` | A field could not be read from the engine and was left out |
| `CountIncomplete` | A `TotalCount` is a lower bound (its `CountComplete` is false) |
| `SelectionNotEvaluated` | The navigation system or its data is unavailable, so `NavDataName` / `FilterClass` was not compared with anything |
| `NonRecastNavData` | A navigation data is not a Recast mesh; mesh-specific items are left out |
| `DefaultAgentNameUnreadable` | The engine's default agent name could not be read, so the main navigation data was chosen without it |
| `QuerierlessFilter` | The filter was initialised without a querier (see above) |
| `SearchNodesClamped` | The filter's own search node count was above 8192 and was lowered, or below 4 and was raised; `Detail` holds the filter's value and the count used, plus, when lowered, the ceiling and the capability that lifts it |
| `ActivePathRegistered` | In the editor world the query registered its path with the navigation data, which is not cleaned up there |
| `StaleCorridor` | Part of the path corridor refers to a tile that has been rebuilt since; those entries are marked `Valid: false` |
| `DeclaredAreaUnreadable` | The area a modifier component declares could not be read |
| `UnobservablePendingUpdates` | The engine holds back updates that cannot be observed, so generation may start right after a quiescent answer |
| `NavMeshNotBuiltAtQuiescence` | The system is quiescent but a navigation data still has no mesh; `Detail` names it |
| `BuildLocked` | A build lock is set; `Detail` names it. Queued areas are processed after it is released |
| `WorldPaused` | The world is paused; queued areas may not be processed meanwhile |
| `AutoUpdateDisabled` | Automatic updates are off in the editor world; dirty areas may be discarded and the system can look quiescent without having generated anything |
| `OutsideNavigationBounds` | `RebuildNavigation`: the `Box` lies outside every registered navigation bounds |
| `ModifiersOnlyRebuild` | `RebuildNavigation`: a navigation data reapplies modifiers only (`DynamicModifiersOnly`) |
| `ActiveTilesGenerationOnly` | `RebuildNavigation`: a navigation data regenerates only the tiles that are active |
| `QueueNotObserved` | `RebuildNavigation`: the build state read right after queuing showed no queued area, so the engine may have discarded the request; `Detail` holds the number of areas queued |

#### Bounds on the output

`Data` carries at most the first 50 entries of a list; the artifact holds the whole captured list. Counts are bounded as follows: tiles and modifiers 4096, path points 4096, navigation data 64, registered bounds 256, areas 64. A list cut by its bound reports its `TotalCount`; inner arrays are cut at 64 entries with `Truncated`. The cost of a request is bounded as well: polygons processed (`MaxPolygons`) and search nodes (8192, or 65534 with `RuntimeNavigationExtendedSearch`).

#### Errors

| ErrorCode | When |
|---|---|
| `InvalidParams` | A parameter is missing, of the wrong type, out of range or unknown; the exclusive combinations above; a `NavDataName` that matches none (the message lists the names that exist); a `FilterClass` that is not loaded or not a navigation query filter; `MaxSearchNodes` above 65534 or below 4; `TargetNetRole` / `TargetPIEInstance` cannot be honoured |
| `CapabilityNotAvailable` | `RuntimeInspect`, `RuntimeNavigationRebuild` (for `RebuildNavigation`) or, for `MaxSearchNodes` above 8192, `RuntimeNavigationExtendedSearch` is not granted. The message names it |
| `PolicyViolation` | The capability is denied explicitly in the safety policy |
| `NotAllowed` | No play world is running for a command that needs one, or none matches `TargetNetRole` / `TargetPIEInstance` |
| `NotFound` | `StartActor`, `EndActor`, `AgentActor` or `ActorIdentifier` matches no actor; for `GetPathFollowingState`, the actor is not driven by an AI controller, or its AI controller has no path following component (each with its own message) |
| `ExecutionFailed` | More than one actor matches an identifier; the filter could not be resolved; the artifact of an observation command could not be written; the world was destroyed while `WaitForNavigationBuild` was waiting |
| `PreconditionFailed` | `RebuildNavigation` only: nothing was queued because the world has no navigation system, nowhere to build, or no navigation data that regenerates while the game runs |
| `Timeout` | `WaitForNavigationBuild` only: the system had not settled within `TimeoutSeconds`; the result and the artifact are still returned |

Every successful observation call saves exactly one JSON artifact; a failed call saves none.

---

## UAIP.Runtime.Animation

Observe the animation state of a character in a running game: which state each state machine is in, how the blends are weighted, which montages are playing, the values of the animation curves, whether the animation is advancing at all, the values of an anim instance's variables and, for Motion Matching, which pose the last search chose. Every command only reads — nothing here changes what an animation does. Works in the editor while PIE is running, and in `-game` and packaged builds. All seven commands accept [`TargetNetRole` / `TargetPIEInstance`](#choosing-which-play-world-a-runtime-command-acts-on). The state machine and state names are spelled as in the Anim Blueprint editor, so a state seen here can be looked up there by name.

**Capabilities.** All seven commands require `RuntimeInspect` (DefaultAllow). `DumpAnimInstanceVariables` also requires `AnimInstanceVariableDump` (DefaultDenied), because it writes out the values of the variables a project's own anim instance classes declare, and those can hold any project data. A missing capability is `CapabilityNotAvailable` naming it. See [Safety & Capabilities](safety.md#runtime-animation).

**Optional plugin.** `GetMotionMatchingState` 🧩 is registered only while the PoseSearch plugin is enabled; without it the command is not there (`CommandNotFound`, with a note naming the plugin) and the other six are unaffected. It is not part of the demo build.

**What a reading is.** The values are those of one moment: the command reads the state as it is when the call arrives and reports no history. It cannot tell when a montage started to blend out, and a montage whose blend out has finished is no longer there. Identifiers in a response (`InstanceId`, `MachineId`, `NodeId`, `MontageInstanceId`) tell the entries of that response apart; they are not kept across a recompile of the Anim Blueprint or a new play session, so do not store them — filter by state machine name and state name the next time.

### Observation (5) — requires `RuntimeInspect`

| Command | Description |
|---|---|
| 🆓 `DumpAnimInstanceState` | Everything below in one capture, so the sections describe the same frame: the update state, the state machines, the blend weights, the montages and the curves of the main, linked and post process anim instances of one skeletal mesh component. It filters its state machines (`StateMachineName`) and its curves (`CurveType`, `CurveNameContains`). Motion Matching and variables are not part of it — use `GetMotionMatchingState` and `DumpAnimInstanceVariables`. The response carries the summary and the leading entries of every list; the artifact holds everything that was kept |
| 🆓 `GetAnimStateMachineStates` | The state machines: for each machine the active state (`ActiveState`) and the time spent in it (`ActiveStateElapsedSeconds`), the states that carry weight (`StateWeights`), the transitions in progress (`ActiveTransitions`: `PreviousState` → `NextState` with the `NextStateWeight`) and the machine's own weight. A state reported as active includes a state that is blending out. A transition has no name and no elapsed time; its progress is the weight of the state it leads to. A machine that has not started yet is reported as `Uninitialized` without weights or transitions. `StateMachineName` narrows the list; every machine with that name is returned |
| 🆓 `GetAnimBlendWeights` | The assets that are playing with their final blend weight (`Players`, with the coordinates and sample weights of a blend space), the blend space player nodes (`BlendSpaceNodes`), the layered bone blend nodes with the weight of each blend pose (`LayeredBlends`) and, for a single node instance, the asset it plays (`SingleNode`). A montage that is blending out still counts, so its blend is part of the weights until the blend out ends. Takes no filter |
| 🆓 `GetActiveMontages` | The montages that are active, a montage that is blending out included. Each montage instance reports its `State` (`BlendingIn`, `Playing`, `BlendingDown`, `BlendingOut`, `Stopped`, `HoldingAtEnd`, `Paused` or `Unknown`), `PositionSeconds` and `PlayLengthSeconds`, `PlayRate`, the current and next section, `Weight` and `DesiredWeight`, the group and the slots it plays on with their weights. A linked anim instance that uses the montage data of the main instance is marked `SharedWithMain` instead of repeating it. Takes no filter |
| 🆓 `GetAnimCurveValues` | The animation curves in name order: name, value and kinds (`Types`). Every curve is an `Attribute` curve; one that also drives a material parameter or a morph target additionally lists `Material` or `MorphTarget`. `CurveType` narrows the list (`Material` or `MorphTarget`; `All` and `Attribute` keep every curve) and `CurveNameContains` keeps the curves whose name contains the text. `TotalCount` counts the curves that passed the filters and `UnfilteredCount` those before them. The values are those of the last completed evaluation; where the update rate optimization skipped the evaluation they are interpolated or the previous ones. The curve list is cut at 1024 entries unless `MaxEntries` says otherwise. A linked instance — and a post process instance while the main instance exists — is marked `SharedWithMain` instead of repeating the curves |

### Observation of variable values (1) — requires `RuntimeInspect` and `AnimInstanceVariableDump`

| Command | Description |
|---|---|
| `DumpAnimInstanceVariables` | The value of every variable that the project's own anim instance classes declare, for the main instance and, unless `InstanceScope` is `Main`, the linked and post process instances, each with its own values. A variable carries its name, the class that declared it, its type and its value. **Project-owned** means the project's Anim Blueprints and C++ classes and the plugins under the project's `Plugins/` folder: variables declared by the engine, by plugins installed in the engine, and by a parent class that lives on the engine side are not dumped (so a project Anim Blueprint whose parent is an engine class does not show what that parent declares), and neither are node internals. An object reference is written as the path of what it refers to and never followed. Large values are cut: arrays at 32 elements, strings at 1024 characters, structs after one level. When the size budget runs out, variables or whole instances are left out with a marker saying so. `VariableNameContains` keeps the variables whose name contains the text. The response carries the first 50 variables of each instance; the artifact holds every variable the capture kept. ⚠️ **Granting the capability writes the strings and paths held in the variables into the artifact as they are** — see [Safety & Capabilities](safety.md#runtime-animation) |

### Motion Matching (1) 🧩 — requires `RuntimeInspect`

Not provided in the demo build. Registered only while the PoseSearch plugin is enabled.

| Command | Description |
|---|---|
| `GetMotionMatchingState` | What the last pose search left in each Motion Matching node: the selected animation (`SelectedAnimationPath`) and the time inside it (`SelectedTimeSeconds`), whether the pose is mirrored (`Mirrored`), its blend space coordinates (`BlendParameters`), the pose search database it came from (`SelectedDatabasePath`), its total cost (`SearchCost`), whether the search kept the pose that was already playing (`IsContinuingPoseSearch`), the play rate the search wants (`WantedPlayRate`) and the seconds since the last pose jump (`ElapsedPoseSearchTimeSeconds`). A node that has not selected anything yet reports `HasSearchResult: false` with every field of the selection `null`. Each anim instance is read in its own entry, with its nodes under `MotionMatching`. A character that does not use Motion Matching is a success with an empty list and the limitation `NoMotionMatchingNode` — said only when every anim instance in scope could be read; an instance that could not be read is reported with its own reason instead. Nodes are listed up to `MaxEntries`; nodes past the cut are not counted, so `TotalCount` is `null` when the list is cut. It does not return the breakdown of the cost, the candidate poses, the databases that were searched or pose indices |

#### Parameters

| Parameter | Commands | Meaning |
|---|---|---|
| `ActorIdentifier` (required) | all | Label or name of the actor whose skeletal mesh component is observed, 1 to 256 characters |
| `ComponentName` | all | Name of the skeletal mesh component, matched exactly but ignoring case, 1 to 256 characters. Left out, the mesh is chosen as described under [Which mesh is read](#which-mesh-is-read) |
| `InstanceScope` | all | `Main` (the main anim instance only) or `All` (the main instance plus the linked and post process instances). Default `All` |
| `MaxEntries` | all | Upper bound on the entries of every list, curves included: an integer from 1 to 4096. Default 256 for every list except curves, which default to 1024. The value applies to every list, so `300` also lowers the curve limit from 1024 to 300 |
| `StateMachineName` | `GetAnimStateMachineStates`, `DumpAnimInstanceState` | Name of the state machines to return, matched exactly but ignoring case, 1 to 256 characters. Every machine with that name is returned |
| `CurveType` | `GetAnimCurveValues`, `DumpAnimInstanceState` | `All` (default), `Attribute`, `Material` or `MorphTarget` |
| `CurveNameContains` | `GetAnimCurveValues`, `DumpAnimInstanceState` | Text a curve name has to contain, ignoring case, 1 to 256 characters |
| `VariableNameContains` | `DumpAnimInstanceVariables` | Text a variable name has to contain, ignoring case, 1 to 256 characters |
| `TargetNetRole` / `TargetPIEInstance` | all | See [Choosing which play world a Runtime command acts on](#choosing-which-play-world-a-runtime-command-acts-on) |

A filter is accepted only by the commands listed for it. Passing it to any other command, an unknown key, an empty string, a name longer than 256 characters, a limit outside 1–4096 or an unknown kind is `InvalidParams`. Parameters are checked before the play world is looked up, so a malformed request is refused even when PIE is not running.

#### Which mesh is read

Without `ComponentName`, the mesh is chosen in this order: the only skeletal mesh component that has an anim instance; else the character's own mesh (for an actor that has one) among several that do; else the only mesh when none has an anim instance. The response says which way the mesh was chosen (`ByName`, `OnlyAnimated`, `CharacterMesh` or `OnlyMesh`) and lists the other candidates. When no rule singles one out the command fails with `InvalidParams` and lists the candidates, so pick one and send its name. A character whose face is a separate mesh (a MetaHuman, for example) reads the body mesh by default; name the face mesh to read it.

A mesh without an anim instance is not an error. The command succeeds with empty animation sections, `NoAnimInstance`, and the mesh's animation mode (Anim Blueprint, single asset, none). This also holds for a mesh named in `ComponentName` that only follows another mesh.

#### Fields in every response

| Field | Meaning |
|---|---|
| `CapturedAt` / `Frame` | When the state was read (ISO 8601, UTC) and the engine frame number at that moment |
| `NetMode` / `WorldContext` / `PIEInstance` | The world that was read. `PIEInstance` is omitted outside PIE |
| `Actor` / `Component` / `ComponentSelection` / `Candidates[]` | The actor and mesh component that were read, how the mesh was chosen, and the other skeletal mesh components of the actor |
| `Instances[]` | One entry per anim instance, main first, then linked, then post process: `InstanceId`, `Role` (`Main`, `Linked` or `PostProcess`), `ClassPath`, `IsAnimBlueprintClass`, `Initialized`, `SharedWithMain` and the sections the command reads. At most 64 anim instances of one mesh are read; the rest are marked as left out |
| `UpdateState` | Whether the animation is advancing at all. When it is not, `Details` lists why: `AnimationDisabled`, `AnimationPaused`, `SkeletonUpdateDisabled`, `ComponentTickDisabled`, `WorldPaused` or `NotRendered`, together with the update rate optimization state. A frame that update rate optimization only skips is reported as `UpdateSkippedByURO`, not as stopped |
| `ValueBasis` | On the values that depend on it, which moment the value belongs to: `NodeLastUpdate`, `RecordedReadBuffer`, `InstanceCurrent` or `LastCompletedEvaluation` |
| `DegradedSections[]` / `Limitations[]` | Parts of the result that could not be filled, each with its reason, and caveats about what was returned, each with a `Code` and sometimes a `Detail`. A reason that repeats is merged into one entry with a `Count` |

When a section cannot be read, only that part is left out and the reason is given; the command still succeeds. Examples: an anim instance that is not initialized yet is listed without being read (`AnimInstanceNotInitialized`); a state machine that has not started is `Uninitialized`; a mesh whose animation is disabled leaves out only the machine weight; a non-finite number is replaced by `null`. An anim instance without an Anim Blueprint (a C++-only anim instance, or a single asset playback) has no state machines or nodes and says why (`NativeAnimInstance`, `SingleNodeInstance`); montages, curves and the assets being played can still be read, though the position of a played asset can be empty for a C++-only instance. For a single asset playback that is playing a montage, `SingleNode` is `null` and the montage is reported as a montage; when it plays something else while another montage is active, the position may be the montage's (`SingleNodePositionFromMontage`).

#### Bounds on the output

A list is cut at `MaxEntries` (default 256, curves 1024, at most 4096), in a fixed order, and reports its `TotalCount`. Inner lists (blend space samples, montage slots, mesh candidates) are cut at 64. The size of one command is bounded as a whole: when it is reached, the lists after that point are not read and are marked as left out, so an empty list and a list that was left out can be told apart. The response holds the first 50 entries of every list; the artifact holds everything that was read within the bounds.

#### Linked anim layers and post process

By default the main, linked and post process anim instances are all returned, main first. Linked curves are a copy of the main ones and are not repeated; post process curves are not repeated either while the main instance exists. A linked instance's montages are not repeated when it uses the main instance's montage data. Variables are returned for every instance with its own values. Right after a linked anim layer was swapped, the first reading can mix in a playback position that is one frame old.

#### Errors

| ErrorCode | When |
|---|---|
| `InvalidParams` | A parameter is of the wrong type, empty, too long, out of range or unknown; a filter passed to a command that does not accept it; the mesh cannot be singled out (the message lists the candidates); `TargetNetRole` / `TargetPIEInstance` cannot be honoured |
| `CapabilityNotAvailable` | `RuntimeInspect`, or `AnimInstanceVariableDump` for `DumpAnimInstanceVariables`, is not granted. The message names it |
| `PolicyViolation` | The capability is denied explicitly in the safety policy |
| `NotAllowed` | No play world is running, or none matches `TargetNetRole` / `TargetPIEInstance` |
| `NotFound` | The actor matches nothing, has no skeletal mesh component, or has none named `ComponentName` (the message lists the candidates) |
| `PreconditionFailed` | The animation of the mesh was being evaluated on a worker thread when the command arrived. Nothing is read and no artifact is saved. Waiting would make game events fire earlier because of the observation, so the command does not wait: call it again |
| `ExecutionFailed` | More than one actor matches the identifier, or the artifact could not be saved |

Every successful call saves exactly one JSON artifact; a failed call saves none.

---

## UAIP.Runtime.Network

Observe the network of a running game: the net drivers of a world and their totals, the connections a net driver holds with their round trip time, loss and traffic, and how an actor is set up to replicate together with what the server knows about sending it. Beyond observation, read the values of replicated properties, compare them between the server and a client, and change the packet emulation that delays, drops, duplicates or reorders packets to reproduce a poor connection. Works while PIE is running, and in `-game` and packaged builds. All seven commands accept [`TargetNetRole` / `TargetPIEInstance`](#choosing-which-play-world-a-runtime-command-acts-on), which pick the server world or one of the client worlds of a networked Play-in-Editor session.

**Capabilities.** `GetNetDriverState`, `ListNetConnections`, `DumpActorReplication`, `DumpReplicatedPropertyValues` and `CompareReplicatedProperties` require `RuntimeInspect` (DefaultAllow). `DumpReplicatedPropertyValues` and `CompareReplicatedProperties` also require `RuntimeReplicatedPropertyValueRead` (DefaultDenied), because the values can include the platform account identifier of a player (the replicated `UniqueId` of a `PlayerState`) and the names of players. `ListNetConnections` additionally needs `RuntimeNetConnectionAddressRead` (DefaultDenied) **only when `IncludeRemoteAddress` is `true`**; that capability is checked per request and does not appear in the command's declared `RequiredCapabilities`. `SetNetworkEmulation` and `ResetNetworkEmulation` require `RuntimeNetworkEmulationControl` (DefaultDenied); they are not read-only, so they are refused while the safety policy is in read-only mode. A missing capability is `CapabilityNotAvailable` naming it. See [Safety & Capabilities](safety.md#runtime-network-and-replication).

**Demo build.** `GetNetDriverState`, `ListNetConnections` and `DumpActorReplication` are provided in the demo binary, together with `RuntimeNetConnectionAddressRead`. `DumpReplicatedPropertyValues`, `CompareReplicatedProperties`, `SetNetworkEmulation` and `ResetNetworkEmulation` are not; in the demo those commands are absent and return `CommandNotFound`. Their capabilities (`RuntimeReplicatedPropertyValueRead`, `RuntimeNetworkEmulationControl`) are registered in the demo but marked as not in this edition, so granting them in the ini has no effect.

**Shipping builds.** `SetNetworkEmulation`, `ResetNetworkEmulation` and `RuntimeNetworkEmulationControl` are registered only in builds that can use the engine's packet emulation. A Shipping build does not register them (`CommandNotFound`).

**What a reading is.** An observation reads the state as it is when the call arrives and keeps no history, and no command waits for a connection to be made. To wait until clients have joined, call `GetNetDriverState` repeatedly and watch `LoggedInConnectionCount` on the server or `Availability` on a client. A connection number (`ConnectionIndex`) is the position of the connection in its net driver as `ListNetConnections` lists it: a server lists its client connections in the order the net driver keeps them, and a client lists its one connection to the server. A closed connection keeps its number until the net driver drops it, so the numbers can shift afterwards; list the connections again before using a number later. The connections of split-screen players beyond the first are not listed. A net driver name (`NetDriverName`) is matched ignoring case.

**Iris.** Under the Iris replication system some items are read from structures that only the generic replication system has. They are returned as `null` and the response carries `Limitations: IrisReplicationActive`: `ActorChannelCount` of `ListNetConnections`, `Connections` and `NetworkObjectInfo` of `DumpActorReplication`, and, in `CompareReplicatedProperties`, the properties whose condition can change at run time, which become `NotComparable`. `GetNetDriverState` carries the same limitation when any of its net drivers uses Iris.

### Observation (3) — requires `RuntimeInspect`

| Command | Description |
|---|---|
| 🆓 `GetNetDriverState` | The net drivers of the target world. Takes no parameters besides the play world selector. `Availability.State` is `Available`, `Connecting` (a client still joining, `Reason: PendingNetGame`) or `Unavailable` (`Reason: NoNetDriver`: the world has no game net driver); `Reason` is left out while available. `RunAsDedicated` and `HasGameViewport` tell what kind of process the world runs in. Each entry of `NetDrivers[]` carries `NetDriverName`, `NetDriverDefinition`, `IsServer`, `ReplicationSystem` (`Generic` or `Iris`), `ConnectionCount`, `LoggedInConnectionCount`, `MaxClientRate`, `MaxInternetClientRate`, `MaxNetTickRate`, `NetServerMaxTickRate`, `ConnectionTimeoutSeconds`, `Totals` over its connections (`InBytesPerSecond`, `OutBytesPerSecond`, `InPacketsPerSecond`, `OutPacketsPerSecond`, `InLossRatioWeighted` / `OutLossRatioWeighted` weighted by the packets per second, `InLossRatioMax` / `OutLossRatioMax` of the worst connection, and `StatsReadyConnectionCount`, the connections whose statistics went into the sums), `MaxPlayers` / `MaxSpectators` (only for a server with a game session; left out otherwise), the net driver's `PacketSimulation` settings, `EmulationModifiedByUAIP` (whether `SetNetworkEmulation` holds saved settings of the net driver or one of its connections) and `EmulationDisabledByConfig` (whether the net driver ignores emulation settings by configuration). A world without a game net driver is a success: the other net drivers are still listed and `Availability` says why. The response and the artifact hold the same content |
| 🆓 `ListNetConnections` | The connections of one net driver (`NetDriverName`, default `GameNetDriver`), a page at a time (`StartIndex`, `MaxEntries`). Each entry carries `ConnectionIndex`, `Direction` (`ToClient` or `ToServer`), `ConnectionState`, `ClientLoginState`, `LoggedIn`, `PlayerController`, `PlayerState`, `ConnectedSeconds`, `LastReceiveAgeSeconds`, `StatsReady`, `RttMs`, `RawPingMs`, `PlayerPingMs`, `JitterMs`, `InLossRatio`, `OutLossRatio`, `InLossRatioAvg`, `OutLossRatioAvg`, `InBytesPerSecond`, `OutBytesPerSecond`, `InPacketsPerSecond`, `OutPacketsPerSecond`, the cumulative `InTotalBytes`, `OutTotalBytes`, `InTotalPackets`, `OutTotalPackets`, `InTotalPacketsLost`, `OutTotalPacketsLost`, `CurrentNetSpeedBytesPerSecond`, `QueuedBits`, `IsNetReady`, `OpenChannelCount`, `ActorChannelCount`, the effective `PacketSimulation` of the connection and `AddressKind` (`Loopback`, `Private`, `Public`, or `Unknown` when the address is not 4 or 16 raw bytes). `RemoteAddress`, the raw IP address and port, is written only when `IncludeRemoteAddress` is `true`. While `StatsReady` is false the round trip time, the jitter, the four loss ratios and the four per-second values are `null`. `RttMs` is the average of the last statistics period, and the previous value is kept until the next period ends. The cumulative counters are 32-bit integers in the engine and can wrap around on a long session. The artifact holds the whole page with `TotalCount`, `ReturnedCount` and, while more connections remain, `NextStartIndex`; the response holds the same fields with the first 50 connections of the page and `Truncated: true` when the page holds more. A world without the game net driver is a success with an empty list when `NetDriverName` is left out, and `Availability` says why |
| 🆓 `DumpActorReplication` | How one actor (`ActorIdentifier`) is set up to replicate and what the server knows about sending it. `Actor` carries `Name`, `Path` and `Class`. `Replication` carries `Replicates`, `LocalRole`, `RemoteRole`, `NetOwner`, `HasOwningConnection`, `NetDormancy`, `NetUpdateFrequency`, `MinNetUpdateFrequency`, `NetCullDistance` (the distance, not its square), `NetPriority`, `AlwaysRelevant`, `OnlyRelevantToOwner`, `IsNetStartupActor` and `ReplicateMovement`. `Properties[]` lists the replicated properties of the actor, and `Components[]` those of each replicated component, each with `Name`, `Type`, `DeclaredBy`, `ArrayDim`, `DeclaredCondition` (the condition name without the `COND_` prefix), `DeclaredRepNotifyCondition` (`OnChanged` or `Always`), `RepNotifyFunction` (`null` when there is none) and `PushBased`. On a server, `Connections[]` tells for each connection whether an actor channel is open (`ActorChannelOpen`), whether a change has been found and not sent yet (`HasUnsentComparedChanges`), which of the actor's own properties are inactive (`InactiveProperties`, `null` until the engine has evaluated them) and whether the last update was empty (`LastUpdateEmpty`), and `NetworkObjectInfo` carries `NextUpdateTime`, `LastNetReplicateTime`, `PendingNetUpdate` and `DormantConnectionCount`. `Connections` and `NetworkObjectInfo` are `null` on a client, under Iris, and in a world without a net driver (`Availability` says why). `HasUnsentComparedChanges: false` does not mean the client is in sync. A replicated property missing from the lifetime properties has `DeclaredCondition: null` and the response carries `Limitations: PropertyMissingFromLifetimeProps`. `MaxProperties` bounds the actor's and the components' properties together and `MaxConnections` the connections; a cut list reports `PropertiesTruncated` / `TotalPropertyCount` or `ConnectionsTruncated` / `TotalConnectionCount`. There is no paging. The response and the artifact hold the same content |

### Observation of property values (2) — requires `RuntimeInspect` and `RuntimeReplicatedPropertyValueRead`

Not provided in the demo build.

| Command | Description |
|---|---|
| `DumpReplicatedPropertyValues` | The values of the replicated properties (only properties marked for replication) of one actor (`ActorIdentifier`) and of each of its replicated components, in the selected world. On a client world the values are those the client received, so calling it on the server world and on a client world lets the two be set side by side. `Actor` carries `Name`, `Path` and `Class`; the actor's properties sit in `Properties[]` (`Name`, `Type`, `Value`) and those of each component in its entry of `Components[]` (`Name` and the same fields). Long strings, large containers and nested structs are cut. Each object reports `PropertiesTruncated`, `PropertiesOmitted`, `TotalPropertyCount` and, when a size budget stopped it, `StopReason` (`PerObjectBudget`, `TotalBudget` or `ExternalBudget`); the top-level `Truncated` is `true` when any object was cut or had properties left out. A 64-bit integer is written as a string only when its magnitude is beyond 2^53, which a JSON number cannot hold exactly; ±2^53 itself is still a number. The values are returned even when the world has no net driver, with `Availability.State: Unavailable` (`Reason: NoNetDriver`). The response and the artifact hold the same content. ⚠️ **The values can include the replicated `UniqueId` of a `PlayerState` (a platform account identifier) and the names of players** — see [Safety & Capabilities](safety.md#runtime-network-and-replication) |
| `CompareReplicatedProperties` | Compares the replicated properties of an actor in the server world with the same actor as one client received it, and reports for each property of the actor and its replicated components `Equal`, `Different` or `NotComparable` with a `Reason`. No value is returned. The play world selector names the **client** world; `ActorIdentifier` names the actor in the **server** world, which must be the only listen or dedicated server in this process (Play-in-Editor with **Run Under One Process**). See [Reading a comparison](#reading-a-comparison) below |

### Packet emulation (2) — requires `RuntimeNetworkEmulationControl`

Not provided in the demo build or in Shipping builds.

| Command | Description |
|---|---|
| `SetNetworkEmulation` | Changes the packet emulation settings (latency, loss, jitter, duplication, reordering) of a net driver of the target play world, or of one of its connections when `ConnectionIndex` is given. Only the items given change; the others keep their current values. Without `ConnectionIndex` the settings of the whole net driver are changed and copied to every connection. The settings that were there before the first change are saved, so `ResetNetworkEmulation` can put them back. The change stays until it is reset or the net driver is destroyed (when the play session ends, or when a client reconnects after travelling to another map). The response carries `Availability`, `Target` (`PIEInstance`, `NetDriverName` and, when given, `ConnectionIndex`), `Before` and `After` (every item of the engine settings, including the read-only `PktFrameDelay`, `PktBufferBloatInMS`, `PktIncomingFrameDelay`, `PktIncomingBufferBloatInMS`, `PktLossMinSize` and `PktLossMaxSize`) and `Limitations[]`. See [Packet emulation](#packet-emulation) below |
| `ResetNetworkEmulation` | Puts a net driver (`NetDriverName`, default `GameNetDriver`) and all its connections back to the settings saved before the first `SetNetworkEmulation` change, unconditionally: a change made afterwards from the console is lost as well. There is no reset of a single connection. The response carries `Availability`, `NetDriverName`, `Restored[]` (the net driver first, then the connections; each with `Scope` `Driver` or `Connection`, the `ConnectionIndex` of a connection — `null` when it is no longer numbered — and `After`), `Discarded` (the number of saved entries dropped because the net driver or connection no longer exists; an earlier call may already have dropped them) and `Limitations[]` (`ForcedPacketSettingsRemains` when the net driver itself was restored). Nothing to restore is a success with an empty `Restored`: a world without a game net driver when `NetDriverName` is left out, a net driver that was never changed, or settings saved in a play session that has already ended |

#### Parameters

| Parameter | Commands | Meaning |
|---|---|---|
| `NetDriverName` | `ListNetConnections`, `SetNetworkEmulation`, `ResetNetworkEmulation` | Name of the net driver as `GetNetDriverState` lists it, 1 to 256 characters, matched ignoring case. Default `GameNetDriver`. A name given explicitly that the world does not hold is `NotFound`, and the message lists the net drivers of the world |
| `StartIndex` | `ListNetConnections` | Integer from 0 to the int32 maximum, default 0. The first connection of the page. A value at or beyond the number of connections returns an empty page |
| `MaxEntries` | `ListNetConnections` | Integer 1–500, default 50. Connections in the page |
| `IncludeRemoteAddress` | `ListNetConnections` | Boolean, default `false`. Writes `RemoteAddress`. `true` needs `RuntimeNetConnectionAddressRead`, checked before the play world is looked up |
| `ActorIdentifier` (required) | `DumpActorReplication`, `DumpReplicatedPropertyValues`, `CompareReplicatedProperties` | Label or object name of the actor, 1 to 256 characters. See [Which actor is read](#which-actor-is-read) |
| `MaxProperties` | `DumpActorReplication`, `CompareReplicatedProperties` | Integer 1–1024, default 256. In `DumpActorReplication` it bounds the properties of the actor and its components together; in `CompareReplicatedProperties` it bounds the `Properties` list only, while the comparison and `Summary` cover every property |
| `MaxConnections` | `DumpActorReplication` | Integer 1–256, default 16 |
| `ConnectionIndex` | `SetNetworkEmulation` | Integer from 0 to the int32 maximum, numbered as `ListNetConnections` numbers the connections. Left out, the whole net driver is changed. A number the net driver does not have is `NotFound` |
| `PktLag`, `PktLagVariance`, `PktLagMin`, `PktLagMax`, `PktIncomingLagMin`, `PktIncomingLagMax`, `PktJitter` | `SetNetworkEmulation` | Integers in milliseconds, 0–10000 |
| `PktLoss`, `PktIncomingLoss`, `PktDup` | `SetNetworkEmulation` | Integers in percent, 0–100 |
| `PktOrder` | `SetNetworkEmulation` | Boolean. Reorders outgoing packets |
| `TargetNetRole` / `TargetPIEInstance` | all | See [Choosing which play world a Runtime command acts on](#choosing-which-play-world-a-runtime-command-acts-on). For `CompareReplicatedProperties` they name the client world |

`SetNetworkEmulation` needs at least one emulation item. A minimum above its maximum (`PktLagMin` / `PktLagMax`, `PktIncomingLagMin` / `PktIncomingLagMax`) is `InvalidParams`, and when only one side is given it is checked against the current value of the other. Booleans must be JSON booleans and limits JSON integers; anything else, an empty string, an unknown key or a value out of range is `InvalidParams`, and nothing is changed.

#### Which actor is read

`ActorIdentifier` matches an actor whose label (in editor builds) or object name is exactly the text, ignoring case. A partial match is not accepted: when nothing matches exactly, the command fails with `NotFound` and the message suggests up to 10 actors whose name or label contains the text. When more than one actor matches exactly, the command fails with `ExecutionFailed`; pass an identifier that matches only one actor.

#### Fields in every response

| Field | Meaning |
|---|---|
| `CapturedAt` / `Frame` | When the state was read (ISO 8601, UTC) and the engine frame number at that moment |
| `NetMode` / `WorldContext` / `PIEInstance` | The world that was read. For `CompareReplicatedProperties` this is the client world; the server world is in `ServerWorld` |
| `Availability` | Every command except `CompareReplicatedProperties`: `State` (`Available`, `Connecting` or `Unavailable`) and, unless available, `Reason` (`PendingNetGame` or `NoNetDriver`) |
| `Limitations[]` | Codes of the caveats about what was returned (see below). `DumpReplicatedPropertyValues` has none |

#### Limitations codes

| Code | Commands | Meaning |
|---|---|---|
| `IrisReplicationActive` | `GetNetDriverState`, `ListNetConnections`, `DumpActorReplication`, `CompareReplicatedProperties` | Iris is in use; the items described under **Iris** above are `null` or not comparable |
| `NetTestDisabledInBuild` | `GetNetDriverState`, `ListNetConnections` | The build has no packet emulation support, so `PacketSimulation` (and `EmulationDisabledByConfig`) are `null` |
| `LossRatioDenominatorsDiffer` | `GetNetDriverState` (always) | The incoming loss ratio is taken over the packets received plus those lost, the outgoing one over the packets acknowledged. Do not compare the two directly |
| `PropertyMissingFromLifetimeProps` | `DumpActorReplication`, `CompareReplicatedProperties` | A property is marked for replication but missing from the lifetime properties, so its condition is unknown. The engine does not send such a property |
| `CustomActiveStateNotObserved` | `CompareReplicatedProperties` (always) | The game can stop sending a property through a custom active state, which is not observed, so such a property can still be reported as `Different` |
| `DriverWideChangeOverwritesConnection` | `SetNetworkEmulation` | The change was made to one connection. A later change to the whole net driver, by this command or from the console (`Net PktLag=...` and the like), overwrites it |
| `ForcedPacketSettingsRemains` | `SetNetworkEmulation`, `ResetNetworkEmulation` | The whole net driver was changed or restored. The engine no longer reloads its settings from the project configuration until the net driver is destroyed, even after a reset |
| `PacketLagSettingIgnored` | `SetNetworkEmulation` | A latency item in `After` is not zero but the engine ignores it, because another item takes precedence (see below) |

#### Reading a comparison

`CompareReplicatedProperties` first finds the client's copy of the actor. `Counterpart.Status` is `Resolved` when it was found; otherwise the command succeeds and compares nothing, and the status says why: `NotReplicated` (the server has no network identifier for the actor), `NotReached` (the client does not know it yet), `Pending` (the client is still loading it), `Broken` (the client marked it as broken), `Destroyed` (the client's copy is no longer valid), or `ConnectionNotFound` (no server connection could be matched to the client world, for example before login). `Pending` and `Broken` occur with the generic replication system only. Each entry of `Components[]` carries its own `Counterpart.Status`.

The response carries `ServerWorld` (`PIEInstance`, `NetMode`), `ClientWorld` (`PIEInstance`), `Actor` (`Name`, `ServerPath`), `ReplicationSystem`, `Counterpart` (`Status`, `ClientPath`), `Summary` (`Equal`, `Different` and `NotComparable` counts over every property), `Properties[]` (`Name`, `Owner`, `Result`, and `Reason` for `NotComparable`) ordered `Different`, `NotComparable`, `Equal`, `PropertiesTruncated`, `TotalPropertyCount` and `Limitations[]`. The response and the artifact hold the same content.

⚠️ **The comparison never says the actor is "in sync".** Only properties that can be evaluated are compared, and `Equal` says only that the two values were the same at the moment of the call. `Different` does not prove a bug either: values legitimately lag while in flight, under the update frequency and under dormancy, and a property the game stops sending through a custom active state is reported as `Different` (`Limitations` always carries `CustomActiveStateNotObserved`). A struct type with its own net serialization is `NotComparable` only when the property itself is of that type; an array whose elements are such a type — for example `TArray<FVector_NetQuantize>` — is compared value by value and can be reported as `Different` because of legitimate quantization.

A property that cannot be evaluated is `NotComparable` with one of these reasons:

| `Reason` | Meaning |
|---|---|
| `InitialOnly` | The property is replicated only once, when the object is created |
| `ConditionUnknown` | The condition is decided at run time (custom or dynamic) and the engine has not evaluated it for this connection. This is always the case for the properties of a component, and under Iris |
| `ConditionNotApplicable` | The condition does not apply to this client, so the property is not sent to it. This includes a property missing from the lifetime properties (`Limitations: PropertyMissingFromLifetimeProps`) |
| `DeltaSerialized` | The property is serialized as a delta (a fast array), which has no whole value to compare |
| `ObjectReference` | The property is an object reference whose target could not be matched between the two worlds |
| `NestedObjectReference` | The property holds an object reference inside a container or struct |
| `CustomNetSerialization` | The property is of a type with its own net serialization, which may round the value legitimately, and the values differ. Equal values are reported as `Equal` |
| `ClassMismatch` | The server object and the client object are of different classes |

**Refusals.** The command is refused with `NotAllowed`, saving nothing, when the client is still connecting (`Connecting`), the selected world has no net driver (`NoNetDriver`) or is not a client (`TargetIsNotClient`), or the process has no server world (`NoServerWorld`) or more than one (`MultipleServerWorlds`; the message lists up to 8 play worlds). The `ErrorMessage` starts with that reason, followed by `nothing was compared`. A server world without a game net driver is `ExecutionFailed`.

#### Packet emulation

The engine reads the outgoing latency items in this order of precedence, and `SetNetworkEmulation` reports `PacketLagSettingIgnored` when an item it would ignore is not zero:

1. When `PktFrameDelay` (read-only here) is above 0 or `PktOrder` is on, `PktLag`, `PktLagVariance`, `PktLagMin`, `PktLagMax` and `PktJitter` are ignored.
2. Otherwise, when `PktJitter` is not 0, the latency is taken from `PktLagMin`, widened by the jitter and the variance; `PktLag` and `PktLagMax` are ignored.
3. Otherwise, when `PktLag` is not 0, it is used with `PktLagVariance`; `PktLagMin` and `PktLagMax` are ignored.
4. Otherwise the latency is drawn between `PktLagMin` and `PktLagMax`, and `PktLagVariance` is ignored.

The incoming items (`PktIncomingLagMin`, `PktIncomingLagMax`, `PktIncomingLoss`) are independent of these.

A setting made on one connection is overwritten by any later change to the whole net driver, made by this command or from the console (`DriverWideChangeOverwritesConnection`). After a change to the whole net driver the engine stops reloading the settings from the project configuration until the net driver is destroyed, even after `ResetNetworkEmulation` (`ForcedPacketSettingsRemains`).

⚠️ **Call `ResetNetworkEmulation` before the `RuntimeNetworkEmulationControl` grant is withdrawn.** Restoring needs the same capability, so once it is withdrawn the change stays until the net driver is destroyed.

**Saving the artifact.** The change (or the restoration) is already made when the artifact is saved, so a failed save leaves `SetNetworkEmulation` and `ResetNetworkEmulation` successful, without an artifact. The one exception is an artifact that was written but whose location cannot be resolved: the command then fails with `ExecutionFailed`, and the message says that the settings were already changed and that `ResetNetworkEmulation` restores them (or, for `ResetNetworkEmulation`, that the saved settings were already restored and forgotten).

#### What completion notifications and audit records hide

The raw addresses and the property values are returned to the caller as they are, and saved in the artifact as they are. The copy of the response that goes to the editor's completion notification — which the editor's own notifications and any code that records commands (audit records, logs) receive — hides them: every `RemoteAddress` in `Connections[]` of `ListNetConnections`, and every `Value` in `Properties[]` and in `Components[].Properties[]` of `DumpReplicatedPropertyValues`, becomes `"<redacted>"`. The other fields are kept. A `ListNetConnections` call without `IncludeRemoteAddress` has no address to hide, so its copy is unchanged. `CompareReplicatedProperties` returns no value, so nothing is hidden. In a scenario, a step that takes an address or a value from an earlier step's response is recorded with its parameters and response `Data` masked. `DescribeCommand` lists these positions under `SensitiveResponseData`; see [Sensitive values and where they are masked](#sensitive-values-and-where-they-are-masked).

#### Errors

| ErrorCode | When |
|---|---|
| `InvalidParams` | A parameter is of the wrong type, empty, too long, out of range or unknown; `SetNetworkEmulation` without any emulation item, or with a minimum above its maximum; `TargetNetRole` / `TargetPIEInstance` cannot be honoured |
| `CapabilityNotAvailable` | `RuntimeInspect`, `RuntimeReplicatedPropertyValueRead`, `RuntimeNetworkEmulationControl`, or — for `IncludeRemoteAddress: true` — `RuntimeNetConnectionAddressRead` is not granted. The message names it |
| `PolicyViolation` | The capability is denied explicitly in the safety policy, or `SetNetworkEmulation` / `ResetNetworkEmulation` is called in read-only mode |
| `NotAllowed` | No play world is running, or none matches `TargetNetRole` / `TargetPIEInstance`; a refusal of `CompareReplicatedProperties` (see above); `SetNetworkEmulation` on a net driver whose configuration forbids emulation (`EmulationDisabledByConfig`) |
| `NotFound` | `ActorIdentifier` matches no actor (the message suggests candidates); a `NetDriverName` given explicitly that the world does not hold (the message lists the net drivers); `SetNetworkEmulation` in a world without a game net driver when `NetDriverName` is left out (a standalone game), or a `ConnectionIndex` the net driver does not have |
| `ExecutionFailed` | More than one actor matches the identifier; the artifact of an observation command could not be saved; the server world of `CompareReplicatedProperties` has no game net driver; the artifact of `SetNetworkEmulation` / `ResetNetworkEmulation` was written but its location cannot be resolved |
| `CommandNotFound` | A command that the build does not provide: the value, comparison and emulation commands in the demo build, and the emulation commands in a Shipping build |

Every successful observation call saves exactly one JSON artifact; a failed call saves none, and a refused request saves nothing.

---

## UAIP.Runtime.Mass

Observe the Mass simulation of a play world: how many entities it holds, which archetypes they are grouped into, which processors run in which order, which element types one entity carries and — when you allow it — the values of those elements. The module needs only the `MassEntity` module that ships with the engine, not the `MassGameplay` plugin, so it carries no 🧩. It is loaded in the editor only (a game build does not contain it) and is not part of the demo build. Every command only reads. To read or assemble the assets a simulation is built from, see [`UAIP.Editor.Mass`](#uaipeditormass-).

Five of the six commands act on the Mass entity manager of a play world in the editor and accept [`TargetNetRole` / `TargetPIEInstance`](#choosing-which-play-world-a-runtime-command-acts-on); `DumpMassEntitySettings` reads engine settings and takes no parameters.

**Capabilities.** All six require `RuntimeInspect` (DefaultAllow). `GetMassEntityFragments` also requires `RuntimeMassFragmentValueRead` (DefaultDenied), because the values of fragments are project data. A missing one is `CapabilityNotAvailable`. See [Safety & Capabilities](safety.md#mass-observation-and-editing).

**Naming an entity.** An entity is named by `EntityIndex` and `EntitySerialNumber` together, as an earlier response listed them (ask `DumpMassEntityArchetypes` for a sample with `SampleEntitiesPerArchetype`). Every response about a play world carries a `WorldToken` identifying the world it observed. Pass it back unchanged: `GetMassEntityFragments` requires it and refuses with `Conflict` to answer for another world (for example after PIE was restarted), and `DescribeMassEntity` verifies it when given and otherwise says so with the `WorldTokenNotVerified` limitation.

**Reading at a safe point.** When the engine state may be half updated (a modal dialog or a long running task holds the game loop, or the world is in the middle of its tick), nothing is read and the command **succeeds** with `Availability: NotAtSafePoint` and no data. That is not the same as an empty world, and for `DescribeMassEntity` / `GetMassEntityFragments` it does not say whether the entity exists. Call again.

**Output bounds.** None of the bounds can be configured. `Data` holds the leading entries and the artifact holds the rest up to a size budget; `…Truncated` flags and counts before the cut say when something was left out.

**Ambiguous element names.** When a short element name matches more than one type, `GetMassEntityCount`, `DumpMassEntityArchetypes` and `GetMassEntityFragments` refuse with `InvalidParams`, and the failed response's `Result` carries `AmbiguousName` (the name as given), `Candidates` (the full type paths, sorted, at most 10) and `TotalCandidateCount` (how many types matched, which can be more than the ten listed). Pass one of the candidate paths to remove the ambiguity.

**Debugging interface.** `GetMassEntityCount`, `DumpMassEntityArchetypes` and `DumpMassProcessorGraph` need the debugging interface of Mass, which some build configurations leave out (an engine build in which `WITH_MASSENTITY_DEBUG` is 0, as in a Shipping build). There they are listed with `Available: false` (`UnavailableDetail: BuildConfiguration`) and a message saying so.

**If Mass is not running.** When the project settings or console variables (for example `mass.RuntimeSubsystemsEnabled`) turn the Mass subsystems off for the play world, the commands that need them are refused with `PreconditionFailed` naming the setting. `DumpMassEntitySettings` is not affected.

**If TEDS is disabled.** With the editor's Typed Elements Data Storage (TEDS) enabled, which is the default, the module adds no side effect. With TEDS disabled, loading the module makes the editor load the `MassEntity` module, and Mass subsystems can then be created in the editor world and in similar editor-side worlds. This stays inside the editor and never reaches a game.

| Command | Description |
|---|---|
| `DumpMassEntitySettings` | The Mass settings of the engine, saved as a JSON artifact: `ChunkMemorySize` (bytes of one chunk of entity memory), `ProcessingPhases` (`Phase` and `PhaseGroupClassPath`, in the order the settings list them) and `ProcessorCDOs`, the processor classes the settings collected (`ClassPath`, `Phase`, `ExecutionOrder` with its `Group`, `Before` and `After`, `ExecutionFlags`, `AutoRegisterWithProcessingPhases`). The settings are read from a class default object, so it needs no play world and its response carries no `WorldToken`; `Availability` is always `Available`. Data holds the first 50 processor classes with `ProcessorCDOsTotalCount` and `ProcessorCDOsTruncated`. Read-only, requires `RuntimeInspect` |
| `GetMassEntityCount` | Counts the entities of the target play world: `TotalEntityCount` (the whole world), `MatchingEntityCount`, `MatchingArchetypeCount` and `Archetypes` (`ArchetypeId` and `EntityCount` of each matching archetype, largest first). `RequiredElements` keeps archetypes that carry every listed element type and `ExcludedElements` drops those that carry any; a name is a short name such as `TransformFragment` or a full path such as `/Script/MassCommon.TransformFragment`, and an unknown, ambiguous or non-element name is refused (at most 64 names of at most 512 characters per list). A world with no entity gives zero counts. Data holds the first 50 archetypes (`ArchetypesTruncated`). Read-only, requires `RuntimeInspect` |
| `DumpMassEntityArchetypes` | Lists the archetypes of the target play world one page at a time. For each: `ArchetypeId`, `Composition` (`Kind` and `Type` of every element), `EntityCount`, `ChunkCount`, `EntitiesPerChunk`, `AllocatedSizeBytes`, `WastedEntityMemoryBytes`, `BytesPerEntity`, `DebugNames` and `SampleEntities` (`Index` and `SerialNumber` of up to `SampleEntitiesPerArchetype` entities; none by default). Same `RequiredElements` / `ExcludedElements` filter as above. `StartIndex`, `MaxArchetypes` (1–500, default 50) and `SampleEntitiesPerArchetype` (0–16) page through a stable order; the response carries `TotalArchetypeCount`, `TotalEntityCount` (before the filter), `MatchingArchetypeCount`, `NextStartIndex` (only when archetypes are left) and `ArchetypesTruncated`. The archetypes can change between pages. Read-only, requires `RuntimeInspect` |
| `DumpMassProcessorGraph` | The processor graph of the target play world: for each processing phase the processors in the order they run, then the processors the engine pruned and the processors that observe the addition or removal of an element. Each processor lists its class, its position, the processors it has to run after, its group, order and execution flags, and the requirements of its queries (element type and kind, read or read-write access, whether the entity has to carry it). Data carries the leading entries and the artifact the rest. A world with no processing environment of the Mass debugger gives an empty graph with the `ProcessingEnvironmentNotFound` limitation, which is not the same as a world without processors. Read-only, requires `RuntimeInspect` |
| `DescribeMassEntity` | Which element types one entity carries, without reading any value: the hash of its archetype and its fragments, tags, shared fragments, const shared fragments and chunk fragments, each with kind and type path. On UE 5.8 and later it also lists the sparse fragments (types only) and always reports `SparseTagsNotListed`: the sparse tags of an entity cannot be listed, so an empty list of tags does not mean the entity has none. Needs `EntityIndex` and `EntitySerialNumber`; `WorldToken` is optional. `NotFound` when the entity does not exist. Read-only, requires `RuntimeInspect`. The values are read by `GetMassEntityFragments` |
| `GetMassEntityFragments` | The values of the fragments, shared fragments and const shared fragments of one entity. Needs `EntityIndex`, `EntitySerialNumber` and `WorldToken`. `ElementTypes` (at most 64 names) limits the read to the named types; a tag or a chunk fragment is `InvalidParams` because it has no value to read for one entity, and a named type the entity does not carry is listed in `MissingRequestedElements`. Each entry of `Elements` has `Kind`, `Type` and, when read, `Value` (a list of the struct's members with `Name`, `Type` and `Value`), `ValueTruncated` (cut at the 16 KiB budget of one fragment) or `ValueOmittedReason`. The values of one response share a 256 KiB budget; the elements after the point it runs out carry their type only with `ValueBudgetExceeded`. `Limitations` lists what was left out: strong object references are never read (`ObjectReferenceOmitted`), a struct whose type is chosen at run time is not expanded (`NestedInstancedStructNotExpanded`), members that are not reflected are not output (`NonReflectedMembersOmitted`), a struct nested deeper than 4 levels of expansion is returned by its type name only (`StructDepthTruncated`; its `Detail` is the type path of the element, once per type, and the value itself carries no mark, so read `Limitations` to tell), and the sparse elements on UE 5.8 and later are listed by type only (`SparseElementValuesNotRead`). Read-only, requires `RuntimeInspect` and `RuntimeMassFragmentValueRead` |

**Errors.**

| ErrorCode | When |
|---|---|
| `NotAllowed` | No play world is running, or none matches `TargetNetRole` / `TargetPIEInstance` |
| `PreconditionFailed` | Mass is switched off for the play world (project settings or console variables) |
| `NotFound` | The entity does not exist, was destroyed, or its serial number does not belong to the index |
| `Conflict` | The `WorldToken` does not name the world observed now |
| `InvalidParams` | An unknown, ambiguous or non-element type name, a tag or chunk fragment in `ElementTypes`, an out-of-range parameter |
| `CapabilityNotAvailable` / `PolicyViolation` | A required capability is not granted / is denied by the safety policy |

---

## Scenario execution route

Scenarios are not a single command — they are a separate route that submits an ordered list of commands as one request. See [Scenario Execution](scenario.md). Available entry points:

| Transport | Entry point |
|---|---|
| MCP | `uaip_run_scenario` |
| HTTP | `POST /uaip/scenarios` (requires `-uaip-enable-scenario`) |
| WebSocket | Frame `Type: "ScenarioRequest"` |
| CLI | `-uaip-scenario=<json>` / `-uaip-scenario-file=<path>` |

Any step in a scenario is dispatched through the same `CommandDispatcher` as `uaip_execute`, so the same Capability + SafetyPolicy rules apply.

---

> Schemas and parameter details are intentionally omitted from this page. Get the full schema for any command with `{"Command": "UAIP.Core.DescribeCommand", "Params": {"Name": "<command name>"}}` over HTTP / WebSocket / CLI, or `uaip_describe_command(CommandName="<command name>")` over MCP (the argument is `Name` in the first form and `CommandName` in the second).

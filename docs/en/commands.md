**[日本語](../ja/commands.md)** | [Back to README](../../README.md)

# Commands Reference

UAIP exposes 1189 **UAIP commands** (provided directly by the plugin itself) and 421 **Toolset bridge commands** (delegating to the UE 5.8 official Toolset framework), for a combined total of 1610 commands organized by domain. Each command name is fully-qualified — e.g. `UAIP.Editor.Observation.CaptureActiveWindowImage`. This page omits the provider prefix in the tables; the section header tells you what to prepend.

## How to use this reference

- Use `uaip_describe_command(CommandName="...")` to get the full parameter schema for a command
- Use `uaip_list_commands(ProviderPrefix="UAIP.Editor")` to filter by domain at runtime
- For the required Capability per command, see [Safety & Capabilities](safety.md)

## Symbols

| Symbol | Meaning |
|---|---|
| 🆓 | Available in the demo binary (also in Pro) |
| (no mark) | Pro-only command |
| 🧩 | Requires an optional UE plugin (the command is not registered if the plugin is disabled) |
| ⚠️ | Experimental — the behaviour or the contract may change, or a known limitation prevents it from working as documented |

## UAIP commands vs Toolset bridge commands

UAIP exposes two categories of commands:

- **UAIP commands** (`UAIP.*` prefix) — first-party commands provided by the plugin itself. They work regardless of UE version or Toolset plugin availability.
- **Toolset bridge commands** (`Toolset.*` prefix; UE 5.8+ with the relevant Toolset plugin installed) — a delegation layer over the official UE 5.8 Toolset framework. Most mirror an existing UAIP command, while a few surface functionality only available through Toolset.

The domain summary below lists counts only. To enumerate the actual Toolset bridge command names at runtime, use `uaip_list_commands(ProviderPrefix="Toolset")`.

---

## Domain summary

| Domain | Provider prefix | UAIP commands | Toolset bridge | Demo |
|---|---|---:|---:|---:|
| Core | `UAIP.Core` | 11 | — | ✅ |
| Editor Workspace | `UAIP.Editor.Workspace` | 21 | 1 | partial (13/21) |
| Editor Engine Log | `UAIP.Editor.Engine.Log` | 1 | 4 | ✅ |
| Editor Engine Plugin | `UAIP.Editor.Engine.Plugin` | 9 | 15 | partial (5/9) |
| Editor Engine CVar 🧩 | `Toolset.Editor.EngineManagement` | — | 1 | — |
| Editor Engine ConfigSettings | `UAIP.Editor.Engine.ConfigSettings` | 8 | 8 | partial (5/8) |
| Editor Observation | `UAIP.Editor.Observation` | 15 | — | ✅ |
| Editor Execution | `UAIP.Editor.Execution` | 9 | — | — |
| Editor UI Automation | `UAIP.Editor.UIAutomation` | 16 | 10 | ✅ |
| Editor Assets | `UAIP.Editor.Assets` | 51 | 6 | partial (29/51) |
| Editor SemanticSearch 🧩 | `UAIP.Editor.SemanticSearch` | 5 | 2 | — |
| Editor Level | `UAIP.Editor.Level` | 20 | 8 | partial (8/20) |
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
| Editor Python Extension 🧩 | `UAIP.Editor.Python` | 2 | — | — |
| Editor Sandbox 🧩 | `UAIP.Editor.Sandbox` | 6 | — | — |
| Editor WorldPartition | `UAIP.Editor.WorldPartition` | 34 | — | — |
| Editor Foliage | `UAIP.Editor.Foliage` | 11 | — | — |
| Editor DataRegistry 🧩 | `UAIP.Editor.DataRegistry` | 9 | 7 | — |
| Editor MotionMatching 🧩 | `UAIP.Editor.MotionMatching` | 23 | — | — |
| Editor AnimSequence | `UAIP.Editor.AnimSequence` | 12 | — | — |
| Editor ChaosDestruction | `UAIP.Editor.ChaosDestruction` | 29 | — | — |
| Editor Subsonic 🧩 | `UAIP.Editor.Subsonic` | 22 | — | — |
| Editor GroomAsset 🧩 | `UAIP.Editor.GroomAsset` | 35 | — | — |
| Editor Validation 🧩 | `UAIP.Editor.Validation` | 7 | — | — |
| Editor LiveLink 🧩 | `UAIP.Editor.LiveLink` | 11 | — | — |
| Runtime Engine Log | `UAIP.Runtime.Engine.Log` | 3 | — | partial (2/3) |
| Runtime Engine Plugin | `UAIP.Runtime.Engine.Plugin` | 5 | — | ✅ |
| Runtime Engine CVar | `UAIP.Runtime.Engine.CVar` | 4 | — | partial (2/4) |
| Runtime Engine Config | `UAIP.Runtime.Engine.Config` | 2 | — | partial (1/2) |
| Runtime PIE | `UAIP.Runtime.PIE` | 6 | 3 | ✅ |
| Runtime World | `UAIP.Runtime.World` | 9 | 1 | — |
| Runtime Observation | `UAIP.Runtime.Observation` | 8 | — | ✅ |
| Runtime Execution | `UAIP.Runtime.Execution` | 3 | — | — |
| Runtime Assertion | `UAIP.Runtime.Assertion` | 4 | — | ✅ |
| Runtime Input | `UAIP.Runtime.Input` | 11 | — | — |
| Runtime GAS 🧩 | `UAIP.Runtime.GAS` | 17 | — | — |
| Runtime Niagara 🧩 | `UAIP.Runtime.Niagara` | 4 | 4 | — |
| Runtime LiveLink | `UAIP.Runtime.LiveLink` | 12 | — | — |
| Runtime Insights Trace | `UAIP.Runtime.Insights.Trace` | 11 | — | partial (3/11) |
| Runtime Insights Analysis | `UAIP.Runtime.Insights.Analysis` | 3 | — | — |

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

## UAIP.Core

System-level commands for discovery, health, and session management.

| Command | Description |
|---|---|
| 🆓 `HealthCheck` | Plugin connectivity check — returns `Status`, `UAIPVersion`, `EngineVersion`, `BuildConfig`, `ProjectFilePath` (absolute path of the open `.uproject`, used by the MCP Bridge to verify it is attaching to the right editor instance), `TransportTimeouts` (per-transport async command timeout in seconds, e.g. `{"HTTP": 120, "WS": 12}`), `QueueCongestion` (how busy the deferred-execution queue is, as one of `None` / `Low` / `High` — the exact number waiting is not returned, since it would let one session infer another session's activity) |
| 🆓 `GetSystemInfo` | Returns UE version (Major/Minor/Patch/Changelist), project name, platform, build config, UAIP version |
| 🆓 `QueryCapabilities` | Returns `Capabilities` (the session's effective set), `RegisteredCapabilityCount` / `UngrantedCapabilityCount` (always) and `OperationalConstraints` (9 policy flags). Pass `IncludeUnavailable: true` to also get `RegisteredCapabilities` — every capability the loaded modules declare, each with `Name` / `DefaultPolicy` / `IsGranted`, so one this session does not hold can still be found by name; the deny-by-default ones are the entries whose `DefaultPolicy` is `Denied` |
| 🆓 `ListCommands` | Filtered command catalog (filters: `ProviderPrefix`, `KeywordFilter`, `IncludeUnavailable`, `Stability`; `ResultMode` — `Commands` (default) or `Providers` to list providers instead of commands; `Limit` — max results returned (1–1000); `IncludeDescription` — include each command's description text in the listing) |
| 🆓 `DescribeCommand` | Full metadata for a single command (schema, required capabilities, availability) |
| 🆓 `ListPlugins` | ⚠️ **Deprecated** — use `UAIP.Runtime.Engine.Plugin.ListPlugins` instead. List installed plugins and their enabled state (JSON) |
| 🆓 `EndSession` | End a session explicitly and release its server-side resources; its artifacts become GC candidates |
| 🆓 `ReloadCapabilities` | Reload the capability set from `Config/DefaultUAIP.ini` without restarting the editor (only registered when `AllowCapabilityReload=True`) |
| 🆓 `GetPendingInteractionStatus` | Reports where one pending interaction stands — `State`, `Cause`, `ElapsedSeconds`, `Prompt`, `Reason`, `Result` — without waiting for it to change. Requires the same explicitly given `SessionId` that started the interaction (an interactive command such as `DrawPCGSpline`); unknown, expired, and other-session all report `NotFound` identically |
| 🆓 `WaitForPendingInteraction` | Blocks until a pending interaction leaves `AwaitingUser`, or until this call's own `TimeoutSeconds` ceiling is reached (default 30, range [1, 600]), whichever comes first; on timeout the interaction itself is unaffected and keeps waiting for the human. Up to 4 concurrent calls may watch the same interaction, but reaching more than one requires `[UAIP.Transport] AllowConcurrentPassiveWaits` — see [Configuration](config.md) |
| 🆓 `CancelPendingInteraction` | Cancels a pending interaction the calling session started, without waiting for the human to act. An interaction already `Completed` is answered with `Success` rather than an error; the capabilities the starting command declared are re-checked against the session's current capability set |

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
| 🆓 `NormalizeEditorLayout` | Focus the main graph tab and hide transient panels |
| 🆓 `SetGraphZoom` | Set graph viewport zoom level |
| 🆓 `FrameGraphAll` | Zoom the graph viewport to fit all nodes |
| 🆓 `FrameGraphSelection` | Zoom the graph viewport to fit selected nodes |
| 🆓 `SetGraphSelection` | Select graph nodes by ID list |
| 🆓 `ShutdownEditor` | Shut down the UE Editor (optionally save packages) |
| 🆓 `RestartEditor` | Restart the UE Editor (optionally save packages) |
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

> **`FocusEditorTab`'s `GraphName` — response contract.** When `GraphName` is a non-empty string, `Result` carries four fields: `WindowFocusRequested` (bool — records that bringing the editor window to front was *requested*; it does not guarantee the OS actually put it in the foreground), `GraphNameRequested` (bool), `GraphNameApplied` (bool), and `Reason` — a closed set of three strings, `Applied` / `BlueprintEditorInterfaceUnavailable` / `OpenFailed`. Read `GraphNameApplied` and `Reason` rather than `Success` alone: a `BlueprintEditorInterfaceUnavailable` reason still reports `Success: true`, because the open editor genuinely has no Blueprint graph-navigation entry point (for example a ControlRig editor with `RigVM.UseNewEditor` enabled) and retrying the same input cannot change that. None of these four fields are set when `GraphName` is omitted or empty — callers must handle both "`Result` absent" and "`Result.GraphNameRequested` is `false`". Applying a graph move clears the editor's current UI selection, and for a Widget Blueprint opened in Designer mode, switches it to Graph mode first (needed to display the graph at all); both happen before the graph itself is opened, so they can already have taken effect even when the open subsequently fails with `OpenFailed`.
>
> ⚠️ **Breaking change** — two of `GraphName`'s error codes changed from `ExecutionFailed` to a non-retryable code, because a scenario's `RetryCount` only retries `ExecutionFailed` and retrying either of these can never succeed on the same input: naming a graph that does not exist in the asset now answers `NotFound` (previously `ExecutionFailed`); naming `GraphName` on an asset that is not Blueprint-derived now answers `InvalidParams` (previously `ExecutionFailed`). `OpenFailed` — a genuine failure to open the graph after its navigation entry point was found — is unchanged and remains `ExecutionFailed`, since that one is still worth retrying.
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

Bridge commands via the EditorToolset plugin (UE 5.8+). Provider: `Toolset.Editor.EngineManagement.*`.

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

## UAIP.Editor.Observation

Capture screenshots and dump editor state — all read-only.

| Command | Description |
|---|---|
| 🆓 `CaptureActiveWindowImage` | Screenshot of the active top-level editor window (PNG artifact). The editor does not have to be the foreground application: when no window is active, the main window is captured instead and `Result.CapturedWindow` says which one you got (`"ActiveWindow"` / `"MainWindow"`). The fallback only reaches the main window, so a floating asset editor or modal dialog needs `CaptureEditorTabImage` |
| 🆓 `CaptureEditorTabImage` | Screenshot of a specified editor tab's widget area, addressed by Slate layout identifier — `DumpEditorState`'s `ActiveTabId` can be passed straight through. Works with the editor in the background. ⚠️ Brings the named tab to the front of its stack before capturing (a tab behind a sibling is not drawn and would come back empty), so capturing changes which tab the user sees |
| 🆓 `CaptureGraphViewportImage` | Screenshot of an SGraphEditor viewport |
| 🆓 `DumpEditorState` | Active tab, open assets, window dimensions, etc. (JSON) |
| 🆓 `DumpSelectionState` | Current editor selection — actors, objects, graph nodes (JSON) |
| 🆓 `DumpOpenTabs` | List of open asset editor tabs (JSON) |
| 🆓 `DumpOutputLog` | Buffered Output Log as a text artifact (line count / filter support) |
| 🆓 `DumpMessageLog` | Message Log entries with category filter (JSON artifact) |
| 🆓 `DumpSlateTree` | Slate widget tree (JSON, root path filter support) |
| 🆓 `InspectMenu` | Top-bar menu structure under a path (labels, enabled, checked) |
| 🆓 `InspectContextMenu` | Context menu items for a target (without executing them) |
| 🆓 `ObserveWidget` | Time-series sampling of widget Visibility / Enabled / Hovered / Focused state |
| 🆓 `GetLogCategories` | List all registered engine log category names (optional substring filter) |
| 🆓 `ListGraphNodes` | List every node in a graph editor tab — `NodeId` (GUID), `NodeClass`, `NodeTitle`, `Position`. Works with any `UEdGraph`-based editor |
| 🆓 `CaptureViewportImageAnnotated` | Viewport screenshot with world-coordinate labels drawn on it (requires `ViewportAnnotationCapture`) |

---

## UAIP.Editor.Execution

Run tests, Python scripts, and Editor Utility Blueprints.

| Command | Description |
|---|---|
| `DiscoverAutomationTests` | Load the automation test modules and return summary counts of discovered tests |
| `ListAutomationTests` | Return a filtered list of automation tests as a JSON artifact |
| `RunAutomationTest` | Run a UE Automation Test by name and return Pass/Fail/Error report |
| `RunAutomationSpec` | Run a UE Automation Spec by name and return Pass/Fail/Error report |
| `GetAutomationTestStatus` | Return the current automation test manager status (inline by default) |
| `StopAutomationTests` | Request cancellation of the running automation test batch |
| `RunEditorPythonScript` 🧩 | Run an inline Python script or a `.py` file (requires `PythonScriptPlugin`) |
| `RunEditorUtilityBlueprint` | Run a specified Editor Utility Blueprint |
| `RunNamedEditorCommand` | Run a named editor console command via `GUnrealEd->Exec` |

> **Note**: `RunAutomationTest` (and its runtime counterpart `RunRuntimeAutomationTest`) runs **every matching test** when `RunAllMatching=true`, which is the default. To bound the run, pass `MaxMatchingTests` (1 or greater; omit it for no bound). `0` is rejected rather than read as "no bound" — they are opposite requests, and quietly turning one into the other is how a bounded run starts claiming full coverage.
>
> The report always carries `Summary.Matched` (how many tests matched the filter) and `Summary.Selected` (how many were actually run). **Both are stated whether or not they differ** — a line that appears only on truncation is one the reader has to already know about, since its absence would otherwise be indistinguishable from a build that never emitted it. The human-readable report and the Output Log carry the same pair.
>
> `TimeoutSec` bounds **each individual test**, not the batch (60 seconds by default). A larger match set still runs in full as long as every test finishes within that time. Separately, the runtime `RunRuntimeAutomationTest` bounds the whole bulk run at 600 seconds of wall clock; reaching it adds a `(bulk execution time limit reached)` entry to the report as an `Error`.
>
> **Changed in v1.1.0**: earlier releases stopped at a hundred matches and **gave the caller no way to tell** — `Pass=100 Fail=0` reads exactly like a clean run over the whole set. If you relied on that ceiling, pass `MaxMatchingTests=100` explicitly.

---

## UAIP.Editor.UIAutomation

Drive the editor UI — click, type, select, drag.

| Command | Description |
|---|---|
| 🆓 `ClickWidget` | Simulate a left click on a widget identified by path |
| 🆓 `SelectMenuItem` | Open and select a menu item by slash-separated label path |
| 🆓 `InputText` | Type text into a widget identified by path |
| 🆓 `SetCheckboxState` | Set the checked state of a checkbox |
| 🆓 `SetComboSelection` | Select a combo box item by label |
| 🆓 `DragGraphNode` | Drag a graph node by a pixel offset on a specified graph editor tab |
| 🆓 `ConnectGraphPins` | Connect two pins on a graph editor tab |
| 🆓 `AcceptDialog` | Accept the active modal dialog (click OK/Yes/Accept) |
| 🆓 `CancelDialog` | Cancel the active modal dialog (click Cancel/No) |
| 🆓 `InvokeContextMenuAction` | Right-click a target and execute an item from the context menu |
| 🆓 `HoverWidget` | Simulate OnMouseEnter on a widget |
| 🆓 `PressKey` | Simulate a key press with modifiers (blacklist for dangerous shortcuts) |
| 🆓 `WaitForWidget` | Poll until a widget reaches an expected state |
| 🆓 `FillForm` | Bulk-fill a form widget using a sequential state machine |
| 🆓 `SnapshotUI` | Capture a structured, scope-filterable snapshot of the UI and report what was left out |
| 🆓 `OpenPasswordTestWindow` | Open a floating test window holding a password `SEditableTextBox` — provides a target for password-field policy tests |

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

Bridge commands via the `SlateInspectorToolset` (UE 5.8+). Provider: `Toolset.Editor.SlateInspector.*`. Widgets are addressed by refPath rather than by the widget-path syntax the native commands use. Every bridge command in this section now requires the same capability as its native counterpart (see [Safety & Capabilities](safety.md)) — earlier releases dispatched these without a capability check.

| Command | Description |
|---|---|
| `Toolset.Editor.SlateInspector.SnapshotUI` | Snapshot the widget tree at the given ref |
| `Toolset.Editor.SlateInspector.ObserveWidget` | Register a widget for observation; returns the observer `Identifier` |
| `Toolset.Editor.SlateInspector.UnobserveWidget` | Stop observing the widget registered under an `Identifier` |
| `Toolset.Editor.SlateInspector.ListObservers` | List every currently active widget observer |
| `Toolset.Editor.SlateInspector.ClickWidget` | Simulate a mouse click on the widget at the given ref |
| `Toolset.Editor.SlateInspector.HoverWidget` | Move the cursor over the widget at the given ref |
| `Toolset.Editor.SlateInspector.InputText` | Type text into the widget at the given ref |
| `Toolset.Editor.SlateInspector.PressKey` | Send a key press; modifier prefixes are supported (e.g. `Ctrl+S`) |
| `Toolset.Editor.SlateInspector.SetComboSelection` | Select an option in a combo box widget |
| `Toolset.Editor.SlateInspector.FillForm` | Fill multiple form fields in a single call |

> **Note**: `Toolset.Editor.SlateInspector.PressKey` applies the same blocked-shortcut list as the native `PressKey` command, but it has no way to resolve which widget currently has focus, so it blocks **Backspace unconditionally** — the native command's exemption for a focused text-input widget does not carry over to the bridge.

---

## UAIP.Editor.Assets

Open, search, create, duplicate, rename, delete assets and folders.

| Command | Description |
|---|---|
| `OpenAsset` | Open the specified asset in its editor |
| `CloseAsset` | Close all editors for the specified asset |
| `SaveAsset` | Write only the named assets to disk (requires `AssetMutate`). Shows no dialog, so it completes unattended |
| 🆓 `ListDirtyPackages` | List the packages holding unsaved changes (pre-flight check before saving) |
| 🆓 `SearchAssets` | Search assets by path / class / tag |
| `CreateAsset` | Create a new asset of the specified class |
| 🆓 `ListCreatableAssetClasses` | Return every UClass that `CreateAsset` can target, with factory count and default factory (heavy call) |
| 🆓 `ListFactoriesForClass` | Return the factory candidates for a `ClassName`, each with its `FactoryParams` schema |
| `DuplicateAsset` | Duplicate an existing asset |
| `CopyAsset` | Copy an asset to a new full package path (fails if the destination exists; requires `AssetCreate`) |
| `RenameAsset` | Rename / move an asset to another path |
| `MoveAsset` | Move an asset to another folder keeping its name; reports whether a redirector was left behind (requires `AssetMutate`) |
| `DeleteAsset` | Delete an asset |
| `CreateFolder` | Create a new folder in the Content Browser |
| `DeleteFolder` | Delete an empty folder (returns `NotEmpty` if not empty) |
| `ForceDeleteFolder` | Delete a folder and its assets (max 50 items, no external-reference check) |
| `MoveFolder` | Move every asset in a folder to a destination folder, preserving sub-folders; partial failures are listed in `FailedAssets` (requires `AssetFolderRefactor`) |
| 🆓 `GetSelectedAssets` | Return the assets currently selected in the Content Browser |
| `SelectAssets` | Select the specified assets in the Content Browser (requires `ContentBrowserNavigate`) |
| 🆓 `GetContentBrowserPath` | Return the current folder path shown in the Content Browser |
| `SetContentBrowserPath` | Navigate the Content Browser to a specified folder (requires `ContentBrowserNavigate`) |
| 🆓 `GetOpenAssets` | Return the list of assets currently open in an asset editor |
| 🆓 `ListAssetRedirectors` | List asset redirectors under a folder (`/Game` project-wide by default) with source/destination paths, without loading any assets |
| `FixAssetRedirectors` (requires `RedirectorFixup`) | Fix up and delete all resolvable asset redirectors under `/Game` (project-wide, recursive, always) |
| `FixUpRedirectorsInFolder` (requires `RedirectorFixup`) | Same fix-up limited to one folder; unresolved entries are returned in `FailedRedirectors` |
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

> **Note**: `StartAssetAudit` is a **job-style command** — it returns immediately and the work continues across editor frames rather than blocking the call. If your `uaip_execute` call includes an MCP `_meta.progressToken`, the bridge sends a `notifications/progress` update roughly every 5 seconds while the call is pending, carrying only the elapsed time and the editor's own state (`STARTING` / `RUNNING` / `UNRESPONSIVE`) — it never carries the job's internal progress; poll `GetAssetAuditStatus` for that. This applies to `uaip_execute` only (not `uaip_run_scenario`), only when the client sends a progress token, and whether the notification is actually surfaced to you depends on the MCP client. The per-frame time budget the audit job spends on each scan step is configurable via `Config/DefaultUAIP.ini` → `[UAIP.Jobs] AuditStepBudgetMs` (default `10.0`, clamped to `[1.0, 100.0]`; a value outside that range is silently clamped rather than rejected).


> **Note**: There are two ways to save, and they differ in blast radius. `SaveAllPackages` writes **every** package holding unsaved changes, so work a person left in progress is committed alongside yours. When you know what you changed, name it with `SaveAsset` instead. To find out what a save would write, call `ListDirtyPackages` first: it reads the same source the editor-wide save consults (`GetDirtyContentPackages` / `GetDirtyWorldPackages`), so its list and the set `SaveAllPackages` would write are the same.
>
> `SaveAsset` only ever writes packages that are **loaded and dirty**. An asset that was never loaded cannot hold unsaved changes, so it is returned under `Skipped` with `Reason: "NotLoaded"` rather than being loaded just to write it back; one that is already saved comes back as `NotDirty`. Neither is an error. Paths under `/Engine/` and `/Script/` are refused as `Failed` with `WriteForbidden` because they reach outside the project, but the call itself still succeeds and the remaining assets are saved. Only `DisableSave=True` in the safety policy rejects the whole call, with `PolicyViolation`.
>
> **Relationship to `ApplyValidationFix`**: when a validator wraps its fix in `FAutoSavingFixer`, applying it through UAIP does **not** write to disk. The engine performs that auto-save through a modal confirmation dialog, which cannot complete when nobody is there to answer it. `ApplyValidationFix` reports `Applied: true` together with `AssetSaved: false` in that case, so **treat `AssetSaved: false` as the signal to persist the change yourself with `SaveAsset`**.

> **Note — a class named in `FactoryParams` can need a capability of its own.** Some domains admit a class named there through the same policy that gates their editing commands — StateTree's `FactoryParams.SchemaClass` and ControlRig's `FactoryParams.ParentClass` today. Neither is loaded on demand any more: a class that is not already in memory is refused rather than loaded in order to decide whether the caller was allowed to name it. When the session does not hold what the named class requires, `CreateAsset` answers **`CapabilityNotAvailable`**, with the missing capability names in the message — the same as everywhere else — see [Capability-gated custom types](#capability-gated-custom-types).

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
| 🆓 `ListActorComponents` | List every component of an actor placed in the level. Each entry carries the `ComponentId` the three commands below take, plus `ComponentClassPath`, `Origin` (`Instance` / `SimpleConstructionScript` / `UserConstructionScript` / `Native`), `IsEditableInstance`, `IsSceneComponent`, `IsRootComponent`, `AttachParentComponentName` and `AttachSocketName`. Each entry also reports what **adding** a component of that class would take — `Admission` (`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`) with `RequiredCapabilities` and `MissingCapabilities` — which is how a caller learns about `ComponentCustomTypeEdit` before attempting a write. Reads the editor world, so it stays answerable during PIE. Requires `EditorInspect` |
| `AddActorComponent` | Add a component to an actor placed in the level — what the Details panel's *Add Component* button does, as one undo step. Returns the new component's `ComponentId`. `ComponentName` may be omitted to let the engine generate one; `AttachParentComponentName` / `AttachSocketName` apply only to a `USceneComponent` subclass, and the new component becomes the root when the actor has none. The class is resolved against what is already loaded and is never loaded on request (an unloaded class is `NotFound`). Requires `ActorComponentEdit`, plus `ComponentCustomTypeEdit` for a class outside `/Script/Engine` and `/Script/LiveLinkComponents` — see [Capability-gated custom types](#capability-gated-custom-types). Refused during PIE |
| `DeleteActorComponent` | Remove an instance component from an actor placed in the level, as one undo step. Only `Origin: Instance` components can be removed — an SCS one belongs to the Blueprint component commands, a construction-script one is rebuilt by the script, and a native one exists on every instance of the class; each refusal names the route that does own it, and the actor's `DefaultSceneRoot` is refused too. Children of a removed scene component are re-attached to its parent, keeping their world transforms. `ExpectedComponentClass` is required (pass back the `ComponentClassPath` from the listing) so a stale identifier is refused with `NotFound` rather than followed. Requires `ActorComponentEdit`. Refused during PIE |
| `ReparentActorComponent` | Attach a scene component of a placed actor beneath a different component of the same actor, keeping its world transform, as one undo step. Both must be `USceneComponent` subclasses on that actor and the moved one must be `Origin: Instance`. There is no "attached to nothing" — detaching is expressed by naming the actor's root as `NewParentComponentName` — and the root itself cannot be moved. A cycle, or a socket the new parent does not have, is refused before anything is written. `ExpectedComponentClass` is required, same as above. Requires `ActorComponentEdit`. Refused during PIE |

> **Note — instance components only.** These four commands operate on components of an actor **placed in the level**. Components declared on the actor's Blueprint go through [UAIP.Editor.Blueprint — Components — SCS](#components--scs-8) instead. Renaming and duplicating an instance component have no counterpart here; add the component again under the name you want.

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

### Variables & graph (10)

| Command | Description |
|---|---|
| `AddBlueprintVariable` | Add a member variable to a Blueprint (type, default, tooltip). The default is now validated once the variable's type has resolved, and a refused default **removes the variable again** rather than leaving it behind with an empty value. The default is engine text only — a reference or container default is refused whatever the session holds; set those afterwards with `SetBlueprintDefault`, which takes `ValueJson` |
| `DeleteBlueprintVariable` | Remove a member variable |
| `SetBlueprintVariableDefault` | Update a Blueprint variable's CDO default value |
| `AddGraphNode` | Add a node to any graph in a Blueprint asset (VariableGet/Set, FunctionCall, Event, ...) — not just the event graph and function graphs. `GraphName` or `GraphGuid` selects the target; see the note below the table for graph selection, ambiguity, and the two-stage acceptance check |
| `DeleteGraphNode` | Delete a graph node by GUID (EntryNode / Tunnel cannot be deleted) |
| `ConnectBlueprintPins` | Connect two pins in a Blueprint graph |
| `DisconnectBlueprintPins` | Disconnect a pin connection |
| `ListBlueprintPins` | List pins of a Blueprint graph node |
| `SetPinDefaultValue` | Set a default value on a Blueprint graph node pin (auto-selects DefaultValue / DefaultObject / DefaultTextValue based on pin type) |
| `GetPinDefaultValue` | Get the current default value of a Blueprint graph node pin |

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

> ⚠️ **Breaking change — `ConnectBlueprintPins`, `DisconnectBlueprintPins`, `DeleteGraphNode`, `GetPinDefaultValue`, `ListBlueprintPins`, and `SetPinDefaultValue` now answer `NotFound` when the node or pin they were asked for does not exist** (previously `ExecutionFailed`). A scenario's `RetryCount` only retries `ExecutionFailed`, so before this change a request naming a nonexistent `NodeId` or `PinName` was retried anyway, even though repeating it can never succeed.
>
> `GetPinDefaultValue` additionally had a defect fixed here: when `PinName` named no pin on the target node, the handler had no branch for that case at all and fell through to reading a pin that was never found, an unchecked access with undefined behavior. It now reports `NotFound` for a `PinName` that does not match any pin on the node, the same as the other commands in this list.

### Components — SCS (8)

| Command | Description |
|---|---|
| `ListBlueprintComponents` | List all components visible from a Blueprint (SCS, Inherited, Native) |
| `AddBlueprintComponent` | Add a new SCS component node to a Blueprint. ⚠️ Now additionally requires `ComponentCustomTypeEdit` for a project- or plugin-defined component class — see the note below |
| `DeleteBlueprintComponent` | Delete an SCS component from a Blueprint |
| `RenameBlueprintComponent` | Rename an SCS component |
| `ReparentBlueprintComponent` | Change an SCS component's parent |
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
| `SetSlotProperties` | Set a widget's slot properties (32 KiB limit, `/Game/` UObject refs only). A reference now requires `WidgetSlotReferenceEdit` and a struct or container `PropertyStructuredEdit`, and those values are supplied as a JSON document rather than engine bracket text — read the property first for its `WriteInputForm`. A refused write leaves no undo entry and does not mark the asset dirty |
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
| `Toolset.Editor.GameplayTags.RemoveTag` | Remove a tag from the project tag table; asset references are **not** updated (requires `GameplayTagEdit`) |
| `Toolset.Editor.GameplayTags.RenameTag` | Rename a tag in INI only — no reference update and no redirect entry. Prefer the native `RenameGameplayTag` (requires `GameplayTagEdit`) |

---

## UAIP.Editor.GameFeatures 🧩

GameFeature Plugin management. Requires `GameFeatures` + `GameFeaturesEditor` plugins.

| Command | Description |
|---|---|
| `ListGameFeatures` 🧩 | List GameFeature Plugins with a `FilterState` filter (All / Installed / Mounted / Registered / Loaded / Active) |
| `GetGameFeatureInfo` 🧩 | GFP details (State, Actions, dependencies) |
| `GetGameFeatureActions` 🧩 | List the actions declared by a GameFeature Plugin's `UGameFeatureData` |
| `CreateGameFeaturePlugin` 🧩 | Scaffold a new GameFeature Plugin (with name validation) |
| `DeleteGameFeaturePlugin` 🧩 | Delete a GameFeature Plugin and its content from disk |

### Toolset bridges — GameFeatures (4) 🧩

Bridge commands via the `GameFeaturesToolset` (UE 5.8+, Experimental). Provider: `Toolset.Editor.GameFeatures.*`.

| Command | Description |
|---|---|
| `Toolset.Editor.GameFeatures.ListGameFeatures` | List all registered GameFeature Plugins with their current state |
| `Toolset.Editor.GameFeatures.FindGameFeatureData` | Resolve the `UGameFeatureData` asset refPath for a named plugin |
| `Toolset.Editor.GameFeatures.GetActions` | List the action class names of a `UGameFeatureData` (takes `{"refPath": "..."}`) |
| `Toolset.Editor.GameFeatures.CreateGameFeaturePlugin` | Create a content-only GameFeature Plugin (requires `GameFeatureCreate`) |

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
| `GetSystemSchema` 🧩 | JSON Schema of all editable top-level `UNiagaraSystem` properties (constant across systems — cacheable) |
| `GetEmitterSchema` 🧩 | JSON Schema of all editable top-level emitter properties (cacheable) |
| `GetRendererSchema` 🧩 | JSON Schema for one `UNiagaraRendererProperties` class, selected by `RendererClassPath` |
| `GetDataInterfaceSchema` 🧩 | JSON Schema for one `UNiagaraDataInterface` class, selected by `DataInterfaceClassPath` |
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
| `GetAvailableDynamicInputs` 🧩 | Dynamic input scripts compatible with a specific module input |

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
> **⚠️ Breaking change — `GetAvailableDynamicInputs`'s pre-5.8 fallback now fails instead of always answering an empty list.** Which dynamic input scripts a stack input accepts is decided by the same engine surface that offers them inside the stack UI, and earlier engine versions have no graph-level equivalent to read it from. The fallback used to answer `{DynamicInputs: []}` and report success for every call, which reads as "no dynamic input fits this input" — indistinguishable from the question never having been asked in the first place. It now answers `ExecutionFailed`, with `ErrorMessage` explaining that this needs an engine API introduced in Unreal Engine 5.8 and is reported as a failure rather than as an empty result for exactly that reason, so it cannot be mistaken for a genuine "no matches" answer. **UE 5.8+ is unaffected** — its own branch already could fail (an unresolved system, emitter, script or module) and keeps doing so unchanged.
>
> **⚠️ Breaking change — `GetEmitterSchema`, `GetSystemSchema`, `GetRendererSchema` and `GetDataInterfaceSchema`'s pre-5.8 fallback now fails instead of always answering an empty `PropertySchema`**: all four used to report success on every call, with `PropertySchema` fixed at an empty string — reading as "this class has no editable properties", indistinguishable from the JSON Schema having genuinely never been built. `PropertySchema` is built by an engine API introduced in UE 5.8, and earlier engine versions have no equivalent to build it from. All four now answer `ExecutionFailed`, with `ErrorMessage` explaining that the command needs an engine API introduced in Unreal Engine 5.8 and is reported as a failure rather than as an empty result for exactly that reason — the same wording `GetStackIssues` and `ApplyStackIssueFix` use below, for the same reason. `GetRendererSchema` and `GetDataInterfaceSchema` are refused before their `RendererClassPath` / `DataInterfaceClassPath` argument is even resolved, so the `RendererClass` / `TypeName` field that used to accompany the empty `PropertySchema` is gone from the failure response too — an unresolved class is still reported separately as `NotFound`, before reaching this refusal. **UE 5.8+ is unaffected** — its own branch already could fail (an unresolved system or class) and keeps doing so unchanged. Read `GetRendererData` / `GetEmitterData` / `GetSystemData` for the actual property values on every engine version, as before.

#### Stack issues (2)

| Command | Description |
|---|---|
| `GetStackIssues` 🧩 | All stack issues (errors / warnings / info, including dismissed) with the `IssueId` and `FixId` needed below |
| `ApplyStackIssueFix` 🧩 | Apply a Fix-style automated fix by `IssueId` + `FixId` (Link-style fixes are rejected; requires `NiagaraStackAutoFix`) |

> **⚠️ Breaking change — `GetStackIssues`'s pre-5.8 fallback now fails instead of always answering no issues, and `ApplyStackIssueFix`'s pre-5.8 fallback now fails instead of always answering `Applied: false`.** Both used to report success on every call — `GetStackIssues` with an empty `Issues` array, `ApplyStackIssueFix` with `{Applied: false}` — which reads as "no issues exist" / "this fix could not be applied", indistinguishable from the check never having run in the first place. Both now answer `ExecutionFailed`, with `ErrorMessage` explaining that the command needs an engine API introduced in Unreal Engine 5.8 and is reported as a failure rather than as an empty result for exactly that reason — the same wording for both, since they are meant to be read as a pair. **`ApplyStackIssueFix` keeps its ordinary `{Success: true, Applied: false}` answer for a genuine "this Fix could not be applied" outcome**, exactly as before — only the engine-version refusal is new, and a fix that legitimately does not apply is still reported success with `Applied: false`, never `ExecutionFailed`. **UE 5.8+ is unaffected for both commands**, including `ApplyStackIssueFix`'s ordinary "could not be applied" outcome, which was already reported this way and stays that way.

#### Editing (21)

| Command | Description |
|---|---|
| `AddEmitter` 🧩 | Add an emitter to a Niagara system |
| `RemoveEmitter` 🧩 | Remove an emitter |
| `DuplicateEmitter` 🧩 | Duplicate an emitter |
| `SetEmitterEnabled` 🧩 | Toggle emitter enabled state |
| `SetEmitterName` 🧩 | Change emitter name |
| `SetEmitterData` 🧩 | Set emitter data |
| `AddRenderer` 🧩 | Add a renderer to an emitter |
| `RemoveRenderer` 🧩 | Remove a renderer |
| `SetRendererData` 🧩 | Set renderer data (requires `NiagaraStackEdit`). When the emitter has no renderer of the named class the command now answers `NotFound` — it no longer falls back to writing whichever renderer came first. A property the write path cannot handle fails the whole request with `PolicyViolation` instead of being ignored, a struct default that only parses part-way is refused with `InvalidParams` instead of being taken as the default, and a successful write raises `PostEditChangeProperty` so the editor reflects it immediately |
| `AddModule` 🧩 | Add a module to an emitter module stack |
| `RemoveModule` 🧩 | Remove a module |
| `MoveModule` 🧩 | Move a module within the stack |
| `SetModuleEnabled` 🧩 | Toggle module enabled state |
| `SetStackInputData` 🧩 | Set a module stack input value |
| `SetSystemData` 🧩 | Set system data |
| `AddUserVariables` 🧩 | Add user variables to a system |
| `RemoveUserVariables` 🧩 | Remove user variables |
| `CompileNiagaraSystem` 🧩 | Compile the Niagara system |
| `AddSetParametersModule` 🧩 | Add a Set Parameters module to a stack and register initial parameter entries. The `DefaultValue` field is applied for common types (float, int, bool, struct) and, with `NiagaraReferenceEdit`, for a data interface or object parameter given as an object path — see the note below. |
| `AddSetParameterEntry` 🧩 | Add a parameter entry to an existing Set Parameters module. Requires `ScriptName` (e.g. `Spawn`, `Update`). The `DefaultValue` field is applied for common types (float, int, bool, struct) and, with `NiagaraReferenceEdit`, for a data interface or object parameter given as an object path — see the note below. |
| `RemoveSetParameterEntry` 🧩 | Remove a parameter entry from a Set Parameters module. Requires `ScriptName` (e.g. `Spawn`, `Update`). |

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
| `SetAnimGraphNodeProperty` | Write an `EditAnywhere` property on an AnimGraph node by dot-notation `PropertyPath`. References go through `ValueJson` and `AnimBlueprintReferenceEdit`, structs / containers through `PropertyStructuredEdit` — see [Writing references, structs and containers](#writing-references-structs-and-containers) |
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
| `GetBehaviorTreeNodeList` | Flat list of every node — `NodeGuid`, `NodeClass`, `DisplayName`, `Depth` (0 = root composite), `ParentNodeGuid` |
| `GetBehaviorTreeSubtree` | Recursive subtree (Composite / Task / Decorator / Service) rooted at a `NodeGuid`, `MaxDepth` 1–32 |
| `GetAvailableBTCompositeClasses` | List `UBTCompositeNode` subclasses — feed `ClassPath` to `AddBehaviorTreeCompositeNode`. Each entry now carries `Admission` (`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`) plus `RequiredCapabilities` / `MissingCapabilities`, from the same policy the add command validates against. No longer filtered to the modules this domain ships. Ordered by `ClassPath`; reports `TotalCount`, `ReturnedCount`, `Truncated` (max 200). `SchemaVersion` is now `2` — see the note below |
| `GetAvailableBTTaskClasses` | List `UBTTaskNode` subclasses — feed `ClassPath` to `AddBehaviorTreeTaskNode`. Reports the same admission and count fields as above |
| `GetAvailableBTDecoratorClasses` | List `UBTDecorator` subclasses — feed `ClassPath` to `AddBehaviorTreeDecoratorNode`. Reports the same admission and count fields as above |
| `GetAvailableBTServiceClasses` | List `UBTService` subclasses — feed `ClassPath` to `AddBehaviorTreeServiceNode`. Reports the same admission and count fields as above |
| `AddBehaviorTreeCompositeNode` | Add a Composite node (Sequence / Selector / SimpleParallel) — a class from outside the modules this domain ships needs a capability, see the note below |
| `AddBehaviorTreeTaskNode` | Add a Task node by TaskClass — sub-tree runners and Blueprint-backed tasks additionally need their own capability, see the note below |
| `AddBehaviorTreeDecoratorNode` | Attach a Decorator to a parent node — same checks as above |
| `AddBehaviorTreeServiceNode` | Attach a Service to a parent Composite node — same checks as above |
| `RemoveBehaviorTreeNode` | Remove a node by NodeId — needs the same capabilities the node's own class asks for |
| `GetBehaviorTreeNodeProperties` | Every property a node's `NodeInstance` declares — `PropertyName`, `PropertyType` (the C++ type name), `PropertyValue` in the exact form `SetBehaviorTreeNodeProperty` accepts back for it, and a nested `WriteRequirements` object. A `FBlackboardKeySelector` property is reported as the bare key name, matching the write command's special-cased handling of it. Read-only; permitted during PIE (degraded mode). Requires `EditorInspect` |
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
| `AddMixerChildTrack` | Add a ControlRig child track parented to the layer at `LayerIndex`, creating a ControlRig instance of `ControlRigPath` (must derive from `UControlRig`) and attaching its parameter section. `LayerIndex` may equal the current layer count to append a new row. Optional `IsLayered` (default false) configures the new ControlRig as additive. Fails with `Conflict` (no side effects) when the target layer already has a child track or animation sections |
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
| `FindOrCreateControlRigTrack` | Find or create a ControlRig parameter track for a binding; reports `TrackCreated`. Optional `IsLayered` (default false) configures a newly created ControlRig as additive; ignored when an existing track is found |
| `BakeToControlRig` | Bake a binding's animation onto a ControlRig track (display-rate frames, `Tolerance` 0.0–1.0) |
| `KeyControls` | Key the given controls at one display-rate frame (all visible controls when `ControlNames` is empty) |
| `KeyControlsAtFrames` | Key the given controls at multiple display-rate frames |
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
| `AddVariable` | Add a RigVM variable. The default value is validated once the variable's type has resolved, and a refused default **removes the variable again**, matching `AddBlueprintVariable`. The default is engine text only — set a reference or container default afterwards with `SetBlueprintDefault`. A refused call does not mark the asset dirty |
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

**`Toolset.Editor.ControlRig.*` (44)** — mirror of the native asset-editing commands above. Groups: asset creation (1), hierarchy observation (8), hierarchy editing (7), graph management (10), nodes (7), pins (6), variables (5).

**`Toolset.Editor.SequencerControlRig.*` (63)** — animation-time control authoring. Implemented in the Sequencer module (`SequencerControlRigTools`) but documented here because every command acts on ControlRig controls. Requires `MovieSceneAnimMixer` in addition to ControlRig. Groups:

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

> **Prerequisite — the plugin has to be named in your `.uproject`**: UAIP links against `ControlRigDynamics` only when the project declares it **explicitly**. Add `{ "Name": "ControlRigDynamics", "Enabled": true }` to the `Plugins` array of your `.uproject` and rebuild. The check reads that entry and nothing else — a plugin the engine considers enabled for any other reason does not count. Without the entry the whole domain is missing from `uaip_list_commands`, and `uaip_list_commands(IncludeUnavailable=true)` reports it as `UnavailableReason: HandlerUnavailable`.

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

> **⚠️ Prerequisite — "the plugin is enabled but the commands are missing" starts here**: `ControlRigPhysics` is enabled by default by the engine, so the Plugins window shows it as on and its rig units already appear in the ControlRig editor — and yet UAIP registers none of these commands until the project names the plugin **explicitly**. Add `{ "Name": "ControlRigPhysics", "Enabled": true }` to the `Plugins` array of your `.uproject` and rebuild. The check reads that entry and nothing else; a plugin the engine turns on by default is invisible to it. Without the entry the whole domain is missing from `uaip_list_commands`, and `uaip_list_commands(IncludeUnavailable=true)` reports it as `UnavailableReason: HandlerUnavailable`.

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
| `DeleteInputAction` | Delete an Input Action asset |
| `DeleteMappingContext` | Delete an Input Mapping Context asset |
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
| `GetDataLayerInfo` | Get detailed info for a Data Layer instance — type, runtime state, visibility, and parent hierarchy |
| `CreateDataLayerAsset` | Create a new Data Layer asset in the Content Browser (requires `DataLayerEdit`) |
| `DeleteDataLayerAsset` | Delete a Data Layer asset (requires `DataLayerEdit`) |
| `CreateDataLayerInstance` | Create a new Data Layer instance in the current level from a Data Layer asset (requires `DataLayerEdit`) |
| `DeleteDataLayerInstance` | Delete a Data Layer instance from the current level (requires `DataLayerEdit`) |
| `SetDataLayerType` | Set the type of a Data Layer instance — Editor or Runtime (requires `DataLayerEdit`) |
| `SetDataLayerInitialRuntimeState` | Set the initial runtime state of a Data Layer — Unloaded, Loaded, or Activated (requires `DataLayerEdit`) |
| `SetDataLayerIsLoadedInEditor` | Set whether a Data Layer is loaded in the editor viewport (requires `DataLayerEdit`) |
| `SetDataLayerVisibility` | Set the visibility of a Data Layer in the editor (requires `DataLayerEdit`) |
| `SetParentDataLayerInstance` | Set the parent Data Layer instance, building a hierarchy (max 64 levels; requires `DataLayerEdit`) |
| `GetActorDataLayers` | Get the Data Layer instances assigned to an actor |
| `AddActorToDataLayer` | Add an actor to a Data Layer instance (requires `DataLayerEdit`) |
| `RemoveActorFromDataLayer` | Remove an actor from a Data Layer instance (requires `DataLayerEdit`) |
| `GetActorsInDataLayer` | List all actors assigned to a specific Data Layer instance |

### HLOD (7)

| Command | Description |
|---|---|
| `ListHLODLayers` | List all HLOD Layer assets in the project |
| `CreateHLODLayer` | Create a new HLOD Layer asset under `/Game/` (requires `HLODBuild`) |
| `DeleteHLODs` | Delete built HLOD data for a specified HLOD Layer (requires `HLODBuild`) |
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

> **Prerequisite**: `DataValidation` ships with the engine and is enabled by default, but UAIP links against it only when the project names it **explicitly**. Add `{ "Name": "DataValidation", "Enabled": true }` to the `Plugins` array of your `.uproject` and rebuild. Without that entry the whole domain is missing from `uaip_list_commands`, and `uaip_list_commands(IncludeUnavailable=true)` reports it as `UnavailableReason: HandlerUnavailable`.

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
| `StartValidationJob` | Validate a folder (`PackagePath` + `Recursive`) or an explicit `AssetPaths` list — one or the other, never both and never neither — in steps across many frames, and answer with a `JobId` rather than a result. `MaxAssets` bounds what is kept after redirectors are resolved and external objects are folded into their owners; anything dropped raises `Summary.AssetLimitReached`. A folder so wide that enumeration alone exceeds the internal ceiling fails outright with `EnumerationLimitExceeded` rather than validating an arbitrary prefix of it, so narrow the folder rather than lowering `MaxAssets`. Starting a second job while one of the same session is still running stops the earlier one and reports `ReplacedPreviousJob`; starting again too soon after the last one answers `TooManyRequests`. `Recursive` is meaningful only alongside `PackagePath`; passing it with `AssetPaths` is rejected rather than ignored, as is an `AssetPaths` list longer than 20,000 |

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

Editor-side LiveLink work: preset assets, binding a Subject to a placed actor's LiveLink controller component, MessageBus discovery and connection, and Take Recorder driven recording. **Requires both the `LiveLink` and the `Takes` plugins**; with either one disabled at build time the whole provider is compiled out and these commands return `CommandNotFound`. Built with both enabled but running with LiveLink switched off, they are still listed — as `Available: false` — so a caller finds out from the listing rather than from a failed call.

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

| Command | Description |
|---|---|
| `SpawnActor` | Spawn an actor of a class in the active PIE world (requires `RuntimeActorManipulation`) |
| `DestroyActor` | Destroy an actor in the active PIE world (requires `RuntimeActorManipulation`) |
| `TeleportActor` | Teleport an actor to a world-space location / rotation |
| `PossessActor` | Have a player controller possess an actor |
| `SetTimeScale` | Set the global time dilation of the active game world |
| `QuitGame` | Request a graceful quit of the running game process |
| `ExecuteConsoleCommand` | Execute a console command in the active game world (requires `RuntimeExecCommand`) |
| `GetConsoleVariable` | Value, type and help text of a console variable; sensitive names report as not found (requires `RuntimeCVarRead`) |
| `SearchConsoleVariables` | Wildcard (`*`) search over registered console variables — `MaxResults` default 50, max 200; sensitive names are excluded |

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
| 🆓 `DumpActorState` | State of a specified actor (optionally including components) |
| 🆓 `DumpComponentState` | State of a specified actor component |
| 🆓 `DumpRuntimeLog` | Buffered runtime log as a text artifact |
| 🆓 `CapturePerformanceSnapshot` | CPU / GPU performance snapshot (FPS, memory, draw calls) |
| 🆓 `CheckpointCapture` | Combined screenshot + state dump (scenario primitive) |
| 🆓 `SearchLoadedClasses` | Search loaded classes (used for runtime introspection) |

---

## UAIP.Runtime.Execution

Test execution in PIE / Standalone.

| Command | Description |
|---|---|
| `RunFunctionalTest` | Run an `AFunctionalTest` actor by asset path and return a JSON report |
| `RunRuntimeAutomationTest` | Run a UE Automation Test in PIE context |
| `RunGauntletTest` | Launch a Gauntlet test as an external process via RunUAT |

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
| `SetAttributeValue` 🧩 | Set an attribute's base value (`AttributeName` format `UMyAttributeSet.Health`) |
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
| `DumpInputState` | Dump current input state (pressed keys, axis values, active mapping contexts with priority, and — with `IncludeActionStates=true` — per-action trigger state) |
| `GetEnhancedInputActionValue` | Get the current value of an Enhanced Input Action |

---

> **Note**: `DumpInputState` always reports `ActiveMappingContexts` (sorted by `Priority` descending, then `Path` ascending) and `EnhancedInputState` (`"Available"` / `"Unavailable"`, telling apart "queried and found none" from "could not query"). Pass `IncludeActionStates=true` to additionally get `ActionStates[]` — one entry per action reachable from the active mapping contexts, each carrying `Trigger` (one of the six `ETriggerEvent` values, including `"None"` for an action that was evaluated but is not currently firing), `ValueX`/`ValueY`/`ValueZ`, `SourceContexts[]` (which active context configured it) and `ConfiguredKeys[]` (deduplicated, sorted) — plus `ActionStatesTotalCount` and `ActionStatesTruncated` (capped at 256, sorted by `ActionPath`). Leaving `IncludeActionStates` at its default `false` keeps the call cheap; the flag is opt-in specifically because its cost scales with the number of mapped actions rather than the number of loaded mapping contexts.

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

**No plugin requirement, and no 🧩.** The client interface these commands use ships in the engine's own always-present `LiveLinkInterface` module, not in the optional `LiveLink` plugin, so the commands are **always registered**. When no LiveLink client is present — the `LiveLink` plugin disabled — they report `Available: false` in `uaip_list_commands` / `uaip_describe_command` rather than vanishing, and `ListLiveLinkSources` answers `LiveLinkAvailable`, so **one call tells you whether LiveLink is usable in this environment**. Preset, connection and recording commands live in [UAIP.Editor.LiveLink](#uaipeditorlivelink-), which does require plugins.

**Naming a Subject.** Two different Sources may publish a Subject of the same name. Reads accept a bare `SubjectName` and resolve it, but a name matching more than one is refused with `InvalidParams` listing every match under `Candidates` — never silently resolved to one of them. Mutations take the full `SubjectKey` (`SourceGuid` + `SubjectName`) instead. The three places where the engine itself only accepts a name — a virtual Subject's member list, `StartLiveLinkRecording`'s targets, and `SetLiveLinkComponentSubject` — resolve against whichever Subject with that name is presently *enabled*, refuse an ambiguous one, and report back what they resolved to.

**Mutual exclusion.** The mutating commands below are refused while a preset apply or a recording is in flight (see [UAIP.Editor.LiveLink](#uaipeditorlivelink-)). `PushLiveLinkSyntheticFrame` is the deliberate exception and is never refused for that reason; reads never are either.

### Observation (5) — requires `RuntimeInspect`

| Command | Description |
|---|---|
| `ListLiveLinkSources` | Every Source registered with the client, real and virtual-subject container alike — `Guid`, human-readable `Type`, `IsStillValid`, `IsVirtual`, `FactoryClassPath`. `LiveLinkAvailable` reports whether a client implementation is registered at all, which is what makes this the one call to start from. ⚠️ `IncludeSensitiveDetails: true` adds `ConnectionString` / `StatusText` / `MachineName` — free-form fields a Source controls that can carry host addresses or credentials — and requires `LiveLinkSourceInspectSensitive`; every response echoes the name under `SensitiveDetailsRequiredCapability` whether or not it was asked for |
| `ListLiveLinkSubjects` | Every Subject the client knows about, filtered by `IncludeDisabled` / `IncludeVirtual`. Each entry carries `SubjectKey`, `RoleClassPath`, `EnabledConfigured` (the persistent configured flag) and `IsSubjectValid`. `State` is included only when `EnabledConfigured` is true, because the engine's own state query is keyed by name and answers for whichever same-named Subject is enabled — reporting it for a disabled row would describe a different Subject |
| `GetLiveLinkSubjectFrame` | Evaluate a Subject's current static and frame data for a role and return both as role-structured JSON (`SubjectKey`, `RoleClassPath`, `StaticData`, `FrameData`, `CapturedAt`). Narrow by `SourceGuid` to evaluate against that exact Source; omit it to evaluate by name, which answers for whichever same-named Subject is enabled. `Role` defaults to the Subject's own. Engine-shipped roles are decoded field by field; a project- or plugin-defined role falls back to the fields common to every role (curve values, times, timecode) — `ListLiveLinkRoles` says which is which |
| `GetLiveLinkSubjectStatus` | A Subject's connection status: `State` (only when the resolved Subject is the enabled one sharing its name, for the reason above), `IsSubjectTimeSynchronized`, `SceneTime` (the most recent frame's, when any frame has arrived), `FrameArrivalTimes` and `CapturedAt`. ⚠️ **No frame rate is computed.** `FrameArrivalTimes` is the raw arrival history exactly as the engine exposes it — the engine documents it as debugging-only and offers no frame-rate query — so any rate is yours to derive |
| `ListLiveLinkRoles` | Every registered `ULiveLinkRole` subclass — `RoleClassPath`, `DisplayName`, `StaticDataStructPath`, `FrameDataStructPath`, and `IsFullySupported` (whether frames of that role are decoded field by field or only through the common base fields). Also lists every **concrete** `ULiveLinkVirtualSubject` subclass under `VirtualSubjectClasses`; `AddLiveLinkVirtualSubject` requires one of these, since the abstract base cannot be instantiated |

### Client state (4)

| Command | Description |
|---|---|
| `SetLiveLinkSubjectEnabled` | Set a Subject's configured enabled flag, addressed by `SubjectKey`. **Only one Subject sharing a name may be enabled at a time**, so enabling one can implicitly disable another; that Subject's key comes back under `ImplicitlyDisabledSubjectKey` (`null` when none was affected). `EnabledConfigured` reflects the change immediately, while `EnabledThisFrame` — the snapshot the client evaluates against — only picks it up on the client's next tick, which is why the two are reported separately. Requires `LiveLinkClientControl` |
| `RemoveLiveLinkSource` | ⚠️ **Cannot be undone.** Remove a Source by `Guid`, taking every Subject it owns with it; a removed Source cannot be recreated under the same `Guid`. When the Source is one UAIP created, its ledger entry is dropped too (`WasSyntheticSource`). `NotFound` for a `SourceGuid` that names no registered Source. Requires `LiveLinkSourceDelete` — held apart from `LiveLinkClientControl` precisely because it is the one irreversible mutation in this group |
| `AddLiveLinkVirtualSubject` | Add a virtual Subject — a combination of one or more existing Subjects — to the shared UAIP virtual-subject container Source. `VirtualSubjectClass` must be a concrete `ULiveLinkVirtualSubject` subclass path (`ListLiveLinkRoles` lists them). Each `MemberSubjectNames` entry resolves against whichever same-named Subject is enabled, `NotFound` when none matches and `InvalidParams` listing candidates when more than one does; the resolved keys come back under `Members`. Up to 64 members, names up to 256 characters. **Virtual Subjects are real client configuration and survive the session that made them** — remove them explicitly. Requires `LiveLinkClientControl` |
| `RemoveLiveLinkVirtualSubject` | Remove a virtual Subject by `SubjectKey`. Idempotent: a key that names no virtual Subject succeeds with `WasPresent: false`. When the container Source is left holding none, the Source is removed too (`WasContainerSourceRemoved`) — **unless that would leave the client with no virtual Source at all**, which the editor's LiveLink panel assumes exists. `InvalidParams` when `SubjectKey` names a real Subject; use `RemoveLiveLinkSource` for those. Requires `LiveLinkClientControl` |

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
| `StartTrace` | Start recording into UAIP's own trace directory with the given channels or channel presets enabled, and return the file name being written to. `Channels` is required; `Label`, `MaxDurationSeconds` (default 300, range 1–3600) and `MaxFileSizeMB` (default 512, range 1–4096) are optional. A trace UAIP already started is never restarted — the request only adds channels and reports `AlreadyRunning` / `LimitsIgnored`. Rejected with `PolicyViolation` when the *effective* channel set (already enabled ∪ requested) records log text and `AllowLogDump` is false; no channel is ever turned off to make a request pass. When that same set carries something the policy will not let the raw file be handed over for, `Warnings` reports `AttachDisabledByPolicy` naming the channels and the setting, so a capture that is meant to be taken away is not started for nothing. Both limits are checked once per second, so the size limit is not a strict ceiling |
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

> Schemas and parameter details are intentionally omitted from this page. Use `uaip_describe_command(CommandName="...")` to get the full schema for any command.

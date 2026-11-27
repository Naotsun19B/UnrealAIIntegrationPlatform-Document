**[日本語](../ja/upcoming-2.0.md)** | [Back to README](../../README.md)

# Changes coming in 2.0.0

> **Status: advance notice.** Nothing on this page changes a call in 1.x.
> Last updated: 2026-11-27 (see "Update history" at the end)

## About this page

This page tells you, while you are on 1.x, what changes in 2.0.0 for the calls and settings you already use. Each item says what it is **Now** in 1.3.0, what it is in **2.0.0**, and what to do to **Migrate**.

- **This is not the complete list.** Some changes have no fixed version or shape yet, and they are added here as they are decided. The 2.0.0 changelog is the final list.
- If the 1.3.0 changelog and this page disagree, this page is newer.
- Changes already implemented for 2.0.0 also appear in the [`next` changelog](https://github.com/Naotsun19B/UnrealAIIntegrationPlatform-Document/blob/next/docs/en/changelog.md). That one shows the form as implemented; this page shows the form as planned.
- No 1.x minor release is planned. A new key, parameter, command or setting described here arrives in 2.0.0 unless the item says otherwise.
- **⚠️ Breaking** marks a change to a call that works in 1.3.0 (including the commands added in 1.3.0): whether it succeeds, its `ErrorCode`, or the keys it returns. It is also used for removing a command and for retiring a capability you may have granted. The 1.3.0 changelog marked its notices against 1.2.0, so the same item can carry a different mark there. An item without the mark can still need a rewrite, such as a rename, a deprecation or a removed switch. Each item's Migrate line says whether the old form keeps being accepted.
- The only commands removed in 2.0.0 are the `Experimental` `Toolset.*` commands. Before any other `Experimental` command is removed, it is listed here first (see the [Deprecation policy](changelog.md#deprecation-policy-rarely-removed)).
- When 2.0.0 is released, a separate migration guide is published and this page is kept as a record.

## Prepare now

Everything here already works in 1.3.0.

- Call the `UAIP.*` commands instead of the `Toolset.*` commands. They do not depend on the engine version.
- After a write to an asset that has a compile step, call the compile command (for example `CompileBlueprint`) yourself instead of relying on the write to compile. After a command that creates an asset, call `SaveAsset` yourself.
- When a refusal for an open modal dialog comes back, read `RejectReason: ModalActive`. Do not rely on `ErrorCode`, which changes.
- Read `IsMasked` and `MaskedFields` in the responses that already return them. Read `Result.Reason` in the responses that already return it. Responses that do not return them yet gain them in 2.0.0.
- Pass `SessionId` to `GET /uaip/artifacts/:id`, and read `ActiveAssetPath` instead of `ActiveTabId` in the artifact of `OpenAsset` and `NormalizeEditorLayout`. To try the 2.0.0 behavior, start the editor with `-uaip-require-artifact-session-id` and `-uaip-active-tab-id-as-layout-id`. Both switches are removed in 2.0.0.

## Toolset entry point

### ⚠️ Breaking: all `Toolset.*` commands are removed
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** The 421 `Toolset.*` commands call the tools of the official Toolsets. They are `Experimental` and work as documented.
- **2.0.0:** Every `Toolset.*` command is removed, with no alias. A call to one returns `CommandNotFound` with no hint. A table that maps each old command to its replacement is published in the documentation and the 2.0.0 changelog. Removing `Experimental` commands is an exception to the [Deprecation policy](changelog.md#deprecation-policy-rarely-removed). The entry point below is not available on UE 5.7, which has no Toolset registry.
- **Migrate:** Use the corresponding `UAIP.*` command where there is one. Otherwise move to the entry point below when you move to 2.0.0.

### A tool that is not in the definition table is refused by default
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** There is no generic entry point yet, so this applies only from 2.0.0.
- **2.0.0:** A tool that UAIP's definition table does not list returns `PolicyViolation` with `Reason: ToolNotInDefinitionTable`. You allow it in `[UAIP.SafetyPolicy]`, either one tool at a time or every tool not in the table. A tool of an external MCP server can only be allowed one tool at a time. The ini keys and the line format are not decided yet.
- **Migrate:** Decide which tools you call, and plan to list them in `[UAIP.SafetyPolicy]` once the keys are published.

### Toolset access is granted in three capabilities (added in 2.0.0)
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** The capabilities of the `UAIP.*` commands apply to the `Toolset.*` commands.
- **2.0.0:** `ToolsetRead` and `ToolsetEdit` are allowed by default, and `ToolsetExecute`, for tools that run code, is `DefaultDenied` and has to be granted. A tool that does what a `UAIP.*` command does needs the same capabilities as that command.
- **Migrate:** If you call tools that run code, grant `ToolsetExecute` when you move to 2.0.0.


### One generic entry point replaces them (added in 2.0.0)
- **Now:** A tool of an official Toolset is called as its own `Toolset.*` command.
- **2.0.0:** Three commands are added: `UAIP.Core.ListToolsetTools`, `UAIP.Core.DescribeToolsetTool` and `UAIP.Core.InvokeToolsetTool`. They take `Toolset`, `Tool` and `Arguments` (the upstream names, as they are), and the tool's result is in `Result.Result`. Because the call uses the upstream names, a tool that a later engine version renames changes in the call too.
- **Migrate:** Nothing to do before 2.0.0.

### You write `refPath` yourself
- **Now:** The bridges for Niagara, PCG, Control Rig and the Sequencer Control Rig wrap an object argument for you.
- **2.0.0:** The wrapping is gone. You write `{"refPath": ...}` in `Arguments` yourself.
- **Migrate:** Pass object arguments as `{"refPath": ...}` in your calls to the new entry point.

## Commands added in 1.3.0

### ⚠️ Breaking: the 125 commands added in 1.3.0 change their names, keys, error codes and response shapes
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** They work as the 1.3.0 documentation describes.
- **2.0.0:** They are aligned with the same shared rules as the older commands, together with the changes in the sections below. The change for each command is listed in the 2.0.0 changelog.
- **Migrate:** Treat their names, keys and response shapes as provisional. Do not build long-lived tooling on an exact response shape before you have read the 2.0.0 list.

### ⚠️ Breaking: `PasswordState` is replaced by `IsMasked` and `MaskedFields`
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** `DumpGameViewportWidgets` returns `Text.PasswordState` in its artifact, and a refusal of `TypeGameViewportText` returns `Data.PasswordState`.
- **2.0.0:** Both commands report a masked field with `IsMasked` and `MaskedFields`, and `PasswordState` is removed.
- **Migrate:** Read `IsMasked` and `MaskedFields` where a response already carries them.

### ⚠️ Breaking: an element's `UnavailableReason` becomes `Reason`
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** `DumpStateTreeInstanceData` returns `UnavailableReason` in each element of `Blocks[]`, and `GetInputState` and `GetActionDisplayNames` of CommonUI return it in each element of `Players[]`, holding a vocabulary of their own.
- **2.0.0:** Each element carries `Reason` instead.
- **Migrate:** Read `Reason` of the element when you move to 2.0.0.


### ⚠️ Breaking: `DumpGameViewportWidgetTexts` no longer returns a password field's text just because two permissions are on
- **Now:** With the capability `RuntimeWidgetPasswordTextRead` granted and `AllowRuntimePasswordFieldRead` turned on, the response carries the text of a password field.
- **2.0.0:** The command takes a new parameter, `false` by default, that has to be set to receive that text. A call that relied on the two permissions alone gets a masked value.
- **Migrate:** If you read password fields on purpose, pass the new parameter when you move to 2.0.0.

## Command names and parameter keys

### Command names and parameter keys follow shared rules, and the old names keep being accepted
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** Names differ between domains. For example, a limit on the number of results is `MaxEntries`, `Limit` or `MaxCount`, a paging start is `StartIndex`, and a main asset is given as `<Type>Path`.
- **2.0.0:** Each kind of target has one verb and the keys have shared names: `MaxResults`, `Offset` / `NextOffset`, `AssetPath`, and a boolean key without the `b` prefix. A call with an old command name gets a `DeprecationWarning`, and a call with an old parameter key gets `DeprecatedParams` in its successful response. When the old names stop being accepted is not decided yet; it is announced with the list of renames.
- **Migrate:** You do not have to change anything to keep calls working. To find the calls to update, watch for `DeprecationWarning` and `DeprecatedParams`. In 1.3.0, `RequestBehaviorTreeAutoArrange` is already deprecated in favor of `ArrangeBehaviorTreeGraph`.

### The graph parameter is `GraphName`, `GraphGuid` or `GraphPath`
- **Now:** The graph is given as `TargetGraph` (Animation Blueprint), `EntryName` (UAF), `SolveEventName` (Control Rig) or `GraphIndex` (Conversation).
- **2.0.0:** Each is replaced by one of `GraphName`, `GraphGuid` and `GraphPath` (`GraphPath` is added in 2.0.0). The current names are kept as aliases.
- **Migrate:** For example, use `GraphName`, which Blueprint commands already accept.

### The node parameter is `NodeId`
- **Now:** Nodes are given as `NodeGuid`, `NodeName`, `NodePath`, `OptionId` and similar keys, depending on the domain.
- **2.0.0:** The parameter is `NodeId`. The current names are kept as aliases. The keys in responses change too (see "Graph editing").
- **Migrate:** For example, where a response already carries `NodeId` (such as the Animation Blueprint read commands), read it.

### The ends of a link are `Output*` and `Input*`
- **Now:** The ends of a link are given as `Source*` and `Target*` (for example `SourceOutputIndex`, `TargetInputIndex`, `SourceNodeGuid`, `TargetNodeGuid`).
- **2.0.0:** They are `OutputNodeId` with the output pin's key and `InputNodeId` with the input pin's key. The current names are kept as aliases. For example, this affects the Blueprint, Animation Blueprint, Material and Conversation commands.
- **Migrate:** None needed to keep calls working.

### ⚠️ Breaking: the position of a node in Dataflow is `NodeX` and `NodeY`
- **Now:** The Dataflow command that adds a node takes the position as a nested `Position` with `X` and `Y`.
- **2.0.0:** The position is given as `NodeX` and `NodeY`, as for the other graph commands.
- **Migrate:** Whether the nested `Position` keeps being accepted is not decided; this item will say so when it is.

### Property keys become `PropertyPath`
- **Now:** The key is `PropertyName`, `SubPropertyName` or `VarName`, depending on the command. For example, the StateTree commands and `SetBlueprintVariableDefault` differ between reading and writing.
- **2.0.0:** The key is `PropertyPath`. The old keys are kept as aliases.
- **Migrate:** None needed to keep calls working.

### Element keys become `ElementKey`
- **Now:** The generic element commands take `ElementKeyJson`.
- **2.0.0:** The key is `ElementKey`. `ElementKeyJson` is kept as an alias.
- **Migrate:** None needed to keep calls working.

### Time and duration keys end in `Seconds`
- **Now:** A time is given as `TimeoutSec`, `WaitTimeoutSeconds` (`WaitForWidget`) or `MaxWaitSeconds` (`LoadPrimaryAsset`), and `WaitSeconds` takes `Seconds`.
- **2.0.0:** A timeout is `TimeoutSeconds` and a duration is `DurationSeconds`. The old keys are kept as aliases.
- **Migrate:** None needed to keep calls working.

### The id of a job in a parameter is `JobId`
- **Now:** A command takes the id of a job under a name of its own: `AuditId`, `BuildId`, `InteractionId`, `AnalysisId`, `HLODBuildJobId` or `BuildJobId`, `AttemptId`, `CaptureId` or `RecordingId`.
- **2.0.0:** The parameter is `JobId`. The old keys are kept as aliases. The keys in responses change too (see "Response shape and keys"). The Deprecated commands of one family (see "Waiting, jobs and scenarios") keep their 1.x keys.
- **Migrate:** None needed to keep calls working.

## Response shape and keys

### ⚠️ Breaking: response keys that do not follow the shared spelling are replaced
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** Spellings differ. A boolean key has a `b` prefix, and some concepts use several spellings. `ReloadPythonCommands` returns `refresh_count`, `new_count_skipped` and `removed_count_skipped`, and some Sequencer Animation Mixer responses use a lowercase `result`.
- **2.0.0:** Each key is replaced at once, with no period in which both spellings are returned. For example, `bIsWorldPartitionEnabled` becomes `IsWorldPartitionEnabled`. The list of replacements is released with 2.0.0.
- **Migrate:** Update code that reads these responses when you move to 2.0.0.

### ⚠️ Breaking: keys that hold a reason are replaced by `Reason`
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** A refusal gives its reason under keys such as `FailureReason`, `BlockedReason`, `RefusalReason`, `RejectReason`, `RejectionReason`, `PreconditionReason` or `Cause`, and a successful response gives it under keys such as `SkipReason` or `NotAddableReason`.
- **2.0.0:** These keys are removed, with no period in which both are returned. A refusal gives it in `Result.Reason`, and a successful response gives it in the `Reason` of the element it explains.
- **Migrate:** Read `Result.Reason` in the responses that already return it.

### ⚠️ Breaking: a write's success flag is replaced by what was observed
- **Now:** A successful write returns constant marks such as `Success: true`, `Removed`, `Updated`, `Deleted`, `Added`, `Compiled`, `Moved` and `Renamed`. For example, this includes `Removed` in the Behavior Tree, EQS and StateTree commands and `Updated` in the StateTree `Set*` commands.
- **2.0.0:** The response carries `Changed` and other values observed from what the write did.
- **Migrate:** Do not treat these marks as proof that something changed; read `Changed` once it is returned.

### ⚠️ Breaking: "no value" is no longer an empty string, `null` or `Unknown`
- **Now:** A response writes an empty string for "none" (for example `ActiveTabId` in the editor state) and `null` or `Unknown` for a value it cannot determine. For example, this includes the `Value: null` of the Chooser cell commands and the `Content: null` of Control Rig.
- **2.0.0:** The key is left out.
- **Migrate:** Treat a missing key as "none" or "unknown".

### ⚠️ Breaking: the `Warnings` of Insights change shape
- **Now:** The Insights commands, such as `StartTrace`, return `Warnings` as an array of `{Code, Message}`.
- **2.0.0:** The shape is replaced.
- **Migrate:** Read the shape in the 2.0.0 changelog when you move.

### ⚠️ Breaking: counts that say nothing are no longer returned
- **Now:** A response that was not cut off still returns `TotalCount`, `ReturnedCount` and a `NextOffset` of `null`, and a response with nothing failed returns an empty `Failed` or `FailedCount` (for example `SaveAsset`, `FixAssetRedirectors`). Many responses return `IsDegraded: false` and an empty `Limitations`.
- **2.0.0:** These keys are returned only when they carry information.
- **Migrate:** Treat a missing key as the empty or false value.

### ⚠️ Breaking: the meaning of two keys changes
- **Now:** The truncation mark is `true` when the list is exactly at the limit (`ListWidgetClasses` at 500 items) or on the last page when `Offset` is above 0 (`ListDataTableRows`). `SetSettingsValues` counts a key written with the same value in `ChangedCount`.
- **2.0.0:** The truncation mark is `false` on the last page, so `ListDataTableRows` no longer returns `true` there. The exact rule for a list that is exactly at the limit, and the exact rule for `ChangedCount`, will be added here when they are decided.
- **Migrate:** Do not rely on the old counts.

### ⚠️ Breaking: the id of a job in a response is `JobId`
- **Now:** A response gives the id as `AuditId`, `BuildId`, `InteractionId`, `AnalysisId`, `HLODBuildJobId` or `BuildJobId`, `AttemptId`, `CaptureId` or `RecordingId`.
- **2.0.0:** The key is `JobId`, with no period in which both are returned. The Deprecated commands of one family (see "Waiting, jobs and scenarios") keep their 1.x keys.
- **Migrate:** Read `JobId` when you move to 2.0.0.

### ⚠️ Breaking: elapsed time is `ElapsedSeconds`
- **Now:** Five keys: `elapsedSeconds`, `ElapsedMs`, `ElapsedSec`, `WaitedSeconds` and `ExecutionTimeSec`.
- **2.0.0:** One key, `ElapsedSeconds`. A value that is now in milliseconds (`ElapsedMs`) is converted to seconds.
- **Migrate:** Check the unit in code that reads `ElapsedMs`.

### ⚠️ Breaking: `SuggestedCommand` is the array `SuggestedCommands`
- **Now:** `SetAssetProperty` (in a refusal) and `GetAssetProperty` return `SuggestedCommand`.
- **2.0.0:** Both return `SuggestedCommands`, an array.
- **Migrate:** Read the first element of the array.

### ⚠️ Breaking: `Remedy` is removed from the `RestartEditor` refusal and omitted when empty
- **Now:** A refused `RestartEditor` returns `Remedy`. The hints of `CommandNotFound` and `ListIntegrations` (for an integration that needs no action) return an empty `Remedy`.
- **2.0.0:** The `RestartEditor` refusal no longer returns `Remedy`; the text stays in `ErrorMessage`. An empty `Remedy` is omitted. `GetRestartStatus` keeps its `Remedy`.
- **Migrate:** Read `ErrorMessage` for the refusal of `RestartEditor`.

### ⚠️ Breaking: the names in a capability refusal use `MissingCapabilities` and `DeniedCapabilities`
- **Now:** The Game Viewport commands return `MissingCapability` (singular), and the MVVM commands return `ExplicitlyDeniedCapabilities`. This is the case in three Game Viewport commands.
- **2.0.0:** They return `MissingCapabilities` and `DeniedCapabilities`.
- **Migrate:** Read the new keys when you move.

### ⚠️ Breaking: `DumpInputState` returns `RequiredCapabilities` with names only
- **Now:** `DumpInputState` returns `RequiresCapabilities`.
- **2.0.0:** It returns `RequiredCapabilities`, an array of capability names without edition marks.
- **Migrate:** Read `RequiredCapabilities` when you move.

### ⚠️ Breaking: `Available` becomes `IsAvailable` and is always returned
- **Now:** The rows of `ListCommands` and `DescribeCommand` return `Available`.
- **2.0.0:** They return `IsAvailable` in every row, whether the command is available or not.
- **Migrate:** Read `IsAvailable`.

### ⚠️ Breaking: the body of an artifact follows the shared key spelling
- **Now:** The body of an artifact has `b`-prefixed keys and some keys in camelCase (four places, such as `GetAllCachedItems`). A mark of change in a body is spelled differently from `Changed`, and a time is given under one of five names.
- **2.0.0:** The keys follow the same spelling as responses, a change is `Changed`, and each time has one name. For example, `PropertyMutationParams` returns `Changed`.
- **Migrate:** Update code that reads artifact bodies when you move to 2.0.0.

## ErrorCode and refusals

### ⚠️ Breaking: some existing commands return a different `ErrorCode`, and a few calls that succeed now are refused
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** The same kind of failure returns different `ErrorCode` values in different commands. For example, a missing target is `NotFound` in some commands and `ExecutionFailed` or `InvalidParams` in others.
- **2.0.0:** The same kind of failure returns the same `ErrorCode` everywhere. The commands that return a different one now change, and each change is listed with its commands in the 2.0.0 changelog.
- **Migrate:** If your scenarios or client code branch on `ErrorCode`, check them when you move to 2.0.0.

### ⚠️ Breaking: a read-only graph is refused instead of changed
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** `ConnectBlueprintPins`, `DisconnectBlueprintPins`, `SetPinDefaultValue` and `DeleteGraphNode` change a read-only graph and succeed with a warning.
- **2.0.0:** The four commands refuse by default with `NotAllowed`.
- **Migrate:** Do not rely on editing a read-only graph.

### ⚠️ Breaking: the refusal for an open modal dialog is `NotAllowed` with `Reason: ModalActive`
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** `ClickWidget`, `HoverWidget`, `PressKey`, `InputText`, `FillForm`, `SetCheckboxState` and `SetComboSelection` return `PolicyViolation`, with `RejectReason: ModalActive`. `RestartEditor` returns `PreconditionFailed`. `AcceptDialog` and `CancelDialog` return `ExecutionFailed` when there is no dialog to answer.
- **2.0.0:** The seven commands and `RestartEditor` return `NotAllowed` with `Result.Reason: ModalActive`, and `AcceptDialog` and `CancelDialog` return `NotFound`.
- **Migrate:** Read `RejectReason: ModalActive` now instead of the `ErrorCode`.

### ⚠️ Breaking: a command that stops at its own deadline returns `Timeout`
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** `WaitForShaderCompilation`, `RecompileGlobalShaders` and `CompileLiveCoding` succeed with `Status: "Timeout"` in their artifact. `WaitForCondition` and `RunFunctionalTest` return `ExecutionFailed` with `Data.TimedOut: true`. For example, `StartPIE`, `LoadMap`, `WaitForWidget`, `CompileNiagaraSystem` and `FillForm` also differ.
- **2.0.0:** They return `Timeout`. The keys `TimedOut`, `Aborted` and `NotExecuted` are replaced by `WorkAfterTimeout` (see "Waiting, jobs and scenarios").
- **Migrate:** Branch on `ErrorCode`, not on these keys, when you move.

### ⚠️ Breaking: the HTTP status of `Timeout` is 504
- **Now:** `Timeout` is HTTP 408, as `api.md` documents.
- **2.0.0:** `Timeout` is HTTP 504.
- **Migrate:** If your scripts read the HTTP status directly, accept 504.

### ⚠️ Breaking: a request refused during shutdown is `NotAllowed` with `Reason: EngineExitRequested`
- **Now:** A request that the queue does not accept while the engine is exiting returns `InternalError`.
- **2.0.0:** It returns `NotAllowed` with `Reason: EngineExitRequested`.
- **Migrate:** Treat it as a refusal, not an internal error.

### ⚠️ Breaking: `CapabilityNotAvailable` is HTTP 403
- **Now:** `CapabilityNotAvailable` is sent with HTTP 503, although `api.md` documents 403.
- **2.0.0:** It is sent with HTTP 403, as documented.
- **Migrate:** If your scripts read the HTTP status directly, accept 403.

### ⚠️ Breaking: a request refused by the origin restriction is `PolicyViolation`
- **Now:** An HTTP request refused because of where it comes from returns an `ErrorCode` of `Forbidden`, which is not in the table of `ErrorCode` values.
- **2.0.0:** It returns `PolicyViolation`.
- **Migrate:** Treat `Forbidden` as `PolicyViolation`.

### ⚠️ Breaking: a command still loading is `TooManyRequests` with `Reason: IntegrationLoading`
- **Now:** A command of an integration in the `Pending` or `Loading` state returns `CommandNotFound`.
- **2.0.0:** It returns `TooManyRequests` with `Reason: IntegrationLoading`.
- **Migrate:** Retry on `TooManyRequests` instead of treating the command as missing.

### ⚠️ Breaking: a busy job queue returns `TooManyRequests`
- **Now:** The three capture areas return `NotAllowed` when the queue is full, a restart attempt returns `Conflict`, and Automation succeeds and reports the error in its report.
- **2.0.0:** All return `TooManyRequests`.
- **Migrate:** Retry on `TooManyRequests`.

### ⚠️ Breaking: the Play-In-Editor check runs before argument validation
- **Now:** During a Play session, a write with an invalid argument returns the validation error.
- **2.0.0:** The Play session check runs first, so the same call returns the refusal for the Play session. For example, this affects the World Partition, MVVM, Level, Enhanced Input and Mass writes.
- **Migrate:** If you branch on the `ErrorCode` of a write during a Play session, check it.

### ⚠️ Breaking: an unavailable GameFeature operation in a commandlet is `AbilityUnavailable`
- **Now:** `CreateGameFeaturePlugin` and `DeleteGameFeaturePlugin` return `NotAllowed` in a commandlet.
- **2.0.0:** They return `AbilityUnavailable`.
- **Migrate:** Read `AbilityUnavailable`.

### ⚠️ Breaking: a limit outside the allowed range is refused
- **Now:** A command rounds a time limit into its range (for example `CompileNiagaraSystem`, the LiveLink discovery and the lower limit of `WaitForWidget`), or accepts a value that has no effect (the `TimeoutSec` of `RunEditorPythonScript`).
- **2.0.0:** A value outside the allowed range returns `InvalidParams`.
- **Migrate:** Send a value inside the range that `DescribeCommand` declares.

### ⚠️ Breaking: a field of an AnimNotify that cannot be edited is `PolicyViolation`
- **Now:** The generic property commands return `NotAllowed` for a field of an AnimNotify that cannot be edited.
- **2.0.0:** They return `PolicyViolation`.
- **Migrate:** Branch on `PolicyViolation`.

### ⚠️ Breaking: a value of the wrong type is `InvalidParams`
- **Now:** `SetPCGNodeProperty` and the StateTree `AddPropertyBinding` return `ExecutionFailed` for a value of the wrong type.
- **2.0.0:** They return `InvalidParams`.
- **Migrate:** Branch on `InvalidParams`.

### ⚠️ Breaking: a partly unavailable operation is `AbilityUnavailable`
- **Now:** An operation that the environment makes impossible returns another code. For example, `SetTransformGizmoSize` returns `InvalidParams` for `AxisSizeMultiplier`, the Niagara `DuplicateEmitter` returns `NotAllowed`, and `GetTransformGizmoSize` reports a reason in `AxisSizeMultiplierUnavailableReason`.
- **2.0.0:** These return `AbilityUnavailable`.
- **Migrate:** Branch on `AbilityUnavailable`.

## Identifiers and references

### ⚠️ Breaking: identifiers in a response take the same form and key name as in a parameter
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** `AssetPath` in a response can be an object path (for example in `ListSoundClasses`, `ListPrimaryAssets` and the DataLayer commands), a class is given by its short name, a reference is quoted export text, a GUID has hyphens, and a key that holds the same identifier as a parameter often has another name. `GetOpenAssets` and `GetSelectedAssets` give only an object path.
- **2.0.0:** `AssetPath` is the package path, a class is its full path, a reference is a plain object path, a GUID is 32 hexadecimal digits without hyphens, and a key that holds the same identifier as a parameter has the parameter's name. The replacement is made with no period in which both are returned.
- **Migrate:** Update code that parses identifiers in responses when you move to 2.0.0.

### ⚠️ Breaking: `TabId` means a Slate tab id only
- **Now:** `TabId` matches part of a tab id in `CaptureGraphViewportImage`, `DumpSelectionState`, `ListGraphNodes`, `DragGraphNode` and `ConnectGraphPins`, and is read as an asset path in `FrameGraphAll`, `FrameGraphSelection`, `SetGraphSelection` and `SetGraphZoom`.
- **2.0.0:** `TabId` is an exact Slate tab id. An asset is given as `AssetPath`. `DragGraphNode` and `ConnectGraphPins` keep their 1.x `TabId` (see "Graph editing").
- **Migrate:** Pass the exact tab id.

### ⚠️ Breaking: `ActorIdentifier` holds the object path of an actor
- **Now:** A Runtime response that returns an actor gives its path in `Path` or `SpawnedActorPath`.
- **2.0.0:** Every response that returns an actor carries the object path in `ActorIdentifier`, and those two keys are replaced. For example, `PlaceActorInLevel` and `GetActorTransform` carry it.
- **Migrate:** Read `ActorIdentifier`.

### ⚠️ Breaking: the Foliage read commands read the editor's world
- **Now:** `GetFoliageInstanceCount`, `GetFoliageInstances`, `GetFoliageTypeInfo` and `ListFoliageTypes` read the running world during a Play session.
- **2.0.0:** They read the editor's world.
- **Migrate:** Do not rely on these commands to read the Play session.

### ⚠️ Breaking: `ListPlayWorlds` uses the selector keys
- **Now:** `ListPlayWorlds` and the context of a response return `PIEInstance` and `NetMode`.
- **2.0.0:** They return `TargetPIEInstance` and `TargetNetRole`, the same keys that select a world.
- **Migrate:** Read the new keys.

### ⚠️ Breaking: a widget reference of the wrong type is `NotFound`
- **Now:** A widget reference of the wrong type returns `InvalidParams` with `TypeMismatch`.
- **2.0.0:** It returns `NotFound`.
- **Migrate:** Branch on `NotFound`.

### ⚠️ Breaking: a name that matches more than one target is refused
- **Now:** A name that matches several targets is used anyway: `FocusOnActors` and `SelectActors` act on all of them, and for Niagara, Sequencer Control Rig and `TabId`, the first match is used, even for a write. For example, the labels of `SelectMenuItem` and `FocusEditorTab` use the first match.
- **2.0.0:** The call returns `InvalidParams`, with the candidates.
- **Migrate:** Give a name or an id that matches one target.

## Secret values

### ⚠️ Breaking: three older secret-mask keys are removed
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** `SetSettingsValues` returns `MaskedReason` on the change entries, four StateTree commands (`GetStateTasks`, `GetStateEnterConditions`, `GetStateTreeGlobalTasks`, `GetStateTreeEvaluators`) return `MaskedDueToPolicy` (always `false`), and DataRegistry's `GetItems`, `GetAllCachedItems` and `AcquireItems` return `MaskedFieldCount`.
- **2.0.0:** The three keys are removed, with no period in which both are returned. The marks are `IsMasked`, `MaskedFields` and `UnverifiedMaskedFields`. The DataRegistry commands and the change entries of `SetSettingsValues` gain `IsMasked` and `MaskedFields`.
- **Migrate:** Read `IsMasked` and `MaskedFields` where they are returned now. Ignore `MaskedDueToPolicy`.

### ⚠️ Breaking: a value in a name-to-value map gets its own `IsMasked`
- **Now:** `DumpMassEntityConfig` returns `Properties` in `OwnTraits[]` as a map, and puts `IsMasked: true` and `MaskedFields` beside it when something is masked. `GetWidgetProperties` (`Properties`), `SetWidgetProperties` (`PreviousValues`) and `GetSlotProperties` return only `MaskedFields`.
- **2.0.0:** The map has a shape that lets each value carry `IsMasked`. The input of a write, `InitialProperties` and the `Properties` of `SetWidgetProperties`, takes the same shape, so what you read can be passed to a write.
- **Migrate:** Read `MaskedFields` in the UMG responses now.

## Edit transactions, compile and save

### ⚠️ Breaking: a write reports whether it was undone in one shared way
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** A write that fails after changing something reports it under different names: `GraphIntegrityState` (`ApplyBlueprintGraphEdit`), `TableIntegrityState` (Chooser), and `Status: RolledBack`, `RollbackFailed`, `RolledBackWithLeftovers`, `RemainingComponents` and `MissingAfterRollback` (`RemoveDynamicsChain`), `bFinalizeRolledBack` (Motion Matching), or only in the message. `RemoveDynamicsChain` answers `Success` when it put everything back.
- **2.0.0:** A failed write carries `Result.IntegrityState` (`Intact`, `RestoredByRollback` or `ChangesRemain`) and `Result.Remaining`. The other names are removed. `RemoveDynamicsChain` fails when it put everything back.
- **Migrate:** Read `Result.IntegrityState` once you move to 2.0.0, and do not treat `Status: RolledBack` as a success.

### ⚠️ Breaking: a write no longer compiles the asset
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** Many writes compile the asset they changed, by default (turned off with `SkipCompile` / `bSkipCompile`) or always. `ApplyBlueprintGraphEdit` and `SetPinDefaultValue` undo the write when the compile reports new errors. `CompileMaterial`, `CompileWidgetBlueprint`, `CompileMetaSound` and `CompileNiagaraSystem` report a failed compile in the artifact and still succeed, and `CompileControlRig` and `CompileSoundCue` always report success.
- **2.0.0:** A write only edits the asset, and every write to an asset that has a compile step carries `Result.RequiresFollowupCompile`. Only the compile commands compile. A compile command that finds errors returns `ExecutionFailed` with `Result.CompileErrors`. What happens to `SkipCompile` is announced with 2.0.0.
- **Migrate:** Call the compile command, such as `CompileBlueprint`, yourself after a write, and check its result.

### ⚠️ Breaking: a command that creates an asset no longer saves it
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** `CreateWidgetBlueprint`, `CreatePhysicsAsset`, the Groom import, binding and texture commands, and `CreateLegacyClothingAsset` (which also saves the Skeletal Mesh it changes) save what they create or change.
- **2.0.0:** Only a request that asks for a save saves. A created asset stays unsaved with its package marked as modified, and a response lists what was saved in `Result.SavedPackages` and the files it wrote in `Result.WrittenFiles`.
- **Migrate:** Call `SaveAsset` yourself after creating an asset.

## Graph editing

### ⚠️ Breaking: a graph parameter that is left out means the default graph of the asset
- **Now:** What a call without a graph parameter does differs by command. For example, some Blueprint commands look through every graph and others use the event graph, and `AddAnimGraphNode` of Animation Blueprint takes no graph parameter and always uses the first AnimGraph.
- **2.0.0:** In a domain with more than one graph, a command treats a missing graph parameter as the default graph of that domain, and its description says which graph that is. `AddAnimGraphNode` and the other commands without a graph parameter gain one (added in 2.0.0). The default graph of each domain is decided with the 2.0.0 list.
- **Migrate:** Give the graph explicitly (for example `GraphName`) on every call that accepts it.

### ⚠️ Breaking: responses name a node `NodeId`
- **Now:** A response gives a node under a key of its own, such as `NodeGuid`, `NodeName`, `NodePath`, `OptionId`, `TestId`, `StateId`, `TaskId`, `ModuleId`, `EmitterId` or `StateNodeId`. For example, this affects Dataflow, Conversation, `GetBehaviorTreeSubtree`, UAF, Control Rig, PCG, EQS, StateTree and Niagara. The Animation Blueprint read commands already return the same node as `NodeId`.
- **2.0.0:** The key is `NodeId`. A node that has a role in the response is `ParentNodeId`, `HostNodeId`, `OutputNodeId` or `InputNodeId`. The keys of parameters change too (see "Command names and parameter keys").
- **Migrate:** Read `NodeId` where a response already carries it.

### ⚠️ Breaking: a graph read returns its connections as `Links`
- **Now:** The list of connections has a name of its own: `Edges` (PCG, MetaSound), `Connections` (Dataflow, and inside the nodes of SoundCue) or `Transitions` (the state machines of Animation Blueprint). The ends are `From*` and `To*` (MetaSound), `FromStateId` and `ToStateId` (the state machines of Animation Blueprint), or `OutputPinIndex`, `InputNodeId` and `InputPinIndex` with no output node (SoundCue). Animation Blueprint gives only `LinkedTo` on each pin.
- **2.0.0:** A read that returns a whole graph with pins has `Nodes` and `Links`, and each link appears once. A link is written with the keys of the connect commands (`OutputNodeId`, `InputNodeId` and the pin keys), so what you read can be passed to a connect or disconnect call. `LinkedTo` on a pin uses the same keys.
- **Migrate:** Read `Links` when you move. PCG and Dataflow already use the connect commands' keys for the ends; only the name of the list changes.

### ⚠️ Breaking: the position and the class of a node in a read use shared keys
- **Now:** The position is a nested `Position` with `X` and `Y` in `GetDataflowGraphInfo`, `ListGraphNodes` and `DumpSelectionState`. MetaSound, UAF, Control Rig (`ListNodes`) and Conversation return no position. The class of a node has seven spellings: `NodeClass`, `ExpressionClass`, `SettingsClassPath`, `TypeName`, `ClassName`, `GeneratorClass` and `StructPath`.
- **2.0.0:** Each element of `Nodes` carries `NodeId`, the full path of the node's class and, in a graph that has coordinates, `NodeX` and `NodeY`. The nested `Position` and the seven class keys are replaced, and the position is added where it is missing. The name of the class key is listed with 2.0.0.
- **Migrate:** Read `NodeX` and `NodeY` when you move to 2.0.0.

### ⚠️ Breaking: a connection that would cut an existing link needs `AllowBreakOthers` (added in 2.0.0)
- **Now:** What happens when you connect to an input pin that already has a link depends on the domain. Dataflow, MetaSound and Conversation refuse such a connection, and other domains (for example Animation Blueprint, Material and SoundCue) leave the decision to the editor's schema, which can replace the old link.
- **2.0.0:** Such a connection is made only with `AllowBreakOthers: true`. Without it, the call returns `Conflict` and lists the links it would have cut in `Result.ExistingLinks`. A write that cut links (a replacement, a disconnect or a node deletion) lists them in `Result.RemovedLinks`.
- **Migrate:** To keep the old result, cut the existing link yourself with the disconnect command of the domain (for example `DisconnectBlueprintPins`) before you connect.

### ⚠️ Breaking: a connection that needs a type conversion needs `AllowConversion` (added in 2.0.0)
- **Now:** The single `ConnectBlueprintPins` accepts a type promotion while a batch in `ApplyBlueprintGraphEdit` refuses it. Animation Blueprint and Material refuse only what the schema calls impossible and leave the rest to the engine, and Conversation accepts a connection that needs a conversion node.
- **2.0.0:** A connection that needs a conversion is made only with `AllowConversion: true`. Without it, the call returns `InvalidParams` and the refusal names the conversion that is needed (the kind of node to insert, or the type to promote). A conversion that was made is reported in `Result`, with the `NodeId` of the inserted node and the pin whose type changed. `ApplyBlueprintGraphEdit` takes the parameter too.
- **Migrate:** Pass the type the pin expects, or insert the conversion node yourself.

### ⚠️ Breaking: `ApplyBlueprintGraphEdit` writes the ends of a connection like the single connect commands
- **Now:** Each end is a nested `From` or `To` object that holds a node (`NodeId` or `NodeRef`) and a pin (`PinName` or `PinId`).
- **2.0.0:** The ends use the same keys as the other connect commands: `OutputNodeId` and `InputNodeId` with the pin keys.
- **Migrate:** Nothing to do before 2.0.0. Whether the nested form keeps being accepted is not decided; this item will say so when it is.

### ⚠️ Breaking: connecting an existing link and cutting a link that does not exist succeed
- **Now:** Dataflow refuses to connect a link that already exists when the input pin has a link. `DisconnectBlueprintPins` returns `ExecutionFailed` for a link that does not exist, and Conversation returns `NotFound`.
- **2.0.0:** Both succeed with `Changed: false`. A disconnect whose node or pin does not exist is `NotFound`.
- **Migrate:** Do not branch on these failures.

### ⚠️ Breaking: the direction of a pin is no longer inferred
- **Now:** Animation Blueprint looks for an output pin of the given name first and takes an input pin if there is none, and the single Blueprint connect takes `Source*` and `Target*` and lets the schema work out which end is the output.
- **2.0.0:** The direction is given by the key (`Output*` or `Input*`) and is never inferred from the name. A call that relied on the guess no longer works.
- **Migrate:** Give each pin under the key of its direction.

### ⚠️ Breaking: deleting a node that cannot be deleted is `NotAllowed`
- **Now:** Deleting an entry, root or output node returns `Conflict` in Blueprint (`DeleteGraphNode`), Material, SoundCue and the batch edit, and `NotFound` for the root of a Behavior Tree. Some domains have no check.
- **2.0.0:** The call returns `NotAllowed`.
- **Migrate:** Branch on `NotAllowed`.

### ⚠️ Breaking: the links removed by a write are in `Result.RemovedLinks`
- **Now:** A deletion reports the links it broke under `BrokenConnections` (Blueprint), `RemovedEdges` (MetaSound and SoundCue) or `BrokenLinks` (the batch edit). Other domains report nothing.
- **2.0.0:** The three keys are replaced by `Result.RemovedLinks`, with the same elements as `Links`.
- **Migrate:** Read `Result.RemovedLinks` when you move.

### ⚠️ Breaking: a default value written to a connected input pin is `NotAllowed`
- **Now:** Blueprint returns `ExecutionFailed`, `SetAnimGraphNodeProperty` of Animation Blueprint skips the write without a message, and UAF, Control Rig, MetaSound and Niagara do not check.
- **2.0.0:** The call returns `NotAllowed`.
- **Migrate:** Branch on `NotAllowed`.

### ⚠️ Breaking: a pin is an object, not one string
- **Now:** `ListUAFPins` and the Control Rig `ListPins` return each pin as one string of the form `Name (Direction, CPPType)`. The `PinType` of Animation Blueprint holds only the category, and PCG returns its pins as an array of label strings with no type.
- **2.0.0:** A pin is an object with separate keys for its name, its identifier (an id, an index or a path, depending on the domain), its direction and its type. The one-string form is removed, and the pins of Animation Blueprint and PCG gain the missing keys (added in 2.0.0).
- **Migrate:** Do not build code on parsing that string.

### ⚠️ Breaking: a read of a tree gives `ParentNodeId` and `ChildIndex` on every node
- **Now:** `GetBehaviorTreeNodeList` returns `ParentNodeGuid` and `Depth`, with no order among siblings. `GetBehaviorTreeSubtree`, EQS and Niagara return only a nested form, and StateTree returns `ParentStateId` and a nested form whose order is the position in the array.
- **2.0.0:** A read of a tree returns a flat list in which each node carries `ParentNodeId` (null for the root) and `ChildIndex`, its order among its siblings. A read that returns a nested form carries the same two keys on each node. The parent keys of today are replaced.
- **Migrate:** Read `ParentNodeId` when you move.

### ⚠️ Breaking: the graph commands of the generic UI take the `NodeId` of the domain
- **Now:** `SetGraphSelection` and the other generic graph commands use the `NodeGuid` of the editor graph. For Material (the GUID of the expression) and Dataflow (the domain's GUID) this is a different value from the domain's own id, and `SetGraphSelection` ignores an id that matches nothing without saying so. UAF, Control Rig and PCG identify nodes by name, so their nodes cannot be passed at all.
- **2.0.0:** These commands take and return the `NodeId` of the domain.
- **Migrate:** Pass the `NodeId` that the read command of the domain returns when you move to 2.0.0.

### `AddState` adds at the end when `AfterStateId` is left out
- **Now:** `AddState` of StateTree adds the state first when `AfterStateId` is left out.
- **2.0.0:** It adds the state last among its siblings. The call still succeeds and the keys do not change; only the resulting order does.
- **Migrate:** Pass `AfterStateId` to keep the position you want.

### `DragGraphNode` and `ConnectGraphPins` are Deprecated
- **Now:** `DragGraphNode` moves a graph node by a pixel offset and `ConnectGraphPins` connects two pins on a graph editor tab.
- **2.0.0:** Deprecated in 2.0.0; the name keeps being accepted. Use the move and connect commands of each domain instead. Their parameters and response stay as they are in 1.x; the shared graph keys on this page (such as `NodeId`, `Output*` and `Input*`) and the new meaning of `TabId` do not apply to them. They become Deprecated in the release in which every domain has its own move and connect commands; until then they are not marked Deprecated. Once they are, the `DeprecationWarning` of a successful call names the command to use for each domain, and there is no single `MigrationTarget`.
- **Migrate:** Calls written for 1.x keep working. Connect with the command of the domain (for example `ConnectBlueprintPins`). Move a node with `SetNodePosition` for Control Rig or `RepositionPCGNode` for PCG; the commands that move a node in the other domains are added in 2.0.0.

## Property read and write

### ⚠️ Breaking: a read returns `Value` as a JSON value
- **Now:** `GetActorProperty`, `GetWorldSetting`, `GetAssetProperty`, `GetBlueprintDefault`, `GetProjectSetting` and `GetDataTableRow` return `Value` as a string: the engine's text, or JSON inside a string. A value that has a reference inside falls back to text. The property reads of the domains have forms of their own.
- **2.0.0:** `Value` is the JSON value itself, in the shape given for its type below. JSON inside a string and the engine's text are no longer used.
- **Migrate:** If your code parses `Value` as text, plan to read JSON when you move.

### ⚠️ Breaking: a write takes `Value` as JSON, and engine text is refused
- **Now:** `SetActorProperty`, `SetWorldSetting`, `SetAssetProperty`, `SetBlueprintDefault`, `SetProjectSetting` and `SetDataTableRow` take the value as engine text in `Value` or as JSON in `ValueJson`, and the type decides which one is accepted. The property commands of the domains take the value in nine different ways, for example as a text `PropertyValue`, a JSON `PropertyValue`, `Value` or `DefaultValue`.
- **2.0.0:** The value is one JSON value in `Value`. A write with engine text such as `(X=1,Y=2)` where a struct is expected, or with a JSON value of the wrong type, returns `InvalidParams`; nothing is converted (a string given for a number is not read as a number).
- **Migrate:** Write references, structs and containers in `ValueJson` where the command takes it (fifteen commands; the Subsonic commands already take a JSON `Value`). Whether `ValueJson` keeps being accepted in 2.0.0 is not decided; this item will say so when it is.

### ⚠️ Breaking: a type has one form for reading and writing
- **Now:** A read and a write of the same type differ. A map is read as `{"A":1}` and written as `[{Key,Value}]`; a `TOptional` and a delegate are read as text; a Boolean is read as `"True"` and a float as `"9.5"`; an enum value that is not declared is read as `"(INVALID)"`, and bit flags as one string joined with `|`; an `FGuid`, an `FGameplayTag` and the 17 struct types of the catalog are text only; writing an `FText` back drops its key; and the path of an Instanced object that you read makes a copy when you write it back. `FDateTime` and `FInstancedStruct` can be read but not written.
- **2.0.0:** One table of forms applies to reads and writes. A Boolean is a JSON Boolean, an integer or a float is a JSON number (a 64-bit integer beyond 2^53 is a decimal string), an enum is its short name, a struct is an object of its members (a write may give only some of them and the others keep their value), a container is an array and a write replaces the whole value, a map is `[{"Key": …, "Value": …}]`, a `TOptional` is `{"IsSet": …, "Value": …}`, a delegate is `{"ObjectPath": …, "FunctionName": …}`, an `FInstancedStruct` is `{"StructType": …, "Value": {…}}`, an `FText` is a string or `{"Namespace", "Key", "SourceString"}`, an `FGuid` is 32 digits, an `FGameplayTag` is its name, an `FDateTime` is an ISO 8601 string, and a reference is a plain object path (see "Identifiers and references"). A value you read can be written back to the same path and succeeds with `Changed: false`. `FDateTime` and `FInstancedStruct` become writable (added in 2.0.0).
- **Migrate:** Update code that builds or parses property values when you move to 2.0.0.

### ⚠️ Breaking: an empty reference is `null`
- **Now:** A read returns `"None"` for an empty reference, and a write accepts `null`, `""` and `"None"`.
- **2.0.0:** A read returns `null`. A write of `""` or `"None"` to a type that can be empty returns `InvalidParams` and points to `null`.
- **Migrate:** Clear a reference with `ValueJson: null` now.

### ⚠️ Breaking: `WriteInputForm` is removed
- **Now:** The write requirements of the generic commands report `WriteInputForm` (`TextOrJson`, `JsonOnly` or `None`), which says which field the value has to be given in.
- **2.0.0:** The key is removed, because the value is always JSON.
- **Migrate:** Do not branch on it.

### ⚠️ Breaking: several properties are written as an array
- **Now:** The argument of a call that writes several properties is an object keyed by name. Its own key is `Properties` in four commands, `Params` in four, `Parameters` in two and `InitialProperties` in one, and the responses have eight shapes. For example, this affects `SetWidgetProperties` and `SetSlotProperties`.
- **2.0.0:** The argument is `Properties`, an array of `{PropertyPath, Value, Operation?, ElementIndex?, ElementKey?}`, and a response lists `Properties` in the same order as the argument.
- **Migrate:** Update the calls when you move to 2.0.0.

### ⚠️ Breaking: a name that is not known refuses the whole batch
- **Now:** `SetSlotProperties` skips an unknown name without saying so, Niagara's `SetRendererData` only logs it, `SetSettingsValues` lists it in `SkippedKeys`, `SetMultipleWorldConditionProperties` lists it in `SkippedEdits`, and PCG puts it in a text under `Warnings`.
- **2.0.0:** If any element is refused, nothing is written. `Result.Refused` lists every refused element as `{PropertyPath, ErrorCode, Reason}`, and the response's `ErrorCode` is that of the first refused element in the order of the argument. A successful write lists `Changed`, `PreviousValue` and `NewValue` for each element.
- **Migrate:** Do not send a name that does not exist, and stop reading `SkippedKeys` and `SkippedEdits`.

### ⚠️ Breaking: the values in a Runtime dump have the same forms, and a cut value is marked
- **Now:** The Runtime dumps have forms of their own. For example, an empty reference is `"None"`; a container is `{Value, TotalCount, Truncated}` with the first 32 elements; a map is a list of `[key, value]`; a string is cut at 1024 characters without a mark; and the SaveGame export and the Chooser cell commands (`ListChooserTableRows`, `GetChooserTableRow`, `SetChooserTableCell`) use the `FJsonObjectConverter` form, with keys that start in lower case and `_structType`.
- **2.0.0:** The values follow the table of forms above. A list read may cut a value by depth, count or length, and a cut value carries the truncation mark instead of being cut silently.
- **Migrate:** Update code that reads these dumps when you move to 2.0.0.

### ⚠️ Breaking: `AssertActorProperty`, `AssertWorldState` and `WaitForCondition` take a property path and a typed value
- **Now:** The commands take `PropertyName` and `ExpectedValue`, and compare the value as text.
- **2.0.0:** The property is a `PropertyPath` and the value is a typed JSON value.
- **Migrate:** Update the calls when you move to 2.0.0. The rename of `PropertyName` is listed under "Command names and parameter keys".

### ⚠️ Breaking: the keys and the path of a binding are shared
- **Now:** The families spell a binding in their own way: StateTree uses `SourceNodeId` with `SourceProperty` and `TargetNodeId` with `TargetProperty` (one level), UMG uses `WidgetName` with `PropertyPath`, MVVM uses `Source` and `Destination` objects, Subsonic uses `ParameterName` or `EventTag` with `Index` and `PropertyName`, and Chooser uses `InputValue` with `Binding`, `ContextIndex` and `PropertyBindingChain`. None of them shares the path parsing or accepts an index.
- **2.0.0:** The source and the target property are `SourcePropertyPath` and `TargetPropertyPath`, with the same path grammar as property paths. A family that has only a target property uses `PropertyPath`. The other keys of a source or a target carry the prefix `Source` or `Target` (not `Destination`).
- **Migrate:** Update the calls when you move to 2.0.0.

### ⚠️ Breaking: adding and removing a binding mean the same in every family
- **Now:** Adding a binding to a target that already has one replaces it without saying so in StateTree, UMG, Subsonic and Chooser, and MVVM accepts a duplicate. Removing a binding that does not exist returns `Removed: true` in StateTree, `ExecutionFailed` in UMG, and `NotFound` in MVVM and Subsonic.
- **2.0.0:** In a family where a target holds one binding, adding to a target that already has one returns `Conflict` and lists the existing binding in `Result.ExistingBindings`, unless `AllowReplace: true` is given. Adding a binding that already exists, and removing one that does not exist, succeed with `Changed: false`. `NotFound` is returned only when the node, widget or view model that would hold the binding does not exist. A write that replaced or removed bindings lists them in `Result.RemovedBindings`.
- **Migrate:** Pass `AllowReplace: true` where you replace on purpose, and do not branch on the failure for a binding that does not exist.

### ⚠️ Breaking: an `FInstancedStruct` cell is `{"StructType": …, "Value": …}`
- **Now:** A Chooser cell that holds an `FInstancedStruct` is an object `{"_structType": "<struct path>", <fields>...}`.
- **2.0.0:** It is `{"StructType": "<struct path>", "Value": {…}}`, the form of the table above.
- **Migrate:** Update code that reads or writes these cells when you move. Whether the `_structType` form keeps being accepted is not decided; this item will say so when it is.

## Waiting, jobs and scenarios

### ⚠️ Breaking: `TimedOut`, `Aborted` and `NotExecuted` are replaced by `WorkAfterTimeout`
- **Now:** A command that stops at its deadline says so under keys of its own. `WaitForCondition` and `RunFunctionalTest` return `Data.TimedOut: true` (added in 1.3.0), `RunEditorPythonScript` returns `Data.Aborted: true` when it aborts, and a command whose wait in the queue ran out returns `NotExecuted: true`. Some commands say it only in the message, for example `AcquireItems` and `WaitForPendingInteraction`.
- **2.0.0:** The three keys are removed. A deadline is read from `ErrorCode: Timeout` and `Result.WorkAfterTimeout`, which is `NotStarted` (nothing was started), `Stopped` (the work was stopped, or the command only waited) or `StillRunning` (the editor goes on). When it is `StillRunning` and a command can check the result later, `Result.SuggestedCommands` names it. Values observed before the deadline may be in `Result`.
- **Migrate:** Branch on `ErrorCode`, then read `WorkAfterTimeout`. See also "ErrorCode and refusals".

### ⚠️ Breaking: a wait for a response that runs out is reported in the same form on every route
- **Now:** The form depends on the route. HTTP returns 408 with `ErrorCode: ExecutionFailed`, MCP returns an HTTP 200 with a JSON-RPC error -32000 (the number of "rate limit exceeded"), and WebSocket sends `{"event":"CommandTimeout","requestId": …}` and drops the completion that arrives later.
- **2.0.0:** Every route returns the command envelope with `Timeout` and `WorkAfterTimeout: StillRunning`. The command goes on running in the editor.
- **Migrate:** If you handle the -32000 error or the `CommandTimeout` event, read the envelope instead. The HTTP status of `Timeout` is in "ErrorCode and refusals".

### The id of a job is a GUID
- **Now:** LiveLink gives the `RecordingId` of a recording as a sequence number, and the ids of audit, PoseSearch, validation and interaction jobs have hyphens.
- **2.0.0:** A job id is a GUID of 32 hexadecimal digits without hyphens, the same form as other identifiers (see "Identifiers and references"). The Deprecated commands of one family (see below) accept an id in this form in their 1.x parameters.
- **Migrate:** Treat a job id as an opaque string.

### ⚠️ Breaking: the state of a job is one of five values
- **Now:** Each family has its own states. For example, audit has `Preparing`, PoseSearch has `Succeeded`, validation has `Preparing`, `Enumerating`, `Normalizing`, `Validating`, `Finalizing` and `Aborted`, an interaction has `AwaitingUser` and `Cause`, trace analysis has `Extracting`, HLOD reports `BuildStatus`, a restart has `Scheduled`, `CloseRetrying`, `Declined` and `ExitStarted`, a capture has `Recording` and `Stopped`, and LiveLink reports `IsRecording`.
- **2.0.0:** `State` is `Pending`, `Running`, `Completed`, `Failed` or `Cancelled`; the last three are final. A stage of a family goes in `Phase`, and `Failed` and `Cancelled` carry `Reason`. A receipt and a status response always carry `JobId`, `JobKind` (the name of the family), `State` and `StopRequired`. The Deprecated commands of one family (see below) keep their 1.x states.
- **Migrate:** Update code that reads a job's state when you move to 2.0.0.

### The commands that ask about, cancel or wait for the jobs of one family are Deprecated
- **Now:** Each family has its own commands to ask about a job, to cancel it and, for an interaction, to wait for it: `GetAssetAuditStatus`, `GetPoseSearchDatabaseIndexBuildStatus`, `GetValidationJobStatus`, `CancelValidationJob`, `GetPendingInteractionStatus`, `CancelPendingInteraction`, `WaitForPendingInteraction`, `GetTraceAnalysisStatus`, `GetHLODBuildStatus`, `CancelHLODBuild`, `GetRestartStatus` and `CancelLiveLinkRecording`. There is no command that lists the jobs of every family. Some of these commands also return the result of the job (PoseSearch, an interaction and a restart) or how far it has got (audit, validation and trace analysis).
- **2.0.0:** Deprecated in 2.0.0; the name keeps being accepted. Use `UAIP.Core.GetJobStatus`, `UAIP.Core.CancelJob`, `UAIP.Core.ListJobs` and `UAIP.Core.WaitForJob` (added in 2.0.0) instead. Their parameters and response stay as they are in 1.x; the shared job keys and states on this page do not apply to them, but their id parameters also accept the `JobId` that a 2.0.0 start command returns. They become Deprecated in the release in which the shared commands and, for PoseSearch, an interaction and a restart, a command that returns the result of the family (added in 2.0.0; its name will be added here) exist; until then they are not marked Deprecated. The `MigrationTarget` is `UAIP.Core.GetJobStatus`, `UAIP.Core.CancelJob` or `UAIP.Core.WaitForJob`, and for the three families whose status command returned the result, the `DeprecationWarning` also names the command that returns it. `UAIP.Core.WaitForJob` takes `JobId` and `TimeoutSeconds`, waits until the job has ended and returns the same response as `UAIP.Core.GetJobStatus`; when it runs out it returns `Timeout` with `WorkAfterTimeout: StillRunning` and does not cancel the job. The shared status response carries `ProcessedCount` and `TotalCount` only for a family that counts its work. `GetLiveLinkRecordingStatus` is not Deprecated: it also reports a recording that was not started through UAIP.
- **Migrate:** Calls written for 1.x keep working. When you move, ask about, cancel and wait for a job with the shared commands, and read the result with the command of the family.

### ⚠️ Breaking: a job that replaces another reports `ReplacedJobId`
- **Now:** `StartValidationJob` returns `ReplacedPreviousJob: true` when it replaces a job, and the replaced job ends as `Aborted`.
- **2.0.0:** The receipt carries `ReplacedJobId`, and the replaced job is `Cancelled` with `Reason: Replaced`.
- **Migrate:** Read `ReplacedJobId` when you move.

### ⚠️ Breaking: cancelling or stopping a job that has ended succeeds
- **Now:** For example, `CancelHLODBuild` returns `ExecutionFailed` and the LiveLink recording commands return `NotAllowed` for a job that has ended.
- **2.0.0:** `UAIP.Core.CancelJob` (added in 2.0.0) and the stop commands of a family succeed and return the actual `State`. A cancel that was accepted while the work has not stopped yet succeeds and returns `Running`. `CancelHLODBuild` and `CancelLiveLinkRecording` are Deprecated and keep their 1.x behavior (see the item above).
- **Migrate:** Do not branch on these failures.

### ⚠️ Breaking: a step reference in a scenario follows the keys of the step's result
- **Now:** A step is referred to as `${StepName.Data.<pointer>}` or `${StepName.Data}`.
- **2.0.0:** A reference is `${<StepName>.<path>}`, and the path follows the keys of the step's result (for example `Success`, `ErrorCode` and `Result.<…>`). `${Variables.<key>}` stays. A reference that cannot be resolved fails the step with `InvalidParams` and is not retried.
- **Migrate:** Whether `${StepName.Data…}` keeps being accepted is not decided; this item will say so when it is.

### ⚠️ Breaking: a scenario returns the same envelope as a single command
- **Now:** The response has `Status` (`Completed`, `Failed` or `TimedOut`) and `AllStepsSucceeded`, and a failure of the whole scenario shows as a step named `__error__` or `__session_ended__`.
- **2.0.0:** The response has the top-level `Success`, `ErrorCode` and `Result.StepResults`, in the order the steps were tried. `Status` and `AllStepsSucceeded` are removed, and so are the steps `__error__` and `__session_ended__`. `Success` is true only when every step succeeded. `Result.TotalStepCount` gives the number of steps requested, and `Result.StoppedAtStep` the step it stopped at. The `ErrorCode` is `ExecutionFailed` with `Reason: StepFailed`, `Timeout` with `Reason: StepTimeout` or `ScenarioTimeout`, `InvalidParams` for a request that is not valid, `TooManyRequests` when another run holds the slot, `PolicyViolation` when the entrance is not enabled, or `NotAllowed` with `Reason: SessionEnded`. Each step's result also carries `AttemptCount`, `ElapsedSeconds` and `Result`.
- **Migrate:** Read `Success` and `ErrorCode` instead of `Status` and `AllStepsSucceeded` when you move.

### ⚠️ Breaking: a scenario returns its artifacts as `Artifacts`, not `ArtifactIds`
- **Now:** Each step's result and the top level carry `ArtifactIds`, an array of artifact id strings.
- **2.0.0:** They carry `Artifacts`, with the same elements as the `Artifacts` of a single command (`ArtifactId`, `FilePath`, `Type` and `SizeBytes`), and `ArtifactIds` is removed, with no period in which both are returned. A step reference `${<StepName>.Artifacts[<n>]}` keeps its form.
- **Migrate:** Read `ArtifactId` from the elements of `Artifacts` when you move to 2.0.0.

### A scenario that is refused is reported in the same form at every entrance
- **Now:** A request that is not valid returns a JSON-RPC error -32602 through MCP, without an `ErrorCode`, and a request that is refused when it is submitted returns HTTP 200 over HTTP. How the session id is read also differs by entrance.
- **2.0.0:** Every entrance (HTTP, MCP, WebSocket and the command line) takes the same request and returns the envelope of the previous item, with `InvalidParams` for a request that is not valid. How the HTTP status and the other details are decided will be added here when they are decided.
- **Migrate:** Read `ErrorCode` from the envelope rather than from the form of the transport.

## Capabilities and ini settings

### ⚠️ Breaking: `ToolsetEditDuringPlaySession` is removed and one `[UAIP.SafetyPolicy]` setting replaces it
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** The capability `ToolsetEditDuringPlaySession` lets the `Toolset.*` commands change the editor during a Play or Simulate session. Without it they are refused.
- **2.0.0:** A setting is added to `[UAIP.SafetyPolicy]`. When it is turned on, both the `UAIP.*` commands and the tools of the official Toolsets can change the editor during a Play or Simulate session; commands that would break during a session stay refused. The setting is added and `ToolsetEditDuringPlaySession` is removed in 2.0.0, with no period in which both exist. The key and the line format are not decided yet.
- **Migrate:** If your configuration grants `ToolsetEditDuringPlaySession`, replace it with the new setting when you move to 2.0.0. If you do not, changes during a Play session are refused.

### Capability names follow one pattern
- **Now:** The names follow no single pattern. Some Runtime capabilities do not say `Runtime`, some names are only a noun, and the wording and the singular or plural vary.
- **2.0.0:** The names follow `<Domain><Object><Verb>`, and the capabilities of the Runtime domain say `Runtime`. A capability that is renamed is still accepted under its old name, with a warning at startup, and responses, refusals and lists show only the new names. Which capabilities are renamed is decided one by one and listed in the 2.0.0 changelog.
- **Migrate:** None needed to keep an ini file working. Do not compare the names you read from a response with names written into your code before you have read the 2.0.0 list.

### Some limits move between flags and capabilities
- **Now:** Some limits are opened by a flag in `[UAIP.SafetyPolicy]`, and some by a capability.
- **2.0.0:** A limit that depends on who is calling becomes a `DefaultDenied` capability, and a limit that depends on the mode of the environment stays a flag that opens it. Which limits move, and how, will be added here when it is decided; the list is in the 2.0.0 changelog.
- **Migrate:** Nothing to do before 2.0.0.

### ⚠️ Breaking: `QueryCapabilities` reports `NotInThisEdition` as `UnavailableDetail`
- **Now:** With `IncludeUnavailable: true`, the elements of `RegisteredCapabilities` for a capability that the edition does not ship carry `UnavailableReason: "NotInThisEdition"`.
- **2.0.0:** They carry `UnavailableDetail: "NotInThisEdition"` instead, with no period in which both are returned.
- **Migrate:** Read `UnavailableDetail` when you move.

## Artifacts

### ⚠️ Breaking: `GET /uaip/artifacts/:id` without `SessionId` is refused
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** A request without `SessionId` is still answered, with a `Deprecation` header.
- **2.0.0:** A request without `SessionId` is refused with HTTP 400 and `ErrorCode: InvalidParams`, not 404.
- **Migrate:** Pass `SessionId` to the command that makes an artifact and to the fetch. The MCP Bridge sends it whenever it holds a session. To try 2.0.0, start the editor with `-uaip-require-artifact-session-id`.

### ⚠️ Breaking: `ActiveTabId` in the artifact of `OpenAsset` and `NormalizeEditorLayout` is a layout identifier
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** `ActiveTabId` holds the asset path, with `ActiveAssetPath` and `DeprecatedFields` beside it.
- **2.0.0:** `ActiveTabId` holds the Slate layout identifier of the focused tab, as in `DumpEditorState`, and `DeprecatedFields` is empty. `ActiveAssetPath` stays.
- **Migrate:** Read `ActiveAssetPath` instead of `ActiveTabId`. To try 2.0.0, start the editor with `-uaip-active-tab-id-as-layout-id`.

### The two trial switches are removed
- Announced in [1.3.0](changelog.md#uaip-plugin-130--2026-11-26).
- **Now:** `-uaip-require-artifact-session-id` and `-uaip-active-tab-id-as-layout-id` are command-line switches that take no value and have no ini setting. They are provided for the 1.x releases only.
- **2.0.0:** Both are removed. The behaviors of the two items above are the only behaviors.
- **Migrate:** Remove them from your launch command lines when you move to 2.0.0.

### ⚠️ Breaking: `Type` of an artifact is `Image`, `Json`, `Text` or `Binary`
- **Now:** `Type` is `Image`, `Json`, `Log`, `Report`, `Bundle` or `Trace`, and the folder of an artifact is named after its use, for example `Dumps`, `Screenshots`, `Logs`, `Reports` and `Traces`.
- **2.0.0:** `Type` says how the content is read, and the folder has the same name as `Type`. Logs are `Text`, reports and the manifest of a bundle are `Json`, a trace is `Binary`, and a CSV is `Text` with the Content-Type `text/csv`. The Content-Type of a fetch is decided from the extension. For example, this affects `ExportDataTableToCSV`, `ImportDataTableFromCSV`, `RunAutomationTest`, `RunGauntletTest` and `AnalyzeTrace`.
- **Migrate:** Do not branch on `Log`, `Report`, `Bundle` or `Trace`; read the extension or the content.

### The file name of an artifact is `<CommandName>-<ArtifactId>.<extension>`
- **Now:** The name is not built in one way, and in some artifacts the command's name is not the registered name.
- **2.0.0:** The name is the registered name of the command that asked for the save, `ArtifactId` and the extension. `FilePath` is still not a path to access the artifact.
- **Migrate:** Fetch an artifact by `ArtifactId`, not by its file name.

### ⚠️ Breaking: the manifest of a bundle is `Json` and the members carry `Role`
- **Now:** A command that returns a bundle returns a manifest that is not typed `Json`. For example: `CheckpointCapture`, `LoadMap`, `StartPIE`, and the DataTable, Enhanced Input and Execution commands.
- **2.0.0:** The manifest is the last element of `Artifacts[]` with `Type: Json`. Each artifact that belongs to a bundle carries `Role` in its element of `Artifacts[]`: `Pre`, `Post`, `Report`, `Log`, `Audit`, `Result`, `Snapshot`, `Payload`, or `Manifest` for the manifest itself (`Role` is added in 2.0.0).
- **Migrate:** Find the manifest by `Role: Manifest` once it is returned.

### ⚠️ Breaking: the artifact list of HTTP uses PascalCase keys
- **Now:** The list that `GET /uaip/sessions/{sessionId}/artifacts` returns uses `artifacts`, `artifactId`, `type`, `commandName`, `sessionId` and `description`, and `GetArtifact` returns the size as `TotalBytes`. The list has no size and no creation time.
- **2.0.0:** The keys are `Artifacts`, `ArtifactId`, `Type`, `CommandName`, `SessionId` and `Description`, and the size is `SizeBytes` on every route. The creation time `CreatedAt` is added.
- **Migrate:** Update the code that reads the list when you move.

### Keys that point to an artifact by path become `ArtifactId`
- **Now:** The keys have six spellings. For example: `ArtifactPath` (`ExportDataTableToCSV`), `PreDeleteArtifactPath`, `PreImportSnapshotPath`, `CaptureArtifactPath` and `WorldStateArtifactPath`.
- **2.0.0:** An artifact is pointed to by `ArtifactId` (or `<What>ArtifactId` when one response holds several), never by a path or a file name, and a command that takes an earlier artifact takes its `ArtifactId`.
- **Migrate:** Read the new keys when you move.

### ⚠️ Breaking: `SchemaVersion` is removed from artifact bodies
- **Now:** Many artifact bodies carry `SchemaVersion`, as 1, 2 or 3, as the string `"1.0"` or as the number `1.0`. For example: `GetAvailableRigVMUnitStructs`.
- **2.0.0:** The key is removed.
- **Migrate:** Do not branch on the value of `SchemaVersion`.

### ⚠️ Breaking: a body that was cut says so in the shared way
- **Now:** The marks differ: Validation puts `Truncation` with `Reason: "ArtifactBytes"` in its body (cut at 8 MiB), Mass writes `ArtifactTruncated` and `ArtifactTruncationIndex` (cut at 1 MiB), DataRegistry writes `Truncated` and `TotalCount`, and `DeleteAsset` writes `ReferencersTruncated`.
- **2.0.0:** The body and `Result` both carry the shared truncation marks, with `Reason: ByteLimit`. No mark is specific to an artifact.
- **Migrate:** Update code that reads these marks when you move to 2.0.0.

### Times in a body are ISO 8601 in UTC
- **Now:** Times in a body are written as `%Y%m%d_%H%M%S` (for example in the audit logs of `RestartEditor`, `SaveAllPackages`, `ShutdownEditor` and `ExecuteConsoleCommand`), and the artifacts of Runtime have no milliseconds.
- **2.0.0:** A time is an ISO 8601 string in UTC, with milliseconds and a trailing `Z`.
- **Migrate:** Update code that parses these times when you move.

## How unavailable commands are shown

### ⚠️ Breaking: when both the plugin and the version are missing, the version is reported first
- **Now:** `UnavailableDetail` is `OptionalPluginDisabled` when a command lacks both the plugin and the engine version it needs. For example, this affects the Niagara and Sequencer Animation Mixer commands.
- **2.0.0:** It is `EngineVersion`. The `ErrorCode` stays `AbilityUnavailable`.
- **Migrate:** Branch on `AbilityUnavailable`, and read `UnavailableDetail` for the reason.

### The schema of a command does not change with the engine version or the plugins
- **Now:** Some commands declare a different schema, with other parameters or enum values, depending on the engine version or on the plugins that are present. For example: `SetPhysicsSolverSettings` and `SetViewModelSource`.
- **2.0.0:** The schema is the same everywhere. A parameter or a value that is not usable in the environment is described in the description and refused when it is used, with `AbilityUnavailable` and `Result.Reason`, and the refusal names the parameter and the value.
- **Migrate:** Read the description of a parameter in `DescribeCommand` for the conditions under which it works.

### ⚠️ Breaking: `UnavailableDetailMessage` becomes `Remedy`
- **Now:** `DescribeCommand` returns the guidance text in `UnavailableDetailMessage`.
- **2.0.0:** The key is `Remedy`, with no period in which both are returned. It is returned only when the main reason is `HandlerUnavailable`, and a row of `ListCommands` has none.
- **Migrate:** Read `Remedy` when you move.

### ⚠️ Breaking: `UnavailableDetail` is returned only with `HandlerUnavailable`, and `Unspecified` is gone
- **Now:** `ListCommands` rows and `DescribeCommand` carry `UnavailableDetail` for every command that is not available, and it takes one of eight values, including `Unspecified`.
- **2.0.0:** A row or a description whose reasons do not include `HandlerUnavailable` carries no `UnavailableDetail`, and the value `Unspecified` is no longer returned, so there are seven values.
- **Migrate:** Treat a missing `UnavailableDetail` as "the reason is not `HandlerUnavailable`".

## Masking environment information

### The markers that replace file paths in responses are unified
- **Now:** The markers differ by response. For example, the crash report, the Python traceback and the Widget Blueprint compile each use their own.
- **2.0.0:** One set of markers replaces the file paths in every response. The set is listed with 2.0.0.
- **Migrate:** Do not match on the text of a marker.

## MCP Bridge and the Claude Code plugin

### ⚠️ Breaking: `Data` is removed from the six responses that the bridge makes itself
- Announced in [MCP Bridge 1.3.0](changelog.md#mcp-bridge-130--released-2026-11-26).
- **Now:** The six responses that the bridge returns itself carry `Result`, and the same value stays in `Data`. They are the `ShutdownEditor` no-op, the launch and attach of `RestartEditor` without a session, the two responses that forward a shutdown, and the two responses that recover an unresponsive editor, all through `uaip_execute`.
- **2.0.0:** `Data` is removed, in the next major version of the bridge, released together with UAIP 2.0.0.
- **Migrate:** Read `Result`.

### ⚠️ Breaking: the keys of `_inlined_artifacts` are PascalCase
- **Now:** Each element has `artifact_id`, `content_type` and `data_base64`.
- **2.0.0:** The keys are in PascalCase (for example `artifact_id` becomes `ArtifactId`). The bridge is released together with UAIP 2.0.0 (see the item above).
- **Migrate:** Update the code that reads inlined artifacts when you move.

### A declined `RestartEditor` through the bridge carries its remedy in `ErrorMessage`
- **Now:** When the editor declines a `RestartEditor` that goes through `uaip_execute`, the bridge answers with the editor's reason and copies the `Remedy` into the result.
- **2.0.0:** The bridge does not copy `Remedy`; the guidance is in `ErrorMessage`.
- **Migrate:** Read `ErrorMessage`.

### A script that reads HTTP 408 for `Timeout` needs a change
- **Now:** The HTTP status of `Timeout` is 408.
- **2.0.0:** It is 504 (see "ErrorCode and refusals").
- **Migrate:** If your own script decides `Timeout` from the HTTP status, decide it from `ErrorCode` instead.

## Changed since the 1.3.0 notice

The 1.3.0 changelog gave notices that this page now states differently. Each item says what the 1.3.0 changelog said and what is true now. The changelog entries carry a note that points here. The 1.3.0 notices are under [UAIP Plugin 1.3.0](changelog.md#uaip-plugin-130--2026-11-26).

### The keys that give the reason a command is unavailable do not stay as they are
- **1.3.0 said:** `UnavailableReason`, `UnavailableDetail` and `AdditionalUnavailableReasons` stay, together with `SecretValuesWithheldReason`.
- **Now:** The names stay, but what they carry changes in 2.0.0. A row or description whose reasons do not include `HandlerUnavailable` carries no `UnavailableDetail`, and `Unspecified` is not returned; `UnavailableDetailMessage` becomes `Remedy`, which only the main reason `HandlerUnavailable` carries; an element of `QueryCapabilities` for a capability that the edition does not ship carries `UnavailableDetail: "NotInThisEdition"` instead of `UnavailableReason`; and a response that uses `UnavailableReason` for something other than availability, such as `DumpStateTreeInstanceData` and CommonUI `GetInputState`, gives it in `Reason`. See "How unavailable commands are shown", "Capabilities and ini settings" and "Commands added in 1.3.0".

### What 1.3.0 said might come earlier in a 1.x release comes in 2.0.0
- **1.3.0 said:** Where a response does not carry `Reason` or the new secret-mask keys yet, it gains them no later than 2.0.0, and `Result.IntegrityState`, `Result.RequiresFollowupCompile`, `Result.SavedPackages` and `Result.WrittenFiles` may already appear in a 1.x release.
- **Now:** All of these first appear in 2.0.0. No 1.x minor release is planned, and a patch release does not change the public API.

### The setting for changes during a Play session and the removal of the capability are in the same version
- **1.3.0 said:** A later release adds a `[UAIP.SafetyPolicy]` setting for changes during a Play session, and `ToolsetEditDuringPlaySession` is removed in 2.0.0.
- **Now:** The setting is added in 2.0.0 and `ToolsetEditDuringPlaySession` is removed in the same version, with no period in which both exist. See "Capabilities and ini settings".

### Only what broke the safety rules and the response contract was fixed in 1.3.0
- **1.3.0 said:** What was wrong with secret values, password fields and the report of artifacts that could not be saved was fixed in that release.
- **Now:** Only what broke the safety rules and the response contract was fixed. The other differences are fixed in 2.0.0, together with those of the older commands. See "Commands added in 1.3.0" and "Secret values".

## Update history

- 2026-11-27: This page was created.
- 2026-11-27: The basis of the ⚠️ mark in the [Versioning Policy](changelog.md#versioning-policy) of the changelog was changed. From the release after 1.3.0, it is the calls that succeeded in 1.3.0.
- 2026-11-27: The [Deprecation policy](changelog.md#deprecation-policy-rarely-removed) of the changelog was rewritten. It now has two exceptions: removing a command when Epic removes an engine API, and removing an `Experimental` command that was announced beforehand.
- 2026-11-27: How `DragGraphNode`, `ConnectGraphPins` and the job commands of one family stay in 2.0.0 was decided: they keep their 1.x form and become Deprecated when the commands that replace them exist. `UAIP.Core.WaitForJob` and the change from `ArtifactIds` to `Artifacts` in a scenario were added.

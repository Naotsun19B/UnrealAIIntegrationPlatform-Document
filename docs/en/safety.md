**[日本語](../ja/safety.md)** | [Back to README](../../README.md)

# Safety & Capabilities

UAIP applies per-command authorization in four layers. Understanding the layers helps you diagnose errors quickly and configure the right permissions for your workflow.

---

## Authorization layers

| Layer | Mechanism | Scope | Error on failure |
|---|---|---|---|
| 1 | `FCapabilitySet` — the process-wide capability set computed once at editor startup from SafetyPolicy | Process-wide (shared by every session) | `CapabilityNotAvailable` |
| 1.5 | `FRoleGate` — a deny-only downgrade bound to the session, resolved from an optional role token | Per-session (only narrows what Layer 1 already grants; can never add a capability) | `CapabilityNotAvailable` |
| 2 | `FSafetyPolicy` bool switches / `DeniedCapabilities` | Process-wide, immutable at runtime | `PolicyViolation` |
| 3 | Route-specific opt-in (e.g. scenario route) | Process-wide | `PolicyViolation` |

Layer 1 is **not** per-session — it is one capability set that every session shares, fixed at startup (or refreshed process-wide by `ReloadCapabilities`). Layer 1.5 is the only layer that varies per session: when the editor is configured with roles (see [Roles](#roles-layer-15) below) and a session is bound to one, that role's deny list is intersected with Layer 1's set for that session only. A session with no role bound behaves exactly like Layer 1 alone.

```mermaid
flowchart TB
    Cmd([CommandRequest])
    L1[Layer 1: Process Capability Set]
    L15[Layer 1.5: Role Gate<br/>deny-only, session-bound]
    L2[Layer 2: SafetyPolicy + DeniedCapabilities + DeniedCommands]
    L3[Layer 3: Route opt-in flags]
    Exec([Execute on game thread])

    Cmd --> L1
    L1 -- "missing required capability" --> E1([CapabilityNotAvailable])
    L1 -- ok --> L15
    L15 -- "capability denied by the session's role" --> E15([CapabilityNotAvailable])
    L15 -- ok --> L2
    L2 -- "capability denied / ReadOnly / DisableSave / etc." --> E2([PolicyViolation])
    L2 -- ok --> L3
    L3 -- "route flag not set at launch" --> E3([PolicyViolation])
    L3 -- ok --> Exec

    style E1 fill:#fdd
    style E15 fill:#fdd
    style E2 fill:#fdd
    style E3 fill:#fdd
```

`AllowedCapabilities` and `DeniedCapabilities` interact at Layer 1 / 2 with **deny-wins** semantics:

```mermaid
flowchart LR
    Reg[Module-registered capabilities] --> Allow{"AllowedCapabilities<br/>list"}
    Allow -- "in list" --> Active(Active in the process capability set)
    Allow -- "not in list" --> S1{"DefaultAllow?"}
    S1 -- yes --> Active
    S1 -- no --> X1(Inactive)
    Active --> Deny{"DeniedCapabilities<br/>list?"}
    Deny -- "listed" --> Final([Layer 2 rejects: PolicyViolation])
    Deny -- "not listed" --> OK([Layer 2 passes])
    style Final fill:#fdd
    style OK fill:#dfd
```

---

## Roles (Layer 1.5)

A role narrows the process-wide capability set (Layer 1) for the sessions bound to it. Roles are **deny-only**: a role can only take capabilities away from what the process already grants — it can never add one the process doesn't have. This makes privilege escalation through a role definition structurally impossible, not just discouraged by convention.

Roles are for running several AI agents against the same editor with different levels of trust — for example, an implementer agent that can edit assets and a reviewer agent that should never call a mutating command, even by mistake.

### Defining roles

Add one `+Role=` line per role to `[UAIP.Roles]` in `Config/DefaultUAIP.ini`:

```ini
[UAIP.Roles]
+Role=(Name="reviewer", DeniedCapabilities=("BlueprintEdit","AssetCreate","AssetDelete","EditorActorEdit"))
+Role=(Name="implementer", DeniedCapabilities=())

; Only needed if you also rely on a transport that cannot carry a role identity — see below.
; AllowRoleBlindTransports=False
```

- `Name` must match `[A-Za-z0-9_-]{1,64}` and be unique within the section. An invalid or duplicate entry is rejected at editor startup (the offending line is skipped and logged as an error) rather than silently accepted.
- `DeniedCapabilities` may be empty (`DeniedCapabilities=()`) for a role that denies nothing.
- Leaving `[UAIP.Roles]` with zero `+Role=` lines keeps the role feature **fully disabled** — every session keeps the unmodified process-wide capability set, exactly as before this feature existed.

### How a session gets bound to a role

A role is never inferred from `SessionId` — that value is a caller-supplied string over MCP and HTTP, so it can't be trusted as an identity. Instead:

- Only **MCP-mode** requests (`-uaip-mcp-enable`) can carry a role, via `Authorization: Bearer <role-token>`.
- The editor generates one token per defined role at startup and writes it to `Saved/UAIP/Roles/<RoleName>.token` (not committed to source control, same handling as the existing HTTP/WS auth tokens).
- The MCP Bridge's `config.json` supplies `role_name` (and reads the matching token from that file automatically) or, alternatively, `role_token` directly when the token is provisioned some other way. Both have environment-variable overrides, `UAIP_ROLE_NAME` and `UAIP_ROLE_TOKEN`. Leaving both empty sends requests exactly as they were before roles existed.
- The first request bearing a given `SessionId` binds that session to the resolved role; every later request for the same `SessionId` is checked against that binding, and a mismatched role is rejected — a session's role never changes mid-connection.

Because roles are configured per MCP client connection (in that client's own bridge config) rather than per request, they compose naturally with one bridge process mapping to one UAIP session — see [Session lifecycle](architecture.md#6-session-lifecycle) in Architecture.

### Transports that can't carry a role

WebSocket, CLI, and the FullHTTP mode of the HTTP transport authenticate with a single shared secret and have no way to identify a role. Once `[UAIP.Roles]` defines at least one role, those transports **refuse to start by default** — starting them would let anyone connecting through one bypass every role restriction silently. Set `AllowRoleBlindTransports=True` to start them anyway; a warning is logged at startup for each affected transport so the bypass stays visible, and commands issued through it run with the unrestricted process-wide capability set.

### How role restrictions surface to a client

- `uaip_list_commands` omits role-denied commands from its default response, the same way it omits any other unavailable command, and counts them under `HiddenReasons.RoleRestricted` (see [Commands Reference → discovery filters](commands.md)).
- `uaip_describe_command` still shows a role-denied command, with `UnavailableReason: "RoleRestricted"`.
- `uaip_query_capabilities` reflects the session's role-narrowed set in its `Capabilities` field, not the full process set — so a capability a role denies never shows up as "available" to a session bound to that role. Its `RegisteredCapabilities` catalog (requested with `IncludeUnavailable: true`) is **not** narrowed: it names every capability the loaded modules declare, with `IsGranted: false` on the ones this session cannot use. That is deliberate — a client has to be able to see that a capability exists in order to ask an operator for it, or to understand why a command it expected is missing. Only names and default policies appear there; a role still denies the operation itself.
- Calling a role-denied command returns the same `CapabilityNotAvailable` error code as a missing process capability, but `ErrorMessage` names both the role and the capability, so the remediation reads differently: a missing process capability is fixed by an operator enabling it, while a role restriction is fixed by not performing that operation under that role — there is nothing to enable.

---

## What this protects against (and what it doesn't)

Both Layer 1.5 (roles) and the token authentication that identifies a role exist to prevent **accidents**, not to hold up against an adversary. There is no way to keep credentials secret from an AI agent running under the same user account on the same machine: a token written to a file can be read, one written to an environment variable can be read from the process environment, and one written to a config file can be read from that file. This is a known, permanent limitation — not a bug to be fixed later.

| Attempted action | Effect |
|---|---|
| Retrying with a different `SessionId` | **Prevented.** The MCP Bridge overwrites every `SessionId` with the one it minted for its own connection, so an MCP client cannot express a different session at all |
| Omitting `SessionId` to fall back to an anonymous session | **Prevented.** The bridge injects its session ID on every forwarded call |
| Connecting through a transport that cannot carry a role identity (WS / CLI / FullHTTP) | **Prevented by default** once at least one role is defined — those transports refuse to start (see [Roles](#roles-layer-15) above). An operator can opt back in with `AllowRoleBlindTransports=True`; doing so makes the bypass visible in the startup log, not undone |
| Pointing an MCP client at a different bridge instance / a different token | **Not prevented technically.** Whether this is possible depends entirely on operating-system file permissions — specifically, whether the AI agent can edit the MCP client's own configuration file. If an agent has broad file-system access, this assumption does not hold automatically |
| Calling `POST /mcp` directly with `curl` or a raw HTTP client | **Not prevented.** Token authentication rejects requests with no token or the wrong one, but an agent that can read the token file can construct a valid request |
| Going around UAIP entirely (a Python script, an Editor Utility Widget, …) | **Not prevented.** Outside UAIP's authorization stack by definition |

What this feature does provide:

1. **An explicit boundary.** Working around it stops being an accident and becomes a deliberate action — one that requires reading a token file, editing a bridge config file, or launching a client another way.
2. **Observability.** Authentication failures, role-binding mismatches, and role-restricted dispatch rejections are all logged as warnings, so bypass attempts (accidental or deliberate) are visible after the fact.

---

## Capability reference

Each command declares the capabilities it requires. A command runs only when the process holds every required capability (Layer 1) and, if the session is bound to a role, that role doesn't deny any of them (Layer 1.5). Capabilities are either **DefaultAllow** (granted automatically) or **DefaultDenied** (must be explicitly enabled in `Config/DefaultUAIP.ini`).

Capabilities marked 🧩 require an optional plugin. If that plugin is not enabled in your `.uproject`, the capability is never registered and commands that require it return `CommandNotFound`.

### Finding out which capabilities exist

`QueryCapabilities` answers two different questions in one response, and it is worth keeping them apart:

| Field | Question it answers |
|---|---|
| `Capabilities` | **What can this session use right now?** The effective set — the process capability set, minus anything `DeniedCapabilities` removes, minus anything the session's bound role denies |
| `RegisteredCapabilityCount` / `UngrantedCapabilityCount` | **How much is there, and how much of it can't this session use?** Always returned, including when both are what you hoped — so "nothing is ungranted" never has to be guessed from a missing field |
| `RegisteredCapabilities` | **What exists at all?** Every capability the loaded modules have declared, whether or not this session holds it. Each entry carries `Name`, `DefaultPolicy` (`Allowed` or `Denied`) and `IsGranted` — so a name present here with `IsGranted: false` is one to ask an operator to enable. **Returned only when you pass `IncludeUnavailable: true`** |

The catalog is **opt-in**, for the same reason `uaip_list_commands` hides unavailable commands by default: it runs to well over a hundred entries in a normal editor, and this is the command you are told to call first. Pass `IncludeUnavailable: true` to receive it. What is *not* optional is knowing it is there — the two counts come back on every call, so a session that never opts in still learns how many capabilities it does not hold, and can then ask for the list.

**"What would an operator have to enable?" is answered from `RegisteredCapabilities` alone**: those are the entries whose `DefaultPolicy` is `Denied`. The response carries no separate list of them, deliberately — it would repeat names already in the catalog without adding anything.

The catalog matters because a DefaultDenied capability is invisible to the effective set by definition. For most of them that is not a problem — they appear in some command's `RequiredCapabilities`, so `uaip_describe_command` names them. `PropertyReferenceEdit` and `PropertyStructuredEdit` are the exception: they are decided from the type of the property being written, long after dispatch, so no command declares them and the catalog is the only place they can be found before one is granted.

Only capability names and their default policies are disclosed. Nothing about the project's contents, and no values, are involved.

---

### DefaultAllow capabilities

These are active in every session without any configuration. They cover read-only observation and common non-destructive operations.

| Capability | What it unlocks |
|---|---|
| `EditorObservation` | Screenshots (`CaptureActiveWindowImage`, `CaptureEditorTabImage`, `CaptureGraphViewportImage`) and JSON state dumps (`DumpEditorState`, `DumpSlateTree`, `DumpSelectionState`, `DumpOutputLog`, `DumpMessageLog`, etc.) |
| `EditorInspect` | Read-only inspection of editor state — assets, details panel, viewport, graph info. Used by shared infrastructure commands |
| `EditorUIAutomation` | UI-driving commands — `ClickWidget`, `SelectMenuItem`, `InputText`, `SetCheckboxState`, `DragGraphNode`, `AcceptDialog`, `CancelDialog`, `InvokeContextMenuAction`, `WaitForWidget`, `FillForm`, `SnapshotUI`, etc. — and their `Toolset.Editor.SlateInspector.*` bridge counterparts, which now require the same capability (earlier releases dispatched the bridge commands without a capability check) |
| `EditorWorkspaceControl` | Tab and panel management — open/close tabs, focus graph editors, manage editor layout |
| `EditorLifecycle` | Editor lifecycle operations — `SaveAll`, `ShutdownEditor`, `RestartEditor` |
| `EditorExecution` | Run Automation Tests and Editor Utility Blueprints from the editor |
| `LiveCoding` | Hot-reload and Live Coding compilation trigger |
| `CrashReportRead` | Access to crash report diagnostic information |
| `AssetCreate` | Create new assets in the Content Browser |
| `AssetMutate` | Modify existing asset properties |
| `AssetWindowControl` | Open and close asset editors |
| `PIEControl` | PIE session control — `StartPIE`, `StopPIE`, `PausePIE`, `ResumePIE`, `LoadMap` |
| `RuntimeInspect` | Read-only inspection of runtime world state — `DumpWorldState`, `DumpActorState`, `DumpComponentState`, `DumpRuntimeLog`, `CapturePerformanceSnapshot` |
| `RuntimeCapture` | Runtime captures — `CaptureViewportImage`, `CheckpointCapture` |
| `RuntimeExecution` | Run functional tests and automation tests in PIE or Standalone |
| `RuntimeGASInspect` 🧩 | Read GAS state during PIE — `GetAttributeValues`, `GetActiveEffects`, `GetGrantedAbilities`, `GetActiveTags`, `FindAttributeSetClasses` (requires `GameplayAbilities` plugin) |
| `RuntimeNiagaraInspect` 🧩 | Read Niagara component state during PIE — `GetUserVariables`, `GetVariable` (requires `Niagara` plugin) |
| `SandboxObserve` 🧩 | Observe the active sandbox — `GetSandboxStatus`, `GetSandboxChanges` (requires `FileSandbox` plugin) |
| `RuntimeInsightsInspect` | Read-only inspection of Unreal Insights tracing — `ListTraceChannels`, `GetTraceStatus`, `ListTraceFiles`. Does not allow starting, stopping or otherwise altering a trace |
| `PendingInteractionInspect` | Poll and cancel a pending interaction — `GetPendingInteractionStatus`, `WaitForPendingInteraction`, `CancelPendingInteraction`. Read-only lookups only; starting an interaction (e.g. `DrawPCGSpline`) is gated separately by the interactive command's own capability plus `SafetyPolicy.AllowUserInteractionPrompt` |

---

### DefaultDenied capabilities

These must be explicitly enabled by adding `+AllowedCapabilities=<name>` entries to `[UAIP.SafetyPolicy]` in `Config/DefaultUAIP.ini`. They cover destructive or significant editing operations.

#### Blueprint & Anim Blueprint editing

| Capability | What it unlocks |
|---|---|
| `BlueprintEdit` | Compile Blueprint assets and inspect their structure |
| `BlueprintVariableEdit` | Add, remove, and modify Blueprint variables |
| `BlueprintGraphEdit` | Add, delete, and connect nodes in Blueprint event graphs |
| `BlueprintComponentEdit` | Add, remove, rename, reparent, duplicate, and edit properties of Blueprint SCS components |
| `AnimBlueprintGraphEdit` | Add, delete, and connect nodes in AnimGraph; compile Anim Blueprints |
| `AnimBlueprintCustomTypeEdit` | Required by `AddAnimGraphNode` when `NodeClass` is not from one of the three modules this domain trusts (`AnimGraph`, `AnimGraphRuntime`, `Engine`) — a project- or plugin-defined `UAnimGraphNode_Base` subclass. There is no separate "dangerous node" capability for this domain: eight node kinds are refused outright regardless of any capability held, see [Commands — UAIP.Editor.AnimBlueprint](commands.md#uaipeditoranimblueprint) |
| `AnimStateMachineEdit` | Add and remove States and Transitions in Anim State Machines |

#### Level / Actor / Property editing

| Capability | What it unlocks |
|---|---|
| `EditorActorEdit` | Spawn, delete, and set transforms of actors in the Level Editor |
| `EditorLevelLoad` | Open and create levels in the editor viewport |
| `EditorViewportControl` | Control the level editor viewport camera — `FocusOnActors`, `GetCameraTransform`, `SetCameraTransform` |
| `PropertyEdit` | Read and write actor / asset properties via the Details panel (`GetActorProperty`, `SetActorProperty`, `GetAssetProperty`, `SetAssetProperty`, etc.) |
| `PropertyReferenceEdit` | Write a property whose value is — or contains, at any depth — an object / class / soft / weak / lazy / interface reference, a delegate or a field path. Clearing a reference needs it too, since attaching and detaching a dependency are the same kind of change |
| `PropertyStructuredEdit` | Write a struct outside the built-in value catalogue, an array, a set, a map, an optional or a fixed-size array — and operate on a single container element rather than replacing the whole value |
| `ProjectConfigEdit` | Read and write project settings (`GetProjectSetting`, `SetProjectSetting`) |
| `EditorUndoRedo` | Undo and redo editor operations |

> **Note**: `PropertyReferenceEdit` and `PropertyStructuredEdit` are not confined to `UAIP.Editor.Property`. They gate reference / struct / container writes in **every** domain that writes properties — Blueprint SCS components, Sequencer sections, Sound and SoundCue assets, PCG and Conversation nodes, DataTable rows, World and project settings, and more. Writing a struct that contains a reference needs both, so the structured one alone is never a way around the reference gate.
>
> A module that already governs reference writes through a capability of its own keeps that name for the reference half — `AnimNotifyReferenceEdit` for `SetAnimNotifyProperty`, `DataflowReferenceEdit` for `SetDataflowNodeProperty`, `SubsonicEventEdit` for the Subsonic property setters, `WidgetSlotReferenceEdit` for `SetSlotProperties`, `EnhancedInputReferenceEdit` for the Enhanced Input mapping mutators, `StateTreeParameterReferenceEdit` for `SetStateTreeParameter`, `NiagaraReferenceEdit` for a reference-typed parameter default on `AddSetParameterEntry` / `AddSetParametersModule` — while the struct / container half is always `PropertyStructuredEdit`. `SetPoseSearchSchemaChannelProperty` is the exception that grants nothing for references: it refuses a reference-bearing type outright, because writing a channel's sub-channel array directly would sidestep the class allowlist `AddPoseSearchSchemaChannel` enforces.
>
> Because both are decided from the property's type while the write runs, **neither appears in any command's declared `RequiredCapabilities`** and `uaip_describe_command` will not show them. They can still be found without attempting a write: `QueryCapabilities` lists both in its `RegisteredCapabilities` catalog — call it with `IncludeUnavailable: true` — with `DefaultPolicy: "Denied"` and `IsGranted: false` until an operator enables them (see [Finding out which capabilities exist](#finding-out-which-capabilities-exist)). To learn what a **particular** property would need, read it first — its `WriteRequirements` object names what a write would need and which of those the session already holds — or take the name out of the refusal. See [Commands — Writing references, structs and containers](commands.md#writing-references-structs-and-containers).

#### Asset management

| Capability | What it unlocks |
|---|---|
| `AssetDelete` | Permanently delete assets |
| `FolderDelete` | Permanently delete content folders |
| `AssetFolderRefactor` | Move and rename assets and folders |
| `RedirectorFixup` | Fix up stale asset redirectors |
| `ShaderCompilation` | Control shader compilation and query its status |
| `ContentBrowserNavigate` | Navigate the Content Browser and select assets — `SelectAssets`, `SetContentBrowserPath` (native and bridge) |
| `PrimaryAssetTypeAdd` | Add a `PrimaryAssetType` to `PrimaryAssetTypesToScan` (`AddPrimaryAssetType`, persisted to `DefaultGame.ini`) |
| `PrimaryAssetTypeRemove` | Remove a `PrimaryAssetType` from `PrimaryAssetTypesToScan` (`RemovePrimaryAssetType`, persisted) |
| `PrimaryAssetRulesOverride` | Temporarily override a `PrimaryAssetId`'s rules in memory (`SetPrimaryAssetRules`, not persisted) |
| `PrimaryAssetLoad` | Explicitly load `PrimaryAsset`s into memory (`LoadPrimaryAsset`) |
| `PrimaryAssetUnload` | Explicitly unload `PrimaryAsset`s from memory (`UnloadPrimaryAsset`) |

#### Material editing

| Capability | What it unlocks |
|---|---|
| `MaterialGraphEdit` | Add, delete, and connect nodes in Material graphs; compile materials |
| `MaterialParameterEdit` | Modify Material parameter values and defaults |
| `MaterialCustomNodeEdit` | Required by `AddMaterialNode` when `ExpressionClass` is `UMaterialExpressionCustom`, `UMaterialExpressionCustomOutput`, or a subclass of either (arbitrary HLSL), regardless of which module it comes from. Already registered before this change, but no command required it until now |
| `MaterialCustomTypeEdit` | Required by `AddMaterialNode` when `ExpressionClass` is not one of the engine's built-in modules (`Engine`, `RenderCore`, `MaterialEditor`, `Landscape`) — a project- or plugin-defined `UMaterialExpression` subclass. A class that is both project-defined and custom-HLSL needs this and `MaterialCustomNodeEdit` together |

> **Note**: `MaterialCustomNodeEdit`, `MaterialCustomTypeEdit`, `AnimBlueprintCustomTypeEdit` (above, under [Blueprint & Anim Blueprint editing](#blueprint--anim-blueprint-editing)), `ControlRigCustomTypeEdit` (below, under [ControlRig editing](#controlrig-editing)), and `EnhancedInputCustomTypeEdit` (below, under [Gameplay systems](#gameplay-systems)) are not only checked when a node of the gated type is added — the same capability is re-checked for every operation that touches an existing node of that type: editing, connecting, disconnecting, compiling, reparenting, and deleting it. ⚠️ Deleting and disconnecting such a node used to be ungated entirely before this change. A type that can no longer be added is still not, by itself, a reason an existing node of it can't be deleted or disconnected. See [Commands — Capability-gated custom types](commands.md#capability-gated-custom-types) for the full explanation.

#### DataTable editing

| Capability | What it unlocks |
|---|---|
| `DataTableRowEdit` | Add and modify rows in DataTable assets |
| `DataTableRowDelete` | Delete rows from DataTable assets |
| `DataTableImport` | Import CSV/JSON data into DataTable assets |

#### Physics Asset editing

| Capability | What it unlocks |
|---|---|
| `PhysicsAssetEdit` | Add, delete, and modify shapes and constraints in Physics Assets |
| `PhysicsBodyEdit` | Add and delete Physics Asset bodies; edit per-body properties (PhysicsMode, MassScale, CollisionProfile, Damping, Offset) |

#### Skeleton / SkeletalMesh editing

| Capability | What it unlocks |
|---|---|
| `SkeletonAssetEdit` | Add, remove, and modify sockets, virtual bones in Skeleton assets |
| `SkeletalMeshMaterialEdit` | Assign and replace material slots on Skeletal Meshes |

#### Geometry Collection (Chaos Destruction) editing

Read-only inspection (`GetGeometryCollectionInfo`, `GetGeometryCollectionClusterInfo`, `GetGeometryCollectionDestructionSettings`) is DefaultAllow (`EditorInspect`). The read-only `SelectGeometryCollectionBones` command is also gated by `EditorInspect`, but additionally requires the `Fracture` plugin — see [Commands Reference](commands.md). Every write is split across three capabilities by risk profile: creating or merging assets, fracturing/merging/deleting/splitting/validating bones (all destructive geometry operations), and everything else (cluster hierarchy, geometry attributes, damage settings).

| Capability | What it unlocks |
|---|---|
| `GeometryCollectionCreate` | Create a new `UGeometryCollection` from a Static Mesh (`CreateGeometryCollectionFromStaticMesh` 🧩, requires the `GeometryCollectionPlugin`) and merge one collection's geometry into another (`MergeGeometryCollectionAssets`, no plugin dependency) |
| `GeometryCollectionFracture` 🧩 | Fracture a collection (`FractureGeometryCollectionUniform` / `Voronoi` / `Plane` / `Slice` / `Brick` / `WithMesh` / `WithMeshArray`), merge or delete bones (`MergeGeometryCollectionBones`, `DeleteGeometryCollectionBranch`), merge tiny geometry (`FixGeometryCollectionTinyGeometry`), split disconnected islands (`SplitGeometryCollectionIslands`), and clean up structural inconsistencies (`ValidateGeometryCollection`) — 12 commands, all requiring the `Fracture` plugin |
| `GeometryCollectionEdit` | Edit the bone cluster hierarchy (`ClusterGeometryCollectionBones`, `UnclusterGeometryCollectionBones`, `RenameGeometryCollectionBone`), geometry display/derived-data attributes (visibility, material, normals, convex hulls, exploded view, bone colors), and the damage-model/clustering settings (`SetGeometryCollectionDestructionSettings`) — 11 commands. `AutoClusterGeometryCollection` and the 6 attribute-editing commands (marked 🧩) additionally require the `Fracture` plugin; the remaining 4 have no plugin dependency |

#### Motion Matching / Pose Search editing

| Capability | What it unlocks |
|---|---|
| `PoseSearchAssetEdit` 🧩 | Add, remove, reorder, and configure channels and compatible skeletons in PoseSearch Schema assets; add and remove animations, set database schema, animation settings, and Normalization Set membership on PoseSearch Database assets; start database index builds (requires `PoseSearch` plugin). Writing a struct or container through `SetPoseSearchSchemaChannelProperty` additionally requires `PropertyStructuredEdit`; a reference-bearing type is refused outright and no capability lifts that |

#### AnimNotify editing

| Capability | What it unlocks |
|---|---|
| `AnimNotifyEdit` | Add / remove notify tracks; add / remove / edit AnimNotify and AnimNotifyState entries on `UAnimSequence` / `UAnimMontage` / `UAnimComposite`; fix up invalid notify guids. Required by every edit command in `UAIP.Editor.AnimSequence` |
| `AnimNotifyReferenceEdit` | Required in addition to `AnimNotifyEdit` when `SetAnimNotifyProperty` writes a property that is — or contains — a reference of any kind (object / class / soft / weak / lazy / interface, delegate, field path). Writing a struct or container additionally requires `PropertyStructuredEdit` |

#### MetaHuman character editing

These capabilities all require the `MetaHumanCharacter` plugin. They are split by risk profile rather than by command count — creating an asset, reading a file off disk, starting a minutes-long synthesis job, sending data to an external service, and running a build that deletes assets on failure each deserve a separate decision.

| Capability | What it unlocks |
|---|---|
| `MetaHumanAssetCreate` 🧩 | Create new MetaHuman character assets — `CreateMetaHumanCharacter` native and `Toolset.Editor.MetaHuman.Create` bridge. The generic `UAIP.Editor.Assets.CreateAsset` command is also blocked for `UMetaHumanCharacter` (and any subclass) unless this capability is granted, so the DefaultAllow `AssetCreate` capability cannot be used to bypass it |
| `MetaHumanEdit` 🧩 | Every local mutation of an existing character — body constraints and shape, skin, eyes, makeup, head model and face evaluation settings, face sculpting and landmark editing, conforming and fitting, wardrobe slot assignment, preview viewport settings, build prerequisite checks and state polling, and `ReleaseEditSession` — plus the reads that require an edit session and therefore cannot declare themselves read-only. Also gates every `Toolset.Editor.MetaHuman.*` bridge command except `Create` |
| `MetaHumanFileImport` 🧩 | Read a face DNA file from the OS file system — `ImportFaceFromDna`, `FitFaceFromBodyWithEyesTeethDna`. Gated separately from ordinary edits because the imported file is untrusted binary handed to an engine parser |
| `MetaHumanTextureSynthesis` 🧩 | Start high resolution face texture synthesis — `RequestTextureSources`. Runs for minutes and writes its results to disk, so it is not granted along with ordinary parameter edits |
| `MetaHumanCloudRigging` 🧩 | Start face rig generation — `RequestAutoRigging`. ⚠️ This is the only command in the module that sends character data to an external service (Epic's cloud rigging service), so it is always an explicit decision |
| `MetaHumanBuild` 🧩 | Run the MetaHuman asset build pipeline — `BuildMetaHuman`. Blocks the game thread for the whole build and deletes the assets it created when the build fails, so it carries both a responsiveness and a destructive aspect |

#### UMG / Widget editing

| Capability | What it unlocks |
|---|---|
| `WidgetTreeEdit` | Add, remove, and reparent widgets in UMG Widget Blueprints |
| `WidgetVariableEdit` | Add and remove widget variables |
| `WidgetAnimationEdit` | Create Widget Animations and add animation tracks |
| `WidgetBindingEdit` | Add and remove property bindings |
| `WidgetSlotReferenceEdit` | Required when `SetSlotProperties` writes a slot property that is — or contains, at any depth — a reference of any kind (object / class / soft / weak / lazy / interface, delegate, field path). Decided from the type of the property being written, so it will not appear in `SetSlotProperties`'s declared `RequiredCapabilities` — see the note under [Level / Actor / Property editing](#level--actor--property-editing). Writing a struct or container additionally requires `PropertyStructuredEdit` |

#### Sequencer editing

| Capability | What it unlocks |
|---|---|
| `SequencerStructureEdit` | Add / remove tracks and sections; set playback range |
| `SequencerKeyframeEdit` | Add, delete, and edit keyframes on Sequencer channels |
| `SequencerBindingEdit` | Add and remove actor Possessable bindings in Level Sequences |
| `SequencerPlaybackControl` | Control Sequencer playback state (Play, Pause, SetPlayheadFrame, SetPlaybackSpeed, SetLoopMode) |
| `SequencerPropertyEdit` | Read and write `UMovieSceneSection` properties |

#### ControlRig editing

| Capability | What it unlocks |
|---|---|
| `ControlRigHierarchyEdit` | Add / remove / transform Control elements, bones, and nulls in the ControlRig hierarchy |
| `ControlRigGraphEdit` | Add, delete, and connect nodes in RigVM graphs; compile ControlRigs |
| `ControlRigBlueprintCreate` | Create ControlRigBlueprint assets via `CreateAsset` |
| `ControlRigComponentEdit` | Add, remove, rename, reparent, and rewrite the content of components on hierarchy elements (`FRigBaseComponent` substructs) — the generic component commands under `UAIP.Editor.ControlRig`, and every write in `UAIP.Editor.ControlRig.Dynamics` and `UAIP.Editor.ControlRig.Physics`. One capability covers all of them deliberately: creating a component with initial content reaches the same import path as replacing the content of an existing one, so granting them separately would only offer a way around the other's checks |
| `ControlRigCustomTypeEdit` | Required whenever a RigVM unit struct or a rig hierarchy component struct comes from outside the seven modules this domain accepts (`/Script/ControlRig`, `/Script/ControlRigDynamics`, `/Script/ControlRigPhysics`, `/Script/ControlRigSpline`, `/Script/ControlRigModules`, `/Script/AnimationCore`, `/Script/Engine`) — a struct a project or a plugin declares. It gates both `AddGraphNode` / `AddComponent` and every later operation on an existing node or component of such a struct. There is no separate "dangerous type" capability for this domain, and control types are not gated at all: structs marked `Deprecated` or `Hidden` are refused regardless of any capability held, see [Commands — UAIP.Editor.ControlRig](commands.md#uaipeditorcontrolrig) |

#### AI systems

| Capability | What it unlocks |
|---|---|
| `BehaviorTreeGraphEdit` | Add and remove Behavior Tree nodes; set node properties |
| `BlackboardEdit` | Add and remove Blackboard keys |

#### StateTree editing

| Capability | What it unlocks |
|---|---|
| `StateTreeStructureEdit` | Add / remove States; compile StateTree assets |
| `StateTreeNodeEdit` | Add / remove Tasks and Transitions; edit node properties |
| `StateTreeParameterReferenceEdit` | Required when `SetStateTreeParameter` writes a root parameter value that is — or contains — a reference of any kind. Decided from the parameter's `PropertyBag` value type at write time, so it will not appear in `SetStateTreeParameter`'s declared `RequiredCapabilities` — see the note under [Level / Actor / Property editing](#level--actor--property-editing). Writing a struct or container additionally requires `PropertyStructuredEdit` |

#### SoundCue editing

| Capability | What it unlocks |
|---|---|
| `SoundCueGraphEdit` | Add, delete, and connect nodes in SoundCue graphs; edit properties; compile SoundCues |

#### Sound asset editing

| Capability | What it unlocks |
|---|---|
| `SoundClassEdit` | Set SoundClass asset properties; add and remove child classes (`SetSoundClassSettings`, `AddSoundClassChild`, `RemoveSoundClassChild`) |
| `SoundAttenuationEdit` | Set FSoundAttenuationSettings fields on SoundAttenuation assets (`SetSoundAttenuationSettings`) |
| `SoundMixEdit` | Set SoundMix properties; add, update, and remove SoundClassAdjuster entries (`SetSoundMixSettings`, `SetSoundMixAdjuster`, `RemoveSoundMixAdjuster`) |

#### MVVM editing

| Capability | What it unlocks |
|---|---|
| `ViewModelBindingEdit` | Add / remove / update View Bindings and View Events on WidgetBlueprints; add / remove ViewModel properties (`AddViewBinding`, `RemoveViewBinding`, `UpdateViewBinding`, `SetViewBindingEnabled`, `SetViewBindingConversionFunction`, `SetViewBindingExecutionMode`, `AddViewEvent`, `RemoveViewEvent`, `AddViewModelProperty`, `RemoveViewModelProperty`) |
| `ViewModelSourceEdit` | Wire and manage ViewModel connections in WidgetBlueprints (`AddViewModelToWidget`, `RemoveViewModelFromWidget`, `RenameViewModelInWidget`, `ReparentViewModelInWidget`, `SetViewModelSource`) |

#### Curve editing

| Capability | What it unlocks |
|---|---|
| `CurveKeyEdit` | Add, delete, and edit keys (value, interpolation, tangents) on UCurveFloat / UCurveVector / UCurveLinearColor |

#### Gameplay systems

| Capability | What it unlocks |
|---|---|
| `GameplayTagEdit` | Add, remove, and rename tags in project tag tables |
| `GameplayTagRestrictedEdit` | Modify restricted tag lists |
| `GameFeatureCreate` 🧩 | Create and scaffold GameFeature Plugin definitions (requires `GameFeatures` + `GameFeaturesEditor` plugins) |
| `GameplayCueMutation` 🧩 | Add / remove GameplayCue tags, create GameplayCueNotify assets, execute Cues on actors (requires `GameplayAbilities` plugin) |
| `EnhancedInputEdit` | Edit Input Action / Input Mapping Context assets — add / remove / modify mappings, modifiers, and triggers |
| `EnhancedInputReferenceEdit` | Required in addition to `EnhancedInputEdit` when a Trigger or Modifier property being written is — or contains — a reference of any kind (object / class / soft / weak / lazy / interface, delegate, field path). Decided from the type of the property being written, so it will not appear in the mapping mutators' declared `RequiredCapabilities` — see the note under [Level / Actor / Property editing](#level--actor--property-editing). Writing a struct or container additionally requires `PropertyStructuredEdit` |
| `EnhancedInputCustomTypeEdit` | Required in addition to `EnhancedInputEdit` when a Trigger or Modifier class comes from outside the `/Script/EnhancedInput` module — a project module, a plugin module, or a Blueprint subclass of `UInputTrigger` / `UInputModifier`. It gates `SetInputMappingTrigger` / `SetInputMappingModifier` / `SetInputActionTrigger` / `SetInputActionModifier` when such a class is named, and `RemoveInputMapping` / `DeleteInputAction` / `DeleteMappingContext` when the target holds an instance of one. Decided from the class named in the request (or found in the target) rather than from the command, so it does not appear in any handler's declared `RequiredCapabilities`. There is no separate "dangerous type" capability for this domain, and two trigger kinds — `UInputTriggerChordAction` and `UInputTriggerChordBlocker`, plus anything derived from either — are refused regardless of any capability held, see [Commands — UAIP.Editor.EnhancedInput](commands.md#uaipeditorenhancedinput) |

#### Editor operations

| Capability | What it unlocks |
|---|---|
| `EditorKeyboardInput` | Simulate keyboard input to editor UI widgets — `PressKey` native and `Toolset.Editor.SlateInspector.PressKey` bridge (the bridge also now applies `AllowKeyboardInput` / `AllowKeyboardModifierInput` and the blocked-shortcut list; see [Commands Reference](commands.md#uaipeditoruiautomation) for the one place it stays stricter than native) |
| `EditorExecCommand` | Execute low-level editor commands via `GUnrealEd->Exec` |
| `LogVerbosityEdit` | Change log verbosity levels — `SetLogVerbosity` native and `Toolset.Editor.Toolset.Logs.SetVerbosity` bridge |
| `ViewportAnnotationCapture` | Capture annotated viewport images with world-coordinate labels — `CaptureViewportImageAnnotated` |
| `EditorTabSpawn` | Open, close, and enumerate editor tabs by their Slate `FTabId` — `OpenTabById`, `CloseTabById`, `ListSpawnableTabs`. Distinct from the DefaultAllow `EditorWorkspaceControl`, which only reaches asset-editor tabs through `AssetPath`: an arbitrary `TabId` can run a third party's bound delegate — `CanSpawnTab`/`OnSpawnTab` when opening, `OnCanCloseTab`/`OnTabClosed` when closing, and the display-name/tooltip `TAttribute` accessors when listing — including internal tabs never shown in a menu. `ListSpawnableTabs` requires the same capability rather than being DefaultAllow: enumerating carries the same delegate-execution risk, and the only use for the list is deciding what to open or close. Closing is not limited to tabs this session opened — any tab currently open can be closed, including ones a human has open for their own work, and closing bypasses the tab permission list entirely so that cleanup never fails after a permission change |

#### Script execution

| Capability | What it unlocks |
|---|---|
| `ScriptExecution` 🧩 | Run Python scripts in the editor (`RunEditorPythonScript`; requires `PythonScriptPlugin`) |
| `PythonCommandExecution` 🧩 | Execute dynamically registered `@uaip_command` Python commands (requires `PythonScriptPlugin`) |
| `PythonExtensionReload` 🧩 | Rescan and reload registered Python commands (`ReloadPythonCommands`; requires `PythonScriptPlugin`) |

#### Runtime — restricted operations

| Capability | What it unlocks |
|---|---|
| `RuntimeCVarRead` | Read engine-wide CVar values — `UAIP.Runtime.Engine.CVar.GetConsoleVariable`, `SearchConsoleVariables` (owned by `UAIPRuntimeEngineManagement`) |
| `RuntimeCVarWrite` | Set or reset CVar values — `UAIP.Runtime.Engine.CVar.SetConsoleVariable`, `ResetConsoleVariable` (sensitive names and `ECVF_ReadOnly` CVars are rejected; `ECVF_Cheat` CVars additionally require the `AllowCheatCVarWrite` SafetyPolicy switch; owned by `UAIPRuntimeEngineManagement`) |
| `CVarInspect` | Search CVars with sensitive-pattern filtering — `Toolset.Editor.Toolset.EngineManagement.SearchCVars` bridge (owned by `UAIPEditorEngineManagement`) |
| `RuntimeActorManipulation` | Spawn, destroy, teleport, and possess actors during PIE |
| `RuntimeExecCommand` | Execute console commands at runtime via `UWorld` |
| `RuntimeInputInjection` | Inject keyboard / Enhanced Input / legacy input events into PIE (`InjectInputKey`, `InjectEnhancedInputAction`, `AddMappingContext`, `SetInputMode`, `FlushInput`, …) |
| `RuntimeNiagaraMutation` 🧩 | Set Niagara user variables / replace Niagara system at runtime (`SetVariable`, `SetSystem`; requires `Niagara` plugin) |
| `GauntletExecution` | Launch Gauntlet automated test sessions |

#### Runtime Insights trace capture

Unreal Insights tracing is split into four capabilities because reading the state of tracing, altering it, taking the raw capture file, and analysing a capture are four different decisions.

| Capability | What it unlocks |
|---|---|
| `RuntimeInsightsControl` | Start, stop, pause and resume a trace, mutate its channel set, and write bookmarks and regions into it — `StartTrace`, `StopTrace`, `PauseTrace`, `ResumeTrace`, `SetTraceChannels`, `AddTraceBookmark`, `BeginTraceRegion`, `EndTraceRegion` |
| `RuntimeInsightsAttachTraceFile` | Hand the captured `.utrace` file itself over as an artifact (`StopTrace` with `AttachTraceFile: true`). Gated separately from `RuntimeInsightsControl`, and never required to *stop* a trace — a session without it can always stop cleanly, the file is simply skipped |
| `RuntimeInsightsAnalyze` | Analyse a captured trace and read the extracted sections — `AnalyzeTrace`, `GetTraceAnalysisStatus`, `GetTraceAnalysisResult`. Only registered in builds where trace analysis is supported |

> ⚠️ **Taking the `.utrace` file discloses more than any channel setting suggests.**
> The full process command line — absolute paths, the user name and every launch option — is written through an always-on internal channel that can neither be listed nor turned off. It is therefore present in **every** trace file regardless of which channels were recorded, and setting `AllowLogDump=False` does **not** prevent it. This is the reason `RuntimeInsightsAttachTraceFile` exists as its own DefaultDenied capability.
> The analysis commands are not equivalent: the `Diagnostics` section reports a sanitised command line, so an analysis result and the raw `.utrace` disclose different things.

**Channel disclosure gating.** Trace channels are classified by what they can disclose (log text, host paths, screen content, network data, asset structure, code structure, or nothing beyond timings). `StartTrace` is rejected with `PolicyViolation` when the effective channel set records log text and `AllowLogDump` is false, so Insights cannot be used to route around the flag that gates `DumpOutputLog`.

Attaching the raw file is then decided per disclosure class, on top of the `RuntimeInsightsAttachTraceFile` capability:

| What the recorded channels could disclose | What has to be set for the file to be attached |
|---|---|
| Nothing beyond timings, asset structure, code structure | Nothing — the analysis sections report these unredacted anyway, so the file discloses nothing they do not |
| Log text (`log`, `bookmark`, `region`) | `AllowLogDump` — the same flag that decides whether those channels may record at all and whether the matching analysis sections may be extracted |
| Host paths (`file`, `cook`), screen content (`screenshot`), network addresses (`net`) | `AllowDisclosingTraceAttachment` — the analysis sections sanitise, mask or reduce these to metadata, and the raw file does none of that |
| A channel this build does not classify | Refused whatever is set — nothing knows what such a channel records, so no setting can speak for it |

Attaching is refused regardless of those settings for a channel set that was mutated while recording, for a trace recovered as an orphan, and for files larger than 64 MB.

> ⚠️ **In the editor, attaching normally needs both flags.** The engine enables `cpu`, `gpu`, `frame`, `log`, `bookmark`, `screenshot` and `region` at editor startup even without a `-trace` argument, so virtually every trace captured in the editor carries both log text and screen content. UAIP will not turn those channels off for you — channel state is process-global and disabling them would break a measurement someone else set up. Set **both** `AllowLogDump=True` and `AllowDisclosingTraceAttachment=True` if you want the `.utrace` file itself.
>
> `StartTrace` says so up front rather than letting you find out after several hundred megabytes: when the channels that would be recording carry something the policy withholds the raw file for, its `Data.Warnings[]` contains an `AttachDisabledByPolicy` entry naming those channels and the setting that would allow them. `StopTrace` still succeeds in that case — it reports `AttachSkippedReason: "DisclosureChannelPolicy"` instead of returning the file, so a cleanup step never fails and leaves a trace running.

> ⚠️ **The channel set is sampled about once per second.** A channel enabled and disabled again inside that window can be missed, which is precisely why attaching the raw file is gated by its own capability rather than by the observed channel set alone. Treat the polling loop as a safety net, not as a guarantee.

**Scope of the network-destination restriction.** No command in this module can send a trace to a network destination — the connection type is hard-coded to a file inside UAIP's own trace directory, and no parameter exposes it. The `trace.` console prefix is additionally on the `ExecuteConsoleCommand` deny-list, so `Trace.Send` / `Trace.Start` / `Trace.Enable` cannot be reached through that command. That deny-list covers one route, not every route: an editor with `PythonScriptPlugin` enabled can still reach the same console commands through `RunEditorPythonScript`, which is why `ScriptExecution` is a capability of its own. Read this as "no command here sends a trace to the network", not as "nothing in the editor can".

**Analysing traces captured outside UAIP.** By default `AnalyzeTrace` only accepts a file name that `ListTraceFiles` reported, which keeps it inside UAIP's own trace directory. To analyse a `.utrace` produced by a packaged build, another machine or a CI run, **both** of these must be set in `[UAIP.SafetyPolicy]`:

```ini
AllowExternalTraceAnalysis=True
ExternalTraceDirectory=D:/TraceDrop
```

Either one alone opens nothing. The path passed as `ExternalTracePath` is then required to resolve inside that directory.

> ⚠️ **Symbolic links and junctions are not resolved.** A link placed inside `ExternalTraceDirectory` that points somewhere else is followed. Point `ExternalTraceDirectory` at a directory kept for UAIP alone — not at a shared drop location, a user profile folder, or the project directory.

> **This is a scope limitation, not a structural guarantee.** `RunEditorPythonScript` still reaches the engine's trace system directly — Python execution is a known path around the capability layer, and it is managed by the capabilities that command requires (`EditorExecution` plus `ScriptExecution`, which is DefaultDenied) rather than by anything in this module. `GetTraceStatus` can report a networked destination such as `TracingToServer`; that is observability of something else's trace, not something UAIP can produce.

#### Optional graph editors

These capabilities depend on specific optional plugins. If the plugin is not enabled, the capability is never registered.

| Capability | Plugin required | What it unlocks |
|---|---|---|
| `MetaSoundGraphEdit` 🧩 | `Metasound` | Add, delete, and connect nodes in MetaSound graphs |
| `DataflowGraphEdit` 🧩 | `Dataflow` | Add, delete, and connect nodes in Dataflow graphs; get/set node properties |
| `DataflowReferenceEdit` 🧩 | `Dataflow` | Write a reference property of any kind — object / class / soft / weak / lazy / interface, delegate, field path — on Dataflow nodes, including one nested inside a struct or container. Required **in addition to** `DataflowGraphEdit`; a struct or container additionally requires `PropertyStructuredEdit`. A hard reference's target must already be loaded (a write never loads an asset as a side effect), while a soft one is validated against the asset registry. Gated separately because it can repoint a graph at a different asset |
| `ClothAssetEdit` 🧩 | `ChaosClothAsset` | Create/convert Chaos Cloth Assets, create legacy Clothing Assets, bind/unbind them to Skeletal Mesh sections, set Weight Map vertex values, and set Import node mesh references (all destructive operations) |
| `PCGGraphEdit` 🧩 | `PCG` | Add, delete, connect, and reposition nodes; edit graph/instance parameters; manage comment boxes and subgraph nodes in PCG graphs |
| `PCGCustomNodeEdit` 🧩 | `PCG` | Write properties on C++ custom PCG nodes (`SetCustomCppPCGNodeProperty`) |
| `PCGBlueprintNodeEdit` 🧩 | `PCG` | Write properties on Blueprint custom PCG nodes — Class CDO and per-Instance modes (`SetCustomBlueprintPCGNodeProperty`) |
| `PCGGraphAssetCreate` 🧩 | `PCG` | Create new UPCGGraph assets (`CreatePCGGraph`) |
| `PCGGraphExecute` 🧩 | `PCG` | Fire-and-forget PCG graph execution without an actor (`RunPCGInstantGraph`) |
| `PCGVolumeSpawn` 🧩 | `PCG` | Spawn APCGVolume actors into the world (`SpawnPCGGraphInstance`) — ⚠️ do not add to `AllowedCapabilities` in DefaultUAIP.ini (world mutation risk) |
| `PCGNodeInspect` 🧩 | `PCG` | Inspect PCG node execution data views (`GetPCGNodeDataView`) — only functional when `PCG_PROFILING_ENABLED=1` |
| `PCGToolsetUnsafeNodeAdd` 🧩 | `PCG` + `PCGToolset` | Bypass the node-type allowlist guard in `Toolset.Editor.PCG.AddNode` — ⚠️ do not add to `AllowedCapabilities` in DefaultUAIP.ini (allowlist bypass risk) |
| `PCGSplineDraw` 🧩 | `PCG` | Start an interactive spline-draw pending interaction that hands the level viewport over to the human — `DrawPCGSpline` native and `Toolset.Editor.PCG.DrawSpline` bridge. Also requires `SafetyPolicy.AllowUserInteractionPrompt`: this capability states *what* may be touched, the policy flag states that starting one at all takes over the human's viewport and input focus |
| `ConversationGraphEdit` 🧩 | `CommonConversation` | Structurally edit `UConversationDatabase` assets |
| `EQSAssetEdit` 🧩 | `EnvironmentQueryEditor` | Add / remove EQS Generators and Tests; set their properties |
| `WorldConditionStructureEdit` 🧩 | `WorldConditions` | Add and remove conditions in WorldCondition assets |
| `WorldConditionNodeEdit` 🧩 | `WorldConditions` | Edit WorldCondition operator, expression depth, and properties |

#### Semantic search

| Capability | Plugin required | What it unlocks |
|---|---|---|
| `SemanticSearchEdit` 🧩 | `SemanticSearch` (UE 5.8+) | Trigger and cancel semantic index rebuilds — `StartIndexing`, `CancelIndexing` |

#### Niagara editing

These capabilities all require the `Niagara` plugin.

| Capability | What it unlocks |
|---|---|
| `NiagaraAssetCreate` 🧩 | Create Niagara System and Parameter Collection assets |
| `NiagaraBlueprintCreate` 🧩 | Generate Blueprint wrapper classes from Niagara Systems and Components |
| `NiagaraEmitterEdit` 🧩 | Add, remove, and configure emitters in Niagara Systems |
| `NiagaraStackEdit` 🧩 | Add / remove modules, set stack input parameters, and write renderer data (`SetRendererData`, native and bridge) on Niagara emitters |
| `NiagaraStackAutoFix` 🧩 | Automatically resolve Niagara stack diagnostic issues |
| `NiagaraReferenceEdit` 🧩 | Required in addition to `NiagaraStackEdit` when `AddSetParameterEntry` or `AddSetParametersModule` supplies a `DefaultValue` for a parameter whose type is a data interface or an object reference. The value is given as an object path and is stored in the dedicated data-interface / object slot of `FNiagaraVariant`, so the reference is retained properly — it is not packed into the byte payload the other parameter types use. Decided from the parameter's type while the write runs, so it will not appear in either command's declared `RequiredCapabilities` — see the note under [Level / Actor / Property editing](#level--actor--property-editing). Leaving `DefaultValue` unset needs nothing extra. ⚠️ In practice only **data interface** types are reachable: an ordinary object type such as `UTexture2D` is refused at the parameter type-name stage by the type allowlist, before this capability is ever consulted |

#### World Partition editing

| Capability | What it unlocks |
|---|---|
| `WorldPartitionEdit` | Modify World Partition settings — `SetWorldPartitionStreamingEnabled`, `SetRuntimeGridSettings`, `SetActorIsSpatiallyLoaded`, `SetActorRuntimeGrid`, `PinActorInWorldPartition`, `UnpinActorFromWorldPartition` |
| `DataLayerEdit` | Create, delete, and modify Data Layer assets and instances — `CreateDataLayerAsset`, `DeleteDataLayerAsset`, `CreateDataLayerInstance`, `DeleteDataLayerInstance`, `SetDataLayerType`, `SetDataLayerInitialRuntimeState`, `SetDataLayerIsLoadedInEditor`, `SetDataLayerVisibility`, `SetParentDataLayerInstance`, `AddActorToDataLayer`, `RemoveActorFromDataLayer` |
| `HLODBuild` | Build and manage HLOD data — `CreateHLODLayer`, `DeleteHLODs`, `SetActorHLODLayer`, `BuildHLODs`, `CancelHLODBuild` |

#### Foliage editing

| Capability | What it unlocks |
|---|---|
| `FoliageTypeEdit` | Register and configure foliage types on a level — `AddFoliageTypeToLevel`, `RemoveFoliageTypeFromLevel`, `SetFoliageTypeSettings` |
| `FoliageInstanceEdit` | Add and remove individual foliage instances — `AddFoliageInstances`, `RemoveFoliageInstances`, `ResimulateProceduralFoliage` |
| `FoliageBulkDelete` | Delete all instances of a foliage type at once — `DeleteAllFoliageInstances` |

#### ConfigSettings editing

| Capability | What it unlocks |
|---|---|
| `ConfigSettingsEdit` | Modify Project Settings / Editor Preferences and write raw ini keys — `SetSettingsValues` (also required for `DryRun` calls), `SetConfigValue` (runtime) |
| `ConfigSettingsSave` | Persist settings to disk via `ISettingsSection::Save()` — `SaveSettings` (blocked when `bDisableSave` is set) |
| `ConfigSettingsReset` | Revert settings to class defaults — `ResetSettingsToDefaults` |

#### Plugin management

Write commands for plugin state and descriptors. Engine and Marketplace plugins are always read-only regardless of capability. Write commands require an editor restart to take effect.

| Capability | What it unlocks |
|---|---|
| `PluginEnableToggle` | Enable or disable a project plugin — `SetPluginEnabled` native and `Toolset.Plugin.SetPluginEnabled` bridge. Always returns `RestartRequired: true`. ⚠️ GameFeature plugins are blocked regardless of this capability |
| `PluginDescriptorEdit` | Overwrite selected fields of a plugin's `.uplugin` file — `UpdatePluginDescriptor` native and `Toolset.Plugin.UpdatePluginDescriptor` bridge. Also required for `DryRun` calls |
| `PluginDependencyEdit` | Add or remove dependency entries in a plugin's `.uplugin` — `AddPluginDependency`, `RemovePluginDependency` native and their Toolset bridge counterparts |

#### Sandbox session management

These capabilities all require the `FileSandbox` plugin.

| Capability | What it unlocks |
|---|---|
| `SandboxSessionControl` 🧩 | Open and close FileSandbox sessions — `BeginSandboxSession`, `EndSandboxSession` |
| `SandboxPersist` 🧩 | Flush sandbox changes to disk — `CommitSandboxChanges` |
| `SandboxRevert` 🧩 | Discard pending sandbox changes — `RevertSandboxChanges` |

#### Subsonic editing & audition

These capabilities all require UE 5.8+ and the `Subsonic` plugin (Experimental).

| Capability | What it unlocks |
|---|---|
| `SubsonicEventEdit` 🧩 | Every mutating event / action / modifier / parameter / property-binding command on a `USubsonicEventCollection` asset — 16 commands. All of them mutate a single asset within a single transaction, so they are bundled at the same granularity as `PhysicsAssetEdit`. It also serves as the reference capability for the three property setters, so no separate grant is needed to write a reference; writing a struct or container through them additionally requires `PropertyStructuredEdit` |
| `SubsonicEventAudition` 🧩 | Audition an event and stop the current audition — `AuditionSubsonicEvent`, `StopSubsonicAudition`. Kept separate from `SubsonicEventEdit` because auditioning does not mutate the asset, but drives audio device side effects and executes the `Execute()` of loaded action types |

#### Groom editing

These capabilities all require the `HairStrands` plugin (Optional, disabled by default); the whole `UAIP.Editor.GroomAsset` domain is unavailable when it is disabled. Split by what a failure can destroy, not by command count — settings changes leave the source curve data untouched and can be restored by writing the old values back, new-asset generation destroys nothing at all, and curve/binding rebuilds can permanently lose data the caller cannot get back.

| Capability | What it unlocks |
|---|---|
| `GroomAssetEdit` 🧩 | Group/LOD/interpolation/rendering settings patches, asset-wide settings, LOD slot add/remove, Cards/Meshes source configuration and derived-data builds, and non-destructive Dataflow graph assignment — 12 commands. Every affected value is a saved setting the caller can restore by writing the prior value back; the source curve data itself is never touched |
| `GroomAssetCreate` 🧩 | Create a new asset from a Groom without modifying the source — follicle-mask and strands texture generation (`GenerateGroomFollicleMaskTexture`, `GenerateGroomStrandsTextures`) and RBF deformation baking into a new `UGroomAsset` (`BakeGroomRBFDeformation`) — 3 commands. Nothing existing is ever lost, but the commands are heavy (GPU texture generation, or a bake whose engine-side root-data generation can crash the editor process on failure — see the `BakeGroomRBFDeformation` entry in the [Commands Reference](commands.md)) |
| `GroomCurveEdit` 🧩 | Everything that can overwrite guide/strand curve control points — direct writes (`SetGroomGuideCurves`, `SetGroomStrandCurves`), Dataflow graph evaluation (`EvaluateGroomDataflow`), and reimporting a Groom from its source file (`ReimportGroom`) — 4 commands. Curve data lost this way cannot be recovered by writing settings back; a failed reimport in particular is not guaranteed to leave the asset's prior content intact |
| `GroomBindingEdit` 🧩 | Create a `UGroomBindingAsset` against a target SkeletalMesh or GeometryCache, and rebuild an existing binding's derived data in place — 3 commands (`CreateGroomBinding`, `CreateGeometryCacheGroomBinding`, `RebuildGroomBinding`). Creation destroys nothing; a failed rebuild does, because the engine discards the binding's prior derived data before regenerating it |

#### Asset validation

These capabilities require the `DataValidation` plugin, which the project must name explicitly in its `.uproject` — see the `UAIP.Editor.Validation` section of the [Commands Reference](commands.md). Listing the validators, following a validation job and reading its result are DefaultAllow (`EditorInspect`); only running validators and applying their fixes are gated here.

| Capability | What it unlocks |
|---|---|
| `AssetValidation` 🧩 | Run the validators the project registered over assets — `ValidateAssets` (synchronous, up to 8 assets) and `StartValidationJob` (a folder or a list, validated in steps). Denied by default because validation executes project-supplied C++ / Blueprint / Python code that the engine does not forbid from having side effects, and because it loads assets and can trigger shader compilation. Both commands declare themselves read-only so an unrelated session holding a sandbox open cannot block them, but they evaluate the `ReadOnly` policy themselves and refuse while it is in force |
| `AssetValidationFix` 🧩 | Apply one fix a validator offered for a message it produced — `ApplyValidationFix`. Denied by default because it rewrites a real asset and the fixer may leave it saved to disk. Refused outright while `DisableSave` is in force, whatever the fix would do, and refused for an asset under a root UAIP will not write to — validation reads from engine content, repair does not reach it |

---

## Enabling DefaultDenied capabilities

Edit `Config/DefaultUAIP.ini` in your project and add one `+AllowedCapabilities` line per capability:

```ini
[UAIP.SafetyPolicy]
+AllowedCapabilities=BlueprintEdit
+AllowedCapabilities=BlueprintVariableEdit
+AllowedCapabilities=BlueprintGraphEdit
+AllowedCapabilities=EditorActorEdit
```

After editing, either restart the editor or (if `AllowCapabilityReload=True` is set) call:

```
uaip_execute(CommandName="UAIP.Core.ReloadCapabilities")
```

---

## SafetyPolicy settings

In addition to capability gates, `FSafetyPolicy` provides process-wide coarse switches. All default to `False`.

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
AllowCheatCVarWrite=False
AllowExternalTraceAnalysis=False
AllowDisclosingTraceAttachment=False
AllowUserInteractionPrompt=False

; Directory externally captured .utrace files may be analysed from.
; Has no default; AllowExternalTraceAnalysis alone opens nothing.
; ExternalTraceDirectory=D:/TraceDrop

; Lift DefaultDenied capabilities:
; +AllowedCapabilities=BlueprintEdit

; Remove DefaultAllow capabilities from sessions:
; +DeniedCapabilities=EditorUIAutomation

; Block specific commands by fully-qualified name:
; +DeniedCommands=UAIP.Editor.Level.PlaceActorInLevel

; Enable runtime capability reload without editor restart:
; AllowCapabilityReload=True
```

| Key | Default | Effect |
|---|---|---|
| `ReadOnly` | `False` | Reject mutating commands. The two editor lifecycle commands are the one exception — see below |
| `DisableSave` | `False` | Reject disk-writing commands |
| `AllowLogDump` | `False` | Allow `DumpOutputLog` / `DumpMessageLog` |
| `AllowContextMenuMutation` | `False` | Allow `InvokeContextMenuAction` |
| `AllowKeyboardInput` | `False` | Allow `PressKey` (also requires `EditorKeyboardInput` capability) |
| `AllowKeyboardModifierInput` | `False` | Allow Ctrl/Alt/Shift modifier keys inside `PressKey` |
| `AllowPasswordFieldWrite` | `False` | Allow `FillForm` to write into password fields |
| `AllowInputModeBypass` | `False` | Allow `BypassInputMode=true` in Inject commands |
| `DisablePIEStart` | `False` | Reject PIE startup |
| `AllowCheatCVarWrite` | `False` | Allow `SetConsoleVariable` / `ResetConsoleVariable` to write `ECVF_Cheat`-flagged CVars (also requires `RuntimeCVarWrite`) |
| `AllowExternalTraceAnalysis` | `False` | Allow `AnalyzeTrace` to read a `.utrace` captured outside UAIP. **Grants nothing on its own** — `ExternalTraceDirectory` must be set as well |
| `ExternalTraceDirectory` | unset | Root directory an externally captured `.utrace` must live under. ini only (no CLI override), and deliberately has no default |
| `AllowDisclosingTraceAttachment` | `False` | Allow `StopTrace` to hand a captured `.utrace` over as an artifact when its channels could have recorded **host paths, screen content or network addresses**. The analysis sections sanitise, mask or reduce those to metadata; the raw file does not, which is why handing it over is a separate decision. Disclosure of **log text** is governed by `AllowLogDump` instead, and an unclassified channel is refused whatever both are set to. Also requires the `RuntimeInsightsAttachTraceFile` capability. In the editor both this and `AllowLogDump` are normally needed, because the engine enables the log and screenshot channels by itself |
| `AllowUserInteractionPrompt` | `False` | Allow a pending interaction (a command that hands off to a human in the editor instead of finishing on its own, e.g. `DrawPCGSpline`) to start at all. Rejected with `PolicyViolation` before it ever reserves a resource or changes anything in the editor. A separate axis from the interactive command's own DefaultDenied capability (e.g. `PCGSplineDraw`): the capability states *what* may be touched, this flag states that taking over the human's viewport and input focus is allowed in the first place. Independently of this flag, starting one is also refused when nothing registered can currently show the human a prompt — see the `UAIP.Editor.PCG` section of the [Commands Reference](commands.md) |
| `AllowedCapabilities` | empty | DefaultDenied capabilities to grant (one `+` entry per line) |
| `DeniedCapabilities` | empty | Remove DefaultAllow capabilities from all sessions |
| `DeniedCommands` | empty | Block commands by fully-qualified name. Blocked commands are hidden from the default `ListCommands` response and counted in `HiddenReasons.DeniedCommand`; pass `IncludeUnavailable=true` to list them explicitly (`Available: false`, `UnavailableReason: "DeniedCommand"`), or use `DescribeCommand`, which always shows them |
| `AllowCapabilityReload` | `False` | Enable `UAIP.Core.ReloadCapabilities` for hot-reload of capability settings |

### ReadOnly and the editor lifecycle commands

What `ReadOnly` protects is **project data** — assets, levels, config files. Two commands are exempt from it and stay callable while `ReadOnly=True`: `UAIP.Editor.Workspace.ShutdownEditor` and `UAIP.Editor.Workspace.RestartEditor`. `ListCommands` and `DescribeCommand` report them as `Available: true` in that mode, matching what a dispatch actually does.

They are exempt because neither writes anything `ReadOnly` exists to protect; what they change is the lifetime of the editor process itself. Refusing them costs something that has nothing to do with safety: an editor launched with `ReadOnly=True` holds the policy in memory, so editing the ini back does not reach the running process, and with both lifecycle commands refused there is no supported way left to shut that editor down or restart it through UAIP at all.

The exemption removes the `ReadOnly` gate and nothing else:

- Both commands still require the `EditorLifecycle` capability, so `+DeniedCapabilities=EditorLifecycle` still takes them away from every session.
- `+DeniedCommands=UAIP.Editor.Workspace.ShutdownEditor` still blocks either of them by name. That is the switch to reach for when you want them gone but want the rest of `ReadOnly` left as it is.
- Their optional `SaveAll` is governed by `DisableSave`, not by `ReadOnly`, so `DisableSave=True` still stops them from writing packages to disk.

Every other mutating command is rejected under `ReadOnly` exactly as before. A handler has to declare the exemption for itself, it defaults to off, and no command other than these two declares it.

---

## Diagnosing errors

| ErrorCode | Diagnosis | Action |
|---|---|---|
| `CapabilityNotAvailable` | Process lacks the capability | Read the name from `ErrorMessage`; add it to `AllowedCapabilities` in the ini and restart (or call `ReloadCapabilities`) |
| `CapabilityNotAvailable` with a role name in `ErrorMessage` | The session's role denies this capability (Layer 1.5) | Nothing to enable — perform the operation from a session bound to a different role, or ask the operator to change the role's `DeniedCapabilities` and restart |
| `PolicyViolation: ... denied by SafetyPolicy` | SafetyPolicy ini flag is blocking | Set the corresponding flag to `True` in `[UAIP.SafetyPolicy]` and restart |
| `PolicyViolation: Scenario execution is not enabled` | Scenario route opt-in missing | Add `"enable_scenario": true` to `config.json` |
| `PolicyViolation: Command is denied` | Command is in `DeniedCommands` | Remove it from `DeniedCommands` in the ini |
| `CommandNotFound` for a 🧩 command | Optional plugin not enabled | Enable the required plugin in your `.uproject` and rebuild |

---

## Other ini sections

`[UAIP.SafetyPolicy]` is the only section covered on this page. The other ini sections (`[UAIP.Session]`, `[UAIP.ArtifactGC]`, `[UAIP.CommandNotification]`, `[UAIP.PythonExtension]`), along with every `-uaip-*` CLI launch flag and the MCP Bridge `config.json`, are documented in [Configuration](config.md).

**[English](../en/commands.md)** | [概要に戻る](overview.md)

# コマンドリファレンス

UAIP はドメイン別に整理された 200 以上のコマンドを提供します。コマンド名はすべて完全修飾名です（例：`UAIP.Editor.Assets.CreateAsset`）。

---

## コマンドの発見

コマンドを呼び出す前に、以下の 3 つの発見ツールを活用してください：

| ツール | 用途 |
|---|---|
| `uaip_query_capabilities` | 現在のセッションで利用可能な Capability を確認 |
| `uaip_list_commands` | 登録済みコマンドを一覧（`ProviderPrefix` でフィルター可能） |
| `uaip_describe_command` | 1 つのコマンドのパラメータスキーマと必要 Capability を確認 |

### よく使う発見パターン

```
# Editor 系コマンドを一覧
uaip_list_commands(ProviderPrefix="UAIP.Editor")

# 安定版のみ一覧
uaip_list_commands(ProviderPrefix="UAIP.Editor", Stability="Stable")

# 呼び出し前にパラメータを確認
uaip_describe_command(CommandName="UAIP.Editor.Assets.CreateAsset")
```

---

## Core コマンド

| コマンド | 説明 |
|---|---|
| `UAIP.Core.HealthCheck` | 接続が生きているか確認 |
| `UAIP.Core.ListCommands` | 登録済みコマンドを一覧 |
| `UAIP.Core.DescribeCommand` | コマンドの詳細を取得 |
| `UAIP.Core.QueryCapabilities` | 現在のセッションの Capability を取得 |
| `UAIP.Core.EndSession` | セッションを終了して Artifact を解放 |
| `UAIP.Core.ReloadCapabilities` | ini から Capability を再読み込み（`AllowCapabilityReload=True` が必要） |

---

## Editor ドメイン — `UAIP.Editor.*`

### Workspace

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.Workspace` | タブ管理、グラフエディタフォーカス、LiveCoding 起動、Undo-Redo、ShutdownEditor、RestartEditor |

### Assets

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.Assets` | CreateAsset、DeleteAsset、DuplicateAsset、OpenAsset、CloseAsset、SaveAll、SearchAssets、RenameAsset |

### Level

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.Level` | OpenLevel、PlaceActorInLevel、DeleteActor、SetActorTransform、ListLevelActors |

### Blueprint

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.Blueprint` | AddVariable、SetVariableDefault、AddFunction、AddGraphNode、ConnectPins、ListGraphNodes、DeleteNode、CompileBlueprint |

### Property

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.Property` | GetActorProperty、SetActorProperty |

### UMG

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.UMG` | AddWidget、SetWidgetProperty、ListWidgets |

### Material

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.Material` | AddMaterialNode、ConnectMaterialPins、SetMaterialProperty、ListMaterialNodes |

### Niagara

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.Niagara` | AddNiagaraModule、SetNiagaraParameter、ListNiagaraEmitters |

### Physics

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.Physics` | AddPhysicsBody、SetPhysicsConstraint、ListPhysicsBodies |

### Dataflow

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.Dataflow` | AddDataflowNode、ConnectDataflowPins、ListDataflowNodes |

### Skeleton

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.Skeleton` | ListBones、AddSocket、SetSocketTransform |

### Anim Blueprint

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.AnimBlueprint` | AddAnimNode、ConnectAnimPins、AddStateMachineState、AddStateMachineTransition |

### Behavior Tree

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.BehaviorTree` | AddBTNode、SetBTNodeProperty、AddBlackboardKey |

### EQS

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.EQS` | AddEQSGenerator、AddEQSTest、SetEQSTestProperty |

### MetaSound

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.MetaSound` | AddMetaSoundNode、ConnectMetaSoundPins、ListMetaSoundNodes |

### Sequencer

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.Sequencer` | AddTrack、AddSection、SetSectionRange、AddKeyframe、BindActor |

### StateTree

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.StateTree` | AddState、AddTransition、AddTask、SetStateProperty |

### ControlRig

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.ControlRig` | AddControl、SetControlTransform、AddRigVMNode、ConnectRigVMPins |

### Gameplay Tags

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.GameplayTags` | AddGameplayTag、RemoveGameplayTag、ListGameplayTags |

### Game Features

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.GameFeatures` | ListGameFeaturePlugins、ActivateGameFeaturePlugin、DeactivateGameFeaturePlugin |

### Enhanced Input

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.EnhancedInput` | AddInputAction、AddMappingContext、AddActionMapping |

### PCG

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.PCG` | AddPCGNode、ConnectPCGPins、ListPCGNodes |

### Observation（観測）

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.Observation` | CaptureActiveWindowImage、CaptureEditorTabImage、CaptureGraphViewportImage、CaptureCanonicalGraphImage、DumpEditorState、DumpSlateTree、DumpSelectionState |

### Execution（実行）

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.Execution` | RunAutomationTest、RunEditorPythonScript、RunEditorUtilityWidget |

### UI Automation（UI 操作）

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Editor.UIAutomation` | ClickWidget、FillForm、PressKey、WaitForWidget、InvokeContextMenuAction、FocusEditorTab |

---

## Runtime ドメイン — `UAIP.Runtime.*`

### PIE

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Runtime.PIE` | StartPIE、StopPIE、LoadMap |

### World

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Runtime.World` | SpawnActor、DestroyActor、TeleportActor、ExecuteConsoleCommand、ListWorldActors |

### Observation（観測）

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Runtime.Observation` | DumpWorldState、CaptureViewportImage、CapturePerformanceSnapshot、CheckpointCapture |

### GAS (Gameplay Ability System)

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Runtime.GAS` | GetAttributeValues、FindAttributeSetClasses、ListGrantedAbilities |

### Input（入力）

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Runtime.Input` | InjectInputKey、InjectEnhancedInputAction |

### Assertion（アサーション、シナリオ用プリミティブ）

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Runtime.Assertion` | WaitSeconds、WaitForCondition、AssertActorProperty、AssertWorldActorExists |

### Execution（実行）

| プロバイダー | カバー範囲 |
|---|---|
| `UAIP.Runtime.Execution` | RunGauntletTest、RunRuntimeAutomationTest |

---

## Toolset ブリッジ — `Toolset.*`

オプションの Toolset プラグインを有効にすると `Toolset.*` プレフィックスの追加コマンドが利用できます。すべての Toolset ブリッジコマンドには、Toolset プラグインなしでも動作する対応する `UAIP.*` ネイティブコマンドが存在します。

| プロバイダー | 必要なプラグイン |
|---|---|
| `Toolset.AutomationTest` | AutomationTestToolset プラグイン |
| `Toolset.SlateInspector` | SlateInspectorToolset プラグイン |
| `Toolset.AIModule` | AIModuleToolset プラグイン |
| `Toolset.AnimationAssistant` | AnimationAssistantToolset プラグイン |

---

## エラーコード

| エラーコード | 原因 | 対処 |
|---|---|---|
| `CommandNotFound` | コマンド名が間違っている | `uaip_list_commands` で正しい完全修飾名を確認 |
| `CapabilityNotAvailable` | セッションに必要な Capability がない | [Safety & Capabilities](safety.md) を参照 |
| `PolicyViolation` | SafetyPolicy による拒否またはオプトイン不足 | [Safety & Capabilities](safety.md) を参照 |
| `InvalidParams` | パラメータが不足または型が違う | `uaip_describe_command` でスキーマを再確認 |
| `NotFound` | アセット・アクターのパスが違う | パスや名前を確認 |
| `ExecutionFailed` | ランタイムエラー | パラメータを修正。シナリオでは `RetryCount` を使用 |
| `NotAllowed` | 禁止パスへの書き込みまたは PIE 中の編集 | パスやタイミングを見直す |
| `Timeout` | ステップが制限時間を超過 | 処理を分割するか `TimeoutSeconds` を増やす |

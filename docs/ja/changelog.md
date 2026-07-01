**[English](../en/changelog.md)** | [概要に戻る](overview.md)

# 更新履歴

UAIP プラグインのリリースごとの変更点をまとめたページです。各バージョン番号の意味（破壊的変更が含まれるかなど）については、まず冒頭の「バージョニング方針」を確認してください。

---

## バージョニング方針

UAIP は [Semantic Versioning 2.0.0](https://semver.org/lang/ja/) に従ってバージョニングを行います。

### バージョン番号の読み方

バージョン番号は `MAJOR.MINOR.PATCH` の 3 セグメント形式です。

| セグメント | 意味 |
|---|---|
| **MAJOR**（例: `1.x.x` → `2.x.x`）| 破壊的変更を含む。アップグレード時にコマンド名・パラメータ・設定ファイルの修正が必要になる可能性がある |
| **MINOR**（例: `1.0.x` → `1.1.x`）| 後方互換な機能追加。新コマンド・新 Capability・新オプションパラメータなど。既存呼び出しはそのまま動作する |
| **PATCH**（例: `1.0.0` → `1.0.1`）| バグ修正のみ。公開 API への影響なし |

### 現在のフェーズ：1.x.y（Fab 製品版公開済み）

現行バージョンは **1.0.0**（1.x.y 系列の初回エントリ）で、UAIP は **Fab で製品版として公開済み**（[リスティング](https://www.fab.com/listings/0eedf909-00ac-4d95-b109-8fda51800fff)）です。

- 以降は通常の SemVer ルールが厳格に適用されます。破壊的変更には MAJOR バンプ（`2.0.0` など）が必要
- 新コマンド・新 Capability 追加は MINOR バンプ（例: `1.0.x` → `1.1.0`）
- バグ修正は PATCH バンプ（例: `1.0.0` → `1.0.1`）

### 1.0 以前の履歴：0.x.y 系列

`0.9.0` / `0.9.1` は Fab 製品版リリース前に GitHub Releases で先行配布したデモ版バージョンです。エントリは履歴として下記に残しています。

### Pre-release タグ

通常は pre-release タグを使用しません。Fab 公開直前に最終確認版を配布する場合のみ、`1.0.0-rc.1` 形式の RC（リリース候補）タグを GitHub Releases に切る場合があります。RC は Fab 提出版と完全に同一のコードで、問題がなければそのまま `1.0.0` として正式公開します。

### Deprecation 方針（基本削除しない）

UAIP はエンジンバージョンごとにブランチを分けず、バージョンマクロで実装を切り替える方針を採用しています。そのため **一度公開したコマンドは原則として削除しません**。

- 廃止予定のコマンドは `Stability: "Deprecated"` に分類されますが、引き続き動作します
- `uaip_describe_command` で `DeprecationMessage` と `MigrationTarget`（推奨移行先）を確認できます
- 例外として、**Epic 社がエンジン側 API を削除し UAIP 側で実装維持が物理的に不可能になった場合** のみ、MAJOR バンプ時に削除を行います

これにより、AI エージェントに学習・記憶された古いコマンド名でも長期的に動作することを保証します。

### デモ版と製品版のバージョン番号

デモ版（GitHub Releases）と製品版（Fab）は **常に同じバージョン番号** を共有します。同一ソースから機能制限のみを切り替えてビルドしているため、HealthCheck コマンドの `UAIPVersion` フィールドも両者で同じ値を返します。

---

## リリース一覧

> **現在 `next` ブランチを閲覧中です。** このページは次回 Fab リリースに向けて開発中のコンテンツを追跡しています。最終リリース版は [`master` ブランチの更新履歴](https://github.com/Naotsun19B/UnrealAIIntegrationPlatform-Document/blob/master/docs/ja/changelog.md) を参照してください。

### Unreleased

プラグインリポジトリには取り込み済みですが、Fab 未リリースの変更です。

#### UAIP Plugin

**追加**

- **Editor Toolset ブリッジコマンド**（`UAIPEditorAssets`・`UAIPEditorLevel`・`UAIPEditorObservation`・`UAIPEditorWorkspace`・`UAIPEditorEngineManagement`・`UAIPRuntimePIE`・`UAIPRuntimeWorld` モジュール）: AI エージェントが UE 5.8 公式 Toolset フレームワーク（`EditorAppToolset` + `LogsToolset`）に委譲する Toolset ブリッジコマンド（`Toolset.*`）を呼び出せるようになりました。ブリッジコマンドは UE 5.8+ かつ対象 Toolset プラグインが有効な場合のみ利用可能で、古いバージョンでは `Available: false` になります。UAIP ネイティブコマンドは引き続き主要パスであり UE 5.7 でも動作します。あわせて 6 つのネイティブコマンドを追加しました：`GetVisibleActors`・`ProjectWorldToScreen`・`ProjectScreenToWorld`（`UAIP.Editor.Level`）、`CaptureViewportImageAnnotated`（`ViewportAnnotationCapture` 必須；`UAIP.Editor.Observation`）、`GetLogVerbosity` / `SetLogVerbosity`（`LogVerbosityEdit` 必須；`UAIP.Editor.Engine.Log`）。新 Capability `ViewportAnnotationCapture`（DefaultDenied）と `CVarInspect`（DefaultDenied；`Toolset.Editor.Toolset.World.SearchCVars` ブリッジをゲート）を追加しました。
- **PCG 拡張コマンドと Capability**（`UAIPEditorPCG` モジュール）: `UAIP.Editor.PCG` 配下に 20 コマンドを追加しました — アセット作成（`CreatePCGGraph`、`PCGGraphAssetCreate` 必須）、スキーマ / 説明 / パラメータ取得編集（`GetPCGGraphSchema`・`GetPCGGraphDescription`・`SetPCGGraphDescription`・`SetPCGGraphParams`・`RemovePCGGraphParams`）、インスタンス管理（`ListPCGGraphInstances`・`SpawnPCGGraphInstance`・`GetPCGGraphInstanceParams`・`SetPCGGraphInstanceParams`・`ResetPCGGraphInstanceParams`）、サブグラフ / ネイティブノード（`ListPCGAvailableSubgraphs`・`GetPCGNativeNodeSchema`・`AddPCGSubgraphNode`）、グラフ構造編集（`RepositionPCGNode`・`AddPCGCommentBox`・`UpdatePCGCommentBox`・`RemovePCGCommentBox`）、データビュー / 実行（`GetPCGNodeDataView`・`RunPCGInstantGraph`）。5 つの DefaultDenied Capability（`PCGGraphAssetCreate`・`PCGGraphExecute`・`PCGVolumeSpawn`・`PCGNodeInspect`・`PCGToolsetUnsafeNodeAdd`）を追加しました。`PCGVolumeSpawn` および `PCGToolsetUnsafeNodeAdd` は `DefaultUAIP.ini` の `AllowedCapabilities` に追記しないでください。`GetPCGNodeDataView` は `PCG_PROFILING_ENABLED=1` でビルドされた場合のみ有効です。また、UE 5.8 以上かつ `PCGToolset` プラグインが有効な環境では `Toolset.Editor.PCG.*` 配下に 31 のブリッジコマンドも利用できます（無効な環境では `Available: false`）。
- **プラグイン管理**（`UAIPRuntimeEngineManagement`・`UAIPEditorEngineManagement` モジュール）: AI エージェントがエディタを離れることなく UE プラグインの状態を確認・管理できるようになりました。エディタ / パッケージ版ビルド共通で使える読み取り専用コマンドを `UAIP.Runtime.Engine.Plugin` 配下に 5 本追加しました（`ListPlugins`・`GetPluginInfo`・`IsEnabled`・`GetPluginDependencies`・`GetPluginForAsset`）。エディタ専用コマンドを `UAIP.Editor.Engine.Plugin` 配下に 9 本追加しました — 観測系 5 本（`GetPluginDescriptor`・`GetPluginDependents`・`GetPluginTemplateDescriptions`・`IsPluginCreationAllowed`・`IsPluginModificationAllowed`）と変更系 4 本（`SetPluginEnabled`・`UpdatePluginDescriptor`・`AddPluginDependency`・`RemovePluginDependency`）。UE 5.8 以上かつ `PluginToolset` プラグインが有効な環境では `Toolset.Plugin.*` 配下に 15 のブリッジコマンドも利用できます（`ListEnabledPlugins`・`ListDiscoveredPlugins`・`GetPluginInfo`・`IsEnabled`・`GetPluginDependencies`・`GetPluginForAsset`・`GetPluginDescriptor`・`GetPluginDependents`・`GetPluginTemplateDescriptions`・`IsPluginCreationAllowed`・`IsPluginModificationAllowed`・`SetPluginEnabled`・`UpdatePluginDescriptor`・`AddPluginDependency`・`RemovePluginDependency`）。3 つの DefaultDenied Capability を追加しました：`PluginEnableToggle`（`SetPluginEnabled` をゲート）・`PluginDescriptorEdit`（`UpdatePluginDescriptor` をゲート）・`PluginDependencyEdit`（`AddPluginDependency` / `RemovePluginDependency` をゲート）。観測系コマンドは `EditorInspect` のみ必要です。`UAIP.Core.ListPlugins` は非推奨になりました；`UAIP.Runtime.Engine.Plugin.ListPlugins` を使用してください。
- **フォリッジ管理**（`UAIPEditorFoliage` モジュール）: AI エージェントがエディタでフォリッジタイプとインスタンスを管理できるようになりました。`UAIP.Editor.Foliage` 配下に 11 コマンドを追加しました — 観測系 4 コマンド（`ListFoliageTypes`・`GetFoliageTypeInfo`・`GetFoliageInstanceCount`・`GetFoliageInstances`、`EditorInspect` 必須、PIE 中でも実行可能）、フォリッジタイプ管理 3 コマンド（`AddFoliageTypeToLevel`・`RemoveFoliageTypeFromLevel`・`SetFoliageTypeSettings`、`FoliageTypeEdit` 必須）、インスタンス操作 4 コマンド（`AddFoliageInstances`・`RemoveFoliageInstances`・`DeleteAllFoliageInstances`・`ResimulateProceduralFoliage`、`FoliageInstanceEdit` または `FoliageBulkDelete` 必須）。インスタンス配置は World Partition 対応で、各インスタンスを正しい `AInstancedFoliageActor` セルにルーティングします。3 つの DefaultDenied Capability（`FoliageTypeEdit`・`FoliageInstanceEdit`・`FoliageBulkDelete`）を追加しました。
- **World Partition 編集**（`UAIPEditorWorldPartition` モジュール、**Pro 版限定** — デモ版では利用不可）: AI エージェントが World Partition ストリーミング・Data Layer・HLOD ワークフローを管理できるようになりました。`UAIP.Editor.WorldPartition` 配下に 34 コマンドを追加しました — World Partition 系 12 コマンド（`GetWorldPartitionInfo`・`GetWorldPartitionStreamingGrids`・`GetRuntimeGridSettings`・`SetRuntimeGridSettings`・`GetActorWorldPartitionSettings`・`SetActorIsSpatiallyLoaded`・`SetActorRuntimeGrid`・`SetWorldPartitionStreamingEnabled`・`PinActorInWorldPartition`・`UnpinActorFromWorldPartition`・`DumpWorldPartitionCells`・`ListExternalActors`）、Data Layer 系 15 コマンド（`ListDataLayers`・`GetDataLayerInfo`・`CreateDataLayerAsset`・`DeleteDataLayerAsset`・`CreateDataLayerInstance`・`DeleteDataLayerInstance`・`SetDataLayerType`・`SetDataLayerInitialRuntimeState`・`SetDataLayerIsLoadedInEditor`・`SetDataLayerVisibility`・`SetParentDataLayerInstance`・`GetActorDataLayers`・`AddActorToDataLayer`・`RemoveActorFromDataLayer`・`GetActorsInDataLayer`）、HLOD 系 7 コマンド（`ListHLODLayers`・`CreateHLODLayer`・`DeleteHLODs`・`SetActorHLODLayer`・`BuildHLODs`・`CancelHLODBuild`・`GetHLODBuildStatus`）。3 Capability（`WorldPartitionEdit`・`DataLayerEdit`・`HLODBuild`、いずれも DefaultDenied）を追加しました。観測系コマンドは World Partition が有効でないレベルでも `Success: true` + `IsWorldPartitionEnabled: false` を返します。
- **MVVM 編集**（`UAIPEditorMVVM` モジュール、**Pro 版限定** — `ModelViewViewModel` プラグイン必須、デモ版では利用不可）: AI エージェントが WidgetBlueprint の MVVM 設定（ViewModel の接続・バインディング・イベント・プロパティ）を操作できるようになりました。`UAIP.Editor.MVVM` 配下に 28 コマンドと 2 Capability（`ViewModelBindingEdit`、`ViewModelSourceEdit`、いずれも DefaultDenied）を追加しました。UE 5.8 以上かつ `MVVMToolset` プラグインが有効な環境では、`Toolset.MVVM.*` 配下に 9 つのブリッジコマンドも利用できます。
- **サウンドアセット編集**（`UAIPEditorSound` モジュール）: AI エージェントが `USoundClass` / `USoundAttenuation` / `USoundMix` アセットのプロパティを読み取り・設定できるようになりました。`UAIP.Editor.SoundSettings` 配下に 13 コマンドと 3 Capability（`SoundClassEdit`、`SoundAttenuationEdit`、`SoundMixEdit`、いずれも DefaultDenied）を追加しました。
- **Sandbox 編集統合**（`UAIPEditorSandbox` モジュール、**Pro 版限定** — `FileSandbox` プラグイン必須、デモ版では利用不可）: AI エージェントが FileSandbox セッションにアセット変更を仮置きし、人間が確認後にコミットまたはリバートできるようになりました。`UAIP.Editor.Sandbox` 配下に 6 コマンド（`BeginSandboxSession`、`EndSandboxSession`、`GetSandboxStatus`、`GetSandboxChanges`、`CommitSandboxChanges`、`RevertSandboxChanges`）と、4 Capability（`SandboxObserve`（DefaultAllow）、`SandboxSessionControl`、`SandboxPersist`、`SandboxRevert`（いずれも DefaultDenied））を追加しました。読み取り専用の observe 系コマンド（`GetSandboxStatus`・`GetSandboxChanges`）を含む全 6 コマンドが `FileSandbox` プラグインを必要とし、デモ版モジュールホワイトリストには含まれません。
- **セマンティックアセット検索**（`UAIPEditorAssets` モジュール — `SemanticSearch` プラグイン UE 5.8+ および OpenAI API キー必須）: AI エージェントが自然言語クエリでプロジェクトのアセットを検索・比較できるようになりました。`UAIP.Editor.SemanticSearch` 配下に 5 コマンド（`SearchAssetsSemantic`、`FindSimilarAssets`、`GetIndexStats`、`StartIndexing`、`CancelIndexing`）と 1 Capability（`SemanticSearchEdit`、DefaultDenied、インデックス再構築操作をゲート）を追加しました。UE 5.8 以上かつ `SemanticSearchToolset` プラグインが有効な環境では、`Toolset.Editor.SemanticSearch.*` 配下に 2 つのブリッジコマンド（`Search`、`FindSimilar`）も利用できます。なお、`SearchAssetsSemantic` および `FindSimilarAssets` はセマンティックインデックスが存在する場合にのみ動作します。検索コマンドを使用する前に `StartIndexing` を一度実行してください。
- **ConfigSettings コマンド**（`UAIPEditorEngineManagement` モジュール）: AI エージェントが `ISettingsModule` 経由でプロジェクト設定とエディタ設定を検査・変更できるようになりました。`UAIP.Editor.Engine.ConfigSettings` 配下に 8 コマンドを追加しました — `ListSettingsContainers`・`ListSettingsCategories`・`ListSettingsSections`（読み取り専用、Capability 不要）、`GetSettingsSchema`（プロパティ名・型・説明・デフォルト値・編集条件を JSON アーティファクトで返す；`EditorInspect` 必要）、`GetSettingsValues`（現在値を JSON アーティファクトで返す；シークレットフィールドは `***` でマスク；`EditorInspect` 必要）、`SetSettingsValues`（`Properties` マップを `ImportText` 経由でマージ；`DryRun` 対応；`ConfigSettingsEdit` 必要；PIE 中は実行不可）、`SaveSettings`（ini ファイルに書き出し；PIE 中および `bDisableSave` 設定時は実行不可；`ConfigSettingsSave` 必要）、`ResetSettingsToDefaults`（クラスデフォルトに戻す；PIE 中は実行不可；`ConfigSettingsReset` 必要）。書き込み操作はプロジェクトの `Config/` ディレクトリ配下のファイルのみ許可されます（エンジン ini ファイルは `PolicyViolation` で拒否）。さらに `UAIP.Runtime.Engine.Config` 配下に 2 コマンドを追加しました — `GetConfigValue`（raw ini キーの読み取り；Capability 不要）と `SetConfigValue`（raw ini キーの書き込み・削除；パッケージ版ビルドでは実行不可；ini インジェクション文字 `[`・`]` は拒否；`ConfigSettingsEdit` 必要）。3 つの DefaultDenied Capability を追加しました：`ConfigSettingsEdit`・`ConfigSettingsSave`・`ConfigSettingsReset`。

- **CVar 管理**（`UAIPRuntimeEngineManagement`・`UAIPEditorEngineManagement` モジュール）: AI エージェントがコンソール変数の読み取り・検索・設定・リセットを行えるようになりました。`UAIP.Runtime.Engine.CVar` 配下に 4 コマンドを追加しました — `GetConsoleVariable`（`RuntimeCVarRead` 必要）・`SearchConsoleVariables`（`RuntimeCVarRead` 必要）・`SetConsoleVariable`（`RuntimeCVarWrite` 必要）・`ResetConsoleVariable`（`RuntimeCVarWrite` 必要）。さらに Toolset ブリッジ `Toolset.Editor.Toolset.EngineManagement.SearchCVars`（`CVarInspect` 必要；UE 5.8+、EditorToolset プラグイン）を追加しました。新しい DefaultDenied Capability `RuntimeCVarWrite`（`SetConsoleVariable` / `ResetConsoleVariable` をゲート）を追加しました。機密パターン（`*password*`・`*token*`・`*secret*` 等）に一致する CVar は存在を隠蔽するため `NotFound` を返します。`ECVF_ReadOnly` の CVar は設定・リセット時に `NotAllowed` を返します。
- **ログエントリ取得**（`UAIPEditorEngineManagement`・`UAIPRuntimeEngineManagement` モジュール）: `UAIP.Editor.Engine.Log` 配下に `GetLogEntries`（エディタ Output Log から最近のエントリをパターンフィルタ付きで取得；Capability 不要）を追加しました。また `UAIP.Runtime.Engine.Log` 配下に `GetLogCategories`（登録済みログカテゴリ名をすべて一覧表示；Capability 不要）を追加しました。
- **`CreateAsset` 自己記述コマンド**（`UAIPEditorAssets` モジュール）: AI エージェントがエラーメッセージによる試行錯誤に頼らず、事前に `CreateAsset` の有効な入力値を確認できるようになりました。`UAIP.Editor.Assets` 配下に読み取り専用の2コマンドを追加しました — `ListCreatableAssetClasses`（作成可能な Factory を1つ以上持つ全 UClass を、Factory数とデフォルト Factory クラス名付きで返す；重い呼び出し、`EditorInspect` 必要）と `ListFactoriesForClass`（指定 `ClassName` に対応する Factory 候補を、各 `FactoryParams` の JSON Schema 付きで返す；`EditorInspect` 必要）。あわせて `ICreateAssetInterceptor::GetFactoryParamsSchema()` を追加し、`DataTable` と `StateTree` のアセット作成が必要とする `FactoryParams` キー（`RowStructPath`・`SchemaClass`）を自己記述するようになりました。

**変更**

- **`UAIP.Runtime.World.GetConsoleVariable` および `UAIP.Runtime.World.SearchConsoleVariables` 非推奨化**: 代わりに `UAIP.Runtime.Engine.CVar.GetConsoleVariable` および `UAIP.Runtime.Engine.CVar.SearchConsoleVariables` を使用してください。両コマンドは引き続き動作し、`Success: true` とともにレスポンスの `Data` に `DeprecationWarning` を返します。
- **`UAIP.Core.ListPlugins` 非推奨化**: 代わりに `UAIP.Runtime.Engine.Plugin.ListPlugins` を使用してください。元のコマンドは引き続き動作しますが、将来のリリースで削除される予定です。
- **Niagara モジュールが UE 5.7 に対応**: `UAIP.Editor.Niagara` および `UAIP.Runtime.Niagara` 配下の全コマンド（UAIP ネイティブ 36 本 + Toolset ブリッジ）が UE 5.7 で利用可能になりました。従来 UE 5.7 ではモジュール全体が未登録となり、全コマンドが `CommandNotFound` を返していました。
- **Niagara `default_value` が適用されるように**: `AddSetParametersModule` および `AddSetParameterEntry` で `default_value` フィールドが一般的な型（float / int / bool / `UScriptStruct`）について解析・適用されます。従来は指定値にかかわらず型のデフォルト値でエントリが作成されていました。
- **`AddSetParameterEntry` / `RemoveSetParameterEntry` に `script_name` が必須に** *(破壊的変更)*: 両コマンドに新しい `script_name` パラメータ（例：`Spawn` / `Update` / `Particle Spawn` / `Particle Update`）が必須追加されました。このパラメータは正しいスクリプトスタックへのルーティングと UE 5.8 External Edit API との互換性のために必要です。`script_name` なしの既存呼び出しは `InvalidParams` を返します。

**修正**

- **9つのEditorドメインモジュール（Foliage / WorldPartition / Level / PCG / Niagara / Sequencer / Property / Physics / UMG）でPIE/SIEミューテーションガードを共通化・修正**: 各モジュールに重複実装されていたPIE/SIE拒否ロジックとエディタワールド取得処理を単一の共通実装へ集約し、その過程で以下の潜在バグを修正しました:
  - `SetActorProperty` / `SetWorldSetting` には**PIE/SIEガードが一切存在せず**、Play-In-Editor または Simulate-In-Editor 中でもエディタワールドを変更できてしまう状態でした。`GetActorProperty` / `GetWorldSetting` は影響を受けず、引き続きPIE/Simulate中も成功します。
  - Niagara / Physics / UMG の各コマンドが使用するToolsetブリッジ用バリデーションヘルパーは、Play-In-Editorのみを検知し Simulate-In-Editor を検知できていませんでした。Simulate中のミューテーションがすり抜ける可能性がありました。
  - `SetActorTransform` / `PlaceActorInLevel` / `DeleteActorFromLevel`（Level）および WorldPartition / DataLayer / HLOD の各ミューテーションコマンドは、PIE/Simulate中の拒否時に `NotAllowed` ではなく `ExecutionFailed` を返していました *(このケースで `ExecutionFailed` をパターンマッチしている呼び出し元には破壊的変更)*。現在は他の全ドメインと同じ `NotAllowed` に統一されています。
  - `GetPCGGraphInfo` と `GetSequenceInfo` は引き続きPIE/Simulate状態をレスポンス内の単純なbool値として返し、Play/Simulate中もブロックされません。
- **`uaip_run_scenario` の `Variables` フィールドが `${Variables.<key>}` テンプレートで解決されるように**: シナリオに渡したトップレベルの `Variables` マップはパースされるものの、ステップ実行コンテキストに一度もロードされておらず、`${Variables.<key>}` を参照するステップは全トランスポート（HTTP / MCP / CLI / WS）で常に `ExecutionFailed: Template resolution failed.` になっていました。初期変数は最初のステップ実行前にロードされるようになり、第1ステップから型を保持したまま参照できます。また、シナリオあたりの変数件数上限または単一値のサイズ上限を超える `Variables` は、該当エントリをサイレントに破棄するのではなく `InvalidParams` として事前に拒否されるようになりました。
- **`SetConsoleVariable` / `ResetConsoleVariable` がデフォルトでチートフラグ（`ECVF_Cheat`）付き CVar への書き込みを拒否するように**: 従来は `ECVF_ReadOnly` のみがチェックされており、`RuntimeCVarWrite` を保有するセッションから `ECVF_Cheat` フラグの有無に関わらず CVar を書き換えられていました。新しい `AllowCheatCVarWrite` SafetyPolicy スイッチ（デフォルト `False`）がチートフラグ付き書き込みをゲートし、無効時は `PolicyViolation` を返します。`ECVF_ReadOnly` は引き続きチート判定より優先されます（`NotAllowed`）。書き込み成功時は Artifact とコマンド結果の両方に `WasCheatCVar` の bool 値が出力されるようになりました。

#### MCP Bridge 1.1.1 — 2026-06-24 リリース済み

**修正**

- **`uaip_max_major` の上限を撤廃** — `compatibility.json` の `uaip_max_major` を `null` に変更しました。これにより、ブリッジは `0.9.1` 以上のいかなる UAIP プラグインバージョン（2.x などの将来のメジャーバージョンを含む）にも接続できます。以前は上限値 `1` のせいで、実際の非互換性がなくてもプラグインのメジャーバージョンが上がるたびに新しいブリッジのリリースが必要でした。

---

#### MCP Bridge 1.1.0 — 2026-06-23 リリース済み

**追加**

- **`uaip_reload_config` ツール**: `config.json` を読み直し、起動パラメータ（`editor_path`・`uproject_path`・`http_port`・`enable_scenario`）に変更がある場合は実行中のエディタをシャットダウンして次回ツール呼び出し時に再起動をスケジュールします — MCP セッションを切断せずに実行可能です。オプション引数 `EditorPath` / `UProjectPath` を使うと、`config.json` に書き込まずに現セッション限りで値を上書きでき、MCP クライアントを再起動せずにエンジンバージョンの切り替えが可能です。
- **接続時のバージョン互換チェック**: 起動時に `compatibility.json` マニフェストと照合してプラグインバージョンを検証し、メジャーバージョン不一致の場合は `VersionIncompatibleError` を発生させます。開発環境では `UAIP_BRIDGE_SKIP_VERSION_CHECK=1` でスキップできます。

**修正**

- `uaip_reload_config` 経由で `enable_scenario`（またはその他の起動パラメータ）が変更されたとき、エディタが正しく再起動されるようになりました。従来は `importlib.reload()` が実行中エディタの確認より先に呼ばれていたため、enum の同一性チェックが失敗し再起動がサイレントにスキップされていました。
- エディタの起動・再起動前にクラッシュダイアログ（`WerFault.exe`、`CrashReportClient.exe`）を自動で終了するようになりました。Windows ではクラッシュダイアログがダイアログを閉じるまでプロジェクトの名前付き mutex を保持し続けるため、手動でダイアログを閉じるまで新しいエディタプロセスを起動できない問題がありました。

---

### UAIP Plugin 1.0.0 — 2026-06-18

**UAIP を Fab で製品版として公開しました。** [https://www.fab.com/listings/0eedf909-00ac-4d95-b109-8fda51800fff](https://www.fab.com/listings/0eedf909-00ac-4d95-b109-8fda51800fff)

[![YouTube でローンチトレーラーを見る](https://markdown-videos-api.jorgenkh.no/youtube/o-33jgYLF0A)](https://youtu.be/o-33jgYLF0A)

UAIP の最初の正式版リリースです。製品版（Pro）は Fab Code Plugin としてソース付きで配布され、デモ版のような機能ゲーティングや透かしなしで UAIP の全機能を提供します。デモ版は引き続き GitHub Releases で評価・非商用利用向けに提供します。

#### 製品版でデモ版から解放される機能

- **全 transport** — MCP に加えて HTTP / WebSocket / CLI を有効化
- **Editor 編集コマンド** — Blueprint / Level / Asset / Material / Niagara / Sequencer / AnimBlueprint / ControlRig / PCG / MetaSound / BehaviorTree / StateTree / Dataflow / EQS / CommonConversation / UMG / Physics / Skeleton / GameplayTags / GameFeatures / EnhancedInput
- **190+ Toolset ブリッジ** — UE 5.8 公式 Toolset API への対応で、総コマンド数は約 730 に到達
- **Runtime ワールド編集** — アクター Spawn、GAS 変更、Input 注入
- **`RunEditorPythonScript` による Python スクリプト実行**
- **キャプチャの透かしを削除**

#### 互換性

- UE 5.7 / 5.8 / Windows (Win64)
- 製品版（Pro）の配布は Fab 限定です。デモ版は引き続き本リポジトリの [Demo Releases](https://github.com/Naotsun19B/UnrealAIIntegrationPlatform-Document/releases?q=Demo) で提供
- MCP Bridge は独立バージョニングのまま `MCPBridge-v1.0.0` を継続使用（[Bridge Releases](https://github.com/Naotsun19B/UnrealAIIntegrationPlatform-Document/releases?q=MCPBridge)）

---

### UAIP Plugin 0.9.1 — 2026-06-18

Pro 版の Fab 提出に先立ち **Fab パッケージング規約に準拠** するため、MCP Bridge の配布形態を刷新したデモ版のフォローアップリリースです。本バージョンに含まれるその他のエンジン側改善は Pro 版向けの範疇であり、デモ版に対するユーザー可視な挙動変更はありません。

#### 変更

- **MCP Bridge をプラグインから分離** — Fab パッケージング規約に従い、プラグイン配布物に Python ツールチェインを同梱できないため、Bridge を本リポジトリの **独立した [Release](https://github.com/Naotsun19B/UnrealAIIntegrationPlatform-Document/releases?q=MCPBridge)**（`MCPBridge-v<X.Y.Z>` タグ）として、UE バージョン非依存・MIT ライセンス・デモ / Pro 共用で配布する形に変更しました。インストーラは Bridge を `<UAIP-parent>/UAIPMCPBridge/`（UAIP プラグインと同階層）にデプロイします。詳細は [接続方法 → MCP Bridge](connections.md#mcp-bridge) を参照。

---

### UAIP Plugin 0.9.0 — 2026-06-18

**デモ版を GitHub Releases で先行公開しました。** 製品版はその後 Fab で公開しています — 上記の [UAIP Plugin 1.0.0](#uaip-plugin-100--2026-06-18) エントリを参照してください。

#### 概要

UAIP の最初の公開バージョン（デモ版）です。SemVer 採用方針に基づき、製品版リリース前のフェーズを示す `0.x.y` 系列の初回バージョンとして `0.9.0` から開始します。

#### Added — デモ版に含まれる機能

- **MCP 接続** — Claude Code / Codex CLI / Cursor / Windsurf / GitHub Copilot などの MCP 対応 AI クライアントからエディタを操作
- **観測コマンド** — エディタ状態・ワールド状態・Slate ツリーの JSON ダンプ、各タブ・ビューポートのスクリーンショット取得
- **PIE 制御** — PIE 開始・停止、マップロード
- **アサーションコマンド** — アクタープロパティ・ワールド状態の検証
- **シナリオ実行** — 複数ステップを 1 リクエストで順序実行（中断・リトライ・タイムアウト設定可）
- **UI 自動化** — Slate ウィジェットへのクリック・キー入力・フォーム入力
- **拡張ポイント** — `ICommandProvider` / `ICommandHandler` 経由でのユーザー独自コマンド追加

#### デモ版で利用できない機能（製品版で提供予定）

- HTTP / WebSocket / CLI トランスポート（デモ版は MCP のみ利用可）
- エディタ編集系コマンド（Blueprint / Level / Asset / Material / Niagara など）
- Runtime ワールド編集（Spawn / GAS / Input 注入）
- Python スクリプト実行
- スクリーンショットへの透かしなし運用（デモ版は「UAIP Demo」透かしが合成される）

詳細は [デモ版ガイド](demo.md) を参照してください。

#### 既知の制限

- 対応プラットフォームは Windows (Win64) のみ
- 対応 UE バージョンは 5.7 / 5.8
- macOS / Linux 対応は将来検討項目（v1.0 では未対応）

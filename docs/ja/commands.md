**[English](../en/commands.md)** | [概要に戻る](overview.md)

# コマンドリファレンス

UAIP は 546 以上の **UAIP コマンド**（プラグイン本体が直接提供する独自実装）と、それを補強する 190 以上の **Toolset ブリッジコマンド**（UE 5.8 公式 Toolset への委譲レイヤー）の合計約 736+ をドメイン別に提供しています。コマンド名はすべて完全修飾名（例：`UAIP.Editor.Observation.CaptureActiveWindowImage`）です。本ページの表ではプロバイダプレフィックスを省略しているため、セクションヘッダーのプレフィックスを付けて使用してください。

## このリファレンスの使い方

- 各コマンドの完全なパラメータスキーマは `uaip_describe_command(CommandName="...")` で取得できます
- 実行時にドメインでフィルタするには `uaip_list_commands(ProviderPrefix="UAIP.Editor")` を使用します
- 各コマンドに必要な Capability については [Safety & Capabilities](safety.md) を参照してください

## 凡例

| 記号 | 意味 |
|---|---|
| 🆓 | デモバイナリで利用可能（製品版でも利用可能） |
| (記号なし) | 製品版限定コマンド |
| 🧩 | オプションプラグインが必要（プラグインが無効の場合は登録されません） |

## UAIP コマンドと Toolset ブリッジコマンド

UAIP では 2 種類のコマンドを公開しています：

- **UAIP コマンド**（`UAIP.*` プレフィックス）：プラグイン本体が直接提供する独自実装のコマンド。UE のバージョンや Toolset プラグインの有無に依存せず動作します。
- **Toolset ブリッジコマンド**（`Toolset.*` プレフィックス・UE 5.8+ かつ Toolset 系プラグイン導入時のみ）：UE 5.8 公式 Toolset フレームワークへの委譲レイヤー。多くは対応する UAIP コマンドのミラーで、Toolset 経由でしか提供されない機能を統一的に呼び出せるようにします。

本ページのドメインサマリでは件数のみを並べています。Toolset ブリッジコマンドの全名前を実行時に列挙したい場合は `uaip_list_commands(ProviderPrefix="Toolset")` を使ってください。

---

## ドメインサマリ

| ドメイン | プロバイダプレフィックス | UAIP コマンド | Toolset ブリッジ | デモ |
|---|---|---:|---:|---:|
| Core | `UAIP.Core` | 6 | — | ✅ |
| Editor Workspace | `UAIP.Editor.Workspace` | 18 | — | 一部（13/18） |
| Editor Observation | `UAIP.Editor.Observation` | 13 | — | ✅（1 件除外） |
| Editor Execution | `UAIP.Editor.Execution` | 5 | — | — |
| Editor UI Automation | `UAIP.Editor.UIAutomation` | 15 | — | ✅ |
| Editor Assets | `UAIP.Editor.Assets` | 10 | — | — |
| Editor Level | `UAIP.Editor.Level` | 13 | — | — |
| Editor Property | `UAIP.Editor.Property` | 13 | — | — |
| Editor Blueprint | `UAIP.Editor.Blueprint` | 20 | — | — |
| Editor UMG | `UAIP.Editor.UMG` | 22 | 13 | — |
| Editor Material | `UAIP.Editor.Material` | 11 | — | — |
| Editor GameplayTags | `UAIP.Editor.GameplayTags` | 7 | — | — |
| Editor GameFeatures 🧩 | `UAIP.Editor.GameFeatures` | 3 | — | — |
| Editor Niagara 🧩 | `UAIP.Editor.Niagara` | 36 | 45 | — |
| Editor Physics | `UAIP.Editor.Physics` | 31 | 17 | — |
| Editor Dataflow 🧩 | `UAIP.Editor.Dataflow` | 7 | — | — |
| Editor Skeleton | `UAIP.Editor.Skeleton` | 8 | — | — |
| Editor DataTable | `UAIP.Editor.DataTable` | 7 | — | — |
| Editor AnimBlueprint | `UAIP.Editor.AnimBlueprint` | 10 | — | — |
| Editor SoundCue | `UAIP.Editor.SoundCue` | 7 | — | — |
| Editor BehaviorTree | `UAIP.Editor.BehaviorTree` | 12 | — | — |
| Editor MetaSound 🧩 | `UAIP.Editor.MetaSound` | 9 | — | — |
| Editor EQS 🧩 | `UAIP.Editor.EQS` | 7 | — | — |
| Editor Sequencer | `UAIP.Editor.Sequencer` | 92 | 61 | — |
| Editor StateTree | `UAIP.Editor.StateTree` | 9 | — | — |
| Editor Curve | `UAIP.Editor.Curve` | 6 | — | — |
| Editor PCG 🧩 | `UAIP.Editor.PCG` | 13 | — | — |
| Editor WorldConditions 🧩 | `UAIP.Editor.WorldConditions` | 6 | — | — |
| Editor Conversation 🧩 | `UAIP.Editor.Conversation` | 12 | — | — |
| Editor ControlRig | `UAIP.Editor.ControlRig` | 59 | 44 | — |
| Editor EnhancedInput | `UAIP.Editor.EnhancedInput` | 13 | — | — |
| Editor GAS 🧩 | `UAIP.Editor.GAS` | 11 | 11 | — |
| Editor Python Extension 🧩 | `UAIP.Editor.PythonExtension` | 2 | — | — |
| Editor Sandbox 🧩 | `UAIP.Editor.Sandbox` | 6 | — | — |
| Runtime PIE | `UAIP.Runtime.PIE` | 12 | — | 一部（5/12） |
| Runtime Observation | `UAIP.Runtime.Observation` | 8 | — | ✅ |
| Runtime Execution | `UAIP.Runtime.Execution` | 3 | — | — |
| Runtime Assertion | `UAIP.Runtime.Assertion` | 4 | — | ✅ |
| Runtime Input | `UAIP.Runtime.Input` | 11 | — | — |
| Runtime GAS 🧩 | `UAIP.Runtime.GAS` | 6 | — | — |
| Runtime Niagara 🧩 | `UAIP.Runtime.Niagara` | 4 | 4 | — |

---

## UAIP.Core

検索・ヘルスチェック・セッション管理などのシステムレベルコマンド。

| コマンド | 説明 |
|---|---|
| 🆓 `HealthCheck` | プラグイン接続確認 — `Status`・`UAIPVersion`・`EngineVersion`・`BuildConfig` を返す |
| 🆓 `GetSystemInfo` | UE バージョン（Major/Minor/Patch/Changelist）・プロジェクト名・プラットフォーム・ビルド設定・UAIP バージョンを返す |
| 🆓 `QueryCapabilities` | セッションの Capability セットと `OperationalConstraints`（7 つのポリシーフラグ）を返す |
| 🆓 `ListCommands` | フィルタ付きコマンドカタログ（`GroupFilter`・`KeywordFilter`・`IncludeUnavailable`） |
| 🆓 `DescribeCommand` | 単一コマンドの完全メタデータ（スキーマ・必要 Capability・可用性） |
| 🆓 `ListCommandGroups` | 中間パス補完付きの全グループパス |

---

## UAIP.Editor.Workspace

エディタライフサイクル・タブ管理・グラフレイアウト・シェーダーコンパイル・Live Coding。

| コマンド | 説明 |
|---|---|
| 🆓 `FocusEditorTab` | 指定アセットのエディタタブを前面に出す |
| 🆓 `CloseEditorTab` | 指定アセットのエディタタブを閉じる |
| 🆓 `NormalizeEditorLayout` | メイングラフタブをフォーカスし、一時パネルを非表示にする |
| 🆓 `SetGraphZoom` | グラフビューポートのズーム倍率を設定 |
| 🆓 `FrameGraphAll` | グラフビューポートを全ノードが収まるようにズーム |
| 🆓 `FrameGraphSelection` | グラフビューポートを選択ノードが収まるようにズーム |
| 🆓 `SetGraphSelection` | ID リストでグラフノードを選択状態にする |
| 🆓 `ShutdownEditor` | UE Editor をシャットダウンする（任意でパッケージ保存） |
| 🆓 `RestartEditor` | UE Editor を再起動する（任意でパッケージ保存） |
| 🆓 `SaveAllPackages` | 変更済みパッケージをすべて保存（任意でマップを含む） |
| 🆓 `Undo` | 直前の Editor 操作を取り消す |
| 🆓 `Redo` | 取り消した操作をやり直す |
| 🆓 `GetLastCrashReport` | 最新のクラッシュレポートを取得 |
| `WaitForShaderCompilation` | シェーダーコンパイル完了まで待機 |
| `RecompileGlobalShaders` | 全グローバルシェーダーを強制再コンパイルし完了を待つ |
| `CompileLiveCoding` | Live Coding 再コンパイルをトリガー |
| `GetLiveCodingStatus` | 現在の Live Coding ステータスを取得 |
| `EnableLiveCodingForSession` | セッションに対して Live Coding を有効化 |

---

## UAIP.Editor.Observation

スクリーンショットとエディタ状態ダンプ（すべて読み取り専用）。

| コマンド | 説明 |
|---|---|
| 🆓 `CaptureActiveWindowImage` | アクティブな最上位ウィンドウのスクリーンショット（PNG Artifact） |
| 🆓 `CaptureEditorTabImage` | 指定エディタタブのウィジェット領域のスクリーンショット |
| 🆓 `CaptureGraphViewportImage` | SGraphEditor ビューポートのスクリーンショット |
| 🆓 `DumpEditorState` | アクティブタブ・開いているアセット・ウィンドウサイズ等（JSON） |
| 🆓 `DumpSelectionState` | 現在の選択状態 — アクター・オブジェクト・グラフノード（JSON） |
| 🆓 `DumpOpenTabs` | 開いているアセットエディタタブ一覧（JSON） |
| 🆓 `DumpOutputLog` | バッファリングされた Output Log（テキスト Artifact、行数・フィルタ対応） |
| 🆓 `DumpMessageLog` | Message Log エントリ（カテゴリフィルタ付き JSON Artifact） |
| 🆓 `DumpSlateTree` | Slate ウィジェットツリー（JSON、ルートパスフィルタ対応） |
| 🆓 `InspectMenu` | 指定パス配下のトップバーメニュー構造（ラベル・enabled・checked） |
| 🆓 `InspectContextMenu` | 指定対象のコンテキストメニュー項目（実行はしない） |
| 🆓 `ObserveWidget` | ウィジェットの Visibility / Enabled / Hovered / Focused 状態を時系列サンプリング |

---

## UAIP.Editor.Execution

テスト・Python スクリプト・Editor Utility Blueprint の実行。

| コマンド | 説明 |
|---|---|
| `RunAutomationTest` | UE Automation Test を名前で実行し Pass/Fail/Error レポートを返す |
| `RunAutomationSpec` | UE Automation Spec を名前で実行し Pass/Fail/Error レポートを返す |
| `RunEditorPythonScript` 🧩 | インライン Python スクリプトまたは `.py` ファイルを実行（`PythonScriptPlugin` 必須） |
| `RunEditorUtilityBlueprint` | 指定 Editor Utility Blueprint を実行 |
| `RunNamedEditorCommand` | `GUnrealEd->Exec` 経由で名前付き Editor コンソールコマンドを実行 |

---

## UAIP.Editor.UIAutomation

エディタ UI の操作 — クリック・入力・選択・ドラッグ。

| コマンド | 説明 |
|---|---|
| 🆓 `ClickWidget` | パスで識別したウィジェットへの左クリックをシミュレート |
| 🆓 `SelectMenuItem` | スラッシュ区切りのラベルパスでメニュー項目を選択 |
| 🆓 `InputText` | パスで識別したウィジェットにテキストを入力 |
| 🆓 `SetCheckboxState` | チェックボックスの状態を設定 |
| 🆓 `SetComboSelection` | コンボボックスでラベル指定の項目を選択 |
| 🆓 `DragGraphNode` | 指定グラフエディタタブでグラフノードをピクセル単位でドラッグ |
| 🆓 `ConnectGraphPins` | 指定グラフエディタタブで 2 つのピンを接続 |
| 🆓 `AcceptDialog` | アクティブなモーダルダイアログを承諾（OK/Yes/Accept をクリック） |
| 🆓 `CancelDialog` | アクティブなモーダルダイアログをキャンセル（Cancel/No をクリック） |
| 🆓 `InvokeContextMenuAction` | 指定対象を右クリックしてコンテキストメニューから項目を実行 |
| 🆓 `HoverWidget` | ウィジェットに OnMouseEnter をシミュレート |
| 🆓 `PressKey` | 修飾キー対応のキー入力をシミュレート（危険ショートカットブラックリスト付き） |
| 🆓 `WaitForWidget` | ウィジェットが期待状態になるまでポーリング |
| 🆓 `FillForm` | フォームウィジェットへの一括入力を逐次 state machine で実行 |
| 🆓 `SnapshotUI` | UI の構造スナップショットを取得 |

---

## UAIP.Editor.Assets

アセットの開閉・検索・作成・複製・リネーム・削除、フォルダ管理。

| コマンド | 説明 |
|---|---|
| `OpenAsset` | 指定アセットをエディタで開く |
| `CloseAsset` | 指定アセットの全エディタを閉じる |
| `SearchAssets` | パス・クラス・タグでアセットを検索 |
| `CreateAsset` | 指定クラスの新規アセットを作成 |
| `DuplicateAsset` | 既存アセットを複製 |
| `RenameAsset` | アセットをリネーム / 別パスへ移動 |
| `DeleteAsset` | アセットを削除 |
| `CreateFolder` | Content Browser に新規フォルダを作成 |
| `DeleteFolder` | 空フォルダを削除（空でない場合 `NotEmpty`） |
| `ForceDeleteFolder` | フォルダと配下アセットを一括削除（50 件上限・外部参照チェックなし） |

---

## UAIP.Editor.Level

Editor 上でのアクター配置・トランスフォーム・レベルロード。

| コマンド | 説明 |
|---|---|
| `ListLevelActors` | 開いているレベルのアクター一覧 |
| `PlaceActorInLevel` | Editor レベルにアクターを配置 |
| `DeleteActorFromLevel` | Editor レベルからアクターを削除 |
| `GetActorTransform` | Editor 上のアクターのトランスフォーム取得 |
| `SetActorTransform` | Editor 上のアクターのトランスフォーム設定 |
| `OpenLevel` | エディタビューポートでレベルを開く（File > Open Level） |
| `NewLevel` | テンプレートから新規レベルを作成（EmptyLevel / EmptyOpenWorld / Basic / OpenWorld） |
| `SelectActors` | 指定アクターを Editor レベルで選択（既存選択を置換または追加） |
| `ListSelectedActors` | 現在 Editor で選択中のアクター一覧を返す |
| `ClearSelection` | Editor レベルの選択をクリア |
| `FocusOnActors` | 指定アクターにビューポートカメラをフォーカス（アクター省略時は選択中のアクターを対象） |
| `GetCameraTransform` | アクティブなレベルエディタビューポートのカメラ位置・回転を取得 |
| `SetCameraTransform` | アクティブなレベルエディタビューポートのカメラ位置・回転を設定 |

---

## UAIP.Editor.Property

アクター・アセット・Blueprint デフォルト・DataTable 行・World / Project 設定のプロパティ読み書き。

| コマンド | 説明 |
|---|---|
| `GetActorProperty` | Editor アクターのプロパティ値を取得 |
| `SetActorProperty` | Editor アクターのプロパティを設定 |
| `GetWorldSetting` | WorldSettings のプロパティ値を取得 |
| `SetWorldSetting` | WorldSettings のプロパティを設定 |
| `GetAssetProperty` | アセット（DataAsset 等）のプロパティ値を取得 |
| `SetAssetProperty` | アセットのプロパティを設定し `MarkPackageDirty` を呼ぶ |
| `GetBlueprintDefault` | Blueprint CDO のプロパティ値を取得 |
| `SetBlueprintDefault` | Blueprint CDO のプロパティを設定 |
| `GetProjectSetting` | `UDeveloperSettings` CDO のプロパティ値を取得 |
| `SetProjectSetting` | `UDeveloperSettings` CDO のプロパティを設定し `SaveConfig()` を呼ぶ |
| `GetDataTableRow` | DataTable 行のプロパティ値を取得 |
| `SetDataTableRow` | DataTable 行のプロパティを設定 |
| `ListPlugins` | インストール済みプラグインと有効/無効状態の一覧（JSON） |

---

## UAIP.Editor.Blueprint

Blueprint 変数・イベントグラフノード・SCS コンポーネントの編集。

### 変数とグラフ（10）

| コマンド | 説明 |
|---|---|
| `AddBlueprintVariable` | Blueprint にメンバー変数を追加（型・デフォルト・Tooltip） |
| `DeleteBlueprintVariable` | メンバー変数を削除 |
| `SetBlueprintVariableDefault` | Blueprint 変数の CDO デフォルト値を更新 |
| `AddGraphNode` | Blueprint グラフにノードを追加（VariableGet/Set・FunctionCall・Event 等） |
| `DeleteGraphNode` | グラフノードを GUID 指定で削除（EntryNode・Tunnel は削除不可） |
| `ConnectBlueprintPins` | Blueprint グラフの 2 ピンを接続 |
| `DisconnectBlueprintPins` | ピン接続を切断 |
| `ListBlueprintPins` | Blueprint グラフノードのピン一覧 |
| `SetPinDefaultValue` | Blueprint グラフノードのピンにデフォルト値を設定（DefaultValue / DefaultObject / DefaultTextValue を型に応じて自動選択） |
| `GetPinDefaultValue` | Blueprint グラフノードのピンのデフォルト値を取得 |

### コンポーネント — SCS（8）

| コマンド | 説明 |
|---|---|
| `ListBlueprintComponents` | Blueprint から見える全コンポーネント一覧（SCS・Inherited・Native） |
| `AddBlueprintComponent` | Blueprint に新規 SCS コンポーネントノードを追加 |
| `DeleteBlueprintComponent` | SCS コンポーネントを削除 |
| `RenameBlueprintComponent` | SCS コンポーネントをリネーム |
| `ReparentBlueprintComponent` | SCS コンポーネントの親を変更 |
| `DuplicateBlueprintComponent` | SCS コンポーネントを複製 |
| `GetBlueprintComponentProperty` | SCS コンポーネントのプロパティ値を取得 |
| `SetBlueprintComponentProperty` | SCS コンポーネントのプロパティを設定 |

### コンパイル（2）

| コマンド | 説明 |
|---|---|
| `CompileBlueprint` | Blueprint をコンパイルし、CompileStatus + 構造化されたメッセージログを返す（AnimBlueprint・WidgetBlueprint は非対応） |
| `GetBlueprintCompileStatus` | コンパイルを実行せずに Blueprint の現在のコンパイル状態を取得する |

---

## UAIP.Editor.UMG

Widget Blueprint 編集 — ツリー・変数・アニメーション・バインディング。

### ネイティブ（22）

| コマンド | 説明 |
|---|---|
| `CreateWidgetBlueprint` | Widget Blueprint アセットを新規作成 |
| `AddWidget` | Widget Blueprint ツリーにウィジェットを追加 |
| `RemoveWidget` | ツリーからウィジェットを削除 |
| `MoveWidget` | ウィジェットを同一パネル内で並び替え / 別パネルへ移動 |
| `RenameWidget` | ウィジェットをリネーム |
| `SetWidgetAsVariable` | ウィジェットの `bIsVariable` フラグを切り替え |
| `SetNamedSlotContent` | NamedSlot ウィジェットの内容を設定 |
| `GetNamedSlots` | Widget Blueprint の NamedSlot 一覧 |
| `ReparentWidgetBlueprint` | Widget Blueprint の親クラスを変更 |
| `GetSlotProperties` | ウィジェットのスロットプロパティを取得（CPF フィルタ・最大 64 キー） |
| `SetSlotProperties` | ウィジェットのスロットプロパティを設定（32 KiB 制限・UObject 参照は `/Game/` 以下のみ） |
| `GetWidgets` | ウィジェットツリー構造を取得（JSON） |
| `ListWidgetClasses` | 利用可能なウィジェットクラス一覧（最大 500 件） |
| `CompileWidgetBlueprint` | Widget Blueprint をコンパイルしエラー / 警告を返す |
| `ListWidgetAnimations` | Widget Blueprint のアニメーション一覧 |
| `GetWidgetAnimationInfo` | アニメーションのトラック / キー情報 |
| `CreateWidgetAnimation` | 新規アニメーションを作成 |
| `AddAnimationTrack` | アニメーションにトラックを追加 |
| `ListPropertyBindings` | プロパティバインディング一覧 |
| `AddPropertyBinding` | プロパティバインディングを追加（同一 WBP 内関数/変数のみ） |
| `RemovePropertyBinding` | プロパティバインディングを削除 |
| `ExtractWidgetToUserWidget` | ウィジェットサブツリーを新規 UserWidget として抽出 |

### Toolset ブリッジ（13）🧩

`UMGToolSet` プラグイン経由でネイティブコマンドを委譲。プロバイダ：`Toolset.Editor.UMG.*`。UE 5.8+ と `UMGToolSet` プラグインが必要です。

---

## UAIP.Editor.Material

Material グラフ編集とパラメータ管理。

| コマンド | 説明 |
|---|---|
| `GetMaterialInfo` | 基本情報（NodeCount・ShadingModel・BlendMode・bHasErrors） |
| `ListMaterialNodes` | Material グラフのノード一覧（NodeId・ExpressionClass・座標・bIsParameter） |
| `AddMaterialNode` | Material グラフにノードを追加（ExpressionClass 指定・6 ステップ allowlist） |
| `DeleteMaterialNode` | NodeId 指定でノードを削除（ルート削除は Conflict） |
| `ConnectMaterialPins` | Material グラフの 2 ピンを接続（循環・型不一致検出） |
| `DisconnectMaterialPins` | ピン接続を切断 |
| `CompileMaterial` | マテリアルをコンパイルしエラー / 警告を返す |
| `SetMaterialParameterValue` | マテリアルパラメータの値を設定 |
| `GetMaterialParameterValue` | マテリアルパラメータの値を取得 |
| `ListMaterialExpressionClasses` | `UMaterialExpression` 派生クラスの一覧（最大 500 件）。`AddMaterialNode` の `ExpressionClass` 引数に使用する |
| `RefreshMaterial` | マテリアルを強制再コンパイル（保存済みアセットをパス省略で即時再ビルド） |

---

## UAIP.Editor.GameplayTags

プロジェクトタグテーブルの管理。

| コマンド | 説明 |
|---|---|
| `ListGameplayTags` | 全タグ一覧（ネイティブ含有・親タグ・ソースでフィルタ）— 最大 2048 件 |
| `GetGameplayTagInfo` | タグ詳細（Comment・Source・bIsNative・bIsRestrictedTag・親子関係） |
| `AddGameplayTag` | 通常タグを INI に追加 |
| `AddRestrictedGameplayTag` | Restricted タグを RestrictedTagList INI に追加 |
| `RemoveGameplayTag` | タグを INI から削除（子タグ / ネイティブタグ保護） |
| `RenameGameplayTag` | タグ名を変更（任意でアセット参照も更新） |
| `FindGameplayTagReferencers` | タグを参照するアセット一覧 |

---

## UAIP.Editor.GameFeatures 🧩

GameFeature Plugin 管理。`GameFeatures` + `GameFeaturesEditor` プラグインが必要です。

| コマンド | 説明 |
|---|---|
| `ListGameFeatures` 🧩 | GameFeature Plugin 一覧（filter_state：All / Installed / Mounted / Registered / Loaded / Active） |
| `GetGameFeatureInfo` 🧩 | GFP 詳細（State・Actions・依存関係） |
| `CreateGameFeaturePlugin` 🧩 | 新規 GameFeature Plugin のスキャフォールド（名前バリデーション付き） |

---

## UAIP.Editor.Niagara 🧩

Niagara VFX システム編集。`Niagara` + `NiagaraEditor` プラグインおよび **UE 5.7 以降**が必要です。

### ネイティブ（36）

#### 観測（13）

| コマンド | 説明 |
|---|---|
| `GetSystemTopology` 🧩 | Niagara システムのエミッター構造。**UE 5.8 制約:** `data` と `dynamic_input_children` はレスポンスに含まれず、`is_dynamic` フラグのみ出力される。解決済みの値が必要な場合は `GetStackInputData` を使用すること。 |
| `GetSystemCompileState` 🧩 | システムのコンパイル状態 |
| `GetAssetDiscoveryInfo` 🧩 | Niagara アセット探索情報 |
| `GetScriptAssets` 🧩 | Niagara スクリプトアセット一覧 |
| `GetNiagaraParameterCollections` 🧩 | Niagara パラメータコレクション一覧 |
| `GetUserVariables` 🧩 | システムのユーザー変数一覧 |
| `GetSystemInfo` 🧩 | システムの詳細情報（メタデータ含む） |
| `GetSystemData` 🧩 | システムのデータ構造 |
| `GetEmitterData` 🧩 | エミッターのデータ構造 |
| `GetRendererData` 🧩 | レンダラーのデータ構造 |
| `GetStackInputData` 🧩 | モジュールスタック入力値 |
| `UEnum_Info` 🧩 | UEnum 情報 |
| `GetAvailableNiagaraRendererClasses` 🧩 | `UNiagaraRendererProperties` 派生クラスの一覧（上限 200 件）。返された `ClassPath` を `AddRenderer` の `RendererClass` 引数として使用する。 |

#### 編集（21）

| コマンド | 説明 |
|---|---|
| `AddEmitter` 🧩 | Niagara システムにエミッターを追加 |
| `RemoveEmitter` 🧩 | エミッターを削除 |
| `DuplicateEmitter` 🧩 | エミッターを複製 |
| `SetEmitterEnabled` 🧩 | エミッターの有効/無効を切り替え |
| `SetEmitterName` 🧩 | エミッターの名前を変更 |
| `SetEmitterData` 🧩 | エミッターのデータを設定 |
| `AddRenderer` 🧩 | エミッターにレンダラーを追加 |
| `RemoveRenderer` 🧩 | レンダラーを削除 |
| `SetRendererData` 🧩 | レンダラーのデータを設定 |
| `AddModule` 🧩 | エミッターのモジュールスタックにモジュールを追加 |
| `RemoveModule` 🧩 | モジュールを削除 |
| `MoveModule` 🧩 | スタック内でモジュールを移動 |
| `SetModuleEnabled` 🧩 | モジュールの有効/無効を切り替え |
| `SetStackInputData` 🧩 | モジュールスタック入力値を設定 |
| `SetSystemData` 🧩 | システムのデータを設定 |
| `AddUserVariables` 🧩 | システムにユーザー変数を追加 |
| `RemoveUserVariables` 🧩 | ユーザー変数を削除 |
| `CompileNiagaraSystem` 🧩 | Niagara システムをコンパイル |
| `AddSetParametersModule` 🧩 | Set Parameters モジュールをスタックに追加し、初期パラメータエントリを登録する。`default_value` フィールドは一般的な型（float / int / bool / struct）で適用される。 |
| `AddSetParameterEntry` 🧩 | 既存の Set Parameters モジュールにパラメータエントリを追加する。`default_value` フィールドは一般的な型（float / int / bool / struct）で適用される。 |
| `RemoveSetParameterEntry` 🧩 | Set Parameters モジュールからパラメータエントリを削除する |

#### Blueprint ラッパー（2）

| コマンド | 説明 |
|---|---|
| `ConstructNiagaraBPWrapperFromSystem` 🧩 | NiagaraSystem アセットのユーザー変数を Blueprint 変数として持つ AActor BP ラッパーを生成する（Two-Phase Commit） |
| `ConstructNiagaraBPWrapperFromComponent` 🧩 | エディタワールド上のアクターの NiagaraComponent からコンポーネント変数オーバーライド値を保持した BP ラッパーを生成する（Two-Phase Commit） |

### Toolset ブリッジ（45）🧩

`NiagaraToolsets` プラグイン（UE 5.8+ Experimental）経由でネイティブコマンドを委譲。プロバイダ：`Toolset.Editor.Niagara.*`。グループ：Info（2）/ Blueprint（2）/ System Schema（12）/ Topology（5）/ Data（5）/ Edit-1（8）/ Edit-2（8）/ Diagnostic（3）。

---

## UAIP.Editor.Physics

Physics Asset 編集 — ボディ・シェイプ・コンストレイント。

### ネイティブ（31）

#### アセット / 観測（3）

| コマンド | 説明 |
|---|---|
| `CreatePhysicsAsset` | SkeletalMesh から Physics Asset を生成・リンク |
| `GetPhysicsAssetSummary` | ボディ数・コンストレイント数などのサマリ |
| `ValidatePhysicsAsset` | 孤立コンストレイント・形状なしボディなどの問題を検出 |

#### ボディ（15）

| コマンド | 説明 |
|---|---|
| `GetBodyNames` | Physics Asset のボディ名一覧 |
| `AddBody` | 指定ボーンにボディを追加 |
| `RemoveBody` | ボディを削除（関連コンストレイントも連鎖削除） |
| `GetBodyPhysicsMode` | ボディの PhysicsMode を取得（Default / Kinematic / Simulated） |
| `SetBodyPhysicsMode` | ボディの PhysicsMode を設定 |
| `SetAllBodiesPhysicsMode` | 名前パターンに一致する全ボディの PhysicsMode を一括設定 |
| `GetBodyMassScale` | ボディの MassScale を取得 |
| `SetBodyMassScale` | ボディの MassScale を設定 |
| `GetBodyCollisionProfile` | ボディの Collision Profile 名を取得 |
| `SetBodyCollisionProfile` | ボディの Collision Profile を設定 |
| `SetBodyLinearDamping` | ボディの Linear Damping を設定 |
| `SetBodyAngularDamping` | ボディの Angular Damping を設定 |
| `GetBodyOffset` | ボディの Center of Mass オフセット（COMNudge）を取得 |
| `SetBodyOffset` | ボディの Center of Mass オフセットを設定 |
| `MirrorBodies` | 命名規則に従い左右ボーンのボディ・形状をミラーコピー |

#### シェイプ（8）

| コマンド | 説明 |
|---|---|
| `GetBodyShapes` | 指定ボディのコリジョン形状一覧（ShapeName 付き） |
| `SetSphere` | 指定ボディのコリジョン形状を Sphere に設定 |
| `SetCapsule` | 指定ボディのコリジョン形状を Capsule に設定 |
| `SetBox` | 指定ボディのコリジョン形状を Box に設定 |
| `RemoveShape` | 指定 ShapeName の形状を削除 |
| `RegenerateBodyShapes` | ボーンのジオメトリから形状を自動再生成 |
| `CopyBodyShapes` | あるボーンの形状を別ボーンにコピー |
| `SetPhysicalMaterial` | ボディまたは全ボディに Physical Material を設定 |

#### コンストレイント（5）

| コマンド | 説明 |
|---|---|
| `GetConstraints` | アセット全コンストレイントを取得（上限 256 件） |
| `ListConstraintsForBody` | 特定ボーンに接続されているコンストレイント一覧（上限 256 件） |
| `AddConstraint` | 剛体コンストレイントを追加 |
| `SetConstraintLimits` | コンストレイントの角度制限を設定 |
| `RemoveConstraint` | コンストレイントを削除 |

### Toolset ブリッジ（17）🧩

`PhysicsToolsets` プラグイン（UE 5.8+ Experimental）経由でネイティブコマンドを委譲。プロバイダ：`Toolset.Editor.Physics.*`。

---

## UAIP.Editor.Dataflow 🧩

Dataflow グラフ編集。`DataflowEditor` プラグインが必要です。

| コマンド | 説明 |
|---|---|
| `GetDataflowGraphInfo` 🧩 | グラフのノード / エッジ / 変数を取得（JSON） |
| `ListDataflowNodeTypes` 🧩 | 利用可能な Dataflow ノードタイプ一覧 |
| `AddDataflowNode` 🧩 | Dataflow グラフにノードを追加 |
| `RemoveDataflowNode` 🧩 | Dataflow グラフからノードを削除 |
| `ConnectDataflowPins` 🧩 | 2 ピンを接続 |
| `DisconnectDataflowPins` 🧩 | ピン接続を切断 |
| `ListDataflowVariables` 🧩 | グラフ変数一覧 |

---

## UAIP.Editor.Skeleton

Skeleton と SkeletalMesh 編集。

| コマンド | 説明 |
|---|---|
| `GetSkeletonInfo` | USkeleton のボーン階層・ソケット・バーチャルボーン（JSON、読み取り専用） |
| `AddSocket` | 指定ボーンにソケットを追加 |
| `RemoveSocket` | ソケットを削除 |
| `SetSocketTransform` | ソケットのトランスフォームを部分更新（省略フィールドは既存値を保持） |
| `AddVirtualBone` | バーチャルボーンを追加（名前省略時は自動生成） |
| `RemoveVirtualBone` | バーチャルボーンを削除 |
| `GetSkeletalMeshInfo` | USkeletalMesh の LOD・マテリアルスロット・関連 Skeleton パス（読み取り専用） |
| `SetSkeletalMeshMaterial` | SkeletalMesh のマテリアルスロットにマテリアルを割り当て |

---

## UAIP.Editor.DataTable

DataTable 行の管理とインポート / エクスポート。

| コマンド | 説明 |
|---|---|
| `ListDataTableRows` | DataTable の行キー一覧 |
| `AddDataTableRow` | 新規行を追加 |
| `DeleteDataTableRow` | 行を削除 |
| `DuplicateDataTableRow` | 行を複製 |
| `ImportDataTableFromCSV` | CSV 文字列を一括インポート（Replace / Merge モード） |
| `ExportDataTableToCSV` | DataTable を CSV Artifact としてエクスポート |
| `GetDataTableRowStruct` | 行構造（UScriptStruct）フィールド定義を取得 |

---

## UAIP.Editor.AnimBlueprint

Anim Blueprint グラフと StateMachine 編集。

| コマンド | 説明 |
|---|---|
| `GetAnimBlueprintInfo` | AnimGraph ノード一覧と StateMachine 構造（PIE 中は degraded モード） |
| `AddAnimGraphNode` | `UAnimGraphNode_Base` 派生ノードを NodeClass 指定で追加 |
| `RemoveAnimGraphNode` | NodeId 指定でノードを削除 |
| `ConnectAnimGraphPins` | 2 ピンを接続（WouldCreateCycle DFS 事前検出） |
| `DisconnectAnimGraphPins` | ピン接続を切断 |
| `AddAnimState` | StateMachine に State を追加 |
| `RemoveAnimState` | NodeId 指定で State を削除 |
| `AddAnimTransition` | From→To Transition を追加（重複時 idempotent） |
| `RemoveAnimTransition` | NodeId 指定で Transition を削除 |
| `CompileAnimBlueprint` | コンパイルし CompileStatus + エラーログを返す |

---

## UAIP.Editor.SoundCue

SoundCue グラフ編集。

| コマンド | 説明 |
|---|---|
| `GetSoundCueInfo` | SoundCue グラフのノード一覧と接続トポロジー（JSON） |
| `AddSoundCueNode` | SoundNodeClass 指定でノードを追加（6 ステップ allowlist） |
| `RemoveSoundCueNode` | NodeId 指定でノードを削除（ルート削除は Conflict） |
| `ConnectSoundCuePins` | 2 ピンを接続（循環検出・動的入力ピン自動追加） |
| `DisconnectSoundCuePins` | ピン接続を切断（PinIndex=-1 で全切断） |
| `SetSoundCueNodeProperty` | SoundCue ノードのプロパティを設定（Object / Class / Delegate denylist） |
| `CompileSoundCue` | SoundNode ツリーをグラフから再構築 |

---

## UAIP.Editor.BehaviorTree

Behavior Tree グラフ編集と Blackboard キー管理。

| コマンド | 説明 |
|---|---|
| `GetBehaviorTreeInfo` | BT グラフのツリー構造（Composite / Task / Decorator / Service）を再帰 JSON で返す |
| `AddBehaviorTreeCompositeNode` | Composite ノードを追加（Sequence / Selector / SimpleParallel） |
| `AddBehaviorTreeTaskNode` | TaskClass 指定で Task ノードを追加 |
| `AddBehaviorTreeDecoratorNode` | 親ノードに Decorator を附加 |
| `AddBehaviorTreeServiceNode` | 親 Composite ノードに Service を附加 |
| `RemoveBehaviorTreeNode` | NodeId 指定でノードを削除 |
| `SetBehaviorTreeNodeProperty` | ノードプロパティを設定（FBlackboardKeySelector / 汎用 ImportText_Direct） |
| `ListBlackboardKeys` | Blackboard アセットのキー一覧（PIE 中も許可） |
| `AddBlackboardKey` | キーを追加（KeyType allowlist・重複名チェック） |
| `RemoveBlackboardKey` | 未参照のキーを削除（使用中は Conflict + 参照元を返す） |
| `SetBehaviorTreeBlackboard` | BT アセットの参照 Blackboard を変更 |
| `RequestBehaviorTreeAutoArrange` | 開いている BT エディタで AutoArrange パスを実行 |

---

## UAIP.Editor.MetaSound 🧩

MetaSound グラフ編集。`Metasound` プラグインが必要です。

| コマンド | 説明 |
|---|---|
| `GetMetaSoundInfo` 🧩 | MetaSoundSource / MetaSoundPatch のグラフトポロジー（ノード一覧・接続・I/O 頂点） |
| `AddMetaSoundNode` 🧩 | `Namespace::Name` 形式でノードを追加（MajorVersion 対応・5 ステップ Policy） |
| `RemoveMetaSoundNode` 🧩 | NodeId 指定でノードを削除 |
| `ConnectMetaSoundPins` 🧩 | 2 ピンを接続（重複時 idempotent フラグ付き） |
| `DisconnectMetaSoundPins` 🧩 | ピン接続を切断 |
| `AddMetaSoundInput` 🧩 | 入力頂点を追加（単一ページアセットのみ） |
| `AddMetaSoundOutput` 🧩 | 出力頂点を追加（単一ページアセットのみ） |
| `SetMetaSoundNodeProperty` 🧩 | 入力デフォルト値を設定（Bool / Int / Float / String、NaN / Inf 拒否） |
| `CompileMetaSound` 🧩 | Frontend に登録（セッション単位 1 秒レートリミット） |

---

## UAIP.Editor.EQS 🧩

EQS クエリ編集。`EnvironmentQueryEditor` プラグインが必要です。

| コマンド | 説明 |
|---|---|
| `GetEQSQueryInfo` 🧩 | EQS Generator Option / Test 構造（PIE 中は degraded モード） |
| `AddEQSGenerator` 🧩 | Generator Option を追加（GeneratorClass・6 ステップ allowlist） |
| `RemoveEQSGenerator` 🧩 | NodeId 指定で Generator Option を削除（配下 Test も一括削除） |
| `AddEQSTest` 🧩 | Generator Option に Test を追加 |
| `RemoveEQSTest` 🧩 | NodeId 指定で Test を削除 |
| `SetEQSGeneratorProperty` 🧩 | Generator プロパティを設定（汎用 ImportText_Direct） |
| `SetEQSTestProperty` 🧩 | Test プロパティを設定（`param:<Name>` → `UAIDataProvider_QueryParams`） |

---

## UAIP.Editor.Sequencer

LevelSequence 編集 — トラック・セクション・キーフレーム・再生・バインド。

### ネイティブ（92）

#### 構造（15）

| コマンド | 説明 |
|---|---|
| `AddTrack` | LevelSequence にトラックを追加（TrackClass 指定） |
| `RemoveTrack` | TrackClass / BindingGuid 指定でトラックを削除 |
| `AddSection` | トラックにセクションを追加（StartFrame / EndFrame は DisplayRate 基準） |
| `RemoveSection` | SectionIndex 指定でセクションを削除 |
| `SetPlaybackRange` | 再生範囲を設定 |
| `FlushSequencerChanges` | 蓄積した変更通知を一括 Flush |
| `GetAvailableSequencerTrackClasses` | 利用可能なトラッククラス一覧 |
| `SetSectionRange` | セクションのフレーム範囲を変更 |
| `DuplicateSection` | セクションを複製 |
| `MoveSection` | セクションを指定フレーム数オフセットで移動 |
| `AddCameraCut` | CameraCutTrack にカメラカットセクションを追加 |
| `SetTrackEnabled` | トラックの有効/無効を切り替え |
| `IsTrackEnabled` | トラックの有効状態を取得 |
| `SetSectionActive` | セクションのアクティブ状態を切り替え |
| `IsSectionActive` | セクションのアクティブ状態を取得 |

#### キーフレーム（7）

| コマンド | 説明 |
|---|---|
| `AddKeyframe` | チャンネルにキーフレームを追加 |
| `RemoveKeyframe` | FrameNumber 指定でキーフレームを削除 |
| `SetKeyframeValue` | キーフレームの値を更新 |
| `SetKeyframeInterpolation` | キーフレームの補間モードを変更 |
| `SetKeyframeTangents` | キーフレームの接線を設定 |
| `OffsetKeyframes` | チャンネルの全キーフレームを時間オフセットで一括移動 |
| `GetKeyframeTangents` | キーフレームの接線を取得（arrive / leave） |

#### バインド（4）

| コマンド | 説明 |
|---|---|
| `BindActor` | Editor World のアクターを Possessable としてバインド |
| `UnbindActor` | BindingGuid 指定でアクターバインドを削除 |
| `GetActorBindingGuid` | アクター名から BindingGuid を逆引き |
| `GetBoundActors` | BindingGuid に対応するアクター一覧 |

#### 観測（12）

| コマンド | 説明 |
|---|---|
| `GetSequenceInfo` | トラック / セクション / チャンネル / バインド / DisplayRate / 再生範囲 |
| `GetBindings` | Possessable バインド一覧（GUID・名前・クラス） |
| `GetTracks` | 指定 BindingGuid のトラック一覧 |
| `GetSections` | トラックのセクション一覧（フレーム範囲付き） |
| `GetDisplayRate` | LevelSequence の DisplayRate |
| `GetTickResolution` | LevelSequence の TickResolution |
| `GetPlaybackRange` | 現在の再生範囲 |
| `GetKeyframes` | チャンネルのキーフレーム一覧（時刻・値・補間） |
| `ValidateSequenceBindings` | 全バインドの有効性を検証（アクター存在・型一致） |
| `GetCameraCutSections` | CameraCutTrack のセクション一覧 |
| `GetCurrentSequence` | 開いている ULevelSequence |
| `GetFocusedSequence` | フォーカス中 Sequencer の ULevelSequence |

#### 再生（10）

| コマンド | 説明 |
|---|---|
| `Play` | Sequencer 再生を開始 |
| `Pause` | 再生を一時停止 |
| `IsPlaying` | 再生中かどうか |
| `SetPlayheadFrame` | 再生ヘッドを指定フレームに移動 |
| `GetPlayheadFrame` | 現在の再生ヘッド位置 |
| `SetPlaybackSpeed` | 再生速度倍率を設定 |
| `GetPlaybackSpeed` | 現在の再生速度倍率 |
| `SetLoopMode` | ループモードを設定（NoLoop / Loop / LoopExactly） |
| `GetLoopMode` | 現在のループモード |
| `ForceEvaluate` | 現在フレームを強制再評価 |

#### セクションプロパティ（4）

| コマンド | 説明 |
|---|---|
| `GetSectionProperty` | UMovieSceneSection のプロパティ値を取得 |
| `SetSectionProperty` | UMovieSceneSection のプロパティを設定 |
| `GetSectionWeight` | セクションの重みを取得 |
| `SetSectionWeight` | セクションの重みを設定 |

#### UI / 状態（10）

| コマンド | 説明 |
|---|---|
| `SetCameraLock` | カメラロック状態を切り替え |
| `IsCameraLockActive` | カメラロック状態を取得 |
| `GetSelectionRange` | 選択範囲を取得 |
| `SetSelectionRange` | 選択範囲を設定 |
| `ClearSelection` | 選択範囲をクリア |
| `GetTrackFilterNames` | 利用可能なトラックフィルター名一覧 |
| `IsTrackFilterActive` | 指定フィルターの有効状態 |
| `SetTrackFilterActive` | 指定フィルターの有効状態を切り替え |
| `SetLocked` | シーケンスのロック状態を切り替え |
| `IsLocked` | ロック状態を取得 |

#### シーケンスプロパティ（6）

| コマンド | 説明 |
|---|---|
| `SetDisplayRate` | LevelSequence の DisplayRate を変更 |
| `GetViewRange` | Sequencer タイムラインのビュー範囲 |
| `SetViewRange` | ビュー範囲を設定 |
| `GetWorkRange` | ワーク範囲 |
| `SetWorkRange` | ワーク範囲を設定 |
| `SetTickResolution` | TickResolution を変更（既存キーフレーム有無を Warning で通知） |

#### マークフレーム（5）

| コマンド | 説明 |
|---|---|
| `AddMarkedFrame` | マークフレームをラベル付きで追加 |
| `GetMarkedFrames` | 全マークフレーム一覧 |
| `DeleteMarkedFrame` | インデックス指定でマークフレームを削除 |
| `DeleteAllMarkedFrames` | 全マークフレームを削除 |
| `FindMarkedFrameByLabel` | ラベル指定でマークフレームを検索 |

#### サブシーケンス（2）

| コマンド | 説明 |
|---|---|
| `GetSubSequences` | SubSequence トラックのセクション一覧 |
| `AddSubSequenceTrack` | SubSequence トラックを追加 |

#### AnimMixer（17、オプショナル `MovieSceneAnimMixer`）

| コマンド | 説明 |
|---|---|
| `GetAnimMixerTrackInfo` | AnimMixer トラック情報を取得 |
| `GetLayerBlendWeight` | レイヤーのブレンドウェイトを取得 |
| `SetLayerBlendWeight` | レイヤーのブレンドウェイトを設定 |
| `IsLayerMuted` | レイヤーのミュート状態を取得 |
| `SetLayerMuted` | レイヤーのミュート状態を切り替え |
| `IsLayerEnabled` | レイヤーの有効状態を取得 |
| `SetLayerEnabled` | レイヤーの有効状態を切り替え |
| `ClearMixerLayer` | レイヤーの全セクションを削除 |
| `AddMixerLayer` | AnimMixer レイヤーを追加 |
| `RemoveMixerLayer` | AnimMixer レイヤーを削除 |
| `MoveMixerLayer` | AnimMixer レイヤーを移動 |
| `AddMixerSection` | AnimMixer セクションを追加 |
| `RemoveMixerSection` | AnimMixer セクションを削除 |
| `SetMixerSectionRange` | AnimMixer セクションのフレーム範囲を設定（生 FFrameNumber Tick 単位） |
| `SetMixerSectionAnimation` | AnimMixer セクションのアニメーションを設定 |
| `AddMixerTransition` | Transition を追加 |
| `RemoveMixerTransition` | Transition を削除 |
| `GetMixerSectionInfo` | AnimMixer セクション情報を取得 |

### Toolset ブリッジ（61）🧩

プロバイダ：`Toolset.AnimationAssistant.*`（41 件 — Lifecycle 6・Playback 10・Property 9・MarkedFrame 5・UI 11）と `Toolset.SequencerAnimMixer.*`（20 件 — Layers 10・Transitions 5・Decorations 5）。UE 5.8+ が必要。

---

## UAIP.Editor.StateTree

StateTree 編集。

| コマンド | 説明 |
|---|---|
| `GetStateTreeInfo` | State ツリー・Task 一覧・Transition 一覧・Schema 情報（PIE 中は degraded モード） |
| `AddState` | State を追加（State / Group / Subtree / Linked / LinkedAsset の 5 種類） |
| `RemoveState` | StateId 指定で State を削除（子 State 再帰削除） |
| `AddStateTask` | State に Task を追加（8 ステップ allowlist） |
| `RemoveStateTask` | TaskId 指定で Task を削除 |
| `AddStateTransition` | Transition を追加（Succeeded / Failed / NextState / NextSelectableState / GotoState） |
| `RemoveStateTransition` | TransitionId 指定で Transition を削除 |
| `SetStateNodeProperty` | Task ノードのプロパティを設定（汎用 ImportText_Direct） |
| `CompileStateTree` | StateTree をコンパイル（セッション単位 1 秒レートリミット） |

---

## UAIP.Editor.Curve

Curve アセット（UCurveFloat / UCurveVector / UCurveLinearColor）のキー編集。

| コマンド | 説明 |
|---|---|
| `GetCurveInfo` | チャンネル一覧・キー・前後外挿（per-channel truncated フラグ付き） |
| `AddCurveKey` | 指定チャンネルにキーを追加 |
| `RemoveCurveKey` | time + tolerance でキーを削除 |
| `SetCurveKeyValue` | 既存キーの値と時刻を更新 |
| `SetCurveKeyInterpolation` | 既存キーの補間モードを変更（Constant / Linear / Cubic / None） |
| `SetCurveKeyTangent` | arrive / leave 接線を設定（非 Cubic キーは自動 Cubic 昇格・`promoted_to_cubic` フラグ通知） |

---

## UAIP.Editor.PCG 🧩

PCG グラフ編集。`PCG` プラグインが必要です。

| コマンド | 説明 |
|---|---|
| `GetPCGGraphInfo` 🧩 | UPCGGraph のノード / エッジ / パラメータ（PIE 中は degraded モード） |
| `ListPCGNodeTypes` 🧩 | allowlist 通過 UPCGSettings サブクラス一覧 |
| `AddPCGNode` 🧩 | SettingsClassPath 指定でノードを追加（NodePath を返す） |
| `RemovePCGNode` 🧩 | NodePath 指定でノードを削除（接続エッジも同時削除） |
| `ConnectPCGPins` 🧩 | NodePath + PinLabel でピンを接続 |
| `DisconnectPCGPins` 🧩 | ピン切断（特定ペア / 出力ピンからの全切断） |
| `SetPCGNodeProperty` 🧩 | UPCGSettings EditAnywhere プロパティを設定（複合型は拒否） |
| `ExecutePCGGraph` 🧩 | `UPCGComponent::Generate` を起動 |
| `ListCustomPCGNodeTypes` 🧩 | C++ / Blueprint カスタム PCG ノードタイプ一覧 |
| `GetCustomPCGNodeSchema` 🧩 | C++ UPCGSettings サブクラスの EditAnywhere プロパティを JSON スキーマで返す |
| `GetCustomBlueprintPCGNodeSchema` 🧩 | Blueprint UPCGBlueprintSettings サブクラスのプロパティを JSON スキーマで返す |
| `SetCustomCppPCGNodeProperty` 🧩 | C++ カスタムノードのプロパティを書き換え（`RecompileTriggered` フラグ） |
| `SetCustomBlueprintPCGNodeProperty` 🧩 | BP カスタムノードのプロパティを書き換え（Class CDO / Instance の 2 モード） |

---

## UAIP.Editor.WorldConditions 🧩

WorldConditions 編集。`WorldConditions` プラグインが必要です。

| コマンド | 説明 |
|---|---|
| `GetWorldConditionInfo` 🧩 | 条件セット構造（Operator / Depth / プロパティ） |
| `AddWorldCondition` 🧩 | 条件を追加（`InsertAtIndex=-1` で末尾追加） |
| `RemoveWorldCondition` 🧩 | インデックス指定で条件を削除 |
| `SetWorldConditionProperty` 🧩 | 条件 USTRUCT のプロパティを設定（ImportText 値文字列） |
| `SetWorldConditionOperator` 🧩 | Operator（And / Or）と bInvert を設定（Index 0 は Copy 固定） |
| `SetWorldConditionExpressionDepth` 🧩 | ExpressionDepth（0–4）を設定 |

---

## UAIP.Editor.Conversation 🧩

ConversationDB グラフ編集。`CommonConversation` プラグインが必要です。

| コマンド | 説明 |
|---|---|
| `ListConversationEntryPoints` 🧩 | エントリポイント一覧 |
| `ListConversationSpeakers` 🧩 | 話者一覧 |
| `ListConversationNodes` 🧩 | 全ノード一覧（refPath 付き） |
| `GetConversationNodeConnections` 🧩 | ノードの接続情報 |
| `ListConversationNodeSubNodes` 🧩 | ノードの SubNode 一覧 |
| `ListConversationNodeTypes` 🧩 | 位置別の許可ノードクラス一覧（最大 256 件） |
| `AddConversationNode` 🧩 | トップレベルノードを追加（`UConversationNodeWithLinks` 派生） |
| `AddConversationSubNode` 🧩 | 親 Task ノードに SubNode を附加 |
| `RemoveConversationNode` 🧩 | NodeGuid 指定でノードを削除 |
| `ConnectConversationNodes` 🧩 | ノード間の遷移エッジを追加 |
| `DisconnectConversationNodes` 🧩 | 遷移エッジを削除 |
| `SetConversationNodeProperty` 🧩 | プロパティを設定（FText は BIDI strip・PUA reject・4096 文字上限） |

---

## UAIP.Editor.ControlRig

ControlRig ヒエラルキーと RigVM グラフ編集。

### ネイティブ（59）

#### ヒエラルキー観測（10）

| コマンド | 説明 |
|---|---|
| `GetElements` | ヒエラルキー全要素一覧 |
| `GetAllBones` | 全ボーン一覧 |
| `GetAllNulls` | 全 Null 要素一覧 |
| `GetAllControls` | 全 Control 要素一覧 |
| `GetGlobalTransform` | 要素のグローバルトランスフォーム |
| `GetLocalTransform` | 要素のローカルトランスフォーム |
| `GetParent` | 要素の親要素 |
| `GetChildren` | 要素の子要素一覧 |
| `GetModuleInstances` | ModularRig のモジュールインスタンス一覧 |
| `GetControlSettings` | Control の `FRigControlSettings`（Gizmo・Limits） |

#### ヒエラルキー編集（11）

| コマンド | 説明 |
|---|---|
| `AddElement` | 汎用要素を追加（ElementType 指定） |
| `AddBone` | ボーンを追加 |
| `AddNull` | Null 要素を追加 |
| `AddControl` | Control 要素を追加（ControlType allowlist） |
| `RemoveElement` | 要素を削除 |
| `RemoveBone` | ボーンを削除 |
| `RemoveNull` | Null 要素を削除 |
| `RemoveControl` | Control 要素を削除 |
| `ReparentElement` | 要素の親を変更（MaintainGlobalTransform オプション） |
| `SetControlOffset` | Control の Initial ローカル変換を設定 |
| `SetControlSettings` | Control の `FRigControlSettings` を設定 |

#### トランスフォーム（3）

| コマンド | 説明 |
|---|---|
| `SetGlobalTransform` | 要素のグローバルトランスフォームを設定 |
| `SetLocalTransform` | 要素のローカルトランスフォームを設定 |
| `ImportBonesFromAsset` | SkeletalMesh / Skeleton アセットからボーン階層をインポート |

#### グラフ管理（11）

| コマンド | 説明 |
|---|---|
| `ListGraphs` | 全 RigVM グラフ一覧 |
| `GetGraph` | 指定グラフ情報 |
| `AddGraph` | カスタムグラフを追加 |
| `DeleteGraph` | カスタムグラフを削除（組み込みグラフは拒否） |
| `GetForwardSolveGraph` | ForwardSolve グラフを取得 |
| `GetBackwardSolveGraph` | BackwardSolve グラフを取得 |
| `GetInteractionGraph` | Interaction グラフを取得 |
| `GetEventGraph` | 指定イベントのグラフを取得 |
| `AddEventGraph` | イベントグラフを追加 |
| `AddBackwardSolveGraph` | BackwardSolve グラフを追加 |
| `AddInteractionGraph` | Interaction グラフを追加 |

#### ノード（10）

| コマンド | 説明 |
|---|---|
| `AddGraphNode` | RigVM グラフにノードを追加（StructPath + SolveEventName） |
| `RemoveGraphNode` | NodeName 指定でノードを削除 |
| `ListNodes` | グラフのノード一覧 |
| `GetNodeInfo` | ノードの StructPath・ピン型・メタデータ |
| `FindNodes` | StructPath / NamePattern 指定でノードを検索 |
| `GetNodePosition` | ノードのグラフ上の位置 |
| `SetNodePosition` | ノードの位置を設定 |
| `DuplicateNode` | ノードを複製（複製後の名前を返す） |
| `AddEventNode` | イベントノードを追加 |
| `AddVariableNode` | 変数ノードを追加 |

#### ピン（7）

| コマンド | 説明 |
|---|---|
| `ListPins` | ノードのピン一覧 |
| `GetPinValue` | ピンの値を取得 |
| `SetPinValue` | ピンの値を設定 |
| `ResetPinValue` | ピン値をデフォルトに戻す |
| `GetConnectedPins` | ピンの接続情報 |
| `ConnectControlRigPins` | RigVM グラフのピンを接続 |
| `DisconnectControlRigPins` | ピン接続を切断 |

#### 変数（5）

| コマンド | 説明 |
|---|---|
| `AddVariable` | RigVM 変数を追加 |
| `ListVariables` | RigVM 変数一覧 |
| `GetVariable` | RigVM 変数の値 |
| `ChangeVariableType` | RigVM 変数の型を変更 |
| `RemoveVariable` | RigVM 変数を削除 |

#### その他（2）

| コマンド | 説明 |
|---|---|
| `CompileControlRig` | ControlRig をコンパイル（セッション単位 1 秒レートリミット） |
| `GetAvailableRigVMUnitStructs` | FRigUnit 派生 UScriptStruct 一覧（上限 1000 件） |

### Toolset ブリッジ（44）🧩

`AnimationAssistantToolset`（UE 5.8+）経由でネイティブコマンドを委譲。プロバイダ：`Toolset.Editor.ControlRig.*`。グループ：アセット作成（1）/ ヒエラルキー観測（8）/ ヒエラルキー編集（7）/ グラフ管理（10）/ ノード（7）/ ピン（6）/ 変数（5）。

---

## UAIP.Editor.EnhancedInput

Enhanced Input アセット編集 — Input Action と Input Mapping Context。

| コマンド | 説明 |
|---|---|
| `ListInputActions` | プロジェクト内の Enhanced Input Action アセット一覧 |
| `ListMappingContexts` | プロジェクト内の Input Mapping Context アセット一覧 |
| `GetInputActionInfo` | Input Action の詳細（ValueType・Triggers・Modifiers） |
| `GetMappingContextInfo` | Mapping Context の詳細（エントリ・キー・Modifier・Trigger） |
| `DeleteInputAction` | Input Action アセットを削除 |
| `DeleteMappingContext` | Input Mapping Context アセットを削除 |
| `AddInputMapping` | Mapping Context にキーマッピングを追加 |
| `RemoveInputMapping` | インデックス指定でキーマッピングを削除 |
| `SetInputMappingKey` | マッピングのキーを変更 |
| `SetInputMappingModifier` | マッピングの Modifier を設定/置換 |
| `SetInputMappingTrigger` | マッピングの Trigger を設定/置換 |
| `SetInputActionModifier` | Input Action の Modifier を設定/置換 |
| `SetInputActionTrigger` | Input Action の Trigger を設定/置換 |

---

## UAIP.Editor.GAS 🧩

エディタ時の GameplayAbilities アセット編集 — GameplayCue タグと Cue Notify アセット。`GameplayAbilities` プラグインが必要（Toolset 版は `GASToolsets` も必要）。

### ネイティブ（11）

| コマンド | 説明 |
|---|---|
| `AddCueTag` | `GameplayCue.*` タグをプロジェクトタグテーブルに追加 |
| `RemoveCueTag` | `GameplayCue.*` タグを削除 |
| `ListCues` | 全 GameplayCue タグを列挙 |
| `GetCueInfo` | GameplayCue タグの詳細と登録済み Cue Notify アセットを取得 |
| `FindCueNotifyAssets` | タグを扱う Cue Notify アセットを検索 |
| `FindCueTagsWithoutNotifies` | Notify アセットが紐づいていない GameplayCue タグを検出 |
| `CreateCueNotifyAsset` | GameplayCueNotify アセットを新規作成（Actor / Static / Burst） |
| `ExecuteCueOnSelectedActor` | 選択中アクターで GameplayCue を実行（テスト用簡易コマンド） |

### Toolset ブリッジ（11）🧩

`GASToolsets`（UE 5.8+）経由でネイティブコマンドを委譲。プロバイダ：`Toolset.Editor.GAS.*`。Runtime 検査ヘルパも併せて橋渡し：`GetAttributeValuesToolset` / `GetActiveEffectsToolset` / `GetGrantedAbilitiesToolset` / `GetActiveTagsToolset` / `FindAttributeSetClassesToolset` / `ListAttributesToolset`。

---

## UAIP.Editor.PythonExtension 🧩

Python コマンド拡張。`PythonScriptPlugin` が必要です。

| コマンド | 説明 |
|---|---|
| `ReloadPythonCommands` 🧩 | コマンドディレクトリを再スキャンし既存ハンドラのディスクリプタをインプレース更新 |
| *(動的コマンド)* 🧩 | `@uaip_command` デコレータで登録されたコマンド（名前はユーザースクリプトに依存） |

---

## UAIP.Editor.Sandbox 🧩

Sandbox セッションのライフサイクル管理。`FileSandbox` プラグインが必要です。`FileSandbox` が有効でない場合、このセクションのコマンドは全て `CommandNotFound` を返します。

| コマンド | 説明 |
|---|---|
| `GetSandboxStatus` 🧩 | 現在の Sandbox 状態を照会 — `Active`・`IsStale`・`SessionId`・`OwnerUAIPSessionId` を返す |
| `GetSandboxChanges` 🧩 | アクティブな Sandbox 内の保留中変更一覧を取得 — `FilePath`・`ChangeKind`（Added / Edited / Removed）・`SizeBytes`・`TotalCount` |
| `BeginSandboxSession` 🧩 | 新しい FileSandbox セッションを開始。以降のアセット書き込みは Sandbox にリダイレクトされる |
| `EndSandboxSession` 🧩 | アクティブな Sandbox セッションを終了。未コミットの変更は自動的に Revert される |
| `CommitSandboxChanges` 🧩 | 選択した（または全ての）Sandbox 変更をディスクにフラッシュ。`CommittedFiles`・`SkippedFiles`・`CommittedCount` を返す |
| `RevertSandboxChanges` 🧩 | 保留中の Sandbox 変更を全て破棄（コミットしない） |

---

## UAIP.Runtime.PIE

PIE セッション制御とランタイムワールド操作。

| コマンド | 説明 |
|---|---|
| 🆓 `StartPIE` | Play-in-Editor セッションを開始 |
| 🆓 `StopPIE` | アクティブな PIE セッションを停止 |
| 🆓 `PausePIE` | アクティブな PIE セッションを一時停止 |
| 🆓 `ResumePIE` | 一時停止中の PIE セッションを再開 |
| 🆓 `LoadMap` | アクティブな PIE セッションでマップをロードし完了を待つ |
| `ExecuteConsoleCommand` | アクティブな PIE セッションでコンソールコマンドを実行 |
| `TeleportActor` | アクターをワールド空間の指定位置 / 回転にテレポート |
| `PossessActor` | プレイヤーコントローラーにアクターを憑依させる |
| `SetTimeScale` | アクティブな PIE セッションのグローバル時間スケールを設定 |
| `QuitGame` | 実行中のゲームプロセスを終了リクエスト |
| `GetConsoleVariable` | コンソール変数（CVar）の現在値・デフォルト値・型・説明を取得 |
| `SearchConsoleVariables` | CVar をキーワード・型・フラグでフィルタし一覧を返す（上限 256 件） |

---

## UAIP.Runtime.Observation

ランタイムキャプチャと状態ダンプ。

| コマンド | 説明 |
|---|---|
| 🆓 `CaptureViewportImage` | 指定プレイヤーのゲームビューポートを PNG キャプチャ |
| 🆓 `DumpWorldState` | アクティブな PIE ワールドの全アクター / コンポーネントのスナップショット（JSON） |
| 🆓 `DumpActorState` | 指定アクターの状態（任意でコンポーネント含む） |
| 🆓 `DumpComponentState` | 指定アクターコンポーネントの状態 |
| 🆓 `DumpRuntimeLog` | バッファリングされた Runtime ログ（テキスト Artifact） |
| 🆓 `CapturePerformanceSnapshot` | CPU / GPU パフォーマンススナップショット（FPS・メモリ・ドローコール） |
| 🆓 `CheckpointCapture` | スクリーンショット + 状態ダンプの複合（シナリオ primitive） |
| 🆓 `SearchLoadedClasses` | ロード済みクラスを検索（ランタイム内省用） |

---

## UAIP.Runtime.Execution

PIE / Standalone でのテスト実行。

| コマンド | 説明 |
|---|---|
| `RunFunctionalTest` | `AFunctionalTest` アクターをアセットパス指定で実行し JSON レポートを返す |
| `RunRuntimeAutomationTest` | PIE 文脈で UE Automation Test を実行 |
| `RunGauntletTest` | RunUAT 経由で Gauntlet テストを外部プロセスとして起動 |

---

## UAIP.Runtime.Assertion

シナリオ primitive — 待機とアサート。

| コマンド | 説明 |
|---|---|
| 🆓 `WaitSeconds` | 指定秒数だけ待機（シナリオ primitive） |
| 🆓 `WaitForCondition` | 条件が真になるまでポーリング |
| 🆓 `AssertActorProperty` | アクタープロパティが期待値と一致することをアサート |
| 🆓 `AssertWorldState` | 複数プロパティを 1 回でバッチアサート |

---

## UAIP.Runtime.GAS 🧩

GameplayAbilities 状態の検査。`GameplayAbilities` プラグインが必要、PIE 必須。

| コマンド | 説明 |
|---|---|
| `GetAttributeValues` 🧩 | アクターの全 AttributeSet 属性値（currentValue / baseValue） |
| `GetActiveEffects` 🧩 | アクターの有効中ゲームプレイエフェクト（Level・StackCount・残時間） |
| `GetGrantedAbilities` 🧩 | アクターに付与されているアビリティ（Class・IsActive・ActiveCount・InputID） |
| `GetActiveTags` 🧩 | アクターが所有する GameplayTags |
| `FindAttributeSetClasses` 🧩 | PIE ワールド内アクターを走査し UAttributeSet クラス一覧を返す（MaxActors 上限） |
| `ListAttributes` 🧩 | AttributeSet クラスに定義されている全属性名 |

---

## UAIP.Runtime.Input

Runtime での入力注入と Enhanced Input 状態検査。PIE 必須。

| コマンド | 説明 |
|---|---|
| `InjectInputKey` | アクティブな PIE ビューポートに生のキー押下/解放を注入 |
| `InjectEnhancedInputAction` | Enhanced Input Action を値付きで発火（Bool / Axis1D / Axis2D / Axis3D） |
| `InjectLegacyAction` | レガシーアクションマッピングイベントを注入 |
| `InjectLegacyAxisInput` | レガシー軸入力を注入 |
| `InjectLegacySpeechInput` | レガシー音声入力を注入 |
| `AddMappingContext` | ローカルプレイヤーに Input Mapping Context を追加 |
| `RemoveMappingContext` | ローカルプレイヤーから Input Mapping Context を削除 |
| `SetInputMode` | 入力モードを設定（GameOnly / UIOnly / GameAndUI） |
| `FlushInput` | テスト終了時の押下中キー状態をフラッシュ |
| `DumpInputState` | 現在の Enhanced Input 状態（有効 Context・Mapping・Action 値）をダンプ |
| `GetEnhancedInputActionValue` | Enhanced Input Action の現在値を取得 |

---

## UAIP.Runtime.Niagara 🧩

PIE 中の Niagara コンポーネント検査とパラメータ上書き。`Niagara` プラグインが必要。

### ネイティブ（4）

| コマンド | 説明 |
|---|---|
| `GetUserVariables` 🧩 | Niagara System Component のユーザー公開変数を取得 |
| `GetVariable` 🧩 | 特定のユーザー変数の値を取得 |
| `SetVariable` 🧩 | ユーザー変数の値を Runtime で設定 |
| `SetSystem` 🧩 | コンポーネントの Niagara System アセットを Runtime で差し替え |

### Toolset ブリッジ（4）🧩

プロバイダ：`Toolset.Runtime.Niagara.*`。UE 5.8+ と `NiagaraToolsets` が必要。ネイティブコマンドをミラー。

---

## シナリオ実行ルート

シナリオは単一コマンドではなく、複数コマンドを順序付きリストとして 1 リクエストで送信する独立ルートです。詳細は [シナリオ実行](scenario.md) を参照してください。利用可能なエントリポイント：

| トランスポート | エントリポイント |
|---|---|
| MCP | `uaip_run_scenario` |
| HTTP | `POST /uaip/scenarios`（`-uaip-enable-scenario` 必須） |
| WebSocket | フレーム `Type: "ScenarioRequest"` |
| CLI | `-uaip-scenario=<json>` / `-uaip-scenario-file=<path>` |

シナリオの各ステップは `uaip_execute` と同じ `CommandDispatcher` を通って実行されるため、Capability と SafetyPolicy のルールが同様に適用されます。

---

> スキーマやパラメータの詳細は本ページでは意図的に省略しています。任意のコマンドの完全スキーマは `uaip_describe_command(CommandName="...")` で取得してください。

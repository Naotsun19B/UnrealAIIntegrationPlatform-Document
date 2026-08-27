**[English](../en/commands.md)** | [概要に戻る](overview.md)

# コマンドリファレンス

UAIP は 1119 個の **UAIP コマンド**（プラグイン本体が直接提供する独自実装）と、それを補強する 421 個の **Toolset ブリッジコマンド**（UE 5.8 公式 Toolset への委譲レイヤー）の合計 1540 をドメイン別に提供しています。コマンド名はすべて完全修飾名（例：`UAIP.Editor.Observation.CaptureActiveWindowImage`）です。本ページの表ではプロバイダプレフィックスを省略しているため、セクションヘッダーのプレフィックスを付けて使用してください。

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
| ⚠️ | Experimental — 挙動や契約が変わる可能性がある、または既知の制約により記載どおりに動作しない |

## UAIP コマンドと Toolset ブリッジコマンド

UAIP では 2 種類のコマンドを公開しています：

- **UAIP コマンド**（`UAIP.*` プレフィックス）：プラグイン本体が直接提供する独自実装のコマンド。UE のバージョンや Toolset プラグインの有無に依存せず動作します。
- **Toolset ブリッジコマンド**（`Toolset.*` プレフィックス・UE 5.8+ かつ Toolset 系プラグイン導入時のみ）：UE 5.8 公式 Toolset フレームワークへの委譲レイヤー。多くは対応する UAIP コマンドのミラーで、Toolset 経由でしか提供されない機能を統一的に呼び出せるようにします。

本ページのドメインサマリでは件数のみを並べています。Toolset ブリッジコマンドの全名前を実行時に列挙したい場合は `uaip_list_commands(ProviderPrefix="Toolset")` を使ってください。

---

## ドメインサマリ

| ドメイン | プロバイダプレフィックス | UAIP コマンド | Toolset ブリッジ | デモ |
|---|---|---:|---:|---:|
| Core | `UAIP.Core` | 11 | — | ✅ |
| Editor Workspace | `UAIP.Editor.Workspace` | 21 | 1 | 一部（13/21） |
| Editor Engine Log | `UAIP.Editor.Engine.Log` | 1 | 4 | ✅ |
| Editor Engine Plugin 🧩 | `UAIP.Editor.Engine.Plugin` | 9 | 15 | 一部（5/9） |
| Editor Engine CVar 🧩 | `Toolset.Editor.EngineManagement` | — | 1 | — |
| Editor Engine ConfigSettings | `UAIP.Editor.Engine.ConfigSettings` | 8 | 8 | 一部（5/8） |
| Editor Observation | `UAIP.Editor.Observation` | 15 | — | ✅ |
| Editor Execution | `UAIP.Editor.Execution` | 9 | — | — |
| Editor UI Automation | `UAIP.Editor.UIAutomation` | 16 | 10 | ✅ |
| Editor Assets | `UAIP.Editor.Assets` | 51 | 6 | 一部（29/51） |
| Editor SemanticSearch 🧩 | `UAIP.Editor.SemanticSearch` | 5 | 2 | — |
| Editor Level | `UAIP.Editor.Level` | 16 | 8 | 一部（7/16） |
| Editor Property | `UAIP.Editor.Property` | 12 | — | 一部（6/12） |
| Editor Blueprint | `UAIP.Editor.Blueprint` | 20 | — | — |
| Editor UMG | `UAIP.Editor.UMG` | 22 | 13 | — |
| Editor Material | `UAIP.Editor.Material` | 11 | — | — |
| Editor GameplayTags | `UAIP.Editor.GameplayTags` | 7 | 6 | — |
| Editor GameFeatures 🧩 | `UAIP.Editor.GameFeatures` | 5 | 4 | — |
| Editor Niagara 🧩 | `UAIP.Editor.Niagara` | 52 | 45 | — |
| Editor Physics | `UAIP.Editor.Physics` | 31 | 17 | — |
| Editor Dataflow 🧩 | `UAIP.Editor.Dataflow` | 9 | 7 | — |
| Editor ChaosClothAsset 🧩 | `UAIP.Editor.ChaosClothAsset` | 10 | 6 | — |
| Editor Skeleton | `UAIP.Editor.Skeleton` | 8 | — | — |
| Editor MetaHuman 🧩 | `UAIP.Editor.MetaHuman` | 56 | 9 | — |
| Editor DataTable | `UAIP.Editor.DataTable` | 8 | — | — |
| Editor AnimBlueprint | `UAIP.Editor.AnimBlueprint` | 11 | — | — |
| Editor SoundCue | `UAIP.Editor.SoundCue` | 7 | — | — |
| Editor SoundSettings | `UAIP.Editor.SoundSettings` | 13 | — | — |
| Editor MVVM 🧩 | `UAIP.Editor.MVVM` | 26 | 9 | — |
| Editor BehaviorTree | `UAIP.Editor.BehaviorTree` | 17 | 7 | — |
| Editor MetaSound 🧩 | `UAIP.Editor.MetaSound` | 10 | — | — |
| Editor EQS 🧩 | `UAIP.Editor.EQS` | 9 | — | — |
| Editor Sequencer | `UAIP.Editor.Sequencer` | 123 | 61 | — |
| Editor StateTree | `UAIP.Editor.StateTree` | 39 | 8 | — |
| Editor Curve | `UAIP.Editor.Curve` | 6 | — | — |
| Editor PCG 🧩 | `UAIP.Editor.PCG` | 34 | 31 | — |
| Editor WorldConditions 🧩 | `UAIP.Editor.WorldConditions` | 13 | 2 | — |
| Editor Conversation 🧩 | `UAIP.Editor.Conversation` | 7 | 5 | — |
| Editor ControlRig | `UAIP.Editor.ControlRig` | 68 | 107 | — |
| Editor ControlRig Dynamics 🧩 | `UAIP.Editor.ControlRig.Dynamics` | 16 | — | — |
| Editor ControlRig Physics 🧩 | `UAIP.Editor.ControlRig.Physics` | 8 | — | — |
| Editor EnhancedInput | `UAIP.Editor.EnhancedInput` | 13 | — | — |
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
| Runtime PIE | `UAIP.Runtime.PIE` | 6 | 3 | ✅ |
| Runtime World | `UAIP.Runtime.World` | 9 | 1 | — |
| Runtime Observation | `UAIP.Runtime.Observation` | 8 | — | ✅ |
| Runtime Execution | `UAIP.Runtime.Execution` | 3 | — | — |
| Runtime Assertion | `UAIP.Runtime.Assertion` | 4 | — | ✅ |
| Runtime Input | `UAIP.Runtime.Input` | 11 | — | — |
| Runtime GAS 🧩 | `UAIP.Runtime.GAS` | 17 | — | — |
| Runtime Niagara 🧩 | `UAIP.Runtime.Niagara` | 4 | 4 | — |
| Runtime Engine Log | `UAIP.Runtime.Engine.Log` | 3 | — | 一部（2/3） |
| Runtime Engine Plugin | `UAIP.Runtime.Engine.Plugin` | 5 | — | ✅ |
| Runtime Engine CVar | `UAIP.Runtime.Engine.CVar` | 4 | — | 一部（2/4） |
| Runtime Engine Config | `UAIP.Runtime.Engine.Config` | 2 | — | 一部（1/2） |
| Runtime Insights Trace | `UAIP.Runtime.Insights.Trace` | 11 | — | 一部（3/11） |
| Runtime Insights Analysis | `UAIP.Runtime.Insights.Analysis` | 3 | — | — |

---

## UAIP.Core

検索・ヘルスチェック・セッション管理などのシステムレベルコマンド。

| コマンド | 説明 |
|---|---|
| 🆓 `HealthCheck` | プラグイン接続確認 — `Status`・`UAIPVersion`・`EngineVersion`・`BuildConfig` に加え、`ProjectFilePath`（開いている `.uproject` の絶対パス。MCP Bridge が正しいエディタインスタンスへアタッチしているか検証するために使う）・`TransportTimeouts`（トランスポートごとの非同期コマンドタイムアウト秒数。例 `{"HTTP": 120, "WS": 12}`）・`QueueCongestion`（遅延実行キューの混雑度。`None` / `Low` / `High` の 3 段階。正確な待ち件数は他セッションの活動量を推測させるため返しません）を返す |
| 🆓 `GetSystemInfo` | UE バージョン（Major/Minor/Patch/Changelist）・プロジェクト名・プラットフォーム・ビルド設定・UAIP バージョンを返す |
| 🆓 `QueryCapabilities` | セッションの Capability セットと `OperationalConstraints`（7 つのポリシーフラグ）を返す |
| 🆓 `ListCommands` | フィルタ付きコマンドカタログ（`ProviderPrefix`・`KeywordFilter`・`IncludeUnavailable`・`Stability`） |
| 🆓 `DescribeCommand` | 単一コマンドの完全メタデータ（スキーマ・必要 Capability・可用性） |
| 🆓 `ListPlugins` | インストール済みプラグインと有効/無効状態の一覧（JSON）— ⚠️ **非推奨**：代わりに `UAIP.Runtime.Engine.Plugin.ListPlugins` を使用 |
| 🆓 `EndSession` | セッションを明示的に終了しサーバー側リソースを解放する（成果物は GC 対象になる） |
| 🆓 `ReloadCapabilities` | エディタを再起動せずに `Config/DefaultUAIP.ini` から Capability セットを再読み込みする（`AllowCapabilityReload=True` のときのみ登録） |
| 🆓 `GetPendingInteractionStatus` | 保留中の対話 1 件の状態 — `State`・`Cause`・`ElapsedSeconds`・`Prompt`・`Reason`・`Result` — を、変化を待たずに報告する。対話（`DrawPCGSpline` などの対話型コマンド）を開始したときと同じ `SessionId` を明示的に指定する必要があり、未知・期限切れ・他セッション所有はすべて同じ `NotFound` として扱われる |
| 🆓 `WaitForPendingInteraction` | 対話が `AwaitingUser` を離れるか、この呼び出し自身の `TimeoutSeconds` 上限（デフォルト 30、範囲 [1, 600]）に達するまでブロックする。タイムアウトしても対話自体には影響せず、人間の応答を待ち続ける。同じ対話を同時に監視できる呼び出しは最大 4 件までだが、2 件目以降には `[UAIP.Transport] AllowConcurrentPassiveWaits` が必要（[設定](config.md) 参照） |
| 🆓 `CancelPendingInteraction` | 呼び出したセッションが開始した対話をキャンセルする（人間の応答は待たない）。既に `Completed` になっている対話はエラーではなく `Success` として扱われる。開始コマンドが宣言した Capability をセッションの現在の Capability セットに対して再チェックする |

---

## UAIP.Editor.Workspace

エディタライフサイクル・タブ管理・グラフレイアウト・シェーダーコンパイル・Live Coding。

| コマンド | 説明 |
|---|---|
| 🆓 `FocusEditorTab` | 指定アセットのエディタタブを前面に出す。対象は `AssetPath` で指定し、Slate レイアウトのタブ識別子では**ない** — `DumpEditorState` が返す `ActiveTabId`（`"Viewport"` / `"Inspector"` など）はここでは拒否される。レイアウト識別子でタブを指定したい場合は `CaptureEditorTabImage` の `TabId` を使う |
| 🆓 `CloseEditorTab` | 指定アセットのエディタタブを閉じる。`FocusEditorTab` と同じく `AssetPath` で指定する |
| 🆓 `ListSpawnableTabs` | 開けるエディタタブの候補を一覧で返す。各行の `TabId` / `OwnerMajorTabId` / `OwnerInstanceId` はそのまま `OpenTabById` / `CloseTabById` の `TabId` / `OwnerTabId` / `OwnerInstanceId` として渡せる。表示名・ツールチップ・そのタブが既に開いているかどうかも含む。開いているかどうかはその行が示す所属先を基準に判定され、`MajorTabLocal` の行はそのウィンドウ内だけを、`Global` の行はエディタ全体を対象とする（エディタ全体に登録されたタブはレイアウト次第でどのタブウェルにも置かれるが、`"Global"` からは常に到達できるため）。網羅的な一覧ではなく、応答は常に `EnumerationScope: "MenuVisible"` を返す — 一覧に無い `TabId` でも開ける場合があり（生成メニューから外れているだけの場合がある）、逆に設定で恒久的に拒否されている場合もあるため、「一覧に無い」は「未列挙」であって「存在しない」ではない。読み取り専用だが、表示名・ツールチップの取得が第三者のデリゲートを評価しうるため `EditorTabSpawn` を要求する |
| 🆓 `OpenTabById` | Slate レイアウトのタブ識別子（`TabId`。`FocusEditorTab` の `AssetPath` とは別の識別子空間）を指定してエディタタブを開く。`FocusEditorTab` やメニュー操作代行では届かないタブ — ToolMenus に一度も登録されていないレガシーメニュー経由のタブや、所属ウィンドウが前面にないタブ — にも到達できる。`OwnerTabId` に `"Global"` を指定するとエディタ全体に登録されたタブ（Output Log 等）を、major tab 自身の `TabId`（複数該当する場合は `OwnerInstanceId` で絞り込み）を指定するとその内部のパネルを対象にできる。所属先のウィンドウがまだ開いていなければ先に開く。既に開いている所属先はそのまま使うため、`ListSpawnableTabs` が返した行はそのまま渡せる（所属先に対するスポナー登録と許可の判定は、この呼び出しが所属先を開く必要がある場合にだけ適用される）。応答には実際に開いたタブの `InstanceId`（この応答からしか得られない値）、`WasAlreadyOpen`、`OwnerOpenedByThisCall` が含まれ、後始末で何を閉じるべきかを判断できる（閉じる順序は対象タブ→所属先）。失敗時はこの呼び出しが開いたものを取り除く。候補の発見には `ListSpawnableTabs` を使う（`EditorTabSpawn` 必要） |
| 🆓 `CloseTabById` | `OpenTabById` と同じ指定（`TabId` / `OwnerTabId` / `InstanceId` / `OwnerInstanceId`）でタブを閉じる。アセットパスでは指定できない。`OpenTabById` と異なり `OwnerTabId` が開いていなくても新たに開くことはせず、その場合は `NotFound` になる。許可判定も行わない — 実行時にポリシーが変わったせいで後始末そのものが失敗する方が悪いという判断による。そのため対象は「このセッションが開いたタブ」に限らず、人間が手動で開いたものも含め、いま生きている任意のタブになる（`EditorTabSpawn` 必要） |
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

### Toolset ブリッジ — LiveCoding（1 件）🧩

`LiveCodingToolset`（UE 5.8+）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.LiveCoding.*`。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.LiveCoding.CompileLiveCoding` | Live Coding 再コンパイルをトリガー（`LiveCodingControl` 必要） |

---

## UAIP.Editor.Engine.Log

エディタ Output Log のログエントリ取得。ログ**詳細レベル**の取得・設定は [`UAIP.Runtime.Engine.Log`](#uaipruntimeenginelog) にあります。

| コマンド | 説明 |
|---|---|
| 🆓 `GetLogEntries` | エディタ Output Log から最近のログエントリを取得（パターンフィルタ対応、Capability 不要） |

### Toolset ブリッジ — Logs（4 件）🧩

`LogsToolset`（UE 5.8+、EditorToolset プラグイン）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.Toolset.Logs.*`。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.Toolset.Logs.GetLogEntries` | エディタ Output Log から最近のログエントリを取得 |
| `Toolset.Editor.Toolset.Logs.GetLogCategories` | 登録済みログカテゴリ名の一覧 |
| `Toolset.Editor.Toolset.Logs.GetVerbosity` | ログカテゴリの詳細レベルを取得 |
| `Toolset.Editor.Toolset.Logs.SetVerbosity` | ログカテゴリの詳細レベルを設定（`LogVerbosityEdit` 必要） |

### Toolset ブリッジ — CVar（1 件）🧩

EditorToolset プラグイン（UE 5.8+）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.EngineManagement.*`。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.Toolset.EngineManagement.SearchCVars` | CVar を名前パターンで検索（センシティブパターンを除外、`CVarInspect` 必要） |

---

## UAIP.Editor.Engine.Plugin 🧩

プラグインの状態・ディスクリプタの観測と変更。エンジンおよびマーケットプレイスのプラグインは常に読み取り専用です。変更コマンドはエディタ再起動後に反映されます。

| コマンド | 説明 |
|---|---|
| 🆓 `GetPluginDescriptor` | プラグインの `.uplugin` ファイル全体を JSON で返す |
| 🆓 `GetPluginDependents` | 指定プラグインに依存する他のプラグイン一覧を返す |
| 🆓 `GetPluginTemplateDescriptions` | 利用可能なプラグインテンプレートの一覧を返す |
| 🆓 `IsPluginCreationAllowed` | 現在の環境でプラグイン作成が許可されているか確認 |
| 🆓 `IsPluginModificationAllowed` | 指定プラグインの変更が許可されているか確認 |
| `SetPluginEnabled` | プラグインを有効化または無効化する（`PluginEnableToggle` 必要；`RestartRequired: true` を返す） |
| `UpdatePluginDescriptor` | プラグインの `.uplugin` 内の選択フィールドを上書き（`PluginDescriptorEdit` 必要） |
| `AddPluginDependency` | プラグインの `.uplugin` に依存エントリを追加（`PluginDependencyEdit` 必要） |
| `RemovePluginDependency` | プラグインの `.uplugin` から依存エントリを削除（`PluginDependencyEdit` 必要） |

### Toolset ブリッジ — Plugin（15 件）🧩

`PluginToolset`（UE 5.8+）経由のブリッジコマンド。プロバイダ：`Toolset.Plugin.*`。

| コマンド | 説明 |
|---|---|
| `Toolset.Plugin.ListEnabledPlugins` | 現在有効なプラグインの一覧 |
| `Toolset.Plugin.ListDiscoveredPlugins` | 検出済みプラグイン（有効・無効を問わず）の一覧 |
| `Toolset.Plugin.GetPluginInfo` | プラグインの基本情報（名前・バージョン・有効状態）を取得 |
| `Toolset.Plugin.IsEnabled` | プラグインが現在有効か確認 |
| `Toolset.Plugin.GetPluginDependencies` | プラグインが依存するプラグイン一覧を返す |
| `Toolset.Plugin.GetPluginForAsset` | 指定アセットを提供するプラグインを返す |
| `Toolset.Plugin.GetPluginDescriptor` | プラグインの `.uplugin` 全体を JSON で返す |
| `Toolset.Plugin.GetPluginDependents` | 指定プラグインに依存する他のプラグイン一覧 |
| `Toolset.Plugin.GetPluginTemplateDescriptions` | 利用可能なプラグインテンプレートの一覧 |
| `Toolset.Plugin.IsPluginCreationAllowed` | プラグイン作成が許可されているか確認 |
| `Toolset.Plugin.IsPluginModificationAllowed` | 指定プラグインの変更が許可されているか確認 |
| `Toolset.Plugin.SetPluginEnabled` | プラグインを有効化または無効化（`PluginEnableToggle` 必要） |
| `Toolset.Plugin.UpdatePluginDescriptor` | `.uplugin` の選択フィールドを上書き（`PluginDescriptorEdit` 必要） |
| `Toolset.Plugin.AddPluginDependency` | `.uplugin` に依存エントリを追加（`PluginDependencyEdit` 必要） |
| `Toolset.Plugin.RemovePluginDependency` | `.uplugin` から依存エントリを削除（`PluginDependencyEdit` 必要） |

---

## UAIP.Editor.Engine.ConfigSettings

`ISettingsModule` 経由でプロジェクト設定やエディタ設定を管理するコマンド群。`ContainerName / CategoryName / SectionName` の 3 階層パスでセクションを指定します。書き込み操作はプロジェクトの `Config/` ディレクトリ配下のファイルのみ許可されます（エンジン ini ファイルは `PolicyViolation` で拒否）。

| コマンド | 説明 |
|---|---|
| 🆓 `ListSettingsContainers` | 登録済みの設定コンテナ（`Project`、`Editor` など）を一覧表示。Capability 不要 |
| 🆓 `ListSettingsCategories` | コンテナ内の設定カテゴリを一覧表示。Capability 不要 |
| 🆓 `ListSettingsSections` | カテゴリ内の設定セクションを一覧表示。Capability 不要 |
| 🆓 `GetSettingsSchema` | セクションの編集可能プロパティ（名前・型・説明・デフォルト値・編集条件）を JSON アーティファクトで返す（`EditorInspect` 必要） |
| 🆓 `GetSettingsValues` | セクションの現在のプロパティ値を JSON アーティファクトで返す。シークレットフィールド（名前がシークレットパターンに一致・シークレットメタデータあり・ファイルパス型）は `***` でマスク（`EditorInspect` 必要） |
| `SetSettingsValues` | `Properties` マップを `ImportText` 経由で設定オブジェクトにマージ。`DryRun`（検証のみ・適用なし）に対応。`ConfigSettingsEdit` 必要。PIE 中は実行不可 |
| `SaveSettings` | `ISettingsSection::Save()` 経由で設定を ini ファイルに書き出す。`ConfigSettingsSave` 必要。PIE 中および `bDisableSave` 設定時は実行不可 |
| `ResetSettingsToDefaults` | 設定オブジェクトをクラスデフォルトに戻して保存。`ConfigSettingsReset` 必要。PIE 中は実行不可 |

### Toolset ブリッジ — ConfigSettings（8 コマンド）🧩

`ConfigSettingsToolset` プラグイン（UE 5.8+）経由のブリッジコマンド。プロバイダ: `Toolset.ConfigSettings.*`。

| コマンド | 説明 |
|---|---|
| `Toolset.ConfigSettings.ListContainers` | 登録済みの設定コンテナを一覧表示 |
| `Toolset.ConfigSettings.ListCategories` | コンテナ内の設定カテゴリを一覧表示 |
| `Toolset.ConfigSettings.ListSections` | カテゴリ内の設定セクションを一覧表示 |
| `Toolset.ConfigSettings.GetSectionSchema` | セクションのプロパティスキーマを取得 |
| `Toolset.ConfigSettings.GetSectionPropertyValues` | セクションの現在のプロパティ値を取得 |
| `Toolset.ConfigSettings.SetSectionProperties` | セクションのプロパティ値を設定して永続化（`ConfigSettingsEdit` 必要） |
| `Toolset.ConfigSettings.SaveSection` | 現在のメモリ上の設定をセクションの ini ファイルに書き出す（`ConfigSettingsSave` 必要） |
| `Toolset.ConfigSettings.ResetSectionToDefaults` | セクションの全プロパティ値をコンパイル済みデフォルトにリセット（`ConfigSettingsReset` 必要） |

---

## UAIP.Editor.Observation

スクリーンショットとエディタ状態ダンプ（すべて読み取り専用）。

| コマンド | 説明 |
|---|---|
| 🆓 `CaptureActiveWindowImage` | アクティブな最上位ウィンドウのスクリーンショット（PNG Artifact）。エディタがフォアグラウンドである必要はない — アクティブなウィンドウがない場合はメインウィンドウを撮影し、どちらを撮ったかを `Result.CapturedWindow`（`"ActiveWindow"` / `"MainWindow"`）で返す。フォールバックはメインウィンドウにしか届かないため、フローティングのアセットエディタやモーダルダイアログは `CaptureEditorTabImage` を使う |
| 🆓 `CaptureEditorTabImage` | 指定エディタタブのウィジェット領域のスクリーンショット。Slate レイアウト識別子で指定するため、`DumpEditorState` が返す `ActiveTabId` をそのまま渡せる。エディタが背面でも動作する。⚠️ 撮影前に対象タブをスタックの前面へ出すため（背面のタブは描画されておらず空の画像になる）、**ユーザーに見えているタブが切り替わる** |
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
| 🆓 `GetLogCategories` | 登録済みエンジンログカテゴリ名の一覧（任意でサブストリングフィルタ対応） |
| 🆓 `ListGraphNodes` | 指定タブのグラフエディタ内の全ノードを列挙 — `NodeId`（GUID）・`NodeClass`・`NodeTitle`・`Position`。`UEdGraph` ベースのエディタ全般で動作 |
| 🆓 `CaptureViewportImageAnnotated` | ワールド座標ラベル付きビューポート画像のキャプチャ（`ViewportAnnotationCapture` 必要） |

---

## UAIP.Editor.Execution

テスト・Python スクリプト・Editor Utility Blueprint の実行。

| コマンド | 説明 |
|---|---|
| `DiscoverAutomationTests` | Automation Test モジュールを読み込み、検出されたテスト数のサマリを返す |
| `ListAutomationTests` | 検出済み Automation Test をフィルタして JSON Artifact で返す |
| `RunAutomationTest` | UE Automation Test を名前で実行し Pass/Fail/Error レポートを返す |
| `RunAutomationSpec` | UE Automation Spec を名前で実行し Pass/Fail/Error レポートを返す |
| `GetAutomationTestStatus` | Automation Test マネージャの現在状態を返す（既定はインライン） |
| `StopAutomationTests` | 実行中の Automation Test バッチのキャンセルを要求 |
| `RunEditorPythonScript` 🧩 | インライン Python スクリプトまたは `.py` ファイルを実行（`PythonScriptPlugin` 必須） |
| `RunEditorUtilityBlueprint` | 指定 Editor Utility Blueprint を実行 |
| `RunNamedEditorCommand` | `GUnrealEd->Exec` 経由で名前付き Editor コンソールコマンドを実行 |

> **Note**: `RunAutomationTest`（および Runtime 側の `RunRuntimeAutomationTest`）は、`RunAllMatching=true`（既定）のとき**マッチした全件を実行します**。件数を絞るには `MaxMatchingTests`（1 以上。省略すると上限なし）を指定してください。`0` は「上限なし」ではなく無効値として拒否されます — 両者は正反対の要求であり、読み替えると絞った実行が全件カバーを名乗ることになるためです。
>
> レポートには常に `Summary.Matched`（フィルタに一致した数）と `Summary.Selected`（実際に走らせた数）が入ります。**差の有無に関わらず必ず出力されます** — 差があるときだけ出す形式では、その行が無いことが「全件だった」のか「その版が出力しないだけ」なのか読み手に区別できないためです。人間向けレポート本文と Output Log にも同じ 2 つが出ます。
>
> `TimeoutSec` は**バッチ全体ではなく 1 テストごとの上限**です（既定 60 秒）。マッチ件数が増えても各テストがこの時間内に終わる限り全件走ります。なお Runtime 側の `RunRuntimeAutomationTest` にはこれとは別に一括実行全体の壁時計上限（600 秒）があり、到達した場合はレポートに `(bulk execution time limit reached)` というエントリが `Error` として現れます。
>
> **v1.1.0 での変更**: 以前は 100 件で打ち切られ、**打ち切られたことが応答から分かりませんでした**（`Pass=100 Fail=0` は全件成功と字面が同じです）。100 件で止まる挙動に依存していた場合は `MaxMatchingTests=100` を明示してください。

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
| 🆓 `SnapshotUI` | 範囲を絞り込め、除外分も報告する UI の構造スナップショットを取得 |
| 🆓 `OpenPasswordTestWindow` | パスワード用 `SEditableTextBox` を持つフローティングテストウィンドウを開く（パスワードフィールドのポリシーテスト用ターゲット） |

> **Note**: `SnapshotUI` は任意の走査範囲を指定できます。起点には `RootWidgetRef` または `RootWidgetPath`（互いに排他。どちらも `WindowTitle` とは併用不可）、走査量には `MaxDepth`（既定 30）と `MaxNodes`（既定 50000。1 回の呼び出しで訪れる全ルートで共有される単一予算）、絞り込みには `WidgetTypes` + `WidgetTypeMode`（`"Add"` は既定の対象に追加、`"Only"` は指定した型だけに限定）と `LabelContains`、既定で外れるウィジェットを拾うには `bIncludeInvisible` / `bIncludeUnclassified` を使います。応答には常に `EmittedCount`・`FilteredCount`・`FilteredReasons`（0 件でも常に存在する 6 つの理由キー — `InvisibleSubtreeRoot` / `StructuralContainer` / `TypeFilterMismatch` / `LabelFilterMismatch` / `Unclassified` / `RegistrationFailed`）・`UnclassifiedTypes`（`Type` + `Count` を件数降順・同数なら型名昇順で最大 200 件。各 `Type` はそのまま `WidgetTypes` に渡せる）・`Traversal`（`Complete` / `NodeLimitReached` / `DepthLimitReached` / `VisitedNodeCount`）・`MatchedRootCount`・`EffectiveParams`（クランプ・正規化後に実際に適用された値）が含まれます。
>
> 応答が答えられるのは常に「現在のフィルタを通過した集合に無い」までです。これを「UI 上のどこにも存在しない」と読み替えてよいのは、次のすべてが成り立つときに限ります: 走査が打ち切られていない（`Traversal.Complete == true`）、未分類型の一覧が全件かつ名指し可能（`UnclassifiedTypesComplete == true` かつ `UnaddressableUnclassifiedCount == 0`）、不可視ウィジェットを刈り取っていない（`FilteredReasons.InvisibleSubtreeRoot == 0`、または `bIncludeInvisible` を指定済み）、`WidgetTypeMode` が `"Add"`（型で絞り込んでいない）、`LabelContains` が空、Ref の登録に失敗したウィジェットが無い（`FilteredReasons.RegistrationFailed == 0`）、`WindowTitle` / `RootWidgetRef` / `RootWidgetPath` のいずれでも呼び出しを絞り込んでいない（絞り込んでいる場合はその範囲内でしか結論が成り立たない）。これらすべてを満たしていても、**構造コンテナ**型（後述）は `Widgets` にも `UnclassifiedTypes` にも現れません — `WidgetTypes` で名指しして確認してください。
>
> 構造コンテナ — レイアウトを組むためだけに存在するウィジェット — は走査はされますが emit されず、未分類型としても列挙されません。代わりに `FilteredReasons.StructuralContainer` にまとめて計上されます: `SBox` / `SBorder` / `SOverlay` / `SSpacer` / `SConstraintCanvas` / `SHorizontalBox` / `SVerticalBox` / `SGridPanel` / `SWrapBox` / `SWidgetSwitcher` / `SCanvas` / `SScaleBox` / `SSizeBox` / `SNullWidget` / `SInvalidationPanel` / `SRetainerWidget`。これらを `WidgetTypes` で名指しすれば emit されます — 明示的な型指定は常に分類より優先されます。
>
> 型名は `SWidget::GetTypeAsString()` から取得されます。これはウィジェットの構築サイトで `SNew(...)` に渡した識別子であり、動的な型ではありません。`SNew(基底型)` で構築されたウィジェットは、実際の型が異なっていても基底クラス名を返します。また `SNew` を経由せずに構築されたウィジェット（例: `MakeShared<SFoo>()`）は、型名としてリテラル文字列 `"None"` を返します。
>
> `RootWidgetRef` は使い捨てです。呼び出しが完了すると、指定した Ref だけでなく**そのセッションの `WidgetRef` がすべて**無効化されます — `SnapshotUI` の呼び出しごとに新しい世代が始まるためです。以前の Ref を残したまま段階的に絞り込みたい場合は `RootWidgetPath` を使ってください。`SnapshotUI` は引き続き `IsReadOnly() == true` を宣言し `bReadOnly` 下でも実行できます — リセットされるのは UAIP 側の Ref キャッシュのみで、永続的なエディタの状態は変わりません。UI Automation の全コマンドを通じて、`WidgetRef` はそれを発行したスナップショットから 60 秒で失効します。

### Toolset ブリッジ — SlateInspector（10 件）🧩

`SlateInspectorToolset`（UE 5.8+）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.SlateInspector.*`。ネイティブ側のウィジェットパス記法ではなく refPath でウィジェットを指定します。このセクションの全ブリッジコマンドは、対応するネイティブコマンドと同じ Capability を要求するようになりました（[Safety & Capabilities](safety.md) 参照）— それまでのリリースでは Capability チェックなしにディスパッチされていました。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.SlateInspector.SnapshotUI` | 指定 ref のウィジェットツリーをスナップショット |
| `Toolset.Editor.SlateInspector.ObserveWidget` | ウィジェットを観測対象として登録し、observer の `Identifier` を返す |
| `Toolset.Editor.SlateInspector.UnobserveWidget` | `Identifier` で登録したウィジェットの観測を解除 |
| `Toolset.Editor.SlateInspector.ListObservers` | 現在有効なウィジェット observer を列挙 |
| `Toolset.Editor.SlateInspector.ClickWidget` | 指定 ref のウィジェットへのマウスクリックをシミュレート |
| `Toolset.Editor.SlateInspector.HoverWidget` | 指定 ref のウィジェット上へカーソルを移動 |
| `Toolset.Editor.SlateInspector.InputText` | 指定 ref のウィジェットにテキストを入力 |
| `Toolset.Editor.SlateInspector.PressKey` | キー入力を送信（`Ctrl+S` のような修飾キープレフィックス対応） |
| `Toolset.Editor.SlateInspector.SetComboSelection` | コンボボックスウィジェットの項目を選択 |
| `Toolset.Editor.SlateInspector.FillForm` | 複数のフォームフィールドを 1 回の呼び出しで入力 |

> **Note**: `Toolset.Editor.SlateInspector.PressKey` はネイティブの `PressKey` と同じ危険ショートカットのブロックリストを適用しますが、現在どのウィジェットにフォーカスがあるかを解決する手段が無いため、**Backspace を常時ブロック**します — ネイティブコマンドが持つ「テキスト入力ウィジェットにフォーカスがある場合の例外」はブリッジには引き継がれません。

---

## UAIP.Editor.Assets

アセットの開閉・検索・作成・複製・リネーム・削除、フォルダ管理。

| コマンド | 説明 |
|---|---|
| `OpenAsset` | 指定アセットをエディタで開く |
| `CloseAsset` | 指定アセットの全エディタを閉じる |
| `SaveAsset` | 名指ししたアセットだけをディスクへ書き込む（`AssetMutate` 必要）。確認ダイアログを出さないため非対話でも完結する |
| 🆓 `ListDirtyPackages` | 未保存の変更を持つパッケージを列挙する（保存前の事前確認用） |
| 🆓 `SearchAssets` | パス・クラス・タグでアセットを検索 |
| `CreateAsset` | 指定クラスの新規アセットを作成 |
| 🆓 `ListCreatableAssetClasses` | `CreateAsset` が作成可能な全 UClass をFactory数・デフォルトFactory付きで返す（重い呼び出し） |
| 🆓 `ListFactoriesForClass` | 指定 `ClassName` に対応する Factory 候補と各 `FactoryParams` スキーマを返す |
| `DuplicateAsset` | 既存アセットを複製 |
| `CopyAsset` | アセットを新しい完全パッケージパスへコピー（コピー先が存在する場合は失敗・`AssetCreate` 必要） |
| `RenameAsset` | アセットをリネーム / 別パスへ移動 |
| `MoveAsset` | 名前を維持したままアセットを別フォルダへ移動し、リダイレクタが残ったかを報告（`AssetMutate` 必要） |
| `DeleteAsset` | アセットを削除 |
| `CreateFolder` | Content Browser に新規フォルダを作成 |
| `DeleteFolder` | 空フォルダを削除（空でない場合 `NotEmpty`） |
| `ForceDeleteFolder` | フォルダと配下アセットを一括削除（50 件上限・外部参照チェックなし） |
| `MoveFolder` | フォルダ内の全アセットをサブフォルダ構造を保ったまま移動。部分失敗は `FailedAssets` に列挙（`AssetFolderRefactor` 必要） |
| 🆓 `GetSelectedAssets` | Content Browser で現在選択中のアセットを返す |
| `SelectAssets` | Content Browser で指定アセットを選択（`ContentBrowserNavigate` 必要） |
| 🆓 `GetContentBrowserPath` | Content Browser に現在表示されているフォルダパスを返す |
| `SetContentBrowserPath` | Content Browser を指定フォルダに移動（`ContentBrowserNavigate` 必要） |
| 🆓 `GetOpenAssets` | アセットエディタで現在開いているアセット一覧を返す |
| 🆓 `ListAssetRedirectors` | フォルダ配下（既定はプロジェクト全体の `/Game`）のアセットリダイレクタを、アセットをロードせずに元パス・先パス付きで一覧取得する |
| `FixAssetRedirectors`（`RedirectorFixup` 必要） | `/Game` 全体（常に再帰的）を対象に、解決可能なアセットリダイレクタを一括修正・削除する |
| `FixUpRedirectorsInFolder`（`RedirectorFixup` 必要） | 同じ修正処理を 1 フォルダに限定して実行。解決できなかったものは `FailedRedirectors` に返る |
| 🆓 `GetAssetReferences` | 指定アセットを起点に参照グラフ（参照元・参照先・両方）を指定深さまで探索する |
| 🆓 `GetAssetSizeMap` | フォルダ配下のディスクサイズ（任意で常駐メモリサイズ）をアセット単位で集計し降順ソートする |
| 🆓 `GetAssetSizeMapByClass` | フォルダ配下のディスクサイズをアセットクラス単位で集計し降順ソートする |
| 🆓 `FindUnreferencedAssets` | ⚠️ **非推奨** — 代わりに `StartAssetAudit` を使用。フォルダ配下でユーザー参照（Engine/Script以外）が存在しないアセットを検出する（ハードリファレンスヒューリスティック）。動作・進捗発火とも変更なし |
| 🆓 `FindCircularReferences` | ⚠️ **非推奨** — 代わりに `StartAssetAudit` を使用。フォルダ配下のアセット間の循環依存チェーンを検出する。動作・進捗発火とも変更なし |
| 🆓 `FindBrokenReferences` | ⚠️ **非推奨** — 代わりに `StartAssetAudit` を使用。アセットレジストリに存在しないパッケージへの依存を検出する。動作・進捗発火とも変更なし |
| 🆓 `GetAssetDependencyPath` | 2つのアセット間の最短依存/参照パスを検索する |
| 🆓 `RunAssetAudit` | ⚠️ **非推奨** — 代わりに `StartAssetAudit` を使用。フォルダ配下の複合監査（未参照アセット・循環参照・壊れた参照・最大サイズアセット）を実行する。動作・進捗発火とも変更なし。同期実行でゲームスレッドを完了まで占有するため、大規模プロジェクトでは数十秒〜数分エディタ（および他の UAIP コマンド）が固まることがある |
| 🆓 `StartAssetAudit` | 監査ジョブを開始し、`AuditId` を即座に返す。実際の走査はゲームスレッドを占有せず、エディタのフレームの合間で少しずつ進むため、エディタも他の UAIP コマンドも応答し続ける。パラメータ：`PackagePath`（必須）、`Recursive`（既定 `true`）、`Reports`（`UnreferencedAssets` / `CircularReferences` / `BrokenReferences` / `TopLargestAssets` の配列。既定は全 4 種 — 空配列を明示指定した場合は `InvalidParams`）、`MaxUnreferenced`（既定 `200`、範囲 `[1, 2000]`）、`MaxCycles` / `MaxBroken` / `MaxTopLargest`（`RunAssetAudit` と同じ既定値）。別の監査ジョブが実行中の場合は `TooManyRequests`、エディタがモーダルダイアログやスロータスクのプログレスバーを表示中の場合は `NotAllowed` を返す。**`SessionId` の明示指定が必須** — トランスポートが自動生成した匿名セッションは `InvalidParams` で拒否される（匿名で開始したジョブは後から照会・取得できなくなるため） |
| 🆓 `GetAssetAuditStatus` | `AuditId` で監査ジョブの状態を照会する — `State`（`Preparing` / `Running` / `Completed` / `Failed`）、現在処理中のレポート種別、処理済み/総件数、経過秒数、失敗時の理由を返す。実行コストはジョブ規模に依存しない（O(1)）。**開始時と同じ `SessionId` が必須** — 未知・期限切れ・他セッションの `AuditId` はいずれも区別されず `NotFound` になる |
| 🆓 `GetAssetAuditResult` | 完了した監査ジョブの成果物参照を `AuditId` で取得する。取得したいレポートを `Reports` で絞り込むこともできる（省略時は開始時に要求した全レポート。開始時に要求していないレポートを指定した場合はエラーにはならず「要求されていない」扱いで未取得側に分類される）。O(1)。状態が `Completed` に達していない場合は現在の `State` とともに `ExecutionFailed` を返す。**開始時と同じ `SessionId` が必須** |
| 🆓 `ListPrimaryAssetTypes` | 登録済みの全 `PrimaryAssetType`（`UAssetManager`）をクラス・ディレクトリ・アセット数サマリー付きで一覧取得する |
| 🆓 `GetPrimaryAssetTypeInfo` | 単一の `PrimaryAssetType` の詳細（ディレクトリ・個別アセット・既定Rule）を取得する |
| 🆓 `ListPrimaryAssets` | 指定 `PrimaryAssetType` に属する `PrimaryAssetId` とアセット一覧を取得する |
| 🆓 `GetAssetBundle` | 指定 `PrimaryAssetId` の `AssetBundle` エントリを取得する（未定義なら空配列） |
| 🆓 `GetAssetTags` | アセットの Asset Registry タグマップを取得する |
| 🆓 `GetPrimaryAssetIdForPath` | アセットパスから `PrimaryAssetId` を逆引きする（未登録時は `Found:false` でエラーにしない） |
| 🆓 `GetPrimaryAssetRules` | 指定 `PrimaryAssetId` のマージ済み（Type既定 + 個別上書き）`PrimaryAssetRules` を取得する |
| 🆓 `GetManagedPackageList` | 指定 `PrimaryAssetId` が管理するパッケージ一覧を取得する |
| 🆓 `GetPrimaryAssetLoadList` | 指定 Bundle 条件下で実際にロードされるオブジェクトパスを解決する |
| 🆓 `GetLoadedPrimaryAssets` | 現在ロード中/ロード予定の `PrimaryAssetId` とそのロード済み Bundle 状態を取得する |
| `AddPrimaryAssetType`（要 `PrimaryAssetTypeAdd`） | `PrimaryAssetType` を `PrimaryAssetTypesToScan` に追加（`DefaultGame.ini` へ永続化）し即座にスキャンする |
| `RemovePrimaryAssetType`（要 `PrimaryAssetTypeRemove`） | `PrimaryAssetType` を `PrimaryAssetTypesToScan` から削除（永続化）する。アセットが存在する場合は `Force` 指定がない限り拒否 |
| `SetPrimaryAssetRules`（要 `PrimaryAssetRulesOverride`） | 指定 `PrimaryAssetId` の Rule をメモリ内のみ一時的に上書きする（非永続） |
| `LoadPrimaryAsset`（要 `PrimaryAssetLoad`） | `PrimaryAsset` を明示的にメモリへロードする（ノンブロッキング、PIE中も許可） |
| `UnloadPrimaryAsset`（要 `PrimaryAssetUnload`） | `PrimaryAsset` を明示的にメモリからアンロードする（PIE中は拒否） |

> **Note**: `StartAssetAudit` は**ジョブ型コマンド**の一例で、呼び出しをブロックせずに即座に応答を返し、実際の処理はエディタのフレームをまたいで進む。`uaip_execute` の呼び出しに MCP の `_meta.progressToken` を添えると、応答待ちの間ブリッジがおよそ 5 秒おきに `notifications/progress` を送出する。内容は経過秒数とエディタ自身の状態（`STARTING` / `RUNNING` / `UNRESPONSIVE`）のみで、**ジョブ内部の進捗は含まれない**（それを知りたい場合は `GetAssetAuditStatus` をポーリングする）。この仕組みは `uaip_execute` にのみ適用され（`uaip_run_scenario` は対象外）、クライアントが進捗トークンを送った場合にのみ働く。また、届いた通知を実際に表示するかどうかは MCP クライアント側の実装による。監査ジョブが 1 フレームあたり走査に使う時間の上限は `Config/DefaultUAIP.ini` の `[UAIP.Jobs] AuditStepBudgetMs` で変更できる（既定 `10.0`、`[1.0, 100.0]` の範囲にクランプされる。範囲外を指定してもエラーにはならず自動的に範囲内へ収められる）。


> **Note**: 保存には `SaveAsset` と `UAIP.Editor.Workspace.SaveAllPackages` の 2 つがあり、影響範囲が異なる。`SaveAllPackages` は**未保存のパッケージをすべて**書き込むため、人が編集途中で放置していた無関係な変更まで一緒に確定してしまう。対象が分かっているなら `SaveAsset` で名指しすること。何が書き込まれるかを事前に知りたい場合は `ListDirtyPackages` を呼ぶ — これはエディタ全体保存が参照するのと同じ情報源（`GetDirtyContentPackages` / `GetDirtyWorldPackages`）を使うため、返る一覧と `SaveAllPackages` が書き込む集合は一致する。
>
> `SaveAsset` が対象にするのは**ロード済みかつ未保存の変更を持つパッケージだけ**。未ロードのアセットは未保存の変更を持ちようがないため、ロードして書き戻すことはせず `Skipped`（`Reason: "NotLoaded"`）として返る。すでに保存済みのものも `Skipped`（`NotDirty`）になる。どちらもエラーではない。`/Engine/` と `/Script/` 配下はプロジェクト外へ影響するため `Failed`（`WriteForbidden`）として拒否されるが、呼び出し全体は失敗せず、他のアセットの保存はそのまま行われる。SafetyPolicy が `DisableSave=True` の場合のみ呼び出し全体が `PolicyViolation` になる。
>
> **`ApplyValidationFix` との関係**: バリデータが提供する修正が `FAutoSavingFixer` で包まれていても、UAIP 経由の適用では**ディスクへ書き込まれない**。エンジンの自動保存が人間の確認を求めるモーダルダイアログ経由であり、応答する人がいない非対話実行では成立しないため。この場合 `ApplyValidationFix` は `Applied: true` と `AssetSaved: false` を返すので、**`AssetSaved` が `false` なら `SaveAsset` で明示的に保存する**こと。

### Toolset ブリッジ — Assets（6 件）🧩

`EditorAppToolset`（UE 5.8+、EditorToolset プラグイン）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.Toolset.Assets.*`。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.Toolset.Assets.GetSelectedAssets` | Content Browser で選択中のアセットを取得 |
| `Toolset.Editor.Toolset.Assets.SelectAssets` | Content Browser でアセットを選択（`ContentBrowserNavigate` 必要） |
| `Toolset.Editor.Toolset.Assets.GetContentBrowserPath` | Content Browser の現在フォルダパスを取得 |
| `Toolset.Editor.Toolset.Assets.SetContentBrowserPath` | Content Browser を指定フォルダに移動（`ContentBrowserNavigate` 必要） |
| `Toolset.Editor.Toolset.Assets.OpenEditorForAsset` | アセットをエディタで開く（`AssetWindowControl` 必要） |
| `Toolset.Editor.Toolset.Assets.GetOpenAssets` | アセットエディタで開いているアセットの一覧 |

---

## UAIP.Editor.SemanticSearch 🧩

セマンティックアセット検索とインデックス管理。`SemanticSearch` プラグイン（UE 5.8+、Experimental）と、エディタ環境設定 → プラグイン → Semantic Search で設定した OpenAI API キーが必要です。

| コマンド | 説明 |
|---|---|
| `Search` | 自然言語クエリでプロジェクトアセットを検索（BM25+ベクトルハイブリッド、最大 500 件） |
| `FindSimilar` | 参照アセットに類似するアセットをベクトル類似度で検索 |
| `GetIndexStats` | 現在のインデックス統計（アセット数・最終構築日時）を返す |
| `StartIndexing` | セマンティックインデックスの完全再構築をトリガー（長時間処理・`SemanticSearchEdit` 必要） |
| `CancelIndexing` | 実行中のインデックス構築をキャンセル（`SemanticSearchEdit` 必要） |

### Toolset ブリッジ（2 件）🧩

`SemanticSearchToolset` プラグイン（UE 5.8+）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.SemanticSearch.*`。上記のネイティブ `Search` / `FindSimilar` に相当し、Toolset ブリッジ専用として提供されます（これら 2 件には対応する UAIP ネイティブコマンドは存在しない。ADR `2026-06-25-SemanticSearchToolset-BridgeOnly-Exception.md` 参照）。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.SemanticSearch.Search` | SemanticSearchToolset 経由の BM25+ベクトルハイブリッド検索 |
| `Toolset.Editor.SemanticSearch.FindSimilar` | SemanticSearchToolset 経由のベクトル類似度検索 |

---

## UAIP.Editor.Level

Editor 上でのアクター配置・トランスフォーム・レベルロード。

| コマンド | 説明 |
|---|---|
| 🆓 `ListLevelActors` | 開いているレベルのアクター一覧 |
| `PlaceActorInLevel` | Editor レベルにアクターを配置 |
| `DeleteActorFromLevel` | Editor レベルからアクターを削除 |
| 🆓 `GetActorTransform` | Editor 上のアクターのトランスフォーム取得 |
| `SetActorTransform` | Editor 上のアクターのトランスフォーム設定 |
| `OpenLevel` | エディタビューポートでレベルを開く（File > Open Level） |
| `NewLevel` | テンプレートから新規レベルを作成（EmptyLevel / EmptyOpenWorld / Basic / OpenWorld） |
| `SelectActors` | 指定アクターを Editor レベルで選択（既存選択を置換または追加） |
| 🆓 `ListSelectedActors` | 現在 Editor で選択中のアクター一覧を返す |
| `ClearSelection` | Editor レベルの選択をクリア |
| `FocusOnActors` | 指定アクターにビューポートカメラをフォーカス（アクター省略時は選択中のアクターを対象） |
| 🆓 `GetCameraTransform` | アクティブなレベルエディタビューポートのカメラ位置・回転を取得 |
| `SetCameraTransform` | アクティブなレベルエディタビューポートのカメラ位置・回転を設定 |
| 🆓 `GetVisibleActors` | アクティブなエディタビューポートに現在表示されているアクターを返す（視錐体カリング） |
| 🆓 `ProjectWorldToScreen` | ワールド空間の位置をスクリーン座標に投影 |
| 🆓 `ProjectScreenToWorld` | スクリーン座標からワールドにレイをキャスト（ECC_Visibility ライントレース） |

### Toolset ブリッジ — Level（8 件）🧩

`EditorAppToolset`（UE 5.8+、EditorToolset プラグイン）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.Toolset.Level.*`。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.Toolset.Level.GetSelectedActors` | Level Editor ビューポートで現在選択中のアクターを返す |
| `Toolset.Editor.Toolset.Level.SelectActors` | Level Editor で指定アクターを選択（`EditorActorEdit` 必要） |
| `Toolset.Editor.Toolset.Level.GetCameraTransform` | アクティブビューポートのカメラトランスフォームを取得 |
| `Toolset.Editor.Toolset.Level.SetCameraTransform` | アクティブビューポートのカメラトランスフォームを設定（`EditorViewportControl` 必要） |
| `Toolset.Editor.Toolset.Level.FocusOnActors` | 指定アクターにビューポートをフォーカス（`EditorViewportControl` 必要） |
| `Toolset.Editor.Toolset.Level.GetVisibleActors` | アクティブビューポートに表示されているアクターの一覧 |
| `Toolset.Editor.Toolset.Level.WorldPosToScreenCoords` | ワールド位置をスクリーン空間に投影 |
| `Toolset.Editor.Toolset.Level.ScreenCoordsToWorld` | スクリーン座標をワールド空間に投影（`EditorInspect` 必要） |

---

## UAIP.Editor.Property

アクター・アセット・Blueprint デフォルト・DataTable 行・World / Project 設定のプロパティ読み書き。`Get*` 系コマンドは、シークレットらしきプロパティ値（名前がシークレットパターンに一致・シークレットメタデータあり・ファイルパス型）をネストした struct メンバーも含めて `***` でマスクする — シークレットなメンバーを内包する複合値（struct 等）は、その部分だけでなく値全体がマスク対象になる。`Set*` 系コマンドは 17 種の struct 型（ベクトル・回転・Transform・カラー・`FGuid`・区間型・`FGameplayTag` / `FGameplayTagContainer` / `FGameplayCueTag`・`FBoneReference` など）と `int8` から `uint64` までの全整数幅を書き込み可能。配列・マップ・セット・オブジェクト参照はこれらのコマンドからは引き続き書き込み不可。

| コマンド | 説明 |
|---|---|
| 🆓 `GetActorProperty` | Editor アクターのプロパティ値を取得 |
| `SetActorProperty` | Editor アクターのプロパティを設定 |
| 🆓 `GetWorldSetting` | WorldSettings のプロパティ値を取得 |
| `SetWorldSetting` | WorldSettings のプロパティを設定 |
| 🆓 `GetAssetProperty` | アセット（DataAsset 等）のプロパティ値を取得 |
| `SetAssetProperty` | アセットのプロパティを設定し `MarkPackageDirty` を呼ぶ |
| 🆓 `GetBlueprintDefault` | Blueprint CDO のプロパティ値を取得 |
| `SetBlueprintDefault` | Blueprint CDO のプロパティを設定 |
| 🆓 `GetProjectSetting` | `UDeveloperSettings` CDO のプロパティ値を取得 |
| `SetProjectSetting` | `UDeveloperSettings` CDO のプロパティを設定し `SaveConfig()` を呼ぶ |
| 🆓 `GetDataTableRow` | DataTable 行のプロパティ値を取得 |
| `SetDataTableRow` | DataTable 行のプロパティを設定 |

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

### Toolset ブリッジ — GameplayTags（6 件）🧩

`GameplayTagsToolset` プラグイン（UE 5.8+、Experimental）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.GameplayTags.*`。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.GameplayTags.ListTags` | 登録済みタグ一覧（`ParentTag` 指定でその子孫に限定、最大 2048 件） |
| `Toolset.Editor.GameplayTags.GetTagInfo` | 単一タグの詳細 — Comment・Source・Children |
| `Toolset.Editor.GameplayTags.FindReferencersByTag` | タグを参照するアセットを検索（最大 256 パス） |
| `Toolset.Editor.GameplayTags.AddTag` | 既存の `.ini` タグソースにタグを追加（`GameplayTagEdit` 必要） |
| `Toolset.Editor.GameplayTags.RemoveTag` | タグをプロジェクトタグテーブルから削除。アセット参照は更新**されない**（`GameplayTagEdit` 必要） |
| `Toolset.Editor.GameplayTags.RenameTag` | INI 上のみのリネーム。参照更新もリダイレクト登録も行わないため、通常はネイティブの `RenameGameplayTag` を推奨（`GameplayTagEdit` 必要） |

---

## UAIP.Editor.GameFeatures 🧩

GameFeature Plugin 管理。`GameFeatures` + `GameFeaturesEditor` プラグインが必要です。

| コマンド | 説明 |
|---|---|
| `ListGameFeatures` 🧩 | GameFeature Plugin 一覧（`FilterState`：All / Installed / Mounted / Registered / Loaded / Active） |
| `GetGameFeatureInfo` 🧩 | GFP 詳細（State・Actions・依存関係） |
| `GetGameFeatureActions` 🧩 | GameFeature Plugin の `UGameFeatureData` が宣言する Action 一覧 |
| `CreateGameFeaturePlugin` 🧩 | 新規 GameFeature Plugin のスキャフォールド（名前バリデーション付き） |
| `DeleteGameFeaturePlugin` 🧩 | コンテンツのみの GameFeature Plugin をディスクから削除 |

### Toolset ブリッジ — GameFeatures（4 件）🧩

`GameFeaturesToolset`（UE 5.8+、Experimental）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.GameFeatures.*`。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.GameFeatures.ListGameFeatures` | 登録済み GameFeature Plugin と現在の状態の一覧 |
| `Toolset.Editor.GameFeatures.FindGameFeatureData` | プラグイン名から `UGameFeatureData` アセットの refPath を解決 |
| `Toolset.Editor.GameFeatures.GetActions` | `UGameFeatureData` の Action クラス名一覧（`{"refPath": "..."}` を渡す） |
| `Toolset.Editor.GameFeatures.CreateGameFeaturePlugin` | コンテンツのみの GameFeature Plugin を作成（`GameFeatureCreate` 必要） |

---

## UAIP.Editor.Niagara 🧩

Niagara VFX システム編集。`Niagara` + `NiagaraEditor` プラグインおよび **UE 5.7 以降**が必要です。

### ネイティブ（52）

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

#### スキーマ（7）

| コマンド | 説明 |
|---|---|
| `GetSystemSchema` 🧩 | `UNiagaraSystem` の編集可能なトップレベルプロパティの JSON Schema（システム間で不変・キャッシュ可） |
| `GetEmitterSchema` 🧩 | エミッタの編集可能なトップレベルプロパティの JSON Schema（キャッシュ可） |
| `GetRendererSchema` 🧩 | `RendererClassPath` で指定した `UNiagaraRendererProperties` クラスの JSON Schema |
| `GetDataInterfaceSchema` 🧩 | `DataInterfaceClassPath` で指定した `UNiagaraDataInterface` クラスの JSON Schema |
| `GetStackInputSchema` 🧩 | 単一モジュール入力の型・カテゴリ・`SupportsExpressions` |
| `GetModuleSchema` 🧩 | スタック上のモジュールインスタンスの入出力一覧 |
| `GetModuleSchemaFromAsset` 🧩 | NiagaraSystem を介さず `UNiagaraScript` モジュールアセットの入出力を取得 |

#### トポロジと Dynamic Input（7）

| コマンド | 説明 |
|---|---|
| `GetEmitterTopology` 🧩 | エミッタの全スクリプトスタックとモジュールを含むモジュールスタックトポロジ |
| `GetScriptStackTopology` 🧩 | 単一スクリプトスタックのモジュールトポロジ |
| `GetModuleTopology` 🧩 | 単一モジュールの入力トポロジ |
| `GetStackInputTopology` 🧩 | 単一入力の完全なトポロジ — 型・値モード・現在値・再帰的な dynamic input の子 |
| `GetDynamicInputSchema` 🧩 | スタック上の dynamic input スクリプトインスタンスの入出力一覧 |
| `GetDynamicInputSchemaFromAsset` 🧩 | NiagaraSystem を介さず `UNiagaraScript` dynamic input アセットの入出力を取得 |
| `GetAvailableDynamicInputs` 🧩 | 指定モジュール入力に適用できる dynamic input スクリプト一覧 |

#### スタック Issue（2）

| コマンド | 説明 |
|---|---|
| `GetStackIssues` 🧩 | システム全体のスタック Issue（エラー / 警告 / 情報、dismiss 済みを含む）と `IssueId`・`FixId` |
| `ApplyStackIssueFix` 🧩 | `IssueId` + `FixId` を指定して Fix 形式の自動修正を適用（Link 形式は拒否・`NiagaraStackAutoFix` 必要） |

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
| `AddSetParametersModule` 🧩 | Set Parameters モジュールをスタックに追加し、初期パラメータエントリを登録する。`DefaultValue` フィールドは一般的な型（float / int / bool / struct）で適用される。 |
| `AddSetParameterEntry` 🧩 | 既存の Set Parameters モジュールにパラメータエントリを追加する。`ScriptName`（例：`Spawn` / `Update`）が必須。`DefaultValue` フィールドは一般的な型（float / int / bool / struct）で適用される。 |
| `RemoveSetParameterEntry` 🧩 | Set Parameters モジュールからパラメータエントリを削除する。`ScriptName`（例：`Spawn` / `Update`）が必須。 |

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
| `GetDataflowGraphInfo` 🧩 | グラフのノード / エッジ / 変数を取得（JSON）。各ノードは `NodeName`（グラフ内の実名。`SetGroomDataflowAsset` の `TerminalNodeName` 等で指定するのはこちら）と `DisplayName`（ノード型の表示名）の両方を返す |
| `ListDataflowNodeTypes` 🧩 | 利用可能な Dataflow ノードタイプ一覧 |
| `AddDataflowNode` 🧩 | Dataflow グラフにノードを追加。任意の `NodeName` でグラフ内の名前を指定できる（省略時はノード型名を基底とした一意名を採番）。確定した名前は応答の `NodeName` に含まれる |
| `RemoveDataflowNode` 🧩 | Dataflow グラフからノードを削除 |
| `ConnectDataflowPins` 🧩 | 2 ピンを接続 |
| `DisconnectDataflowPins` 🧩 | ピン接続を切断 |
| `ListDataflowVariables` 🧩 | グラフ変数一覧 |
| `GetDataflowNodeProperty` 🧩 | ノードの `EditAnywhere` プロパティ値を取得（プリミティブ / enum / FName / FString / 単純構造体） |
| `SetDataflowNodeProperty` 🧩 | ノードの `EditAnywhere` プロパティ値を設定。ドメイン非依存（Cloth の Weight Map・シミュレーション設定ノード等から利用される）。トップレベルのハードなオブジェクト / クラス参照（例: `TObjectPtr<UGroomAsset>`）も書き込める — 値は**既にロード済み**のアセットのオブジェクトパスで、`DataflowGraphEdit` に加えて `DataflowReferenceEdit` が必要。プロパティ書き込みが副作用でアセットをロードすることはない。ソフト / ウィーク / レイジー参照と、参照を含む構造体・配列は引き続き書き込めない |

### Toolset ブリッジ — Dataflow（7 件）🧩

`DataflowAgentToolset`（UE 5.8+）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.DataflowAgent.*`。編集系は `DataflowGraphEdit` が必要です。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.DataflowAgent.ListDataflowNodeTypes` | 利用可能な Dataflow ノード型の一覧（common 型のみ） |
| `Toolset.Editor.DataflowAgent.GetDataflowGraphInfo` | Dataflow アセットのノード・接続構造 |
| `Toolset.Editor.DataflowAgent.ListDataflowVariables` | Dataflow アセットの変数一覧 |
| `Toolset.Editor.DataflowAgent.AddDataflowNode` | Dataflow グラフにノードを追加（`DataflowGraphEdit` 必要） |
| `Toolset.Editor.DataflowAgent.RemoveDataflowNode` | Dataflow グラフからノードを削除（`DataflowGraphEdit` 必要） |
| `Toolset.Editor.DataflowAgent.ConnectDataflowPins` | 2 ピンを接続（`DataflowGraphEdit` 必要） |
| `Toolset.Editor.DataflowAgent.DisconnectDataflowPins` | ピン接続を切断（`DataflowGraphEdit` 必要） |

---

## UAIP.Editor.ChaosClothAsset 🧩

Chaos Cloth Asset 編集と `ChaosClothAssetToolset` ブリッジ（UE 5.8, Experimental）。`ChaosClothAsset` プラグイン群が必要です。

| コマンド | 説明 |
|---|---|
| `CreateClothingAsset` | Skeletal Mesh から Clothing Asset を作成 |
| `AssignClothingToSection` | Clothing Asset を Skeletal Mesh の LOD/セクションにバインド |
| `RemoveClothingFromSection` | セクションから Clothing Asset のバインドを解除（破壊的・不可逆） |
| `ListClothingAssets` | Skeletal Mesh にバインド済みの Clothing Asset 一覧 |
| `GetSectionClothing` | 指定した LOD/セクションにバインドされている Clothing Asset を取得 |
| `ConvertClothingAssetCommonToChaosClothAsset` | legacy `UClothingAssetCommon` を `UChaosClothAsset` に変換（Experimental、LOD0のみ） |
| `GetClothAssetInfo` | LOD数・Sim/Render Mesh頂点数・参照している `UDataflow` アセットパス・Weight Map属性名一覧を取得 |
| `SetClothWeightMapVertexValues` | Weight Map ノードの頂点重み配列を直接設定（破壊的） |
| `SetClothMeshImportSource` | Import Dataflow ノード（`SkeletalMeshImport`/`StaticMeshImport`）にインポート元の SkeletalMesh/StaticMesh 参照を設定。ノード種別は自動判定、既存参照の上書きには `AllowOverwrite` が必要（破壊的） |
| `CreateLegacyClothingAsset` | 既存 SkeletalMesh の描画セクションからシミュレーションメッシュを抽出し、新規 legacy `UClothingAssetCommon` を作成 |

`GetClothAssetInfo` が返す `UDataflow` 参照パスを `UAIP.Editor.Dataflow.*` コマンドに渡すことで、Weight Map・シミュレーション設定ノードのプロパティを汎用的に編集できます。

### Toolset ブリッジ（6）

`ChaosClothAssetToolset` の6関数をそのままミラー。プロバイダ：`Toolset.Editor.ChaosClothAsset.*`。UE 5.8+ かつ `ChaosClothAssetToolset` + `ToolsetRegistry` 有効時のみ利用可能。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.ChaosClothAsset.CreateClothingAsset` | `ChaosClothAssetToolset` への委譲 |
| `Toolset.Editor.ChaosClothAsset.AssignClothingToSection` | `ChaosClothAssetToolset` への委譲 |
| `Toolset.Editor.ChaosClothAsset.RemoveClothingFromSection` | `ChaosClothAssetToolset` への委譲 |
| `Toolset.Editor.ChaosClothAsset.ListClothingAssets` | `ChaosClothAssetToolset` への委譲 |
| `Toolset.Editor.ChaosClothAsset.GetSectionClothing` | `ChaosClothAssetToolset` への委譲 |
| `Toolset.Editor.ChaosClothAsset.ConvertClothingAssetCommonToChaosClothAsset` | `ChaosClothAssetToolset` への委譲 |

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

## UAIP.Editor.MetaHuman 🧩

MetaHuman キャラクターのオーサリング — アセット作成、体型 / 肌 / 眼 / メイク設定、顔の造形、コンフォーム・フィッティング、クラウドリギング、テクスチャ合成、ワードローブ、プレビュー、アセットビルドパイプライン。`MetaHumanCharacter` プラグインが必要です（無効な場合、これらのコマンドは一切登録されません）。

編集系コマンドは必要に応じて MetaHuman 編集セッションを開き、そのまま保持します（同一キャラクターに対する連続実行で再オープンのコストを払わないため）。セッションを開くこと自体が編集モードへの移行であるため、**このドメインの読み取り系コマンドの多くは読み取り専用ではありません** — `MetaHumanEdit` を必要とし、SafetyPolicy が読み取り専用モードのときは拒否されます。一連の作業が終わったら `ReleaseEditSession` を呼んでください。唯一の例外は `GetViewportSettings` で、`EditorInspect` のみで実行できます。

**⬆️ = UE 5.8 以降専用。** 以下 56 コマンドのうち 14 コマンドは UE 5.7 に存在しないエンジン API に依存しています。UE 5.7 でも登録自体は行われますが、`uaip_list_commands` の既定応答には現れず、`HiddenCount` と `HiddenReasons.HandlerUnavailable` に計上されます。`IncludeUnavailable=true` を指定すると `Available: false` として明示的に列挙されます。`uaip_describe_command` はこのフィルタに関わらず常に表示します。実行すると `CommandNotFound` ではなく `PolicyViolation` が返ります。記号のないコマンドは UE 5.7 / UE 5.8 の両方で動作します。この記号は本セクション限定の表記です。

### ネイティブ（56）

#### 作成（1）

| コマンド | 説明 |
|---|---|
| `CreateMetaHumanCharacter` | デフォルトテンプレートから MetaHuman キャラクターアセットを新規作成しディスクへ書き出し（パッケージパスは `/Game/` 配下必須、`MetaHumanAssetCreate` 必須） |

#### 体型・肌・眼（8）

| コマンド | 説明 |
|---|---|
| `GetBodyConstraints` | 体型制約を全件取得（現在の目標寸法・体型ソルブへの参加有無・許容範囲、JSON artifact）。名前はデータ駆動のため `SetBodyConstraints` の前に本コマンドで列挙する |
| `SetBodyConstraints` | 名前を指定して体型制約を更新し体型を再評価（指定しなかった制約は現在値を保持、全エントリを検証してから適用） |
| `GetBodyShape` | 簡易体型を取得 — 男性寄り / 女性寄り・体脂肪・筋肉量（0..1 正規化）と身長（cm） |
| `SetBodyShape` | 簡易体型を設定し体型を再評価（省略値は変更なし、範囲外はクランプせず拒否） |
| `GetSkinSettings` | 肌設定を全件取得 — 肌トーン（明度 / 赤み）、テクスチャバリアントインデックス、ラフネス、手のひらと爪、そばかす、部位別トーンアクセント |
| `SetSkinTone` | 肌トーンの 2 軸（明度 / 赤み）のみを設定。その他の肌設定は変更しない |
| `GetEyeSettings` | 両眼を全件取得 — Iris / Pupil / Cornea / Sclera の 4 グループ |
| `SetEyeColor` | 指定した色温度・明度を両眼の虹彩プライマリ / セカンダリカラーへ書き込み |

#### 外見詳細（8）

| コマンド | 説明 |
|---|---|
| `SetSkinSettings` | 肌設定を部分更新（省略フィールドは現在値を保持、範囲外はクランプせず拒否） |
| `GetMakeupSettings` | メイク設定を取得 — ファンデーション・アイメイク・チーク・リップ |
| `SetMakeupSettings` | メイク設定を部分更新（スタイル名はエンジン側の名前と完全一致が必要） |
| `GetHeadModelSettings` | まつげのスタイル・色と、歯の形状・色の設定を全件取得 |
| `SetHeadModelSettings` | ヘッドモデル設定を部分更新 |
| `SetEyeSettings` | 眼を部分更新。左右を個別に指定し、Iris / Pupil / Cornea / Sclera の 4 グループを扱う |
| `GetFaceEvaluationSettings` | 顔の全体偏差・微細サーフェス偏差・頭部の均一スケールを取得 |
| `SetFaceEvaluationSettings` | 顔評価設定を部分更新 |

#### 顔の造形（9）

| コマンド | 説明 |
|---|---|
| `GetFaceModelCoefficients` ⬆️ | 内部フェイスモデルの係数をフラットな数値配列として取得（JSON artifact）。同じ配列を戻せば形状を復元できる |
| `SetFaceModelCoefficients` ⬆️ | フェイスモデルの係数を書き込み（配列長は `GetFaceModelCoefficients` の値と完全一致が必要、それ以外は拒否） |
| `GetFaceLandmarks` | 顔のランドマーク位置を JSON artifact として取得。配列内の位置が `TranslateFaceLandmarks` の指定するインデックスになる |
| `TranslateFaceLandmarks` | 指定したランドマークを対応する差分だけ移動（1 件でも不正なら何も適用しない） |
| `CommitFaceState` | 蓄積された造形編集をアセットへコミット（造形系コマンドは単体ではコミットしない） |
| `ImportFaceFromDna` | プロジェクトディレクトリ内の `.dna` ファイルから顔を差し替え（`MetaHumanFileImport` 必須） |
| `ImportFaceFromTemplate` | MetaHuman ヘッドと同一トポロジのテンプレートヘッドメッシュに顔をフィット |
| `ImportFaceFromIdentity` | MetaHuman Identity アセットのコンフォーム済みメッシュに顔をフィット（Identity はコンフォーム済みである必要あり） |
| `CompareFaceState` | 2 キャラクターの全対応頂点・頂点法線が `Tolerance` 以内かを判定（真偽値のみ、頂点単位の内訳は返さない） |

#### コンフォームとフィッティング（10）

| コマンド | 説明 |
|---|---|
| `GetMeshDataForConforming` ⬆️ | Static / Skeletal Mesh の頂点と三角形インデックスを、コンフォーム系コマンドがターゲットとして受け取る形式で JSON artifact へ出力 |
| `ConformBodyToTarget` | 指定頂点に体型をコンフォーム（手足のジョイントをメッシュから推定するオプションあり）。ターゲットは `MeshDataArtifactId` またはインライン `Vertices` で指定 |
| `ConformFaceToTargetMeshes` ⬆️ | ターゲットメッシュへ寄せる非同期ソルブを開始。成功は「開始した」ことを意味するため `GetAsyncConformState` をポーリングする |
| `AlignToTargetMeshes` ⬆️ | 形状を変えずに移動・回転・スケールでターゲットメッシュへ剛体アラインを開始。`ConformFaceToTargetMeshes` の前に実行する |
| `RefineVerticesToTarget` ⬆️ | パラメトリックモデル単体では表現できない部分まで頂点を寄せるリファインを開始。コンフォーム完了後に実行する |
| `CommitPosedStateAsAPose` ⬆️ | コンフォーム済みボディを MetaHuman A ポーズで評価し、そこから顔ステートを再構築（通常どおりポーズ・アニメーションできる状態にする） |
| `FitStateToTargetVertices` | 反復ソルブを使わず、MetaHuman ヘッドのトポロジ・頂点順の目標頂点へ 1 パスでヘッドをフィット |
| `FitFaceFromBodyWithEyesTeethTemplate` ⬆️ | 現在の体型からヘッドを再構築し、眼と歯をテンプレートメッシュで置き換え |
| `FitFaceFromBodyWithEyesTeethDna` ⬆️ | 同上（眼と歯は顔 DNA ファイルから取得）。ヘッド形状は体型由来のため顔のインポート手段ではない（`MetaHumanFileImport` 必須） |
| `GetAsyncConformState` ⬆️ | コンフォーム / アライン / リファインの実行中かを取得。エンジンが完了イベントを提供しないため `bIsRunning` が false になるまでポーリングする |

#### ビルドパイプライン（6）

| コマンド | 説明 |
|---|---|
| `RequestTextureSources` | 高解像度フェイステクスチャの合成を開始し、リクエスト発行時点で返す。処理はバックグラウンドで数分継続する（`MetaHumanTextureSynthesis` 必須） |
| `GetTextureSourceState` | テクスチャ合成が実行中かどうか、および合成済みテクスチャを保持しているかをポーリング |
| `RequestAutoRigging` | フェイスリグの生成を開始。⚠️ **キャラクターの顔データを Epic のクラウドリギングサービスへアップロードします** — リグはリモートで生成されてアセットへダウンロードされるため、Epic アカウントへのサインインとネットワーク接続が必要で、キャラクターデータはこのマシンの外へ出ます。リギングには通常数分かかるため `GetRiggingState` をポーリングする（`MetaHumanCloudRigging` 必須） |
| `GetRiggingState` | リギング状態（`Unrigged` / `RigPending` / `Rigged`）をポーリング。リクエスト終了後に `Unrigged` ならば失敗（多くはサインインまたは接続の問題） |
| `CanBuildMetaHuman` | `BuildMetaHuman` が当該キャラクターを受け付けるか、受け付けない場合は最初の未充足要件を返す。ビルド前に必ず呼ぶ |
| `BuildMetaHuman` | キャラクターをコレクション・インスタンス・キャラクターブループリントとして新規サブフォルダに組み立てる。⚠️ **ビルド完了までゲームスレッドを占有します（数秒〜数分）。** エンジンが進捗ダイアログを表示して再描画を続けるため、エディタは応答しなくなるのではなく画面を見られる状態を保ちますが、ビルドが返るまで他のコマンドは一切実行されません。ビルドが長引くと HTTP トランスポート自体の非同期コマンドタイムアウト（120 秒）を超えることがあり、その場合 `Timeout` が返りますが、**エディタ側ではビルドが実行を継続している可能性があります**。すぐに再実行せず、まず `uaip_get_editor_status` を呼んで `RecommendedAction`（`WAIT` が期待値）に従ってください。artifact はビルドが実際に完了した後になって生成される場合があります。先に `CanBuildMetaHuman` を呼ぶこと（オートリギングと合成済みテクスチャが揃っていないビルドは必ず失敗します）。失敗時は出力フォルダ配下に作成されたアセットが削除されます。出力フォルダが既存の場合は拒否されます。ビルド実行中は他の MetaHuman コマンドが拒否されます（`MetaHumanBuild` 必須） |

#### プレビュー（3）

| コマンド | 説明 |
|---|---|
| `GetViewportSettings` | プレビュービューポート設定を取得 — ライティング環境・ライト回転・背景色・LOD・ヘアカード / ストランドの切り替え・プレビュー用スキンマテリアル・カメラフレーミング（読み取り専用、`EditorInspect` のみで実行可能） |
| `SetViewportSettings` | プレビュービューポート設定を部分更新（最低 1 項目の指定が必要、範囲外はクランプせず拒否）。`PreviewMaterial` はエディタのビューポートツールバーの表示名に合わせてあり、**色を確認するためにキャプチャする前には `Skin` を選ぶこと** — `Topology` はトポロジ可視化で肌・メイク・眼の色を完全に隠し、`Clay` はテクスチャなしのグレー。`CameraFrame` は常にキャラクターへ記録されるが、プレビューカメラが実際に動くのは MetaHuman キャラクターエディタで開いている間だけ。カスタムライティング環境はここからは選べない — サポート対象の 2 つのエンジンバージョンで表現が異なるため、エディタのビューポートツールバーで設定する |
| `RefreshCharacterPreview` ⬆️ | 保留中のコレクション編集をキャラクターへ反映し、エディタパイプラインを再実行してプレビューへ反映 |

#### ワードローブ（10）

| コマンド | 説明 |
|---|---|
| `ListWardrobeSlots` | キャラクターのコレクションが定義するワードローブスロットと各スロットのアイテム数を列挙。名前は実行時にパイプラインから取得されるため `AssignWardrobeItem` の前に本コマンドで確認する |
| `ListWardrobeItems` | ワードローブアイテムを列挙（スロット指定は任意）。各エントリは不透明なハンドル `ItemKey` を持つ |
| `GetWardrobeItemInfo` | ワードローブアイテム 1 件を取得 — 占有スロット・表示名・ラップしているアセットのパッケージパス |
| `AssignWardrobeItem` ⬆️ | グルームやガーメントなどのアセットをワードローブスロットへ割り当てて選択し、プレビューを再構築（`RefreshCharacterPreview` の追加呼び出しは不要） |
| `RemoveWardrobeItem` ⬆️ | ワードローブアイテムを削除（着用中の場合はスロット選択を先に解除）し、プレビューを再構築 |
| `ReplaceWardrobeItem` ⬆️ | ワードローブアイテムを、元のアイテムが占有していたスロットのまま別アセットへ置き換え、プレビューを再構築 |
| `GetWardrobeItem` | パッケージパスで指定したワードローブアイテムアセットを 1 件取得 — 元アセットのパッケージパス・パイプラインのクラスパス・サムネイル画像のパス・サムネイル名・単体アセットかどうか。対象はアイテムアセットそのものであり、キャラクターが着用しているアイテムではない（後者は `GetWardrobeItemInfo` で、キャラクターパスと `ItemKey` を指定する） |
| `SetWardrobeItem` | ワードローブアイテムアセットの元アセット・サムネイル画像・サムネイル名を部分更新（省略フィールドは現在値を保持、ただし最低 1 項目の指定が必要。パス項目に空文字列を渡すとアセットの指定ではなくその参照のクリアになる）。パイプラインは本コマンドでは設定できず `SetWardrobeItemPipeline` を使う |
| `SetWardrobeItemPipeline` | ワードローブアイテムアセットへ指定クラスのパイプラインを設定し、元のパイプラインを置き換える。`PipelineClassPath` はクラスパスのため、組み立てずに `ListItemPipelineClasses` の結果から選ぶ |
| `ListItemPipelineClasses` | ワードローブアイテムアセットのビルドに使えるアイテムパイプラインクラスを表示名付きで列挙。存在するクラスはプロジェクトがロードしているプラグインに依存する。abstract・deprecated・ホットリロードで置換されたクラスは除外されるため、列挙されたクラスはすべて `SetWardrobeItemPipeline` が受け付ける |

#### セッション（1）

| コマンド | 説明 |
|---|---|
| `ReleaseEditSession` | キャラクターに対して保持している編集セッションを解放（実行中の処理を中断することはありません） |

### Toolset ブリッジ（9）🧩

`MetaHumanGenerator` Python Toolset へのブリッジコマンド。プロバイダ：`Toolset.Editor.MetaHuman.*`。UE 5.8+ かつ `MetaHumanGenerator` + `ToolsetRegistry` 有効時のみ利用可能で、UE 5.7 ではブリッジプロバイダ自体が登録されないため `CommandNotFound` になります。委譲先のエンジン Python Toolset 自体が experimental であるため `Stability: Experimental` です。

ネイティブコマンドと異なり、`Create` 以外のブリッジコマンドは `BeginEdit` が返すセッション参照を必須とします。そのため SafetyPolicy が読み取り専用のときはいずれも実行できません。必要な Capability は `MetaHumanEdit`（`Create` のみ `MetaHumanAssetCreate`）です。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.MetaHuman.BeginEdit` | キャラクターに対する編集セッションを開き、他のブリッジコマンドが受け取るセッション参照を返す |
| `Toolset.Editor.MetaHuman.EndEdit` | `BeginEdit` で開いたセッションを閉じ、キャラクターをエディタの編集対象から外す |
| `Toolset.Editor.MetaHuman.GetBodyShape` | セッション対象キャラクターの簡易体型 4 値を返す |
| `Toolset.Editor.MetaHuman.SetBodyShape` | 簡易体型 4 値を設定し、体型変更に伴うネック領域の再構築まで含めてコミット（範囲外の値は拒否されず Toolset 側でクランプされる — ネイティブコマンドとの唯一の挙動差） |
| `Toolset.Editor.MetaHuman.GetSkinTone` | セッション対象キャラクターの肌トーン 2 値（明度・赤み）を返す |
| `Toolset.Editor.MetaHuman.SetSkinTone` | 明度・赤みを設定して肌設定をコミット（その他の肌設定は変更しない） |
| `Toolset.Editor.MetaHuman.GetEyeColor` | 右眼の虹彩プライマリカラーから読み取った色温度・明度を返す |
| `Toolset.Editor.MetaHuman.SetEyeColor` | 1 つの眼色を両眼へ設定して眼設定をコミット（左右は常に一致する） |
| `Toolset.Editor.MetaHuman.Create` | `/Game/` 配下に MetaHuman キャラクターアセットを新規作成し、その参照を返す（`MetaHumanAssetCreate` 必須） |

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
| `ListDataTableRowStructs` | 行構造に使える `FTableRowBase` 派生 struct の一覧 — `ClassPath` を `CreateAsset` の `FactoryParams.RowStructPath` に渡す |

---

## UAIP.Editor.AnimBlueprint

Anim Blueprint グラフと StateMachine 編集。

| コマンド | 説明 |
|---|---|
| `GetAnimBlueprintInfo` | AnimGraph ノード一覧と StateMachine 構造（PIE 中は degraded モード） |
| `GetAvailableAnimGraphNodeClasses` | `UAnimGraphNode_Base` サブクラス一覧 — `ClassPath` を `AddAnimGraphNode` に渡す |
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

## UAIP.Editor.SoundSettings

SoundClass ツリー・SoundAttenuation・SoundMix アセットのプロパティ設定。

| コマンド | 説明 |
|---|---|
| `GetSoundClassInfo` | SoundClass の Properties（FSoundClassProperties）・ChildClasses・ParentClass・PassiveSoundMixModifiers を返す |
| `SetSoundClassSettings` | SoundClass の FSoundClassProperties フィールドを 1 プロパティ単位で設定（LoadingBehavior の変更は拒否） |
| `ListSoundClasses` | プロジェクト内 SoundClass を列挙（AssetPath / ParentClassPath / ChildClassPaths；最大 1000 件） |
| `AddSoundClassChild` | SoundClass 階層に子クラスを追加（循環参照検出・深度上限 32） |
| `RemoveSoundClassChild` | SoundClass 階層から子クラスを削除し、双方向リンクを解除 |
| `GetSoundAttenuationInfo` | SoundAttenuation の FSoundAttenuationSettings を JSON で返す |
| `SetSoundAttenuationSettings` | SoundAttenuation の FSoundAttenuationSettings フィールドを 1 プロパティ単位で設定 |
| `ListSoundAttenuations` | プロジェクト内 SoundAttenuation を列挙（最大 1000 件） |
| `GetSoundMixInfo` | SoundMix の全設定（EQ・SoundClassEffects・Fade タイミング）を JSON で返す |
| `SetSoundMixSettings` | SoundMix のトップレベルフィールドを 1 プロパティ単位で設定（SoundClassEffects 配列の直接書き込みは拒否） |
| `SetSoundMixAdjuster` | SoundClassAdjuster を追加または更新（SoundClass パスをキーとした Upsert；省略フィールドは既存値を維持または既定値） |
| `RemoveSoundMixAdjuster` | SoundMix から対象 SoundClass の SoundClassAdjuster を削除 |
| `ListSoundMixes` | プロジェクト内 SoundMix を列挙（最大 1000 件） |

---

## UAIP.Editor.MVVM 🧩

ViewModel Blueprint のプロパティ管理、View Binding / Event の作成、Widget への ViewModel 接続管理。`ModelViewViewModel` プラグインが必要（UE 5.5 以降はデフォルト有効）。

### Native（26）

#### ViewModel プロパティ管理

| コマンド | 説明 |
|---|---|
| `ListViewModelClasses` | AssetRegistry から `UMVVMViewModelBase` 派生 Blueprint クラスを列挙する（`SearchPath` フィルタ省略可；最大 1000 件） |
| `AddViewModelProperty` | ViewModel Blueprint にプロパティを追加する（7 種類の PropertyType；`DefaultValue` 省略可；Getter / Setter 生成省略可） |
| `RemoveViewModelProperty` | ViewModel Blueprint からプロパティを名前指定で削除する |
| `ListViewModelProperties` | ViewModel Blueprint の全プロパティを一覧返却する |

#### Widget ViewModel 接続管理

| コマンド | 説明 |
|---|---|
| `AddViewModelToWidget` | WidgetBlueprint に ViewModel を接続する（`/Game/` 配下の `UMVVMViewModelBase` 派生クラスのみ許可） |
| `RemoveViewModelFromWidget` | WidgetBlueprint から ViewModel エントリを名前指定で削除する |
| `ListWidgetViewModels` | WidgetBlueprint に接続済みの ViewModel 一覧を返す |
| `RenameViewModelInWidget` | WidgetBlueprint 内の ViewModel エントリ名を変更する |
| `ReparentViewModelInWidget` | WidgetBlueprint 内の ViewModel エントリのクラスを変更する |

#### View Binding 操作

| コマンド | 説明 |
|---|---|
| `AddViewBinding` | WidgetBlueprint に View Binding を追加する |
| `RemoveViewBinding` | `BindingId` 指定で WidgetBlueprint の View Binding を削除する |
| `ListViewBindings` | WidgetBlueprint の全 View Binding を一覧返却する |
| `GetViewBinding` | `BindingId` 指定で View Binding の詳細を返す |
| `UpdateViewBinding` | View Binding のフィールドを部分更新する |
| `SetViewBindingEnabled` | View Binding の有効・無効を切り替える |
| `SetViewBindingConversionFunction` | View Binding に変換関数を設定または解除する |
| `SetViewBindingExecutionMode` | View Binding の実行モードを設定する |
| `ListConversionFunctions` | WidgetBlueprint に適用可能な変換関数を列挙する（大規模プロジェクトでは `SearchPath` フィルタ推奨） |

#### View Event 操作

| コマンド | 説明 |
|---|---|
| `AddViewEvent` | WidgetBlueprint に View Event を追加する（戻り値: `EventId` 文字列；空文字列なら失敗） |
| `RemoveViewEvent` | WidgetBlueprint から View Event を削除する |
| `ListViewEvents` | WidgetBlueprint の全 View Event を一覧返却する |

#### ViewModel ソース設定

| コマンド | 説明 |
|---|---|
| `SetViewModelSource` | ViewModel エントリの `CreationType` を変更する（Remove + Add ラウンドトリップ実装；`Context` タイプは UE 5.8 以降のみ） |
| `GetViewModelSource` | ViewModel エントリの現在のソース設定を返す |

#### 観察・検証

| コマンド | 説明 |
|---|---|
| `GetWidgetBindableProperties` | WidgetBlueprint のバインド可能プロパティを列挙する（ウィジェットプロパティ・ViewModel プロパティ） |
| `ValidateViewBindings` | WidgetBlueprint の全 View Binding を検証する（大規模プロジェクトではコスト高） |
| `GetMVVMViewInfo` | WidgetBlueprint の MVVM 設定サマリを返す（MVVM 未設定時は `bMVVMConfigured: false` の空応答） |

### Toolset ブリッジ（9）🧩

`MVVMToolset` プラグイン（UE 5.8 以上）経由のブリッジコマンド。プロバイダ: `Toolset.MVVM.*`。`CreateViewModel` および `ListViewModels` はブリッジ固有；その他はネイティブコマンドに対応する。

| コマンド | 説明 |
|---|---|
| `Toolset.MVVM.CreateViewModel` | ViewModel Blueprint アセットを作成する |
| `Toolset.MVVM.AddViewModelProperty` | ViewModel Blueprint にプロパティを追加する |
| `Toolset.MVVM.ListViewModels` | ViewModel クラスを列挙する（クラス型フィルタ方式） |
| `Toolset.MVVM.ListWidgetViewModels` | WidgetBlueprint に接続済みの ViewModel を列挙する |
| `Toolset.MVVM.AddViewModelToWidget` | WidgetBlueprint に ViewModel を接続する |
| `Toolset.MVVM.ListWidgetViewBindings` | WidgetBlueprint の View Binding 一覧を返す |
| `Toolset.MVVM.RemoveWidgetViewBinding` | WidgetBlueprint から View Binding を削除する |
| `Toolset.MVVM.CreateViewBinding` | WidgetBlueprint に View Binding を作成する |
| `Toolset.MVVM.ListConversionFunctions` | 利用可能な変換関数を列挙する |

---

## UAIP.Editor.BehaviorTree

Behavior Tree グラフ編集と Blackboard キー管理。

| コマンド | 説明 |
|---|---|
| `GetBehaviorTreeNodeList` | 全ノードのフラットな一覧 — `NodeGuid`・`NodeClass`・`DisplayName`・`Depth`（0 = ルート Composite）・`ParentNodeGuid` |
| `GetBehaviorTreeSubtree` | `NodeGuid` を起点としたサブツリー（Composite / Task / Decorator / Service）を再帰 JSON で返す（`MaxDepth` 1〜32） |
| `GetAvailableBTCompositeClasses` | `UBTCompositeNode` サブクラス一覧 — `ClassPath` を `AddBehaviorTreeCompositeNode` に渡す |
| `GetAvailableBTTaskClasses` | `UBTTaskNode` サブクラス一覧 — `ClassPath` を `AddBehaviorTreeTaskNode` に渡す |
| `GetAvailableBTDecoratorClasses` | `UBTDecorator` サブクラス一覧 — `ClassPath` を `AddBehaviorTreeDecoratorNode` に渡す |
| `GetAvailableBTServiceClasses` | `UBTService` サブクラス一覧 — `ClassPath` を `AddBehaviorTreeServiceNode` に渡す |
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

### Toolset ブリッジ — AIModule（7 件）🧩

`AIModuleToolset`（UE 5.8+、Experimental）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.AIModule.*`。観測専用です。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.AIModule.GetBlackboard` | BehaviorTree に紐づく Blackboard アセット |
| `Toolset.Editor.AIModule.GetRootDecorators` | ルート Composite ノードに附加された Decorator 一覧 |
| `Toolset.Editor.AIModule.ListNodes` | 全ノードのインデックスと型の一覧 |
| `Toolset.Editor.AIModule.GetNodeDepth` | インデックス指定した単一ノードの深さ |
| `Toolset.Editor.AIModule.GetNodeDepths` | 全ノードの深さをフラットな一覧で返す |
| `Toolset.Editor.AIModule.GetChildren` | refPath で指定した Composite ノードの直下の子 |
| `Toolset.Editor.AIModule.GetSubtree` | refPath で指定したノードを起点とするサブツリー |

---

## UAIP.Editor.MetaSound 🧩

MetaSound グラフ編集。`Metasound` プラグインが必要です。

| コマンド | 説明 |
|---|---|
| `GetMetaSoundInfo` 🧩 | MetaSoundSource / MetaSoundPatch のグラフトポロジー（ノード一覧・接続・I/O 頂点） |
| `GetAvailableMetaSoundNodeClasses` 🧩 | Frontend レジストリのノードクラス一覧（`ClassName`・`Variant`・`MajorVersion`・`DisplayName`）。`AddMetaSoundNode` の引数に使う。エンジン標準の名前空間に絞り込み済み |
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
| `GetAvailableEQSGeneratorClasses` 🧩 | `UEnvQueryGenerator` サブクラス一覧 — `ClassPath` を `AddEQSGenerator` に渡す |
| `GetAvailableEQSTestClasses` 🧩 | `UEnvQueryTest` サブクラス一覧 — `ClassPath` を `AddEQSTest` に渡す |
| `AddEQSGenerator` 🧩 | Generator Option を追加（GeneratorClass・6 ステップ allowlist） |
| `RemoveEQSGenerator` 🧩 | NodeId 指定で Generator Option を削除（配下 Test も一括削除） |
| `AddEQSTest` 🧩 | Generator Option に Test を追加 |
| `RemoveEQSTest` 🧩 | NodeId 指定で Test を削除 |
| `SetEQSGeneratorProperty` 🧩 | Generator プロパティを設定（汎用 ImportText_Direct） |
| `SetEQSTestProperty` 🧩 | Test プロパティを設定（`param:<Name>` → `UAIDataProvider_QueryParams`） |

---

## UAIP.Editor.Sequencer

LevelSequence 編集 — トラック・セクション・キーフレーム・再生・バインド。

### ネイティブ（123）

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

#### AnimMixer（36、オプショナル `MovieSceneAnimMixer`）

| コマンド | 説明 |
|---|---|
| `GetAnimMixerTrackInfo` | AnimMixer トラック情報を取得 |
| `GetMixerLayers` | バインディングの全 AnimMixer レイヤーの概要 |
| `GetMixerLayerCount` | バインディングの AnimMixer トラックのレイヤー数 |
| `GetLayerName` | レイヤーの表示名を取得 |
| `SetLayerName` | レイヤーの表示名を設定 |
| `GetLayerIndex` | 表示名からレイヤーの 0 始まりインデックスを取得（存在しなければ `NotFound`） |
| `GetLayerSections` | レイヤー内の全アニメーションセクション |
| `IsLayerEmpty` | レイヤーにアニメーションセクションが無いかどうか |
| `InsertMixerLayer` | 指定インデックスに空レイヤーを挿入し以降をずらす。新しいインデックスを返す |
| `GetTransitionsForSection` | 指定セクションが関与する Transition 一覧（`FromSectionIndex`・`ToSectionIndex`・`TransitionClass`） |
| `GetTransitionBetween` | 2 つのセクションインデックス間の Transition の基本情報（無ければ `NotFound`） |
| `GetTransitionInfo` | 2 つのセクション間の Transition の詳細情報 |
| `GetTransitionName` | 2 つのセクション間の Transition の表示名 |
| `ChangeTransitionType` | Transition を `NewTransitionClass` のものへ差し替え（単一トランザクション内で作成→削除の順） |
| `GetCompatibleDecorations` | レイヤーに適用可能な Decoration クラス一覧 |
| `GetDecorations` | レイヤー上の既存 Decoration 一覧 |
| `FindDecoration` | レイヤー上の特定 Decoration を検索（無ければ `NotFound`） |
| `AddDecoration` | レイヤーに Decoration を追加（既存があればそれを返す） |
| `RemoveDecoration` | レイヤーから Decoration を削除 |
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

#### ControlRig トラック（12）

**LevelSequence 内**での ControlRig オーサリング。ControlRig アセット自体の編集は [`UAIP.Editor.ControlRig`](#uaipeditorcontrolrig) を参照してください。

| コマンド | 説明 |
|---|---|
| `GetControlRigTracks` | LevelSequence 内の全 ControlRig パラメータトラック |
| `GetControlRigSectionInfo` | セクションのプロパティ — `IsInfinite`・`StartFrame`・`EndFrame`・`IsActive`・クラス名 |
| `FindOrCreateControlRigTrack` | バインディングの ControlRig パラメータトラックを取得または作成し `TrackCreated` を返す |
| `BakeToControlRig` | バインディングのアニメーションを ControlRig トラックへベイク（表示レートフレーム・`Tolerance` は 0.0〜1.0） |
| `KeyControls` | 指定コントロールを 1 つの表示レートフレームでキー（`ControlNames` 省略時は表示中の全コントロール） |
| `KeyControlsAtFrames` | 指定コントロールを複数の表示レートフレームでキー |
| `GetControlsMask` | ControlRig セクションのコントロール別表示マスク |
| `SetControlsMask` | 指定コントロールの表示状態を設定（未指定のコントロールは現状維持） |
| `ShowAllControls` | セクション内の全コントロールを表示 |
| `HideAllControls` | セクション内の全コントロールを非表示 |
| `LoadAnimIntoRig` | ⚠️ 常に `UnsupportedOperation` を返す — エンジン API が静的アセット編集では取得できない `USkeletalMeshComponent*` を要求するため。代わりに `Toolset.Editor.SequencerControlRig.LoadAnimIntoRig` を使用 |
| `GetActorTransformAtFrame` | 指定フレームでシーケンスを評価し、名前指定したアクターのワールドトランスフォームを返す |

### Toolset ブリッジ（61）🧩

プロバイダ：`Toolset.Editor.AnimationAssistant.*`（41 件 — Lifecycle 6・Playback 10・Property 9・MarkedFrame 5・UI 11）と `Toolset.Editor.SequencerAnimMixer.*`（20 件 — Layers 10・Transitions 5・Decorations 5）。UE 5.8+ が必要。

> Sequencer モジュール実装のもう 1 つのブリッジプロバイダ `Toolset.Editor.SequencerControlRig.*`（63 件）は、コマンドの対象が ControlRig のコントロールであるため [`UAIP.Editor.ControlRig`](#uaipeditorcontrolrig) 側に掲載しています。

---

## UAIP.Editor.StateTree

StateTree 編集。

### ネイティブ（39）

#### State 観測（8）

| コマンド | 説明 |
|---|---|
| `GetRootStates` | トップレベル State のディスクリプタ（`StateId`・`Name`・`Type`・`ParentStateId`・`ChildCount`） |
| `GetStateChildren` | 単一 State の直下の子 State ディスクリプタ |
| `GetStateTasks` | 単一 State の Task 一覧（PIE 中の degraded モードではクラス名を秘匿） |
| `GetStateTransitions` | 単一 State の Transition 一覧（PIE 中は遷移先 State ID を秘匿） |
| `GetStateEnterConditions` | 単一 State の Enter Condition 一覧 |
| `GetStateTreeGlobalTasks` | アセットのグローバル Task 一覧（アクティブ State に関係なく実行される） |
| `GetStateTreeEvaluators` | アセットの Evaluator 一覧（毎 Tick 実行され共有データを更新する） |
| `GetStateNodeDescription` | ノード GUID のクラスパスと表示名（グローバル Task・Evaluator・全 State を横断検索） |

#### クラス / スキーマ探索（5）

| コマンド | 説明 |
|---|---|
| `GetAvailableTaskClasses` | ノードクラスポリシーで許可された Task クラス（ネイティブ struct + Blueprint） |
| `GetAvailableConditionClasses` | Condition クラス（ネイティブ struct + Blueprint） |
| `GetAvailableEvaluatorClasses` | Evaluator クラス（ネイティブ struct + Blueprint） |
| `GetAvailableStateTreeSchemaClasses` | `UStateTreeSchema` サブクラス — `ClassPath` を `CreateAsset` の `FactoryParams.SchemaClass` に渡す |
| `GetStateTreeSchema` | アセットの Schema クラスパスとルートパラメータのディスクリプタ |

#### State 構造編集（4）

| コマンド | 説明 |
|---|---|
| `AddState` | State を追加（State / Group / Subtree / Linked / LinkedAsset の 5 種類）。`StateId` を返す |
| `RemoveState` | StateId 指定で State を削除（子 State 再帰削除） |
| `SetStateName` | State をリネーム |
| `MoveState` | State の親／順序を変更（循環参照になる移動は拒否） |

#### Task / Transition / Condition 編集（9）

| コマンド | 説明 |
|---|---|
| `AddStateTask` | State に Task を追加（8 ステップ allowlist）。`TaskId` を返す |
| `RemoveStateTask` | TaskId 指定で Task を削除 |
| `AddStateTransition` | Transition を追加（`Succeeded` / `Failed` / `NextState` / `NextSelectableState` / GUID 指定）。`OnDelegate` は非対応 |
| `RemoveStateTransition` | TransitionId 指定で Transition を削除 |
| `AddStateEnterCondition` | State に Enter Condition を追加。`ConditionId` を返す |
| `RemoveStateEnterCondition` | ConditionId 指定で Enter Condition を削除 |
| `SetEnterConditionProperty` | Enter Condition ノードのプロパティを設定 |
| `GetStateNodeProperty` | ノード GUID のトップレベルプロパティ 1 件をエクスポートテキストで取得 |
| `SetStateNodeProperty` | Task ノードのプロパティを設定（汎用 ImportText_Direct） |

#### グローバル Task / Evaluator 編集（6）

| コマンド | 説明 |
|---|---|
| `AddGlobalTask` | グローバル Task を追加。`TaskId` を返す |
| `RemoveGlobalTask` | TaskId 指定でグローバル Task を削除 |
| `SetGlobalTaskProperty` | グローバル Task ノードのプロパティを設定 |
| `AddEvaluator` | Evaluator を追加。`EvaluatorId` を返す |
| `RemoveEvaluator` | EvaluatorId 指定で Evaluator を削除 |
| `SetEvaluatorProperty` | Evaluator ノードのプロパティを設定 |

#### パラメータ・バインディング・コンパイル（7）

| コマンド | 説明 |
|---|---|
| `GetStateTreeParameters` | ルートパラメータのディスクリプタ（`Name`・`ParameterType`・現在のシリアライズ値） |
| `AddStateTreeParameter` | ルートパラメータを追加（Bool / Byte / Int32 / Int64 / Float / Double / Name / String / Text） |
| `RemoveStateTreeParameter` | 名前指定でルートパラメータを削除 |
| `SetStateTreeParameter` | ルートパラメータ値を文字列エンコード値から設定 |
| `AddPropertyBinding` | ソースノードのプロパティをターゲットノードのプロパティへバインド |
| `RemovePropertyBinding` | ターゲットノードのプロパティバインディングを削除 |
| `CompileStateTree` | StateTree をコンパイル（連続呼び出しにはアセット単位のレートリミット） |

### Toolset ブリッジ（8 件）🧩

`StateTreeToolset`（UE 5.8+、Experimental）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.StateTree.*`。観測専用です。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.StateTree.GetEditorData` | StateTree アセットのエディタデータ |
| `Toolset.Editor.StateTree.GetRootStates` | StateTree アセットのルート State |
| `Toolset.Editor.StateTree.GetGlobalTasks` | StateTree アセットのグローバル Task |
| `Toolset.Editor.StateTree.GetEvaluators` | StateTree アセットの Evaluator |
| `Toolset.Editor.StateTree.GetChildren` | `UStateTreeState` の子 State |
| `Toolset.Editor.StateTree.GetTasks` | `UStateTreeState` の Task |
| `Toolset.Editor.StateTree.GetEnterConditions` | `UStateTreeState` の Enter Condition |
| `Toolset.Editor.StateTree.GetTransitions` | `UStateTreeState` の Transition |

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
| `CreatePCGGraph` 🧩 | 新規 UPCGGraph アセットを Content ディレクトリに作成（`PCGGraphAssetCreate` 必須） |
| `GetPCGGraphSchema` 🧩 | グラフのノード / ピン構成をスキーマ形式で取得 |
| `GetPCGGraphDescription` 🧩 | グラフの Description 文字列を取得 |
| `SetPCGGraphDescription` 🧩 | グラフの Description を設定（`PCGGraphEdit` 必須） |
| `SetPCGGraphParams` 🧩 | グラフパラメータを追加 / 更新（`PCGGraphEdit` 必須） |
| `RemovePCGGraphParams` 🧩 | グラフパラメータを削除（`PCGGraphEdit` 必須） |
| `ListPCGGraphInstances` 🧩 | レベル内の UPCGComponent 一覧を取得 |
| `SpawnPCGGraphInstance` 🧩 | APCGVolume を World にスポーン（`PCGVolumeSpawn` 必須） |
| `GetPCGGraphInstanceParams` 🧩 | インスタンスのオーバーライドパラメータを取得 |
| `SetPCGGraphInstanceParams` 🧩 | インスタンスパラメータをオーバーライド（`PCGGraphEdit` 必須） |
| `ResetPCGGraphInstanceParams` 🧩 | インスタンスパラメータをデフォルトにリセット（`PCGGraphEdit` 必須） |
| `ListPCGAvailableSubgraphs` 🧩 | プロジェクト内のサブグラフ候補を列挙 |
| `GetPCGNativeNodeSchema` 🧩 | ネイティブ PCG ノードクラスの EditAnywhere プロパティを JSON スキーマで返す |
| `AddPCGSubgraphNode` 🧩 | サブグラフ参照ノードを追加（`PCGGraphEdit` 必須） |
| `RepositionPCGNode` 🧩 | ノード位置を変更（`PCGGraphEdit` 必須） |
| `AddPCGCommentBox` 🧩 | コメントボックスを追加（`PCGGraphEdit` 必須） |
| `UpdatePCGCommentBox` 🧩 | コメントボックスを更新（`PCGGraphEdit` 必須） |
| `RemovePCGCommentBox` 🧩 | コメントボックスを削除（`PCGGraphEdit` 必須） |
| `GetPCGNodeDataView` 🧩 | PCG ノードの実行データビューを取得（`PCGNodeInspect` 必須。`PCG_PROFILING_ENABLED=0` 時は CapabilityNotAvailable） |
| `RunPCGInstantGraph` 🧩 | アクター / コンポーネント不要の fire-and-forget PCG グラフ実行（`PCGGraphExecute` 必須） |
| `DrawPCGSpline` 🧩 | レベルビューポートで人間がスプラインを描き終える対話を開始し、待たずに `InteractionId` を返す（`IsInteractive: true`）。`GetPendingInteractionStatus` でポーリング、`WaitForPendingInteraction` で短時間ブロック、`CancelPendingInteraction` でキャンセルできる。`PCGSplineDraw` と `SafetyPolicy.AllowUserInteractionPrompt`（別ゲート）が必須。ビューポートを保持できる対話は同時に 1 件のみ |

### Toolset ブリッジ — PCG（31 件）🧩

`PCGToolset`（UE 5.8+）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.PCG.*`。アクティブな PCG エディタタブが必要なコマンドは非インタラクティブコンテキストで `ExecutionFailed` を返す場合があります（PCGToolset の既知の制約）。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.PCG.CreateGraph` 🧩 | PCG グラフアセットを作成（`PCGGraphAssetCreate` 必須） |
| `Toolset.Editor.PCG.GetGraphStructure` 🧩 | グラフ全体の構造（ノード・エッジ・パラメータ）を取得 |
| `Toolset.Editor.PCG.SetGraphParams` 🧩 | グラフパラメータを設定（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.RemoveGraphParams` 🧩 | グラフパラメータを削除（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.GetGraphSchema` 🧩 | グラフスキーマを取得 |
| `Toolset.Editor.PCG.GetGraphDescription` 🧩 | グラフの説明文を取得 |
| `Toolset.Editor.PCG.SetGraphDescription` 🧩 | グラフの説明文を設定（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.ListGraphInstances` 🧩 | グラフを参照しているボリュームアクター一覧 |
| `Toolset.Editor.PCG.SpawnGraphInstance` 🧩 | PCG ボリュームアクターをスポーン（`PCGVolumeSpawn` 必須） |
| `Toolset.Editor.PCG.ExecuteGraphInstance` 🧩 | PCG ボリューム上でグラフを実行（`PCGGraphExecute` 必須；非同期・デフォルト 300 秒） |
| `Toolset.Editor.PCG.GetGraphInstanceParams` 🧩 | インスタンスのパラメータオーバーライドを取得 |
| `Toolset.Editor.PCG.SetGraphInstanceParams` 🧩 | インスタンスパラメータを上書き（`PCGGraphExecute` 必須） |
| `Toolset.Editor.PCG.ResetGraphInstanceParams` 🧩 | インスタンスパラメータをリセット（`PCGGraphExecute` 必須） |
| `Toolset.Editor.PCG.ListNativeNodes` 🧩 | 登録済みネイティブ PCG ノードクラスを一覧 |
| `Toolset.Editor.PCG.ListAvailableSubgraphs` 🧩 | サブグラフとして利用可能な PCG アセットを一覧 |
| `Toolset.Editor.PCG.GetNativeNodeSchema` 🧩 | ネイティブノードクラスのパラメータスキーマを取得 |
| `Toolset.Editor.PCG.AddNode` 🧩 | ネイティブノードを追加（`PCGGraphEdit` + `PCGToolsetUnsafeNodeAdd` 必須；Allowlist バイパス） |
| `Toolset.Editor.PCG.AddSubgraphNode` 🧩 | サブグラフノードを追加（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.UpdateNode` 🧩 | ノードのプロパティを更新（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.SetNodeComment` 🧩 | ノードのインラインコメントを設定（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.GetNodeInfo` 🧩 | 特定ノードの情報を取得 |
| `Toolset.Editor.PCG.RepositionNode` 🧩 | グラフキャンバス上のノードを移動（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.RemoveNode` 🧩 | ノードを削除（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.GetNodeDataView` 🧩 | ノードの最終実行データビューを取得（`PCGNodeInspect` 必須） |
| `Toolset.Editor.PCG.ConnectNodePins` 🧩 | 2 つのノードピンを接続（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.DisconnectNodePins` 🧩 | ノードピンを切断（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.AddCommentBox` 🧩 | コメントボックスを追加（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.UpdateCommentBox` 🧩 | コメントボックスを更新（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.RemoveCommentBox` 🧩 | コメントボックスを削除（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.RunPCGInstantGraph` 🧩 | `UPCGSpatialToolset` 経由で PCG グラフを即時実行（`PCGGraphExecute` 必須；非同期・デフォルト 300 秒） |
| `Toolset.Editor.PCG.DrawSpline` 🧩 | `UAIP.Editor.PCG.DrawPCGSpline` のブリッジ版。`UPCGToolset::DrawSpline` に委譲する（Experimental）。Admission ルールと Capability ゲートはネイティブ版と同じだが、登録する待機時間は Toolset ディスパッチ自体の上限により 600 秒でクランプされる（ネイティブ版のデフォルト 1800 秒とは異なる） |

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
| `ListWorldConditionClasses` 🧩 | クラスポリシーで許可された `FWorldConditionBase` 派生クラス一覧 — 有効な `ConditionClass` 値の探索に使う |
| `ValidateWorldConditionQuery` 🧩 | クエリに対して `Initialize()` + `IsValid()` を実行し `{IsValid, Errors}` を返す（PIE 中も可） |
| `MoveWorldCondition` 🧩 | 条件を `SourceIndex` から `TargetIndex` へ移動（インデックス 0 は固定） |
| `DuplicateWorldCondition` 🧩 | `SourceIndex` の条件を複製し `InsertIndex` に挿入 |
| `ReplaceWorldCondition` 🧩 | 条件の型を `NewConditionClass` の既定値へ差し替え（Depth・Operator・bInvert は維持） |
| `ClearWorldConditionQuery` 🧩 | 全条件を削除して空のクエリにする |
| `SetMultipleWorldConditionProperties` 🧩 | 1〜32 件のプロパティ編集を単一トランザクションで適用し、編集ごとの成否を返す |

### Toolset ブリッジ — WorldConditions（2 件）🧩

`WorldConditionTools`（UE 5.8+、Experimental）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.WorldConditions.*`。入力 JSON は 64 KiB 上限です。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.WorldConditions.GetQueryDescription` | `FWorldConditionQueryDefinition` の人間可読な説明 |
| `Toolset.Editor.WorldConditions.GetConditionDescription` | 単一条件型の人間可読な説明 |

---

## UAIP.Editor.Conversation 🧩

ConversationDB グラフ編集。`CommonConversation` プラグインが必要です。

| コマンド | 説明 |
|---|---|
| `ListConversationNodeTypes` 🧩 | 位置別の許可ノードクラス一覧（最大 256 件） |
| `AddConversationNode` 🧩 | トップレベルノードを追加（`UConversationNodeWithLinks` 派生） |
| `AddConversationSubNode` 🧩 | 親 Task ノードに SubNode を附加 |
| `RemoveConversationNode` 🧩 | NodeGuid 指定でノードを削除 |
| `ConnectConversationNodes` 🧩 | ノード間の遷移エッジを追加 |
| `DisconnectConversationNodes` 🧩 | 遷移エッジを削除 |
| `SetConversationNodeProperty` 🧩 | プロパティを設定（FText は BIDI strip・PUA reject・4096 文字上限） |

### Toolset ブリッジ — Conversation（5 件）🧩

`ConversationToolset`（UE 5.8+）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.Conversation.*`。観測専用で、編集は上記のネイティブコマンドが担当します。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.Conversation.ListConversationEntryPoints` | `UConversationDatabase` のエントリポイントノード一覧 |
| `Toolset.Editor.Conversation.ListConversationSpeakers` | `UConversationDatabase` に定義された話者一覧 |
| `Toolset.Editor.Conversation.ListConversationNodes` | 全ノード一覧（以下 2 コマンドで使う refPath 付き） |
| `Toolset.Editor.Conversation.GetConversationNodeConnections` | `NodeRefPath` で指定したノードの接続グラフ |
| `Toolset.Editor.Conversation.ListConversationNodeSubNodes` | ノードの SubNode（選択肢・要求・副作用）一覧 |

---

## UAIP.Editor.ControlRig

ControlRig ヒエラルキーと RigVM グラフ編集。

### ネイティブ（68）

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

#### リグヒエラルキーコンポーネント（9）

ヒエラルキー要素に取り付けられたコンポーネント（`FRigBaseComponent` 派生構造体）を扱う汎用コマンド群です。モジュール allowlist が許可するすべてのコンポーネント型に対して動作し、後述の 2 ドメインが型ごとの専用コマンドを提供する ControlRigDynamics / ControlRigPhysics の型も含みます。コンポーネントは `ElementName` と `ElementType`（`Bone` / `Null` / `Control`。`All` は不可）と `ComponentName` の組で指定します。読み取り 4 コマンドは `EditorInspect` を、書き込み 5 コマンドは `ControlRigComponentEdit`（既定無効）を要求し、PIE 実行中は拒否されます。

| コマンド | 説明 |
|---|---|
| `ListComponents` | 1 要素のコンポーネント一覧。`ElementName` と `ElementType` をどちらも省略するとヒエラルキー全体を列挙する。各エントリは所属要素・型パス・`IsProcedural` を持ち、レスポンスは `TotalCount` / `ReturnedCount` / `Truncated` を返す |
| `GetComponent` | 1 コンポーネントの型と内容。`ContentText`（エンジンのエクスポート形式）は常に返る。`Content`（JSON）は JSON で表現できない型の場合に明示的な `null` と `ContentConversion` 理由になり、変換不能なコンポーネントが空のものと取り違えられることはない |
| `ListAddableComponentTypes` | エディタが知る `FRigBaseComponent` 派生構造体をすべて列挙する（対象ヒエラルキーにコンポーネントが 1 つも無くても列挙できる）。各エントリは `AddComponent` が検証するのと同じポリシー由来の `Addable` フラグを持ち、false のときは `NotAddableReason` が付く |
| `CanAddComponent` | ある型をある要素に取り付けられるかどうかを、実際に取り付けずに判定する。`CanAdd` が false のときは `FailureReason` に、ポリシー段階（型そのものが許可されていない）かエンジン自身の拒否（要素が受け付けない）かが示される |
| `AddComponent` | 新しいコンポーネントを取り付ける。初期内容は任意で、`Content`（JSON）**または** `ContentText`（エクスポート形式）のどちらか一方のみ。作成前に内容を完全に検証するため、拒否された要求はコンポーネントを残さない |
| `RemoveComponent` | コンポーネントを削除する。そのキーを保持する他コンポーネントの扱いは `ReferenceHandling` が決める（`Reject`＝既定 / `Detach` / `Force`）。見つかった参照はすべて `References` に、どう扱われたかとともに返る |
| `RenameComponent` | コンポーネントを `NewName` へ改名し、そのコンポーネントを指していた参照を張り替える |
| `ReparentComponent` | `NewParentName` と `NewParentType` が指す要素へコンポーネントを付け替え、参照を張り替える。存在しない付け替え先は、何も変更する前に拒否される |
| `SetComponentContent` | コンポーネントの内容を置き換える（`Content` **または** `ContentText` のどちらか一方が必須）。書き込み後に読み戻し、実際に書き込まれた内容を返す |

> **Note — 指定した名前がそのまま付くとは限りません**: `AddComponent`・`RenameComponent`・`ReparentComponent` は名前の衝突で失敗しません。エンジンが空いている名前を割り当て、結果には**実際に付いたキー**が返ります（`RenameComponent` / `ReparentComponent` は `NameChanged` も返します）。以降はその返されたキーを使ってください。今と同じ名前への改名、今ぶら下がっている要素への付け替えは、成功して何も変わりません。
>
> **Note — 書き込まれなかったプロパティは「一覧化」されるのであって「既定値に戻る」のではありません**: オブジェクト参照・デリゲート・実行時専用の状態は外部から書き込みません。`AddComponent`・`SetComponentContent`、および後述 2 ドメインの型付き `Set*` コマンドはそれらを `FilteredProperties` として返し、各項目は**いまの値のまま**残ります。
>
> **Note — `ReferenceWarnings` が空でも「何も壊れていない」とは限りません**: `Detach` または `Force` を指定した `RemoveComponent` は、片端が解決できなくなったコンポーネントを `ReferenceWarnings` として返します。この状態についてエンジンもシミュレーションも何も言わないためです — 揺れ物側では、パーティクルを失った拘束がメッセージ無しで読み飛ばされ、物理側では、ソルバーや親ボディを失ったボディ／ジョイントがエンジンの自動探索の結果へ黙って繋ぎ変わります。これらのコンポーネントはそのまま残され、代わりに削除されることはありません。このコマンドが型を知らないコンポーネントは警告の対象にできないため、`References` も併せて読んでください。`Reject` と `Detach` はそうした参照を残すくらいなら拒否します — その安全弁を外すのが `Force` です。
>
> **Note — リグが自分で作ったコンポーネントは編集できません**: `IsProcedural: true` のエントリは手で作られたものではなくリグ実行が再生成するもので、ここの書き込みコマンドはすべて拒否します。

#### その他（2）

| コマンド | 説明 |
|---|---|
| `CompileControlRig` | ControlRig をコンパイル（セッション単位 1 秒レートリミット） |
| `GetAvailableRigVMUnitStructs` | FRigUnit 派生 UScriptStruct 一覧（上限 1000 件）。各エントリは `AddGraphNode` が検証するのと同じポリシー由来の `Addable` フラグを持ち、false のときは `NotAddableReason` が付く。`SchemaVersion` / `TotalCount` / `ReturnedCount` / `Truncated` を返す |

> **⚠️ 変更 — `GetAvailableRigVMUnitStructs` の出力が `SchemaVersion: 2` になりました**: 各エントリが `Addable` を持ち、false のときは機械可読な `NotAddableReason`（`InvalidFormat` / `InvalidPrefix` / `StructNotFound` / `ModuleNotAllowed` / `NotARigUnit` / `DeprecatedOrHidden` のいずれか）が付きます。レスポンスは `SchemaVersion`・`TotalCount`（件数上限を適用する前の総数）・`ReturnedCount`・`Truncated` も返します。いずれも追加のみで、`ClassPath` と `ClassDisplayName` は変わらないため、既存の読み取りコードはそのまま動作します。変わったのは、このフラグが `AddGraphNode` の検証に使われるポリシーそのものから作られる点（一覧に出ているのに `AddGraphNode` が受け付けない、という食い違いが起きなくなりました）と、件数上限で打ち切られたレスポンスがそれを明示するようになった点です。
>
> **⚠️ 破壊的変更 — `AddGraphNode` の背後にあるモジュール allowlist が完全一致になりました**: 従来は `StructPath` の所属パッケージが `/Script/ControlRig`・`/Script/AnimationCore`・`/Script/Engine` のいずれかで**始まってさえいれば**受理していました。今後は 7 モジュール（`/Script/ControlRig`、`/Script/ControlRigDynamics`、`/Script/ControlRigPhysics`、`/Script/ControlRigSpline`、`/Script/ControlRigModules`、`/Script/AnimationCore`、`/Script/Engine`）との**等価比較**になります。前方が一致していただけのパッケージ — `/Script/ControlRigDeveloper`、`/Script/ControlRigEditor`、`/Script/EngineMessages` など — は以前は受理されていましたが、今後は `ModuleNotAllowed` で拒否されます。前方一致の挙動に依存していた呼び出しは動かなくなります。回避手段はありません（この allowlist はもともとそれらのモジュールへ届くことを意図していません）。
>
> **Note — ControlRig 系の兄弟モジュールは、今回から意図して一覧に載っています**: `/Script/ControlRigDynamics`、`/Script/ControlRigPhysics`、`/Script/ControlRigSpline`、`/Script/ControlRigModules` は、従来は `/Script/ControlRig` の前方一致の副作用として偶然到達できていただけでした。今回これらを明示的に列挙したため、物理系の RigUnit 約 73 件（`FRigUnit_SpawnPhysicsSolver`、`FRigUnit_AddPhysicsBody`、`FRigUnit_AddPhysicsJoint` など）は、厳格化された規則に巻き込まれることなく引き続き追加できます。ノード用とコンポーネント用の allowlist は同じモジュール集合を対象としているため、コンポーネントとして作れる型はノードとしても置けます。

### Toolset ブリッジ（107）🧩

いずれも `AnimationAssistantToolset`（UE 5.8+）へ委譲する 2 つのブリッジプロバイダがあります。

**`Toolset.Editor.ControlRig.*`（44 件）** — 上記ネイティブのアセット編集コマンドのミラー。グループ：アセット作成（1）/ ヒエラルキー観測（8）/ ヒエラルキー編集（7）/ グラフ管理（10）/ ノード（7）/ ピン（6）/ 変数（5）。

**`Toolset.Editor.SequencerControlRig.*`（63 件）** — アニメーション時のコントロールオーサリング。実装は Sequencer モジュール（`SequencerControlRigTools`）ですが、全コマンドが ControlRig のコントロールを対象とするため本セクションに掲載しています。ControlRig に加えて `MovieSceneAnimMixer` が必要です。グループ：

| グループ | 件数 | コマンド |
|---|---:|---|
| コントロール値 | 16 | `Get`/`SetFloatValue`・`BoolValue`・`IntValue`・`Vector2DValue`・`PositionValue`・`RotatorValue`・`ScaleValue`・`EulerTransformValue` |
| ワールドトランスフォーム | 3 | `GetWorldTransform`・`SetWorldTransform`・`GetActorTransformAtFrame` |
| レイヤードリグ | 6 | `CollapseAnimLayers`・`IsLayeredControlRig`・`SetLayeredMode`・`Get`/`SetPriorityOrder`・`IsFKControlRig` |
| アニメーションレイヤー | 6 | `GetControlRigAnimLayers`・`AddControlRigLayerFromSelection`・`Delete`/`Duplicate`/`Reorder`/`MergeControlRigAnimLayers` |
| スペース | 4 | `Set`/`Move`/`Delete`/`BakeControlRigSpace` |
| トゥイーン | 3 | `TweenControlRig`・`BlendValuesOnSelected`・`SnapControlRig` |
| ミラーリング | 3 | `SelectMirroredControls`・`MirrorSelectedControls`・`ZeroControlRigTransforms` |
| 選択 | 4 | `GetSelectedControls`・`SelectControl`・`ClearControlSelection`・`FrameControlSelection` |
| FBX | 2 | `ExportFBXFromRig`・`ImportFBXToRig` |
| Sequencer 問い合わせ | 4 | `GetSequencerControlRigs`・`GetSequencerControlsInfo`・`Get`/`SetControlRigTransformInSequencer` |
| アニメーションモード設定 | 12 | `AnimModeGizmoScale`・`AnimModeHierarchy`・`AnimModeNulls`・`AnimModeHideManips`・`AnimModeOnlyRigSel`・`AnimModeLocalSpaces` の `Get`/`Set` |

---

## UAIP.Editor.ControlRig.Dynamics 🧩

ControlRig ヒエラルキー上の `ControlRigDynamics` コンポーネント型（ソルバー・パーティクル・コライダー・拘束・コーンリミット・コンファイナー）を型ごとに編集します。加えて、一連の構成をまとめて構築・付け替えする 4 コマンドを提供します。UE 5.8+ と `ControlRigDynamics` プラグイン（Experimental）が必要で、UE 5.7 またはプラグイン無効時はドメインごと利用できません。[`UAIP.Editor.ControlRig`](#uaipeditorcontrolrig) の汎用コンポーネントコマンドは、このプラグイン無しでもまったく同じコンポーネントに到達できます — ここで増えるのは、型ごとに項目名が付き、範囲検査が入ったスキーマです。このドメインに Toolset ブリッジは存在しません。

`ControlRigDynamics` は Experimental のエンジンプラグインであり、その構造体はエンジンのマイナーバージョン間で変わりうるため、**このドメインのコマンドはすべて `Stability: Experimental`** を返します。読み取りは `EditorInspect`、書き込みはすべて `ControlRigComponentEdit`（既定無効）を要求し、PIE 実行中は拒否されます。本ドメインと `UAIP.Editor.ControlRig.Physics` は互いに独立しており、片方だけを持つプロジェクト構成でもそれぞれ単独で現れます。

> **前提条件 — プラグインを `.uproject` に明記する必要があります**: UAIP が `ControlRigDynamics` にリンクするのは、プロジェクトが**明示的に**宣言している場合だけです。`.uproject` の `Plugins` 配列へ `{ "Name": "ControlRigDynamics", "Enabled": true }` を追加してリビルドしてください。判定はこのエントリだけを読みます — それ以外の理由でエンジンが有効とみなしているプラグインは数えません。エントリが無いとドメインごと `uaip_list_commands` に現れず、`uaip_list_commands(IncludeUnavailable=true)` が `UnavailableReason: HandlerUnavailable` を返します。

#### Typed reads（6 コマンド）— 要 `EditorInspect`

| コマンド | 説明 |
|---|---|
| `GetDynamicsSolverSettings` | `FRigDynamicsSolverComponent` の `Settings`・`SpaceMotion`・`TeleportDetection`。`Particles` / `Colliders` / `Constraints` / `ConeLimits` / `Confiners` の参照配列はここでは返らない — `GetComponent` で読む |
| `GetDynamicsParticleProperties` | `FRigDynamicsParticleComponent` の `ParticleProperties` |
| `GetDynamicsColliderShapes` | `FRigDynamicsColliderComponent` の `Shapes`（`Boxes`・`Capsules`・`Planes`）。`SetDynamicsColliderShapes` がそのまま受け取れる形状 |
| `GetDynamicsConstraintSettings` | `FRigDynamicsConstraintComponent` の `ConstraintType`・`Strength`・`DampingRatio`・`ExtraDamping`・`bAccelerationMode`・`LengthMultiplier`・`ExtraLength`。トポロジのキーはここでは返らない |
| `GetDynamicsConeLimitSettings` | `FRigDynamicsConeLimitComponent` の `Strength`・`DampingRatio`・`Angle`。トポロジのキーはここでは返らない |
| `GetDynamicsConfinerSettings` | `FRigDynamicsConfinerComponent` の `Shapes` と `Strength` |

#### Typed writes（6 コマンド）— 要 `ControlRigComponentEdit`

| コマンド | 説明 |
|---|---|
| `SetDynamicsSolverSettings` | `Settings`・`SpaceMotion`・`TeleportDetection` を置き換える。ソルバーの参照配列はここでは変更できない — `AddComponentToDynamicsSolver` / `RemoveComponentFromDynamicsSolver` を使う |
| `SetDynamicsParticleProperties` | `ParticleProperties` の 1 つ以上の項目を置き換える。`Radius` と `Mass` は正、`Strength`・`DampingRatio`・`ExtraDamping`・`AngleLimit`・`AngleLimitStrength`・`Damping` は非負、`TargetMode` は 0.0〜1.0、`MovementType` は `Kinematic` か `Simulated` |
| `SetDynamicsColliderShapes` | `Shapes` コレクション全体を置き換える。各トランスフォームは有限、ボックス／平面の extent は全軸で正、カプセルの半径は正、カプセルの長さは非負 |
| `SetDynamicsConstraintSettings` | 1 つ以上の設定を置き換える。`ConstraintType` は `Hard` か `Soft`、`Strength`・`DampingRatio`・`ExtraDamping`・`LengthMultiplier` は非負、`ExtraLength` は有限であれば正負どちらでもよい。トポロジのキーはそのまま引き継がれる |
| `SetDynamicsConeLimitSettings` | `Strength`・`DampingRatio`・`Angle` を置き換える。3 つとも負または非有限なら拒否。トポロジのキーはここでは変更できない — `SetComponentContent` を使う |
| `SetDynamicsConfinerSettings` | `Shapes` と `Strength` を置き換える。形状の検査は `SetDynamicsColliderShapes` と同じ。`Strength` は有限かつ非負 |

#### Orchestration（4 コマンド）— 要 `ControlRigComponentEdit`

| コマンド | 説明 |
|---|---|
| `AddDynamicsChain` | チェーンを 1 コマンドで構築する。`StartElementName` から `EndElementName` までの各要素にパーティクルを、隣接するペアごとに拘束を作り、それらすべてを指定ソルバーへ登録する。`StartElementName` は `EndElementName` の祖先である必要があり、両者が同一要素であってはならない。任意の `ParticleContent` / `ConstraintContent` はその種類のすべてに適用される。`ConstraintContent` はトポロジのキーを指定できない（どのパーティクル同士を繋ぐかはチェーン側が決めるため） |
| `ImportDynamicsCollidersFromPhysicsAsset` | PhysicsAsset の各ボディのうち、対応する骨がリグに存在するものについてコライダーを 1 つずつ作る。ボックス・スフィア・カプセルの形状を変換する（スフィアは長さ 0 のカプセルになる）。作成したものの一覧と、`SkippedBodies` として飛ばしたものとその理由を返す |
| `AddComponentToDynamicsSolver` | Dynamics コンポーネントをソルバーへ登録する。ソルバーのどの配列へ入るかは型から決まり、選べない。使われた配列は `SolverArray` として返る。既に登録済みのものを登録しても何も変わらず、`Added: false` が返る |
| `RemoveComponentFromDynamicsSolver` | ソルバーのすべての参照配列からコンポーネントを外す。ソルバーが参照していないものを外しても何も変わらず、`Removed: false` が返る |

> **Note — 型付き `Set*` は部分書き込みですが、空の書き込みは認められません**: 各項目は独立して省略可能ですが、少なくとも 1 つは必須です。省略した項目は型の既定値に戻るのではなく、**いまの値のまま**残ります。シミュレーションが受け付けない値（非有限な数値、負の質量や強さ、0〜1 の外の比率、0 以下のタイムステップや反復回数）は拒否され、コンポーネントは変更されません。汎用の `SetComponentContent` も同じ検査を行うため、型付きコマンドを迂回して不正値を通す抜け道はありません。
>
> **Note — 違う型のコンポーネント名を渡すと `NotFound` であり、ポリシーエラーではありません**: コライダー用のコマンドに拘束の名前を渡すと `NotFound` が返ります。型の取り違えは「どのコンポーネントを指していたか」の勘違いであることがほとんどで、どの型が許可されているかという話ではないためです。
>
> **Note — `ImportDynamicsCollidersFromPhysicsAsset` は 2 種類の「合わない」を区別します**: 対応する骨がリグに無い、その要素にはコライダーを付けられない、変換対象の形状が 1 つも無い（凸包・テーパードカプセル・レベルセットは変換しない）ボディは**飛ばして**残りを取り込み、理由付きで `SkippedBodies` に返します。骨は実在するのに形状の値が使えないボディは**リクエスト全体を拒否**します — 黙って一部だけ作るのを避けるためです。作られたコライダーはどのソルバーにも登録されません。登録は `AddComponentToDynamicsSolver` で明示的に行ってください。
>
> **Note — `RemoveComponentFromDynamicsSolver` は登録解除であって削除ではありません**: コンポーネント自体はヒエラルキーに残ります（削除は `RemoveComponent`）。対象が既に存在しなくても構わないため、削除済みコンポーネントが残したキーの掃除にも使えます。また、どの配列かを指定する引数は無く、ソルバーのすべての配列から外します。ソルバーがまだシミュレートしている拘束やコーンリミットのうちその対象を指しているものは `ReferenceWarnings` として返り、そのまま残されます — ソルバーはパーティクルを解決できない拘束を、エラーも警告も出さずに読み飛ばすためです。

---

## UAIP.Editor.ControlRig.Physics 🧩

ControlRig ヒエラルキー上の `ControlRigPhysics` コンポーネント型（ソルバー・ボディ・ジョイント・コントロール）を型ごとに編集します。`ControlRigPhysics` プラグイン（Beta）が必要です。上記の Dynamics ドメインと異なり、UE 5.8 だけでなく UE 5.7 でも利用できます。[`UAIP.Editor.ControlRig`](#uaipeditorcontrolrig) の汎用コンポーネントコマンドは、このプラグイン無しでもまったく同じコンポーネントに到達できます。このドメインに Toolset ブリッジは存在しません。

読み取りは `EditorInspect`、書き込みはすべて `ControlRigComponentEdit`（既定無効）を要求し、PIE 実行中および ModularRig アセットに対しては拒否されます。本ドメインと `UAIP.Editor.ControlRig.Dynamics` は互いに独立しており、片方だけを持つプロジェクト構成でもそれぞれ単独で現れます。

> **⚠️ 前提条件 — 「プラグインは有効なのにコマンドが無い」はここから始まります**: `ControlRigPhysics` はエンジン既定で有効（`EnabledByDefault`）のため、Plugins ウィンドウでは有効と表示され、その RigUnit も ControlRig エディタに既に出ています — それでも、プロジェクトがプラグインを**明示的に**宣言するまで UAIP はこれらのコマンドを 1 つも登録しません。`.uproject` の `Plugins` 配列へ `{ "Name": "ControlRigPhysics", "Enabled": true }` を追加してリビルドしてください。判定はこのエントリだけを読み、エンジンが既定で有効にしているという事実は見えていません。エントリが無いとドメインごと `uaip_list_commands` に現れず、`uaip_list_commands(IncludeUnavailable=true)` が `UnavailableReason: HandlerUnavailable` を返します。

#### Typed reads（4 コマンド）— 要 `EditorInspect`

| コマンド | 説明 |
|---|---|
| `GetPhysicsSolverSettings` | UE 5.8 では `FRigPhysicsSolverComponent` の `SolverSettings`・`SpaceMotion`・`TeleportDetection`（UE 5.7 では `SolverSettings` と `SimulationSpaceSettings`）。`SolverSettings.SpaceBone` はここでは返らない — `GetComponent` で読む |
| `GetPhysicsBodySettings` | `FRigPhysicsBodyComponent` の調整可能な設定（質量・慣性のオーバーライド、ダンピング、`MovementType`、`CollisionType`、`KinematicTargetSpace`、重力倍率、ブレンドウェイト、CCD ほか）をトップレベルで返す。トポロジ・コリジョン形状・キネマティックターゲットはここでは返らない |
| `GetPhysicsJointSettings` | `FRigPhysicsJointComponent` の `JointData` と `DriveData` を JSON オブジェクトとして返す。親／子ボディのキーはここでは返らない |
| `GetPhysicsControlSettings` | `FRigPhysicsControlComponent` の `ControlData`・`ControlMultiplier`・`ControlTarget`・`UseParentBodyAsDefault`。親／子ボディのキーはここでは返らない |

#### Typed writes（4 コマンド）— 要 `ControlRigComponentEdit`

| コマンド | 説明 |
|---|---|
| `SetPhysicsSolverSettings` | UE 5.8 では `SolverSettings`・`SpaceMotion`・`TeleportDetection` を置き換える（UE 5.7 では `SolverSettings` と `SimulationSpaceSettings`）。`SpaceBone` を指定した `SolverSettings` は拒否される |
| `SetPhysicsBodySettings` | 1 つ以上のボディ設定を置き換える。`MovementType` は `Static` / `Kinematic` / `Simulated` / `Default`、`CollisionType` は `NoCollision` / `QueryOnly` / `PhysicsOnly` / `QueryAndPhysics` / `ProbeOnly` / `QueryAndProbe`、`KinematicTargetSpace` は `World` / `Component` / `OffsetInBoneSpace` / `OffsetInWorldSpace`。`LinearDamping` と `AngularDamping` は非負。トポロジ・コリジョン形状・キネマティックターゲットはそのまま引き継がれる |
| `SetPhysicsJointSettings` | `JointData` と `DriveData` を置き換える。`LinearProjectionAmount` と `AngularProjectionAmount` は 0.0〜1.0、`ParentInverseMassScale` は非負。親／子ボディのキーはここでは変更できない — `SetComponentContent` を使う |
| `SetPhysicsControlSettings` | `ControlData`・`ControlMultiplier`・`ControlTarget`・`UseParentBodyAsDefault` を置き換える。負の強さ・ダンピング・倍率は拒否される。親／子ボディのキーはここでは変更できない — `SetComponentContent` を使う |

> **⚠️ Note — ソルバー系コマンドは UE 5.7 と UE 5.8 でスキーマが異なります**: UE 5.8 の `GetPhysicsSolverSettings` / `SetPhysicsSolverSettings` は `SolverSettings`・`SpaceMotion`・`TeleportDetection` を扱いますが、UE 5.7 の同じ 2 コマンドは `SolverSettings` と `SimulationSpaceSettings` を扱います。これはエンジンプラグイン側の構造体の構成に従ったものです。形状を決め打ちせず、実行時に `uaip_describe_command` でコマンド自身の `Description` を読んでください。残り 6 コマンドは両バージョンで同じスキーマです。
>
> **Note — 型付き `Set*` は部分書き込みですが、空の書き込みは認められません**: 各項目は独立して省略可能ですが、少なくとも 1 つは必須です。省略した項目は型の既定値に戻るのではなく、いまの値のまま残ります。ソルバーが受け付けない値（非有限な数値、下限を下回る反復数やステップ数、負のしきい値、0〜1 の外の比率）は拒否され、コンポーネントは変更されません。汎用の `SetComponentContent` も同じ検査を行います。
>
> **Note — 違う型のコンポーネント名を渡すと `NotFound` であり、ポリシーエラーではありません**: ボディ用のコマンドにジョイントの名前を渡すと `NotFound` が返ります。理由は Dynamics ドメインと同じです。

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

### ネイティブ（8）

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

### Toolset ブリッジ（14）🧩

`GASToolsets`（UE 5.8+）経由でネイティブコマンドを委譲。プロバイダ：`Toolset.Editor.GAS.*`。グループ：Runtime 検査（6 件）— `GetAttributeValues` / `GetActiveEffects` / `GetGrantedAbilities` / `GetActiveTags` / `FindAttributeSetClasses` / `ListAttributes`、GameplayCue オーサリング（8 件）— `ListCues` / `GetCueInfo` / `FindCueNotifyAssets` / `FindCueTagsWithoutNotifies` / `ExecuteCueOnSelectedActor` / `CreateCueNotifyAsset` / `AddCueTag` / `RemoveCueTag`。

---

## UAIP.Editor.Python 🧩

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

## UAIP.Editor.WorldPartition

パーティション化されたワールドの World Partition・Data Layer・HLOD 管理（`WorldPartition` プラグイン必須）。World Partition が有効でないレベルでは、変更系コマンドは `ExecutionFailed` を、観測系コマンドは `Success: true` + `IsWorldPartitionEnabled: false` を返します。

### World Partition（12 コマンド）

| コマンド | 説明 |
|---|---|
| `GetWorldPartitionInfo` | World Partition の設定情報を取得 — ストリーミングモード・ランタイムハッシュクラス・WP 有効状態 |
| `GetWorldPartitionStreamingGrids` | World Partition 設定に定義されたランタイムストリーミンググリッド一覧を返す |
| `GetRuntimeGridSettings` | 指定したランタイムグリッドの設定を取得 |
| `SetRuntimeGridSettings` | 指定したランタイムグリッドの設定を変更（`WorldPartitionEdit` 必須） |
| `GetActorWorldPartitionSettings` | アクターの WP 設定を取得 — HLOD レイヤー・spatially loaded フラグ・ランタイムグリッド名 |
| `SetActorIsSpatiallyLoaded` | アクターの spatially loaded フラグを設定（`WorldPartitionEdit` 必須） |
| `SetActorRuntimeGrid` | アクターを特定のランタイムストリーミンググリッドに割り当て（`WorldPartitionEdit` 必須） |
| `SetWorldPartitionStreamingEnabled` | 現在のレベルの WP ストリーミングを有効/無効に切り替え（`WorldPartitionEdit` 必須） |
| `PinActorInWorldPartition` | アクターをストリーミング状態に関係なく常にロードされるよう Pin（`WorldPartitionEdit` 必須） |
| `UnpinActorFromWorldPartition` | アクターの常時ロード Pin を解除（`WorldPartitionEdit` 必須） |
| `DumpWorldPartitionCells` | 現在の WP ストリーミングセルグリッドを JSON アーティファクトとしてダンプ |
| `ListExternalActors` | 外部パッケージとして保存されたアクター一覧を返す（WP 外部アクターワークフロー） |

### Data Layer（15 コマンド）

| コマンド | 説明 |
|---|---|
| `ListDataLayers` | 現在のレベルに存在する全 Data Layer インスタンスを一覧表示 |
| `GetDataLayerInfo` | Data Layer インスタンスの詳細情報を取得 — タイプ・ランタイム状態・可視性・親階層 |
| `CreateDataLayerAsset` | コンテンツブラウザに新しい Data Layer アセットを作成（`DataLayerEdit` 必須） |
| `DeleteDataLayerAsset` | Data Layer アセットを削除（`DataLayerEdit` 必須） |
| `CreateDataLayerInstance` | Data Layer アセットから現在のレベルに Data Layer インスタンスを追加（`DataLayerEdit` 必須） |
| `DeleteDataLayerInstance` | 現在のレベルから Data Layer インスタンスを削除（`DataLayerEdit` 必須） |
| `SetDataLayerType` | Data Layer インスタンスのタイプを設定 — Editor または Runtime（`DataLayerEdit` 必須） |
| `SetDataLayerInitialRuntimeState` | Data Layer の初期ランタイム状態を設定 — Unloaded / Loaded / Activated（`DataLayerEdit` 必須） |
| `SetDataLayerIsLoadedInEditor` | エディタビューポートで Data Layer をロードするかどうかを設定（`DataLayerEdit` 必須） |
| `SetDataLayerVisibility` | エディタ内の Data Layer の可視性を設定（`DataLayerEdit` 必須） |
| `SetParentDataLayerInstance` | 親 Data Layer インスタンスを設定して階層を構築（最大 64 レベル・`DataLayerEdit` 必須） |
| `GetActorDataLayers` | アクターに割り当てられた Data Layer インスタンスを取得 |
| `AddActorToDataLayer` | アクターを Data Layer インスタンスに追加（`DataLayerEdit` 必須） |
| `RemoveActorFromDataLayer` | アクターを Data Layer インスタンスから除外（`DataLayerEdit` 必須） |
| `GetActorsInDataLayer` | 指定した Data Layer インスタンスに割り当てられた全アクターを一覧表示 |

### HLOD（7 コマンド）

| コマンド | 説明 |
|---|---|
| `ListHLODLayers` | プロジェクト内の全 HLOD Layer アセットを一覧表示 |
| `CreateHLODLayer` | `/Game/` 配下に新しい HLOD Layer アセットを作成（`HLODBuild` 必須） |
| `DeleteHLODs` | 指定した HLOD Layer のビルド済み HLOD データを削除（`HLODBuild` 必須） |
| `SetActorHLODLayer` | アクターを HLOD Layer アセットに割り当て（`HLODBuild` 必須） |
| `BuildHLODs` | 現在のワールドの HLOD ビルドジョブを開始。`HLODBuildJobId` を返す（`HLODBuild` 必須） |
| `CancelHLODBuild` | ジョブ ID を指定して進行中の HLOD ビルドジョブをキャンセル（`HLODBuild` 必須） |
| `GetHLODBuildStatus` | HLOD ビルドジョブの現在の状態を取得 — 実行中・完了・未発見 |

---

## UAIP.Editor.Foliage

エディタでのフォリッジタイプ管理とインスタンス配置。観測系コマンドは PIE 中でも実行可能。編集系コマンドはエディタ停止中（PIE・SIE 以外）でのみ実行可能。

### フォリッジ観測（4 コマンド）

| コマンド | 説明 |
|---|---|
| `ListFoliageTypes` | 現在のレベルの `AInstancedFoliageActor` に登録されているフォリッジタイプをインスタンス数つきで一覧表示 |
| `GetFoliageTypeInfo` | フォリッジタイプの詳細設定を取得 — メッシュパス・密度・スケール範囲・カリング距離・法線整合・傾斜角・インスタンス数 |
| `GetFoliageInstanceCount` | 配置済みインスタンスの合計数を取得。フォリッジタイプ指定でフィルタリング可能（未指定時はタイプ別内訳付きで全合計を返す） |
| `GetFoliageInstances` | 指定バウンディングボックス内のフォリッジインスタンス一覧を取得 — 位置・回転・スケールを返す |

### フォリッジタイプ管理（3 コマンド）

| コマンド | 説明 |
|---|---|
| `AddFoliageTypeToLevel` | フォリッジタイプアセットを現在のレベルの `AInstancedFoliageActor` に登録（`FoliageTypeEdit` 必須） |
| `RemoveFoliageTypeFromLevel` | フォリッジタイプの登録を解除し、全インスタンスを現在のレベルから削除（`FoliageTypeEdit` 必須） |
| `SetFoliageTypeSettings` | フォリッジタイプの設定を更新 — 密度・スケール範囲・カリング距離・法線整合・傾斜角・メッシュ（ISM タイプのみ）（`FoliageTypeEdit` 必須） |

### フォリッジインスタンス操作（4 コマンド）

| コマンド | 説明 |
|---|---|
| `AddFoliageInstances` | 指定トランスフォームにフォリッジインスタンスを配置。World Partition 対応 — 各インスタンスを正しい `AInstancedFoliageActor` セルにルーティング（`FoliageInstanceEdit` 必須） |
| `RemoveFoliageInstances` | バウンディングボックスまたは球体内のフォリッジインスタンスを `MaxRemoveCount` 件まで削除（`FoliageInstanceEdit` 必須） |
| `DeleteAllFoliageInstances` | フォリッジタイプの配置済みインスタンスをすべて削除（`FoliageBulkDelete` 必須） |
| `ResimulateProceduralFoliage` 🧩 | `ProceduralFoliageVolume` を再シミュレーションして結果インスタンスを配置（`ProceduralFoliage` プラグインおよび `FoliageInstanceEdit` 必須） |

---

## UAIP.Editor.DataRegistry 🧩

UE 5.8 Data Registry のエディタ時観測 — 一覧・スキーマ取得・機密フィールドマスキング付きキャッシュ済みアイテム取得。`DataRegistry` プラグインが必要（ブリッジ版はさらに `DataRegistryToolset` + `ToolsetRegistry` が必要）。

### ネイティブ（9 コマンド）

| コマンド | 説明 |
|---|---|
| `ListRegistries` | 登録済みの全 Data Registry を一覧表示。アイテム構造体名でのフィルタ（`StructFilter`）に対応。`IsDataRegistrySystemEnabled` / `AreRegistriesInitialized` の診断情報を同梱 |
| `GetRegistryInfo` | レジストリの ID 数・最低ソース可用性・説明・ID フォーマットを取得 |
| `GetSchema` | アイテム構造体のプロパティスキーマ（名前・型・`IsSecret` フラグ）を取得 |
| `ListItems` | レジストリに登録済みのアイテム ID を一覧表示（キャッシュ済みとは限らない） |
| `ListDataSources` | レジストリの編集時定義データソースを一覧表示 |
| `ListRuntimeSources` | レジストリの実行時展開後データソースを一覧表示 |
| `GetItems` | 指定名のキャッシュ済みアイテムを機密フィールドマスキング付きで取得。未キャッシュのアイテムは黙って省略せず `MissingItems` に理由付きで報告 |
| `GetAllCachedItems` | アイテム名を事前指定せず、現在キャッシュ済みの全アイテムを取得（1000件・1MiB を上限。Toolset に対応なし） |
| `AcquireItems` | 指定アイテムの非同期キャッシュロードをトリガー — カスタム/Remote ソースで必要（DataTable ソースは自動事前ロード済み。Toolset に対応なし） |

### Toolset ブリッジ（7 コマンド）🧩

`DataRegistryToolset` プラグイン（UE 5.8+）経由でネイティブコマンドのうち先頭7個をミラー。プロバイダ: `Toolset.Editor.DataRegistry.*`。`GetItems` はここでは挙動が異なる: 見つからないアイテムは黙って省略され、機密マスキングも適用されない — マスキングや欠損明示が必要な場合はネイティブの `GetItems` を使用すること。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.DataRegistry.ListRegistries` | `DataRegistryToolset` への passthrough |
| `Toolset.Editor.DataRegistry.GetRegistryInfo` | `DataRegistryToolset` への passthrough |
| `Toolset.Editor.DataRegistry.GetSchema` | `DataRegistryToolset` への passthrough（生 JSON 文字列、`IsSecret` フラグなし） |
| `Toolset.Editor.DataRegistry.ListItems` | `DataRegistryToolset` への passthrough |
| `Toolset.Editor.DataRegistry.ListDataSources` | `DataRegistryToolset` への passthrough |
| `Toolset.Editor.DataRegistry.ListRuntimeSources` | `DataRegistryToolset` への passthrough |
| `Toolset.Editor.DataRegistry.GetItems` | `DataRegistryToolset` への passthrough。欠損アイテムは黙って省略、マスキングなし |

---

## UAIP.Editor.MotionMatching 🧩

Pose Search プラグイン向けの Motion Matching 編集機能 — `UPoseSearchDatabase` へのアニメーション登録、`UPoseSearchSchema` の構造（ロール付きスケルトンとフィーチャーチャンネルツリー）、`UPoseSearchNormalizationSet` のメンバーシップ、非同期インデックスビルド。`PoseSearch` プラグインが必要。

> **Note**: このドメインの編集系コマンドは、自分自身の変更が反映された時点で `Success: true` を返す。これは Schema の `Finalize()` が後続で失敗して巻き戻る場合（スケルトンが未割り当て、あるいは `UPoseSearchFeatureChannel_Group` が空になった場合など）でも同じ。インデックスが構築できる状態かどうかは `Success` 単体ではなく応答の `bSchemaReadyForIndexBuild` を確認すること — ロール付きスケルトンが 1 つもない Schema は、チャンネルをいくつ追加しても `bSchemaReadyForIndexBuild: false` のままなので、先に `AddSkeletonToPoseSearchSchema` でスケルトンを設定すること。`bSchemaReadyForIndexBuild` が保証するのはこの Schema 単体の前提条件のみで、実際のインデックスビルドには Database 側が Schema を参照していること（`SetPoseSearchDatabaseSchema`）とアニメーションが登録済みであること（`AddAnimationToPoseSearchDatabase`）も必要。

### Database（6 コマンド）

| コマンド | 説明 |
|---|---|
| `GetPoseSearchDatabaseInfo` | `UPoseSearchDatabase` の構造情報を取得 — Schema/NormalizationSet 参照、PoseSearchMode、PCA/KDTree 設定、`AnimationAssets` の各エントリ（パス・クラス・有効フラグ・ミラーオプション・サンプリング範囲/グリッド）。Chooser 内包データベースは拒否 |
| `AddAnimationToPoseSearchDatabase`（要 `PoseSearchAssetEdit`） | アニメーションアセットを `InsertAt` に追加。任意のエントリ設定（有効フラグ・ミラーオプション・サンプリング範囲/グリッド）を指定可能。通常（非 BranchIn）エントリとしてすでに登録済みの場合は既定で冪等。`bAllowDuplicate: true` を指定するとこの判定を迂回し、常に新しいエントリを追加する |
| `RemoveAnimationFromPoseSearchDatabase`（要 `PoseSearchAssetEdit`） | 指定アニメーションアセットを参照する全エントリを削除。全体成功/全体失敗方式 — 一致したエントリのいずれかが PoseSearchBranchIn アニメーション通知で作成されたものだった場合は失敗 |
| `SetPoseSearchDatabaseAnimationSettings`（要 `PoseSearchAssetEdit`） | 既存の `AnimationAssets` エントリ 1 件の設定を部分更新。アニメーションパスで対象を解決し、必要な場合は `Index` で一意化。UE 5.8 限定（UE 5.7 では `Available: false`） |
| `SetPoseSearchDatabaseSchema`（要 `PoseSearchAssetEdit`） | データベースの `Schema` 参照を設定。既存の Schema を差し替えるには `bAllowOverwrite` が必要 |
| `SynchronizePoseSearchDatabase`（要 `PoseSearchAssetEdit`） | PoseSearchBranchIn アニメーション通知を持つ全 `UAnimSequenceBase` の `BranchInId != 0` エントリを、データベースの `AnimationAssets` へ明示的にマージする。エンジンにはこのマージが自動的に起きたことを観測できる確実な手段がないため、`PoseSearchBranchIn` 通知の追加・編集後（アニメーションアセットの保存後）、`GetPoseSearchDatabaseInfo` を読む前に本コマンドを呼ぶこと。⚠️ 保存と同じリクエスト内で呼ぶと 0 件になる場合がある — アセットレジストリの参照インデックスは保存後に非同期で再構築されるため、保存が落ち着いてから再実行すること。冪等 — マージ対象がなければデータベースは変更されない。Chooser 内包データベースは `NotAllowed` で拒否 |

### Schema（11 コマンド）

| コマンド | 説明 |
|---|---|
| `GetPoseSearchSchemaInfo` | `UPoseSearchSchema` の構造情報を取得 — SampleRate、DataPreprocessor、SchemaCardinality、ロール付き `Skeletons` 配列、`Finalize()` 展開後の `Channels` 配列、そして編集系コマンドが実際に対象とする finalize 前の `RawChannels` ツリー（`ChannelPath` / `ClassPath`） |
| `SetPoseSearchSchemaDataPreprocessor`（要 `PoseSearchAssetEdit`） | `DataPreprocessor` を変更（`None` / `Normalize` / `NormalizeOnlyByDeviation` / `NormalizeWithCommonSchema`）。応答にはこの Schema を参照していると見つかった全データベース（ベストエフォート）を列挙 |
| `AddPoseSearchSchemaChannel`（要 `PoseSearchAssetEdit`） | `ChannelClass` のチャンネルを作成し、チャンネルツリーへ挿入。任意で `ParentChannelPath` の下へネストし、`InsertAt` で挿入位置を指定可能。冪等ではない — 同じクラスで 2 回呼ぶとチャンネルが 2 つできる |
| `RemovePoseSearchSchemaChannel`（要 `PoseSearchAssetEdit`） | `ChannelPath` のチャンネルを、ネストされた子孫チャンネルもろとも削除。任意の `ExpectedChannelClass` で、古いパスによる誤削除を防止できる |
| `MovePoseSearchSchemaChannel`（要 `PoseSearchAssetEdit`） | `SourceChannelPath` のチャンネルを、その親の中で `TargetIndex` へ並べ替え。別の親への移動は非対応 — 削除して追加し直すこと |
| `SetPoseSearchSchemaChannelProperty`（要 `PoseSearchAssetEdit`） | `ChannelPath` のチャンネルのトップレベルプロパティへ `Value`（UE テキストインポート形式、最大 4 KiB）を書き込む。書き込み後の検証に失敗した場合は書き込みをロールバック |
| `AddDefaultPoseSearchSchemaChannels`（要 `PoseSearchAssetEdit`） | エディタの Schema ファクトリが作成するのと同じ既定チャンネル（Trajectory + Pose）を追加。既存チャンネルは削除されず維持される — 2 回呼ぶと重複したペアが追加される |
| `GetAvailablePoseSearchChannelClasses` | `AddPoseSearchSchemaChannel` が `ChannelClass` として受け付ける `UPoseSearchFeatureChannel` サブクラスを一覧表示。`bCanHostSubChannels` で有効な `ParentChannelPath` の対象を示す。Heavy コマンド — ロード済みの全 `UClass` を走査するため、結果をキャッシュすること |
| `GetPoseSearchChannelClassSchema` | チャンネルクラスの Details パネル表示プロパティを一覧表示。各プロパティについて `SetPoseSearchSchemaChannelProperty` で書き込み可能かを `bIsWritable` / `NotWritableReason` で示し、`DefaultValueText` はそのまま使えるテキストインポート形式の例を提供 |
| `AddSkeletonToPoseSearchSchema`（要 `PoseSearchAssetEdit`） | `Role` のロール付きスケルトンエントリを追加または置き換え。任意で `MirrorDataTablePath` を指定可能。既存の `Role` を置き換えるには `bAllowOverwrite` が必要 |
| `RemoveSkeletonFromPoseSearchSchema`（要 `PoseSearchAssetEdit`） | `Skeletons` 配列から `Role` のロール付きスケルトンエントリを削除 |

> **Note**: `AddPoseSearchSchemaChannel` の `ChannelClass`、および各編集コマンドの `ExpectedChannelClass` には**完全修飾クラスパス**（例: `/Script/PoseSearch.PoseSearchFeatureChannel_Position`）を渡すこと — `GetPoseSearchSchemaInfo` の `RawChannels[].ClassPath` または `GetAvailablePoseSearchChannelClasses` の `ClassPath` を使い、同じエントリの短い `ChannelClass` フィールドは使わないこと。`ChannelPath` は `RawChannels[]` に対する `/` 区切りのインデックスパス（例: `"0"`、`"2/0"`）であり、`Finalize()` 展開後の `Channels[]` に対するものでは**ない**。編集のたびに後続の兄弟チャンネルの `ChannelPath` がずれうるため、呼び出し前に取得したパスを使い回さず、都度 `RawChannels` を読み直すこと。

### NormalizationSet（4 コマンド）

| コマンド | 説明 |
|---|---|
| `GetPoseSearchNormalizationSetInfo` | `UPoseSearchNormalizationSet` の `Databases` 配列（`Index` / `DatabasePath` / `bIsNull`）を格納順で一覧表示 |
| `SetPoseSearchDatabaseNormalizationSet`（要 `PoseSearchAssetEdit`） | データベースの `NormalizationSet` 参照を設定またはクリア（`NormalizationSetPath` と `bClearNormalizationSet` は排他）。データベース側のみを編集する — 両側を一致させたい場合は `AddDatabaseToPoseSearchNormalizationSet` と併用すること |
| `AddDatabaseToPoseSearchNormalizationSet`（要 `PoseSearchAssetEdit`） | `UPoseSearchNormalizationSet` の `Databases` 配列にデータベースを追加。冪等。NormalizationSet 側のみを編集する — `SetPoseSearchDatabaseNormalizationSet` と併用すること |
| `RemoveDatabaseFromPoseSearchNormalizationSet`（要 `PoseSearchAssetEdit`） | 指定データベースを参照する全スロットを削除。一致したスロットは詰めずに null にクリアされるため、他のスロットの `Index` は変化しない |

### Index Build（2 コマンド）

| コマンド | 説明 |
|---|---|
| `StartPoseSearchDatabaseIndexBuild`（要 `PoseSearchAssetEdit`） | データベースのインデックスビルドを非同期で開始し、ポーリング用の `BuildId` を返す。対象データベースによらずエディタ全体で同時に走るビルドは 1 件のみ |
| `GetPoseSearchDatabaseIndexBuildStatus` | 1 件のビルドの `State`（`Running` / `Succeeded` / `Failed`）と `ElapsedSeconds` を取得。`Succeeded` になると `NumPoses` / `SchemaCardinality` も報告 |

> **Note**: `StartPoseSearchDatabaseIndexBuild` と `GetPoseSearchDatabaseIndexBuildStatus` は、いずれも明示的な `SessionId` を指定して呼び出す必要があり、両方で**同じ** `SessionId` を使うこと。自動生成されるセッションは呼び出しごとに異なるため、そのセッションで開始したビルドを後からポーリングできない。両コマンドとも、匿名または未指定の `SessionId` を `InvalidParams` で拒否する。

---

## UAIP.Editor.AnimSequence

`UAnimSequence` / `UAnimMontage` / `UAnimComposite` アセットの AnimNotify / AnimNotifyState エントリと通知トラックの追加・削除・編集。エンジン標準の型のみで構成されており、オプションプラグインは不要。

> **Note**: `NotifyGuid` はハイフンなしの 32 桁 16 進数（`FGuid::ToString(EGuidFormats::Digits)`）— `GetAnimNotifyInfo` が報告し、本ドメインの他の全コマンドが受け取る形式と同じ。`SetAnimNotifyProperty` はすべての書き込みで `AnimNotifyEdit` を必要とし、書き込むプロパティがハードなオブジェクト/クラス参照であるか、それを内包する場合は追加で `AnimNotifyReferenceEdit` が必要（`GetAnimNotifyClassSchema` がプロパティごとに `bIsObjectReference` として報告）。`GetAnimNotifyProperty` は読み取り専用の対となるコマンドで、`NotifyGuid` / `PropertyName` によるアドレッシングも、`SetAnimNotifyProperty` の `Value` および `GetAnimNotifyClassSchema` の `DefaultValueText` と同じテキスト形式も共通であり、ゼロ値のプロパティ（空文字列ではなく "0" / "False" / "None"）も含めて 3 コマンド間でバイト単位に往復できる。本ドメインの編集系コマンドはすべて、PIE または SIE 実行中は拒否される。

| コマンド | 説明 |
|---|---|
| `GetAnimNotifyInfo` | アセット上の全通知トラック（`TrackIndex` / `TrackName` / `TrackColor`）と全通知/通知ステートエントリ（guid・クラス・タイミング・Montage 固有フィールド）、およびアセットレベルのスカラー値（`AssetKind` / `PlayLength` / `NumTracks` / `NumNotifies` / `NumInvalidGuids`）を取得。`UAnimComposite` の場合、対象はアセット自身の `Notifies` 配列のみで、セグメントの `AnimSequence` が持つ通知は含まれない。読み取り専用、要 `EditorInspect` |
| `GetAvailableAnimNotifyClasses` | `AddAnimNotify` / `AddAnimNotifyState` が `ClassPath` として受け付ける全 `UAnimNotify` / `UAnimNotifyState` サブクラスを一覧表示。`bIsNotifyState` / `bCanBePlaced` / `NotPlaceableReason` を付与。現在ロード済みのクラスのみが対象。Heavy コマンド — ロード済みの全 `UClass` を走査するため、結果をキャッシュすること。読み取り専用、要 `EditorInspect` |
| `GetAnimNotifyClassSchema` | `UAnimNotify` / `UAnimNotifyState` サブクラスの Details パネル表示プロパティを一覧表示。各プロパティについて `SetAnimNotifyProperty` で書き込み可能かを `bIsWritable` / `NotWritableReason` で示し、`bIsObjectReference` と、そのまま使えるテキストインポート形式の例 `DefaultValueText` を提供。読み取り専用、要 `EditorInspect` |
| `GetAnimNotifyProperty` | `NotifyGuid` で識別される通知インスタンスについて、プロパティ 1 件（`PropertyName`）、または省略時・空文字時は `GetAnimNotifyClassSchema` が列挙する全プロパティを読み取る。全件読み取りは `PropertyName` / `Value` の代わりに `NumProperties` / `bTruncated` を報告し、上限超過時は切り詰める。単一プロパティ読み取りは切り詰めず、上限超過は `InvalidParams` で拒否する。秘密扱いの値は `GetAnimNotifyClassSchema` の `DefaultValueText` や `SetAnimNotifyProperty` の `AppliedValue` と同じ方式でマスクされる。アセットを変更しない。読み取り専用かつ冪等、要 `EditorInspect` |
| `AddAnimNotifyTrack`（要 `AnimNotifyEdit`） | `TrackName` という名前の通知トラックが存在することを保証し、存在しない場合は作成する（任意の `TrackColor`、既定は白）。既存判定に対して冪等 — 既存トラックの `TrackIndex` はそのまま返され、`TrackColor` は無視される。PIE/SIE 実行中は拒否 |
| `RemoveAnimNotifyTrack`（要 `AnimNotifyEdit`） | `TrackName` という名前の通知トラックを削除し、その上に置かれた全通知も削除する。以降のトラックのインデックスは 1 つずつ繰り上がる — 応答の `RemovedNotifyGuids` / `ReindexedNotifies` が影響範囲全体を報告する。すでに削除済みのトラックには `NotFound` で失敗。PIE/SIE 実行中は拒否 |
| `AddAnimNotify`（要 `AnimNotifyEdit`） | `TrackName` の `StartTime` へ単発の点通知を追加する。`ClassPath`（`UAnimNotify` サブクラス）/ `NotifyName`（クラスなし、`bRegisterOnSkeleton` で Skeleton へ任意登録可能）のいずれか一方が必須。冪等ではない — 繰り返し呼ぶと新しい `NotifyGuid` を持つ独立した通知が作成される。PIE/SIE 実行中は拒否 |
| `AddAnimNotifyState`（要 `AnimNotifyEdit`） | `TrackName` へ `[StartTime, StartTime + Duration]` にまたがる単発の通知ステートを追加する。`ClassPath` は `UAnimNotifyState` サブクラスを解決する必要がある。冪等ではない — 繰り返し呼ぶと新しい `NotifyGuid` を持つ独立した通知ステートが作成される。PIE/SIE 実行中は拒否 |
| `RemoveAnimNotify`（要 `AnimNotifyEdit`） | `NotifyGuid` で識別される通知を 1 件だけ削除する。任意の `ExpectedNotifyClassPath` / `ExpectedNotifyName` は楽観的並行性制御のガード。guid が解決できなくなった場合は no-op 成功ではなく `NotFound` で失敗する。PIE/SIE 実行中は `NotAllowed` で拒否 |
| `SetAnimNotifyEvent`（要 `AnimNotifyEdit`） | `NotifyGuid` で識別される通知のイベントフィールド（`StartTime` / `Duration` / `TrackName` / `NotifyName` / `MontageTickType` / トリガー・フィルタ設定）を部分更新する — 指定したフィールドのみが変更される。`Duration` は点通知に対しては拒否、`MontageTickType` は `UAnimMontage` 以外では拒否。PIE/SIE 実行中は `NotAllowed` で拒否 |
| `SetAnimNotifyProperty`（要 `AnimNotifyEdit`。ハードなオブジェクト/クラス参照の書き込みは追加で `AnimNotifyReferenceEdit` が必要） | `NotifyGuid` で識別される通知インスタンスのトップレベルプロパティ 1 件を、`GetAnimNotifyClassSchema` が `DefaultValueText` として報告するのと同じテキストインポート形式で書き込む。新たに `FGameplayTag` / `FGameplayTagContainer` / `FGameplayCueTag`（未登録タグ、`Categories` / `GameplayTagFilter` の範囲外のタグ、コンテナ内の重複タグはいずれも `InvalidParams` で拒否）と `FBoneReference`（対象スケルトンに存在しないボーン名、または照合先スケルトンを解決できない場合は `InvalidParams` で拒否）も書き込み可能。ソフト/ウィーク/レイジー参照、マップ、セット、参照を含むその他の構造体/配列は引き続き書き込み不可。PIE/SIE 実行中は `NotAllowed` で拒否 |
| `FixupAnimNotifyGuids`（要 `AnimNotifyEdit`） | guid が現在無効な全通知に新しい guid を割り当てる。レガシー通知はこれを実行してアセットを保存するまで、リロードのたびに不安定な guid を持ち続ける。冪等 — 修復対象がない場合も `NumFixed: 0` で成功する。PIE/SIE 実行中は拒否 |

---

## UAIP.Editor.ChaosDestruction

Geometry Collection（Chaos Destruction）編集 — `UGeometryCollection` アセットの構造・階層・ダメージ設定の読み取り、アセットの新規作成・マージ、フラクチャ（Uniform / Voronoi / Plane / Slice / Brick / Mesh / Mesh Array）、ボーンのクラスタ階層編集、ジオメトリ属性のクリーンアップ・編集、ダメージモデルとクラスタリング設定の変更。Fracture Editor Mode のツール群に対応します。本ドメインに Toolset ブリッジはありません。

書き込み系コマンドは 3 つの DefaultDenied capability で保護されています — `GeometryCollectionCreate`（2 コマンド）、`GeometryCollectionFracture`（12 コマンド）、`GeometryCollectionEdit`（11 コマンド）。詳細は [Safety & Capabilities](safety.md) を参照してください。29 コマンド中 20 コマンド（🧩 印）は追加で `Fracture` プラグインを、1 コマンド（🧩 印）は `GeometryCollectionPlugin` を必要とします。印の無いコマンドにプラグイン依存はありません。書き込み系コマンドはすべて PIE/SIE 実行中は拒否され、また設定系・マージ系コマンド（`bAllowOverwrite` を使用）を除き、対象アセットが Dataflow グラフを参照している場合は `AllowOverwrite` を指定しない限り拒否されます。

#### Observation（4）— 要 `EditorInspect`

| コマンド | 説明 |
|---|---|
| `GetGeometryCollectionInfo` | 構造サマリ — `TransformCount`・`GeometryCount`・`HierarchyDepth`・`MaterialCount`・Dataflow グラフアセットのパス・未保存変更の有無・破壊設定サマリを取得 |
| `GetGeometryCollectionClusterInfo` | ボーン単位の階層をエントリ配列として取得（`BoneIndex`・`Parent`・`Children`・`SimulationType`・`BoneName`・`Level`・`BoundingBox`）。上限 256 件、超過時は `bTruncated` を設定 |
| `GetGeometryCollectionDestructionSettings` | 完全なダメージモデル・クラスタリング設定を取得 — `DamageModel`・階層レベルごとの `DamageThreshold` 配列・`SizeSpecificData`・クラスタリング設定 |
| `SelectGeometryCollectionBones` 🧩 | ボーン選択クエリを 1 件実行（`Root` / `Parent` / `Children` / `Siblings` / `Level` / `Contact` / `Leaf` / `Cluster` / `BySize` / `ByVolume` / `ByPercentage`）し、結果のボーンインデックス配列を返す。他コマンドの `BoneIndices` パラメータへそのまま渡せる。読み取り専用だが `Fracture` プラグインが必要 |

#### Creation（2）— 要 `GeometryCollectionCreate`

| コマンド | 説明 |
|---|---|
| `CreateGeometryCollectionFromStaticMesh` 🧩 | `UStaticMesh` を変換して新規 `UGeometryCollection` アセットを作成する。`ChaosEditor` プラグインが利用可能な場合はプロジェクトの Fracture Mode 既定設定を適用する。出力先パスが既存アセットと衝突する場合は拒否する。`GeometryCollectionPlugin` が必要。新規アセットは未保存のまま残る |
| `MergeGeometryCollectionAssets` | 片方のジオメトリをもう片方へ追加する（`UGeometryCollection::AppendGeometry`）。既存データはどちらのアセットでも失われない。2 つのアセットは異なる必要がある。対象アセットは未保存のまま残る |

#### Fracture（7）— 要 `GeometryCollectionFracture`、すべて 🧩

各コマンドは選択したボーン（`BoneIndices` 省略時はルート以下すべて）をフラクチャし、切断された各ボーンをフラクチャ片で置き換えます。

| コマンド | 説明 |
|---|---|
| `FractureGeometryCollectionUniform` 🧩 | 選択した全ボーンが 1 つのランダムなサイト配置を共有する Voronoi 図でフラクチャする。Fracture Editor Mode の Uniform ツールに対応 |
| `FractureGeometryCollectionVoronoi` 🧩 | 呼び出し側が指定した Voronoi サイト（全選択ボーンで共有）でフラクチャする |
| `FractureGeometryCollectionPlane` 🧩 | 1 つ以上の切断平面でフラクチャする — 明示的な平面（`CutPlaneTransforms`）とランダム配置の平面（`NumPlanes`）は加算方式 |
| `FractureGeometryCollectionSlice` 🧩 | 軸整列グリッド状の切断平面（`SlicesX` × `SlicesY` × `SlicesZ`）でフラクチャする。Slice ツールに対応 |
| `FractureGeometryCollectionBrick` 🧩 | レンガ状パターンの切断セルグリッドでフラクチャする。Brick ツールに対応 |
| `FractureGeometryCollectionWithMesh` 🧩 | 1 つの `UStaticMesh` を切断カッターとして使用し、`CutterMeshTransforms` エントリごとに 1 回フラクチャする。Mesh Cut ツールに対応 |
| `FractureGeometryCollectionWithMeshArray` 🧩 | 1 つ以上の `UStaticMesh` アセットを切断カッターとして使用してフラクチャする。`FractureGeometryCollectionWithMesh` を複数カッターメッシュに拡張したもの |

#### Cluster hierarchy（4）— 要 `GeometryCollectionEdit`

ボーンの再親子付け・リネーム・グループ化のみを行い、ジオメトリとトポロジーは変更されません。

| コマンド | 説明 |
|---|---|
| `ClusterGeometryCollectionBones` | 選択したボーンを新しいクラスタノードの下に再親子付けする（`NewNodeAtIndex` / `NewNodeWithParent` / `AllBonesUnderNewRoot`） |
| `AutoClusterGeometryCollection` 🧩 | 選択したボーンを自動的に新しいクラスタノードへグループ化する（`AutoCluster` / `ConvexityBasedCluster` / `ClusterMagnet`）。`Fracture` プラグインが必要 |
| `UnclusterGeometryCollectionBones` | 中間クラスタノードの削除、またはボーンをルート方向へ移動する（5 モード: `MoveUpOneHierarchyLevel` / `CollapseHierarchyOneLevel` / `CollapseLevelHierarchy` / `RemoveDanglingClusters` / `RemoveClustersOfOnlyOneChild`）。ジオメトリを持つボーンが削除されることはない |
| `RenameGeometryCollectionBone` | ボーンを 1 件リネームする。任意で全子孫へも新しい名前を伝播できる（`UpdateChildren`、既定 true） |

#### Geometry editing & clean-up（11）

| コマンド | 説明 |
|---|---|
| `MergeGeometryCollectionBones` 🧩 | 選択した 2 件以上のボーンをマージする — 1 つの生存ボーンへジオメトリごと統合する（`MergeAllSelectedBones`）か、ジオメトリに触れず共有クラスタの下へ再親子付けする（`MergeSelectedClusters`）。`GeometryCollectionFracture` と `Fracture` プラグインが必要 |
| `DeleteGeometryCollectionBranch` 🧩 | 選択したボーンとその全子孫を削除する。Prune ツールに対応。選択ボーン自身がコレクションのルートの場合は削除されない。`GeometryCollectionFracture` と `Fracture` プラグインが必要 |
| `FixGeometryCollectionTinyGeometry` 🧩 | サイズ閾値未満のジオメトリ（`MergeGeometry`）またはクラスタ（`MergeClusters`）を隣接ボーンへマージする。Geometry Merge ツールに対応。`NeighborSelection` の値 `LargestContactArea` は UE 5.8 以降が必要。`GeometryCollectionFracture` と `Fracture` プラグインが必要 |
| `SplitGeometryCollectionIslands` 🧩 | 選択したボーンを非連結成分ごとに分割する。Split Islands ツールに対応。分割対象が無い場合は成功扱いの no-op となる。`GeometryCollectionFracture` と `Fracture` プラグインが必要 |
| `ValidateGeometryCollection` 🧩 | コレクション全体を対象に、未参照ジオメトリ・単一子クラスタ・孤立クラスタをクリーンアップする（少なくとも 1 つのフラグが必要）。対象が無い場合は成功扱いの no-op となる。`GeometryCollectionFracture` と `Fracture` プラグインが必要 |
| `SetGeometryCollectionBoneVisibility` 🧩 | ボーン選択（`SelectionMode: Transform`）または明示的な面選択（`SelectionMode: Face`）で面の `Visible` フラグを切り替える。`GeometryCollectionEdit` と `Fracture` プラグインが必要 |
| `SetGeometryCollectionBoneMaterial` 🧩 | ボーン選択の内側 / 外側 / 全面（`TargetFaces`）へ `MaterialID` を割り当てる — フラクチャで新たに露出した面（`TargetFaces` の `InternalFaces`）へ専用の内部マテリアルを指定する用途に有用。`GeometryCollectionEdit` と `Fracture` プラグインが必要 |
| `RecomputeGeometryCollectionNormals` 🧩 | ボーン選択の法線（`OnlyTangents` 未指定時は接線も）を再計算する — 値が古くなる操作の後に実行しても安全。`GeometryCollectionEdit` と `Fracture` プラグインが必要 |
| `SimplifyGeometryCollectionConvexHulls` 🧩 | 凸包コリジョンの三角形数を削減する（`MeshQSlim` または `AngleTolerance`）。コレクションに凸包データが無い場合は `ExecutionFailed` で失敗する。`GeometryCollectionEdit` と `Fracture` プラグインが必要 |
| `GenerateGeometryCollectionExplodedView` 🧩 | Fracture Mode ビューポートの「View Exploded Amount」スライダーが駆動する分解ビュー表示属性を書き込む。表示専用。`GeometryCollectionEdit` と `Fracture` プラグインが必要 |
| `SetGeometryCollectionBoneColors` 🧩 | 7 種類のアルゴリズム（`ByParent` / `ByLevel` / `ByCluster` / `ByLeafLevel` / `ByLeaf` / `ByAttr` / `Random`）のいずれかでボーンカラー表示属性を割り当てる。任意で頂点カラーへも転送できる。表示専用。`GeometryCollectionEdit` と `Fracture` プラグインが必要 |

#### Settings（1）— 要 `GeometryCollectionEdit`

| コマンド | 説明 |
|---|---|
| `SetGeometryCollectionDestructionSettings` | ダメージモデルとクラスタリング設定を原子的に置き換える — `DamageModel`・階層レベルごとの `DamageThreshold` 配列・`SizeSpecificData`・クラスタリング設定。部分更新モードは無い。事前に `GetGeometryCollectionDestructionSettings` で現在の設定を読み取ること |

---

## UAIP.Editor.Subsonic 🧩

Subsonic オーディオイベントシステム向け `USubsonicEventCollection` アセットの構造編集 — イベント、そのアクションシーケンス、アクションごとの Modifier、Collection/Event スコープのパラメータ、プロパティ⇔パラメータのバインディング — に加え、エディタを離れずにイベントを試聴できます。UE 5.8 以降かつ `Subsonic` プラグイン（Experimental）が必要です。UE 5.7、またはプラグイン無効時はドメイン全体が存在しません。本ドメインに Toolset ブリッジはありません。

> **Note**: アクションまたは Modifier へのインデックスベースの書き込み（`RemoveSubsonicEventAction`、`MoveSubsonicEventAction`、`SetSubsonicEventActionProperty`、`AddSubsonicActionModifier`、`RemoveSubsonicActionModifier`、`MoveSubsonicActionModifier`、`SetSubsonicActionModifierProperty`、および `InsertIndex` を明示指定した `AddSubsonicEventAction`）はすべて `ExpectedActionFingerprint`（`Move*` 系コマンドと挿入位置指定を伴う呼び出しではさらに `ExpectedActionsFingerprint`）を要求し、呼び出し側が直前に観測した値と一致しない場合は拒否されます。これは権限チェックではなく楽観的並行性制御です — インデックスベースのアドレッシングは、そうしなければ同時編集によって別のアクションを黙って壊しうるため安全ではありません。拒否された場合はコレクションを読み直すか、直前の書き込みが返した `ActionsFingerprint` / `Actions[]` を使って現在値を取得してください。
>
> `AuditionSubsonicEvent` の応答フィールドは「再生された」ではなく `EventDispatched` です — イベントが解決され、public であり、そのアクションの `Execute()` が呼ばれたことを意味するだけで、実際に何か聞こえたことを保証しません。`StopSubsonicAudition` はその executor 自身のスコープが所有する音のみを解放します — `Global` 実行スコープで開始された音は**停止しません**。試聴の発行前に、イベントから静的に到達可能な `FGameplayTag` 参照を走査し、循環している、またはチェーン深度・到達可能アクション数の上限を超える場合は `ExecutionFailed`（応答に `CyclePath`）で拒否します — 実行時にタグを組み立てるプロジェクト独自のアクション型は、このチェックからは見えません。
>
> プロパティ⇔パラメータのバインディング（`AddSubsonicPropertyBinding`）に `ParameterScope` 引数はありません — 対象の `ParameterName` は名前のみで解決され、Event スコープのパラメータは同名の Collection スコープのパラメータを覆い隠します。

#### Observation（4 コマンド）— 要 `EditorInspect`

| コマンド | 説明 |
|---|---|
| `ListSubsonicEventCollections` | AssetRegistry 経由で `USubsonicEventCollection` アセットを `AssetPath` 順に一覧表示。各エントリは `AssetPath` のみ — 詳細には `GetSubsonicEventCollectionInfo` を使用。`PageIndex` / `PageSize` でページング、`PathFilter` でコンテンツブラウザのパスプレフィックスによる絞り込みが可能 |
| `GetSubsonicEventCollectionInfo` | 1 つのコレクションの完全な event/action/modifier/parameter/binding 内訳を取得。`EventTagFilter` は `EventTag` に対するプレフィックス一致で絞り込む。`MaxEvents` / `MaxTotalItems` / `MaxResponseBytes` / `MaxContainerElements` / `MaxRecursionDepth` で上限を設定できる（下げることのみ可能、ハード上限は超えられない）。応答本文は artifact として保存され、`Data` にはサマリのみが入る。PIE 実行中でも呼び出し可能 |
| `ListSubsonicActionTypes` | 検出可能な Subsonic アクション構造体型（非 `Abstract` / 非 `Hidden` / 非 `Deprecated`）を、各型ごとに `SetSubsonicEventActionProperty` が受け付けるプロパティスキーマとともに一覧表示。必須入力は無し。`MaxTotalItems` / `MaxResponseBytes` で上限を設定可能 |
| `ListSubsonicModifierTypes` | `ActionStructPath` / `PropertyName` で指定された、ネストされた instanced-struct 配列の検出可能な派生型をすべて一覧表示し、各型について `SetSubsonicActionModifierProperty` が受け付けるプロパティスキーマを付与する。基底型はプロパティの `BaseStruct` メタデータから解決されるため、任意の `TArray<TInstancedStruct<...>>` プロパティに対して機能する |

#### Event & Action editing（7 コマンド）— 要 `SubsonicEventEdit`

| コマンド | 説明 |
|---|---|
| `AddSubsonicEvent` | `EventTag` のイベントを追加する。冪等 — 既に存在するタグの場合は何も変更せず `AlreadyExisted: true` を返す。`EventTag` は登録済みの GameplayTag である必要がある。プレイセッション実行中は拒否 |
| `RemoveSubsonicEvent` | `EventTag` のイベントを、それが所有する全アクション・Event スコープのパラメータ・プロパティバインディングごと削除し、それぞれの削除件数を報告する。`EventTag` を持つイベントが無い場合は `NotFound` で失敗。`AffectedEvents` は常に空 — イベントの削除はそのイベントにスコープされた状態のみを削除する。プレイセッション実行中は拒否 |
| `SetSubsonicEventSettings` | `EventTag` のイベントの設定を更新する。現在設定可能なフィールドは `IsPublic` のみ。少なくとも 1 つの設定を指定する必要があり、何も変更しないリクエストは no-op として成功するのではなく `InvalidParams` で拒否される。プレイセッション実行中は拒否 |
| `AddSubsonicEventAction` | `ActionStructPath` をインスタンス化し、`EventTag` のアクションシーケンスの `InsertIndex` へ挿入、省略時は末尾に追加する。`ExpectedActionsFingerprint` は `InsertIndex` を指定した場合のみ必須。更新後の `ActionsFingerprint` と、上限付きの `Actions[]` を返す。プレイセッション実行中は拒否 |
| `RemoveSubsonicEventAction` | `EventTag` のアクションシーケンスから `Index` のアクション（およびそのプロパティバインディング）を削除する。`ExpectedActionFingerprint` は常に必須。更新後の `ActionsFingerprint` と `Actions[]` を返す。プレイセッション実行中は拒否 |
| `MoveSubsonicEventAction` | `FromIndex` のアクションを移動し、`ToIndex`（移動対象を取り除いた後の配列における位置）へ配置する。`FromIndex == ToIndex` は成功する no-op。`ExpectedActionFingerprint` と `ExpectedActionsFingerprint` の両方が常に必須。プレイセッション実行中は拒否 |
| `SetSubsonicEventActionProperty` | `Index` のアクションのトップレベルプロパティ `PropertyName` へ `Value` を書き込む。ネストされた `TArray<TInstancedStruct<...>>`（`Modifiers`）プロパティは拒否される — 代わりに専用の `AddSubsonicActionModifier` / `RemoveSubsonicActionModifier` / `MoveSubsonicActionModifier` / `SetSubsonicActionModifierProperty` を使用すること。`ExpectedActionFingerprint` は常に必須。プレイセッション実行中は拒否 |

#### Action Modifier editing（4 コマンド）— 要 `SubsonicEventEdit`

| コマンド | 説明 |
|---|---|
| `AddSubsonicActionModifier` | `ModifierStructPath` をインスタンス化し、`Index` のアクションの `ModifiersPropertyName` 配列へ、`InsertIndex` または末尾に挿入する。冪等ではない — 同じ引数で繰り返し呼ぶと複数の Modifier が追加される。Modifier 配列はその所有アクションの fingerprint の一部であるため、常に `ExpectedActionFingerprint` が必須。プレイセッション実行中は拒否 |
| `RemoveSubsonicActionModifier` | `Index` のアクションの `ModifiersPropertyName` 配列から `ModifierIndex` の Modifier を削除する。常に `ExpectedActionFingerprint` が必須。プレイセッション実行中は拒否 |
| `MoveSubsonicActionModifier` | `Index` のアクションの `ModifiersPropertyName` 配列内で、`ModifierFromIndex` の Modifier を `ModifierToIndex` へ移動する。同一インデックスの指定はトランザクションを開かず成功する no-op。常に `ExpectedActionFingerprint` が必須。プレイセッション実行中は拒否 |
| `SetSubsonicActionModifierProperty` | `ModifierIndex` の Modifier のトップレベルプロパティ `PropertyName` へ `Value` を書き込む。常に `ExpectedActionFingerprint` が必須。プレイセッション実行中は拒否 |

#### Parameter editing（3 コマンド）— 要 `SubsonicEventEdit`

| コマンド | 説明 |
|---|---|
| `AddSubsonicParameter` | `Scope`（`Collection` または `Event`。`Event` の場合は `EventTag` が必須）で選択された `FInstancedPropertyBag` へ、`ParameterName` という名前のパラメータを追加する。`ParameterType` は `EPropertyBagPropertyType` の列挙子名（`Bool` / `Int32` / `Int64` / `Float` / `Double` / `Name` / `String` / `Enum` / `Object` / `Struct`）。`ValueTypePath` は `Enum` / `Object` / `Struct` でのみ必須で、それ以外では省略が必要 — struct 型の `ValueTypePath` はさらに `FGameplayTag`（現時点で書き込み可能な唯一の struct 型）に限定される。既存のパラメータ名を再度追加しようとした場合は、上書きではなく拒否される。プレイセッション実行中は拒否 |
| `RemoveSubsonicParameter` | 選択された `Scope` のバッグから `ParameterName` のパラメータを削除する。`UnboundPropertyCount` / `ReboundPropertyCount` は、そのパラメータにバインドされていた全アクションプロパティの結果を分類する — rebind されたプロパティは、同名かつ型互換の Collection レベルのパラメータが引き継いだために解決を維持できたもの（`Scope: "Event"` の場合のみ発生しうる）。選択したスコープに `ParameterName` のパラメータが無い場合は `NotFound` で失敗。プレイセッション実行中は拒否 |
| `SetSubsonicParameterValue` | 選択された `Scope` のバッグにある既存パラメータ `ParameterName` の既定値を設定する。`Value` はアクションプロパティの setter と同じ許可リストで検証され、`Float` / `Double` の NaN/Inf も拒否される。選択したスコープに `ParameterName` のパラメータが無い場合は `NotFound` で失敗。プレイセッション実行中は拒否 |

#### Property Binding editing（2 コマンド）— 要 `SubsonicEventEdit`

| コマンド | 説明 |
|---|---|
| `AddSubsonicPropertyBinding` | イベント `EventTag` の `Index` のアクションが持つ、`PropertyName` という名前のアクションプロパティを `ParameterName` のパラメータへバインドし、既存のバインディングを置き換える。プロパティが `NoBinding` メタデータを持つ場合、値の許可リスト外である場合、またはパラメータと型が非互換の場合は拒否される。`ExpectedActionFingerprint` は常に必須。プレイセッション実行中は拒否 |
| `RemoveSubsonicPropertyBinding` | イベント `EventTag` の `Index` のアクションが持つ、`PropertyName` という名前のアクションプロパティのバインディングを削除する。現在バインドされていないプロパティは no-op 成功ではなく `NotFound` として報告される。`ExpectedActionFingerprint` は常に必須。プレイセッション実行中は拒否 |

#### Audition（2 コマンド）— 要 `SubsonicEventAudition`

| コマンド | 説明 |
|---|---|
| `AuditionSubsonicEvent` | `USubsonicEventCollection` アセット内の `EventTag` のイベントを試聴する。このセッションが以前保持していた試聴があれば置き換える。`EventDispatched` の意味と到達可能性の循環チェックについては上記の Note を参照。プレイセッション実行中は拒否 |
| `StopSubsonicAudition` | このセッションが現在試聴しているものを、保持している executor の登録解除・解放によって停止する。入力は不要 — 停止対象は常にリクエスト自身の `SessionId`。冪等 — 試聴していないセッションでもコマンドが失敗するのではなく `AuditionWasActive: false` で成功する。`Global` 実行スコープで開始された音は**停止しない** — 解放されるのは executor 自身のスコープが所有するソースのみ |

---

## UAIP.Editor.GroomAsset 🧩

`UGroomAsset`（Strand-Based Hair）アセットの構造編集 — グループ/LOD/シミュレーション/補間/レンダリング設定、カード/メッシュのソース設定と派生データビルド、ガイド/ストランドのカーブ制御点、Dataflow グラフの割り当てと実行、毛根マスク/ストランドテクスチャの生成、対象メッシュへのバインディング生成、再取り込み、RBF 変形の焼き込み。`HairStrands` プラグイン（Optional・既定無効）が必要です。プラグインが無効な場合はドメイン全体が利用できません。本ドメインに Toolset ブリッジはありません — エンジンが Groom ドメイン向けの Toolset を出荷していないためです。

4 つの DefaultDenied Capability が書き込み系コマンドを制御します — `GroomAssetEdit`（12 コマンド）、`GroomAssetCreate`（3 コマンド）、`GroomCurveEdit`（4 コマンド）、`GroomBindingEdit`（3 コマンド）。詳細は [Safety & Capabilities](safety.md) を参照してください。書き込み系コマンドはすべて PIE / SIE 実行中は拒否されます。ほとんどの書き込みコマンドは対象アセットを未保存のまま残します（各コマンドの説明にその旨が明記されています）。永続化するには `UAIP.Editor.Workspace.SaveAllPackages` を使用してください。新規アセットを生成する 5 コマンド（`GenerateGroomFollicleMaskTexture`、`GenerateGroomStrandsTextures`、`CreateGroomBinding`、`CreateGeometryCacheGroomBinding`、`BakeGroomRBFDeformation`）は、応答を返す前に生成物を保存します。

#### Observation（13 コマンド）— 要 `EditorInspect`

| コマンド | 説明 |
|---|---|
| `GetGroomAssetInfo` | グループ数、グループごとの `FHairGroupInfo` フィールド（カーブ/ガイド/頂点数、最大カーブ長）、グループ自身の LOD スロット数（グループ間の最大値ではない）、アセット全体の設定（マテリアルスロット数、Dataflow アセットパス、未保存フラグ、グローバル補間 / シミュレーションキャッシュ / ヘア補間種別） |
| `GetGroomLODSettings` | 各グループの `AutoLODBias` と、全 LOD スロットの `FHairLODSettings` 全体。出力の形は `SetGroomLODSettings` の入力と一致する |
| `GetGroomSimulationSettings` | 各グループの `FHairGroupsPhysics` 全体（ソルバー、外力、曲げ/伸び/衝突拘束、ストランドパラメータ）。4 種のスカラーカーブをキー単位でシリアライズする。出力の形は `SetGroomSimulationSettings` の入力と一致する |
| `GetGroomInterpolationSettings` | 各グループの `FHairGroupsInterpolation` 全体（デシメーション・補間設定）。出力の形は `SetGroomInterpolationSettings` の入力と一致する |
| `GetGroomRenderingSettings` | 各グループの `FHairGroupsRendering` 全体（ジオメトリ/シャドウ/上級者向け設定）。出力の形は `SetGroomRenderingSettings` の入力と一致する |
| `GetGroomCardsInfo` | 全 `FHairGroupsCardsSourceDescription` エントリ（元メッシュ、ガイド種別、テクスチャレイアウトとパス、カード/頂点数）と、`"HairCardGenerator"` 実装が現在登録されているかどうか |
| `GetGroomMeshesInfo` | 全 `FHairGroupsMeshesSourceDescription` エントリ（元メッシュ、テクスチャレイアウトとパス） |
| `GetGroomGuideCurves` | 1 グループのガイドカーブ制御点を、呼び出し側が指定した 1 つ以上の範囲で取得する（「全件ダンプ」モードは無い）。範囲が 1 応答あたりの上限を超える場合は拒否ではなく切り詰め、`bTruncated` と実際に返した範囲を報告する |
| `GetGroomStrandCurves` | ストランドカーブの制御点。範囲・切り詰めの契約は `GetGroomGuideCurves` と同じで、頂点ごとの色/ラフネス/AO とカーブごとのガイドウェイトフィールドが加わる |
| `GetGroomDataflowInfo` | 現在割り当てられている `UDataflow` アセット（未割り当てなら空）と、設定されたターミナルノード名。未割り当ては通常の結果でありエラーではない |
| `GetGroomBindingInfo` | `UGroomBindingAsset` 自体のプロパティ — バインディング種別、元/対象メッシュのパス、補間点数、グループごとの `GroupInfos`、コンパイル中かどうか、有効性 |
| `ListGroomBindings` | 対象の `UGroomAsset` を参照する全 `UGroomBindingAsset`。Asset Registry のタグのみから回答し、候補となるバインディングは一切ロードしない |
| `GetGroomCacheInfo` | `UGroomCache` 自体の内容 — 種別（Strands/Guides）、フレーム範囲、尺、保存されているアニメーション情報の属性フラグ |

#### Settings & LOD writes（7 コマンド）— 要 `GroomAssetEdit`

| コマンド | 説明 |
|---|---|
| `SetGroomSimulationSettings` | 1 グループの物理設定への部分パッチ。4 種のスカラーカーブは全キー置換となる。`GetGroomSimulationSettings` が返す形をそのまま受け付けるため、Get → 編集 → Set の往復ができる |
| `SetGroomLODSettings` | 既存の 1 LOD スロットのフィールドと、所属グループの `AutoLODBias` への部分パッチ。スロットの追加・削除は行わない |
| `SetGroomInterpolationSettings` | 1 グループのデシメーション/補間設定への部分パッチ。対象が Dataflow アセットを参照している場合、`bAllowOverwrite` を指定しない限り拒否される — `GuideType` はまさに Dataflow の実行が上書きする値のため |
| `SetGroomRenderingSettings` | 1 グループのジオメトリ/シャドウ/上級者向けレンダリング設定への部分パッチ |
| `SetGroomAssetSettings` | アセット全体の 3 フィールド（`EnableGlobalInterpolation`、`EnableSimulationCache`、`HairInterpolationType`）への部分パッチ — 上記のグループ単位の書き込みと異なり `GroupIndex` を持たない |
| `AddGroomLOD` | 既定値で構築した LOD スロットを 1 つグループへ追加し、新スロットのインデックスを返す。以後の設定は `SetGroomLODSettings` で行う |
| `RemoveGroomLOD` | LOD スロットを 1 つ削除する。失われるのはそのスロット自身の設定値のみ — グループのカーブデータは無傷 — だが元に戻すには削除前の全フィールドを `AddGroomLOD` + `SetGroomLODSettings` で再適用する必要がある |

#### Cards / Meshes（4 コマンド）— 要 `GroomAssetEdit`

| コマンド | 説明 |
|---|---|
| `SetGroomCardsSource` | `FHairGroupsCardsSourceDescription` エントリを 1 つ upsert する（ガイド種別、取り込み済みメッシュ、テクスチャレイアウト/パス）— 既存の（グループ, LOD）エントリがあればパッチし、無ければ新規追加する。カードの派生データはビルドしない |
| `SetGroomMeshesSource` | `FHairGroupsMeshesSourceDescription` エントリを 1 つ upsert する。パッチ/追加の契約は同じ。メッシュの派生データはビルドしない |
| `BuildGroomCardsData` | `UGroomAsset::BuildCardsData()` を強制実行する（Derived Data Cache の参照/ビルド、Heavy、上限時間なし）。ソース記述が `GuideType == Generated` を要求しており `"HairCardGenerator"` 実装が未登録の場合、事前に `NotAllowed` で拒否する |
| `BuildGroomMeshesData` | `UGroomAsset::BuildMeshesData()` を強制実行する（Derived Data Cache の参照/ビルド、Heavy、上限時間なし） |

#### Texture generation（2 コマンド）— 要 `GroomAssetCreate`

| コマンド | 説明 |
|---|---|
| `GenerateGroomFollicleMaskTexture` | 元の Groom 自身のパッケージの隣に新規の毛根マスク `UTexture2D` を作成し、そのピクセル生成を投入する。保証されるのは投入のみ — GPU での生成/読み戻しは以降の複数フレームにわたって完了するが、エンジンは完了シグナルを一切公開しない。生成したテクスチャを Groom へ紐付けはしない — 紐付けには `SetGroomCardsSource`/`SetGroomMeshesSource` を使用する |
| `GenerateGroomStrandsTextures` | 選択した Layout が要求するスロット数分の新規ストランドテクスチャ（`UTexture2D`）を作成し、SkeletalMesh または StaticMesh に対してストランド形状をトレースして生成を投入する。投入のみ保証・自動紐付けなしという契約は `GenerateGroomFollicleMaskTexture` と同じ |

#### Curve editing & Dataflow（4 コマンド）

| コマンド | Capability | 説明 |
|---|---|---|
| `SetGroomGuideCurves` | `GroomCurveEdit` | グループ内の 1 つ以上の範囲について、ガイドカーブの制御点を単一の `ConvertFromGroomAsset` → `ConvertToGroomAsset` 往復で差し替える。`GetGroomGuideCurves` が返す形をそのまま受け付ける。書き込みはカーブの追加・削除を一切行わず、（読み取りと異なり）範囲がグループの終端を越える場合は切り詰めではなく拒否される。対象が Dataflow アセットを参照している場合、`bAllowOverwrite` を指定しない限り拒否される |
| `SetGroomStrandCurves` | `GroomCurveEdit` | `SetGroomGuideCurves` と同じ契約で、ストランドカーブを対象とする |
| `SetGroomDataflowAsset` | `GroomAssetEdit` | Dataflow 割り当て（アセットパス / ターミナルノード名）への部分パッチ。非破壊 — 割り当てを変更するだけで、グラフを実行したりカーブデータに触れたりはしない |
| `EvaluateGroomDataflow` ⚠️ | `GroomCurveEdit` | **Experimental — 現時点で有用な結果を生みません。** 割り当てられた Dataflow グラフを実行する（`FDataflowInstance::UpdateOwnerAsset()`）。全グループのガイド/ストランドのカーブ形状と `GuideType` をグラフの出力で上書きする — 実行前のカーブはこのコマンドでは復元できない。Dataflow アセットが割り当てられていない場合は `NotFound` を返す。**既知のエンジン側の不具合**: Groom の終端ノードは `FDataflowTerminalNode` の 2 引数版 `Evaluate()` しか実装しておらず、`UpdateOwnerAsset()` が呼ぶ 1 引数版の基底実装は `ensure(false)` である。そのためグラフは評価されないまま終端ノードが空の結果を書き込み、**対象のヘアグループが消える**。エンジン自身の経路（コンテンツブラウザの Re-evaluate Dataflow、`RegenerateAssetFromDataflow` / `EvaluateTerminalNodeByName`）でも同じ結果になるため、本コマンド固有の問題ではない。UE 5.8 で確認。成功応答は「要求がエンジンへ届いた」ことを示すに留まるので、実行後にグループ数を確認すること |

#### Bindings（3 コマンド）— 要 `GroomBindingEdit`

| コマンド | 説明 |
|---|---|
| `CreateGroomBinding` | Groom を対象の `USkeletalMesh` にバインドする新規 `UGroomBindingAsset` を作成し、ビルド完了まで待ってから結果を保存する。元メッシュ（Source）を省略すると、後で `BakeGroomRBFDeformation` に使えないバインディングになる。指定パスが既存アセットと衝突した場合は上書きせず別名（連番）で作成し、応答が実際のパスを報告する |
| `CreateGeometryCacheGroomBinding` | `CreateGroomBinding` と同じ契約で、代わりに `UGeometryCache` へバインドする（このバインディング種別ではビルドは同期実行） |
| `RebuildGroomBinding` | 既存バインディングの派生データをその場で再ビルドし、ビルド完了まで待ってから応答する。同じバインディングを別のリクエストが既にビルド中の場合は待たずに即座に `TooManyRequests` を返す。再ビルドの失敗は元に戻せない — エンジンは再生成の前に既存の派生データを破棄するため |

#### Import / Bake（2 コマンド）

| コマンド | Capability | 説明 |
|---|---|---|
| `ReimportGroom` | `GroomCurveEdit` | Groom のヘア記述を、元ファイル（省略時はアセット自身の既存の取り込みファイル）から新たに翻訳した内容で置き換え、派生データをその場で再ビルドする。元ファイルの翻訳自体が失敗した場合、アセットは変更されない。翻訳は成功したが後続の取り込み/再ビルドが失敗した場合、アセットの以前の内容が保たれる保証はない。対象が Dataflow アセットを参照している場合は `bAllowOverwrite` を指定して再取り込みする |
| `BakeGroomRBFDeformation` | `GroomAssetCreate` | バインディングの RBF 変形を、そのバインディングの元 Groom から複製した（カード/メッシュのジオメトリを含む）新規の `UGroomAsset` へ焼き込む。元の Groom とバインディングは一切変更しない。バインディングが元/対象両方の SkeletalMesh を持ち、かつ全グループのデシメーションが無効（`VertexDecimation=1`、`CurveDecimation=1`）であることを要求し、満たさない場合は事前に拒否する。**検証可能な前提条件をすべて満たしていても、エンジン自身の RBF ルートデータ生成が予測不能な形で失敗し、エディタプロセスがクラッシュすることがある** — このコマンドが `GroomAssetCreate`（既定無効）の背後にあるのは、まさにこの残存リスクのためである |

---

## UAIP.Editor.Validation 🧩

プロジェクトが登録したアセットバリデータを、少数のアセットに対してもコンテンツフォルダ全体に対しても実行し、検出された内容を読み、バリデータが提供する修正を適用します。何が「正しい」かを UAIP が決めることはありません — 判定はすべて `UEditorValidatorSubsystem` と、そこにエンジンおよびプロジェクトが登録したバリデータに由来します。`DataValidation` プラグインが必要です。このドメインに Toolset ブリッジは存在しません。

> **前提条件**: `DataValidation` はエンジン同梱で既定有効ですが、UAIP がリンクするのはプロジェクトが**明示的に**宣言している場合だけです。`.uproject` の `Plugins` 配列へ `{ "Name": "DataValidation", "Enabled": true }` を追加してリビルドしてください。このエントリがないとドメインごと `uaip_list_commands` に現れず、`uaip_list_commands(IncludeUnavailable=true)` が `UnavailableReason: HandlerUnavailable` を返します。

> **Note — マテリアル検証にはさらに設定が必要です**: エンジンのマテリアルバリデータは、プロジェクトの `MaterialValidationPlatforms` 設定が空の間はすべてのマテリアルをスキップします。このプラットフォーム一覧はバリデータのクラスデフォルトオブジェクトの構築時に 1 度だけ作られるため、**設定変更はエディタを再起動するまで反映されません**。`ListValidators` はこれについて観測できる内容を `MaterialValidation` として返しますが、`EffectivelyRunnable` は答えではなく推定値です — バリデータが実際に保持している一覧は外部から読めないため、すべてのフラグが true でもマテリアルがスキップされることがあります。
>
> **Note — この設定は UAIP からは書き込めません**: `UAIP.Editor.Engine.ConfigSettings.SetSettingsValues` は `MaterialValidationPlatforms` を受け付けて `ChangedCount: 1` を返し、続く `SaveSettings` も成功し、その直後の `ListValidators` は `PlatformsConfigured: true` を返します — しかし値はメモリ上の設定オブジェクトにしか届いていません。どの `.ini` にも書き込まれず、エディタを再起動すると失われます。設定は **Project Settings → Editor → Data Validation → Material Validation Platforms** から行うか、`Config/DefaultEditor.ini`（`[/Script/DataValidation.DataValidationSettings]` セクション）を直接編集し、その後エディタを再起動してください。
>
> **Note — ジョブの結果は 1 回の呼び出しと一致するとは保証されません**: `StartValidationJob` はエディタを操作可能なまま保つために少しずつ検証しますが、エンジンはバッチ単位の検証フックをチャンクごとに発火させます。そのため、バッチ全体を集約するプロジェクト独自バリデータは 1 つのバッチではなく複数のバッチを見ることになります。一致が重要な場合は `ValidateAssets`（1 回の呼び出しで検証。最大 8 件）を使ってください。
>
> **Note — 修正はエンジンではなくプロジェクトが提供するものです**: エンジン同梱のバリデータは修正を 1 つも生成しないため、`Assets[].Fixes[]` が空なのは異常ではなく通常の状態です。修正は、それを提供するバリデータをプロジェクトが自作している場合にのみ現れます。また、検証と修正の届く範囲は意図的に異なります — 検証はエンジン・プラグインコンテンツを含むすべてのマウント済みコンテンツルートを読みますが、`ApplyValidationFix` は UAIP が書き込まないルート（`/Engine/` など）配下のアセットを `NotAllowed` で拒否します。その種のアセットはプロジェクトコンテンツへ複写してから修正してください。
>
> **Note — `ListValidators` 以外のすべてのコマンドは明示的な `SessionId` を要求します**。検証は開始した呼び出しの後から追跡・取得・修正されるものであり、それに到達できるのは開始したセッションだけだからです。呼び出し元セッションが到達できない識別子は、理由を問わず（不明・期限切れ・他セッションのもの・ジョブ系コマンドへ `ResultId` を渡した場合）すべて `NotFound` となります。なお `ListValidators` が列挙できるのはエンジンが**有効とみなす**バリデータだけで、無効なものが何件あるかは観測できません。

#### Validator observation（1 コマンド）— 要 `EditorInspect`

| コマンド | 説明 |
|---|---|
| `ListValidators` | エディタが現在有効とみなしているバリデータを、`ClassPath` / `ClassName` / `IsEnabled` とともに列挙し、`EnabledCount` と `MaterialValidation` ブロック（`ValidatorPresent`、`SettingsEnabled`、`PlatformsConfigured`、`EffectivelyRunnable`、`Note`）を返します。「問題がなかった」のか「そもそも検査されていない」のかを切り分けるために使います。このドメインで唯一、明示的な `SessionId` なしで呼べるコマンドです |

#### Validation（2 コマンド）— 要 `AssetValidation`

| コマンド | 説明 |
|---|---|
| `ValidateAssets` | 1〜8 件のアセットを同期的に検証して結果を返します。無効だったアセット、警告のあるアセット、検査されなかったアセットは個別に列挙され、何も見つからなかったアセットは `Summary` に集計され、`IncludeValid` が true のときにのみ列挙されます。結果 JSON は 64 KiB 未満の間はインラインで返され、いずれにせよ artifact としても書き出されます。⚠️ 本コマンドには時間予算も中断点も進捗取得もありません — マテリアル 1 件の検証だけでシェーダーコンパイルを伴い数秒かかりうるため、重いアセットを含む呼び出しはエディタを数秒〜数十秒応答させなくしうることに注意してください。`ResultId` は、結果に修正が 1 件以上含まれるときにのみ返ります。`AssetPaths` 内で重複したパスは、黙って重複除去せず `InvalidParams` で拒否します（8 件を明示指定したのに 7 件しか検証されない結果は分かりにくいため） |
| `StartValidationJob` | フォルダ（`PackagePath` + `Recursive`）または明示的な `AssetPaths` リスト — どちらか一方だけであり、両方指定も両方省略も不可 — を複数フレームに分けて検証し、結果ではなく `JobId` を返します。`MaxAssets` は、リダイレクタ解決と外部オブジェクトの所有者への畳み込みの後に残る件数を制限します（切り捨てた場合は `Summary.AssetLimitReached` が立ちます）。列挙だけで内部上限を超えるほど広いフォルダは、先頭の一部を検証するのではなく `EnumerationLimitExceeded` で失敗しますので、`MaxAssets` を下げるのではなくフォルダを絞ってください。同一セッションのジョブが実行中に 2 つ目を開始すると前のジョブが中断され `ReplacedPreviousJob` が返り、前回からの間隔が短すぎる場合は `TooManyRequests` が返ります。`Recursive` は `PackagePath` と併用したときにのみ意味を持つため、`AssetPaths` と同時に指定した場合は黙って無視せず拒否します（20,000 件を超える `AssetPaths` も同様です） |

#### Job observation & control（3 コマンド）— 要 `EditorInspect`

| コマンド | 説明 |
|---|---|
| `GetValidationJobStatus` | ジョブの進捗を問い合わせます。`State`（`Preparing` / `Enumerating` / `Normalizing` / `Validating` / `Finalizing` / `Completed` / `Failed` / `Aborted`）、`PhaseLabel`、`ProcessedCount` / `TotalCount`、`ElapsedSeconds`、`FailureReason`（固定の列挙値。失敗するまでは `None`）、および途中集計の `NumInvalid` / `NumWarnings` を返します。返されるのは件数・状態・経過秒だけで、バリデータのメッセージもアセットパスも含まれません。応答コストはジョブの規模によらず一定なので、ポーリングが検証を遅くすることはありません |
| `GetValidationJobResult` | ジョブが生成した結果を取得します。ジョブ全体の集計をインラインで、完全な結果を JSON artifact として返します（無効だったアセット・警告のあるアセット・検査されなかったアセットの明細）。ここで再検証・再走査は行いません。完了したジョブだけでなく、失敗したジョブや中断されたジョブに対しても結果を返します — 停止するまでに検証されていた分は artifact に含まれ、何が落ちたかは `Truncation` が説明します。未完了のジョブに対して部分結果を返すことはありませんので、先にステータスをポーリングしてください。読み取りに成功するとジョブの保持期限が延長されます |
| `CancelValidationJob` | ジョブを次のチャンク境界で停止します — **即時ではありません**。エンジンの検証呼び出しは一度入ると中断できないため、実行中のチャンク 1 つ分は最後まで走り、その結果も保持されます。直後に進捗を見るとまだ実行中に見えることがあります。ジョブは識別子と結果を保持したまま `Aborted` になります（長い実行を途中で止める目的は通常これです）。すでに終了したジョブへの中断要求は成功し、`WasRunning: false` を返して何もしません。⚠️ ジョブを `Aborted` へ遷移させる状態変更を伴いますが、観測系コマンドと同じく read-only 宣言・`EditorInspect` ゲートです。これを境界づけているのはジョブの所有権です |

#### Fix application（1 コマンド）— 要 `AssetValidationFix`

| コマンド | 説明 |
|---|---|
| `ApplyValidationFix` | バリデータがメッセージに添えて提供した修正を 1 件適用します。`ResultId`（`StartValidationJob` が返した `JobId`、または `ValidateAssets` が返した `ResultId`）と、その結果の `Assets[].Fixes[]` から引いた `FixId` で指定します。修正は 1 件ずつ適用します。ある修正を適用すると排他関係にあった他の修正が適用不可になりうるため、応答には `UpdatedFixes`（その結果が保持する全修正の適用可否を適用後に再取得したもの）が含まれます。修正へはそれを生成した結果経由でしか到達できません — その結果が保持していない識別子は `NotFound` となり、識別子の文字列からアセットを引き当てることはありません（検証していないアセットの修正に結果をチケットとして使えないため）。`AssetSaved` はアセットがディスクへ保存されたかを表します。このドメインで唯一 read-only ではないコマンドで、`DisableSave` が有効な間は一律に拒否されます（修正が保存を伴うかどうかを fixer に事前に問う手段がないため） |

---

## UAIP.Runtime.PIE

PIE セッションのライフサイクル。実行中ワールドの操作は [`UAIP.Runtime.World`](#uaipruntimeworld) にあります。

| コマンド | 説明 |
|---|---|
| 🆓 `StartPIE` | Play-in-Editor セッションを開始 |
| 🆓 `StopPIE` | アクティブな PIE セッションを停止 |
| 🆓 `PausePIE` | アクティブな PIE セッションを一時停止 |
| 🆓 `ResumePIE` | 一時停止中の PIE セッションを再開 |
| 🆓 `LoadMap` | アクティブな PIE セッションでマップをロードし完了を待つ |
| 🆓 `GetPIEState` | 現在の PIE 状態を返す — `Running`・`Stopped`・`Paused`・`Simulating` |

### Toolset ブリッジ（3 件）🧩

`EditorAppToolset`（UE 5.8+、EditorToolset プラグイン）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.Toolset.PIE.*`。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.Toolset.PIE.StartPIE` | PIE セッションを開始（非同期、`PIEControl` 必要） |
| `Toolset.Editor.Toolset.PIE.StopPIE` | PIE セッションを停止（非同期、`PIEControl` 必要） |
| `Toolset.Editor.Toolset.PIE.IsPIERunning` | PIE が実行中かどうかを返す |

---

## UAIP.Runtime.World

**実行中**のゲームワールドの操作・検査。旧バージョンではこれらは `UAIP.Runtime.PIE` 配下に登録されていました。

| コマンド | 説明 |
|---|---|
| `SpawnActor` | アクティブな PIE ワールドに指定クラスのアクターをスポーン（`RuntimeActorManipulation` 必要） |
| `DestroyActor` | アクティブな PIE ワールドのアクターを破棄（`RuntimeActorManipulation` 必要） |
| `TeleportActor` | アクターをワールド空間の指定位置 / 回転にテレポート |
| `PossessActor` | プレイヤーコントローラーにアクターを憑依させる |
| `SetTimeScale` | アクティブなゲームワールドのグローバル時間スケールを設定 |
| `QuitGame` | 実行中のゲームプロセスの正常終了をリクエスト |
| `ExecuteConsoleCommand` | アクティブなゲームワールドでコンソールコマンドを実行（`RuntimeExecCommand` 必要） |
| `GetConsoleVariable` | コンソール変数の値・型・ヘルプテキストを取得。機微な名前は not found 扱い（`RuntimeCVarRead` 必要） |
| `SearchConsoleVariables` | ワイルドカード（`*`）でコンソール変数を検索。`MaxResults` は既定 50・最大 200、機微な名前は除外 |

### Toolset ブリッジ（1 件）🧩

`EditorAppToolset`（UE 5.8+、EditorToolset プラグイン）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.Toolset.World.*`。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.Toolset.World.SearchCVars` | コンソール変数を名前の部分一致で検索。機微な変数は除外（`CVarInspect` 必要） |

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

GameplayAbilities 状態の検査と実行時操作。`GameplayAbilities` プラグインが必要で、注記のあるもの以外は PIE 必須です。

#### 検査（8）

| コマンド | 説明 |
|---|---|
| `GetAttributeValues` 🧩 | アクターの全 AttributeSet 属性値（currentValue / baseValue） |
| `GetActiveEffects` 🧩 | アクターの有効中ゲームプレイエフェクト（Level・StackCount・残時間） |
| `GetGrantedAbilities` 🧩 | アクターに付与されているアビリティ（Class・IsActive・ActiveCount・InputID） |
| `GetActiveTags` 🧩 | アクターが所有する GameplayTags |
| `FindAttributeSetClasses` 🧩 | PIE ワールド内アクターを走査し `UAttributeSet` クラス一覧を返す（MaxActors 上限） |
| `ListAttributes` 🧩 | AttributeSet クラスに定義されている全属性名 |
| `GetAbilityAssetInfo` 🧩 | `UGameplayAbility` クラスの CDO レベルのメタデータ（コスト・クールダウン・タグ）。**PIE 不要** |
| `GetEffectAssetInfo` 🧩 | `UGameplayEffect` クラスの CDO レベルのメタデータ（Duration Policy・Modifier・付与タグ）。**PIE 不要** |

#### 操作（9）

いずれも `RuntimeGASManipulation` Capability と PIE セッションが必要です。

| コマンド | 説明 |
|---|---|
| `GrantAbility` 🧩 | アクターの AbilitySystemComponent に GameplayAbility を付与 |
| `RemoveAbility` 🧩 | 付与済みの GameplayAbility を削除 |
| `ClearGrantedAbilities` 🧩 | アクターの付与済み GameplayAbility をすべて削除 |
| `ApplyEffect` 🧩 | アクターに GameplayEffect を適用 |
| `RemoveEffect` 🧩 | 指定 GameplayEffect クラスの有効インスタンスをすべて削除 |
| `ClearActiveEffects` 🧩 | 有効な GameplayEffect をすべて削除（`TagFilter` で絞り込み可） |
| `SetAttributeValue` 🧩 | 属性の base 値を設定（`AttributeName` は `UMyAttributeSet.Health` 形式） |
| `ResetAttributesToBase` 🧩 | 全属性の current 値を base 値へリセット |
| `SendGameplayEvent` 🧩 | アクターへ GameplayEvent を送信（magnitude 任意） |

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

## UAIP.Runtime.Engine.Log

ランタイム環境でのログ詳細レベル取得・ログカテゴリ一覧取得。`UAIP.Editor.Engine.Log` の Runtime 版に相当します。

| コマンド | 説明 |
|---|---|
| 🆓 `GetLogVerbosity` | 指定ログカテゴリの現在の詳細レベルを取得 |
| 🆓 `GetLogCategories` | 登録済みログカテゴリ名をすべて一覧表示 |
| `SetLogVerbosity` | ログカテゴリの詳細レベルを設定（`LogVerbosityEdit` 必要） |

---

## UAIP.Runtime.Engine.Plugin

エディタ / パッケージ版ビルド共通で使えるプラグイン観測コマンド（読み取り専用）。

| コマンド | 説明 |
|---|---|
| 🆓 `ListPlugins` | インストール済みプラグインと有効 / 無効状態の一覧 |
| 🆓 `GetPluginInfo` | プラグインの基本情報（名前・バージョン・有効状態）を取得 |
| 🆓 `IsEnabled` | プラグインが現在有効か確認 |
| 🆓 `GetPluginDependencies` | プラグインが依存するプラグイン一覧を返す |
| 🆓 `GetPluginForAsset` | 指定アセットを提供するプラグインを返す |

---

## UAIP.Runtime.Engine.CVar

エンジン全体のコンソール変数（CVar）を取得・検索・設定するコマンド。CVar は World 非依存のグローバル状態です。機密パターンの CVar は自動除外されます。

🔒 は `RuntimeCVarRead`（DefaultDenied）が必要。✏️ は `RuntimeCVarWrite`（DefaultDenied）が必要。デモ版配布物の `Config/DefaultUAIP.ini` は `RuntimeCVarRead` を事前付与しているため、以下の 🆓 コマンドはデモ版でもそのまま利用できます。

| コマンド | 説明 |
|---|---|
| 🆓🔒 `GetConsoleVariable` | 指定した CVar の名前・現在値・型・ヘルプテキストを返す（機密名は `NotFound`） |
| 🆓🔒 `SearchConsoleVariables` | ワイルドカード（`*`）パターンで CVar を検索（デフォルト 50 件・上限 200 件） |
| ✏️ `SetConsoleVariable` | 指定した CVar の値を設定（機密名・`ECVF_ReadOnly` 付きは拒否。`ECVF_Cheat` 付きは `AllowCheatCVarWrite` が有効でない限り拒否） |
| ✏️ `ResetConsoleVariable` | 指定した CVar をデフォルト値にリセット（機密名・`ECVF_ReadOnly` 付きは拒否。`ECVF_Cheat` 付きは `AllowCheatCVarWrite` が有効でない限り拒否） |

> **注意**: `UAIP.Runtime.PIE` にあった旧 `GetConsoleVariable` / `SearchConsoleVariables` コマンドは非推奨です（v1.2 で削除予定）。本コマンド群を使用してください。

---

## UAIP.Runtime.Engine.Config

ランタイムおよびパッケージ版ビルドで ini キーを直接読み書きするコマンド群。`ISettingsModule` を経由せず ini ファイルに直接アクセスします。書き込みコマンドはパッケージ版ビルドでは実行できません。

| コマンド | 説明 |
|---|---|
| 🆓 `GetConfigValue` | セクション名とキー名を指定して ini キーの文字列値を読み取る。Capability 不要 |
| `SetConfigValue` | raw ini キーを書き込みまたは削除。`ConfigSettingsEdit` 必要。パッケージ版ビルドでは実行不可。キー・値フィールドへの ini インジェクション文字（`[`・`]`）は拒否 |

---

## UAIP.Runtime.Insights.Trace

Unreal Insights のトレース採取を制御するコマンド群。トレースは常に `Saved/Profiling/UAIP/` 配下のファイルへ書き出されます — **本モジュールのどのコマンドもトレースをネットワーク宛先へ送出できません**。UAIP が開始していないトレースは一切変更しません。`GetTraceStatus` は「他者が採取中である」ことのみを報告し、`StopTrace`（明示的に拒否）を除く制御コマンドはそのトレースに触れません。

読み取り 3 コマンドは `RuntimeInsightsInspect`（DefaultAllow）が必要です。制御 8 コマンドは `RuntimeInsightsControl`（DefaultDenied）が必要です。採取した `.utrace` ファイルの添付にはさらに `RuntimeInsightsAttachTraceFile`（DefaultDenied）が必要です — 詳細は [安全性と Capability](safety.md#runtime-insights-トレース採取) を参照してください。

トレース採取は PIE のライフサイクルから独立しています。PIE の開始・停止はトレースを開始も停止もせず、トレースは PIE セッションをまたいで採取を続けます。

### 読み取り（3）

| コマンド | 説明 |
|---|---|
| 🆓 `ListTraceChannels` | このビルドが認識するすべてのトレースチャネルを一覧（説明・現在の有効状態・切り替え可否・開示しうる内容）。エンジンが宣言するチャネルプリセットも、展開後のチャネルとその開示クラスとともに一覧します。エンジンのプリセットは大半がログチャネルを含むため、プリセットを `StartTrace` に渡す前に展開後の開示クラスを確認してください |
| 🆓 `GetTraceStatus` | エンジンが採取中か・採取が一時停止中か・稼働中のトレースが UAIP の開始したものかを報告。UAIP が開始したトレースについてはラベル・ファイル名・チャネル・開示クラス・経過時間・ファイルサイズ・自動停止の上限も報告します。UAIP が開始していないトレースについては活動の種別のみを報告し、宛先・チャネル集合・経過時間・サイズは秘匿します。経過時間とサイズは監視間隔ごとに更新されるため、最大で 1 間隔分古い値になりえます |
| 🆓 `ListTraceFiles` | UAIP が採取したトレースファイルを新しい順に一覧（ラベル・サイズ・ファイル名に埋め込まれた UTC タイムスタンプ。`MaxCount` は既定 50・上限 500）。ここに出た `FileName` が `AnalyzeTrace` の受け付ける値です。SafetyPolicy で外部トレース解析が有効な場合は、設定された外部ディレクトリ内の `.utrace` も `Source: External` として一覧します。一覧は何も削除しません（ローテーションはトレース開始時に行われます） |

### トレース制御（8）

| コマンド | 説明 |
|---|---|
| `StartTrace` | 指定したチャネル / チャネルプリセットを有効にして UAIP 専用のトレースディレクトリへ採取を開始し、書き込み先のファイル名を返します。`Channels` は必須、`Label`・`MaxDurationSeconds`（既定 300、範囲 1〜3600）・`MaxFileSizeMB`（既定 512、範囲 1〜4096）は省略可。UAIP が既に開始しているトレースは再起動されず、追加分のチャネルを有効化して `AlreadyRunning` / `LimitsIgnored` を報告するだけです。**実効チャネル集合**（既に有効 ∪ 要求）がログテキストを記録し `AllowLogDump` が false の場合は `PolicyViolation` で拒否します（要求を通すためにチャネルを無効化することはありません）。同じ集合に、ポリシーが生ファイルの引き渡しを認めない内容が含まれる場合は、`Warnings` に該当チャネル名と設定名を含む `AttachDisabledByPolicy` を返します（持ち出す前提の採取を無駄に始めずに済みます）。両上限は 1 秒ごとの確認のため、サイズ上限は厳密な天井ではありません |
| `StopTrace` | UAIP が開始したトレースを停止し、`AttachTraceFile` が true なら採取した `.utrace` を artifact として引き渡します。停止は常に成功します（何も採取していなければ成功の no-op、停止直後に再度停止した場合も同じ no-op — エンジンはトレースの後始末が終わるまで接続を稼働中として報告し続けますが、呼び出し元から見れば既に終わっています。ファイルを引き渡せない場合も `AttachSkippedReason` を付けてスキップし停止自体は成功）。UAIP が開始していないトレースは停止せず `NotAllowed` を返します。⚠️ ファイルの添付は、チャネル構成に関わらず**プロセスのコマンドラインを必ず開示します**。採取中にチャネル集合が変更されたトレース、未分類チャネルを含む集合、64 MB を超えるファイルは添付を拒否します。ログテキストを含む集合には `AllowLogDump`、ホスト側パス / 画面内容 / ネットワークアドレスを含む集合には `AllowDisclosingTraceAttachment` が必要です（エディタではエンジンが log / screenshot チャネルを自分で有効化するため、通常は両方必要になります）。停止しただけでは採取ファイルは閉じられません — エンジンのトレースライタが少し遅れて別スレッドで閉じます — そのためファイルを要求した場合は最大 3 秒まで解放を待ち、それでも書き込み中なら `AttachSkippedReason: "TraceFileStillOpen"` を返します（少し待ってから再度要求する価値があります）。ファイルを要求しなかった場合は待機しません |
| `PauseTrace` | 本モジュールが開始したトレースの採取を、停止せずに一時停止します。冪等（既に一時停止中なら `WasPaused: false`）、UAIP が開始したトレースが稼働していなければ成功の no-op、UAIP が開始していないトレースには `NotAllowed`。一時停止中もチャネル監視は動き続け、時間上限は実際に採取していた秒数のみを消費します |
| `ResumeTrace` | `PauseTrace` で一時停止した採取を再開します。冪等（一時停止中でなければ `WasResumed: false`）、UAIP が開始していないトレースには `NotAllowed`。名前が `Channel` で終わらないチャネルが再開時に復帰しないというエンジン側の既知不具合があるため、復帰しなかったチャネルは `Warnings` に `ChannelNotRestoredAfterResume` として報告されます（`SetTraceChannels` で再有効化できます） |
| `SetTraceChannels` | 本モジュールが開始したトレースの採取を続けたままチャネルを有効化 / 無効化します。`EnableChannels` / `DisableChannels` の少なくとも一方が非空である必要があります。チャネル状態はトレースより長く残るため、トレース非稼働時および UAIP が開始していないトレースに対しては `NotAllowed`。判定は「適用後に有効となる集合」に対して行うため、開示するチャネルを**無効化する**要求がそれ自体で拒否されることはありません。⚠️ 本コマンドを使うとトレースのチャネル集合が外部変更済みとしてマークされ、`StopTrace` はファイルの添付を拒否するようになります |
| `AddTraceBookmark` | 採取中のトレースへ時点マーカー（`Text`）を書き込みます。ブックマークチャネルが無効な場合（何も採取していない時点を含む）は何も書き込まず、`Written: false` で成功します。テキストは解析済みトレースからログテキストと同じポリシーで読み出されるため、`AllowLogDump` が false のときは `PolicyViolation` で拒否します。テキスト中の絶対パスは可搬なプレースホルダに置換されます |
| `BeginTraceRegion` | 採取中のトレースに名前付き区間（`Name`、省略可の `Category`）を開き、それを閉じるための `RegionId` を返します。区間は名前ではなく id で対応付けるため、入れ子の区間や同名の区間も区別されます。区間チャネルが無効でも `RegionId` は返り（`Written: false`）、閉じ方は同じです。開いたままの区間はトレース停止時とモジュール終了時に自動で閉じられます。`AddTraceBookmark` と同じく `AllowLogDump` でゲートされます |
| `EndTraceRegion` | `BeginTraceRegion` が開いた区間を `RegionId` で閉じます（開いている区間を指さない id は `NotFound`。自動クローズ済みの id を含む）。`DurationSeconds` はプロセス内で計測するため、区間チャネルが無効で何も書き込まれていなくても報告されます。自身はテキストを持たないため、ログダンプポリシーで拒否されることはありません |

---

## UAIP.Runtime.Insights.Analysis

採取済み `.utrace` ファイルのオフライン解析。本 Provider はトレース解析が有効なビルド構成でのみ登録されます。それ以外（デモ版を含む）ではコマンド自体が存在せず、呼び出すたびに失敗するのではなく `CommandNotFound` を返します。

3 コマンドすべてが `RuntimeInsightsAnalyze`（DefaultDenied）を必要とします（ステータス取得も同様。トレースを解析できない呼び出し元にとって解析の進捗は用途がないため）。

解析は非同期です。`AnalyzeTrace` で `AnalysisId` を取得し、`GetTraceAnalysisStatus` を `State` が `Completed` になるまでポーリングしてから `GetTraceAnalysisResult` を読みます。同時に実行できる解析は 1 件のみで、パース中 / 抽出中に届いた要求は `TooManyRequests` で拒否されます。このときエラーメッセージには枠を占有している解析の `AnalysisId` が含まれるため、当てずっぽうに再試行するのではなく `GetTraceAnalysisStatus` でその解析を監視できます。実行中の解析をキャンセルする手段はありません。完了した解析は枠を占有しません（保持時間の間は読み取り可能なまま残りますが、次の解析の開始を妨げません）。

また、解析は開始したセッションに属します。`GetTraceAnalysisStatus` と `GetTraceAnalysisResult` が `AnalysisId` を見つけられるのは、`AnalyzeTrace` を呼んだときと同じ `SessionId` で呼び出した場合だけです。それ以外のセッションから見た同じ識別子は `NotFound` になります。これは存在しない識別子に対する応答と意図的に同一です。未知の `AnalysisId`・保持時間が切れた `AnalysisId`・他セッションが所有する `AnalysisId` は区別されないため、この 2 コマンドで他の呼び出し元の識別子の存在を確かめることはできません。ひとつの `SessionId` を使い続けている限り、呼び出し方は従来どおりで構いません。ただし `SessionId` を省略すると、トランスポートが呼び出しごとに別々の匿名セッションを作るため、そうして開始した解析は二度と照会できなくなります。これはアセット監査ジョブのコマンドと同じ性質の要求です。

| コマンド | 説明 |
|---|---|
| `AnalyzeTrace` | トレースファイルの解析を開始し `AnalysisId` を返します。**開始した解析はこの呼び出しの `SessionId` に紐づき**、以後の照会・取得も同じ `SessionId` からのみ行えます。`FileName` は `ListTraceFiles` が報告した名前（パスではない）である必要があります。UAIP 以外が採取したトレースは `ExternalTracePath` を渡して解析しますが、これには外部解析のポリシー設定が必要です。省略可のパラメータは `Sections`・`StartTimeSeconds` / `EndTimeSeconds`・`TopN`（既定 32）・`MaxSeries`（既定 256）・`MaxSamplesPerSeries`（既定 1024）・`NameFilter`・`HitchThresholdMs`（既定 33.3）。512 MB を超えるトレースは拒否します。要求された各セクションは完了した順に個別の JSON artifact として書き出されるため、本コマンドは read-only ではありません。チャネルが記録されていないセクションや SafetyPolicy が秘匿するセクションは、実行を失敗させるのではなく理由付きで unavailable として報告されます |
| `GetTraceAnalysisStatus` | 解析の進行状況を報告します — `Running`（パース中）・`Extracting`（セクション抽出中）・`Completed`・`Failed` と経過時間、`CompletedSections`・`AvailableSections`・`UnavailableSections`（それぞれ理由付き）。`FailureReason` は固定の値集合から選ばれ、`State` が `Failed` のときのみ意味を持ちます。解析エンジン自身が報告したメッセージは絶対パスを含みうるため返さず、出力ログにのみ記録します。**開始時と同じ `SessionId` が必須** — 未知・保持時間切れ・他セッションの `AnalysisId` はいずれも区別されず `NotFound` になります。read-only |
| `GetTraceAnalysisResult` | 完了した解析が生成した artifact をセクションごとに返します（セクションごとの `TotalCount` / `ReturnedCount`、いずれかが上限に達した場合の `Truncated` を含む）。読めるのは `State` が `Completed` の解析のみで、**開始時と同じ `SessionId` からのみ**読めます（それ以外のセッションからは未知の識別子と同じく `NotFound`）。本コマンドは参照を返すだけで何も読まないため、必要なセクションだけを取得できます。元の `AnalyzeTrace` が要求しなかったセクションは、ここで解析し直すのではなく拒否されます。結果を読むたびに保持時間が延長されます（1 回の読み取りにつき 15 分、絶対上限 1 時間） |

`Sections` が受け付けるセクション名: `Frames`・`Counters`・`Timers`・`Threads`・`StackSamples`・`LoadTime`・`Memory`・`Allocations`・`Tasks`・`FileActivity`・`NetProfiler`・`CsvProfiler`・`ContextSwitches`・`CookProfiler`・`Bookmarks`・`Regions`・`Diagnostics`・`Channels`・`Log`・`Screenshots`、および `Objects`（UE 5.8 以降のみ。UE 5.7 には対応する Provider が存在しません）。

結果を読む前に知っておくとよいセクション個別の挙動が 3 点あります。

- **`Frames`** は開始と終了の両方が揃ったフレームだけを数えます。採取はフレームの途中で止まるため、各フレーム種別の最後のフレームはほぼ常に開いたままで報告できる長さを持ちません。そうしたフレームは統計からも `TotalCount` からも同様に除外されます。したがって `TotalCount` と `ReturnedCount` が食い違うのは時間範囲を指定したときだけで、本セクションが切り詰めを行うことはありません。
- **`Screenshots`** はメタデータのみを報告します（各スクリーンショットの識別子・名前・時刻・幅・高さと `ImageDataIncluded: false`）。エンコード済みの画像バイト列は返しません。画像が後から届くことはないため、メタデータ以外に待つものはありません。
- **`Diagnostics`** は UE 5.7 では `EngineVersion` キー自体を出力しません。UE 5.7 のトレース形式はエンジンバージョンを一切運んでいないため、空文字列（本当に記録がなかった採取と区別できない）ではなくキーの省略で表現しています。

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

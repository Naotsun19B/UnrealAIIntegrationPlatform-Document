**[English](../en/demo.md)** | [概要に戻る](overview.md)

# デモ版ガイド

UAIP のデモ版は GitHub Releases で無償配布している、機能を絞ったバイナリです。観測・PIE 制御・アサーション・シナリオ実行・UI 自動化のコマンドを利用できるので、AI エージェントをレビューやテストのワークフローに組み込むには十分な機能がそろっています。

> **ライセンス**：デモ版は **個人利用・評価目的のみ** での利用を許諾しています。商用利用は対象外で、リリースアーカイブ同梱の `EULA.txt` に従ってください。商用利用の場合は、製品版（[Fab で公開中](https://www.fab.com/listings/0eedf909-00ac-4d95-b109-8fda51800fff)）をご利用ください。

---

## デモ版と製品版の比較

| | デモ版 | 製品版（Fab） |
|---|:---:|:---:|
| **接続方式** | | |
| MCP | ✅ | ✅ |
| HTTP API（`/uaip/execute`） | — | ✅ |
| WebSocket | — | ✅ |
| CLI | — | ✅ |
| Artifact 取得（`/uaip/artifacts/*`） | ✅ | ✅ |
| **コマンド** | | |
| Core（HealthCheck、ListCommands など） | ✅ | ✅ |
| Editor 観測（スクリーンショット・ダンプ） | ✅ | ✅ |
| PIE 制御（StartPIE、StopPIE、LoadMap など） | ✅ | ✅ |
| Runtime 観測（ビューポートキャプチャ・ワールドダンプ） | ✅ | ✅ |
| シナリオ実行（`uaip_run_scenario`） | ✅ | ✅ |
| UI 自動化（ClickWidget、PressKey、FillForm など） | ✅ | ✅ |
| Runtime アサーション（WaitSeconds、AssertActorProperty など） | ✅ | ✅ |
| Editor 編集（Blueprint、Level、Assets、Material など） | — | ✅ |
| Runtime ワールド編集（SpawnActor、GAS、Input inject など） | — | ✅ |
| Python スクリプト実行（`RunEditorPythonScript`） | — | ✅ |
| Canonical グラフキャプチャ（外部キャプチャプロバイダ連携） | — | ✅ |
| **その他** | | |
| キャプチャ画像への透かし | ✅ | — |
| ユーザー拡張ポイント（`ICommandProvider`） | ✅ | ✅ |
| オプション依存プラグイン（Toolset、GAS、Niagara など） | — | ✅ |
| 対応 UE バージョン | 5.7 / 5.8 | 5.7 / 5.8 |

---

## インストール

1. [Releases](../../../releases) ページから `UAIP-Demo-UE<version>-Win64.zip` をダウンロード
2. zip を UE プロジェクトの `Plugins/UnrealAIIntegrationPlatform/` として展開
3. zip 内の `Config/DefaultUAIP.ini` をプロジェクトの `Config/` フォルダにコピー（`PIEControl` / `SlateUIAutomation` / `ObservationCapture` Capability が有効化済みの設定）
4. AI クライアントに MCP サーバーを登録（[接続方法 → MCP Bridge](connections.md#mcp-bridge) を参照）

### 製品版への移行

`Config/DefaultUAIP.ini` の設定形式はデモ版と製品版で共通です。デモ版でコピーした `DefaultUAIP.ini` はそのまま引き継げるため、ini の差し替えは不要です。プラグインフォルダの構造も MCP サーバの登録方法も同じなので、他に変更は必要ありません。

---

## 有効なコマンド一覧

### `UAIP.Core.*`

| コマンド | 説明 |
|---|---|
| `UAIP.Core.HealthCheck` | 接続状態と UAIP バージョンを返す |
| `UAIP.Core.GetSystemInfo` | プロジェクト名・プラットフォーム・エンジン版・ビルド設定を返す |
| `UAIP.Core.ListCommands` | 登録済みコマンド一覧を返す（ProviderPrefix・キーワードフィルター対応） |
| `UAIP.Core.DescribeCommand` | コマンドの詳細（説明・パラメータスキーマ・必要 Capability）を返す |
| `UAIP.Core.QueryCapabilities` | 現在のセッションの Capability セットを返す |
| `UAIP.Core.ListPlugins` | UE プラグイン情報（名前・バージョン・有効化状態）を返す |
| `UAIP.Core.EndSession` | セッション終了・ウィジェット参照解放・Artifact GC |
| `UAIP.Core.ReloadCapabilities` | `DefaultUAIP.ini` から Capability を再読み込み（`AllowCapabilityReload=True` が必要） |

### `UAIP.Editor.Observation.*`

| コマンド | 説明 | 備考 |
|---|---|---|
| `UAIP.Editor.Observation.CaptureActiveWindowImage` | アクティブウィンドウのスクリーンショット | 透かしあり |
| `UAIP.Editor.Observation.CaptureEditorTabImage` | 指定エディタータブのスクリーンショット | 透かしあり |
| `UAIP.Editor.Observation.CaptureGraphViewportImage` | グラフビューポート（Blueprint 等）のスクリーンショット | 透かしあり |
| `UAIP.Editor.Observation.DumpEditorState` | エディター状態（開いているアセット・アクティブタブ等）を JSON で返す | |
| `UAIP.Editor.Observation.DumpSelectionState` | 現在の選択状態を JSON で返す | |
| `UAIP.Editor.Observation.DumpOpenTabs` | 開いているタブ一覧を JSON で返す | |
| `UAIP.Editor.Observation.DumpOutputLog` | 出力ログを取得する | |
| `UAIP.Editor.Observation.DumpMessageLog` | メッセージログを取得する | |
| `UAIP.Editor.Observation.DumpSlateTree` | Slate ウィジェット階層を JSON で返す | |
| `UAIP.Editor.Observation.InspectMenu` | メニュー構造情報を返す | |
| `UAIP.Editor.Observation.InspectContextMenu` | コンテキストメニュー情報を返す | |
| `UAIP.Editor.Observation.ObserveWidget` | ウィジェットを監視登録（キャッシュ）する | |
| `UAIP.Editor.Observation.ListGraphNodes` | グラフのノード一覧を返す | |

### `UAIP.Runtime.PIE.*`

| コマンド | 説明 |
|---|---|
| `UAIP.Runtime.PIE.StartPIE` | Play in Editor（PIE）を起動する |
| `UAIP.Runtime.PIE.StopPIE` | PIE を停止する |
| `UAIP.Runtime.PIE.PausePIE` | PIE を一時停止する |
| `UAIP.Runtime.PIE.ResumePIE` | PIE を再開する |
| `UAIP.Runtime.PIE.LoadMap` | マップを読み込む |

### `UAIP.Runtime.Observation.*`

| コマンド | 説明 | 備考 |
|---|---|---|
| `UAIP.Runtime.Observation.CaptureViewportImage` | ゲームビューポートのスクリーンショット | 透かしあり |
| `UAIP.Runtime.Observation.DumpWorldState` | ワールド状態（全アクター・コンポーネント・トランスフォーム）を JSON で返す | |
| `UAIP.Runtime.Observation.DumpActorState` | 指定アクターの状態を JSON で返す | |
| `UAIP.Runtime.Observation.DumpComponentState` | 指定コンポーネントの状態を JSON で返す | |
| `UAIP.Runtime.Observation.DumpRuntimeLog` | ランタイムログを取得する | |
| `UAIP.Runtime.Observation.CapturePerformanceSnapshot` | FPS・メモリ等のパフォーマンス統計を取得する | |
| `UAIP.Runtime.Observation.CheckpointCapture` | スクリーンショット＋状態ダンプの複合観測（シナリオ primitive） | |
| `UAIP.Runtime.Observation.SearchLoadedClasses` | ロード済みクラスを検索する | |

### `UAIP.Runtime.Assertion.*`

| コマンド | 説明 |
|---|---|
| `UAIP.Runtime.Assertion.WaitSeconds` | 指定秒数待機する（シナリオ primitive） |
| `UAIP.Runtime.Assertion.WaitForCondition` | 条件評価ループで待機する（シナリオ primitive） |
| `UAIP.Runtime.Assertion.AssertActorProperty` | アクタープロパティをアサートする（失敗時も Artifact を出力） |
| `UAIP.Runtime.Assertion.AssertWorldState` | 複数プロパティをバッチアサートする |

### `UAIP.Editor.UIAutomation.*`

| コマンド | 説明 |
|---|---|
| `UAIP.Editor.UIAutomation.SnapshotUI` | UI 構造スナップショットを取得する |
| `UAIP.Editor.UIAutomation.ClickWidget` | ウィジェットをクリックする |
| `UAIP.Editor.UIAutomation.SelectMenuItem` | メニューアイテムを選択する |
| `UAIP.Editor.UIAutomation.InputText` | テキストを入力する |
| `UAIP.Editor.UIAutomation.SetCheckboxState` | チェックボックスの状態を設定する |
| `UAIP.Editor.UIAutomation.SetComboSelection` | コンボボックスを選択する |
| `UAIP.Editor.UIAutomation.DragGraphNode` | グラフノードをドラッグする |
| `UAIP.Editor.UIAutomation.ConnectGraphPins` | グラフピンを接続する |
| `UAIP.Editor.UIAutomation.AcceptDialog` | ダイアログを OK で閉じる |
| `UAIP.Editor.UIAutomation.CancelDialog` | ダイアログをキャンセルで閉じる |
| `UAIP.Editor.UIAutomation.InvokeContextMenuAction` | コンテキストメニューアクションを呼び出す |
| `UAIP.Editor.UIAutomation.HoverWidget` | ウィジェットをホバーする |
| `UAIP.Editor.UIAutomation.PressKey` | キー入力を送る |
| `UAIP.Editor.UIAutomation.WaitForWidget` | ウィジェットの出現を待機する |
| `UAIP.Editor.UIAutomation.FillForm` | フォームを自動入力する |

---

## 制限事項

### 接続方式

デモ版は **MCP 専用モード** で動作します。`-uaip-http-enable` を指定しても HTTP API ルート（`/uaip/execute` 等）は登録されません（警告ログが出て無視されます）。有効なエンドポイントは `/mcp` と `/uaip/artifacts/*` のみです。

### キャプチャ画像への透かし

以下のキャプチャコマンドが出力する PNG には **「UAIP Demo」** の透かしが入ります：

- `CaptureActiveWindowImage`
- `CaptureEditorTabImage`
- `CaptureGraphViewportImage`
- `CaptureViewportImage`

<p align="center">
  <img src="../../images/demo-watermark-full.png" alt="デモ版キャプチャ画像（右下に透かし）" width="80%">
</p>

<p align="center">
  <img src="../../images/demo-watermark-zoom.png" alt="透かしのクローズアップ" width="40%">
</p>

レビューやテストの証跡として共有された画像が、デモ版で取得されたものだと分かるようにするための表示です。製品版では入りません。

### 除外コマンド

製品版には存在するが、デモ版では `CommandNotFound` を返すコマンド：

| コマンド | 理由 |
|---|---|
| `UAIP.Editor.Execution.RunEditorPythonScript` | Python 実行は製品版のみ |
| ホワイトリスト外モジュールが提供する全コマンド | Editor 編集・Runtime ワールド編集・GAS・Niagara・Input inject など |

### ロード対象

デモ版はエディタ専用のバイナリです。パッケージビルドやランタイム（スタンドアロン・配布ビルド）には載りません。ランタイム側に UAIP を組み込みたい場合（Gauntlet テストや配布後の観測など）は、製品版を利用してください。

---

## シナリオ実行

シナリオ実行（`uaip_run_scenario`）はデモ版でも利用できます。`config.json` で有効化してください：

```json
{
  "editor_path":    "...",
  "uproject_path":  "...",
  "enable_scenario": true
}
```

詳細は [シナリオ実行](scenario.md) を参照してください。

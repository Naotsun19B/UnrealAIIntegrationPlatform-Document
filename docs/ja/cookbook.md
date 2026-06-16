**[English](../en/cookbook.md)** | [概要に戻る](overview.md)

# Examples / Cookbook

UAIP のよくあるワークフローを実例レシピとしてまとめたものです。各レシピは独立しており、使用するコマンドと必要 Capability、AI クライアントへの依頼例を含みます。

> ほとんどのレシピは **シナリオ** を使用しており、複数ステップを 1 リクエストにまとめて、失敗時の中断・成果物の一括返却が可能です。シナリオが初めての方は [シナリオ実行](scenario.md) を参照してください。

---

## 目次

| レシピ | ユースケース | デモ可 |
|---|---|:---:|
| [1. PIE スモークテスト](#1-pie-スモークテスト) | 「このマップは少なくともクラッシュせず起動するか？」 | ✅ |
| [2. AI コード / Blueprint レビュー](#2-ai-コード--blueprint-レビュー) | AI に Blueprint を視覚的・構造的に評価させる | ✅ |
| [3. アセット監査・命名チェック](#3-アセット監査命名チェック) | フォルダ単位で命名規則・クラスの違反を検出 | ✅ |
| [4. Blueprint 編集→検証ループ](#4-blueprint-編集検証ループ) | ノードを追加してコンパイル→エラー修正 | — |
| [5. UI 自動化テスト](#5-ui-自動化テスト) | エディタメニュー・ボタンを End-to-End で操作 | ✅ |
| [6. PIE プレイテスト + キャプチャ](#6-pie-プレイテスト--キャプチャ) | 実行・チェックポイントでスクショ・状態アサート | ✅ |
| [7. CI から Automation Test を実行](#7-ci-から-automation-test-を実行pro) | ヘッドレステスト実行（Pro 限定） | — |

デモ可 = デモバイナリで動作する。それ以外は Pro 版が必要。

---

## 1. PIE スモークテスト

**AI に依頼**: 「`/Game/Maps/MainMenu` で PIE スモークテストして」

**シナリオ**:

```json
{
  "ScenarioName": "PIE_Smoke_MainMenu",
  "Steps": [
    { "StepName": "Load",   "CommandName": "UAIP.Runtime.PIE.LoadMap",
      "Params": { "MapPath": "/Game/Maps/MainMenu" } },
    { "StepName": "Start",  "CommandName": "UAIP.Runtime.PIE.StartPIE" },
    { "StepName": "Settle", "CommandName": "UAIP.Runtime.Assertion.WaitSeconds",
      "Params": { "Seconds": 3 } },
    { "StepName": "Shot",   "CommandName": "UAIP.Runtime.Observation.CheckpointCapture",
      "Params": { "Label": "after-load" } },
    { "StepName": "Stop",   "CommandName": "UAIP.Runtime.PIE.StopPIE",
      "AbortOnFailure": false }
  ]
}
```

**得られるもの**: スクリーンショット + JSON ダンプをまとめたチェックポイント artifact。実行後に `Read` で確認できます。途中で失敗してもクリーンアップステップ（`AbortOnFailure: false`）の `Stop` は実行されるため、PIE が起動しっぱなしになりません。

**必要 Capability**: `PIEControl`、`RuntimeCapture` — どちらも DefaultAllow。

---

## 2. AI コード / Blueprint レビュー

**ゴール**: AI に Blueprint のロジックフローと視覚状態を評価してもらう。

**単発呼び出しの流れ**:

1. アセットを開く:
   `uaip_execute(CommandName="UAIP.Editor.Assets.OpenAsset", Params={"AssetPath": "/Game/Blueprints/BP_PlayerCharacter"})`
2. スクリーンショットを再現性のあるレイアウトに整える:
   `uaip_execute(CommandName="UAIP.Editor.Workspace.NormalizeEditorLayout")`
3. グラフをキャプチャ:
   `uaip_execute(CommandName="UAIP.Editor.Observation.CaptureGraphViewportImage", Params={"TabId": "/Game/Blueprints/BP_PlayerCharacter"})`
4. グラフ構造をダンプ:
   `uaip_execute(CommandName="UAIP.Editor.Blueprint.ListBlueprintPins", Params={...})`

そして AI に「この Blueprint をレビューして — 未接続の実行ピン、Cast ノードの null チェック漏れ、孤立したイベントノードを探して」と依頼。

**デモ版の注意**: キャプチャコマンドが出力する PNG には `UAIP Demo` 透かしが入りますが、レイアウト評価には影響しません。

**必要 Capability**: `EditorObservation`、`EditorInspect` — DefaultAllow。

---

## 3. アセット監査・命名チェック

**ゴール**: フォルダ配下の `BP_*` Blueprint を列挙し、命名規則に合致するか確認。

**単発呼び出し**:

```
uaip_execute(
  CommandName="UAIP.Editor.Assets.SearchAssets",
  Params={
    "Path": "/Game/Characters",
    "ClassNames": ["Blueprint"],
    "Recursive": true
  }
)
```

返却される JSON artifact に該当アセットがすべて含まれます。AI に渡して「`BP_` で始まらない、`_Character` で終わらない、または PascalCase でないパス要素がある Blueprint を列挙して」と依頼。

依存関係系の監査（未参照アセット・循環参照・サイズマップ）は [ロードマップ → アセット参照解析・SizeMap](roadmap.md#アセット参照解析sizemap) を参照（計画中・未実装）。

**必要 Capability**: `EditorInspect` — DefaultAllow。

---

## 4. Blueprint 編集→検証ループ

**ゴール**: Blueprint にメンバー変数を追加・ノードグラフを配線・保存・検証する。

**シナリオ**:

```json
{
  "ScenarioName": "BP_AddHealth",
  "Steps": [
    { "StepName": "AddVar", "CommandName": "UAIP.Editor.Blueprint.AddBlueprintVariable",
      "Params": {
        "BlueprintPath": "/Game/Blueprints/BP_PlayerCharacter",
        "VariableName":  "Health",
        "PinCategory":   "real",
        "PinSubCategory":"double",
        "DefaultValue":  "100.0"
      } },
    { "StepName": "AddGet", "CommandName": "UAIP.Editor.Blueprint.AddGraphNode",
      "Params": {
        "BlueprintPath": "/Game/Blueprints/BP_PlayerCharacter",
        "NodeKind":      "VariableGet",
        "VariableName":  "Health",
        "NodeX": 0, "NodeY": 200
      } },
    { "StepName": "Inspect", "CommandName": "UAIP.Editor.Blueprint.ListBlueprintPins",
      "Params": {
        "BlueprintPath": "/Game/Blueprints/BP_PlayerCharacter",
        "NodeId":        "${AddGet.Data.NodeId}"
      } },
    { "StepName": "Save",   "CommandName": "UAIP.Editor.Workspace.SaveAllPackages" }
  ]
}
```

保存後、AI に `CaptureGraphViewportImage` で Blueprint グラフを視覚的に検査し、配線が意図通りか確認してもらう。構造化されたエラー取得付きの専用 `CompileBlueprint` コマンドは計画中 — [ロードマップ → Blueprint Compile / コンパイルエラー取得](roadmap.md#blueprint-compile--コンパイルエラー取得) を参照。

**必要 Capability**: `BlueprintEdit`、`BlueprintVariableEdit`、`BlueprintGraphEdit` — すべて **DefaultDenied**。`Config/DefaultUAIP.ini` に以下を追加：

```ini
[UAIP.SafetyPolicy]
+AllowedCapabilities=BlueprintEdit
+AllowedCapabilities=BlueprintVariableEdit
+AllowedCapabilities=BlueprintGraphEdit
```

Pro 版限定 — Blueprint 編集モジュールはデモ版に含まれません。

---

## 5. UI 自動化テスト

**ゴール**: メニューから Project Settings ダイアログを開き、指定タブが表示されることを確認。

```json
{
  "ScenarioName": "OpenProjectSettings",
  "Steps": [
    { "StepName": "Menu",  "CommandName": "UAIP.Editor.UIAutomation.SelectMenuItem",
      "Params": { "MenuPath": "Edit/Project Settings" } },
    { "StepName": "Wait",  "CommandName": "UAIP.Editor.UIAutomation.WaitForWidget",
      "Params": { "WidgetPath": "Window:Project Settings", "TimeoutSeconds": 10 } },
    { "StepName": "Shot",  "CommandName": "UAIP.Editor.Observation.CaptureActiveWindowImage" }
  ]
}
```

AI はスクショを `Read` してダイアログが本当に表示されたか検証できます。インタラクティブなフローは `ClickWidget`・`InputText`・`SetComboSelection`・`AcceptDialog` を組み合わせて構築。

**必要 Capability**: `EditorUIAutomation` — DefaultAllow。一部のサブ機能は明示 opt-in が必要：`PressKey` 用の `EditorKeyboardInput`、`InvokeContextMenuAction` 用の `AllowContextMenuMutation`。詳細は [Safety & Capabilities](safety.md)。

---

## 6. PIE プレイテスト + キャプチャ

**ゴール**: レベルロード・PIE 開始・一定時間間隔でスクショ取得・プロパティアサート。

```json
{
  "ScenarioName": "PlaytestCharacterMove",
  "Variables": { "ExpectedHealth": 100 },
  "Steps": [
    { "StepName": "Load",  "CommandName": "UAIP.Runtime.PIE.LoadMap",
      "Params": { "MapPath": "/Game/Maps/TestArena" } },
    { "StepName": "Play",  "CommandName": "UAIP.Runtime.PIE.StartPIE" },
    { "StepName": "T0",    "CommandName": "UAIP.Runtime.Observation.CheckpointCapture",
      "Params": { "Label": "t0" } },
    { "StepName": "Wait1", "CommandName": "UAIP.Runtime.Assertion.WaitSeconds",
      "Params": { "Seconds": 5 } },
    { "StepName": "T5",    "CommandName": "UAIP.Runtime.Observation.CheckpointCapture",
      "Params": { "Label": "t5" } },
    { "StepName": "Check", "CommandName": "UAIP.Runtime.Assertion.AssertActorProperty",
      "Params": {
        "ActorIdentifier": "PlayerCharacter",
        "PropertyName":    "Health",
        "ExpectedValue":   "${Variables.ExpectedHealth}"
      } },
    { "StepName": "Stop",  "CommandName": "UAIP.Runtime.PIE.StopPIE", "AbortOnFailure": false }
  ]
}
```

2 つの CheckpointCapture artifact を比較すれば、AI が「2 時点での位置・ライティング・状態の差分」を記述できます。

**必要 Capability**: `PIEControl`、`RuntimeCapture`、`RuntimeInspect` — DefaultAllow。

---

## 7. CI から Automation Test を実行（Pro）

UAIP は **CLI トランスポート**（Pro 限定）経由で CI / CD パイプラインから呼び出せます。エディタは 1 リクエスト処理して終了するため、ヘッドレステスト実行に適しています。

### 例（Windows GitHub Actions ランナーでの PowerShell）

```powershell
# 1. リクエストを JSON で書き出し
@'
{
  "CommandName": "UAIP.Editor.Execution.RunAutomationTest",
  "Params": {
    "TestName": "MyGame.Smoke.MainMenu",
    "RunAllMatching": false
  }
}
'@ | Set-Content cmd.json

# 2. CLI トランスポートでエディタ実行
& "C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe" `
    "$pwd/MyGame.uproject" `
    "-uaip-request-file=$pwd/cmd.json" `
    "-uaip-response-file=$pwd/result.json"

# 3. 結果 JSON を検査、Success でなければ CI を失敗にする
$r = Get-Content result.json | ConvertFrom-Json
if (-not $r.Success) { exit 1 }
```

同じパターンが `RunAutomationSpec`・`RunFunctionalTest`・`RunGauntletTest` でも使えます。

### 注意点

- **エディタ起動は遅い**（CI 環境では 30〜90 秒程度）。それを見越したタイムアウト設計を。
- **デモ版は CLI 非対応** — デモ版バイナリは MCP 専用。CI には Pro 版が必要。
- **ヘッドレス / `-nullrhi` ではキャプチャコマンドが無効**。CI でスクショが必要な場合は実 GPU ランナーを使うこと。
- より充実した CI 連携は [ロードマップ → Build / Package パイプライン](roadmap.md#build--package-パイプライン) で計画中（未実装）。

---

## 押さえておくと便利なパターン

- **シナリオテンプレート**（`${StepName.Data.x}`・`${Variables.y}`）で、後ステップが前ステップの出力を消費可能。詳細は [シナリオ実行 → テンプレート](scenario.md#4-テンプレートで前ステップの結果を後ステップに差し込む)。
- **`AbortOnFailure: true` がデフォルト**で、最初の失敗ステップで中断します。クリーンアップ系ステップは `false` に上書きして、PIE / アセット操作が途中失敗しても実行されるようにしましょう。
- **キャプチャコマンドはファイルパスではなく artifact ID を返します**。PNG / JSON を見るには、レスポンスに含まれる `FilePath` を `Read` で参照してください。詳細は [Artifacts](artifacts.md)。
- **セッションで作業を分離**。`SessionId="my-test"` を渡せば artifact がタスク毎にグループ化されます（保存先: `Saved/UAIP/<session>/`）。
- **ユーザーに聞く前に自己検証**。「これうまくいったかな？」と思ったら、Capture / Dump コマンドを先に呼んでみるべきです。

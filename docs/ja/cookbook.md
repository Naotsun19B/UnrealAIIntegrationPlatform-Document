**[English](../en/cookbook.md)** | [概要に戻る](overview.md)

# Examples / Cookbook

UAIP でよく出てくるワークフローを、すぐに動かせるレシピとしてまとめました。各レシピは独立しており、使用コマンド・必要な Capability・AI クライアントへの依頼例をひととおり含んでいます。

> ほとんどのレシピは **シナリオ** を使います。複数ステップを 1 リクエストにまとめると、失敗時の中断や成果物の一括返却がそのまま使えるためです。シナリオが初めての方は [シナリオ実行](scenario.md) を一読してください。

---

## 目次

| レシピ | やりたいこと | デモ可 |
|---|---|:---:|
| [1. PIE スモークテスト](#1-pie-スモークテスト) | このマップが少なくともクラッシュせずに起動するかを確認したい | ✅ |
| [2. AI コード / Blueprint レビュー](#2-ai-コード--blueprint-レビュー) | AI に Blueprint を視覚と構造の両面で評価させたい | ✅ |
| [3. アセット監査と命名チェック](#3-アセット監査命名チェック) | フォルダ単位で命名規則やクラスの違反を洗い出したい | ✅ |
| [4. Blueprint 編集と検証のループ](#4-blueprint-編集検証ループ) | ノードを追加し、コンパイルし、エラーを直す流れを回したい | — |
| [5. UI 自動化テスト](#5-ui-自動化テスト) | エディタのメニューやボタンを End-to-End で動かしたい | ✅ |
| [6. PIE プレイテスト + キャプチャ](#6-pie-プレイテスト--キャプチャ) | 実行中にチェックポイントでスクショと状態アサートを残したい | ✅ |
| [7. CI から Automation Test を実行](#7-ci-から-automation-test-を実行pro) | ヘッドレスでテストを回したい（製品版限定） | — |

「デモ可」列はデモバイナリでも動作するレシピを示しています。それ以外は製品版が必要です。

---

## 1. PIE スモークテスト

**AI への依頼例**：「`/Game/Maps/MainMenu` で PIE スモークテストして」

**シナリオ**：

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

**得られる結果**：スクリーンショットと JSON ダンプをまとめたチェックポイント Artifact が返却され、実行後に `Read` で確認できます。途中で失敗してもクリーンアップ用ステップ（`AbortOnFailure: false` を指定した `Stop`）は実行されるため、PIE が起動したまま残ることはありません。

**必要な Capability**：`PIEControl` と `RuntimeCapture`。どちらも DefaultAllow です。

---

## 2. AI コード / Blueprint レビュー

**目的**：AI に Blueprint のロジックフローと見た目の状態を評価してもらう。

**一連の呼び出し**：

1. アセットを開く：
   `uaip_execute(CommandName="UAIP.Editor.Assets.OpenAsset", Params={"AssetPath": "/Game/Blueprints/BP_PlayerCharacter"})`
2. スクリーンショットの再現性を担保するためレイアウトを整える：
   `uaip_execute(CommandName="UAIP.Editor.Workspace.NormalizeEditorLayout")`
3. グラフをキャプチャする：
   `uaip_execute(CommandName="UAIP.Editor.Observation.CaptureGraphViewportImage", Params={"TabId": "/Game/Blueprints/BP_PlayerCharacter"})`
4. グラフ構造をダンプする：
   `uaip_execute(CommandName="UAIP.Editor.Blueprint.ListBlueprintPins", Params={...})`

ここまでお膳立てしたうえで、AI に「この Blueprint をレビューして — 未接続の実行ピン、Cast ノードでの null チェック漏れ、孤立したイベントノードを探して」と依頼します。

**デモ版利用時の注意**：キャプチャコマンドが出力する PNG には `UAIP Demo` の透かしが入りますが、レイアウト評価には支障ありません。

**必要な Capability**：`EditorObservation` と `EditorInspect`（いずれも DefaultAllow）。

---

## 3. アセット監査と命名チェック

**目的**：フォルダ配下の `BP_*` Blueprint を列挙し、命名規則に合致しているかを確認する。

**呼び出し例**：

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

返却される JSON Artifact に該当アセットがすべて含まれます。これを AI に渡して「`BP_` で始まらない、`_Character` で終わらない、または PascalCase でないパス要素を含む Blueprint を列挙して」と依頼します。

依存関係まで踏み込んだ監査（未参照アセット検出・循環参照検出・サイズマップ生成）は計画中で未実装です。[ロードマップ → アセット参照解析・SizeMap](roadmap.md#アセット参照解析sizemap) を参照してください。

**必要な Capability**：`EditorInspect`（DefaultAllow）。

---

## 4. Blueprint 編集と検証のループ

**目的**：Blueprint にメンバー変数を追加し、ノードグラフを配線し、保存して検証する。

**シナリオ**：

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

保存が完了したら、続けて AI に `CaptureGraphViewportImage` で Blueprint グラフを取得させ、配線が意図どおりになっているかを目視で確認してもらいます。構造化されたエラー取得つきの専用 `CompileBlueprint` コマンドは計画段階です。詳細は [ロードマップ → Blueprint Compile / コンパイルエラー取得](roadmap.md#blueprint-compile--コンパイルエラー取得) を参照してください。

**必要な Capability**：`BlueprintEdit`・`BlueprintVariableEdit`・`BlueprintGraphEdit`（いずれも **DefaultDenied**）。`Config/DefaultUAIP.ini` に以下を追加してください：

```ini
[UAIP.SafetyPolicy]
+AllowedCapabilities=BlueprintEdit
+AllowedCapabilities=BlueprintVariableEdit
+AllowedCapabilities=BlueprintGraphEdit
```

**製品版限定**：Blueprint 編集モジュールはデモ版には含まれません。

---

## 5. UI 自動化テスト

**目的**：メニューから Project Settings ダイアログを開き、指定のタブが表示されることを確認する。

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

AI はスクリーンショットを `Read` することで、ダイアログが実際に表示されたかを自分で確認できます。対話的なフローを組む場合は `ClickWidget`・`InputText`・`SetComboSelection`・`AcceptDialog` を組み合わせてください。

**必要な Capability**：`EditorUIAutomation`（DefaultAllow）が基本です。サブ機能のなかには明示的な opt-in が必要なものがあります — `PressKey` には `EditorKeyboardInput`、`InvokeContextMenuAction` には `AllowContextMenuMutation` を有効化してください。詳細は [Safety & Capabilities](safety.md) を参照してください。

---

## 6. PIE プレイテスト + キャプチャ

**目的**：レベルをロードして PIE を開始し、一定間隔でスクリーンショットを残しつつプロパティをアサートする。

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

2 つの CheckpointCapture の Artifact を見比べれば、AI が「2 時点での位置・ライティング・状態の差分」を文章で説明できます。

**必要な Capability**：`PIEControl`・`RuntimeCapture`・`RuntimeInspect`（いずれも DefaultAllow）。

---

## 7. CI から Automation Test を実行（製品版）

UAIP は **CLI トランスポート**（製品版限定）経由で CI / CD パイプラインから呼び出せます。エディタは 1 リクエストを処理してそのまま終了するため、ヘッドレスなテスト実行に適しています。

### 例：Windows の GitHub Actions ランナーから PowerShell で

```powershell
# 1. リクエストを JSON ファイルとして書き出す
@'
{
  "CommandName": "UAIP.Editor.Execution.RunAutomationTest",
  "Params": {
    "TestName": "MyGame.Smoke.MainMenu",
    "RunAllMatching": false
  }
}
'@ | Set-Content cmd.json

# 2. CLI トランスポートでエディタを起動して実行する
& "C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe" `
    "$pwd/MyGame.uproject" `
    "-uaip-request-file=$pwd/cmd.json" `
    "-uaip-response-file=$pwd/result.json"

# 3. 結果の JSON を確認し、Success でなければ CI を失敗扱いにする
$r = Get-Content result.json | ConvertFrom-Json
if (-not $r.Success) { exit 1 }
```

同じ要領で `RunAutomationSpec`・`RunFunctionalTest`・`RunGauntletTest` も実行できます。

### 注意点

- **エディタの起動はやはり遅い**：CI 環境では 30〜90 秒程度かかります。タイムアウト設計はその前提で組んでください。
- **デモ版は CLI 非対応**：デモバイナリは MCP 専用なので、CI 用途には製品版が必要です。
- **ヘッドレス / `-nullrhi` 環境ではキャプチャコマンドが動作しません**。CI でスクリーンショットを取りたい場合は、実 GPU を備えたランナーを使ってください。
- より本格的な CI 連携機能は [ロードマップ → Build / Package パイプライン](roadmap.md#build--package-パイプライン) で計画中です（未実装）。

---

## 押さえておくと便利なパターン

- **シナリオテンプレート**（`${StepName.Data.x}` や `${Variables.y}`）を使うと、後段のステップが前段ステップの出力を引き継げます。詳細は [シナリオ実行 → テンプレート](scenario.md#4-テンプレートで前ステップの結果を後ステップに差し込む) を参照してください。
- **`AbortOnFailure: true` がデフォルト**のため、最初に失敗したステップでシナリオは中断します。クリーンアップ系のステップは `false` で上書きして、途中で何かが失敗しても確実に実行されるようにしましょう。
- **キャプチャコマンドはファイルパスではなく Artifact ID を返します**。PNG や JSON を確認するには、レスポンスに含まれる `FilePath` を `Read` で開いてください。詳細は [Artifacts](artifacts.md) を参照してください。
- **セッションで作業を分離する**：`SessionId="my-test"` を渡しておけば、Artifact がタスク単位でグループ化されます（保存先は `Saved/UAIP/<session>/`）。
- **ユーザーに聞く前に自己検証する**：「これうまくいったかな」と思ったら、まず Capture や Dump 系コマンドを呼んで自分で確認しましょう。

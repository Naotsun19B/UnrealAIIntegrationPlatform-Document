**[English](../en/cookbook.md)** | [概要に戻る](overview.md)

# 使用例集 / レシピ集

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
      "Params": { "MapPath": "/Game/Maps/MainMenu" }, "AbortOnFailure": false },
    { "StepName": "Start",  "CommandName": "UAIP.Runtime.PIE.StartPIE",
      "AbortOnFailure": false },
    { "StepName": "Settle", "CommandName": "UAIP.Runtime.Assertion.WaitSeconds",
      "Params": { "Seconds": 3 }, "AbortOnFailure": false },
    { "StepName": "Shot",   "CommandName": "UAIP.Runtime.Observation.CheckpointCapture",
      "Params": { "Label": "after_load" }, "AbortOnFailure": false },
    { "StepName": "Stop",   "CommandName": "UAIP.Runtime.PIE.StopPIE" }
  ]
}
```

**得られる結果**：スクリーンショットと JSON ダンプをまとめたチェックポイント Artifact が返却され、実行後に `Read` で確認できます。

**すべてのステップに `AbortOnFailure: false` を付けている理由**：このフラグは **失敗したステップ自身** に対して評価され、後続のステップに設定した値は参照されません。`Load` 〜 `Shot` をデフォルトの `true` のままにすると、最初の失敗でシナリオが終了し `Stop` がディスパッチされず、PIE が起動したまま残ります。`Stop` に到達させるには手前のステップを `false` にする必要があります。代償としてシナリオは最初の失敗で止まらなくなるため、失敗箇所は `StepResults` から特定してください。詳細は [シナリオ実行 → 失敗時の挙動とクリーンアップ](scenario.md#失敗時の挙動とクリーンアップ) を参照してください。

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
   `uaip_execute(CommandName="UAIP.Editor.Observation.CaptureGraphViewportImage", Params={"TabId": "BP_PlayerCharacter"})`
4. グラフのノードを一覧し、成果物から目的のノードの `NodeId`（NodeGuid）を読み取る。各要素には `NodeClass`・`NodeTitle`・`Position` も入っている：
   `uaip_execute(CommandName="UAIP.Editor.Observation.ListGraphNodes", Params={"TabId": "BP_PlayerCharacter"})`
5. そのノードのピンをダンプする：
   `uaip_execute(CommandName="UAIP.Editor.Blueprint.ListBlueprintPins", Params={"BlueprintPath": "/Game/Blueprints/BP_PlayerCharacter", "NodeId": "<ListGraphNodes の成果物から読み取った NodeId>"})`

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
    "PackagePath": "/Game/Characters",
    "ClassNames": ["/Script/Engine.Blueprint"],
    "Recursive": true
  }
)
```

返却される JSON Artifact に該当アセットがすべて含まれます。これを AI に渡して「`BP_` で始まらない、`_Character` で終わらない、または PascalCase でないパス要素を含む Blueprint を列挙して」と依頼します。

依存関係まで踏み込んだ監査（未参照アセット・循環参照・壊れた参照の検出、サイズマップ生成）は [コマンドリファレンス → `UAIP.Editor.Assets`](commands.md#uaipeditorassets) の監査コマンドを参照してください。フォルダ単位の監査はジョブとして実行されます。`StartAssetAudit` が ID を即座に返し、走査はエディタのフレームの合間で進みます。進み具合は `GetAssetAuditStatus` で確認し、完了後に `GetAssetAuditResult` でレポートごとの Artifact を取得します。3 コマンドとも同じ `SessionId` を明示指定して呼びます。

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
        "VarName":       "Health",
        "VarType":       "Float",
        "DefaultValue":  "100.0"
      } },
    { "StepName": "AddGet", "CommandName": "UAIP.Editor.Blueprint.AddGraphNode",
      "Params": {
        "BlueprintPath": "/Game/Blueprints/BP_PlayerCharacter",
        "NodeType":      "VariableGet",
        "VarName":       "Health",
        "NodeX": 0, "NodeY": 200
      } },
    { "StepName": "Save",   "CommandName": "UAIP.Editor.Workspace.SaveAllPackages" }
  ]
}
```

`AddGraphNode` は新しいノードの `NodeId` を成果物にだけ書き、ステップの `Data` には書きません。そのため `${AddGet.Data.NodeId}` というテンプレートでは後続のステップへ渡せません。次の 2 段階で確認します。

1. `AddGet` ステップの成果物から、新しいノードの `NodeId` を読み取る。
2. 別の呼び出しでその値を渡す：
   `uaip_execute(CommandName="UAIP.Editor.Blueprint.ListBlueprintPins", Params={"BlueprintPath": "/Game/Blueprints/BP_PlayerCharacter", "NodeId": "<成果物から読み取った NodeId>"})`

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

**目的**：メニューから Project Settings ダイアログを開き、画面をキャプチャして AI が表示を確認できるようにし、各ウィジェットの `WidgetRef` を得る UI スナップショットを取る。

```json
{
  "ScenarioName": "OpenProjectSettings",
  "Steps": [
    { "StepName": "Menu",   "CommandName": "UAIP.Editor.UIAutomation.SelectMenuItem",
      "Params": { "MenuPath": "Edit/Project Settings..." } },
    { "StepName": "Settle", "CommandName": "UAIP.Runtime.Assertion.WaitSeconds",
      "Params": { "Seconds": 2 } },
    { "StepName": "Snap",   "CommandName": "UAIP.Editor.UIAutomation.SnapshotUI" },
    { "StepName": "Shot",   "CommandName": "UAIP.Editor.Observation.CaptureActiveWindowImage" }
  ]
}
```

AI はスクリーンショットを `Read` することで、ダイアログが実際に表示されたかを自分で確認できます。

**ウィジェットを待つ**には 2 回の別々の呼び出しが要ります。`WidgetRef` は `SnapshotUI` が発行するもので、同じシナリオの中へは差し込めないためです。ref はセッション単位で、60 秒で失効します（2 回の呼び出しには同じ `SessionId` を渡し、1 回目の直後に 2 回目を呼んでください）。

1. `SnapshotUI` を呼び、その成果物から待ちたいウィジェットの `WidgetRef` を読み取る。ウィジェットの要素の `Ref` フィールドがそれにあたります（上の `Snap` ステップがこの呼び出しです）。
2. 別の呼び出しで、その ref を `WaitForWidget` に渡す：

```json
{
  "WidgetRef":          "<SnapshotUI の Artifact から読み取った ref>",
  "ExpectedState":      "Visible",
  "WaitTimeoutSeconds": 10
}
```

ref が失効していたら、`SnapshotUI` をもう一度呼んで取り直してください。

対話的なフローを組む場合は `ClickWidget`・`InputText`・`SetComboSelection`・`AcceptDialog` を組み合わせてください。

**必要な Capability**：`EditorUIAutomation`（DefaultAllow）が基本です。サブ機能のなかには明示的な opt-in が必要なものがあります — `PressKey` には `EditorKeyboardInput`、`InvokeContextMenuAction` には `AllowContextMenuMutation` を有効化してください。詳細は [Safety & Capabilities](safety.md) を参照してください。

---

## 6. PIE プレイテスト + キャプチャ

**目的**：レベルをロードして PIE を開始し、一定間隔でスクリーンショットを残しつつプロパティをアサートする。

```json
{
  "ScenarioName": "PlaytestCharacterMove",
  "Variables": { "ExpectedHealth": "100" },
  "Steps": [
    { "StepName": "Load",  "CommandName": "UAIP.Runtime.PIE.LoadMap",
      "Params": { "MapPath": "/Game/Maps/TestArena" }, "AbortOnFailure": false },
    { "StepName": "Play",  "CommandName": "UAIP.Runtime.PIE.StartPIE",
      "AbortOnFailure": false },
    { "StepName": "T0",    "CommandName": "UAIP.Runtime.Observation.CheckpointCapture",
      "Params": { "Label": "t0" }, "AbortOnFailure": false },
    { "StepName": "Wait1", "CommandName": "UAIP.Runtime.Assertion.WaitSeconds",
      "Params": { "Seconds": 5 }, "AbortOnFailure": false },
    { "StepName": "T5",    "CommandName": "UAIP.Runtime.Observation.CheckpointCapture",
      "Params": { "Label": "t5" }, "AbortOnFailure": false },
    { "StepName": "Check", "CommandName": "UAIP.Runtime.Assertion.AssertActorProperty",
      "Params": {
        "ActorIdentifier": "PlayerCharacter",
        "PropertyName":    "Health",
        "ExpectedValue":   "${Variables.ExpectedHealth}"
      }, "AbortOnFailure": false },
    { "StepName": "Stop",  "CommandName": "UAIP.Runtime.PIE.StopPIE" }
  ]
}
```

2 つの CheckpointCapture の Artifact を見比べれば、AI が「2 時点での位置・ライティング・状態の差分」を文章で説明できます。

`Stop` より前のステップをすべて `AbortOnFailure: false` にしている理由はレシピ 1 と同じで、これを省くと最初の失敗でシナリオが終了し `Stop` が実行されません。アサーションの成否は `Check` ステップの `StepResults[].Success` で確認できます。

**必要な Capability**：`PIEControl`・`RuntimeCapture`・`RuntimeInspect`（いずれも DefaultAllow）。

---

## 7. CI から Automation Test を実行（製品版）

UAIP は **CLI トランスポート**（製品版限定）経由で CI / CD パイプラインから呼び出せます。エディタは 1 リクエストを処理してそのまま終了するため、ヘッドレスなテスト実行に適しています。

### 例：Windows の GitHub Actions ランナーから PowerShell で

プロジェクトのルートで実行します。

```powershell
# 1. リクエストを JSON ファイルとして書き出す（読み込めるのは Saved/UAIP/Requests/ の下だけ）
New-Item -ItemType Directory -Force Saved/UAIP/Requests, Saved/UAIP/Responses | Out-Null
@'
{
  "Command": "UAIP.Editor.Execution.RunAutomationTest",
  "Params": {
    "TestName": "MyGame.Smoke.MainMenu",
    "RunAllMatching": false
  }
}
'@ | Set-Content Saved/UAIP/Requests/cmd.json

# 2. CLI トランスポートでエディタを起動し、終了を待つ
Start-Process -Wait -FilePath "C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe" -ArgumentList @(
    "`"$pwd/MyGame.uproject`"",
    "-uaip-request-file=Saved/UAIP/Requests/cmd.json",
    "-uaip-response-file=Saved/UAIP/Responses/result.json"
)

# 3. 結果の JSON を確認し、Success でなければ CI を失敗扱いにする
$r = Get-Content Saved/UAIP/Responses/result.json | ConvertFrom-Json
if (-not $r.Success) { exit 1 }
```

- リクエストのコマンド名のキーは `Command` です（MCP の `uaip_execute` の引数名 `CommandName` とは違います）。
- リクエストファイルは `Saved/UAIP/Requests/`、レスポンスファイルは `Saved/UAIP/Responses/` の下に置きます。その下にあれば、相対パスでも絶対パスでも渡せます。
- `UnrealEditor.exe` は GUI アプリなので、PowerShell の `&` で呼ぶと終了を待たずに戻ります。`Start-Process -Wait` で終了を待ってから結果を読みます。

同じ要領で `RunAutomationSpec`・`RunFunctionalTest`・`RunGauntletTest` も実行できます。

### 注意点

- **エディタの起動はやはり遅い**：CI 環境では 30〜90 秒程度かかります。タイムアウト設計はその前提で組んでください。
- **デモ版は CLI 非対応**：デモバイナリは MCP 専用なので、CI 用途には製品版が必要です。
- **ヘッドレス / `-nullrhi` 環境ではキャプチャコマンドが動作しません**。CI でスクリーンショットを取りたい場合は、実 GPU を備えたランナーを使ってください。
- より本格的な CI 連携機能は [ロードマップ → Build / Package パイプライン](roadmap.md#build--package-パイプライン) で計画中です（未実装）。

---

## 押さえておくと便利なパターン

- **シナリオテンプレート**（`${StepName.Data.x}` や `${Variables.y}`）を使うと、後段のステップが前段ステップの出力を引き継げます。詳細は [シナリオ実行 → テンプレート](scenario.md#4-テンプレートで前ステップの結果を後ステップに差し込む) を参照してください。
- **`AbortOnFailure: true` がデフォルト**のため、最初に失敗したステップでシナリオは中断します。このフラグは **失敗したステップ自身** に対して評価されるため、末尾のクリーンアップ用ステップにだけ `false` を付けても意味がありません（そのステップもスキップされます）。クリーンアップ用ステップに到達させたい場合は、その前にある全ステップを `false` にするか、シナリオ完了後に別途コマンドを呼んで後始末してください。詳細は [シナリオ実行 → 失敗時の挙動とクリーンアップ](scenario.md#失敗時の挙動とクリーンアップ) を参照してください。
- **キャプチャコマンドはファイルパスではなく Artifact ID を返します**。PNG や JSON を確認するには、レスポンスに含まれる `FilePath` を `Read` で開いてください。詳細は [Artifacts](artifacts.md) を参照してください。
- **セッションで作業を分離する**：`SessionId="my-test"` を渡しておけば、Artifact がタスク単位でグループ化されます（保存先は `Saved/UAIP/<session>/`）。
- **ユーザーに聞く前に自己検証する**：「これうまくいったかな」と思ったら、まず Capture や Dump 系コマンドを呼んで自分で確認しましょう。

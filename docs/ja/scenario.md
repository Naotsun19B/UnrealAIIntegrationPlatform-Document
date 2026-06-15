**[English](../en/scenario.md)** | [概要に戻る](overview.md)

# シナリオ実行

`uaip_run_scenario` は複数のコマンドを順序付きリストとして一括送信します。各ステップはゲームスレッド上で順番に実行され、失敗時の中断・リトライ・ステップごとのタイムアウトを宣言的に設定できます。

---

## 有効化

シナリオ実行はデフォルトで無効です。`config.json` に `"enable_scenario": true` を追加して MCP クライアントを再接続すると有効になります：

```json
{
  "editor_path":    "...",
  "uproject_path":  "...",
  "enable_scenario": true
}
```

---

## 単発コマンドとシナリオの使い分け

| `uaip_execute` を使う場面 | `uaip_run_scenario` を使う場面 |
|---|---|
| 1 回で完結する操作（スクリーンショット、アセットを開く） | 順序のある手順（LoadMap → PIE → キャプチャ → アサート） |
| 読み取り専用で状態変化なし | 後のステップが前のステップの出力を必要とする |
| 探索フェーズ — 結果を見てから次を決める | 失敗時の中断・リトライ・ステップごとのタイムアウトが必要 |

**目安**：`uaip_execute` を 2 回以上続けて呼び出すときは、シナリオにまとめることを検討してください。

---

## 呼び出し形式

```
uaip_run_scenario(
  ScenarioName="MyScenario",          # [A-Za-z0-9_]{1,128}
  SessionId="scenario-<purpose>",      # 省略可
  Variables={ "Key": "Value", ... },   # 省略可（初期値マップ）
  Steps=[
    {
      "StepName":        "Load",        # [A-Za-z0-9_]{1,64}、Steps 内で一意
      "CommandName":     "UAIP.Runtime.PIE.LoadMap",
      "Params":          { "MapPath": "/Game/Maps/TestMap" },
      "AbortOnFailure":  true,          # デフォルト: true
      "RetryCount":      0,             # デフォルト: 0
      "TimeoutSeconds":  60             # デフォルト: 60
    },
    ...
  ]
)
```

---

## テンプレート `${...}` による値の受け渡し

`${StepName.Data.<path>}` を使って前のステップの出力を後のステップのパラメータに渡せます。

| 式 | 意味 |
|---|---|
| `${StepName.Success}` | bool — ステップが成功したか |
| `${StepName.ErrorCode}` | エラーコード文字列 |
| `${StepName.Data.<JsonPointer>}` | ステップのレスポンスデータ内の値 |
| `${StepName.Artifacts[0]}` | ステップの最初の Artifact ID |
| `${Variables.<key>}` | `Variables` マップの値 |

テンプレートはステップ実行直前に 1 回だけ解決されます。`Variables` に `${...}` を書いても再展開はされません（循環展開防止のための仕様）。

---

## レスポンスの形式

```json
{
  "ScenarioId": "<uuid>",
  "Status": "Completed",
  "AllStepsSucceeded": true,
  "StepResults": [
    {
      "StepName": "Load",
      "Success": true,
      "ErrorCode": "Success",
      "ArtifactIds": ["..."]
    }
  ],
  "ArtifactIds": ["...", "..."]
}
```

| Status | 意味 |
|---|---|
| `Completed` | すべてのステップが成功 |
| `Failed` | 1 つ以上のステップが失敗 |
| `Aborted` | シナリオ全体が 1800 秒の制限を超過 |

---

## 上限値

| 項目 | 上限 |
|---|---|
| 最大ステップ数 | 100 |
| シナリオ全体の制限時間 | 1800 秒 |
| 同時実行数 | 1（実行中に送信すると `TooManyRequests`） |
| ペイロードサイズ | 合計 1 MiB、Params 文字列 8 KiB |

---

## 例 — PIE バリデーションの完全なフロー

```json
{
  "ScenarioName": "PIE_HealthCheck",
  "Variables": { "ExpectedHp": 100 },
  "Steps": [
    { "StepName": "Load",   "CommandName": "UAIP.Runtime.PIE.LoadMap",
      "Params": { "MapPath": "/Game/Maps/TestMap" } },
    { "StepName": "Start",  "CommandName": "UAIP.Runtime.PIE.StartPIE", "Params": {} },
    { "StepName": "Settle", "CommandName": "UAIP.Runtime.Assertion.WaitSeconds",
      "Params": { "Seconds": 2 } },
    { "StepName": "Cap",    "CommandName": "UAIP.Runtime.Observation.CaptureViewportImage",
      "Params": {} },
    { "StepName": "Assert", "CommandName": "UAIP.Runtime.Assertion.AssertActorProperty",
      "Params": { "ActorIdentifier": "PlayerCharacter",
                  "PropertyName": "Health",
                  "ExpectedValue": "${Variables.ExpectedHp}" } },
    { "StepName": "Stop",   "CommandName": "UAIP.Runtime.PIE.StopPIE",
      "Params": {}, "AbortOnFailure": false }
  ]
}
```

`Stop` ステップに `AbortOnFailure: false` を設定することで、前のステップが失敗しても必ず PIE を終了させることができます。

---

## よくある問題

| 症状 | 原因 | 対処 |
|---|---|---|
| `PolicyViolation: Scenario execution is not enabled` | `enable_scenario` が未設定 | `config.json` に `"enable_scenario": true` を追加 |
| `StepResults` に Step 2 以降が含まれない | Step 1 がデフォルトの `AbortOnFailure: true` で失敗 | 続行したいステップに `"AbortOnFailure": false` を設定 |
| テンプレートが `"${...}"` のまま展開されない | シングルパス解決の仕様 — `Variables` は再展開されない | 値を `Variables` で直接渡すか、2 つのステップに分割する |
| `TooManyRequests` | 別のシナリオが実行中 | 完了するまで待つ |

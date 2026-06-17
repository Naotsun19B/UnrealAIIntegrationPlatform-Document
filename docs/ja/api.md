**[English](../en/api.md)** | [概要に戻る](overview.md)

# API リファレンス

本ページは UAIP の **機械向けリファレンス** です — リクエスト / レスポンス形式、エラーコード、Artifact 契約、シナリオプリミティブ、コマンド毎の JSON スキーマダンプ。独自ツール（LLM エージェント、CI スクリプト、コードジェネレータ）から UAIP を統合する場合、本ページをブックマークしてください。

人間向けにコマンド一覧を眺める場合は [コマンドリファレンス](commands.md) を参照。

---

## 目次

1. [Transport エンドポイント](#1-transport-エンドポイント)
2. [リクエスト形式](#2-リクエスト形式)
3. [レスポンス形式](#3-レスポンス形式)
4. [エラーコード](#4-エラーコード)
5. [Artifact 契約](#5-artifact-契約)
6. [セッション API](#6-セッション-api)
7. [シナリオ API](#7-シナリオ-api)
8. [型マッピング（UE → JSON）](#8-型マッピングue--json)
9. [コマンド完全スキーマダンプ](#9-コマンド完全スキーマダンプ)
10. [クライアント実装例](#10-クライアント実装例)
11. [バージョニング規約](#11-バージョニング規約)

---

## 1. Transport エンドポイント

どのトランスポートを使ってもリクエストは最終的に同じ `CommandDispatcher` にたどり着くため、Capability・Policy・ErrorCode のセマンティクスは transport に関係なく同一です。

| Transport | 形式 | エディタポート | パッケージポート | bind 層 | 認証 |
|---|---|---|---|---|---|
| HTTP（製品版） | REST + JSON | 8765 | 8767 | `0.0.0.0`（FullHTTP モードはリモート到達可、MCPOnly モードはアプリ層で localhost 強制） | `Authorization: Bearer <token>` |
| WebSocket（製品版） | JSON フレーム | 8766 | 8768 | `127.0.0.1` 固定 | 最初のフレームの `Token` フィールド |
| CLI（製品版） | stdin/stdout + CLI フラグ | — | — | — | なし（プロセス内） |
| MCP | AI クライアントの stdio 子プロセス | — | — | — | なし（子プロセス） |

トークンファイル（エディタ起動時に自動生成）：

```
<プロジェクト>/Saved/UAIP/EditorHttpAuthToken.txt
<プロジェクト>/Saved/UAIP/EditorWsAuthToken.txt
```

bind 層と認証層の関係の詳細は [セキュリティ → ネットワーク面](security.md#ネットワーク面) を参照してください。

---

## 2. リクエスト形式

### 2.1 `CommandRequest`（HTTP `POST /uaip/commands`）

```json
{
  "CommandName": "UAIP.Editor.Observation.CaptureActiveWindowImage",
  "Params":      { ... },
  "SessionId":   "my-task-001"
}
```

| フィールド | 型 | 必須 | 備考 |
|---|---|---|---|
| `CommandName` | string | はい | 完全修飾名（例：`UAIP.Core.HealthCheck`） |
| `Params` | object | いいえ | コマンド固有パラメータ（デフォルト `{}`）。コマンドの `ParameterSchema` で検証 |
| `SessionId` | string | いいえ | `[A-Za-z0-9_-]{1,128}`。省略時は匿名セッション |

### 2.2 `CommandRequest`（WebSocket フレーム）

```json
{
  "Type":                  "CommandRequest",
  "ClientProtocolVersion": "1.0",
  "Token":                 "<32文字 Bearer>",
  "RequestId":             "req-001",
  "SessionId":             "my-task-001",
  "CommandName":           "UAIP.Core.HealthCheck",
  "Params":                {}
}
```

- `Token` は最初のフレームのみ必須 — 接続が確立すれば寿命中は信頼される
- `RequestId` は対応する `CommandResponse` にエコーバックされ、クライアント側で対応付け可能
- `ClientProtocolVersion` でサーバが互換性ネゴシエート

### 2.3 `CommandRequest`（CLI インライン）

```
UnrealEditor.exe MyProject.uproject -uaip-request="{\"CommandName\":\"UAIP.Core.HealthCheck\",\"Params\":{}}"
```

または繰り返し利用：

```
UnrealEditor.exe MyProject.uproject -uaip-request-file=path/to/cmd.json
```

CLI リクエストは自動生成 `SessionId` を取得し、レスポンス書き出し後にエディタ終了。

### 2.4 `CommandRequest`（MCP）

MCP Bridge が同じ `CommandRequest` 形状をツール呼び出しでラップ：

```python
uaip_execute(
    CommandName="UAIP.Editor.Observation.CaptureActiveWindowImage",
    Params={"TabId": "/Game/Maps/Main"},
    SessionId="my-task-001"
)
```

`SessionId` 省略時 Bridge が自動設定（`MCP-Anonymous-<guid>`）。

---

## 3. レスポンス形式

### 3.1 `CommandResponse`（全 transport 統一）

```json
{
  "Success":      true,
  "Data":         { ... },
  "Artifacts":    [ { "ArtifactId": "...", "FilePath": "...", "Type": "Image" } ],
  "ErrorCode":    "Success",
  "ErrorMessage": ""
}
```

| フィールド | 型 | 備考 |
|---|---|---|
| `Success` | bool | `ErrorCode == "Success"` なら true |
| `Data` | object | コマンド固有の結果データ（各コマンドが形状を定義） |
| `Artifacts` | array | 生成された Artifact 毎に 1 エントリ。詳細は [§5](#5-artifact-契約) |
| `ErrorCode` | string | [§4](#4-エラーコード) のコードのいずれか、または `"Success"` |
| `ErrorMessage` | string | 人間可読の詳細。成功時は空 |

### 3.2 WebSocket エンベロープ

```json
{
  "Event":     "CommandResponse",
  "RequestId": "req-001",
  "Response":  { /* CommandResponse */ }
}
```

サーバが要求なしでイベントをプッシュすることもあります：

| `Event` | 方向 | 用途 |
|---|---|---|
| `AuthChallenge` | サーバ → クライアント | 新規接続での認証要求 |
| `Welcome` | サーバ → クライアント | 認証成功後送信、`SessionId` + `Capabilities` を含む |
| `CommandResponse` | サーバ → クライアント | `CommandRequest` への返信 |
| `ScenarioResponse` | サーバ → クライアント | `ScenarioRequest` への返信 |
| `OutputLogEntry` | サーバ → クライアント | UE ログストリーミング（`-uaip-ws-no-output-log` で抑止可能） |

### 3.3 CLI レスポンス

`-uaip-response-file=<path>` 指定時は JSON をそのパスに書き出します。指定なしの場合、レスポンスは stdout マーカーで囲まれます：

```
__UAIP_RESPONSE_BEGIN__
{ "Success": true, ... }
__UAIP_RESPONSE_END__
```

stdin-stream モードでも同じマーカーがリクエスト毎に出ます。

---

## 4. エラーコード

| ErrorCode | HTTP ステータス | 発生時 | 復旧方法 |
|---|---|---|---|
| `Success` | 200 | コマンド完了 | — |
| `CommandNotFound` | 404 | `CommandName` 未登録 | `UAIP.Core.ListCommands` で確認。オプションプラグインコマンドはプラグインロードが必要 |
| `InvalidParams` | 400 | 必須欠落 / 型不一致 / `AdditionalProperties:false` での未知フィールド | `UAIP.Core.DescribeCommand` でスキーマ再取得 |
| `CapabilityNotAvailable` | 403 | セッションに必要 Capability 不足 | `ErrorMessage` に不足 Capability 名。`Config/DefaultUAIP.ini` で有効化して再起動、または `UAIP.Core.ReloadCapabilities` |
| `PolicyViolation` | 403 | SafetyPolicy ゲートまたはルート opt-in 不足 | `ErrorMessage` で「SafetyPolicy 拒否」と「環境で未有効」を区別 |
| `NotFound` | 404 | パラメータ参照のアセット / アクター / オブジェクトが存在しない | `Search*` / `List*` コマンドでパス / GUID 確認 |
| `NotAllowed` | 409 | 禁止パス（例：`/Engine/`）または禁止タイミング（PIE 中の Editor 編集） | 別パスを選ぶか PIE 停止まで待つ |
| `ExecutionFailed` | 500 | ハンドラ内の Runtime 失敗 | `ErrorMessage` に詳細。シナリオでは `RetryCount` 活用 |
| `Timeout` | 408 | ステップ単位 / シナリオ単位の壁時計上限超過 | `TimeoutSeconds` を増やすかシナリオ分割 |
| `TooManyRequests` | 429 | 並行性制限ヒット（シナリオ同時 1 等） | 進行中リクエスト終了待ち |
| `InternalError` | 500 | プロセス障害レベル（ハンドラ例外、ディスパッチャ不変条件違反） | `RestartEditor`、継続なら `Saved/Crashes/` 添付で Issue 起票 |

HTTP ステータスは参考値 — 分岐は常に `ErrorCode` で。WebSocket と CLI は HTTP ステータスを持ちません。

---

## 5. Artifact 契約

### 5.1 `Artifact` オブジェクト

```json
{
  "ArtifactId":   "8D1403DB4896B4742E423CBD9F535F19",
  "FilePath":     "MCP-Anonymous-7b8e/Screenshots/CaptureActiveWindowImage-8D14....png",
  "Type":         "Image",
  "ContentType":  "image/png",
  "SizeBytes":    524288,
  "CreatedAt":    "2026-06-17T05:34:12Z"
}
```

| フィールド | 型 | 備考 |
|---|---|---|
| `ArtifactId` | string | 32 文字 hex。取得の主キー |
| `FilePath` | string | サーバ内部の **相対** パス（`Saved/UAIP/` 配下）。クライアント側で組み立てない — `ArtifactId` を使う |
| `Type` | enum | `Image` / `Json` / `Log` / `Report` / `Bundle` |
| `ContentType` | string | 取得時の MIME タイプ |
| `SizeBytes` | int | ストリーミング予算判断に使用 |
| `CreatedAt` | string | ISO 8601、UTC |

### 5.2 Artifact バイト取得

```http
GET /uaip/artifacts/{artifactId}
Authorization: Bearer <token>
```

レスポンス: 生バイト列、Artifact メタの `Content-Type`。GC 済み（セッション終了または TTL 切れ）の場合 404。

セッション単位の一覧取得：

```http
GET /uaip/sessions/{sessionId}/artifacts
Authorization: Bearer <token>
```

### 5.3 インライン埋め込み（MCP Bridge のみ）

MCP Bridge は小さな Artifact をレスポンスに base64 でインライン埋め込み可能：

```json
{
  "Success": true,
  "Artifacts": [ { "ArtifactId": "...", "Type": "Json", ... } ],
  "_inlined_artifacts": [
    {
      "artifact_id":   "...",
      "content_type":  "application/json",
      "data_base64":   "eyJTdGF0dXMiOiJIZWFsdGh5In0="
    }
  ]
}
```

インラインポリシーは [Artifacts → インライン vs フェッチの判定](artifacts.md#インライン-vs-フェッチの判定) を参照。HTTP / WebSocket / CLI はインラインせず、常にフェッチが必要。

---

## 6. セッション API

### 6.1 セッション作成・利用

セッションは新規 `SessionId` を使った最初のコマンドで暗黙的に作成されます。明示作成は不要 — 最初のリクエストで `SessionId="my-task"` を渡すだけ。

明示作成（HTTP、オプション）：

```http
POST /uaip/sessions
Authorization: Bearer <token>
Content-Type: application/json

{ "Hint": "my-task" }
```

レスポンス：

```json
{ "SessionId": "my-task-1718601234" }
```

### 6.2 セッション照会

```http
GET /uaip/sessions/{sessionId}
Authorization: Bearer <token>
```

セッションの Capability・OperationalConstraints（SafetyPolicy スナップショット）・Artifact 数を返却。

### 6.3 セッション終了

```
uaip_execute(CommandName="UAIP.Core.EndSession", Params={"SessionId":"my-task"})
```

または HTTP：

```http
DELETE /uaip/sessions/{sessionId}
Authorization: Bearer <token>
```

セッション終了で観測 Widget キャッシュ解放、Artifact が GC マーク。

### 6.4 Capability 発見

```
uaip_execute(CommandName="UAIP.Core.QueryCapabilities")
```

レスポンス `Data`：

```json
{
  "Capabilities": ["EditorInspect", "PIEControl", "RuntimeCapture", ...],
  "OperationalConstraints": {
    "ReadOnly":              false,
    "DisableSave":           false,
    "AllowLogDump":          true,
    "AllowContextMenuMutation": false,
    "AllowKeyboardInput":    true,
    "AllowKeyboardModifierInput": false,
    "DisablePIEStart":       false
  }
}
```

`OperationalConstraints` を先読みゲートとして利用：`ReadOnly:true` なら変更系コマンドを試行しない。

---

## 7. シナリオ API

シナリオは順序付きコマンドリストを 1 リクエストで実行します。概念ガイドは [シナリオ実行](scenario.md) を参照。

### 7.1 `ScenarioRequest`

```json
{
  "ScenarioName": "MyScenario",
  "SessionId":    "scenario-001",
  "Variables":    { "TargetHp": 100 },
  "Steps": [
    {
      "StepName":       "Load",
      "CommandName":    "UAIP.Runtime.PIE.LoadMap",
      "Params":         { "MapPath": "/Game/Maps/Foo" },
      "AbortOnFailure": true,
      "RetryCount":     0,
      "TimeoutSeconds": 60
    }
  ]
}
```

| ステップフィールド | 型 | デフォルト | 備考 |
|---|---|---|---|
| `StepName` | string | — | `[A-Za-z0-9_]{1,64}`、シナリオ内で一意 |
| `CommandName` | string | — | `uaip_execute` と同じ |
| `Params` | object | `{}` | テンプレート解決後 |
| `AbortOnFailure` | bool | `true` | false なら失敗してもシナリオ継続 |
| `RetryCount` | int | `0` | `ExecutionFailed` のみリトライ — `CapabilityNotAvailable` / `PolicyViolation` はしない |
| `TimeoutSeconds` | int | `60` | ステップ単位の壁時計上限 |

### 7.2 テンプレート式

| 式 | 解決値 |
|---|---|
| `${StepName.Success}` | bool |
| `${StepName.ErrorCode}` | string |
| `${StepName.Data.<JSON Pointer>}` | そのステップの `Data` 内のポインタ位置の任意 JSON 値 |
| `${StepName.Artifacts[<index>]}` | Artifact id 文字列 |
| `${StepName.Artifacts.<ArtifactId>}` | Artifact id 文字列 |
| `${Variables.<key>}` | リクエストの `Variables` マップの値 |

**型保持**：文字列フィールドがちょうど 1 つの `${...}` 式の場合、解決された JSON 値がそのまま置き換わります。混在文字列は文字列化されて連結。

**単一パス不変条件**：テンプレート結果は再評価されません。`Variables` に格納された `${...}` は後続ステップにリテラル文字列として渡ります。

### 7.3 `ScenarioResponse`

```json
{
  "ScenarioId":         "fc2a1c2e-...-7e9c",
  "ScenarioName":       "MyScenario",
  "Status":             "Completed",
  "StartedAt":          "2026-06-17T05:34:10Z",
  "CompletedAt":        "2026-06-17T05:34:18Z",
  "AllStepsSucceeded":  true,
  "StepResults": [
    {
      "StepName":     "Load",
      "Success":      true,
      "ErrorCode":    "Success",
      "ErrorMessage": "",
      "Data":         { ... },
      "ArtifactIds":  ["8D14..."],
      "AttemptCount": 1,
      "DurationMs":   1234
    }
  ],
  "ArtifactIds": ["8D14...", "F521..."]
}
```

| `Status` | 意味 |
|---|---|
| `Completed` | すべてのステップが成功 |
| `Failed` | 1 つ以上のステップが `Success:false` を返した |
| `Aborted` | シナリオ全体の 1800 秒上限を超過 |

### 7.4 ハード上限

| 上限 | 値 |
|---|---|
| 最大ステップ数 | 100 |
| シナリオ単位壁時計上限 | 1800 秒 |
| 同時実行シナリオ | 1（それ以外は `TooManyRequests`） |
| ステップ単位 `Params` 文字列 | 8 KiB |
| 合計 `Params` ペイロード | 256 KiB |
| `ScenarioRequest` 合計サイズ | 1 MiB |

---

## 8. 型マッピング（UE → JSON）

クライアント生成や LLM プロンプトを書く際、UE C++ 型が JSON ワイヤ形式でどう現れるかを知る必要があります。

| UE C++ 型 | JSON | 例 |
|---|---|---|
| `bool` | bool | `true` |
| `int32` / `int64` | number（整数） | `42` |
| `float` / `double` | number | `3.14` |
| `FString` / `FName` / `FText` | string | `"PlayerCharacter"` |
| `FGuid` | string（32 文字 hex、ブレース / ハイフンなし） | `"8D1403DB4896B4742E423CBD9F535F19"` |
| `FVector` | object `{X,Y,Z}` | `{"X":0,"Y":0,"Z":100}` |
| `FRotator` | object `{Pitch,Yaw,Roll}` | `{"Pitch":0,"Yaw":90,"Roll":0}` |
| `FTransform` | object `{Location,Rotation,Scale}` | ネスト |
| `FLinearColor` | object `{R,G,B,A}`（0.0–1.0） | `{"R":1,"G":0,"B":0,"A":1}` |
| `FColor` | object `{R,G,B,A}`（0–255 int） | `{"R":255,"G":0,"B":0,"A":255}` |
| `TArray<T>` | `T` の配列 | `[1,2,3]` |
| `TMap<FString,T>` | object | `{"k":v}` |
| `UObject*` 参照 | string（アセットパス / アクター識別子） | `"/Game/Blueprints/BP_Foo"` |
| `TSubclassOf<T>` | string（クラスパス） | `"/Script/Engine.StaticMeshActor"` |
| `enum class` | string（enum 値名） | `"Default"` |
| `FInstancedStruct` | object `{StructType, Value:{...}}` | `{"StructType":"/Script/Foo.FBar","Value":{...}}` |

NaN / Inf は `Number` フィールドで拒否 — ディスパッチャが `InvalidParams` を返します。

---

## 9. コマンド完全スキーマダンプ

プログラム的用途（ツール作成・コード生成・LLM 側バリデーション）には、全コマンドの完全スキーマを単一 JSON で取得します。

### 9.1 3 つの入手先

| 入手元 | 使い所 | 注意 |
|---|---|---|
| Runtime に `UAIP.Core.DescribeCommand` | 1 コマンドずつ、起動中エディタの実状反映 | 起動中エディタが必要 |
| 事前生成済み `commands-schema.json`（リリース同梱） | ビルド時ツール、オフラインコード生成 | 既知 UAIP バージョンの安定スナップショット |
| `docs/scripts/generate_command_schema.py` でローカル生成 | `ICommandProvider` で登録したプロジェクト固有コマンドも含む | 起動中エディタ + HTTP transport が必要 |

### 9.2 ローカル生成

```powershell
$Token = Get-Content "<プロジェクト>/Saved/UAIP/EditorHttpAuthToken.txt"
$env:UAIP_HTTP_TOKEN = $Token

python docs/scripts/generate_command_schema.py `
    --host http://127.0.0.1:8765 `
    --out  commands-schema.json
```

`-uaip-http-no-auth` 起動時は `--no-auth` を追加。Provider 毎の JSON も欲しい場合は `--split-by-provider` を追加（`by-provider/` 配下に出力）。

想定実行時間：オプションプラグイン構成にもよるが、約 730 コマンドで 10〜60 秒。

### 9.3 出力形状

```json
{
  "generatedAt":     "2026-06-17T05:34:12Z",
  "uaipVersion":     "1.0.0",
  "engineVersion":   "5.8.0",
  "commandCount":    735,
  "commands": [
    {
      "Name":                 "UAIP.Editor.Blueprint.AddBlueprintVariable",
      "ProviderName":         "UAIP.Editor.Blueprint",
      "Description":          "Blueprint にメンバー変数を追加（型・デフォルト・Tooltip）",
      "RequiredCapabilities": ["BlueprintEdit", "BlueprintVariableEdit"],
      "IsReadOnly":           false,
      "Available":            true,
      "Stability":            "Stable",
      "DeprecationMessage":   null,
      "MigrationTarget":      null,
      "ParameterSchema": {
        "Type":                 "Object",
        "AdditionalProperties": false,
        "Properties": {
          "BlueprintPath":   { "Type": "String",  "Description": "Blueprint アセットのパス（例：/Game/Blueprints/BP_Foo）" },
          "VariableName":    { "Type": "String",  "Description": "変数名。有効な識別子であること" },
          "PinCategory":     { "Type": "String",  "Description": "ピンカテゴリ（bool / int / real / object / struct / …）" },
          "PinSubCategory":  { "Type": "String",  "Description": "サブカテゴリ（例：real の double）" },
          "DefaultValue":    { "Type": "String",  "Description": "ImportText 形式のデフォルト値" }
        },
        "Required": ["BlueprintPath", "VariableName", "PinCategory"]
      }
    }
  ]
}
```

### 9.4 代表的なスキーマ 3 例

#### シンプル、パラメータなし

```json
{
  "Name": "UAIP.Core.HealthCheck",
  "RequiredCapabilities": [],
  "IsReadOnly": true,
  "ParameterSchema": {
    "Type": "Object", "AdditionalProperties": false,
    "Properties": {}, "Required": []
  }
}
```

#### ネストオブジェクト

```json
{
  "Name": "UAIP.Editor.Level.SetActorTransform",
  "RequiredCapabilities": ["EditorActorEdit"],
  "IsReadOnly": false,
  "ParameterSchema": {
    "Type": "Object", "AdditionalProperties": false,
    "Properties": {
      "ActorIdentifier": { "Type": "String" },
      "Location": { "Type": "Object", "Properties": {
        "X": {"Type":"Number"}, "Y": {"Type":"Number"}, "Z": {"Type":"Number"}
      } },
      "Rotation": { "Type": "Object", "Properties": {
        "Pitch": {"Type":"Number"}, "Yaw": {"Type":"Number"}, "Roll": {"Type":"Number"}
      } },
      "Scale":    { "Type": "Object", "Properties": {
        "X": {"Type":"Number"}, "Y": {"Type":"Number"}, "Z": {"Type":"Number"}
      } }
    },
    "Required": ["ActorIdentifier"]
  }
}
```

#### 配列 + enum 文字列

```json
{
  "Name": "UAIP.Editor.Assets.SearchAssets",
  "RequiredCapabilities": ["EditorInspect"],
  "IsReadOnly": true,
  "ParameterSchema": {
    "Type": "Object", "AdditionalProperties": false,
    "Properties": {
      "Path":       { "Type": "String", "Description": "コンテンツパス接頭辞（例：/Game/Characters）" },
      "ClassNames": { "Type": "Array",  "Description": "アセットクラス名（Blueprint / Material / DataAsset 等）" },
      "Recursive":  { "Type": "Boolean" }
    },
    "Required": ["Path"]
  }
}
```

---

## 10. クライアント実装例

### 10.1 HTTP — curl

```bash
TOKEN=$(cat /path/to/Saved/UAIP/EditorHttpAuthToken.txt)

curl -s -X POST http://127.0.0.1:8765/uaip/commands \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "CommandName": "UAIP.Core.HealthCheck",
    "Params": {},
    "SessionId": "smoke-test"
  }' | jq .
```

Artifact 取得：

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8765/uaip/artifacts/8D1403DB4896B4742E423CBD9F535F19 \
  -o capture.png
```

### 10.2 HTTP — Python

```python
import requests

class UAIPClient:
    def __init__(self, host="http://127.0.0.1:8765", token=None):
        self.host = host
        self.session = requests.Session()
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
        self.session.headers["Content-Type"] = "application/json"

    def execute(self, command, params=None, session_id=None):
        body = {"CommandName": command, "Params": params or {}}
        if session_id:
            body["SessionId"] = session_id
        r = self.session.post(f"{self.host}/uaip/commands", json=body, timeout=120)
        r.raise_for_status()
        data = r.json()
        if not data["Success"]:
            raise RuntimeError(f'{data["ErrorCode"]}: {data["ErrorMessage"]}')
        return data

    def fetch_artifact(self, artifact_id):
        r = self.session.get(f"{self.host}/uaip/artifacts/{artifact_id}", timeout=60)
        r.raise_for_status()
        return r.content

client = UAIPClient(token=open("...EditorHttpAuthToken.txt").read().strip())
print(client.execute("UAIP.Core.HealthCheck")["Data"])
```

### 10.3 WebSocket — JavaScript

```javascript
import WebSocket from "ws";
import { readFileSync } from "fs";

const token = readFileSync(".../EditorWsAuthToken.txt", "utf-8").trim();
const ws = new WebSocket("ws://127.0.0.1:8766/");

const pending = new Map();
let nextId = 1;

ws.on("open", () => {
  ws.send(JSON.stringify({
    Type: "CommandRequest",
    ClientProtocolVersion: "1.0",
    Token: token,
    RequestId: "init",
    SessionId: "ws-session",
    CommandName: "UAIP.Core.HealthCheck",
    Params: {}
  }));
});

ws.on("message", (raw) => {
  const msg = JSON.parse(raw);
  if (msg.Event === "CommandResponse") {
    const cb = pending.get(msg.RequestId);
    if (cb) { pending.delete(msg.RequestId); cb(msg.Response); }
    else    { console.log("init:", msg.Response); }
  }
});

function execute(command, params, sessionId) {
  return new Promise((resolve) => {
    const id = `req-${nextId++}`;
    pending.set(id, resolve);
    ws.send(JSON.stringify({
      Type: "CommandRequest",
      RequestId: id,
      SessionId: sessionId,
      CommandName: command,
      Params: params
    }));
  });
}
```

### 10.4 CLI — PowerShell ワンショット

```powershell
@'
{
  "CommandName": "UAIP.Editor.Execution.RunAutomationTest",
  "Params":      { "TestName": "MyGame.Smoke.MainMenu" }
}
'@ | Set-Content cmd.json

& "C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe" `
    "$pwd/MyGame.uproject" `
    "-uaip-request-file=$pwd/cmd.json" `
    "-uaip-response-file=$pwd/result.json"

$result = Get-Content result.json | ConvertFrom-Json
if (-not $result.Success) {
    Write-Error "$($result.ErrorCode): $($result.ErrorMessage)"
    exit 1
}
```

### 10.5 CLI — stdin-stream ラッパー（Python）

```python
import subprocess, json, threading

proc = subprocess.Popen(
    ["UnrealEditor.exe", "MyGame.uproject", "-uaip-stdin-stream"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    text=True, bufsize=1
)

def read_responses():
    buffer, capturing = [], False
    for line in proc.stdout:
        if "__UAIP_STREAM_READY__" in line:
            print("editor ready")
        elif "__UAIP_RESPONSE_BEGIN__" in line:
            capturing, buffer = True, []
        elif "__UAIP_RESPONSE_END__" in line:
            capturing = False
            yield json.loads("".join(buffer))
        elif capturing:
            buffer.append(line)

threading.Thread(target=lambda: list(read_responses()), daemon=True).start()

proc.stdin.write(json.dumps({"CommandName":"UAIP.Core.HealthCheck","Params":{}}) + "\n")
proc.stdin.flush()
```

---

## 11. バージョニング規約

UAIP はコマンドレベルで **セマンティックバージョニング** を採用します：

- **メジャー（1.x → 2.x）**: 破壊的変更可 — コマンドリネーム、パラメータ形状変更、Capability リネーム
- **マイナー（1.0 → 1.1）**: 追加のみ — 新規コマンド、新規オプションパラメータ、`Data` に新規フィールド。既存フィールドは維持
- **パッチ（1.0.0 → 1.0.1）**: バグ修正のみ、スキーマ変更なし

### コマンド毎の Stability ティア

| `Stability` | 契約 |
|---|---|
| `Stable` | スキーマはマイナーバージョン間で固定。リネーム / 削除はメジャー昇格時のみ |
| `Experimental` | 任意のリリースでスキーマ変更可能。スキーマダンプはスナップショット扱い、契約ではない |
| `Deprecated` | 次のメジャーで削除予定。`DeprecationMessage` + `MigrationTarget` が設定される |

### Capability リネーム

`RequiredCapabilities` エントリのリネーム時、旧名は 1 マイナーバージョンサイクル分は deny-default エイリアスとして残ります（例：1.2 でリネーム、旧エイリアスは 1.2・1.3 で認識、2.0 で削除）。

### バージョン取得

```
uaip_execute(CommandName="UAIP.Core.GetSystemInfo")
```

`UAIPVersion`・`EngineVersion`・`BuildConfig`・起動中エディタの `commandCount` を返却。

---

## 関連リンク

- [コマンドリファレンス](commands.md) — 1 行/コマンドのブラウズ用インデックス
- [Safety & Capabilities](safety.md) — Capability と SafetyPolicy のリファレンス
- [アーキテクチャ](architecture.md) — 内部ディスパッチパス
- [接続方法](connections.md) — transport 毎のセットアップ
- [シナリオ実行](scenario.md) — シナリオルートの概念ガイド
- [Artifacts](artifacts.md) — Artifact ライフサイクルとインラインポリシー

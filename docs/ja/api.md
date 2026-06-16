**[English](../en/api.md)** | [概要に戻る](overview.md)

# API リファレンス — コマンド完全スキーマ

[コマンドリファレンス](commands.md) は各コマンドを 1 行説明で列挙しています。プログラム的用途（ツール作成・コード生成・LLM 側バリデーション）には、各コマンドの **完全スキーマ**（パラメータ型・必須フィールド・デフォルト値・必要 Capability）が必要です。

本ページでは、その完全スキーマを JSON として生成する方法と利用方法を解説します。

---

## コマンド完全スキーマを取得する 3 つの方法

| 入手元 | 使い所 | 備考 |
|---|---|---|
| `uaip_describe_command(CommandName="...")` | Runtime に 1 コマンドずつ | 起動中エディタの実際の状態を反映。「自分のプラグイン構成でこのコマンドが使えるか」確認に最適 |
| 事前生成 JSON ダンプ（本ページ） | ツール / ジェネレータをオフラインで構築 | 既知の UAIP バージョンの安定スナップショット。消費時にエディタ起動不要 |
| ソースヘッダを読む | 最終手段 | 信頼できるが機械的なパースが大変 |

---

## ダンプを自分で生成する

スタンドアロンスクリプトを本リポジトリの [`docs/scripts/generate_command_schema.py`](../scripts/generate_command_schema.py) に同梱しています。

### 前提条件

- UAIP プラグインを有効化した UE エディタ
- エディタを HTTP transport 付きで起動: `-uaip-http-enable`
- Python 3.10+ と `requests`（`pip install requests`）

### 実行

```powershell
# 起動時に書き出された認証トークンを取得
$Token = Get-Content "<プロジェクト>/Saved/UAIP/EditorHttpAuthToken.txt"
$env:UAIP_HTTP_TOKEN = $Token

# スキーマダンプを生成
python docs/scripts/generate_command_schema.py `
    --host http://127.0.0.1:8765 `
    --out  commands-schema.json
```

エディタを `-uaip-http-no-auth` で起動した場合は `--no-auth` を追加。Provider 毎の JSON も欲しい場合は `--split-by-provider` を追加（`by-provider/` 配下に出力）。

### 実行時間

オプションプラグイン構成にもよりますが、約 730 コマンドで 10〜60 秒程度。

---

## 出力フォーマット

```json
{
  "generatedAt": "2026-06-17T05:34:12Z",
  "uaipVersion": "1.0.0",
  "engineVersion": "5.8.0",
  "commandCount": 735,
  "commands": [
    {
      "Name": "UAIP.Core.HealthCheck",
      "ProviderName": "UAIP.Core",
      "Description": "プラグイン接続確認 — Status・UAIPVersion・EngineVersion・BuildConfig を返却",
      "RequiredCapabilities": [],
      "IsReadOnly": true,
      "Available": true,
      "Stability": "Stable",
      "ParameterSchema": {
        "Type": "Object",
        "AdditionalProperties": false,
        "Properties": {},
        "Required": []
      }
    },
    ...
  ]
}
```

### コマンドディスクリプタのフィールド

| フィールド | 型 | 備考 |
|---|---|---|
| `Name` | string | 完全修飾コマンド名 |
| `ProviderName` | string | 所属プロバイダ（`UAIP.Editor.Blueprint`・`Toolset.AnimationAssistant` 等） |
| `Description` | string | 人間可読の 1 行サマリ |
| `RequiredCapabilities` | string 配列 | すべてセッションに必要 |
| `IsReadOnly` | bool | true なら `ReadOnly=True` SafetyPolicy に阻まれない |
| `Available` | bool | オプションプラグイン未ロード時は false |
| `Stability` | enum | `Stable` / `Experimental` / `Deprecated` |
| `DeprecationMessage` | string? | `Stability=Deprecated` の場合に存在 |
| `MigrationTarget` | string? | 廃止予定コマンドの後継コマンド名 |
| `ParameterSchema` | object | `Params` の JSON-Schema 風記述 |

### ParameterSchema 構造

パラメータスキーマは軽量な JSON-Schema 方言です：

```json
{
  "Type": "Object",
  "AdditionalProperties": false,
  "Properties": {
    "ActorIdentifier": { "Type": "String", "Description": "..." },
    "Location":        { "Type": "Object", "Properties": {
                          "X": { "Type": "Number" },
                          "Y": { "Type": "Number" },
                          "Z": { "Type": "Number" }
                        } },
    "Rotation":        { "Type": "Object", "Properties": { ... } }
  },
  "Required": ["ActorIdentifier", "Location"]
}
```

- `Type`: `String` / `Number` / `Integer` / `Boolean` / `Object` / `Array`
- `Required`: 省略不可フィールド
- `AdditionalProperties: false`: 余分なフィールドは `InvalidParams` を返す
- 列挙型の候補リストは通常 `Description` 内に記載

---

## 利用例

### スキーマから TypeScript 型を生成

```typescript
import schema from './commands-schema.json' assert { type: 'json' };

type CommandName = (typeof schema.commands)[number]['Name'];
// → "UAIP.Core.HealthCheck" | "UAIP.Editor.Blueprint.AddGraphNode" | ...
```

### LLM 側バリデーションプロンプト

> システム: UAIP コマンドを呼び出す際は、呼び出し前に以下のスキーマに対してパラメータを検証してください。Required フィールド欠落、または Properties に含まれないフィールドを持つ呼び出しは拒否してください。
>
> `<CommandName>` のスキーマ: { ... }

### Capability を意識したコマンドピッカ

ダンプから、特定セッションが実際に実行可能なコマンドのみフィルタ：

```python
import json
with open("commands-schema.json", "r", encoding="utf-8") as f:
    payload = json.load(f)

granted_capabilities = {"EditorInspect", "EditorObservation", "PIEControl"}
available = [
    cmd for cmd in payload["commands"]
    if cmd["Available"]
       and all(cap in granted_capabilities for cap in cmd["RequiredCapabilities"])
]
print(f"{len(available)} 件のコマンドが現在の Capability で呼び出し可能")
```

---

## 事前生成ダンプの入手先

各プラグインリリースアーカイブに `commands-schema.json` として同梱。特定の UE バージョン + UAIP バージョンの組み合わせの現在スナップショットだけ必要なら [Releases](../../../releases) を参照（エディタ起動不要）。

プロジェクト固有のカスタムコマンド（自分のモジュールで `ICommandProvider` 経由登録したもの）は、ローカル生成ダンプのみが捕捉します。

---

## スキーマの安定性

- **UAIP マイナーバージョン内** では `Name`・`RequiredCapabilities`・`ParameterSchema` フィールドは安定
- **メジャーバージョン跨ぎ** の破壊的変更は [ロードマップ](roadmap.md) に列挙、リリースノートで告知
- **`Stability: Experimental`** コマンドは任意のリリースで変わる可能性。スキーマは情報用扱い
- **`Stability: Deprecated`** コマンドには `DeprecationMessage` と `MigrationTarget` が付く。移行を計画してください

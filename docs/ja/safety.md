**[English](../en/safety.md)** | [概要に戻る](overview.md)

# Safety & Capabilities

UAIP はコマンドごとの認可を 3 つの層で管理します。層を理解するとエラーの原因を素早く特定できます。

---

## 認可の 3 層構造

| 層 | メカニズム | 失敗時のエラー |
|---|---|---|
| 1 | セッションの `FCapabilitySet` — セッション × コマンド単位 | `CapabilityNotAvailable` |
| 2 | `FSafetyPolicy` のブールスイッチ / DeniedCapabilities — プロセス全体 | `PolicyViolation` |
| 3 | ルート単位のオプトイン（シナリオルートなど）— プロセス全体 | `PolicyViolation` |

---

## Capability（ケイパビリティ）

各コマンドは `RequiredCapabilities` を宣言しています。セッションが必要な Capability をすべて持っているときのみコマンドを実行できます。

- **DefaultAllow** — 新しいセッションに自動で付与される
- **DefaultDenied** — デフォルトでは付与されない。`Config/DefaultUAIP.ini` で明示的に有効化が必要

```
# コマンドが必要とする Capability を確認
uaip_describe_command(CommandName="UAIP.Editor.Blueprint.CompileBlueprint")
→ RequiredCapabilities: ["BlueprintEdit"]

# 現在のセッションの Capability を確認
uaip_query_capabilities()
→ Capabilities: ["...", ...]
```

Capability が不足している場合のエラー：

```json
{ "ErrorCode": "CapabilityNotAvailable",
  "ErrorMessage": "Required capability is not available: BlueprintEdit" }
```

DefaultDenied の Capability は `Config/DefaultUAIP.ini` で解除できます（下記参照）。

---

## SafetyPolicy の設定

プロジェクトの `Config/DefaultUAIP.ini` を編集します：

```ini
[UAIP.SafetyPolicy]
ReadOnly=False
DisableSave=False
AllowLogDump=False
AllowContextMenuMutation=False
AllowKeyboardInput=False
AllowKeyboardModifierInput=False
AllowPasswordFieldWrite=False
AllowInputModeBypass=False
DisablePIEStart=False

; DefaultDenied の Capability を解除（1行に1つ）：
; +AllowedCapabilities=BlueprintEdit
; +AllowedCapabilities=SkeletonAssetEdit

; 特定のコマンドをブロック：
; +DeniedCommands=UAIP.Editor.Level.PlaceActorInLevel
```

### 設定一覧

| キー | デフォルト | 効果 |
|---|---|---|
| `ReadOnly` | `False` | すべての書き込みコマンドを拒否 |
| `DisableSave` | `False` | ディスク書き込みコマンドを拒否 |
| `AllowLogDump` | `False` | `DumpOutputLog` / `DumpMessageLog` を許可 |
| `AllowContextMenuMutation` | `False` | `InvokeContextMenuAction` を許可 |
| `AllowKeyboardInput` | `False` | `PressKey` を許可 |
| `AllowKeyboardModifierInput` | `False` | `PressKey` 内の Ctrl/Alt/Shift を許可 |
| `AllowPasswordFieldWrite` | `False` | `FillForm` でパスワードフィールドへの書き込みを許可 |
| `AllowInputModeBypass` | `False` | Inject 系コマンドの `BypassInputMode=true` を許可 |
| `DisablePIEStart` | `False` | PIE 起動を拒否 |
| `AllowedCapabilities` | 空 | DefaultDenied の Capability を解除（1行に1つ） |
| `DeniedCapabilities` | 空 | DefaultAllow の Capability をセッションから取り除く |
| `DeniedCommands` | 空 | 完全修飾名で指定したコマンドをブロック |
| `AllowCapabilityReload` | `False` | `UAIP.Core.ReloadCapabilities` コマンドを有効化 |

---

## DefaultDenied の Capability を解除する

`[UAIP.SafetyPolicy]` に `+AllowedCapabilities=<name>` を追加します：

```ini
[UAIP.SafetyPolicy]
+AllowedCapabilities=BlueprintEdit
+AllowedCapabilities=SkeletonAssetEdit
```

ini を編集した後、Editor を再起動するか（`AllowCapabilityReload=True` が設定済みなら）以下を呼び出します：

```
uaip_execute(CommandName="UAIP.Core.ReloadCapabilities")
```

---

## エラーの診断

| エラーコード | 診断 | 対処 |
|---|---|---|
| `CapabilityNotAvailable` | セッションに Capability がない | `ErrorMessage` の Capability 名を `AllowedCapabilities` に追加して再起動 |
| `PolicyViolation: ... denied by SafetyPolicy` | SafetyPolicy の ini フラグで拒否 | `[UAIP.SafetyPolicy]` の対応するフラグを `True` にして再起動 |
| `PolicyViolation: Scenario execution is not enabled` | シナリオルートのオプトイン不足 | `config.json` に `"enable_scenario": true` を追加 |
| `PolicyViolation: Command is denied` | コマンドが `DeniedCommands` に入っている | ini から該当エントリを削除して再起動 |

---

## よく使う DefaultDenied Capability

| Capability | 必要なコマンド |
|---|---|
| `BlueprintEdit` | Blueprint グラフ・変数・関数の編集 |
| `SkeletonAssetEdit` | スケルトン・スケルタルメッシュの編集 |
| `EditorLifecycle` | `ShutdownEditor`、`RestartEditor` |
| `LogDump` | `DumpOutputLog`、`DumpMessageLog` |

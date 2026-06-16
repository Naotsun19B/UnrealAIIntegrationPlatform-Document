**[English](../en/security.md)** | [概要に戻る](overview.md)

# セキュリティモデル

UAIP は UE エディタと Runtime を AI エージェントや外部ツールに公開します。本ページではセキュリティ境界 — UAIP がデフォルトで許可する範囲、ゲートの位置、運用者がデプロイを強化するために行う設定 — を解説します。

---

## 脅威モデル

UAIP は **開発者マシンと信頼された社内 CI** 向けに設計されており、公開インターネットサービスではありません。緩和する脅威：

| 脅威 | 緩和策 |
|---|---|
| ネットワーク攻撃者によるポートスキャン | Localhost 限定バインド（外部インターフェースで listen しない） |
| UAIP 以外のローカルプロセスによるコマンド呼び出し | HTTP / WebSocket での Bearer トークン認証 |
| AI が破壊的コマンドを幻覚で呼び出し | Capability ゲート（編集系はデフォルト拒否）+ コマンド毎の `IsReadOnly` フラグ |
| AI が騙されて広範囲な変更を実行 | SafetyPolicy でエディタをプロセス全体 Read-Only に切替可能 |
| レスポンス経由のファイルパスインジェクション | Artifact は ID 参照、生パスはサーバ外に出さない |
| 透かし除去目的のプラグインファイル差し替え | 透かしを DLL にコンパイル、合成失敗時はフェイルクローズ |

緩和**しない**脅威：

- ホストにシェルアクセスできる攻撃者は `Saved/UAIP/EditorHttpAuthToken.txt` を読み、AI クライアントを偽装可能。ホスト全体を信頼境界と見なす
- 同一マシン上で UAIP 自体をロードする悪意あるプロジェクトは任意のコマンドを登録可能。信頼できない UAIP 入りプロジェクトをロードしないこと
- AI クライアントへの prompt injection は UAIP のスコープ外 — AI クライアント自身で対処すべき

---

## ネットワーク面

| コンポーネント | バインド | デフォルトポート | 認証 |
|---|---|---|---|
| HTTP transport（製品版） | `127.0.0.1` と `::1` | 8765（エディタ）/ 8767（パッケージ） | Bearer トークン |
| WebSocket transport（製品版） | `127.0.0.1` と `::1` | 8766（エディタ）/ 8768（パッケージ） | Bearer トークン（最初のフレーム） |
| MCP Bridge | AI クライアントと Bridge プロセス間の stdio | — | なし — ホスト信頼に依存 |
| CLI transport（製品版） | なし（プロセス内） | — | なし |

**UAIP transport はすべて非ループバック接続を拒否します。** `-uaip-http-bind=0.0.0.0` のようなフラグは存在しません。マシン間で UAIP を公開する場合は、自管理のリバースプロキシ / VPN の背後に置いてください。

---

## 認証

### HTTP / WebSocket Bearer トークン

起動時に UAIP が 32 文字のランダムトークンを生成し、以下に書き出します：

```
Saved/UAIP/EditorHttpAuthToken.txt
Saved/UAIP/EditorWsAuthToken.txt
```

ファイルは OS デフォルト権限で書き込まれます。`Saved/UAIP/` を読める者はクライアントを偽装可能 — エディタ利用ユーザーを信頼プリンシパルとみなしてください。

トークンはエディタ再起動の度に自動でローテーションされます。エディタ起動中に強制ローテーションするにはファイルを削除して再起動してください。

### 認証無効化（開発時のみ）

```
UnrealEditor.exe MyProject.uproject -uaip-http-enable -uaip-http-no-auth
UnrealEditor.exe MyProject.uproject -uaip-ws-enable -uaip-ws-no-auth
```

**信頼できないプロセスが存在しない** 隔離開発マシンや CI ランナーでのみ使用。バインドは依然ループバック限定なので `-no-auth` でもネットワーク到達不能ですが、同一マシン上の任意プロセスがコマンドを発行可能になります。

### MCP Bridge

MCP は AI クライアントの stdio 子プロセスとして動くため、認証は AI クライアント自身の MCP transport が使うもの（通常なし — 既に子プロセス）に依存します。Bridge はエディタを自身の子プロセスとして起動するため、コマンドフローはエンドツーエンドでローカル。

---

## 認可

UAIP は各コマンドに対して 3 つの独立した認可層を実行します：

```mermaid
flowchart TB
    Req([CommandRequest])
    L1[Layer 1:<br/>DeniedCommands に含まれる?]
    L2[Layer 2:<br/>セッションが必要 Capability を持つ?]
    L3[Layer 3:<br/>SafetyPolicy フラグが許可?]
    OK([実行])

    Req --> L1
    L1 -- ブロック --> X1([PolicyViolation])
    L1 -- pass --> L2
    L2 -- 不足 --> X2([CapabilityNotAvailable])
    L2 -- あり --> L3
    L3 -- 拒否 --> X3([PolicyViolation])
    L3 -- 許可 --> OK
```

### Layer 1 — Capability セット

各コマンドは必要 Capability を宣言（`BlueprintEdit`・`PIEControl` 等）。セッションの Capability セットが何を呼べるか決定。DefaultAllow Capability は自動付与、DefaultDenied は `Config/DefaultUAIP.ini` で明示的に `+AllowedCapabilities=<名前>` が必要。

### Layer 2 — SafetyPolicy 真偽フラグ

プロセス全体のキルスイッチ：

| フラグ | 効果 |
|---|---|
| `ReadOnly=True` | すべての変更コマンドを拒否（`IsReadOnly=false` ハンドラ） |
| `DisableSave=True` | すべてのディスク書き込みコマンドを拒否 |
| `AllowLogDump=False` | `DumpOutputLog` / `DumpMessageLog` を拒否 |
| `AllowContextMenuMutation=False` | `InvokeContextMenuAction` を拒否 |
| `AllowKeyboardInput=False` | `PressKey` を拒否 |
| `AllowKeyboardModifierInput=False` | `PressKey` 内の修飾キーを拒否 |
| `AllowPasswordFieldWrite=False` | `FillForm` のパスワードフィールド書き込みを拒否 |
| `AllowInputModeBypass=False` | 入力注入の `BypassInputMode=true` を拒否 |
| `DisablePIEStart=True` | PIE 起動を拒否 |

これらは意図的にプロセス全体スコープで、Runtime に AI が変更不可。オペレーターのみ変更可能（ini 編集 + エディタ再起動、または `AllowCapabilityReload=True` の場合は `UAIP.Core.ReloadCapabilities`）。

### Layer 3 — ルート opt-in

一部の機能はエディタ起動時の CLI フラグが必要：

| 機能 | フラグ |
|---|---|
| HTTP transport | `-uaip-http-enable` |
| WebSocket transport | `-uaip-ws-enable` |
| MCP transport | `-uaip-mcp-enable` |
| シナリオルート | `-uaip-enable-scenario` |

フラグなしの場合、対応するコードパスは登録すらされません（「登録されているが拒否」ではない）。デモバイナリでは HTTP / WS / CLI フラグはサイレントに無視されます。

完全リファレンスと ini 例は [Safety & Capabilities](safety.md) を参照。

---

## 推奨セキュリティプロファイル

### 「Read-only レビュー」 — 信頼できない PR の AI レビュー用

```ini
[UAIP.SafetyPolicy]
ReadOnly=True
DisableSave=True
AllowLogDump=True
DisablePIEStart=False
```

AI は観測・キャプチャ可能だが、何も編集できない。新しくチェックアウトしたブランチを LLM に PR レビューさせたいときに有用。

### 「サンドボックスプレイテスト」 — AI 駆動テスト自動化（エディタ編集なし）

```ini
[UAIP.SafetyPolicy]
ReadOnly=False
DisableSave=True
AllowLogDump=True

+AllowedCapabilities=PIEControl
+AllowedCapabilities=RuntimeActorManipulation
+AllowedCapabilities=RuntimeExecCommand
+AllowedCapabilities=RuntimeInputInjection
```

PIE 制御 + Runtime 入力 + アサート、エディタ編集なし、ディスク書き込みなし。

### 「フル編集」 — エディタ編集を含む AI ペアプロ用

```ini
[UAIP.SafetyPolicy]
ReadOnly=False
AllowLogDump=True
AllowContextMenuMutation=True
AllowKeyboardInput=True
AllowKeyboardModifierInput=True
AllowCapabilityReload=True

; 実際に必要な編集 Capability のみ列挙すること
+AllowedCapabilities=BlueprintEdit
+AllowedCapabilities=BlueprintGraphEdit
+AllowedCapabilities=BlueprintVariableEdit
+AllowedCapabilities=PropertyEdit
+AllowedCapabilities=AssetDelete
+AllowedCapabilities=EditorActorEdit
; …ワークフローに応じて追加
```

`+AllowedCapabilities` の付与は慎重に。1 つ追加するごとに、AI が確認なしで実行できる操作カテゴリが 1 つ増えます。

---

## Artifact のストレージ

Artifact は `<プロジェクト>/Saved/UAIP/<SessionId>/` 配下に書き出されます。デフォルトではパス制約なし — ハンドラは `Saved/UAIP/` 配下のどこにでも書ける。サンドボックスルートを強制するには：

```ini
[UAIP.SafetyPolicy]
AllowedArtifactDirectory=Saved/UAIP/
```

このルートから逸脱するパスは `NotAllowed` で拒否されます。デフォルト値が既に `Saved/UAIP/` のため、明示設定は主により厳格なサブパス（例：CI ジョブ毎）を指定したい場合に有用です。

Artifact はディスク上で暗号化されません。`DumpWorldState` 等でダンプされた機密データはファイルシステムアクセスを持つ任意ユーザーが読めます。問題になる場合は `Saved/UAIP/` の OS レベル権限を制限してください。

---

## 監査ログ

各コマンドは UE の出力ログに構造化されたログ行を書きます。`DumpOutputLog` と組み合わせると、以下の事後監査トレイルが得られます：

- コマンド名と SessionId
- ErrorCode（失敗時）
- 生成された ArtifactId
- 壁時計実行時間

CI では UE 出力をファイルにリダイレクトし、テスト artifact と一緒にアーカイブしてください。

v1.0 時点では別途のコマンド監査ログファイルはありません。必要なら機能リクエストをお寄せください。

---

## 脆弱性報告

セキュリティ問題については **公開 GitHub Issue を立てないでください**。`1999naotsun0411@gmail.com` 宛にメールで以下を送ってください：
- UE バージョン + UAIP バージョン（`UAIP.Core.GetSystemInfo`）
- 脆弱性の説明と再現手順
- 非ループバックオリジンから悪用可能か（最優先）／ローカルコード実行が必要か（優先度低だがトラッキング対象）

数営業日以内に受領確認し、開示を調整します。

**[English](../en/config.md)** | [概要に戻る](overview.md)

# 設定リファレンス

このページは SafetyPolicy / Capability 以外の UAIP 設定項目を列挙します。
SafetyPolicy と Capability については [Safety & Capabilities](safety.md) を参照してください。

---

## 設定の読み込み元

UAIP は以下 4 つの場所から設定を読み込み、優先度順にマージします（後勝ち）：

| 優先度 | 読み込み元 | スコープ | 反映 |
|---|---|---|---|
| 1 | `Plugins/UnrealAIIntegrationPlatform/Config/DefaultUAIP.ini` | プラグイン同梱のデフォルト | エディタ再起動 |
| 2 | `<Project>/Config/DefaultUAIP.ini` | プロジェクト単位のオーバーライド（バージョン管理対象） | エディタ再起動 |
| 3 | `<Project>/Saved/UAIP/UAIPOverride.ini` | **パッケージビルド専用** — 初回起動時に自動生成されるユーザー編集可能オーバーライド | エディタ再起動 |
| 4 | CLI 起動フラグ（`-uaip-*`） | プロセス単位の一時設定 | エディタ再起動 |

`AllowedCapabilities` / `DeniedCapabilities` は `UAIP.Core.ReloadCapabilities` コマンドで再起動なしに反映できます（[Safety & Capabilities](safety.md#enabling-defaultdenied-capabilities) を参照）。それ以外のキーはエディタ再起動が必要です。

> MCP Bridge（インストール後は `Plugins/UAIPMCPBridge/`）には独自の設定レイヤー（`config.json` + 環境変数）があります。Bridge はプラグイン本体とは別配布です — 下の [MCP Bridge `config.json`](#mcp-bridge-configjson) を参照。

---

## ini セクション（SafetyPolicy 以外）

すべて `Config/DefaultUAIP.ini` の `[UAIP.*]` ヘッダ配下に置きます。各キーは opt-in 形式で、コメントアウトされたキーは下表の組み込みデフォルト値が使われます。

### `[UAIP.CommandNotification]` — エディタのトースト通知

コマンド実行ごとに Slate のトースト通知を表示します。開発・ライブデモ用途を想定しており、**CI / 自動化では無効化** してください（トーストがスクリーンショットや録画に映り込みます）。

| キー | 型 | デフォルト | 範囲 | 説明 |
|---|---|---|---|---|
| `Enabled` | bool | `False` | — | トースト通知のマスタースイッチ |
| `DurationSeconds` | float | `4.0` | `[1.0, 30.0]` | 各トーストの表示秒数。失敗トーストは +2.0 秒追加 |
| `MaxConcurrentNotifications` | int32 | `5` | `[1, 20]` | 同時表示数の上限 |
| `ThrottleWindowSeconds` | float | `2.0` | `[0.1, 60.0]` | 同一コマンドの集約ウィンドウ |

CLI フラグ：なし。

### `[UAIP.Session]` — セッション永続化

セッションメタデータ（ID・コマンドログ・Capability セット）をディスクに永続化し、エディタ再起動を跨いでセッションを復元する機能の設定。

| キー | 型 | デフォルト | 範囲 | 説明 |
|---|---|---|---|---|
| `Enabled` | bool | `True` | — | セッション永続化のマスタースイッチ |
| `SubDirectory` | string | `Sessions` | — | Artifact ルート配下のセッション格納サブディレクトリ |
| `MaxCommandLogEntries` | int32 | `100` | `[1, 10000]` | セッションファイルあたりの最大コマンドログ件数 |
| `SessionLifetimeHours` | float | `24.0` | `[1.0, 8760.0]` | アイドル状態とみなされるまでの時間 |
| `MaxAllowedLifetimeHours` | float | `168.0` | `[1.0, 87600.0]` | 更新を含めたセッション総寿命の上限 |
| `MaxScanFiles` | int32 | `1000` | `[1, 100000]` | 起動時にセッションを復元する際にスキャンする最大ファイル数 |

CLI フラグ：`-uaip-session-enabled` / `-uaip-session-sub-directory=...` / `-uaip-session-max-command-log-entries=N` / `-uaip-session-lifetime-hours=N` / `-uaip-session-max-allowed-lifetime-hours=N` / `-uaip-session-max-scan-files=N`

### `[UAIP.ArtifactGC]` — Artifact 自動 GC

Artifact ルート配下の古い Artifact ファイルを定期的に削除する仕組み。長時間運用で `Saved/UAIP/` が無制限に肥大化するのを防ぎます。

| キー | 型 | デフォルト | 範囲 | 説明 |
|---|---|---|---|---|
| `Enabled` | bool | `True` | — | 定期 GC のマスタースイッチ |
| `MaxAgeHours` | int32 | `24` | `[1, 8760]` | この時間を超えた Artifact が GC 対象 |
| `MaxSessionCount` | int32 | `50` | `[1, 100000]` | セッション数がこれを超えると古い順に削除 |
| `CleanupIntervalSeconds` | float | `3600.0` | `[60.0, 86400.0]` | GC 実行間隔 |

CLI フラグ：`-uaip-gc-enabled` / `-uaip-gc-max-age-hours=N` / `-uaip-gc-max-session-count=N` / `-uaip-gc-cleanup-interval-seconds=N`

### `[UAIP.PythonExtension]` — Python コマンド拡張（🧩 `PythonScriptPlugin`）

`@uaip_command` デコレータ付き Python ファイルをスキャンする場所を指定します。`.uproject` で `PythonScriptPlugin` が有効な場合のみ登録されます。

| キー | 型 | デフォルト | 説明 |
|---|---|---|---|
| `CommandsDir` | string | `<Project>/Scripts/UAIPCommands` | Python コマンド定義ファイルを探すディレクトリ。相対パスはプロジェクトルートを基点に解決 |

CLI フラグ：なし。

> `[UAIP.SafetyPolicy]` セクションは意図的にこのページから除外しています — `AllowedCapabilities` / `DeniedCapabilities` / `DeniedCommands` / `AllowCapabilityReload` を含む完全なリファレンスは [Safety & Capabilities](safety.md) を参照。

### `AllowedArtifactDirectory` オーバーライド

`[UAIP.SafetyPolicy]` 配下に置かれているキー（サンドボックス境界は安全性の懸案事項のため）ですが、すべての Artifact 生成コマンドが参照する基本パスです：

```ini
[UAIP.SafetyPolicy]
AllowedArtifactDirectory=Saved/MyCustomUAIPStorage
```

- デフォルト：`<Project>/Saved/UAIP/`
- ini 専用（CLI フラグはなし — サンドボックスルートはプロセス起動時に確定）
- 絶対パスでなければプロジェクトルートからの相対パスとして解決

---

## CLI 起動フラグ

CLI フラグはエディタプロセスのコマンドライン（`UnrealEditor.exe MyProject.uproject <flags>`）から読み込まれます。ini 由来の値より優先され、プロセス起動中のみ有効です。

### Transport opt-in

各 Transport はデフォルト無効。起動時の opt-in が必要です。

| フラグ | 説明 |
|---|---|
| `-uaip-http-enable` | HTTP API モード（FullHTTP）を有効化。`0.0.0.0:<port>` にバインドし `/uaip/*` + `/mcp` を公開。`-uaip-http-no-auth` がない限り Bearer Token 必須 |
| `-uaip-mcp-enable` | MCP 専用モードを有効化。`-uaip-http-enable` を暗黙的に有効化するが `/mcp` と `/uaip/artifacts/*` のみ公開。5 段階の localhost チェック（PeerAddress / Host / Origin）を強制。認証不要 |
| `-uaip-ws-enable` | WebSocket Transport を有効化。`127.0.0.1:<port>` にバインド（ハードコード）。`-uaip-ws-no-auth` がない限り初回フレームに Bearer Token 必須 |
| `-uaip-enable-scenario` | `uaip_run_scenario` ルートを有効化。これがないと scenario 送信時に `PolicyViolation: Scenario execution is not enabled` |

`-uaip-http-enable` と `-uaip-mcp-enable` を両方指定した場合は **MCP モードが優先** され、HTTP API モードは起動しません。

### ポート上書き

| フラグ | デフォルト | 説明 |
|---|---|---|
| `-uaip-http-port=N` | `8765` | HTTP / MCP Transport の TCP ポート |
| `-uaip-ws-port=N` | `8766` | WebSocket Transport の TCP ポート |

### 認証バイパス（CI / サンドボックス専用）

| フラグ | 説明 |
|---|---|
| `-uaip-http-no-auth` | HTTP API の Bearer Token 検証を無効化。**隔離された CI 環境でのみ** 使用 — [Security](security.md) を参照 |
| `-uaip-ws-no-auth` | WebSocket の Bearer Token 検証を無効化。同じ注意事項。指定時は OutputLog 転送チャネルも無効化される |

### WebSocket ログ

| フラグ | 説明 |
|---|---|
| `-uaip-ws-log-verbose` | OutputLog 転送の閾値を `Display` → `Verbose` に下げる |
| `-uaip-ws-no-output-log` | OutputLog 転送を完全に無効化（`-uaip-ws-no-auth` 指定時も自動で無効） |

### CLI Transport（一発実行）

エディタコマンドラインから単一コマンド（または scenario）を実行し、JSON レスポンスを書き出して終了します。シェルスクリプトや CI フックでの利用を想定。

| フラグ | 説明 |
|---|---|
| `-uaip-request=<json>` | インライン `uaip_execute` リクエスト JSON（シェルに応じてクォートをエスケープ） |
| `-uaip-request-file=<path>` | ファイルからリクエスト JSON を読み込み |
| `-uaip-scenario=<json>` | インライン `uaip_run_scenario` ペイロード |
| `-uaip-scenario-file=<path>` | ファイルから scenario JSON を読み込み |
| `-uaip-response-file=<path>` | レスポンス書き出し先。省略時は stdout |
| `-uaip-stdin` | リクエスト JSON を標準入力から読み込み |

例：

```bash
# HealthCheck を 1 回実行し、JSON レスポンスを ./result.json に書き出し
UnrealEditor-Cmd.exe MyProject.uproject \
  -uaip-request='{"CommandName":"UAIP.Core.HealthCheck","Params":{}}' \
  -uaip-response-file=./result.json

# 保存済み scenario を実行
UnrealEditor-Cmd.exe MyProject.uproject \
  -uaip-scenario-file=./scenarios/pie-smoke.json \
  -uaip-response-file=./scenarios/pie-smoke.result.json
```

### SafetyPolicy 系 CLI フラグ

`[UAIP.SafetyPolicy]` の各 bool フラグには対応する `-uaip-policy-*` CLI フラグがあります（ini キー側の説明は [Safety & Capabilities](safety.md#safetypolicy-settings) を参照）：

| ini キー | CLI フラグ |
|---|---|
| `ReadOnly` | `-uaip-policy-read-only` |
| `DisableSave` | `-uaip-policy-disable-save` |
| `AllowLogDump` | `-uaip-policy-allow-log-dump` |
| `AllowContextMenuMutation` | `-uaip-policy-allow-context-menu-mutation` |
| `AllowKeyboardInput` | `-uaip-policy-allow-keyboard-input` |
| `AllowKeyboardModifierInput` | `-uaip-policy-allow-keyboard-modifier-input` |
| `AllowPasswordFieldWrite` | `-uaip-policy-allow-password-field-write` |
| `AllowInputModeBypass` | `-uaip-policy-allow-input-mode-bypass` |
| `DisablePIEStart` | `-uaip-policy-disable-pie-start` |

`AllowCapabilityReload` / `AllowedCapabilities` / `DeniedCapabilities` / `DeniedCommands` / `AllowedArtifactDirectory` は **ini 専用**（CLI フラグなし — Capability の昇格やサンドボックス境界に関わるため、プロセスコマンドラインからの変更を許可しない設計）。

---

## ランタイムオーバーライド機構（パッケージビルド）

パッケージビルド（`!WITH_EDITOR`）では UAIP が初回起動時に `<Project>/Saved/UAIP/UAIPOverride.ini` を自動生成・読み込みします：

```ini
; UAIP Runtime Configuration Override
; Settings placed here override the defaults packaged in Config/DefaultUAIP.ini.
; Call UAIP.Core.ReloadCapabilities to apply AllowedCapabilities changes without restarting.
;
; Example:
;   [UAIP.SafetyPolicy]
;   +AllowedCapabilities=RuntimeExecCommand
```

- ファイルがない場合はコメント付きテンプレートが生成される
- ここに置いたキーは pak 内 `DefaultUAIP.ini` の値の上にマージされる
- ゲームをリビルドせずに実行時挙動を調整するために自由に編集してよい
- `AllowedCapabilities` / `DeniedCapabilities` の変更は `UAIP.Core.ReloadCapabilities` で再起動なしに適用可能（その他のキーは再起動が必要）

このファイルはエディタビルドには存在しません — エディタでは `Config/DefaultUAIP.ini` を直接編集してください。

---

## MCP Bridge `config.json`

MCP Bridge（`<UAIP-parent>/UAIPMCPBridge/` — 通常は `<Project>/Plugins/UAIPMCPBridge/` にデプロイ）経由で接続する場合、追加の JSON 設定レイヤーが適用されます。これは Python プロキシ側が読み込むもので、エディタ側は関与しません。Bridge はドキュメントリポジトリの [Releases](../../../releases) から `UAIP-MCPBridge-<version>.zip` として配布されます。

| キー | 型 | デフォルト | 説明 |
|---|---|---|---|
| `ue_editor_path` | string | — | `UnrealEditor.exe` の絶対パス。環境変数オーバーライド：`UAIP_UE_EDITOR_PATH` |
| `uproject_path` | string | — | `.uproject` ファイルの絶対パス。環境変数オーバーライド：`UAIP_UPROJECT_PATH` |
| `subprocess_timeout_seconds` | int | `300` | UE サブプロセス呼び出しの個別タイムアウト |
| `log_level` | string | `"INFO"` | Python logger の冗長度 — `DEBUG` / `INFO` / `WARNING` / `ERROR` |
| `enable_scenario` | bool | `false` | `true` のとき Bridge がエディタを `-uaip-enable-scenario` 付きで起動する。環境変数オーバーライド：`UAIP_ENABLE_SCENARIO=1` |
| `inline_artifacts.image` | bool | `false` | PNG Artifact を MCP レスポンスに base64 インライン化する。**長時間セッションで PNG が蓄積し `"Could not process image"` API エラーが発生するため、デフォルト OFF** — スクリーンショットは Artifact パスを `Read` ツールに渡して表示する |
| `inline_artifacts.json` | bool | `true` | JSON Artifact を MCP レスポンスに base64 インライン化する |
| `inline_artifacts.text` | bool | `true` | テキスト Artifact を MCP レスポンスに base64 インライン化する |

環境変数が設定されている場合は JSON 値を上書きします。フルコメント付きテンプレートは `config.json.example`（Bridge zip 同梱、インストール後は `<bridge-root>/config.json.example`）を参照してください。

---

## 設定ミスのトラブルシューティング早見表

| 症状 | 最初に確認する設定 |
|---|---|
| `PolicyViolation: Scenario execution is not enabled` | `-uaip-enable-scenario` フラグ（または Bridge の `config.json` の `enable_scenario: true`） |
| HTTP / MCP / WS サーバが起動しない | 対応する `-uaip-<transport>-enable` フラグ未指定 |
| Artifact がディスクに溜まり続ける | `[UAIP.ArtifactGC]` の `Enabled` / `MaxAgeHours` / `MaxSessionCount` |
| 再起動でセッションが消える | `[UAIP.Session].Enabled=True` および `MaxScanFiles` が十分大きいか |
| `"Could not process image"` API エラー | Bridge `config.json` の `inline_artifacts.image` が `true` — `false` に変更 |
| 録画時にエディタのトーストが映り込む | `[UAIP.CommandNotification].Enabled=False` |
| Bearer Token が拒否される | `Saved/UAIP/Auth/http_token.txt`（HTTP）または `ws_token.txt`（WS）と Token 値が一致しているか確認。[Security](security.md) を参照 |
| `CapabilityNotAvailable: <name>` | `[UAIP.SafetyPolicy]` に `+AllowedCapabilities=<name>` を追記して `UAIP.Core.ReloadCapabilities` を実行（または再起動） |

それ以外のケースは [Troubleshooting](troubleshooting.md) を参照。

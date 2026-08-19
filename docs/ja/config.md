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

### `[UAIP.CommandPump]` — モーダル表示中のコマンド実行（既定で無効）

エディタがモーダルダイアログを表示している間、UAIP は通常いっさい応答できません。コマンドはティッカーのコールバック内で実行されており、モーダルはそのティッカーごとゲームスレッドを止めてしまうためです。AI 側からは「エディタが固まった」ようにしか見えません。

この機能を有効にすると、コマンドの実行を受付とは別のタイミング（フレーム終端）へ移し、モーダル表示中でも **状態を読むだけの安全なコマンド** に応答を返せるようになります。エディタを変更するコマンドは失敗せずに順番待ちへ入り、モーダルが閉じた後に実行されます。

> **既定は無効です。** 有効化するとすべてのコマンドの実行タイミングが変わるため、段階的に確認したうえで判断してください。コマンドライン実行（commandlet）では、フレーム終端が回らない構成があるため自動的に無効になります。

| キー | 型 | デフォルト | 説明 |
|---|---|---|---|
| `StarvedTickAllowList` | string | `UAIP.Core.HealthCheck,UAIP.Core.QueryCapabilities` | モーダル表示中に実行してよいコマンドの完全修飾名（カンマ区切り）。ここに無いコマンドは**拒否されず、モーダルが閉じるまで順番待ちのまま**になります |

`StarvedTickAllowList` を既定の 2 件に絞っているのは、モーダルが開いている最中は「他の処理の途中」だからです。`ListCommands` / `DescribeCommand` は読み取り専用ですが、登録済みの全ハンドラへ問い合わせるため、あらゆるドメインのコードをこの状況で動かすことになります。そのため既定には含めていません。

対応する CLI フラグ：`-uaip-command-pump-starved-tick-allow-list=...`

実効値は起動時に解決され、Output Log に 1 行だけ記録されます（`Starved tick allowlist: ...`）。ini に書いたのに効いていない場合や、書式を誤って無視されたエントリがある場合は、**起動直後のログで確認できます**。CVar `uaip.Command.StarvedTickAllowList` を読んでも既定値しか返らない点に注意してください — ini とコマンドラインは CVar を書き換えず、その上に重ねます。

#### コンソール変数

| CVar | デフォルト | 実行中の変更 | 説明 |
|---|---|---|---|
| `uaip.Command.PumpedExecution` | `0` | 可能 | この機能のマスタースイッチ。`1` で有効 |
| `uaip.Command.MaxQueuedCommands` | `32` | 可能 | 順番待ちできるコマンド数の上限。超過分は `TooManyRequests` で断られます（実行されていないので再送は安全）。1 セッションあたりの上限はこの値から導出されます |
| `uaip.Command.MaxCommandsPerDrain` | `8` | 可能 | 1 フレームで実行する最大コマンド数 |
| `uaip.Command.StarvedTickAllowList` | 上表のとおり | **不可** | 読み取り専用。ini またはコマンドラインからのみ設定できます |

`StarvedTickAllowList` を読み取り専用にしているのは、コンソールがまさにこの制限で守ろうとしている経路から到達できるためです。実行中に広げられる防御は防御になりません。

### `[UAIP.Jobs]` — ジョブ型コマンドの 1 フレームあたりの予算

`UAIP.Editor.Assets.StartAssetAudit` はジョブを登録した時点で応答を返し、実際の走査は監査が終わるまでゲームスレッドを占有せず、エディタのフレームの合間で進みます。このキーは、その走査が 1 フレームあたりに使ってよい時間を決めます。

| キー | 型 | デフォルト | 範囲 | 説明 |
|---|---|---|---|---|
| `AuditStepBudgetMs` | float | `10.0` | `[1.0, 100.0]` | 監査ジョブが 1 フレームあたり走査に使ってよいミリ秒数。大きくすると監査は早く終わりますが実行中のエディタは重くなり、小さくするとその逆になります。範囲外の値はエラーにはならず、範囲内へ収められます |

値はモジュール起動時に一度だけ読まれるため、変更はエディタの次回起動時から反映されます。

これは努力目標であり保証ではありません。分割できない処理は予算を超過します — `Preparing` が発行するアセット一覧の取得と、アセット 1 件あたりのディスクサイズ取得がこれに当たります。

CLI フラグ：なし。

### `[UAIP.Session]` — セッション永続化

セッションメタデータ（ID・コマンドログ・キーバリューのコンテキスト）をディスクに永続化し、エディタ再起動を跨いでセッションを復元する機能の設定。セッションの Capability セットはこの対象に含まれません — そもそもセッション側に保存されるものではなく、プロセス全体の Capability セットと（該当すれば）セッションが束縛された役割から都度計算されます（詳細は [Safety & Capabilities → 役割](safety.md#役割layer-15)）。役割の束縛も再起動を跨いでは残りません — 復元されたセッションは未束縛の状態に戻り、有効な役割の資格情報を運ぶ次のリクエストによって改めて束縛される必要があります。そのため、古いセッションがかつて持っていた役割のまま復活することはありません。

| キー | 型 | デフォルト | 範囲 | 説明 |
|---|---|---|---|---|
| `Enabled` | bool | `True` | — | セッション永続化のマスタースイッチ |
| `SubDirectory` | string | `Sessions` | — | Artifact ルート配下のセッション格納サブディレクトリ |
| `MaxCommandLogEntries` | int32 | `100` | `[1, 10000]` | セッションファイルあたりの最大コマンドログ件数 |
| `SessionLifetimeHours` | float | `24.0` | `[1.0, 8760.0]` | アイドル状態とみなされるまでの時間 |
| `MaxAllowedLifetimeHours` | float | `168.0` | `[1.0, 87600.0]` | 更新を含めたセッション総寿命の上限 |
| `MaxScanFiles` | int32 | `1000` | `[1, 100000]` | 起動時にセッションを復元する際にスキャンする最大ファイル数 |

CLI フラグ：`-uaip-session-enabled` / `-uaip-session-sub-directory=...` / `-uaip-session-max-command-log-entries=N` / `-uaip-session-lifetime-hours=N` / `-uaip-session-max-allowed-lifetime-hours=N` / `-uaip-session-max-scan-files=N`

### `[UAIP.Roles]` — 役割による Capability の降格

意図的にここでは詳細を扱いません — 役割は Capability をゲートする仕組み（Layer 1.5）であり安全性に関わる事項のため、完全なリファレンス（ini 書式・セッションが役割へ束縛される仕組み・役割を運べない Transport 向けの opt-in フラグ）は、他の認可レイヤーと合わせて [Safety & Capabilities → 役割](safety.md#役割layer-15) にまとめています。概要だけ述べると、`+Role=(Name="...", DeniedCapabilities=(...))` の行で役割を定義し、`AllowRoleBlindTransports`（ini 専用、既定 `False`）で、役割が 1 つでも定義された後に WS・CLI・FullHTTP を明示的に併用できるようにします。

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

### `[UAIP.Transport]` — 通常起動のエディタで MCP transport を自動起動する

通常の手順で起動したエディタ（Epic Games Launcher・`.uproject` のダブルクリック・IDE のデバッグ実行など、`-uaip-mcp-enable` / `-uaip-http-enable` を指定していない起動）が、自ら MCP 接続を受け付ける状態になれるようにします。これにより、ゲストモードで設定した Bridge が後から接続できる相手が用意されます。一連の流れは [接続方法 → ゲストモード接続](connections.md#ゲストモード接続) を参照してください。

| キー | 型 | デフォルト | 範囲 | 説明 |
|---|---|---|---|---|
| `AutoStartMCP` | bool | `False` | — | マスタースイッチ。`True` のとき、エディタは `OnPostEngineInit` で **MCPOnly モード**として transport を起動します。この方法で FullHTTP を自動起動する ini キーはありません |
| `AutoStartPort` | int32 | `0` | `[0, 65535]` | 最初に試すポート。`0` は transport の組み込み既定ポート（`8765`）を意味します |
| `AutoStartPortScanCount` | int32 | `8` | `[1, 64]` | `AutoStartPort` から何個連続したポートを試すか |

CLI フラグ（ini を編集せずに 1 回だけ試すための alias）：`-uaip-auto-start-mcp` / `-uaip-auto-start-port=N` / `-uaip-auto-start-port-scan-count=N`

範囲外の値は**丸められません** — 起動時に Warning を出したうえで既定値のまま動作します（UAIP が読む他の範囲付き ini キーと同じ「警告して変更しない」挙動です）。コマンドラインに `-uaip-mcp-enable` または `-uaip-http-enable` が指定されている場合、このセクションはそもそも読まれません — 明示フラグは常に自動起動より優先されます。

このセクションはデモビルドでは読まれません。デモは以前からこのセクションの設定に関係なく MCPOnly として無条件に起動します。

> **セキュリティ上の注意**: `Config/DefaultUAIP.ini` はバージョン管理対象で、エディタには per-user のオーバーライド層がありません。`AutoStartMCP=True` をそこで有効化すると、そのプロジェクトを開く全開発者が通常起動のたびに接続を受け付ける MCP エンドポイントを持つことになり、個人単位で打ち消す方法もありません — [Security → 運用上のセキュリティ注意点](security.md#運用上のセキュリティ注意点) を参照。

#### 接続情報の記述子ファイル

HTTP transport が実際に起動すると（`AutoStartMCP` 経由でも、`-uaip-mcp-enable` / `-uaip-http-enable` 経由でも）、`<Project>/Saved/UAIP/EditorEndpoint.json` を書き出します：

```json
{
  "Port": 8765,
  "Mode": "MCPOnly",
  "ProjectFilePath": "F:/MyProjects/MyGame/MyGame.uproject"
}
```

- リスナーが実際に bind された時点で原子的に（一時ファイル + リネームで）書き出され、正常終了時に削除されます
- 読み取り時は 1024 バイトの上限があり、超えるものは解析せず無視されます
- **権限判断の入力には一切なりません。** ゲスト接続候補にどのポートを試すかを伝えるだけのヒントであり、役割名・認証トークン・プロセス ID は含みません。読み手は、そのポートを目的のエディタとして扱う前に、既存の `HealthCheck` によるプロジェクト同一性検証を必ず通す必要があります
- エディタが異常終了すると、古い記述子が残ることがあります。読み手はそれを見つけても信用する前にポートへ probe し、待ち受けていなければ設定に書かれたポートへフォールバックします

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
| `-uaip-http-enable` | HTTP API モード（FullHTTP）を有効化。ループバック（`127.0.0.1:<port>`）にバインドし `/uaip/*` + `/mcp` を公開。`-uaip-http-no-auth` がない限り Bearer Token 必須 — [Security → ネットワーク面](security.md#ネットワーク面) を参照 |
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
| `AllowCheatCVarWrite` | `-uaip-policy-allow-cheat-cvar-write` |
| `AllowExternalTraceAnalysis` | `-uaip-policy-allow-external-trace-analysis` |
| `AllowDisclosingTraceAttachment` | `-uaip-policy-allow-disclosing-trace-attachment` |

`AllowCapabilityReload` / `AllowedCapabilities` / `DeniedCapabilities` / `DeniedCommands` / `AllowedArtifactDirectory` / `ExternalTraceDirectory` は **ini 専用**（CLI フラグなし — Capability の昇格やサンドボックス境界に関わるため、プロセスコマンドラインからの変更を許可しない設計）。

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
| `editor_path` | string | `""` | `UnrealEditor.exe` の絶対パス。環境変数 `UAIP_UE_EDITOR_PATH` が設定されている場合はそちらが優先。**`attach_only` が `true` のときは不要** — ゲストモードの Bridge はエディタを一切起動しないため、指す先が無い |
| `uproject_path` | string | `""` | `.uproject` ファイルの絶対パス。環境変数 `UAIP_UPROJECT_PATH` が設定されている場合はそちらが優先。**どのモードでも常に必須** — プロジェクト同一性検証・認証トークンの解決・crash marker のパス・接続情報記述子の解決に使われる |
| `attach_only` | bool | `false` | ゲストモード。`true` のとき、Bridge は自分ではエディタを一切起動せず、既に待ち受けているエディタへアタッチするだけになる。ポートは[接続情報の記述子ファイル](config.md#接続情報の記述子ファイル)から解決し、見つからなければ `http_port` へフォールバックする。アタッチ中のエディタとの接続が切れても（ヘルスチェック失敗・config リロードのいずれでも）代わりのエディタを起動しない。詳細は [接続方法 → ゲストモード接続](connections.md#ゲストモード接続) を参照。環境変数オーバーライド：`UAIP_ATTACH_ONLY`（`1` / `true` / `yes`） |
| `http_port` | int | `8765` | エディタ側 MCP エンドポイントの HTTP ポート。`-uaip-http-port` と一致させること |
| `http_startup_timeout_seconds` | int | `120` | Bridge が起動後のエディタ準備完了を待つ最大秒数 |
| `command_timeout_seconds` | int | `180` | 転送されるコマンドのリクエストごとの HTTP タイムアウト。**HTTP トランスポート自身の非同期コマンドタイムアウト（120 秒）より小さい値には設定できない** — 詳細は下記「タイムアウトの不変条件」を参照 |
| `unresponsive_timeout_seconds` | int | `30` | ポートは LISTEN しているがヘルス ping に応答しない状態を何秒許容してから `UNRESPONSIVE` と判定するか。この状態では自動起動も自動再起動も行わない — [接続方法 → エディタ状態の確認](connections.md#エディタ状態の確認uaip_get_editor_status) を参照 |
| `health_poll_interval_seconds` | int | `15` | エディタが稼働中とみなされている間のバックグラウンドヘルス ping の間隔 |
| `handshake_timeout_seconds` | int | `10` | プロジェクト同一性検証に使う `HealthCheck` 呼び出し、および config リロード時に発行される `ShutdownEditor` 呼び出しのタイムアウト |
| `scenario_timeout_seconds` | int | `1800` | Bridge 経由で転送される `uaip_run_scenario` の wall-clock 上限（scenario ルート自体の 30 分制限に合わせている） |
| `artifact_timeout_seconds` | int | `60` | Artifact ダウンロードのタイムアウト。コマンド実行時間とは独立に管理される |
| `probe_tcp_timeout_seconds` | float | `1.0` | エディタのポートが LISTEN しているかどうかだけを確認する TCP connect タイムアウト |
| `probe_ping_timeout_seconds` | float | `5.0` | LISTEN 中のエディタが実際に応答するかを確認する HTTP ping タイムアウト |
| `process_exit_wait_seconds` | int | `10` | Bridge が起動したエディタプロセスの終了を待つ最大秒数 |
| `allow_unverified_attach` | bool | `false` | `HealthCheck` 応答に `ProjectFilePath` を持たない旧バージョンのプラグインへアタッチすることを許可するオプトイン。**既定では拒否**される — 同一性を検証できないピアは黙ってアタッチせず拒否するのが既定の挙動 |
| `log_level` | string | `"INFO"` | Python logger の冗長度 — `DEBUG` / `INFO` / `WARNING` / `ERROR` |
| `enable_scenario` | bool | `false` | `true` のとき Bridge がエディタを `-uaip-enable-scenario` 付きで起動する。環境変数オーバーライド：`UAIP_ENABLE_SCENARIO=1` |
| `role_name` | string | `""` | エディタの `[UAIP.Roles]` が役割を 1 つ以上定義している場合のみ必要。この Bridge が認証する役割名を指定する。対応するトークンは `Saved/UAIP/Roles/<role_name>.token` から**遅延読み込み**される — 一定周期ではなく、リクエストが `401` で返ってきたときにだけ読み直す。環境変数オーバーライド：`UAIP_ROLE_NAME` |
| `role_token` | string | `""` | 役割の Bearer Token 値を直接指定し、`role_token_file` の読み込みを完全にバイパスする。トークンをシークレット管理ツールなど別の方法で払い出している場合に使う。設定されていれば `role_name` によるファイル参照より優先される。環境変数オーバーライド：`UAIP_ROLE_TOKEN`。`role_name` と `role_token` を両方とも空のままにすると、役割機能が存在しなかった場合と全く同じリクエストが送信される — 詳細は [Safety & Capabilities → 役割](safety.md#役割layer-15) を参照 |
| `inline_artifacts.image` | bool | `false` | PNG Artifact を MCP レスポンスに base64 インライン化する。**長時間セッションで PNG が蓄積し `"Could not process image"` API エラーが発生するため、デフォルト OFF** — スクリーンショットは Artifact パスを `Read` ツールに渡して表示する |
| `inline_artifacts.json` | bool | `true` | JSON Artifact を MCP レスポンスに base64 インライン化する |
| `inline_artifacts.text` | bool | `true` | テキスト Artifact を MCP レスポンスに base64 インライン化する |

環境変数（`UAIP_UE_EDITOR_PATH`・`UAIP_UPROJECT_PATH`・`UAIP_ENABLE_SCENARIO`・`UAIP_ROLE_NAME`・`UAIP_ROLE_TOKEN`）が設定されている場合は対応する JSON 値を上書きします。フルコメント付きテンプレートは `config.json.example`（Bridge zip 同梱、インストール後は `<bridge-root>/config.json.example`）を参照してください。

### タイムアウトの不変条件

Bridge はタイムアウト設定を検証し、どの不変条件が破られたかによって異なる挙動を取ります。

- `health_poll_interval_seconds` < `unresponsive_timeout_seconds` < `command_timeout_seconds`、かつ `unresponsive_timeout_seconds` < `http_startup_timeout_seconds`。この 4 値は**ひとまとまりのプロファイル**として扱われ、いずれか 1 つの比較でも破られると **4 値すべて**が既定値へ戻される（Bridge のログに警告が出力される）。中途半端なプロファイルのまま起動することはない。
- `handshake_timeout_seconds` < `command_timeout_seconds` は独立して検証され、違反時は `handshake_timeout_seconds` のみが既定値へ戻される。
- `TransportTimeouts.HTTP`（エディタ自身の非同期コマンドタイムアウト。既定 `120`）`<` `command_timeout_seconds` は、ハードコードされた定数ではなく**起動/アタッチ直後にエディタの `HealthCheck` 応答から取得した実値**に対して検証される。違反時は警告ログのみで、起動をブロックしたり値をリセットしたりはしない（このチェックが走る時点でエディタプロセスは既に生きているため）。`command_timeout_seconds` をエディタの実際の非同期タイムアウトより小さく設定すると、エディタ側ではまだ実行を継続してよいコマンドを Bridge 側が先に諦めてしまうことになる。詳細は [接続方法 → 長時間コマンドと 120 秒の非同期タイムアウト](connections.md#長時間コマンドと-120-秒の非同期タイムアウト) を参照。

`inflight_suppression_max_seconds` という独立キーは存在しない。`scenario_timeout_seconds + 60` の導出値であり、境界で scenario ルート自体のタイムアウトとレースしないようにするための設計。

### 実行時の config リロード（`uaip_reload_config`）

`uaip_reload_config` を使うと、**MCP クライアントを再起動せずに** config の変更を適用できます。`config.json` を読み直し、起動パラメータが現セッションと異なる場合は実行中のエディタをシャットダウンして次回ツール呼び出し時に再起動をスケジュールします。

```
uaip_reload_config()
→ { "EditorRestartScheduled": true/false, "EditorPath": "...", ... }
```

**オプション引数**（セッション限りのオーバーライド。`config.json` には書き込まれない）:

| 引数 | 効果 |
|---|---|
| `EditorPath` | `config.json` を編集せずに実行時でエンジンバージョンを切り替える |
| `UProjectPath` | このセッション限り別の `.uproject` を使用する |

`config.json` 編集後の典型的な手順：

1. `config.json` を編集（例：`enable_scenario: true`）
2. `uaip_reload_config()` を呼び出す — Bridge が変更を検出してエディタ再起動をスケジュール
3. 次の `uaip_execute` 呼び出し時に新しいパラメータでエディタが起動する

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

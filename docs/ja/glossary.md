**[English](../en/glossary.md)** | [概要に戻る](overview.md)

# 用語集

UAIP のドキュメントで繰り返し登場する用語の定義です。アルファベット順に並べています。

---

### Artifact（アーティファクト）
コマンドが生成するファイルのことです（PNG スクリーンショット、JSON ダンプ、テキストログ、レポートバンドルなど）。レスポンスにはファイルパスではなく ID（`ArtifactId`）が含まれ、`Saved/UAIP/<SessionId>/` 配下に保存されます。詳細は [Artifacts](artifacts.md) を参照してください。

### Bearer Token
HTTP / WebSocket リクエストの認証に使う、32 文字のランダムな文字列です。エディタ起動時に生成され、`Saved/UAIP/EditorHttpAuthToken.txt` と `EditorWsAuthToken.txt` に書き出されます。HTTP は `Authorization: Bearer <token>` ヘッダで、WebSocket は最初のハンドシェイクフレームで渡します。詳細は [接続方法](connections.md) を参照してください。

### Capability
コマンド単位・セッション単位の認可タグのことです（例：`BlueprintEdit`、`PIEControl`）。各コマンドハンドラは必要な Capability を宣言しており、セッションがそれらをすべて所有しているときだけコマンドを実行できます。Capability には 2 種類あります — **DefaultAllow**（自動付与）と **DefaultDenied**（`Config/DefaultUAIP.ini` で明示的に有効化が必要）。詳細は [Safety & Capabilities](safety.md) を参照してください。

### Capability Set
セッションが所有する Capability の集合のことです。セッション生成時に、プロジェクトの SafetyPolicy をもとに決まります。`UAIP.Core.QueryCapabilities` で問い合わせ可能です。

### CommandDispatcher
`CommandRequest` を受け取り、Capability と Policy をチェックし、ハンドラを解決してゲームスレッドで実行し、`CommandResponse` を返す Core コンポーネントです。4 つのトランスポートとシナリオルートが共通して使います。

### CommandRegistry
完全修飾コマンド名（例：`UAIP.Editor.Blueprint.CompileBlueprint`）と実装ハンドラを対応付ける Core コンポーネントです。モジュールの起動時に登録され、`uaip_list_commands` / `uaip_describe_command` から問い合わせできます。

### DefaultAllow / DefaultDenied
Capability の 2 つのクラスを指します。**DefaultAllow** は新規セッションに自動で付与されます（例：`EditorInspect`、`PIEControl`）。**DefaultDenied** は `Config/DefaultUAIP.ini` に `+AllowedCapabilities=<名前>` を明示的に書く必要があります。この区別はおおまかに「読み取り」と「書き込み」の境界に対応しています。

### Demo / Pro（デモ版 / 製品版）
UAIP には 2 つの配布形式があります。**デモ版** は GitHub Releases で配布している無償の機能制限版です（MCP トランスポートのみ、観測 / PIE / アサート / UI 自動化、キャプチャに透かしあり）。**製品版** は Fab で公開している完全版です（全トランスポート、Editor と Runtime の完全な編集機能、透かしなし、[Fab で公開中](https://www.fab.com/listings/0eedf909-00ac-4d95-b109-8fda51800fff)）。詳細は [デモ版ガイド](demo.md) を参照してください。

### ErrorCode
失敗時のレスポンスに含まれる、機械可読なエラーカテゴリです（`CommandNotFound`・`CapabilityNotAvailable`・`PolicyViolation`・`InvalidParams`・`NotFound`・`ExecutionFailed`・`NotAllowed`・`Timeout`・`TooManyRequests`・`InternalError`）。人間向けの詳細は `ErrorMessage` フィールドに入ります。詳細は [トラブルシューティング](troubleshooting.md) を参照してください。

### Fully-Qualified Command Name（完全修飾コマンド名）
コマンドを呼び出すときに使う、ドット区切りの完全な名前です（例：`UAIP.Editor.Observation.CaptureActiveWindowImage`）。短縮名（`CaptureActiveWindowImage` だけなど）は `CommandNotFound` を返します。先頭セグメントは `UAIP`、`Toolset`、またはプロジェクト独自のプレフィックスのいずれかになります。

### Handler（ハンドラ）
1 つのコマンドを実装する C++ クラスのことです（例：`FCaptureActiveWindowImageHandler`）。起動時に親モジュールが `CommandRegistry` に登録し、対応する `UAIPEditor*` / `UAIPRuntime*` モジュール内に置かれます。

### MCP（Model Context Protocol）
AI クライアント（Claude Code・Codex CLI・Cursor・Windsurf・Copilot など）がツールを発見・呼び出しするときに使うオープンプロトコルです。UAIP は **MCP Bridge**（`thin_proxy.py`）を介して MCP サーバとして自身を公開します。詳細は [接続方法](connections.md) を参照してください。

### MCP Bridge
AI クライアントと UE Editor をつなぐ薄い Python プロキシ（`Plugins/UAIPMCPBridge/thin_proxy.py`）です。MCP のツール呼び出しを内部で UAIP の HTTP リクエストに変換し、エディタのライフサイクル（自動起動、クラッシュやハングからの復旧）も管理します。Artifact のインライン化処理もここで行います。プラグイン本体とは別配布で、ドキュメントリポジトリの [Releases](https://github.com/Naotsun19B/UnrealAIIntegrationPlatform-Document/releases?q=MCPBridge)（`MCPBridge-v<X.Y.Z>` タグ）から `UAIP-MCPBridge-<version>.zip` として提供されます。

### Operational Constraints
`UAIP.Core.QueryCapabilities` が返す SafetyPolicy フラグのスナップショットです。AI が事前に「この操作が許可されるか」を判断するために使います（例：`ReadOnly=True` ならすべての書き込みが失敗することが事前にわかる）。

### PIE（Play in Editor）
エディタ内でゲームを実行する UE のモードです。UAIP は `UAIP.Runtime.PIE.*` で start / stop / pause / resume / map-load を公開しており、PIE 実行中には Runtime の観測・アサート・入力コマンドも利用できます。

### Provider
関連するコマンドをまとめる名前空間のことです（例：`UAIP.Editor.Observation`、`Toolset.AnimationAssistant`）。各 Provider は起動時にモジュールが登録します。`uaip_list_commands` を `ProviderPrefix` でフィルタすれば、特定 Provider のコマンドだけを列挙できます。

### SafetyPolicy
プロセス全体に適用される設定です（`Config/DefaultUAIP.ini` の `[UAIP.SafetyPolicy]` セクション）。Capability セットの内容に関係なく、カテゴリ全体の操作をゲートできます — Read-Only モード、ログダンプ許可、キーボード入力許可、シナリオ opt-in などです。AI が Runtime で SafetyPolicy を解除することはできず、変更できるのはオペレーターだけです（通常はエディタの再起動も必要）。詳細は [Safety & Capabilities](safety.md) を参照してください。

### Scenario（シナリオ）
順序付きのコマンドリストを 1 リクエストで送信する仕組みのことです（`uaip_run_scenario`、`POST /uaip/scenarios`、WebSocket の `ScenarioRequest` フレーム、CLI の `-uaip-scenario-file=…` フラグから利用可能）。ステップごとの `AbortOnFailure`・`RetryCount`・`TimeoutSeconds`、および前ステップの出力を後ステップに渡すテンプレート式（`${StepName.Data.x}`）に対応しています。詳細は [シナリオ実行](scenario.md) を参照してください。

### Session（セッション）
サーバ側のタスク単位のスコープです。Capability セット・Artifact のサブフォルダ（`Saved/UAIP/<SessionId>/`）・Widget 観測キャッシュ・レートリミタを所有します。新しい `SessionId` を使った最初のリクエストで作成され、`EndSession` または TTL 切れで GC されます。論理的なタスクごとに新しい `SessionId` を使うと、Artifact が整理しやすくなります。

### Stability（安定性）
各コマンドに付く記述子（`Stable`・`Experimental`・`Deprecated`）で、`uaip_describe_command` の結果に含まれます。Experimental は予告なしに変更される可能性があり、Deprecated には代替コマンドを示す `MigrationTarget` フィールドが付きます。

### Toolset / Toolset Bridge
**Toolset** は UE 5.8 のファーストパーティ Toolset フレームワークのことで、一部のプラグインが公開する独立したエンジン側サーフェスです。**Toolset bridge** コマンド（UAIP コマンドのうち `Toolset.*` プレフィックスを持つもの）は、その面を UAIP のリクエスト / レスポンス形式に適応するものです。ほとんどの場合、対応する UAIP ネイティブコマンドと同等の機能を提供します。UE 5.8 以降と、該当する Toolset プラグイン（`NiagaraToolsets`・`PhysicsToolsets`・`AnimationAssistantToolset` など）の導入が必要です。

### Transport（トランスポート）
外部クライアントと UAIP Core の間の通信経路のことです。次の 4 種類があります — **MCP**（Bridge 経由）・**HTTP**・**WebSocket**・**CLI**。4 つすべてが同じ `CommandDispatcher` に到達するため、Capability と Policy の判定はトランスポートに関係なく同一です。詳細は [接続方法](connections.md) を参照してください。

### UAIP
**Unreal AI Integration Platform** の略称で、本リポジトリで扱っているプラグインそのものを指します。

### Watermark（透かし）
デモバイナリがキャプチャ出力（`CaptureActiveWindowImage`・`CaptureEditorTabImage`・`CaptureGraphViewportImage`・`CaptureViewportImage`）に重ねる `UAIP Demo` の表示です。レビューやテストの証跡として共有された画像が、デモ版で取得されたものだと分かるようにするために入れています。製品版では入りません。

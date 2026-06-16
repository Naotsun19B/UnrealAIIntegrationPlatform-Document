**[English](../en/glossary.md)** | [概要に戻る](overview.md)

# 用語集

UAIP ドキュメントで頻出する用語の定義です。アルファベット順。

---

### Artifact（アーティファクト）
コマンドが生成するファイル（PNG スクリーンショット・JSON ダンプ・テキストログ・レポートバンドル）。パスではなく ID 参照（`ArtifactId`）で返却。`Saved/UAIP/<SessionId>/` 配下に保存。詳細は [Artifacts](artifacts.md)。

### Bearer Token
HTTP / WebSocket リクエスト認証用に UAIP が起動時に生成・書き出す 32 文字のランダムトークン。`Saved/UAIP/EditorHttpAuthToken.txt` および `EditorWsAuthToken.txt` に保存。HTTP は `Authorization: Bearer <token>` ヘッダ、WebSocket は最初のハンドシェイクフレームで渡す。詳細は [接続方法](connections.md)。

### Capability
コマンド毎・セッション毎の認可タグ（例：`BlueprintEdit`、`PIEControl`）。各コマンドハンドラは必要 Capability を宣言し、セッションが必要 Capability すべてを所有する場合のみ実行可能。2 種類：**DefaultAllow**（自動付与）と **DefaultDenied**（`Config/DefaultUAIP.ini` で明示的に有効化が必要）。詳細は [Safety & Capabilities](safety.md)。

### Capability Set
セッションが所有する Capability のコレクション。spawn 時にプロジェクトの SafetyPolicy から計算。`UAIP.Core.QueryCapabilities` で問い合わせ可能。

### CommandDispatcher
`CommandRequest` を受け取り、Capability + Policy をチェックし、ハンドラを解決し、ゲームスレッドで実行し、`CommandResponse` を返す Core コンポーネント。4 transport すべてとシナリオルートが共用。

### CommandRegistry
完全修飾コマンド名（例：`UAIP.Editor.Blueprint.CompileBlueprint`）を実装ハンドラにマップする Core コンポーネント。モジュール起動時に登録。`uaip_list_commands` / `uaip_describe_command` で問い合わせ。

### DefaultAllow / DefaultDenied
Capability の 2 クラス。**DefaultAllow** は新規セッションに自動付与（例：`EditorInspect`、`PIEControl`）。**DefaultDenied** は `Config/DefaultUAIP.ini` に `+AllowedCapabilities=<名前>` を明示的に追加する必要があります。この区別はおおよそ「読み取り vs 書き込み」に対応。

### Demo / Pro（デモ版 / Pro 版）
UAIP の 2 つの配布チャネル。**デモ版** は GitHub Releases で配布する無償・機能制限版（MCP transport のみ、観測 + PIE + アサート + UI 自動化、キャプチャに透かし）。**Pro 版** は [Fab](https://www.fab.com) で配布する完全版（全 transport、完全な Editor + Runtime 編集、透かしなし）。詳細は [デモ版ガイド](demo.md)。

### ErrorCode
失敗レスポンス内の機械可読エラーカテゴリ（`CommandNotFound`・`CapabilityNotAvailable`・`PolicyViolation`・`InvalidParams`・`NotFound`・`ExecutionFailed`・`NotAllowed`・`Timeout`・`TooManyRequests`・`InternalError`）。`ErrorMessage` フィールドに人間可読な詳細が入る。詳細は [トラブルシューティング](troubleshooting.md)。

### Fully-Qualified Command Name（完全修飾コマンド名）
コマンド呼び出しに使うドット区切りの完全名（例：`UAIP.Editor.Observation.CaptureActiveWindowImage`）。短縮名（`CaptureActiveWindowImage` 単独）は `CommandNotFound` を返す。最初のセグメントは `UAIP`・`Toolset`・またはプロジェクト定義のプレフィックス。

### Handler（ハンドラ）
1 つのコマンドを実装する C++ クラス（例：`FCaptureActiveWindowImageHandler`）。起動時に親モジュールが `CommandRegistry` に登録。対応する `UAIPEditor*` / `UAIPRuntime*` モジュール内に配置。

### MCP（Model Context Protocol）
AI クライアント（Claude Code・Cursor・Windsurf・Copilot）がツール発見・呼び出しに使うオープンプロトコル。UAIP は **MCP Bridge**（`thin_proxy.py`）経由で MCP サーバとして自身を公開。詳細は [接続方法](connections.md)。

### MCP Bridge
AI クライアントと UE Editor をつなぐ薄い Python プロキシ（`Scripts/MCPBridge/thin_proxy.py`）。MCP ツール呼び出しを内部で UAIP HTTP リクエストに変換し、エディタライフサイクル（自動起動・クラッシュ / ハング復旧）を管理し、artifact のインライン化を処理。

### Operational Constraints
`UAIP.Core.QueryCapabilities` が返す SafetyPolicy フラグのスナップショット — AI が事前に「特定アクションが許可されるか」（例：`ReadOnly=True` ならすべての書き込みが失敗する）を知るために使用。

### PIE（Play in Editor）
エディタ内でゲームを実行する UE のモード。UAIP は `UAIP.Runtime.PIE.*` で start / stop / pause / resume / map-load を、PIE 中に Runtime 観測 / アサート / 入力コマンドを公開。

### Provider
関連コマンドをまとめる名前空間（例：`UAIP.Editor.Observation`、`Toolset.AnimationAssistant`）。各 Provider はモジュールが起動時に登録。`uaip_list_commands` を `ProviderPrefix` でフィルタすると 1 つの Provider のコマンドを列挙可能。

### SafetyPolicy
プロセス全体に適用される設定（`Config/DefaultUAIP.ini` の `[UAIP.SafetyPolicy]` セクション）で、Capability セットに関係なくカテゴリ全体の操作をゲート — Read-Only モード・ログダンプ許可・キーボード入力許可・シナリオ opt-in 等。AI は Runtime で SafetyPolicy を解除できない。オペレーターのみが変更可能（通常はエディタ再起動も必要）。詳細は [Safety & Capabilities](safety.md)。

### Scenario（シナリオ）
`uaip_run_scenario`・`POST /uaip/scenarios`・WebSocket の `ScenarioRequest` フレーム・`-uaip-scenario-file=…` CLI フラグで 1 リクエストとして送信される、順序付きコマンドリスト。ステップ毎の `AbortOnFailure`・`RetryCount`・`TimeoutSeconds`、および前ステップの出力を後ステップにパイプするテンプレート式（`${StepName.Data.x}`）をサポート。詳細は [シナリオ実行](scenario.md)。

### Session（セッション）
サーバ側のタスク単位スコープ。Capability セット・artifact サブフォルダ（`Saved/UAIP/<SessionId>/`）・Widget 観測キャッシュ・レートリミタを所有。新しい `SessionId` での最初のリクエストで作成。`EndSession` または TTL 切れで GC。論理タスク毎に新しい `SessionId` を使うと artifact が整理されやすい。

### Stability（安定性）
各コマンドの記述子（`Stable`・`Experimental`・`Deprecated`）で、`uaip_describe_command` が返却。Experimental コマンドは予告なく変わる可能性あり。Deprecated コマンドには代替を示す `MigrationTarget` フィールドが付く。

### Toolset / Toolset Bridge
**Toolset** は UE 5.8 のファーストパーティ Toolset フレームワーク — 一部のプラグインが公開する別のエンジン側サーフェス。**Toolset bridge** コマンド（`Toolset.*` プレフィックス付きの UAIP コマンド）はその面を UAIP のリクエスト / レスポンス形式に適応し、ほとんどの場合対応する UAIP ネイティブコマンドをミラーします。UE 5.8+ と該当 Toolset プラグイン（例：`NiagaraToolsets`・`PhysicsToolsets`・`AnimationAssistantToolset`）が必要。

### Transport（トランスポート）
外部クライアントと UAIP Core の間の通信チャネル。4 種類：**MCP**（Bridge 経由）・**HTTP**・**WebSocket**・**CLI**。4 つすべてが同じ `CommandDispatcher` にフィードし、Capability + Policy 判定は transport に関わらず同一。詳細は [接続方法](connections.md)。

### UAIP
**Unreal AI Integration Platform** — 本リポジトリで文書化しているプラグイン。

### Watermark（透かし）
デモバイナリがキャプチャ出力（`CaptureActiveWindowImage`・`CaptureEditorTabImage`・`CaptureGraphViewportImage`・`CaptureViewportImage`）の右下にアルファブレンドで合成する `UAIP Demo` テキスト + プラグインアイコンバナー。DLL にコンパイル済み、ファイル差し替えで除去不可。フェイルクローズ：透かし合成失敗時は `ExecutionFailed` を返す。

**[English](../en/faq.md)** | [概要に戻る](overview.md)

# FAQ

## 全般

### UAIP は何をするためのプラグインですか？

AI エージェントから UE Editor と Runtime を操作・観測・検証するための共通基盤です。座標クリックや UI 内部のスクリプティングといった壊れやすい手段を使わずに、構造化された Capability ゲートつきの API でやり取りできるようにします。

### どんな人が使いますか？

- **AI を主軸に開発する人** — Claude Code / Codex CLI / Cursor / Windsurf / Copilot 上のセッションから、実際にエディタを動かしたい（アセットを開く、Blueprint を編集する、PIE を実行する、スクリーンショットを撮る、など）
- **QA・テスト自動化エンジニア** — LLM ベースのスモークテストや PIE アサーション、キャプチャによるリグレッション証跡をすべて手書きせずに用意したい
- **ツールプログラマー** — UE エディタのメニューをリバースエンジニアリングするのではなく、安定したコマンドの上にワークフローを構築したい

### UE 標準の Python スクリプトとは何が違うのですか？

Python は自動化の手法のひとつにすぎません。UAIP は **意味レベルのコマンド** を、宣言済みのパラメータスキーマ・必要な Capability・統一された Artifact 出力とセットで、MCP・HTTP・WebSocket・CLI の 4 つのトランスポートから公開します。Python スクリプト（`RunEditorPythonScript`）も使えますが、Capability や Policy のレイヤーをバイパスしてしまうため、登録済みコマンドでまかなえないケースに限定して使うのが原則です。

### デモ版に期間制限はありますか？

ありません。デモ版は **機能だけが制限されたバージョン**（Editor 編集不可、HTTP / WS / CLI 不可、キャプチャに透かしが入る）であって、期間制限はないので無期限に使えます。

---

## デモ版と製品版

### どちらから始めるべきですか？

まずは **デモ版** から始めるのがおすすめです。観測・PIE 制御・シナリオ・UI 自動化・アサーションを一通りカバーしており、UAIP の統合モデルが自分のワークフローに合うかを評価するには十分です。

以下が必要になった時点で **製品版** に移行してください — Editor 編集（Blueprint・Level・Asset・Material 等）、Runtime ワールド編集（Spawn・GAS・Input 注入 等）、HTTP / WebSocket / CLI トランスポート、Python スクリプト実行。

機能比較の詳細は [デモ版ガイド](demo.md) を参照してください。

### 1 つのプロジェクトでデモ版と製品版を併用できますか？

できません。同じプラグインパスを共有するため、片方をもう片方に置き換える形になります。両者の違いは実質的に `DefaultUAIP.ini` の Capability セットだけです。

### なぜデモ版のキャプチャに透かしが入るのですか？

デモ版を製品版と区別し、デモ版で取得したスクリーンショットがそうと分かるようにするためです。レビューやテストの証跡として外部に共有されるケースを想定し、出所が明確になるようにしています。製品版では透かしは入りません。

---

## セットアップと接続

### Bridge は呼び出しの間もエディタを起動したままにしますか？

はい。MCP Bridge は最初の呼び出しでエディタを起動し、その後は接続を維持し続けます。クラッシュやハングを検出すると自動的に再起動も行います（60 秒間に最大 3 回まで、それを超えた場合は AI 側にエラーが返ります）。エディタのライフサイクルを手動で管理する必要はありません。詳細は [usage.md §2](../../README.md#エディタライフサイクル) を参照してください。

### デモ版で `-uaip-http-enable` が効かないのはなぜですか？

デモバイナリは **MCP 専用** だからです。HTTP / WebSocket / CLI のフラグはすべて無視されます。これはフラグハンドラを削除しているわけではなく、モジュールのロード時点でブロックしています。製品版を使えばこの制限は外れます。

### macOS / Linux でも動きますか？

UAIP v1.0 は **Windows（Win64）のみ対応** です。`.uplugin` の `PlatformAllowList` も `Win64` 固定です。macOS / Linux 対応はロードマップ上で将来検討項目としていますが、優先度は低く、特に Linux のほうがさらに後の検討になります。

### 認証はどう設定しますか？

- **MCP**：認証なし（Bridge はローカル実行のため）
- **HTTP / WebSocket（製品版）**：起動時に 32 文字の Bearer トークンが生成されて `Saved/UAIP/EditorHttpAuthToken.txt` および `EditorWsAuthToken.txt` に書き出されます。HTTP は `Authorization` ヘッダ、WebSocket は最初のフレームで渡してください。開発時のみ `-uaip-http-no-auth` / `-uaip-ws-no-auth` で無効化できます。接続は設計上 localhost に限定されています

---

## Capability と安全性

### `AddBlueprintVariable` が `CapabilityNotAvailable` で返ってきます

編集系の Capability（`BlueprintEdit`・`BlueprintVariableEdit` など）は **DefaultDenied** です。`Config/DefaultUAIP.ini` に以下のように追加してください：

```ini
[UAIP.SafetyPolicy]
+AllowedCapabilities=BlueprintEdit
+AllowedCapabilities=BlueprintVariableEdit
+AllowedCapabilities=BlueprintGraphEdit
```

そのうえでエディタを再起動するか、`AllowCapabilityReload=True` が設定されていれば `UAIP.Core.ReloadCapabilities` を呼び出してください。

### Capability と SafetyPolicy はどう違いますか？

- **Capability** はコマンド単位・セッション単位の認可です（例：このセッションは Blueprint を編集してよい）。
- **SafetyPolicy** はプロセス全体に適用されるゲートで、Capability の有無に関係なくカテゴリ全体を禁止できます（例：Read-Only モードはすべての書き込みを拒否）。SafetyPolicy はオペレーターが設定するもので、AI 側が Runtime で解除することはできません。

詳細は [Safety & Capabilities](safety.md) を参照してください。

### `EditorKeyboardInput` を有効にしたのに `PressKey` が拒否されます

`PressKey` には SafetyPolicy 側のフラグ `AllowKeyboardInput=True` も必要です（プロセスレベルで deny-by-default）。修飾キー（Ctrl / Alt / Shift / Cmd）まで使う場合は、さらに `AllowKeyboardModifierInput=True` も必要です。Capability は「どのセッションがその要求を出せるか」、SafetyPolicy は「そもそも要求を受け付けるかどうか」を制御していると考えてください。

### AI に対して実質的に Read-Only として運用できますか？

できます。`[UAIP.SafetyPolicy]` に `ReadOnly=True` を設定すれば、Capability セットに関係なくすべての変更系コマンドが `PolicyViolation` を返すようになります。評価環境やサンドボックスとして使う場合に有効です。

---

## ワークフロー

### `uaip_execute` を繰り返すべきか、シナリオを組むべきか？

ひとつの論理的なタスクのために `uaip_execute` を 2 回以上呼ぶようなら、`uaip_run_scenario` への切り替えを検討してください。シナリオの利点は次のとおりです：

- ゲームスレッド上で順序どおりに実行される（割り込みなし）
- 失敗時の中断・リトライ・ステップ単位のタイムアウトを宣言的に指定できる
- すべての Artifact が 1 レスポンスにまとまる
- シナリオ単位の壁時計ウォッチドッグ（最大 1800 秒）が効く

詳細仕様は [シナリオ実行](scenario.md) を、テンプレートの実例は [使用例集](cookbook.md) を参照してください。

### スクリーンショットやダンプはどこに保存されますか？

`<プロジェクト>/Saved/UAIP/<SessionId>/` 配下です。さらに `Screenshots/`・`Dumps/`・`Logs/`・`Reports/` に分かれています。サーバ内部の正確なパスは外に出さない設計のため、AI クライアント側は Artifact ID を受け取り、Bridge またはエディタの HTTP Artifact エンドポイント経由でファイルを取得します。詳細は [Artifacts](artifacts.md) を参照してください。

### UI の状態を私が見ずに AI に確認してもらいたい

キャプチャコマンド（`CaptureActiveWindowImage`・`CaptureGraphViewportImage`・`CaptureEditorTabImage`）を呼んで、出力された PNG を AI に読み取らせるのが基本です。AI クライアントのファイル読み取りツールが画像をコンテキストに表示してくれます。構造を確認したいだけなら `DumpEditorState` / `DumpSlateTree` のほうが効率的です（JSON を解析するほうがピクセル解析より軽い）。

### コマンドを呼ぶときに `UAIP.` プレフィックスは必須ですか？

はい、コマンド名は完全修飾名です。`HealthCheck` だけ渡すと `CommandNotFound` を返します。`UAIP.Core.HealthCheck` のように完全名で指定してください。完全名が分からない場合は `uaip_list_commands(ProviderPrefix="UAIP.Core")` で確認できます。

---

## CI / 本番運用

### UAIP を CI で使えますか？

技術的には可能です（製品版の CLI トランスポート経由、[Cookbook レシピ 7](cookbook.md#7-ci-から-automation-test-を実行製品版) を参照）。ただし現実的にはエディタの起動が遅い（CI 環境で 30〜90 秒）、デモ版は CLI 非対応、Cook や Package、Validation といった充実した CI 向けプリミティブはまだロードマップ段階、という制約があります。

### 複数の AI エージェントで 1 つのエディタを共有できますか？

MCP Bridge は現状「1 プロジェクトに 1 エディタ」を前提としています。同じエディタ内での並行コマンドはディスパッチャレベルで直列化されますし、並行シナリオは `TooManyRequests` で拒否されます。並列でエージェント作業をしたい場合はエディタやプロジェクトを分けてください。

### UAIP はパッケージビルドに影響しますか？

デモ版・製品版ともに、プラグインはデフォルトではエディタ構成でしかロードされません。`UAIPRuntime*` モジュールは Gauntlet や Runtime 観測のためにパッケージビルドへの組み込みを opt-in できますが、`UAIPEditor*` モジュールはパッケージされません。

---

## バグ報告とコントリビューション

### 不具合はどこに報告すればよいですか？

リポジトリの [Issue](../../issues) に、以下の情報を添えて起票してください：

- UE バージョン（5.7 / 5.8 とマイナー番号）
- デモ版か製品版か
- 失敗したコマンド名とパラメータ
- レスポンスの `ErrorCode` と `ErrorMessage`
- 該当する場合はエディタのクラッシュログ（`Saved/Crashes/`）

### 新しいコマンドを提案したいです

ユースケースを Issue にまとめてご投稿ください。現状の候補は [ロードマップ](roadmap.md) を参照してください。

### Pull Request は受け付けていますか？

はい、PR も受け付けています。コードスタイルや実装内容については作者が精査し、必要に応じて修正したうえで取り込みます。事前に Issue で相談していただくと方針のすり合わせがしやすくなります。

**[English](../en/faq.md)** | [概要に戻る](overview.md)

# FAQ

## 全般

### UAIP は何のためのもの？

AI エージェントに、UE Editor と Runtime を「構造化された Capability ゲート付き API」で操作・観測・検証させるためのプラグインです。座標クリックや UI 内部スクリプティングのような壊れやすい手段に頼らない点が特徴です。

### 典型的なユーザーは？

- **AI を主軸に置く開発者** — Claude Code / Cursor / Windsurf / Copilot のセッションから実際にエディタを操作（アセットを開く、Blueprint を編集する、PIE を実行する、スクショを取る）したい
- **QA / テスト自動化エンジニア** — LLM 駆動のスモークテスト・PIE アサーション・キャプチャベースのリグレッション証跡を手書きせずに揃えたい
- **ツールプログラマー** — UE エディタメニューをリバースエンジニアリングする代わりに、安定したコマンド面の上にワークフローを構築したい

### UE 標準の Python スクリプトと何が違うの？

Python は実行チャネルの 1 つに過ぎません。UAIP は **意味的コマンド** を宣言済みパラメータスキーマ・必要 Capability・統一された artifact 出力とともに、MCP・HTTP・WebSocket・CLI の 4 transport で公開します。Python スクリプト（`RunEditorPythonScript`）も使えますが Capability / Policy 層をバイパスするため、登録済みコマンドでカバーできないケースに限定して使うべきです。

### デモ版に期間制限はある？

ありません。デモ版は **機能制限** のみ（Editor 編集不可、HTTP / WS / CLI 不可、キャプチャ画像に透かし）であって時間制限ではありません。期限なしで使えます。

---

## デモ版と Pro 版

### どちらから始めるべき？

まず **デモ版** から。観測・PIE 制御・シナリオ・UI 自動化・アサーションをカバーしており、統合モデルが自分のワークフローに合うか評価するのに十分です。

以下が必要になったら **Pro 版** にアップグレード：Editor 編集（Blueprint・Level・Asset・Material 等）、Runtime ワールド編集（Spawn・GAS・Input 注入 等）、HTTP / WebSocket / CLI トランスポート、Python スクリプト実行。

詳細比較は [デモ版ガイド](demo.md)。

### 1 プロジェクト内でデモ版と Pro 版を併用できる？

できません。同じプラグインパスを共有するため、置き換える形になります。`DefaultUAIP.ini` の Capability セットが異なるだけです。

### なぜデモ版のキャプチャに透かしが入る？

右下に `UAIP Demo` テキスト + プラグインアイコンのバナーをアルファブレンドで合成します。DLL にコンパイル済みのためファイル差し替えで除去できません。透かし合成失敗時は `ExecutionFailed` を返し（フェイルクローズ）、透かしなし画像を保存しません。

---

## セットアップ・接続

### Bridge は呼び出しの間エディタを起動したままにする？

はい。MCP Bridge は初回呼び出し時にエディタを起動し、接続を維持しつつクラッシュ / ハングを検出して自動再起動します（60 秒に最大 3 回まで、それ以降は AI にエラーを返す）。エディタライフサイクルを手動管理する必要はありません — 詳細は [usage.md §2](../../README.md#エディタライフサイクル)。

### デモ版で `-uaip-http-enable` が効かないのはなぜ？

デモバイナリは **MCP 専用** です。HTTP / WebSocket / CLI フラグは無視されます。これはフラグハンドラーを削除するのではなくモジュールロード時点で強制されています。Pro 版で解除されます。

### macOS / Linux で動く？

デモバイナリは Windows 専用。Pro 版は MCP Bridge と CLI / HTTP / WS トランスポートが macOS / Linux 対応ですが、グラフエディタコマンドや一部のオプションプラグインは Windows での検証が先行します。

### 認証はどう設定する？

- **MCP**: 認証なし（Bridge はローカル実行）
- **HTTP / WebSocket（Pro）**: 起動時に 32 文字 Bearer トークンを生成し `Saved/UAIP/EditorHttpAuthToken.txt` / `EditorWsAuthToken.txt` に保存。HTTP は `Authorization` ヘッダ、WebSocket は最初のフレームで渡す。開発時のみ `-uaip-http-no-auth` / `-uaip-ws-no-auth` を使用可能。接続は設計上 localhost 限定。

---

## Capability・安全性

### `AddBlueprintVariable` が `CapabilityNotAvailable` で返ってくる

編集系 Capability（`BlueprintEdit`、`BlueprintVariableEdit` 等）は **DefaultDenied** です。`Config/DefaultUAIP.ini` に追加してください：

```ini
[UAIP.SafetyPolicy]
+AllowedCapabilities=BlueprintEdit
+AllowedCapabilities=BlueprintVariableEdit
+AllowedCapabilities=BlueprintGraphEdit
```

その後エディタを再起動するか、`AllowCapabilityReload=True` を設定している場合は `UAIP.Core.ReloadCapabilities` を呼び出してください。

### Capability と SafetyPolicy はどう違う？

- **Capability** はコマンド毎・セッション毎の認可（例: このセッションは Blueprint を編集可能）。
- **SafetyPolicy** はプロセス全体に適用されるゲートで、Capability に関係なくカテゴリ全体を禁止できる（例: Read-Only モードはすべての書き込みを拒否）。SafetyPolicy はオペレーターが設定するもので、AI が Runtime で解除することはできません。

完全リファレンス: [Safety & Capabilities](safety.md)。

### `EditorKeyboardInput` を追加したのに `PressKey` が拒否される

`PressKey` には SafetyPolicy スイッチ `AllowKeyboardInput=True` も必要です（プロセスレベルで deny-by-default）。修飾キー（Ctrl/Alt/Shift/Cmd）には追加で `AllowKeyboardModifierInput=True` も必要です。Capability は「どのセッションが要求できるか」を、SafetyPolicy は「そもそも要求を受け付けるか」を制御します。

### AI に対して実質的に Read-Only にできる？

できます。`[UAIP.SafetyPolicy]` に `ReadOnly=True` を設定すれば、Capability セットに関わらずすべての変更系コマンドが `PolicyViolation` を返します。評価環境やサンドボックス向けに有用です。

---

## ワークフロー

### `uaip_execute` を繰り返すべき？それともシナリオを組むべき？

1 つの論理的タスクのために `uaip_execute` を 2 回以上呼ぶなら、`uaip_run_scenario` に切り替えるべきです。シナリオの利点：
- ゲームスレッド上での順序実行（割り込みなし）
- 失敗時中断・リトライ・ステップ単位タイムアウトを宣言的に指定可能
- 全 artifact が 1 レスポンスにまとまる
- シナリオごとに壁時計ウォッチドッグ（最大 1800 秒）

詳細仕様は [シナリオ実行](scenario.md)、テンプレートは [Cookbook](cookbook.md) を参照。

### スクリーンショット・ダンプの保存先は？

`<プロジェクト>/Saved/UAIP/<SessionId>/` 配下。`Screenshots/`・`Dumps/`・`Logs/`・`Reports/` に分かれています。正確なパスはサーバ内部のもので、AI クライアントは artifact ID を受け取り Bridge またはエディタの HTTP artifact エンドポイント経由でファイルを読みます。詳細は [Artifacts](artifacts.md)。

### UI 状態を私が見なくても AI に確認させたい

キャプチャコマンド（`CaptureActiveWindowImage`・`CaptureGraphViewportImage`・`CaptureEditorTabImage`）を呼んでから、出力 PNG を読み取らせます。AI クライアントのファイル読み取りツールが画像をコンテキストに表示できます。構造的な状態確認は `DumpEditorState` / `DumpSlateTree` の方が安価（JSON 解析の方がピクセル解析より低コスト）。

### コマンドを呼ぶときに `UAIP.` プレフィックスは必須？

はい、コマンド名は完全修飾です。`HealthCheck` は `CommandNotFound` を返します。`UAIP.Core.HealthCheck` のように指定してください。不明な場合は `uaip_list_commands(ProviderPrefix="UAIP.Core")` で完全名を確認できます。

---

## CI / 本番運用

### UAIP を CI で動かせる？

技術的には可能（Pro の CLI トランスポート経由、[Cookbook レシピ 7](cookbook.md#7-ci-から-automation-test-を実行pro) 参照）。現実的には、エディタ起動が遅い（CI 環境で 30〜90 秒）、デモは CLI 非対応、より充実した CI プリミティブ（Cook・Package・Validation）はロードマップ段階、という制約があります。

### 複数の AI エージェントで 1 つのエディタを共有できる？

MCP Bridge は現状「プロジェクト 1 つにエディタ 1 つ」を前提とします。1 エディタ内の並行コマンドはディスパッチャレベルで直列化されます。並行シナリオは `TooManyRequests` で拒否されます。並列エージェント作業が必要ならエディタ / プロジェクトを分けてください。

### UAIP はパッケージビルドに影響する？

デモ版・Pro 版ともプラグインはデフォルトでエディタ構成でのみロードされます。`UAIPRuntime*` モジュールは Gauntlet / Runtime 観測のためパッケージビルドへの組み込みを opt-in できますが、`UAIPEditor*` モジュールはパッケージされません。

---

## バグ報告・コントリビューション

### 不具合はどこに報告すれば？

リポジトリの [Issue](../../issues) に以下の情報とともに起票してください：
- UE バージョン（5.7 / 5.8 + マイナー）
- デモ版 / Pro 版
- 失敗したコマンド + パラメータ
- レスポンスの `ErrorCode` と `ErrorMessage`
- 該当する場合はエディタクラッシュログ（`Saved/Crashes/`）

### 新しいコマンドを提案したい

ユースケースを Issue に記載してください。候補は [ロードマップ](roadmap.md) で管理しています。横断的な設計変更は ADR が必要、小規模な追加は既存モジュールパターンに従います。

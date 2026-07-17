**[English](../en/roadmap.md)** | [概要に戻る](overview.md)

# ロードマップ

以下は今後追加予定 / 調査中の項目です。具体的なリリース時期は約束しておらず、ユーザー要望や上流の UE バージョンの API 安定性次第で変更される可能性があります。

> **1.1.0 で実装済み。** かつて本ロードマップに掲載していた複数の機能 — Foliage、World Partition / DataLayer / HLOD、MVVM、サウンドアーキテクチャ、Config Settings、Data Registry、Plugin 管理、PCG 拡張、Chaos Cloth、アセット参照解析 / Asset Manager / Redirector 修正、コンソール変数（CVar）管理、ビューポート座標変換、可視アクター一覧取得、ログ Verbosity 制御（および Semantic Search は部分的 — 埋め込みパイプラインは依然 Epic 社内環境のみ）— は実装済みとなり [Changelog](changelog.md) へ移動しました。以降のリストには掲載していません。

---

## エンジンバージョン対応

### UE 5.6 以下の後方互換
UAIP は現在 UE 5.7 / 5.8 を対象としています。UE 5.6 以下への対応は将来リリースでの検討項目です。UE 5.5 以下は要望次第で判断します。

### Linux / macOS 対応
現在は Windows (Win64) のみ対応しています。Linux / macOS への対応は、需要と検証環境が整ったタイミングで検討します。

---

## Editor — アセット・プロジェクト管理

### アセット検証（Validation）
登録済みの `UEditorValidatorSubsystem` Validator を個別アセット / フォルダ単位で実行。結果は構造化された JSON Artifact で返却。

### ローカライズパイプライン
ローカライズワークフロー全体の自動化：テキスト収集、ローカライズデータコンパイル、Culture 管理、StringTable エントリの追加/編集/削除、検証用の Editor 表示言語切替。

### Build / Package パイプライン
コンテンツの Cook、プロジェクトのパッケージング、Project Launcher プロファイルの AI 経由実行。長時間処理は進捗報告とキャンセル対応。

---

## Editor — 編集ドメイン拡張

### MetaHuman 編集
`MetaHumanCharacterEditorSubsystem` 経由で MetaHuman の Body / Face / Skin / Eye / Hair パラメータを編集 — MetaHuman Character プラグインを採用するプロジェクト向け。長時間処理は進捗報告に対応。`MetaHuman Character` プラグインと **UE 5.8 以降** が必要。

### マテリアル検証・テンプレート
プロジェクトルールに対するマテリアル検証、類似マテリアル検索、ワークフローテンプレートからのマテリアル作成。

### Mixed Control Rig トラック
Level Sequence への Mixed Control Rig トラック追加（AnimMixer 部分は既に実装済み、本項目は残る `MovieSceneMixedControlRig` ネイティブコマンドが対象）。

### Motion Matching（PoseSearch）
UE の Motion Matching 採用プロジェクト向けに、PoseSearchDatabase の内容、Schema 設定、ノーマライゼーションパラメータを管理。

### Chaos Destruction（Geometry Collection）
Geometry Collection アセットの編集 — メッシュのフラクチャ、ダメージ閾値設定、クラスタ構造の検査。

### Groom（Strand-Based Hair）
Groom Asset の設定 — シミュレーションパラメータ・LOD 設定・SkeletalMesh バインディング。

### 追加のオプショングラフエディタ
- **MetaSound 向け Subsonic**（UE 5.8）: イベント駆動オーディオ統合
- **ControlRig Dynamics**（UE 5.8）: ControlRig グラフ内の簡易物理シミュレーションノード
- **AnimationLayering / UAF**（UE 5.8）: ボーンマスクレイヤーと Unified Animation Framework ノード
- **MeshPartition（MegaMesh）**（UE 5.8）: 大規模メッシュの空間分割と非破壊モディファイア
- **Enhanced Input デバッグ**（UE 5.8）: 現在の Enhanced Input / CommonUI 入力状態のダンプと Input Action の仮想発火 — `PlayerInputDebugger` プラグインを活用
- **CustomizableSequencerTracks**: Blueprint 定義のカスタム Sequencer トラック型対応
- **DataPrep Asset**: DataPrep インポートパイプライン Asset の実行と検査

---

## Runtime — 検査・デバッグ

### BehaviorTree / StateTree Runtime 状態
PIE 中の現在アクティブノード、遷移履歴、Blackboard 値のダンプ — 既存の Editor 側 BT / StateTree コマンドと組み合わせて「設計 → プレイテスト → デバッグ」ループを完結。

### AnimInstance Runtime 状態
PIE 中のアクターのアクティブステートマシン状態、ブレンドウェイト、再生中モンタージュ、Anim Curve 値のダンプ。

### AI Perception 観測
`UAIPerceptionComponent` のセンサー状態、現在感知中のアクター、アクターが発している Stimuli のダンプ — 「なぜ敵が気づかなかったか」のデバッグに対応。

### Navigation Runtime クエリ
2 点間のパス計算、到達可能性テスト、NavMesh タイルカバレッジダンプ、NavModifier ゾーンの検査 — 観測専用、NavMesh 編集は含まない。

### GameViewport Widget 観測
`UGameViewportClient` をルートとした Widget ツリーのダンプ（HUD / メニュー / Runtime UI）— Editor 全体を対象とする `DumpSlateTree` よりも絞られたノイズの少ない結果。

### CommonUI スタック観測
`UCommonUISubsystem` のアクティブ Widget スタック・フォーカス状態・現在の入力モードのダンプ。CommonUI 採用プロジェクト向け。

### Subsystem 列挙・状態
登録済みの `UGameInstanceSubsystem` / `UWorldSubsystem` / `ULocalPlayerSubsystem` の列挙と `UPROPERTY` 値のダンプ — 現在の Subsystem 検査フローにおける Discovery ギャップを埋める。

### Network / Replication 観測
NetConnection 統計（RTT、パケットロス、帯域）、NetDriver 情報、アクター単位の Replicated プロパティダンプ — マルチプレイヤーデバッグ用。

### Chaos Runtime 状態
PIE 中の `UGeometryCollectionComponent` のクラスタ状態、破壊イベントログ、Chaos Field System 状態のダンプ — Editor 側の Geometry Collection 編集と組み合わせて使用。

### Mass Entity 観測
PIE 中の Mass Entity アーキタイプ一覧・エンティティ数・プロセッサ実行グラフのダンプ — 群衆 AI や大規模エンティティシミュレーションを採用するプロジェクトのデバッグ向け。`MassEntity` / `MassGameplay` プラグインが必要。

### パフォーマンス Insights Tracing
UE Trace セッションのチャネル指定での開始 / 停止、フレーム統計と Hitch サマリの取得、ドメイン別 Trace（HTTP イベント、Niagara タイミング、レンダリングコマンド）の検査。

### GameplayMessage Subsystem
イベント駆動アーキテクチャ向けに `UGameplayMessageSubsystem` メッセージのリッスンと注入 — 疎結合なゲームプレイシステムのテストに有用。

### SaveGame 操作
`USaveGame` スロットの一覧 / ロード / 保存 / 削除 — テストを特定セーブ状態から開始したり、既知のベースラインへリセットしたりが可能に。

---

## インフラ

### 人間向け Editor GUI
AI アクティビティ監視用のオプショナル Editor タブ：Command History（コマンドとレスポンスのタイムライン表示）、Artifact Viewer（スクリーンショット・JSON ダンプ・レポートのインラインプレビュー）。

### EDA トランスポート
既存の MCP / HTTP / WebSocket / CLI に加えて、Epic の Epic Developer Assistant (EDA) と UAIP を接続するオプショナルトランスポート。Epic 側の `window.eda.*` JavaScript API の安定化が前提。

---

> 機能リクエスト・バグ報告は、リポジトリの [Issue](../../issues) からお願いします。

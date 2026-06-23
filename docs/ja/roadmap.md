**[English](../en/roadmap.md)** | [概要に戻る](overview.md)

# ロードマップ

以下は今後追加予定 / 調査中の項目です。具体的なリリース時期は約束しておらず、ユーザー要望や上流の UE バージョンの API 安定性次第で変更される可能性があります。

---

## エンジンバージョン対応

### UE 5.6 以下の後方互換
UAIP は現在 UE 5.7 / 5.8 を対象としています。UE 5.6 以下への対応は将来リリースでの検討項目です。UE 5.5 以下は要望次第で判断します。

### Linux / macOS 対応
現在は Windows (Win64) のみ対応しています。Linux / macOS への対応は、需要と検証環境が整ったタイミングで検討します。

---

## Editor — アセット・プロジェクト管理

### サンドボックス機能
AI による変更を Sandbox に仮置きし、人間が確認・承認してから本体に反映する仕組み。Undo に頼らず変更を選択的に承認・却下できます。内部で UE 5.8 の `FileSandboxCore` を利用するため、実装後も **UE 5.8 以降限定** の機能となります。

### Config Settings 管理
Project Settings / Editor Preferences をプログラムから読み書き — コンテナ・カテゴリの列挙、セクションスキーマの取得、プロパティ値の取得・設定、変更の保存、デフォルトへのリセット。書き込みには `ConfigSettingsEdit` Capability が必要。

### Data Registry
登録済みの Data Registry の列挙、スキーマ取得、データソース一覧、アイテムクエリ — UE の Data Registry を採用するプロジェクト向けに、既存の DataTable コマンドを補完する機能。

### Plugin 管理
探索済みプラグイン・有効プラグインの列挙、プラグイン情報と依存グラフの検査、プラグインのプログラムからの有効化 / 無効化 — AI 主導のプロジェクトセットアップと依存管理ワークフロー向け。書き込みには `PluginManagementEdit` Capability が必要。

### アセット参照解析・SizeMap
アセット参照グラフ取得・未参照アセット検出・循環参照検出・コンテンツツリー全体の SizeMap 生成。

### アセット検証（Validation）
登録済みの `UEditorValidatorSubsystem` Validator を個別アセット / フォルダ単位で実行。結果は構造化された JSON Artifact で返却。

### Asset Manager 設定
PrimaryAssetType 定義・アセットバンドル・アセットタグをプログラムから管理。DLC・ContentBundle・Cook ルール用ワークフローを想定。

### Asset Redirector 修正
リネーム・移動で生成された Redirector を一括修正 — 全 Redirector の列挙、フォルダ指定の一括修正、参照先のクリーンアップを AI 主導のリファクタリングフロー内で完結。

### ローカライズパイプライン
ローカライズワークフロー全体の自動化：テキスト収集、ローカライズデータコンパイル、Culture 管理、StringTable エントリの追加/編集/削除、検証用の Editor 表示言語切替。

### Build / Package パイプライン
コンテンツの Cook、プロジェクトのパッケージング、Project Launcher プロファイルの AI 経由実行。長時間処理は進捗報告とキャンセル対応。

---

## Editor — 編集ドメイン拡張

### MetaHuman 編集
`MetaHumanCharacterEditorSubsystem` 経由で MetaHuman の Body / Face / Skin / Eye / Hair パラメータを編集 — MetaHuman Character プラグインを採用するプロジェクト向け。長時間処理は進捗報告に対応。`MetaHuman Character` プラグインと **UE 5.8 以降** が必要。

### World Partition / DataLayer 操作
World Partition マップでの DataLayer 管理 — 作成、削除、初期状態設定、アクターの紐付け。HLOD レイヤー割り当て・External Actor 一覧も含む。

### Foliage 編集
レベル内の FoliageType 一覧取得、座標指定でのインスタンス追加、領域指定での一括削除、FoliageType の設定変更（密度・スケール・カリング）。

### マテリアル検証・テンプレート
プロジェクトルールに対するマテリアル検証、類似マテリアル検索、ワークフローテンプレートからのマテリアル作成。

### MVVM 対応
`ModelViewViewModel` プラグイン採用プロジェクト向けに、ViewModel クラス作成・View Binding の追加 / 削除 / 設定を AI から実行可能に。

### Mixed Control Rig トラック
Level Sequence への Mixed Control Rig トラック追加（AnimMixer 部分は既に実装済み、本項目は残る `MovieSceneMixedControlRig` ネイティブコマンドが対象）。

### Motion Matching（PoseSearch）
UE の Motion Matching 採用プロジェクト向けに、PoseSearchDatabase の内容、Schema 設定、ノーマライゼーションパラメータを管理。

### サウンドアーキテクチャ（SoundClass / Attenuation / Mix）
既存の SoundCue コマンドを拡張し、SoundClass（ボリューム階層）・SoundAttenuation（空間設定）・SoundMix（EQ・ピッチ変調）の操作をカバー。

### Chaos Destruction（Geometry Collection）
Geometry Collection アセットの編集 — メッシュのフラクチャ、ダメージ閾値設定、クラスタ構造の検査。

### Groom（Strand-Based Hair）
Groom Asset の設定 — シミュレーションパラメータ・LOD 設定・SkeletalMesh バインディング。

### 追加のオプショングラフエディタ
- **MetaSound 向け Subsonic**（UE 5.8）: イベント駆動オーディオ統合
- **ControlRig Dynamics**（UE 5.8）: ControlRig グラフ内の簡易物理シミュレーションノード
- **AnimationLayering / UAF**（UE 5.8）: ボーンマスクレイヤーと Unified Animation Framework ノード
- **MeshPartition（MegaMesh）**（UE 5.8）: 大規模メッシュの空間分割と非破壊モディファイア
- **ChaosCloth Asset**（UE 5.8）: Weight Map、Sim / Render Mesh、Cloth シミュレーション設定
- **PCG 拡張コマンド**（UE 5.8）: 空間オペレーション・Async 実行・属性プロパティセレクタを含む約 30 件の追加コマンド — 既存 PCG ネイティブコマンドを補完し、**UE 5.8 以降限定**で利用可能
- **Enhanced Input デバッグ**（UE 5.8）: 現在の Enhanced Input / CommonUI 入力状態のダンプと Input Action の仮想発火 — `PlayerInputDebugger` プラグインを活用
- **CustomizableSequencerTracks**: Blueprint 定義のカスタム Sequencer トラック型対応
- **DataPrep Asset**: DataPrep インポートパイプライン Asset の実行と検査

---

## Editor — 観察・状態取得

### ビューポート座標変換
エディタビューポートでのワールド座標 ↔ スクリーン座標の相互変換。アクターの画面上位置の確認、UI 自動化での座標指定、空間クエリとの組み合わせ計算など、複数のワークフローで横断的に利用できます。

### 可視アクター一覧取得
エディタビューポートのフラスタムに入っているアクターの一覧を取得。コマンドの適用対象を「今カメラに映っているもの」に絞りたいワークフロー向け。

### ログ Verbosity 制御
カテゴリ別のログ出力レベルの取得・設定。デバッグセッション中に特定モジュールのログを詳細化してから自動的に元に戻すワークフローを AI から一括制御。

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

### Semantic Asset Search（凍結中）
AI による Content Browser のセマンティック検索。内部で UE 5.8 の `SemanticSearch` プラグインを使うため、実装後も **UE 5.8 以降限定** の機能となります。さらに UE 5.8 時点では `SemanticSearch` の埋め込みパイプラインが Epic 社内環境でしか動作しない状態のため、公開ビルドでの動作が確認できた時点で再評価します。それまで本項目は **凍結中** です。

---

## インフラ

### 人間向け Editor GUI
AI アクティビティ監視用のオプショナル Editor タブ：Command History（コマンドとレスポンスのタイムライン表示）、Artifact Viewer（スクリーンショット・JSON ダンプ・レポートのインラインプレビュー）。

### EDA トランスポート
既存の MCP / HTTP / WebSocket / CLI に加えて、Epic の Epic Developer Assistant (EDA) と UAIP を接続するオプショナルトランスポート。Epic 側の `window.eda.*` JavaScript API の安定化が前提。

---

> 機能リクエスト・バグ報告は、リポジトリの [Issue](../../issues) からお願いします。

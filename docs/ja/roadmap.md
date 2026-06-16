**[English](../en/roadmap.md)** | [概要に戻る](overview.md)

# ロードマップ

以下は現在計画中または検討中の機能です。リリース時期は未確定であり、内容は変更される場合があります。

---

## エンジンバージョン対応

### UE 5.5 以前への後方対応
現在は UE 5.7 / 5.8 に対応しています。UE 5.5 程度までは積極的に後方対応を進める予定です。それ以前のバージョン（5.4 以下）については要望状況を見て判断します。

---

## 新規コマンド実装

### Sandbox Editing（サンドボックス編集）
AI が提案した編集をサンドボックスに仮置きし、人間が確認・承認してからディスクに反映するワークフロー。変更を選択的に受け入れ・破棄でき、Undo に頼る必要がありません。

### アセット監査・依存関係解析
アセット依存グラフの取得、未参照アセットの検出、循環参照の特定、コンテンツツリー全体のサイズマップ生成。

### アセットバリデーション
`UEditorValidatorSubsystem` に登録済みのバリデーターを単一アセットやフォルダ単位で実行。結果は JSON の Artifact として返却されるため、CI/CD ゲートとして利用できます。

### Asset Manager 設定
PrimaryAssetType 定義・アセットバンドル・アセットタグのプログラマブルな管理。DLC・コンテンツバンドル・クック対象制御を対象にしています。

### ローカライゼーションパイプライン自動化
ソーステキストのギャザー・コンパイル・カルチャー管理・StringTable エントリの追加/編集/削除・エディタ表示言語切替まで、ローカライゼーション全工程の自動化。

### ビルド・パッケージパイプライン
コンテンツのクック・プロジェクトのパッケージング・Project Launcher プロファイルの実行。長時間処理の進捗報告とキャンセルに対応し、CI/CD パイプラインへの組み込みを想定しています。

### パフォーマンス Insights トレーシング
チャンネル指定で UE Trace セッションを開始・停止し、フレーム統計・ヒッチサマリ・ドメイン別トレース（HTTP イベント・Niagara タイミング・レンダーコマンド）を照会。結果は JSON Artifact として返却されます。

### マテリアルバリデーション・テンプレート
マテリアルをプロジェクトルールに照らして検証、類似マテリアルの検出、ワークフローテンプレートからの新規マテリアル作成。

### MVVM サポート
`ModelViewViewModel` プラグインを利用するプロジェクト向けに、ViewModel クラスの作成・View Binding の追加/削除/設定を AI から操作できるコマンド群。

### Enhanced Input 状態診断
現在の Enhanced Input 状態の取得（`DumpInputState`）と Input Action の仮想発火（`SimulateInputAction`）。UI 自動化テストのデバッグを対象にしています。

### セマンティックアセット検索
ファイル名ではなく意味でアセットを検索できる AI 駆動のコンテンツブラウザ検索。現時点では埋め込み生成の安定性の問題により開発を一時停止しています。

### 追加グラフエディタ統合
- **Niagara Subsonic**：MetaSound・Niagara グラフへの Subsonic オーディオイベントノード対応
- **ControlRig Dynamics**：ControlRig グラフ内の簡易物理シミュレーションノード設定
- **Mixed Control Rig トラック**：Level Sequence への Mixed Control Rig トラック追加
- **AnimationLayering / UAF**：Anim Blueprint でのボーンマスクレイヤーと UAF ノード操作
- **MeshPartition（MegaMesh）**：大規模メッシュへの空間分割・非破壊モディファイア設定
- **ChaosCloth Asset**：Weight Map・Sim/Render Mesh・クロス物理シミュレーション設定
- **CustomizableSequencerTracks**：Blueprint 定義のカスタム Sequencer トラック型への対応
- **DataPrep Asset**：DataPrep インポートパイプラインアセットの実行・検査

---

## 環境・インフラ

### 人間向けエディタ GUI
AI の活動を人間がモニタリングするためのオプショナルエディタタブ。CommandHistory（コマンドとレスポンスのタイムライン）・ArtifactViewer（スクリーンショット・JSON ダンプ・レポートのインラインプレビュー）を想定しています。

### EDA トランスポート
既存の MCP・HTTP・WebSocket・CLI に加え、Epic の Epic Developer Assistant（EDA）へ接続するオプショナルトランスポート。

---

> 機能リクエストやバグ報告は、このリポジトリの [Issue](../../issues) からお願いします。

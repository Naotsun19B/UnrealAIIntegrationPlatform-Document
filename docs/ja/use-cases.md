**[English](../en/use-cases.md)** | [概要に戻る](overview.md)

# ユースケース

UAIP は「誰が」「何のために」「なぜ」使うのか。本ページはその全体像をまとめたものです。各ユースケースには Cookbook の対応レシピと必要な Capability へのリンクを添えています。

> 動くサンプル JSON が必要な場合は [使用例集](cookbook.md) に直接ジャンプしてください。本ページは「なぜそれをやりたくなるか」の文脈整理に重点を置いています。

---

## 1. エディタ側の AI ペアプログラミング

**こんな人向け**：Claude Code / Cursor / Copilot をメイン IDE として使っているソロ開発者や小規模チーム。UAIP が一番想定しているメインユースケースです。

**何が問題か**：AI は C++ のパッチ生成は得意ですが、UE プロジェクトの Blueprint 側に踏み込むと何もできなくなります。「このウィジェットをあのイベントに繋ぎたい」という変更はソースコードには存在せず、BP グラフそのものが正解となるためです。

**UAIP が用意している手段**：
- `UAIP.Editor.Blueprint.*` で変数追加・ノード追加・ピン配線
- `UAIP.Editor.UMG.*` でウィジェットツリー・アニメーション・バインディングを編集
- `UAIP.Editor.Level.*` でアクター配置やトランスフォーム調整
- `UAIP.Editor.Property.*` でアセットやアクターのフィールドを変更
- `CompileBlueprint` とエラー取得（計画中、[ロードマップ → Blueprint Compile / コンパイルエラー取得](roadmap.md#blueprint-compile--コンパイルエラー取得) を参照）で「編集 → 検証 → 修正」のループを閉じる

**必要な Capability**：`BlueprintEdit`・`BlueprintGraphEdit`・`BlueprintVariableEdit`・`WidgetTreeEdit`・`EditorActorEdit`・`PropertyEdit` はいずれも DefaultDenied です。実際のワークフローで必要なものだけを明示的に有効化してください（[セキュリティ → 推奨セキュリティプロファイル](security.md#推奨セキュリティプロファイル) を参照）。

**製品版限定**：編集系モジュールはデモバイナリには含まれません。

**Cookbook の対応レシピ**：[Blueprint 編集と検証のループ](cookbook.md#4-blueprint-編集検証ループ)。

---

## 2. AI 駆動のテスト作成と QA

**こんな人向け**：QA / テスト自動化エンジニアや、プレイテストスクリプトを抱えているゲームプレイプログラマー。

**何が問題か**：PIE スモークテストを毎回手で書くのは時間がかかるうえ、レベルレイアウトが変わると一気に陳腐化します。AI エージェントは「マップを動き回って異変を報告する」のは得意ですが、それを実現するにはゲームを実際に操作できる手段が必要です。

**UAIP が用意している手段**：
- `UAIP.Runtime.PIE.*` で PIE の起動・停止・マップロードを制御
- `UAIP.Runtime.Input` と `UAIP.Editor.UIAutomation.*` でキャラクタや UI を実際に操作
- `UAIP.Runtime.Observation.CheckpointCapture` で任意のタイミングにスクリーンショットと状態ダンプを残す
- `UAIP.Runtime.Assertion.AssertActorProperty` / `AssertWorldState` で事後条件を宣言的にチェック
- シナリオ機能で一連の流れを単一の監査可能なレコードにまとめる

**必要な Capability**：`PIEControl`・`RuntimeCapture`・`RuntimeInspect`（いずれも DefaultAllow）。キャラクタを操作する場合はさらに `RuntimeActorManipulation` と `RuntimeInputInjection` が必要です。

**Cookbook の対応レシピ**：[PIE スモークテスト](cookbook.md#1-pie-スモークテスト)、[PIE プレイテスト + キャプチャ](cookbook.md#6-pie-プレイテスト--キャプチャ)。

---

## 3. AI によるコード / Blueprint レビュー

**こんな人向け**：リードプログラマや、PR の一次レビューを LLM に任せたい人。

**何が問題か**：Blueprint を多用するプロジェクトのコードレビューは厄介です。グラフは視覚情報なので diff ツールでは判別しづらく、「重要な変更だったか」を見極めるには結局エディタを開く必要があります。単純な PR ごとに人間が開いて確認するのは負担が大きすぎます。

**UAIP が用意している手段**：
- `UAIP.Editor.Assets.OpenAsset` で対象 Blueprint をフォーカス
- `UAIP.Editor.Workspace.NormalizeEditorLayout` でスクリーンショットを再現可能なレイアウトに整える
- `UAIP.Editor.Observation.CaptureGraphViewportImage` で AI にグラフそのものを見せる
- `UAIP.Editor.Blueprint.ListBlueprintPins` で構造レベルの解析を可能にする（ピクセル比較ではない）
- `UAIP.Editor.Observation.DumpEditorState` で同時に開いている他のアセットの状態も把握させる

**必要な Capability**：`EditorInspect`・`EditorObservation`・`EditorWorkspaceControl`（いずれも DefaultAllow）。**書き込み系の Capability は不要** なので、デモバイナリだけで実現できます。

**Cookbook の対応レシピ**：[AI コード / Blueprint レビュー](cookbook.md#2-ai-コード--blueprint-レビュー)。

---

## 4. アセット監査とクリーンアップ

**こんな人向け**：テクニカルアーティスト、コンテンツリード、プロジェクト規約の遵守を担当している人。

**何が問題か**：規模が大きくなると「`BP_FooBar` は `/Misc/` ではなく `/Characters/Heroes/` に置く」といったルールがすぐに守られなくなります。5000 アセット規模のプロジェクトで違反を洗い出すのは結局スクリプト作業になり、しかもそのスクリプトはエディタのバージョンアップで壊れがちです。

**UAIP が用意している手段**：
- `UAIP.Editor.Assets.SearchAssets` でパス / クラス / タグごとにアセットを列挙
- `UAIP.Editor.Property.GetAssetProperty` で個別フィールドの値を検査
- `UAIP.Editor.GameplayTags.FindGameplayTagReferencers` でタグの使用箇所を追跡
- エディタの UI 変更に左右されにくい、意味レベルの安定したコマンド面

**必要な Capability**：`EditorInspect`（DefaultAllow）のみ。AI に違反の報告だけでなく修正まで任せたい場合は `AssetDelete` / `AssetFolderRefactor` を追加してください。

**Cookbook の対応レシピ**：[アセット監査と命名チェック](cookbook.md#3-アセット監査命名チェック)。

**関連するロードマップ項目**：依存関係のより深い解析（未参照アセット検出・循環参照検出・サイズマップ生成）は計画中で未実装です。[ロードマップ → アセット参照解析・SizeMap](roadmap.md#アセット参照解析sizemap) を参照してください。

---

## 5. エディタ拡張の UI 自動化テスト

**こんな人向け**：プラグイン作者や、エディタユーティリティを作っているツールプログラマー。

**何が問題か**：カスタムエディタツールを検証するにはメニュー操作・フォーム入力・ダイアログ確認が欠かせません。これを毎リリース手作業で行うのは現実的でなく、かといって座標ベースのスクリプトで自動化するとレイアウト変更ですぐ壊れます。

**UAIP が用意している手段**：
- `SelectMenuItem`・`ClickWidget`・`InputText`・`SetCheckboxState`・`SetComboSelection` で入力操作
- `WaitForWidget` で同期処理（`Sleep` を挟むような不安定なやり方が不要）
- `AcceptDialog` / `CancelDialog` でモーダルダイアログの応答
- `CaptureActiveWindowImage` で視覚的なリグレッション証跡を残す

**必要な Capability**：`EditorUIAutomation`（DefaultAllow）が基本。`PressKey` を使う場合は `EditorKeyboardInput` を、`InvokeContextMenuAction` を使う場合は `AllowContextMenuMutation` を追加で有効化します。

**Cookbook の対応レシピ**：[UI 自動化テスト](cookbook.md#5-ui-自動化テスト)。

---

## 6. プロシージャルコンテンツのワークフロー

**こんな人向け**：PCG ユーザー、プロシージャルアーティスト、テクニカルデザイナー。

**何が問題か**：PCG のパラメータ調整は「値を変える → 再生成 → 結果確認」を繰り返す反復作業です。ノードが 1 つならエディタで手動でもよいのですが、グラフ全体に数十ノードあると一気に手間が膨らみます。

**UAIP が用意している手段**：
- `UAIP.Editor.PCG.GetPCGGraphInfo` でグラフ構造を取得
- `UAIP.Editor.PCG.SetPCGNodeProperty` でパラメータを変更
- `UAIP.Editor.PCG.ExecutePCGGraph` で再生成をトリガー
- `CaptureViewportImage` / `DumpWorldState` で結果を確認
- シナリオ機能でパラメータを範囲スイープし、各ステップでスクリーンショットを残す

**必要な Capability**：`PCGGraphEdit`（DefaultDenied、`PCG` プラグインが必要）。カスタムノードのプロパティを触る場合は `PCGCustomNodeEdit` / `PCGBlueprintNodeEdit` も。

**製品版限定**：PCG 編集はデモ版には含まれません。

---

## 7. アニメーションパイプラインの統合

**こんな人向け**：アニメーションテクニカルアーティスト、AnimBlueprint の保守担当、ControlRig ユーザー。

**何が問題か**：複雑なアニメツリーは規模が大きく、AnimGraph のステート・ステートマシンの遷移・ControlRig のリグ・Sequencer のシネマティックがすべて絡み合っています。1 ヶ所変えると思わぬところが壊れやすく、目視検証は必要ですが、変更のたびに毎回やるのは現実的ではありません。

**UAIP が用意している手段**：
- `UAIP.Editor.AnimBlueprint.*` で AnimGraph と StateMachine を編集
- `UAIP.Editor.ControlRig.*` でヒエラルキーと RigVM グラフを編集（ネイティブ 59 件 + Toolset 44 件）
- `UAIP.Editor.Sequencer.*` で LevelSequence を編集（ネイティブ 93 件 + Toolset 61 件）
- `UAIP.Editor.Skeleton.*` でソケットやバーチャルボーンを管理
- `UAIP.Editor.Physics.*` で物理アセットを調整
- `UAIP.Runtime.PIE.*` 経由の Runtime 検証と、計画中の Anim 観測（[ロードマップ → AnimInstance Runtime 状態](roadmap.md#animinstance-runtime-状態) を参照）

**必要な Capability**：`AnimBlueprintGraphEdit`・`AnimStateMachineEdit`・`ControlRigGraphEdit`・`ControlRigHierarchyEdit`・`SequencerStructureEdit`・`SequencerKeyframeEdit`・`SkeletonAssetEdit`・`PhysicsAssetEdit`・`PhysicsBodyEdit`（いずれも DefaultDenied）。

**製品版限定**。

---

## 8. マルチプレイヤー / ゲームプレイシステムのデバッグ

**こんな人向け**：PIE 環境でしか再現しないバグを追っているゲームプレイプログラマー。

**何が問題か**：「スタンドアロンでは動くがマルチプレイで壊れる」「特定の条件で AI がプレイヤーを認識しない」。再現には PIE が必要で、解析には Replicated プロパティ・AI Perception・BehaviorTree のアクティブノード・GameplayAbility の状態など、複数の視点を同時に読む必要があります。エディタ標準のデバッグ UI は一度に一視点しか見られず、効率がよくありません。

**UAIP が用意している手段**：
- `UAIP.Runtime.Observation.DumpWorldState` でワールド全体を俯瞰
- `UAIP.Runtime.GAS.*` でアビリティ / 属性 / エフェクトを検査
- 計画中：AI Perception、BehaviorTree / StateTree の Runtime 状態、AnimInstance 状態、Network / Replication 状態（[ロードマップ → Runtime — 検査・デバッグ](roadmap.md#runtime--検査デバッグ)）
- シナリオ機能で不具合状態を再現させ、証跡を一度の実行でまとめて残す

**必要な Capability**：`PIEControl`・`RuntimeInspect`・`RuntimeGASInspect`（いずれも DefaultAllow）。書き込みが必要な場合は `RuntimeActorManipulation` を追加。

---

## 9. コンテンツコンプライアンス / Pre-submit ゲート

**こんな人向け**：ビルドエンジニアや、社内ツールの保守担当。

**何が問題か**：「コンパイルが通らない Blueprint が紛れていないか」「`/Game/Tests/` 配下に意図せずアセットが追加されていないか」といったチェックは Pre-submit ゲートに組み込みたいところですが、C++ で書こうとするとカスタムコマンドレットを cook する必要があり、反復もロールアウトも遅くなりがちです。

**UAIP が用意している手段**：
- CLI トランスポート（製品版）で、Pre-submit フックや CI からのヘッドレス one-shot 実行
- `UAIP.Editor.Execution.RunAutomationTest` でテスト実行
- 計画中：`ValidateAsset` / `ValidateFolder`（[ロードマップ → アセット検証（Validation）](roadmap.md#アセット検証validation)）
- 計画中：Build / Package パイプライン（[ロードマップ → Build / Package パイプライン](roadmap.md#build--package-パイプライン)）

**必要な Capability**：`EditorInspect`・`EditorExecution`（いずれも DefaultAllow）。

**Cookbook の対応レシピ**：[CI から Automation Test を実行（製品版）](cookbook.md#7-ci-から-automation-test-を実行製品版)。

**現実的な注意**：現状の CI 連携は使えますが粗削りです（エディタ起動が遅い、デモ版は CLI 非対応、検証プリミティブはロードマップ段階）。コミット単位のサブ秒 lint ではなく、ビルド検証クラスのユースケースに向いています。

---

## 10. ライブオプス / データ駆動バランシング

**こんな人向け**：ゲームプレイデザイナーやライブオプスエンジニア。

**何が問題か**：ゲームバランスを決める定数は DataTable・Blueprint のデフォルト値・プロジェクト設定に散らばっています。バランス調整の反復には、エンジニアが個々を手で編集するか、その都度使い捨てツールを書くしかなく、いずれもスピードが出ません。

**UAIP が用意している手段**：
- `UAIP.Editor.DataTable.*` で行の CRUD と CSV インポート / エクスポート
- `UAIP.Editor.Property.GetBlueprintDefault` / `SetBlueprintDefault` で CDO を調整
- `UAIP.Editor.Property.GetProjectSetting` / `SetProjectSetting` で `UDeveloperSettings` ベースの設定を変更
- `UAIP.Runtime.GAS.*` で属性 / アビリティに反映された結果を PIE 内で検証

**必要な Capability**：`DataTableRowEdit`・`DataTableImport`・`BlueprintEdit`・`ProjectConfigEdit`（いずれも DefaultDenied）。

**製品版限定**。

---

## UAIP を **使うべきでない** ケース

- **本番ユーザー向けの自動化**：UAIP は開発 / CI 用途を想定したもので、出荷後のゲーム挙動を制御するためのものではありません。Runtime ゲームプレイにはエンジン本体のサブシステム（Gameplay Abilities、オンラインサービスなど）を使ってください
- **サブ秒の反復ループ**：エディタ起動のオーバーヘッドが大きいため、10 ms 単位のレスポンスが必要な場面には向きません。その用途には UE プラグインを直接書くべきです
- **IDE の置き換え**：UAIP は C++ ソースコードを編集しません。コード変更には引き続き IDE を使い、UAIP はエディタ内に存在するプロジェクト要素（Blueprint、アセット、レベル等）の操作に使ってください
- **マルチテナント運用**：UAIP は「1 プロジェクトに 1 エディタ」を前提としています。1 つの Bridge を複数ユーザーで同時に共有しないでください
- **公開ネット越しの無防備な利用**：HTTP の FullHTTP モードは、Bearer トークンとファイアウォール越しに別 PC からも到達できる設計です。ただし UAIP は開発者マシンや信頼できる社内 CI を前提としており、インターネットへ直接公開することは想定していません。必要な場合は VPN・リバースプロキシ・IP 制限などを運用側で担保してください。詳細は [セキュリティ → 脅威モデル](security.md#脅威モデル) を参照

---

## 関連リンク

- [クイックスタート](quickstart.md) — 5 分でセットアップ
- [使用例集](cookbook.md) — 動かせるレシピ集
- [デモ版ガイド](demo.md) — 製品版なしで使える範囲
- [ロードマップ](roadmap.md) — 計画中の機能
- [セキュリティ](security.md) — デプロイ環境の強化方針

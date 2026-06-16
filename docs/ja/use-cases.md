**[English](../en/use-cases.md)** | [概要に戻る](overview.md)

# ユースケース

誰が UAIP を何のために何故使うのか。各シナリオは関連 Cookbook レシピと必要 Capability にリンクします。

> コピペ可能な JSON が欲しければ [Cookbook](cookbook.md) を参照してください。本ページは「なぜ・いつ」側です。

---

## 1. AI 駆動テスト作成・QA

**誰**: QA / テスト自動化エンジニア、プレイテストスクリプトを所有するゲームプレイプログラマー。

**課題**: PIE スモークテストを手書きするのは遅く、レベルレイアウトが変わるとすぐに腐ります。AI エージェントは「このマップでプレイヤーを動かして異常を報告する」のは得意ですが、実際にゲームを動かせるのが前提です。

**UAIP が提供するもの**:
- `UAIP.Runtime.PIE.*` で start / stop / map ロード
- `UAIP.Runtime.Input` と `UAIP.Editor.UIAutomation.*` で実際の操作
- `UAIP.Runtime.Observation.CheckpointCapture` で固定タイミングにスクショ + 状態証跡を残す
- `UAIP.Runtime.Assertion.AssertActorProperty` / `AssertWorldState` で宣言的事後条件
- シナリオで全体を 1 つの監査可能なレコードに

**必要 Capability**: `PIEControl`・`RuntimeCapture`・`RuntimeInspect`（すべて DefaultAllow）。キャラクタ操作には `RuntimeActorManipulation` と `RuntimeInputInjection`。

**Cookbook**: [PIE スモークテスト](cookbook.md#1-pie-スモークテスト)、[PIE プレイテスト + キャプチャ](cookbook.md#6-pie-プレイテスト--キャプチャ)。

---

## 2. AI コードレビュー・Blueprint レビュー

**誰**: リードプログラマ、PR 最初のレビューワーに LLM を使う方。

**課題**: Blueprint 中心のプロジェクトのコードレビューは難しい — グラフが視覚的、diff ツールがあまり役立たず、「重要な変更があったか？」を判断するにはエディタを開く必要がある。シンプルな PR で人間に毎回開かせるのは無駄。

**UAIP が提供するもの**:
- `UAIP.Editor.Assets.OpenAsset` で BP をフォーカス
- `UAIP.Editor.Workspace.NormalizeEditorLayout` でスクショを再現可能に
- `UAIP.Editor.Observation.CaptureGraphViewportImage` で AI にグラフを見せる
- `UAIP.Editor.Blueprint.ListBlueprintPins` でピクセル単位ではなく構造的推論
- `UAIP.Editor.Observation.DumpEditorState` で他に何が開いているかも AI が把握

**必要 Capability**: `EditorInspect`・`EditorObservation`・`EditorWorkspaceControl` — すべて DefaultAllow。**書き込み Capability 不要** — デモバイナリで十分。

**Cookbook**: [AI コード / Blueprint レビュー](cookbook.md#2-ai-コード--blueprint-レビュー)。

---

## 3. アセット監査・クリーンアップ

**誰**: テクニカルアーティスト、コンテンツリード、プロジェクト規約を守らせる役。

**課題**: スケールすると「`BP_FooBar` は `/Characters/Heroes/` に置くべき、`/Misc/` ではない」のようなルールが常時ドリフトします。5000 アセットのプロジェクトで違反を特定するのはスクリプト作業。スクリプトはエディタ変更で壊れる。

**UAIP が提供するもの**:
- `UAIP.Editor.Assets.SearchAssets` でパス / クラス / タグ別の列挙
- `UAIP.Editor.Property.GetAssetProperty` で特定フィールド検査
- `UAIP.Editor.GameplayTags.FindGameplayTagReferencers` でタグ使用追跡
- エディタ UI 変更に強い意味的コマンド面

**必要 Capability**: `EditorInspect`（DefaultAllow）。AI に違反を報告するだけでなく修正もさせるなら `AssetDelete` / `AssetFolderRefactor` を追加。

**Cookbook**: [アセット監査・命名チェック](cookbook.md#3-アセット監査命名チェック)。

**ロードマップ近接**: より深い依存関係解析（未参照アセット検出、循環参照、サイズマップ）は計画中・未実装。[ロードマップ → アセット参照解析・SizeMap](roadmap.md#アセット参照解析sizemap) を参照。

---

## 4. エディタ側 AI ペアプログラミング

**誰**: Claude Code / Cursor / Copilot を主 IDE として使うソロ開発者・小規模チーム。

**課題**: AI は C++ パッチ生成は得意ですが、UE プロジェクトの Blueprint 側だと盲目に。「このウィジェットをこのイベントに繋いで」はソースで完結せず、BP グラフがソースそのもの。

**UAIP が提供するもの**:
- `UAIP.Editor.Blueprint.*` で変数追加、ノード追加、ピン配線
- `UAIP.Editor.UMG.*` でウィジェットツリー・アニメーション・バインディング編集
- `UAIP.Editor.Level.*` でアクター配置、トランスフォーム調整
- `UAIP.Editor.Property.*` でアセット・アクターのフィールド設定
- `CompileBlueprint` + エラー取得（計画中、[ロードマップ → Blueprint Compile / コンパイルエラー取得](roadmap.md#blueprint-compile--コンパイルエラー取得) 参照）で編集→検証ループを閉じる

**必要 Capability**: `BlueprintEdit`・`BlueprintGraphEdit`・`BlueprintVariableEdit`・`WidgetTreeEdit`・`EditorActorEdit`・`PropertyEdit` — すべて DefaultDenied。ワークフローに必要なものだけ有効化（[セキュリティ → フル編集プロファイル](security.md#推奨セキュリティプロファイル) 参照）。

**Pro 版限定** — 編集モジュールはデモバイナリに含まれません。

**Cookbook**: [Blueprint 編集→検証ループ](cookbook.md#4-blueprint-編集検証ループ)。

---

## 5. エディタ拡張の UI 自動化テスト

**誰**: プラグイン作者、エディタユーティリティを作るツールプログラマー。

**課題**: カスタムエディタツールのテストはメニュークリック・フォーム入力・ダイアログ確認が必須。毎リリース手動、座標スクリプティングは脆い。

**UAIP が提供するもの**:
- `SelectMenuItem`・`ClickWidget`・`InputText`・`SetCheckboxState`・`SetComboSelection` で入力
- `WaitForWidget` で同期（`Sleep` ハック不要）
- `AcceptDialog` / `CancelDialog` でモーダル処理
- `CaptureActiveWindowImage` で視覚的リグレッション証跡

**必要 Capability**: `EditorUIAutomation`（DefaultAllow）。`PressKey` 用に `EditorKeyboardInput`。`InvokeContextMenuAction` 用に `AllowContextMenuMutation`。

**Cookbook**: [UI 自動化テスト](cookbook.md#5-ui-自動化テスト)。

---

## 6. プロシージャルコンテンツワークフロー

**誰**: PCG ユーザー、プロシージャルアーティスト、テクニカルデザイナー。

**課題**: PCG ノードパラメータ調整は反復的 — 値を変えて、再生成し、結果を確認、繰り返し。1 ノードならエディタ手動で良いが、数十ノードのグラフ全体だと面倒。

**UAIP が提供するもの**:
- `UAIP.Editor.PCG.GetPCGGraphInfo` でグラフ構造取得
- `UAIP.Editor.PCG.SetPCGNodeProperty` でパラメータ変更
- `UAIP.Editor.PCG.ExecutePCGGraph` で再生成
- `CaptureViewportImage` / `DumpWorldState` で結果確認
- シナリオで値域パラメータスイープしつつ各ステップでスクショ

**必要 Capability**: `PCGGraphEdit`（DefaultDenied、`PCG` プラグイン必須）。カスタムノードプロパティには `PCGCustomNodeEdit` / `PCGBlueprintNodeEdit`。

**Pro 版限定** — PCG 編集はデモ版にありません。

---

## 7. アニメーションパイプライン統合

**誰**: アニメーションテクニカルアーティスト、AnimBlueprint オーナー、ControlRig ユーザー。

**課題**: 複雑なアニメツリーは大きく、AnimGraph ステート・ステートマシン遷移・ControlRig リグ・Sequencer シネマティックの関係を壊しやすい。視覚的検証は必要だが、変更毎にやるのは非現実的。

**UAIP が提供するもの**:
- `UAIP.Editor.AnimBlueprint.*` で AnimGraph + StateMachine 編集
- `UAIP.Editor.ControlRig.*` でヒエラルキー + RigVM グラフ編集（ネイティブ 59 + Toolset 44）
- `UAIP.Editor.Sequencer.*` で LevelSequence 編集（ネイティブ 93 + Toolset 61）
- `UAIP.Editor.Skeleton.*` でソケット / バーチャルボーン管理
- `UAIP.Editor.Physics.*` で物理アセット調整
- `UAIP.Runtime.PIE.*` 経由の Runtime チェック + Anim 観測（計画中、[ロードマップ → AnimInstance Runtime 状態](roadmap.md#animinstance-runtime-状態) 参照）

**必要 Capability**: `AnimBlueprintGraphEdit`・`AnimStateMachineEdit`・`ControlRigGraphEdit`・`ControlRigHierarchyEdit`・`SequencerStructureEdit`・`SequencerKeyframeEdit`・`SkeletonAssetEdit`・`PhysicsAssetEdit`・`PhysicsBodyEdit` — すべて DefaultDenied。

**Pro 版限定**。

---

## 8. マルチプレイヤー・ゲームプレイシステムデバッグ

**誰**: PIE 専用バグを追うゲームプレイプログラマー。

**課題**: 「Standalone では動くがマルチプレイで壊れる」「X が起きると AI がプレイヤーを認識しない」。リプロは PIE が必要、バグ解析は Replicated 状態・AI Perception 状態・BehaviorTree アクティブノード・GameplayAbility 状態等の読み取りが必要。エディタのデバッグ UI でやると一度に一視点ずつ。

**UAIP が提供するもの**:
- `UAIP.Runtime.Observation.DumpWorldState` で全体像
- `UAIP.Runtime.GAS.*` でアビリティ / 属性 / エフェクト検査
- 計画中: AI Perception、BT / StateTree Runtime 状態、AnimInstance 状態、Network / Replication 状態（[ロードマップ → Runtime 検査・デバッグ](roadmap.md#runtime--検査デバッグ)）
- シナリオで不正状態を再現し証跡を一度に捕捉

**必要 Capability**: `PIEControl`・`RuntimeInspect`・`RuntimeGASInspect`（すべて DefaultAllow）。編集には `RuntimeActorManipulation`。

---

## 9. コンテンツコンプライアンス / Pre-submit ゲート

**誰**: ビルドエンジニア、社内ツールメンテナンス担当。

**課題**: 「誰かがコンパイル通らない Blueprint をコミットしたか」「誰かが `/Game/Tests/` にアセットを追加したか」 — Pre-submit ゲートにすべきだが、C++ で書くにはカスタム commandlet を cook する必要があり、反復・ロールアウトが遅い。

**UAIP が提供するもの**:
- CLI transport（Pro 版）で Pre-submit フック / CI でのヘッドレス one-shot 実行
- `UAIP.Editor.Execution.RunAutomationTest` でテスト側
- 計画中: `ValidateAsset` / `ValidateFolder`（[ロードマップ → アセット検証（Validation）](roadmap.md#アセット検証validation)）
- 計画中: Build / Package パイプライン（[ロードマップ → Build / Package パイプライン](roadmap.md#build--package-パイプライン)）

**必要 Capability**: `EditorInspect`・`EditorExecution`（DefaultAllow）。

**Cookbook**: [CI から Automation Test を実行（Pro）](cookbook.md#7-ci-から-automation-test-を実行pro)。

**現実的な注意**: 現状の CI 統合は実用可能だが粗い（エディタ起動遅、デモ版 CLI 非対応、検証プリミティブはロードマップ段階）。コミット毎のサブ秒 lint ではなく、ビルド検証スタイルのユースケース向け。

---

## 10. ライブオプス / データ駆動バランシング

**誰**: ゲームプレイデザイナー、ライブオプスエンジニア。

**課題**: ゲームプレイ定数は DataTable・Blueprint デフォルト・プロジェクト設定に分散。バランス反復はエンジニアが各々を手編集するか、使い捨てツールを書くか。

**UAIP が提供するもの**:
- `UAIP.Editor.DataTable.*` で行 CRUD と CSV インポート / エクスポート
- `UAIP.Editor.Property.GetBlueprintDefault` / `SetBlueprintDefault` で CDO 調整
- `UAIP.Editor.Property.GetProjectSetting` / `SetProjectSetting` で `UDeveloperSettings` 系設定
- `UAIP.Runtime.GAS.*` で PIE 内の属性 / アビリティ状態への効果検証

**必要 Capability**: `DataTableRowEdit`・`DataTableImport`・`BlueprintEdit`・`ProjectConfigEdit` — DefaultDenied。

**Pro 版限定**。

---

## UAIP を **使うべきでない** ケース

- **本番ユーザー向けの自動化** — UAIP は dev / CI 用に作られており、出荷ゲームの操舵用ではありません。Runtime ゲームプレイにはエンジン自体のサブシステム（Gameplay Abilities・オンラインサービス等）を使ってください
- **サブ秒の反復ループ** — エディタ起動は遅い。10 ms レスポンスが必要なら UE プラグインを直接書く
- **IDE 置き換え** — UAIP は C++ ソースを編集しません。コード変更には IDE を使い、UAIP はエディタ内に住むプロジェクト部分に使う
- **マルチテナントデプロイ** — UAIP は「プロジェクト 1 つにエディタ 1 つ」。1 つの Bridge を複数同時ユーザーで共有しないこと
- **信頼できない公開** — UAIP は localhost 限定でホストユーザーを信頼する。[セキュリティ → 脅威モデル](security.md#脅威モデル) 参照

---

## 関連リンク

- [クイックスタート](quickstart.md) — 5 分でセットアップ
- [Cookbook](cookbook.md) — コピペ可能なレシピ
- [デモ版ガイド](demo.md) — Pro 版なしで使える範囲
- [ロードマップ](roadmap.md) — 計画中の機能
- [セキュリティ](security.md) — デプロイの強化方法

**[English](../en/changelog.md)** | [概要に戻る](overview.md)

# 更新履歴

UAIP プラグインのリリースごとの変更点をまとめたページです。各バージョン番号の意味（破壊的変更が含まれるかなど）については、まず冒頭の「バージョニング方針」を確認してください。

---

## バージョニング方針

UAIP は [Semantic Versioning 2.0.0](https://semver.org/lang/ja/) に従ってバージョニングを行います。

### バージョン番号の読み方

バージョン番号は `MAJOR.MINOR.PATCH` の 3 セグメント形式です。

| セグメント | 意味 |
|---|---|
| **MAJOR**（例: `1.x.x` → `2.x.x`）| 破壊的変更を含む。アップグレード時にコマンド名・パラメータ・設定ファイルの修正が必要になる可能性がある |
| **MINOR**（例: `1.0.x` → `1.1.x`）| 後方互換な機能追加。新コマンド・新 Capability・新オプションパラメータなど。既存呼び出しはそのまま動作する |
| **PATCH**（例: `1.0.0` → `1.0.1`）| バグ修正のみ。公開 API への影響なし |

### 現在のフェーズ：1.x.y（Fab 製品版公開済み）

現行バージョンは **1.1.0** で、UAIP は **Fab で製品版として公開済み**（[リスティング](https://www.fab.com/listings/0eedf909-00ac-4d95-b109-8fda51800fff)）です。1.x.y 系列の初回エントリである 1.0.0 からの変更点は、下記のリリース一覧を参照してください。

- 以降は通常の SemVer ルールが厳格に適用されます。破壊的変更には MAJOR バンプ（`2.0.0` など）が必要
- 新コマンド・新 Capability 追加は MINOR バンプ（例: `1.0.x` → `1.1.0`）
- バグ修正は PATCH バンプ（例: `1.0.0` → `1.0.1`）

### 1.0 以前の履歴：0.x.y 系列

`0.9.0` / `0.9.1` は Fab 製品版リリース前に GitHub Releases で先行配布したデモ版バージョンです。エントリは履歴として下記に残しています。

### Pre-release タグ

通常は pre-release タグを使用しません。Fab 公開直前に最終確認版を配布する場合のみ、`1.0.0-rc.1` 形式の RC（リリース候補）タグを GitHub Releases に切る場合があります。RC は Fab 提出版と完全に同一のコードで、問題がなければそのまま `1.0.0` として正式公開します。

### Deprecation 方針（基本削除しない）

UAIP はエンジンバージョンごとにブランチを分けず、バージョンマクロで実装を切り替える方針を採用しています。そのため **一度公開したコマンドは原則として削除しません**。

- 廃止予定のコマンドは `Stability: "Deprecated"` に分類されますが、引き続き動作します
- `uaip_describe_command` で `DeprecationMessage` と `MigrationTarget`（推奨移行先）を確認できます
- 例外として、**Epic 社がエンジン側 API を削除し UAIP 側で実装維持が物理的に不可能になった場合** のみ、MAJOR バンプ時に削除を行います

これにより、AI エージェントに学習・記憶された古いコマンド名でも長期的に動作することを保証します。

### デモ版と製品版のバージョン番号

デモ版（GitHub Releases）と製品版（Fab）は **常に同じバージョン番号** を共有します。同一ソースから機能制限のみを切り替えてビルドしているため、HealthCheck コマンドの `UAIPVersion` フィールドも両者で同じ値を返します。

---

## リリース一覧

> 未リリース・開発中の変更は [`next` ブランチの更新履歴](https://github.com/Naotsun19B/UnrealAIIntegrationPlatform-Document/blob/next/docs/ja/changelog.md) で確認できます。

### Unreleased

プラグインリポジトリには取り込み済みですが、Fab 未リリースの変更です。

#### UAIP Plugin

**追加**

- **アセット検証（ジョブ実行・同期実行の 2 経路）**（`UAIPEditorValidation` モジュール、**新規**、`DataValidation` プラグイン必須、**Pro 版限定** — デモ版では利用不可）: AI エージェントが、プロジェクトの登録したアセットバリデータを実行し、検出内容を構造化された結果として読み、バリデータが提供する修正を適用できるようになりました。`UAIP.Editor.Validation` 配下に 7 コマンドを追加 — `ListValidators`（どのバリデータが有効か、マテリアル検証がそもそも実行可能か）、`ValidateAssets`（最大 8 件を同期・エンジンへの 1 回の呼び出しで検証）、`StartValidationJob` / `GetValidationJobStatus` / `GetValidationJobResult` / `CancelValidationJob`（フォルダや大量のリストを少しずつ検証し、エディタを操作可能なまま保つ）、`ApplyValidationFix`。DefaultDenied の Capability を 2 つ追加: `AssetValidation`（バリデータの実行 — エンジンが副作用を禁じていないプロジェクト提供コードの実行）と `AssetValidationFix`（アセットの書き換え）。UAIP は独自の品質ルールを持たず、判定はすべて `UEditorValidatorSubsystem` に由来します。⚠️ `DataValidation` をプロジェクトの `.uproject` で**明示的に**有効化していないと、これらのコマンドは一つも登録されません。またマテリアル検証には `MaterialValidationPlatforms` の設定とエディタ再起動が別途必要です。チャンク実行するジョブの結果は 1 回の呼び出しで検証した場合と一致するとは保証されず、修正はプロジェクトが自作したバリデータからしか現れません（エンジン同梱バリデータは修正を 1 つも生成しません）。
- **AnimNotify 編集**（`UAIPEditorAnimSequence` モジュール、**新規**、**Pro 版限定** — デモ版では利用不可）: AI エージェントが `UAnimSequence` / `UAnimMontage` / `UAnimComposite` アセット上の AnimNotify / AnimNotifyState エントリと通知トラックを追加・削除・編集できるようになりました。ロード後に不安定になった通知 guid の修復も可能です。`UAIP.Editor.AnimSequence` 配下に 11 コマンドを追加しました — 読み取り専用の `GetAnimNotifyInfo`・`GetAvailableAnimNotifyClasses`・`GetAnimNotifyClassSchema`（要 `EditorInspect`）、トラック管理の `AddAnimNotifyTrack` / `RemoveAnimNotifyTrack`、通知の配置・削除 `AddAnimNotify` / `AddAnimNotifyState` / `RemoveAnimNotify`、イベントフィールド編集 `SetAnimNotifyEvent`、通知インスタンス単位の汎用プロパティ書き込み `SetAnimNotifyProperty`、guid 修復 `FixupAnimNotifyGuids`。2 つの DefaultDenied Capability を追加しました：`AnimNotifyEdit`（全編集系コマンドで必須）と `AnimNotifyReferenceEdit`（`SetAnimNotifyProperty` がハードなオブジェクト/クラス参照であるか、それを内包するプロパティへ書き込む場合に `AnimNotifyEdit` に加えて必要）。エンジン標準の AnimNotify 型のみで構成されており、オプションプラグインは不要です。編集系コマンドはすべて PIE または SIE 実行中は拒否されます。
- **`SynchronizePoseSearchDatabase`**（`UAIPEditorMotionMatching` モジュール）: AI エージェントが、PoseSearchBranchIn アニメーション通知のエントリを `UPoseSearchDatabase` の `AnimationAssets` へ明示的にマージできるようになりました。エンジンにはこのマージが自動的に起きたことを観測できる確実な手段がないためです。`UAIP.Editor.MotionMatching` 配下に 1 コマンドを追加しました（要 `PoseSearchAssetEdit`）。⚠️ 参照元のアニメーションアセットの保存と同じリクエスト内で呼ぶと 0 件になる場合があります。アセットレジストリの参照インデックスは保存後に非同期で再構築されるため、保存が落ち着いてから再実行してください。
- **MetaHuman キャラクター編集**（`UAIPEditorMetaHuman` モジュール、**新規**、`MetaHumanCharacter` プラグイン必須、**Pro 版限定** — デモ版では利用不可）: AI エージェントが MetaHuman キャラクターを一貫して作成・編集できるようになりました — アセットの新規作成、体型 / 肌 / 眼 / メイク / ヘッドモデル / 顔評価設定、顔の造形、ターゲットメッシュへのコンフォーム・フィッティング、ワードローブ管理、プレビュービューポート操作、クラウドリギングと高解像度テクスチャ合成のリクエスト、アセットビルドパイプラインの実行。`UAIP.Editor.MetaHuman` 配下に 56 コマンドを追加しました — 作成（`CreateMetaHumanCharacter`）、体型・肌・眼（`GetBodyConstraints`・`SetBodyConstraints`・`GetBodyShape`・`SetBodyShape`・`GetSkinSettings`・`SetSkinTone`・`GetEyeSettings`・`SetEyeColor`）、外見詳細（`SetSkinSettings`・`GetMakeupSettings`・`SetMakeupSettings`・`GetHeadModelSettings`・`SetHeadModelSettings`・`SetEyeSettings`・`GetFaceEvaluationSettings`・`SetFaceEvaluationSettings`）、顔の造形（`GetFaceModelCoefficients`・`SetFaceModelCoefficients`・`GetFaceLandmarks`・`TranslateFaceLandmarks`・`CommitFaceState`・`ImportFaceFromDna`・`ImportFaceFromTemplate`・`ImportFaceFromIdentity`・`CompareFaceState`）、コンフォームとフィッティング（`GetMeshDataForConforming`・`ConformBodyToTarget`・`ConformFaceToTargetMeshes`・`AlignToTargetMeshes`・`RefineVerticesToTarget`・`CommitPosedStateAsAPose`・`FitStateToTargetVertices`・`FitFaceFromBodyWithEyesTeethTemplate`・`FitFaceFromBodyWithEyesTeethDna`・`GetAsyncConformState`）、ビルドパイプライン（`RequestTextureSources`・`GetTextureSourceState`・`RequestAutoRigging`・`GetRiggingState`・`CanBuildMetaHuman`・`BuildMetaHuman`）、プレビュー（`GetViewportSettings`・`SetViewportSettings`・`RefreshCharacterPreview`）、ワードローブ（`ListWardrobeSlots`・`ListWardrobeItems`・`GetWardrobeItemInfo`・`AssignWardrobeItem`・`RemoveWardrobeItem`・`ReplaceWardrobeItem`・`GetWardrobeItem`・`SetWardrobeItem`・`SetWardrobeItemPipeline`・`ListItemPipelineClasses`）、セッション管理（`ReleaseEditSession`）。6 つの DefaultDenied Capability（`MetaHumanAssetCreate`・`MetaHumanEdit`・`MetaHumanFileImport`・`MetaHumanTextureSynthesis`・`MetaHumanCloudRigging`・`MetaHumanBuild`）を追加しました。編集系コマンドは必要に応じて編集セッションを開いて保持するため、**このドメインの読み取り系コマンドの多くは読み取り専用ではありません** — `MetaHumanEdit` を必要とし、読み取り専用の SafetyPolicy 下では拒否されます（唯一の例外は `GetViewportSettings` で `EditorInspect` のみで実行できます）。⚠️ `RequestAutoRigging` は **キャラクターの顔データを Epic のクラウドリギングサービスへアップロード** するため、Epic アカウントへのサインインとネットワーク接続が必要です。⚠️ `BuildMetaHuman` はビルド完了までゲームスレッドを占有します（数秒〜数分）。エンジンが進捗ダイアログを表示して再描画を続けるため、エディタは応答しなくなるのではなく画面を見られる状態を保ちますが、ビルドが返るまで他のコマンドは一切実行されません。これは MCP ブリッジの freeze 検知（30 秒）と既定のコマンドタイムアウト（60 秒）を超えるため、呼び出し前に `command_timeout_seconds` を引き上げ、先に `CanBuildMetaHuman` を呼んでください。56 コマンドのうち 14 コマンド（`GetFaceModelCoefficients`・`SetFaceModelCoefficients`・`ConformFaceToTargetMeshes`・`AlignToTargetMeshes`・`RefineVerticesToTarget`・`GetAsyncConformState`・`CommitPosedStateAsAPose`・`FitFaceFromBodyWithEyesTeethTemplate`・`FitFaceFromBodyWithEyesTeethDna`・`GetMeshDataForConforming`・`AssignWardrobeItem`・`RemoveWardrobeItem`・`ReplaceWardrobeItem`・`RefreshCharacterPreview`）は UE 5.8 のエンジン API に依存します。UE 5.7 でも登録はされますが `Available: false` となり、実行すると `PolicyViolation` を返します。あわせて `Toolset.Editor.MetaHuman.*` 配下に 9 つの Toolset ブリッジコマンド（`BeginEdit`・`EndEdit`・`GetBodyShape`・`SetBodyShape`・`GetSkinTone`・`SetSkinTone`・`GetEyeColor`・`SetEyeColor`・`Create`）を追加しました。`MetaHumanGenerator` Python Toolset へ委譲するもので、UE 5.8+ かつ `MetaHumanGenerator` + `ToolsetRegistry` 有効時のみ利用でき、UE 5.7 では登録されません。

- **Unreal Insights のトレース採取と解析**（`UAIPRuntimeInsights` モジュール、**新規**）: AI エージェントが Unreal Insights のトレースを採取し、採取中に目印を書き込み、採取済みトレースをオフラインで解析できるようになりました。`UAIP.Runtime.Insights.Trace` 配下に 11 コマンド — 読み取り `ListTraceChannels`・`GetTraceStatus`・`ListTraceFiles`、制御 `StartTrace`・`StopTrace`・`PauseTrace`・`ResumeTrace`・`SetTraceChannels`・`AddTraceBookmark`・`BeginTraceRegion`・`EndTraceRegion` — と、`UAIP.Runtime.Insights.Analysis` 配下に 3 コマンド（`AnalyzeTrace`・`GetTraceAnalysisStatus`・`GetTraceAnalysisResult`）を追加しました。解析側はトレース解析が有効なビルド構成でのみ登録され、それ以外では `CommandNotFound` を返します。Capability を 4 つ追加しました: `RuntimeInsightsInspect`（DefaultAllow）と `RuntimeInsightsControl`・`RuntimeInsightsAttachTraceFile`・`RuntimeInsightsAnalyze`（いずれも DefaultDenied）。新しい artifact 型 `Trace` と、SafetyPolicy キー 3 つも追加しました: `AllowExternalTraceAnalysis`・`ExternalTraceDirectory`（**両方が設定されて初めて有効**。UAIP 以外が採取した `.utrace` を `AnalyzeTrace` で読めるようにするもので、当該ディレクトリ内のシンボリックリンクは解決されないため UAIP 専用の隔離ディレクトリを指定してください）と、`AllowDisclosingTraceAttachment`（採取した `.utrace` のチャネルがホスト側パス・画面内容・ネットワークアドレスを記録しえた場合に、そのファイルを artifact として引き渡すことを許可します。ログテキストの開示は引き続き `AllowLogDump` が担い、このビルドが分類していないチャネルは両方の設定に関わらず拒否されます）。トレースは常に `Saved/Profiling/UAIP/` 配下のファイルへ書き出され、本モジュールのどのコマンドもネットワーク宛先へ送出できません。加えて `UAIP.Runtime.World.ExecuteConsoleCommand` の deny-list に `trace.` プレフィックスを追加してコンソール経由の経路も塞いでいます（ただし `RunEditorPythonScript` からはエンジンのトレースシステムへ依然到達可能であり、これは当該コマンドが要求する Capability の付与判断で管理されます）。チャネルは開示しうる内容で分類され、実効チャネル集合（既に有効 ∪ 要求）がログテキストを記録し `AllowLogDump` が false の場合、`StartTrace` は `PolicyViolation` で拒否されます。解析は非同期で同時実行は 1 件のみで、パース中 / 抽出中に届いた要求は `TooManyRequests` で拒否されます。このときエラーメッセージには枠を占有している解析の `AnalysisId` が含まれるため、当てずっぽうに再試行するのではなく `GetTraceAnalysisStatus` で監視できます。要求した各セクションは個別の JSON artifact として書き出されます。解析は開始したセッションに属します — `GetTraceAnalysisStatus` / `GetTraceAnalysisResult` が `AnalysisId` を見つけられるのは `AnalyzeTrace` と同じ `SessionId` で呼ばれた場合だけで、他のセッションからは `NotFound` になります。これは存在しない ID に対する応答と意図的に同一で、他の呼び出し元の解析が存在するかどうかを推測する手段にはなりません。`SessionId` を省略するとこの経路は成立しません（トランスポートが呼び出しごとに別の匿名セッションを作るため、そうして開始した解析は二度と照会できません）。⚠️ 生の `.utrace` の添付（`StopTrace` の `AttachTraceFile: true`）は、チャネル構成に関わらずプロセスのコマンドラインを必ず開示します（列挙も無効化もできない常時オンの内部チャネルに書き込まれるため）。専用 Capability `RuntimeInsightsAttachTraceFile` でゲートしているのはこのためであり、サニタイズ済みのコマンドラインを返す解析側の `Diagnostics` セクションとはファイル本体の開示レベルが異なります。また、エディタはエンジン自身が起動時に log / bookmark / region / screenshot チャネルを有効化するため、エディタで採取したトレースの添付には実際上 `AllowLogDump=True` と `AllowDisclosingTraceAttachment=True` の**両方**が必要です。これから記録するチャネル構成ではファイルを引き渡せない場合、`StartTrace` が `AttachDisabledByPolicy` warning で事前に通知します。停止しただけでは採取ファイルは閉じられない（エンジンのトレースライタが少し遅れて別スレッドで閉じる）ため、ファイルを要求した `StopTrace` は最大 3 秒まで解放を待ち、それでも書き込み中なら `AttachSkippedReason: "TraceFileStillOpen"` を返します（少し待ってから再度要求する価値があります）。ファイルを要求しなかった停止は待機しません。デモ版には読み取り 3 コマンドのみが含まれ、解析側 Provider はコンパイル自体から除外されます。

- **アセット監査がゲームスレッドを占有せずジョブとして実行されるようになりました**（`UAIPEditorAssets` モジュール）：大きなコンテンツフォルダの監査は完了までゲームスレッドを占有し、数十秒〜数分にわたってエディタと他のすべての UAIP コマンドを止めていました。しかも呼び出し側からは、動作中の監査とハングしたエディタを区別できませんでした。`UAIP.Editor.Assets` 配下に読み取り専用の 3 コマンドを追加しました。`StartAssetAudit` はジョブを登録して `AuditId` を即座に返し、以降の走査はエディタのフレームの合間で少しずつ進むため、走査中もエディタは操作でき他のコマンドにも応答し続けます。`GetAssetAuditStatus` は `State`（`Preparing` / `Running` / `Completed` / `Failed`）、処理中のレポート種別、処理済み/総件数、経過秒数、走査中に消えて飛ばしたアセットの件数、失敗理由を返します。`GetAssetAuditResult` はジョブが `Completed` になった後、レポートごとの artifact を返します。3 コマンドとも必要な Capability は `EditorInspect` のみで（新規 Capability の追加はありません）、**`SessionId` の明示指定が必須**です（匿名セッションは `InvalidParams` で拒否されます。呼び出しごとに別物になる匿名セッションで開始したジョブは、後から照会も取得もできなくなるためです）。ジョブは開始したセッションからのみ見えます — 未知・期限切れ・他セッションの `AuditId` はいずれも区別されず `NotFound` になります。監査の同時実行は 1 本のみで（それ以外は `TooManyRequests`。`AuditId` が併記されるのは自分が投げた監査の場合だけです）、エディタがモーダルダイアログやプログレスバーを表示している間は開始が `NotAllowed` で拒否され、走査中に表示された場合は失敗ではなく一時停止になります。再投入には同一セッション単位のレート制限に加えて、直近に監査が消費したエディタ時間に基づく全セッション横断の制限がかかります。エディタ時間を 10 分消費したジョブは、走らせ続けるのではなく失敗として打ち切られます（待ち時間ではなく実消費時間で数えます）。完了したジョブは 15 分保持され、結果取得に成功するたびに保持期間が延長されますが、開始から 1 時間で確実に破棄されます。またセッション終了時・ライブコーディングのリロード時・エディタ終了時にも破棄されるため、**結果はセッションを終了する前に取得してください**。1 フレームあたり走査に使う時間は `Config/DefaultUAIP.ini` の `[UAIP.Jobs] AuditStepBudgetMs` で変更できます（既定 `10.0`、`[1.0, 100.0]` にクランプ）。詳細は [設定リファレンス → `[UAIP.Jobs]`](config.md#uaipjobs--ジョブ型コマンドの-1-フレームあたりの予算) を参照してください。⚠️ `FindUnreferencedAssets` / `FindCircularReferences` / `FindBrokenReferences` / `RunAssetAudit` は `Deprecated` になり、`MigrationTarget` として `StartAssetAudit` が案内されます。**動作はこれまでと完全に同じです**（結果も進捗発火も変わりません）。ただし監査の間ゲームスレッドを占有する点も従来どおりであり、それが移行を推奨する理由です。あわせて循環参照レポートの誤報告を修正しました。最後の起点アセットを調べている最中に出力件数の上限へ達した場合、「切り詰めていない」と報告されていました。報告される循環参照の中身と順序は変わりません。

- **`AddAnimationToPoseSearchDatabase` に、自身の冪等性判定を迂回する opt-in を追加しました**（`UAIPEditorMotionMatching` モジュール）。このコマンドは元々、通常（非 BranchIn）エントリとしてすでに登録済みのアニメーションに対しては冪等でした — 再度追加しようとすると、新規エントリを作らずに既存エントリの `Index` を返します。しかし、これでは異なるエントリ設定で同じアニメーションを意図的に複数回登録する手段がありませんでした（`UPoseSearchDatabase` の正当な用途であり、エディタ UI では元々可能な操作です）。新しい任意パラメータ `bAllowDuplicate`（既定 `false`）を `true` に設定すると、この判定を迂回します — コマンドは常に新しいエントリを追加し、`InsertAt` とすべての設定フィールドは初回追加時と同じように適用され、応答は新エントリの `Index` を `bAlreadyPresent: false` とともに返します。既定の挙動は変わっていません — パラメータを省略すれば、これまでと全く同じ冪等な挙動のままです。

- **ControlRig コンポーネントの型付き編集 — 汎用 CRUD と 2 つの型付きドメイン**（`UAIPEditorControlRig` モジュール）: AI エージェントが、汎用のヒエラルキー要素コマンドを介さずに、ControlRig ヒエラルキーのコンポーネント（`FRigBaseComponent` サブ構造体）を直接アタッチ・参照・変更できるようになりました。`UAIP.Editor.ControlRig` 配下に、モジュールのアローリストが対象とするすべてのコンポーネント型に対して動作する汎用コンポーネントコマンドを 9 つ追加しました（`ListComponents`・`GetComponent`・`ListAddableComponentTypes`・`CanAddComponent`・`AddComponent`・`RemoveComponent`・`RenameComponent`・`ReparentComponent`・`SetComponentContent`）。同じコンポーネント群に対して型付きドメインを 2 つ追加しました: `UAIP.Editor.ControlRig.Dynamics`（16 コマンド — 型付き読み取り 6・型付き書き込み 6・ソルバー / パーティクル / コンストレイントの一式をまとめて構築・つなぎ直すオーケストレーションコマンド 4。`Experimental`。`ControlRigDynamics` プラグインを `.uproject` で明示的に有効化する必要があり、UE 5.8 以降限定）と `UAIP.Editor.ControlRig.Physics`（8 コマンド — ソルバー / ボディ / ジョイント / コントロールの型付き読み取り 4・書き込み 4。`Stable`。`ControlRigPhysics` プラグインを `.uproject` で明示的に有効化する必要があり、UE 5.8 に加えて UE 5.7 でも利用可能）。DefaultDenied の Capability を 1 つ追加しました: `ControlRigComponentEdit`。汎用コマンドと 2 つの型付きドメインの全書き込みが共通で要求します — 初期コンテンツを指定したコンポーネントの新規作成が、既存コンポーネントのコンテンツ置き換えと同じインポート経路を通るため、意図的に 1 つの Capability に統合しています。全書き込みは PIE 実行中は拒否され、Physics ドメインの書き込みはさらに ModularRig アセットに対しても拒否されます。⚠️ `ControlRigDynamics` と `ControlRigPhysics` は、いずれもプロジェクトの `.uproject` の `Plugins` 配列で**明示的に**プラグインを有効化した場合にのみコマンドが登録されます — エンジンが既定で有効とみなすプラグイン（`ControlRigPhysics` はまさにそれです）であっても、この明示指定がなければ登録されません。

- **Slate のレイアウト識別子を指定して、任意のエディタタブを開閉できるようになりました**（`UAIPEditorWorkspace` モジュール）: これまで AI エージェントには、まだ開いていないタブを開く手段がありませんでした — `FocusEditorTab` は**既に開いている**アセットエディタを前面に出すだけで、`SelectMenuItem` によるメニュー操作代行は新しい `UToolMenus` フレームワークに登録されたタブにしか届かず、旧来の `FMenuBarBuilder` 系メニュー経由でしか開けないタブには構造的に到達できませんでした。`UAIP.Editor.Workspace` 配下に 3 コマンドを追加しました: `ListSpawnableTabs`（読み取り専用。開ける候補を、所属先の識別子・表示名・ツールチップ・その所属先が既に 1 つ開いているかどうかとともに列挙します。この一覧は網羅ではなく、応答自身がその旨を申告します）、`OpenTabById`（`TabId` と `OwnerTabId` を指定してタブを開きます。必要であれば所属先のウィンドウを先に開き、所属先を自分が開いたかどうかを応答に含めるため、呼び出し側は後始末の範囲を判断できます）、`CloseTabById`（同じ識別子の組で閉じます。同じ種類のタブが複数開いている場合は `InstanceId` で絞り込みます）。`OwnerTabId` に該当するウィンドウが複数開いている場合は、推測せず候補を列挙した `InvalidParams` で拒否し、エディタ側の許可設定で拒否されているタブは再試行される `ExecutionFailed` ではなく `NotAllowed` を返します。また `OpenTabById` は、対象タブ自体の生成に失敗した場合、自分が開いたものを内側から順に取り除きます。DefaultDenied の Capability を 1 つ追加しました: `EditorTabSpawn`。3 コマンドすべてが要求します — 任意のタブを開閉する操作は第三者プラグインのコード（`OnSpawnTab` / `OnCanCloseTab`、および読み取り専用の一覧が表示名・ツールチップを取得する際に呼ぶデリゲート）を実行しうるため、`ListSpawnableTabs` も読み取り専用ながら同じ Capability を要求します。⚠️ `EditorTabSpawn` を許可すると、AI エージェントは**自分が開いたタブに限らず、いま開いている任意のタブ**を閉じられるようになります。また、エディタ側の設定で表示を禁止しているタブ種別であっても、**既に開いていれば閉じられます** — 開く側にはその禁止設定が効きますが、閉じる側は意図的に対象外としています。設定変更によって後始末が失敗しないようにするためです。

**変更**

> **MAJOR に該当しない理由。** 本リリースには動作が変わる項目がいくつか含まれますが、いずれも SemVer の MAJOR には該当しません。該当する変更はそれぞれ、ドキュメント上は公開されていたが実際には到達不能だった契約の修正、`Experimental` コマンドの仕様変更、宣言された契約に反していた挙動の修正のいずれかです。`Stable` かつ宣言どおりに到達可能だった挙動が実際に変わる場合は、理由を問わず常に MAJOR とします。

- **コマンドパラメータがスキーマ宣言の型に対して検査されるようになりました**（`UAIPCore` モジュール）。従来は未知プロパティと必須フィールドの有無のみを検査し、値そのものは `FJsonObject::TryGet*Field` へ直接渡っていました。同 API の暗黙変換はほぼ何でも受け付けるため、`"yes"` がブール `true` として、`"abc"` が整数 `0` としてハンドラに届いていました。今後は dispatch 前にすべての値が宣言された `Type` と照合され、不一致は期待型と実際の型を示す `InvalidParams` として拒否されます。配列要素は `Items.Type` に対して 1 階層のみ検査し、`Integer` は小数部を持たないことも要求します。JSON `null` は「未指定」として扱うためハンドラ側の既定値処理には影響せず、認識できない型キーワードは制約を課しません。⚠️ **動作変更（要確認）— 従来の暗黙変換に依存していた呼び出しに影響します。** 特にシナリオでは型保存規則により、数値の `Variables` エントリを String 型パラメータへ差し込むと数値のまま届きます。`AssertActorProperty` の `ExpectedValue` へ渡す `"Variables": { "ExpectedHp": 100 }` は `"ExpectedHp": "100"` と書く必要があります。
- **`FocusEditorTab` / `CloseEditorTab` の `TabId` パラメータを `AssetPath` へ改名**（`UAIPEditorWorkspace` モジュール）。⚠️ **動作変更（要確認）— この 2 コマンドの呼び出し側に影響** — `TabId` は `InvalidParams` で拒否されます。どちらのコマンドも従来から対象をアセットパスとして解決していたため、旧名は `DumpEditorState` が返す `ActiveTabId`（Slate レイアウト識別子）を渡すよう誤誘導するものでした。旧名をエイリアスとして受理せず拒否するのは、黙って無視された `TabId` が原因から離れた場所で後から失敗するためです。`CaptureEditorTabImage` の `TabId` は本当にレイアウト識別子なので据え置きです。
- **`CaptureActiveWindowImage` がエディタのフォアグラウンドを要求しなくなりました**（`UAIPEditorObservation` モジュール）: 従来は他アプリが前面にあると必ず失敗していました。Slate は Windows から実際のアクティブ化通知が届くまでアクティブなトップレベルウィンドウを報告せず、ユーザーが別アプリで作業中に MCP ブリッジが起動したエディタには通知が届かないためです。スクリーンショットは画面を読むわけではないので背面のエディタは元から撮影可能でした。エディタのメインウィンドウへフォールバックし、どちらを撮ったかを `Result.CapturedWindow`（`"ActiveWindow"` / `"MainWindow"`）で返します。フォールバックはメインウィンドウにしか届かないため、他アプリが前面にある間のフローティングなアセットエディタやモーダルダイアログは引き続き `CaptureEditorTabImage` が必要です。
- **`CaptureEditorTabImage` がネストされたタブマネージャのタブも解決するようになりました**（`UAIPEditorObservation` モジュール）: `LevelEditorViewport` のような識別子は major tab 自身のマネージャに属する minor tab を指すため、従来のグローバル限定の検索では `DumpEditorState` が `ActiveTabId` として返す値のほとんどが拒否されていました。ドキュメントは以前からその値をそのまま渡すよう案内していたので、検索側を実態に合わせています。なお撮影時に対象タブをスタックの前面へ出す（背面のタブは描画されておらず空の画像になる）ため、**ユーザーに見えているタブが切り替わります**。
- **シナリオテンプレートのポインタ記法を確定し、解決失敗の理由を返すようにしました**（`UAIPScenario` モジュール）。bridge コマンドの応答を後続ステップへ綴じ込めない問題がありました。トークナイザがポインタ内の `.` をすべて `/` に書き換えていたため、先頭にスラッシュを付けて書いた本文が `//refPath` になって外れており、さらにガイド間でどちらの記法が正しいか記述が食い違っていました。ポインタ本文は先頭 1 文字で 2 通りに読み分けるようになりました — `/` で始まる本文はリテラルな JSON Pointer として扱われ、これが `.` を含むキーへ到達できる唯一の方法です。それ以外の本文は従来どおり `.` と `/` を等価な区切りとして扱うため、**これまで解決できていたポインタはすべてそのまま解決できます**。ポインタを伴わない `${StepName.Data}` はオブジェクト全体を指すようになりました。⚠️ **動作変更（要確認）— 偶然当たっていたポインタに影響します**: オブジェクトキーの照合が大文字小文字を区別する完全一致になり（`Data.refPath` と `Data.RefPath` は別のキーになります）、配列添字は `0` または先頭が非ゼロの数字列のみを受理し（`01` / `+1` / `1abc` は拒否）、`~1` と `~0` は RFC 6901 のエスケープとしてデコードされるようになり（`~` を含むキーは `~0` と書く必要があります）、リテラルを含む文字列の中にオブジェクトや配列を埋め込むと黙って空文字になるのではなく失敗するようになりました。解決失敗はどの種類の失敗かを返すようになり — ステップ名の綴り誤り・変数の未供給・ポインタの不一致・不正なエスケープがそれぞれ別の文言になります — エラーコードは `ExecutionFailed` から **`InvalidParams`** へ変わりました。これにより、これらの失敗は **`RetryCount` による再試行の対象外**になります。ステップデータから綴じ込む値にはサイズ検査が入り、オブジェクトと配列は記録済みのステップ結果と共有せず複製して渡すようになり、Params ツリー全体は展開差分に対して課金されるバイト予算の下で解決されるようになりました。
- **5 モジュールにまたがるコマンドパラメータ群を PascalCase へ改名し、あわせて実際にハンドラへ届くようになりました**（`UAIPEditorSequencer`・`UAIPEditorUIAutomation`・`UAIPEditorPhysics`・`UAIPEditorGameFeatures`・`UAIPEditorEnhancedInput` モジュール）。これらのパラメータはコマンドスキーマが公開している綴りとパーサーが読む綴りが食い違っており、**どちらの綴りを送っても機能していませんでした**。公開されている綴りはスキーマ検証を通過したあと黙って破棄され、パラメータは常にデフォルト値のままでした。一方、パーサーが読む綴りは、これらのスキーマが `AdditionalProperties: false` を宣言しているため入口で `InvalidParams` として拒否されていました。スキーマがパーサーの読むキーをそのまま公開するようになり、これらのパラメータは**今回はじめて使えるようになりました**。改名の内訳：
  - `UAIP.Editor.Sequencer` — `AddKeyframe`・`AddSection`・`AddTrack`・`BindActor`・`RemoveKeyframe`・`RemoveSection`・`RemoveTrack`・`SetKeyframeValue`・`SetPlaybackRange`・`UnbindActor` の `bDeferNotification` → `DeferNotification`、`RemoveKeyframe` の `bRemoveAll` → `RemoveAll`。
  - `UAIP.Editor.UIAutomation` — `FillForm` の `bStopOnFirstError` → `StopOnFirstError`。
  - `UAIP.Editor.Physics` — `SetBox`・`SetCapsule`・`SetSphere` の `offset_x` / `offset_y` / `offset_z` → `OffsetX` / `OffsetY` / `OffsetZ`、`AddConstraint` の `constraint_mode` → `ConstraintMode`。
  - `UAIP.Editor.GameFeatures` — `CreateGameFeaturePlugin` の `plugin_name` → `PluginName`・`output_path` → `OutputPath`、`GetGameFeatureInfo` の `plugin_name` → `PluginName`・`plugin_url` → `PluginUrl`、`ListGameFeatures` の `filter_state` → `FilterState`。
  - `UAIP.Editor.EnhancedInput` — `ListInputActions` と `ListMappingContexts` の `path_filter` → `PathFilter`。

  ⚠️ **既存の呼び出し側に対する変化は 2 点あり、いずれも「動いていた挙動が失われる」性質のものではありません。** 1 点目は、旧名を送っていた呼び出しが「受理されて無視される」のではなく `InvalidParams` で拒否されるようになることです。送っていた値は元から一切効いていなかったため、綴りを新名に置き換えるだけで対応は完了します。2 点目は、新名を送った呼び出しが、これまで黙って使われていたデフォルト値ではなくドキュメントどおりの挙動を得るようになることです。`DeferNotification` は実際に Sequencer の通知を遅延し、`RemoveAll` は実際に削除範囲を切り替え、`StopOnFirstError` は実際に `FillForm` を最初の失敗フィールドで停止させ、`OffsetX` / `OffsetY` / `OffsetZ` は実際に形状へ適用され、GameFeatures / EnhancedInput のフィルタは実際に絞り込みを行います。なお `UAIP.Editor.Niagara` は本項目の対象外です。同ネームスペースのパラメータについては、すぐ下の Niagara の項目を参照してください。

- **`UAIP.Editor.Niagara` のパラメータと Artifact フィールドをすべて PascalCase へ統一しました**（`UAIPEditorNiagara` モジュール）。このモジュールにはキー定数が 2 系統存在していました。1 つは PascalCase で、観測系・トポロジ系コマンドと、Niagara インスペクタが Artifact へ書き出すすべてのフィールドが使っていたものです。もう 1 つは snake_case で、後から追加された編集系コマンドが使っていたものです。そのため、同じ意味のフィールドがどのコマンドから出力されたかによって別の名前で返っていました。もっとも分かりやすい症状は、`CompileNiagaraSystem` が結果を `compile_state` / `compile_errors` として書き出す一方で、`GetSystemCompileState` がまったく同じ 2 つのフィールドを `CompileState` / `CompileErrors` として書き出していたことで、単一のキーで両方を読むことはできませんでした。この 2 系統を 1 つに統合し、モジュール内のすべてのキーを PascalCase に揃えました。以下の改名は、そのキーがモジュール内で現れるすべての箇所 — コマンドパラメータ、Artifact フィールド、`Parameters` / `Variables` 配列の要素オブジェクトのフィールド — に適用されます。
  - 対象の識別 — `asset_path` → `AssetPath`、`asset_type` → `AssetType`、`asset_name` → `AssetName`、`emitter_id` → `EmitterId`、`emitter_name` → `EmitterName`、`emitter_asset_path` → `EmitterAssetPath`、`module_id` → `ModuleId`、`module_name` → `ModuleName`、`script_path` → `ScriptPath`、`script_name` → `ScriptName`、`script_usage` → `ScriptUsage`、`stack_usage` → `StackUsage`、`input_name` → `InputName`、`parameter_name` → `ParameterName`、`enum_path` → `EnumPath`。
  - 値とオプション — `insert_index` → `InsertIndex`、`new_index` → `NewIndex`、`new_name` → `NewName`、`timeout_seconds` → `TimeoutSeconds`、`type_name` → `TypeName`、`type_path` → `TypePath`、`default_value` → `DefaultValue`、`variable_name` → `VariableName`、`variable_names` → `VariableNames`、`renderer_class_path` → `RendererClassPath`、`renderer_index` → `RendererIndex`、`local_space` → `LocalSpace`、`warmup_time` → `WarmupTime`。
  - Blueprint ラッパー — `actor_identifier` → `ActorIdentifier`、`component_name` → `ComponentName`、`target_blueprint_path` → `TargetBlueprintPath`、`parent_class_path` → `ParentClassPath`、`blueprint_path` → `BlueprintPath`。
  - Artifact 専用フィールド — `compile_state` → `CompileState`、`compile_errors` → `CompileErrors`、`requires_followup_compile` → `RequiresFollowupCompile`、`parsed_as_default` → `ParsedAsDefault`、`parsed_as_default_array` → `ParsedAsDefaultArray`、`variable_count` → `VariableCount`。
  - 大文字小文字のみの違いであり、旧綴りのままでも引き続き受理されるもの — `kind` → `Kind`、`value` → `Value`、`force` → `Force`、`enabled` → `Enabled`、`name` → `Name`、`properties` → `Properties`、`parameters` → `Parameters`、`variables` → `Variables`、`determinism` → `Determinism`、`success` → `Success`。

  ⚠️ **上記のうち最初の 4 グループはすべて動作変更（要確認）です。** エンジンの JSON キー照合は大文字小文字を区別しないため、最後のグループは旧綴りのままでも動作し続けます。しかしそれ以外は大文字小文字以外の点でも綴りが変わるため、旧綴りを送ったリクエストは `InvalidParams` で拒否されるようになり（これらのスキーマは `AdditionalProperties: false` を宣言しています）、旧フィールド名で Artifact を読んでいたコードは値を見つけられなくなります。対応は綴りを置き換えるだけで完了します。コマンド・Capability・値・挙動は名前以外に一切変わっていません。`Toolset.Editor.Niagara.*` のブリッジコマンドは対象外です。これらはエンジン側の Toolset スキーマをそのまま転送するものであり、その綴りを維持します。あわせて、`AddSetParametersModule` が `Parameters` 配列の要素スキーマを `Items` ではなく `items` として公開していた不具合も修正しました。これにより `uaip_describe_command` が要素の構造を返せていませんでした。

- **`ReadOnly` が `ShutdownEditor` / `RestartEditor` を拒否しなくなりました**（`UAIPCore` および `UAIPEditorWorkspace` モジュール）。`ReadOnly=True` はすべての変更系コマンドを拒否しており、エディタライフサイクルの 2 コマンドも変更系です。そのためこのポリシーで起動したエディタは、UAIP 経由で終了することも再起動することもできませんでした。ポリシーは起動時に読まれるため、ini を戻しても走行中のプロセスには届きません。残る手段はエディタを手で閉じるかプロセスを強制終了するかで、これはドキュメントが避けるよう案内している操作であり、プラグイン DLL がロックされたままになる原因でもありました。この 2 コマンドは読み取り専用ポリシーの拒否対象から除外され、`ReadOnly=True` でも `Available: true` として報告されます。`ReadOnly` のそれ以外の挙動は変わらず、省略可能な `SaveAll` は引き続き `DisableSave` が制御し、例外を宣言しているコマンドはこの 2 つ以外にありません。⚠️ **`EditorLifecycle` は DefaultAllow** であるため、追加設定をしていない既定の構成では、`ReadOnly=True` にしても AI はエディタを終了・再起動できます。これを塞ぐには明示的な設定が必要です（`+DeniedCapabilities=EditorLifecycle`、またはこの 2 コマンドを名指しした `+DeniedCommands=`）。詳細は [Safety & Capabilities → ReadOnly とエディタライフサイクルコマンド](safety.md#readonly-とエディタライフサイクルコマンド) を参照してください。
- **CLI トランスポートが自動生成する `SessionId` がプロセス番号ベースではなくなりました**（`UAIPTransportCLI` モジュール）。`SessionId` を指定しない CLI の単発実行では、従来はプロセス番号から組み立てた ID が使われていましたが、HTTP / WebSocket / MCP と同じ匿名セッションの経路を通るようになり、`CLI-Anonymous-<guid>` が生成されます。この経路を通ることでセッションが内部的に匿名として印付けされ、明示的なセッションを要求するコマンド（アセット監査のジョブ系、トレース解析系）が、二度と名指しできないセッションを受理せず拒否できるようになります。⚠️ 成果物の保存先フォルダ名は生成された ID に基づくため、単発実行の成果物をプロセス番号で探していたスクリプトは動かなくなります。`SessionId` を明示指定している場合は影響がなく、そちらが本来の対処です。
- **記述の訂正: シナリオ内でクリーンアップステップの実行を保証することはできません**（ドキュメントおよびプラグインに同梱される MCP ブリッジガイド。挙動の変更はありません）。`AbortOnFailure` は元から**失敗したステップ自身**に対して評価されるものであり、その後続ステップに対して評価されることはありません。しかしガイドはこれと逆の説明 — 末尾のクリーンアップステップに `AbortOnFailure: false` を付ければ前段の失敗を跨いで実行される — を記載していました。実際にはそうならず、前段のステップが既定の `true` のまま失敗した時点でシナリオは終了し、クリーンアップステップはディスパッチされず `StepResults` にも現れません。⚠️ **旧来の記述に従って書かれたシナリオでは、クリーンアップステップが実行されていません** — 末尾に置いた `StopPIE`・`StopTrace`・タブのクローズ・一時アセットの削除といったステップは、前段が失敗するたびに黙ってスキップされていました。ガイドは実際に成立する手段（クリーンアップ用ステップより前の**すべての**ステップを `false` にする、またはシナリオが返った後にクライアント側のループでクリーンアップする）と、シナリオ内のどの書き方でもカバーできないケース（送信時点での拒否、シナリオ全体のウォッチドッグ発火時 — 空の `StepResults` を返す一方でランナーはバックグラウンドで走り続けます — およびエディタのクラッシュ）を記載するよう書き改めました。詳細は [シナリオ実行 → 失敗時の挙動とクリーンアップ](scenario.md#失敗時の挙動とクリーンアップ) を参照してください。
- **`SetAssetProperty` / `SetActorProperty` / `SetWorldSetting` / `SetDataTableRow` / `SetBlueprintDefault` / `SetProjectSetting` は、書き込み自体が拒否された場合に `ExecutionFailed` ではなく `InvalidParams` を返すようになりました**（`UAIPEditorProperty` モジュール）。この拒否は常に、呼び出し側が渡した `PropertyPath` / `Value` と解決済みターゲットとの組み合わせに起因するものです — 解決できないパス、`SetPropertyValue` が書き込みを拒否するプロパティ型、そのプロパティの UE テキストインポート形式として解析できない値のいずれかであり、環境要因やランタイムの失敗ではありません。そのため `InvalidParams` の方が正確なコードです。あわせて、同一の失敗に対してすでに `InvalidParams` を返している `SetBlueprintComponentProperty`（`UAIPEditorBlueprint` モジュール）とも整合します。⚠️ **動作変更** — この 6 コマンドについて、この失敗ケースを `ExecutionFailed` としてパターンマッチしていた呼び出し側は `InvalidParams` へ切り替える必要があります。シナリオ内の `RetryCount` もこの失敗を再試行しなくなります（`InvalidParams` は再試行対象外のため）。これら 6 コマンドの他の `ExecutionFailed`（エディタ利用不可、対象解決の失敗、`PreEdit` 拒否）は変わりません。
- **`AddGraphNode` のモジュールアローリストが完全一致になり、`GetAvailableRigVMUnitStructs` が `SchemaVersion: 2` を返すようになりました**（`UAIPEditorControlRig` モジュール）。従来、`StructPath` の所属パッケージは `/Script/ControlRig`・`/Script/AnimationCore`・`/Script/Engine` のいずれかで**始まっている**だけで受理されており、`/Script/ControlRigDeveloper`・`/Script/ControlRigEditor`・`/Script/EngineMessages` のようにプレフィックスが偶然一致しただけの無関係なパッケージも、アローリストが本来対象とすべき範囲に反して受理されていました。現在は 7 つのモジュール — `/Script/ControlRig`・`/Script/ControlRigDynamics`・`/Script/ControlRigPhysics`・`/Script/ControlRigSpline`・`/Script/ControlRigModules`・`/Script/AnimationCore`・`/Script/Engine` — との完全一致で比較されます。ControlRig の姉妹モジュールを、旧来の前方一致の副作用としてではなく明示的に列挙しているため、Physics / Dynamics のリグユニット群は厳格化後も引き続き追加可能です。`GetAvailableRigVMUnitStructs` は `SchemaVersion: 2` を返すようになりました — 各エントリが、`AddGraphNode` が検証するのとまったく同じポリシーに由来する `Addable` フラグと、`false` の場合は機械可読な `NotAddableReason` を持つようになり、応答には `TotalCount` / `ReturnedCount` / `Truncated` も追加されました。`ClassPath` と `ClassDisplayName` は変わりません。⚠️ **破壊的変更 — 旧来の前方一致に依存していた呼び出しは動作しなくなります**: 許可対象モジュールとプレフィックスが一致するだけでモジュール自体とは異なるパッケージを持つ `StructPath` は、すべて `ModuleNotAllowed` で拒否されるようになりました。回避策はありません — このアローリストは元々そうしたパッケージへ到達することを意図していませんでした。
- **`DumpOpenTabs` の出力から `TabId` フィールドが無くなりました**（`UAIPEditorObservation` モジュール）。⚠️ **動作変更（要確認）— `DumpOpenTabs` の出力を読んでいるコードを確認してください** — 同じ値は同じオブジェクトの `AssetPath` フィールドに引き続き入っているため、そちらを読むように変更してください。このフィールドは名前に反してタブ識別子ではなくアセットのパスを保持していたため、Slate のレイアウト識別子を期待するコマンド（`CaptureEditorTabImage` の `TabId` など）へそのまま渡しても解決できませんでした。この値は元から同じオブジェクトの `AssetPath` にも重複して入っていたため、誤解を招くフィールドを削除しても失われる情報はありません。
- **`FocusEditorTab` と `CloseEditorTab` が、成功したときに JSON artifact を返すようになりました**（`UAIPEditorWorkspace` モジュール）。「すべてのコマンドは artifacts を返す」というプロジェクト全体の方針に合わせたものです。artifact の中身は解決済みのアセットパス（サブグラフのタブを対象にした場合はその名前も）です。これは追加のみの変更です — 既存の応答フィールドは変わらず、失敗したときは従来どおり artifact を返しません。

**修正**

- **プロパティ書き込みが拒否されたとき、`ExecutionFailed` に空の `ErrorMessage` が返っていました。** `FObjectPropertyUtils::SetPropertyValue`（`UAIPEditorShared` モジュール）は、`SetAssetProperty`・`SetActorProperty`・`SetWorldSetting`・`SetDataTableRow`・`SetBlueprintDefault`・`SetProjectSetting`、および他モジュールのいくつかのノード/コンポーネントプロパティ設定コマンドが共有する書き込み経路です。`ImportText_InContainer` より手前のすべての失敗分岐が `OutError` へ一切書き込まずに結果コードだけを返していたため、書き込みが拒否された場合 — `PropertyPath` の一部が解決できない、パス中にオブジェクト参照をまたぐ、配列添字が範囲外、あるいは `SetPropertyValue` が書き込みを拒否するプロパティ型・フラグ（配列全体、`EditConst`、このコンテキストでは無効、非推奨）— のいずれでも、呼び出し側には `{"Success": false, "ErrorCode": "ExecutionFailed", "ErrorMessage": ""}` が届き、何が悪かったのか一切分かりませんでした。`ErrorMessage` はプロパティパス、解決したプロパティの C++ 型、型/フラグによる拒否の場合はその具体的な理由を示すようになりました（配列全体への書き込みは、配列は全体としては書き込めないことと、代わりにインデックス指定を使うよう案内します）。`ImportText` の失敗（値の文字列が対象プロパティの UE テキストインポート形式に一致しない）も、固定の一般的な文言ではなく、プロパティ・期待される型・拒否された値を示すようになりました。


#### MCP Bridge

MCP Bridge 1.1.2 以降の未リリース分です。ブリッジはプラグインとは独立に採番・リリースされます（採番規則は上記のバージョニング方針を参照）。

**追加**

- **`uaip_execute` の応答待ち中に進捗通知を送るようになりました。** クライアントが呼び出しに MCP の進捗トークンを添えた場合、その呼び出しが返るまでおよそ 5 秒おきに `notifications/progress` を送出します。内容は経過秒数とエディタの状態（`STARTING` / `RUNNING` / `UNRESPONSIVE`）です。エディタ内部の情報は一切載せず（ジョブ自身の進捗は `GetAssetAuditStatus` のようにそれを知るコマンドで取得します）、`uaip_run_scenario` は対象外です。トークンが無ければ何も送りません。⚠️ **その通知を表示するかどうかはクライアント側の判断**であり、`notifications/progress` を扱わないクライアントでは応答待ちの間に何も表示されません（本ドキュメント執筆時点の Claude Code がその一例です）。詳細は [接続方法 → 応答待ちの間に送られる進捗通知](connections.md#応答待ちの間に送られる進捗通知) を参照してください。

**修正**

- **エディタが拒否したシャットダウンが成功として報告されていました。** `ShutdownEditor` はエディタの応答を読まずに `{"Success": true}` を返していたため、拒否された場合（読み取り専用のセーフティポリシーがコマンドを退けた場合など）でも正常終了に見え、実際にはプロセスが動き続けてファイルを掴んだままになっていました。エディタ自身のエラーをそのまま返し、ポートが実際に解放されたことを確認してから「停止した」と報告するようになりました。判断できない場合は推測せずその旨を返します。
- **再起動するとブリッジがエディタと一切通信できなくなりました。** `RestartEditor` はエディタが自分自身を再起動するため、後継プロセスはブリッジが起動したものではありません。ブリッジは死んだハンドルを掴んだまま、以降のあらゆるコマンドを「ポートがこのプロジェクトのエディタ以外のプロセスに占有されている」として拒否し続けました。この拒否は状態を書き換えないため**恒久的**で、復旧するにはエディタを手動で閉じるしかありませんでした。同じプロジェクトを報告することを確認したうえで、ポートに応答しているエディタを引き継ぐようになりました。
- **応答が途中で切れても健全なエディタを再起動しなくなりました。** 応答の途中で切断された接続と、そもそも接続できなかった場合が同じ分類だったため、動作中のエディタを再起動し、既に実行を始めていたリクエストを再送することがありました。両者を区別し、応答の切断は**ポートが実際に消えている場合にのみ**エディタの死亡として扱います。
- **長時間かかるコマンドがエディタの死亡と誤認されなくなりました。** ブリッジは 15 秒ごとに ping を送り、30 秒無応答でエディタ停止と判定していましたが、それより長くゲームスレッドを占有するコマンド（`BuildMetaHuman` は約 75 秒）は ping を枯渇させます。その結果、同じプロジェクトに対して 2 つ目のエディタを起動するか、作業中の健全なエディタを終了させていました。
- **先頭にスラッシュを置いたシナリオテンプレートが一致するようになりました。** ポインタのトークナイザがすべての `.` を `/` に書き換えていたため、`${S.Data./refPath}` と書くと `//refPath` になり何にも一致しませんでした。`/` で始まる本体はリテラルな JSON ポインタとして読まれるようになり（`.` を含むキーに到達できる唯一の方法です）、それ以外の本体では従来どおり `.` と `/` の双方を区切りとして扱います。解決に失敗した場合も、原因を問わず固定文を返すのではなく、どの部分で失敗したかを示します。
- **動作中のエディタが「停止済み」と判定され、そのロックが 2 つ目のブリッジへ渡ることがありました。** ブリッジは保持者のプロセス ID が生きているかを `os.kill(pid, 0)` で確かめていましたが、Windows のこの呼び出しは「そのプロセスは存在しない」場合と「存在するが問い合わせる権限がない」場合の**どちらでも同じエラーを返します**。ブリッジは前者と解釈していたため、動作中のエディタを保持しているプロセスを「もういない」と判断できてしまいました。ロックを二重に持った 2 つのブリッジが同じエディタへ同時に指示を出すと、コマンドの取り違えやエディタの予期しない終了につながります。プロセスを直接照会して終了コードを読むようになり、権限不足で問い合わせられない場合は**存在するもの**として扱います。

**変更**

- **インライン化されない artifact をダウンロードしなくなりました。** 従来は artifact のバイト列を取得してから、その MIME タイプがインライン許可リストに含まれるかを判定していました。先に長さとコンテンツタイプを読み、実際に使う場合にのみ本体を取得します。**設計上インライン化されないバイナリ artifact で効きます** —— `.utrace` の採取結果は数百 MB になりえます。

---

### UAIP Plugin 1.1.0 — 2026-07-24

**UAIP 1.1.0 を Fab で公開しました。** [https://www.fab.com/listings/0eedf909-00ac-4d95-b109-8fda51800fff](https://www.fab.com/listings/0eedf909-00ac-4d95-b109-8fda51800fff)

[![YouTube でアップデートトレーラーを見る](https://markdown-videos-api.jorgenkh.no/youtube/0Z2MKvMQ0g8)](https://youtu.be/0Z2MKvMQ0g8)

後方互換な MINOR リリースです。以下の変更はすべてプラグインリポジトリに取り込み済みで（`.uplugin` の `VersionName` は `1.1.0`）、Fab 審査を通過してリリースされました。

> **移行に関する注意（Migration notes）。** 1.1.0 は後方互換な MINOR リリースですが、特定の挙動にパターンマッチしている呼び出し側に影響しうる 3 つの限定的な例外があります：
> - **Niagara `AddSetParameterEntry` / `RemoveSetParameterEntry` に `script_name` が必須化** — 指定なしの呼び出しは `InvalidParams` を返します。下記「変更」を参照。
> - **PIE/SIE 拒否時の ErrorCode が `ExecutionFailed` から `NotAllowed` に変更** — `SetActorTransform`・`PlaceActorInLevel`・`DeleteActorFromLevel` および WorldPartition / DataLayer / HLOD の変更系コマンドが対象。PIE 中のケースで `ExecutionFailed` にパターンマッチしていた呼び出し側は `NotAllowed` に切り替えてください。
> - **Physics 読み取り専用コマンドが PIE/Simulate 中に拒否しなくなった** — `UAIP.Editor.Physics` の読み取り専用10コマンドが `NotAllowed` の代わりに `Success: true` + `PieInProgress: true` フィールドを返すようになりました。当該ケースで `NotAllowed` に依存していた呼び出し側は更新が必要です。

#### UAIP Plugin

**追加**

- **Editor Toolset ブリッジコマンド**（`UAIPEditorAssets`・`UAIPEditorLevel`・`UAIPEditorObservation`・`UAIPEditorWorkspace`・`UAIPEditorEngineManagement`・`UAIPRuntimePIE`・`UAIPRuntimeWorld` モジュール）: AI エージェントが UE 5.8 公式 Toolset フレームワーク（`EditorAppToolset` + `LogsToolset`）に委譲する Toolset ブリッジコマンド（`Toolset.*`）を呼び出せるようになりました。ブリッジコマンドは UE 5.8+ かつ対象 Toolset プラグインが有効な場合のみ利用可能で、古いバージョンでは `Available: false` になります。UAIP ネイティブコマンドは引き続き主要パスであり UE 5.7 でも動作します。あわせて 6 つのネイティブコマンドを追加しました：`GetVisibleActors`・`ProjectWorldToScreen`・`ProjectScreenToWorld`（`UAIP.Editor.Level`）、`CaptureViewportImageAnnotated`（`ViewportAnnotationCapture` 必須；`UAIP.Editor.Observation`）、`GetLogVerbosity` / `SetLogVerbosity`（`LogVerbosityEdit` 必須；`UAIP.Editor.Engine.Log`）。新 Capability `ViewportAnnotationCapture`（DefaultDenied）と `CVarInspect`（DefaultDenied；`Toolset.Editor.Toolset.World.SearchCVars` ブリッジをゲート）を追加しました。
- **PCG 拡張コマンドと Capability**（`UAIPEditorPCG` モジュール）: `UAIP.Editor.PCG` 配下に 20 コマンドを追加しました — アセット作成（`CreatePCGGraph`、`PCGGraphAssetCreate` 必須）、スキーマ / 説明 / パラメータ取得編集（`GetPCGGraphSchema`・`GetPCGGraphDescription`・`SetPCGGraphDescription`・`SetPCGGraphParams`・`RemovePCGGraphParams`）、インスタンス管理（`ListPCGGraphInstances`・`SpawnPCGGraphInstance`・`GetPCGGraphInstanceParams`・`SetPCGGraphInstanceParams`・`ResetPCGGraphInstanceParams`）、サブグラフ / ネイティブノード（`ListPCGAvailableSubgraphs`・`GetPCGNativeNodeSchema`・`AddPCGSubgraphNode`）、グラフ構造編集（`RepositionPCGNode`・`AddPCGCommentBox`・`UpdatePCGCommentBox`・`RemovePCGCommentBox`）、データビュー / 実行（`GetPCGNodeDataView`・`RunPCGInstantGraph`）。5 つの DefaultDenied Capability（`PCGGraphAssetCreate`・`PCGGraphExecute`・`PCGVolumeSpawn`・`PCGNodeInspect`・`PCGToolsetUnsafeNodeAdd`）を追加しました。`PCGVolumeSpawn` および `PCGToolsetUnsafeNodeAdd` は `DefaultUAIP.ini` の `AllowedCapabilities` に追記しないでください。`GetPCGNodeDataView` は `PCG_PROFILING_ENABLED=1` でビルドされた場合のみ有効です。また、UE 5.8 以上かつ `PCGToolset` プラグインが有効な環境では `Toolset.Editor.PCG.*` 配下に 31 のブリッジコマンドも利用できます（無効な環境では `Available: false`）。
- **プラグイン管理**（`UAIPRuntimeEngineManagement`・`UAIPEditorEngineManagement` モジュール）: AI エージェントがエディタを離れることなく UE プラグインの状態を確認・管理できるようになりました。エディタ / パッケージ版ビルド共通で使える読み取り専用コマンドを `UAIP.Runtime.Engine.Plugin` 配下に 5 本追加しました（`ListPlugins`・`GetPluginInfo`・`IsEnabled`・`GetPluginDependencies`・`GetPluginForAsset`）。エディタ専用コマンドを `UAIP.Editor.Engine.Plugin` 配下に 9 本追加しました — 観測系 5 本（`GetPluginDescriptor`・`GetPluginDependents`・`GetPluginTemplateDescriptions`・`IsPluginCreationAllowed`・`IsPluginModificationAllowed`）と変更系 4 本（`SetPluginEnabled`・`UpdatePluginDescriptor`・`AddPluginDependency`・`RemovePluginDependency`）。UE 5.8 以上かつ `PluginToolset` プラグインが有効な環境では `Toolset.Plugin.*` 配下に 15 のブリッジコマンドも利用できます（`ListEnabledPlugins`・`ListDiscoveredPlugins`・`GetPluginInfo`・`IsEnabled`・`GetPluginDependencies`・`GetPluginForAsset`・`GetPluginDescriptor`・`GetPluginDependents`・`GetPluginTemplateDescriptions`・`IsPluginCreationAllowed`・`IsPluginModificationAllowed`・`SetPluginEnabled`・`UpdatePluginDescriptor`・`AddPluginDependency`・`RemovePluginDependency`）。3 つの DefaultDenied Capability を追加しました：`PluginEnableToggle`（`SetPluginEnabled` をゲート）・`PluginDescriptorEdit`（`UpdatePluginDescriptor` をゲート）・`PluginDependencyEdit`（`AddPluginDependency` / `RemovePluginDependency` をゲート）。観測系コマンドは `EditorInspect` のみ必要です。`UAIP.Core.ListPlugins` は非推奨になりました；`UAIP.Runtime.Engine.Plugin.ListPlugins` を使用してください。
- **フォリッジ管理**（`UAIPEditorFoliage` モジュール）: AI エージェントがエディタでフォリッジタイプとインスタンスを管理できるようになりました。`UAIP.Editor.Foliage` 配下に 11 コマンドを追加しました — 観測系 4 コマンド（`ListFoliageTypes`・`GetFoliageTypeInfo`・`GetFoliageInstanceCount`・`GetFoliageInstances`、`EditorInspect` 必須、PIE 中でも実行可能）、フォリッジタイプ管理 3 コマンド（`AddFoliageTypeToLevel`・`RemoveFoliageTypeFromLevel`・`SetFoliageTypeSettings`、`FoliageTypeEdit` 必須）、インスタンス操作 4 コマンド（`AddFoliageInstances`・`RemoveFoliageInstances`・`DeleteAllFoliageInstances`・`ResimulateProceduralFoliage`、`FoliageInstanceEdit` または `FoliageBulkDelete` 必須）。インスタンス配置は World Partition 対応で、各インスタンスを正しい `AInstancedFoliageActor` セルにルーティングします。3 つの DefaultDenied Capability（`FoliageTypeEdit`・`FoliageInstanceEdit`・`FoliageBulkDelete`）を追加しました。
- **World Partition 編集**（`UAIPEditorWorldPartition` モジュール、**Pro 版限定** — デモ版では利用不可）: AI エージェントが World Partition ストリーミング・Data Layer・HLOD ワークフローを管理できるようになりました。`UAIP.Editor.WorldPartition` 配下に 34 コマンドを追加しました — World Partition 系 12 コマンド（`GetWorldPartitionInfo`・`GetWorldPartitionStreamingGrids`・`GetRuntimeGridSettings`・`SetRuntimeGridSettings`・`GetActorWorldPartitionSettings`・`SetActorIsSpatiallyLoaded`・`SetActorRuntimeGrid`・`SetWorldPartitionStreamingEnabled`・`PinActorInWorldPartition`・`UnpinActorFromWorldPartition`・`DumpWorldPartitionCells`・`ListExternalActors`）、Data Layer 系 15 コマンド（`ListDataLayers`・`GetDataLayerInfo`・`CreateDataLayerAsset`・`DeleteDataLayerAsset`・`CreateDataLayerInstance`・`DeleteDataLayerInstance`・`SetDataLayerType`・`SetDataLayerInitialRuntimeState`・`SetDataLayerIsLoadedInEditor`・`SetDataLayerVisibility`・`SetParentDataLayerInstance`・`GetActorDataLayers`・`AddActorToDataLayer`・`RemoveActorFromDataLayer`・`GetActorsInDataLayer`）、HLOD 系 7 コマンド（`ListHLODLayers`・`CreateHLODLayer`・`DeleteHLODs`・`SetActorHLODLayer`・`BuildHLODs`・`CancelHLODBuild`・`GetHLODBuildStatus`）。3 Capability（`WorldPartitionEdit`・`DataLayerEdit`・`HLODBuild`、いずれも DefaultDenied）を追加しました。観測系コマンドは World Partition が有効でないレベルでも `Success: true` + `IsWorldPartitionEnabled: false` を返します。
- **MVVM 編集**（`UAIPEditorMVVM` モジュール、**Pro 版限定** — `ModelViewViewModel` プラグイン必須、デモ版では利用不可）: AI エージェントが WidgetBlueprint の MVVM 設定（ViewModel の接続・バインディング・イベント・プロパティ）を操作できるようになりました。`UAIP.Editor.MVVM` 配下に 26 コマンドと 2 Capability（`ViewModelBindingEdit`、`ViewModelSourceEdit`、いずれも DefaultDenied）を追加しました。UE 5.8 以上かつ `MVVMToolset` プラグインが有効な環境では、`Toolset.MVVM.*` 配下に 9 つのブリッジコマンドも利用できます。
- **サウンドアセット編集**（`UAIPEditorSound` モジュール）: AI エージェントが `USoundClass` / `USoundAttenuation` / `USoundMix` アセットのプロパティを読み取り・設定できるようになりました。`UAIP.Editor.SoundSettings` 配下に 13 コマンドと 3 Capability（`SoundClassEdit`、`SoundAttenuationEdit`、`SoundMixEdit`、いずれも DefaultDenied）を追加しました。
- **Sandbox 編集統合**（`UAIPEditorSandbox` モジュール、**Pro 版限定** — `FileSandbox` プラグイン必須、デモ版では利用不可）: AI エージェントが FileSandbox セッションにアセット変更を仮置きし、人間が確認後にコミットまたはリバートできるようになりました。`UAIP.Editor.Sandbox` 配下に 6 コマンド（`BeginSandboxSession`、`EndSandboxSession`、`GetSandboxStatus`、`GetSandboxChanges`、`CommitSandboxChanges`、`RevertSandboxChanges`）と、4 Capability（`SandboxObserve`（DefaultAllow）、`SandboxSessionControl`、`SandboxPersist`、`SandboxRevert`（いずれも DefaultDenied））を追加しました。読み取り専用の observe 系コマンド（`GetSandboxStatus`・`GetSandboxChanges`）を含む全 6 コマンドが `FileSandbox` プラグインを必要とし、デモ版モジュールホワイトリストには含まれません。
- **セマンティックアセット検索**（`UAIPEditorAssets` モジュール — `SemanticSearch` プラグイン UE 5.8+ および OpenAI API キー必須）: AI エージェントが自然言語クエリでプロジェクトのアセットを検索・比較できるようになりました。`UAIP.Editor.SemanticSearch` 配下に 5 コマンド（`SearchAssetsSemantic`、`FindSimilarAssets`、`GetIndexStats`、`StartIndexing`、`CancelIndexing`）と 1 Capability（`SemanticSearchEdit`、DefaultDenied、インデックス再構築操作をゲート）を追加しました。UE 5.8 以上かつ `SemanticSearchToolset` プラグインが有効な環境では、`Toolset.Editor.SemanticSearch.*` 配下に 2 つのブリッジコマンド（`Search`、`FindSimilar`）も利用できます。なお、`SearchAssetsSemantic` および `FindSimilarAssets` はセマンティックインデックスが存在する場合にのみ動作します。検索コマンドを使用する前に `StartIndexing` を一度実行してください。
- **ConfigSettings コマンド**（`UAIPEditorEngineManagement` モジュール）: AI エージェントが `ISettingsModule` 経由でプロジェクト設定とエディタ設定を検査・変更できるようになりました。`UAIP.Editor.Engine.ConfigSettings` 配下に 8 コマンドを追加しました — `ListSettingsContainers`・`ListSettingsCategories`・`ListSettingsSections`（読み取り専用、Capability 不要）、`GetSettingsSchema`（プロパティ名・型・説明・デフォルト値・編集条件を JSON アーティファクトで返す；`EditorInspect` 必要）、`GetSettingsValues`（現在値を JSON アーティファクトで返す；シークレットフィールドは `***` でマスク；`EditorInspect` 必要）、`SetSettingsValues`（`Properties` マップを `ImportText` 経由でマージ；`DryRun` 対応；`ConfigSettingsEdit` 必要；PIE 中は実行不可）、`SaveSettings`（ini ファイルに書き出し；PIE 中および `bDisableSave` 設定時は実行不可；`ConfigSettingsSave` 必要）、`ResetSettingsToDefaults`（クラスデフォルトに戻す；PIE 中は実行不可；`ConfigSettingsReset` 必要）。書き込み操作はプロジェクトの `Config/` ディレクトリ配下のファイルのみ許可されます（エンジン ini ファイルは `PolicyViolation` で拒否）。さらに `UAIP.Runtime.Engine.Config` 配下に 2 コマンドを追加しました — `GetConfigValue`（raw ini キーの読み取り；Capability 不要）と `SetConfigValue`（raw ini キーの書き込み・削除；パッケージ版ビルドでは実行不可；ini インジェクション文字 `[`・`]` は拒否；`ConfigSettingsEdit` 必要）。3 つの DefaultDenied Capability を追加しました：`ConfigSettingsEdit`・`ConfigSettingsSave`・`ConfigSettingsReset`。UE 5.8+ かつ `ConfigSettingsToolset` プラグインが有効な環境では、`Toolset.ConfigSettings.*` 配下に 8 つのブリッジコマンドも利用できます。

- **CVar 管理**（`UAIPRuntimeEngineManagement`・`UAIPEditorEngineManagement` モジュール）: AI エージェントがコンソール変数の読み取り・検索・設定・リセットを行えるようになりました。`UAIP.Runtime.Engine.CVar` 配下に 4 コマンドを追加しました — `GetConsoleVariable`（`RuntimeCVarRead` 必要）・`SearchConsoleVariables`（`RuntimeCVarRead` 必要）・`SetConsoleVariable`（`RuntimeCVarWrite` 必要）・`ResetConsoleVariable`（`RuntimeCVarWrite` 必要）。さらに Toolset ブリッジ `Toolset.Editor.Toolset.EngineManagement.SearchCVars`（`CVarInspect` 必要；UE 5.8+、EditorToolset プラグイン）を追加しました。新しい DefaultDenied Capability `RuntimeCVarWrite`（`SetConsoleVariable` / `ResetConsoleVariable` をゲート）を追加しました。機密パターン（`*password*`・`*token*`・`*secret*` 等）に一致する CVar は存在を隠蔽するため `NotFound` を返します。`ECVF_ReadOnly` の CVar は設定・リセット時に `NotAllowed` を返します。
- **ログエントリ取得**（`UAIPEditorEngineManagement`・`UAIPRuntimeEngineManagement` モジュール）: `UAIP.Editor.Engine.Log` 配下に `GetLogEntries`（エディタ Output Log から最近のエントリをパターンフィルタ付きで取得；Capability 不要）を追加しました。また `UAIP.Runtime.Engine.Log` 配下に `GetLogCategories`（登録済みログカテゴリ名をすべて一覧表示；Capability 不要）を追加しました。
- **`CreateAsset` 自己記述コマンド**（`UAIPEditorAssets` モジュール）: AI エージェントがエラーメッセージによる試行錯誤に頼らず、事前に `CreateAsset` の有効な入力値を確認できるようになりました。`UAIP.Editor.Assets` 配下に読み取り専用の2コマンドを追加しました — `ListCreatableAssetClasses`（作成可能な Factory を1つ以上持つ全 UClass を、Factory数とデフォルト Factory クラス名付きで返す；重い呼び出し、`EditorInspect` 必要）と `ListFactoriesForClass`（指定 `ClassName` に対応する Factory 候補を、各 `FactoryParams` の JSON Schema 付きで返す；`EditorInspect` 必要）。あわせて `ICreateAssetInterceptor::GetFactoryParamsSchema()` を追加し、`DataTable` と `StateTree` のアセット作成が必要とする `FactoryParams` キー（`RowStructPath`・`SchemaClass`）を自己記述するようになりました。
- **Data Registry 観測**（`UAIPEditorDataRegistry` モジュール、`DataRegistry` プラグイン必須）: AI エージェントが UE 5.8 Data Registry の一覧・スキーマ確認・キャッシュ済みアイテム取得を行えるようになりました。`UAIP.Editor.DataRegistry` 配下に9コマンドを追加しました — `ListRegistries`（`StructFilter` とシステム診断情報付き）、`GetRegistryInfo`、`GetSchema`（プロパティごとの `IsSecret` を返す）、`ListItems`、`ListDataSources`、`ListRuntimeSources`、`GetItems`（名前パターン・メタデータ・`FFilePath`/`FDirectoryPath`・ネストした `FInstancedStruct` を含む機密フィールドをマスクし、未キャッシュのアイテムは黙って省略せず理由付きで `MissingItems` に報告）、および Toolset に対応がない native 専用2コマンド: `GetAllCachedItems`（アイテム名を事前指定せず現在キャッシュ済みの全アイテムを取得、1000件・1MiB を上限）と `AcquireItems`（カスタム/Remote ソース向けに非同期キャッシュロードをトリガー。DataTable ソースは自動事前ロード済みのため通常不要。デフォルト30秒でタイムアウトし部分結果を返す）。全9コマンドは読み取り専用で `EditorInspect` のみ必要とし、新規 Capability は追加していません。UE 5.8+ で `DataRegistryToolset` プラグインが有効な場合、`Toolset.Editor.DataRegistry.*` 配下に7つのブリッジコマンドが追加で利用可能です — ブリッジ版の `GetItems` はネイティブ版と異なり、欠損アイテムを黙って省略しマスキングも適用しません。
- **アセット監査・参照グラフ・サイズマップコマンド**（`UAIPEditorAssets` モジュール）: AI エージェントがエディタを離れることなく、アセット参照グラフの探索、ディスク/メモリサイズの集計、未参照・循環・壊れた参照の検出を行えるようになりました。`UAIP.Editor.Assets` 配下に読み取り専用の8コマンドを追加しました — `GetAssetReferences`（参照元・参照先・両方を指定深さまで探索）、`GetAssetSizeMap`（アセット単位のディスクサイズ集計、既にロード済みのアセットは常駐メモリサイズも任意で取得）、`GetAssetSizeMapByClass`（アセットクラス単位のディスクサイズ集計）、`FindUnreferencedAssets`（ハードリファレンスのみのヒューリスティック；コード参照・ini参照・PrimaryAssetRule参照は検出不可）、`FindCircularReferences`（深さ優先探索による循環依存検出）、`FindBrokenReferences`（未登録パッケージへの依存検出）、`GetAssetDependencyPath`（2アセット間の最短パス検索）、`RunAssetAudit`（上記4分析を統合した複合レポート）。全8コマンドは既存の `EditorInspect` のみ必要（新規 Capability 追加なし）。各レスポンスには `TruncationReason`（`"OutputLimit"` または `"VisitedNodeCap"`）が含まれ、出力件数上限と内部探索コスト上限（訪問ノード20万件）のどちらで打ち切られたかを区別します。`FindUnreferencedAssets`・`FindCircularReferences`・`FindBrokenReferences`・`RunAssetAudit` は進捗通知に対応していますが、これらのコマンドはゲームスレッドで同期実行されるため、進捗が最終レスポンスとまとめて届く可能性があります（transport 実装依存）。
- **AssetManager / PrimaryAssetType コマンド**（`UAIPEditorAssets` モジュール）: AI エージェントが `UAssetManager` の `PrimaryAssetType`・`AssetBundle`・アセットごとの Rule を確認・管理できるようになりました。`UAIP.Editor.Assets` 配下に15コマンドを追加しました — 読み取り専用10コマンド（`ListPrimaryAssetTypes`、`GetPrimaryAssetTypeInfo`、`ListPrimaryAssets`、`GetAssetBundle`、`GetAssetTags`、`GetPrimaryAssetIdForPath`、`GetPrimaryAssetRules`、`GetManagedPackageList`、`GetPrimaryAssetLoadList`、`GetLoadedPrimaryAssets`；`EditorInspect` のみ必要）と mutation 5コマンド：`AddPrimaryAssetType` / `RemovePrimaryAssetType`（`DefaultGame.ini` の `PrimaryAssetTypesToScan` へ永続化；PIE中・Live Coding コンパイル中・エンジン終了処理中は拒否）、`SetPrimaryAssetRules`（メモリ内のみの Rule 上書き、非永続；PIE中も許可）、`LoadPrimaryAsset`（ノンブロッキングな明示的ロード；PIE中も許可）、`UnloadPrimaryAsset`（明示的アンロード；PIE中は拒否）。新規 DefaultDenied Capability を5つ追加：`PrimaryAssetTypeAdd`、`PrimaryAssetTypeRemove`、`PrimaryAssetRulesOverride`、`PrimaryAssetLoad`、`PrimaryAssetUnload`。`GetPrimaryAssetIdForPath` は構文的に有効だが未管理のパスに対して `Success: true` かつ `Found: false`（エラーではない）を返し、`GetAssetBundle` が Bundle 未定義のアセットに対して `Success: true` かつ空の `BundleEntries` 配列を返すのと同じ設計方針に従っています。
- **Chaos Cloth Asset 編集**（`UAIPEditorChaosClothAsset` モジュール、**新規**、`ChaosClothAsset` プラグインファミリー必須、UE 5.8、Experimental）: AI エージェントが Clothing Asset の Skeletal Mesh セクションへのバインド/アンバインド、Chaos Cloth Asset の作成・変換、Weight Map 頂点データの読み書き、Import Dataflow ノードへのインポート元メッシュ参照設定を行えるようになりました。`UAIP.Editor.ChaosClothAsset` 配下に10コマンドを追加しました — `CreateClothingAsset`、`AssignClothingToSection`、`RemoveClothingFromSection`（破壊的・不可逆）、`ListClothingAssets`、`GetSectionClothing`、`ConvertClothingAssetCommonToChaosClothAsset`（Experimental、LOD0のみ）、および Toolset に対応がない native 専用4コマンド：`GetClothAssetInfo`（LOD数・Sim/Render Meshの頂点数・参照先 `UDataflow` アセットパス・Weight Map 属性名を取得）、`SetClothWeightMapVertexValues`（Weight Map ノードの頂点ごとの重み配列を直接書き込む破壊的操作）、`SetClothMeshImportSource`（Import ノード `SkeletalMeshImport`/`StaticMeshImport` へのインポート元 SkeletalMesh/StaticMesh 参照設定；ノード種別は自動判定、既存参照の上書きには `AllowOverwrite` が必要な破壊的操作）、`CreateLegacyClothingAsset`（既存 SkeletalMesh の描画セクションからシミュレーションメッシュを抽出し、`UClothingAssetFactory::CreateFromSkeletalMesh` 経由で新規 legacy `UClothingAssetCommon` を作成。legacy クロスのテストフィクスチャ生成に有用）。新規 DefaultDenied Capability を1つ追加：`ClothAssetEdit`。UE 5.8+ で `ChaosClothAssetToolset` プラグインが有効な場合、同じ操作をミラーする6つのブリッジコマンドが `Toolset.Editor.ChaosClothAsset.*` 配下に追加で利用可能です。
- **Dataflow ノードプロパティ Get/Set**（`UAIPEditorDataflow` モジュール）: AI エージェントが、ノードタイプごとにドメイン固有コマンドを用意することなく、Dataflow ノードの `EditAnywhere` プロパティ値を直接読み書きできるようになりました。`UAIP.Editor.Dataflow` 配下に2コマンドを追加しました — `GetDataflowNodeProperty`（プリミティブ / enum / `FName` / `FString` / 単純構造体）と `SetDataflowNodeProperty`（既存の `DataflowGraphEdit` Capability を再利用；新規 Capability は追加なし）。コンテナ型プロパティ（`TArray`/`TMap`/`TSet`）とオブジェクト参照は `InvalidParams` で拒否されます。これはドメイン非依存の汎用機能であり、`UAIPEditorChaosClothAsset` が Cloth の Weight Map・シミュレーション設定ノードのプロパティ編集に利用する仕組みですが、Cloth へのモジュール依存は持ちません。
- **アセットリダイレクタの一覧取得とプロジェクト全体一括修正**（`UAIPEditorAssets` モジュール）: リファクタリング後に残った古いアセットリダイレクタを、AI エージェントが棚卸し・一括修正できるようになりました。`UAIP.Editor.Assets` 配下に2コマンドを追加しました — `ListAssetRedirectors`（読み取り専用；フォルダ配下（既定はプロジェクト全体の `/Game`）のリダイレクタを一覧化し、Asset Registry の `DestinationObject` タグからアセットをロードせずに各エントリの `SourcePath`/`DestinationPath` を解決；`EditorInspect` のみ必要）と `FixAssetRedirectors`（常に `/Game` 全体・再帰的を対象とし `FolderPath` は受け付けない；特定フォルダのみを対象にしたい場合は既存の `FixUpRedirectorsInFolder` を使用；`FixUpRedirectorsInFolder` と同じ DefaultDenied Capability `RedirectorFixup` が必要）。両コマンドは既存 `FixUpRedirectorsInFolder` と共通の修正ロジックを共有するようになり、2点改善されています：失敗判定が単純な前後件数差分ではなく修正前スナップショットとの集合差分になり、呼び出し中に他所で新規発生したリダイレクタを誤カウントしなくなったこと、およびレスポンスに `RequiresSave`（リダイレクタの修正は必ず参照元パッケージをダーティ化するため、事後に `SaveAllPackages` の実行が必要）と `ReferencerPackageCount` / `ReferencersOutsideGameCount`（修正処理は参照元パッケージを書き換えるが、参照元は必ずしも `/Game` 配下とは限らない）を追加したことです。新規 Capability の追加はありません。

**変更**

- **`UAIP.Runtime.World.GetConsoleVariable` および `UAIP.Runtime.World.SearchConsoleVariables` 非推奨化**: 代わりに `UAIP.Runtime.Engine.CVar.GetConsoleVariable` および `UAIP.Runtime.Engine.CVar.SearchConsoleVariables` を使用してください。両コマンドは引き続き動作し、`Success: true` とともにレスポンスの `Data` に `DeprecationWarning` を返します。
- **`UAIP.Core.ListPlugins` 非推奨化**: 代わりに `UAIP.Runtime.Engine.Plugin.ListPlugins` を使用してください。元のコマンドは引き続き動作しますが、将来のリリースで削除される予定です。
- **Niagara モジュールが UE 5.7 に対応**: `UAIP.Editor.Niagara` および `UAIP.Runtime.Niagara` 配下の全コマンド（UAIP ネイティブ 36 本 + Toolset ブリッジ）が UE 5.7 で利用可能になりました。従来 UE 5.7 ではモジュール全体が未登録となり、全コマンドが `CommandNotFound` を返していました。
- **Niagara `default_value` が適用されるように**: `AddSetParametersModule` および `AddSetParameterEntry` で `default_value` フィールドが一般的な型（float / int / bool / `UScriptStruct`）について解析・適用されます。従来は指定値にかかわらず型のデフォルト値でエントリが作成されていました。
- **`AddSetParameterEntry` / `RemoveSetParameterEntry` に `script_name` が必須に** *(破壊的変更)*: 両コマンドに新しい `script_name` パラメータ（例：`Spawn` / `Update` / `Particle Spawn` / `Particle Update`）が必須追加されました。このパラメータは正しいスクリプトスタックへのルーティングと UE 5.8 External Edit API との互換性のために必要です。`script_name` なしの既存呼び出しは `InvalidParams` を返します。
- **`UAIP.Editor.Engine.ConfigSettings.SetSettingsValues` の `DryRun` `ValueType` フォーマットを移行**（`UAIPEditorEngineManagement` モジュール）: `DryRun=true` レスポンスの `WouldChange[].ValueType` フィールドが、これらの型カテゴリについて生の C++ 型名へのフォールバックではなく、`GetSettingsSchema` と同じ型文字列フォーマット（`enum:EMyEnum`・`struct:FMyStruct`・`TArray`・`TMap`・`TSet`・`UObject*:UMyClass`・`uint8`）を使用するようになりました。従来重複していた（かつ対応範囲が狭かった）型名変換ロジックを、`GetSettingsSchema` が既に使用している共有ユーティリティ `FPropertySchemaSerializer` へ統合したものです。`SetSettingsValues` は `Stability: Experimental` のため、本フォーマット変更はバージョニング方針の Experimental 例外条項により非破壊的変更として扱われます。スカラー型（`bool`・`int32`・`int64`・`float`・`double`・`FString`・`FName`・`FText`）には影響しません。

**修正**

- **9つのEditorドメインモジュール（Foliage / WorldPartition / Level / PCG / Niagara / Sequencer / Property / Physics / UMG）でPIE/SIEミューテーションガードを共通化・修正**: 各モジュールに重複実装されていたPIE/SIE拒否ロジックとエディタワールド取得処理を単一の共通実装へ集約し、その過程で以下の潜在バグを修正しました:
  - `SetActorProperty` / `SetWorldSetting` には**PIE/SIEガードが一切存在せず**、Play-In-Editor または Simulate-In-Editor 中でもエディタワールドを変更できてしまう状態でした。`GetActorProperty` / `GetWorldSetting` は影響を受けず、引き続きPIE/Simulate中も成功します。
  - Niagara / Physics / UMG の各コマンドが使用するToolsetブリッジ用バリデーションヘルパーは、Play-In-Editorのみを検知し Simulate-In-Editor を検知できていませんでした。Simulate中のミューテーションがすり抜ける可能性がありました。
  - `SetActorTransform` / `PlaceActorInLevel` / `DeleteActorFromLevel`（Level）および WorldPartition / DataLayer / HLOD の各ミューテーションコマンドは、PIE/Simulate中の拒否時に `NotAllowed` ではなく `ExecutionFailed` を返していました *(このケースで `ExecutionFailed` をパターンマッチしている呼び出し元には破壊的変更)*。現在は他の全ドメインと同じ `NotAllowed` に統一されています。
  - `GetPCGGraphInfo` と `GetSequenceInfo` は引き続きPIE/Simulate状態をレスポンス内の単純なbool値として返し、Play/Simulate中もブロックされません。
- **`uaip_run_scenario` の `Variables` フィールドが `${Variables.<key>}` テンプレートで解決されるように**: シナリオに渡したトップレベルの `Variables` マップはパースされるものの、ステップ実行コンテキストに一度もロードされておらず、`${Variables.<key>}` を参照するステップは全トランスポート（HTTP / MCP / CLI / WS）で常に `ExecutionFailed: Template resolution failed.` になっていました。初期変数は最初のステップ実行前にロードされるようになり、第1ステップから型を保持したまま参照できます。また、シナリオあたりの変数件数上限または単一値のサイズ上限を超える `Variables` は、該当エントリをサイレントに破棄するのではなく `InvalidParams` として事前に拒否されるようになりました。
- **`SetConsoleVariable` / `ResetConsoleVariable` がデフォルトでチートフラグ（`ECVF_Cheat`）付き CVar への書き込みを拒否するように**: 従来は `ECVF_ReadOnly` のみがチェックされており、`RuntimeCVarWrite` を保有するセッションから `ECVF_Cheat` フラグの有無に関わらず CVar を書き換えられていました。新しい `AllowCheatCVarWrite` SafetyPolicy スイッチ（デフォルト `False`）がチートフラグ付き書き込みをゲートし、無効時は `PolicyViolation` を返します。`ECVF_ReadOnly` は引き続きチート判定より優先されます（`NotAllowed`）。書き込み成功時は Artifact とコマンド結果の両方に `WasCheatCVar` の bool 値が出力されるようになりました。
- **Physics ネイティブハンドラを共通PIE/SIEガードへ移行**（`UAIPEditorPhysics` モジュール）: `UAIP.Editor.Physics` 配下の全31ネイティブコマンドは、上記の共通実装ではなく独自のインラインPIE/SIEチェックを実装しており、拒否メッセージも3系統に分裂していました。書き込み系21コマンド（`AddBody` / `SetBox` / `SetCapsule` / `SetSphere` 等）は共通ガードへ移行し、メッセージが単一に統一されました（PIE/Simulate中の挙動自体は変更なし）。読み取り専用の10コマンド（`GetBodyNames` / `GetBodyShapes` / `GetConstraints` / `GetPhysicsAssetSummary` / `ValidatePhysicsAsset` 等）は、PhysicsAssetをディスクから読み込むのみでライブワールドに一切触れないため、PIE/Simulate中でも拒否されなくなりました *(このケースで `NotAllowed` に依存していた呼び出し元には破壊的変更)*。Play/Simulate中に呼び出すとレスポンスに `PieInProgress: true` フィールドが含まれるようになり、上記の `GetPCGGraphInfo` / `GetSequenceInfo` と同様の単純なbool値パターンに揃えられています。
- **`UAIP.Editor.SoundCue.*` コマンドで `bSkipCompile` が実際に反映されるように**（`UAIPEditorSoundCue` モジュール）: `CompileSoundCue`・`AddSoundCueNode`・`RemoveSoundCueNode`・`ConnectSoundCuePins`・`DisconnectSoundCuePins` はいずれもスキーマ上 `bSkipCompile` パラメータを公開していましたが、パーサーが誤った内部キーを参照していたため、呼び出し元が指定した値は常に無視され、グラフは常に再コンパイルされていました。`bSkipCompile: true` を指定すると正しくコンパイルステップをスキップするようになりました。
- **JSONキー不一致により複数の `b` プレフィックス付きパラメータ・レスポンスフィールドが無視されていた問題を修正**（`UAIPEditorGameplayTags`・`UAIPEditorMaterial` モジュール）: コマンドスキーマ上で公開されていた入力パラメータ — GameplayTag系コマンドの `bIncludeNative`・`bAllowNonRestrictedChildren`・`bForceRemoveChildren`・`bUpdateAssetReferences`・`bFallbackToFullScan`、Material系コマンドの `bSkipCompile`・`bAllowParameterDeletion` — は、`b` プレフィックスを欠いた内部キーに対してパースされていたため、呼び出し元が指定した値は常に破棄されデフォルト値のまま扱われていました。同様の不一致は複数の bool 型レスポンスフィールドにも及んでおり、実際の結果に関わらず常にデフォルト値が返されていました：GameplayTag系の `bIsNative`・`bIsRestrictedTag`・`bRedirectAdded`・`bCodeReferencesNotDetected`・`bTruncated`、Material系の `bTruncated`・`bHasInvalidCoords`・`bConnected`・`bAlreadyConnected`・`bRequiresFollowupCompile`・`bIsParameter`・`bHasErrors`。いずれも正しいキーで読み書きされるようになりました。
- **float/double プロパティ値の小数点以下6桁固定パディングを廃止**（`UAIPEditorShared` モジュール。`GetActorProperty`・`GetWorldSetting`・DataTable行の読み取り・Blueprintデフォルト値の読み取りなど、float/doubleプロパティを読むあらゆるコマンドに影響）: 従来は汎用の `%f` ベースのフォールバックでフォーマットされ（`9.5` → `"9.500000"`）ていましたが、API内の他箇所と同じ `FString::SanitizeFloat`（`9.5` → `"9.5"`）を使用するようになりました。
- **`EndSandboxSession` の `DiscardPending` パラメータが非bool値を拒否するように**（`UAIPEditorSandbox` モジュール）: 従来は緩い bool 型強制変換を使用しており、`"yes"` のような任意のJSON文字列を `true` として黙って受理していました。現在は実際のJSON bool値を要求し、それ以外は `InvalidParams` を返します。
- **`FindCueNotifyAssets` の `CueTag` パラメータが `GameplayCue.` プレフィックスを検証するように**（`UAIPEditorGAS` モジュール）: 兄弟コマンド（`AddCueTag`・`RemoveCueTag`・`ExecuteCueOnSelectedActor`）と同様、空でない `CueTag` が `GameplayCue.` で始まらない場合、黙って受理されるのではなく `InvalidParams` を返すようになりました。
- **複数コマンドの ErrorCode を修正**（`UAIPEditorUMG`・`UAIPEditorNiagara`・`UAIPEditorPCG` モジュール）: `AddWidget`・`GetWidgets`・`SetSlotProperties` は対象 WidgetBlueprint のロードに失敗した際、他の全UMGコマンドの規約に合わせて `NotFound` ではなく `ExecutionFailed` を返すようになりました。`RemoveSetParameterEntry` は対象の Niagara システムのロードに失敗した際、`NotFound` ではなく `ExecutionFailed` を返すようになりました。`UpdatePCGCommentBox` は対象コメントボックスの GUID が解決できない際、`RemovePCGCommentBox` と同様に `ExecutionFailed` ではなく `NotFound` を返すようになりました。
- **UE5.7 で `GetItems` のシークレットフィールドマスキングがネストした `FInstancedStruct` フィールドに対して正しく機能するように**（`UAIPEditorDataRegistry` モジュール）: UE5.8 では `FInstancedStruct` 専用の JSON オブジェクト化パスが追加されましたが、UE5.7 には存在せず（代わりに単純な文字列としてシリアライズされる）、マスキング処理がこれを考慮していませんでした。そのため UE5.7 では `FInstancedStruct` 内にネストしたシークレットフィールドがマスクされずに返される可能性がありました。現在は構造体の個別プロパティを検査できない場合、フィールド全体をフェイルセキュアでマスクするようになりました。

---

#### MCP Bridge 1.1.2 — 2026-07-10 リリース済み

**修正**

- **特定の起動環境で同階層モジュールの import が失敗する問題を修正** — `PYTHONSAFEPATH=1`（または `python -P`）を設定するランチャーでは、Python インタプリタがスクリプト自身のディレクトリを `sys.path` に自動追加しなくなります。`thin_proxy.py` はこの挙動に暗黙的に依存して同階層モジュール（`artifact_inliner`・`config`・`http_mcp_client`・`lifecycle_manager`）を import していたため、該当環境ではブリッジの起動が失敗し、バージョン互換チェックの失敗など一見無関係なエラーとして表面化していました。スクリプト自身のディレクトリを明示的に `sys.path` へ追加するよう修正しました。

---

#### MCP Bridge 1.1.1 — 2026-06-24 リリース済み

**修正**

- **`uaip_max_major` の上限を撤廃** — `compatibility.json` の `uaip_max_major` を `null` に変更しました。これにより、ブリッジは `0.9.1` 以上のいかなる UAIP プラグインバージョン（2.x などの将来のメジャーバージョンを含む）にも接続できます。以前は上限値 `1` のせいで、実際の非互換性がなくてもプラグインのメジャーバージョンが上がるたびに新しいブリッジのリリースが必要でした。

---

#### MCP Bridge 1.1.0 — 2026-06-23 リリース済み

**追加**

- **`uaip_reload_config` ツール**: `config.json` を読み直し、起動パラメータ（`editor_path`・`uproject_path`・`http_port`・`enable_scenario`）に変更がある場合は実行中のエディタをシャットダウンして次回ツール呼び出し時に再起動をスケジュールします — MCP セッションを切断せずに実行可能です。オプション引数 `EditorPath` / `UProjectPath` を使うと、`config.json` に書き込まずに現セッション限りで値を上書きでき、MCP クライアントを再起動せずにエンジンバージョンの切り替えが可能です。
- **接続時のバージョン互換チェック**: 起動時に `compatibility.json` マニフェストと照合してプラグインバージョンを検証し、メジャーバージョン不一致の場合は `VersionIncompatibleError` を発生させます。開発環境では `UAIP_BRIDGE_SKIP_VERSION_CHECK=1` でスキップできます。

**修正**

- `uaip_reload_config` 経由で `enable_scenario`（またはその他の起動パラメータ）が変更されたとき、エディタが正しく再起動されるようになりました。従来は `importlib.reload()` が実行中エディタの確認より先に呼ばれていたため、enum の同一性チェックが失敗し再起動がサイレントにスキップされていました。
- エディタの起動・再起動前にクラッシュダイアログ（`WerFault.exe`、`CrashReportClient.exe`）を自動で終了するようになりました。Windows ではクラッシュダイアログがダイアログを閉じるまでプロジェクトの名前付き mutex を保持し続けるため、手動でダイアログを閉じるまで新しいエディタプロセスを起動できない問題がありました。

---

### UAIP Plugin 1.0.0 — 2026-06-18

**UAIP を Fab で製品版として公開しました。** [https://www.fab.com/listings/0eedf909-00ac-4d95-b109-8fda51800fff](https://www.fab.com/listings/0eedf909-00ac-4d95-b109-8fda51800fff)

[![YouTube でローンチトレーラーを見る](https://markdown-videos-api.jorgenkh.no/youtube/o-33jgYLF0A)](https://youtu.be/o-33jgYLF0A)

UAIP の最初の正式版リリースです。製品版（Pro）は Fab Code Plugin としてソース付きで配布され、デモ版のような機能ゲーティングや透かしなしで UAIP の全機能を提供します。デモ版は引き続き GitHub Releases で評価・非商用利用向けに提供します。

#### 製品版でデモ版から解放される機能

- **全 transport** — MCP に加えて HTTP / WebSocket / CLI を有効化
- **Editor 編集コマンド** — Blueprint / Level / Asset / Material / Niagara / Sequencer / AnimBlueprint / ControlRig / PCG / MetaSound / BehaviorTree / StateTree / Dataflow / EQS / CommonConversation / UMG / Physics / Skeleton / GameplayTags / GameFeatures / EnhancedInput
- **190+ Toolset ブリッジ** — UE 5.8 公式 Toolset API への対応で、総コマンド数は約 730 に到達
- **Runtime ワールド編集** — アクター Spawn、GAS 変更、Input 注入
- **`RunEditorPythonScript` による Python スクリプト実行**
- **キャプチャの透かしを削除**

#### 互換性

- UE 5.7 / 5.8 / Windows (Win64)
- 製品版（Pro）の配布は Fab 限定です。デモ版は引き続き本リポジトリの [Demo Releases](https://github.com/Naotsun19B/UnrealAIIntegrationPlatform-Document/releases?q=Demo) で提供
- MCP Bridge は独立バージョニングのまま `MCPBridge-v1.0.0` を継続使用（[Bridge Releases](https://github.com/Naotsun19B/UnrealAIIntegrationPlatform-Document/releases?q=MCPBridge)）

---

### UAIP Plugin 0.9.1 — 2026-06-18

Pro 版の Fab 提出に先立ち **Fab パッケージング規約に準拠** するため、MCP Bridge の配布形態を刷新したデモ版のフォローアップリリースです。本バージョンに含まれるその他のエンジン側改善は Pro 版向けの範疇であり、デモ版に対するユーザー可視な挙動変更はありません。

#### 変更

- **MCP Bridge をプラグインから分離** — Fab パッケージング規約に従い、プラグイン配布物に Python ツールチェインを同梱できないため、Bridge を本リポジトリの **独立した [Release](https://github.com/Naotsun19B/UnrealAIIntegrationPlatform-Document/releases?q=MCPBridge)**（`MCPBridge-v<X.Y.Z>` タグ）として、UE バージョン非依存・MIT ライセンス・デモ / Pro 共用で配布する形に変更しました。インストーラは Bridge を `<UAIP-parent>/UAIPMCPBridge/`（UAIP プラグインと同階層）にデプロイします。詳細は [接続方法 → MCP Bridge](connections.md#mcp-bridge) を参照。

---

### UAIP Plugin 0.9.0 — 2026-06-18

**デモ版を GitHub Releases で先行公開しました。** 製品版はその後 Fab で公開しています — 上記の [UAIP Plugin 1.0.0](#uaip-plugin-100--2026-06-18) エントリを参照してください。

#### 概要

UAIP の最初の公開バージョン（デモ版）です。SemVer 採用方針に基づき、製品版リリース前のフェーズを示す `0.x.y` 系列の初回バージョンとして `0.9.0` から開始します。

#### Added — デモ版に含まれる機能

- **MCP 接続** — Claude Code / Codex CLI / Cursor / Windsurf / GitHub Copilot などの MCP 対応 AI クライアントからエディタを操作
- **観測コマンド** — エディタ状態・ワールド状態・Slate ツリーの JSON ダンプ、各タブ・ビューポートのスクリーンショット取得
- **PIE 制御** — PIE 開始・停止、マップロード
- **アサーションコマンド** — アクタープロパティ・ワールド状態の検証
- **シナリオ実行** — 複数ステップを 1 リクエストで順序実行（中断・リトライ・タイムアウト設定可）
- **UI 自動化** — Slate ウィジェットへのクリック・キー入力・フォーム入力
- **拡張ポイント** — `ICommandProvider` / `ICommandHandler` 経由でのユーザー独自コマンド追加

#### デモ版で利用できない機能（製品版で提供予定）

- HTTP / WebSocket / CLI トランスポート（デモ版は MCP のみ利用可）
- エディタ編集系コマンド（Blueprint / Level / Asset / Material / Niagara など）
- Runtime ワールド編集（Spawn / GAS / Input 注入）
- Python スクリプト実行
- スクリーンショットへの透かしなし運用（デモ版は「UAIP Demo」透かしが合成される）

詳細は [デモ版ガイド](demo.md) を参照してください。

#### 既知の制限

- 対応プラットフォームは Windows (Win64) のみ
- 対応 UE バージョンは 5.7 / 5.8
- macOS / Linux 対応は将来検討項目（v1.0 では未対応）

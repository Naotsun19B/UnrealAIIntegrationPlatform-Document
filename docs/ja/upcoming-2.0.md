**[English](../en/upcoming-2.0.md)** | [概要に戻る](overview.md)

# 2.0.0 で変わること

> **Status: 事前の告知です。** このページに書いてあることで、1.x での呼び出しが変わるものはありません。
> 最終更新: 2026-11-27（末尾の「更新履歴」を参照）

## このページについて

このページは、1.x を使っている間に、すでに使っている呼び出しや設定が 2.0.0 でどう変わるかをお知らせします。各項目に、1.3.0 での**現在**の姿、**2.0.0** での姿、そして**移行**のためにすることを書いています。

- **これは全件の一覧ではありません。** 版や形がまだ決まっていない変更があり、決まり次第ここに足します。2.0.0 の changelog が最終の一覧です。
- 1.3.0 の changelog とこのページが食い違うときは、このページのほうが新しい内容です。
- 2.0.0 に向けて実装済みの変更は、[`next` の changelog](https://github.com/Naotsun19B/UnrealAIIntegrationPlatform-Document/blob/next/docs/ja/changelog.md) にも載ります。そちらは実装した形、このページは予定の形です。
- 1.x の MINOR リリースは予定していません。ここに書いた新しいキー・パラメータ・コマンド・設定は、項目に断りがない限り 2.0.0 で入ります。
- **⚠️ 破壊的変更** は、1.3.0 で動いている呼び出し（1.3.0 で追加したコマンドを含む）の成否・`ErrorCode`・返すキーが変わることを表す印です。コマンドの削除や、付与していたかもしれない Capability の廃止にも使います。1.3.0 の changelog は 1.2.0 を基準に印を付けたので、同じ項目でも印が違うことがあります。印のない項目でも、改名・非推奨・スイッチの削除など、書き換えが要るものがあります。旧い形を受け付け続けるかどうかは、各項目の「移行」に書いています。
- 2.0.0 で削除するコマンドは、`Experimental` の `Toolset.*` コマンドだけです。ほかの `Experimental` のコマンドを削除するときは、その前にここへ載せます（[Deprecation 方針](changelog.md#deprecation-方針基本削除しない)を参照）。
- 2.0.0 の公開時に移行ガイドを別に公開し、このページは記録として残します。

## 今のうちにできる準備

ここに書いたことは、すべて 1.3.0 で今すぐ使えます。

- `Toolset.*` コマンドではなく `UAIP.*` コマンドを呼んでください。エンジンのバージョンに依存しません。
- コンパイルの手順があるアセットへ書き込んだあとは、書き込みがコンパイルするのを当てにせず、コンパイルのコマンド（例: `CompileBlueprint`）を自分で呼んでください。アセットを作るコマンドのあとは、`SaveAsset` を自分で呼んでください。
- 開いているモーダルダイアログによる拒否が返ってきたときは、`RejectReason: ModalActive` を読んでください。変わる `ErrorCode` には頼らないでください。
- すでに `IsMasked` と `MaskedFields` を返している応答では、それを読んでください。すでに `Result.Reason` を返している応答では、それを読んでください。まだ返していない応答には、2.0.0 で加わります。
- `GET /uaip/artifacts/:id` に `SessionId` を渡し、`OpenAsset` と `NormalizeEditorLayout` の成果物では `ActiveTabId` ではなく `ActiveAssetPath` を読んでください。2.0.0 の動作を試すには、エディタを `-uaip-require-artifact-session-id` と `-uaip-active-tab-id-as-layout-id` で起動します。どちらのスイッチも 2.0.0 で削除します。

## Toolset の入口

### ⚠️ 破壊的変更: `Toolset.*` コマンドをすべて削除します
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** 421 件の `Toolset.*` コマンドが、公式 Toolset のツールを呼びます。`Experimental` で、ドキュメントどおりに動きます。
- **2.0.0:** `Toolset.*` コマンドをすべて削除します。別名は残しません。呼ぶと、ヒントなしの `CommandNotFound` が返ります。旧いコマンドと移行先の対応表を、ドキュメントと 2.0.0 の changelog に公開します。`Experimental` のコマンドの削除は、[Deprecation 方針](changelog.md#deprecation-方針基本削除しない)の例外です。下の入口は、Toolset のレジストリがない UE 5.7 では使えません。
- **移行:** 対応する `UAIP.*` コマンドがあるものはそれを使ってください。ないものは、2.0.0 へ移るときに下の入口へ移してください。

### 定義表にないツールは、既定で拒否されます
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** 汎用の入口はまだないので、これは 2.0.0 からの話です。
- **2.0.0:** UAIP の定義表にないツールを呼ぶと、`Reason: ToolNotInDefinitionTable` を伴う `PolicyViolation` が返ります。`[UAIP.SafetyPolicy]` で、ツールを 1 つずつ、または定義表にないツールすべてを許可します。外部の MCP サーバーのツールは、1 つずつしか許可できません。ini のキーと行の書式は、まだ決まっていません。
- **移行:** 呼ぶツールを決めておき、キーが公開されたら `[UAIP.SafetyPolicy]` に書く準備をしてください。

### Toolset へのアクセスは 3 つの Capability で付与します（2.0.0 で追加）
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** `UAIP.*` コマンドの Capability が、`Toolset.*` コマンドにも適用されます。
- **2.0.0:** `ToolsetRead` と `ToolsetEdit` は既定で許可され、コードを実行するツール向けの `ToolsetExecute` は `DefaultDenied` なので、付与が必要です。`UAIP.*` コマンドと同じことをするツールには、そのコマンドと同じ Capability が要ります。
- **移行:** コードを実行するツールを呼ぶなら、2.0.0 へ移るときに `ToolsetExecute` を付与してください。

### 1 つの汎用の入口が代わりになります（2.0.0 で追加）
- **現在:** 公式 Toolset のツールは、それぞれ専用の `Toolset.*` コマンドとして呼びます。
- **2.0.0:** `UAIP.Core.ListToolsetTools`・`UAIP.Core.DescribeToolsetTool`・`UAIP.Core.InvokeToolsetTool` の 3 コマンドを追加します。`Toolset`・`Tool`・`Arguments`（上流の名前のまま）を取り、ツールの結果は `Result.Result` に入ります。呼び出しに上流の名前を使うので、後のエンジンのバージョンでツールが改名されると、呼び出しも変わります。
- **移行:** 2.0.0 より前にすることはありません。

### `refPath` は自分で書きます
- **現在:** Niagara・PCG・Control Rig・Sequencer Control Rig のブリッジが、オブジェクトの引数を代わりに包みます。
- **2.0.0:** 包む処理はなくなります。`Arguments` に `{"refPath": ...}` を自分で書きます。
- **移行:** 新しい入口を呼ぶときは、オブジェクトの引数を `{"refPath": ...}` で渡してください。

## 1.3.0 で追加したコマンド

### ⚠️ 破壊的変更: 1.3.0 で追加した 125 件のコマンドは、名前・キー・エラーコード・応答の形が変わります
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** 1.3.0 のドキュメントに書いたとおりに動きます。
- **2.0.0:** 古いコマンドと同じ共通の規則にそろえます。下の節の変更も含みます。コマンドごとの変更は、2.0.0 の changelog に載せます。
- **移行:** 名前・キー・応答の形は暫定のものとして扱ってください。2.0.0 の一覧を読む前に、応答の正確な形に長く使う道具を組まないでください。

### ⚠️ 破壊的変更: `PasswordState` は `IsMasked` と `MaskedFields` に置き換わります
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** `DumpGameViewportWidgets` は成果物に `Text.PasswordState` を返し、`TypeGameViewportText` の拒否は `Data.PasswordState` を返します。
- **2.0.0:** どちらのコマンドも、マスクした欄を `IsMasked` と `MaskedFields` で示し、`PasswordState` は削除します。
- **移行:** すでに応答に `IsMasked` と `MaskedFields` が付いているところでは、それを読んでください。

### ⚠️ 破壊的変更: 要素の `UnavailableReason` は `Reason` になります
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** `DumpStateTreeInstanceData` は `Blocks[]` の各要素に、CommonUI の `GetInputState` と `GetActionDisplayNames` は `Players[]` の各要素に、それぞれ独自の語彙を持つ `UnavailableReason` を返します。
- **2.0.0:** 各要素が代わりに `Reason` を持ちます。
- **移行:** 2.0.0 へ移るときに、要素の `Reason` を読んでください。

### ⚠️ 破壊的変更: `DumpGameViewportWidgetTexts` は、2 つの許可がそろっただけではパスワード欄のテキストを返さなくなります
- **現在:** Capability `RuntimeWidgetPasswordTextRead` を付与し、`AllowRuntimePasswordFieldRead` をオンにすると、応答にパスワード欄のテキストが入ります。
- **2.0.0:** コマンドに新しいパラメータ（既定は `false`）を足し、それを指定しないとテキストを受け取れません。2 つの許可だけに頼っていた呼び出しは、マスクされた値を受け取ります。
- **移行:** パスワード欄を意図して読んでいるなら、2.0.0 へ移るときに新しいパラメータを渡してください。

## コマンド名とパラメータのキー

### コマンド名とパラメータのキーは共通の規則にそろえ、旧い名前も受け付け続けます
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** ドメインごとに名前が違います。例: 結果の件数の上限は `MaxEntries`・`Limit`・`MaxCount` のいずれか、ページングの開始は `StartIndex`、主のアセットは `<Type>Path` で渡します。
- **2.0.0:** 対象の種類ごとに動詞を 1 つにし、キーの名前をそろえます。`MaxResults`、`Offset` / `NextOffset`、`AssetPath`、`b` の接頭辞を付けない真偽値のキーです。旧いコマンド名で呼ぶと `DeprecationWarning` が付き、旧いパラメータのキーで呼ぶと成功の応答に `DeprecatedParams` が付きます。旧い名前を受け付けなくなる時期はまだ決まっていません。改名の一覧とともに告知します。
- **移行:** 呼び出しを動かし続けるためにすることはありません。更新すべき呼び出しを見つけるには、`DeprecationWarning` と `DeprecatedParams` を見てください。1.3.0 では、`RequestBehaviorTreeAutoArrange` がすでに `ArrangeBehaviorTreeGraph` への移行を促す非推奨になっています。

### グラフのパラメータは `GraphName`・`GraphGuid`・`GraphPath` です
- **現在:** グラフは `TargetGraph`（Animation Blueprint）、`EntryName`（UAF）、`SolveEventName`（Control Rig）、`GraphIndex`（Conversation）で渡します。
- **2.0.0:** それぞれ `GraphName`・`GraphGuid`・`GraphPath` のいずれかに置き換わります（`GraphPath` は 2.0.0 で追加）。今の名前は別名として残します。
- **移行:** 例: Blueprint のコマンドがすでに受け付けている `GraphName` を使ってください。

### ノードのパラメータは `NodeId` です
- **現在:** ノードは、ドメインによって `NodeGuid`・`NodeName`・`NodePath`・`OptionId` などのキーで渡します。
- **2.0.0:** パラメータは `NodeId` です。今の名前は別名として残します。応答のキーも変わります（「グラフ編集」を参照）。
- **移行:** 例: 応答にすでに `NodeId` が付いているところ（Animation Blueprint の読み取りコマンドなど）では、それを読んでください。

### リンクの端は `Output*` と `Input*` です
- **現在:** リンクの端は `Source*` と `Target*`（例: `SourceOutputIndex`・`TargetInputIndex`・`SourceNodeGuid`・`TargetNodeGuid`）で渡します。
- **2.0.0:** 出力ピンのキーを伴う `OutputNodeId` と、入力ピンのキーを伴う `InputNodeId` になります。今の名前は別名として残します。例: Blueprint・Animation Blueprint・Material・Conversation のコマンドが対象です。
- **移行:** 呼び出しを動かし続けるために要ることはありません。

### ⚠️ 破壊的変更: Dataflow のノードの位置は `NodeX` と `NodeY` です
- **現在:** ノードを追加する Dataflow のコマンドは、位置を `X` と `Y` を持つ入れ子の `Position` で受け取ります。
- **2.0.0:** 位置は、ほかのグラフのコマンドと同じく `NodeX` と `NodeY` で渡します。
- **移行:** 入れ子の `Position` を受け付け続けるかどうかはまだ決まっていません。決まったらこの項目に書きます。

### プロパティのキーは `PropertyPath` になります
- **現在:** コマンドによって、キーは `PropertyName`・`SubPropertyName`・`VarName` のいずれかです。例: StateTree のコマンドと `SetBlueprintVariableDefault` は、読み取りと書き込みで違います。
- **2.0.0:** キーは `PropertyPath` です。旧いキーは別名として残します。
- **移行:** 呼び出しを動かし続けるために要ることはありません。

### 要素のキーは `ElementKey` になります
- **現在:** 汎用の要素のコマンドは `ElementKeyJson` を取ります。
- **2.0.0:** キーは `ElementKey` です。`ElementKeyJson` は別名として残します。
- **移行:** 呼び出しを動かし続けるために要ることはありません。

### 時間と長さのキーは `Seconds` で終わります
- **現在:** 時間は `TimeoutSec`・`WaitTimeoutSeconds`（`WaitForWidget`）・`MaxWaitSeconds`（`LoadPrimaryAsset`）で渡し、`WaitSeconds` は `Seconds` を取ります。
- **2.0.0:** タイムアウトは `TimeoutSeconds`、長さは `DurationSeconds` です。旧いキーは別名として残します。
- **移行:** 呼び出しを動かし続けるために要ることはありません。

### パラメータのジョブ ID は `JobId` です
- **現在:** コマンドは、ジョブの ID を独自の名前で受け取ります。`AuditId`・`BuildId`・`InteractionId`・`AnalysisId`・`HLODBuildJobId` または `BuildJobId`・`AttemptId`・`CaptureId` または `RecordingId` です。
- **2.0.0:** パラメータは `JobId` です。旧いキーは別名として残します。応答のキーも変わります（「応答の形とキー」を参照）。1 つのファミリーの非推奨のコマンド（「待機・ジョブ・シナリオ」を参照）は、1.x のキーのままです。
- **移行:** 呼び出しを動かし続けるために要ることはありません。

## 応答の形とキー

### ⚠️ 破壊的変更: 共通の綴りに従わない応答のキーは置き換わります
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** 綴りがそろっていません。真偽値のキーに `b` の接頭辞が付き、同じ概念に複数の綴りがあります。`ReloadPythonCommands` は `refresh_count`・`new_count_skipped`・`removed_count_skipped` を返し、Sequencer の Animation Mixer の応答の一部は小文字の `result` を使います。
- **2.0.0:** 各キーを一度に置き換え、両方の綴りを返す期間は設けません。例: `bIsWorldPartitionEnabled` は `IsWorldPartitionEnabled` になります。置き換えの一覧は 2.0.0 とともに公開します。
- **移行:** 2.0.0 へ移るときに、これらの応答を読むコードを更新してください。

### ⚠️ 破壊的変更: 理由を持つキーは `Reason` に置き換わります
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** 拒否は理由を `FailureReason`・`BlockedReason`・`RefusalReason`・`RejectReason`・`RejectionReason`・`PreconditionReason`・`Cause` などのキーで返し、成功の応答は `SkipReason`・`NotAddableReason` などのキーで返します。
- **2.0.0:** これらのキーは削除し、両方を返す期間は設けません。拒否は `Result.Reason` で、成功の応答は説明する要素の `Reason` で理由を返します。
- **移行:** すでに `Result.Reason` を返している応答では、それを読んでください。

### ⚠️ 破壊的変更: 書き込みの成功の印は、観測した内容に置き換わります
- **現在:** 書き込みが成功すると、`Success: true`・`Removed`・`Updated`・`Deleted`・`Added`・`Compiled`・`Moved`・`Renamed` のような固定の印を返します。例: Behavior Tree・EQS・StateTree のコマンドの `Removed` や、StateTree の `Set*` コマンドの `Updated` が含まれます。
- **2.0.0:** 応答は、書き込みが実際にしたことから観測した `Changed` などの値を持ちます。
- **移行:** これらの印を、何かが変わった証拠として扱わないでください。`Changed` が返るようになったら、それを読んでください。

### ⚠️ 破壊的変更: 「値がない」ことを、空文字列・`null`・`Unknown` で表さなくなります
- **現在:** 応答は、「なし」を空文字列（例: エディタの状態の `ActiveTabId`）で、判定できない値を `null` や `Unknown` で書きます。例: Chooser のセルのコマンドの `Value: null` や、Control Rig の `Content: null` が含まれます。
- **2.0.0:** そのキーを省きます。
- **移行:** キーがないことを「なし」または「不明」として扱ってください。

### ⚠️ 破壊的変更: Insights の `Warnings` の形が変わります
- **現在:** `StartTrace` などの Insights のコマンドは、`Warnings` を `{Code, Message}` の配列で返します。
- **2.0.0:** 形を置き換えます。
- **移行:** 移るときに、2.0.0 の changelog で形を確かめてください。

### ⚠️ 破壊的変更: 意味のない件数を返さなくなります
- **現在:** 途中で切れていない応答でも、`TotalCount`・`ReturnedCount`・`null` の `NextOffset` を返し、失敗のなかった応答でも、空の `Failed` や `FailedCount` を返します（例: `SaveAsset`・`FixAssetRedirectors`）。多くの応答が `IsDegraded: false` と空の `Limitations` を返します。
- **2.0.0:** これらのキーは、情報を持つときだけ返します。
- **移行:** キーがないことを、空または false の値として扱ってください。

### ⚠️ 破壊的変更: 2 つのキーの意味が変わります
- **現在:** 切り詰めの印は、一覧がちょうど上限のとき（`ListWidgetClasses` の 500 件）や、`Offset` が 0 より大きいときの最後のページ（`ListDataTableRows`）で `true` になります。`SetSettingsValues` は、同じ値で書いたキーを `ChangedCount` に数えます。
- **2.0.0:** 切り詰めの印は、最後のページで `false` になるので、`ListDataTableRows` はそこで `true` を返さなくなります。一覧がちょうど上限のときの正確な規則と、`ChangedCount` の正確な規則は、決まり次第ここに足します。
- **移行:** 旧い件数に頼らないでください。

### ⚠️ 破壊的変更: 応答のジョブ ID は `JobId` です
- **現在:** 応答は ID を `AuditId`・`BuildId`・`InteractionId`・`AnalysisId`・`HLODBuildJobId` または `BuildJobId`・`AttemptId`・`CaptureId` または `RecordingId` で返します。
- **2.0.0:** キーは `JobId` で、両方を返す期間は設けません。1 つのファミリーの非推奨のコマンド（「待機・ジョブ・シナリオ」を参照）は、1.x のキーのままです。
- **移行:** 2.0.0 へ移るときに、`JobId` を読んでください。

### ⚠️ 破壊的変更: 経過時間は `ElapsedSeconds` です
- **現在:** `elapsedSeconds`・`ElapsedMs`・`ElapsedSec`・`WaitedSeconds`・`ExecutionTimeSec` の 5 つのキーがあります。
- **2.0.0:** キーは `ElapsedSeconds` の 1 つです。今はミリ秒の値（`ElapsedMs`）は秒に換算します。
- **移行:** `ElapsedMs` を読むコードでは、単位を確かめてください。

### ⚠️ 破壊的変更: `SuggestedCommand` は配列の `SuggestedCommands` になります
- **現在:** `SetAssetProperty`（拒否のとき）と `GetAssetProperty` は `SuggestedCommand` を返します。
- **2.0.0:** どちらも配列の `SuggestedCommands` を返します。
- **移行:** 配列の先頭の要素を読んでください。

### ⚠️ 破壊的変更: `RestartEditor` の拒否から `Remedy` を外し、空の `Remedy` は省きます
- **現在:** 拒否された `RestartEditor` は `Remedy` を返します。`CommandNotFound` のヒントと `ListIntegrations`（操作が要らない連携の場合）は、空の `Remedy` を返します。
- **2.0.0:** `RestartEditor` の拒否は `Remedy` を返さなくなり、文面は `ErrorMessage` に残ります。空の `Remedy` は省きます。`GetRestartStatus` の `Remedy` は残ります。
- **移行:** `RestartEditor` の拒否は `ErrorMessage` を読んでください。

### ⚠️ 破壊的変更: Capability の拒否の名前は `MissingCapabilities` と `DeniedCapabilities` です
- **現在:** Game Viewport のコマンドは `MissingCapability`（単数）を、MVVM のコマンドは `ExplicitlyDeniedCapabilities` を返します。Game Viewport のコマンドのうち 3 つが該当します。
- **2.0.0:** `MissingCapabilities` と `DeniedCapabilities` を返します。
- **移行:** 移るときに、新しいキーを読んでください。

### ⚠️ 破壊的変更: `DumpInputState` は名前だけの `RequiredCapabilities` を返します
- **現在:** `DumpInputState` は `RequiresCapabilities` を返します。
- **2.0.0:** エディションの印を付けない Capability 名の配列、`RequiredCapabilities` を返します。
- **移行:** 移るときに、`RequiredCapabilities` を読んでください。

### ⚠️ 破壊的変更: `Available` は `IsAvailable` になり、常に返します
- **現在:** `ListCommands` と `DescribeCommand` の行は `Available` を返します。
- **2.0.0:** コマンドが使えるかどうかにかかわらず、すべての行が `IsAvailable` を返します。
- **移行:** `IsAvailable` を読んでください。

### ⚠️ 破壊的変更: 成果物の本体も共通のキーの綴りに従います
- **現在:** 成果物の本体には `b` の接頭辞付きのキーや、キャメルケースのキー（`GetAllCachedItems` など 4 か所）があります。本体の変更の印は `Changed` と綴りが違い、時間は 5 つの名前のいずれかで返ります。
- **2.0.0:** キーは応答と同じ綴りに従い、変更の印は `Changed`、時間はそれぞれ 1 つの名前になります。例: `PropertyMutationParams` は `Changed` を返します。
- **移行:** 2.0.0 へ移るときに、成果物の本体を読むコードを更新してください。

## ErrorCode と拒否

### ⚠️ 破壊的変更: 既存のコマンドの一部は別の `ErrorCode` を返し、今は成功する呼び出しの一部は拒否されます
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** 同じ種類の失敗が、コマンドによって別の `ErrorCode` を返します。例: 対象が見つからないとき、あるコマンドは `NotFound`、別のコマンドは `ExecutionFailed` や `InvalidParams` を返します。
- **2.0.0:** 同じ種類の失敗は、どこでも同じ `ErrorCode` を返します。今は別のコードを返しているコマンドが変わり、変更はコマンドとともに 2.0.0 の changelog に載せます。
- **移行:** シナリオやクライアントのコードが `ErrorCode` で分岐しているなら、2.0.0 へ移るときに確かめてください。

### ⚠️ 破壊的変更: 読み取り専用のグラフは、変更せずに拒否します
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** `ConnectBlueprintPins`・`DisconnectBlueprintPins`・`SetPinDefaultValue`・`DeleteGraphNode` は、読み取り専用のグラフを変更し、警告付きで成功します。
- **2.0.0:** 4 つのコマンドは、既定で `NotAllowed` を返して拒否します。
- **移行:** 読み取り専用のグラフの編集に頼らないでください。

### ⚠️ 破壊的変更: 開いているモーダルダイアログによる拒否は、`Reason: ModalActive` を伴う `NotAllowed` です
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** `ClickWidget`・`HoverWidget`・`PressKey`・`InputText`・`FillForm`・`SetCheckboxState`・`SetComboSelection` は、`RejectReason: ModalActive` を伴う `PolicyViolation` を返します。`RestartEditor` は `PreconditionFailed` を返します。`AcceptDialog` と `CancelDialog` は、答えるダイアログがないとき `ExecutionFailed` を返します。
- **2.0.0:** 7 つのコマンドと `RestartEditor` は、`Result.Reason: ModalActive` を伴う `NotAllowed` を返し、`AcceptDialog` と `CancelDialog` は `NotFound` を返します。
- **移行:** `ErrorCode` ではなく、今は `RejectReason: ModalActive` を読んでください。

### ⚠️ 破壊的変更: 自分の期限で止まるコマンドは `Timeout` を返します
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** `WaitForShaderCompilation`・`RecompileGlobalShaders`・`CompileLiveCoding` は、成果物に `Status: "Timeout"` を入れて成功します。`WaitForCondition` と `RunFunctionalTest` は、`Data.TimedOut: true` を伴う `ExecutionFailed` を返します。例: `StartPIE`・`LoadMap`・`WaitForWidget`・`CompileNiagaraSystem`・`FillForm` も違います。
- **2.0.0:** これらは `Timeout` を返します。キー `TimedOut`・`Aborted`・`NotExecuted` は `WorkAfterTimeout` に置き換わります（「待機・ジョブ・シナリオ」を参照）。
- **移行:** 移るときに、これらのキーではなく `ErrorCode` で分岐してください。

### ⚠️ 破壊的変更: `Timeout` の HTTP ステータスは 504 です
- **現在:** `Timeout` は、`api.md` に書いたとおり HTTP 408 です。
- **2.0.0:** `Timeout` は HTTP 504 です。
- **移行:** スクリプトが HTTP ステータスを直接読んでいるなら、504 を受け付けてください。

### ⚠️ 破壊的変更: 終了中に断られた要求は、`Reason: EngineExitRequested` を伴う `NotAllowed` です
- **現在:** エンジンの終了中に、キューが受け付けない要求は `InternalError` を返します。
- **2.0.0:** `Reason: EngineExitRequested` を伴う `NotAllowed` を返します。
- **移行:** 内部エラーではなく、拒否として扱ってください。

### ⚠️ 破壊的変更: `CapabilityNotAvailable` は HTTP 403 です
- **現在:** `api.md` には 403 と書いてありますが、`CapabilityNotAvailable` は HTTP 503 で送られます。
- **2.0.0:** ドキュメントどおり、HTTP 403 で送られます。
- **移行:** スクリプトが HTTP ステータスを直接読んでいるなら、403 を受け付けてください。

### ⚠️ 破壊的変更: 送信元の制限で断られた要求は `PolicyViolation` です
- **現在:** 送信元を理由に断られた HTTP 要求は、`ErrorCode` の表にない `Forbidden` を返します。
- **2.0.0:** `PolicyViolation` を返します。
- **移行:** `Forbidden` を `PolicyViolation` として扱ってください。

### ⚠️ 破壊的変更: 読み込み中のコマンドは、`Reason: IntegrationLoading` を伴う `TooManyRequests` です
- **現在:** `Pending` または `Loading` の状態にある連携のコマンドは、`CommandNotFound` を返します。
- **2.0.0:** `Reason: IntegrationLoading` を伴う `TooManyRequests` を返します。
- **移行:** コマンドがないものとして扱わず、`TooManyRequests` で再試行してください。

### ⚠️ 破壊的変更: ジョブのキューが混んでいるときは `TooManyRequests` を返します
- **現在:** キャプチャの 3 領域はキューが満杯のとき `NotAllowed` を返し、再起動の試行は `Conflict` を返し、Automation は成功を返してエラーをレポートに載せます。
- **2.0.0:** すべて `TooManyRequests` を返します。
- **移行:** `TooManyRequests` で再試行してください。

### ⚠️ 破壊的変更: Play-In-Editor の確認が、引数の検証より先に走ります
- **現在:** Play セッションの間、不正な引数での書き込みは、検証のエラーを返します。
- **2.0.0:** Play セッションの確認が先に走るので、同じ呼び出しが、Play セッションを理由にした拒否を返します。例: World Partition・MVVM・Level・Enhanced Input・Mass の書き込みが対象です。
- **移行:** Play セッション中の書き込みの `ErrorCode` で分岐しているなら、確かめてください。

### ⚠️ 破壊的変更: コマンドレットで使えない GameFeature の操作は `AbilityUnavailable` です
- **現在:** `CreateGameFeaturePlugin` と `DeleteGameFeaturePlugin` は、コマンドレットで `NotAllowed` を返します。
- **2.0.0:** `AbilityUnavailable` を返します。
- **移行:** `AbilityUnavailable` を読んでください。

### ⚠️ 破壊的変更: 許される範囲の外にある上限は、拒否します
- **現在:** コマンドは、時間の上限を範囲に丸めたり（例: `CompileNiagaraSystem`・LiveLink の検出・`WaitForWidget` の下限）、効かない値を受け付けたり（`RunEditorPythonScript` の `TimeoutSec`）します。
- **2.0.0:** 許される範囲の外の値は `InvalidParams` を返します。
- **移行:** `DescribeCommand` が宣言する範囲の中の値を送ってください。

### ⚠️ 破壊的変更: 編集できない AnimNotify のフィールドは `PolicyViolation` です
- **現在:** 汎用のプロパティのコマンドは、編集できない AnimNotify のフィールドに `NotAllowed` を返します。
- **2.0.0:** `PolicyViolation` を返します。
- **移行:** `PolicyViolation` で分岐してください。

### ⚠️ 破壊的変更: 型の違う値は `InvalidParams` です
- **現在:** `SetPCGNodeProperty` と StateTree の `AddPropertyBinding` は、型の違う値に `ExecutionFailed` を返します。
- **2.0.0:** `InvalidParams` を返します。
- **移行:** `InvalidParams` で分岐してください。

### ⚠️ 破壊的変更: 一部が使えない操作は `AbilityUnavailable` です
- **現在:** 環境のせいでできない操作が、別のコードを返します。例: `SetTransformGizmoSize` は `AxisSizeMultiplier` に `InvalidParams` を返し、Niagara の `DuplicateEmitter` は `NotAllowed` を返し、`GetTransformGizmoSize` は `AxisSizeMultiplierUnavailableReason` に理由を書きます。
- **2.0.0:** これらは `AbilityUnavailable` を返します。
- **移行:** `AbilityUnavailable` で分岐してください。

## 識別子と参照

### ⚠️ 破壊的変更: 応答の識別子は、パラメータと同じ形・同じキー名になります
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** 応答の `AssetPath` がオブジェクトパスのことがあり（例: `ListSoundClasses`・`ListPrimaryAssets`・DataLayer のコマンド）、クラスは短い名前で、参照は引用符付きのエクスポートテキストで、GUID はハイフン付きで、パラメータと同じ識別子を持つキーが別の名前であることも多くあります。`GetOpenAssets` と `GetSelectedAssets` はオブジェクトパスだけを返します。
- **2.0.0:** `AssetPath` はパッケージパス、クラスは完全なパス、参照は素のオブジェクトパス、GUID はハイフンなしの 16 進 32 桁、パラメータと同じ識別子を持つキーはパラメータの名前になります。置き換えは、両方を返す期間を設けずに行います。
- **移行:** 2.0.0 へ移るときに、応答の識別子を解析するコードを更新してください。

### ⚠️ 破壊的変更: `TabId` は Slate のタブ ID だけを指します
- **現在:** `TabId` は、`CaptureGraphViewportImage`・`DumpSelectionState`・`ListGraphNodes`・`DragGraphNode`・`ConnectGraphPins` ではタブ ID の一部に一致し、`FrameGraphAll`・`FrameGraphSelection`・`SetGraphSelection`・`SetGraphZoom` ではアセットパスとして読まれます。
- **2.0.0:** `TabId` は Slate のタブ ID そのものです。アセットは `AssetPath` で渡します。`DragGraphNode` と `ConnectGraphPins` は、1.x の `TabId` のままです（「グラフ編集」を参照）。
- **移行:** タブ ID そのものを渡してください。

### ⚠️ 破壊的変更: `ActorIdentifier` はアクターのオブジェクトパスを持ちます
- **現在:** アクターを返す Runtime の応答は、パスを `Path` または `SpawnedActorPath` で返します。
- **2.0.0:** アクターを返すすべての応答が、オブジェクトパスを `ActorIdentifier` で返し、その 2 つのキーは置き換わります。例: `PlaceActorInLevel` と `GetActorTransform` が返します。
- **移行:** `ActorIdentifier` を読んでください。

### ⚠️ 破壊的変更: Foliage の読み取りコマンドは、エディタのワールドを読みます
- **現在:** `GetFoliageInstanceCount`・`GetFoliageInstances`・`GetFoliageTypeInfo`・`ListFoliageTypes` は、Play セッション中は実行中のワールドを読みます。
- **2.0.0:** エディタのワールドを読みます。
- **移行:** これらのコマンドが Play セッションを読むことに頼らないでください。

### ⚠️ 破壊的変更: `ListPlayWorlds` はセレクターのキーを使います
- **現在:** `ListPlayWorlds` と応答のコンテキストは、`PIEInstance` と `NetMode` を返します。
- **2.0.0:** ワールドを選ぶのと同じキー、`TargetPIEInstance` と `TargetNetRole` を返します。
- **移行:** 新しいキーを読んでください。

### ⚠️ 破壊的変更: 型の違うウィジェットの参照は `NotFound` です
- **現在:** 型の違うウィジェットの参照は、`TypeMismatch` を伴う `InvalidParams` を返します。
- **2.0.0:** `NotFound` を返します。
- **移行:** `NotFound` で分岐してください。

### ⚠️ 破壊的変更: 複数の対象に一致する名前は拒否します
- **現在:** 複数の対象に一致する名前も、そのまま使われます。`FocusOnActors` と `SelectActors` は全部に作用し、Niagara・Sequencer Control Rig・`TabId` では、書き込みでも最初の一致が使われます。例: `SelectMenuItem` と `FocusEditorTab` のラベルは、最初の一致を使います。
- **2.0.0:** 呼び出しは、候補を添えた `InvalidParams` を返します。
- **移行:** 対象が 1 つに決まる名前か ID を渡してください。

## 秘密の値

### ⚠️ 破壊的変更: 旧い秘密マスクのキー 3 種を削除します
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** `SetSettingsValues` は変更のエントリに `MaskedReason` を返し、4 つの StateTree コマンド（`GetStateTasks`・`GetStateEnterConditions`・`GetStateTreeGlobalTasks`・`GetStateTreeEvaluators`）は `MaskedDueToPolicy`（常に `false`）を返し、DataRegistry の `GetItems`・`GetAllCachedItems`・`AcquireItems` は `MaskedFieldCount` を返します。
- **2.0.0:** 3 つのキーを削除し、両方を返す期間は設けません。印は `IsMasked`・`MaskedFields`・`UnverifiedMaskedFields` です。DataRegistry のコマンドと `SetSettingsValues` の変更のエントリに、`IsMasked` と `MaskedFields` が加わります。
- **移行:** 今返っているところでは `IsMasked` と `MaskedFields` を読んでください。`MaskedDueToPolicy` は無視してください。

### ⚠️ 破壊的変更: 名前と値の対応表の中の値が、それぞれ `IsMasked` を持ちます
- **現在:** `DumpMassEntityConfig` は `OwnTraits[]` の `Properties` を対応表で返し、何かをマスクしたときは、その隣に `IsMasked: true` と `MaskedFields` を置きます。`GetWidgetProperties`（`Properties`）・`SetWidgetProperties`（`PreviousValues`）・`GetSlotProperties` は `MaskedFields` だけを返します。
- **2.0.0:** 対応表は、各値が `IsMasked` を持てる形になります。書き込みの入力である `InitialProperties` と `SetWidgetProperties` の `Properties` も同じ形を取るので、読んだものをそのまま書き込みに渡せます。
- **移行:** UMG の応答では、今は `MaskedFields` を読んでください。

## 編集のトランザクション・コンパイル・保存

### ⚠️ 破壊的変更: 書き込みは、元に戻したかどうかを 1 つの共通の方法で報告します
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** 何かを変えたあとで失敗した書き込みは、それを別々の名前で報告します。`GraphIntegrityState`（`ApplyBlueprintGraphEdit`）、`TableIntegrityState`（Chooser）、`Status: RolledBack`・`RollbackFailed`・`RolledBackWithLeftovers`・`RemainingComponents`・`MissingAfterRollback`（`RemoveDynamicsChain`）、`bFinalizeRolledBack`（Motion Matching）、またはメッセージの中だけです。`RemoveDynamicsChain` は、すべてを元に戻したときに `Success` を返します。
- **2.0.0:** 失敗した書き込みは `Result.IntegrityState`（`Intact`・`RestoredByRollback`・`ChangesRemain`）と `Result.Remaining` を持ちます。ほかの名前は削除します。`RemoveDynamicsChain` は、すべてを元に戻したときに失敗します。
- **移行:** 2.0.0 へ移ったら `Result.IntegrityState` を読み、`Status: RolledBack` を成功として扱わないでください。

### ⚠️ 破壊的変更: 書き込みはアセットをコンパイルしなくなります
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** 多くの書き込みは、変更したアセットを、既定で（`SkipCompile` / `bSkipCompile` で切れます）または常にコンパイルします。`ApplyBlueprintGraphEdit` と `SetPinDefaultValue` は、コンパイルが新しいエラーを報告すると、書き込みを元に戻します。`CompileMaterial`・`CompileWidgetBlueprint`・`CompileMetaSound`・`CompileNiagaraSystem` は、コンパイルの失敗を成果物で報告しつつ成功を返し、`CompileControlRig` と `CompileSoundCue` は常に成功を報告します。
- **2.0.0:** 書き込みはアセットを編集するだけで、コンパイルの手順があるアセットへのすべての書き込みが `Result.RequiresFollowupCompile` を持ちます。コンパイルするのはコンパイルのコマンドだけです。エラーを見つけたコンパイルのコマンドは、`Result.CompileErrors` を伴う `ExecutionFailed` を返します。`SkipCompile` をどうするかは、2.0.0 とともに告知します。
- **移行:** 書き込みのあとに、`CompileBlueprint` などのコンパイルのコマンドを自分で呼び、その結果を確かめてください。

### ⚠️ 破壊的変更: アセットを作るコマンドは、保存しなくなります
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** `CreateWidgetBlueprint`・`CreatePhysicsAsset`、Groom のインポート・バインディング・テクスチャのコマンド、`CreateLegacyClothingAsset`（変更する Skeletal Mesh も保存します）は、作ったものや変更したものを保存します。
- **2.0.0:** 保存を求めた要求だけが保存します。作ったアセットは、パッケージを変更済みにした未保存のままで、応答は保存したものを `Result.SavedPackages` に、書き出したファイルを `Result.WrittenFiles` に載せます。
- **移行:** アセットを作ったあとに、`SaveAsset` を自分で呼んでください。

## グラフ編集

### ⚠️ 破壊的変更: グラフのパラメータを省くと、アセットの既定のグラフを指します
- **現在:** グラフのパラメータを省いた呼び出しの動作は、コマンドごとに違います。例えば、Blueprint のコマンドにはすべてのグラフを探すものとイベントグラフを使うものがあり、Animation Blueprint の `AddAnimGraphNode` はグラフのパラメータを持たず、常に最初の AnimGraph を使います。
- **2.0.0:** グラフが複数あるドメインでは、グラフのパラメータを省くと、そのドメインの既定のグラフを指すものとして扱い、コマンドの説明にどのグラフかを書きます。`AddAnimGraphNode` などグラフのパラメータを持たないコマンドには、それが加わります（2.0.0 で追加）。各ドメインの既定のグラフは、2.0.0 の一覧で決めます。
- **移行:** グラフのパラメータを受け付ける呼び出しすべてで、グラフを明示してください（例: `GraphName`）。

### ⚠️ 破壊的変更: 応答はノードを `NodeId` と呼びます
- **現在:** 応答はノードを、`NodeGuid`・`NodeName`・`NodePath`・`OptionId`・`TestId`・`StateId`・`TaskId`・`ModuleId`・`EmitterId`・`StateNodeId` など、それぞれの名前のキーで返します。例えば、Dataflow・Conversation・`GetBehaviorTreeSubtree`・UAF・Control Rig・PCG・EQS・StateTree・Niagara が該当します。Animation Blueprint の読み取りコマンドは、すでに同じノードを `NodeId` で返しています。
- **2.0.0:** キーは `NodeId` です。応答の中で役割を持つノードは、`ParentNodeId`・`HostNodeId`・`OutputNodeId`・`InputNodeId` です。パラメータのキーも変わります（「コマンド名とパラメータのキー」を参照）。
- **移行:** 応答がすでに `NodeId` を持っているところでは、それを読んでください。

### ⚠️ 破壊的変更: グラフの読み取りは、接続を `Links` で返します
- **現在:** 接続の一覧は、それぞれの名前を持ちます。`Edges`（PCG・MetaSound）、`Connections`（Dataflow と、SoundCue のノードの中）、`Transitions`（Animation Blueprint のステートマシン）です。端は、`From*` と `To*`（MetaSound）、`FromStateId` と `ToStateId`（Animation Blueprint のステートマシン）、または出力ノードを持たない `OutputPinIndex`・`InputNodeId`・`InputPinIndex`（SoundCue）です。Animation Blueprint は、各ピンに `LinkedTo` だけを返します。
- **2.0.0:** ピンを含むグラフ全体を返す読み取りは、`Nodes` と `Links` を持ち、各リンクは 1 回だけ現れます。リンクは、接続のコマンドのキー（`OutputNodeId`・`InputNodeId` とピンのキー）で書かれるので、読んだものをそのまま接続や切断の呼び出しに渡せます。ピンの `LinkedTo` も同じキーを使います。
- **移行:** 2.0.0 へ移るときに `Links` を読んでください。PCG と Dataflow は、すでに端に接続のコマンドのキーを使っています。変わるのは一覧の名前だけです。

### ⚠️ 破壊的変更: 読み取りのノードの位置とクラスは、共通のキーを使います
- **現在:** 位置は、`GetDataflowGraphInfo`・`ListGraphNodes`・`DumpSelectionState` では、`X` と `Y` を持つ入れ子の `Position` です。MetaSound・UAF・Control Rig（`ListNodes`）・Conversation は位置を返しません。ノードのクラスには、`NodeClass`・`ExpressionClass`・`SettingsClassPath`・`TypeName`・`ClassName`・`GeneratorClass`・`StructPath` の 7 通りの書き方があります。
- **2.0.0:** `Nodes` の各要素は、`NodeId`、ノードのクラスの完全なパス、座標を持つグラフでは `NodeX` と `NodeY` を持ちます。入れ子の `Position` と 7 つのクラスのキーは置き換わり、位置が無かったところには加わります。クラスのキーの名前は、2.0.0 とともに一覧にします。
- **移行:** 2.0.0 へ移るときに `NodeX` と `NodeY` を読んでください。

### ⚠️ 破壊的変更: 既存のリンクを切ることになる接続には、`AllowBreakOthers` が要ります（2.0.0 で追加）
- **現在:** すでにリンクのある入力ピンへ接続したときの動作は、ドメインによって違います。Dataflow・MetaSound・Conversation はそうした接続を拒否し、ほかのドメイン（例: Animation Blueprint・Material・SoundCue）は、エディタのスキーマに判断を任せ、古いリンクが置き換わることがあります。
- **2.0.0:** そうした接続は、`AllowBreakOthers: true` のときだけ行います。無ければ、呼び出しは `Conflict` を返し、切ることになるリンクを `Result.ExistingLinks` に並べます。リンクを切った書き込み（置き換え・切断・ノードの削除）は、切ったリンクを `Result.RemovedLinks` に並べます。
- **移行:** これまでの結果を保ちたいときは、接続する前に、ドメインの切断のコマンド（例: `DisconnectBlueprintPins`）で既存のリンクを自分で切ってください。

### ⚠️ 破壊的変更: 型の変換が要る接続には、`AllowConversion` が要ります（2.0.0 で追加）
- **現在:** 単独の `ConnectBlueprintPins` は型の昇格を受け付けますが、`ApplyBlueprintGraphEdit` の中のバッチは拒否します。Animation Blueprint と Material は、スキーマが不可能とするものだけを拒否して残りをエンジンに任せ、Conversation は変換ノードが要る接続を受け付けます。
- **2.0.0:** 変換が要る接続は、`AllowConversion: true` のときだけ行います。無ければ、呼び出しは `InvalidParams` を返し、拒否の文は必要な変換（挿入するノードの種類、または昇格させる型）を示します。行った変換は `Result` に載り、挿入したノードの `NodeId` と、型が変わったピンを伴います。`ApplyBlueprintGraphEdit` もこのパラメータを取ります。
- **移行:** ピンが期待する型を渡すか、変換のノードを自分で挿入してください。

### ⚠️ 破壊的変更: `ApplyBlueprintGraphEdit` は、接続の端を単独の接続コマンドと同じように書きます
- **現在:** 各端は、入れ子の `From` または `To` のオブジェクトで、ノード（`NodeId` または `NodeRef`）とピン（`PinName` または `PinId`）を持ちます。
- **2.0.0:** 端は、ほかの接続コマンドと同じキーを使います。`OutputNodeId` と `InputNodeId` とピンのキーです。
- **移行:** 2.0.0 の前にすることはありません。入れ子の形を受け付け続けるかどうかは、まだ決まっていません。決まったらこの項目に書きます。

### ⚠️ 破壊的変更: すでにあるリンクの接続と、無いリンクの切断は成功します
- **現在:** Dataflow は、入力ピンにリンクがあるとき、すでにあるリンクの接続を拒否します。`DisconnectBlueprintPins` は、無いリンクに `ExecutionFailed` を返し、Conversation は `NotFound` を返します。
- **2.0.0:** どちらも `Changed: false` で成功します。ノードやピンが無い切断は `NotFound` です。
- **移行:** これらの失敗で分岐しないでください。

### ⚠️ 破壊的変更: ピンの向きを推測しなくなります
- **現在:** Animation Blueprint は、指定した名前の出力ピンを先に探し、無ければ入力ピンを取ります。Blueprint の単独の接続は `Source*` と `Target*` を取り、どちらが出力かをスキーマが判断します。
- **2.0.0:** 向きはキー（`Output*` または `Input*`）で与え、名前から推測することはありません。推測に頼っていた呼び出しは動かなくなります。
- **移行:** 各ピンを、向きに合ったキーで渡してください。

### ⚠️ 破壊的変更: 削除できないノードの削除は `NotAllowed` です
- **現在:** エントリ・ルート・出力のノードの削除は、Blueprint（`DeleteGraphNode`）・Material・SoundCue・バッチ編集では `Conflict` を返し、Behavior Tree のルートでは `NotFound` を返します。確認の無いドメインもあります。
- **2.0.0:** 呼び出しは `NotAllowed` を返します。
- **移行:** `NotAllowed` で分岐してください。

### ⚠️ 破壊的変更: 書き込みが取り除いたリンクは `Result.RemovedLinks` にあります
- **現在:** 削除は、壊したリンクを `BrokenConnections`（Blueprint）・`RemovedEdges`（MetaSound と SoundCue）・`BrokenLinks`（バッチ編集）で報告します。ほかのドメインは何も報告しません。
- **2.0.0:** 3 つのキーは `Result.RemovedLinks` に置き換わり、要素は `Links` と同じです。
- **移行:** 2.0.0 へ移るときに `Result.RemovedLinks` を読んでください。

### ⚠️ 破壊的変更: 接続済みの入力ピンへの既定値の書き込みは `NotAllowed` です
- **現在:** Blueprint は `ExecutionFailed` を返し、Animation Blueprint の `SetAnimGraphNodeProperty` は何も言わずに書き込みを飛ばし、UAF・Control Rig・MetaSound・Niagara は確認しません。
- **2.0.0:** 呼び出しは `NotAllowed` を返します。
- **移行:** `NotAllowed` で分岐してください。

### ⚠️ 破壊的変更: ピンは 1 つの文字列ではなく、オブジェクトです
- **現在:** `ListUAFPins` と Control Rig の `ListPins` は、各ピンを `Name (Direction, CPPType)` の形の 1 つの文字列で返します。Animation Blueprint の `PinType` はカテゴリだけを持ち、PCG はピンを、型の無いラベルの文字列の配列で返します。
- **2.0.0:** ピンは、名前・識別子（ドメインによって ID・インデックス・パス）・向き・型を、別々のキーで持つオブジェクトです。1 つの文字列の形は削除し、Animation Blueprint と PCG のピンには足りなかったキーが加わります（2.0.0 で追加）。
- **移行:** その文字列の解析に頼ったコードを作らないでください。

### ⚠️ 破壊的変更: ツリーの読み取りは、すべてのノードに `ParentNodeId` と `ChildIndex` を付けます
- **現在:** `GetBehaviorTreeNodeList` は `ParentNodeGuid` と `Depth` を返し、兄弟の順序はありません。`GetBehaviorTreeSubtree`・EQS・Niagara は入れ子の形だけを返し、StateTree は `ParentStateId` と、順序が配列の位置である入れ子の形を返します。
- **2.0.0:** ツリーの読み取りは、各ノードが `ParentNodeId`（ルートは null）と、兄弟の中の順序である `ChildIndex` を持つ平らな一覧を返します。入れ子の形を返す読み取りも、各ノードに同じ 2 つのキーを付けます。今の親のキーは置き換わります。
- **移行:** 2.0.0 へ移るときに `ParentNodeId` を読んでください。

### ⚠️ 破壊的変更: 汎用 UI のグラフコマンドは、ドメインの `NodeId` を取ります
- **現在:** `SetGraphSelection` などの汎用のグラフコマンドは、エディタのグラフの `NodeGuid` を使います。Material（式の GUID）と Dataflow（ドメインの GUID）では、ドメイン自身の ID とは別の値で、`SetGraphSelection` は何にも一致しない ID を何も言わずに無視します。UAF・Control Rig・PCG はノードを名前で識別するので、そのノードはまったく渡せません。
- **2.0.0:** これらのコマンドは、ドメインの `NodeId` を取り、返します。
- **移行:** 2.0.0 へ移るときに、ドメインの読み取りコマンドが返す `NodeId` を渡してください。

### `AddState` は `AfterStateId` を省くと末尾に追加します
- **現在:** StateTree の `AddState` は、`AfterStateId` を省くと、ステートを先頭に追加します。
- **2.0.0:** 兄弟の中で最後にステートを追加します。呼び出しはこれまでどおり成功し、キーも変わりません。変わるのは結果の順序だけです。
- **移行:** 位置を保ちたいときは `AfterStateId` を渡してください。

### `DragGraphNode` と `ConnectGraphPins` は非推奨です
- **現在:** `DragGraphNode` はグラフのノードをピクセルの差分で動かし、`ConnectGraphPins` はグラフエディタのタブで 2 つのピンを接続します。
- **2.0.0:** 2.0.0 で非推奨になります。名前は受け付け続けます。代わりに、各ドメインの移動と接続のコマンドを使ってください。パラメータと応答は 1.x のままで、このページの共通のグラフのキー（`NodeId`・`Output*` と `Input*` など）と `TabId` の新しい意味は当てはまりません。非推奨になるのは、すべてのドメインが移動と接続のコマンドを持つ版で、それまでは非推奨の印を付けません。非推奨になった後は、成功した呼び出しの `DeprecationWarning` が、ドメインごとに使うコマンドを示します。`MigrationTarget` は 1 つに決まらないので置きません。
- **移行:** 1.x 向けに書いた呼び出しは動き続けます。ドメインのコマンド（例: `ConnectBlueprintPins`）で接続してください。ノードを動かすには、Control Rig なら `SetNodePosition`、PCG なら `RepositionPCGNode` を使います。ほかのドメインでノードを動かすコマンドは、2.0.0 で追加されます。

## プロパティの読み書き

### ⚠️ 破壊的変更: 読み取りは `Value` を JSON の値で返します
- **現在:** `GetActorProperty`・`GetWorldSetting`・`GetAssetProperty`・`GetBlueprintDefault`・`GetProjectSetting`・`GetDataTableRow` は、`Value` を文字列で返します。エンジンのテキスト、または文字列の中の JSON です。参照を含む値は、テキストに戻ります。各ドメインのプロパティの読み取りには、それぞれの形があります。
- **2.0.0:** `Value` は JSON の値そのもので、形は以下の型ごとの定めに従います。文字列の中の JSON と、エンジンのテキストは使いません。
- **移行:** `Value` をテキストとして解析しているコードは、2.0.0 へ移るときに JSON を読むよう準備してください。

### ⚠️ 破壊的変更: 書き込みは `Value` を JSON で取り、エンジンのテキストは拒否します
- **現在:** `SetActorProperty`・`SetWorldSetting`・`SetAssetProperty`・`SetBlueprintDefault`・`SetProjectSetting`・`SetDataTableRow` は、値を `Value` のエンジンのテキスト、または `ValueJson` の JSON で取り、型によってどちらを受け付けるかが決まります。各ドメインのプロパティのコマンドは、値を 9 通りの方法で取ります。例えば、テキストの `PropertyValue`・JSON の `PropertyValue`・`Value`・`DefaultValue` です。
- **2.0.0:** 値は、`Value` の 1 つの JSON の値です。構造体を期待するところに `(X=1,Y=2)` のようなエンジンのテキストを書いたり、型の違う JSON の値を書いたりすると、`InvalidParams` を返し、何も変換しません（数値に文字列を渡しても、数値として読みません）。
- **移行:** 参照・構造体・コンテナは、コマンドが取るところでは `ValueJson` に書いてください（15 のコマンド。Subsonic のコマンドは、すでに JSON の `Value` を取ります）。`ValueJson` を 2.0.0 でも受け付け続けるかどうかは、まだ決まっていません。決まったらこの項目に書きます。

### ⚠️ 破壊的変更: 型は読み取りと書き込みで 1 つの形を持ちます
- **現在:** 同じ型の読み取りと書き込みが違います。マップは `{"A":1}` として読まれ `[{Key,Value}]` として書かれ、`TOptional` とデリゲートはテキストとして読まれ、真偽値は `"True"`、浮動小数点は `"9.5"` として読まれ、宣言されていない列挙値は `"(INVALID)"`、ビットフラグは `|` で結んだ 1 つの文字列として読まれ、`FGuid`・`FGameplayTag`・カタログの 17 の構造体型はテキストだけで、`FText` を書き戻すとキーが失われ、読んだ Instanced オブジェクトのパスを書き戻すとコピーができます。`FDateTime` と `FInstancedStruct` は読めますが書けません。
- **2.0.0:** 読み取りと書き込みに、形の 1 つの表を使います。真偽値は JSON の真偽値、整数と浮動小数点は JSON の数値（2^53 を超える 64 ビット整数は 10 進の文字列）、列挙は短い名前、構造体はメンバーのオブジェクト（書き込みは一部だけを与えてよく、残りは値を保ちます）、コンテナは配列で書き込みは全体を置き換え、マップは `[{"Key": …, "Value": …}]`、`TOptional` は `{"IsSet": …, "Value": …}`、デリゲートは `{"ObjectPath": …, "FunctionName": …}`、`FInstancedStruct` は `{"StructType": …, "Value": {…}}`、`FText` は文字列または `{"Namespace", "Key", "SourceString"}`、`FGuid` は 32 桁、`FGameplayTag` はその名前、`FDateTime` は ISO 8601 の文字列、参照は素のオブジェクトパスです（「識別子と参照」を参照）。読んだ値は、同じパスへ書き戻すと `Changed: false` で成功します。`FDateTime` と `FInstancedStruct` は書き込めるようになります（2.0.0 で追加）。
- **移行:** 2.0.0 へ移るときに、プロパティの値を組み立てたり解析したりするコードを更新してください。

### ⚠️ 破壊的変更: 空の参照は `null` です
- **現在:** 読み取りは空の参照に `"None"` を返し、書き込みは `null`・`""`・`"None"` を受け付けます。
- **2.0.0:** 読み取りは `null` を返します。空にできる型への `""` または `"None"` の書き込みは、`InvalidParams` を返し、`null` を案内します。
- **移行:** 参照は、今から `ValueJson: null` で空にしてください。

### ⚠️ 破壊的変更: `WriteInputForm` を削除します
- **現在:** 汎用コマンドの書き込みの要件は `WriteInputForm`（`TextOrJson`・`JsonOnly`・`None`）を報告し、値をどのフィールドに渡すかを示します。
- **2.0.0:** 値は常に JSON なので、このキーを削除します。
- **移行:** このキーで分岐しないでください。

### ⚠️ 破壊的変更: 複数のプロパティは配列で書きます
- **現在:** 複数のプロパティを書く呼び出しの引数は、名前をキーにしたオブジェクトです。そのキー自身は、4 つのコマンドでは `Properties`、4 つでは `Params`、2 つでは `Parameters`、1 つでは `InitialProperties` で、応答には 8 通りの形があります。例えば、`SetWidgetProperties` と `SetSlotProperties` が該当します。
- **2.0.0:** 引数は `Properties` で、`{PropertyPath, Value, Operation?, ElementIndex?, ElementKey?}` の配列です。応答は、引数と同じ順序で `Properties` を並べます。
- **移行:** 2.0.0 へ移るときに、呼び出しを更新してください。

### ⚠️ 破壊的変更: 知らない名前があると、バッチ全体を拒否します
- **現在:** `SetSlotProperties` は知らない名前を何も言わずに飛ばし、Niagara の `SetRendererData` はログに出すだけで、`SetSettingsValues` は `SkippedKeys` に並べ、`SetMultipleWorldConditionProperties` は `SkippedEdits` に並べ、PCG は `Warnings` の下のテキストに入れます。
- **2.0.0:** 1 つでも要素を拒否したら、何も書きません。`Result.Refused` が、拒否したすべての要素を `{PropertyPath, ErrorCode, Reason}` で並べ、応答の `ErrorCode` は、引数の順序で最初に拒否した要素のものです。成功した書き込みは、各要素の `Changed`・`PreviousValue`・`NewValue` を並べます。
- **移行:** 存在しない名前を送らないでください。`SkippedKeys` と `SkippedEdits` を読むのもやめてください。

### ⚠️ 破壊的変更: Runtime のダンプの値は同じ形を持ち、切った値には印が付きます
- **現在:** Runtime のダンプには、それぞれの形があります。例えば、空の参照は `"None"` で、コンテナは最初の 32 要素の `{Value, TotalCount, Truncated}`、マップは `[key, value]` の一覧、文字列は印なしで 1024 文字で切られ、SaveGame のエクスポートと Chooser のセルのコマンド（`ListChooserTableRows`・`GetChooserTableRow`・`SetChooserTableCell`）は、小文字で始まるキーと `_structType` を持つ `FJsonObjectConverter` の形を使います。
- **2.0.0:** 値は、上の形の表に従います。一覧の読み取りは、深さ・個数・長さで値を切ることがあり、切った値は、何も言わずに切られる代わりに、切ったことを示す印を持ちます。
- **移行:** 2.0.0 へ移るときに、これらのダンプを読むコードを更新してください。

### ⚠️ 破壊的変更: `AssertActorProperty`・`AssertWorldState`・`WaitForCondition` は、プロパティのパスと型付きの値を取ります
- **現在:** これらのコマンドは `PropertyName` と `ExpectedValue` を取り、値をテキストとして比べます。
- **2.0.0:** プロパティは `PropertyPath`、値は型付きの JSON の値です。
- **移行:** 2.0.0 へ移るときに、呼び出しを更新してください。`PropertyName` の改名は、「コマンド名とパラメータのキー」に載せています。

### ⚠️ 破壊的変更: バインディングのキーとパスは共通になります
- **現在:** 各ファミリーは、バインディングを独自の書き方で表します。StateTree は `SourceNodeId` と `SourceProperty`、`TargetNodeId` と `TargetProperty`（1 階層）、UMG は `WidgetName` と `PropertyPath`、MVVM は `Source` と `Destination` のオブジェクト、Subsonic は `ParameterName` または `EventTag` と `Index` と `PropertyName`、Chooser は `InputValue` と `Binding`・`ContextIndex`・`PropertyBindingChain` を使います。どれもパスの解析を共有せず、インデックスも受け付けません。
- **2.0.0:** ソースとターゲットのプロパティは、プロパティのパスと同じ文法の `SourcePropertyPath` と `TargetPropertyPath` です。ターゲットのプロパティしか持たないファミリーは `PropertyPath` を使います。ソースやターゲットのほかのキーは、`Source` または `Target` の接頭辞を持ちます（`Destination` ではありません）。
- **移行:** 2.0.0 へ移るときに、呼び出しを更新してください。

### ⚠️ 破壊的変更: バインディングの追加と削除は、どのファミリーでも同じ意味になります
- **現在:** すでにバインディングを持つターゲットへの追加は、StateTree・UMG・Subsonic・Chooser では何も言わずに置き換え、MVVM では重複を受け付けます。存在しないバインディングの削除は、StateTree では `Removed: true`、UMG では `ExecutionFailed`、MVVM と Subsonic では `NotFound` を返します。
- **2.0.0:** ターゲットが 1 つのバインディングを持つファミリーでは、すでにバインディングを持つターゲットへの追加は、`AllowReplace: true` を渡さない限り `Conflict` を返し、既存のバインディングを `Result.ExistingBindings` に並べます。すでにあるバインディングの追加と、存在しないバインディングの削除は、`Changed: false` で成功します。`NotFound` を返すのは、バインディングを持つはずのノード・ウィジェット・ビューモデルが存在しないときだけです。バインディングを置き換えたり削除したりした書き込みは、それらを `Result.RemovedBindings` に並べます。
- **移行:** 意図して置き換えるところでは `AllowReplace: true` を渡してください。存在しないバインディングについての失敗で分岐しないでください。

### ⚠️ 破壊的変更: `FInstancedStruct` のセルは `{"StructType": …, "Value": …}` です
- **現在:** `FInstancedStruct` を持つ Chooser のセルは、`{"_structType": "<struct path>", <fields>...}` のオブジェクトです。
- **2.0.0:** 上の表の形、`{"StructType": "<struct path>", "Value": {…}}` です。
- **移行:** 移るときに、これらのセルを読み書きするコードを更新してください。`_structType` の形を受け付け続けるかどうかは、まだ決まっていません。決まったらこの項目に書きます。

## 待機・ジョブ・シナリオ

### ⚠️ 破壊的変更: `TimedOut`・`Aborted`・`NotExecuted` は `WorkAfterTimeout` に置き換わります
- **現在:** 期限で止まるコマンドは、それぞれの名前のキーでそう伝えます。`WaitForCondition` と `RunFunctionalTest` は `Data.TimedOut: true` を返し（1.3.0 で追加）、`RunEditorPythonScript` は中止したときに `Data.Aborted: true` を返し、キューでの待ちが尽きたコマンドは `NotExecuted: true` を返します。メッセージだけで伝えるコマンドもあります。例えば、`AcquireItems` です。
- **2.0.0:** 3 つのキーを削除します。期限は、`ErrorCode: Timeout` と `Result.WorkAfterTimeout` から読みます。値は、`NotStarted`（何も始めなかった）・`Stopped`（作業を止めた、またはコマンドが待っただけ）・`StillRunning`（エディタが続けている）のいずれかです。`StillRunning` で、あとから結果を確かめられるコマンドがあるときは、`Result.SuggestedCommands` がそれを示します。期限の前に観測した値は、`Result` に入ることがあります。`WaitForPendingInteraction` は非推奨で、1.x の応答のままです。`WorkAfterTimeout` は `UAIP.Core.WaitForJob`（2.0.0 で追加）が返します（「1 つのファミリーのジョブを問い合わせ・取り消し・待機するコマンドは非推奨です」を参照）。
- **移行:** `ErrorCode` で分岐してから、`WorkAfterTimeout` を読んでください。「ErrorCode と拒否」も参照してください。

### ⚠️ 破壊的変更: 応答の待ちが尽きたことは、どの経路でも同じ形で報告します
- **現在:** 形は経路によって違います。HTTP は `ErrorCode: ExecutionFailed` の 408 を返し、MCP は HTTP 200 の JSON-RPC エラー -32000（「rate limit exceeded」の番号）を返し、WebSocket は `{"event":"CommandTimeout","requestId": …}` を送って、あとから届く完了を捨てます。
- **2.0.0:** どの経路も、`Timeout` と `WorkAfterTimeout: StillRunning` を持つコマンドのエンベロープを返します。コマンドはエディタの中で動き続けます。
- **移行:** -32000 のエラーや `CommandTimeout` のイベントを扱っているなら、代わりにエンベロープを読んでください。`Timeout` の HTTP ステータスは、「ErrorCode と拒否」にあります。

### ジョブの ID は GUID です
- **現在:** LiveLink は録画の `RecordingId` を連番で返し、audit・PoseSearch・検証・インタラクションのジョブの ID はハイフンを持ちます。
- **2.0.0:** ジョブの ID は、ハイフンなしの 16 進 32 桁の GUID で、ほかの識別子と同じ形です（「識別子と参照」を参照）。1 つのファミリーの非推奨のコマンド（下を参照）は、1.x のパラメータでこの形の ID を受け付けます。
- **移行:** ジョブの ID は、中身を見ない文字列として扱ってください。

### ⚠️ 破壊的変更: ジョブの状態は 5 つの値のどれかです
- **現在:** 各ファミリーが独自の状態を持ちます。例えば、audit には `Preparing`、PoseSearch には `Succeeded`、検証には `Preparing`・`Enumerating`・`Normalizing`・`Validating`・`Finalizing`・`Aborted`、インタラクションには `AwaitingUser` と `Cause`、トレース解析には `Extracting`、HLOD は `BuildStatus` を報告し、再起動には `Scheduled`・`CloseRetrying`・`Declined`・`ExitStarted`、キャプチャには `Recording` と `Stopped` があり、LiveLink は `IsRecording` を報告します。
- **2.0.0:** `State` は `Pending`・`Running`・`Completed`・`Failed`・`Cancelled` で、最後の 3 つは終了の状態です。ファミリーごとの段階は `Phase` に載せ、`Failed` と `Cancelled` は `Reason` を持ちます。受領の応答と状態の応答は、常に `JobId`・`JobKind`（ファミリーの名前）・`State`・`StopRequired` を持ちます。1 つのファミリーの非推奨のコマンド（下を参照）は、1.x の状態のままです。
- **移行:** 2.0.0 へ移るときに、ジョブの状態を読むコードを更新してください。

### 1 つのファミリーのジョブを問い合わせ・取り消し・待機するコマンドは非推奨です
- **現在:** 各ファミリーが、ジョブの問い合わせと取り消しのコマンドを持ち、インタラクションは待機のコマンドも持ちます。`GetAssetAuditStatus`・`GetPoseSearchDatabaseIndexBuildStatus`・`GetValidationJobStatus`・`CancelValidationJob`・`GetPendingInteractionStatus`・`CancelPendingInteraction`・`WaitForPendingInteraction`・`GetTraceAnalysisStatus`・`GetHLODBuildStatus`・`CancelHLODBuild`・`GetRestartStatus`・`CancelLiveLinkRecording` です。すべてのファミリーのジョブを一覧にするコマンドはありません。これらのコマンドの一部は、ジョブの結果（PoseSearch・インタラクション・再起動）や進み具合（audit・検証・トレース解析）も返します。
- **2.0.0:** 2.0.0 で非推奨になります。名前は受け付け続けます。代わりに、`UAIP.Core.GetJobStatus`・`UAIP.Core.CancelJob`・`UAIP.Core.ListJobs`・`UAIP.Core.WaitForJob`（2.0.0 で追加）を使ってください。パラメータと応答は 1.x のままで、このページの共通のジョブのキーと状態は当てはまりません。ただし、ID のパラメータは、2.0.0 の開始のコマンドが返す `JobId` も受け付けます。非推奨になるのは、共通のコマンドと、PoseSearch・インタラクション・再起動ではファミリーの結果を返すコマンド（2.0.0 で追加。名前は決まり次第ここに書きます）がそろう版で、それまでは非推奨の印を付けません。`MigrationTarget` は `UAIP.Core.GetJobStatus`・`UAIP.Core.CancelJob`・`UAIP.Core.WaitForJob` のどれかで、状態のコマンドが結果を返していた 3 つのファミリーでは、`DeprecationWarning` が結果を返すコマンドも示します。`UAIP.Core.WaitForJob` は `JobId` と `TimeoutSeconds` を受け取り、ジョブが終わるまで待って、`UAIP.Core.GetJobStatus` と同じ応答を返します。待ちが尽きたときは `WorkAfterTimeout: StillRunning` を伴う `Timeout` を返し、ジョブは取り消しません。共通の状態の応答は、作業の件数を数えるファミリーでだけ `ProcessedCount` と `TotalCount` を持ちます。`GetLiveLinkRecordingStatus` は非推奨になりません。UAIP を通さずに始めた録画も報告するためです。
- **移行:** 1.x 向けに書いた呼び出しは動き続けます。2.0.0 へ移るときに、ジョブの問い合わせ・取り消し・待機は共通のコマンドで行い、結果はファミリーのコマンドで読んでください。

### ⚠️ 破壊的変更: 別のジョブを置き換えたジョブは `ReplacedJobId` を報告します
- **現在:** `StartValidationJob` は、ジョブを置き換えたときに `ReplacedPreviousJob: true` を返し、置き換えられたジョブは `Aborted` で終わります。
- **2.0.0:** 受領の応答が `ReplacedJobId` を持ち、置き換えられたジョブは `Reason: Replaced` を伴う `Cancelled` になります。
- **移行:** 2.0.0 へ移るときに `ReplacedJobId` を読んでください。

### ⚠️ 破壊的変更: 終わったジョブの取り消しと停止は成功します
- **現在:** 例えば、終わったジョブに対して、`CancelHLODBuild` は `ExecutionFailed` を返し、LiveLink の録画のコマンドは `NotAllowed` を返します。
- **2.0.0:** `UAIP.Core.CancelJob`（2.0.0 で追加）とファミリーの停止のコマンドは成功し、実際の `State` を返します。受け付けた取り消しで、作業がまだ止まっていないときは、成功して `Running` を返します。`CancelHLODBuild` と `CancelLiveLinkRecording` は非推奨で、1.x の振る舞いのままです（前の項目を参照）。
- **移行:** これらの失敗で分岐しないでください。

### ⚠️ 破壊的変更: シナリオのステップの参照は、ステップの結果のキーに従います
- **現在:** ステップは、`${StepName.Data.<pointer>}` または `${StepName.Data}` で参照します。
- **2.0.0:** 参照は `${<StepName>.<path>}` で、パスはステップの結果のキー（例: `Success`・`ErrorCode`・`Result.<…>`）に従います。`${Variables.<key>}` は残ります。解決できない参照は、`InvalidParams` でステップを失敗させ、再試行しません。
- **移行:** `${StepName.Data…}` を受け付け続けるかどうかは、まだ決まっていません。決まったらこの項目に書きます。

### ⚠️ 破壊的変更: シナリオは単独のコマンドと同じエンベロープを返します
- **現在:** 応答は `Status`（`Completed`・`Failed`・`TimedOut`）と `AllStepsSucceeded` を持ち、シナリオ全体の失敗は、`__error__` または `__session_ended__` という名前のステップとして現れます。
- **2.0.0:** 応答は、最上位の `Success`・`ErrorCode` と、試した順序の `Result.StepResults` を持ちます。`Status` と `AllStepsSucceeded` は削除し、`__error__` と `__session_ended__` のステップも削除します。`Success` は、すべてのステップが成功したときだけ true です。`Result.TotalStepCount` は要求したステップの数を、`Result.StoppedAtStep` は止まったステップを示します。`ErrorCode` は、`Reason: StepFailed` を伴う `ExecutionFailed`、`Reason: StepTimeout` または `ScenarioTimeout` を伴う `Timeout`、不正な要求への `InvalidParams`、別の実行が枠を持っているときの `TooManyRequests`、入口が有効でないときの `PolicyViolation`、`Reason: SessionEnded` を伴う `NotAllowed` です。各ステップの結果も、`AttemptCount`・`ElapsedSeconds`・`Result` を持ちます。
- **移行:** 2.0.0 へ移るときに、`Status` と `AllStepsSucceeded` の代わりに `Success` と `ErrorCode` を読んでください。

### ⚠️ 破壊的変更: シナリオは成果物を `ArtifactIds` ではなく `Artifacts` で返します
- **現在:** 各ステップの結果と最上位は、成果物の ID の文字列の配列 `ArtifactIds` を持ちます。
- **2.0.0:** 単独のコマンドの `Artifacts` と同じ要素（`ArtifactId`・`FilePath`・`Type`・`SizeBytes`）の `Artifacts` を持ち、`ArtifactIds` は削除します。両方を返す期間は設けません。ステップの参照 `${<StepName>.Artifacts[<n>]}` の形は変わりません。
- **移行:** 2.0.0 へ移るときに、`Artifacts` の要素の `ArtifactId` を読んでください。

### 拒否されたシナリオは、どの入口でも同じ形で報告します
- **現在:** 不正な要求は、MCP では `ErrorCode` の無い JSON-RPC エラー -32602 を返し、受け付けのときに拒否された要求は、HTTP では HTTP 200 を返します。セッション ID の読み方も、入口によって違います。
- **2.0.0:** すべての入口（HTTP・MCP・WebSocket・コマンドライン）が、同じ要求を受け取り、前の項目のエンベロープを返し、不正な要求には `InvalidParams` を返します。HTTP のステータスなどの詳細の決め方は、決まり次第ここに足します。
- **移行:** `ErrorCode` は、トランスポートの形ではなく、エンベロープから読んでください。

## Capability と ini の設定

### ⚠️ 破壊的変更: `ToolsetEditDuringPlaySession` を削除し、`[UAIP.SafetyPolicy]` の 1 つの設定が代わりになります
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** Capability `ToolsetEditDuringPlaySession` は、Play または Simulate のセッション中に、`Toolset.*` コマンドがエディタを変更することを許します。無ければ拒否されます。
- **2.0.0:** `[UAIP.SafetyPolicy]` に設定を加えます。それを有効にすると、`UAIP.*` コマンドと公式の Toolset のツールの両方が、Play または Simulate のセッション中にエディタを変更できます。セッション中に壊れるコマンドは、拒否のままです。設定の追加と `ToolsetEditDuringPlaySession` の削除は 2.0.0 で行い、両方が存在する期間はありません。キーと行の形式は、まだ決まっていません。
- **移行:** 設定が `ToolsetEditDuringPlaySession` を付与しているなら、2.0.0 へ移るときに新しい設定へ置き換えてください。そうしないと、Play セッション中の変更は拒否されます。

### Capability の名前は 1 つの型に従います
- **現在:** 名前は 1 つの型に従っていません。`Runtime` と書かない Runtime の Capability があり、名詞だけの名前があり、言い回しや単数・複数もまちまちです。
- **2.0.0:** 名前は `<Domain><Object><Verb>` に従い、Runtime ドメインの Capability は `Runtime` と書きます。改名した Capability は、起動時の警告つきで、旧い名前でも受け付けます。応答・拒否・一覧には、新しい名前だけが出ます。どの Capability を改名するかは 1 つずつ決め、2.0.0 の changelog に一覧にします。
- **移行:** ini ファイルを動かし続けるために必要なことはありません。2.0.0 の一覧を読む前に、応答から読んだ名前を、コードに書いた名前と比べないでください。

### 一部の制限は、フラグと Capability の間で移ります
- **現在:** 制限には、`[UAIP.SafetyPolicy]` のフラグで開くものと、Capability で開くものがあります。
- **2.0.0:** 誰が呼ぶかによる制限は `DefaultDenied` の Capability になり、環境のモードによる制限は、それを開くフラグのままです。どの制限がどう移るかは、決まり次第ここに足します。一覧は 2.0.0 の changelog にあります。
- **移行:** 2.0.0 の前にすることはありません。

### ⚠️ 破壊的変更: `QueryCapabilities` は `NotInThisEdition` を `UnavailableDetail` で報告します
- **現在:** `IncludeUnavailable: true` のとき、エディションが提供しない Capability の `RegisteredCapabilities` の要素は、`UnavailableReason: "NotInThisEdition"` を持ちます。
- **2.0.0:** 代わりに `UnavailableDetail: "NotInThisEdition"` を持ち、両方を返す期間は設けません。
- **移行:** 2.0.0 へ移るときに `UnavailableDetail` を読んでください。

## アーティファクト

### ⚠️ 破壊的変更: `SessionId` の無い `GET /uaip/artifacts/:id` は拒否されます
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** `SessionId` の無い要求にも、`Deprecation` ヘッダーを付けて応答します。
- **2.0.0:** `SessionId` の無い要求は、404 ではなく、HTTP 400 と `ErrorCode: InvalidParams` で拒否されます。
- **移行:** 成果物を作るコマンドと取得の両方に `SessionId` を渡してください。MCP Bridge は、セッションを持っているときは常に送ります。2.0.0 の動作を試すには、エディタを `-uaip-require-artifact-session-id` で起動します。

### ⚠️ 破壊的変更: `OpenAsset` と `NormalizeEditorLayout` の成果物の `ActiveTabId` は、レイアウトの識別子です
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** `ActiveTabId` はアセットパスを持ち、その隣に `ActiveAssetPath` と `DeprecatedFields` があります。
- **2.0.0:** `ActiveTabId` は、`DumpEditorState` と同じく、フォーカスのあるタブの Slate のレイアウト識別子を持ち、`DeprecatedFields` は空です。`ActiveAssetPath` は残ります。
- **移行:** `ActiveTabId` の代わりに `ActiveAssetPath` を読んでください。2.0.0 の動作を試すには、エディタを `-uaip-active-tab-id-as-layout-id` で起動します。

### 2 つの試用のスイッチは削除します
- [1.3.0 で告知](changelog.md#uaip-plugin-130--2026-11-26)
- **現在:** `-uaip-require-artifact-session-id` と `-uaip-active-tab-id-as-layout-id` は、値を取らず ini の設定も持たないコマンドラインのスイッチです。1.x のリリースだけに用意しています。
- **2.0.0:** どちらも削除します。上の 2 つの項目の動作が、唯一の動作になります。
- **移行:** 2.0.0 へ移るときに、起動のコマンドラインから外してください。

### ⚠️ 破壊的変更: 成果物の `Type` は `Image`・`Json`・`Text`・`Binary` です
- **現在:** `Type` は `Image`・`Json`・`Log`・`Report`・`Bundle`・`Trace` で、成果物のフォルダは、用途にちなんで `Dumps`・`Screenshots`・`Logs`・`Reports`・`Traces` などと名付けられています。
- **2.0.0:** `Type` は中身の読み方を表し、フォルダは `Type` と同じ名前です。ログは `Text`、レポートとバンドルのマニフェストは `Json`、トレースは `Binary`、CSV は Content-Type `text/csv` の `Text` です。取得の Content-Type は拡張子から決めます。例えば、`ExportDataTableToCSV`・`ImportDataTableFromCSV`・`RunAutomationTest`・`RunGauntletTest`・`AnalyzeTrace` が該当します。
- **移行:** `Log`・`Report`・`Bundle`・`Trace` で分岐しないでください。拡張子か中身を読んでください。

### 成果物のファイル名は `<CommandName>-<ArtifactId>.<extension>` です
- **現在:** 名前の作り方は 1 つではなく、成果物によっては、コマンドの名前が登録された名前ではありません。
- **2.0.0:** 名前は、保存を求めたコマンドの登録された名前・`ArtifactId`・拡張子です。`FilePath` は、これまでどおり、成果物にアクセスするためのパスではありません。
- **移行:** 成果物は、ファイル名ではなく `ArtifactId` で取得してください。

### ⚠️ 破壊的変更: バンドルのマニフェストは `Json` で、メンバーは `Role` を持ちます
- **現在:** バンドルを返すコマンドは、`Json` の型を持たないマニフェストを返します。例: `CheckpointCapture`・`LoadMap`・`StartPIE`、DataTable・Enhanced Input・Execution のコマンド。
- **2.0.0:** マニフェストは、`Type: Json` を持つ `Artifacts[]` の最後の要素です。バンドルに属する各成果物は、`Artifacts[]` の要素に `Role` を持ちます。`Pre`・`Post`・`Report`・`Log`・`Audit`・`Result`・`Snapshot`・`Payload`、マニフェスト自身は `Manifest` です（`Role` は 2.0.0 で追加）。
- **移行:** マニフェストが返るようになったら、`Role: Manifest` で見つけてください。

### ⚠️ 破壊的変更: HTTP の成果物の一覧は PascalCase のキーを使います
- **現在:** `GET /uaip/sessions/{sessionId}/artifacts` が返す一覧は、`artifacts`・`artifactId`・`type`・`commandName`・`sessionId`・`description` を使い、`GetArtifact` はサイズを `TotalBytes` で返します。一覧にはサイズも作成時刻もありません。
- **2.0.0:** キーは `Artifacts`・`ArtifactId`・`Type`・`CommandName`・`SessionId`・`Description` で、サイズはすべての経路で `SizeBytes` です。作成時刻 `CreatedAt` が加わります。
- **移行:** 2.0.0 へ移るときに、一覧を読むコードを更新してください。

### パスで成果物を指すキーは `ArtifactId` になります
- **現在:** キーには 6 通りの書き方があります。例: `ArtifactPath`（`ExportDataTableToCSV`）・`PreDeleteArtifactPath`・`PreImportSnapshotPath`・`CaptureArtifactPath`・`WorldStateArtifactPath`。
- **2.0.0:** 成果物は、パスやファイル名ではなく、`ArtifactId`（1 つの応答が複数を持つときは `<What>ArtifactId`）で指します。以前の成果物を取るコマンドは、その `ArtifactId` を取ります。
- **移行:** 2.0.0 へ移るときに、新しいキーを読んでください。

### ⚠️ 破壊的変更: 成果物の本体から `SchemaVersion` を削除します
- **現在:** 多くの成果物の本体は、`SchemaVersion` を 1・2・3、文字列 `"1.0"`、数値 `1.0` のいずれかで持ちます。例: `GetAvailableRigVMUnitStructs`。
- **2.0.0:** このキーを削除します。
- **移行:** `SchemaVersion` の値で分岐しないでください。

### ⚠️ 破壊的変更: 切った本体は、共通の方法でそれを示します
- **現在:** 印はまちまちです。Validation は本体に `Reason: "ArtifactBytes"` の `Truncation` を置き（8 MiB で切る）、Mass は `ArtifactTruncated` と `ArtifactTruncationIndex` を書き（1 MiB で切る）、DataRegistry は `Truncated` と `TotalCount` を書き、`DeleteAsset` は `ReferencersTruncated` を書きます。
- **2.0.0:** 本体と `Result` の両方が、`Reason: ByteLimit` を伴う共通の切り詰めの印を持ちます。成果物に固有の印はありません。
- **移行:** 2.0.0 へ移るときに、これらの印を読むコードを更新してください。

### 本体の時刻は UTC の ISO 8601 です
- **現在:** 本体の時刻は `%Y%m%d_%H%M%S` で書かれ（例えば、`RestartEditor`・`SaveAllPackages`・`ShutdownEditor`・`ExecuteConsoleCommand` の監査ログ）、Runtime の成果物はミリ秒を持ちません。
- **2.0.0:** 時刻は、ミリ秒と末尾の `Z` を持つ、UTC の ISO 8601 の文字列です。
- **移行:** 移るときに、これらの時刻を解析するコードを更新してください。

## 使えないコマンドの見え方

### ⚠️ 破壊的変更: プラグインとバージョンの両方が足りないときは、バージョンを先に報告します
- **現在:** コマンドに必要なプラグインとエンジンのバージョンの両方が足りないとき、`UnavailableDetail` は `OptionalPluginDisabled` です。例えば、Niagara と Sequencer Animation Mixer のコマンドが該当します。
- **2.0.0:** `EngineVersion` です。`ErrorCode` は `AbilityUnavailable` のままです。
- **移行:** `AbilityUnavailable` で分岐し、理由は `UnavailableDetail` を読んでください。

### コマンドのスキーマは、エンジンのバージョンやプラグインで変わりません
- **現在:** コマンドによっては、エンジンのバージョンやあるプラグインの有無によって、パラメータや列挙値の違うスキーマを宣言します。例: `SetPhysicsSolverSettings` と `SetViewModelSource`。
- **2.0.0:** スキーマはどこでも同じです。環境で使えないパラメータや値は、説明に書き、使ったときに `AbilityUnavailable` と `Result.Reason` で拒否し、拒否の文はパラメータと値を示します。
- **移行:** 動く条件は、`DescribeCommand` のパラメータの説明を読んでください。

### ⚠️ 破壊的変更: `UnavailableDetailMessage` は `Remedy` になります
- **現在:** `DescribeCommand` は、案内の文を `UnavailableDetailMessage` で返します。
- **2.0.0:** キーは `Remedy` で、両方を返す期間は設けません。主な理由が `HandlerUnavailable` のときだけ返り、`ListCommands` の行は持ちません。
- **移行:** 2.0.0 へ移るときに `Remedy` を読んでください。

### ⚠️ 破壊的変更: `UnavailableDetail` は `HandlerUnavailable` のときだけ返り、`Unspecified` はなくなります
- **現在:** `ListCommands` の行と `DescribeCommand` は、使えないすべてのコマンドに `UnavailableDetail` を持ち、`Unspecified` を含む 8 つの値のどれかを取ります。
- **2.0.0:** 理由に `HandlerUnavailable` を含まない行や説明は `UnavailableDetail` を持たず、値 `Unspecified` も返さなくなるので、値は 7 つです。
- **移行:** `UnavailableDetail` が無いことを、「理由が `HandlerUnavailable` ではない」として扱ってください。

## 環境情報の伏せ方

### 応答のファイルパスを置き換える印は、1 つにそろいます
- **現在:** 印は応答によって違います。例えば、クラッシュレポート・Python のトレースバック・Widget Blueprint のコンパイルは、それぞれ独自の印を使います。
- **2.0.0:** すべての応答で、1 組の印がファイルパスを置き換えます。その組は、2.0.0 とともに一覧にします。
- **移行:** 印の文字列に一致させないでください。

## MCP Bridge と Claude Code プラグイン

### ⚠️ 破壊的変更: ブリッジ自身が作る 6 つの応答から `Data` を削除します
- [MCP Bridge 1.3.0 で告知](changelog.md#mcp-bridge-130--2026-11-26-リリース済み)
- **現在:** ブリッジ自身が返す 6 つの応答は `Result` を持ち、同じ値を `Data` にも残しています。`ShutdownEditor` の no-op、セッション無しの `RestartEditor` の起動と接続、シャットダウンを転送する 2 つの応答、応答の無いエディタを復旧する 2 つの応答で、すべて `uaip_execute` を通ります。
- **2.0.0:** `Data` を削除します。UAIP 2.0.0 と同時にリリースする、ブリッジの次のメジャーバージョンで行います。
- **移行:** `Result` を読んでください。

### ⚠️ 破壊的変更: `_inlined_artifacts` のキーは PascalCase です
- **現在:** 各要素は `artifact_id`・`content_type`・`data_base64` を持ちます。
- **2.0.0:** キーは PascalCase です（例えば、`artifact_id` は `ArtifactId` になります）。ブリッジは UAIP 2.0.0 と同時にリリースします（上の項目を参照）。
- **移行:** 2.0.0 へ移るときに、インライン化された成果物を読むコードを更新してください。

### ブリッジ経由で断られた `RestartEditor` は、案内を `ErrorMessage` で返します
- **現在:** `uaip_execute` を通る `RestartEditor` をエディタが断ると、ブリッジはエディタの理由で応答し、`Remedy` を結果にコピーします。
- **2.0.0:** ブリッジは `Remedy` をコピーしません。案内は `ErrorMessage` にあります。
- **移行:** `ErrorMessage` を読んでください。

### `Timeout` を HTTP 408 で読むスクリプトは、変更が要ります
- **現在:** `Timeout` の HTTP ステータスは 408 です。
- **2.0.0:** 504 です（「ErrorCode と拒否」を参照）。
- **移行:** 自分のスクリプトが `Timeout` を HTTP ステータスで判定しているなら、代わりに `ErrorCode` で判定してください。

## 1.3.0 の告知からの変更

1.3.0 の changelog には、このページが今は違う形で述べている告知があります。各項目は、1.3.0 の changelog が何と言っていたかと、今は何が正しいかを書きます。changelog の項目には、ここを指す注記が付いています。1.3.0 の告知は [UAIP Plugin 1.3.0](changelog.md#uaip-plugin-130--2026-11-26) にあります。

### コマンドを使えない理由を示すキーは、今のままではありません
- **1.3.0 の記述:** `UnavailableReason`・`UnavailableDetail`・`AdditionalUnavailableReasons` は、`SecretValuesWithheldReason` とともに残ります。
- **現在:** 名前は残りますが、載せるものが 2.0.0 で変わります。理由に `HandlerUnavailable` を含まない行や説明は `UnavailableDetail` を持たず、`Unspecified` は返さなくなります。`UnavailableDetailMessage` は、主な理由 `HandlerUnavailable` だけが持つ `Remedy` になります。エディションが提供しない Capability の `QueryCapabilities` の要素は、`UnavailableReason` の代わりに `UnavailableDetail: "NotInThisEdition"` を持ちます。`DumpStateTreeInstanceData` や CommonUI の `GetInputState` のように、可用性とは別のことに `UnavailableReason` を使う応答は、それを `Reason` に載せます。「使えないコマンドの見え方」「Capability と ini の設定」「1.3.0 で追加したコマンド」を参照してください。

### 1.x のリリースで早く入るかもしれないと 1.3.0 が書いたことは、2.0.0 で入ります
- **1.3.0 の記述:** `Reason` や新しい秘密のマスクのキーをまだ持たない応答は、遅くとも 2.0.0 でそれらを持つようになり、`Result.IntegrityState`・`Result.RequiresFollowupCompile`・`Result.SavedPackages`・`Result.WrittenFiles` は、すでに 1.x のリリースに現れるかもしれません。
- **現在:** これらはすべて、2.0.0 で初めて現れます。1.x の MINOR リリースは予定しておらず、パッチリリースは公開 API を変えません。

### Play セッション中の変更の設定と、Capability の削除は、同じ版で行います
- **1.3.0 の記述:** のちのリリースが、Play セッション中の変更のための `[UAIP.SafetyPolicy]` の設定を加え、`ToolsetEditDuringPlaySession` は 2.0.0 で削除します。
- **現在:** 設定は 2.0.0 で追加され、`ToolsetEditDuringPlaySession` も同じ版で削除します。両方が存在する期間はありません。「Capability と ini の設定」を参照してください。

### 1.3.0 で直したのは、安全の規則と応答の契約に反していたものだけです
- **1.3.0 の記述:** 秘密の値・パスワード欄・保存できなかった成果物の報告の誤りは、そのリリースで直しました。
- **現在:** 直したのは、安全の規則と応答の契約に反していたものだけです。ほかの違いは、既存のコマンドの違いと一緒に 2.0.0 で直します。「1.3.0 で追加したコマンド」と「秘密の値」を参照してください。

## 更新履歴

- 2026-11-27: このページを作成しました。
- 2026-11-27: changelog の [バージョニング方針](changelog.md#バージョニング方針) にある ⚠️ の印の基準を変えました。1.3.0 の次のリリース以降は、1.3.0 で成功していた呼び出しが基準です。
- 2026-11-27: changelog の [Deprecation 方針](changelog.md#deprecation-方針基本削除しない)を書き直しました。例外が 2 つになりました。Epic 社がエンジン API を削除したときのコマンドの削除と、前もって告知した `Experimental` のコマンドの削除です。
- 2026-11-27: `DragGraphNode`・`ConnectGraphPins` と、1 つのファミリーのジョブのコマンドが 2.0.0 でどう残るかを決めました。1.x の形のままで、置き換えのコマンドがそろったときに非推奨になります。`UAIP.Core.WaitForJob` と、シナリオの `ArtifactIds` から `Artifacts` への変更を足しました。

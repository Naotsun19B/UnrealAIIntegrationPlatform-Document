**[English](../en/commands.md)** | [概要に戻る](overview.md)

# コマンドリファレンス

UAIP は 1320 個の **UAIP コマンド**（プラグイン本体が直接提供する独自実装）と、それを補強する 421 個の **Toolset ブリッジコマンド**（UE 5.8 公式 Toolset への委譲レイヤー）の合計 1741 をドメイン別に提供しています。この数は、UE 5.8 の Win64 エディタで本プラグインが定義するすべてのコマンドの数で、必要なプラグインが無効なため `Available: false` として一覧に出るコマンドも含みます。コマンド名はすべて完全修飾名（例：`UAIP.Editor.Observation.CaptureActiveWindowImage`）です。本ページの表ではプロバイダプレフィックスを省略しているため、セクションヘッダーのプレフィックスを付けて使用してください。

## このリファレンスの使い方

- 各コマンドの完全なパラメータスキーマは `{"Command": "UAIP.Core.DescribeCommand", "Params": {"Name": "<コマンド名>"}}`（HTTP / WebSocket / CLI）または `uaip_describe_command(CommandName="<コマンド名>")`（MCP）（引数名は前者が `Name`、後者が `CommandName` で異なります） で取得できます
- 実行時にドメインでフィルタするには `uaip_list_commands(ProviderPrefix="UAIP.Editor")` を使用します
- 各コマンドに必要な Capability については [Safety & Capabilities](safety.md) を参照してください
- 次のコマンドはディスク上のファイルを削除・移動・リネームするため、安全ポリシーで `DisableSave` が有効なときは、他の何よりも先に（PIE 中かどうかの判定よりも先に）`PolicyViolation` で拒否します（"Disk write operations are disabled by the current safety policy."）: `DeleteAsset`・`DeleteFolder`・`ForceDeleteFolder`・`RenameAsset`・`MoveAsset`・`MoveFolder`・`FixAssetRedirectors`・`FixUpRedirectorsInFolder`・`DeleteInputAction`・`DeleteMappingContext`・`DeleteDataLayerAsset`・`DeleteHLODs`・`DeleteGameFeaturePlugin`。以前から `DisableSave` で拒否していたコマンドは変わりません。詳細は [Safety & Capabilities](safety.md#disablesave-と削除移動リネームのコマンド) を参照してください

## 凡例

| 記号 | 意味 |
|---|---|
| 🆓 | デモバイナリで利用可能（製品版でも利用可能） |
| (記号なし) | 製品版限定コマンド |
| 🧩 | オプションプラグインが必要（プラグインが無効の場合は登録されません）。エディタビルドでは、そのプラグインがエンジンに存在していて単に無効なだけなら、有効化してエディタを再起動すれば十分です — `.uproject` の編集もリビルドも不要です。このエンジン版にそのプラグインがそもそも存在しない場合はどの設定を変えても解決しません — [UnavailableDetail](#unavailabledetail--handlerunavailable-の8つの詳細理由) の `UnavailableDetail: OptionalPluginDisabled` を参照してください。いずれの場合も `UAIP.Core.ListIntegrations` で正確な状態が分かります |
| ⚠️ | Experimental — 挙動や契約が変わる可能性がある、または既知の制約により記載どおりに動作しない |

## UAIP コマンドと Toolset ブリッジコマンド

UAIP では 2 種類のコマンドを公開しています：

- **UAIP コマンド**（`UAIP.*` プレフィックス）：プラグイン本体が直接提供する独自実装のコマンド。UE のバージョンや Toolset プラグインの有無に依存せず動作します。
- **Toolset ブリッジコマンド**（`Toolset.*` プレフィックス・UE 5.8+ かつ Toolset 系プラグイン導入時のみ）：UE 5.8 公式 Toolset フレームワークへの委譲レイヤー。多くは対応する UAIP コマンドのミラーで、Toolset 経由でしか提供されない機能を統一的に呼び出せるようにします。

本ページのドメインサマリでは件数のみを並べています。Toolset ブリッジコマンドの全名前を実行時に列挙したい場合は `uaip_list_commands(ProviderPrefix="Toolset")` を使ってください。

Toolset ブリッジコマンドが、経由する Toolset 連携の準備ができていないために実行できないとき、エラー文はまずその連携とその状態を示し、続けて状態に応じた対処を述べます。たとえば Toolset 連携を含まない無償のデモ版では、`This command runs through the Toolset integration 'UAIPCoreToolsetRegistry', which is not loaded (state: NotInThisEdition). The integration is not included in the free demo edition of UAIP. Its commands are available in the Pro edition on Fab.` となります。連携がまだ読み込み中（状態が `Pending` または `Loading`）のときは、最初の文が `is not loaded` ではなく `has not finished loading yet` になります。同じ状態は `UAIP.Core.ListIntegrations` でも確認できます。

### Toolset ブリッジコマンドへの引数宣言・厳格検証の導入が進行中

これまで、Toolset ブリッジコマンドの大半は**引数を一切宣言していませんでした**。`uaip_describe_command` を呼んでも空の `Properties` が返り、実際にどんな引数を受け付けるかは分かりませんでした。送った JSON はそのまま検証なしで Toolset 側の呼び出しへ渡され、誤った引数を送ってもたいていエンジン側で汎用的な `ExecutionFailed` として失敗するだけで、どのキーが問題だったかは分かりませんでした。

これをコマンド単位で、宣言済み・厳格検証（`AdditionalProperties: false`、実際の `Required` フラグ、実際の型）へ移行する作業が進行中です。**本更新時点で 161 件の Toolset ブリッジコマンドが移行を完了しています**——`Toolset.Editor.Niagara.*` / `Toolset.Editor.PCG.*` / `Toolset.Editor.Sequencer.*`（`SequencerAnimMixer` / `AnimationAssistant` の姉妹プロバイダを含む）/ `Toolset.Editor.Physics.*` / `Toolset.Editor.UMG.*` / `Toolset.MVVM.*` に集中しており、それ以外にも個別のコマンドがいくつか含まれます。移行は継続中で、あるコマンドが移行済みかどうかはそのコマンド自身のスキーマから直接分かります——`Properties` が非空で `AdditionalProperties: false` なら厳格検証済み、`Properties` が空で `AdditionalProperties: true` ならまだ未移行で引数は従来どおり素通りします。このリファレンスの記載を当てにせず、常に `uaip_describe_command` で最新のスキーマを確認してください。

**これは「たまたま動いていた」呼び出しにとっての破壊的変更です**。余計なキーや綴り間違いのキーを送っても従来は黙って受理される（無視される、またはエンジン内部まで転送されて拒否される）だけでしたが、移行済みのコマンドでは、その場で問題のキー名を名指しした `InvalidParams` として拒否されるようになります。

`Toolset.Editor.Niagara.*` の 5 コマンド（`DuplicateEmitter` / `GetScriptAssets` / `MoveModule` / `SetEmitterEnabled` / `SetEmitterName`）は、本更新時点でもまだ引数を宣言していませんが、**これはもう未確定ではありません**。5 件とも、このプラグインが対応するどの Niagara toolset にも一致する関数が無いため、スキーマへ移行する代わりに、5 件すべてが `Available: false`（`UnavailableReason: "HandlerUnavailable"` / `UnavailableDetail: "DelegationTargetMissing"`）を返すようになりました——スキーマが説明すべき対象がそもそも無いということです。それぞれが何を理由に拒否するか、どれに動くネイティブ代替があるかは [UAIP.Editor.Niagara → Toolset ブリッジ](#uaipeditorniagara-) の注記を参照してください。「委譲先の toolset に一致する関数が無い」という同じ形は `Toolset.Editor.GameFeatures.ListGameFeatures` と `Toolset.Editor.Niagara.GetNiagaraParameterCollections` にも当てはまりますが、この 2 件はもともと正しい空のスキーマを宣言済みだったため、上記の 5 件には数えられていません——[UAIP.Editor.GameFeatures → Toolset ブリッジ](#uaipeditorgamefeatures-) を参照してください。**本更新で、この状態にあるコマンドの全件が分かりました。** ブリッジコマンド 421 件のうち、共通のブリッジハンドラで作られた 419 件について、委譲先の (toolset 名, tool 名) の組がエンジン側に実在するかを静的に突き合わせた結果、**404 件が到達し、15 件が到達しません**。残る 2 件（`CompileLiveCoding` と `DrawPCGSpline`）はこのハンドラで作られておらず、この突き合わせの対象外です。15 件はすべて `Available: false` と `UnavailableDetail: "DelegationTargetMissing"` を返します（内訳: Niagara 7 件 / GameFeatures 4 件 / SlateInspector 2 件 / UMG 2 件）。あわせて、**委譲先の綴りが誤っていた 16 件が実際に到達するようになりました**（Dataflow 7 件 / SlateInspector 8 件 / Niagara 1 件）——それまでは、このリファレンスが動作すると書いていながら実行時に失敗していました。個別のコマンドの現在の状態は、引き続き `uaip_describe_command` で確認できます。

---

## UnavailableDetail — HandlerUnavailable の8つの詳細理由

このページの多くの注記が、`UnavailableReason: "HandlerUnavailable"` と並んで `UnavailableDetail` を挙げています。`HandlerUnavailable` 単体では、そのコマンドの `IsAvailable()` が `false` を返したという事実しか分かりません — なぜ拒否されたかは分かりません。`UnavailableDetail` はその理由を 8 つの値のいずれかへ絞り込みます。

`UnavailableDetail` は、現在利用可能かどうかにかかわらず、どのコマンドについても `uaip_describe_command` から確認できます。`uaip_list_commands` の `HiddenReasons` オブジェクトには**含まれません** — こちらは常に固定 5 種の `UnavailableReason` キー（`DeniedCommand` / `MissingCapability` / `RoleRestricted` / `ReadOnlyPolicy` / `HandlerUnavailable`）のままです。特定の `HandlerUnavailable` エントリの詳細を見るには、そのコマンド名を指定して `uaip_describe_command` を呼ぶか、`uaip_list_commands` に `IncludeUnavailable: true` を付けて呼んでください — 隠れている各行にも同じ per-command の `UnavailableDetail` 文字列が付くようになりました（`UnavailableDetailMessage` は付きません。一覧レスポンスのサイズを抑えるため、こちらは引き続き `describe_command` だけが持つフィールドです）。以下のうち `Unspecified` 以外の 7 値をハンドラーが返す場合、通常はあわせて `UnavailableDetailMessage` 文字列も返ります — ハンドラー自身による自由記述の補足説明で、独自に言い換えず、そのまま利用者へ伝えてください。

| `UnavailableDetail` | 意味 | 解消する方法 |
|---|---|---|
| `Unspecified` | `HandlerUnavailable` 以上の詳細なし — この項目が追加される前から存在するハンドラーの既定値であり、`Available` が再び `true` になったときにも全ハンドラーがこの値を返す | — |
| `EngineVersion` | 現在動作しているものとは異なるエンジンバージョンを必要とする（特定のリリースで導入された、または特定のリリースまでしか存在しない API など） | エンジンバージョンを上げる、または下げる |
| `BuildConfiguration` | このプロセスがビルドされていないビルド構成を必要とする（Developer Tools・Editor ターゲットなど） | 必要な構成でリビルドする |
| `ExecutionEnvironment` | この実行環境が提供していないインフラを必要とする（レンダーハードウェアインターフェース、対話セッション、オプションの Runtime プラグインが登録するモジュラー機能クライアントなど） | 別の実行環境で動かす |
| `OptionalPluginDisabled` | 依存先のオプションプラグインへの対応が、このバイナリには一切コンパイルされていない — この UAIP バイナリがビルドされた時点のエンジンに、そのプラグインが存在しなかったことを意味する | **「プラグインを有効化して再起動する」はここでは何も解決しません。** エディタビルドでは、そのプラグインを含むエンジン版向けの UAIP ビルドが対処です（ソースビルドの場合は、そのエンジンにプラグインを追加してリビルドする）。パッケージ化ゲームでは、`.uproject` でプラグインを有効化し、再度パッケージ化します。プラグインが単に無効なだけで存在はしている場合、この値にはなりません — その場合は代わりに（対処付きの）`CommandNotFound`、または Toolset ブリッジなら `ExecutionEnvironment` として現れます。[`UAIP.Core.ListIntegrations`](#uaipcore) を参照 |
| `EngineApiNotExported` | サポート対象のどのエンジンバージョンでもプラグインへエクスポートされないエンジン側 API に依存している | エンジンバージョンの変更やプラグインの切り替えでは解決しない — 別の経路（例: エディタスクリプティング経由で同じ効果に到達する Toolset ブリッジコマンド）を探す |
| `DelegationTargetMissing` | 委譲先の外部サーフェス（Toolset ブリッジのターゲット）に、サポート対象のどのエンジンバージョンも実際には宣言していない関数を呼び出しており、実装へ到達する手段がそもそも存在しない | これも解決しない — そのサーフェスを持つプラグイン自体はすでに有効になっている場合がある。同じ操作を行うネイティブコマンドがあれば、それを使う |
| `SafetyPolicyDisabled` | 環境にもビルドにも欠けているものは無い — 既定で無効な SafetyPolicy フラグでゲートされており、そのフラグがこのプロセスでオフになっている | `Config/DefaultUAIP.ini` でそのフラグを設定して再起動する（`ErrorMessage` がフラグ名を名指しする）。`AllowCapabilityReload=True` の環境なら `UAIP.Core.ReloadCapabilities` で再起動なしに反映できる |

`EngineVersion` / `BuildConfiguration` / `ExecutionEnvironment` / `OptionalPluginDisabled` は、いずれも人間が変更できるものを指します。`EngineApiNotExported` と `DelegationTargetMissing` はそうではありません — ini フラグ、Capability 付与、エンジンバージョン、プラグインの切り替えのいずれも解決しません。取れる手段は別の経路を探すことだけです。`SafetyPolicyDisabled` だけは性質が異なり、**唯一 ini の問題である値**です。`Config/DefaultUAIP.ini` への `AllowedCapabilities` / `DeniedCapabilities` と同種の編集で解決する値はこれだけです。

`Available: false` のコマンドを名前で呼び出すと失敗しますが、**返る ErrorCode は detail によって変わります**。環境・ビルドに関する 6 値（`EngineVersion` / `BuildConfiguration` / `ExecutionEnvironment` / `OptionalPluginDisabled` / `EngineApiNotExported` / `DelegationTargetMissing`）は `AbilityUnavailable`（HTTP 501「ここでは実行できない」）で失敗します。`SafetyPolicyDisabled` と `Unspecified` は `PolicyViolation`（HTTP 403）で失敗します — この 2 つだけが「設定を変えれば直る」に当てはまるためです。`ErrorMessage` にはいずれの場合も同じ情報が繰り返されます：`"Command '<name>' is not available (<UnavailableDetail>): <UnavailableDetailMessage>"` — `UnavailableDetail` が `Unspecified` の場合は、従来からの汎用的な文 `"... is not available in the current SafetyPolicy configuration."` になります。

### 新たに詳細が付くようになった対象

- **`UAIP.Runtime.LiveLink.*` — このドメインの全 14 コマンド**は、このプロセスにモジュラー機能として `ILiveLinkClient` が登録されていない場合（`LiveLink` プラグインが無効、または未ロード）に `UnavailableDetail: "ExecutionEnvironment"` を返します。このモジュールでコンパイルから除外されているものはありません — [UAIP.Runtime.LiveLink](#uaipruntimelivelink) を参照。
- **`UAIP.Editor.AnimSequence.SelectAnimNotify`** は UE 5.8 以降専用です。UE 5.7 では通知ウィジェットの型とそのノードオブジェクトインターフェースが Persona モジュール内部限定であるため、`UnavailableDetail: "EngineVersion"` を返します。[UAIP.Editor.AnimSequence](#uaipeditoranimsequence) を参照。
- **`UAIP.Core.ReloadCapabilities`** は、`AllowCapabilityReload` が既定の `False` のままのとき、従来の汎用的な文だけでなく、設定すべき ini キー名を含む `UnavailableDetail: "SafetyPolicyDisabled"` を返すようになりました。この値だけは ErrorCode が `AbilityUnavailable` ではなく `PolicyViolation` のままです。フラグを設定すれば実際に解決するためです。[UAIP.Core](#uaipcore) を参照。

---

## ドメインサマリ

| ドメイン | プロバイダプレフィックス | UAIP コマンド | Toolset ブリッジ | デモ |
|---|---|---:|---:|---:|
| Core | `UAIP.Core` | 12 | — | ✅ |
| Core Artifacts | `UAIP.Core.Artifacts` | 1 | — | ✅ |
| Editor Workspace | `UAIP.Editor.Workspace` | 24 | 1 | 一部（19/24） |
| Editor Engine Log | `UAIP.Editor.Engine.Log` | 1 | 4 | ✅ |
| Editor Engine Plugin 🧩 | `UAIP.Editor.Engine.Plugin` | 9 | 15 | 一部（5/9） |
| Editor Engine CVar 🧩 | `Toolset.Editor.Toolset.EngineManagement` | — | 1 | — |
| Editor Engine ConfigSettings | `UAIP.Editor.Engine.ConfigSettings` | 8 | 8 | 一部（5/8） |
| Editor Engine Toolset 🧩 | `UAIP.Editor.Engine.Toolset` | 1 | — | — |
| Editor Observation | `UAIP.Editor.Observation` | 15 | — | ✅ |
| Editor Execution | `UAIP.Editor.Execution` | 9 | — | — |
| Editor UI Automation | `UAIP.Editor.UIAutomation` | 17 | 10 | ✅ |
| Editor Assets | `UAIP.Editor.Assets` | 51 | 6 | 一部（29/51） |
| Editor SemanticSearch 🧩 | `UAIP.Editor.SemanticSearch` | 5 | 2 | — |
| Editor Level | `UAIP.Editor.Level` | 24 | 8 | 一部（10/24） |
| Editor Property | `UAIP.Editor.Property` | 12 | — | 一部（6/12） |
| Editor Blueprint | `UAIP.Editor.Blueprint` | 21 | — | — |
| Editor UMG | `UAIP.Editor.UMG` | 22 | 13 | — |
| Editor Material | `UAIP.Editor.Material` | 11 | — | — |
| Editor GameplayTags | `UAIP.Editor.GameplayTags` | 7 | 6 | — |
| Editor GameFeatures 🧩 | `UAIP.Editor.GameFeatures` | 5 | 4 | — |
| Editor Niagara 🧩 | `UAIP.Editor.Niagara` | 52 | 45 | — |
| Editor Physics | `UAIP.Editor.Physics` | 31 | 17 | — |
| Editor Dataflow 🧩 | `UAIP.Editor.Dataflow` | 9 | 7 | — |
| Editor ChaosClothAsset 🧩 | `UAIP.Editor.ChaosClothAsset` | 10 | 6 | — |
| Editor Skeleton | `UAIP.Editor.Skeleton` | 11 | — | — |
| Editor MetaHuman 🧩 | `UAIP.Editor.MetaHuman` | 56 | 9 | — |
| Editor DataTable | `UAIP.Editor.DataTable` | 8 | — | — |
| Editor AnimBlueprint | `UAIP.Editor.AnimBlueprint` | 19 | — | — |
| Editor AnimBlueprint UAF 🧩 | `UAIP.Editor.AnimBlueprint.UAF` | 1 | — | — |
| Editor UAF 🧩 | `UAIP.Editor.UAF` | 19 | — | — |
| Editor UAF AnimGraph 🧩 | `UAIP.Editor.UAF.AnimGraph` | 1 | — | — |
| Editor SoundCue | `UAIP.Editor.SoundCue` | 8 | — | — |
| Editor SoundSettings | `UAIP.Editor.SoundSettings` | 13 | — | — |
| Editor MVVM 🧩 | `UAIP.Editor.MVVM` | 26 | 9 | — |
| Editor BehaviorTree | `UAIP.Editor.BehaviorTree` | 18 | 7 | — |
| Editor MetaSound 🧩 | `UAIP.Editor.MetaSound` | 10 | — | — |
| Editor EQS 🧩 | `UAIP.Editor.EQS` | 9 | — | — |
| Editor Sequencer | `UAIP.Editor.Sequencer` | 131 | 61 | — |
| Editor StateTree | `UAIP.Editor.StateTree` | 39 | 8 | — |
| Editor Curve | `UAIP.Editor.Curve` | 6 | — | — |
| Editor PCG 🧩 | `UAIP.Editor.PCG` | 34 | 31 | — |
| Editor WorldConditions 🧩 | `UAIP.Editor.WorldConditions` | 13 | 2 | — |
| Editor Conversation 🧩 | `UAIP.Editor.Conversation` | 7 | 5 | — |
| Editor ControlRig | `UAIP.Editor.ControlRig` | 68 | 107 | — |
| Editor ControlRig Dynamics 🧩 | `UAIP.Editor.ControlRig.Dynamics` | 17 | — | — |
| Editor ControlRig Physics 🧩 | `UAIP.Editor.ControlRig.Physics` | 8 | — | — |
| Editor EnhancedInput | `UAIP.Editor.EnhancedInput` | 15 | — | — |
| Editor GAS 🧩 | `UAIP.Editor.GAS` | 8 | 14 | — |
| Editor Python Extension 🧩 | `UAIP.Editor.Python` | 1 | — | — |
| Editor Sandbox 🧩 | `UAIP.Editor.Sandbox` | 6 | — | — |
| Editor WorldPartition | `UAIP.Editor.WorldPartition` | 34 | — | — |
| Editor Foliage | `UAIP.Editor.Foliage` | 11 | — | — |
| Editor DataRegistry 🧩 | `UAIP.Editor.DataRegistry` | 9 | 7 | — |
| Editor MotionMatching 🧩 | `UAIP.Editor.MotionMatching` | 23 | — | — |
| Editor Chooser 🧩 | `UAIP.Editor.Chooser` | 20 | — | — |
| Editor AnimSequence | `UAIP.Editor.AnimSequence` | 13 | — | — |
| Editor ChaosDestruction | `UAIP.Editor.ChaosDestruction` | 29 | — | — |
| Editor Subsonic 🧩 | `UAIP.Editor.Subsonic` | 22 | — | — |
| Editor GroomAsset 🧩 | `UAIP.Editor.GroomAsset` | 35 | — | — |
| Editor Validation 🧩 | `UAIP.Editor.Validation` | 7 | — | — |
| Editor LiveLink 🧩 | `UAIP.Editor.LiveLink` | 11 | — | — |
| Editor Mass 🧩 | `UAIP.Editor.Mass` | 7 | — | — |
| Runtime PIE | `UAIP.Runtime.PIE` | 6 | 3 | ✅ |
| Runtime World | `UAIP.Runtime.World` | 14 | 1 | — |
| Runtime Observation | `UAIP.Runtime.Observation` | 14 | — | ✅ |
| Runtime Execution | `UAIP.Runtime.Execution` | 3 | — | — |
| Runtime Assertion | `UAIP.Runtime.Assertion` | 4 | — | ✅ |
| Runtime Input | `UAIP.Runtime.Input` | 15 | — | 一部（2/15） |
| Runtime GAS 🧩 | `UAIP.Runtime.GAS` | 17 | — | — |
| Runtime Niagara 🧩 | `UAIP.Runtime.Niagara` | 4 | 4 | — |
| Runtime LiveLink | `UAIP.Runtime.LiveLink` | 14 | — | — |
| Runtime Engine Log | `UAIP.Runtime.Engine.Log` | 3 | — | 一部（2/3） |
| Runtime Engine Plugin | `UAIP.Runtime.Engine.Plugin` | 5 | — | ✅ |
| Runtime Engine CVar | `UAIP.Runtime.Engine.CVar` | 4 | — | 一部（2/4） |
| Runtime Engine Config | `UAIP.Runtime.Engine.Config` | 2 | — | 一部（1/2） |
| Runtime Insights Trace | `UAIP.Runtime.Insights.Trace` | 11 | — | 一部（3/11） |
| Runtime Insights Analysis | `UAIP.Runtime.Insights.Analysis` | 3 | — | — |
| Runtime SaveGame | `UAIP.Runtime.SaveGame` | 10 | — | — |
| Runtime AI | `UAIP.Runtime.AI` | 14 | — | 一部（13/14） |
| Runtime StateTree 🧩 | `UAIP.Runtime.StateTree` | 7 | — | — |
| Runtime CommonUI 🧩 | `UAIP.Runtime.CommonUI` | 4 | — | — |
| Runtime Chaos Destruction | `UAIP.Runtime.ChaosDestruction` | 8 | — | 一部（7/8） |
| Runtime Navigation | `UAIP.Runtime.Navigation` | 8 | — | 一部（7/8） |
| Runtime Animation | `UAIP.Runtime.Animation` | 7 | — | 一部（6/7） |
| Runtime Network | `UAIP.Runtime.Network` | 7 | — | 一部（3/7） |
| Runtime Mass | `UAIP.Runtime.Mass` | 6 | — | — |

---

## 参照・構造体・コンテナの書き込み

以下に挙げるプロパティ書き込みコマンドは、値を 2 通りの形式で受け取り、値全体を置き換える代わりにコンテナの要素 1 つだけを操作することもできます。どの Capability が必要になるかは書き込み実行時にプロパティの型から決まるため、コマンドが宣言する `RequiredCapabilities` には現れません — 先にプロパティを読む（[書き込みに何が必要かを知る](#書き込みに何が必要かを知る)を参照）か、拒否の返答から不足している名前を読み取ってください。

### Capability

| Capability | 必要になる条件 |
|---|---|
| `PropertyReferenceEdit` | 書き込む値がオブジェクト / クラス / ソフト / ウィーク / レイジー / インターフェース参照、デリゲート、フィールドパスであるか、それらを（どの深さであれ）内包している場合。参照を空にする操作にも必要です — 依存関係を付けることと外すことは同じ種類の変更だからです |
| `PropertyStructuredEdit` | プロパティが、組み込みの値カタログ外の構造体・配列・セット・マップ・オプショナル・固定長配列である場合 |

どちらも DefaultDenied です — `Config/DefaultUAIP.ini` で有効化してください（[Safety & Capabilities](safety.md) 参照）。参照を内包する構造体の書き込みには**両方**が必要なので、構造側の Capability だけで参照のゲートを迂回することはできません。

すでに独自の Capability で参照の書き込みを管理しているモジュールは、参照側についてはその名前を使い続けます — `SetAnimNotifyProperty` は `AnimNotifyReferenceEdit`、`SetDataflowNodeProperty` は `DataflowReferenceEdit`、Subsonic の各コマンドは `SubsonicEventEdit`、`SetSlotProperties` は `WidgetSlotReferenceEdit`、Enhanced Input の Trigger / Modifier setter 4 コマンドは `EnhancedInputReferenceEdit`、`SetStateTreeParameter` は `StateTreeParameterReferenceEdit` を参照します。構造・コンテナ側は常に `PropertyStructuredEdit` です。同じパターンはこの一覧の外でも成り立ちます — `AddSetParameterEntry` / `AddSetParametersModule` は、渡された `DefaultValue` がデータインターフェース / オブジェクト型パラメータのものである場合に `NiagaraReferenceEdit` を参照します。拒否の返答は、そのコマンド自身の書き込み経路が実際に参照する Capability 名を返すため、案内された名前は常に運用者へ依頼する価値のある名前になっています。

### パラメータ

| パラメータ | 型 | 意味 |
|---|---|---|
| `ValueJson` | 任意の JSON 値 | エンジンのテキスト形式ではなく JSON ドキュメントとしての値。`Replace` では新しい値そのもの、配列の `Insert` では挿入する要素、マップの `Insert` ではペアの値側を運びます |
| `Operation` | 文字列 | `Replace`（既定）/ `Insert` / `Remove` / `Clear`。省略すると、要素操作が存在しなかった頃とまったく同じ挙動になります |
| `ElementIndex` | 整数 | 配列要素を挿入・削除する位置。`Insert` では最後の要素の 1 つ後ろの位置を指定して末尾へ追加できます。32 ビット符号付き整数に収まる整数値である必要があります — `1.5` は丸められるのではなく拒否されます |
| `ElementKeyJson` | 任意の JSON 値 | セット操作が指す要素、またはマップ操作が指すペアのキー側 |

`ValueJson` はそのコマンドのテキスト値パラメータと排他です — 以下のコマンドではすべて `Value` ですが、`SetSectionProperty` だけは `PropertyValue` という綴りです。両方を指定すると `InvalidParams` になります。

| 操作 | 配列 | セット | マップ |
|---|---|---|---|
| `Replace` | コンテナ全体を置き換える | コンテナ全体を置き換える | コンテナ全体を置き換える |
| `Insert` | `ElementIndex` の位置へ `ValueJson` を挿入 | `ElementKeyJson` がまだ無ければ追加 | `ElementKeyJson` をキーとして `ValueJson` を格納（既存の値は上書き） |
| `Remove` | `ElementIndex` の要素を削除 | `ElementKeyJson` を削除 | `ElementKeyJson` をキーとするエントリを削除 |
| `Clear` | コンテナを空にする | コンテナを空にする | コンテナを空にする |

各操作が受け付けるパラメータ：

- `Replace` はテキスト値と `ValueJson` の**ちょうど一方**を取り、`ElementIndex` / `ElementKeyJson` はいずれも取りません
- `Insert` / `Remove` は `ElementIndex` と `ElementKeyJson` の**ちょうど一方**を取り、テキスト値は取りません
- `Clear` は `ElementIndex` / `ElementKeyJson` / `ValueJson` のいずれも取りません

これらの違反はすべて、プロパティパスを解決する**前**に `InvalidParams` として拒否されます。したがって答えが「たまたま名指ししたプロパティの事情」に左右されることはありません。

`ValueJson` に JSON の `null` を指定するのは「値の省略」ではなく「値として null を指定する」ことであり、参照を空にする方法がこれです。

### `Value` は必須パラメータではなくなりました

下表のすべてのコマンドで、テキスト値のパラメータ（`Value`、`SetSectionProperty` では `PropertyValue`）がスキーマ上 `Required` から `Optional` へ変わりました。スキーマは「どちらか一方が必要」を表現できず、必須のままでは `Remove` / `Clear` と `ValueJson` による書き込みがすべて到達不能になるためです。Subsonic の各コマンドの `Value` も同様に変わりました。

**拒否されるリクエストの集合は変わっていませんが、拒否される段と文言が変わりました。** 値を何も指定しない `Replace` は、従来はスキーマ検証の段で「`Value` が必須である」旨のメッセージとともに拒否されていました。現在はコマンド自身が次の文言で拒否します。

- 両方の形式を受け付ける 15 コマンド: `Invalid parameters: operation 'Replace' requires either 'Value' or 'ValueJson'.`
- `ValueJson` を持たない Subsonic の 3 コマンド: `Invalid parameters: operation 'Replace' requires 'Value'.`

`ErrorCode` はいずれも `InvalidParams` のままです。古いメッセージ本文で分岐している場合は書き換えてください。

要素操作について知っておくとよいこと：

- コンテナの性質上そうなる範囲で冪等です。セットに既にある要素を足す、セットやマップに無い要素を消す、といった操作は成功します。したがって `Success` だけでは何かが動いたかどうかは分かりません — そのために成果物には `Operation` と並んで `Changed` フィールドが載ります（`Replace` でも載ります）
- 既に 4096 要素を超えるコンテナは、`Remove` / `Clear` を含めどの操作でも拒否されます。コミット前にコンテナ全体をコピーして検証するため、この上限は「その操作がコンテナに何をするか」ではなく「コンテナを読むコスト」に対するものです
- キーの型が参照であるエントリは、キーだけを書き換えることはできません — 削除してから挿入し直してください
- マップを丸ごと置き換えるドキュメントに同じキーが複数含まれる場合は、後から現れたものが残ります（`Insert` と同じ扱い）
- オプショナルな値は「値なし」「値ありだが中身が空」「値あり」の 3 状態を区別します。受け付ける操作は `Replace` のみです — `Insert` / `Remove` / `Clear` が言おうとすることは、この 3 状態で既に表現できるためです
- 固定長配列（`int32 Values[3]` のような形）も `Replace` のみを受け付け、渡す JSON 配列の要素数はプロパティが宣言する個数と一致している必要があります
- **固定長配列は、1 要素ずつ指すか、全体として扱うかのどちらかです。** 下の表のうち共有のプロパティ経路で読み書きするすべてのコマンド（`GetDataflowNodeProperty` / `SetDataflowNodeProperty` を含む）に当てはまります
  - `Values[1]` は 1 要素を指します。その要素だけを読み書きでき、宣言された個数以上の添字は `InvalidParams` で断られます
  - 添字なしの `Values` は配列全体を指します。読み取りは全要素を 1 つの JSON 配列で返し、その値はそのまま全体の書き込みに渡せます。全体の書き込みは全要素を検証し、1 つでも断られれば何も書きません。全体の読み取りは JSON だけで、エンジンのテキスト形式はありません（固定長配列の書き戻しは `ValueJson` でしか行えないため）
  - 構造体の固定長配列は、添字なしで経路の途中に置けません。`Arr.Member` は `InvalidParams` で断られ、メッセージに添字付きの形（`Arr[0]` 〜 `Arr[N-1]`）が示されます。以前は黙って要素 0 を読み書きしていました。エンジンのセクションのチャンネル（`GetSectionProperty` の `Translation.Times` など）もこれに含まれます
- **配列要素をその場で置き換える操作は `Operation` ではなく `PropertyPath` で表します。** `Arr[3]` を既定の `Replace` で書いてください。`Insert` は「新しい要素を差し込む」操作であり、「その位置の要素を上書きする」操作ではありません

### これらのパラメータを受け付けるコマンド

| コマンド | ドメイン | テキスト値のパラメータ | `ValueJson` | 参照側の Capability |
|---|---|---|---|---|
| `SetActorProperty` | `UAIP.Editor.Property` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetAssetProperty` | `UAIP.Editor.Property` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetBlueprintDefault` | `UAIP.Editor.Property` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetWorldSetting` | `UAIP.Editor.Property` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetProjectSetting` | `UAIP.Editor.Property` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetDataTableRow` | `UAIP.Editor.Property` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetBlueprintComponentProperty` | `UAIP.Editor.Blueprint` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetActorComponentProperty` | `UAIP.Editor.Level` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetSectionProperty` | `UAIP.Editor.Sequencer` | `PropertyValue` | ✅ | `PropertyReferenceEdit` |
| `SetSoundClassSettings` | `UAIP.Editor.SoundSettings` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetSoundAttenuationSettings` | `UAIP.Editor.SoundSettings` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetSoundMixSettings` | `UAIP.Editor.SoundSettings` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetSoundCueNodeProperty` | `UAIP.Editor.SoundCue` | `Value` | ✅ | `PropertyReferenceEdit` |
| `SetAnimGraphNodeProperty` | `UAIP.Editor.AnimBlueprint` | `Value` | ✅ | `AnimBlueprintReferenceEdit` |
| `SetDataflowNodeProperty` 🧩 | `UAIP.Editor.Dataflow` | `Value` | ✅ | `DataflowReferenceEdit` |
| `SetAnimNotifyProperty` | `UAIP.Editor.AnimSequence` | `Value` | ✅ | `AnimNotifyReferenceEdit` |
| `SetPoseSearchSchemaChannelProperty` 🧩 | `UAIP.Editor.MotionMatching` | `Value` | ✅ | —（参照は一律拒否） |
| `SetSubsonicEventActionProperty` 🧩 | `UAIP.Editor.Subsonic` | `Value`（元から JSON 値） | — | `SubsonicEventEdit` |
| `SetSubsonicActionModifierProperty` 🧩 | `UAIP.Editor.Subsonic` | `Value`（元から JSON 値） | — | `SubsonicEventEdit` |
| `SetSubsonicParameterValue` 🧩 | `UAIP.Editor.Subsonic` | `Value`（元から JSON 値） | — | `SubsonicEventEdit` |

Subsonic の 3 コマンドは `ValueJson` を**取りません**。既存の `Value` パラメータがエンジンのテキストではなく元から JSON 値であり、構造化された値をそのまま運べるためです。同じ意味のパラメータを 2 つ並べても、利用者がどちらを使うべきか判断できなくなるだけです。`Operation` / `ElementIndex` / `ElementKeyJson` は他と同様に受け付けます。拒否文も `Value` だけを名指しし、宣言していないパラメータには一切触れません — `Replace` は `Value` を必要とし、`Clear` は `Value` を拒否します。

`SetPCGNodeProperty` / `SetCustomCppPCGNodeProperty` / `SetCustomBlueprintPCGNodeProperty` / `SetConversationNodeProperty` は、元から値を JSON ドキュメントとして受け取っており、要素操作は取りません。これらで変わったのは、参照・構造体・コンテナを**恒久的に拒否しなくなった**点です — 他と同じく、上記 2 つの Capability で開くようになりました。

### 書き込みに何が必要かを知る

対応する `Get*` コマンドは、読み取った値に `WriteRequirements` オブジェクトを添えて返します。

| フィールド | 意味 |
|---|---|
| `RequiredCapabilities` | そのコマンド自身の書き込み経路が実際に照会する Capability 名。付与すれば実際に書けるようになる名前 |
| `HeldCapabilities` / `MissingCapabilities` | 上記のうち、読み取りを発行したセッションが保有しているもの / していないもの |
| `IsWritable` / `RefusalReason` | セッションが何を持っているかに関わらず、そのプロパティの型とフラグが書き込みを許すかどうか |
| `WriteInputForm` | `TextOrJson` / `JsonOnly` / `None` — 値をどちらの入力欄で渡す必要があるか。`None` は `IsWritable: false` と対で返り、どの形式でも受け付けないこと（どの Capability を付与しても変わらないこと）を意味します |

一部のコマンドは独自の判定で書き込み可否を決めており、この報告を添えません。その場合は書き込みを試してください — 拒否の返答に不足している Capability 名が載ります。無いのは事前の案内だけで、進めなくなるわけではありません。

さらに 10 個の取得系コマンドがこの報告を返すようになりました。既存の値の返し方に合わせて 2 つの形のいずれかを取ります。

| コマンド | 報告の位置 |
|---|---|
| `GetSlotProperties`（`UAIP.Editor.UMG`） | `Properties` と並ぶ `PropertyWriteRequirements` マップ（キーはプロパティ名） |
| `GetInputActionInfo` / `GetMappingContextInfo`（`UAIP.Editor.EnhancedInput`） | 各 Trigger / Modifier エントリの中、`Params` と並ぶ `PropertyWriteRequirements` マップ |
| `GetStateTreeParameters`（`UAIP.Editor.StateTree`） | 各パラメータエントリに入れ子の `WriteRequirements` オブジェクト |
| `GetWorldConditionInfo`（`UAIP.Editor.WorldConditions`） | 各条件プロパティエントリに入れ子の `WriteRequirements` オブジェクト |
| `GetAnimNotifyClassSchema`（`UAIP.Editor.AnimSequence`） | 各プロパティエントリに入れ子の `WriteRequirements` オブジェクト |
| `GetAnimNotifyProperty`（`UAIP.Editor.AnimSequence`） | 各プロパティエントリに入れ子の `WriteRequirements` オブジェクト。単一プロパティを指定した場合は `Data` の `PropertyName` / `Value` と並べて直接返す |
| `GetPoseSearchChannelClassSchema`（`UAIP.Editor.MotionMatching`） | 各プロパティエントリに入れ子の `WriteRequirements` オブジェクト |
| `GetBehaviorTreeNodeProperties`（`UAIP.Editor.BehaviorTree`） | 各プロパティエントリに入れ子の `WriteRequirements` オブジェクト |
| `GetStackInputData`（`UAIP.Editor.Niagara`） | 各スタック入力エントリに入れ子の `WriteRequirements` オブジェクト |

値マップ自体（`Properties` / `Params`）の形は変えていないため、値だけを読む呼び出し側に影響はありません。Enhanced Input の 2 つの取得系では、値マップが従来スキップしていた参照・コンテナも含め **編集可能な全プロパティ** を報告します — スキップされていた型こそが Capability を要求する型だからです。`GetWorldConditionInfo` の `RequiredCapabilities` は常に空配列です。この経路は参照もコンテナも一切受け付けないため、運用者へ依頼すべき Capability が存在せず、名前を挙げると「付与しても何も解禁されない権限」を案内することになるためです。`GetAnimNotifyProperty` は `GetAnimNotifyClassSchema` と同じキー名・同じ入れ子の形で返すため、読み方は両者で共通です。違いは判定の対象で、クラスのデフォルトではなく `NotifyGuid` で指定された実際の通知インスタンス（`SetAnimNotifyProperty` が実際に書き込む対象）に対して解決されます。`GetBehaviorTreeNodeProperties` は `FBlackboardKeySelector` プロパティを、構造体自身のフィールドではなくベアなキー名のプレーンテキストとして報告・受理します — このプロパティは共有の書き込みモデルに一切乗らないため、`WriteRequirements` は `SetBehaviorTreeNodeProperty` の書き込み経路が実際に照会する唯一の Capability である `BehaviorTreeNodeReferenceEdit` だけを名指しします。`GetStackInputData` の `WriteRequirements` は `AddSetParameterEntry` で既定値を変更するのに何が要るかを述べます。プレーンなオブジェクト参照を既に保持している入力は、依然として `ValueMode: "Unknown"` と空の `Value` を返します — `AddSetParameterEntry` 自身の型許可リストにその種類のエントリを作る経路がそもそも存在しないためです。これは書き込める範囲の欠落であって、このコマンドの読み取り側の欠落ではありません。

> ⚠️ **破壊的変更**: `GetAnimNotifyClassSchema` と `GetPoseSearchChannelClassSchema` は従来、この報告をプロパティエントリの直下に、独自の名前 — `bIsWritable` / `NotWritableReason` / `WriteInputForm` / `RequiredCapabilities` — で返しており、`HeldCapabilities` / `MissingCapabilities` に相当するものは一切ありませんでした。両コマンドとも、上の表と同じ入れ子の `WriteRequirements` オブジェクトを返すようになったため、旧来のフラットな名前を読み続けている呼び出し側には何も見つかりません。`WriteRequirements.IsWritable` / `.RefusalReason` / `.WriteInputForm` / `.RequiredCapabilities` を読んでください。`.HeldCapabilities` / `.MissingCapabilities` は改名ではなく新しい情報です。どのプロパティが書けるか、書くのに何が要るかという判定自体は変わっておらず、変わったのは読む位置だけです。これにより、UAIP 全体で「書き込みに何が必要か」を返す取得系コマンドが、すべて同じ形になりました。

### つまずきやすいところ

- **ハード参照は、既に読み込まれているアセットしか指せません。** プロパティの書き込みが副作用でアセットを読み込むことはないため、オブジェクトパスは、そのアセットを既に何かが開いている場合にのみ解決されます。「存在しない」と「存在するが読み込まれていない」は同じ拒否として返ります — 読み込まずに両者を区別する手段がないためです。先にアセットを開いてから書き込んでください。ソフト参照（`TSoftObjectPtr` / `TSoftClassPtr` / `FSoftObjectPath` / `FSoftClassPath`）は対象外で、アセットレジストリに対して検証されるため対象の読み込みを必要としません。この規則は、参照を書き込む**すべての** UAIP コマンドに及びます — 従来は参照先を暗黙に読み込んでいた Subsonic の各コマンドも含まれるため、以前は通っていた書き込みが、先にアセットを開かないと通らなくなる場合があります。
- **参照と複合値はテキスト形式では書けません。** これらの `WriteInputForm` は `JsonOnly` で、Capability を付与してもオブジェクトパスを `Value` に渡すと拒否されます。テキストインポート経路は Capability のゲートの内側で参照を解決・ロードしてしまうためです。`ValueJson`（Subsonic の各コマンドでは元から JSON である `Value`）を使ってください。逆にテキスト形式でしか書けない値型もわずかに存在します。どちらかは `WriteInputForm` が示します。
- **一部のコマンドは、Capability の有無に関わらず参照そのものを拒否します。** `SetPoseSearchSchemaChannelProperty` は参照を内包する型を一切書き込みません — チャンネルのサブチャンネル配列はチャンネルを作成する経路そのものであり、そこへ直接書けると `AddPoseSearchSchemaChannel` が持つクラス許可リストを迂回できてしまうためです。専用のチャンネルコマンドを使ってください。これは権限で解除できるものではなく `PolicyViolation` として返ります。
- **ユーザー製 PCG ノードでは、Capability を持たないセッションに見える型が絞られます。** `GetCustomPCGNodeSchema` / `GetCustomBlueprintPCGNodeSchema` / `GetPCGNativeNodeSchema` はそうしたセッションに対して curated な型だけを列挙し、対応する setter の拒否文も意図的に型名を明かしません。ただし応答は「何かが除かれたこと」自体は伝えます — `HiddenCount`、`HiddenCapabilities`（どの権限があれば見えるか）、そして `MissingCapability` / `Unwritable` の 2 キーを常に持ち合計が `HiddenCount` と一致する `HiddenReasons` オブジェクトが返ります。案内された Capability を付与すれば隠れていた項目が現れ、`HiddenCount` は 0 に戻ります。なお**プロパティ名**は元から隠していません — 綴りを間違えれば「そのプロパティは無い」と返るため、打ち間違いと権限不足は引き続き区別できます。
- **パスの途中のセグメントも検査されます。** `Struct` 自体が読み取り専用・非推奨・Details パネルに現れない場合、`Struct.Inner` は拒否されます — 内側のメンバーを名指しして読み取り専用の階層を通り抜けることはできません。コンテナのインデックスを挟む場合（`Array[0].Inner`）にも同じ検査が働き、判定対象はコンテナ本体になります。
- **アセットパスを保持する値は 1 つのまとまりとして書き込みます。** `FSoftObjectPath` / `FSoftClassPath` / `FTopLevelAssetPath` はメンバー単位では指定できません — 内側を書き換えられると参照のゲートを素通りできてしまうためです。
- **参照へ書き込むクラス自体が、`PropertyReferenceEdit` に加えてドメイン自身の Capability を要求することがあります。** 従来は `PropertyEdit` + `PropertyReferenceEdit` を持っていれば、`SetAssetProperty` など同型のコマンドで、既にロード済みのどのクラスでもハード参照や instanced subobject プロパティへ書き込めました — そのクラスが何であるかは一切問われませんでした。呼び出し側が名指ししたクラスから instanced subobject を構築する経路も同じ確認を通ります。この 2 つの Capability しか持たないセッションはどちらにしても影響を受けません — そもそも参照書き込みへ到達できたことが一度もないためです。現時点では `UAIP.Editor.Material` にこの確認が配線されています。`UMaterialExpression` 派生クラスを参照または instanced subobject プロパティへ書き込むには、`AddMaterialNode` が要求するのと同じく `MaterialCustomTypeEdit` / `MaterialCustomNodeEdit` が追加で必要になります — [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照してください。他のドメインはまだこの確認を登録していないため、汎用プロパティコマンド経由でそのドメイン自身がゲートしている型を書き込んでも、現時点では捕捉されません。

---

## Capability でゲートされたカスタム型

いくつかのドメインは、プロジェクトやプラグインが定義した型を Capability の付与があって初めて通します — 各ドメイン自身の Note を参照してください（例: [UAIP.Editor.Material](#uaipeditormaterial)、[UAIP.Editor.AnimBlueprint](#uaipeditoranimblueprint)、[UAIP.Editor.ControlRig](#uaipeditorcontrolrig)、[UAIP.Editor.EnhancedInput](#uaipeditorenhancedinput)、[UAIP.Editor.UAF](#uaipeditoruaf-)、[UAIP.Editor.BehaviorTree](#uaipeditorbehaviortree)、[UAIP.Editor.MetaSound](#uaipeditormetasound-)、[UAIP.Editor.EQS](#uaipeditoreqs-)、[UAIP.Editor.StateTree](#uaipeditorstatetree)、[UAIP.Editor.WorldConditions](#uaipeditorworldconditions-)、[UAIP.Editor.Sequencer](#uaipeditorsequencer)、[UAIP.Editor.SoundCue](#uaipeditorsoundcue)、[UAIP.Editor.MotionMatching](#uaipeditormotionmatching-)、[UAIP.Editor.Conversation](#uaipeditorconversation-)）。以下はそれらすべてに共通する内容で、ドメインごとには繰り返しません。

コンポーネントクラスも同じ考え方でゲートされますが、規則は独自のものです（詳細は [UAIP.Editor.Blueprint — コンポーネント — SCS](#コンポーネント--scs8)）。Capability 名は `ComponentCustomTypeEdit` で、そのクラスのコンポーネントの**数が増える**操作すべて（`AddActorComponent` / `AddBlueprintComponent` / `DuplicateBlueprintComponent`）が共有します。上記ドメインと違い、コンポーネントの削除・リネーム・付け替えはこの Capability の対象では**ありません**。

- **確認は `Add*` だけでなく、その型に触る操作すべてで行われます。** ゲートされた型のノードがグラフに存在するようになった後は、そのノードを編集・接続・切断・コンパイル・削除するとき、また実効型を変更する（Reparent）ときや参照を新規作成・差し替えるときにも、同じ Capability があらためて確認されます。追加時に Capability を持っていたことは以降の呼び出しには引き継がれません — セッションが後から Capability を失えば（role の変更、`AllowedCapabilities` の絞り込みなど）、それらの後続操作も `Add*` と同じように権限不足で断られます。
- **⚠️ 破壊的変更 — 削除と切断は従来ゲートされていませんでした。** この変更以前は、各ドメインの `Add*` コマンドだけが追加する型を検査しており、ノードの削除やピンの切断はノードの型に関わらず無条件で通っていました。現在はそうではありません。ゲートされた型のノードを削除・切断するには、それを最初に作成するときに `Add*` が要求したのと同じ Capability が必要です。
- **もう追加できない型でも、片付けることはできます。** クラスの読み込みに失敗する型や、エンジンの更新でサポートが打ち切られた型は再追加できません — これは Capability を付与しても解消しない構造的な拒否です。しかしそのこと自体は、既存のノードを削除・切断できない理由にはなりません。セッションがその型に要る Capability を保有している限り、削除・切断は引き続き通ります。
- **コンパイルで確認されるのは「危険な種類」だけで、「自作」であること自体は対象にしません。** 「プロジェクト・プラグイン定義」と「危険」を分けて扱うドメイン（Material はそうです。この区別が無いドメインについては該当ドメイン自身の Note を参照してください）では、アセットのコンパイルはそのアセットに含まれる危険な種類の型についてだけ Capability を要求します。危険な種類ではない、ただの自作型はコンパイルを妨げません。そうでなければ、カスタム型を 1 つでも含むプロジェクトは、どのセッションでも毎回 Capability の付与なしには一切コンパイルできなくなってしまいます。
- **アセット作成経路の Capability 不足も、他の経路と同じく `CapabilityNotAvailable` で返ります。** `CreateAsset` の `FactoryParams` で名指しされた型（現時点では StateTree の `SchemaClass` と ControlRig の `ParentClass`）は、他と同じ admission ポリシーを通り、Capability 不足は `CapabilityNotAvailable` として返り、不足している Capability 名がメッセージ本文にすべて列挙されます（`Required capability is not available: <names>`）— `Add*` 自身の拒否とまったく同じです。同じフィールドに対する構造的な拒否（クラスが解決できない・基底型違い・abstract・deprecated）は、権限の欠落ではなくパラメータ自体についての判定であるため、引き続き `InvalidParams` です。⚠️ 本ページの過去の記述を訂正します: `ICreateAssetInterceptor` の割り込み地点はもともと成否の真偽値とメッセージだけを返す契約で、エラー分類を持ち回す手段がありませんでした — その結果、原因を問わず Capability 不足を含むこの経路の拒否はすべて `InvalidParams` になっていました。現在は分類を持ち回せるようになり、他の Capability でゲートされたドメインと同じエラーコードで分岐できます。

---

## 実行時コマンドの対象プレイワールドを指定する

ネットワークプレイの PIE セッションでは、**同じエディタプロセスの中で複数のワールドが同時に動きます** — サーバー 1 つと、1 つ以上のクライアントです。そのため 112 個の実行時コマンドが、どのワールドに作用するかを指定する 2 つの任意パラメータを受け付けます。どちらも任意で、両方とも省略した場合の挙動はこれらのパラメータが存在しなかった頃とまったく同じです。つまり**既存の呼び出しの意味は変わりません**。

| パラメータ | 型 | 意味 |
|---|---|---|
| `TargetNetRole` | string | `"Standalone"` / `"Server"` / `"Client"`。大文字小文字は区別しません。`"Server"` は Dedicated Server と Listen Server の**両方**にマッチします — 呼び出し側が考えるのは権限の所在であって、PIE がどちらの形式のサーバーを起動したかではないためです |
| `TargetPIEInstance` | integer | `ListPlayWorlds` が返すインスタンス番号。役割だけでは対象が 1 つに定まらないときに使います |

まずは [`ListPlayWorlds`](#uaipruntimeworld) から始めてください。エンジンがいま保持しているプレイワールドをすべて、それぞれの `PIEInstance` / `NetMode` / `MapName` / `bIsPrimaryPIEInstance` 付きで返します。この `PIEInstance` がそのまま `TargetPIEInstance` に渡せる値です。

### 対象の決まり方

| 送った内容 | 結果 |
|---|---|
| どちらも省略 | これらのパラメータが存在しなかった頃にこのコマンドが使っていたワールド — 主となるプレイセッション |
| `TargetNetRole` のみ、該当ワールドが 1 つ | そのワールド |
| `TargetNetRole` のみ、該当ワールドが複数 | `InvalidParams`。メッセージに候補が `TargetPIEInstance <n> (TargetNetRole "...", NetMode ..., map ...)` の形ですべて列挙されるため、そのうちの番号を足して同じ呼び出しを再実行できます |
| `TargetPIEInstance` のみ | そのインスタンス |
| 両方指定し、内容が一致 | そのインスタンス |
| 両方指定し、内容が食い違う | `InvalidParams`。そのインスタンスが実際には何の役割で動いているかを示します |
| どれにも当てはまらない役割・番号 | `NotAllowed` — プレイワールドは存在するが、指定したものが無い場合です。メッセージに実在するものが列挙されます |
| そもそも何も動いていない | `NotAllowed`。メッセージは `PIE is not running.`（パッケージ実行時は `No active game world.`） |

`InvalidParams` は「要求が実現できない対象を名指しした」こと、`NotAllowed` は「エディタがそのコマンドを実行できる状態にない」ことを意味します。どちらが返るかが、「呼び出しを直す」のか「プレイを開始する」のかの区別になります。

押さえておくべき制限が 2 つあります。

- **選べるのはこのエディタプロセス内のプレイセッションだけです。** 別プロセスとして起動した Dedicated Server は候補にならず、`ListPlayWorlds` にも現れません。
- **Toolset ブリッジコマンド（`Toolset.*`）はこれらのパラメータを受け付けません。** ブリッジはエンジン側 Toolset の入力をそのまま転送する層であり、スキーマも Toolset の宣言から生成されるため、UAIP 独自のパラメータを足す場所がありません。セッションを指定したい場合は、同じ操作を行うネイティブコマンドの方を使ってください。

### これらのパラメータを受け付けるコマンド

| ドメイン | コマンド |
|---|---|
| `UAIP.Runtime.World` | `SpawnActor`、`DestroyActor`、`TeleportActor`、`PossessActor`、`SetTimeScale`、`ExecuteConsoleCommand`、`SetDataLayerRuntimeState`、`GetDataLayerRuntimeState`、`ListDataLayerRuntimeStates`、`WaitForDataLayerStreaming` |
| `UAIP.Runtime.Observation` | `CaptureViewportImage`、`DumpWorldState`、`DumpActorState`、`DumpComponentState`、`CheckpointCapture`、`DumpGameViewportWidgets`、`FindGameViewportWidgets`、`DumpGameViewportWidgetTexts`、`DumpHUDState`、`ListSubsystems`、`DumpSubsystemState` |
| `UAIP.Runtime.Execution` | `RunFunctionalTest`、`RunRuntimeAutomationTest` |
| `UAIP.Runtime.Assertion` | `WaitForCondition`、`AssertActorProperty`、`AssertWorldState` |
| `UAIP.Runtime.Input` | `InjectInputKey`、`InjectEnhancedInputAction`、`InjectLegacyAction`、`InjectLegacyAxisInput`、`InjectLegacySpeechInput`、`AddMappingContext`、`RemoveMappingContext`、`SetInputMode`、`FlushInput`、`DumpInputState`、`GetEnhancedInputActionValue`、`EvaluateInputGateWithProjectCode`、`ClickGameViewportWidget`、`PressGameViewportUIKey`、`TypeGameViewportText` |
| `UAIP.Runtime.GAS` 🧩 | `GetAttributeValues`、`GetActiveEffects`、`GetGrantedAbilities`、`GetActiveTags`、`FindAttributeSetClasses`、`GrantAbility`、`RemoveAbility`、`ClearGrantedAbilities`、`ApplyEffect`、`RemoveEffect`、`ClearActiveEffects`、`SetAttributeValue`、`ResetAttributesToBase`、`SendGameplayEvent` |
| `UAIP.Runtime.Niagara` 🧩 | `GetUserVariables`、`GetVariable`、`SetVariable`、`SetSystem` |
| `UAIP.Runtime.AI` | `DumpAIPerceptionState`、`GetPerceivedActors`、`GetActorPerceivers`、`DumpAIPerceptionSystemState`、`ExplainSightPerception`、`DumpAIPerceptionSenseConfigs`、`DumpBehaviorTreeState`、`GetActiveBehaviorTreeNode`、`ListBehaviorTreeAgents`、`GetBlackboardValues`、`DescribeBehaviorTreeWithProjectCode`、`StartBehaviorTreeCapture` |
| `UAIP.Runtime.StateTree` 🧩 | `DumpStateTreeState`、`GetActiveStateTreeState`、`ListStateTreeComponents`、`DumpStateTreeInstanceData`、`StartStateTreeCapture` |
| `UAIP.Runtime.CommonUI` 🧩 | `DumpActivatableStacks`、`GetInputState`、`GetActionDisplayNames`、`DescribeActivatableWidgetsWithProjectCode` |
| `UAIP.Runtime.ChaosDestruction` | `ListGeometryCollections`、`DumpGeometryCollectionState`、`DumpChaosFieldState`、`StartDestructionCapture`、`CaptureGeometryCollectionStrain` |
| `UAIP.Runtime.Navigation` | `DumpNavigationSystemState`、`FindPath`、`IsLocationReachable`、`DumpNavMeshTiles`、`QueryNavModifiers`、`GetPathFollowingState`、`WaitForNavigationBuild`、`RebuildNavigation` |
| `UAIP.Runtime.Animation` | `DumpAnimInstanceState`、`GetAnimStateMachineStates`、`GetAnimBlendWeights`、`GetActiveMontages`、`GetAnimCurveValues`、`DumpAnimInstanceVariables`、`GetMotionMatchingState` |
| `UAIP.Runtime.Network` | `GetNetDriverState`、`ListNetConnections`、`DumpActorReplication`、`DumpReplicatedPropertyValues`、`CompareReplicatedProperties`、`SetNetworkEmulation`、`ResetNetworkEmulation` |
| `UAIP.Runtime.Mass` | `GetMassEntityCount`、`DumpMassEntityArchetypes`、`DumpMassProcessorGraph`、`DescribeMassEntity`、`GetMassEntityFragments` |

上の一覧のうち `CheckpointCapture` だけは、自分でワールドを解決しません。`CaptureViewportImage` と `DumpWorldState` を組み合わせたコマンドであり、指定された対象をそのまま両方へ引き渡します。これにより、1 つのチェックポイントに含まれるスクリーンショットと状態ダンプが、エンジンが別々に選んだ 2 つのワールドではなく、常に同じワールドを指すようになります。

`QuitGame` と `ListPlayWorlds`、および CVar 系コマンドはどちらのパラメータも受け付けません。前 2 つは単一のワールドに宛てた操作ではなく、CVar はワールド単位ではなくエンジン全体のものだからです。

### 互換性: すでにあったコマンドで変わったこと

ゲームビューポートの UI のコマンド（[`UAIP.Runtime.Observation`](#uaipruntimeobservation)・[`UAIP.Runtime.Input`](#uaipruntimeinput)）の追加にあわせて、既存の実行時コマンドがプレイワールドが無いことを報告する方法を揃えました。プレイワールドがあるあいだは何も変わりません。以下の違いが現れるのは、プレイワールドが無いとき、または Capability を拒否しているときだけです。

**プレイワールドが無いとき: エラーコードは `NotAllowed` になります。** プレイワールドを必要とする実行時コマンドは、共通の 1 つの対応表を通して、同じ `NotAllowed` で拒否するようになりました。シナリオがステップを自動で再試行するのは `ExecutionFailed` と `PreconditionFailed` の後だけなので、**これらのコマンドは、プレイワールドが無いときに再試行されなくなります**。PIE の起動を再試行で待っていたシナリオは、明示的に待つ形へ書き換えてください。

| モジュール | コマンド | 変更前 | 変更後 |
|---|---|---|---|
| Observation | `DumpWorldState`・`DumpActorState`・`DumpComponentState`・`CaptureViewportImage`・`CheckpointCapture` | `ExecutionFailed` | `NotAllowed` |
| Input | 既存の 11 コマンド | `ExecutionFailed` | `NotAllowed` |
| World | `SpawnActor`・`DestroyActor`（ほかの 8 コマンドは以前から `NotAllowed`） | `ExecutionFailed` | `NotAllowed` |
| GAS 🧩 | 14 コマンドすべて | `ExecutionFailed` | `NotAllowed` |
| Assertion | `AssertActorProperty`・`AssertWorldState`・`WaitForCondition` | `ExecutionFailed` | `NotAllowed` |
| Execution | `RunFunctionalTest`・`RunRuntimeAutomationTest` | `ExecutionFailed` | `NotAllowed` |
| Niagara 🧩 — **向きが逆です** | `GetUserVariables`・`GetVariable`・`SetSystem`・`SetVariable`（Toolset ブリッジ経由も同じ） | `PreconditionFailed` | `NotAllowed` |

- GAS の読み取り系 5 コマンド（`GetActiveEffects`・`GetActiveTags`・`GetAttributeValues`・`GetGrantedAbilities`・`FindAttributeSetClasses`）は、**ワールドを指定しなければ**（`TargetNetRole` / `TargetPIEInstance` を渡さなければ）、プレイワールドが無いとき、これまでどおり編集中のレベルを読みます。`NotAllowed` になるのは、ワールドを指定したのにそれが動いていない場合だけです。
- `WaitForCondition` は、待機の最初の判定でプレイワールドが無ければ `NotAllowed` になります。一度ワールドが見つかった後、待機の途中で消えた場合は、これまでどおり `ExecutionFailed` で終わり、シナリオは再試行します。
- `RunFunctionalTest` / `RunRuntimeAutomationTest` の実行の**途中で**プレイワールドが消えた場合は、これまでどおり `NotAllowed` ではなく、タイムアウトまたはテストの失敗として返ります。

**Capability。** `DumpWorldState`・`DumpActorState`・`DumpComponentState`・`DumpRuntimeLog`・`CapturePerformanceSnapshot`・`SearchLoadedClasses` は `RuntimeInspect` を、`CaptureViewportImage` は `RuntimeCapture` を必要とするようになりました。`CheckpointCapture` は内部でワールドの状態を書き出すため、これまでの Capability に加えて `RuntimeInspect` も必要です。どれも DefaultAllow なので、影響があるのは `DeniedCapabilities` でそれらを拒否している構成だけです。その場合、要求の受け付け時に `PolicyViolation` で拒否され、artifact は作られません。許可されていないだけの場合は `CapabilityNotAvailable` です。

**読み取り専用。** 上のコマンドと `CaptureViewportImage` は読み取り専用として扱われるようになり、安全ポリシーが `ReadOnly` のときもモーダルが開いている間も動きます。

**`CaptureViewportImage` は選んだワールドを撮ります。** `TargetNetRole` / `TargetPIEInstance` で選んだワールドのゲームビューポートを撮るようになり、複数の PIE があるときに別のインスタンスの画面を撮ることはなくなりました。

**`PlayerIndex` の意味はコマンドによって違います。** 既存の入力コマンド（`InjectInputKey` など）は**プレイヤーコントローラー**の番号を取ります。`PressGameViewportUIKey`・`TypeGameViewportText`・`DumpHUDState` は、ゲームインスタンスの**ローカルプレイヤー**の一覧の番号を取ります。どちらかはパラメータの説明に書かれています。

**`DumpGameViewportWidgetTexts` がパスワード欄の平文を返すには、安全設定が要るようになりました。** これまでは `RuntimeWidgetPasswordTextRead` だけで返っていました。これからは、その Capability **と**、`[UAIP.SafetyPolicy]` の `AllowRuntimePasswordFieldRead=True`（起動時に読まれます。起動フラグは `-uaip-policy-allow-runtime-password-field-read=True`）の両方が要ります。Capability だけに頼っていた運用者の呼び出しは、失敗せずに値が伏せられ、`PasswordTextWithheldBySafetyPolicy` の limitation が伏せた欄の数を示します。設定がオンで Capability が無いときの limitation は、これまでどおり `PasswordTextWithheld` です。[Safety & Capabilities](safety.md#runtime-ゲームビューポートの-ui) を参照してください。

**`SnapshotUI` と `DumpSlateTree` のラベル。** ラベルが `None` だったノードは型名になり、リッチテキストは表示内容の近似になり、パスワード欄のラベルはヒント文か型名になります。`DumpSlateTree` の `AccessibleText` も同じ規則に従います。リッチテキストは `SnapshotUI` の既定の対象に入るので、ノード数や Ref の番号の振られ方が変わることがあります。[UAIP.Editor.UIAutomation](#uaipeditoruiautomation) を参照してください。

**`DumpSlateTree` の `MaxDepth` は 29 まで。** それより大きい値は、ほかの範囲外の値と同じく 29 に切り詰められます。30 ではウィンドウのダンプの入れ子が深すぎて書き出せず、それでもコマンドは `Success` と空の成果物を返していました。ツリーを書き出せなかった場合は、空のファイルを保存せずに `ExecutionFailed` で失敗するようになりました。

**`SetComboSelection` と `FillForm` がゲームビューポート内のコンボボックスを選べるようになりました。** プレイセッション中（またはウィジェットコンポーネント内）のコンボボックスは、リストを新しいウィンドウではなく自分が属するウィンドウの中に開くため、どちらのコマンドも「Dropdown did not appear within timeout」で失敗していました。そのリストも見つけるようになりました。エディタ自身の UI のコンボボックスの扱いは変わりません。

**`Toolset.Editor.SlateInspector.SnapshotUI` は入力欄の行を、パスワード欄かどうかによらず伏せます。** [UAIP.Editor.UIAutomation](#uaipeditoruiautomation) を参照してください。

**シナリオは、宣言されていない引数へ渡される機微な値を拒否します**（`PolicyViolation`、`Reason: SensitiveValueToUndeclaredParam`）。[機微な値と伏せる場所](#機微な値と伏せる場所) を参照してください。

---

## UAIP.Core

検索・ヘルスチェック・セッション管理などのシステムレベルコマンド。

| コマンド | 説明 |
|---|---|
| 🆓 `HealthCheck` | プラグイン接続確認 — `Status`・`UAIPVersion`・`EngineVersion`・`BuildConfig` に加え、`ProjectFilePath`（開いている `.uproject` の絶対パス。MCP Bridge が正しいエディタインスタンスへアタッチしているか検証するために使う）・`TransportTimeouts`（トランスポートごとの非同期コマンドタイムアウト秒数。例 `{"HTTP": 120, "WS": 12}`）・`QueueCongestion`（遅延実行キューの混雑度。`None` / `Low` / `High` の 3 段階。正確な待ち件数は他セッションの活動量を推測させるため返しません）・`MinBridgeVersion`（この UAIP が受け入れる MCP Bridge の最低バージョン。Bridge はこの応答から読み取り、これ未満では動作を拒否します）を返す |
| 🆓 `GetSystemInfo` | UE バージョン（Major/Minor/Patch/Changelist）・プロジェクト名・プラットフォーム・ビルド設定・UAIP バージョンを返す |
| 🆓 `QueryCapabilities` | `Capabilities`（セッションの実効セット）・`RegisteredCapabilityCount` / `UngrantedCapabilityCount`（常に返る）・`OperationalConstraints`（9 つのポリシーフラグ）を返す。`IncludeUnavailable: true` を渡すと `RegisteredCapabilities`（ロード済みモジュールが宣言したすべての Capability。各要素が `Name` / `DefaultPolicy` / `IsGranted` を持つため、このセッションが保有していないものも名前で見つけられる。既定で拒否されるものは `DefaultPolicy` が `Denied` の要素）も返る。無償のデモ版では、製品版でだけ使う Capability の要素に `UnavailableReason: "NotInThisEdition"` も付く。その `IsGranted` は常に `false` で、`AllowedCapabilities` に書いても変わらない（[Safety & Capabilities](safety.md#デモ版が提供しない-capability)）。`UnavailableReason` が無い要素は、その理由では塞がれていない。製品版では付かない |
| 🆓 `ListCommands` | フィルタ付きコマンドカタログ（`ProviderPrefix`・`KeywordFilter`・`IncludeUnavailable`・`Stability`。`ResultMode` — `Commands`（既定）または `Providers` を指定するとコマンドではなく Provider の一覧を返す。`Limit` — 返却件数の上限（1〜1000）。`IncludeDescription` — 一覧に各コマンドの説明文を含める） |
| 🆓 `DescribeCommand` | 単一コマンドの完全メタデータ（スキーマ・必要 Capability・可用性） |
| 🆓 `ListPlugins` | インストール済みプラグインと有効/無効状態の一覧（JSON）— ⚠️ **非推奨**：代わりに `UAIP.Runtime.Engine.Plugin.ListPlugins` を使用 |
| 🆓 `EndSession` | セッションを明示的に終了しサーバー側リソースを解放する（成果物は GC 対象になる） |
| 🆓 `ReloadCapabilities` | エディタを再起動せずに `Config/DefaultUAIP.ini` から Capability セットを再読み込みする。`AllowCapabilityReload=True` になるまでは `ListCommands` の既定応答から隠れ、`Available: false`（設定すべき ini キー名を含む `UnavailableDetail: "SafetyPolicyDisabled"`）を返す — [UnavailableDetail](#unavailabledetail--handlerunavailable-の8つの詳細理由) 参照 |
| 🆓 `ListIntegrations` | UAIP が把握しているすべてのオプション統合（実行時に無効・不在になりうるプラグインを必要とする UAIP モジュール、またはその一部）の状態を返す。各エントリは `Name`・`State`（`Pending` / `Loading` / `Loaded` / `CompiledOut` / `PluginDisabled` / `PluginNotInstalled` / `DependencyNotLoaded` / `NotApplicable` / `LoadFailed`。無償のデモ版では、製品版にだけ含まれる統合を示す `NotInThisEdition` も加わる）・`RequiredPlugins`・`MissingPlugins`・`DependsOn`・`CommandMatchers`・平易な文の `Remedy`（そのコマンドの `CommandNotFound` ヒントと同じ文言）を持ち、`State` が `LoadFailed` のときだけ `FailureKind` / `FailureReason` も持つ。`CompiledOut` は、その統合のコードがこのバイナリに組み込まれていないことを示す。ビルド時に統合先のプラグインが有効と判定されなかった、またはエンジン版が統合の対応版より古い場合である。`MissingPlugins` は「有効にすれば直るプラグイン」、つまりビルド時に有効と判定されなかったプラグインの一覧で、理由がエンジン版の場合（`Remedy` に必要な最小エンジン版が書かれる）と `NotInThisEdition` の場合は空になる。統合が必要とするプラグインは常に `RequiredPlugins` で確認できる。エンジンにインストールした Fab 配布版の UAIP からパッケージしたゲームには、これらの統合を含められない。UAIP をプロジェクトの `Plugins` フォルダーに置き、プロジェクトと一緒にコンパイルすれば使える。任意の `State` パラメータで返す `Integrations` 配列をその状態だけに絞り込めるが、`IntegrationCount` / `LoadedCount` / `NotLoadedCount` は絞り込みに関係なく常に全体の数を返す。未知の `State` 値は `InvalidParams` で拒否される。Capability は不要 |
| 🆓 `GetPendingInteractionStatus` | 保留中の対話 1 件の状態 — `State`・`Cause`・`ElapsedSeconds`・`Prompt`・`Reason`・`Result` — を、変化を待たずに報告する。対話（`DrawPCGSpline` などの対話型コマンド）を開始したときと同じ `SessionId` を明示的に指定する必要があり、未知・期限切れ・他セッション所有はすべて同じ `NotFound` として扱われる |
| 🆓 `WaitForPendingInteraction` | 対話が `AwaitingUser` を離れるか、この呼び出し自身の `TimeoutSeconds` 上限（デフォルト 30、範囲 [1, 600]）に達するまでブロックする。タイムアウトしても対話自体には影響せず、人間の応答を待ち続ける。同じ対話を同時に監視できる呼び出しは最大 4 件までだが、2 件目以降には `[UAIP.Transport] AllowConcurrentPassiveWaits` が必要（[設定](config.md) 参照） |
| 🆓 `CancelPendingInteraction` | 呼び出したセッションが開始した対話をキャンセルする（人間の応答は待たない）。既に `Completed` になっている対話はエラーではなく `Success` として扱われる。開始コマンドが宣言した Capability をセッションの現在の Capability セットに対して再チェックし、もう保有していないものは `CapabilityNotAvailable` で、運用者が `DeniedCapabilities` で明示的に拒否しているものは `PolicyViolation` で拒否する |

### 機微な値と伏せる場所

`DescribeCommand` は、UAIP が自身の記録に残さない値を、コマンドごとに示します。

- `SensitiveParams` — パラメータのトップレベルの名前。例: `TypeGameViewportText` の `Text`
- `SensitiveResponseData` — 応答の `Data` の中の位置。`[]` が「配列の全要素」を表すドット区切りのパスで書きます: `PasswordFieldValues`（`DumpGameViewportWidgetTexts` のトップレベルの項目）、`Connections[].RemoteAddress`（`ListNetConnections`）、`Properties[].Value` と `Components[].Properties[].Value`（`DumpReplicatedPropertyValues`）。名前だけのパスはトップレベルの項目なので、入れ子のパスが入る前に書かれた一覧もそのまま同じ意味で読めます

**パスの書き方。** `.` で区切り、各セグメントは空でない項目名と、その後ろの 0 個以上の `[]` です。項目名に `.`・`[`・`]` は使えず、添字の指定（`[0]`）はありません。項目名は大文字小文字を区別せずに照合します。応答に無い項目・`null`・空の配列に至るパスは、そこでは何も伏せず、何も足しません。

**伏せる場所。** コマンドのたびにエディタが出す完了通知です。エディタ自身の通知と、コマンドを記録するコード（監査記録・ログ）がこれを受け取ります。宣言した位置の値は、型にかかわらず（`null`・オブジェクト・配列も）長さも載らない文字列 `"<redacted>"` になります。応答の形がパスの示す形と違うときは、飛ばさずに伏せます。`[]` の位置にある値が配列でも `null` でもないとき、また項目を読む位置にある値がオブジェクトでも `null` でもないとき（例: `A.B` の `A` が文字列や配列）は、その値ごと伏せます。宣言を頼れないときは、トップレベルの項目名を残して `Data` 全体を伏せます。宣言したパスが不正なとき（コマンドの登録時にエディタがエラーをログに出します）と、コマンドを引けないとき（未知の名前、または実行中に登録が解除されたコマンド）です。[シナリオ](scenario.md) で、前のステップの応答から伏せる値（またはそれを含む配列やオブジェクト）を `${...}` のテンプレートで取ったステップは、パラメータと応答の `Data` の全体を伏せて記録されます。その値を受け取った後続のステップも同じです。ステップ自身には元の値が届きます。

**伏せない場所。** 呼び出し元に返す応答（MCP・HTTP・WebSocket・CLI、およびシナリオの結果の各ステップ）と、コマンドが保存する成果物は元の値のままです。その値は、コマンドが求める Capability のもとで呼び出し元自身が求めたものだからです。成果物は、Artifact の自動 GC が消すまでディスクに残ります。

**シナリオで機微な値を渡してよい場所。** `${...}` テンプレートは、前のステップの応答の機微な部分（`SensitiveResponseData` の位置。`SnapshotUI` の `PasswordFieldValues` など）を、後のステップのパラメータへ写せます。ただし、受け取るコマンドが機微な値の行き先として宣言した位置にだけです。宣言されている行き先は次のとおりです。

| コマンド | 行き先 |
|---|---|
| `InputText` | `Text` |
| `FillForm` | `Fields` の各エントリの `Value`（エントリの `WidgetRef` は含みません） |
| `TypeGameViewportText` | `Text` |

これらのコマンドは、行き先で受け取った値を、エラー文・応答・artifact・ログに書きません。`DescribeCommand` は行き先を一覧しないので、この表が一覧です。機微な値をそれ以外の場所へ渡すステップは**実行されず**、`PolicyViolation` と `Result.Reason: SensitiveValueToUndeclaredParam` で失敗します。エラー文は値もテンプレートの式も含まない固定の文で、再試行されません。コマンドを引けないときも同じです。位置は**キーの大文字小文字も含めて**完全一致で比べます。`Text` が宣言されているとき、`text` に入れた機微な値は拒否されます。検査するのは直接の参照だけです。機微な値を持ったステップの応答を参照しただけのステップ（たとえば `InputText` の応答から `WidgetRef` を取る `ClickWidget`）は拒否されません。この検査ができる前に、宣言されていない引数へ機微な値を渡していたシナリオは、これから失敗します。そうする必要があるセッションには、DefaultDenied の Capability `ScenarioSensitiveValueToUndeclaredParam` が要ります（[Safety & Capabilities](safety.md#シナリオ実行) 参照）。

**そのようなステップのエラー文。** 機微な値を受け取ったステップ（全パラメータを伏せて記録されるステップ）は、シナリオの結果の `ErrorMessage` が固定の文に置き換わります。`ErrorCode` は残ります。シナリオ実行のログにも出しません。完了通知でも、全パラメータが伏せられる要求の `ErrorMessage` は同じように置き換えられます。

---

## UAIP.Core.Artifacts

先行するコマンドが生成した artifact の内容を読み戻す。artifact のモデル自体は [Artifacts](artifacts.md) を参照。

| コマンド | 説明 |
|---|---|
| 🆓 `GetArtifact` | `ArtifactId` で指定した artifact の内容を返す（呼び出したセッションが所有するものに限る）。テキスト系（`Json` / `Log` / `Report` / `Bundle`）は 1 回あたり最大 `MaxBytes`（デフォルト・上限とも 65536、下限 4）まで `Content` に入って返る。バイナリ系（`Image` / `Trace`）は `Content` を返さずメタデータと `TotalBytes` のみで、ファイルとして開くことを想定している。続きを読むには前回の `NextOffset` を `Offset` に渡す — 返る範囲は必ず文字境界で終わるため、ページングが文字を分割したりテキストを重複・欠落させたりすることはない。末尾を越えた `Offset` は `ReturnedBytes` 0 で成功し、これがページ読み取りの終端判定になる。`MetaIsPartial` が true の場合はストアのインデックスが失われた後にディスク上のファイルからメタデータを再構築したことを意味し、`Sequence` / `Description` は無く `CreatedAt` はファイルの更新時刻になる。`CommandNameVerified` が false の場合、artifact のファイル名が持つコマンド名を裏付けるものが無いことを示す。他セッションの artifact は `NotFound` となり、存在しない場合と区別できない。`ArtifactContentRead` が必要 |

---

## UAIP.Editor.Workspace

エディタライフサイクル・タブ管理・グラフレイアウト・シェーダーコンパイル・Live Coding。

| コマンド | 説明 |
|---|---|
| 🆓 `FocusEditorTab` | 指定アセットのエディタタブを前面に出す。対象は `AssetPath` で指定し、Slate レイアウトのタブ識別子では**ない** — `DumpEditorState` が返す `ActiveTabId`（`"Viewport"` / `"Inspector"` など）はここでは拒否される。レイアウト識別子でタブを指定したい場合は `CaptureEditorTabImage` の `TabId` を使う。任意の `GraphName` を指定すると、そのサブグラフのタブも前面に出す。対象は「アセットの種類が Blueprint かどうか」ではなく「**現在開いているエディタが Blueprint グラフのナビゲーションに対応しているか**」で決まり、素の Blueprint に限らず AnimBlueprint・WidgetBlueprint（UMG）・GameplayAbility Blueprint・ControlRig なども含まれる。空文字列は指定しなかった場合と同じ扱い。`Result` の契約と、エラーコード 2 件の破壊的変更は表の下の注記を参照 |
| 🆓 `CloseEditorTab` | 指定アセットのエディタタブを閉じる。`FocusEditorTab` と同じく `AssetPath` で指定する |
| 🆓 `ListSpawnableTabs` | 開けるエディタタブの候補を一覧で返す。各行の `TabId` / `OwnerMajorTabId` / `OwnerInstanceId` はそのまま `OpenTabById` / `CloseTabById` の `TabId` / `OwnerTabId` / `OwnerInstanceId` として渡せる。表示名・ツールチップ・そのタブが既に開いているかどうかも含む。開いているかどうかはその行が示す所属先を基準に判定され、`MajorTabLocal` の行はそのウィンドウ内だけを、`Global` の行はエディタ全体を対象とする（エディタ全体に登録されたタブはレイアウト次第でどのタブウェルにも置かれるが、`"Global"` からは常に到達できるため）。網羅的な一覧ではなく、応答は常に `EnumerationScope: "MenuVisible"` を返す — 一覧に無い `TabId` でも開ける場合があり（生成メニューから外れているだけの場合がある）、逆に設定で恒久的に拒否されている場合もあるため、「一覧に無い」は「未列挙」であって「存在しない」ではない。読み取り専用だが、表示名・ツールチップの取得が第三者のデリゲートを評価しうるため `EditorTabSpawn` を要求する |
| 🆓 `OpenTabById` | Slate レイアウトのタブ識別子（`TabId`。`FocusEditorTab` の `AssetPath` とは別の識別子空間）を指定してエディタタブを開く。`FocusEditorTab` やメニュー操作代行では届かないタブ — ToolMenus に一度も登録されていないレガシーメニュー経由のタブや、所属ウィンドウが前面にないタブ — にも到達できる。`OwnerTabId` に `"Global"` を指定するとエディタ全体に登録されたタブ（Output Log 等）を、major tab 自身の `TabId`（複数該当する場合は `OwnerInstanceId` で絞り込み）を指定するとその内部のパネルを対象にできる。所属先のウィンドウがまだ開いていなければ先に開く。既に開いている所属先はそのまま使うため、`ListSpawnableTabs` が返した行はそのまま渡せる（所属先に対するスポナー登録と許可の判定は、この呼び出しが所属先を開く必要がある場合にだけ適用される）。応答には実際に開いたタブの `InstanceId`（この応答からしか得られない値）、`WasAlreadyOpen`、`OwnerOpenedByThisCall` が含まれ、後始末で何を閉じるべきかを判断できる（閉じる順序は対象タブ→所属先）。失敗時はこの呼び出しが開いたものを取り除く。候補の発見には `ListSpawnableTabs` を使う（`EditorTabSpawn` 必要） |
| 🆓 `CloseTabById` | `OpenTabById` と同じ指定（`TabId` / `OwnerTabId` / `InstanceId` / `OwnerInstanceId`）でタブを閉じる。アセットパスでは指定できない。`OpenTabById` と異なり `OwnerTabId` が開いていなくても新たに開くことはせず、その場合は `NotFound` になる。許可判定も行わない — 実行時にポリシーが変わったせいで後始末そのものが失敗する方が悪いという判断による。そのため対象は「このセッションが開いたタブ」に限らず、人間が手動で開いたものも含め、いま生きている任意のタブになる（`EditorTabSpawn` 必要） |
| 🆓 `NormalizeEditorLayout` | メイングラフタブをフォーカスし、一時パネルを非表示にする。`OpenAsset` と同じエディタ状態の成果物を保存し、非推奨の `ActiveTabId` フィールドも含む — 代わりに `ActiveAssetPath` を読むこと（[`OpenAsset`](#uaipeditorassets) を参照） |
| 🆓 `SetEditorWindowState` | エディタのメインウィンドウを最小化する、または最小化から復元し、ウィンドウが指定の状態に落ち着いてから返る。必須パラメータは `State`（`Restored` または `Minimized`。それ以外は `InvalidParams`）。`Restored` は最小化を解く。Windows は前面のアプリにしかウィンドウを前に出させないため、ユーザーが別のアプリで作業しているときは、エディタは**そのアプリの後ろで**元に戻る。キーボードフォーカスはそのアプリに残り、エディタのタスクバーのボタンが点滅することがある。後ろにあってもキャプチャは撮れる。最小化の前に最大化されていたウィンドウは、`Restored` が最大化を解かないので、最大化の状態に戻る。対象はメインウィンドウだけ。`EditorWindowStateControl`（DefaultDenied。表の下の注を参照）が必要 |
| 🆓 `SetGraphZoom` | グラフビューポートのズーム倍率を設定 |
| 🆓 `FrameGraphAll` | グラフビューポートを全ノードが収まるようにズーム |
| 🆓 `FrameGraphSelection` | グラフビューポートを選択ノードが収まるようにズーム |
| 🆓 `SetGraphSelection` | ID リストでグラフノードを選択状態にする |
| 🆓 `ShutdownEditor` | UE Editor をシャットダウンする（任意でパッケージ保存）。進行中の `RestartEditor` の試行があれば取り消すので、終了が再起動に化けることはない |
| 🆓 `RestartEditor` | UE Editor を再起動する（任意でパッケージ保存）。`Success` は要求を**受け付けた**ことを表し、再起動が済んだことではない。結果は `GetRestartStatus` で確認でき、MCP Bridge 経由なら Bridge が自動で待つ。表の下の注記を参照 |
| 🆓 `GetRestartStatus` | `RestartEditor` の試行の状態（`Scheduled` / `CloseRetrying` / `Declined` / `ExitStarted`）を返す。読み取り専用で `EditorLifecycle` が必要 |
| 🆓 `SaveAllPackages` | 変更済みパッケージをすべて保存（任意でマップを含む） |
| 🆓 `Undo` | 直前の Editor 操作を取り消す |
| 🆓 `Redo` | 取り消した操作をやり直す |
| 🆓 `GetUndoHistory` | 取り消し履歴を読む（何も実行しない）。戻せる件数・やり直せる件数と操作名を返す |
| 🆓 `GetLastCrashReport` | 最新のクラッシュレポートを取得 |
| `WaitForShaderCompilation` | シェーダーコンパイル完了まで待機 |
| `RecompileGlobalShaders` | 全グローバルシェーダーを強制再コンパイルし完了を待つ |
| `CompileLiveCoding` | Live Coding 再コンパイルをトリガー |
| `GetLiveCodingStatus` | 現在の Live Coding ステータスを取得 |
| `EnableLiveCodingForSession` | セッションに対して Live Coding を有効化 |

> **`SetEditorWindowState` — 結果と拒否。** `Result` は `PreviousState`・`State`（どちらも `Normal` / `Minimized` / `Maximized`。待機中にウィンドウが破棄された場合は `NoWindow`）・`Changed`（bool）・`Size`（画面ピクセルの `Width` / `Height`）を返し、同じ内容を JSON アーティファクトにも保存する。すでに指定の状態にあるときは、待たずに `Changed: false` ですぐ返る。そうでなければ最大 2 秒、ウィンドウが落ち着くのを待つ。落ち着かない、または待つ間にウィンドウが破棄された場合は、観測した状態を添えて `ExecutionFailed` を返す。待つ間にウィンドウを変更するため、このコマンドは実行中のコマンドとして数えられ、最大 2 秒のあいだ transport のスロットを占有する。
>
> 操作の対象が無いときは、[キャプチャのコマンド](#キャプチャが断られるとき)と同じ語彙の `Reason` を付けて拒否される。`Headless`・`BlockedByModal`・`Hidden` は `NotAllowed`、`NoWindow`（メインウィンドウがまだ無い）は `PreconditionFailed`。`Minimized` のウィンドウや、Slate が今は描けないウィンドウ（`DebuggerPaused`・`NotInVisibleTree`・`NotRenderable`）は、ウィンドウを変更することがこのコマンドの目的なので、**拒否されない**。
>
> **`Restored` の後の大きさの同期。** 復元の後（すでに `Restored` の状態で `Restored` を求められたときも。その場合は `Changed: false` のまま）、Slate が持つウィンドウの大きさを OS が報告する大きさに同期する。直らないときは `NotAllowed` と `Reason: WindowSizeMismatch` を返す。結果には `PreviousState`・`State`・`Changed`・`Size`（同期の後の値）に加えて `OsClientSize` と `SlateSize`（どちらも `Width` / `Height`）が入り、同じ内容が JSON アーティファクトにも保存される。ウィンドウを最小化して復元し直すか、ユーザーに大きさを手で変えてもらう。`Minimized` を求めたときは大きさを比べない。
>
> `EditorWindowStateControl` は **DefaultDenied** で、デモ版でも登録される（デモ版での「使えない」の印は付かない）。無いと `CapabilityNotAvailable`、`ReadOnly` のときは `PolicyViolation` で、他の書き込みコマンドと同様に拒否される。許可するには `Config/DefaultUAIP.ini` の `[UAIP.SafetyPolicy]` に `+AllowedCapabilities=EditorWindowStateControl` を足す（デモ版の `DefaultUAIP.ini` には、この行がコメントとして入っている）。

> **`RestartEditor` と `GetRestartStatus` — `Success` の意味と、結果の確かめ方。** どちらも `EditorLifecycle` が必要です。`RestartEditor` の引数は省略可能な `SaveAll` だけです。省略すると、`DisableSave` が有効でない限り未保存の変更を先に保存し、有効なときは保存しません。`DisableSave` のときに `SaveAll: true` を明示すると `PolicyViolation` で拒否します。`Success` は要求を**受け付けた**ことを表します。`Data` には `AttemptId`・`State`（`Scheduled`）・`RestartScheduled: true`・`CloseDeadlineSeconds`・`ProcessId`（要求を受け付けたエディタのプロセス ID）が入ります。
>
> - **MCP Bridge 経由**では、受け付けた時点では応答を返しません。Bridge が結果が出るまで待ち、その間も AI クライアントへ進捗を送り続け、新しいエディタにつながったとき・再起動が見送られたとき（エディタが返した理由と対処をそのままエラーとして返す）・上限時間内に結果を確認できなかったときに応答します。待ちの上限は 2 段あります。エディタが閉じるまでは、エディタが示した期限に約 30 秒を足した時間（終了処理が始まったら、そこからさらに最大 60 秒）。閉じてから先は、Bridge のエディタ起動待ち（既定 120 秒）です。Bridge が「結果を確認できなかった」と返したときは、`GetRestartStatus` と `uaip_get_editor_status` で今の状態を確かめてください。
> - **それ以外の経路**（HTTP など）では、`Success` は受付だけを意味します。`AttemptId` を指定して `GetRestartStatus` を呼びます。省略すると最新の試行になります。答えるのは、要求を受け付けたエディタがまだ動いている間だけです。再起動した後のエディタは以前の試行を持たず、存在しない `AttemptId`、または保持の範囲（直近 8 件）から外れた `AttemptId` は `NotFound` になります。`NotFound` を含むすべての `GetRestartStatus` の応答に `ProcessId` が入るので、呼び出し側は、照会したエディタと後継のエディタを見分けられます。
> - **`GetRestartStatus` の `Data`**: `AttemptId`・`State`・`RequestedAt`・`ElapsedSeconds`・`CloseDeadlineSeconds`・`ProcessId`。`State` は `Scheduled`、`CloseRetrying`（保存や読み込みで忙しく、閉じるのを再試行中）、`Declined`、`ExitStarted` のいずれかです。`Declined` の試行には、さらに `DeclineReason`・`DeclineDetail`・`Remedy`・`OutcomeErrorCode`（`ExecutionFailed`）・`OutcomeErrorMessage`・`RestoredDirtyPackageCount`・`LostDirtyPackageCount` が入ります。
> - **受付前に断られる場合（保存も破棄もせず、何も変えない）**: ライティングビルド（`LightingBuildRunning`）・Interchange のインポート（`InterchangeActive`）・メインウィンドウの作り直し（`MainFrameRecreating`）の最中、またはモーダルダイアログが開いている間（`ModalWindowOpen`。人が操作する通常起動のときだけで、Bridge が起動する無人のエディタは対象外）は `PreconditionFailed` です。`Data` に `DeclineReason` と `Remedy` が入り、メッセージの末尾にも対処が付きます。エディタが既に終了処理に入っていれば `NotAllowed`。別の試行が進行中なら `Conflict`（`Data.AttemptId` が進行中の試行を示します。上の条件より先に判定します）。保存を指定して一部のパッケージが保存できなかったときは `ExecutionFailed`（`Data.FailedPackages` に一覧）で、再起動しません。
> - **受付後に見送られる場合**: エディタはログに警告を出し、再起動のために変えた設定を元に戻し、破棄しかけた未保存の変更を未保存の状態に戻します（件数は `RestoredDirtyPackageCount` / `LostDirtyPackageCount`）。`DeclineReason` は `LightingBuildRunning`・`InterchangeActive`・`CloseRequestDeclined`・`CloseTimedOut`・`SupersededByShutdown` のいずれかです。エディタはそのまま動き続けます。
> - **閉じる期限**: 受付から `CloseDeadlineSeconds`（既定 60 秒）以内に閉じられないと、試行は `CloseTimedOut` で見送られます。人が操作する通常起動では、モーダルダイアログが開いている間は見送りません（再起動そのものは保存確認を出さないので、そのダイアログは他の処理が開いたものです）。`DefaultUAIP.ini` の `[UAIP.EditorRestart]` の `CloseDeadlineSeconds`（10〜600。[Configuration](config.md#uaipeditorrestart--restarteditor-の閉じる期限) を参照）で変更できます。重い保存やシェーダーのコンパイルの直後に再起動することが多い場合は延ばしてください。
> - **試行の途中での終了**: `ShutdownEditor`、または `QuitGame` が結果としてエディタ自体の終了を要求した場合は、試行を取り消し、新しいエディタを起動せずに終了します。安全ポリシーに拒否された（`PolicyViolation`）`ShutdownEditor` は何も取り消しません。エディタが終了する前に照会すると、その試行は `SupersededByShutdown` の `Declined` になっています。人がウィンドウを閉じた場合や、UAIP 以外の経路での終了は、試行の期間中なら再起動になります。
> - **古い組み合わせ**: 古い MCP Bridge は今までどおり受付の時点で応答を返し、古いエディタは `AttemptId` を返しません。新しい Bridge は今までどおりに振る舞います。どちらの場合も、受付後に見送られた再起動は、新しいエディタの `GetRestartStatus` でしか分かりません。

> **`FocusEditorTab` の `GraphName` — 応答の契約。** `GraphName` を非空の文字列で指定した呼び出しに限り、`Result` に 4 つのフィールドが載る: `WindowFocusRequested`（bool — エディタウィンドウを前面化する**要求を行った**ことの記録。OS が実際に最前面へ持って行ったことまでは保証しない）、`GraphNameRequested`（bool）、`GraphNameApplied`（bool）、`Reason`（`Applied` / `BlueprintEditorInterfaceUnavailable` / `OpenFailed` の 3 値だけを取る閉じた列挙）。成否判定には `Success` だけでなく `GraphNameApplied` と `Reason` を読むこと — `BlueprintEditorInterfaceUnavailable` の場合も `Success: true` が返る。これは開いているエディタに Blueprint グラフのナビゲーション手段がそもそも存在しない（例: `RigVM.UseNewEditor` を有効にした ControlRig エディタ）という構造的な状態であり、同じ指定で呼び直しても変わらないため。`GraphName` を省略または空文字列にした呼び出しでは、この 4 フィールドはいずれも設定されない — 呼び出し側は「`Result` が無い」場合と「`Result.GraphNameRequested` が `false`」の場合の両方を扱う必要がある。グラフ移動が適用されると、エディタの現在の UI 選択状態がクリアされ、Widget Blueprint を Designer モードで開いている場合は先に Graph モードへ切り替わる（グラフを表示するために必要）。この 2 つはいずれもグラフを開く処理より前に起きるため、その後グラフを開く処理自体が `OpenFailed` で失敗した場合でも、既に起きていることがある。
>
> ⚠️ **破壊的変更** — `GraphName` のエラーコードのうち 2 件が、`ExecutionFailed` から再試行対象外のコードへ変わった。シナリオの `RetryCount` は `ExecutionFailed` と `PreconditionFailed` だけを再試行対象にしており、この 2 件はいずれも同じ指定で再試行しても成功しようがないため: アセットに存在しないグラフ名を指定した場合は `NotFound`（従来は `ExecutionFailed`）、Blueprint 系ではないアセットに `GraphName` を指定した場合は `InvalidParams`（従来は `ExecutionFailed`）を返す。`OpenFailed`（ナビゲーション手段は取得できたが実際にグラフを開く処理自体が失敗した場合）は変更なく `ExecutionFailed` のままで、こちらは再試行に意味がある。
>
> **`GraphName` が同一アセット内の複数のグラフに一致する場合、いずれか 1 つが開かれるが、どれが選ばれるかはこの契約の対象外**であり、特定の 1 つが選ばれ続けることを前提にした使い方はしないこと。呼び出し側がどちらを意図していたかを読み取る仕組みではなく、返り値も変わらない — `GraphNameApplied` と `Reason` はグラフを開けたかどうかを表すだけで、どのグラフを開いたかは表さない。実際に名前が重なる状況はまれ: 同じ階層に並ぶグラフ（関数・マクロ・イベントグラフ・インターフェース実装のグラフ）同士は、そもそも同じ名前で共存させる手段がエディタに無い。名前が重なりうるのは**折りたたんだグラフ**が絡む場合だけで、折りたたんだグラフの中にあるグラフが外側のグラフと名前が重なることがある。

### Toolset ブリッジ — LiveCoding（1 件）🧩

`LiveCodingToolset`（UE 5.8+）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.LiveCoding.*`。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.LiveCoding.CompileLiveCoding` | Live Coding 再コンパイルをトリガー（`LiveCodingControl` 必要） |

---

## UAIP.Editor.Engine.Log

エディタ Output Log のログエントリ取得。ログ**詳細レベル**の取得・設定は [`UAIP.Runtime.Engine.Log`](#uaipruntimeenginelog) にあります。

| コマンド | 説明 |
|---|---|
| 🆓 `GetLogEntries` | エディタ Output Log から最近のログエントリを取得（パターンフィルタ対応）。Capability は不要ですが、安全設定 `AllowLogDump`（`bAllowLogDump`）が有効なときだけ動きます（`DumpOutputLog` と同じ設定）。既定では無効なので、既定の構成では `PolicyViolation` で断られ、設定を有効にするよう案内されます。今の状態は `uaip_query_capabilities` の `IsLogDumpAllowed` で確かめられます。以前は設定によらず読めました |

### Toolset ブリッジ — Logs（4 件）🧩

`LogsToolset`（UE 5.8+、EditorToolset プラグイン）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.Toolset.Logs.*`。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.Toolset.Logs.GetLogEntries` | エディタ Output Log から最近のログエントリを取得。ネイティブ版と同じ安全設定 `AllowLogDump`（`bAllowLogDump`）が必要で、無効の間は `PolicyViolation` で断られる |
| `Toolset.Editor.Toolset.Logs.GetLogCategories` | 登録済みログカテゴリ名の一覧 |
| `Toolset.Editor.Toolset.Logs.GetVerbosity` | ログカテゴリの詳細レベルを取得 |
| `Toolset.Editor.Toolset.Logs.SetVerbosity` | ログカテゴリの詳細レベルを設定（`LogVerbosityEdit` 必要） |

### Toolset ブリッジ — CVar（1 件）🧩

EditorToolset プラグイン（UE 5.8+）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.Toolset.EngineManagement.*`。

> `SearchCVars`（と `World` の別名）は `Name` を任意のままにし、既定値 `""`（全 CVar）をスキーマに出します。Toolset が必須とする `name` は、ブリッジが常に送ります。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.Toolset.EngineManagement.SearchCVars` | CVar を名前パターンで検索（センシティブパターンを除外、`CVarInspect` 必要） |

---

## UAIP.Editor.Engine.Plugin 🧩

プラグインの状態・ディスクリプタの観測と変更。エンジンおよびマーケットプレイスのプラグインは常に読み取り専用です。変更コマンドはエディタ再起動後に反映されます。

| コマンド | 説明 |
|---|---|
| 🆓 `GetPluginDescriptor` | プラグインの `.uplugin` ファイル全体を JSON で返す |
| 🆓 `GetPluginDependents` | 指定プラグインに依存する他のプラグイン一覧を返す |
| 🆓 `GetPluginTemplateDescriptions` | 利用可能なプラグインテンプレートの一覧を返す |
| 🆓 `IsPluginCreationAllowed` | 現在の環境でプラグイン作成が許可されているか確認 |
| 🆓 `IsPluginModificationAllowed` | 指定プラグインの変更が許可されているか確認 |
| `SetPluginEnabled` | プラグインを有効化または無効化する（`PluginEnableToggle` 必要；`RestartRequired: true` を返す） |
| `UpdatePluginDescriptor` | プラグインの `.uplugin` 内の選択フィールドを上書き（`PluginDescriptorEdit` 必要） |
| `AddPluginDependency` | プラグインの `.uplugin` に依存エントリを追加（`PluginDependencyEdit` 必要） |
| `RemovePluginDependency` | プラグインの `.uplugin` から依存エントリを削除（`PluginDependencyEdit` 必要） |

### Toolset ブリッジ — Plugin（15 件）🧩

`PluginToolset`（UE 5.8+）経由のブリッジコマンド。プロバイダ：`Toolset.Plugin.*`。

> **引数は Plugin Toolset が宣言する形に揃えています。**
>
> - ⚠️ **`UpdatePluginDescriptor` はデスクリプターの全体を取ります。** `Descriptor` は次の 14 メンバーだけを持つオブジェクトで、すべて必須、ほかのメンバーは取りません: `FriendlyName`・`Description`・`Category`・`VersionName`・`CreatedBy`・`CreatedByURL`・`DocsURL`・`MarketplaceURL`・`SupportURL`（文字列）、`Version`（整数）、`bCanContainContent`・`bIsBetaVersion`・`bIsExperimentalVersion`・`bIsSealed`（真偽値）。Toolset は 14 メンバーすべてを書き込んで `.uplugin` を保存するため、省いたメンバーは空で保存されてしまいます。そのため一部だけの `Descriptor` は `InvalidParams` で断ります。以前の呼び出しは、Toolset 側で必ず失敗していました。
> - **`AddPluginDependency`: `bOptional` の既定値は `false`、`bEnabled` の既定値は `true`** で、ネイティブコマンドと同じです。どちらも常に送ります。

| コマンド | 説明 |
|---|---|
| `Toolset.Plugin.ListEnabledPlugins` | 現在有効なプラグインの一覧 |
| `Toolset.Plugin.ListDiscoveredPlugins` | 検出済みプラグイン（有効・無効を問わず）の一覧 |
| `Toolset.Plugin.GetPluginInfo` | プラグインの基本情報（名前・バージョン・有効状態）を取得 |
| `Toolset.Plugin.IsEnabled` | プラグインが現在有効か確認 |
| `Toolset.Plugin.GetPluginDependencies` | プラグインが依存するプラグイン一覧を返す |
| `Toolset.Plugin.GetPluginForAsset` | 指定アセットを提供するプラグインを返す |
| `Toolset.Plugin.GetPluginDescriptor` | プラグインの `.uplugin` 全体を JSON で返す |
| `Toolset.Plugin.GetPluginDependents` | 指定プラグインに依存する他のプラグイン一覧 |
| `Toolset.Plugin.GetPluginTemplateDescriptions` | 利用可能なプラグインテンプレートの一覧 |
| `Toolset.Plugin.IsPluginCreationAllowed` | プラグイン作成が許可されているか確認 |
| `Toolset.Plugin.IsPluginModificationAllowed` | 指定プラグインの変更が許可されているか確認 |
| `Toolset.Plugin.SetPluginEnabled` | プラグインを有効化または無効化（`PluginEnableToggle` 必要） |
| `Toolset.Plugin.UpdatePluginDescriptor` | `.uplugin` の選択フィールドを上書き（`PluginDescriptorEdit` 必要） |
| `Toolset.Plugin.AddPluginDependency` | `.uplugin` に依存エントリを追加（`PluginDependencyEdit` 必要） |
| `Toolset.Plugin.RemovePluginDependency` | `.uplugin` から依存エントリを削除（`PluginDependencyEdit` 必要） |

---

## UAIP.Editor.Engine.ConfigSettings

`ISettingsModule` 経由でプロジェクト設定やエディタ設定を管理するコマンド群。`ContainerName / CategoryName / SectionName` の 3 階層パスでセクションを指定します。書き込み操作はプロジェクトの `Config/` ディレクトリ配下のファイルのみ許可されます（エンジン ini ファイルは `PolicyViolation` で拒否）。

| コマンド | 説明 |
|---|---|
| 🆓 `ListSettingsContainers` | 登録済みの設定コンテナ（`Project`、`Editor` など）を一覧表示。Capability 不要 |
| 🆓 `ListSettingsCategories` | コンテナ内の設定カテゴリを一覧表示。Capability 不要 |
| 🆓 `ListSettingsSections` | カテゴリ内の設定セクションを一覧表示。Capability 不要 |
| 🆓 `GetSettingsSchema` | セクションの編集可能プロパティ（名前・型・説明・デフォルト値・編集条件）を JSON アーティファクトで返す（`EditorInspect` 必要） シークレットプロパティの既定値は `***` と `IsMasked: true` になる（以前は平文）。`IncludeSecretValues` を取る — [シークレット値の読み取り](#reading-secret-values)を参照 |
| 🆓 `GetSettingsValues` | セクションの現在のプロパティ値を JSON アーティファクトで返す。シークレットフィールド（名前がシークレットパターンに一致・シークレットメタデータあり・ファイルパス型）は `***` でマスク（`EditorInspect` 必要） 名前だけでシークレットと分かるプロパティもマスクされる。`IncludeSecretValues` を取る — [シークレット値の読み取り](#reading-secret-values)を参照 |
| `SetSettingsValues` | `Properties` マップを `ImportText` 経由で設定オブジェクトにマージ。`DryRun`（検証のみ・適用なし）に対応。`ConfigSettingsEdit` 必要。PIE 中は実行不可。値はエンジンのテキスト形式のみを受け取るため、参照・コンテナ・組み込みカタログ外の構造体は **どの Capability を付与しても拒否されます** — これらは同じ設定オブジェクトへ届き `ValueJson` を受け取る `SetProjectSetting` で書いてください。途中までしか解釈できない値は、断片が適用されるのではなく `InvalidParams` で拒否されるようになりました 渡した `Properties` は、シークレットかどうかに関わらず監査ログ・完了通知・コマンドの記録で伏せられ、失敗理由の文も伏せられる。呼び出し側への応答は変わらない。拒否の文は送った値を引用せず、プロパティ・型やフラグ・足りない Capability の名前だけを示す。`DryRun` では、シークレットプロパティの変更前・変更後の値が `***` と `IsMasked: true` になる（以前は `null`）。`IncludeSecretValues` は `DryRun` の平文を返す。`DryRun` なしの応答には値が含まれないので何もしない — [シークレット値の読み取り](#reading-secret-values)を参照。プロパティが宣言する `ClampMin` / `ClampMax` の外の数値は、詳細パネルと同じく `DryRun` の有無にかかわらず `InvalidParams` で拒否される。文はプロパティ名と範囲を示し、値は含まない |
| `SaveSettings` | `ISettingsSection::Save()` 経由で設定を ini ファイルに書き出す。`ConfigSettingsSave` 必要。PIE 中および `bDisableSave` 設定時は実行不可 |
| `ResetSettingsToDefaults` | 設定オブジェクトをクラスデフォルトに戻して保存。`ConfigSettingsReset` 必要。PIE 中は実行不可 シークレット値は `DryRun` のプレビューでも、実行時の元の値のバックアップ（アーティファクト）でも `***` になる。`IncludeSecretValues` を取る — [シークレット値の読み取り](#reading-secret-values)を参照。既定値へ戻せないセクション（`ListSettingsSections` で `CanResetDefaults: false`）は `DryRun` の有無にかかわらず `NotAllowed` で拒否されるので、実行で拒否されるリセットをプレビューが表示することはない |

### Toolset ブリッジ — ConfigSettings（8 コマンド）🧩

`ConfigSettingsToolset` プラグイン（UE 5.8+）経由のブリッジコマンド。プロバイダ: `Toolset.ConfigSettings.*`。

| コマンド | 説明 |
|---|---|
| `Toolset.ConfigSettings.ListContainers` | 登録済みの設定コンテナを一覧表示 |
| `Toolset.ConfigSettings.ListCategories` | コンテナ内の設定カテゴリを一覧表示 |
| `Toolset.ConfigSettings.ListSections` | カテゴリ内の設定セクションを一覧表示 |
| `Toolset.ConfigSettings.GetSectionSchema` | セクションのプロパティスキーマを取得 |
| `Toolset.ConfigSettings.GetSectionPropertyValues` | 指定したプロパティの現在値を取得。`PropertyNames`（1 つ以上のプロパティ名の配列）が必須。`Result` は JSON 文字列で、シークレットプロパティは `***`。`IncludeSecretValues` を取る — [シークレット値の読み取り](#reading-secret-values)と[型どおりの値とマスクされた結果](#toolset-bridges--configsettings-typed-values-and-masked-results)を参照 |
| `Toolset.ConfigSettings.SetSectionProperties` | セクションのプロパティ値を設定して永続化（`ConfigSettingsEdit` 必要）。`Properties` は「プロパティ名 → プロパティの型どおりの JSON 値」のマップで、プロパティがそのまま受け入れられない値は書き込む前に拒否される。書き込んだ値は監査ログとコマンドの記録で伏せられる — [型どおりの値とマスクされた結果](#toolset-bridges--configsettings-typed-values-and-masked-results)を参照 |
| `Toolset.ConfigSettings.SaveSection` | 現在のメモリ上の設定をセクションの ini ファイルに書き出す（`ConfigSettingsSave` 必要） |
| `Toolset.ConfigSettings.ResetSectionToDefaults` | セクションの全プロパティ値をコンパイル済みデフォルトにリセット（`ConfigSettingsReset` 必要） |

<a id="toolset-bridges--configsettings-typed-values-and-masked-results"></a>
### Toolset ブリッジ — ConfigSettings：型どおりの値とマスクされた結果

**`SetSectionProperties`** は、各値をプロパティの JSON 型どおりに受け取ります（数値は数値、真偽値は `true` / `false`、文字列は文字列、配列は配列、構造体はオブジェクト）。UAIP は Toolset を呼ぶ前に、すべてのプロパティ名と値を設定クラスと突き合わせます。Toolset が別の値として保存してしまう値は `InvalidParams` で拒否され、何も書かれません。拒否の文にはプロパティ名と求める形が入り、送った値は入りません。構造体・配列・Map・参照を含むプロパティに書くには `SetSettingsValues` と同じ Capability が必要で、この経路だけが緩い入口にはなりません（不足時は同じエラーになります）。

| プロパティの型 | 受け入れる値 |
|---|---|
| 真偽値 | `true` / `false` |
| 列挙 | 列挙子の名前の文字列、または整数値の数値 |
| 小数 | 有限の数値（`float` は `float` の範囲内） |
| 整数 | 小数部の無い有限の数値（絶対値 2^53 以下）。`"42"` のような文字列は拒否 |
| `FString` | 文字列 |
| `FName` | 空白と `"` `'` `(` `)` `,` `=` を含まない文字列 |
| `FText` | 文字列。ただし `NSLOCTEXT(` / `LOCTEXT(` / `INVTEXT(` / `LOCTABLE(` / `LOCGEN_` で始まるものは拒否 |
| `FLinearColor` | `R` / `G` / `B` / `A` を全部持ち、それ以外を持たないオブジェクト |
| `FGuid` | ハイフン区切りの GUID 文字列 |
| オブジェクト・クラス参照、ソフト参照、ソフトオブジェクトパス | `/` で始まる `/Package/Path.ObjectName` 形式の文字列。空・`None`・`null` は拒否 |
| その他の構造体 | 1 つ以上のメンバーを持つオブジェクト。各メンバーは同じ規則 |
| `TArray` / `TSet` | `null` の要素を含まない配列。各要素は同じ規則 |

次の型のプロパティは、値によらず拒否されます（このコマンドでは書けません）: `TMap`・`FColor`・固定長配列・`FTransform`・`FTopLevelAssetPath`・独自の文字列表現を持つ構造体（GameplayTag など）・Instanced な参照・弱い参照／遅延参照／インターフェース参照・optional・delegate・field path。これらは `UAIP.Editor.Engine.ConfigSettings.SetSettingsValues` で書いてください。`Properties` は 1 つ以上のプロパティ名を指定する必要があり、コンテナ・カテゴリ・セクション・プロパティの名前が 1024 文字以上のときも拒否されます。Toolset が書き込みの途中で失敗した場合、または「書けなかった」と答えた場合は、呼び出しが失敗し、一部のプロパティが既に書かれている可能性があるので値を読み直して確かめるよう案内されます。

**`GetSectionPropertyValues`** は `PropertyNames` に挙げた名前だけを読みます。要求していない名前や、セクションに存在しない名前が結果に混ざっていた場合も、安全のため隠されます。応答には `MaskedFields`（隠した名前）と `MaskedFieldCount` が付きます。秘密かどうかを判断できずに隠した名前は `UnverifiedMaskedFields` にも載り、`IncludeSecretValues` でも平文になりません。マスクされた数値や真偽値は文字列の `"***"` になります。読んでいる途中で設定が変わった（設定やコードの再読み込みと重なった）場合は失敗し、呼び直すよう案内されます。Toolset の戻りが UAIP の読めない形のときは、隠せない値を返さないよう失敗にするので、代わりに `UAIP.Editor.Engine.ConfigSettings.GetSettingsValues` で読んでください。存在しないコンテナ・カテゴリ・セクションは、ネイティブの設定コマンドと同じ文の `NotFound` になります。

**Toolset ブリッジコマンドの失敗**は `Toolset.<ツール名> failed: <原因>` の形で返ります。`<ツール名>` は委譲先の Toolset の関数名で、コマンド名の最後の部分と一致しないことがあります（`Toolset.SetSectionProperties failed: ...`、`Toolset.set_anim_mode_gizmo_scale failed: ...`）。原因からは、コマンドが秘密と宣言した入力値と、URL・ID・ファイルシステムのパスの類が取り除かれ、256 文字を超えた分は切り詰められます。ログにも同じ文が出ます。秘密の入力に確実には伏せられない値（1〜3 文字の値、数値）が含まれる場合と、秘密の値を読むコマンドでは、原因を付けずに `Toolset.<ツール名> failed.` だけになります。`SetSectionProperties` は値に数値を含むことが多いため、この形になりがちです（型の誤りは、その前に原因付きで拒否されます）。秘密と宣言されていない入力値（アセットのパスなど）は、原因の文に現れることがあります。


<a id="reading-secret-values"></a>
### シークレット値の読み取り

設定値を返すコマンドは、シークレットの値を `***` に置き換え、同じ場所に `IsMasked: true` を付けます。`IncludeSecretValues` を取るコマンドは平文を返せますが、解禁されるのは次の **3 層すべて** が許したときだけです。

1. **引数** — 呼び出しに `IncludeSecretValues: true` を付ける（真偽値）。
2. **Capability** — セッションに `SecretValueRead`（DefaultDenied）が付いている。付与は再起動なしで反映される。
3. **SafetyPolicy** — `[UAIP.SafetyPolicy]` の `AllowSecretValueRead=True`、または起動引数 `-uaip-policy-allow-secret-value-read`。変更にはエディタの再起動が必要で、今の状態は `uaip_query_capabilities` の `IsSecretValueReadAllowed` で確かめられる。

平文は `Result.SecretFieldValues` に**だけ**入ります。いつもの場所、すべてのアーティファクト、監査ログ、完了通知には `***` が残ります。どれかの層が許さなくてもコマンドは成功し、値は隠れたままで、`Result.SecretValuesWithheldReason` が理由を示します。デモ版には `SecretValueRead` が含まれません。何をシークレットとみなすか（プロパティのパス全体、エンジンのパスワード欄の印、CryptoKeys の固定の一覧）、件数と長さの上限、マスクが及ばない経路は [Safety & Capabilities](safety.md#秘密値の平文での読み取り) にあります。

`IncludeSecretValues` を取るコマンドは、`Toolset.ConfigSettings.GetSectionPropertyValues`、上の ConfigSettings のネイティブ 4 本（`GetSettingsSchema`・`GetSettingsValues`・`DryRun` の `SetSettingsValues`・`ResetSettingsToDefaults`）、`UAIP.Runtime.Engine.Config.GetConfigValue` / `SetConfigValue`、[UAIP.Editor.Property](#uaipeditorproperty) の `Get*` 6 本、`UAIP.Editor.Level.GetActorComponentProperty`、`UAIP.Editor.Blueprint.GetBlueprintComponentProperty` です。`Toolset.ConfigSettings.GetSectionSchema` は値を返さず（型・説明・範囲・enum の名前だけ）、対象に含まれません。

---

## UAIP.Editor.Engine.Toolset 🧩

Toolset ブリッジコマンドを実装する際の調査用コマンド。通常の操作で使うものではありません。`ToolsetRegistry` プラグイン（UE 5.8+）が必要で、無い環境では `Available: false`（`UnavailableDetail: OptionalPluginDisabled`）を返し、`uaip_list_commands` の既定出力にも現れません——その環境で理由を確認するには `uaip_describe_command` で名指しで呼んでください。

| コマンド | 説明 |
|---|---|
| `DumpToolsetParameterSchemas` | `ToolsetRegistry` が現在登録している全 Toolset について、生の JSON Schema（パラメータ名・型・`Required` フラグ）を `Json` アーティファクトとしてダンプする。`{}` で呼ぶと登録済み全 Toolset 分が返る。任意の `ToolsetName` で、`<Module>.<Toolset>` という完全な名前への**大小文字を区別する完全一致**で1件に絞り込める（例: `PCGToolset.PCGToolset`——モジュール名だけでは何にも一致しない）。一致しない名前を渡すと `NotFound` ではなく `Success: true` かつ空配列が返る。Capability 不要、読み取り専用 |

---

## UAIP.Editor.Observation

スクリーンショットとエディタ状態ダンプ（すべて読み取り専用）。

| コマンド | 説明 |
|---|---|
| 🆓 `CaptureActiveWindowImage` | アクティブな最上位ウィンドウのスクリーンショット（PNG Artifact）。エディタがフォアグラウンドである必要はない — アクティブなウィンドウがない場合はメインウィンドウを撮影し、どちらを撮ったかを `Result.CapturedWindow`（`"ActiveWindow"` / `"MainWindow"`）で返す。フォールバックはメインウィンドウにしか届かないため、フローティングのアセットエディタやモーダルダイアログは `CaptureEditorTabImage` を使う。対象が描かれない状態（ウィンドウが最小化・非表示、モーダルが開いている、など）のときは、空の画像を返さずに、`Reason` を付けて `NotAllowed` または `PreconditionFailed` で拒否する（[キャプチャが断られるとき](#キャプチャが断られるとき)） |
| 🆓 `CaptureEditorTabImage` | 指定エディタタブのウィジェット領域のスクリーンショット。Slate レイアウト識別子で指定するため、`DumpEditorState` が返す `ActiveTabId` をそのまま渡せる。エディタが背面でも動作する。⚠️ 撮影前に対象タブを前面へ出すため（背面のタブは描画されておらず空の画像になる）、それを収めた外側のエディタのタブ（たとえばブループリントエディタが手前にあるときのレベルエディタのタブ）ごと前に出る。**ユーザーに見えているタブが切り替わり**、タブが点滅する。エディタの OS ウィンドウは他のアプリの前には出さない。タブを前に出したときは、描かれるのを最長 2 秒待ってから撮る。すでに前にあるタブはすぐ撮る。それでも描かれないときは、文がユーザーにタブを前に出してもらうよう案内する。対象が描かれない状態（ウィンドウが最小化・非表示、モーダルが開いている、など）のときは、空の画像を返さずに、`Reason` を付けて `NotAllowed` または `PreconditionFailed` で拒否する（[キャプチャが断られるとき](#キャプチャが断られるとき)） |
| 🆓 `CaptureGraphViewportImage` | SGraphEditor ビューポートのスクリーンショット。対象が描かれない状態（ウィンドウが最小化・非表示、モーダルが開いている、など）のときは、空の画像を返さずに、`Reason` を付けて `NotAllowed` または `PreconditionFailed` で拒否する（[キャプチャが断られるとき](#キャプチャが断られるとき)） |
| 🆓 `DumpEditorState` | アクティブタブ・開いているアセット・ウィンドウサイズ等（JSON）。あわせてプレイセッションの状態を `IsPIERunning` / `IsPIEPaused` / `IsSimulatingInEditor` の 3 つの真偽値で返す。編集系コマンドの多くはセッション実行中に拒否され、その間に取ったワールドのダンプはエディタワールドではなくプレイワールドを表すため、変更を加える前にここを読む。3 つとも常に存在するので「何も再生されていない」と「報告されていない」を区別できる。`MainWindowSize` は最初の最上位ウィンドウの大きさで、メインフレームとは限らない。メインフレームそのものは `MainWindowState` で読む。`MainWindowState` は `State`（`Normal` / `Minimized` / `Maximized` / `Hidden` / `NoWindow`。一度も表示されていないウィンドウは `Hidden`）・`Size` と `RestoredSize`（どちらも `Width` と `Height` を持つオブジェクト。ウィンドウが無いときは 0）・`CaptureBlocker`（キャプチャが撮れるときは `None`、そうでなければキャプチャが拒否される[`Reason`](#キャプチャが断られるとき)）を持つ。このコマンドは読み取りだけで同期はしないので、キャプチャや `SetEditorWindowState` なら自動で直る食い違いでも、`CaptureBlocker` が `WindowSizeMismatch` になりうる。`MainWindowState` には `SizeCheck`（`NotQueryable` / `Minimized` / `Matched` / `Mismatched`）・`SizeMismatched`（bool または null）・`OsClientSize` と `SlateSize`（どちらも `Width` / `Height`。`SizeCheck` が `Matched` / `Mismatched` 以外のときは null）もある。ルートには `WindowMessageRecording` がある: `RecordingEnabled`・`RecordingActive`・`RecordingStatus`（`Disabled` / `NotRegistered` / `WaitingForMessages` / `Recording`）・`TotalRecordedCount`・`Capacity`（64。優先でないウィンドウが共有するリングの容量）・`PriorityWindowCapacity`（64。優先ウィンドウ 1 つあたり）・`MaxPriorityWindowCount`（8）・`PriorityMessageCount`・`SharedMessageCount`（この 2 つの合計が `RecentMessages` の件数）・`RecentMessages`（古い順。1 件は `Kind`・`WindowHandle`・`IsPriorityWindow`・`SizeType`・`MessageSize`・`MessageSizeMeaning`・`WindowPosFlags`・`ClientStateAtArrival`・`TimeSeconds`・`SequenceNumber`）。Slate の通常のウィンドウ（メインウィンドウ、別ウィンドウになったフローティングタブやアセットエディタ、モーダルダイアログ）のメッセージは優先として扱われ、ウィンドウごとに専用のリングで直近 64 件を保持する（最大 8 ウィンドウ。9 つ目が送ってきたら、最後のメッセージが最も古いウィンドウが記録ごと外れる）。数百件のメッセージを送る通知トーストやメニューは優先ウィンドウではないため、これらを押し出さない。それ以外のウィンドウのメッセージも、共有の 1 つのリング（直近 64 件）に記録される。一覧は合計で最大 576 件になりうる。どちらの記録かは `IsPriorityWindow` で分かる。`MessageSizeMeaning` は `MessageSize` が何の大きさかを示す: `ClientArea`（`WM_SIZE`）・`WholeWindow`（`WM_WINDOWPOSCHANGED`。クライアント領域ではなくウィンドウ全体なので、`ClientArea` とそのまま比べない）・`ProposedWholeWindow`（`WM_NCCALCSIZE`）。メッセージが大きさを持たなかったときは `MessageSize` が null、`WM_SIZE` 以外では `SizeType` が null、OS にウィンドウの状態を問い合わせられなかったときは `ClientStateAtArrival` が null になる。記録の有無は [`RecordWindowMessages`](config.md#uaipruntimeobservation--ウィンドウサイズメッセージの記録と-hud-描画統計) で切り替える |
| 🆓 `DumpSelectionState` | 現在の選択状態（JSON）。`SelectedActors` / `SelectedObjects` は常に返る。`TabId` が開いているグラフエディタタブを指す場合に限り `SelectedNodes`（ノードごとに `NodeId` / `NodeClass` / `NodeTitle` / `Position`）も返る — 解決方法は `CaptureGraphViewportImage` の `TabId` と同じ（Slate タブへの完全一致、続いて開いているアセットの名前への大小文字を区別しない部分一致。`/` を含むコンテンツブラウザ形式のパスは `InvalidParams` で拒否される）。`TabId` がどのタブにも一致しない場合は `SelectedNodes` を空にして成功させるのではなく `NotFound` を返す。`TabId` を省略した場合の挙動は変更なし — `SelectedNodes` は空のままで、アクター/オブジェクトの選択は従来どおり返る |
| 🆓 `DumpOpenTabs` | 開いているアセットエディタタブ一覧（JSON） |
| 🆓 `DumpOutputLog` | バッファリングされた Output Log（テキスト Artifact、行数・フィルタ対応） |
| 🆓 `DumpMessageLog` | Message Log エントリ（カテゴリフィルタ付き JSON Artifact） |
| 🆓 `DumpSlateTree` | Slate ウィジェットツリー（JSON、ルートパスフィルタ対応）。`IncludeTextContent: true` のときの `AccessibleText` には `SnapshotUI` と同じラベルが入る（型名またはリッチテキストの近似。パスワード欄と判定できない欄では、アクセシビリティ文字列ではなくヒント文か型名） |
| 🆓 `InspectMenu` | 指定パス配下のトップバーメニュー構造（ラベル・enabled・checked） |
| 🆓 `InspectContextMenu` | 指定対象のコンテキストメニュー項目（実行はしない） |
| 🆓 `ObserveWidget` | ウィジェットの Visibility / Enabled / Hovered / Focused 状態を時系列サンプリング |
| 🆓 `GetLogCategories` | 登録済みエンジンログカテゴリ名の一覧（任意でサブストリングフィルタ対応） |
| 🆓 `ListGraphNodes` | 指定タブのグラフエディタ内の全ノードを列挙 — `NodeId`（GUID）・`NodeClass`・`NodeTitle`・`Position`。`UEdGraph` ベースのエディタ全般で動作 |
| 🆓 `CaptureViewportImageAnnotated` | ワールド座標ラベル付きビューポート画像のキャプチャ（`ViewportAnnotationCapture` 必要）。ビューポートを持つウィンドウが描かれない状態（たとえば最小化）のときは、古いフレームを返さずに、`Reason` を付けて `NotAllowed` または `PreconditionFailed` で拒否する（[キャプチャが断られるとき](#キャプチャが断られるとき)） |

### キャプチャが断られるとき

`CaptureActiveWindowImage`・`CaptureEditorTabImage`・`CaptureGraphViewportImage`・`CaptureViewportImageAnnotated` は、何かを撮る前に、対象が描かれる状態かを確かめる。描かれない状態なら、撮らずに拒否する（空の画像は返さず、`CaptureViewportImageAnnotated` も古いフレームを返さなくなった）。応答には `Reason` と、直し方を示すエラー文が付く。確認は表の順に行い、最初に満たさなかった条件が `Reason` になる。`DumpEditorState` はメインウィンドウについて同じ語彙を `MainWindowState.CaptureBlocker` で報告し、`SetEditorWindowState` も拒否にこの語彙を使う。

| `Reason` | ErrorCode | 意味 | 対処 |
|---|---|---|---|
| `NoWindow` | `PreconditionFailed` | Slate が未初期化、対象がウィンドウを持たない、またはウィンドウのネイティブウィンドウがまだ無い | ウィンドウが現れるのを待ってから呼び直す。対象が別のタブの後ろに回ったタブの中にある場合（判定が拾えないことがある）は、待っても直らない。`OpenTabById`（`EditorTabSpawn` が必要）でタブを前に出すか、ユーザーに頼む |
| `Headless` | `NotAllowed` | このプロセスでは Slate がウィジェットを描かない（描画デバイスが無い、コマンドレット、専用サーバー）。描画デバイスが無い場合は、文でもそう伝える | 描画デバイスのある環境でエディタを起動し直す |
| `DebuggerPaused` | `NotAllowed` | ブループリントのデバッガのブレークポイントが、フレームの途中でゲームスレッドを止めている | 実行を再開してから撮り直す |
| `NotInVisibleTree` | `NotAllowed` | ウィンドウからウィジェットまでの経路が無い（ウィジェットまたは祖先が折りたたまれている、隠されている） | その部分を表示させてから撮り直す |
| `BlockedByModal` | `NotAllowed` | モーダルウィンドウが開いていて、描かれるのはモーダル・その子・ツールチップ・通知だけ | モーダルを閉じてから撮り直す |
| `Minimized` | `NotAllowed` | ウィンドウ、または先に描かれるはずの祖先のウィンドウが最小化されている | 復元する。エディタのメインウィンドウなら、`SetEditorWindowState` を `State: Restored` で呼ぶ（`EditorWindowStateControl` が必要）か、ユーザーに戻してもらう |
| `Hidden` | `NotAllowed` | ウィンドウ、または祖先のウィンドウのネイティブウィンドウが見えない状態。作られたがまだ一度も表示されていないウィンドウも、エンジンが両者を区別できないので同じ扱い | ウィンドウを表示させる。起動直後なら、表示し終わってから呼び直す |
| `NotRenderable` | `PreconditionFailed` | レンダラーがそのウィンドウのビューポートを持たない、またはビューポートの大きさが 0 | ウィンドウの表示が終わるのを待ってから呼び直す |
| `InBackgroundTab` | `NotAllowed` | 対象が、別のタブの後ろに回ったドッキングタブの中、または別のエディタのタブの後ろに回ったエディタのタブの中（たとえばブループリントエディタを開いたあとのレベルエディタのビューポート）にあり、描かれない。確認は、Slate 未初期化の `NoWindow` の直後に行う | タブを前に出す。`OpenTabById`（`EditorTabSpawn` が必要。開いているタブも、それを収めたエディタのタブごと前に出る）を使うか、ユーザーに頼む。`OpenTabById` は `TabId` と `OwnerTabId` の両方を取る。`OwnerTabId` は対象を収めたエディタのタブ（レベルエディタなら `LevelEditor`）で、有効な組み合わせは `ListSpawnableTabs` が一覧する。待っても変わらない。`CaptureEditorTabImage` は自分で前に出す |
| `WindowSizeMismatch` | `NotAllowed` | Slate が持つウィンドウの大きさが OS の報告する大きさと食い違い、撮る前に試みる同期でも直らなかったため、撮ると壊れた画像になる。全てのキャプチャのコマンドが、撮る前に両者を比べる。最小化されたウィンドウは比べない。確認は `Minimized` / `Hidden` の後、`NotRenderable` の前に行う | エディタのメインウィンドウなら、`SetEditorWindowState` で `Minimized` にしてから `Restored` に戻し（`EditorWindowStateControl` が必要）、もう一度キャプチャする。それでも直らなければ、ユーザーにウィンドウの大きさを手で変えてもらう。メインウィンドウ以外は、ユーザーに大きさを変えてもらう |

- **`InBackgroundTab` だけは表の順と違う**: `Headless` と Slate 未初期化の `NoWindow` の後、ほかのウィンドウの確認より前に確認する。表の末尾近くにあるのは、後から足したため。`WindowSizeMismatch` は `Minimized` / `Hidden` の後、`NotRenderable` の前に確認する。
- **`NoWindow` と `NotRenderable` は `PreconditionFailed`**: 土台がまだ無く、待てば直る。シナリオのステップに `RetryCount` があれば再試行される。
- **それ以外の `Reason` は `NotAllowed`**: 既にあるウィンドウの状態がキャプチャを許さない。シナリオの `RetryCount` は `NotAllowed` を**再試行しない**。以前は最小化されたウィンドウに `ExecutionFailed` が返っていたため再試行の対象だったステップも、今は 1 回で失敗する。表のとおり、先に状態を変える。
- 親のウィンドウが描かれないとき、子のウィンドウも描かれない。そのため、親が最小化または非表示のウィンドウの子（浮いているウィンドウなど）は、子自身が最小化されていなくても、親の状態（`Minimized` または `Hidden`）で拒否される。モーダルが開いている間は、モーダル・その子・ツールチップ・通知だけが撮れる。
- 撮れる状態のはずが撮影に失敗した場合（エンジンが画像を返さない、画像が空、PNG への変換に失敗）は、`Reason` なしの `ExecutionFailed` で、文がどの段階の失敗かを言う。

**ゲームビューポートのコマンドも同じように断る。** `CaptureViewportImage`（`UAIP.Runtime.Observation`）は、撮る前にゲームビューポートが描かれる状態かを確かめる。描かれない状態（ビューポートを持つウィンドウが最小化・非表示、モーダルが開いている、など）なら、撮らずに拒否する。`Reason`・エラーコード・`Result.Reason` は上の表と同じで、エラー文が直し方を言う。最小化されたウィンドウがエディタのメインウィンドウ（そこに収まった Play In Editor のウィンドウ）なら `SetEditorWindowState` の案内、別ウィンドウの PIE やスタンドアロンのゲームなら、そのウィンドウを戻してもらう案内になる。撮れる状態のはずが撮影に失敗した場合は、従来どおり `Reason` なしの `ExecutionFailed`。

- **`CheckpointCapture` は拒否をそのまま引き継ぐ。** 最初に `CaptureViewportImage` で撮るため、それが拒否されると、チェックポイントも同じ `NotAllowed` または `PreconditionFailed` で拒否し、`Reason` を自分の `Result.Reason` にコピーする。エラー文は `CheckpointCapture: CaptureViewportImage failed: ` に `CaptureViewportImage` の文が続く形。組み合わせている 2 つのコマンドのそれ以外の失敗は `ExecutionFailed` のまま。
- **ゲームビューポートの UI 操作は、ホストウィンドウの状態で拒否される。** `ClickGameViewportWidget`・`PressGameViewportUIKey`・`TypeGameViewportText` は、何かを送る前にゲームを載せているウィンドウを確かめ、`Reason: HostWindowUnavailable` で拒否する。`NoWindow`（ゲームビューポートのウィンドウがまだ無い）は `PreconditionFailed`（`The game viewport has no window yet. Retry after the game window has been created.`）、`Hidden` と `Minimized` は `NotAllowed`（`The window that hosts the game is not visible, so nothing in it is laid out.` / `The window that hosts the game is minimized, so nothing in it is laid out.`）。最小化は `PreconditionFailed` ではなく `NotAllowed` なので、シナリオの `RetryCount` は再試行しない。先にウィンドウを戻す。

---

## UAIP.Editor.Execution

テスト・Python スクリプト・Editor Utility Blueprint の実行。

| コマンド | 説明 |
|---|---|
| `DiscoverAutomationTests` | Automation Test モジュールを読み込み、検出されたテスト数のサマリを返す |
| `ListAutomationTests` | 検出済み Automation Test をフィルタして JSON Artifact で返す |
| `RunAutomationTest` | UE Automation Test を名前で実行し、テストごとのレポート（Pass / Fail / Skipped / Error / Cancelled。[レポートの共通契約](#automation-test-のレポートの共通契約) を参照）を返す |
| `RunAutomationSpec` | UE Automation Spec を名前で実行し、テストごとのレポート（`RunAutomationTest` と同じ契約）を返す |
| `GetAutomationTestStatus` | Automation Test マネージャの現在状態を返す（既定はインライン） |
| `StopAutomationTests` | 実行中の Automation Test バッチのキャンセルを要求 |
| `RunEditorPythonScript` 🧩 | インライン Python スクリプトまたは `.py` ファイルを実行（`PythonScriptPlugin` 必須） |
| `RunEditorUtilityBlueprint` | 指定 Editor Utility Blueprint を実行 |
| `RunNamedEditorCommand` | `GUnrealEd->Exec` 経由で名前付き Editor コンソールコマンドを実行 |

> **`RunEditorPythonScript` は、長引いたスクリプトを打ち切れます。** 省略可能な `AbortAfterSeconds` は `0`〜`1800` の整数です。`0` は打ち切らない意味で、省略するか `null` を渡すと ini の既定（`[UAIP.Python] DefaultAbortAfterSeconds`、これ自体の既定は `0`。[設定](config.md#uaippython--runeditorpythonscript-の既定の打ち切り期限) を参照）が使われます。期限が過ぎると、ゲームスレッド上でスクリプトの中に例外が送られ、スクリプトが止まるまで 1 秒ごとに送り直されます。
>
> **これは best effort です。** 例外が届くのは Python のバイトコードの合間だけなので、ネイティブ呼び出し（`time.sleep` や長いエンジン呼び出しなど）の途中にいるスクリプトは、その呼び出しが戻った時点で初めて止まります。打ち切り前に行われた編集は**残ります**。例外を握りつぶすスクリプトは止まらず（1 秒ごとに送り直されます）、繰り返し送られる例外がスクリプト自身の後始末を中断することもあります。期限後は、同じスレッドで動く他の Python に例外が届くこともあります。スクリプトが起動したスレッドは止まりません。打ち切りは Python 3.11 のビルドでだけ使え、他の版では打ち切りを求めた呼び出しが `AbilityUnavailable` で拒否されます。
>
> **打ち切られた呼び出し**は `Timeout` を返し、`Data.Aborted: true`・`Data.NotExecuted: false`（スクリプトは部分的に実行済み。再実行の前にエディタの状態を確認してください）が付きます。`Data` には `AbortAfterSeconds`、`AbortSource`（`Argument` または `Config`）、`DeadlineExceeded`、`Aborted`、`AbortSignalsSent`、`ElapsedSeconds` が載り、該当する場合に限り `NotExecuted`、`AbortDrainFailed`、`AbortInjectionFailed` も載ります。引数で `0` を明示した場合は `AbortAfterSeconds` と `AbortSource` の 2 キーだけ、ini 由来の `0` では `Data` は付きません。
>
> **拒否:** ゲームスレッド上の別の Python 実行の中から呼ぶと `NotAllowed`、Python の初期化前または終了処理中は `PreconditionFailed` になります。
>
> **推奨:** 呼び出しの `TimeoutSeconds`（MCP / HTTP のリクエストの待ち時間）は `AbortAfterSeconds` より長くしてください。短いと、スクリプトの応答が届く前にリクエストが諦めます。Python をデバッグ中は `0` を明示してください。`TimeoutSec` は受け付けますが効きません。打ち切りたいときは `AbortAfterSeconds` を使ってください。

> **Note**: `RunAutomationTest`（および Runtime 側の `RunRuntimeAutomationTest`）は、`RunAllMatching=true`（既定）のとき**マッチした全件を実行します**。件数を絞るには `MaxMatchingTests`（1 以上。省略すると上限なし）を指定してください。`0` は「上限なし」ではなく無効値として拒否されます — 両者は正反対の要求であり、読み替えると絞った実行が全件カバーを名乗ることになるためです。
>
> レポートには常に `Summary.Matched`（フィルタに一致した数）と `Summary.Selected`（実際に走らせた数）が入ります。**差の有無に関わらず必ず出力されます** — 差があるときだけ出す形式では、その行が無いことが「全件だった」のか「その版が出力しないだけ」なのか読み手に区別できないためです。人間向けレポート本文と Output Log にも同じ 2 つが出ます。
>
> `TimeoutSec` は**バッチ全体ではなく 1 テストごとの上限**です（既定 60 秒）。マッチ件数が増えても各テストがこの時間内に終わる限り全件走ります。なお Runtime 側の `RunRuntimeAutomationTest` にはこれとは別に一括実行全体の壁時計上限（600 秒）があり、到達した場合はレポートに `(bulk execution time limit reached)` というエントリが `Error` として現れます。
>
> **v1.1.0 での変更**: 以前は 100 件で打ち切られ、**打ち切られたことが応答から分かりませんでした**（`Pass=100 Fail=0` は全件成功と字面が同じです）。100 件で止まる挙動に依存していた場合は `MaxMatchingTests=100` を明示してください。

> **v1.2.0 での変更**: `RunAutomationSpec` がパラメータスキーマを宣言し、それ以外を拒否するようになりました — 受け付けるのは `TestName`（必須）・`TimeoutSec`・`RunAllMatching`・`MaxMatchingTests`（`RunAutomationTest` と同じパーサーを共有するため同じ4キー）で、`AdditionalProperties: false` です。**`SpecName` などこの集合の外のキーを指定すると、これまでの黙って無視される挙動から `InvalidParams` に変わりました** — 以前はスキーマを一切宣言していなかったため、未知のキーはチェックされずに通過し、単に何も起こしませんでした。`RunAllMatching` と `MaxMatchingTests` は `RunAutomationTest` とのスキーマ上の対称性のために受理されますが、**Spec の実行には影響しません** — `Execute()` は常に単一の完全一致に強制されるため、どちらのパラメータの値も無視されます。

#### Automation Test のレポートの共通契約

`RunAutomationTest`・`RunAutomationSpec`・`RunRuntimeAutomationTest` は同じ形のレポートを返します。

**`Tests[]` の各要素**は `Name`・`Result`・`TimeSec` を持ち、さらに 3 つのメッセージ配列を、**空でないときだけ**この順で持ちます: `FailMessages`、`SkipMessages`、`WarningMessages`。

**`Result` は次の 5 値のいずれかです。**

| 値 | 意味 |
|---|---|
| `Pass` | テストが成功し、スキップ行も出さなかった |
| `Fail` | テストがエラーを 1 つ以上記録した。エラーは `FailMessages` に入る |
| `Skipped` | テストが成功し、スキップ行（`TEST-SKIP[<Reason>]: <Detail>`）を 1 つ以上出した。その行は `SkipMessages` に入る |
| `Error` | テストがエラーを記録せずに失敗した（または実行側がテストを走らせられなかった。例: タイムアウト）。テストがエラーを記録していないときは、`FailMessages` に合成メッセージ `The test reported failure without recording an error.` が入り、失敗した結果には必ず理由が付く |
| `Cancelled` | テストが完了する前にキャンセルされた |

エラーを記録したテストは、メッセージの 1 つがスキップ行に見えても `Fail` です。警告は `Result` を変えません。警告は `WarningMessages` に入り、テストを失敗させません。

**`Summary`** は `Pass`、`Fail`（`Fail` と `Error` の両方）、`Skip`（`Skipped` の結果）、`Cancelled` を数え、`Matched`・`Selected`・`TotalTimeSec` も持ちます。スキップしたテストは `Summary.Pass` ではなく **`Summary.Skip`** に数えられます。

**ログの成果物**は、各テストのエントリを `FAIL:`（`FailMessages`）→ `SKIP:`（`SkipMessages`）→ `WARN:`（`WarningMessages`）→ `LOG:`（その他の出力）の順に並べます。

**`ReportErrors`**（レポートのルート）は、特定の 1 テストに属さない実行全体の問題を持ちます。1 件以上あるときだけ出力され、`Summary` の件数には数えません。

---

## UAIP.Editor.UIAutomation

エディタ UI の操作 — クリック・入力・選択・ドラッグ。

| コマンド | 説明 |
|---|---|
| 🆓 `ClickWidget` | `SnapshotUI` が返す `WidgetRef` で識別したウィジェットへの左クリックをシミュレート |
| 🆓 `SelectMenuItem` | スラッシュ区切りのラベルパスでメニュー項目を選択 |
| 🆓 `InputText` | `SnapshotUI` が返す `WidgetRef` で識別したウィジェットにテキストを入力 |
| 🆓 `SetCheckboxState` | チェックボックスの状態を設定 |
| 🆓 `SetComboSelection` | コンボボックスでラベル指定の項目を選択 |
| 🆓 `DragGraphNode` | 指定グラフエディタタブでグラフノードをピクセル単位でドラッグ |
| 🆓 `ConnectGraphPins` | 指定グラフエディタタブで 2 つのピンを接続 |
| 🆓 `AcceptDialog` | アクティブなモーダルダイアログを承諾（OK/Yes/Accept をクリック） |
| 🆓 `CancelDialog` | アクティブなモーダルダイアログをキャンセル（Cancel/No をクリック） |
| 🆓 `InvokeContextMenuAction` | 指定対象を右クリックしてコンテキストメニューから項目を実行 |
| 🆓 `HoverWidget` | ウィジェットに OnMouseEnter をシミュレート |
| 🆓 `PressKey` | 修飾キー対応のキー入力をシミュレート（危険ショートカットブラックリスト付き）。メニューを閉じるには `DismissMenus` を使う（Escape は受け取ったウィジェットが消費しうる） |
| 🆓 `WaitForWidget` | `SnapshotUI` の `WidgetRef` で識別したウィジェットが期待状態になるまでポーリング |
| 🆓 `FillForm` | フォームウィジェットへの一括入力を逐次 state machine で実行 |
| 🆓 `SnapshotUI` | 範囲を絞り込め、除外分も報告する UI の構造スナップショットを取得。`IncludeFieldValues: true` を指定すると入力欄の値とヒント文も返す。パスワード欄の平文には `AllowPasswordFieldRead` と `EditorWidgetPasswordTextRead` が必要 |
| 🆓 `DismissMenus` | 開いているメニューやポップアップ（すべて、または指定したウィジェットを含むメニューとそのサブメニュー）を閉じ、消えるまで待つ |
| 🆓 `OpenPasswordTestWindow` | パスワード用 `SEditableTextBox` を持つ小さな単独のテストウィンドウを開く（`InputText` やパスワードフィールドのポリシーが、パスワード欄をどう扱うかを確かめるためのターゲット）。アセット・設定・保存済みの状態は何も変更しない。窓を開くだけなので、製品版だけでなくデモ版にも含まれる |

> **Note**: ウィジェットを対象にするコマンドは、ウィジェットパスではなく `SnapshotUI` が返す `WidgetRef` を受け取ります。先に `SnapshotUI` を呼び、対象ウィジェットの `WidgetRef` を渡してください。
>
> **`SelectMenuItem`** の必須パラメータは `MenuPath` の 1 つです。スラッシュ区切りのメニューラベルの並びで、例は `Edit/Project Settings...` です。
>
> - 先頭の要素はメニュー名です。2 番目以降の要素は、メニュー名か表示ラベルに、大文字小文字を無視して完全一致する必要があります。
> - `/` を含むラベルは指定できません。
> - `...` を含むラベル（`Project Settings...` など）は使えます。
> - 次のものは `InvalidParams` で拒否されます: `..` だけのセグメント、空のセグメント、制御文字、長さが 256 を超えるもの、階層が 10 を超えるもの。
>
> **`WaitForWidget`** は `WidgetRef`（必須）と `ExpectedState`（必須。`Exists` / `Absent` / `Visible` / `Hidden` / `Enabled` / `Disabled` / `Focused` のいずれか）を受け取ります。`WaitTimeoutSeconds` は任意です（既定 5.0、30 以下）。`PollIntervalSeconds`（既定 0.1、0.05 以上）と `ConfirmTickCount`（既定 3、10 以下）も任意です。

> **Note — 入力経路と `PartialDelivery`**: `ClickWidget`・`HoverWidget`・`PressKey`・`AcceptDialog`・`CancelDialog`・`SetComboSelection`・`FillForm` は、実行時の UI コマンド（[`ClickGameViewportWidget`](#ゲームビューポートの-ui-入力3) など）と同じ作り方で入力を作るようになりました。パラメータ・エラー・拒否される条件（メニュー・モーダル）は変わらず、`HoverWidget` も従来どおり成功を返します（送った後にホバーが立ったかを確かめ、結果はログに残すだけです）。ホバー・コンボ操作・キー押下が本物のマウス・キーボードと同じユーザー番号で届くようになるため、ユーザー番号で入力を振り分ける UI では、以前は効かなかった操作が効くようになることがあります。`SetComboSelection` / `FillForm` のコンボ操作は、カーソルを動かしてから押し、対象（またはその中身）にカーソルが乗ったことを確かめるようになりました。他の UI に覆われているなど乗らなかった場合は、押す前にその欄の失敗として返ります。
>
> 挙動が変わるのは 1 点です。`ClickWidget`・`AcceptDialog`・`CancelDialog` で、押した操作そのものでモーダルが開いた場合、以前は離す操作がモーダルを閉じた後（応答を返した後）に届いていました。これからは離す操作を送らず、応答は押下を送ったこととして `ModalOpened` と `PartialDelivery: DownOnly` を添えて返ります（ゲームビューポートの UI のクリックと同じです）。

> **Note**: `SnapshotUI` は任意の走査範囲を指定できます。起点には `RootWidgetRef` または `RootWidgetPath`（互いに排他。どちらも `WindowTitle` とは併用不可）、走査量には `MaxDepth`（既定 30）と `MaxNodes`（既定 50000。1 回の呼び出しで訪れる全ルートで共有される単一予算）、絞り込みには `WidgetTypes` + `WidgetTypeMode`（`"Add"` は既定の対象に追加、`"Only"` は指定した型だけに限定）と `LabelContains`、既定で外れるウィジェットを拾うには `bIncludeInvisible` / `bIncludeUnclassified` を使います。応答には常に `EmittedCount`・`FilteredCount`・`FilteredReasons`（0 件でも常に存在する 6 つの理由キー — `InvisibleSubtreeRoot` / `StructuralContainer` / `TypeFilterMismatch` / `LabelFilterMismatch` / `Unclassified` / `RegistrationFailed`）・`UnclassifiedTypes`（`Type` + `Count` を件数降順・同数なら型名昇順で最大 200 件。各 `Type` はそのまま `WidgetTypes` に渡せる）・`Traversal`（`Complete` / `NodeLimitReached` / `DepthLimitReached` / `VisitedNodeCount`）・`MatchedRootCount`・`EffectiveParams`（クランプ・正規化後に実際に適用された値）が含まれます。
>
> 応答が答えられるのは常に「現在のフィルタを通過した集合に無い」までです。これを「UI 上のどこにも存在しない」と読み替えてよいのは、次のすべてが成り立つときに限ります: 走査が打ち切られていない（`Traversal.Complete == true`）、未分類型の一覧が全件かつ名指し可能（`UnclassifiedTypesComplete == true` かつ `UnaddressableUnclassifiedCount == 0`）、不可視ウィジェットを刈り取っていない（`FilteredReasons.InvisibleSubtreeRoot == 0`、または `bIncludeInvisible` を指定済み）、`WidgetTypeMode` が `"Add"`（型で絞り込んでいない）、`LabelContains` が空、Ref の登録に失敗したウィジェットが無い（`FilteredReasons.RegistrationFailed == 0`）、`WindowTitle` / `RootWidgetRef` / `RootWidgetPath` のいずれでも呼び出しを絞り込んでいない（絞り込んでいる場合はその範囲内でしか結論が成り立たない）。これらすべてを満たしていても、**構造コンテナ**型（後述）は `Widgets` にも `UnclassifiedTypes` にも現れません — `WidgetTypes` で名指しして確認してください。
>
> 構造コンテナ — レイアウトを組むためだけに存在するウィジェット — は走査はされますが emit されず、未分類型としても列挙されません。代わりに `FilteredReasons.StructuralContainer` にまとめて計上されます: `SBox` / `SBorder` / `SOverlay` / `SSpacer` / `SConstraintCanvas` / `SHorizontalBox` / `SVerticalBox` / `SGridPanel` / `SWrapBox` / `SWidgetSwitcher` / `SCanvas` / `SScaleBox` / `SSizeBox` / `SNullWidget` / `SInvalidationPanel` / `SRetainerWidget`。これらを `WidgetTypes` で名指しすれば emit されます — 明示的な型指定は常に分類より優先されます。
>
> 型名は `SWidget::GetTypeAsString()` から取得されます。これはウィジェットの構築サイトで `SNew(...)` に渡した識別子であり、動的な型ではありません。`SNew(基底型)` で構築されたウィジェットは、実際の型が異なっていても基底クラス名を返します。また `SNew` を経由せずに構築されたウィジェット（例: `MakeShared<SFoo>()`）は、型名としてリテラル文字列 `"None"` を返します。
>
> `RootWidgetRef` は使い捨てです。呼び出しが完了すると、指定した Ref だけでなく**そのセッションの `WidgetRef` がすべて**無効化されます — `SnapshotUI` の呼び出しごとに新しい世代が始まるためです。以前の Ref を残したまま段階的に絞り込みたい場合は `RootWidgetPath` を使ってください。`SnapshotUI` は引き続き `IsReadOnly() == true` を宣言し `bReadOnly` 下でも実行できます — リセットされるのは UAIP 側の Ref キャッシュのみで、永続的なエディタの状態は変わりません。UI Automation の全コマンドを通じて、`WidgetRef` はそれを発行したスナップショットから 60 秒で失効します。

> **ラベル。** `SnapshotUI` のノードの `Label` は、次の順で決まります。ウィジェットのアクセシビリティ文字列、リッチテキスト（`SRichTextBlock`）なら表示内容の近似、ウィジェットの Tag、型名。名前もアクセシビリティ文字列も無いウィジェットは、`None` ではなく型名がラベルになりました。リッチテキストの近似は、`<...>` のタグをすべて取り除くので、タグ名や属性（リンク先など）はラベルに出ません。複数行は空白 1 つでつなぎます。実際の表示と少し食い違うことがあります。スタイルに無いタグを使った文字列は近似になり、文字どおりの `<b>` も除かれます。リッチテキストは既定の対象（ロール `tb`）に入るので、ノード数・Ref の番号の振られ方・`MaxNodes` に達する位置が変わることがあります。
>
> - ボタンのラベルは子のアクセシビリティの要約をつなげて作られるため、子がリッチテキストでも改善しません。
> - `Label` は、パス属性 `[Label=...]` が照合する文字列（加工していないアクセシビリティ文字列）とは別物です。`Label` をそのまま `[Label=...]` に書いても一致しないことがあります。
> - `DumpSlateTree` では、`AccessibleText`（`IncludeTextContent: true` のとき）にも同じラベルが入ります。互換のためキー名は変えていないので、名前と中身は正確には一致しません。`PressKey` の `FocusedWidgetTypeName` も、名前に反して中身は対象のウィジェットの型です。こちらもそのままです。
> - パスワード欄と、パスワード欄かどうか判定できない欄のラベルは、アクセシビリティ文字列ではなく、ヒント文（無ければ型名）になります。`SnapshotUI` では `IncludeFieldValues` によらず常にそうで、`DumpSlateTree` の `AccessibleText` も同じです。アプリがパスワード欄のアクセシビリティ文字列を値に結び付けていても、ラベルから漏れません。通常の欄のラベルは変わりません。ボタンのように子から組み立てる親のラベルは対象外です。アプリがパスワード欄のアクセシビリティ文字列を値に結び付けていると、その値が親のラベルに現れることがあります。
>
> **`IncludeFieldValues`。** `SnapshotUI` は bool の `IncludeFieldValues`（既定 `false`）を受け取ります。`true` にすると、入力テキスト（`SEditableTextBox` の内側の `SEditableText` と `SMultiLineEditableText`）のノードに次の欄が付きます。
>
> | 欄 | 付く条件 | 内容 |
> |---|---|---|
> | `HintText` | 常に | ヒント文。制御文字を除き、256 文字で切ります |
> | `Value` | パスワード欄でないとき | 入力されている文字列。256 文字で切り、切ったときは `ValueTruncated: true`。改行とタブは残し、それ以外の制御文字は除きます |
> | `ValueWithheld` | パスワード欄、またはパスワード欄かどうか判定できないとき | `Value` の代わりに `"Password"` または `"PasswordUnknown"` |
>
> 保存されるスナップショット（artifact の JSON。応答の `Result` ではありません）のトップレベルに、伏せた欄の数（`ValueWithheldCount`）と、伏せた値を応答に返さなかったときの理由（`PasswordValuesWithheldReason`）も入ります。`IncludeFieldValues` はスキーマのパラメーターで、`EffectiveParams` にも出ます。`LabelContains` が見るのは `Label` だけで、値は検索しません。複数行の入力欄は既定の対象に入りません。`WidgetTypes` で名指しする（または `bIncludeUnclassified` を指定する）と含まれますが、内側のテキストは判定できない欄として扱うので、値は伏せられます。
>
> パスワード欄（と、判定できない欄）の平文が返るのは、安全設定 `AllowPasswordFieldRead` がオンで、**かつ**セッションが Capability `EditorWidgetPasswordTextRead` を持つときだけです（[Safety & Capabilities](safety.md#エディタ操作) 参照）。返るときは、応答の `Result` にだけ、スナップショットの保存と添付が成功し、値が 1 件以上あるときに限って（それ以外の `Result` は空です）、`PasswordFieldValues`（`{Ref, Value, ValueTruncated?}` の配列。最大 16 件・各 256 文字）に入ります。入りきらない分は `PasswordFieldValuesTruncated: true` と `PasswordFieldValuesOmittedCount` で知らせます。保存されるスナップショットとログには出ず、完了通知では伏せられます。失敗した応答（スナップショットを保存できなかったときなど）にも入りません。`SnapshotUI` 自体は `EditorWidgetPasswordTextRead` を要求しないので、持たないセッションでもスナップショットは返り、値だけが伏せられます。理由は（保存されるスナップショットの）`PasswordValuesWithheldReason` が示します。安全設定がオフなら Capability の有無によらず `PasswordTextWithheldBySafetyPolicy`（設定は起動時に読まれるため、最初に直すべきものとして先に知らせます）。設定がオンで Capability が無ければ `PasswordTextWithheld` です。名前と優先順は `DumpGameViewportWidgetTexts` と同じです。
>
> **とても深いツリー。** 保存する JSON には、入れ子の深さの上限があります。出力するウィジェットの入れ子が 30 段を超えるウィジェットは、その下も含めて出力しません。`Traversal.OutputNestingLimitReached` が `true` になり、出力しなかった数が `Traversal.OutputNestingSkippedCount` に入り、見ていない枝があるので `Traversal.Complete` も `false` になります。出力しなかったウィジェットには `WidgetRef` が付きません。以前は、こういうツリーで何も知らせずに空の artifact が返ることがありました。それでも JSON を作れないときは、深さの上限を示す `ExecutionFailed` で失敗し、直前のスナップショットの `WidgetRef` は有効のまま残ります。
>
> **`DismissMenus`** は、開いているメニューやポップアップを閉じ、消えるまで待ちます。
>
> - `WidgetRef`（任意）。省略するか `null` なら、開いているメニューをすべて閉じます。`WidgetRef` を指定すると、そのウィジェットを含むメニューと、そこから開いたサブメニューだけを閉じます。親のメニューは開いたまま残り、応答には `MenuStackOpenAfter: true` が付きます。空文字列・文字列以外の値・形式の正しくない Ref は `InvalidParams` で拒否します。Ref を取り損ねたときに「すべて閉じる」にすり替わらないようにするためです。
> - Capability は `EditorUIAutomation` です。読み取り専用ではなく、デモ版に含まれ、Toolset ブリッジはありません。キーボードフォーカスは動かさず、Escape も送りません。
> - `Result`（と artifact）には `MenusOpenBefore`・`MenuWindowCountBefore`・`MenuWindowCountAfter`・`MenuStackOpenAfter`・`FramesWaited` が入ります。閉じた後にフォーカスを持つウィジェットがあれば `KeyboardFocusWidgetType` も入ります。
> - 閉じたメニューのウィンドウが消えるまで、最大で 10 フレーム**かつ** 1 秒（遅いほう）待ちます。それでも残っていれば `ExecutionFailed` で、残ったウィンドウの数とメニュースタックの状態を `Result` に入れます。
> - 拒否されるのはドラッグ中だけです（`PolicyViolation`、`Reason: DragInProgress`、`GuardDiagnostics` 付き）。メニューやモーダルの外にあることは理由になりません。
> - 何も開いておらず `WidgetRef` も無いときは、`MenusOpenBefore: false`・`FramesWaited: 0` の成功です。何度呼んでも構いません。`WidgetRef` を指定した呼び出しは、メニューが閉じた後では冪等になりません。`NotFound` を返し、ウィジェットが破棄されていれば `Result.Reason: WidgetDestroyed`（閉じたメニューの中のウィジェットは通常破棄されます。要求の受付前でも後でも同じです）、ウィジェットは残っているがどのメニューにも属さなければ `Result.Reason: WidgetNotInApplicationMenu` です。どのメニューにも属さないウィジェットを指定したときも `WidgetNotInApplicationMenu` です。これらのときは何も閉じません。形式の不正や期限切れの Ref は、他の UI コマンドと同じく `InvalidParams` / `NotFound` です。
> - 待っている間に UAIP が停止したときは、`ExecutionFailed` と `Reason: DeliveryCancelledByShutdown` を 1 回だけ返します。
> - **制限。** 閉じる対象にも数える対象にもなるのは、アプリのメニュースタックに載ったメニューだけです。スタックに載らずに開くメニュー（一部のエンジンのプラグインにあります）には触れません。`WidgetRef` なしで、そういうメニューだけが開いているときは、`MenusOpenBefore: false` の成功を返してウィンドウは残ります（`MenuWindowCountAfter` で分かります）。その中のウィジェットを `WidgetRef` に指定したときは、`NotFound` と `WidgetNotInApplicationMenu` です。そのメニュー自身の操作で閉じてください。
> - **モーダルダイアログの中から。** モーダルダイアログが開いている間、`StarvedTickAllowList` に無いコマンドはその場で `NotAllowed`（メッセージは `[StarvedTick]` で始まります）で断られ、何も閉じません。ダイアログが閉じてから送り直してください。コマンドポンプを有効にしている場合（`uaip.Command.PumpedExecution=1`）だけは、断られずにキューで待ち、ダイアログが閉じてから実行されます。その間に呼び出し側の Transport がタイムアウトすることがあります。モーダルの中から開いたピッカーを閉じるには、`StarvedTickAllowList` に `UAIP.Editor.UIAutomation.DismissMenus` を足して、エディタを再起動します（このリストは起動時に 1 回だけ読まれます。コマンドポンプの有効化は不要です）。閉じるのはピッカーだけで、モーダルダイアログは開いたまま残ります。[`[UAIP.CommandPump]`](config.md#uaipcommandpump--モーダル表示中のコマンド実行既定で無効) を参照してください。
> - `PressKey` で Escape を送ることはできますが、キーを受け取ったウィジェット（メニューの検索欄など）が消費すると、メニューは閉じません。メニューを閉じるには `DismissMenus` を使ってください。
>
> **操作が拒否された理由の確認。** `ClickWidget`・`HoverWidget`・`PressKey` は、ドラッグ中（`DragInProgress`）、モーダルが開いていて対象がその外にあるとき（`ModalActive`）、メニューが開いていて対象がその外にあるとき（`ForeignMenuActive`）に、`PolicyViolation` で拒否されます。`ErrorMessage` はその理由です。応答の `Result` と保存される報告の両方に `GuardDiagnostics` オブジェクトが付くので、artifact を開かなくても原因が分かります。
>
> | 欄 | 内容 |
> |---|---|
> | `RejectReason` | 上の理由 |
> | `TargetWidgetType`, `TargetWindowType` | 対象の型と、それが属するウィンドウの種類（`Normal` / `Menu` / `ToolTip` / `Notification` / `CursorDecorator` / `Unknown`） |
> | `TargetInMenuStack` | 対象がアプリのメニュースタックのメニューに属するか |
> | `KeyboardFocusWidgetType`, `KeyboardFocusWindowType` | キーボードフォーカスの位置（誰も持っていなければ出ません） |
> | `OpenMenuWindowCount`, `MenuStackOpen` | 見えているメニューのウィンドウの数と、メニュースタックが開いているか |
> | `ActiveModalWindowTitle` | 開いているモーダルウィンドウのタイトル（あれば） |
>
> 出るのは型名・ウィンドウの種類・モーダルのタイトルだけで、ウィジェットのテキストは入りません。どの理由でも同じキーを同じ規則で出します。対象が「開いているメニューの中」かどうかは、アプリのメニュースタックのメニューに属するか（補助的に、Menu 型ウィンドウの中か）で判定するようになり、親を最大 50 段たどる方式ではなくなりました。そのため、メニューの深い位置にあるウィジェットや、独自のウィンドウを持たずに開くメニュー（PIE のゲーム画面のコンボなど）が、「メニューの外」として拒否されることはなくなります。
>
> **書き込み系コマンドのガード（`GuardWriteCommands`）。** `InputText`・`FillForm`・`SetCheckboxState`・`SetComboSelection` は、既定ではこのガードを通りません。`DefaultUAIP.ini` の `[UAIP.UIAutomation]` で `GuardWriteCommands=True` にする（起動時に 1 回だけ読むのでエディタの再起動が必要。ini のみで起動フラグはありません。[設定リファレンス](config.md#uaipuiautomation--書き込み系コマンドのガード既定で無効) 参照）と、要求を受け付けるときに 1 回、クリックと同じ判定を受けます。ドラッグ中、または対象が開いているモーダルウィンドウやメニューの外にあるときは、`PolicyViolation` と同じ `GuardDiagnostics` で拒否されます。`FillForm` は全か無かです。どれか 1 つの欄の対象が拒否されたら、どの欄にも書き込まず、最初に拒否された欄の拒否を返します。このとき `Result.RejectedFieldName` にその欄の `WidgetRef` が入ります。解決できない欄が混じる `FillForm` は、ガードを判定する前に、これまでどおりの検証エラーを返します。`SetComboSelection` は要求を受け付けるときに 1 回だけ判定し、コンボを開いた後の項目のクリックでは判定し直しません。判定はその時点のもので、値を書き込む前に状態が変わる可能性は残ります。
>
> **記録。** `InputText` に渡した文字列（`Text`）と `FillForm` に渡した値（`Fields`）は、`TypeGameViewportText` の文字列と同じく、完了通知と監査記録で伏せられるようになりました。以前は入力したとおりに記録されていました。


### Toolset ブリッジ — SlateInspector（10 件）🧩

`SlateInspectorToolset`（UE 5.8+）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.SlateInspector.*`。refPath でウィジェットを指定します。ネイティブ側のコマンドは、`SnapshotUI` が返す `WidgetRef` でウィジェットを指定します。このセクションの全ブリッジコマンドは、対応するネイティブコマンドと同じ Capability を要求するようになりました（[Safety & Capabilities](safety.md) 参照）— それまでのリリースでは Capability チェックなしにディスパッチされていました。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.SlateInspector.SnapshotUI` | 指定 ref のウィジェットツリーをスナップショット |
| `Toolset.Editor.SlateInspector.ObserveWidget` | ⚠️ **呼び出せません** — 委譲先が存在しない。下の注記を参照 |
| `Toolset.Editor.SlateInspector.UnobserveWidget` | ⚠️ **呼び出せません** — 委譲先が存在しない。下の注記を参照 |
| `Toolset.Editor.SlateInspector.ListObservers` | 現在有効なウィジェット observer を列挙 |
| `Toolset.Editor.SlateInspector.ClickWidget` | 指定 ref のウィジェットへのマウスクリックをシミュレート |
| `Toolset.Editor.SlateInspector.HoverWidget` | 指定 ref のウィジェット上へカーソルを移動 |
| `Toolset.Editor.SlateInspector.InputText` | 指定 ref のウィジェットにテキストを入力 |
| `Toolset.Editor.SlateInspector.PressKey` | キー入力を送信（`Ctrl+S` のような修飾キープレフィックス対応）。メニューを閉じるには `DismissMenus` を使う（Escape は受け取ったウィジェットが消費しうる） |
| `Toolset.Editor.SlateInspector.SetComboSelection` | コンボボックスウィジェットの項目を選択 |
| `Toolset.Editor.SlateInspector.FillForm` | 複数のフォームフィールドを 1 回の呼び出しで入力 |

> **Note**: `Toolset.Editor.SlateInspector.PressKey` はネイティブの `PressKey` と同じ危険ショートカットのブロックリストを適用しますが、現在どのウィジェットにフォーカスがあるかを解決する手段が無いため、**Backspace を常時ブロック**します — ネイティブコマンドが持つ「テキスト入力ウィジェットにフォーカスがある場合の例外」はブリッジには引き継がれません。

> **`Toolset.Editor.SlateInspector.SnapshotUI` は入力欄の行を伏せます。** エンジンが描画する行には各ウィジェットのラベルが入り、入力欄ではそれが入力中の文字列そのものです。UAIP は、入力欄（`SEditableText`・`SEditableTextBox`・`SMultiLineEditableText`・`SMultiLineEditableTextBox`）に属する行は、パスワード欄かどうかによらず、また Ref の接頭辞が `tb` の行も、ラベルを `"(withheld)"` に置き換えます。ウィジェットと結び付けられない行（Ref を引き当てられない、Ref が無い、ラベルを解析できない）も伏せます。ラベルの範囲すら分からない行は、行全体が `(withheld)` だけになります。それ以外の行と応答の形は変わりません。`Ref` が解決できなかったときの 1 行の応答 `Error: Could not resolve ref` は、そのまま返ります。エンジンの結果が UAIP の想定と違う形のときは、結果の一部も含まない固定の文で `InternalError` を返します。Ref を引き当てる部分が読み込まれていないときは、Ref のある行をすべて伏せます。入力欄に入っている値を読むには、ネイティブの `SnapshotUI` を `IncludeFieldValues` 付きで使ってください。パスワード欄を扱えるのはネイティブのコマンドだけです。**このマスクは最善の努力です。パスワード欄を扱うときは、ネイティブの `SnapshotUI` を使ってください。** エンジンが行を描画してから UAIP が伏せるので、伏せるかどうかは、その行の Ref が今引き当たるウィジェットで判断するしかありません。エディタの中で動くコードがもたらす行は覆えません。たとえば、他のプラグインが入力欄に `textbox` 以外のロールを与え（`RegisterWidgetRole`）、さらに Toolset の Ref のキャッシュをリセットして、その行の Ref が入力欄でない別のウィジェットを指すようになった場合や、他のプラグインが上の 4 つの入力欄の型以外の型にラベルの抽出器（`RegisterLabelExtractor`）を登録して欄の値を返す場合です。UAIP は、エディタのプロセスの中で動くコードを信頼する側として扱います（[安全性と Capability](safety.md#エディタ操作) を参照）。

> **⚠️ Breaking change — このセクションの 10 件は、これまで 1 件も動いていませんでした。** 委譲先の toolset 名を**モジュール修飾なしの `SlateInspectorToolset`** として渡しており、ToolsetRegistry は 1 回の完全一致検索でしか解決しないため（前方一致もサフィックス一致もありません）、正しい `SlateInspectorToolset.SlateInspectorToolset` に一致せず、どのコマンドも実行時に「そのような toolset は無い」で失敗していました。**本更新で 8 件が実際に動くようになりました**（`SnapshotUI` / `ListObservers` / `ClickWidget` / `HoverWidget` / `InputText` / `PressKey` / `SetComboSelection` / `FillForm`）。
>
> 残る 2 件、`ObserveWidget` と `UnobserveWidget` は**修飾名を直しても到達しません**。toolset が宣言しているのは `Observe` と `Unobserve` で、引数の形が違います（`Observe` はウィジェット ref と走査深さを取り、このコマンドが受け付ける observer 名を取りません。`Unobserve` は `Observe` が返した識別子で解除しますが、この経路の呼び出し元はその識別子を受け取りません）。名前を寄せるだけでは「到達はするが違うことをする」状態になるため、2 件とも `Available: false` と `UnavailableDetail: "DelegationTargetMissing"` を返します。`ObserveWidget` については **`UAIP.Editor.Observation.ObserveWidget`** が同じ操作をネイティブで行います。`UnobserveWidget` に対応するネイティブコマンドはありません。

---

## UAIP.Editor.Assets

アセットの開閉・検索・作成・複製・リネーム・削除、フォルダ管理。

| コマンド | 説明 |
|---|---|
| `OpenAsset` | 指定アセットをエディタで開く。エディタ状態の成果物は、フォーカス中のエディタのアセットを `ActiveAssetPath` として返す。⚠️ **非推奨のフィールド:** 同じ成果物の `ActiveTabId` もそのアセットのパスを持つ（`DumpEditorState` が同じ名前で返す Slate レイアウト識別子ではない）。次の MAJOR でレイアウト識別子に切り替わるため、`ActiveAssetPath` を読むこと。成果物の `DeprecatedFields` 配列が同じことを機械可読な形で示す。エディタを `-uaip-active-tab-id-as-layout-id` 付きで起動すると、切り替え後の意味を先行して試せる（1.x の間だけ提供） |
| `CloseAsset` | 指定アセットの全エディタを閉じる |
| `SaveAsset` | 名指ししたアセットだけをディスクへ書き込む（`AssetMutate` 必要）。確認ダイアログを出さないため非対話でも完結する |
| 🆓 `ListDirtyPackages` | 未保存の変更を持つパッケージを列挙する（保存前の事前確認用） |
| 🆓 `SearchAssets` | パス・クラス・タグでアセットを検索 |
| `CreateAsset` | 指定クラスの新規アセットを作成。`AssetPath` に既にアセットがある場合（保存済みかどうか・クラスを問わない）は `InvalidParams` で断り、何も作らず既存のアセットにも触れず、上書き確認ダイアログも出ません。先に削除するか別のパスを指定してください。レジストリが既存アセットを把握している場合は、応答の `Result` にそのクラスが `ExistingClassName` として入ります。Factory が `ClassName` と違うクラスのアセットを作った場合、またはアセット種別ごとの後処理に失敗した場合は、作成したアセットを破棄してからエラーを返します。破棄できなかったときはエラーにその旨が書かれ、`Result.RemainingAssetPath` が残っている場所を示します。要求した種類を無視して常に普通の Blueprint を作る汎用の Blueprint Factory は、特定の種類の Blueprint では候補から外れます（`/Script/Engine.Blueprint` 自体では今までどおり使えます）。`/Script/Engine.Blueprint` を指定した次の 2 つの要求は、何も作る前に `InvalidParams` で断ります。汎用の Factory は、そのままだと別の種類のアセットを、その種類に必要な検査を通さずに作ってしまうためです。エンジンが専用の Blueprint の種類を対応付けている `FactoryParams.ParentClass`（Animation Instance の派生は Animation Blueprint、User Widget の派生は Widget Blueprint など）には、代わりに使うクラスをメッセージと `Result.RequiredClassName` で返します（例: `/Script/Engine.AnimBlueprint`。そのクラスの Factory と受け取る `FactoryParams` は `ListFactoriesForClass` で調べられます）。`UControlRig` の派生を `ParentClass` に渡した場合は、使うべき Control Rig のクラスを挙げるメッセージで断ります（`Result.RequiredClassName` は付きません）。Actor など専用の種類が要らない親と、`ParentClass` の省略は、今までどおり作れます。Control Rig については [Control Rig アセットの形式](#control-rig-アセットの形式) を参照 |
| 🆓 `ListCreatableAssetClasses` | `CreateAsset` が作成可能な全 UClass をFactory数・デフォルトFactory付きで返す（重い呼び出し） |
| 🆓 `ListFactoriesForClass` | 指定 `ClassName` に対応する Factory 候補と各 `FactoryParams` スキーマを返す。汎用の Blueprint Factory は、特定の種類の Blueprint では一覧に出なくなりました（`CreateAsset` を参照） |
| `DuplicateAsset` | 既存アセットを複製 |
| `CopyAsset` | アセットを新しい完全パッケージパスへコピー（コピー先が存在する場合は失敗・`AssetCreate` 必要） |
| `RenameAsset` | アセットをリネーム / 別パスへ移動。`DisableSave` が有効なときは `PolicyViolation` で拒否 |
| `MoveAsset` | 名前を維持したままアセットを別フォルダへ移動し、リダイレクタが残ったかを報告（`AssetMutate` 必要）。`DisableSave` が有効なときは `PolicyViolation` で拒否 |
| `DeleteAsset` | アセットを削除。`DisableSave` が有効なときは `PolicyViolation` で拒否 |
| `CreateFolder` | Content Browser に新規フォルダを作成 |
| `DeleteFolder` | 空フォルダを削除（空でない場合 `NotEmpty`）。`DisableSave` が有効なときは `PolicyViolation` で拒否 |
| `ForceDeleteFolder` | フォルダと配下アセットを一括削除（50 件上限・外部参照チェックなし）。削除した・一部だけ削除した・フォルダが無い・上限を超えた、のどれでも成功を返し、どれだったかは `Result.Status`（`Deleted` / `PartiallyDeleted` / `NotFound` / `TooManyAssets`）に入る。削除まで進んだときは `DeletedAssetCount` / `FailedAssetCount` も入る。`DisableSave` が有効なときは `PolicyViolation` で拒否 |
| `MoveFolder` | フォルダ内の全アセットをサブフォルダ構造を保ったまま移動。部分失敗は `FailedAssets` に列挙（`AssetFolderRefactor` 必要）。`DisableSave` が有効なときは `PolicyViolation` で拒否 |
| 🆓 `GetSelectedAssets` | Content Browser で現在選択中のアセットを返す |
| `SelectAssets` | Content Browser で指定アセットを選択（`ContentBrowserNavigate` 必要） |
| 🆓 `GetContentBrowserPath` | Content Browser に現在表示されているフォルダパスを返す |
| `SetContentBrowserPath` | Content Browser を指定フォルダに移動（`ContentBrowserNavigate` 必要） |
| 🆓 `GetOpenAssets` | アセットエディタで現在開いているアセット一覧を返す |
| 🆓 `ListAssetRedirectors` | フォルダ配下（既定はプロジェクト全体の `/Game`）のアセットリダイレクタを、アセットをロードせずに元パス・先パス付きで一覧取得する |
| `FixAssetRedirectors`（`RedirectorFixup` 必要） | `/Game` 全体（常に再帰的）を対象に、解決可能なアセットリダイレクタを一括修正・削除する。`DisableSave` が有効なときは `PolicyViolation` で拒否 |
| `FixUpRedirectorsInFolder`（`RedirectorFixup` 必要） | 同じ修正処理を 1 フォルダに限定して実行。解決できなかったものは `FailedRedirectors` に返る。`DisableSave` が有効なときは `PolicyViolation` で拒否 |
| 🆓 `GetAssetReferences` | 指定アセットを起点に参照グラフ（参照元・参照先・両方）を指定深さまで探索する |
| 🆓 `GetAssetSizeMap` | フォルダ配下のディスクサイズ（任意で常駐メモリサイズ）をアセット単位で集計し降順ソートする |
| 🆓 `GetAssetSizeMapByClass` | フォルダ配下のディスクサイズをアセットクラス単位で集計し降順ソートする |
| 🆓 `FindUnreferencedAssets` | ⚠️ **非推奨** — 代わりに `StartAssetAudit` を使用。フォルダ配下でユーザー参照（Engine/Script以外）が存在しないアセットを検出する（ハードリファレンスヒューリスティック）。動作・進捗発火とも変更なし |
| 🆓 `FindCircularReferences` | ⚠️ **非推奨** — 代わりに `StartAssetAudit` を使用。フォルダ配下のアセット間の循環依存チェーンを検出する。動作・進捗発火とも変更なし |
| 🆓 `FindBrokenReferences` | ⚠️ **非推奨** — 代わりに `StartAssetAudit` を使用。アセットレジストリに存在しないパッケージへの依存を検出する。動作・進捗発火とも変更なし |
| 🆓 `GetAssetDependencyPath` | 2つのアセット間の最短依存/参照パスを検索する |
| 🆓 `RunAssetAudit` | ⚠️ **非推奨** — 代わりに `StartAssetAudit` を使用。フォルダ配下の複合監査（未参照アセット・循環参照・壊れた参照・最大サイズアセット）を実行する。動作・進捗発火とも変更なし。同期実行でゲームスレッドを完了まで占有するため、大規模プロジェクトでは数十秒〜数分エディタ（および他の UAIP コマンド）が固まることがある |
| 🆓 `StartAssetAudit` | 監査ジョブを開始し、`AuditId` を即座に返す。実際の走査はゲームスレッドを占有せず、エディタのフレームの合間で少しずつ進むため、エディタも他の UAIP コマンドも応答し続ける。パラメータ：`PackagePath`（必須）、`Recursive`（既定 `true`）、`Reports`（`UnreferencedAssets` / `CircularReferences` / `BrokenReferences` / `TopLargestAssets` の配列。既定は全 4 種 — 空配列を明示指定した場合は `InvalidParams`）、`MaxUnreferenced`（既定 `200`、範囲 `[1, 2000]`）、`MaxCycles` / `MaxBroken` / `MaxTopLargest`（`RunAssetAudit` と同じ既定値）。別の監査ジョブが実行中の場合は `TooManyRequests`、エディタがモーダルダイアログやスロータスクのプログレスバーを表示中の場合は `NotAllowed` を返す。**`SessionId` の明示指定が必須** — トランスポートが自動生成した匿名セッションは `InvalidParams` で拒否される（匿名で開始したジョブは後から照会・取得できなくなるため） |
| 🆓 `GetAssetAuditStatus` | `AuditId` で監査ジョブの状態を照会する — `State`（`Preparing` / `Running` / `Completed` / `Failed`）、現在処理中のレポート種別、処理済み/総件数、経過秒数、失敗時の理由を返す。実行コストはジョブ規模に依存しない（O(1)）。**開始時と同じ `SessionId` が必須** — 未知・期限切れ・他セッションの `AuditId` はいずれも区別されず `NotFound` になる |
| 🆓 `GetAssetAuditResult` | 完了した監査ジョブの成果物参照を `AuditId` で取得する。取得したいレポートを `Reports` で絞り込むこともできる（省略時は開始時に要求した全レポート。開始時に要求していないレポートを指定した場合はエラーにはならず「要求されていない」扱いで未取得側に分類される）。O(1)。状態が `Completed` に達していない場合は現在の `State` とともに `ExecutionFailed` を返す。**開始時と同じ `SessionId` が必須** |
| 🆓 `ListPrimaryAssetTypes` | 登録済みの全 `PrimaryAssetType`（`UAssetManager`）をクラス・ディレクトリ・アセット数サマリー付きで一覧取得する |
| 🆓 `GetPrimaryAssetTypeInfo` | 単一の `PrimaryAssetType` の詳細（ディレクトリ・個別アセット・既定Rule）を取得する |
| 🆓 `ListPrimaryAssets` | 指定 `PrimaryAssetType` に属する `PrimaryAssetId` とアセット一覧を取得する |
| 🆓 `GetAssetBundle` | 指定 `PrimaryAssetId` の `AssetBundle` エントリを取得する（未定義なら空配列） |
| 🆓 `GetAssetTags` | アセットの Asset Registry タグマップを取得する |
| 🆓 `GetPrimaryAssetIdForPath` | アセットパスから `PrimaryAssetId` を逆引きする（未登録時は `Found:false` でエラーにしない） |
| 🆓 `GetPrimaryAssetRules` | 指定 `PrimaryAssetId` のマージ済み（Type既定 + 個別上書き）`PrimaryAssetRules` を取得する |
| 🆓 `GetManagedPackageList` | 指定 `PrimaryAssetId` が管理するパッケージ一覧を取得する |
| 🆓 `GetPrimaryAssetLoadList` | 指定 Bundle 条件下で実際にロードされるオブジェクトパスを解決する |
| 🆓 `GetLoadedPrimaryAssets` | 現在ロード中/ロード予定の `PrimaryAssetId` とそのロード済み Bundle 状態を取得する |
| `AddPrimaryAssetType`（要 `PrimaryAssetTypeAdd`） | `PrimaryAssetType` を `PrimaryAssetTypesToScan` に追加（`DefaultGame.ini` へ永続化）し即座にスキャンする |
| `RemovePrimaryAssetType`（要 `PrimaryAssetTypeRemove`） | `PrimaryAssetType` を `PrimaryAssetTypesToScan` から削除（永続化）する。アセットが存在する場合は `Force` 指定がない限り拒否 |
| `SetPrimaryAssetRules`（要 `PrimaryAssetRulesOverride`） | 指定 `PrimaryAssetId` の Rule をメモリ内のみ一時的に上書きする（非永続） |
| `LoadPrimaryAsset`（要 `PrimaryAssetLoad`） | `PrimaryAsset` を明示的にメモリへロードする（ノンブロッキング、PIE中も許可） |
| `UnloadPrimaryAsset`（要 `PrimaryAssetUnload`） | `PrimaryAsset` を明示的にメモリからアンロードする（PIE中は拒否） |

> **フォルダを受け取るパラメータは、コンテンツのルートそのものを受け付ける。** `SearchAssets`・`ListAssetRedirectors`・`GetAssetSizeMap`・`GetAssetSizeMapByClass`・`StartAssetAudit`・`RunAssetAudit`・`FindUnreferencedAssets`・`FindCircularReferences`・`FindBrokenReferences` は、`PackagePath` / `FolderPath` に `/Game`（またはプラグインのコンテンツのルート。たとえば `/MyPlugin`）を、`/Game/` やその下のフォルダと同じように渡せる。末尾の `/` は外され、フォルダは末尾の `/` が無い形で扱われる（`ListAssetRedirectors` は応答の `FolderPath` にもその形を返す）。マウントされたルートでもその下でもないパスや空の文字列は `InvalidParams` で、エラー文に引数名と渡された値が入る（`'PackagePath' value '…': <理由>`）。`StartValidationJob` も `PackagePath` にコンテンツのルートを同じように受け付ける。アセット 1 件のパスを求めるコマンドは変わらず、ルートそのものはそこでは拒否される。
>
> **Content Browser のコマンドは、Content Browser があるかどうかを示す。** `GetSelectedAssets`・`SelectAssets`・`GetContentBrowserPath`・`SetContentBrowserPath` は、Content Browser のモジュールが読み込まれていない環境では、コマンド一覧で使えないもの（`Available: false`、`UnavailableReason: HandlerUnavailable`、`UnavailableDetail: ExecutionEnvironment`）として示され、呼ぶ前に分かる。以前は使えるものとして示され、呼ぶと断られていた。Toolset ブリッジ側（`Toolset.Editor.Toolset.Assets.GetContentBrowserPath` など）は対象外で、可否は Toolset 連携に従う。

> **Note**: `StartAssetAudit` は**ジョブ型コマンド**の一例で、呼び出しをブロックせずに即座に応答を返し、実際の処理はエディタのフレームをまたいで進む。`uaip_execute` の呼び出しに MCP の `_meta.progressToken` を添えると、応答待ちの間ブリッジがおよそ 5 秒おきに `notifications/progress` を送出する。内容は経過秒数とエディタ自身の状態（`STARTING` / `RUNNING` / `UNRESPONSIVE`）のみで、**ジョブ内部の進捗は含まれない**（それを知りたい場合は `GetAssetAuditStatus` をポーリングする）。この仕組みは `uaip_execute` にのみ適用され（`uaip_run_scenario` は対象外）、クライアントが進捗トークンを送った場合にのみ働く。また、届いた通知を実際に表示するかどうかは MCP クライアント側の実装による。監査ジョブが 1 フレームあたり走査に使う時間の上限は `Config/DefaultUAIP.ini` の `[UAIP.Jobs] AuditStepBudgetMs` で変更できる（既定 `10.0`、`[1.0, 100.0]` の範囲にクランプされる。範囲外を指定してもエラーにはならず自動的に範囲内へ収められる）。


> **Note**: 保存には `SaveAsset` と `UAIP.Editor.Workspace.SaveAllPackages` の 2 つがあり、影響範囲が異なる。`SaveAllPackages` は**未保存のパッケージをすべて**書き込むため、人が編集途中で放置していた無関係な変更まで一緒に確定してしまう。対象が分かっているなら `SaveAsset` で名指しすること。何が書き込まれるかを事前に知りたい場合は `ListDirtyPackages` を呼ぶ — これはエディタ全体保存が参照するのと同じ情報源（`GetDirtyContentPackages` / `GetDirtyWorldPackages`）を使うため、返る一覧と `SaveAllPackages` が書き込む集合は一致する。
>
> `SaveAsset` が対象にするのは**ロード済みかつ未保存の変更を持つパッケージだけ**。未ロードのアセットは未保存の変更を持ちようがないため、ロードして書き戻すことはせず `Skipped`（`Reason: "NotLoaded"`）として返る。すでに保存済みのものも `Skipped`（`NotDirty`）になる。どちらもエラーではない。`/Engine/` と `/Script/` 配下はプロジェクト外へ影響するため `Failed`（`WriteForbidden`）として拒否されるが、呼び出し全体は失敗せず、他のアセットの保存はそのまま行われる。SafetyPolicy が `DisableSave=True` の場合のみ呼び出し全体が `PolicyViolation` になる。
>
> **`ApplyValidationFix` との関係**: バリデータが提供する修正が `FAutoSavingFixer` で包まれていても、UAIP 経由の適用では**ディスクへ書き込まれない**。エンジンの自動保存が人間の確認を求めるモーダルダイアログ経由であり、応答する人がいない非対話実行では成立しないため。この場合 `ApplyValidationFix` は `Applied: true` と `AssetSaved: false` を返すので、**`AssetSaved` が `false` なら `SaveAsset` で明示的に保存する**こと。

> **Note — `FactoryParams` で名指しするクラス自体が Capability を要求することがあります。** 一部のドメインは、ここで名指しされたクラスを、そのドメインの編集コマンドと同じポリシーで審査します — 現時点では StateTree の `FactoryParams.SchemaClass` と ControlRig の `FactoryParams.ParentClass` が該当します。Blueprint 自身の `FactoryParams.ParentClass`（省略可能、既定は `AActor`）と Anim Blueprint の `FactoryParams.TargetSkeleton`（必須）は**この対象ではなく**、`AssetCreate` 以外の Capability を要求しません。どちらもオンデマンドには読み込まれなくなりました。すでにメモリ上にないクラスは、呼び出し側がその名前を指定できるかを判定するためだけに読み込まれることなく、未解決として拒否されます。名指しされたクラスが要求する Capability をセッションが持っていない場合、`CreateAsset` は **`CapabilityNotAvailable`** を返し、不足している Capability 名はメッセージ本文に入ります — 他の経路と同じ扱いです。詳細は [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照してください。

### Toolset ブリッジ — Assets（6 件）🧩

`EditorAppToolset`（UE 5.8+、EditorToolset プラグイン）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.Toolset.Assets.*`。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.Toolset.Assets.GetSelectedAssets` | Content Browser で選択中のアセットを取得 |
| `Toolset.Editor.Toolset.Assets.SelectAssets` | Content Browser でアセットを選択（`ContentBrowserNavigate` 必要） |
| `Toolset.Editor.Toolset.Assets.GetContentBrowserPath` | Content Browser の現在フォルダパスを取得 |
| `Toolset.Editor.Toolset.Assets.SetContentBrowserPath` | Content Browser を指定フォルダに移動（`ContentBrowserNavigate` 必要） |
| `Toolset.Editor.Toolset.Assets.OpenEditorForAsset` | アセットをエディタで開く（`AssetWindowControl` 必要） |
| `Toolset.Editor.Toolset.Assets.GetOpenAssets` | アセットエディタで開いているアセットの一覧 |

---

## UAIP.Editor.SemanticSearch 🧩

セマンティックアセット検索とインデックス管理。`SemanticSearch` プラグイン（UE 5.8+、Experimental）と、エディタ環境設定 → プラグイン → Semantic Search で設定した OpenAI API キーが必要です。

| コマンド | 説明 |
|---|---|
| `Search` | 自然言語クエリでプロジェクトアセットを検索（BM25+ベクトルハイブリッド、最大 500 件） |
| `FindSimilar` | 参照アセットに類似するアセットをベクトル類似度で検索 |
| `GetIndexStats` | 現在のインデックス統計（アセット数・最終構築日時）を返す |
| `StartIndexing` | セマンティックインデックスの完全再構築をトリガー（長時間処理・`SemanticSearchEdit` 必要） |
| `CancelIndexing` | 実行中のインデックス構築をキャンセル（`SemanticSearchEdit` 必要） |

### Toolset ブリッジ（2 件）🧩

`SemanticSearchToolset` プラグイン（UE 5.8+）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.SemanticSearch.*`。上記のネイティブ `Search` / `FindSimilar` に相当し、Toolset ブリッジ専用として提供されます（これら 2 件には対応する UAIP ネイティブコマンドは存在しない。ADR `2026-06-25-SemanticSearchToolset-BridgeOnly-Exception.md` 参照）。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.SemanticSearch.Search` | SemanticSearchToolset 経由の BM25+ベクトルハイブリッド検索 |
| `Toolset.Editor.SemanticSearch.FindSimilar` | SemanticSearchToolset 経由のベクトル類似度検索 |

---

## UAIP.Editor.Level

Editor 上でのアクター配置・トランスフォーム・レベルロード。

| コマンド | 説明 |
|---|---|
| 🆓 `ListLevelActors` | 開いているレベルのアクター一覧 |
| `PlaceActorInLevel` | Editor レベルにアクターを配置 |
| `DeleteActorFromLevel` | Editor レベルからアクターを削除 |
| 🆓 `GetActorTransform` | Editor 上のアクターのトランスフォーム取得 |
| `SetActorTransform` | Editor 上のアクターのトランスフォーム設定 |
| `OpenLevel` | エディタビューポートでレベルを開く（File > Open Level） |
| `NewLevel` | テンプレートから新規レベルを作成（EmptyLevel / EmptyOpenWorld / Basic / OpenWorld） |
| `SelectActors` | 指定アクターを Editor レベルで選択（既存選択を置換または追加） |
| 🆓 `ListSelectedActors` | 現在 Editor で選択中のアクター一覧を返す |
| `ClearSelection` | Editor レベルの選択をクリア |
| `FocusOnActors` | 指定アクターにビューポートカメラをフォーカス（アクター省略時は選択中のアクターを対象） |
| 🆓 `GetCameraTransform` | アクティブなレベルエディタビューポートのカメラ位置・回転を取得 |
| `SetCameraTransform` | アクティブなレベルエディタビューポートのカメラ位置・回転を設定 |
| 🆓 `GetVisibleActors` | アクティブなエディタビューポートに現在表示されているアクターを返す（視錐体カリング） |
| 🆓 `ProjectWorldToScreen` | ワールド空間の位置をスクリーン座標に投影 |
| 🆓 `ProjectScreenToWorld` | スクリーン座標からワールドにレイをキャスト（ECC_Visibility ライントレース） |
| 🆓 `GetTransformGizmoSize` | トランスフォームギズモの大きさの設定と、使用中のギズモがどれを読むかを返す。`AxisSizeMultiplier`（TRS ギズモの倍率。UE 5.8 の既定）、`LegacySizeOffset`（旧ギズモのオフセット）、`GizmoVersion` / `UsesNewTRSGizmos`（使用中のギズモの種類）、`EffectiveSetting`（`AxisSizeMultiplier` / `LegacySizeOffset`、判断できない場合は `Unknown`）。UE 5.7 には倍率が無く、`GizmoVersion` と `AxisSizeMultiplier` は返らず、代わりに `AxisSizeMultiplierUnavailableReason` が理由を示す。新しいギズモを使っている場合の `EffectiveSetting` は `Unknown`。`EditorInspect` 必要 |
| `SetTransformGizmoSize` | ギズモの大きさを設定し、エディタ設定に保存してビューポートを描き直す。`AxisSizeMultiplier`（0.1〜10）は TRS ギズモの倍率、`LegacySizeOffset`（-10〜150）は旧ギズモの大きさに足すオフセット。どちらか一方または両方を指定する。両方を検証してから書くので、範囲外・数値でない値・無限大・どちらも未指定は、何も書かずに `InvalidParams` で断られる。応答には書いた欄（`Applied`）と `EffectiveSetting` が入る。描画が変わるのは今のギズモが読む方だけで、効いていない方だけを書いた場合は値を保存し、`Note` で「今のギズモは別の値を読んでいる」と知らせる（`EffectiveSetting` が `Unknown` のときは `Note` なし）。UE 5.7 では `AxisSizeMultiplier` を含む呼び出しは、エンジンの版が理由と分かる文の `InvalidParams` で呼び出し全体を断り、`LegacySizeOffset` だけなら書ける。同じ設定は `UAIP.Editor.Sequencer.SetAnimModeGizmoScale` でも書ける。`EditorViewportControl` 必要 |
| 🆓 `ListActorComponents` | レベルに配置済みのアクターが持つコンポーネントを列挙。各エントリは以下の 3 コマンドが受け取る `ComponentId` に加え、`ComponentClassPath`・`Origin`（`Instance` / `SimpleConstructionScript` / `UserConstructionScript` / `Native`）・`IsEditableInstance`・`IsSceneComponent`・`IsRootComponent`・`AttachParentComponentName`・`AttachSocketName` を返す。さらに各エントリは、そのクラスのコンポーネントを**追加**するのに何が要るかを `Admission`（`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`）・`RequiredCapabilities`・`MissingCapabilities` として返す — `ComponentCustomTypeEdit` が要るかどうかを書き込みを試す前に確認できるのはこれによる。エディタワールドを読むため PIE 中も応答する。`EditorInspect` が必要。`ComponentId` は不透明で、すでにエスケープ済みの識別子。他のコンポーネント系コマンドにそのまま渡し、手で組み立てたり編集したりしない |
| `AddActorComponent` | レベルに配置済みのアクターにコンポーネントを追加（Details パネルの *Add Component* ボタン相当）。1 つの Undo ステップとして記録され、新しい `ComponentId` を返す。`ComponentName` は省略するとエンジンが命名する。`AttachParentComponentName` / `AttachSocketName` は `USceneComponent` 派生にのみ適用され、アクターにルートが無い場合は新しいコンポーネントがルートになる。クラスは既にロード済みのものからのみ解決し、要求に応じたロードは行わない（未ロードのクラスは `NotFound`）。`ActorComponentEdit` が必要で、`/Script/Engine` と `/Script/LiveLinkComponents` 以外のクラスにはさらに `ComponentCustomTypeEdit` が必要 — [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照。PIE 中は拒否 |
| `DeleteActorComponent` | レベルに配置済みのアクターからインスタンスコンポーネントを削除。1 つの Undo ステップとして記録される。削除できるのは `Origin: Instance` のみ — SCS のものは Blueprint コンポーネントコマンドの担当、コンストラクションスクリプト由来のものはスクリプトが作り直し、Native のものはそのクラスの全インスタンスに存在するため、いずれも「どの経路が担当か」を示して拒否する。アクターの `DefaultSceneRoot` も拒否対象。削除したシーンコンポーネントの子は、ワールドトランスフォームを保ったままその親へ付け替えられる。`ExpectedComponentClass` は必須（一覧が返した `ComponentClassPath` をそのまま渡す）で、古くなった識別子は追従せず `NotFound` で拒否する。`ActorComponentEdit` が必要。PIE 中は拒否 |
| `ReparentActorComponent` | レベルに配置済みのアクターのシーンコンポーネントを、同じアクターの別のコンポーネントの下へ、ワールドトランスフォームを保ったまま付け替える。1 つの Undo ステップとして記録される。両方が同一アクター上の `USceneComponent` 派生で、動かす側は `Origin: Instance` である必要がある。「どこにも付いていない」状態は表現できず、切り離しはアクターのルートを `NewParentComponentName` に指定して表す。ルート自身は動かせない。循環になる付け替えと、新しい親に存在しないソケットは、書き込み前に拒否される。`ExpectedComponentClass` は上と同様に必須。`ActorComponentEdit` が必要。PIE 中は拒否 |
| 🆓 `GetActorComponentProperty` | レベルに配置済みのアクターが持つコンポーネントのプロパティ値を、`ListActorComponents` / `AddActorComponent` が返す `ComponentId` で指定して読み取る — `GetActorProperty` は、アクターがコンポーネントを保持するオブジェクト参照を辿るパスを拒否するため、これが唯一の到達手段になる。`Value`・`PropertyType`・`Origin`、および `WriteRequirements`（そのプロパティへの書き込みが `ActorComponentEdit` に加えて何を要求するか、このセッションが既に持っているものと不足しているものに分けたもの、書き込みがそもそも可能かどうか、`SetActorComponentProperty` の 2 つの値パラメータのどちらで渡す必要があるか）を返す。`ExpectedComponentClass` は必須で、古くなった `ComponentId` は追従せず拒否する。どの `Origin` のコンポーネントも読み取れる。エディタワールドを読むため PIE 中も応答する。`EditorInspect` が必要。`ComponentId` は不透明で、すでにエスケープ済み。`ListActorComponents` が返した形のまま渡す シークレットのプロパティ、またはパスの途中に秘密の親があるものは `***` で返る（以前、コンポーネントの読み取りはマスクされなかった）。`IncludeSecretValues` を取る — [シークレット値の読み取り](#reading-secret-values)を参照 |
| `SetActorComponentProperty` | レベルに配置済みのアクターが持つコンポーネントへプロパティ値を書き込む。指定方法は `GetActorComponentProperty` と同じで、1 つの Undo ステップとして記録される。値は UE インポートテキストとして `Value`、または JSON として `ValueJson` で渡し、`Operation` / `ElementIndex` / `ElementKeyJson` で値全体の置換ではなくコンテナの要素 1 つだけを操作できる — これらのパラメータと、参照・複合値の書き込みに追加で必要な Capability（先に `GetActorComponentProperty` を呼べば分かる）については [参照・構造体・コンテナの書き込み](#参照構造体コンテナの書き込み) を参照。`ExpectedComponentClass` は上と同様に必須。コンポーネントの `Origin` が `UserConstructionScript` の場合は拒否される — そのスクリプトが次回実行されると書き込みが失われるため。`ActorComponentEdit` が必要。PIE 中は拒否 |

> **Note — インスタンス側専用です。** この 6 コマンドが対象とするのは、**レベルに配置済みのアクター**が持つコンポーネントです（`GetActorComponentProperty` は、コンストラクションスクリプトが所有するものを含め、どの `Origin` のコンポーネントも読み取れる — 書き込みだけが拒否される）。アクターの Blueprint 側に宣言されたコンポーネントは [UAIP.Editor.Blueprint — コンポーネント — SCS](#コンポーネント--scs8) を使ってください。インスタンス側にリネームと複製に相当する操作はありません（望む名前を指定して追加し直してください）。

> **Note — GeometryCollection コンポーネントの `RestCollection` の書き込み。** `SetActorComponentProperty` が GeometryCollection コンポーネントの `RestCollection` を書き、値が実際に変わった場合、書き込みは単純なプロパティ代入ではなくエンジンの `SetRestCollection` を通して確定されます。そのため、アセットの既定値（ダメージ設定など）がコンポーネントに取り込まれます。順序が重要です。`RestCollection` を先に書いてからダメージ設定を書く順なら、書いた設定が残ります。逆の順だと、ダメージ設定はアセットの値で上書きされます。値が変わらない書き込み（同じアセットの書き直し）では、既定値の取り込みは起きません。

### Toolset ブリッジ — Level（8 件）🧩

`EditorAppToolset`（UE 5.8+、EditorToolset プラグイン）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.Toolset.Level.*`。

> ⚠️ **`SelectActors` と `FocusOnActors` は `Actors` を、アクターのパス文字列または `{"refPath": ...}` を要素とする配列で受け、ブリッジが各要素を `{"refPath": ...}` にして送ります。** 空文字列・`null`・`{"refPath": ""}`・数値・`refPath` の無いオブジェクトの要素は除いて、残りを送ります。除いた結果が空の配列は空配列として送られます（`SelectActors` では、空配列は選択の全解除です）。⚠️ `Actors` が `null`・省略・配列でないときは、Toolset を呼ぶ前に `InvalidParams` で断ります。以前の `SelectActors` は `null` を「選択の全解除」として扱いましたが、配列の渡し忘れで選択が黙って消えてはならないので断ります。全解除したいときは `[]` を渡してください。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.Toolset.Level.GetSelectedActors` | Level Editor ビューポートで現在選択中のアクターを返す |
| `Toolset.Editor.Toolset.Level.SelectActors` | Level Editor で指定アクターを選択（`EditorActorEdit` 必要） |
| `Toolset.Editor.Toolset.Level.GetCameraTransform` | アクティブビューポートのカメラトランスフォームを取得 |
| `Toolset.Editor.Toolset.Level.SetCameraTransform` | アクティブビューポートのカメラトランスフォームを設定（`EditorViewportControl` 必要） |
| `Toolset.Editor.Toolset.Level.FocusOnActors` | 指定アクターにビューポートをフォーカス（`EditorViewportControl` 必要） |
| `Toolset.Editor.Toolset.Level.GetVisibleActors` | アクティブビューポートに表示されているアクターの一覧 |
| `Toolset.Editor.Toolset.Level.WorldPosToScreenCoords` | ワールド位置をスクリーン空間に投影 |
| `Toolset.Editor.Toolset.Level.ScreenCoordsToWorld` | スクリーン座標をワールド空間に投影（`EditorInspect` 必要） |

---

## UAIP.Editor.Property

アクター・アセット・Blueprint デフォルト・DataTable 行・World / Project 設定のプロパティ読み書き。`Get*` 系コマンドは、シークレットらしきプロパティ値（名前がシークレットパターンに一致・シークレットメタデータあり・ファイルパス型）をネストした struct メンバーも含めて `***` でマスクする — シークレットなメンバーを内包する複合値（struct 等）は、その部分だけでなく値全体がマスク対象になる。`Set*` 系コマンドは、テキスト値 `Value` で 17 種の struct 型（ベクトル・回転・Transform・カラー・`FGuid`・区間型・`FGameplayTag` / `FGameplayTagContainer` / `FGameplayCueTag`・`FBoneReference` など）と `int8` から `uint64` までの全整数幅を書き込める。配列・マップ・セット・オプショナル・その他の構造体・オブジェクト参照は `ValueJson` で渡し、コンテナの要素 1 つだけを `Operation` / `ElementIndex` / `ElementKeyJson` で操作できる — パラメータと、これらを制御する 2 つの Capability（`PropertyReferenceEdit` / `PropertyStructuredEdit`）については [参照・構造体・コンテナの書き込み](#参照構造体コンテナの書き込み) を参照。 シークレットかどうかはパス全体で判定する。パスの途中のどれか 1 つでも秘密なら（`MyPath.FilePath` など）値はマスクされる（以前は末端だけを見ていた）。エンジンのパスワード欄の印 `meta=(PasswordField=true)` と、CryptoKeys の `EncryptionKey`・`SigningPrivateExponent`・`SecondaryEncryptionKeys` も秘密として扱う。以下の `Get*` 6 本は `IncludeSecretValues` で平文を `Result.SecretFieldValues` に返せる — [シークレット値の読み取り](#reading-secret-values)を参照。

| コマンド | 説明 |
|---|---|
| 🆓 `GetActorProperty` | Editor アクターのプロパティ値を取得 `IncludeSecretValues` を取る |
| `SetActorProperty` | Editor アクターのプロパティを設定 |
| 🆓 `GetWorldSetting` | WorldSettings のプロパティ値を取得 `IncludeSecretValues` を取る |
| `SetWorldSetting` | WorldSettings のプロパティを設定 |
| 🆓 `GetAssetProperty` | アセット（DataAsset 等）のプロパティ値を取得 `IncludeSecretValues` を取る |
| `SetAssetProperty` | アセットのプロパティを設定し `MarkPackageDirty` を呼ぶ |
| 🆓 `GetBlueprintDefault` | Blueprint CDO のプロパティ値を取得 `IncludeSecretValues` を取る |
| `SetBlueprintDefault` | Blueprint CDO のプロパティを設定 |
| 🆓 `GetProjectSetting` | `UDeveloperSettings` CDO のプロパティ値を取得 `IncludeSecretValues` を取る |
| `SetProjectSetting` | `UDeveloperSettings` CDO のプロパティを設定し `SaveConfig()` を呼ぶ |
| 🆓 `GetDataTableRow` | DataTable 行のプロパティ値を取得 `IncludeSecretValues` を取る |
| `SetDataTableRow` | DataTable 行のプロパティを設定 |

**失敗の結果コード。** `Get*` コマンドは、プロパティ経路を対応する `Set*` コマンドと同じ `ErrorCode` で断ります。プロパティが無いときは `NotFound`、経路の書式の誤り・深すぎる経路・範囲外の添字・たどれないものを経由する経路（添字なしの構造体の固定長配列など）は `InvalidParams` です。⚠️ これらの読み取りは、以前は理由によらず `ExecutionFailed` を返していました。対象そのもの（アクター・アセット・Blueprint・行・設定のオブジェクト）が見つからないときは、読み取りも書き込みも従来どおり `ExecutionFailed` を返します。次の 2 つのドメインはプロパティ経路について独自の結果コードのままで、理由はメッセージで示します。`GetDataflowNodeProperty` / `SetDataflowNodeProperty` は `InvalidParams`、`GetSectionProperty`（`UAIP.Editor.Sequencer`）は `ExecutionFailed` を返します。

**断られた書き込みは何も変えません。** `Set*` コマンドが理由を問わず断られたとき、対象の値は変わらず、そのパッケージの未保存の印も呼び出し前のままです（保存済みのパッケージは保存済みのまま）。`SetActorComponentProperty`（`UAIP.Editor.Level`）も同じです。

---

## UAIP.Editor.Blueprint

Blueprint 変数・イベントグラフノード・SCS コンポーネントの編集。

### アセット作成（1）

| コマンド | 説明 |
|---|---|

### 変数とグラフ（11）

| コマンド | 説明 |
|---|---|
| `AddBlueprintVariable` | Blueprint にメンバー変数を追加（型・デフォルト・Tooltip）。Blueprint で変数の型として使えない型は、エディタの変数型メニューと同じ規則で `InvalidParams` として拒否されます。クラスは自身または祖先に `BlueprintType`（または `BlueprintSpawnableComponent`）が必要で、`NotBlueprintType` のものは拒否されます。構造体は `BlueprintType` が必要で、`BlueprintInternalUseOnly` のものは拒否されます。拒否された呼び出しは Blueprint を変更しません（変数は追加されず、アセットも dirty になりません）。デフォルト値は変数の型が確定してから検証されるようになり、拒否された場合は **変数の追加ごと取り消されます**（空の値を持つ変数が残ることはありません）。デフォルト値はエンジンのテキスト形式のみを受け取るため、参照・コンテナのデフォルトはどの Capability を付与しても拒否されます — その場合は追加後に `ValueJson` を受け取る `SetBlueprintDefault` で設定してください |
| `DeleteBlueprintVariable` | メンバー変数を削除 |
| `SetBlueprintVariableDefault` | Blueprint 変数の CDO デフォルト値を更新 |
| `AddGraphNode` | Blueprint アセットの**あらゆるグラフ**にノードを追加（VariableGet/Set・FunctionCall・EventBeginPlay/EventTick、または親やインターフェースのイベントを上書きする `Event`）— イベントグラフと関数グラフに限らない。対象は `GraphName` または `GraphGuid` で選ぶ。グラフの選び方・複数一致時の扱い・2 段階の受け入れ判定は表の下の注記を参照 |
| `AddFunctionOverride` | 値を返す・出力引数を持つ・const の、親クラスかインターフェースの関数を、Override メニューと同じく関数グラフとして上書きする。グラフと、その入口・結果ノードの GUID を返す |
| `DeleteGraphNode` | グラフノードを GUID 指定で削除（EntryNode・Tunnel は削除不可） |
| `ConnectBlueprintPins` | Blueprint グラフの 2 ピンを接続 |
| `DisconnectBlueprintPins` | ピン接続を切断 |
| `ListBlueprintPins` | Blueprint グラフノードのピン一覧 |
| `SetPinDefaultValue` | Blueprint グラフノードのピンにデフォルト値を設定（DefaultValue / DefaultObject / DefaultTextValue を型に応じて自動選択） |
| `GetPinDefaultValue` | Blueprint グラフノードのピンのデフォルト値を取得 |

> **新規 — `AddGraphNode` に `NodeType: "Event"` を渡すと、親クラスまたは実装しているインターフェースのイベントを `FunctionName` で指定してオーバーライドできる**（例: `ReceiveDestroyed`、`ReceiveActorBeginOverlap`）。My Blueprint パネルの Override メニューでイベントノードを追加するのと同じ動作。`EventBeginPlay` と `EventTick` はこれまでどおり使える。1 つの Blueprint で同じイベントをオーバーライドできるのは 1 回だけで、オーバーライドが Blueprint 内のどこかにすでにあるときは、2 つ目を作らずに既存のノードを返す。戻り値・出力パラメータを持つ関数や const 関数はイベントノードにできないため、`AddFunctionOverride` を案内する `InvalidParams` で拒否する。親クラスにもインターフェースにも `BlueprintImplementableEvent` / `BlueprintNativeEvent` として宣言されていない名前も `InvalidParams` で拒否する。
>
> **新規 — `AddFunctionOverride` は、そうした関数を関数グラフとしてオーバーライドする**（例: `ACharacter::CanJumpInternal`）。グラフには親のシグネチャどおりのエントリノードとリザルトノード、親実装の呼び出しが入り、`SkipCompile` が `true` でない限りコンパイルされる。artifact は `GraphName`・`GraphGuid`・`EntryNodeId`・`ResultNodeId`（戻り値が無い関数では省略）・`OverriddenClass`・`AlreadyExisted` を返す。グラフの中身は `AddGraphNode` と `ConnectBlueprintPins` で組む。同じ要求をもう一度送ると、既存のグラフを `AlreadyExisted: true` で返す。イベントノードにできる関数と、すでにイベントノードとしてオーバーライドされている関数は、`AddGraphNode` を案内する `InvalidParams` で拒否する。`BlueprintGraphEdit` が必要。

> **`AddGraphNode` は、イベントグラフと関数グラフだけでなくアセット内のすべてのグラフを見るようになった。** マクロ・インターフェース実装のグラフ・折りたたんだグラフの中にあるグラフも `GraphName` で指せるようになった — この変更より前は、グラフが実在していても `NotFound`（この変更より前は `ExecutionFailed`）で終わっていた。
>
> ⚠️ **破壊的変更 — `GraphName` の一致判定が大文字・小文字を区別しなくなった。** 従来は大文字・小文字まで一致しないと見つからなかったが、一致するようになった。アセット内に大文字・小文字だけが違う同名のグラフが 2 つある場合、**従来は正確な大文字・小文字で一致する片方だけが選ばれて成功していた呼び出しが、両方に当たるようになり、複数一致として断られる**（下記参照）ようになる。
>
> **`GraphGuid`（Optional String）は、名前の代わりに `UEdGraph::GraphGuid` でグラフを 1 つ選ぶパラメータで、`GraphName` と排他** — 両方指定すると `InvalidParams`。直前の呼び出しが同じ `GraphName` を複数一致として断っていない限り、指定する必要はない。
>
> **`GraphName` が複数のグラフに一致した場合、何も追加しない。** コマンドは `InvalidParams` を返し、`Result.MatchedGraphGuids` に候補となる各グラフの `GraphGuid`（文字列）が入る。そのいずれかをそのまま `GraphGuid` として渡し直せば、1 つに絞って対象にできる（加工は不要）。空の `GraphName` と文字列 `"EventGraph"` は影響を受けず、どちらも引き続きイベントグラフを直接選び、この複数一致判定には入らない。
>
> **ノードをその場所に置けるかどうかは 2 段階でチェックされ、これを行うのは `AddGraphNode` だけ**（この表の他のコマンドは、新しく置く場所を決めるのではなく既存のノード・ピンに対して操作するため、このチェックは行わない）:
> - *そもそもそのグラフが編集を受け付けるか？* イベントディスパッチャ自身の定義グラフ、インターフェースアセット自身が持つグラフ（インターフェースを実装した側の Blueprint にあるグラフは編集できる）、数式グラフ、エディタが内部的に生成したグラフは、いずれも `NotAllowed` で断る。
> - *この種類のノードがこの種類のグラフに置けるか？* ステートマシンの全体図（ステートと遷移が並ぶ画面）とブレンドスペースのグラフは、その組み合わせを `InvalidParams` で断る — グラフ自体は編集を受け付けるが、このノード種別は受け付けない。ここでの判定はエディタ自身のグラフスキーマがその組み合わせを受け入れるかどうかであり、置いた結果が実行時に意味を持つかどうかは判定しない（例: ステートの中身のポーズ評価グラフに一般的なノードを置くことはこの判定を通過するが、そこでは何も機能しない場合がある）。
>
> **存在しないグラフ名を指定した場合、`NotFound` を返すようになった**（従来は `ExecutionFailed`）— 同じ要求を繰り返しても成功しようがないため、シナリオの `RetryCount` がこれ以上無駄な再試行に使われることがなくなった。

> ⚠️ **破壊的変更 — `ConnectBlueprintPins` / `DisconnectBlueprintPins` / `DeleteGraphNode` / `GetPinDefaultValue` / `ListBlueprintPins` / `SetPinDefaultValue` は、指定したノードやピンが存在しないとき `NotFound` を返すようになった**（従来は `ExecutionFailed`）。シナリオの `RetryCount` は `ExecutionFailed` と `PreconditionFailed` だけを再試行対象にしており、この変更より前は存在しない `NodeId` や `PinName` を指定した要求も再試行の対象になっていた（同じ要求を繰り返しても成功しようがないにもかかわらず）。
>
> `GetPinDefaultValue` にはさらに、この変更で修正した欠陥がある。`PinName` が対象ノードのどのピンにも一致しない場合の分岐がそもそも無く、見つからなかったピンをそのまま読みに行く未検査のアクセス（未定義動作になりうる）になっていた。現在は、ノードのどのピンにも一致しない `PinName` に対して、この表の他のコマンドと同じく `NotFound` を返す。

### コンポーネント — SCS（8）

| コマンド | 説明 |
|---|---|
| `ListBlueprintComponents` | Blueprint から見える全コンポーネント一覧（SCS・Inherited・Native） |
| `AddBlueprintComponent` | Blueprint に新規 SCS コンポーネントノードを追加。⚠️ プロジェクト・プラグイン定義のコンポーネントクラスには `ComponentCustomTypeEdit` が追加で必要になりました — 下の Note を参照 |
| `DeleteBlueprintComponent` | SCS コンポーネントを削除 |
| `RenameBlueprintComponent` | SCS コンポーネントをリネーム |
| `ReparentBlueprintComponent` | SCS コンポーネントの親を変更。親を指定する場合はコンポーネントと親の双方が `USceneComponent` のサブクラスである必要がある。ルートレベルへの移動（`NewParentVariableName` が空）はどのコンポーネントクラスでも可能 |
| `DuplicateBlueprintComponent` | SCS コンポーネントを複製。⚠️ プロジェクト・プラグイン定義のコンポーネントクラスには `ComponentCustomTypeEdit` が追加で必要になりました — 下の Note を参照 |
| `GetBlueprintComponentProperty` | SCS コンポーネントのプロパティ値を取得 シークレットのプロパティ、またはパスの途中に秘密の親があるものは `***` で返る。`IncludeSecretValues` を取る — [シークレット値の読み取り](#reading-secret-values)を参照 |
| `SetBlueprintComponentProperty` | SCS コンポーネントのプロパティを設定。値はエンジンテキストなら `Value`、JSON なら `ValueJson` で渡し、`Operation` / `ElementIndex` / `ElementKeyJson` でコンテナの要素 1 つを操作できる — [参照・構造体・コンテナの書き込み](#参照構造体コンテナの書き込み) を参照 |

> ⚠️ **破壊的変更 — `AddBlueprintComponent` と `DuplicateBlueprintComponent` がコンポーネントクラスをゲートするようになりました。**
>
> **そのクラスのコンポーネントの数が増える**操作は、すべて同じ Capability 名で同じ判定を通るようになりました — 新設のインスタンス側 `AddActorComponent` と、この 2 つの Blueprint / SCS コマンドです。`/Script/Engine` と `/Script/LiveLinkComponents` が宣言するコンポーネントクラスは従来どおり `BlueprintComponentEdit` だけで通ります。**それ以外のクラス — プロジェクトの C++ が宣言したもの、他プラグイン（Niagara などエンジン同梱プラグインを含む）が宣言したもの、Blueprint 由来のコンポーネントクラス — には `ComponentCustomTypeEdit` が追加で必要**になり、セッションが保有していない場合は Capability 名を明示した `CapabilityNotAvailable` で拒否されます。
>
> **アップグレード時の影響**: これまで `BlueprintComponentEdit` だけでプロジェクト定義のコンポーネントを追加・複製できていたセッションは、拒否されるようになります。`Config/DefaultUAIP.ini` の `[UAIP.SafetyPolicy]` に `+AllowedCapabilities=ComponentCustomTypeEdit` を追加すると従来どおりに戻ります — [Safety & Capabilities](safety.md#level--アクター--プロパティ編集) を参照。
>
> **両方の経路を対象にした理由**: 片方だけをゲートしても、もう一方から同じクラスに到達できてしまうためです。**削除・リネーム・付け替え・プロパティ書き込みは対象外**です — いずれもそのクラスのインスタンス数を増やさないためです。この要件はコマンド実行中にクラスから決まるため、どちらのコマンドの `RequiredCapabilities` にも現れません。`ListActorComponents` がクラスごとに「追加に何が要るか」を返し、拒否時のメッセージも常に不足している名前を示します。

### コンパイル（2）

| コマンド | 説明 |
|---|---|
| `CompileBlueprint` | Blueprint をコンパイルし、CompileStatus + 構造化されたメッセージログを返す（AnimBlueprint・WidgetBlueprint は非対応） |
| `GetBlueprintCompileStatus` | コンパイルを実行せずに Blueprint の現在のコンパイル状態を取得する |

---

## UAIP.Editor.UMG

Widget Blueprint 編集 — ツリー・変数・アニメーション・バインディング。

### ネイティブ（22）

| コマンド | 説明 |
|---|---|
| `CreateWidgetBlueprint` | Widget Blueprint アセットを新規作成 |
| `AddWidget` | Widget Blueprint ツリーにウィジェットを追加 |
| `RemoveWidget` | ツリーからウィジェットを削除 |
| `MoveWidget` | ウィジェットを同一パネル内で並び替え / 別パネルへ移動 |
| `RenameWidget` | ウィジェットをリネーム |
| `SetWidgetAsVariable` | ウィジェットの `bIsVariable` フラグを切り替え |
| `SetNamedSlotContent` | NamedSlot ウィジェットの内容を設定 |
| `GetNamedSlots` | Widget Blueprint の NamedSlot 一覧 |
| `ReparentWidgetBlueprint` | Widget Blueprint の親クラスを変更 |
| `GetSlotProperties` | ウィジェットのスロットプロパティを取得（CPF フィルタ・最大 64 キー）。あわせて `PropertyWriteRequirements` マップを返し、各プロパティへの書き込みに何が必要か・どの入力形式で渡すかを示します |
| `SetSlotProperties` | ウィジェットのスロットプロパティを設定（32 KiB 制限・UObject 参照は `/Game/` 以下のみ）。参照には `WidgetSlotReferenceEdit`、構造体・コンテナには `PropertyStructuredEdit` が必要になり、これらの値はエンジンの括弧表記ではなく **JSON ドキュメント** で渡します — 書く前に取得系の `WriteInputForm` を確認してください。拒否された書き込みは undo エントリを残さず、アセットを dirty にもしません。成功した書き込みは Widget Blueprint をコンパイルし、実行時に作られるウィジェットへ変更が届きます。`bSkipCompile: true` を渡すと変更済みの印だけを付け（応答は `bRequiresFollowupCompile: true` になる）、複数の編集のあとに `CompileWidgetBlueprint` で 1 回コンパイルできます |
| `GetWidgets` | ウィジェットツリー構造を取得（JSON） |
| `ListWidgetClasses` | 利用可能なウィジェットクラス一覧（最大 500 件） |
| `CompileWidgetBlueprint` | Widget Blueprint をコンパイルしエラー / 警告を返す |
| `ListWidgetAnimations` | Widget Blueprint のアニメーション一覧 |
| `GetWidgetAnimationInfo` | アニメーションのトラック / キー情報 |
| `CreateWidgetAnimation` | 新規アニメーションを作成 |
| `AddAnimationTrack` | アニメーションにトラックを追加 |
| `ListPropertyBindings` | プロパティバインディング一覧 |
| `AddPropertyBinding` | プロパティバインディングを追加（同一 WBP 内関数/変数のみ） |
| `RemovePropertyBinding` | プロパティバインディングを削除 |
| `ExtractWidgetToUserWidget` | ウィジェットサブツリーを新規 UserWidget として抽出 |

### Toolset ブリッジ（13）🧩

`UMGToolSet` プラグイン経由でネイティブコマンドを委譲。プロバイダ：`Toolset.Editor.UMG.*`。UE 5.8+ と `UMGToolSet` プラグインが必要です。

> **⚠️ Breaking change — このうち 2 件は呼び出せません：`Toolset.Editor.UMG.ReparentWidgetBlueprint` と `Toolset.Editor.UMG.SetWidgetAsVariable`。** `UMGToolSet` はどちらの名前の tool も宣言していません。`SetWidgetAsVariable` については、toolset が宣言している `ToggleWidgetAsVariable` はフラグを**指定した値へ設定するのではなく反転させる**ため、そこへ寄せると「到達はするが違うことをする」状態になります。2 件とも `Available: false` と `UnavailableDetail: "DelegationTargetMissing"` を返すようになりました。**`UMGToolSet` プラグインを有効にしても解決しません。** ネイティブの **`UAIP.Editor.UMG.ReparentWidgetBlueprint`** と **`UAIP.Editor.UMG.SetWidgetAsVariable`** が同じ操作をプラグインなしで行います。

---

## UAIP.Editor.Material

Material グラフ編集とパラメータ管理。

| コマンド | 説明 |
|---|---|
| `GetMaterialInfo` | 基本情報（NodeCount・ShadingModel・BlendMode・bHasErrors） |
| `ListMaterialNodes` | Material グラフのノード一覧（NodeId・ExpressionClass・座標・bIsParameter） |
| `AddMaterialNode` | Material グラフにノードを追加（`ExpressionClass` 指定）— プロジェクト定義またはカスタム HLSL のクラスには Capability が必要、詳細は下記の Note を参照 |
| `DeleteMaterialNode` | NodeId 指定でノードを削除（ルート削除は Conflict） |
| `ConnectMaterialPins` | Material グラフの 2 ピンを接続（循環・型不一致検出） |
| `DisconnectMaterialPins` | ピン接続を切断 |
| `CompileMaterial` | マテリアルをコンパイルしエラー / 警告を返す |
| `SetMaterialParameterValue` | マテリアルパラメータの値を設定 |
| `GetMaterialParameterValue` | マテリアルパラメータの値を取得 |
| `ListMaterialExpressionClasses` | `UMaterialExpression` 派生クラスの一覧（最大 500 件）。各エントリは `AddMaterialNode` が検証するのと同じポリシー由来の `Admission`（`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`）と `RequiredCapabilities` / `MissingCapabilities` を持つ。`ClassPath` を `AddMaterialNode` の `ExpressionClass` 引数に使用する。`TotalCount` / `ReturnedCount` / `Truncated` を返す — 詳細は下記の Note を参照 |
| `RefreshMaterial` | マテリアルを強制再コンパイル（保存済みアセットをパス省略で即時再ビルド） |

> **Note — プロジェクト定義・カスタム HLSL の ExpressionClass は Capability で制御されます**: エンジン組み込みモジュール（`Engine` / `RenderCore` / `MaterialEditor` / `Landscape`）由来の `ExpressionClass` は従来どおり追加できます。それ以外のモジュール由来のクラス — プロジェクトやプラグインが定義した `UMaterialExpression` 派生クラス — は `MaterialCustomTypeEdit` が必要になりました。`UMaterialExpressionCustom` / `UMaterialExpressionCustomOutput` とその派生クラス（任意の HLSL を含められる）は、どのモジュール由来かに関わらず `MaterialCustomNodeEdit` が必要です — この Capability は以前から登録されていましたが、これまでどのコマンドも要求していませんでした。両方に該当するクラスは両方の Capability が必要で、拒否には不足しているものがすべて挙がります。どちらも既定では付与されません。[Safety & Capabilities](safety.md#マテリアル編集) を参照。
>
> これらの確認は `AddMaterialNode` だけに限りません — 既存ノードの編集・接続・切断・コンパイル・Reparent・削除でも同じ Capability があらためて確認されます。削除・切断固有の破壊的変更を含め、詳細は [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照してください。
>
> ⚠️ **破壊的変更**: これらのクラスは従来、無条件で拒否されていました — 型 policy が拒否したクラスには `PolicyViolation`、クラスをまったく解決できない場合は `InvalidParams`。`AddMaterialNode` は現在、クラスが読み込まれていれば `CapabilityNotAvailable` を返し不足している Capability 名を挙げます。旧エラーコードとの移行期間は設けていません — 旧コードは「権限を与えても通らない」ことを意味していたため、残すと存在しない権限体系を案内することになるためです。
>
> `ExpressionClass` はあらかじめ読み込まれている必要があります。`AddMaterialNode` は副作用としてクラスを読み込まなくなり、解決できないクラスには（上記のいずれに該当するかに関わらず）`NotFound` を返します。
>
> **Note — `ListMaterialExpressionClasses` は各クラスの Admission を報告するようになりました**: 各エントリは `Admission` を持ち、4 つの値のいずれかになります — `Allowed`（現在のセッションで今すぐ追加できる）、`RequiresCapabilities`（`MissingCapabilities` に挙がる Capability を付与すれば追加できる。`MissingCapabilities` は `RequiredCapabilities` の部分集合）、`NotAddable`（基底型違い・abstract・deprecated・クラスピッカーから隠されている等、Capability をどれだけ付与しても解消しない構造的な理由で拒否される）、`CompatibilityUnknownUntilAuthorized`（セッションは必要な Capability をすべて保有しているが、エンジン側の互換性チェックはまだ実行されていない — 一覧は権限を与えられていないセッションのためにクラス自身のコードを実行してはならないため、最終的な可否は実際にノードを追加してみるまで分からない）。レスポンスは `TotalCount` / `ReturnedCount` / `Truncated` も返します — この一覧が従来から持っていた 500 件の上限は、これまで一度も報告されていませんでした。返されるクラスの集合も従来より広がりました — abstract・deprecated・`NewerVersionExists`・クラスピッカーから隠されているクラスは、従来はレスポンスから黙って除外されていましたが、現在は除外されず `Admission: NotAddable` を付けて列挙されます。この一覧は権威的な判定ではなくスナップショットです — 一覧取得後に Capability や role が変わり得るため、実際の可否は `AddMaterialNode` 側で毎回あらためて判定されます。

---

## UAIP.Editor.GameplayTags

プロジェクトタグテーブルの管理。

| コマンド | 説明 |
|---|---|
| `ListGameplayTags` | 全タグ一覧（ネイティブ含有・親タグ・ソースでフィルタ）— 最大 2048 件 |
| `GetGameplayTagInfo` | タグ詳細（Comment・Source・bIsNative・bIsRestrictedTag・親子関係） |
| `AddGameplayTag` | 通常タグを INI に追加 |
| `AddRestrictedGameplayTag` | Restricted タグを RestrictedTagList INI に追加 |
| `RemoveGameplayTag` | タグを INI から削除（子タグ / ネイティブタグ保護） |
| `RenameGameplayTag` | タグ名を変更（任意でアセット参照も更新） |
| `FindGameplayTagReferencers` | タグを参照するアセット一覧 |

### Toolset ブリッジ — GameplayTags（6 件）🧩

`GameplayTagsToolset` プラグイン（UE 5.8+、Experimental）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.GameplayTags.*`。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.GameplayTags.ListTags` | 登録済みタグ一覧（`ParentTag` 指定でその子孫に限定、最大 2048 件） |
| `Toolset.Editor.GameplayTags.GetTagInfo` | 単一タグの詳細 — Comment・Source・Children |
| `Toolset.Editor.GameplayTags.FindReferencersByTag` | タグを参照するアセットを検索（最大 256 パス） |
| `Toolset.Editor.GameplayTags.AddTag` | 既存の `.ini` タグソースにタグを追加（`GameplayTagEdit` 必要） |
| `Toolset.Editor.GameplayTags.RemoveTag` | タグをプロジェクトタグテーブルから削除。アセット参照は更新**されない**（`GameplayTagEdit` 必要。Restricted タグの場合は `GameplayTagRestrictedEdit` も必要） |
| `Toolset.Editor.GameplayTags.RenameTag` | INI 上のみのリネーム。参照更新もリダイレクト登録も行わないため、通常はネイティブの `RenameGameplayTag` を推奨（`GameplayTagEdit` 必要。Restricted タグの場合は `GameplayTagRestrictedEdit` も必要） |

> **Note — プロジェクト自身の `Config/` の外への書き込みには `GameplayTagExternalSourceEdit` が必要です**: `AddGameplayTag` / `AddRestrictedGameplayTag` / `RemoveGameplayTag` / `RenameGameplayTag` と、Toolset の `AddTag` / `RemoveTag` / `RenameTag` は、実際に書き込む場所を何も変更する前に解決します。書き込み先がプロジェクト自身の `Config/` の外 — エンジンのプラグイン、Fab やサードパーティのプラグイン、**プロジェクト自身のゲームプラグインや Game Feature プラグインを含む** — の場合、`GameplayTagEdit` / `GameplayTagRestrictedEdit` に加えて DefaultDenied の `GameplayTagExternalSourceEdit` が必要になり、無ければ `CapabilityNotAvailable` で拒否されその名前が示されます。⚠️ **挙動の変化**: プラグインが持つ置き場へのタグの追加・リネームは、これまで `GameplayTagEdit` だけで行えましたが、`GameplayTagExternalSourceEdit` も必要になりました。プラグインの検索パス経由で見つかる Restricted な置き場で、書き込み先が実際の読み込み元と一致しないものは、代わりに `NotAllowed` で無条件に拒否されます — 書き込み先が読み込み元と異なる場所になってしまうため、Capability を付与しても解消しません。境界の判定はパスの文字列だけで行われ、`Config/` の中にシンボリックリンクやジャンクションで外部を差し込んでいても、内側として扱われます。詳細は [Safety & Capabilities — Gameplay systems](safety.md#gameplay-systems)。
>
> **Note — Restricted タグの削除・リネームには `GameplayTagRestrictedEdit` が必要です**: Restricted タグの追加にはこれまでもこの Capability が必要でしたが、`RemoveGameplayTag` / `RenameGameplayTag` と Toolset の `RemoveTag` / `RenameTag` も、削除・リネームの対象タグ（強制削除や子を含むリネームの場合はその子孫のいずれか）が Restricted であれば同様に必要になりました。`GameplayTagEdit` だけを保有するセッションは `CapabilityNotAvailable` で拒否され、不足している Capability 名が示されます。
>
> **Note — Restricted タグのリネームでは旧タグが残ります**: これは UAIP の仕様ではなくエンジン側の制限です。エンジンのリネーム実装は、新しいタグを旧タグのソースへ追加する一方で旧タグ自体は残し、リダイレクトの登録はプロジェクトの既定タグファイルへ書き込みます（Restricted な置き場へは書きません）。`RenameGameplayTag` と Toolset の `RenameTag` はこの挙動をそのまま通します。上記の Capability・置き場の確認は、エンジンが実際に書き込む対象（旧タグの置き場と、リダイレクト用の既定の置き場の両方）に対して行われます。
>
> **Note — `AddGameplayTag` / Toolset `AddTag` は Restricted な置き場の名前を先に拒否します**: Restricted な置き場の名前を制限なしの追加コマンドに渡すと、Capability の確認より前に `InvalidParams` で拒否され、代わりに `AddRestrictedGameplayTag` を使うよう案内が出ます。逆に、制限なしの置き場の名前を `AddRestrictedGameplayTag` に渡した場合も同様に拒否されます。

---

## UAIP.Editor.GameFeatures 🧩

GameFeature Plugin 管理。`GameFeatures` + `GameFeaturesEditor` プラグインが必要です。

| コマンド | 説明 |
|---|---|
| `ListGameFeatures` 🧩 | GameFeature Plugin 一覧（`FilterState`：All / Installed / Mounted / Registered / Loaded / Active） |
| `GetGameFeatureInfo` 🧩 | GFP 詳細（State・Actions・依存関係） |
| `GetGameFeatureActions` 🧩 | GameFeature Plugin の `UGameFeatureData` が宣言する Action 一覧 |
| `CreateGameFeaturePlugin` 🧩 | プロジェクトの `Plugins/GameFeatures/` の下に新しい GameFeature Plugin を作り、Game Feature サブシステムに登録して `InitialState` まで進める。表の下の注記を参照 |
| `DeleteGameFeaturePlugin` 🧩 | プロジェクトの `Plugins/GameFeatures/` にあるコンテンツのみの GameFeature Plugin を削除。`GameFeatureDelete` が必要。`DisableSave` が有効なときは `PolicyViolation` で拒否。表の下の注記を参照 |

> **`CreateGameFeaturePlugin`** には `GameFeatureCreate` と `PluginName`（英字で始まり、英数字と `_` を合わせて最大 64 文字）が必要です。省略可能な `OutputPath` の既定はプロジェクトの `Plugins/GameFeatures/` で、相対パスで指定するとプロジェクトルートが基準になります（`Plugins/GameFeatures/Combat` なら、`Plugins/GameFeatures/Combat/<PluginName>/` に作成）。省略可能な `InitialState`（`Installed` / `Registered` / `Loaded` / `Active`。既定は `Active`）は、作成後に進める状態で、再起動後に始まる状態でもあります。プラグインには同名の GameFeature データのアセットが作られ、作成したセッションのうちに（通常は数秒以内）GameFeature として登録されます。エディタを再起動しても同じように登録されます。`.uproject` は変更しません。
>
> - **成功**: `Data` に `PluginPath`（プロジェクトルートからの相対パス。実際の作成先）・`PluginUrl`・`State`・`Warnings` が入ります。プロジェクトに GameFeature データのアセット管理設定が無いときは、`Warnings` に、パッケージ版でこの GameFeature のデータが含まれない恐れがあることと、`DefaultGame.ini` に足す設定行が入ります。プロジェクトの設定をコマンドが書き換えることはありません。
> - **`InvalidParams`**: `OutputPath` がプロジェクトの `Plugins/GameFeatures/` の外（`Plugins/` の直下やプロジェクトの外など）・既存プラグインの中・ジャンクション経由でプロジェクト外を指す場合、名前や `InitialState` が不正な場合。何も作りません。同名のフォルダやプラグインがあると `Conflict`、エディタが終了中・PIE 中・コマンドレット実行中は `NotAllowed`、安全ポリシーがディスク書き込みを無効にしていると `PolicyViolation` です。
> - **`ExecutionFailed`**: 途中の手順（プラグイン作成・データアセットの作成や保存・登録）が失敗した、登録が 30 秒以内に終わらなかった、エディタの終了が始まった、または作成後にもう一度場所を確かめたらプロジェクトの外だった場合。作ったものは消さずに残し、`Data` にどこまで進んだか（`CreatedOnDisk` / `Mounted` / `DataAssetCreated` / `DataAssetSaved` / `Registered`）・到達した `State`・`PluginPath` を載せます。同じ内容を JSON の成果物にも残し、`.uplugin` があればその写しも付けます。後始末には `DeleteGameFeaturePlugin` を使ってください。ただし場所の確認で外れた場合は例外で、プラグインはエディタから外されますがファイルは残り、`DeleteGameFeaturePlugin` も拒否するので、手で確認して削除してください。
>
> **`DeleteGameFeaturePlugin`** は `PluginName` を取ります。GameFeature の登録を解除し（作成の途中で失敗して一度も登録されなかったものは、この手順を飛ばします）、アセットの読み込みを解除し、削除してよい対象かをもう一度確かめてから、プラグインを外してフォルダを削除します。次の場合は拒否し、何も消しません。プラグインが無い（`NotFound`）。対象が GameFeature ではない（`Plugins/GameFeatures/` の外にあるプラグイン、旧版が `Plugins/` 直下に作ったもの）、`GameFeatures` フォルダそのもの、他のプラグインを含む、コードのモジュールを持つ、またはジャンクションなどのリンクを含む（`NotAllowed`）。GameFeature の状態が切り替わっている最中（`PreconditionFailed`。待ってから再試行）。アセットの読み込み解除に失敗した、登録の解除が 30 秒以内に終わらなかった、またはエディタの終了が始まった（`ExecutionFailed`）。

### Toolset ブリッジ — GameFeatures（4 件）🧩

`GameFeaturesToolset`（UE 5.8+、Experimental）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.GameFeatures.*`。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.GameFeatures.ListGameFeatures` | このブリッジコマンド経由では利用不可 — 代わりに `UAIP.Editor.GameFeatures.ListGameFeatures` を使ってください（後述の注記を参照） |
| `Toolset.Editor.GameFeatures.FindGameFeatureData` | ⚠️ **呼び出せません** — 委譲先が存在せず、ネイティブの代替もありません（後述の注記を参照） |
| `Toolset.Editor.GameFeatures.GetActions` | ⚠️ **呼び出せません** — 委譲先が存在せず、ネイティブの代替もありません（後述の注記を参照） |
| `Toolset.Editor.GameFeatures.CreateGameFeaturePlugin` | ⚠️ **呼び出せません** — 代わりに `UAIP.Editor.GameFeatures.CreateGameFeaturePlugin` を使ってください（後述の注記を参照） |

> **⚠️ Breaking change — `Toolset.Editor.GameFeatures.ListGameFeatures` は、このブリッジコマンド経由ではどのエンジンバージョンでも呼び出せません。** 内部で委譲している `GameFeaturesToolset` が `ListGameFeatures` という名前の関数を宣言していないため、そもそも実行に到達できませんでした — これまでは何を渡しても実行時に汎用的な `ExecutionFailed` で失敗していました。現在は `UAIP.Core.DescribeCommand` と `uaip_list_commands` が `Available: false` を報告し、`UnavailableReason: "HandlerUnavailable"` / `UnavailableDetail: "DelegationTargetMissing"` が付きます。名前指定で呼び出すと依然として失敗しますが、今度は `PolicyViolation` になり、`ErrorMessage` には同じ説明が入ります。**代わりに `UAIP.Editor.GameFeatures.ListGameFeatures` を使ってください** — ネイティブコマンドが委譲せずに同じ操作を行い、この変更の影響を受けません。

> **⚠️ Breaking change — 同じ状態がこのセクションの残り 3 件にも当てはまります。** 全件の突き合わせにより、`FindGameFeatureData` / `GetActions` / `CreateGameFeaturePlugin` も `GameFeaturesToolset` が宣言していない名前へ委譲していたことが分かりました（同 toolset が宣言しているのは `GetGameFeatureState` / `IsGameFeatureActive` / `IsGameFeaturePlugin` / `ListDiscoveredGameFeaturePlugins` / `ListEnabledGameFeaturePlugins` / `RequestActivateGameFeature` / `RequestDeactivateGameFeature` の 7 件のみ）。3 件とも `Available: false` と `UnavailableDetail: "DelegationTargetMissing"` を返すようになりました。**`GameFeaturesToolset` プラグインを有効にしても解決しません。** `CreateGameFeaturePlugin` には **`UAIP.Editor.GameFeatures.CreateGameFeaturePlugin`** という同じ操作を行うネイティブコマンドがあります。`FindGameFeatureData` と `GetActions` にはネイティブの代替がなく、本更新時点でこの 2 つの操作にはこのプラグイン内に動く経路がありません。

---

## UAIP.Editor.Niagara 🧩

Niagara VFX システム編集。`Niagara` + `NiagaraEditor` プラグインおよび **UE 5.7 以降**が必要です。

### ネイティブ（52）

#### 観測（13）

| コマンド | 説明 |
|---|---|
| `GetSystemTopology` 🧩 | Niagara システムのエミッター構造 — 各エミッターの `Spawn` / `Update` / `Event` モジュール一覧で、各エントリは `ModuleName` に加えて `ModuleId` も返すようになった（そのまま `GetStackInputData` へ渡せる）。ここのモジュールエントリに `Inputs` 配列は含まれない — モジュールの入力を調べるには `GetModuleTopology` や `GetStackInputTopology` を使うこと。⚠️ `Spawn`/`Update` は*エミッター単位*の Spawn/Update スタック、`Event` はイベントハンドラースタックであり、システムの Particle Spawn / Particle Update モジュールはここには一切含まれない。粒子単位まで必要な場合は `GetEmitterTopology` を使うこと。 |
| `GetSystemCompileState` 🧩 | システムのコンパイル状態 |
| `GetAssetDiscoveryInfo` 🧩 | Niagara アセット探索情報 |
| `GetScriptAssets` 🧩 | Niagara スクリプトアセット一覧 |
| `GetNiagaraParameterCollections` 🧩 | Niagara パラメータコレクション一覧 |
| `GetUserVariables` 🧩 | システムのユーザー変数一覧 |
| `GetSystemInfo` 🧩 | システムの詳細情報（メタデータ含む） |
| `GetSystemData` 🧩 | システムのデータ構造 |
| `GetEmitterData` 🧩 | エミッターのデータ構造 |
| `GetRendererData` 🧩 | レンダラーのデータ構造 |
| `GetStackInputData` 🧩 | モジュールスタック入力値 — 名前・型・値モード（Local/Linked/Dynamic/DataInterface/Expression）・`AddSetParameterEntry` がそのまま書き戻せる形の現在値・入れ子の `WriteRequirements` オブジェクトを返す。必須パラメータ `ModuleId` は `GetSystemTopology` / `GetEmitterTopology` / `GetScriptStackTopology` / `GetModuleTopology` のいずれか、または `AddModule` 自身のレスポンスから得られる（4つの取得系と書き込み系すべてが同じ小文字ハイフン区切り形式で返す）。UAIP でモジュールを追加したことのないアセットでも、既存モジュールを読み取ることができる。 |
| `UEnum_Info` 🧩 | UEnum 情報 |
| `GetAvailableNiagaraRendererClasses` 🧩 | `UNiagaraRendererProperties` 派生クラスの一覧（上限 200 件）。返された `ClassPath` を `AddRenderer` の `RendererClass` 引数として使用する。 |

#### スキーマ（7）

| コマンド | 説明 |
|---|---|
| `GetSystemSchema` 🧩 | `UNiagaraSystem` の編集可能なトップレベルプロパティの JSON Schema（システム間で不変・キャッシュ可）。UE 5.8+ 専用。UE 5.7 では `Available: false` |
| `GetEmitterSchema` 🧩 | エミッタの編集可能なトップレベルプロパティの JSON Schema（キャッシュ可）。UE 5.8+ 専用。UE 5.7 では `Available: false` |
| `GetRendererSchema` 🧩 | `RendererClassPath` で指定した `UNiagaraRendererProperties` クラスの JSON Schema。UE 5.8+ 専用。UE 5.7 では `Available: false` |
| `GetDataInterfaceSchema` 🧩 | `DataInterfaceClassPath` で指定した `UNiagaraDataInterface` クラスの JSON Schema。UE 5.8+ 専用。UE 5.7 では `Available: false` |
| `GetStackInputSchema` 🧩 | 単一モジュール入力の型・カテゴリ・`SupportsExpressions` |
| `GetModuleSchema` 🧩 | スタック上のモジュールインスタンスの入出力一覧 |
| `GetModuleSchemaFromAsset` 🧩 | NiagaraSystem を介さず `UNiagaraScript` モジュールアセットの入出力を取得 |

#### トポロジと Dynamic Input（7）

| コマンド | 説明 |
|---|---|
| `GetEmitterTopology` 🧩 | エミッタの全スクリプトスタックとモジュールを含むモジュールスタックトポロジ。各モジュールエントリが `ModuleId` を持つ |
| `GetScriptStackTopology` 🧩 | 単一スクリプトスタックのモジュールトポロジ。各モジュールエントリが `ModuleId` を持つ |
| `GetModuleTopology` 🧩 | 単一モジュールの入力トポロジ。そのモジュール自身の `ModuleId` を含む |
| `GetStackInputTopology` 🧩 | 単一入力のトポロジ — 名前・型・`IsVisible`/`IsEditable`/`IsDynamic`。解決済みの値は含まれず、`DynamicInputChildren` はどのエンジンバージョンでも辿った結果ではなく常に空配列で返る — dynamic input 自身の入出力を読むには `GetDynamicInputSchema` を、現在値が必要な場合は `GetStackInputData` を使うこと。同じ `Name`/`Type`/`IsVisible`/`IsEditable`/`IsDynamic`/`DynamicInputChildren` の形、および同じく常に空配列になる `DynamicInputChildren` は、`GetModuleTopology`・`GetEmitterTopology`・`GetScriptStackTopology` が返す各モジュールの `Inputs[]` エントリでも共通して使われる |
| `GetDynamicInputSchema` 🧩 | スタック上の dynamic input スクリプトインスタンスの入出力一覧 |
| `GetDynamicInputSchemaFromAsset` 🧩 | NiagaraSystem を介さず `UNiagaraScript` dynamic input アセットの入出力を取得 |
| `GetAvailableDynamicInputs` 🧩 | 指定モジュール入力に適用できる dynamic input スクリプト一覧。UE 5.8+ 専用。UE 5.7 では `Available: false` |

> **⚠️ Note — `GetStackInputSchema`・`GetModuleSchema`・`GetDynamicInputSchema` の UE 5.8 未満向けフォールバックも通常モジュールに対応し、そのフォールバックのキー名が UE 5.8+ と揃いました**: この3コマンドはこれまで UE 5.7 では「Set Parameters」モジュール（Assignment ノード）にしか成功しませんでした — `GetStackInputSchema` と `GetDynamicInputSchema` はそれ以外を対象にすると呼び出し全体が `ExecutionFailed` で失敗し、`GetModuleSchema` は失敗せず `Inputs` が空配列のまま成功していました。現在は3コマンドとも、通常の関数呼び出しモジュールをグラフから直接読み取れます（ビューモデルは使いません）。`GetModuleSchema` は対象モジュールにスクリプト・グラフが無い場合、空配列で成功する代わりに失敗するようになりました。`GetDynamicInputSchema` は、対象の入力が実際に dynamic input で駆動されていない場合は引き続き失敗します — これは記述すべき dynamic input が無いという正当な失敗であり、不具合ではありません。これとは別に、このフォールバックが返す入力エントリの JSON キー名が `InputName`/`InputType` から `Name`/`Type` に変わりました — `GetStackInputSchema` 自身のエントリ、および `GetModuleSchema`・`GetDynamicInputSchema` が返す `Inputs` 配列の各要素の両方です。これにより3コマンドとも、UE 5.8+ が元から使っているキー名と一致するようになりました。`GetDynamicInputSchema` 自身の Set Parameters 経路も、自身の通常モジュール経路と同じ封筒に揃え、独自形式の `{InputName, InputType, Inputs: [], Outputs: []}` から `{ModuleAssetPath, Inputs: [{Name, Type}], Outputs: []}` に変わりました。**`GetStackInputData` はこの変更の対象外**で、どのエンジンバージョンでも引き続き `InputName`/`InputType` を返します。
>
> **⚠️ Note — `GetStackInputTopology` の UE 5.8 未満向けフォールバックが、Set Parameters 以外の通常モジュールにも対応しました**: レスポンスの形（`Name`/`Type`/`IsVisible`/`IsEditable`/`IsDynamic`/`DynamicInputChildren`）は、両分岐が統一されて以来 UE 5.8+ とすでに揃っています。今回変わったのは対応できるモジュールの範囲です。これまでは「Set Parameters」モジュール（Assignment ノード）に対してしか成功せず、それ以外を対象にすると呼び出し全体が `ExecutionFailed` で失敗していました。現在は通常の関数呼び出しモジュールに対しても成功し、その入力をグラフから直接読み取ります（ビューモデルは使いません）。このフォールバックが複数要素の `InputNameStack` をどう辿るかはこの後変わりました — 詳細は後述のノートを参照。static switch 入力は、どちらのモジュール種別でもこの分岐からは指定できません。
>
> `IsVisible`/`IsEditable`/`IsDynamic` がどこまで実測かは、一致したモジュールの種類によって変わります。
> - **Set Parameters** モジュールに一致した場合は従来と変わりません: `IsVisible` と `IsEditable` は引き続き常に `true` です — モジュールから実測した値ではなく（Assignment Target 自体には可視性・編集可能性を示すメタデータがありません）、この結果に到達する時点で対象の存在意義自体が「Assignment Target を編集可能にすること」であるために `true` としています。`IsDynamic` は引き続き判定材料が無いための保守的な既定値として常に `false` を返します — この経路には対象が実際に dynamic input を持つかどうかを検出する手段がありません。
> - **通常モジュール**に一致した場合、`IsDynamic` は実測になりました — 入力の override ピンの接続先が Dynamic Input スクリプトの関数呼び出しノードであるときだけ `true` を返します。これは UE 5.8+ が値モード `Dynamic` と呼ぶ条件と同じです。`IsVisible` も実測ですが、モジュールが現在隠している入力集合から算出しており、`VisibleCondition` 式そのものは評価しません。そのため、条件が false なだけで隠れている入力は visible と報告されます。`IsEditable` はこの実測された可視性をそのまま使うため、実測は半分だけです — `EditCondition` 式（評価には兄弟入力の現在値が必要でグラフだけからは解決できません）は評価しないため、条件が false なだけで編集不可になっている入力は editable と報告されます。
>
> **⚠️ Breaking change — `GetStackInputTopology`・`GetStackInputSchema`・`GetDynamicInputSchema` の UE 5.8 未満向けフォールバックが、`InputNameStack` の先頭要素だけでなく全要素を辿るようになりました**: この3コマンドはこれまで `InputNameStack[0]` しか見ず、それより後の要素を黙って無視していました — ネストした dynamic input 自身の入力（例: `[TopLevelInput, NestedInput]`）を狙った呼び出しは、`TopLevelInput` 自身のデータを、通常の成功として受け取っていました。ネストした要素が一度も読まれていないことを示すものは何もありませんでした。**つまり、従来のネストしたスタックへの回答は単に不完全だったのではなく、成功を報告しながら誤った入力を記述していました。** 現在はこのフォールバックも、UE 5.8+ がすでに行っているのと同じ方法でスタック全体を辿ります — `InputNameStack[0]` はモジュール自身の入力に対して解決し、それ以降の各要素は、直前の要素を現在駆動している Dynamic Input スクリプトインスタンス上の入力に対して解決します。途中の要素が実際には dynamic input で駆動されていない場合や、名前が解決できない場合は、指定と異なる入力を黙って答える代わりに呼び出し全体が失敗するようになりました。`GetDynamicInputSchema` は、`InputNameStack[0]` を駆動しているものではなく、**解決された葉**を駆動している dynamic input インスタンスを記述するようになりました。**Set Parameters**（Assignment ノード）モジュールに対しては特に、2要素以上のスタックは今回から明確に拒否されます — Assignment Target には辿り込める dynamic input が存在しないため、従来は要素数にかかわらず Assignment Target 自身のデータを黙って返していました。**UE 5.8+ は影響を受けません** — 元からスタック全体を辿っていたためです。単一要素の `InputNameStack`（通常のケース）は、どのエンジンバージョンでも従来どおり解決されます。
>
> **⚠️ Breaking change — `GetModuleTopology` の UE 5.8 未満向けフォールバックが返す形が変わり、`ScriptName` を実際に見るようになり、システムレベルのスクリプトも対象にできるようになりました**: これまでのフォールバックはシステムビューモデルでエミッターのスタック全体を走査し、`{ModuleName, ModuleAssetPath, Inputs: [{InputName, InputType}], Outputs: []}` を返していました。`ScriptName` 引数は一切参照されておらず、モジュールは `ScriptName` が指す特定のスタックではなく、エミッターの全スタックのどこかにあれば一致していました。`EmitterName` が空の場合はどのスタックにも一致せず、システムレベルのモジュールはこの分岐からは一切読めませんでした。現在のフォールバックは、UE 5.8+ がすでに行っているのと同じ crash-safe な方法で対象スクリプトのグラフを直接読み取り、`ScriptName` を実際に参照します。`EmitterName` が空の場合は、`GetEmitterTopology` や `GetScriptStackTopology` がすでに受け付けていたのと同様に、システム自身の Spawn/Update スクリプトを解決するようになりました。レスポンスの形もこれに合わせて変わりました — `ModuleAssetPath` は `ModuleScript` に改名。`Outputs` は無くなりました（モジュールのトポロジはどちらのエンジンバージョンでも出力に相当する概念を持たず、旧フォールバックの `Outputs` もそもそも常に空配列だったため、実質的に失われるものはありません）。`Enabled` と `IsSetParametersModule` が新規追加。各 `Inputs[]` エントリは `InputName`/`InputType` だけの形から、`Name`/`Type`/`IsVisible`/`IsEditable`/`IsDynamic`/`DynamicInputChildren`（上記 `GetStackInputTopology` の行、および `DynamicInputChildren` の制約を参照）へ変わりました。モジュール名の照合も、これまでの大文字小文字を無視する方式から、大文字小文字を区別する方式に変わりました。`Enabled` はモジュール自身のファンクションコールノードから読み取っています — サブノードだけを本体ノードと切り離して無効化した異常な状態では、UE 5.8+ のスタックビューが示す `Enabled` と食い違う場合があります。
>
> **⚠️ Breaking change — `GetEmitterTopology` の UE 5.8 未満向けフォールバックから `IsEnabled` が無くなり、各スクリプトスタックが UE 5.8+ が元から使っている `{ScriptName, Modules}` の形にラップされ、各 `Modules[]` エントリに5つのフィールドが増えました**: これまでのフォールバックは `{EmitterName, IsEnabled, EmitterSpawn: [{ModuleName}], EmitterUpdate: [...], ParticleSpawn: [...], ParticleUpdate: [...], Renderers: [{RendererClass}]}` を返していました — `EmitterSpawn`/`EmitterUpdate`/`ParticleSpawn`/`ParticleUpdate` はモジュールの生の配列で、各モジュールは `ModuleName` だけを持っていました。`IsEnabled` は無くなりました。UE 5.8+ 自身のエミッタートポロジもこのフィールドを一度も持ったことがなく、片方のエンジンバージョンにしか存在しないフィールドは、無い方がまだましだからです。エミッターの有効/無効はどのエンジンバージョンでも引き続き読み取れます — `GetSystemTopology` の各エミッターエントリ、または `GetEmitterData` から取得できます。4つのスクリプトスタックはそれぞれ、UE 5.8+ が元から返している `{ScriptName, Modules}` というオブジェクトの形にラップされるようになりました — `EmitterSpawn` などを生の配列として走査していた呼び出し側は、`Modules` フィールドを読むように切り替える必要があります。各 `Modules[]` エントリは `ModuleName` 単独のフィールドから、`GetModuleTopology` と `GetScriptStackTopology`（上記・下記参照）のモジュールエントリと同じ6フィールド — `ModuleName`、`ModuleId`、`Enabled`、`IsSetParametersModule`、`ModuleScript`、`Inputs` — へと増えました。各 `Renderers[]` エントリにも、既存の `RendererClass` に加えて `RendererIndex` が増えました。これは UE 5.8+ と同じで、報告されたインデックスをそのまま `RemoveRenderer` に渡せます。このフォールバックでは `RendererClass` 自体の値も変わり、完全なクラスパス（例: `/Script/Niagara.NiagaraSpriteRendererProperties`）から、UE 5.8+ が元から返している素のクラス名（例: `NiagaraSpriteRendererProperties`）になりました — この同じ素のクラス名を `GetRendererSchema` も直接受け付けるようになっています（後述）。
>
> **Note — `GetScriptStackTopology` の UE 5.8 未満向けフォールバックは各 `Modules[]` エントリにフィールドが増えるだけで、何かが無くなることはありません**: 各エントリはこれまで `ModuleName` だけを持っていました。現在は `GetModuleTopology` や `GetEmitterTopology` のモジュールエントリと同じ6フィールド — `ModuleName`、`ModuleId`、`Enabled`、`IsSetParametersModule`、`ModuleScript`、`Inputs`（上記 `GetStackInputTopology` と同じ形）を持ちます。ただし `ModuleName` の意味はこれまでと変わらず、周囲を包む `{ScriptName, Modules}` という封筒の形も変わっていないため、各エントリの `ModuleName` だけを読んでいたコードはそのまま動作し続けます。
>
> **⚠️ Breaking change — `GetScriptStackTopology` の UE 5.8 未満向けフォールバックが、呼び出し側が渡した綴りではなく正規の `ScriptName` を返すようになりました**: レスポンスの `ScriptName` フィールドは、これまで `ScriptName` 引数として渡された文字列を、綴りや大文字小文字を問わずそのまま反射していました — `"particlespawn"` や `"whatever"` を渡した呼び出しでもその文字列がそのまま返り、本物の答えと見分けが付きませんでした。現在は、同じ旧エンジン向けフォールバック上で `GetEmitterTopology` のスクリプトスタックエントリが元から報告していたのと同じ正規名（`EmitterSpawnScript`、`ParticleUpdateScript`、`SystemSpawnScript` など）を返します — この2コマンドは同じエンジンセッション上の同じスタックに対して異なる答えを返していましたが、その食い違いは無くなりました。**UE 5.8+ は影響を受けません** — 元から正規名を返していたためです。
>
> **Note — UE 5.8+ では `Modules[]` エントリの `ModuleId` はベストエフォートで欠けることがあり、UE 5.7 以前では常に存在します**: `GetEmitterTopology`・`GetScriptStackTopology`・`GetModuleTopology` はいずれも UE 5.8+ では同じ方法で `ModuleId` を得ています。`UNiagaraExternalEditUtilities` のトポロジ構造体はモジュールを表示名でしか識別せず、guid フィールドを一切持たないため、`ModuleId` はスクリプトのグラフを辿り、各エントリの `ModuleName` を `UNiagaraNodeFunctionCall` ノードと大文字小文字を区別して照合することで、後から補うしかありません。一致するノードが見つからない場合、そのエントリには空文字列ではなく `ModuleId` キー自体が付きません — 一致した他のエントリよりフィールドが1つ少なくなります。UE 5.7 以前のフォールバックは、エントリの他のフィールドを組み立てるために同じグラフを辿っている最中にノードの guid をそのまま読み取るため、`ModuleId` は常に存在します。`Modules[].ModuleId` を無条件に読むコードは、UE 5.8+ ではこの欠落が起こりうることを踏まえておくこと。
>
> **⚠️ Breaking change（UE 5.8+ のみ）— enum 型の入力の `Type` フィールドが、`NiagaraInt32` の代わりに enum 自身の名前を返すようになりました。** `Type` フィールドはすべて1つの直列化関数を通っており、これまでは `FNiagaraTypeDefinition::GetStruct()` を `GetEnum()` より先に判定していました。Niagara は enum の値を `int32` の構造体に格納しているため `GetStruct()` は enum 型に対しても null を返さず、enum 型の入力はすべて `"NiagaraInt32"` と報告され、enum としての正体が失われていました。これは新機能ではなく不具合の修正です — 判定順序が `GetEnum()` を先に試すように変わったため、enum 型の入力は自身の enum 名（例: `"ENiagaraCoordinateSpace"`）を返すようになりました。struct 型の入力（`"NiagaraFloat"`、あるいは本物の整数入力の `"NiagaraInt32"`）や class 型の入力は影響を受けません。この変更は UE 5.8+ で `Type` フィールドが現れるすべての箇所に及びます — `GetModuleTopology`・`GetEmitterTopology`・`GetScriptStackTopology` の各入力エントリ、`GetStackInputTopology`、`GetStackInputSchema`、`GetModuleSchema`、`GetDynamicInputSchema`、`GetDynamicInputSchemaFromAsset`、および（`GetDynamicInputSchemaFromAsset` に委譲する）`GetModuleSchemaFromAsset` です。**UE 5.7 以前は影響を受けません** — 旧エンジンのフォールバックは元から `FNiagaraTypeDefinition::GetName()` で enum 自身の名前を読んでいたため、今回の変更は UE 5.8+ を UE 5.7 以前が元から返していた値へ揃えたものです。
>
> **Note — `GetRendererSchema` の `RendererClassPath` が、どのエンジンバージョンでも素のクラス名も受け付けるようになりました。** これまでこのパラメータは完全なクラスパス（例: `/Script/Niagara.NiagaraSpriteRendererProperties`）のみを解決していました。現在は `GetEmitterTopology` の `Renderers[].RendererClass`（前述）や `GetRendererData` が既に報告している素のクラス名（例: `NiagaraSpriteRendererProperties`）も解決します。パラメータ名 `RendererClassPath` は変わっておらず、従来のパス形式もそのまま通ります。素のクラス名が複数のレンダラークラスに一致する場合は、推測せず拒否されます。`AddRenderer` と `SetRendererData` も自身の `RendererClassPath` 引数で同じ2形式を受け付けます。
>
> **Note — `GetDataInterfaceSchema` の `DataInterfaceClassPath` が、どのエンジンバージョンでも素のクラス名も受け付けるようになりました。** これまでこのパラメータは完全なクラスパスのみを解決していました。現在はこのコマンド自身の `TypeName` フィールドや、トポロジ・スキーマ読み取りのどこかにあるデータインターフェース型の `Type` フィールドが既に報告している素のクラス名（例: `NiagaraDataInterfaceCurve`）も解決します。これにより、それらのフィールドから読み取った型名をそのままこのコマンドへ渡せるようになります。パラメータ名 `DataInterfaceClassPath` は変わっておらず、従来のパス形式もそのまま通ります。
>
> **Note — `GetModuleSchema` と `GetDynamicInputSchema` の UE 5.8 未満向けフォールバックが、UE 5.8+ が元から持つ `Inputs[]` の同じ4キーを返すようになりました。** 各 `Inputs[]` エントリはこれまで `Name`/`Type` だけを持っていましたが、現在は UE 5.8+ と同じ形に合わせて `Category` と `SupportsExpressions` も持ちます。ただしこのフォールバックでは、新しい2つのフィールドはどちらも実測ではありません — `Category` は常に空文字列、`SupportsExpressions` は常に `false` です。どちらも通常はスタックのビューモデルから読むものであり、このフォールバックが使うグラフだけの経路には対応するものがないためです。`Name` と `Type` は影響を受けず、`Outputs[]` はこれまでどおりこのフォールバックでは常に空のままです。
>
> **⚠️ Breaking change — `GetDynamicInputSchemaFromAsset` の UE 5.8 未満向けフォールバックが、常に空配列を返すのをやめ、アセットが実際に宣言している入力を返すようになりました。** これまでこのフォールバックは、アセットが何を宣言していようと `{ModuleAssetPath, Inputs: [], Outputs: []}` を常に返し、常に成功を報告していました — 呼び出し側から見れば「このアセットは入力を宣言していない」としか読めませんでしたが、実際は何も読んでいませんでした。現在は UE 5.8+ が元からアセットのグラフから読んでいるのと同じ `Module.` 名前空間の宣言（各エントリ `Name`/`Type`/`Category`/`SupportsExpressions`、静的スイッチは除外）を読むため、アセットが何か宣言していれば成功時の `Inputs` はそれで埋まります。**従来は常に成功していた呼び出しが失敗しうるようになりました**: アセットに読み取れるグラフが無い場合、以前の「空だが成功」の代わりに `ExecutionFailed` を返します。`Outputs` はこれまでどおりこのフォールバックでは空配列のままです。単体アセットはスタック内の呼び出し元を経由せず直接読むため、報告される集合は同じスクリプトをスタック内から読んだときの**上位集合**になります — ある呼び出し元では到達しない静的スイッチの分岐にある入力も列挙され、スタック側の hidden 絞り込みもここには効きません。`GetModuleSchemaFromAsset` はこの読み取りへ委譲しているため、まったく同じように変わります。**UE 5.8+ は影響を受けません** — こちらの分岐は元々グラフの無いアセットで失敗しうる作りであり、その挙動は変わっていません。
>
> **⚠️ Breaking change — `GetAvailableDynamicInputs` は UE 5.7 では一切使えなくなりました。これまで `ExecutionFailed` で失敗していましたが、現在は `uaip_list_commands` の既定一覧にも出てきません。** あるスタック入力がどの dynamic input スクリプトを受け付けるかは、スタック UI が同じ入力候補を提示するときに使うのと同じエンジン API が決めており、UE 5.7 にはグラフレベルで代替できる情報がありません。このコマンドはこれまでどのエンジンバージョンでも `Available: true` を報告してハンドラまで到達させており、旧エンジン向けフォールバックは当初 `{DynamicInputs: []}` を返して成功を報告していました（「この入力に合う dynamic input が無い」と読めてしまい、そもそも調べていないことと区別できませんでした）。その後 `ExecutionFailed` へ変更され、`ErrorMessage` に UE 5.8 のエンジン API が必要な旨の説明が入るようになりました。**拒否のタイミングが再び移動し、今度は実行時ではなく照会時になりました。** `UAIP.Core.DescribeCommand` と `uaip_list_commands` は、UE 5.7 では最初から `Available: false` を報告し、`UnavailableReason: "HandlerUnavailable"` / `UnavailableDetail: "EngineVersion"` が付きます。UE 5.7 で名前指定して呼び出すと依然として失敗しますが、今度は `ExecutionFailed` ではなく `PolicyViolation` になり、`ErrorMessage` には同じ説明が入ります。**UE 5.8+ は影響を受けません** — こちらの分岐は元々（未解決のシステム・エミッター・スクリプト・モジュールで）失敗しうる作りであり、その挙動は変わっていません。
>
> **⚠️ Breaking change — `GetEmitterSchema`・`GetSystemSchema`・`GetRendererSchema`・`GetDataInterfaceSchema` は UE 5.7 では一切使えなくなりました。これまで `ExecutionFailed` で失敗していましたが、現在は `uaip_list_commands` の既定一覧にも出てきません。** `PropertySchema` は UE 5.8 で新設されたエンジン API から組み立てるものであり、UE 5.7 には生成元となる同等の API がありません。この4コマンドはこれまでどのエンジンバージョンでも `Available: true` を報告してハンドラまで到達させており、当初は成功を報告して `PropertySchema` を常に空文字列に固定していた版もあれば、その後 `ExecutionFailed` へ変更され `ErrorMessage` に説明が入るようになった版もありました。**拒否のタイミングが再び移動し、今度は実行時ではなく照会時になりました。** `UAIP.Core.DescribeCommand` と `uaip_list_commands` は、UE 5.7 では4コマンドとも最初から `Available: false` を報告し、`UnavailableReason: "HandlerUnavailable"` / `UnavailableDetail: "EngineVersion"` が付きます。UE 5.7 で4コマンドのいずれかを名前指定して呼び出すと依然として失敗しますが、今度は `ExecutionFailed` ではなく `PolicyViolation` になり、`ErrorMessage` には同じ説明が入ります。**UE 5.8+ は影響を受けません** — こちらの分岐は元々（未解決のシステムやクラスで）失敗しうる作りであり、その挙動は変わっていません。実際のプロパティ値を見るには、どのエンジンバージョンでも従来どおり `GetRendererData` / `GetEmitterData` / `GetSystemData` を読むこと。
>
> **Note — 失敗した `GetDynamicInputSchema` は、失敗理由を6種類の `FailureReason` のいずれかに分類し、エンジンの文面を転送するのではなく自身の文章を組み立てます。** `ErrorCode` はどの場合も `ExecutionFailed` のままです — 6種類を見分けるのは `Result.FailureReason` だけです: `NestedStackOnAssignmentModule`（対象が Set Parameters モジュールであり、`InputNameStack` は単一要素しか受け付けないのに複数要素が渡された）、`AssignmentTargetNotFound`（Set Parameters モジュールにその名前の Assignment Target が無い）、`InputNotFound`（そのモジュール・dynamic input スクリプトのどちらを見ても名前が入力に解決しない）、`NoOverridePin`（入力は存在するが上書きが一切設定されておらず、自身の既定値のまま）、`OverrideIsNotDynamicInput`（入力の上書きは存在するが、それ自体は dynamic input ではない別のスクリプトを指している）、`InputIsNotDynamic`（入力は存在するが Dynamic モードになっていない）。失敗がこの6種類のどれにも当てはまらない場合（例えばシステム・スクリプト・モジュール自体が解決できなかった場合）、`FailureReason` は応答に含まれません。**UE 5.8+ では、`NoOverridePin` と `OverrideIsNotDynamicInput` を、純粋に Dynamic でない入力と見分けられません** — エンジン自身の公開トポロジ API は、この3つをすべて `InputIsNotDynamic` として報告します。UE 5.7 はグラフを直接読むため、6種類すべてを区別できます。この集約が発生する場合、応答には `FailureReason: "InputIsNotDynamic"` に加えて `Result.AmbiguousFailureReasons: ["NoOverridePin", "OverrideIsNotDynamicInput"]` も含まれ、呼び出し側は「厳密にこれだと判定された」のか「どちらか見分けられなかった」のかを区別できます — このフィールドは、実行中のエンジンバージョンが両者を区別できる場合には現れません。`ErrorMessage` は常に UAIP 自身が組み立てた文面であり、エンジンの文字列がそのまま転送されることはありません。
>
> **Note — `GetStackInputSchema`・`GetStackInputTopology`・`GetDynamicInputSchema`・`GetAvailableDynamicInputs` は、`InputNameStack` パラメータが受け付ける書き方を広げるようになりました。ただし到達できる入力の集合は広がりません。** `GetStackIssues` の `Location.InputNameStack`（後述）には、それ自体は Dynamic モードの入力ではない conditional / static-switch 構造の先頭部分が含まれることがあります — この構造は、この4コマンド自身が持つフラットな単一要素検索がそもそも直接到達できるものです。これまでは、このスタックをそのままこの4コマンドのいずれかへ渡すと、指している葉が短いスタックでも到達可能であるにもかかわらず、その先頭要素で失敗することがありました。この4コマンドは現在、まず渡されたスタックをそのまま試し、それで解決しない場合は、それ自体が Dynamic モードと報告されない最初の要素までの先頭部分を取り除いたうえで、残りを単一要素検索として解決します — ただし、その短縮形が対象モジュール配下でちょうど1つの入力にのみ一致する場合に限ります。**到達できる入力の集合は変わりません。変わるのは、同じ入力を指すのに必要な要素数だけです。** 短縮した先頭名がそのモジュール配下で複数の入力に一致する場合（異なる親の配下に同じ名前が存在する場合）は、推測で1つを選ばずに拒否されます。また、どの書き方で渡しても解決しない名前は、引き続き拒否されます。これにより、`GetStackIssues` の `Location.InputNameStack` を、呼び出し側が短いパスを手で組み立て直すことなく、そのままこの4コマンドのいずれかへ渡せるようになります。

#### スタック Issue（2）

| コマンド | 説明 |
|---|---|
| `GetStackIssues` 🧩 | システム全体のスタック Issue（エラー / 警告 / 情報、dismiss 済みを含む）と `IssueId`・`FixId`。UE 5.8+ 専用。UE 5.7 では `Available: false` |
| `ApplyStackIssueFix` 🧩 | `IssueId` + `FixId` を指定して Fix 形式の自動修正を適用（Link 形式は拒否・`NiagaraStackAutoFix` 必要）。UE 5.8+ 専用。UE 5.7 では `Available: false` |

> **Note — `GetStackIssues` が返す各 issue の `Location` オブジェクトは、該当する方に応じて `InputNameStack` か `RendererIndex` のどちらかを持ち、issue がモジュールやシステム全体を指す場合はどちらも持ちません。** `Location` は常に `EmitterName`・`ScriptName`・`ModuleName` を持ちます。issue が特定のスタック入力を指す場合、`Location` はさらに `InputNameStack` を持ちます — これは `GetStackInputSchema`・`GetStackInputTopology`・`GetDynamicInputSchema`・`SetStackInputData` が自身の `InputNameStack` パラメータとして受け付けるのと同じ、モジュールレベルから末端の入力までの順序付き名前配列です。issue がレンダラーを指す場合は、代わりに `RendererIndex` を持ちます。この2フィールドは互いに排他的で、該当しない場合に空配列や `-1` で埋められることもありません — フィールドの**値**ではなく**存在そのもの**が「該当するかどうか」を表します。`GetStackIssues` が返した `InputNameStack` を、パスを組み立て直すことなくそのまま上記4コマンドのいずれかへ渡せば、issue が指す入力をそのまま調べたり修正したりできます。`GetStackIssues` 自体が UE 5.8+ 専用（前述）なので、`Location` とこの往復も UE 5.8+ でのみ成立します。
>
> **⚠️ Breaking change — `GetStackIssues` と `ApplyStackIssueFix` は UE 5.7 では一切使えなくなりました。これまで `ExecutionFailed` で失敗していましたが、現在は `uaip_list_commands` の既定一覧にも出てきません。** どちらもこれまでどのエンジンバージョンでも `Available: true` を報告してハンドラまで到達させており、当初のフォールバックは無条件に成功を報告していました（`GetStackIssues` は空の `Issues` 配列、`ApplyStackIssueFix` は `{Applied: false}`）。その後 `ExecutionFailed` へ変更され、`ErrorMessage` に説明が入るようになりました — いずれの版でも「issue が存在しない」「この fix は適用できなかった」と読めてしまい、そもそもチェックが実行されていないことと区別できない、という問題がありました。**拒否のタイミングが再び移動し、今度は実行時ではなく照会時になりました。** `UAIP.Core.DescribeCommand` と `uaip_list_commands` は、UE 5.7 ではどちらも最初から `Available: false` を報告し、`UnavailableReason: "HandlerUnavailable"` / `UnavailableDetail: "EngineVersion"` が付きます。UE 5.7 でどちらかを名前指定して呼び出すと依然として失敗しますが、今度は `ExecutionFailed` ではなく `PolicyViolation` になり、`ErrorMessage` には同じ説明が入ります。**UE 5.7 では「エンジンバージョンによる拒否」と「この Fix は正当に適用できなかった」を区別していた仕組みそのものが無くなります** — `ApplyStackIssueFix` へ UE 5.7 から到達する経路自体が消えるためです。**両コマンドとも UE 5.8+ は影響を受けません**。`ApplyStackIssueFix` の通常の `{Success: true, Applied: false}` という結果も、元からこの形で報告されており、そのまま変わっていません。

#### 編集（21）

| コマンド | 説明 |
|---|---|
| `AddEmitter` 🧩 | Niagara システムにエミッターを追加 |
| `RemoveEmitter` 🧩 | エミッターを削除 |
| `DuplicateEmitter` 🧩 | エミッターを複製。このネイティブコマンドでは使えず、対応する Toolset ブリッジ側にも動く委譲先がありません — 後述の注記を参照 |
| `SetEmitterEnabled` 🧩 | エミッターの有効/無効を切り替え |
| `SetEmitterName` 🧩 | エミッターの名前を変更 |
| `SetEmitterData` 🧩 | エミッターのデータを設定 |
| `AddRenderer` 🧩 | エミッターにレンダラーを追加 |
| `RemoveRenderer` 🧩 | レンダラーを削除 |
| `SetRendererData` 🧩 | レンダラーのデータを設定（`NiagaraStackEdit` 必須）。指定クラスのレンダラーがエミッタに無い場合は `NotFound` を返すようになりました — 最初に見つかった別のレンダラーへ書き込むフォールバックは廃止されています。書き込み経路が扱えないプロパティ名は黙って無視されず、リクエスト全体が `PolicyViolation` で失敗します。構造体の初期値が途中までしか解釈できない場合は「既定値として解釈した」成功ではなく `InvalidParams` で拒否されます。成功時は `PostEditChangeProperty` を呼ぶため、変更がエディタへ即座に反映されます |
| `AddModule` 🧩 | エミッターのモジュールスタックにモジュールを追加 |
| `RemoveModule` 🧩 | モジュールを削除 |
| `MoveModule` 🧩 | スタック内でモジュールを移動。このネイティブコマンドでは使えず、対応する Toolset ブリッジ側にも動く委譲先がありません — 後述の注記を参照 |
| `SetModuleEnabled` 🧩 | モジュールの有効/無効を切り替え |
| `SetStackInputData` 🧩 | モジュールスタック入力値を設定 |
| `SetSystemData` 🧩 | システムのデータを設定 |
| `AddUserVariables` 🧩 | システムにユーザー変数を追加 |
| `RemoveUserVariables` 🧩 | ユーザー変数を削除 |
| `CompileNiagaraSystem` 🧩 | Niagara システムをコンパイル |
| `AddSetParametersModule` 🧩 | Set Parameters モジュールをスタックに追加し、初期パラメータエントリを登録する。`DefaultValue` フィールドは一般的な型（float / int / bool / struct）に加え、`NiagaraReferenceEdit` があればオブジェクトパスで渡したデータインターフェース / オブジェクト型パラメータにも適用される — 下の Note を参照。 |
| `AddSetParameterEntry` 🧩 | 既存の Set Parameters モジュールにパラメータエントリを追加する。`ScriptName`（例：`Spawn` / `Update`）が必須。`DefaultValue` フィールドは一般的な型（float / int / bool / struct）に加え、`NiagaraReferenceEdit` があればオブジェクトパスで渡したデータインターフェース / オブジェクト型パラメータにも適用される — 下の Note を参照。 |
| `RemoveSetParameterEntry` 🧩 | Set Parameters モジュールからパラメータエントリを削除する。`ScriptName`（例：`Spawn` / `Update`）が必須。 |

> **⚠️ Breaking change — `DuplicateEmitter` と `MoveModule` は、これらのネイティブコマンド経由ではどのエンジンバージョンでも呼び出せません。** 内部で呼んでいるエンジン側 API（`FNiagaraSystemViewModel::DuplicateEmitters` と `FNiagaraStackGraphUtilities::MoveModule`）がエンジンモジュールの外へ export されていないため、そもそも実行に到達できませんでした — これまでは何を渡しても実行時に `NotAllowed` で失敗していました。現在は `UAIP.Core.DescribeCommand` と `uaip_list_commands` が、どのエンジンバージョンでも両方とも `Available: false` を報告し、`UnavailableReason: "HandlerUnavailable"` / `UnavailableDetail: "EngineApiNotExported"` が付きます。**エンジンを上げても解決しません** — export の欠落はどのバージョンでも同じだからです。名前指定で呼び出すと依然として失敗しますが、今度は `PolicyViolation` になり、`ErrorMessage` には同じ説明が入ります。
>
> **⚠️ 更新 — Toolset ブリッジ側の同等コマンドも、この穴を埋めません。** `Toolset.Editor.Niagara.DuplicateEmitter` と `Toolset.Editor.Niagara.MoveModule` は、エンジン自身の toolset 経由で同じ操作に到達できると想定されていましたが、`NiagaraToolsets` プラグインは、このプラグインが対応するどのエンジンバージョンでも、どちらの名前の関数も宣言していません。この 2 件のブリッジコマンドも `Available: false` を返すようになり、`UnavailableDetail: "DelegationTargetMissing"` が付きます（後述の Toolset ブリッジの注記を参照）。**本更新時点で、どちらの操作もこのプラグイン内に動く経路が 1 つもありません。**
>
> **⚠️ 挙動の変更 — 参照型の `DefaultValue` が、捨てられずに書き込まれるようになりました。** パラメータの型がデータインターフェースまたはオブジェクト参照の場合、`AddSetParameterEntry` / `AddSetParametersModule` は従来 `DefaultValue` を**黙って無視**していました（リクエストは成功し、既定値の無いエントリが作られていました）。今後は値をオブジェクトパスとして渡すと、`FNiagaraVariant` のデータインターフェース / オブジェクト専用スロットへ保存されます。ここでは参照が正しく保持され、他のパラメータ型が使うバイト列へ詰め込まれることはありません。成功の代わりに返りうるもの:
>
> - `CapabilityNotAvailable` — セッションが `NiagaraReferenceEdit` を保有していない（両コマンドが元から要求する `NiagaraStackEdit` に**追加で**必要）。拒否の返答にこの名前が載ります。
> - `NotFound` — オブジェクトパスが指すアセットをまだ何もロードしていない。書き込みが副作用でアセットをロードすることはないため、先にアセットを開いてください（「存在しない」と「存在するが未ロード」は同じ拒否として返ります）。
> - `InvalidParams` — オブジェクトは解決できたが、パラメータ型のクラスではない。
>
> Capability を付与し、対象がロード済みであれば書き込みは成功し、参照が保持されます。**`DefaultValue` を指定しない場合の挙動は従来どおり**です — 追加の Capability は不要で、既定値の無いエントリが作られます。
>
> ⚠️ **実運用で到達できるのはデータインターフェース型だけです。** パラメータの型名は値を見るより前に型の許可リストと突き合わされるため、`UTexture2D` のような通常のオブジェクト型はその段階で `InvalidParams`（拒否した型名を明記）となり、`NiagaraReferenceEdit` の出番はありません。Niagara の**ユーザー**パラメータ（`AddUserVariables`）は別のストアで、そもそも既定値を受け取りません。
>
> **⚠️ 挙動変更 — 解決できない型は、float に置き換えられず拒否されます。** 両コマンドは以前、解決できない型を指定されるとエントリを `float` として作ったうえで成功を返していました。気付く手段は読み戻して要求と違う型を見つけることだけでした。現在は拒否した型名を添えて `InvalidParams` を返します。`AddSetParametersModule` はモジュールを作る前に拒否するため、2 件目のパラメータが解決できない要求で「解決できた分だけを持つモジュール」が残ることはありません。`ParsedAsDefault` / `ParsedAsDefaultArray` は「型が解決できなかった」という意味を含まなくなり、値が型の既定へ落ちたことだけを表します。
>
> 書き込んだ既定値は**読み戻せます**。`GetStackInputData` が各入力の現在値を返すため、Set Parameters エントリへの書き込みは確認できます。
>
> **Note — `AddSetParameterEntry` と `AddSetParametersModule` の `TypePath` が、どのエンジンバージョンでも読み取りが返すベア型名も受け付けるようになりました。** これまで `TypePath` は短縮形（`float`、`Vector3f`）か完全なオブジェクトパス（`/Script/Niagara.NiagaraFloat`）しか解決していませんでした。現在は読み取り系の `Type` フィールドが元から報告しているベア型名 — `NiagaraFloat`、`ENiagaraCoordinateSpace`、`NiagaraDataInterfaceCurve`、`Quat4f` など — も解決します。これにより、`GetModuleTopology`・`GetEmitterTopology`・`GetScriptStackTopology`・`GetStackInputTopology`・`GetStackInputSchema`・`GetModuleSchema`・`GetDynamicInputSchema`・`GetDynamicInputSchemaFromAsset`・`GetModuleSchemaFromAsset` のいずれかで読み取った型名を、そのまま `TypePath` へ渡せます（これまで存在しなかった往復が成立するようになりました）。**`TypePath` が受け付ける型の集合は変わっていません** — ベア名も、登録済みの Niagara 型一覧を経由したうえで、他の2つの綴りと同じ許可リストを通ります。到達できるようになった型は1つもなく、綴りが広がっただけです。従来の2つの綴りはこれまでどおり解決でき、解決できない名前は引き続き拒否した型名を添えて `InvalidParams` を返します。

#### Blueprint ラッパー（2）

| コマンド | 説明 |
|---|---|
| `ConstructNiagaraBPWrapperFromSystem` 🧩 | NiagaraSystem アセットのユーザー変数を Blueprint 変数として持つ AActor BP ラッパーを生成する（Two-Phase Commit） |
| `ConstructNiagaraBPWrapperFromComponent` 🧩 | エディタワールド上のアクターの NiagaraComponent からコンポーネント変数オーバーライド値を保持した BP ラッパーを生成する（Two-Phase Commit） |

### Toolset ブリッジ（45）🧩

`NiagaraToolsets` プラグイン（UE 5.8+ Experimental）経由でネイティブコマンドを委譲。プロバイダ：`Toolset.Editor.Niagara.*`。グループ：Info（2）/ Blueprint（2）/ System Schema（12）/ Topology（5）/ Data（5）/ Edit-1（8）/ Edit-2（8）/ Diagnostic（3）。

> **⚠️ 破壊的変更 — `Toolset.Editor.Niagara.SetRendererData` が要求する Capability が `NiagaraStackEdit` になりました**（ネイティブ版と同じ名前）。従来は `NiagaraEmitterEdit` を要求していたため、運用者が `NiagaraStackEdit` を閉じてもブリッジ経由で同じ書き込みが通っていました。**`NiagaraEmitterEdit` だけを付与していたセッションはこのコマンドを使えなくなります** — `NiagaraStackEdit` を追加してください。
>
> **ブリッジ経由では UAIP の値検査が及びません。** ブリッジの書き込みはエンジンの toolset の内部で行われるため、ネイティブ版が適用する型ゲート・途中終了パースの検査・全件不可なら 1 件も書かない扱いは適用されません。検査が必要な場合はネイティブの `SetRendererData` を使ってください。
>
> **⚠️ Breaking change — このうち 6 件のブリッジコマンドは、どのエンジンバージョンでも呼び出せません：`GetScriptAssets` / `GetNiagaraParameterCollections` / `SetEmitterEnabled` / `SetEmitterName` / `DuplicateEmitter` / `MoveModule`。** これら 6 件が委譲する Niagara toolset は、6 つの名前のいずれにも一致する関数を宣言していないため、このプラグインが対応するどのエンジンバージョンでも、転送された呼び出しは実装に到達できませんでした——これまでは何を渡しても実行時に汎用的な `ExecutionFailed` で失敗していました。現在は 6 件すべてが `UAIP.Core.DescribeCommand` と `uaip_list_commands` で `Available: false` を返し、`UnavailableReason: "HandlerUnavailable"` / `UnavailableDetail: "DelegationTargetMissing"` が付きます。名前指定で呼び出すと依然として失敗しますが、今度は `PolicyViolation` になり、`ErrorMessage` には同じ説明が入ります。
>
> **6 件のうち 4 件には動くネイティブ代替があります**：`UAIP.Editor.Niagara.GetScriptAssets` / `GetNiagaraParameterCollections` / `SetEmitterEnabled` / `SetEmitterName` は委譲せずに同じ操作を行い、この変更の影響を受けません。
>
> **`DuplicateEmitter` と `MoveModule` にはありません。** 対応するネイティブコマンド自体が、別の理由で利用不可になっています（上の「編集」節の Breaking change 注記を参照）——必要とするエンジン側 API が、どのエンジンバージョンでもプラグインへ export されていないためです。**本更新時点で、どちらの操作もこのプラグイン内に動く経路が 1 つもありません** — ネイティブコマンドでも、このブリッジでも。
>
> **7 件目として `GetSystemInfo` が加わりました。** 全件の突き合わせにより、`Toolset.Editor.Niagara.GetSystemInfo` も委譲先が存在しないことが分かりました。toolset が宣言しているのは `GetSystemSummary` と `GetSystemData` で、どちらもこのコマンドの呼び出し元に約束された形を返しません。`Available: false` と `UnavailableDetail: "DelegationTargetMissing"` を返すようになりました。**`UAIP.Editor.Niagara.GetSystemInfo`** が同じ操作をネイティブで行います。
>
> **逆に `GetAssetDiscoveryInfo` は動くようになりました。** このコマンドは `NiagaraToolset_Info` へ委譲していましたが、実物は `NiagaraToolset_Assets` にあり、ToolsetRegistry は 1 回の完全一致検索でしか解決しないため到達していませんでした。宛先を修正済みです。

> **引数は Niagara Toolset が宣言する形に揃えています。**
>
> - **参照引数は、オブジェクトパスの文字列でも `{"refPath": "..."}` でも渡せます。** このセクションの全コマンドの、アセット・クラス・`System` の参照が対象です。どちらの形も以前から受け付けていました。ブリッジは Toolset へ `{"refPath": ...}` で送ります。
> - **スタック項目の参照は、メンバーとその既定値を宣言します。** 参照を取る 19 コマンド（`AddRenderer`・`AddSetParameterEntry`・`AddSetParametersModule`・`GetDynamicInputSchema`・`GetEmitterData`・`GetEmitterTopology`・`GetModuleSchema`・`GetModuleTopology`・`GetRendererData`・`GetScriptStackTopology`・`GetStackInputData`・`GetStackInputSchema`・`GetStackInputTopology`、および次の項目の 6 コマンド）のスキーマに、`EmitterName` / `ScriptName` / `ModuleName`（既定値 `"None"`）、`RendererIndex`（既定値 `-1`）、`InputNameStack`（省略すると空配列を送る）が載ります。Toolset 自身の既定値なので、メンバーを省略した呼び出しの意味は以前と変わりません。
> - ⚠️ **次の 6 コマンドは、スタック項目の参照を中身を検査しないオブジェクトで受けていましたが、宣言するようになりました:** `RemoveRenderer`（`RendererToRemove`）、`RemoveSetParameterEntry` と `SetModuleEnabled`（`ModuleRef`）、`SetEmitterData`（`Emitter`）、`SetRendererData`（`Renderer`）、`SetStackInputData`（`StackInputRef`）。`System` は必須（パス文字列または `{"refPath": ...}`）、`EmitterName` / `ScriptName` / `ModuleName` は文字列、`RendererIndex` は整数、`InputNameStack` は配列です。`System` の欠落や、メンバーの型違い（たとえば整数でない `RendererIndex`）は、Toolset を呼ぶ前に `InvalidParams` で断ります。参照の中の宣言していないメンバーは受け付けて無視します（Toolset へは送りません）。これは上の 6 コマンドに限らず、スタック項目の参照を取る 19 の Niagara コマンド（上の 6 コマンドに加えて `AddSetParametersModule`・`AddSetParameterEntry`・`AddRenderer`・`GetEmitterTopology`・`GetEmitterData`・`GetScriptStackTopology`・`GetModuleTopology`・`GetModuleSchema`・`GetStackInputData`・`GetStackInputTopology`・`GetStackInputSchema`・`GetRendererData`・`GetDynamicInputSchema`）に共通です。
> - ⚠️ **`SetEmitterData`（`EmitterData`）・`SetRendererData`（`RendererData`）・`SetSystemData`（`SystemData`）は `PropertyValues` だけを取ります**（文字列、必須）。ほかのメンバー、`PropertyValues` の欠落、文字列でない値は `InvalidParams` で断ります。
> - ⚠️ **`GetAvailableDynamicInputs` は `Type` の中に `ClassStructOrEnum` だけを取ります**（必須。パス文字列または `{"refPath": ...}`）。ほかのメンバーや `ClassStructOrEnum` の欠落は `InvalidParams` で断ります。
> - **次の 5 つの引数の要素の形を宣言するようになりました:** `AddUserVariables`（`VariablesToAdd`）・`RemoveUserVariables`（`VariablesToRemove`）・`AddSetParametersModule`（`Parameters`）・`AddSetParameterEntry`（`Entry`）・`SetStackInputData`（`InputData`）。以前は検査しない値の配列、または開いたオブジェクトで受けていました。
>   - 変数は `Name`（文字列、必須）と `Type.ClassStructOrEnum`（必須。パス文字列または `{"refPath": ...}`。Toolset へは `{"refPath": ...}` で送ります）です。`AddUserVariables` は `Description`（文字列、既定値 `""`）も取ります。`AddSetParametersModule` では同じ 2 つが `Variable` の下（`Variable.Name`・`Variable.Type.ClassStructOrEnum`）に、`AddSetParameterEntry` では `Entry.Variable` の下にあります。`RemoveUserVariables` は、Toolset が名前と型の両方でパラメータを探すため、どちらも必要です。
>   - `DefaultValue`（`VariablesToAdd` の要素、`Parameters` の要素、`Entry` の中）は省略可能で、`Struct`（パス文字列または `{"refPath": ...}`）と `value`（中身が構造体ごとに違い、検査しないオブジェクト）の 2 メンバーを持ちます。両方を渡すか、両方とも渡さないかにしてください。片方だけはスキーマを通りますが、Toolset が断ります。`DefaultValue` を省略した呼び出しは従来どおり動きます。
>   - `SetStackInputData` は `InputData.Struct`（必須。パス文字列または `{"refPath": ...}`）と `InputData.value`（必須のオブジェクト）を取ります。`value` は Toolset が読む綴りで、`GetStackInputData` が返す綴りでもある小文字なので、結果をそのまま渡せます。
>   - これらの形の要素や、その中のどの階層でも、宣言していないメンバーは受け付けて無視します（従来どおり Toolset へは送りません）。裸の文字列の要素と、`Name`・型・`Struct`・`value` の欠落は、Toolset も断っていたので `InvalidParams` で断ります。上に挙げたスタック項目の参照（`ModuleRef` など）の中も同じで、断るのは `System` の欠落とメンバーの型違いだけです。

---

## UAIP.Editor.Physics

Physics Asset 編集 — ボディ・シェイプ・コンストレイント。

### ネイティブ（31）

#### アセット / 観測（3）

| コマンド | 説明 |
|---|---|
| `CreatePhysicsAsset` | SkeletalMesh から Physics Asset を生成・リンク |
| `GetPhysicsAssetSummary` | ボディ数・コンストレイント数などのサマリ |
| `ValidatePhysicsAsset` | 孤立コンストレイント・形状なしボディなどの問題を検出 |

#### ボディ（15）

| コマンド | 説明 |
|---|---|
| `GetBodyNames` | Physics Asset のボディ名一覧 |
| `AddBody` | 指定ボーンにボディを追加 |
| `RemoveBody` | ボディを削除（関連コンストレイントも連鎖削除） |
| `GetBodyPhysicsMode` | ボディの PhysicsMode を取得（Default / Kinematic / Simulated） |
| `SetBodyPhysicsMode` | ボディの PhysicsMode を設定 |
| `SetAllBodiesPhysicsMode` | 名前パターンに一致する全ボディの PhysicsMode を一括設定 |
| `GetBodyMassScale` | ボディの MassScale を取得 |
| `SetBodyMassScale` | ボディの MassScale を設定 |
| `GetBodyCollisionProfile` | ボディの Collision Profile 名を取得 |
| `SetBodyCollisionProfile` | ボディの Collision Profile を設定 |
| `SetBodyLinearDamping` | ボディの Linear Damping を設定 |
| `SetBodyAngularDamping` | ボディの Angular Damping を設定 |
| `GetBodyOffset` | ボディの Center of Mass オフセット（COMNudge）を取得 |
| `SetBodyOffset` | ボディの Center of Mass オフセットを設定 |
| `MirrorBodies` | 命名規則に従い左右ボーンのボディ・形状をミラーコピー |

#### シェイプ（8）

| コマンド | 説明 |
|---|---|
| `GetBodyShapes` | 指定ボディのコリジョン形状一覧（ShapeName 付き） |
| `SetSphere` | 指定ボディのコリジョン形状を Sphere に設定 |
| `SetCapsule` | 指定ボディのコリジョン形状を Capsule に設定 |
| `SetBox` | 指定ボディのコリジョン形状を Box に設定 |
| `RemoveShape` | 指定 ShapeName の形状を削除 |
| `RegenerateBodyShapes` | ボーンのジオメトリから形状を自動再生成 |
| `CopyBodyShapes` | あるボーンの形状を別ボーンにコピー |
| `SetPhysicalMaterial` | ボディまたは全ボディに Physical Material を設定 |

#### コンストレイント（5）

| コマンド | 説明 |
|---|---|
| `GetConstraints` | アセット全コンストレイントを取得（上限 256 件） |
| `ListConstraintsForBody` | 特定ボーンに接続されているコンストレイント一覧（上限 256 件） |
| `AddConstraint` | 剛体コンストレイントを追加 |
| `SetConstraintLimits` | コンストレイントの角度制限を設定 |
| `RemoveConstraint` | コンストレイントを削除 |

### Toolset ブリッジ（17）🧩

`PhysicsToolsets` プラグイン（UE 5.8+ Experimental）経由でネイティブコマンドを委譲。プロバイダ：`Toolset.Editor.Physics.*`。

---

## UAIP.Editor.Dataflow 🧩

Dataflow グラフ編集。`DataflowEditor` プラグインが必要です。

| コマンド | 説明 |
|---|---|
| `GetDataflowGraphInfo` 🧩 | グラフのノード / エッジ / 変数を取得（JSON）。各ノードは `NodeName`（グラフ内の実名。`SetGroomDataflowAsset` の `TerminalNodeName` 等で指定するのはこちら）と `DisplayName`（ノード型の表示名）の両方を返す |
| `ListDataflowNodeTypes` 🧩 | 利用可能な Dataflow ノードタイプ一覧 |
| `AddDataflowNode` 🧩 | Dataflow グラフにノードを追加。任意の `NodeName` でグラフ内の名前を指定できる（省略時はノード型名を基底とした一意名を採番）。確定した名前は応答の `NodeName` に含まれる |
| `RemoveDataflowNode` 🧩 | Dataflow グラフからノードを削除 |
| `ConnectDataflowPins` 🧩 | 2 ピンを接続 |
| `DisconnectDataflowPins` 🧩 | ピン接続を切断 |
| `ListDataflowVariables` 🧩 | グラフ変数一覧 |
| `GetDataflowNodeProperty` 🧩 | ノードの `EditAnywhere` プロパティ値を取得（プリミティブ / enum / FName / FString / 単純構造体） |
| `SetDataflowNodeProperty` 🧩 | ノードの `EditAnywhere` プロパティ値を設定。ドメイン非依存（Cloth の Weight Map・シミュレーション設定ノード等から利用される）。参照・構造体・コンテナは `ValueJson` で書き込み、コンテナの要素 1 つは `Operation` / `ElementIndex` / `ElementKeyJson` で指定する — [参照・構造体・コンテナの書き込み](#参照構造体コンテナの書き込み) を参照。参照に触れる書き込みは `DataflowGraphEdit` に加えて `DataflowReferenceEdit` が必要で、構造体・コンテナにはさらに `PropertyStructuredEdit` が必要。ハード参照（例: `TObjectPtr<UGroomAsset>`）の値は**既にロード済み**のアセットのオブジェクトパス — プロパティ書き込みが副作用でアセットをロードすることはない。ソフト参照はアセットレジストリに対して検証されるため、対象のロードを必要としない |

### Toolset ブリッジ — Dataflow（7 件）🧩

`DataflowAgentToolset`（UE 5.8+）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.DataflowAgent.*`。編集系は `DataflowGraphEdit` が必要です。

> **このセクションの 7 件は、本更新まで 1 件も動いていませんでした。** 委譲先の toolset 名を**モジュール修飾なしの `DataflowAgentToolset`** として渡しており、正しい `DataflowAgent.DataflowAgentToolset` に一致していませんでした（ToolsetRegistry は 1 回の完全一致検索でしか解決しません）。加えて `ConnectDataflowPins` と `DisconnectDataflowPins` は tool 名も誤っており、toolset の実際の名前は `ConnectNodePins` / `DisconnectNodePins` です。**7 件とも修正され、実際に動作します。**

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.DataflowAgent.ListDataflowNodeTypes` | 利用可能な Dataflow ノード型の一覧（common 型のみ） |
| `Toolset.Editor.DataflowAgent.GetDataflowGraphInfo` | Dataflow アセットのノード・接続構造 |
| `Toolset.Editor.DataflowAgent.ListDataflowVariables` | Dataflow アセットの変数一覧 |
| `Toolset.Editor.DataflowAgent.AddDataflowNode` | Dataflow グラフにノードを追加（`DataflowGraphEdit` 必要） |
| `Toolset.Editor.DataflowAgent.RemoveDataflowNode` | Dataflow グラフからノードを削除（`DataflowGraphEdit` 必要） |
| `Toolset.Editor.DataflowAgent.ConnectDataflowPins` | 2 ピンを接続（`DataflowGraphEdit` 必要） |
| `Toolset.Editor.DataflowAgent.DisconnectDataflowPins` | ピン接続を切断（`DataflowGraphEdit` 必要） |

---

## UAIP.Editor.ChaosClothAsset 🧩

Chaos Cloth Asset 編集と `ChaosClothAssetToolset` ブリッジ（UE 5.8, Experimental）。`ChaosClothAsset` プラグイン群が必要です。

| コマンド | 説明 |
|---|---|
| `CreateClothingAsset` | Skeletal Mesh から Clothing Asset を作成 |
| `AssignClothingToSection` | Clothing Asset を Skeletal Mesh の LOD/セクションにバインド |
| `RemoveClothingFromSection` | セクションから Clothing Asset のバインドを解除（破壊的・不可逆） |
| `ListClothingAssets` | Skeletal Mesh にバインド済みの Clothing Asset 一覧 |
| `GetSectionClothing` | 指定した LOD/セクションにバインドされている Clothing Asset を取得 |
| `ConvertClothingAssetCommonToChaosClothAsset` | legacy `UClothingAssetCommon` を `UChaosClothAsset` に変換（Experimental、LOD0のみ） |
| `GetClothAssetInfo` | LOD数・Sim/Render Mesh頂点数・参照している `UDataflow` アセットパス・Weight Map属性名一覧を取得 |
| `SetClothWeightMapVertexValues` | Weight Map ノードの頂点重み配列を直接設定（破壊的） |
| `SetClothMeshImportSource` | Import Dataflow ノード（`SkeletalMeshImport`/`StaticMeshImport`）にインポート元の SkeletalMesh/StaticMesh 参照を設定。ノード種別は自動判定、既存参照の上書きには `AllowOverwrite` が必要（破壊的） |
| `CreateLegacyClothingAsset` | 既存 SkeletalMesh の描画セクションからシミュレーションメッシュを抽出し、新規 legacy `UClothingAssetCommon` を作成 |

`GetClothAssetInfo` が返す `UDataflow` 参照パスを `UAIP.Editor.Dataflow.*` コマンドに渡すことで、Weight Map・シミュレーション設定ノードのプロパティを汎用的に編集できます。

### Toolset ブリッジ（6）

`ChaosClothAssetToolset` の6関数をそのままミラー。プロバイダ：`Toolset.Editor.ChaosClothAsset.*`。UE 5.8+ かつ `ChaosClothAssetToolset` + `ToolsetRegistry` 有効時のみ利用可能。

> ⚠️ **`AssignClothingToSection`・`GetSectionClothing`・`RemoveClothingFromSection` は整数を取ります。** `LodIndex`・`SectionIndex`、および `AssignClothingToSection` の `ClothingLodIndex` は数値として宣言されていました。小数部のない数値は受け付けます（`1` も `1.0` も添字 1 です）。小数部のある値（例: `1.5`）は `InvalidParams` で断ります。以前は、そうした値を Toolset が 0 方向へ切り捨てて受け取っていたため、`1.5` が添字 `1` に効き、指定とは別の位置を操作していました。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.ChaosClothAsset.CreateClothingAsset` | `ChaosClothAssetToolset` への委譲 |
| `Toolset.Editor.ChaosClothAsset.AssignClothingToSection` | `ChaosClothAssetToolset` への委譲 |
| `Toolset.Editor.ChaosClothAsset.RemoveClothingFromSection` | `ChaosClothAssetToolset` への委譲 |
| `Toolset.Editor.ChaosClothAsset.ListClothingAssets` | `ChaosClothAssetToolset` への委譲 |
| `Toolset.Editor.ChaosClothAsset.GetSectionClothing` | `ChaosClothAssetToolset` への委譲 |
| `Toolset.Editor.ChaosClothAsset.ConvertClothingAssetCommonToChaosClothAsset` | `ChaosClothAssetToolset` への委譲 |

---

## UAIP.Editor.Skeleton

Skeleton と SkeletalMesh 編集。

| コマンド | 説明 |
|---|---|
| `GetSkeletonInfo` | USkeleton のボーン階層・ソケット・バーチャルボーン（JSON、読み取り専用） |
| `AddSocket` | 指定ボーンにソケットを追加 |
| `RemoveSocket` | ソケットを削除 |
| `SetSocketTransform` | ソケットのトランスフォームを部分更新（省略フィールドは既存値を保持） |
| `AddVirtualBone` | バーチャルボーンを追加（名前省略時は自動生成） |
| `RemoveVirtualBone` | バーチャルボーンを削除 |
| `GetSkeletalMeshInfo` | USkeletalMesh の LOD・マテリアルスロット・関連 Skeleton パス（読み取り専用） |
| `SetSkeletalMeshMaterial` | SkeletalMesh のマテリアルスロットにマテリアルを割り当て |
| `CreateBlendProfile` | Skeleton に BlendProfile を新規作成 — `Mode` は `TimeFactor` / `WeightFactor` / `BlendMask` のいずれか（`LayeredBoneBlend` ノードの `BlendMasks` に割り当てる場合は `BlendMask` を使う。他の 2 モードはそこでは何も効果を持たない） |
| `SetBlendProfileBoneScale` | 既存の BlendProfile 内にある 1 ボーンの Blend Scale を設定 |
| `ListBlendProfiles` | Skeleton に登録済みの BlendProfile を列挙（読み取り専用） |

> **Note**: このドメインの書き込みコマンドはすべて、`/Game/` プレフィックスの条件は満たすもののより深い検証に失敗するパス（`..` によるパストラバーサル・512 文字超過・不可視の制御文字・不正なパッケージ名）に対して、従来の `NotFound` ではなく `NotAllowed` を返すようになりました。これは破壊的変更ではありません — これらのパスは従来も成功しておらず、この端ケース固有の従来のエラーコードもドキュメント化されていませんでした — が、`ErrorCode` でパス拒否を判定しているツールがあれば留意してください。

---

## UAIP.Editor.MetaHuman 🧩

MetaHuman キャラクターのオーサリング — アセット作成、体型 / 肌 / 眼 / メイク設定、顔の造形、コンフォーム・フィッティング、クラウドリギング、テクスチャ合成、ワードローブ、プレビュー、アセットビルドパイプライン。`MetaHumanCharacter` プラグインが必要です（無効な場合、これらのコマンドは一切登録されません）。

編集系コマンドは必要に応じて MetaHuman 編集セッションを開き、そのまま保持します（同一キャラクターに対する連続実行で再オープンのコストを払わないため）。セッションを開くこと自体が編集モードへの移行であるため、**このドメインの読み取り系コマンドの多くは読み取り専用ではありません** — `MetaHumanEdit` を必要とし、SafetyPolicy が読み取り専用モードのときは拒否されます。一連の作業が終わったら `ReleaseEditSession` を呼んでください。唯一の例外は `GetViewportSettings` で、`EditorInspect` のみで実行できます。

**⬆️ = UE 5.8 以降専用。** 以下 56 コマンドのうち 14 コマンドは UE 5.7 に存在しないエンジン API に依存しています。UE 5.7 でも登録自体は行われますが、`uaip_list_commands` の既定応答には現れず、`HiddenCount` と `HiddenReasons.HandlerUnavailable` に計上されます。`IncludeUnavailable=true` を指定すると `Available: false` として明示的に列挙されます。`uaip_describe_command` はこのフィルタに関わらず常に表示します。実行すると `CommandNotFound` ではなく `PolicyViolation` が返ります。記号のないコマンドは UE 5.7 / UE 5.8 の両方で動作します。この記号は本セクション限定の表記です。

### ネイティブ（56）

#### 作成（1）

| コマンド | 説明 |
|---|---|
| `CreateMetaHumanCharacter` | デフォルトテンプレートから MetaHuman キャラクターアセットを新規作成しディスクへ書き出し（パッケージパスは `/Game/` 配下必須、`MetaHumanAssetCreate` 必須） |

#### 体型・肌・眼（8）

| コマンド | 説明 |
|---|---|
| `GetBodyConstraints` | 体型制約を全件取得（現在の目標寸法・体型ソルブへの参加有無・許容範囲、JSON artifact）。名前はデータ駆動のため `SetBodyConstraints` の前に本コマンドで列挙する |
| `SetBodyConstraints` | 名前を指定して体型制約を更新し体型を再評価（指定しなかった制約は現在値を保持、全エントリを検証してから適用） |
| `GetBodyShape` | 簡易体型を取得 — 男性寄り / 女性寄り・体脂肪・筋肉量（0..1 正規化）と身長（cm） |
| `SetBodyShape` | 簡易体型を設定し体型を再評価（省略値は変更なし、範囲外はクランプせず拒否） |
| `GetSkinSettings` | 肌設定を全件取得 — 肌トーン（明度 / 赤み）、テクスチャバリアントインデックス、ラフネス、手のひらと爪、そばかす、部位別トーンアクセント |
| `SetSkinTone` | 肌トーンの 2 軸（明度 / 赤み）のみを設定。その他の肌設定は変更しない |
| `GetEyeSettings` | 両眼を全件取得 — Iris / Pupil / Cornea / Sclera の 4 グループ |
| `SetEyeColor` | 指定した色温度・明度を両眼の虹彩プライマリ / セカンダリカラーへ書き込み |

#### 外見詳細（8）

| コマンド | 説明 |
|---|---|
| `SetSkinSettings` | 肌設定を部分更新（省略フィールドは現在値を保持、範囲外はクランプせず拒否） |
| `GetMakeupSettings` | メイク設定を取得 — ファンデーション・アイメイク・チーク・リップ |
| `SetMakeupSettings` | メイク設定を部分更新（スタイル名はエンジン側の名前と完全一致が必要） |
| `GetHeadModelSettings` | まつげのスタイル・色と、歯の形状・色の設定を全件取得 |
| `SetHeadModelSettings` | ヘッドモデル設定を部分更新 |
| `SetEyeSettings` | 眼を部分更新。左右を個別に指定し、Iris / Pupil / Cornea / Sclera の 4 グループを扱う |
| `GetFaceEvaluationSettings` | 顔の全体偏差・微細サーフェス偏差・頭部の均一スケールを取得 |
| `SetFaceEvaluationSettings` | 顔評価設定を部分更新 |

#### 顔の造形（9）

| コマンド | 説明 |
|---|---|
| `GetFaceModelCoefficients` ⬆️ | 内部フェイスモデルの係数をフラットな数値配列として取得（JSON artifact）。同じ配列を戻せば形状を復元できる |
| `SetFaceModelCoefficients` ⬆️ | フェイスモデルの係数を書き込み（配列長は `GetFaceModelCoefficients` の値と完全一致が必要、それ以外は拒否） |
| `GetFaceLandmarks` | 顔のランドマーク位置を JSON artifact として取得。配列内の位置が `TranslateFaceLandmarks` の指定するインデックスになる |
| `TranslateFaceLandmarks` | 指定したランドマークを対応する差分だけ移動（1 件でも不正なら何も適用しない） |
| `CommitFaceState` | 蓄積された造形編集をアセットへコミット（造形系コマンドは単体ではコミットしない） |
| `ImportFaceFromDna` | プロジェクトディレクトリ内の `.dna` ファイルから顔を差し替え（`MetaHumanFileImport` 必須） |
| `ImportFaceFromTemplate` | MetaHuman ヘッドと同一トポロジのテンプレートヘッドメッシュに顔をフィット |
| `ImportFaceFromIdentity` | MetaHuman Identity アセットのコンフォーム済みメッシュに顔をフィット（Identity はコンフォーム済みである必要あり） |
| `CompareFaceState` | 2 キャラクターの全対応頂点・頂点法線が `Tolerance` 以内かを判定（真偽値のみ、頂点単位の内訳は返さない） |

#### コンフォームとフィッティング（10）

| コマンド | 説明 |
|---|---|
| `GetMeshDataForConforming` ⬆️ | Static / Skeletal Mesh の頂点と三角形インデックスを、コンフォーム系コマンドがターゲットとして受け取る形式で JSON artifact へ出力 |
| `ConformBodyToTarget` | 指定頂点に体型をコンフォーム（手足のジョイントをメッシュから推定するオプションあり）。ターゲットは `MeshDataArtifactId` またはインライン `Vertices` で指定 |
| `ConformFaceToTargetMeshes` ⬆️ | ターゲットメッシュへ寄せる非同期ソルブを開始。成功は「開始した」ことを意味するため `GetAsyncConformState` をポーリングする |
| `AlignToTargetMeshes` ⬆️ | 形状を変えずに移動・回転・スケールでターゲットメッシュへ剛体アラインを開始。`ConformFaceToTargetMeshes` の前に実行する |
| `RefineVerticesToTarget` ⬆️ | パラメトリックモデル単体では表現できない部分まで頂点を寄せるリファインを開始。コンフォーム完了後に実行する |
| `CommitPosedStateAsAPose` ⬆️ | コンフォーム済みボディを MetaHuman A ポーズで評価し、そこから顔ステートを再構築（通常どおりポーズ・アニメーションできる状態にする） |
| `FitStateToTargetVertices` | 反復ソルブを使わず、MetaHuman ヘッドのトポロジ・頂点順の目標頂点へ 1 パスでヘッドをフィット |
| `FitFaceFromBodyWithEyesTeethTemplate` ⬆️ | 現在の体型からヘッドを再構築し、眼と歯をテンプレートメッシュで置き換え |
| `FitFaceFromBodyWithEyesTeethDna` ⬆️ | 同上（眼と歯は顔 DNA ファイルから取得）。ヘッド形状は体型由来のため顔のインポート手段ではない（`MetaHumanFileImport` 必須） |
| `GetAsyncConformState` ⬆️ | コンフォーム / アライン / リファインの実行中かを取得。エンジンが完了イベントを提供しないため `bIsRunning` が false になるまでポーリングする |

#### ビルドパイプライン（6）

| コマンド | 説明 |
|---|---|
| `RequestTextureSources` | 高解像度フェイステクスチャの合成を開始し、リクエスト発行時点で返す。処理はバックグラウンドで数分継続する（`MetaHumanTextureSynthesis` 必須） |
| `GetTextureSourceState` | テクスチャ合成が実行中かどうか、および合成済みテクスチャを保持しているかをポーリング |
| `RequestAutoRigging` | フェイスリグの生成を開始。⚠️ **キャラクターの顔データを Epic のクラウドリギングサービスへアップロードします** — リグはリモートで生成されてアセットへダウンロードされるため、Epic アカウントへのサインインとネットワーク接続が必要で、キャラクターデータはこのマシンの外へ出ます。リギングには通常数分かかるため `GetRiggingState` をポーリングする（`MetaHumanCloudRigging` 必須） |
| `GetRiggingState` | リギング状態（`Unrigged` / `RigPending` / `Rigged`）をポーリング。リクエスト終了後に `Unrigged` ならば失敗（多くはサインインまたは接続の問題） |
| `CanBuildMetaHuman` | `BuildMetaHuman` が当該キャラクターを受け付けるか、受け付けない場合は最初の未充足要件を返す。ビルド前に必ず呼ぶ |
| `BuildMetaHuman` | キャラクターをコレクション・インスタンス・キャラクターブループリントとして新規サブフォルダに組み立てる。⚠️ **ビルド完了までゲームスレッドを占有します（数秒〜数分）。** エンジンが進捗ダイアログを表示して再描画を続けるため、エディタは応答しなくなるのではなく画面を見られる状態を保ちますが、ビルドが返るまで他のコマンドは一切実行されません。ビルドが長引くと HTTP トランスポート自体の非同期コマンドタイムアウト（120 秒）を超えることがあり、その場合 `Timeout` が返りますが、**エディタ側ではビルドが実行を継続している可能性があります**。すぐに再実行せず、まず `uaip_get_editor_status` を呼んで `RecommendedAction`（`WAIT` が期待値）に従ってください。artifact はビルドが実際に完了した後になって生成される場合があります。先に `CanBuildMetaHuman` を呼ぶこと（オートリギングと合成済みテクスチャが揃っていないビルドは必ず失敗します）。失敗時は出力フォルダ配下に作成されたアセットが削除されます。出力フォルダが既存の場合は拒否されます。ビルド実行中は他の MetaHuman コマンドが拒否されます（`MetaHumanBuild` 必須） |

#### プレビュー（3）

| コマンド | 説明 |
|---|---|
| `GetViewportSettings` | プレビュービューポート設定を取得 — ライティング環境・ライト回転・背景色・LOD・ヘアカード / ストランドの切り替え・プレビュー用スキンマテリアル・カメラフレーミング（読み取り専用、`EditorInspect` のみで実行可能） |
| `SetViewportSettings` | プレビュービューポート設定を部分更新（最低 1 項目の指定が必要、範囲外はクランプせず拒否）。`PreviewMaterial` はエディタのビューポートツールバーの表示名に合わせてあり、**色を確認するためにキャプチャする前には `Skin` を選ぶこと** — `Topology` はトポロジ可視化で肌・メイク・眼の色を完全に隠し、`Clay` はテクスチャなしのグレー。`CameraFrame` は常にキャラクターへ記録されるが、プレビューカメラが実際に動くのは MetaHuman キャラクターエディタで開いている間だけ。カスタムライティング環境はここからは選べない — サポート対象の 2 つのエンジンバージョンで表現が異なるため、エディタのビューポートツールバーで設定する |
| `RefreshCharacterPreview` ⬆️ | 保留中のコレクション編集をキャラクターへ反映し、エディタパイプラインを再実行してプレビューへ反映 |

#### ワードローブ（10）

| コマンド | 説明 |
|---|---|
| `ListWardrobeSlots` | キャラクターのコレクションが定義するワードローブスロットと各スロットのアイテム数を列挙。名前は実行時にパイプラインから取得されるため `AssignWardrobeItem` の前に本コマンドで確認する |
| `ListWardrobeItems` | ワードローブアイテムを列挙（スロット指定は任意）。各エントリは不透明なハンドル `ItemKey` を持つ |
| `GetWardrobeItemInfo` | ワードローブアイテム 1 件を取得 — 占有スロット・表示名・ラップしているアセットのパッケージパス |
| `AssignWardrobeItem` ⬆️ | グルームやガーメントなどのアセットをワードローブスロットへ割り当てて選択し、プレビューを再構築（`RefreshCharacterPreview` の追加呼び出しは不要） |
| `RemoveWardrobeItem` ⬆️ | ワードローブアイテムを削除（着用中の場合はスロット選択を先に解除）し、プレビューを再構築 |
| `ReplaceWardrobeItem` ⬆️ | ワードローブアイテムを、元のアイテムが占有していたスロットのまま別アセットへ置き換え、プレビューを再構築 |
| `GetWardrobeItem` | パッケージパスで指定したワードローブアイテムアセットを 1 件取得 — 元アセットのパッケージパス・パイプラインのクラスパス・サムネイル画像のパス・サムネイル名・単体アセットかどうか。対象はアイテムアセットそのものであり、キャラクターが着用しているアイテムではない（後者は `GetWardrobeItemInfo` で、キャラクターパスと `ItemKey` を指定する） |
| `SetWardrobeItem` | ワードローブアイテムアセットの元アセット・サムネイル画像・サムネイル名を部分更新（省略フィールドは現在値を保持、ただし最低 1 項目の指定が必要。パス項目に空文字列を渡すとアセットの指定ではなくその参照のクリアになる）。パイプラインは本コマンドでは設定できず `SetWardrobeItemPipeline` を使う |
| `SetWardrobeItemPipeline` | ワードローブアイテムアセットへ指定クラスのパイプラインを設定し、元のパイプラインを置き換える。`PipelineClassPath` はクラスパスのため、組み立てずに `ListItemPipelineClasses` の結果から選ぶ |
| `ListItemPipelineClasses` | ワードローブアイテムアセットのビルドに使えるアイテムパイプラインクラスを表示名付きで列挙。存在するクラスはプロジェクトがロードしているプラグインに依存する。abstract・deprecated・ホットリロードで置換されたクラスは除外されるため、列挙されたクラスはすべて `SetWardrobeItemPipeline` が受け付ける |

#### セッション（1）

| コマンド | 説明 |
|---|---|
| `ReleaseEditSession` | キャラクターに対して保持している編集セッションを解放（実行中の処理を中断することはありません） |

### Toolset ブリッジ（9）🧩

`MetaHumanGenerator` Python Toolset へのブリッジコマンド。プロバイダ：`Toolset.Editor.MetaHuman.*`。UE 5.8+ かつ `MetaHumanGenerator` + `ToolsetRegistry` 有効時のみ利用可能で、UE 5.7 ではブリッジプロバイダ自体が登録されないため `CommandNotFound` になります。委譲先のエンジン Python Toolset 自体が experimental であるため `Stability: Experimental` です。

ネイティブコマンドと異なり、`Create` 以外のブリッジコマンドは `BeginEdit` が返すセッション参照を必須とします。そのため SafetyPolicy が読み取り専用のときはいずれも実行できません。必要な Capability は `MetaHumanEdit`（`Create` のみ `MetaHumanAssetCreate`）です。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.MetaHuman.BeginEdit` | キャラクターに対する編集セッションを開き、他のブリッジコマンドが受け取るセッション参照を返す |
| `Toolset.Editor.MetaHuman.EndEdit` | `BeginEdit` で開いたセッションを閉じ、キャラクターをエディタの編集対象から外す |
| `Toolset.Editor.MetaHuman.GetBodyShape` | セッション対象キャラクターの簡易体型 4 値を返す |
| `Toolset.Editor.MetaHuman.SetBodyShape` | 簡易体型 4 値を設定し、体型変更に伴うネック領域の再構築まで含めてコミット（範囲外の値は拒否されず Toolset 側でクランプされる — ネイティブコマンドとの唯一の挙動差） |
| `Toolset.Editor.MetaHuman.GetSkinTone` | セッション対象キャラクターの肌トーン 2 値（明度・赤み）を返す |
| `Toolset.Editor.MetaHuman.SetSkinTone` | 明度・赤みを設定して肌設定をコミット（その他の肌設定は変更しない） |
| `Toolset.Editor.MetaHuman.GetEyeColor` | 右眼の虹彩プライマリカラーから読み取った色温度・明度を返す |
| `Toolset.Editor.MetaHuman.SetEyeColor` | 1 つの眼色を両眼へ設定して眼設定をコミット（左右は常に一致する） |
| `Toolset.Editor.MetaHuman.Create` | `/Game/` 配下に MetaHuman キャラクターアセットを新規作成し、その参照を返す（`MetaHumanAssetCreate` 必須） |

---

## UAIP.Editor.DataTable

DataTable 行の管理とインポート / エクスポート。

| コマンド | 説明 |
|---|---|
| `ListDataTableRows` | DataTable の行キー一覧 |
| `AddDataTableRow` | 新規行を追加 |
| `DeleteDataTableRow` | 行を削除 |
| `DuplicateDataTableRow` | 行を複製 |
| `ImportDataTableFromCSV` | CSV 文字列を一括インポート（Replace / Merge モード） |
| `ExportDataTableToCSV` | DataTable を CSV Artifact としてエクスポート |
| `GetDataTableRowStruct` | 行構造（UScriptStruct）フィールド定義を取得 |
| `ListDataTableRowStructs` | 行構造に使える `FTableRowBase` 派生 struct の一覧 — `ClassPath` を `CreateAsset` の `FactoryParams.RowStructPath` に渡す |

---

## UAIP.Editor.AnimBlueprint

Anim Blueprint グラフと StateMachine 編集。

| コマンド | 説明 |
|---|---|
| `GetAnimBlueprintInfo` | AnimGraph ノード一覧と StateMachine 構造（PIE 中は degraded モード）。任意引数 `IncludePins`（既定 false）を true にすると各ノードエントリに `Pins[]` 配列が追加される。省略時の出力は従来どおり変わらない |
| `GetAvailableAnimGraphNodeClasses` | `UAnimGraphNode_Base` サブクラス一覧 — `ClassPath` を `AddAnimGraphNode` に渡す |
| `AddAnimGraphNode` | `UAnimGraphNode_Base` 派生ノードを NodeClass 指定で追加 — プロジェクトやプラグインが定義したクラスには Capability が必要、詳細は下記の Note を参照 |
| `RemoveAnimGraphNode` | NodeId 指定でノードを削除 |
| `ConnectAnimGraphPins` | 2 ピンを接続（WouldCreateCycle DFS 事前検出） |
| `DisconnectAnimGraphPins` | ピン接続を切断 |
| `AddAnimState` | StateMachine に State を追加 |
| `RemoveAnimState` | NodeId 指定で State を削除 |
| `AddAnimTransition` | From→To Transition を追加（重複時 idempotent） |
| `RemoveAnimTransition` | NodeId 指定で Transition を削除 |
| `CompileAnimBlueprint` | コンパイルし CompileStatus + エラーログを返す |
| `SetAnimGraphNodeProperty` | AnimGraph ノードの `EditAnywhere` プロパティをドット記法の `PropertyPath` で書き込み。参照は `ValueJson` + `AnimBlueprintReferenceEdit`、構造体・コンテナは `PropertyStructuredEdit` 経由 — [参照・構造体・コンテナの書き込み](#参照構造体コンテナの書き込み) を参照。プロパティがピンとして公開されていて何も接続されていない場合、書き込みに合わせてピンの既定値も更新されるため、次のコンパイルで値が捨てられない。接続済みのピンには触れない |
| `GetAnimGraphNodeDetails` | AnimGraph ノード 1 個分のピン・プロパティ詳細（読み取り専用。秘匿値は `IsSecret: true` のみ報告され `Value` は省略される） |
| `AddAnimGraphNodePosePin` | 動的な Pose 入力ピンを 1 つ追加（現状は `UAnimGraphNode_LayeredBoneBlend` のみ対応）。非冪等 |
| `RemoveAnimGraphNodePosePin` | `PinIndex` 指定で動的な Pose 入力ピンを 1 つ削除。削除すると残りのピン番号が繰り上がる |
| `AddAnimLayerGraph` | ルート AnimBlueprint 上に自己完結型の Anim Layer グラフを新規作成。派生 AnimBlueprint 上では拒否される |
| `RemoveAnimLayerGraph` | 自己完結型の Anim Layer グラフを削除。`RemoveReferencingNodes` が true の場合、参照している `LinkedAnimLayer` ノードも合わせて削除 |
| `ImplementAnimLayerInterface` | `UAnimLayerInterface` 派生インターフェースを実装し、宣言された anim-layer 関数ごとに 1 つずつレイヤーグラフを生成。`AnimBlueprintReferenceEdit` が必要（実装インターフェース一覧へクラス参照を書き込むため） |
| `AddLinkedAnimLayerNode` | 自己完結型レイヤー、または（`InterfacePath` 指定時は）実装済みインターフェースのレイヤー関数を指す `LinkedAnimLayer` ノードを配置。後者はさらに `AnimBlueprintReferenceEdit` が必要。ノードを配置するグラフは `TargetGraph`（名前）または `GraphGuid` で選ぶ。詳細は表の下の Note を参照 |

> **Note — `AddLinkedAnimLayerNode` の `TargetGraph` / `GraphGuid`（ノードを配置するグラフ）**: `TargetGraph`（Optional String。未指定は最初の AnimGraph）と `GraphGuid`（Optional String。`UEdGraph::GraphGuid`）は排他 — 両方指定すると `InvalidParams`。`TargetGraph` はまず AnimBlueprint 自身の AnimGraph（ルートグラフとその自己完結型レイヤー）の中で探し、そこで一致が無かった場合に限り、実装済みインターフェースのレイヤーグラフへフォールバックする — そのため自己完結型レイヤーが同名のインターフェースレイヤーに負けることはなく、このフォールバック自体が自己側の候補との間で複数一致になることもない（自己側を先に網羅的に確認するため）。実際に一致が生じた側の集合内で複数のグラフに一致した場合は `InvalidParams` を返し、`Result.MatchedGraphGuids` に各候補の `GraphGuid` が入る — いずれかを `GraphGuid` として渡し直せば絞り込める。どちらの集合にも存在しない名前を指定した場合は `NotFound`。
>
> **Note — `LayerName` / `InterfacePath`（ノードが指すレイヤー）は `TargetGraph` とは別系統の解決**: `InterfacePath` を指定しない場合は AnimBlueprint 自身の自己完結型レイヤーの中だけを `LayerName` で探し、指定した場合はそのインターフェース自身のレイヤー関数の中だけを探す — 両方を探すことはないため、この解決には自己実装とインターフェース実装の優先順位という概念自体が存在しない。その一方の集合の中で `LayerName` が複数のグラフに一致した場合（自己完結型レイヤー同士、または 1 つのインターフェースが持つレイヤー関数同士は名前が一意であることを前提としている）も同じく `InvalidParams` + `Result.MatchedGraphGuids` を返す — これはエンジンが通常許さないはずの名前衝突に対する防御的なチェックであり、日常的に起きる想定ではない。
>
> **Note — プロジェクト定義・プラグイン定義の AnimGraph ノードクラスは Capability で制御されます**: このドメインが従来から信頼してきた 3 モジュール（`AnimGraph` / `AnimGraphRuntime` / `Engine`）由来の `NodeClass` は、従来どおり追加できます。それ以外のモジュール由来のクラス — プロジェクトやプラグインが定義した `UAnimGraphNode_Base` 派生クラス — は `AnimBlueprintCustomTypeEdit` が必要になりました。Material とは異なり、このドメインには対になる「危険なノード」用の Capability はありません — 8 種のノード（`UAnimGraphNode_StateResult` / `TransitionResult` / `TransitionPoseEvaluator` / `Root` / `StateMachineBase` / `LinkedAnimGraph` / `LinkedAnimLayer` / `CustomProperty`）は、**どの Capability を持っていても** AnimGraph のルートには置けません — これらは内部専用・サブグラフ専用のノード種別であり、グラフがその方向からの追加を受け付けないという話であって、権限で解禁できる危険性ではありません。`AnimBlueprintCustomTypeEdit` を含むいかなる Capability もこの結果を変えません。[Safety & Capabilities](safety.md#blueprintanimblueprint-編集) を参照。
>
> この確認は `AddAnimGraphNode` だけに限りません — ゲートされたクラスの既存ノードを編集・接続・切断・コンパイル・削除する場合も同じ `AnimBlueprintCustomTypeEdit` があらためて確認されます。削除・切断固有の破壊的変更を含め、詳細は [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照してください。
>
> ⚠️ **破壊的変更**: プロジェクト定義・プラグイン定義の `NodeClass` は従来、無条件で `PolicyViolation` として拒否されていました。`AddAnimGraphNode` は現在、クラスが読み込まれていれば `CapabilityNotAvailable` を返し `AnimBlueprintCustomTypeEdit` の名前を挙げます。旧エラーコードとの移行期間は設けていません — 旧コードは「権限を与えても通らない」ことを意味していたため、残すと存在しない権限体系を案内することになるためです。上記 8 種の内部専用・サブグラフ専用ノードはこの変更の対象外で、引き続き `PolicyViolation` を返します。
>
> `NodeClass` はあらかじめ読み込まれている必要があります。`AddAnimGraphNode` は副作用としてクラスを読み込まなくなり、解決できないクラスには `NotFound` を返します。

---

## UAIP.Editor.AnimBlueprint.UAF 🧩

Unified Animation Framework のグラフを AnimBlueprint に埋め込む唯一のコマンド。Engine の `UAFAnimGraph` プラグイン（`UAF` 本体も必須）が必要で、どちらかが無効な場合はこのコマンドは登録されません。

[UAIP.Editor.UAF](#uaipeditoruaf-) と同じ理由で **`Stability: Experimental`** です。

| コマンド | 説明 |
|---|---|
| `AddUAFGraphNodeToAnimBlueprint` | `UAnimGraphNode_AnimNextGraph` ノードを `TargetGraph`（既定は最初の AnimGraph）、または排他の `GraphGuid` で指定したグラフに配置し、`UAFGraphPath` で指定した `UUAFAnimGraph` アセットを指す。`UAFGraphPath` はこのエディタに既にロード済みのものだけを解決対象とし、強制ロードは行わない。解決するのは必要な Capability がすべて確認できた後。`AnimBlueprintGraphEdit` / `AnimBlueprintReferenceEdit` / `AnimBlueprintCustomTypeEdit`（ノードクラスがこのドメインの同梱外モジュール由来のため）が必要。Play-in-Editor 中は不可 |

> **Note — `TargetGraph` / `GraphGuid` の複数一致**: `TargetGraph` は AnimBlueprint 自身の AnimGraph（ルートグラフと自己完結型レイヤー）の中だけを探す — `AddLinkedAnimLayerNode` と異なり、実装済みインターフェースのレイヤーグラフへはフォールバックしない。AnimBlueprint 自身が持つグラフのうち複数に名前が一致した場合は `InvalidParams` を返し、`Result.MatchedGraphGuids` に各候補の `GraphGuid` が入る。いずれかを `GraphGuid` として渡し直せば絞り込める。存在しないグラフ名を指定した場合は `NotFound`。

---

## UAIP.Editor.UAF 🧩

Unified Animation Framework アセット（`UUAFAnimGraph` / `UUAFSystem`）の編集・調査 — RigVM グラフノード、ピン、変数、イベントグラフ。Engine 本体の `UAF` プラグインが必要で、無効な場合これらのコマンドは一切登録されません。

**このセクションの全コマンドは `Stability: Experimental` です**。基盤となる UAF プラグイン自体がエンジン側の Experimental 機能であり、将来のエンジンリリースで API が予告なく変わりうるためです。

| コマンド | 説明 |
|---|---|
| `GetUAFAssetInfo` | UAF アセットの概要情報 — アセットクラス・エントリ数・degraded フラグ（読み取り専用） |
| `ListUAFEntries` | UAF アセットのエディタデータに格納された全エントリ（グラフ・変数・共有変数・カテゴリなど）を列挙（読み取り専用） |
| `ListUAFGraphs` | RigVM グラフを保持する全エントリ（アニメーショングラフエントリ・イベントグラフエントリなど）を列挙（読み取り専用） |
| `ListUAFNodes` | UAF アセットエントリが持つ RigVM グラフの全ノード名を列挙（読み取り専用） |
| `GetUAFNodeInfo` | UAF アセットエントリの RigVM グラフ内の 1 ノードについて、構造体パスとピン記述を返す（読み取り専用） |
| `ListUAFPins` | UAF アセットエントリの RigVM グラフ内の 1 ノードの全ピン記述を返す（読み取り専用） |
| `GetUAFPinValue` | `NodeName.PinName` で指定したピンの既定値を返す（読み取り専用） |
| `ListUAFVariables` | UAF アセットのメンバー変数を全て列挙（読み取り専用） |
| `GetUAFVariable` | 指定した名前のメンバー変数の記述を返す（読み取り専用） |
| `GetAvailableUAFUnitStructs` | 利用可能な `FRigUnit_AnimNextBase` サブ構造体を列挙 — `ClassPath` を `AddUAFGraphNode` の `StructPath` として渡す。各エントリは `Admission` と `RequiredCapabilities` / `MissingCapabilities` を持ち、今は追加できない構造体でも必要になる Capability を示す |
| `AddUAFGraphNode` | `StructPath`（このエディタに既にロード済みの構造体のみ解決対象、オンデマンドロードなし）経由で RigVM Unit ノードを追加。このドメインの同梱外モジュール由来の構造体には `UAFCustomTypeEdit` が必要 |
| `RemoveUAFGraphNode` | 名前指定で RigVM ノードを削除。削除するノードの構造体がこのドメインの同梱外の場合は `UAFCustomTypeEdit` が必要 |
| `ConnectUAFPins` | 出力ピンと入力ピンを接続（`NodeName.PinName` 形式）。接続の両端いずれかの構造体がこのドメインの同梱外の場合は `UAFCustomTypeEdit` が必要 |
| `DisconnectUAFPins` | 出力ピンと入力ピンの接続を切断。`ConnectUAFPins` と同じ `UAFCustomTypeEdit` の条件が適用される |
| `SetUAFPinValue` | ピンの既定値を設定（UE テキストインポート表記）。所有ノードの構造体がこのドメインの同梱外の場合は `UAFCustomTypeEdit`、ピンの宣言型がオブジェクト／クラス参照を含む場合は `UAFReferenceEdit` が必要 |
| `AddUAFVariable` | メンバー変数を新規作成。`ValueType` / `ContainerType` は `EPropertyBagPropertyType` / `EPropertyBagContainerType` の列挙子名。参照型の変数には `UAFReferenceEdit` が必要。⚠️ 型は、アセットを開く前に UAF エディタの変数型メニューで選べるものに限られます。64 ビット整数、テキスト型、ソフト参照、ユーザー定義構造体、Blueprint で使えない型は `InvalidParams` で拒否され（権限では解除できません）、`ValueType` と種類が合わない `TypeObject` も同じです。UAF のエンジンが扱えない `Int8` / `Int16` / `UInt16` / `UInt32` / `UInt64` も、アセットを開く前に拒否されます。`ValueTypeObjectPath` にはユーザー定義の構造体・列挙型（コンテンツ上のパス）を渡せず、`/Script/<Module>.<Class>` の型を指定します。`ContainerType` は `None` か `Array` で、セット・マップは `UnsupportedOperation` です |
| `RemoveUAFVariable` | 名前指定でメンバー変数を削除（同名のエントリが存在しない場合も、存在するが変数でない場合も `VariableNotFound`） |
| `AddUAFEventGraph` | `StructPath` で指定した RigVM Unit 構造体をルートとする新規イベントグラフエントリを追加。`UUAFSystem` 専用 — `UUAFAnimGraph` はアニメーショングラフエントリを 1 つ固定で持ちイベントグラフの余地がないため `UnsupportedOperation` で拒否される |
| `CompileUAFAsset` | `RequestAssetCompilation` 経由で同期コンパイルを実行。アセットごとにセッション単位のレート制限（`MinCompileIntervalSeconds`）あり |

上記の書き込み系 9 コマンドはすべて、静的な必須 Capability として `UAFGraphEdit` を要求します。

---

## UAIP.Editor.UAF.AnimGraph 🧩

UAF アニメーショングラフアセットに固有の読み取り専用コマンド 1 個。Engine の `UAFAnimGraph` プラグイン（`UAF` 本体も必須）が必要です。

[UAIP.Editor.UAF](#uaipeditoruaf-) と同じ理由で **`Stability: Experimental`** です。

| コマンド | 説明 |
|---|---|
| `GetAvailableUAFTraits` | 利用可能な `FAnimNextTraitSharedData` サブ構造体（UAF アニメーション Trait）を列挙 — `ClassPath` を `AddUAFGraphNode` の `StructPath` として渡す。`GetAvailableUAFUnitStructs` と同じ `Admission` / Capability プレビュー形式 |

---

## UAIP.Editor.SoundCue

SoundCue グラフ編集。

| コマンド | 説明 |
|---|---|
| `GetSoundCueInfo` | SoundCue グラフのノード一覧と接続トポロジー（JSON） |
| `GetAvailableSoundCueNodeClasses` | このエディタがロード済みの `USoundNode` 派生クラスを、このセッションが今追加できるかどうかにかかわらず全件返す — 結果の `NodeClass` を `AddSoundCueNode` の `SoundNodeClass` として渡せる。各エントリは `Admission`（`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`）と `RequiredCapabilities` / `MissingCapabilities` を持ち、`AddSoundCueNode` が検証するのと同じポリシーで判定される — `/Script/Engine` の外から来るクラスも一覧から外されず `SoundCueCustomTypeEdit` を挙げて掲載される。`NodeClass` 順にソートされ、`TotalCount` / `ReturnedCount` / `Truncated`（上限 200）を報告する。`SchemaVersion` は `1`。`EditorInspect` が必要 |
| `AddSoundCueNode` | SoundNodeClass 指定でノードを追加。`SoundNodeClass` が `/Script/Engine` の外から来る場合、`SoundCueGraphEdit` に加えて `SoundCueCustomTypeEdit` が必要 — [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照。⚠️ **変更** — `SoundNodeClass` はこのエディタが既にロード済みのクラスに対してのみ解決され、強制ロードはしなくなった。未解決のパスは以前は `InvalidParams` だったが、現在は `NotFound` |
| `RemoveSoundCueNode` | NodeId 指定でノードを削除（ルート削除は Conflict）。削除するノードのクラスが `/Script/Engine` の外から来る場合は `SoundCueCustomTypeEdit` が必要 |
| `ConnectSoundCuePins` | 2 ピンを接続（循環検出・動的入力ピン自動追加）。どちらかの端点のクラスが `/Script/Engine` の外から来る場合は `SoundCueCustomTypeEdit` が必要。ルート出力ノードは自身の SoundNode クラスを持たないため、この確認には一切関与しない |
| `DisconnectSoundCuePins` | ピン接続を切断（PinIndex=-1 で全切断）。対象ノードのクラスが `/Script/Engine` の外から来る場合は `SoundCueCustomTypeEdit` が必要 |
| `SetSoundCueNodeProperty` | SoundCue ノードのプロパティを設定。オブジェクト / クラス / デリゲート参照・構造体・コンテナは恒久的に拒否されなくなり、`ValueJson` で渡して `PropertyReferenceEdit` / `PropertyStructuredEdit` で制御される — [参照・構造体・コンテナの書き込み](#参照構造体コンテナの書き込み) を参照。対象ノードのクラスが `/Script/Engine` の外から来る場合は追加で `SoundCueCustomTypeEdit` が必要 |
| `CompileSoundCue` | SoundNode ツリーをグラフから再構築。`SoundCueCustomTypeEdit` は一切要求しない — このコマンド自体はノードクラスを一切名指しせず、cue が既に保持しているクラス群は権限を要求しない別の判定で確認されるため、プロジェクト製のノードを含む cue でも権限なしでコンパイルし続けられる |

> ⚠️ **破壊的変更 — 削除・接続・切断・プロパティ編集は以前ゲートされていませんでした。** この Capability が導入される前は `AddSoundCueNode` だけが追加するノードクラスを確認しており、残り 4 つの mutation コマンドは対象ノードのクラスにかかわらず無条件で実行されていました。一般則については [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照してください。

---

## UAIP.Editor.SoundSettings

SoundClass ツリー・SoundAttenuation・SoundMix アセットのプロパティ設定。

下記 3 つの `Set*Settings` コマンドは、値をエンジンテキストなら `Value`、JSON なら `ValueJson` で受け取り、`Operation` / `ElementIndex` / `ElementKeyJson` でコンテナの要素 1 つを操作できる — [参照・構造体・コンテナの書き込み](#参照構造体コンテナの書き込み) を参照。

| コマンド | 説明 |
|---|---|
| `GetSoundClassInfo` | SoundClass の Properties（FSoundClassProperties）・ChildClasses・ParentClass・PassiveSoundMixModifiers を返す |
| `SetSoundClassSettings` | SoundClass の FSoundClassProperties フィールドを 1 プロパティ単位で設定（LoadingBehavior の変更は拒否） |
| `ListSoundClasses` | プロジェクト内 SoundClass を列挙（AssetPath / ParentClassPath / ChildClassPaths；最大 1000 件） |
| `AddSoundClassChild` | SoundClass 階層に子クラスを追加（循環参照検出・深度上限 32） |
| `RemoveSoundClassChild` | SoundClass 階層から子クラスを削除し、双方向リンクを解除 |
| `GetSoundAttenuationInfo` | SoundAttenuation の FSoundAttenuationSettings を JSON で返す |
| `SetSoundAttenuationSettings` | SoundAttenuation の FSoundAttenuationSettings フィールドを 1 プロパティ単位で設定 |
| `ListSoundAttenuations` | プロジェクト内 SoundAttenuation を列挙（最大 1000 件） |
| `GetSoundMixInfo` | SoundMix の全設定（EQ・SoundClassEffects・Fade タイミング）を JSON で返す |
| `SetSoundMixSettings` | SoundMix のトップレベルフィールドを 1 プロパティ単位で設定（SoundClassEffects 配列の直接書き込みは拒否） |
| `SetSoundMixAdjuster` | SoundClassAdjuster を追加または更新（SoundClass パスをキーとした Upsert；省略フィールドは既存値を維持または既定値） |
| `RemoveSoundMixAdjuster` | SoundMix から対象 SoundClass の SoundClassAdjuster を削除 |
| `ListSoundMixes` | プロジェクト内 SoundMix を列挙（最大 1000 件） |

---

## UAIP.Editor.MVVM 🧩

ViewModel Blueprint のプロパティ管理、View Binding / Event の作成、Widget への ViewModel 接続管理。`ModelViewViewModel` プラグインが必要（UE 5.5 以降はデフォルト有効）。

### Native（26）

#### ViewModel プロパティ管理

| コマンド | 説明 |
|---|---|
| `ListViewModelClasses` | AssetRegistry から `UMVVMViewModelBase` 派生 Blueprint クラスを列挙する（`SearchPath` フィルタ省略可；最大 1000 件） |
| `AddViewModelProperty` | ViewModel Blueprint にプロパティを追加する（7 種類の PropertyType；`DefaultValue` 省略可；Getter / Setter 生成省略可） |
| `RemoveViewModelProperty` | ViewModel Blueprint からプロパティを名前指定で削除する |
| `ListViewModelProperties` | ViewModel Blueprint の全プロパティを一覧返却する |

#### Widget ViewModel 接続管理

| コマンド | 説明 |
|---|---|
| `AddViewModelToWidget` | WidgetBlueprint に ViewModel を接続する（`/Game/` 配下の `UMVVMViewModelBase` 派生クラスのみ許可） |
| `RemoveViewModelFromWidget` | WidgetBlueprint から ViewModel エントリを名前指定で削除する |
| `ListWidgetViewModels` | WidgetBlueprint に接続済みの ViewModel 一覧を返す |
| `RenameViewModelInWidget` | WidgetBlueprint 内の ViewModel エントリ名を変更する |
| `ReparentViewModelInWidget` | WidgetBlueprint 内の ViewModel エントリのクラスを変更する |

#### View Binding 操作

| コマンド | 説明 |
|---|---|
| `AddViewBinding` | WidgetBlueprint に View Binding を追加する |
| `RemoveViewBinding` | `BindingId` 指定で WidgetBlueprint の View Binding を削除する |
| `ListViewBindings` | WidgetBlueprint の全 View Binding を一覧返却する |
| `GetViewBinding` | `BindingId` 指定で View Binding の詳細を返す |
| `UpdateViewBinding` | View Binding のフィールドを部分更新する |
| `SetViewBindingEnabled` | View Binding の有効・無効を切り替える |
| `SetViewBindingConversionFunction` | View Binding に変換関数を設定または解除する |
| `SetViewBindingExecutionMode` | View Binding の実行モードを設定する |
| `ListConversionFunctions` | WidgetBlueprint に適用可能な変換関数を列挙する（大規模プロジェクトでは `SearchPath` フィルタ推奨） |

#### View Event 操作

| コマンド | 説明 |
|---|---|
| `AddViewEvent` | WidgetBlueprint に View Event を追加する（戻り値: `EventId` 文字列；空文字列なら失敗） |
| `RemoveViewEvent` | WidgetBlueprint から View Event を削除する |
| `ListViewEvents` | WidgetBlueprint の全 View Event を一覧返却する |

#### ViewModel ソース設定

| コマンド | 説明 |
|---|---|
| `SetViewModelSource` | ViewModel エントリの `CreationType` を変更する（Remove + Add ラウンドトリップ実装；`Context` タイプは UE 5.8 以降のみ） |
| `GetViewModelSource` | ViewModel エントリの現在のソース設定を返す |

#### 観察・検証

| コマンド | 説明 |
|---|---|
| `GetWidgetBindableProperties` | WidgetBlueprint のバインド可能プロパティを列挙する（ウィジェットプロパティ・ViewModel プロパティ） |
| `ValidateViewBindings` | WidgetBlueprint の全 View Binding を検証する（大規模プロジェクトではコスト高） |
| `GetMVVMViewInfo` | WidgetBlueprint の MVVM 設定サマリを返す（MVVM 未設定時は `bMVVMConfigured: false` の空応答） |

### Toolset ブリッジ（9）🧩

`MVVMToolset` プラグイン（UE 5.8 以上）経由のブリッジコマンド。プロバイダ: `Toolset.MVVM.*`。`CreateViewModel` および `ListViewModels` はブリッジ固有；その他はネイティブコマンドに対応する。

> **参照引数は、Toolset の参照の形に揃えています。**
>
> - ⚠️ **参照は、文字列の `refPath` が必須のオブジェクトです。** 対象は `AddViewModelProperty` の `ViewModel`、`AddViewModelToWidget` の `WidgetBlueprint` と `ViewModelClass`、`CreateViewBinding` の `WidgetBlueprint` / `SourceContext` / `DestinationContext`、`ListConversionFunctions`・`ListWidgetViewBindings`・`ListWidgetViewModels`・`RemoveWidgetViewBinding` の `WidgetBlueprint` です。これらの引数は、中身を問わないオブジェクトとして受けていました。`{}`、文字列でない `refPath`、裸の文字列は `InvalidParams` で断ります。Toolset も以前から断っていた形です。`refPath` 以外のメンバーは受け付けますが、送りません。
> - ⚠️ **参照が必須の引数では、空の `refPath` を先に断ります。** 次の 6 引数は、`{"refPath": ""}` を Toolset を呼ばずに `InvalidParams`（`Parameter '<名前>.refPath' must not be empty`）で断ります: `AddViewModelProperty` の `ViewModel`、`AddViewModelToWidget`・`CreateViewBinding`・`ListWidgetViewBindings`・`ListWidgetViewModels`・`RemoveWidgetViewBinding` の `WidgetBlueprint`。空の参照は Toolset も失敗していました。編集系のコマンドでは、書き込みパスの `NotAllowed` ではなく `InvalidParams` になる点も変わります。
> - **以前動いていた `null` は引き続き受け付けます:** `CreateViewBinding` の `SourceContext` / `DestinationContext`（ウィジェットブループリント自身）、`ListConversionFunctions` の `WidgetBlueprint`、`AddViewModelToWidget` の `ViewModelClass`。`CreateViewBinding` では `{"refPath": ""}` も `null` と同じ意味です。

| コマンド | 説明 |
|---|---|
| `Toolset.MVVM.CreateViewModel` | ViewModel Blueprint アセットを作成する |
| `Toolset.MVVM.AddViewModelProperty` | ViewModel Blueprint にプロパティを追加する |
| `Toolset.MVVM.ListViewModels` | ViewModel クラスを列挙する（クラス型フィルタ方式） |
| `Toolset.MVVM.ListWidgetViewModels` | WidgetBlueprint に接続済みの ViewModel を列挙する |
| `Toolset.MVVM.AddViewModelToWidget` | WidgetBlueprint に ViewModel を接続する |
| `Toolset.MVVM.ListWidgetViewBindings` | WidgetBlueprint の View Binding 一覧を返す |
| `Toolset.MVVM.RemoveWidgetViewBinding` | WidgetBlueprint から View Binding を削除する |
| `Toolset.MVVM.CreateViewBinding` | WidgetBlueprint に View Binding を作成する |
| `Toolset.MVVM.ListConversionFunctions` | 利用可能な変換関数を列挙する |

---

## UAIP.Editor.BehaviorTree

Behavior Tree グラフ編集と Blackboard キー管理。

| コマンド | 説明 |
|---|---|
| `GetBehaviorTreeNodeList` | 全ノードのフラットな一覧 — `NodeGuid`・`NodeClass`・`DisplayName`・`Depth`（0 = ルート Composite）・`ParentNodeGuid`。各ノードに `ExecutionIndex`（そのアセットをトップレベルのツリーとして実行したときのノードの番号で、実行時の応答が返す番号と同じ）も付く。付けられないノードは `null` と `ExecutionIndexUnavailableReason`。[実行時のノードをエディタのアセットと突き合わせる](#実行時のノードをエディタのアセットと突き合わせる) を参照 |
| `GetBehaviorTreeSubtree` | `NodeGuid` を起点としたサブツリー（Composite / Task / Decorator / Service）を再帰 JSON で返す（`MaxDepth` 1〜32）。各ノードに `ExecutionIndex`（そのアセットをトップレベルのツリーとして実行したときのノードの番号で、実行時の応答が返す番号と同じ）も付く。付けられないノードは `null` と `ExecutionIndexUnavailableReason`。[実行時のノードをエディタのアセットと突き合わせる](#実行時のノードをエディタのアセットと突き合わせる) を参照 |
| `GetAvailableBTCompositeClasses` | `UBTCompositeNode` サブクラス一覧 — `ClassPath` を `AddBehaviorTreeCompositeNode` に渡す。各エントリは追加コマンドと同じ policy から得た `Admission`（`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`）と `RequiredCapabilities` / `MissingCapabilities` を併記するようになりました。このドメインが出荷しているモジュールでの絞り込みは廃止しています。`ClassPath` 昇順で並び、`TotalCount` / `ReturnedCount` / `Truncated`（上限 200 件）を報告します。`SchemaVersion` は `2` になりました — 下の Note を参照してください |
| `GetAvailableBTTaskClasses` | `UBTTaskNode` サブクラス一覧 — `ClassPath` を `AddBehaviorTreeTaskNode` に渡す。上と同じ Admission・件数フィールドを報告します |
| `GetAvailableBTDecoratorClasses` | `UBTDecorator` サブクラス一覧 — `ClassPath` を `AddBehaviorTreeDecoratorNode` に渡す。上と同じ Admission・件数フィールドを報告します |
| `GetAvailableBTServiceClasses` | `UBTService` サブクラス一覧 — `ClassPath` を `AddBehaviorTreeServiceNode` に渡す。上と同じ Admission・件数フィールドを報告します |
| `AddBehaviorTreeCompositeNode` | Composite ノードを追加（Sequence / Selector / SimpleParallel）— このドメインが出荷していないモジュール由来のクラスには Capability が要ります。下の Note を参照してください |
| `AddBehaviorTreeTaskNode` | TaskClass 指定で Task ノードを追加 — サブツリー実行ノードと Blueprint ベースの Task には別の Capability が追加で要ります。下の Note を参照してください |
| `AddBehaviorTreeDecoratorNode` | 親ノードに Decorator を附加 — 確認内容は上と同じ |
| `AddBehaviorTreeServiceNode` | 親 Composite ノードに Service を附加 — 確認内容は上と同じ |
| `RemoveBehaviorTreeNode` | NodeId 指定でノードを削除 — そのノードのクラスが要求する Capability が同じく必要です |
| `GetBehaviorTreeNodeProperties` | ノードの `NodeInstance` が宣言する全プロパティ — `PropertyName`・`PropertyType`（C++ の型名）・`SetBehaviorTreeNodeProperty` がそのまま書き戻せる形の `PropertyValue`・入れ子の `WriteRequirements` オブジェクトを返す。`FBlackboardKeySelector` プロパティはベアなキー名として報告され、書き込みコマンド側の特別扱いと一致する。列挙される `ExecutionIndex` プロパティはアセットに保存されない一時的なエンジンの値で、BehaviorTree エディタで開いた後にだけ値が入り、アセットを読み込んだ直後は 0 のままのため、実行時の応答と突き合わせるには代わりに `GetBehaviorTreeNodeList` / `GetBehaviorTreeSubtree` の `ExecutionIndex` を使う。読み取り専用、PIE 中も許可（縮退モード）。要 `EditorInspect` |
| `SetBehaviorTreeNodeProperty` | ノードプロパティを設定（FBlackboardKeySelector / 汎用 ImportText_Direct）。書き込み対象ノードのクラスと、そのプロパティを宣言しているクラスの**両方**が要求する Capability が必要です。ツリーに Blackboard アセットが設定されていない場合、キーセレクタへの書き込みは拒否されるようになりました — Blackboard が無いとキー名の妥当性を確認できず、従来は名前と種類が食い違った状態が残ることがありました。拒否された書き込みはアセットを dirty にせず、空の undo エントリも残しません |
| `ListBlackboardKeys` | Blackboard アセットのキー一覧（PIE 中も許可） |
| `AddBlackboardKey` | キーを追加（重複名チェック）。`/Script/AIModule` 以外のキー型と、書き込み側が指す先を選べる 2 種のキー型には、それぞれ Capability が要ります — 下の Note を参照してください |
| `RemoveBlackboardKey` | 未参照のキーを削除（使用中は Conflict + 参照元を返す）— そのキーの型が要求する Capability が同じく必要です |
| `SetBehaviorTreeBlackboard` | BT アセットの参照 Blackboard を変更 |
| `RequestBehaviorTreeAutoArrange` | 開いている BT エディタで AutoArrange パスを実行 |

> **Note — このドメインは 3 か所で型を受理しており、Capability も 3 つあります**: 配置・操作されるノードのクラス、書き込まれるノードプロパティを宣言しているクラス、宣言・削除される Blackboard キー型のクラス、の 3 か所です。それぞれ従来から受け入れてきたモジュールの集合が異なり、その非対称は意図的なものです。
>
> - **`BehaviorTreeCustomTypeEdit`** — 型がこのドメインの出荷物の外から来た場合に必要です。ノードクラスなら `/Script/AIModule` または `/Script/AITestSuite`、ノードプロパティの宣言クラスなら `/Script/AIModule` または `/Script/Engine`、Blackboard キー型なら `/Script/AIModule` のみが「出荷物」です。プロジェクトのモジュール、プラグインのモジュール（`GameplayBehaviorSmartObjects` のようなエンジンプラグインを含む）、Blueprint 生成クラスはいずれも外側になります。3 か所で 1 つの名前を共有しているのは意図的で、「このドメインが出荷していない型を扱う」という 1 つの許可を表すためです。プロジェクト製の型がどの面から届くかは、その許可を与える運用者が別々に決めたい事柄ではありません。
> - **`BehaviorTreeExternalBehaviorNodeEdit`** — ノードの本体がクラス自身ではない場所にある 5 系統に必要です。別の Behavior Tree アセットをまるごと実行する `UBTTask_RunBehavior` / `UBTTask_RunBehaviorDynamic` と、サブクラスがエディタで組まれたグラフを持つ `UBTTask_BlueprintBase` / `UBTDecorator_BlueprintBase` / `UBTService_BlueprintBase` です。名前の一致ではなく継承で判定します。
> - **`BlackboardReferenceKeyTypeEdit`** — 保持する値が「書き込む側が指す先を選べる参照」である 2 種のキー型に必要です。プロジェクト内の任意の UObject を受け付ける `UBlackboardKeyType_Object` と、クラス名を保持してエンジンに解決させる `UBlackboardKeyType_Class` です。これも継承で判定します。
>
> いずれも既定では付与されません。[安全性と Capability](safety.md#ai-システム) を参照してください。
>
> ⚠️ **Blueprint で作った Behavior Tree ノードには Capability が 2 つ要ります。** そのクラスは「このドメインが出荷していない型」であると同時に「本体がグラフである型」でもあるため、`BehaviorTreeCustomTypeEdit` と `BehaviorTreeExternalBehaviorNodeEdit` の**両方**が必要です。片方だけを保有していてもリクエストは拒否され、まだ足りないもう一方が名指しで返ります。プロジェクト製の `UBlackboardKeyType_Object` 派生キー型も同様で、`BehaviorTreeCustomTypeEdit` と `BlackboardReferenceKeyTypeEdit` の両方が要ります。1 つの型に 2 つの Capability が掛かるのは Material に続いて 2 例目であり、驚かれやすい箇所です。カスタム型の Capability だけを付与した運用者は、プロジェクトが定義した Blueprint ノードのすべてで依然として拒否されます。
>
> **ツリーの組み直しは、そのツリーが既に含んでいるクラスによってゲートされることはありません。** 主ノードの追加・削除の後にはツリーのノードテンプレート鎖が書き直されますが、その書き直しはアセットに既に入っているクラスについて何も要求しません。そうでなければ、プロジェクト製のノードクラスを 1 つでも含むツリーは Capability の付与なしには一切編集できなくなってしまいます。ゲートされるのは、リクエストが**名指しした**クラスと、リクエストが**操作対象にした**ノードだけです。Blackboard キー型についても同じで、キーの宣言はスロットの形を述べるだけなので、オブジェクトキーを持つ Blackboard を参照している Behavior Tree は `BlackboardReferenceKeyTypeEdit` なしで編集できます。
>
> **認可の後にエンジン側が拒否することはありません。** Material や ControlRig と異なり、このドメインにはクラス単位で問い合わせるエンジン述語がありません。Behavior Tree エディタが答えるのは「そのグラフが Behavior Tree グラフか」であって「そのクラスがそこに属するか」ではなく、Blackboard も受け入れるキー型についてスキーマを持ちません。したがって残る要件が Capability だけの型は、その Capability を保有した時点で受理されます。
>
> これらの確認は `Add*` コマンドに限りません — 既存ノードの編集・削除、既存キーの削除でも同じ Capability があらためて確認されます。詳細と削除に関する破壊的変更は [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照してください。
>
> ⚠️ **破壊的変更**: こうしたクラスは従来 `PolicyViolation` で拒否されていました。4 つの `Add*` コマンドと `AddBlackboardKey` は `CapabilityNotAvailable` を返し、不足している Capability をすべて一度に名指しします。あわせて 2 つのエラーコードが変わりました。現在ロードされている中に該当が無いクラスパスは `InvalidParams` ではなく `NotFound` に、abstract・deprecated・新版あり・そもそも Behavior Tree ノードでないクラスは `PolicyViolation` ではなく `InvalidParams` になります。旧コードの互換期間は設けません — 旧コードは「どんな許可でも通らない」という意味であり、残せば存在しない権限体系を案内することになるためです。**クラスパスの解決のためにロードは行いません** — 4 つの `Add*` コマンドと `AddBlackboardKey` は、名指しされたクラスが未ロードのときにロードへフォールバックしていましたが、これを廃止しました。
>
> **Note — 4 つの一覧は何も隠さなくなり、各クラスに何が要るかを述べます**: 従来は「具象で、deprecated でなく、新版が無く、エディタのドロップダウンで非表示にされていない」クラスだけを返しており、追加経路が使う policy を一切参照していませんでした。その結果、食い違いが両方向に生じていました — サブツリー実行ノードやプロジェクト製ノードは一覧に出るのに追加は拒否され、逆にドロップダウン非表示マーカーを持つクラスは追加経路では通るのに、それを見つけられる唯一の場所から消えていました。現在は 4 つとも同じ policy から答え、エントリごとに `Admission` を報告し、そもそも配置できないクラスも落とさずに `NotAddable` として載せます。`ClassPath` 昇順で並び、`TotalCount` / `ReturnedCount` / `Truncated` を報告するため、打ち切られた応答でも常に同じ先頭クラス群が返ります（従来はクラス走査が先に到達したものが返っていました）。一覧はスナップショットであって認可ではありません — 一覧取得から mutation までの間に Capability や role は変わりうるため、各コマンドは自身のリクエストで判定をやり直します。
>
> **Blackboard キー型の一覧コマンドはありません。** ゲートされる 3 か所の開示状況は同じではありません。ノードクラスには上の 4 つの一覧がありますが、Blackboard が受け付けるキー型と、ノードが公開するプロパティには、Admission 付きで列挙するコマンドがありません。キー型のために `BlackboardReferenceKeyTypeEdit` や `BehaviorTreeCustomTypeEdit` を付与する運用者は、クラスパスを事前に知っている必要があります。

### Toolset ブリッジ — AIModule（7 件）🧩

`AIModuleToolset`（UE 5.8+、Experimental）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.AIModule.*`。観測専用です。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.AIModule.GetBlackboard` | BehaviorTree に紐づく Blackboard アセット |
| `Toolset.Editor.AIModule.GetRootDecorators` | ルート Composite ノードに附加された Decorator 一覧 |
| `Toolset.Editor.AIModule.ListNodes` | 全ノードのインデックスと型の一覧 |
| `Toolset.Editor.AIModule.GetNodeDepth` | インデックス指定した単一ノードの深さ |
| `Toolset.Editor.AIModule.GetNodeDepths` | 全ノードの深さをフラットな一覧で返す |
| `Toolset.Editor.AIModule.GetChildren` | refPath で指定した Composite ノードの直下の子 |
| `Toolset.Editor.AIModule.GetSubtree` | refPath で指定したノードを起点とするサブツリー |

---

## UAIP.Editor.MetaSound 🧩

MetaSound グラフ編集。`Metasound` プラグインが必要です。

| コマンド | 説明 |
|---|---|
| `GetMetaSoundInfo` 🧩 | MetaSoundSource / MetaSoundPatch のグラフトポロジー（ノード一覧・接続・I/O 頂点）。各ノードは実際の `ClassName` に加え、そのノードに触るのに必要な `Admission` / `RequiredCapabilities` / `MissingCapabilities` を返す — 詳細は下記の Note を参照 |
| `GetAvailableMetaSoundNodeClasses` 🧩 | Frontend レジストリのノードクラス一覧（`ClassName`・`Variant`・`MajorVersion`・`DisplayName`）。`AddMetaSoundNode` の引数に使う。各エントリは `AddMetaSoundNode` が検証するのと同じポリシー由来の `Admission`（`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`）と `RequiredCapabilities` / `MissingCapabilities` を持つ。エンジン標準の名前空間による絞り込みは廃止。`ClassName` 昇順で並び、`TotalCount` / `ReturnedCount` / `Truncated`（上限 1000 件）を返す — 詳細は下記の Note を参照 |
| `AddMetaSoundNode` 🧩 | `Namespace::Name` 形式でノードを追加（MajorVersion 対応）— エンジンの 4 Namespace 外のクラスには Capability が必要、詳細は下記の Note を参照 |
| `RemoveMetaSoundNode` 🧩 | NodeId 指定でノードを削除 — 対象ノードがそれらのクラスの場合は同じ Capability が必要 |
| `ConnectMetaSoundPins` 🧩 | 2 ピンを接続（重複時 idempotent フラグ付き）— 両端が確認される |
| `DisconnectMetaSoundPins` 🧩 | ピン接続を切断 — 両端が確認される |
| `AddMetaSoundInput` 🧩 | 入力頂点を追加（単一ページアセットのみ） |
| `AddMetaSoundOutput` 🧩 | 出力頂点を追加（単一ページアセットのみ） |
| `SetMetaSoundNodeProperty` 🧩 | 入力デフォルト値を設定（Bool / Int / Float / String、NaN / Inf 拒否）— 対象ノードがそれらのクラスの場合は同じ Capability が必要 |
| `CompileMetaSound` 🧩 | Frontend に登録（セッション単位 1 秒レートリミット）— カスタム型の Capability を要求することはない |

> **Note — エンジンの 4 Namespace 外のノードクラスは Capability で制御されます**: `ClassName` の Namespace が `UE` / `Metasound` / `MetasoundStandardNodes` / `MetasoundEditor` のいずれかであれば従来どおり追加できます。それ以外の Namespace のクラス — プロジェクトやプラグインのモジュールが独自に登録したもの — は、無条件で拒否されるのではなく `MetaSoundCustomTypeEdit` が必要になりました。既定では付与されません。[Safety & Capabilities](safety.md#オプショングラフエディタ) を参照。このドメインには（AnimBlueprint・ControlRig・Enhanced Input と同じく、Material とは異なり）対になる「危険な型」用の Capability はありません — MetaSound ノードはレジストリエントリが記述する固定の信号処理を評価するだけで、リクエストが持ち込んだコードは実行しないためです。
>
> ⚠️ **このドメインでは、ゲート対象の他ドメインより通常のグラフへの影響が大きく出ます。Capability を付与するか否かを決める前に必ずお読みください。** MetaSound は**すべての MetaSound アセット自身のグラフクラスを Namespace なしで登録します**。そして、別の MetaSound アセットを参照するノード — サブグラフ、およびプリセットの参照先 — はまさにそのクラスとして現れます。したがってそうしたノードは構成上つねに 4 Namespace の外に落ち、`MetaSoundCustomTypeEdit` を持たないセッションは**サブグラフやプリセットのノードに対する接続・切断・削除・入力デフォルト値の設定を一切行えません**。グラフ自体に特殊な点は何もなくてもそうなります。MetaSound ではサブグラフの再利用が、このゲートが対象とする他ドメインとは違って通常の作り方ですので、実際のオーサリング作業ではこの Capability を付与することになる場面が多いと考えてください。除外していないのは、プロジェクト自身のアセットが登録したグラフクラスは紛れもなくプロジェクト自身の型であり、除外するとこのドメインでは Capability の意味がほとんど失われるためです。
>
> **コンパイルはこの Capability を要求しません。** `CompileMetaSound` も、各 mutation コマンドが自身の変更後に行う暗黙の再登録も、アセットが単に**含んでいる**だけのクラスについては何も要求しません — そうでなければ、プロジェクト自身のアセットを 1 つでも参照する MetaSound は権限なしには一切コンパイルできなくなるためです。ゲートされるのは、リクエストが**名指しした**クラスと、リクエストが**操作対象にした**ノードだけです。
>
> これらの確認は `AddMetaSoundNode` だけに限りません — 既存ノードの編集・接続・切断・削除でも同じ Capability があらためて確認されます。削除・切断固有の破壊的変更を含め、詳細は [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照してください。
>
> ⚠️ **破壊的変更**: これらのクラスは従来 `PolicyViolation` で拒否されていました。`AddMetaSoundNode` は現在 `CapabilityNotAvailable` を返し、不足している Capability 名を挙げます。あわせて 2 つのコードが変わりました — Frontend レジストリに存在しない `ClassName` は `PolicyViolation` ではなく `NotFound`、非推奨クラスは `PolicyViolation` ではなく `InvalidParams` になります。テンプレートクラス（`Reroute` など）は従来どおり `PolicyViolation` のままです。旧エラーコードとの移行期間は設けていません — 旧コードは「権限を与えても通らない」ことを意味していたため、残すと存在しない権限体系を案内することになるためです。クラス名の解決にあたって何かがロードされることはありません（レジストリは現状のまま読まれます）。
>
> **Note — 2 つの一覧は Admission を報告するようになり、何も隠さなくなりました**: `GetAvailableMetaSoundNodeClasses` は従来、4 Namespace 外のクラスをレスポンスから除外していたため、アクセスを許可した運用者から見てもプロジェクト自身のノードは一覧に現れませんでした。現在はレジストリの External クラスを `ClassName` 昇順ですべて返し、各エントリに `Admission` — `Allowed`、`RequiresCapabilities`（`MissingCapabilities` に挙がるものを付与すれば使える。`MissingCapabilities` は `RequiredCapabilities` の部分集合）、`NotAddable`（非推奨・テンプレートクラス・レジストリに存在しない等、Capability をどれだけ付与しても解消しない構造的な拒否）、`CompatibilityUnknownUntilAuthorized` — を付け、新設の 1000 件上限に対する `TotalCount` / `ReturnedCount` / `Truncated` も返します。⚠️ `GetMetaSoundInfo` も同様に、さらに大きく変わりました。従来は 4 Namespace 外のノードを `ClassName: "<Unknown>"` として報告し、**その端点を持つ辺をすべて出力から除外していた**ため、返されるトポロジーがアセットの実態と一致していませんでした。現在は実際のクラス名とすべての辺を返し、編集系の経路が問うのと同じ問いから得た `Admission` / `RequiredCapabilities` / `MissingCapabilities` を各ノードに付けます。`"<Unknown>"` を番兵として扱っていた呼び出し側、辺の一覧が事前にフィルタされている前提の呼び出し側は修正が必要です。どちらの一覧も権威的な判定ではなくスナップショットです — 一覧取得後に Capability や role が変わり得るため、実際の可否は各コマンド側で毎回あらためて判定されます。

---

## UAIP.Editor.EQS 🧩

EQS クエリ編集。`EnvironmentQueryEditor` プラグインが必要です。

| コマンド | 説明 |
|---|---|
| `GetEQSQueryInfo` 🧩 | EQS Generator Option / Test 構造。すべての Option と Test が実際のクラス名を返すようになりました — degraded（PIE 中）の読み取りでも伏せ字にしません — あわせて `Admission` / `RequiredCapabilities` / `MissingCapabilities` を報告します。詳細は下記の Note を参照。degraded モードでは引き続き `NodeX` / `NodeY` と `GeneratorProperties` を省略します。`SchemaVersion` は `2` になりました |
| `GetAvailableEQSGeneratorClasses` 🧩 | `UEnvQueryGenerator` サブクラス一覧 — `ClassPath` を `AddEQSGenerator` に渡す。各エントリは追加コマンドと同じ policy から得た `Admission`（`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`）と `RequiredCapabilities` / `MissingCapabilities` を併記するようになりました。このドメインが出荷しているモジュールでの絞り込みは廃止しています。`ClassPath` 昇順で並び、`TotalCount` / `ReturnedCount` / `Truncated`（上限 200 件）を報告します。`SchemaVersion` は `2` になりました — 下の Note を参照してください |
| `GetAvailableEQSTestClasses` 🧩 | `UEnvQueryTest` サブクラス一覧 — `ClassPath` を `AddEQSTest` に渡す。上と同じ Admission・件数フィールドを報告します |
| `AddEQSGenerator` 🧩 | Generator Option を追加 — このドメインが出荷していないモジュール由来のクラスには Capability が要ります。下の Note を参照してください |
| `RemoveEQSGenerator` 🧩 | NodeId 指定で Generator Option を削除（配下 Test も一括削除）— その Generator のクラスが要求する Capability が同じく必要です |
| `AddEQSTest` 🧩 | Generator Option に Test を追加 — 確認内容は `AddEQSGenerator` と同じ |
| `RemoveEQSTest` 🧩 | NodeId 指定で Test を削除 — その Test のクラスが要求する Capability が同じく必要です |
| `SetEQSGeneratorProperty` 🧩 | Generator プロパティを設定（汎用 ImportText_Direct）— 書き込み対象 Generator のクラスと、そのプロパティを宣言しているクラスの**両方**が要求する Capability が必要です |
| `SetEQSTestProperty` 🧩 | Test プロパティを設定（`param:<Name>` → `UAIDataProvider_QueryParams`）— 確認内容は上と同じ。`bTestEnabled` の切り替え（`PropertyName: "TestEnabled"`）も、そのフラグ自体はグラフノード側にあり Test インスタンス側にはないにもかかわらず、Test 自身のクラスによってゲートされるようになりました — この経路は従来まったくゲートされていませんでした。下の Note を参照してください |

> **Note — このドメインは 3 か所で型を受理しており、Capability は 2 つあります**: 配置・操作される Generator のクラス、配置・操作される Test のクラス、書き込まれるノードプロパティを宣言しているクラス、の 3 か所です。3 つの面はいずれも従来から `/Script/AIModule` という同じ 1 つのモジュールだけを受け入れてきました。
>
> - **`EQSCustomTypeEdit`** — 型が `/Script/AIModule` の外から来た場合に必要です。プロジェクトのモジュール、プラグインのモジュール（`SmartObjects` や `MassEQS` のようなエンジンプラグインを含む）、Blueprint 生成の Test クラスはいずれも外側になります。3 か所で 1 つの名前を共有しているのは他の対象ドメインと同じ理由です — プロジェクト製の型が Generator・Test・プロパティ宣言者のどの面から届くかは、その許可を与える運用者が別々に決めたい事柄ではありません。
> - **`EQSDelegatedGeneratorEdit`** — 項目の生成が自身のコンパイル済みコードではない Generator 種別に必要です。内部に保持した複数の子 Generator インスタンスを走らせる `UEnvQueryGenerator_Composite` と、サブクラスがエディタで組まれたグラフを持つ `UEnvQueryGenerator_BlueprintBase` です。名前の一致ではなく継承で判定し、クラスの出自とは関係なく要求されます — `/Script/AIModule` 自身がこの 2 種を出荷しているため、モジュールを信頼するだけでは何を実行するかについて何も言えないためです。そうした Generator が宣言するプロパティにも同じ Capability が要ります（Composite Generator 自身のプロパティは、それが走らせる子 Generator 群を記述するものだからです）。
>
> いずれも既定では付与されません。[安全性と Capability](safety.md#オプショングラフエディタ) を参照してください。
>
> ⚠️ **プロジェクト製の Composite 派生 Generator には Capability が 2 つ要ります。** そのクラスは「このドメインが出荷していない型」であると同時に「項目の生成が他所で行われる型」でもあるため、`EQSCustomTypeEdit` と `EQSDelegatedGeneratorEdit` の**両方**が必要です。片方だけを保有していてもリクエストは拒否され、まだ足りないもう一方が名指しで返ります。そのクラスが宣言するプロパティについても同様です。
>
> **Test 面には対になる「危険な型」用の Capability がありません。** Generator 面と異なり、このドメインが受け入れる Test はどれも自身のコンパイル済みクラス以外の場所でコードを実行しません — Blueprint で作られた Test のグラフも、他のプロジェクト製クラスと同じく出自だけで判定され、2 つ目の判定基準は存在しません。
>
> **クエリの組み直しは、そのクエリが既に含んでいるクラスによってゲートされることはありません。** Generator や Test の追加・削除の後にはグラフがクエリの Option 一覧へ書き戻されますが、その書き戻しはアセットに既に入っているクラスについて何も要求しません。そうでなければ、プロジェクト製の Generator や Test クラスを 1 つでも含むクエリは Capability の付与なしには一切編集できなくなってしまいます。ゲートされるのは、リクエストが**名指しした**クラスと、リクエストが**操作対象にした**ノードだけです。
>
> **認可の後にエンジン側が拒否することはありません。** このドメインにはクラス単位で問い合わせるエンジン述語がありません。環境クエリエディタはサブクラスを列挙して abstract・deprecated・非表示のものを落とすことでクラスメニューを構築するだけで、グラフスキーマが答えるのは「そのグラフがクエリグラフか」であって「その Generator や Test がそこに属するか」ではありません。したがって残る要件が Capability だけの型は、その Capability を保有した時点で受理されます。
>
> これらの確認は `Add*` コマンドに限りません — 既存の Generator や Test の編集・削除でも同じ Capability があらためて確認されます。詳細と削除に関する破壊的変更は [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照してください。⚠️ **`bTestEnabled` の切り替えは削除・切断とともに従来まったくゲートされていませんでした** — この変更より前は `Add*` と `Set*`（ノードインスタンスへ書くプロパティに限る）だけが型 policy を確認しており、この経路は Test のクラスにかかわらずアセットへ到達していました。
>
> ⚠️ **破壊的変更**: こうしたクラスは従来 `PolicyViolation` で拒否されていました。`AddEQSGenerator` / `AddEQSTest` / `SetEQSGeneratorProperty` / `SetEQSTestProperty` は `CapabilityNotAvailable` を返し、不足している Capability をすべて一度に名指しします。現在ロードされている中に該当が無いクラスパスは `InvalidParams` ではなく `NotFound` になります — このドメインはもともと未解決クラスをロードへフォールバックしていなかったため、この点に変化はありません。旧コードの互換期間は設けません — 旧コードは「どんな許可でも通らない」という意味であり、残せば存在しない権限体系を案内することになるためです。
>
> **Note — 2 つの一覧は何も隠さなくなり、各クラスに何が要るかを述べます**: 従来は基底型とクラスフラグだけでクラスを列挙しており、追加経路が使う policy を一切参照せず、`/Script/AIModule` 以外のクラスをすべてレスポンスから除外していました。その結果、食い違いが両方向に生じていました — Composite Generator やプロジェクト製クラスは一覧に出るのに追加は拒否され、逆に `UEnvQueryGenerator_BlueprintBase` のような abstract クラスは正しく拒否されているのに、それを見つけられる唯一の場所から消えていました。現在は 2 つとも同じ policy から答え、エントリごとに `Admission` を報告し、そもそも配置できないクラスも落とさずに `NotAddable` として載せます。`ClassPath` 昇順で並び、`TotalCount` / `ReturnedCount` / `Truncated`（上限 200 件）を報告するため、打ち切られた応答でも常に同じ先頭クラス群が返ります（従来はクラス走査が先に到達したものが返っていました）。一覧はスナップショットであって認可ではありません — 一覧取得から mutation までの間に Capability や role は変わりうるため、各コマンドは自身のリクエストで判定をやり直します。
>
> **`GetEQSQueryInfo` はクラス名を伏せ字にしなくなりました。** これまで、すべての Option と Test は、このドメインが無条件では受け入れないクラスについて、degraded（PIE 中）の読み取りではクラス名の代わりに `<redacted>` を報告しており、そのノードが何なのかも、何をすれば使えるようになるのかも呼び出し側には分かりませんでした。現在は常に実際のクラス名を報告し、あわせて `SetEQSGeneratorProperty` / `SetEQSTestProperty` / `RemoveEQSGenerator` / `RemoveEQSTest` が問うのと同じ問いに対する `Admission` / `RequiredCapabilities` / `MissingCapabilities` を返します。

---
---

## UAIP.Editor.Sequencer

LevelSequence 編集 — トラック・セクション・キーフレーム・再生・バインド。

### ネイティブ（131）

#### 構造（15）

| コマンド | 説明 |
|---|---|
| `AddTrack` | LevelSequence にトラックを追加（TrackClass 指定）。`TrackClass` がこのドメインがトラックを供給する 4 モジュールの外から来る場合、`SequencerStructureEdit` に加えて `SequencerCustomTypeEdit` が必要 — [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照 |
| `RemoveTrack` | TrackClass / BindingGuid 指定でトラックを削除。削除するトラックのクラスが信頼済み 4 モジュールの外から来る場合は `SequencerCustomTypeEdit` が必要。**ただし** `UMovieSceneSubTrack` / `UMovieSceneCinematicShotTrack` / `UMovieSceneEventTrack` の 3 クラスは例外 — これらは `AddTrack` から追加することは一切できないが、信頼済みモジュール由来である限り、既にシーケンスに置かれているものを削除するのに Capability は一切不要 |
| `AddSection` | トラックにセクションを追加（StartFrame / EndFrame は DisplayRate 基準）。所属トラックのクラスが信頼できないものである場合は `SequencerCustomTypeEdit` が必要 |
| `RemoveSection` | SectionIndex 指定でセクションを削除。所属トラックのクラスが信頼できないものである場合は `SequencerCustomTypeEdit` が必要 |
| `SetPlaybackRange` | 再生範囲を設定 |
| `FlushSequencerChanges` | 蓄積した変更通知を一括 Flush |
| `GetAvailableSequencerTrackClasses` | このエディタが読み込み済みの `UMovieSceneTrack` サブクラスをすべて一覧表示（現在のセッションが追加できるかどうかに関わらず）。`SchemaVersion` は `2`。各エントリは `Admission`（`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`）と `RequiredCapabilities` / `MissingCapabilities` を持ち、応答には `TotalCount` / `ReturnedCount` / `Truncated` が付く。⚠️ **変更点** — 従来この一覧は `Deprecated`・`NewerVersionExists`・`HideDropDown` のクラスを黙って除外していたが、現在は `AddTrack` 自身が同じクラスに対して下す判定と一致する `Admission` を伴って一覧に含める |
| `SetSectionRange` | セクションのフレーム範囲を変更 |
| `DuplicateSection` | セクションを複製 |
| `MoveSection` | セクションを指定フレーム数オフセットで移動 |
| `AddCameraCut` | CameraCutTrack にカメラカットセクションを追加 |
| `SetTrackEnabled` | トラックの有効/無効を切り替え |
| `IsTrackEnabled` | トラックの有効状態を取得 |
| `SetSectionActive` | セクションのアクティブ状態を切り替え |
| `IsSectionActive` | セクションのアクティブ状態を取得 |

#### キーフレーム（7）

| コマンド | 説明 |
|---|---|
| `AddKeyframe` | チャンネルにキーフレームを追加。所属トラックのクラスが信頼できないものである場合は `SequencerCustomTypeEdit` が必要 |
| `RemoveKeyframe` | FrameNumber 指定でキーフレームを削除。所属トラックのクラスが信頼できないものである場合は `SequencerCustomTypeEdit` が必要 |
| `SetKeyframeValue` | キーフレームの値を更新。所属トラックのクラスが信頼できないものである場合は `SequencerCustomTypeEdit` が必要 |
| `SetKeyframeInterpolation` | キーフレームの補間モードを変更 |
| `SetKeyframeTangents` | キーフレームの接線を設定 |
| `OffsetKeyframes` | チャンネルの全キーフレームを時間オフセットで一括移動 |
| `GetKeyframeTangents` | キーフレームの接線を取得（arrive / leave） |

> これらの確認は `AddTrack` だけに限りません — 既存トラックのセクションやキーフレームの編集・削除でも同じ Capability があらためて確認されます。削除固有の破壊的変更を含め、詳細は [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照してください。⚠️ **内部専用の 3 トラッククラスだけは例外**: `UMovieSceneSubTrack`・`UMovieSceneCinematicShotTrack`（それぞれ専用コマンドからのみ到達可能）・`UMovieSceneEventTrack`（このドメインには追加するコマンドが一切ない）は、どの Capability を保有していても `AddTrack` からは追加できませんが、`RemoveTrack` は信頼済みモジュール由来である限り、既にシーケンスにあるものを削除するのに Capability を一切要求しません — 削除は内容を持ち込まないため、汎用の追加経路を塞ぐ制限が撤去には引き継がれません。

#### バインド（4）

| コマンド | 説明 |
|---|---|
| `BindActor` | Editor World のアクターを Possessable としてバインド |
| `UnbindActor` | BindingGuid 指定でアクターバインドを削除 |
| `GetActorBindingGuid` | アクター名から BindingGuid を逆引き |
| `GetBoundActors` | BindingGuid に対応するアクター一覧 |

#### 観測（12）

| コマンド | 説明 |
|---|---|
| `GetSequenceInfo` | トラック / セクション / チャンネル / バインド / DisplayRate / 再生範囲 |
| `GetBindings` | Possessable バインド一覧（GUID・名前・クラス） |
| `GetTracks` | 指定 BindingGuid のトラック一覧 |
| `GetSections` | トラックのセクション一覧（フレーム範囲付き） |
| `GetDisplayRate` | LevelSequence の DisplayRate |
| `GetTickResolution` | LevelSequence の TickResolution |
| `GetPlaybackRange` | 現在の再生範囲 |
| `GetKeyframes` | チャンネルのキーフレーム一覧（時刻・値・補間） |
| `ValidateSequenceBindings` | 全バインドの有効性を検証（アクター存在・型一致） |
| `GetCameraCutSections` | CameraCutTrack のセクション一覧 |
| `GetCurrentSequence` | 開いている ULevelSequence |
| `GetFocusedSequence` | フォーカス中 Sequencer の ULevelSequence |

#### 再生（10）

| コマンド | 説明 |
|---|---|
| `Play` | Sequencer 再生を開始 |
| `Pause` | 再生を一時停止 |
| `IsPlaying` | 再生中かどうか |
| `SetPlayheadFrame` | 再生ヘッドを指定フレームに移動 |
| `GetPlayheadFrame` | 現在の再生ヘッド位置 |
| `SetPlaybackSpeed` | 再生速度倍率を設定 |
| `GetPlaybackSpeed` | 現在の再生速度倍率 |
| `SetLoopMode` | ループモードを設定（NoLoop / Loop / LoopExactly） |
| `GetLoopMode` | 現在のループモード |
| `ForceEvaluate` | 現在フレームを強制再評価 |

#### セクションプロパティ（4）

| コマンド | 説明 |
|---|---|
| `GetSectionProperty` | UMovieSceneSection のプロパティ値を取得 |
| `SetSectionProperty` | UMovieSceneSection のプロパティを設定。値はエンジンテキストなら `PropertyValue`、JSON なら `ValueJson` で渡し、`Operation` / `ElementIndex` / `ElementKeyJson` でコンテナの要素 1 つを操作できる — [参照・構造体・コンテナの書き込み](#参照構造体コンテナの書き込み) を参照 |
| `GetSectionWeight` | セクションの重みを取得 |
| `SetSectionWeight` | セクションの重みを設定 |

#### UI / 状態（10）

| コマンド | 説明 |
|---|---|
| `SetCameraLock` | カメラロック状態を切り替え |
| `IsCameraLockActive` | カメラロック状態を取得 |
| `GetSelectionRange` | 選択範囲を取得 |
| `SetSelectionRange` | 選択範囲を設定 |
| `ClearSelection` | 選択範囲をクリア |
| `GetTrackFilterNames` | 利用可能なトラックフィルター名一覧 |
| `IsTrackFilterActive` | 指定フィルターの有効状態 |
| `SetTrackFilterActive` | 指定フィルターの有効状態を切り替え |
| `SetLocked` | シーケンスのロック状態を切り替え |
| `IsLocked` | ロック状態を取得 |

#### シーケンスプロパティ（6）

| コマンド | 説明 |
|---|---|
| `SetDisplayRate` | LevelSequence の DisplayRate を変更 |
| `GetViewRange` | Sequencer タイムラインのビュー範囲 |
| `SetViewRange` | ビュー範囲を設定 |
| `GetWorkRange` | ワーク範囲 |
| `SetWorkRange` | ワーク範囲を設定 |
| `SetTickResolution` | TickResolution を変更（既存キーフレーム有無を Warning で通知） |

#### マークフレーム（5）

| コマンド | 説明 |
|---|---|
| `AddMarkedFrame` | マークフレームをラベル付きで追加 |
| `GetMarkedFrames` | 全マークフレーム一覧 |
| `DeleteMarkedFrame` | インデックス指定でマークフレームを削除 |
| `DeleteAllMarkedFrames` | 全マークフレームを削除 |
| `FindMarkedFrameByLabel` | ラベル指定でマークフレームを検索 |

#### サブシーケンス（2）

| コマンド | 説明 |
|---|---|
| `GetSubSequences` | SubSequence トラックのセクション一覧 |
| `AddSubSequenceTrack` | SubSequence トラックを追加 |

#### AnimMixer（42、オプショナル `MovieSceneAnimMixer`）

| コマンド | 説明 |
|---|---|
| `GetAnimMixerTrackInfo` | AnimMixer トラック情報を取得 |
| `GetMixerLayers` | バインディングの全 AnimMixer レイヤーの概要 |
| `GetMixerLayerCount` | バインディングの AnimMixer トラックのレイヤー数 |
| `GetLayerName` | レイヤーの表示名を取得 |
| `SetLayerName` | レイヤーの表示名を設定 |
| `GetLayerIndex` | 表示名からレイヤーの 0 始まりインデックスを取得（存在しなければ `NotFound`） |
| `GetLayerSections` | レイヤー内の全アニメーションセクション |
| `IsLayerEmpty` | レイヤーにアニメーションセクションが無いかどうか |
| `InsertMixerLayer` | 指定インデックスに空レイヤーを挿入し以降をずらす。新しいインデックスを返す |
| `GetTransitionsForSection` | 指定セクションが関与する Transition 一覧（`FromSectionIndex`・`ToSectionIndex`・`TransitionClass`） |
| `GetTransitionBetween` | 2 つのセクションインデックス間の Transition の基本情報（無ければ `NotFound`） |
| `GetTransitionInfo` | 2 つのセクション間の Transition の詳細情報 |
| `GetTransitionName` | 2 つのセクション間の Transition の表示名 |
| `ChangeTransitionType` | Transition を `NewTransitionClass` のものへ差し替え（単一トランザクション内で作成→削除の順） |
| `GetCompatibleDecorations` | レイヤーに適用可能な Decoration クラス一覧。任意の `Target`（既定 `"Layer"` または `"ChildTrack"`）でレイヤーか子トラックかを選択できる。⚠️ **変更点** — `CompatibleDecorations` の配列要素は単純なクラスパス文字列ではなく、`DecorationClass` と `Admission` / `RequiredCapabilities` / `MissingCapabilities` を持つオブジェクトになった |
| `GetDecorations` | レイヤー上の既存 Decoration 一覧。任意の `Target`（既定 `"Layer"` または `"ChildTrack"`）でレイヤーか子トラックかを選択できる。⚠️ **変更点** — `Decorations` の配列要素は単純なクラスパス文字列ではなく、`DecorationClass` と `Admission` / `RequiredCapabilities` / `MissingCapabilities` を持つオブジェクトになった |
| `FindDecoration` | レイヤー上の特定 Decoration を検索（無ければ `NotFound`）。任意の `Target`（既定 `"Layer"` または `"ChildTrack"`）でレイヤーか子トラックかを選択できる。`Target` が `"ChildTrack"` で子トラックが無い場合も `NotFound`。解決できない `DecorationClass` を強制ロードすることはない |
| `AddDecoration` | レイヤーに Decoration を追加（既存があればそれを返す）。任意の `Target`（既定 `"Layer"` または `"ChildTrack"`）で解決先を選択でき、互換性判定は `Target` が解決した対象に対して行われる。`DecorationClass` がこのドメインが Decoration を出荷する 5 モジュールの外から来る場合、`SequencerStructureEdit` に加えて `SequencerCustomTypeEdit` が必要 — [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照。⚠️ **変更点** — `DecorationClass` はこのエディタが既に読み込み済みのものだけを対象に解決され、強制ロードされなくなった。解決できないパスは、従来のオンデマンドロードに代わり `NotFound` になる |
| `RemoveDecoration` | レイヤーから Decoration を削除。任意の `Target`（既定 `"Layer"` または `"ChildTrack"`）でレイヤーか子トラックかを選択できる。`Target` が `"ChildTrack"` で子トラックが無い場合も `NotFound`。削除する Decoration のクラスが信頼できないものである場合は `SequencerCustomTypeEdit` が必要 |
| `GetLayerBlendWeight` | レイヤーのブレンドウェイトを取得 |
| `SetLayerBlendWeight` | レイヤーのブレンドウェイトを設定 |
| `IsLayerMuted` | レイヤーのミュート状態を取得 |
| `SetLayerMuted` | レイヤーのミュート状態を切り替え |
| `IsLayerEnabled` | レイヤーの有効状態を取得 |
| `SetLayerEnabled` | レイヤーの有効状態を切り替え |
| `ClearMixerLayer` | レイヤーの全セクションを削除 |
| `AddMixerLayer` | AnimMixer レイヤーを追加 |
| `RemoveMixerLayer` | AnimMixer レイヤーを削除 |
| `MoveMixerLayer` | AnimMixer レイヤーを移動 |
| `AddMixerSection` | AnimMixer セクションを追加 |
| `RemoveMixerSection` | AnimMixer セクションを削除 |
| `SetMixerSectionRange` | AnimMixer セクションのフレーム範囲を設定（生 FFrameNumber Tick 単位） |
| `SetMixerSectionAnimation` | AnimMixer セクションのアニメーションを設定 |
| `AddMixerTransition` | Transition を追加 |
| `RemoveMixerTransition` | Transition を削除 |
| `GetMixerSectionInfo` | AnimMixer セクション情報を取得 |
| `AddMixerChildTrack` | `LayerIndex` のレイヤーに紐づく子トラックとして ControlRig 子トラックを追加し、`ControlRigPath`（`UControlRig` 派生である必要がある）の ControlRig インスタンスを生成してパラメータセクションを紐づける。`LayerIndex` は現在のレイヤー数と同じ値を指定して末尾に新規行を追加できる。任意の `IsLayered`（既定 false）で新しい ControlRig を加算式に設定できる。対象レイヤーに既に子トラックまたはアニメーションセクションがある場合は副作用なしで `Conflict`。`ControlRigPath` はどちらの形式の Control Rig アセットも受け付ける（UE 5.8 ではアセット本体のパス。例: `/Game/X.X`。`/Game/X.X:X_EditorOnly` のような内部の部品のパスは見つからない扱い）。Control Rig ではないパスは `NotFound` |
| `RemoveMixerChildTrack` | `LayerIndex` のレイヤーに紐づく子トラックを削除し、レイヤー参照・子トラック管理データ・Decoration・バインディングをまとめて片付ける。レイヤーに子トラックが無ければ `NotFound` |
| `GetMixerChildTracks` | バインディングの AnimMixer トラックの全レイヤーにわたる子トラック一覧。各エントリは `LayerIndex`・`TrackName`・`TrackClass` を持つ |
| `MoveMixerChildTrack` | `LayerIndex` に紐づく子トラックを `NewLayerIndex` へ移動する。両インデックスが等しい場合は副作用なしの no-op として成功する。移動先レイヤーに既に子トラックまたはアニメーションセクションがある場合は副作用なしで `Conflict` |
| `SetMixerSectionBlendType` | `LayerIndex` に紐づく子トラックの `SectionIndex` のアニメーションセクションのブレンドタイプを設定する。`BlendType` は Absolute / Additive / Relative / Override のいずれかと大文字小文字を区別せず照合され、対象セクションがサポートしている必要がある |
| `GetMixerSectionBlendType` | `LayerIndex` に紐づく子トラックの `SectionIndex` のアニメーションセクションの現在のブレンドタイプと、サポートされているブレンドタイプの一覧を取得する |

#### ControlRig トラック（12）

**LevelSequence 内**での ControlRig オーサリング。ControlRig アセット自体の編集は [`UAIP.Editor.ControlRig`](#uaipeditorcontrolrig) を参照してください。

| コマンド | 説明 |
|---|---|
| `GetControlRigTracks` | LevelSequence 内の全 ControlRig パラメータトラック。各エントリは `IsChildTrack` を持ち、`true` のときのみ `LayerIndex` も含まれる |
| `GetControlRigSectionInfo` | セクションのプロパティ — `IsInfinite`・`StartFrame`・`EndFrame`・`IsActive`・クラス名 |
| `FindOrCreateControlRigTrack` | バインディングの ControlRig パラメータトラックを取得または作成し `TrackCreated` を返す。任意の `IsLayered`（既定 false）で新規作成する ControlRig を加算式に設定できる。既存トラックが見つかった場合は無視される。どちらの形式の Control Rig アセットも受け付ける（UE 5.8 では内部の部品のパスではなくアセット本体のパス、例: `/Game/X.X` を渡す）。Control Rig を指さないパスは `NotFound`。別の Control Rig のトラックを取り違えることはない |
| `BakeToControlRig` | バインディングのアニメーションを ControlRig トラックへベイク（表示レートフレーム・`Tolerance` は 0.0〜1.0）。どちらの形式の Control Rig も受け付け、Control Rig を指さないパスは `NotFound`。**UE 5.8 の新形式（ランタイムアセット）の Control Rig ではキー削減が異なります。** `Tolerance` が 0 より大きければ削減する点は同じですが、古い形式のキー値の差そのものではなく値の幅に対する割合（`0.1` なら 10%）として扱われるため、既定の `0.1` はエンジンの画面の既定（5%）より強く削減します。削減にはそのシーケンスをレベルシーケンスエディタで開いておく必要があり、開いていない場合（別のシーケンスが開いている場合も含む）は `PreconditionFailed` で断り、トラックもキーも変更しません。シーケンスを開くか、削減しないなら `Tolerance: 0` を渡してください。ベイク後は、そのバインディングのアニメーショントラックをすべて無効にします（古い形式は 1 本目のみ） |
| `KeyControls` | 指定コントロールを 1 つの表示レートフレームでキー（`ControlNames` 省略時は表示中の全コントロール） |
| `KeyControlsAtFrames` | 指定コントロールを複数の表示レートフレームでキー。UE 5.8+ 専用。UE 5.7 では `Available: false`（`UnavailableDetail: "EngineVersion"`） |
| `GetControlsMask` | ControlRig セクションのコントロール別表示マスク |
| `SetControlsMask` | 指定コントロールの表示状態を設定（未指定のコントロールは現状維持） |
| `ShowAllControls` | セクション内の全コントロールを表示 |
| `HideAllControls` | セクション内の全コントロールを非表示 |
| `LoadAnimIntoRig` | AnimSequence を ControlRig セクションのコントロールへ焼き込む。トラックのバインディングが解決するスケルタルメッシュを通してアニメーションをサンプリングするため、対象アクターのいるレベルが開かれている必要がある（開かれていない場合は `NotFound`） |
| `GetActorTransformAtFrame` | 指定フレームでシーケンスを評価し、名前指定したアクターのワールドトランスフォームを返す |

#### ギズモの大きさ（2）

Animation Mode ビューポートの旧トランスフォームギズモの大きさで、エディタ設定に保存される値です。この 2 コマンドは Toolset レジストリが無くても、UE 5.7 でも使えます。引数名 `Scale` はそのままですが、**倍率ではありません**。旧ギズモの大きさに足すオフセットで、範囲は -10〜150、既定は 0 です。0 と負の値は受け付け、150 を超える値・数値でない値・無限大は `InvalidParams` で断られます。読むのは旧ギズモだけです。UE 5.8 で既定の TRS ギズモは軸の倍率で大きさが決まるので、[`UAIP.Editor.Level.SetTransformGizmoSize`](#uaipeditorlevel) で変えてください（このオフセットも `LegacySizeOffset` として書けます）。

| コマンド | 説明 |
|---|---|
| `GetAnimModeGizmoScale` | 旧ギズモの大きさのオフセットを `Scale` として返す。同名の Toolset ブリッジコマンドと違い、エディタ設定に保存された値を読む。`EditorInspect` 必要 |
| `SetAnimModeGizmoScale` | 旧ギズモの大きさのオフセット（`Scale`、-10〜150、既定 0）を設定し、エディタ設定に保存してビューポートを描き直す。Toolset ブリッジコマンドと違い、値は再起動後も残る。`SequencerStructureEdit` 必要 |

### Toolset ブリッジ（61）🧩

プロバイダ：`Toolset.Editor.AnimationAssistant.*`（41 件 — Lifecycle 6・Playback 10・Property 9・MarkedFrame 5・UI 11）と `Toolset.Editor.SequencerAnimMixer.*`（20 件 — Layers 10・Transitions 5・Decorations 5）。UE 5.8+ が必要。

> Sequencer モジュール実装のもう 1 つのブリッジプロバイダ `Toolset.Editor.SequencerControlRig.*`（63 件）は、コマンドの対象が ControlRig のコントロールであるため [`UAIP.Editor.ControlRig`](#uaipeditorcontrolrig) 側に掲載しています。

> Decoration の変更系 2 コマンド（`AddDecoration` / `RemoveDecoration`）は、native 版とまったく同じ形で `SequencerCustomTypeEdit` によりゲートされています — native 側だけを塞いでも、同じクラスが bridge 経由でそのまま到達できてしまうためです。Decoration の一覧系 2 コマンド（`GetCompatibleDecorations` / `GetDecorations`）は、外部 Toolset レジストリの応答をそのまま通す passthrough 実装のため、native の一覧コマンドが返すようになった `Admission` / `RequiredCapabilities` / `MissingCapabilities` を持ちません。この情報が必要な場合は native コマンドを使用してください。

> **範囲・マーカー・ロックの引数は、Sequencer Toolset 自身の引数に揃えています。** 各コマンドは、対応する Toolset 関数が取る単位で受け付けます。ブリッジはフレームと秒の換算をしません（もう一方の単位やラベルが要るときは、ネイティブの `UAIP.Editor.Sequencer.*` コマンドを使ってください）。
>
> - ⚠️ **`AddMarkedFrame` は `Label` を取らなくなりました。** Toolset にラベルの引数が無く、反映されなかったためです。`Label` を送ると `InvalidParams` で断ります。
> - ⚠️ **`SetPlaybackRange` と `SetSelectionRange` は `StartFrame` と `EndFrame` が必須になりました**（整数。以前は任意）。`SetPlaybackRange` は `StartSeconds` / `EndSeconds` を取らなくなりました。開始が終了より前でない再生範囲は Toolset が断ります。
> - ⚠️ **`SetViewRange` と `SetWorkRange` は `StartSeconds` と `EndSeconds` が必須になりました**（数値。以前は任意）。`StartFrame` / `EndFrame` は取らなくなりました。片側だけの範囲や数値でない値は `InvalidParams` で断ります。
> - ⚠️ **`SetSequenceLocked` は `Locked` ではなく `Lock` を取ります**（真偽値、必須）。`Locked` で呼ぶと常に失敗していました。
> - ⚠️ **`Toolset.Editor.SequencerControlRig.MergeControlRigAnimLayers`: `Indices` の要素を整数と宣言しました。** 数値は従来どおり動きます。文字列の要素は `InvalidParams` で断ります。

---

## UAIP.Editor.StateTree

StateTree 編集。

### ネイティブ（39）

#### State 観測（8）

| コマンド | 説明 |
|---|---|
| `GetRootStates` | トップレベル State のディスクリプタ（`StateId`・`Name`・`Type`・`ParentStateId`・`ChildCount`） |
| `GetStateChildren` | 単一 State の直下の子 State ディスクリプタ |
| `GetStateTasks` | 単一 State の Task 一覧（PIE 中の degraded モードではクラス名を秘匿）。各エントリは Task 自身のクラスに対する `Admission` / `RequiredCapabilities` / `MissingCapabilities` を併記するようになりました — 下の Note を参照してください。`SchemaVersion` は `2` になりました |
| `GetStateTransitions` | 単一 State の Transition 一覧（PIE 中は遷移先 State ID を秘匿） |
| `GetStateEnterConditions` | 単一 State の Enter Condition 一覧。`GetStateTasks` と同じ Admission フィールドを報告します。`SchemaVersion` は `2` になりました |
| `GetStateTreeGlobalTasks` | アセットのグローバル Task 一覧（アクティブ State に関係なく実行される）。`GetStateTasks` と同じ Admission フィールドを報告します。`SchemaVersion` は `2` になりました |
| `GetStateTreeEvaluators` | アセットの Evaluator 一覧（毎 Tick 実行され共有データを更新する）。`GetStateTasks` と同じ Admission フィールドを報告します。`SchemaVersion` は `2` になりました |
| `GetStateNodeDescription` | ノード GUID のクラスパスと表示名（グローバル Task・Evaluator・全 State を横断検索） |

> **Note — 上の 4 つのノード一覧は、このドメインが出荷していないクラスをもう秘匿しません。** 従来は追加経路が拒否するノードについて `TaskClass` / `ConditionClass` / `EvaluatorClass` を `"<redacted>"` に置き換え、`MaskedDueToPolicy: true` を立てていました。現在は 4 つとも実クラス名を返し、代わりに `Admission` / `RequiredCapabilities` / `MissingCapabilities` を併記します。これは下記の `GetAvailableTaskClasses` / `GetAvailableConditionClasses` / `GetAvailableEvaluatorClasses` が未配置のクラスについて既に行っている報告と同じ形です。`MaskedDueToPolicy` フィールドは互換のため残していますが、常に `false` になりました。**これは degraded（PIE）読み取り中に依然として掛かる秘匿とは無関係です** — この機能より前から存在する理由により、PIE 中は Capability の有無にかかわらず引き続きクラス名を `"<redacted>"` に置き換えます。
>
> ⚠️ あわせて無関係な 2 つの不具合も修正しました。ネイティブ struct（Blueprint インスタンスではなく）が裏付けとなるグローバル Task・Evaluator・Enter Condition ノードは、従来ノードクラスポリシーを一切経由せず Admission フィールドが一度も付与されていませんでしたが、現在は経由するようになりました。Evaluator・Enter Condition ノードは従来 Task ノードとして判定されており、追加経路では通るクラスに対して `WrongBaseType` 相当の拒否を報告することがありましたが、現在は自分自身の基底クラスに対して判定します。

#### クラス / スキーマ探索（5）

| コマンド | 説明 |
|---|---|
| `GetAvailableTaskClasses` | `FStateTreeTaskBase` フィールド一覧（ネイティブ struct + Blueprint）— `ClassPath` を `AddStateTask` / `AddGlobalTask` に渡す。各エントリは追加コマンドと同じ policy から得た `Admission`（`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`）と `RequiredCapabilities` / `MissingCapabilities` を併記するようになりました — ネイティブ struct 階層を含みます（従来のフィルタはこの階層を一切参照していませんでした）。`ClassPath` 昇順で並び、`TotalCount` / `ReturnedCount` / `Truncated`（上限 200 件。struct 階層と class 階層を合算したうえで 1 回だけ適用）を報告します。`SchemaVersion` は `2` になりました — 下の Note を参照してください |
| `GetAvailableConditionClasses` | `FStateTreeConditionBase` フィールド一覧（ネイティブ struct + Blueprint）— `ClassPath` を `AddStateEnterCondition` に渡す。上と同じ Admission・件数フィールドを報告します |
| `GetAvailableEvaluatorClasses` | `FStateTreeEvaluatorBase` フィールド一覧（ネイティブ struct + Blueprint）— `ClassPath` を `AddEvaluator` に渡す。上と同じ Admission・件数フィールドを報告します |
| `GetAvailableStateTreeSchemaClasses` | `UStateTreeSchema` サブクラス — `ClassPath` を `CreateAsset` の `FactoryParams.SchemaClass` に渡す。各エントリは `Admission`（`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`）と `RequiredCapabilities` / `MissingCapabilities` を持ちます。判定元は `CreateAsset` が名指しされた Schema クラスを審査するのと同じポリシーで、このドメインが提供していない Schema クラスも、一覧から除外されるのではなく「何が要るか」を添えて列挙されます。エディタの Schema ピッカーが隠すクラスも `NotAddable` として列挙されます。`ClassPath` 順で、`TotalCount` / `ReturnedCount` / `Truncated` を報告します。`SchemaVersion` は `2` になりました — 下記の Note を参照 |
| `GetStateTreeSchema` | アセットの Schema クラスパスとルートパラメータのディスクリプタ |

#### State 構造編集（4）

| コマンド | 説明 |
|---|---|
| `AddState` | State を追加（State / Group / Subtree / Linked / LinkedAsset の 5 種類）。`StateId` を返す |
| `RemoveState` | StateId 指定で State を削除（子 State 再帰削除） |
| `SetStateName` | State をリネーム |
| `MoveState` | State の親／順序を変更（循環参照になる移動は拒否） |

#### Task / Transition / Condition 編集（9）

| コマンド | 説明 |
|---|---|
| `AddStateTask` | State に Task を追加 — このドメインが出荷していないモジュール由来のクラスには Capability が要ります。下の Note を参照してください。`TaskId` を返す |
| `RemoveStateTask` | TaskId 指定で Task を削除 — 削除される Task 自身のクラスが要求する Capability が同じく必要です |
| `AddStateTransition` | Transition を追加（`Succeeded` / `Failed` / `NextState` / `NextSelectableState` / GUID 指定）。`OnDelegate` は非対応 |
| `RemoveStateTransition` | TransitionId 指定で Transition を削除 |
| `AddStateEnterCondition` | State に Enter Condition を追加 — `AddStateTask` と同じ Capability 確認。`ConditionId` を返す |
| `RemoveStateEnterCondition` | ConditionId 指定で Enter Condition を削除 — 削除される Condition 自身のクラスが要求する Capability が同じく必要です |
| `SetEnterConditionProperty` | Enter Condition ノードのプロパティを設定 — Condition 自身のクラスと、そのプロパティを宣言しているクラスの**両方**が要求する Capability が必要です |
| `GetStateNodeProperty` | ノード GUID のトップレベルプロパティ 1 件をエクスポートテキストで取得 |
| `SetStateNodeProperty` | Task ノードのプロパティを設定（汎用 ImportText_Direct）— Task 自身のクラスと、そのプロパティを宣言しているクラスの**両方**が要求する Capability が必要です |

#### グローバル Task / Evaluator 編集（6）

| コマンド | 説明 |
|---|---|
| `AddGlobalTask` | グローバル Task を追加 — `AddStateTask` と同じ Capability 確認。`TaskId` を返す |
| `RemoveGlobalTask` | TaskId 指定でグローバル Task を削除 — 削除される Task 自身のクラスが要求する Capability が同じく必要です |
| `SetGlobalTaskProperty` | グローバル Task ノードのプロパティを設定 — Task 自身のクラスと、そのプロパティを宣言しているクラスの**両方**が要求する Capability が必要です |
| `AddEvaluator` | Evaluator を追加 — `AddStateTask` と同じ Capability 確認。`EvaluatorId` を返す |
| `RemoveEvaluator` | EvaluatorId 指定で Evaluator を削除 — 削除される Evaluator 自身のクラスが要求する Capability が同じく必要です |
| `SetEvaluatorProperty` | Evaluator ノードのプロパティを設定 — Evaluator 自身のクラスと、そのプロパティを宣言しているクラスの**両方**が要求する Capability が必要です |

> **Note — プロジェクト製の Task・Evaluator・Enter Condition クラスは Capability でゲートされ、無条件に拒否されることはありません**: `/Script/StateTreeModule`・`/Script/AIModule`・`/Script/GameplayStateTreeModule` 以外から来たクラスまたは struct — プロジェクトのモジュール、プラグインのモジュール、Blueprint 生成クラス — には `StateTreeCustomTypeEdit` が必要です。既定では付与されません。[安全性と Capability](safety.md#statetree-編集) を参照してください。MetaSound や Enhanced Input と同様、Material とは異なり、このドメインに「危険な型」用の別 Capability はありません。Task・Evaluator・Enter Condition フィールドはツリーが自身のインスタンスデータの値で呼び出すコンパイル済み関数であり、ノードプロパティは単なるデータメンバです — どちらも呼び出し元が持ち込んだコードを運びません。
>
> **プロパティの書き込みは 2 つのクラスを独立して確認します。** `SetStateNodeProperty` / `SetGlobalTaskProperty` / `SetEvaluatorProperty` / `SetEnterConditionProperty` はいずれも、ノード自身のクラスと、書き込まれるプロパティを宣言している struct/class を別々の問いとして admit します。どちらか一方でもセッションが持たない Capability を要求すれば書き込み全体が拒否され、拒否メッセージは両方の不足 Capability を一度に名指しします。
>
> **コンパイルはこの Capability によってゲートされることはありません。** `CompileStateTree` は、アセットが単に含んでいるクラスについては何も要求しません — そうでなければ、プロジェクト製の Task を 1 つでも含む StateTree は Capability の付与なしには一切コンパイルできなくなってしまいます。ゲートされるのは、リクエストが**名指しした**クラスと、リクエストが**操作対象にした**ノードだけです。
>
> これらの確認は `Add*` コマンドに限りません — 既存ノードの編集・削除でも同じ Capability があらためて確認されます。詳細は [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照してください。
>
> ⚠️ **破壊的変更**: こうしたクラスは従来 `PolicyViolation` で拒否されていました。`AddStateTask` / `AddGlobalTask` / `AddEvaluator` / `AddStateEnterCondition` と 4 つの `Set*Property` コマンドは `CapabilityNotAvailable` を返し、不足している Capability をすべて一度に名指しします。現在ロードされている中に該当が無いクラスパスは `NotFound`、abstract・deprecated・新版あり・そもそも StateTree ノードでないクラスは `InvalidParams` になります。**`RemoveStateTask` / `RemoveGlobalTask` / `RemoveEvaluator` / `RemoveStateEnterCondition` は、今回初めて Capability を確認するようになりました** — 従来はこの 4 つのいずれも policy を一切参照しておらず、削除はクラスにかかわらず拒否されることがありませんでした。クラスパスの解決のためのロードは行いません — クラス解決は従来から `FindObject` のみを使っており、ロードへのフォールバックはありません。
>
> **Note — 3 つのクラス一覧は、ネイティブ struct 階層をもう隠しません。何が要るかも一緒に述べます**: `GetAvailableTaskClasses`・`GetAvailableConditionClasses`・`GetAvailableEvaluatorClasses` は、従来ネイティブな `FStateTree*Base` struct 階層を一切 policy に通さず、Blueprint のクラス階層についても `GetAvailableTaskClasses` でしか通していませんでした — その結果、プロジェクト製の struct ベース Task はエンジン同梱のものとまったく同じ自由さで一覧に載り、Blueprint ベースの Condition や Evaluator も出自を問わず一覧に載っていました。現在は 3 つとも両方の階層を追加コマンドと同じ policy から答え、エントリごとに `Admission` を報告し、そもそも配置できないクラスも落とさず `NotAddable` として載せます。2 つの階層は 1 つの整列・打ち切り済み集合へ統合されました — 従来は階層ごとに独立して上限を適用していたため、応答が理論上、明示された上限の最大 2 倍まで膨らみうるバグがありました。一覧はスナップショットであって認可ではありません — 一覧取得から mutation までの間に Capability や role は変わりうるため、各コマンドは自身のリクエストで判定をやり直します。
>
> **⚠️ アセット作成時に名指しする Schema クラスもゲート対象になりました。エンジン同梱のものも含みます。** `CreateAsset` の `FactoryParams.SchemaClass` は従来、「解決できること」と「`UStateTreeSchema` の子孫であること」の 2 条件だけで受け入れられており、出自は一切見ていませんでした。現在は上記のノードクラスと同じ出自判定を通り、`/Script/StateTreeModule`・`/Script/AIModule`・`/Script/GameplayStateTreeModule` 以外の Schema クラスには `StateTreeCustomTypeEdit` が必要です。これはプロジェクト製のクラスに限った話ではありません。`/Script/MassAIBehavior`・`/Script/GameplayCameras`・`/Script/GameplayInteractionsModule`・`/Script/AvalancheTransition`・`/Script/UAFStateTree` はいずれもエンジン同梱ですが、上記 3 モジュールの外にあるため、これらの Schema を使うには Capability が必要になります。`/Script/GameplayStateTreeModule` の Schema は従来どおり何も要求しません。また、abstract・deprecated・新しい版に置き換えられたクラス、およびエディタの Schema ドロップダウンから隠されているクラスは、どの Capability を持っていても拒否されます — 従来は abstract のみ拒否で、deprecated は警告ログを出すだけでした。クラスのオンデマンド読み込みもやめました。すでにメモリ上にないクラスは、判定のためだけに読み込まれることなく拒否されます。Schema クラスに対する `StateTreeCustomTypeEdit` 不足は、他の経路と同じく Capability 名を挙げて `CapabilityNotAvailable` で返ります — [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照してください。構造的な拒否（abstract・deprecated・新版あり・非表示・未ロード）は `InvalidParams` のままです。

#### パラメータ・バインディング・コンパイル（7）

| コマンド | 説明 |
|---|---|
| `GetStateTreeParameters` | ルートパラメータのディスクリプタ（`Name`・`ParameterType`・現在のシリアライズ値）と、パラメータごとに入れ子の `WriteRequirements` オブジェクト。`ParameterType` は enum / struct / object / soft object / class / soft class と残りの整数幅を名前で返すようになりました（従来は非スカラーを一律 `Unknown` と報告していました） |
| `AddStateTreeParameter` | ルートパラメータを追加（Bool / Byte / Int32 / Int64 / Float / Double / Name / String / Text） |
| `RemoveStateTreeParameter` | 名前指定でルートパラメータを削除 |
| `SetStateTreeParameter` | ルートパラメータ値を設定。参照には `StateTreeParameterReferenceEdit`、構造体・コンテナには `PropertyStructuredEdit` が必要で、これらの値は括弧表記ではなく JSON で渡します。拒否コードは一律 `NotFound` ではなく `CapabilityNotAvailable` / `PolicyViolation` / `InvalidParams` / `NotFound` に細分化され、拒否された書き込みはアセットを dirty にせず、成功した書き込みは undo できるようになりました |
| `AddPropertyBinding` | ソースノードのプロパティをターゲットノードのプロパティへバインド |
| `RemovePropertyBinding` | ターゲットノードのプロパティバインディングを削除 |
| `CompileStateTree` | StateTree をコンパイル（連続呼び出しにはアセット単位のレートリミット） |

### Toolset ブリッジ（8 件）🧩

`StateTreeToolset`（UE 5.8+、Experimental）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.StateTree.*`。観測専用です。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.StateTree.GetEditorData` | StateTree アセットのエディタデータ |
| `Toolset.Editor.StateTree.GetRootStates` | StateTree アセットのルート State |
| `Toolset.Editor.StateTree.GetGlobalTasks` | StateTree アセットのグローバル Task |
| `Toolset.Editor.StateTree.GetEvaluators` | StateTree アセットの Evaluator |
| `Toolset.Editor.StateTree.GetChildren` | `UStateTreeState` の子 State |
| `Toolset.Editor.StateTree.GetTasks` | `UStateTreeState` の Task |
| `Toolset.Editor.StateTree.GetEnterConditions` | `UStateTreeState` の Enter Condition |
| `Toolset.Editor.StateTree.GetTransitions` | `UStateTreeState` の Transition |

---

## UAIP.Editor.Curve

Curve アセット（UCurveFloat / UCurveVector / UCurveLinearColor）のキー編集。

| コマンド | 説明 |
|---|---|
| `GetCurveInfo` | チャンネル一覧・キー・前後外挿（per-channel truncated フラグ付き） |
| `AddCurveKey` | 指定チャンネルにキーを追加 |
| `RemoveCurveKey` | time + tolerance でキーを削除 |
| `SetCurveKeyValue` | 既存キーの値と時刻を更新 |
| `SetCurveKeyInterpolation` | 既存キーの補間モードを変更（Constant / Linear / Cubic / None） |
| `SetCurveKeyTangent` | arrive / leave 接線を設定（非 Cubic キーは自動 Cubic 昇格・`promoted_to_cubic` フラグ通知） |

---

## UAIP.Editor.PCG 🧩

PCG グラフ編集。`PCG` プラグインが必要です。

| コマンド | 説明 |
|---|---|
| `GetPCGGraphInfo` 🧩 | UPCGGraph のノード / エッジ / パラメータ（PIE 中は degraded モード） |
| `ListPCGNodeTypes` 🧩 | allowlist 通過 UPCGSettings サブクラス一覧 |
| `AddPCGNode` 🧩 | SettingsClassPath 指定でノードを追加（NodePath を返す） |
| `RemovePCGNode` 🧩 | NodePath 指定でノードを削除（接続エッジも同時削除） |
| `ConnectPCGPins` 🧩 | NodePath + PinLabel でピンを接続 |
| `DisconnectPCGPins` 🧩 | ピン切断（特定ペア / 出力ピンからの全切断） |
| `SetPCGNodeProperty` 🧩 | UPCGSettings EditAnywhere プロパティを設定。値は JSON ドキュメント。参照・構造体・コンテナは恒久的に拒否されなくなり、`PropertyReferenceEdit` / `PropertyStructuredEdit` で制御される — [参照・構造体・コンテナの書き込み](#参照構造体コンテナの書き込み) を参照 |
| `ExecutePCGGraph` 🧩 | `UPCGComponent::Generate` を起動 |
| `ListCustomPCGNodeTypes` 🧩 | C++ / Blueprint カスタム PCG ノードタイプ一覧 |
| `GetCustomPCGNodeSchema` 🧩 | C++ UPCGSettings サブクラスの EditAnywhere プロパティを JSON スキーマで返す。`PropertyReferenceEdit` / `PropertyStructuredEdit` のいずれも持たないセッションには型を絞った集合を返す。除かれた分は黙って省略せず `HiddenCount` / `HiddenCapabilities` / `HiddenReasons` として報告する |
| `GetCustomBlueprintPCGNodeSchema` 🧩 | Blueprint UPCGBlueprintSettings サブクラスのプロパティを JSON スキーマで返す。`GetCustomPCGNodeSchema` と同じ絞り込みが働き、列挙する 2 クラス分をまとめた 1 つの `HiddenCount` / `HiddenCapabilities` / `HiddenReasons` を返す |
| `SetCustomCppPCGNodeProperty` 🧩 | C++ カスタムノードのプロパティを書き換え（`RecompileTriggered` フラグ）。参照・構造体・コンテナは `PropertyReferenceEdit` / `PropertyStructuredEdit` で制御され、拒否文は意図的にプロパティの型を明かさない — [参照・構造体・コンテナの書き込み](#参照構造体コンテナの書き込み) を参照 |
| `SetCustomBlueprintPCGNodeProperty` 🧩 | BP カスタムノードのプロパティを書き換え（Class CDO / Instance の 2 モード）。制御のされ方は `SetCustomCppPCGNodeProperty` と同じ |
| `CreatePCGGraph` 🧩 | 新規 UPCGGraph アセットを Content ディレクトリに作成（`PCGGraphAssetCreate` 必須） |
| `GetPCGGraphSchema` 🧩 | グラフのノード / ピン構成をスキーマ形式で取得 |
| `GetPCGGraphDescription` 🧩 | グラフの Description 文字列を取得 |
| `SetPCGGraphDescription` 🧩 | グラフの Description を設定（`PCGGraphEdit` 必須） |
| `SetPCGGraphParams` 🧩 | グラフパラメータを追加 / 更新（`PCGGraphEdit` 必須）。値は範囲・NaN を検査し、不正な値は `InvalidParams` で拒否します。適用はいったん複製に対して行うため、拒否時に部分適用・undo エントリ・dirty マークが残りません |
| `RemovePCGGraphParams` 🧩 | グラフパラメータを削除（`PCGGraphEdit` 必須） |
| `ListPCGGraphInstances` 🧩 | レベル内の UPCGComponent 一覧を取得 |
| `SpawnPCGGraphInstance` 🧩 | APCGVolume を World にスポーン（`PCGVolumeSpawn` 必須） |
| `GetPCGGraphInstanceParams` 🧩 | インスタンスのオーバーライドパラメータを取得 |
| `SetPCGGraphInstanceParams` 🧩 | インスタンスパラメータをオーバーライド（`PCGGraphEdit` 必須）。範囲 / NaN の検査と全件適用か全件不適用かの扱いは `SetPCGGraphParams` と同じ |
| `ResetPCGGraphInstanceParams` 🧩 | インスタンスパラメータをデフォルトにリセット（`PCGGraphEdit` 必須）。リセットする対象が無い場合も従来どおり成功を返しますが、トランザクションを開かず dirty マークも付けなくなりました |
| `ListPCGAvailableSubgraphs` 🧩 | プロジェクト内のサブグラフ候補を列挙 |
| `GetPCGNativeNodeSchema` 🧩 | ネイティブ PCG ノードクラスの EditAnywhere プロパティを JSON スキーマで返す。`GetCustomPCGNodeSchema` と同じ絞り込みが働き、`HiddenCount` / `HiddenCapabilities` / `HiddenReasons` を返す |
| `AddPCGSubgraphNode` 🧩 | サブグラフ参照ノードを追加（`PCGGraphEdit` 必須） |
| `RepositionPCGNode` 🧩 | ノード位置を変更（`PCGGraphEdit` 必須） |
| `AddPCGCommentBox` 🧩 | コメントボックスを追加（`PCGGraphEdit` 必須） |
| `UpdatePCGCommentBox` 🧩 | コメントボックスを更新（`PCGGraphEdit` 必須） |
| `RemovePCGCommentBox` 🧩 | コメントボックスを削除（`PCGGraphEdit` 必須） |
| `GetPCGNodeDataView` 🧩 | PCG ノードの実行データビューを取得（`PCGNodeInspect` 必須。`PCG_PROFILING_ENABLED=0` 時は CapabilityNotAvailable） |
| `RunPCGInstantGraph` 🧩 | アクター / コンポーネント不要の fire-and-forget PCG グラフ実行（`PCGGraphExecute` 必須） |
| `DrawPCGSpline` 🧩 | レベルビューポートで人間がスプラインを描き終える対話を開始し、待たずに `InteractionId` を返す（`IsInteractive: true`）。`GetPendingInteractionStatus` でポーリング、`WaitForPendingInteraction` で短時間ブロック、`CancelPendingInteraction` でキャンセルできる。`PCGSplineDraw` と `SafetyPolicy.AllowUserInteractionPrompt`（別ゲート）が必須。ビューポートを保持できる対話は同時に 1 件のみ |

### Toolset ブリッジ — PCG（31 件）🧩

`PCGToolset`（UE 5.8+）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.PCG.*`。アクティブな PCG エディタタブが必要なコマンドは非インタラクティブコンテキストで `ExecutionFailed` を返す場合があります（PCGToolset の既知の制約）。

> **⚠️ 破壊的変更 — `SetGraphInstanceParams` と `ResetGraphInstanceParams` が要求する Capability が `PCGGraphExecute` から `PCGGraphEdit` になりました**（ネイティブ版と同じ名前）。どちらも同じパラメータ bag を書き換える操作であり、実行系の Capability を要求していたため、運用者が `PCGGraphEdit` を閉じてもブリッジ経由でインスタンスのオーバーライドを変更できていました。**`PCGGraphExecute` だけを付与していたセッションはこの 2 コマンドを使えなくなります** — `PCGGraphEdit` を追加してください。
>
> **ブリッジ経由では UAIP の値検査が及びません。** `SetGraphParams` / `SetGraphInstanceParams` / `ResetGraphInstanceParams` の書き込みは `UPCGToolset` の内部で行われるため、ネイティブ版が適用する型ゲート・範囲 / NaN の検査・途中終了パースの検査・全件不可なら 1 件も書かない扱いは適用されません。検査が必要な場合はネイティブの `SetPCGGraphParams` / `SetPCGGraphInstanceParams` / `ResetPCGGraphInstanceParams` を使ってください。

> **引数は PCG Toolset が宣言する形に揃えています。**
>
> - **オブジェクト引数は、オブジェクトパスの文字列でも `{"refPath": "..."}` でも渡せます。** 対象は `AddNode`・`AddSubgraphNode`・`ConnectNodePins`・`DisconnectNodePins`・`ExecuteGraphInstance`・`GetGraphDescription`・`GetGraphInstanceParams`・`GetGraphSchema`・`GetGraphStructure`・`GetNodeDataView`・`GetNodeInfo`・`RemoveCommentBox`・`RemoveGraphParams`・`RemoveNode`・`RepositionNode` の `Graph` / `Node` / `FromNode` / `ToNode` / `PCGVolume` / `SubGraphForNode` と、下の作り直した 9 コマンドのオブジェクト引数です。`{"refPath": ...}` の呼び出しは従来どおり動きます。以前は Toolset に断られていたパス文字列も動くようになりました。パスは `Package.Object` の形（例: `/Game/PCG/G.G`）で、パッケージパスだけでは解決できません。
> - **Toolset が必須とする引数に既定値を付けました。** `AddNode` と `AddSubgraphNode` の `JsonParams` / `NodeTitle` / `NodeComment`、`GetNodeDataView` の `AttributeName`、`UpdateNode` の `JsonParams` / `NodeTitle` は既定値 `""` です。省略しても Toolset 側で失敗しなくなります。
> - **`AddCommentBox`: `Graph` と `Nodes` はパス文字列でも `{"refPath": ...}` でも渡せます。** `Color` はオブジェクトで、`r` / `g` / `b` / `a` は数値（`"0.5"` のような数値の文字列は変換します）、既定値は各 `1` で、ブリッジは常に 4 つとも送ります。`Color` のそれ以外のメンバーは無視し、送りません。数値として読めない成分は Toolset へ渡し、Toolset が断ります。
> - **`UpdateCommentBox` は呼ぶたびに色を設定します。** `Color` を省略すると既定の白で上書きされます（ブリッジは現在の色を読めないため）。
> - ⚠️ **9 コマンドを Toolset 自身の引数で作り直しました。** 以前は Toolset が宣言していないネイティブ風のキーを送っていたため、Toolset が必ず断っていました。旧キーは `InvalidParams` で先に断るようになりますが、動いていた呼び出しが失われることはありません。
>
> | コマンド | 現在の引数 | 受け付けなくなった旧キー |
> |---|---|---|
> | `ResetGraphInstanceParams` | `PCGVolume`（必須）、`ParamNames`（必須、文字列の配列） | `ActorIdentifier` |
> | `RunPCGInstantGraph` | `Graph`（必須）、`Params`（必須、値がすべて文字列のオブジェクト。無ければ `{}`） | `AssetPath` |
> | `SetGraphDescription` | `Graph`（必須）、`Description`（必須） | `AssetPath` |
> | `SetGraphInstanceParams` | `PCGVolume`（必須）、`JsonParams`（必須、**JSON 文字列**） | `ActorIdentifier`、`Parameters` |
> | `SetGraphParams` | `Graph`（必須）、`Params`（必須、パラメータ定義の配列。`Name` と `Type` は必須、`Description`・`ContainerType`・`DefaultValueJson` は省略可能） | `AssetPath`、`Parameters` |
> | `SetNodeComment` | `Node`（必須）、`NodeComment`（必須） | `AssetPath`、`NodePath`、`CommentText` |
> | `SpawnGraphInstance` | `Graph`（必須）、`Name`（必須）、`Transform`（任意。`Transform.location.x/y/z`・`Transform.rotation.pitch/yaw/roll`・`Transform.scale.x/y/z`。省略した部分は恒等変換）、`JsonParams`（既定値 `""`） | `AssetPath`、`ActorLabel` |
> | `UpdateCommentBox` | `Graph`（必須）、`CommentId`（必須）、`Nodes`（必須。ノードをそのままにするなら `[]`）、`Comment`（既定値 `""`）、`Color.r/g/b/a`（既定値 `1`） | `AssetPath`、`CommentNodeGuid`、`CommentText`、`NodeX`、`NodeY`、`CommentWidth`、`CommentHeight` |
> | `UpdateNode` | `Node`（必須）、`JsonParams`（既定値 `""`）、`NodeTitle`（既定値 `""`） | `AssetPath`、`NodePath`、`PropertyName`、`PropertyValue` |
>
> 同名の `UAIP.Editor.PCG.*` ネイティブコマンドは、これまでのキーのままです。
> - **`SetGraphParams` は `Params` の要素の形を宣言します。** 各要素は、`Name`（文字列）と `Type`（Toolset の型名。`float` のような小文字も可。または数値）がどちらも必須のオブジェクトで、`Description`（既定値 `""`）・`ContainerType`（既定値 `"None"`）・`DefaultValueJson`（既定値 `""`）は省略するとこの既定値で送られます。一覧にないメンバーは受け付けて送らず、文字列でない（数値など）`Description` / `ContainerType` / `DefaultValueJson` は従来どおりそのまま Toolset へ渡します。⚠️ `Name` や `Type` の無い要素と裸の文字列の要素は、Toolset を呼ぶ前に `InvalidParams` で断ります。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.PCG.CreateGraph` 🧩 | PCG グラフアセットを作成（`PCGGraphAssetCreate` 必須） |
| `Toolset.Editor.PCG.GetGraphStructure` 🧩 | グラフ全体の構造（ノード・エッジ・パラメータ）を取得 |
| `Toolset.Editor.PCG.SetGraphParams` 🧩 | グラフパラメータを設定（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.RemoveGraphParams` 🧩 | グラフパラメータを削除（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.GetGraphSchema` 🧩 | グラフスキーマを取得 |
| `Toolset.Editor.PCG.GetGraphDescription` 🧩 | グラフの説明文を取得 |
| `Toolset.Editor.PCG.SetGraphDescription` 🧩 | グラフの説明文を設定（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.ListGraphInstances` 🧩 | グラフを参照しているボリュームアクター一覧 |
| `Toolset.Editor.PCG.SpawnGraphInstance` 🧩 | PCG ボリュームアクターをスポーン（`PCGVolumeSpawn` 必須） |
| `Toolset.Editor.PCG.ExecuteGraphInstance` 🧩 | PCG ボリューム上でグラフを実行（`PCGGraphExecute` 必須；非同期・デフォルト 300 秒） |
| `Toolset.Editor.PCG.GetGraphInstanceParams` 🧩 | インスタンスのパラメータオーバーライドを取得 |
| `Toolset.Editor.PCG.SetGraphInstanceParams` 🧩 | インスタンスパラメータを上書き（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.ResetGraphInstanceParams` 🧩 | インスタンスパラメータをリセット（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.ListNativeNodes` 🧩 | 登録済みネイティブ PCG ノードクラスを一覧 |
| `Toolset.Editor.PCG.ListAvailableSubgraphs` 🧩 | サブグラフとして利用可能な PCG アセットを一覧 |
| `Toolset.Editor.PCG.GetNativeNodeSchema` 🧩 | ネイティブノードクラスのパラメータスキーマを取得 |
| `Toolset.Editor.PCG.AddNode` 🧩 | ネイティブノードを追加（`PCGGraphEdit` + `PCGToolsetUnsafeNodeAdd` 必須；Allowlist バイパス） |
| `Toolset.Editor.PCG.AddSubgraphNode` 🧩 | サブグラフノードを追加（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.UpdateNode` 🧩 | ノードのプロパティを更新（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.SetNodeComment` 🧩 | ノードのインラインコメントを設定（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.GetNodeInfo` 🧩 | 特定ノードの情報を取得 |
| `Toolset.Editor.PCG.RepositionNode` 🧩 | グラフキャンバス上のノードを移動（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.RemoveNode` 🧩 | ノードを削除（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.GetNodeDataView` 🧩 | ノードの最終実行データビューを取得（`PCGNodeInspect` 必須） |
| `Toolset.Editor.PCG.ConnectNodePins` 🧩 | 2 つのノードピンを接続（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.DisconnectNodePins` 🧩 | ノードピンを切断（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.AddCommentBox` 🧩 | コメントボックスを追加（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.UpdateCommentBox` 🧩 | コメントボックスを更新（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.RemoveCommentBox` 🧩 | コメントボックスを削除（`PCGGraphEdit` 必須） |
| `Toolset.Editor.PCG.RunPCGInstantGraph` 🧩 | `UPCGSpatialToolset` 経由で PCG グラフを即時実行（`PCGGraphExecute` 必須；非同期・デフォルト 300 秒） |
| `Toolset.Editor.PCG.DrawSpline` 🧩 | `UAIP.Editor.PCG.DrawPCGSpline` のブリッジ版。`UPCGToolset::DrawSpline` に委譲する（Experimental）。Admission ルールと Capability ゲートはネイティブ版と同じだが、登録する待機時間は Toolset ディスパッチ自体の上限により 600 秒でクランプされる（ネイティブ版のデフォルト 1800 秒とは異なる） |

---

## UAIP.Editor.WorldConditions 🧩

WorldConditions 編集。`WorldConditions` プラグインが必要です。

| コマンド | 説明 |
|---|---|
| `GetWorldConditionInfo` 🧩 | 条件セット構造（Operator / Depth / プロパティ）。各プロパティエントリに `WriteRequirements` オブジェクトが入れ子で付きます。`RequiredCapabilities` は常に空です — この経路は参照もコンテナも一切受け付けないため、付与して解禁できる Capability が存在しません。各条件も自身の型について `Admission` / `RequiredCapabilities` / `MissingCapabilities` を報告するようになりました。下の Note を参照してください |
| `AddWorldCondition` 🧩 | 条件を追加（`InsertAtIndex=-1` で末尾追加）— このドメインが出荷していないモジュール由来の型には Capability が要ります。下の Note を参照してください |
| `RemoveWorldCondition` 🧩 | インデックス指定で条件を削除 — 削除される条件の型が要求する Capability が同じく必要です |
| `SetWorldConditionProperty` 🧩 | 条件 USTRUCT のプロパティを設定（ImportText 値文字列）— 書き込み対象の条件の型と、そのプロパティを宣言している型の**両方**が要求する Capability が必要です |
| `SetWorldConditionOperator` 🧩 | Operator（And / Or）と bInvert を設定（Index 0 は Copy 固定）— その条件自身の型が要求する Capability が同じく必要です |
| `SetWorldConditionExpressionDepth` 🧩 | ExpressionDepth（0–4）を設定 — 確認内容は上と同じ |
| `ListWorldConditionClasses` 🧩 | `FWorldConditionBase` 派生クラス一覧 — 有効な `ConditionClass` 値の探索に使う。各エントリは `AddWorldCondition` と同じ policy から得た `Admission`（`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`）と `RequiredCapabilities` / `MissingCapabilities` を併記するようになりました。このドメインが出荷しているモジュールでの絞り込みは廃止しています。フルパス（`/Script/<Module>.<Class>`）昇順で並び、`TotalCount` / `ReturnedCount` / `Truncated`（上限 200 件）を報告します |
| `ValidateWorldConditionQuery` 🧩 | クエリに対して `Initialize()` + `IsValid()` を実行し `{IsValid, Errors}` を返す（PIE 中も可） |
| `MoveWorldCondition` 🧩 | 条件を `SourceIndex` から `TargetIndex` へ移動（インデックス 0 は固定）— 移動される条件の型が要求する Capability が同じく必要です |
| `DuplicateWorldCondition` 🧩 | `SourceIndex` の条件を複製し `InsertIndex` に挿入 — 確認内容は `AddWorldCondition` と同じ |
| `ReplaceWorldCondition` 🧩 | 条件の型を `NewConditionClass` の既定値へ差し替え（Depth・Operator・bInvert は維持）— 確認内容は `AddWorldCondition` と同じ |
| `ClearWorldConditionQuery` 🧩 | 全条件を削除して空のクエリにする — 削除される全条件が要求する Capability が必要です |
| `SetMultipleWorldConditionProperties` 🧩 | 1〜32 件のプロパティ編集を単一トランザクションで適用（全件適用か全件不適用）— 編集ごとに `SetWorldConditionProperty` と同じ確認を行います |

> **⚠️ 破壊的変更 — `SetMultipleWorldConditionProperties` の成功応答の形が変わりました。** このコマンドは全件適用か全件不適用のどちらかになりました。全編集をいったんステージングして検査し（ドメインゲート・テキストインポート・途中終了パースの検出・妥当性検証）、すべて通ったときにだけトランザクションを開いて一括コミットします。1 件でも失敗するとトップレベルの `ErrorCode` / `ErrorMessage` だけを返して何も書きません。したがって従来の編集ごとの `Results[]` と `AllSucceeded` は表すものが無くなりました。成功応答は `AppliedEdits`（実際にコミットされた `{ConditionIndex, SubPropertyName}` の配列）と `SkippedEdits`（プロパティ名が一致せず飛ばされた同形の配列。名前の不一致は従来どおりバッチを失敗させません）になります。`Results[]` / `AllSucceeded` を読んでいる呼び出し側は修正が必要です。
>
> **Note — このドメインは条件の型を 1 か所で受理しており、Capability は 1 つ（`WorldConditionsCustomTypeEdit`）だけです。** 配置・差し替え・操作される条件の型と、書き込まれるプロパティを宣言している型は同じ扱いを受け、1 つの名前を共有します — プロジェクト製の条件は自分のプロパティを自分で宣言するため、プロパティ面に別の許可を求める理由がありません。型が `/Script/WorldConditions` の外から来た場合に必要です。プロジェクトのモジュール、プラグインのモジュール（`SmartObjects` のようなエンジンプラグインを含む）、Blueprint 生成の型はいずれも外側になります。既定では付与されません。[安全性と Capability](safety.md#オプショングラフエディタ) を参照してください。
>
> **既にアセットに置かれているプロパティへの書き込みにも Capability が要るようになりました — これは移行ではなく新設です。** この Capability が存在する前は、`SetWorldConditionProperty` / `SetMultipleWorldConditionProperties` は書き込みフラグと値種別だけを確認しており、プロジェクト製の条件が持つプロパティは宣言型に対する Capability 確認なしに書き込めていました。宣言型が `/Script/WorldConditions` 自身でない場合、これらは今後 `WorldConditionsCustomTypeEdit` も要求します。
>
> **追加だけでなく、削除・移動・複製もゲートされます。** `RemoveWorldCondition` / `ClearWorldConditionQuery` / `MoveWorldCondition` / `DuplicateWorldCondition` / `SetWorldConditionOperator` / `SetWorldConditionExpressionDepth` は従来、対象条件の型にかかわらずアセットへ到達していました。現在は操作対象の条件について同じ Capability をあらためて確認します。配置面では拒否される型（例えばインスタンス化できない型）であっても、既に置かれているものの削除・移動は Capability さえ保有していれば引き続き可能です — 完全に拒否されたままなのは、そもそもインスタンス化できない型を新たに配置しようとする経路だけです。
>
> **エンジン側の確認も行われますが、Capability を要求した型についてのみ、かつセッションがそれを保有した後にだけ行われます。** `AddWorldCondition` と `DuplicateWorldCondition` は Capability 確認を通過した後、クエリ定義自身のスキーマ（`UWorldConditionSchema::IsStructAllowed`）にも確認します — スキーマがその型を拒否すれば、Capability を保有していても `PolicyViolation` で拒否されます。`ReplaceWorldCondition` はこの段階に到達しません — アセット（とそのスキーマ）を解決する前に `NewConditionClass` を検証するため、そこで受理された型は Capability の確認だけで判定されます。スキーマを持たないクエリ定義はどちらの経路でも影響を受けません。
>
> ⚠️ **破壊的変更**: このドメイン自身のモジュール外の型は従来、無条件に `PolicyViolation` で拒否されていました。`AddWorldCondition` / `ReplaceWorldCondition` / `SetWorldConditionProperty` / `SetMultipleWorldConditionProperties` は `CapabilityNotAvailable` を返して不足している Capability を名指しするようになり、実際にその Capability を付与すれば成功するようになりました（旧実装はこれができませんでした）。現在ロードされている中に該当が無いクラスパスは `NotFound` です — このドメインはもともと未解決クラスをロードへフォールバックしていなかったため、この点に変化はありません。
>
> **Note — `ListWorldConditionClasses` はゲートされた型を隠さなくなりました。** 従来は基底型とモジュール所属だけでクラスを絞り込んでおり、`/Script/WorldConditions` 以外の型をすべてレスポンスから黙って除外していました。現在は `AddWorldCondition` と同じ policy から答え、エントリごとに `Admission` を報告します — 除外されるのは `FWorldConditionBase` の派生ではない型、または名前解決に失敗した型だけです。一覧はスナップショットであって認可ではありません — 一覧取得から mutation までの間に Capability や role は変わりうるため、各コマンドは自身のリクエストで判定をやり直します。
>
> **`GetWorldConditionInfo` はもともとクラス名を伏せ字にしておらず、現在も同様です** — このコマンドが行う唯一の伏せ字化は `FWorldConditionContextDataRef` プロパティの値に対するもので、条件がどの型のインスタンスかとは無関係です。現在は各条件について、`SetWorldConditionProperty` / `RemoveWorldCondition` が問うのと同じ問いに対する `Admission` / `RequiredCapabilities` / `MissingCapabilities` も追加で報告します。

### Toolset ブリッジ — WorldConditions（2 件）🧩

`WorldConditionTools`（UE 5.8+、Experimental）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.WorldConditions.*`。入力 JSON は 64 KiB 上限です。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.WorldConditions.GetQueryDescription` | `FWorldConditionQueryDefinition` の人間可読な説明 |
| `Toolset.Editor.WorldConditions.GetConditionDescription` | 単一条件型の人間可読な説明 |

---

## UAIP.Editor.Conversation 🧩

ConversationDB グラフ編集。`CommonConversation` プラグインが必要です。

| コマンド | 説明 |
|---|---|
| `ListConversationNodeTypes` 🧩 | 位置別（`TopLevel` / `SubNode`、省略時は両方）のノードクラス一覧。各エントリは `Admission`（`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`）と、下記の mutation コマンドが検証するのと同じ policy に基づく `RequiredCapabilities` / `MissingCapabilities` を持つ。`/Script/CommonConversationRuntime` 以外へのフィルタは廃止 — プロジェクト・プラグイン製や Blueprint 製のクラスも `Admission: RequiresCapabilities` として一覧から省略されずに説明される。`ClassPath` 昇順。`TotalCount` / `ReturnedCount` / `Truncated` を返す（位置ごと最大 256 件）— 下記 Note を参照 |
| `AddConversationNode` 🧩 | トップレベルノードを追加（`UConversationNodeWithLinks` 派生）。`NodeClass` が `/Script/CommonConversationRuntime` の外から来る場合、`ConversationGraphEdit` に加えて `ConversationCustomTypeEdit` が必要 — [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照 |
| `AddConversationSubNode` 🧩 | 親 Task ノードに SubNode を附加。`NodeClass` が `/Script/CommonConversationRuntime` の外から来る場合、追加で `ConversationCustomTypeEdit` が必要 |
| `RemoveConversationNode` 🧩 | NodeGuid 指定でノードを削除。削除するノードのクラスが `/Script/CommonConversationRuntime` の外から来る場合 `ConversationCustomTypeEdit` が必要 — トップレベルノードの削除は、一緒に削除される全 SubNode についても同じ確認を行う |
| `ConnectConversationNodes` 🧩 | ノード間の遷移エッジを追加。両端いずれかのクラスが `/Script/CommonConversationRuntime` の外から来る場合 `ConversationCustomTypeEdit` が必要 |
| `DisconnectConversationNodes` 🧩 | 遷移エッジを削除。両端いずれかのクラスが `/Script/CommonConversationRuntime` の外から来る場合 `ConversationCustomTypeEdit` が必要 |
| `SetConversationNodeProperty` 🧩 | プロパティを設定（FText は BIDI strip・PUA reject・4096 文字上限）。値は JSON ドキュメント。参照・構造体・コンテナは恒久的に拒否されなくなり、`PropertyReferenceEdit` / `PropertyStructuredEdit` で制御される — [参照・構造体・コンテナの書き込み](#参照構造体コンテナの書き込み) を参照。対象ノードのクラスが `/Script/CommonConversationRuntime` の外から来る場合、追加で `ConversationCustomTypeEdit` が必要 |

> ⚠️ **破壊的変更 — 削除・接続・切断・プロパティ編集は以前ゲートされていませんでした。** この Capability が導入される前は `AddConversationNode` / `AddConversationSubNode` だけが追加するノードクラスを確認しており、残り 4 つの mutation コマンドは対象ノードのクラスにかかわらず無条件で実行されていました。一般則については [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照してください。すべての mutation はデータベースのコンパイル済みバンクも再構築しますが、これはデータベースが既に保持している全ノードクラスに対しても同じ確認を行います — プロジェクト製のノードを既に含むデータベースは、コンパイルも既存ノードの削除も、Capability の付与なしに引き続き行えます。既存インスタンスへの操作はリクエストが持ち込んだコードを一切実行しないためです。

> **Blueprint で作った Task ノードや SubNode は恒久的な拒否ではなくなりました。** この Capability が導入される前は、標準グラフエディタの「Add Node」メニューがネイティブクラスと並べて提示する `UConversationTaskNode` / `UConversationRequirementNode` / `UConversationSideEffectNode` / `UConversationChoiceNode` の Blueprint 派生サブクラスであっても、`AddConversationNode` / `AddConversationSubNode` は常に拒否しており、付与によって解禁する手段がありませんでした。現在はプロジェクト・プラグイン製クラスと同じ扱いで判定され、セッションが `ConversationCustomTypeEdit` を保有していれば追加できます。

> ⚠️ **変更 — `ListConversationNodeTypes` は `NodeTypesTruncated` を返さなくなりました。** 上限を超えたかどうかは、キャップ付きの UAIP 一覧が共通して返す `Truncated` フィールド（`TotalCount` / `ReturnedCount` と併記）で報告されます。従来の `NodeTypesTruncated` を読んでいた呼び出し元は、その値が存在しなくなります。

### Toolset ブリッジ — Conversation（5 件）🧩

`ConversationToolset`（UE 5.8+）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.Conversation.*`。観測専用で、編集は上記のネイティブコマンドが担当します。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.Conversation.ListConversationEntryPoints` | `UConversationDatabase` のエントリポイントノード一覧 |
| `Toolset.Editor.Conversation.ListConversationSpeakers` | `UConversationDatabase` に定義された話者一覧 |
| `Toolset.Editor.Conversation.ListConversationNodes` | 全ノード一覧（以下 2 コマンドで使う refPath 付き） |
| `Toolset.Editor.Conversation.GetConversationNodeConnections` | `NodeRefPath` で指定したノードの接続グラフ |
| `Toolset.Editor.Conversation.ListConversationNodeSubNodes` | ノードの SubNode（選択肢・要求・副作用）一覧 |

---

## UAIP.Editor.ControlRig

ControlRig ヒエラルキーと RigVM グラフ編集。

#### Control Rig アセットの形式

UE 5.8 の Control Rig アセットには 2 つの形式があります。ここのネイティブコマンドはどちらも同じパラメーターで受け付けます（Undo / Redo、ダーティ印、ModularRig の保護も同じように働きます）。

| 形式 | クラスパス | 備考 |
|---|---|---|
| ランタイムアセット（UE 5.8 の既定） | `/Script/ControlRig.ControlRigRuntimeAsset` | UE 5.7 には存在しない |
| 旧形式（Blueprint） | `/Script/ControlRigDeveloper.ControlRigBlueprint` | |

新規アセットがどちらの形式になるかは、プロジェクトのコンソール変数 `RigVM.BlueprintIndependentAssets` で決まります（UE 5.8 の既定は有効。プロジェクトの `DefaultEngine.ini` の `[ConsoleVariables]` に `RigVM.BlueprintIndependentAssets=0` を置くと旧形式になります）。この変数はエディタの作成メニューを含むプロジェクト全体に効き、UAIP が変更することはありません。

- **`CreateAsset` は設定に従います。** クラスパスは設定と一致している必要があります。プロジェクトがランタイムアセットを作る設定なのに旧形式のクラスを指定した場合（逆の場合も）は `InvalidParams` で断り、何も作らず、正しいクラスと変更すべき変数をメッセージで案内します。`ControlRigBlueprintCreate` Capability が無い場合はそちらが先に、`AssetPath` に既にアセットがある場合は Factory の指定の誤りより先に報告されます。プロジェクトが旧形式の設定なら、旧形式のクラスに `FactoryClassName` は不要です。
- **以前のドキュメントにあったクラスパス `/Script/ControlRig.ControlRigBlueprint` は誤りでした。** UE 5.8 では解決できず「class could not be resolved」になります。上の 2 つのパスのどちらかを使ってください。
- **応答に出るアセットのパス**は常にアセット本体（`/Game/X.X`）です。ランタイムアセットの内部の部品のパス（`/Game/X.X:X_EditorOnly`）は、これらのネイティブコマンドでは入力として受け付けられ、応答にはアセット本体のパスが返ります。
- **`AddVariable` は実際に付いた名前を返し**、リグを再コンパイルし、初期値を保存して開き直しても保持します。ランタイムアセットの Control Rig では `IsReadOnly` は受け付けられますが効きません。エンジンが反映せず、変数は読み書きできるままです。
- **`Toolset.Editor.ControlRig.*` はランタイムアセット形式を断ります。** 委譲する前に `UnsupportedOperation` で断り、同じことができる `UAIP.Editor.ControlRig.*` のコマンド名（無い場合はこのドメイン）を案内します。この判定は ModularRig の保護より先です。旧形式のアセットと読めなかったアセットは、今までどおり Toolset に任せます。`Toolset.Editor.ControlRig.Create` はプロジェクトの設定にかかわらず常に**旧形式**で作成し、作成先に既存アセットがある場合の扱いも今までどおりです。
- **`ClassName=/Script/Engine.Blueprint` で Control Rig の `FactoryParams.ParentClass` を渡した `CreateAsset` は断られます。** 何も作る前に `InvalidParams` になります（親は `UControlRig` かその派生: Modular Rig、プロジェクト定義の派生、Control Rig の生成クラス）。汎用の Blueprint Factory は、Control Rig のアセットではなくそのクラスを親にした普通の Blueprint を、`ControlRigBlueprintCreate` Capability を調べずに作ってしまい、Control Rig のコマンドでは編集できません。メッセージは `ClassName` に指定するクラス（プロジェクトが作る形式に応じてランタイムアセットか旧形式のクラス）を挙げ、親クラスは `FactoryParams.ParentClass` に残すよう案内します（例: `/Script/ControlRig.ModularRig`）。Capability の不足、`AssetPath` の使用中、`FactoryClassName` の誤りは、これより先に報告されます。
- UE 5.7 には旧形式しかありません。ランタイムアセットのクラスを指定すると `InvalidParams`（「class could not be resolved」）になります。

#### 変数の型・名前と、エディタに届く前の検証

`AddVariable` と `ChangeVariableType`（ネイティブも Toolset ブリッジも）は、変数の型をエディタの変数型メニューで選べるものに限ります。また、Control Rig のコマンドに渡される名前は、エンジンに届く前に長さの上限で検査されます。どちらもアセットを開く前に確かめるので、拒否されたときにアセットは変わりません。

- ⚠️ **型は基本型名か完全なパスで書き、それ以外は受け付けません。** 基本型名は `bool` / `int32` / `float` / `double` / `FName` / `FString`（大文字小文字を区別）で、ほかは `/Script/CoreUObject.Vector` のような完全なオブジェクトパスです。配列は、そのどちらかを 1 段の `TArray<...>` で包みます。短い名前（`Vector`）、C++ の書き方（`FVector` / `TObjectPtr<AActor>` / `TSubclassOf<AActor>` / `EMyEnum`）、引用付きの書き方（`Class'/Script/Engine.Actor'`）、入れ子の配列、閉じていない `TArray<` は `InvalidParams` で拒否されます。クラスのパスは、そのクラスのオブジェクトへの参照を意味します。読み込み済みの型に解決できない完全なパスも `InvalidParams` です。型を含むアセットやモジュールを読み込んでから再実行してください。型の指定が 1023 文字を超える場合も拒否されます。
- ⚠️ **変数型メニューで選べない型は `InvalidParams` で拒否され、権限を付けても解除されません。** 例: テキスト型（`FText`）、メニューに無い 64 ビット整数などの整数型、素のバイト型、ワイルドカード、Blueprint で使えない構造体・列挙型・クラス、実行ピン系の構造体、（エディタがオブジェクトを扱わない設定のときの）オブジェクト型。マップ・セットの型は `UnsupportedOperation` です。
- ⚠️ **拒否の優先順が変わりました。** 型の判定はアセットを開く前に行われるため、存在しないアセット（`AddVariable` では、既にある名前も）に不正な型を指定すると、`NotFound` や重複ではなく型の拒否が返ります。UE 5.7 で存在しないパスのオブジェクト型を指定した場合は、`UnsupportedOperation` ではなく `InvalidParams`（型が見つからない）になります。UE 5.8 では、**インターフェース**のクラスパスは `InvalidParams` で拒否されます（以前は、インターフェースとして働かない変数が作られていました）。
- ⚠️ **名前に長さの上限があります。** グラフ名・要素名・コンポーネント名・変数名・イベント名などの名前は、1023 文字を超えると `InvalidParams` で拒否されます。新しく作るグラフの名前は 1012 文字まで、ノード名とコントロール名は従来どおり 128 文字までです。メッセージにはフィールドと上限が示されます。Toolset ブリッジのコマンドにも同じ上限が掛かります。
- ⚠️ **ピン系のコマンドは、より長いアセットパスを受け付けます。** 257〜512 文字の `AssetPath` を誤って拒否していたピン系の 7 コマンドが、512 文字まで受け付けるようになりました。
- **Toolset ブリッジの `AddVariable` は、既にある名前を `InvalidParams` で拒否します。** 委譲の前に判定されます（`UAIP.Editor.ControlRig.AddVariable` と同じです）。
- ⚠️ **Toolset ブリッジの `ChangeVariableType` が扱えるのは、基本型・構造体とその配列です。** それ以外の型（列挙型・オブジェクト型・クラス）への変更と、ノードから参照されている変数の変更（エディタが確認を求める状況）は `UnsupportedOperation` で拒否され、代わりに使うネイティブの `UAIP.Editor.ControlRig.ChangeVariableType` が案内されます。両方のブリッジのパラメータ説明には、通る型の例（`/Script/CoreUObject.Vector`、`float`、`TArray<FString>`）が示されます。
- ⚠️ **権限が要る初期値や新しい型は、何かを変更する前に権限が確かめられます。** ブリッジでも、参照を含む型の初期値には `PropertyReferenceEdit` が要り、参照先のアセットはロードされません。`ChangeVariableType`（ネイティブもブリッジも）は、変数に値があるかどうかにかかわらず、新しい型の書き込み権限を判定します。参照を含む型への変更には `PropertyReferenceEdit` が、配列の型と、`Vector` などの組み込みの構造体ではない構造体への変更には `PropertyStructuredEdit` が要ります（無ければ `CapabilityNotAvailable`）。基本型と組み込みの構造体には、どちらも要りません。拒否されたときにアセットは変わりません。
- **旧形式の Control Rig の `ChangeVariableType` で、列挙型・オブジェクト型へ変えられるようになりました。** 以前は、エディタが落ちるか、型が壊れたまま成功が返っていました。エディタの確認ダイアログでコマンドが止まることはなくなり、応答には常に `RebuiltReferencingNodeCount`（その変数を参照していて作り直したノードの数。0 件でも載ります）が含まれます。UE 5.7 のオブジェクト型は、`AddVariable` と同じく `UnsupportedOperation` です。 ⚠️ ランタイムアセットの Control Rig では、変数の既存の初期値は、新しい型で読めればそのまま保たれ（float の 2.5 を double に変える場合など）、読めない場合や一部しか読めない場合（テキスト `not a vector` を Vector に変える場合など）は捨てられて、変数は新しい型の初期値から始まります。どちらの場合も型の変更は成立します。`Result` と artifact に `DefaultValueDiscarded` が載ります（値を捨てたときは `true`、読めた・元から空・旧形式のときは `false`）。載るのは `RebuiltReferencingNodeCount` と同じ応答（成功と、型が要求と違った失敗）です。
- **型の変更・追加が成立しなかったときは失敗として返ります。** ネイティブの `ChangeVariableType` と、Toolset ブリッジの `AddVariable` / `ChangeVariableType` は、実行後に変数を読み直して確かめます。変数が消えている、または要求と違う型になっているときは `ExecutionFailed` で、`Result` に `VariableLost` と `ActualType`（変数の実際の型）が載ります。ネイティブは artifact にも同じ項目を載せ、ブリッジも同じ形で応答します。変更は自動では元に戻されず、エディタの元に戻す履歴に残ります。ランタイムアセットの Control Rig で、エンジンが型を引き直すときにアセットの読み込みが要る型（ユーザー定義の列挙型など）への変更は、何も変更せず `UnsupportedOperation` で拒否されます（以前は変数が消えたまま成功が返っていました）。同じ短い名前の別の型がある型への変更も同様です。
- **Toolset ブリッジの `AddVariable` で、エンジンが別の名前を付けた場合は確かめられません。** 委譲先が実際の名前を返さないため、「要求した名前の変数が見つからない」という `ExecutionFailed` になり、作られた変数がどれかは示されません。

### ネイティブ（68）

#### ヒエラルキー観測（10）

| コマンド | 説明 |
|---|---|
| `GetElements` | ヒエラルキー全要素一覧 |
| `GetAllBones` | 全ボーン一覧 |
| `GetAllNulls` | 全 Null 要素一覧 |
| `GetAllControls` | 全 Control 要素一覧 |
| `GetGlobalTransform` | 要素のグローバルトランスフォーム |
| `GetLocalTransform` | 要素のローカルトランスフォーム |
| `GetParent` | 要素の親要素 |
| `GetChildren` | 要素の子要素一覧 |
| `GetModuleInstances` | ModularRig のモジュールインスタンス一覧 |
| `GetControlSettings` | Control の `FRigControlSettings`（Gizmo・Limits） |

#### ヒエラルキー編集（11）

| コマンド | 説明 |
|---|---|
| `AddElement` | 汎用要素を追加（ElementType 指定） |
| `AddBone` | ボーンを追加 |
| `AddNull` | Null 要素を追加 |
| `AddControl` | Control 要素を追加（ControlType allowlist） |
| `RemoveElement` | 要素を削除 |
| `RemoveBone` | ボーンを削除 |
| `RemoveNull` | Null 要素を削除 |
| `RemoveControl` | Control 要素を削除 |
| `ReparentElement` | 要素の親を変更（MaintainGlobalTransform オプション） |
| `SetControlOffset` | Control の Initial ローカル変換を設定 |
| `SetControlSettings` | Control の `FRigControlSettings` を設定 |

#### トランスフォーム（3）

| コマンド | 説明 |
|---|---|
| `SetGlobalTransform` | 要素のグローバルトランスフォームを設定 |
| `SetLocalTransform` | 要素のローカルトランスフォームを設定 |
| `ImportBonesFromAsset` | SkeletalMesh / Skeleton アセットからボーン階層をインポート |

#### グラフ管理（11）

| コマンド | 説明 |
|---|---|
| `ListGraphs` | 全 RigVM グラフ一覧 |
| `GetGraph` | 指定グラフ情報 |
| `AddGraph` | カスタムグラフを追加 |
| `DeleteGraph` | カスタムグラフを削除（組み込みグラフは拒否） |
| `GetForwardSolveGraph` | ForwardSolve グラフを取得 |
| `GetBackwardSolveGraph` | BackwardSolve グラフを取得 |
| `GetInteractionGraph` | Interaction グラフを取得 |
| `GetEventGraph` | 指定イベントのグラフを取得 |
| `AddEventGraph` | イベントグラフを追加 |
| `AddBackwardSolveGraph` | BackwardSolve グラフを追加 |
| `AddInteractionGraph` | Interaction グラフを追加 |

#### ノード（10）

| コマンド | 説明 |
|---|---|
| `AddGraphNode` | RigVM グラフにノードを追加（StructPath + SolveEventName） |
| `RemoveGraphNode` | NodeName 指定でノードを削除 |
| `ListNodes` | グラフのノード一覧 |
| `GetNodeInfo` | ノードの StructPath・ピン型・メタデータ |
| `FindNodes` | StructPath / NamePattern 指定でノードを検索 |
| `GetNodePosition` | ノードのグラフ上の位置 |
| `SetNodePosition` | ノードの位置を設定 |
| `DuplicateNode` | ノードを複製（複製後の名前を返す） |
| `AddEventNode` | イベントノードを追加 |
| `AddVariableNode` | 変数ノードを追加 |

#### ピン（7）

| コマンド | 説明 |
|---|---|
| `ListPins` | ノードのピン一覧 |
| `GetPinValue` | ピンの値を取得 |
| `SetPinValue` | ピンの値を設定 |
| `ResetPinValue` | ピン値をデフォルトに戻す |
| `GetConnectedPins` | ピンの接続情報 |
| `ConnectControlRigPins` | RigVM グラフのピンを接続 |
| `DisconnectControlRigPins` | ピン接続を切断 |

> **修正 — グラフが見つからない場合とアセットが読めない場合が、別のエラーコードで返るようになった。** `GraphName` でモデルを解決する以下のコマンド（`GetGraph` / `AddGraph` / `DeleteGraph` / `AddGraphNode` / `AddEventNode` / `AddVariableNode` / `FindNodes` / `GetConnectedPins` / `GetNodeInfo` / `GetNodePosition` / `GetPinValue` / `ListNodes` / `ListPins` / `SetNodePosition` / `SetPinValue` / `ResetPinValue` / `DuplicateNode`）は従来、`GraphName` がどのモデルにも一致しない場合と、対象アセット自身の ControlRigBlueprint 参照そのものが無効な場合の両方で、同じ `ExecutionFailed`「Graph is null.」を返していた — コード上には「見つかりません」用の専用応答が用意されていたが、内部では両方の状況が同じ結果として報告されていたため、実際には一度も返っていなかった。現在はこの 2 つを区別する: アセット自体は正しく読み込めているのに `GraphName` がどのモデルにも一致しない場合は `NotFound`、アセット自身の ControlRigBlueprint が読めない場合は引き続き `ExecutionFailed` を返す。呼び出し側は「別の `GraphName` を試す価値があるか」と「アセット自体が読み込めるまで再試行しても無駄か」を区別できるようになった。
>
> ⚠️ **破壊的変更 — `GraphName` の部分一致は日常的に起こりうるものであり、アセットを変更するコマンドは複数一致時にいずれか 1 つを選ぶのではなく断るようになった。** `GraphName` は先頭一致（プレフィックス）を受け付ける — 短い名前を渡すと、それで始まる完全なモデル名を持つグラフに一致する。これは意図して用意された省略記法であり、まれな例外ではない。この方式で複数のモデルに一致した場合、従来はどのコマンドでも黙っていずれか 1 つが選ばれていた。読み取り専用の 8 コマンド — `FindNodes` / `GetConnectedPins` / `GetGraph` / `GetNodeInfo` / `GetNodePosition` / `GetPinValue` / `ListNodes` / `ListPins` — は引き続きこの挙動のままで、複数一致でもいずれか 1 つを選んで実行する（誤ったグラフを読んでも修正すべき副作用が無いため）。一方、アセットを変更する 7 コマンド — `AddEventNode` / `AddVariableNode` / `DeleteGraph` / `DuplicateNode` / `ResetPinValue` / `SetNodePosition` / `SetPinValue` — は、`GraphName` が複数のモデルに一致した場合、**何も変更せず** `InvalidParams` を返し、`Result.MatchedFullGraphNames` に各候補の完全なモデル名を一覧で返すようになった。返された完全な名前のいずれかを `GraphName` として渡し直せば、1 つのグラフに絞り込める — この解決のために新しいパラメータは追加されていない（Blueprint / AnimBlueprint が使う `GraphGuid` / `MatchedGraphGuids` の仕組みとは異なり、ControlRig にはもともと省略記法から導ける曖昧さのない完全な名前があるため）。

#### 変数（5）

| コマンド | 説明 |
|---|---|
| `AddVariable` | RigVM 変数を追加。デフォルト値は変数の型が確定してから検証され、拒否された場合は **変数の追加ごと取り消されます**（`AddBlueprintVariable` と同じ扱い）。デフォルト値はエンジンのテキスト形式のみを受け取るため、参照・コンテナのデフォルトは追加後に `SetBlueprintDefault` で設定してください。拒否された呼び出しはアセットを dirty にしません。変数が実際に受け取った名前（エンジンがスペースを含む名前などを整えることがあります）を返し、リグを再コンパイルします。UE 5.8 のランタイムアセットの Control Rig では `IsReadOnly` は受け付けられますが効かず、変数は読み書きできるままです |
| `ListVariables` | RigVM 変数一覧 |
| `GetVariable` | RigVM 変数の値 |
| `ChangeVariableType` | RigVM 変数の型を変更 |
| `RemoveVariable` | RigVM 変数を削除 |

#### リグヒエラルキーコンポーネント（9）

ヒエラルキー要素に取り付けられたコンポーネント（`FRigBaseComponent` 派生構造体）を扱う汎用コマンド群です。モジュール allowlist が許可するすべてのコンポーネント型に対して動作し、後述の 2 ドメインが型ごとの専用コマンドを提供する ControlRigDynamics / ControlRigPhysics の型も含みます。コンポーネントは `ElementName` と `ElementType`（`Bone` / `Null` / `Control`。`All` は不可）と `ComponentName` の組で指定します。読み取り 4 コマンドは `EditorInspect` を、書き込み 5 コマンドは `ControlRigComponentEdit`（既定無効）を要求し、PIE 実行中は拒否されます。

| コマンド | 説明 |
|---|---|
| `ListComponents` | 1 要素のコンポーネント一覧。`ElementName` と `ElementType` をどちらも省略するとヒエラルキー全体を列挙する。各エントリは所属要素・型パス・`IsProcedural` を持ち、レスポンスは `TotalCount` / `ReturnedCount` / `Truncated` を返す |
| `GetComponent` | 1 コンポーネントの型と内容。`ContentText`（エンジンのエクスポート形式）は常に返る。`Content`（JSON）は JSON で表現できない型の場合に明示的な `null` と `ContentConversion` 理由になり、変換不能なコンポーネントが空のものと取り違えられることはない |
| `ListAddableComponentTypes` | エディタが知る `FRigBaseComponent` 派生構造体をすべて列挙する（対象ヒエラルキーにコンポーネントが 1 つも無くても列挙できる）。各エントリは `AddComponent` が検証するのと同じポリシー由来の `Admission`（`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`）と `RequiredCapabilities` / `MissingCapabilities` を持ち、レスポンスは `TotalCount` / `ReturnedCount` / `Truncated` を返す — 詳細は下記の Note を参照 |
| `CanAddComponent` | ある型をある要素に取り付けられるかどうかを、実際に取り付けずに判定する。上記一覧と同じ `Admission` と `RequiredCapabilities` / `MissingCapabilities` を返し、**このセッションが既にその型を扱える場合に限り**エンジンにも問い合わせて `CanAdd` / `FailureReason` にその答えを返す — 詳細は下記の Note を参照 |
| `AddComponent` | 新しいコンポーネントを取り付ける。初期内容は任意で、`Content`（JSON）**または** `ContentText`（エクスポート形式）のどちらか一方のみ。作成前に内容を完全に検証するため、拒否された要求はコンポーネントを残さない |
| `RemoveComponent` | コンポーネントを削除する。そのキーを保持する他コンポーネントの扱いは `ReferenceHandling` が決める（`Reject`＝既定 / `Detach` / `Force`）。見つかった参照はすべて `References` に、どう扱われたかとともに返る |
| `RenameComponent` | コンポーネントを `NewName` へ改名し、そのコンポーネントを指していた参照を張り替える |
| `ReparentComponent` | `NewParentName` と `NewParentType` が指す要素へコンポーネントを付け替え、参照を張り替える。存在しない付け替え先は、何も変更する前に拒否される |
| `SetComponentContent` | コンポーネントの内容を置き換える（`Content` **または** `ContentText` のどちらか一方が必須）。書き込み後に読み戻し、実際に書き込まれた内容を返す |

> **⚠️ 変更 — `ListAddableComponentTypes` と `CanAddComponent` は単純な `Addable` フラグではなく `Admission` を返すようになりました**: 各エントリは `Admission` を持ち、4 つの値のいずれかになります — `Allowed`（現在のセッションで今すぐ使える）、`RequiresCapabilities`（`MissingCapabilities` に挙がる Capability を付与すれば使える。`MissingCapabilities` は `RequiredCapabilities` の部分集合）、`NotAddable`（基底型違い・`Deprecated`・`Hidden` など、Capability をどれだけ付与しても解消しない構造的な理由で拒否される）、`CompatibilityUnknownUntilAuthorized`（セッションはこの構造体に対する `ControlRigCustomTypeEdit` を既に保有しているが、エンジン側の互換性チェックはまだ実行されていない — 詳細は [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照）。あわせて `RequiredCapabilities` / `MissingCapabilities` を返します。`CanAddComponent` はさらにエンジン（`URigHierarchy::CanAddComponent`）にも問い合わせますが、**`Admission` が `Allowed` または `CompatibilityUnknownUntilAuthorized` の型に限られます** — `NotAddable` または `RequiresCapabilities` の型はエンジンに一切触れずに回答されるため、Capability を持たないセッションがその型自身のコードを走らせることはありません。エンジンの回答は `Admission` を上書きせず、`CanAdd` / `FailureReason` に入ります。両者は併せて読めます（`Admission: CompatibilityUnknownUntilAuthorized` かつ `CanAdd: false` は、セッションは認可されているがエンジンがこの組み合わせを拒否した、という意味になります）。⚠️ **破壊的変更 — この 2 コマンドが返していた bool の `Addable` と文字列の `NotAddableReason` は無くなりました**。どちらかで分岐していた呼び出し元は `Admission` に切り替える必要があります。形式不正な `ComponentStructPath` は、`CanAddComponent` では `CanAdd: false` のレスポンスではなく `InvalidParams` になりました（`AddComponent` と同じ扱いです）。
>
> **Note — 指定した名前がそのまま付くとは限りません**: `AddComponent`・`RenameComponent`・`ReparentComponent` は名前の衝突で失敗しません。エンジンが空いている名前を割り当て、結果には**実際に付いたキー**が返ります（`RenameComponent` / `ReparentComponent` は `NameChanged` も返します）。以降はその返されたキーを使ってください。今と同じ名前への改名、今ぶら下がっている要素への付け替えは、成功して何も変わりません。
>
> **Note — 書き込まれなかったプロパティは「一覧化」されるのであって「既定値に戻る」のではありません**: オブジェクト参照・デリゲート・実行時専用の状態は外部から書き込みません。`AddComponent`・`SetComponentContent`、および後述 2 ドメインの型付き `Set*` コマンドはそれらを `FilteredProperties` として返し、各項目は**いまの値のまま**残ります。
>
> **Note — `ReferenceWarnings` が空でも「何も壊れていない」とは限りません**: `Detach` または `Force` を指定した `RemoveComponent` は、片端が解決できなくなったコンポーネントを `ReferenceWarnings` として返します。この状態についてエンジンもシミュレーションも何も言わないためです — 揺れ物側では、パーティクルを失った拘束がメッセージ無しで読み飛ばされ、物理側では、ソルバーや親ボディを失ったボディ／ジョイントがエンジンの自動探索の結果へ黙って繋ぎ変わります。これらのコンポーネントはそのまま残され、代わりに削除されることはありません。このコマンドが型を知らないコンポーネントは警告の対象にできないため、`References` も併せて読んでください。`Reject` と `Detach` はそうした参照を残すくらいなら拒否します — その安全弁を外すのが `Force` です。
>
> **Note — リグが自分で作ったコンポーネントは編集できません**: `IsProcedural: true` のエントリは手で作られたものではなくリグ実行が再生成するもので、ここの書き込みコマンドはすべて拒否します。

#### その他（2）

| コマンド | 説明 |
|---|---|
| `CompileControlRig` | ControlRig をコンパイル（セッション単位 1 秒レートリミット） |
| `GetAvailableRigVMUnitStructs` | FRigUnit 派生 UScriptStruct 一覧（上限 1000 件）。各エントリは `AddGraphNode` が検証するのと同じポリシー由来の `Admission`（`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`）と `RequiredCapabilities` / `MissingCapabilities` を持つ。`SchemaVersion`（3）/ `TotalCount` / `ReturnedCount` / `Truncated` を返す |

> **⚠️ 変更 — `GetAvailableRigVMUnitStructs` の出力が `SchemaVersion: 3` になりました**: 各エントリは `Admission` を持ちます — 上記 Note の `ListAddableComponentTypes` / `CanAddComponent` と同じ 4 つの値です — あわせて `RequiredCapabilities` / `MissingCapabilities` も、`AddGraphNode` が検証するのと同じポリシー由来で返します。これは `SchemaVersion: 2` が返していた bool の `Addable` と文字列の `NotAddableReason` を置き換えるもので、どちらかで分岐していた呼び出し元は `Admission` に切り替える必要があります。`ClassPath` と `ClassDisplayName` は変わらないため、それらだけを使っていた既存の読み取りコードはそのまま動作します。レスポンスは `TotalCount`（件数上限を適用する前の総数）・`ReturnedCount`・`Truncated` も返し、`ClassPath` 昇順で列挙されるため、件数上限で打ち切られたレスポンスは毎回同じ末尾が切り落とされます。
>
> **⚠️ 破壊的変更 — `AddGraphNode` の背後にあるモジュール allowlist が完全一致になりました**: 従来は `StructPath` の所属パッケージが `/Script/ControlRig`・`/Script/AnimationCore`・`/Script/Engine` のいずれかで**始まってさえいれば**受理していました。今後は 7 モジュール（`/Script/ControlRig`、`/Script/ControlRigDynamics`、`/Script/ControlRigPhysics`、`/Script/ControlRigSpline`、`/Script/ControlRigModules`、`/Script/AnimationCore`、`/Script/Engine`）との**等価比較**になります。前方が一致していただけのパッケージ — `/Script/ControlRigDeveloper`、`/Script/ControlRigEditor`、`/Script/EngineMessages` など — は以前は受理されていましたが、今後は `ModuleNotAllowed` で拒否されます。前方一致の挙動に依存していた呼び出しは動かなくなります。回避手段はありません（この allowlist はもともとそれらのモジュールへ届くことを意図していません）。
>
> **Note — ControlRig 系の兄弟モジュールは、今回から意図して一覧に載っています**: `/Script/ControlRigDynamics`、`/Script/ControlRigPhysics`、`/Script/ControlRigSpline`、`/Script/ControlRigModules` は、従来は `/Script/ControlRig` の前方一致の副作用として偶然到達できていただけでした。今回これらを明示的に列挙したため、物理系の RigUnit 約 73 件（`FRigUnit_SpawnPhysicsSolver`、`FRigUnit_AddPhysicsBody`、`FRigUnit_AddPhysicsJoint` など）は、厳格化された規則に巻き込まれることなく引き続き追加できます。ノード用とコンポーネント用の allowlist は同じモジュール集合を対象としているため、コンポーネントとして作れる型はノードとしても置けます。

> **Note — プロジェクト定義・プラグイン定義の RigVM unit 構造体と rig ヒエラルキー component 構造体は Capability で制御されます**: このドメインが従来から受け入れてきた 7 モジュール由来の構造体を `StructPath` に指定した場合は、従来どおり使えます。それ以外のモジュール由来の構造体 — プロジェクトやプラグインが宣言したもの — は `ControlRigCustomTypeEdit` が必要になりました。対象はこのドメインが受け入れる 2 系統の型の両方です: `AddGraphNode` がグラフノードとして配置する `FRigUnit` 派生と、`AddComponent` が要素に付ける `FRigBaseComponent` 派生です。control type（`AddControl` / `SetControlSettings`）はゲートされません — control type の集合はエンジンが固定しており、プロジェクト独自の control type というものが存在しないため、Capability で守る対象がありません。
>
> Material とは異なり、このドメインには対になる「危険な型」用の Capability はありません — unit 構造体は VM がピンの値を渡して呼ぶコンパイル済み関数であり、component 構造体はヒエラルキー要素にぶら下がるデータであって、いずれも呼び出し側が書いたコードを運びません。`Deprecated` や `Hidden` が付いた構造体、および期待される基底型を継承していない構造体は、**どの Capability を持っていても**引き続き拒否されます — これらは「そもそも使えない型」であって、権限で解禁できる危険性ではありません。
>
> この確認は `AddGraphNode` と `AddComponent` だけに限りません — 一般則は [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を、このドメイン固有の内容は直下の破壊的変更を参照してください。
>
> ⚠️ **破壊的変更 — ゲートされた型の既存ノード・既存コンポーネントに対する操作も Capability を要求するようになりました。** この変更以前は、型 policy を参照していたのは `AddGraphNode` と `AddComponent` だけで、同じリグに到達する他のすべての経路は無条件に通っていました。`ControlRigCustomTypeEdit` を持たないセッションは今後、次の操作ができません: プロジェクト定義・プラグイン定義の unit 構造体を持つノードの削除（`RemoveGraphNode`）、そのピンの接続・切断（`ConnectControlRigPins` / `DisconnectControlRigPins`）、ピン既定値の書き込み・リセット（`SetPinValue` / `ResetPinValue`）、移動（`SetNodePosition`）、複製（`DuplicateNode`）、およびプロジェクト定義・プラグイン定義の構造体を持つコンポーネントの削除・改名・付け替え・内容の書き換え（`RemoveComponent` / `RenameComponent` / `ReparentComponent` / `SetComponentContent`、および下記 Dynamics / Physics ドメインの型別 `Set*` コマンドすべて）。
>
> `CompileControlRig` は**対象外**です。このドメインには危険な種類の型が存在しないため、プロジェクト定義の unit 構造体や component 構造体を含むだけのリグをコンパイルするのに追加の権限は要りません。自身では型を名指ししないグラフ操作コマンド — `AddGraph` / `DeleteGraph` / `AddEventGraph` / `AddBackwardSolveGraph` / `AddInteractionGraph` / `AddEventNode` / `AddVariableNode` — も同様です。
>
> ⚠️ **破壊的変更 — 読み込まれていない構造体は `InvalidParams` ではなく `NotFound` になりました。** `AddGraphNode` と `AddComponent` は、`StructPath` が指す構造体を副作用として読み込まなくなりました。読み込んでしまうと、その構造体を名指ししてよいかを判断するために、先にそのモジュールのコードを走らせることになるためです。まだメモリ上に無い構造体は `NotFound` として拒否され、「この問いに答えるために何も読み込まない」旨のメッセージが返ります。`StructPath` の形式が不正な場合 — 空、256 文字超、オブジェクトパスに現れない文字を含む — は引き続き `InvalidParams` です。これは型についての言明ではなく、パラメータについての言明だからです。
>
> 2 つの拒否が返る順序も変わりました。従来は構造体をアセット検索より前に判定していたため、構造体とアセットパスの両方が誤っているリクエストには構造体について回答していました。現在はアセットを手にした状態で判定します — 同じ判定がリグの既存内容も対象に取れなければならないためです — ので、そうしたリクエストにはアセットについて回答します。`StructPath` の形式検査は引き続き最初に行うため、明らかな綴り誤りは何も読み込む前に `InvalidParams` で返ります。
>
> **⚠️ アセット作成時に名指しする親クラスもゲート対象になりました。** `CreateAsset` の `FactoryParams.ParentClass`（新規 Control Rig アセットの基になる `UControlRig` サブクラス）は従来、ファクトリ自身の条件だけで受け入れられていました — 解決できること、`UControlRig` 派生であること、（Blueprint ベースのファクトリの場合）Blueprint の親クラスに使えること。現在は上記の unit 構造体・component 構造体と同じ出自判定を通り、上記 7 モジュールの外のクラスには `ControlRigCustomTypeEdit` が必要です。**エンジン同梱の親クラスはすべて従来どおり権限不要です**。いずれもその 7 モジュール内にあるためです。Capability が要るのはプロジェクト側のクラス — プロジェクトやサードパーティプラグインが宣言するネイティブの `UControlRig` 派生クラスと、プロジェクト内の Control Rig ブループリントの生成クラス（`/Game/….CR_Foo_C`）です。`ParentClass` を省略した場合は従来どおり素の `UControlRig` が作られ、何も要求されません。クラスのオンデマンド読み込みもやめました。すでにメモリ上にないクラスは、判定のためだけに読み込まれることなく拒否されます。親クラスに対する `ControlRigCustomTypeEdit` 不足は、他の経路と同じく Capability 名を挙げて `CapabilityNotAvailable` で返ります — [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照してください。構造的な拒否（未解決・基底型違い）は `InvalidParams` のままです。なお、コマンド全体を守る `ControlRigBlueprintCreate` の確認は、プロセス全体ではなく呼び出し元セッションに対して行われるようになりました。この Capability を拒む role に紐づいたセッションは、従来通っていたところで拒否されます（この拒否は従来どおり `PolicyViolation`）。

### Toolset ブリッジ（107）🧩

いずれも `AnimationAssistantToolset`（UE 5.8+）へ委譲する 2 つのブリッジプロバイダがあります。

**`Toolset.Editor.ControlRig.*`（44 件）** — 上記ネイティブのアセット編集コマンドのミラー。グループ：アセット作成（1。`Create` はプロジェクトの `RigVM.BlueprintIndependentAssets` の設定にかかわらず常に旧形式の Control Rig を作ります。`CreateAsset` とは異なります。[Control Rig アセットの形式](#control-rig-アセットの形式) を参照）/ ヒエラルキー観測（8）/ ヒエラルキー編集（7）/ グラフ管理（10）/ ノード（7）/ ピン（6）/ 変数（5）。

**`Toolset.Editor.SequencerControlRig.*`（63 件）** — アニメーション時のコントロールオーサリング。実装は Sequencer モジュール（`SequencerControlRigTools`）ですが、全コマンドが ControlRig のコントロールを対象とするため本セクションに掲載しています。ControlRig に加えて `MovieSceneAnimMixer` が必要です。UE 5.8 では、`ControlRigPath` を使う 37 件（残りの 26 件は使わず、影響を受けません。`ZeroControlRigTransforms` は `ControlRigPath` を互換のために受け付けるだけで、アクティブな Sequencer の rig に作用するので、この 26 件に入ります）は、ランタイムアセットの Control Rig を、委譲する前に `UnsupportedOperation` で断ります。委譲先の Toolset はシーケンス内の rig を Blueprint のクラスで探しますが、ランタイムアセットにはそのクラスが無く、見つからずに失敗するか、パスの文字列が重なる別の旧形式の rig を操作してしまうためです。値の読み取りだけのコマンド（`Get...` / `Is...`）も同じく断ります。メッセージにはコマンド名とアセットのパスが入り、パスはオブジェクトパス（`/Game/Rigs/CR_X.CR_X`）でもパッケージパス（`/Game/Rigs/CR_X`）でも同じです。案内できる同等のネイティブコマンドはありません。`AssetPath` や `ControlRigPath` の欠落は今までどおり先に `InvalidParams` になり、旧形式の rig、アセットが存在しないパス、アセットのパスでない値は今までどおり委譲されます。グループ：

> **`Toolset.Editor.ControlRig.*` の引数は、Control Rig Toolset 自身の引数に揃えています。**
>
> - **要素とイベントの種別は、取りうる値をスキーマに載せます。** `AddBone`・`AddNull`・`AddControlElement`・`AddElement` の `Parent.Type`、`GetChildren`・`GetParent`・`GetGlobalTransform`・`SetGlobalTransform`・`GetLocalTransform`・`SetLocalTransform` の `Item.Type`、`GetElements` の `ElementType` に、Toolset が取る要素の種別（`Bone` が先頭）が載ります。`AddEventNode` と `GetEventGraph` の `EventType` は `FORWARD_SOLVE`・`BACKWARD_SOLVE`・`INTERACTION` を載せます。値は素通しで、強制はしないので、以前動いた呼び出しは引き続き動きます。`AddEventGraph` は `FORWARD_SOLVE` を取りません。Toolset が断るため、`EventType` には `BACKWARD_SOLVE` と `INTERACTION` だけを載せます。
> - ⚠️ **`AddElement` は `ElementType` を省略するとボーンを追加します。** スキーマに `Bone` と `Null` が載り、既定値 `Bone` が示されます。Toolset は種別を必須とするため、省略した呼び出しは以前は失敗していましたが、今はボーンを追加して成功します。`Control` は引き続き Toolset が断ります。
> - ⚠️ **`AddEventNode` と `AddVariableNode` は、`X` / `Y` で指定した位置にノードを置きます。** 以前は位置が黙って捨てられていました。片方の座標だけを指定した場合はもう一方が `0` になり、どちらも無ければ位置を送りません。
> - ⚠️ **`CreateNode` は、`OffsetX` / `OffsetY` の位置にノードを置きます。** この 2 つの引数は宣言されていましたが、Toolset に届いていませんでした。同じ規則で、欠けた座標は `0`、どちらも無ければ位置を送りません。`X` / `Y` は受け付けません（以前もスキーマが断っていました）。
> - **`SetNodePosition` が動くようになりました。** 以前は呼ぶたびに失敗していました。今は位置を Toolset へ送ります。`X` と `Y` の両方が必須なのは従来どおりです。
> - **Toolset が必要とする次の 2 引数に、既定値 `""` を付けました:** `CreateNode` の `NodeName`、`AddVariable` の `DefaultValue`。省略しても Toolset 側で失敗しなくなります。
> - **`AddControlElement` は `Settings` のすべてのメンバーを、Toolset の既定値つきで宣言します。** `Settings` は省略可能です。省略したとき、または一部のメンバーだけを渡したときは、ブリッジが呼び出しの前に 23 メンバー全部へ補うので、Toolset の必須メンバーの一覧で断られることはありません。渡した値は保たれ、省略したメンバーは次の既定値になります。`LimitEnabled` の要素の中（`bMinimum`・`bMaximum`: `false`）、`MinimumValue` / `MaximumValue`（すべて 0）、`ShapeColor`、`Customization` の中も同様です。既定値: `AnimationType` `"AnimationControl"`、`ControlType` `"EulerTransform"`、`DisplayName` `"None"`、`PrimaryAxis` `"X"`、`bIsCurve` `false`、`LimitEnabled` `[]`、`bDrawLimits` `true`、`bShapeVisible` `true`、`ShapeVisibility` `"UserDefined"`、`ShapeName` `"Default"`、`ShapeColor` 赤（`R` 1、`G` 0、`B` 0、`A` 1）、`bIsTransientControl` `false`、`ControlEnum` `null`、`Customization` は `AvailableSpaces` と `RemovedSpaces` が空、`DrivenControls` `[]`、`bGroupWithParentControl` `false`、`bRestrictSpaceSwitching` `false`、`FilteredChannels` `[]`、`PreferredRotationOrder` `"YZX"`、`bUsePreferredRotationOrder` `false`、`ShapeTransform` は恒等（`Location` はすべて 0、`Rotation` はすべて 0、`Scale` はすべて 1。省略した部分はこの値で補われ、結果は変わりません）。列挙の 5 メンバー（`AnimationType`・`ControlType`・`PrimaryAxis`・`ShapeVisibility`・`PreferredRotationOrder`）は名前でも数値でも渡せます。一覧にない `Settings` のメンバーは受け付けて、そのまま渡します。 `Settings` の中で要素名・表示名になる名前は、Toolset を呼ぶ前に長さを確認します。対象は `DisplayName`、`ShapeName`、`Customization.AvailableSpaces`（`Key.Name` と `Label`）・`Customization.RemovedSpaces`・`DrivenControls` の各要素の `Name` と `Label` です。1023 文字を超えるものは `InvalidParams` で断られ、メッセージには一覧の中の位置まで含めたフィールド名（例: `Settings.DrivenControls[1].Name`）が入ります。ここでもメンバー名は大文字小文字を区別せずに照合します。
>   スカラーのメンバー（真偽値と数値）は、もう一方の JSON の型も受け付けます（文字列で渡した真偽値、数値の文字列など）。Toolset は従来どおりに読みます。

| グループ | 件数 | コマンド |
|---|---:|---|
| コントロール値 | 16 | `Get`/`SetFloatValue`・`BoolValue`・`IntValue`・`Vector2DValue`・`PositionValue`・`RotatorValue`・`ScaleValue`・`EulerTransformValue` |
| ワールドトランスフォーム | 3 | `GetWorldTransform`・`SetWorldTransform`・`GetActorTransformAtFrame` |
| レイヤードリグ | 6 | `CollapseAnimLayers`・`IsLayeredControlRig`・`SetLayeredMode`・`Get`/`SetPriorityOrder`・`IsFKControlRig` |
| アニメーションレイヤー | 6 | `GetControlRigAnimLayers`・`AddControlRigLayerFromSelection`・`Delete`/`Duplicate`/`Reorder`/`MergeControlRigAnimLayers` |
| スペース | 4 | `Set`/`Move`/`Delete`/`BakeControlRigSpace` |
| トゥイーン | 3 | `TweenControlRig`・`BlendValuesOnSelected`・`SnapControlRig` |
| ミラーリング | 3 | `SelectMirroredControls`・`MirrorSelectedControls`・`ZeroControlRigTransforms` |
| 選択 | 4 | `GetSelectedControls`・`SelectControl`・`ClearControlSelection`・`FrameControlSelection` |
| FBX | 2 | `ExportFBXFromRig`・`ImportFBXToRig` |
| Sequencer 問い合わせ | 4 | `GetSequencerControlRigs`・`GetSequencerControlsInfo`・`Get`/`SetControlRigTransformInSequencer` |
| アニメーションモード設定 | 12 | `AnimModeGizmoScale`（`Scale` は旧ギズモの大きさに足すオフセットで、倍率ではない。範囲 -10〜150、既定 0。0 と負の値は受け付け、150 超・数値でない値・無限大は拒否される。ブリッジは動作中のエディタだけを変えて何も保存せず、UE 5.8 の既定ギズモは読まない。保存したいときは[ギズモの大きさ](#ギズモの大きさ2)のネイティブ 2 本を、既定ギズモには [`UAIP.Editor.Level.SetTransformGizmoSize`](#uaipeditorlevel) を使う）・`AnimModeHierarchy`・`AnimModeNulls`・`AnimModeHideManips`・`AnimModeOnlyRigSel`・`AnimModeLocalSpaces` の `Get`/`Set` |

---

## UAIP.Editor.ControlRig.Dynamics 🧩

ControlRig ヒエラルキー上の `ControlRigDynamics` コンポーネント型（ソルバー・パーティクル・コライダー・拘束・コーンリミット・コンファイナー）を型ごとに編集します。加えて、一連の構成をまとめて構築・付け替えする 4 コマンドを提供します。UE 5.8+ と `ControlRigDynamics` プラグイン（Experimental）が必要で、UE 5.7 またはプラグイン無効時はドメインごと利用できません。[`UAIP.Editor.ControlRig`](#uaipeditorcontrolrig) の汎用コンポーネントコマンドは、このプラグイン無しでもまったく同じコンポーネントに到達できます — ここで増えるのは、型ごとに項目名が付き、範囲検査が入ったスキーマです。このドメインに Toolset ブリッジは存在しません。

`ControlRigDynamics` は Experimental のエンジンプラグインであり、その構造体はエンジンのマイナーバージョン間で変わりうるため、**このドメインのコマンドはすべて `Stability: Experimental`** を返します。読み取りは `EditorInspect`、書き込みはすべて `ControlRigComponentEdit`（既定無効）を要求し、PIE 実行中は拒否されます。本ドメインと `UAIP.Editor.ControlRig.Physics` は互いに独立しており、片方だけを持つプロジェクト構成でもそれぞれ単独で現れます。

> **前提条件 — プラグインを有効化してエディタを再起動してください**: エディタビルドでは、ビルド対象のエンジンに `ControlRigDynamics` が存在していれば UAIP が自動的にその対応をコンパイルへ含めます — `.uproject` の `Plugins` 配列への追加もリビルドも不要になりました。残っているのはプラグイン自体を有効化することだけです（`ControlRigDynamics` は Experimental で既定無効のため、たいていのプロジェクトはこの手順が必要です）。**Edit → Plugins** から有効化する（または `.uproject` へ自分で `{ "Name": "ControlRigDynamics", "Enabled": true }` を追加する）か、いずれにせよエディタを再起動してください。プラグインが無効な間はドメインごと `uaip_list_commands` に現れず、これらのコマンドを呼ぶと有効化すべきプラグイン名を含む `CommandNotFound` が返ります。`UAIP.Core.ListIntegrations` でもこのドメインの状態を直接確認できます。

#### Typed reads（6 コマンド）— 要 `EditorInspect`

| コマンド | 説明 |
|---|---|
| `GetDynamicsSolverSettings` | `FRigDynamicsSolverComponent` の `Settings`・`SpaceMotion`・`TeleportDetection`。`Particles` / `Colliders` / `Constraints` / `ConeLimits` / `Confiners` の参照配列はここでは返らない — `GetComponent` で読む |
| `GetDynamicsParticleProperties` | `FRigDynamicsParticleComponent` の `ParticleProperties` |
| `GetDynamicsColliderShapes` | `FRigDynamicsColliderComponent` の `Shapes`（`Boxes`・`Capsules`・`Planes`）。`SetDynamicsColliderShapes` がそのまま受け取れる形状 |
| `GetDynamicsConstraintSettings` | `FRigDynamicsConstraintComponent` の `ConstraintType`・`Strength`・`DampingRatio`・`ExtraDamping`・`bAccelerationMode`・`LengthMultiplier`・`ExtraLength`。トポロジのキーはここでは返らない |
| `GetDynamicsConeLimitSettings` | `FRigDynamicsConeLimitComponent` の `Strength`・`DampingRatio`・`Angle`。トポロジのキーはここでは返らない |
| `GetDynamicsConfinerSettings` | `FRigDynamicsConfinerComponent` の `Shapes` と `Strength` |

#### Typed writes（6 コマンド）— 要 `ControlRigComponentEdit`

| コマンド | 説明 |
|---|---|
| `SetDynamicsSolverSettings` | `Settings`・`SpaceMotion`・`TeleportDetection` を置き換える。ソルバーの参照配列はここでは変更できない — `AddComponentToDynamicsSolver` / `RemoveComponentFromDynamicsSolver` を使う |
| `SetDynamicsParticleProperties` | `ParticleProperties` の 1 つ以上の項目を置き換える。`Radius` と `Mass` は正、`Strength`・`DampingRatio`・`ExtraDamping`・`AngleLimit`・`AngleLimitStrength`・`Damping` は非負、`TargetMode` は 0.0〜1.0、`MovementType` は `Kinematic` か `Simulated` |
| `SetDynamicsColliderShapes` | `Shapes` コレクション全体を置き換える。各トランスフォームは有限、ボックス／平面の extent は全軸で正、カプセルの半径は正、カプセルの長さは非負 |
| `SetDynamicsConstraintSettings` | 1 つ以上の設定を置き換える。`ConstraintType` は `Hard` か `Soft`、`Strength`・`DampingRatio`・`ExtraDamping`・`LengthMultiplier` は非負、`ExtraLength` は有限であれば正負どちらでもよい。トポロジのキーはそのまま引き継がれる |
| `SetDynamicsConeLimitSettings` | `Strength`・`DampingRatio`・`Angle` を置き換える。3 つとも負または非有限なら拒否。トポロジのキーはここでは変更できない — `SetComponentContent` を使う |
| `SetDynamicsConfinerSettings` | `Shapes` と `Strength` を置き換える。形状の検査は `SetDynamicsColliderShapes` と同じ。`Strength` は有限かつ非負 |

#### Orchestration（5 コマンド）— 要 `ControlRigComponentEdit`

| コマンド | 説明 |
|---|---|
| `AddDynamicsChain` | チェーンを 1 コマンドで構築する。`StartElementName` から `EndElementName` までの各要素にパーティクルを、隣接するペアごとに拘束を作り、それらすべてを指定ソルバーへ登録する。`StartElementName` は `EndElementName` の祖先である必要があり、両者が同一要素であってはならない。任意の `ParticleContent` / `ConstraintContent` はその種類のすべてに適用される。`ConstraintContent` はトポロジのキーを指定できない（どのパーティクル同士を繋ぐかはチェーン側が決めるため） |
| `ImportDynamicsCollidersFromPhysicsAsset` | PhysicsAsset の各ボディのうち、対応する骨がリグに存在するものについてコライダーを 1 つずつ作る。ボックス・スフィア・カプセルの形状を変換する（スフィアは長さ 0 のカプセルになる）。作成したものの一覧と、`SkippedBodies` として飛ばしたものとその理由を返す |
| `AddComponentToDynamicsSolver` | Dynamics コンポーネントをソルバーへ登録する。ソルバーのどの配列へ入るかは型から決まり、選べない。使われた配列は `SolverArray` として返る。既に登録済みのものを登録しても何も変わらず、`Added: false` が返る |
| `RemoveComponentFromDynamicsSolver` | ソルバーのすべての参照配列からコンポーネントを外す。ソルバーが参照していないものを外しても何も変わらず、`Removed: false` が返る |
| `RemoveDynamicsChain` | チェーンを 1 コマンドで撤収する。`AddDynamicsChain` に渡したのと同じ指定（`StartElementName` / `EndElementName` / `ElementType`）、またはその応答が返した実キー（`Particles[]` / `Constraints[]`）でチェーンを同定し、ソルバーの登録から外し、拘束を消し、パーティクルを消す。同定が曖昧・不完全なら**何も変更せずに**拒否する。`DryRun` では削除せず、対象と外部参照だけを返す |

> **Note — 型付き `Set*` は部分書き込みですが、空の書き込みは認められません**: 各項目は独立して省略可能ですが、少なくとも 1 つは必須です。省略した項目は型の既定値に戻るのではなく、**いまの値のまま**残ります。シミュレーションが受け付けない値（非有限な数値、負の質量や強さ、0〜1 の外の比率、0 以下のタイムステップや反復回数）は拒否され、コンポーネントは変更されません。汎用の `SetComponentContent` も同じ検査を行うため、型付きコマンドを迂回して不正値を通す抜け道はありません。
>
> **Note — 違う型のコンポーネント名を渡すと `NotFound` であり、ポリシーエラーではありません**: コライダー用のコマンドに拘束の名前を渡すと `NotFound` が返ります。型の取り違えは「どのコンポーネントを指していたか」の勘違いであることがほとんどで、どの型が許可されているかという話ではないためです。
>
> **Note — `ImportDynamicsCollidersFromPhysicsAsset` は 2 種類の「合わない」を区別します**: 対応する骨がリグに無い、その要素にはコライダーを付けられない、変換対象の形状が 1 つも無い（凸包・テーパードカプセル・レベルセットは変換しない）ボディは**飛ばして**残りを取り込み、理由付きで `SkippedBodies` に返します。骨は実在するのに形状の値が使えないボディは**リクエスト全体を拒否**します — 黙って一部だけ作るのを避けるためです。作られたコライダーはどのソルバーにも登録されません。登録は `AddComponentToDynamicsSolver` で明示的に行ってください。
>
> **Note — `RemoveComponentFromDynamicsSolver` は登録解除であって削除ではありません**: コンポーネント自体はヒエラルキーに残ります（削除は `RemoveComponent`）。対象が既に存在しなくても構わないため、削除済みコンポーネントが残したキーの掃除にも使えます。また、どの配列かを指定する引数は無く、ソルバーのすべての配列から外します。ソルバーがまだシミュレートしている拘束やコーンリミットのうちその対象を指しているものは `ReferenceWarnings` として返り、そのまま残されます — ソルバーはパーティクルを解決できない拘束を、エラーも警告も出さずに読み飛ばすためです。
>
> **Note — `RemoveDynamicsChain` はチェーンの指し方をちょうど 1 通りだけ受け付けます**: `AddDynamicsChain` に渡したのと同じ `StartElementName` / `EndElementName` / `ElementType`（とソルバー）による指定、またはその応答が返した実キーの `Particles[]` / `Constraints[]` による指定のどちらか一方だけです。両方渡す、またはどちらも渡さない場合は `InvalidParams` です。どちらの指定でも、対象は**分岐も輪も欠けも無い 1 本の連なり**にちょうど一致していなければなりません。それ以外はアセットを変更せずに拒否されます — 候補が複数あれば `AmbiguousElements[]`、足りない箇所があれば `IncompleteElements[]` が返ります。「そこに何も無い」場合の扱いは指定のしかたで変わります — 範囲の指定でチェーンが無ければ「既に片付いている」扱い（`Status: AlreadyAbsent`、成功扱いの no-op で、繰り返し呼んでも安全）ですが、実キーの指定で名指ししたキーが存在しなければ `NotFound` になります。個体を名指ししている以上、無いことは「何もしなくてよい」ではなく実際のエラーだからです。
>
> **Note — チェーンの外からの参照の扱いは `ReferenceHandling` が決めます**。値は上記 `RemoveComponent` と同じ 3 つで、大文字小文字も区別されます: `Reject`（既定）は拒否し、見つかった外部参照をすべて `References` に返します。`Detach` は先に参照を外しますが、1 件でも外せないものがあれば**外す前に**拒否します。`Force` は参照を残したまま撤収し、片端が解決できなくなったものは `RemoveComponent` と同じ形で `ReferenceWarnings` に返ります。`DryRun` はこの確認を含むすべての検査を行い、対象と外部参照だけをアセットに触れずに返します（`Status: Previewed`、`RemovedCount: 0`）。同じ指定から `DryRun` を外して呼び直せば、ここで示されたものがそのまま撤収されます。
>
> **Note — 事前の拒否は無変更を保証しますが、削除の途中の失敗は完全な復元を保証しません**: すべての検査を通過した後に何かが失敗すると、`Status` は `RolledBack` または `RollbackFailed` にもなり得ます。ロールバックはできる範囲を戻し、`RemovedBeforeFailure[]` / `RestoredComponents[]` / `MissingAfterRollback[]` / `UnrestoredReferrers[]` / `SolverRestored` で達成範囲を開示します — 完全な復元を主張するのではありません。削除済みコンポーネントを作り直しても、同じキーが再現される保証が無いためです。⚠️ 撤収そのものは成功したのに応答の記録が保存できなかった場合、チェーンは既に消えているにもかかわらず `ExecutionFailed` が返ります — その旨は `ErrorMessage` に明記されます。このドメインで artifact の保存を検査しているのはこのコマンドだけです。

---

## UAIP.Editor.ControlRig.Physics 🧩

ControlRig ヒエラルキー上の `ControlRigPhysics` コンポーネント型（ソルバー・ボディ・ジョイント・コントロール）を型ごとに編集します。`ControlRigPhysics` プラグイン（Beta）が必要です。上記の Dynamics ドメインと異なり、UE 5.8 だけでなく UE 5.7 でも利用できます。[`UAIP.Editor.ControlRig`](#uaipeditorcontrolrig) の汎用コンポーネントコマンドは、このプラグイン無しでもまったく同じコンポーネントに到達できます。このドメインに Toolset ブリッジは存在しません。

読み取りは `EditorInspect`、書き込みはすべて `ControlRigComponentEdit`（既定無効）を要求し、PIE 実行中および ModularRig アセットに対しては拒否されます。本ドメインと `UAIP.Editor.ControlRig.Dynamics` は互いに独立しており、片方だけを持つプロジェクト構成でもそれぞれ単独で現れます。

> **前提条件**: エディタビルドでは、ビルド対象のエンジンに `ControlRigPhysics` が存在していれば UAIP が自動的にその対応をコンパイルへ含めます — `.uproject` の `Plugins` 配列への追加もリビルドも不要になりました。`ControlRigPhysics` はエンジン既定で有効なため、ほとんどのプロジェクトではこれらのコマンドはそのまま動きます。プロジェクトが明示的に無効化している場合は、**Edit → Plugins** から有効化してエディタを再起動してください。プラグインが無効な間はドメインごと `uaip_list_commands` に現れず、これらのコマンドを呼ぶと有効化すべきプラグイン名を含む `CommandNotFound` が返ります。`UAIP.Core.ListIntegrations` でもこのドメインの状態を直接確認できます。

#### Typed reads（4 コマンド）— 要 `EditorInspect`

| コマンド | 説明 |
|---|---|
| `GetPhysicsSolverSettings` | UE 5.8 では `FRigPhysicsSolverComponent` の `SolverSettings`・`SpaceMotion`・`TeleportDetection`（UE 5.7 では `SolverSettings` と `SimulationSpaceSettings`）。`SolverSettings.SpaceBone` はここでは返らない — `GetComponent` で読む |
| `GetPhysicsBodySettings` | `FRigPhysicsBodyComponent` の調整可能な設定（質量・慣性のオーバーライド、ダンピング、`MovementType`、`CollisionType`、`KinematicTargetSpace`、重力倍率、ブレンドウェイト、CCD ほか）をトップレベルで返す。トポロジ・コリジョン形状・キネマティックターゲットはここでは返らない |
| `GetPhysicsJointSettings` | `FRigPhysicsJointComponent` の `JointData` と `DriveData` を JSON オブジェクトとして返す。親／子ボディのキーはここでは返らない |
| `GetPhysicsControlSettings` | `FRigPhysicsControlComponent` の `ControlData`・`ControlMultiplier`・`ControlTarget`・`UseParentBodyAsDefault`。親／子ボディのキーはここでは返らない |

#### Typed writes（4 コマンド）— 要 `ControlRigComponentEdit`

| コマンド | 説明 |
|---|---|
| `SetPhysicsSolverSettings` | UE 5.8 では `SolverSettings`・`SpaceMotion`・`TeleportDetection` を置き換える（UE 5.7 では `SolverSettings` と `SimulationSpaceSettings`）。`SpaceBone` を指定した `SolverSettings` は拒否される |
| `SetPhysicsBodySettings` | 1 つ以上のボディ設定を置き換える。`MovementType` は `Static` / `Kinematic` / `Simulated` / `Default`、`CollisionType` は `NoCollision` / `QueryOnly` / `PhysicsOnly` / `QueryAndPhysics` / `ProbeOnly` / `QueryAndProbe`、`KinematicTargetSpace` は `World` / `Component` / `OffsetInBoneSpace` / `OffsetInWorldSpace`。`LinearDamping` と `AngularDamping` は非負。トポロジ・コリジョン形状・キネマティックターゲットはそのまま引き継がれる |
| `SetPhysicsJointSettings` | `JointData` と `DriveData` を置き換える。`LinearProjectionAmount` と `AngularProjectionAmount` は 0.0〜1.0、`ParentInverseMassScale` は非負。親／子ボディのキーはここでは変更できない — `SetComponentContent` を使う |
| `SetPhysicsControlSettings` | `ControlData`・`ControlMultiplier`・`ControlTarget`・`UseParentBodyAsDefault` を置き換える。負の強さ・ダンピング・倍率は拒否される。親／子ボディのキーはここでは変更できない — `SetComponentContent` を使う |

> **⚠️ Note — ソルバー系コマンドは UE 5.7 と UE 5.8 でスキーマが異なります**: UE 5.8 の `GetPhysicsSolverSettings` / `SetPhysicsSolverSettings` は `SolverSettings`・`SpaceMotion`・`TeleportDetection` を扱いますが、UE 5.7 の同じ 2 コマンドは `SolverSettings` と `SimulationSpaceSettings` を扱います。これはエンジンプラグイン側の構造体の構成に従ったものです。形状を決め打ちせず、実行時に `uaip_describe_command` でコマンド自身の `Description` を読んでください。残り 6 コマンドは両バージョンで同じスキーマです。
>
> **Note — 型付き `Set*` は部分書き込みですが、空の書き込みは認められません**: 各項目は独立して省略可能ですが、少なくとも 1 つは必須です。省略した項目は型の既定値に戻るのではなく、いまの値のまま残ります。ソルバーが受け付けない値（非有限な数値、下限を下回る反復数やステップ数、負のしきい値、0〜1 の外の比率）は拒否され、コンポーネントは変更されません。汎用の `SetComponentContent` も同じ検査を行います。
>
> **Note — 違う型のコンポーネント名を渡すと `NotFound` であり、ポリシーエラーではありません**: ボディ用のコマンドにジョイントの名前を渡すと `NotFound` が返ります。理由は Dynamics ドメインと同じです。

---

## UAIP.Editor.EnhancedInput

Enhanced Input アセット編集 — Input Action と Input Mapping Context。

| コマンド | 説明 |
|---|---|
| `ListInputActions` | プロジェクト内の Enhanced Input Action アセット一覧 |
| `ListMappingContexts` | プロジェクト内の Input Mapping Context アセット一覧 |
| `GetInputActionInfo` | Input Action の詳細（ValueType・Triggers・Modifiers）。各 Trigger / Modifier の `Params` が参照・コンテナ・構造体の値も返すようになり（書き込み側が受け付けるのと同じ形式）、あわせて `PropertyWriteRequirements` マップが付きます |
| `GetMappingContextInfo` | Mapping Context の詳細（エントリ・キー・Modifier・Trigger）。`Params` の構造化された値と `PropertyWriteRequirements` マップは `GetInputActionInfo` と同じ |
| `DeleteInputAction` | Input Action アセットを削除。`DisableSave` が有効なときは `PolicyViolation` で拒否 |
| `DeleteMappingContext` | Input Mapping Context アセットを削除。`DisableSave` が有効なときは `PolicyViolation` で拒否 |
| `AddInputMapping` | Mapping Context にキーマッピングを追加 |
| `RemoveInputMapping` | インデックス指定でキーマッピングを削除 |
| `SetInputMappingKey` | マッピングのキーを変更 |
| `SetInputMappingModifier` | マッピングの Modifier を設定/置換 |
| `SetInputMappingTrigger` | マッピングの Trigger を設定/置換 |
| `SetInputActionModifier` | Input Action の Modifier を設定/置換 |
| `SetInputActionTrigger` | Input Action の Trigger を設定/置換 |
| `GetAvailableInputTriggerClasses` | このエディタがロード済みの `UInputTrigger` 派生クラスを、このセッションが今名指しできるかどうかにかかわらず全件返す — 結果の `ClassPath` を `SetInputActionTrigger` / `SetInputMappingTrigger` の `Triggers` エントリの `Class` として渡せる。各エントリは `Admission`（`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`）と `RequiredCapabilities` / `MissingCapabilities` を持ち、両セッターが検証するのと同じポリシーで判定される — `/Script/EnhancedInput` の外から来るクラスも一覧から外されず `EnhancedInputCustomTypeEdit` を挙げて掲載され、`UInputTriggerChordAction` / `UInputTriggerChordBlocker` はどの Capability でも開かないため `NotAddable` として掲載される。`ClassPath` 順にソートされ、`TotalCount` / `ReturnedCount` / `Truncated`（上限 200）を報告する。`EditorInspect` が必要 |
| `GetAvailableInputModifierClasses` | このエディタがロード済みの `UInputModifier` 派生クラスを、このセッションが今名指しできるかどうかにかかわらず全件返す — 結果の `ClassPath` を `SetInputActionModifier` / `SetInputMappingModifier` の `Modifiers` エントリの `Class` として渡せる。`GetAvailableInputTriggerClasses` と同じ `Admission` / `RequiredCapabilities` / `MissingCapabilities` を、両セッターが検証するのと同じポリシーで報告する — `/Script/EnhancedInput` の外から来るクラスも一覧から外されず `EnhancedInputCustomTypeEdit` を挙げて掲載される。`ClassPath` 順にソートされ、`TotalCount` / `ReturnedCount` / `Truncated`（上限 200）を報告する。`EditorInspect` が必要 |

> Trigger / Modifier を書き込む 4 コマンド（`SetInputMappingModifier` / `SetInputMappingTrigger` / `SetInputActionModifier` / `SetInputActionTrigger`）は、参照・コンテナを一律拒否しなくなりました。参照には `EnhancedInputEdit` に加えて `EnhancedInputReferenceEdit`、構造体・コンテナには `PropertyStructuredEdit` が必要で、これらの値はエンジンの括弧表記ではなく JSON で渡します — 必要な形式は上記 2 つの取得系がプロパティごとに報告します。なお他の多くの書き込みコマンドと異なり、`Params` にプロパティ名と一致しないキーがあるとリクエスト全体が失敗します（これらの応答には「飛ばしたキー」を報告する場所が無いためです）。

> **Note — プロジェクト・プラグイン定義の Trigger / Modifier クラスは Capability でゲートされます**: `/Script/EnhancedInput` モジュール由来の `Class` はこれまでどおり受け付けられます。それ以外に由来するクラス — プロジェクトモジュール、プラグインモジュール、`UInputTrigger` / `UInputModifier` の Blueprint 派生クラス — には `EnhancedInputCustomTypeEdit` が必要になりました。Material と違い、このドメインに対になる「危険な型」用の Capability はありません。Trigger はキー状態を評価し、Modifier は入力値を変換するだけで、どちらもリクエストが運んできたコードを実行しないためです。2 種の Trigger — `UInputTriggerChordAction` と `UInputTriggerChordBlocker`、およびそれらの派生 — は、**どの Capability を持っていても拒否されます**。Enhanced Input が chord の一部として自前で組み立てて設定する種別であり、作者が選ぶ対象ではないからです（エンジン自身のクラスピッカーも同じ理由でこれらを隠しています）。`UInputTrigger` / `UInputModifier` 自体は抽象クラスで、同様に到達できません。[安全性と Capability](safety.md#ゲームプレイシステム) を参照してください。
>
> **`Class` はフルオブジェクトパスも受け付けるようになりました。** パス区切りを含まない名前はこれまでどおり `/Script/EnhancedInput` の中で解決されます（`Pressed` も `InputTriggerPressed` も従来と同じように解決されます）。それ以外に由来するクラスはフルオブジェクトパスで指定します — `/Script/MyGame.MyGameInputTrigger`、Blueprint なら `/Game/Input/BPT_Hold.BPT_Hold_C` のように書きます。これが無い間は、そうしたクラスへ到達できる綴りがそもそも存在しませんでした。クラスは既にロード済みである必要があります。許可されるかどうかを判定するためにロードは行わず、何にも一致しない名前は `NotFound` になります。
>
> この確認は 4 つの書き込みコマンドに限りません — 一般規則は [Capability でゲートされたカスタム型](#capability-でゲートされたカスタム型) を参照してください。このドメインではさらに `RemoveInputMapping` / `DeleteInputAction` / `DeleteMappingContext` も対象です。マッピングエントリの削除やアセットの削除は、それが保持していた Trigger / Modifier インスタンスを丸ごと捨てるため、このドメインが同梱していないクラスは「入れるとき」と同じ Capability を「出すとき」にも要します。3 コマンドについてこれ以外の変更はなく、Enhanced Input のクラスしか保持していない対象 — エディタから普通に設定した chord トリガーを含みます — は従来どおり Capability 不要で削除できます。
>
> ⚠️ **破壊的変更**: 従来の判定に落ちた Trigger / Modifier の `Class` は `PolicyViolation` または `InvalidParams` で拒否されていました。4 つの書き込みコマンドは、単に別モジュール由来であるクラスには `CapabilityNotAvailable` を返して `EnhancedInputCustomTypeEdit` を挙げ、ロードされていないクラスには `NotFound`、`UInputTrigger` / `UInputModifier` の派生ですらないクラスには `InvalidParams` を返します。2 種の chord トリガーは引き続き `PolicyViolation` です。旧コードの互換期間は設けません — 旧コードは「権限があっても通らない」という意味であり、残すと存在しない権限体系を説明することになるためです。
>
> ⚠️ **破壊的変更 — 系統違いのクラスが拒否されるようになりました。** 従来の判定はクラスの基底型を一切見ていなかったため、Trigger でも Modifier でもない Enhanced Input のクラス（たとえば `InputAction`）を名指ししても素通りし、リストへ実体化する呼び出しまで到達していました。この組み合わせは `InvalidParams` になります。もともと使えるアセットにはなりませんでした。

---

## UAIP.Editor.GAS 🧩

エディタ時の GameplayAbilities アセット編集 — GameplayCue タグと Cue Notify アセット。`GameplayAbilities` プラグインが必要（Toolset 版は `GASToolsets` も必要）。

### ネイティブ（8）

| コマンド | 説明 |
|---|---|
| `AddCueTag` | `GameplayCue.*` タグをプロジェクトタグテーブルに追加 |
| `RemoveCueTag` | `GameplayCue.*` タグを削除 |
| `ListCues` | 全 GameplayCue タグを列挙 |
| `GetCueInfo` | GameplayCue タグの詳細と登録済み Cue Notify アセットを取得 |
| `FindCueNotifyAssets` | タグを扱う Cue Notify アセットを検索 |
| `FindCueTagsWithoutNotifies` | Notify アセットが紐づいていない GameplayCue タグを検出 |
| `CreateCueNotifyAsset` | GameplayCueNotify アセットを新規作成（Actor / Static / Burst） |
| `ExecuteCueOnSelectedActor` | 選択中アクターで GameplayCue を実行（テスト用簡易コマンド） |

### Toolset ブリッジ（14）🧩

`GASToolsets`（UE 5.8+）経由でネイティブコマンドを委譲。プロバイダ：`Toolset.Editor.GAS.*`。グループ：Runtime 検査（6 件）— `GetAttributeValues` / `GetActiveEffects` / `GetGrantedAbilities` / `GetActiveTags` / `FindAttributeSetClasses` / `ListAttributes`、GameplayCue オーサリング（8 件）— `ListCues` / `GetCueInfo` / `FindCueNotifyAssets` / `FindCueTagsWithoutNotifies` / `ExecuteCueOnSelectedActor` / `CreateCueNotifyAsset` / `AddCueTag` / `RemoveCueTag`。

---

## UAIP.Editor.Python 🧩

Python コマンド拡張。`PythonScriptPlugin` が必要です。

| コマンド | 説明 |
|---|---|
| `ReloadPythonCommands` 🧩 | コマンドディレクトリを再スキャンし既存ハンドラのディスクリプタをインプレース更新 |
| *(動的コマンド)* 🧩 | `@uaip_command` デコレータで登録されたコマンド（名前はユーザースクリプトに依存） |

---

## UAIP.Editor.Sandbox 🧩

Sandbox セッションのライフサイクル管理。`FileSandbox` プラグインが必要です。`FileSandbox` が有効でない場合、このセクションのコマンドは全て `CommandNotFound` を返します。

| コマンド | 説明 |
|---|---|
| `GetSandboxStatus` 🧩 | 現在の Sandbox 状態を照会 — `Active`・`IsStale`・`SessionId`・`OwnerUAIPSessionId` を返す |
| `GetSandboxChanges` 🧩 | アクティブな Sandbox 内の保留中変更一覧を取得 — `FilePath`・`ChangeKind`（Added / Edited / Removed）・`SizeBytes`・`TotalCount` |
| `BeginSandboxSession` 🧩 | 新しい FileSandbox セッションを開始。以降のアセット書き込みは Sandbox にリダイレクトされる |
| `EndSandboxSession` 🧩 | アクティブな Sandbox セッションを終了。未コミットの変更は自動的に Revert される |
| `CommitSandboxChanges` 🧩 | 選択した（または全ての）Sandbox 変更をディスクにフラッシュ。`CommittedFiles`・`SkippedFiles`・`CommittedCount` を返す |
| `RevertSandboxChanges` 🧩 | 保留中の Sandbox 変更を全て破棄（コミットしない） |

---

## UAIP.Editor.WorldPartition

パーティション化されたワールドの World Partition・Data Layer・HLOD 管理（`WorldPartition` プラグイン必須）。World Partition が有効でないレベルでは、変更系コマンドは `ExecutionFailed` を、観測系コマンドは `Success: true` + `IsWorldPartitionEnabled: false` を返します。

### World Partition（12 コマンド）

| コマンド | 説明 |
|---|---|
| `GetWorldPartitionInfo` | World Partition の設定情報を取得 — ストリーミングモード・ランタイムハッシュクラス・WP 有効状態 |
| `GetWorldPartitionStreamingGrids` | World Partition 設定に定義されたランタイムストリーミンググリッド一覧を返す |
| `GetRuntimeGridSettings` | 指定したランタイムグリッドの設定を取得 |
| `SetRuntimeGridSettings` | 指定したランタイムグリッドの設定を変更（`WorldPartitionEdit` 必須） |
| `GetActorWorldPartitionSettings` | アクターの WP 設定を取得 — HLOD レイヤー・spatially loaded フラグ・ランタイムグリッド名 |
| `SetActorIsSpatiallyLoaded` | アクターの spatially loaded フラグを設定（`WorldPartitionEdit` 必須） |
| `SetActorRuntimeGrid` | アクターを特定のランタイムストリーミンググリッドに割り当て（`WorldPartitionEdit` 必須） |
| `SetWorldPartitionStreamingEnabled` | 現在のレベルの WP ストリーミングを有効/無効に切り替え（`WorldPartitionEdit` 必須） |
| `PinActorInWorldPartition` | アクターをストリーミング状態に関係なく常にロードされるよう Pin（`WorldPartitionEdit` 必須） |
| `UnpinActorFromWorldPartition` | アクターの常時ロード Pin を解除（`WorldPartitionEdit` 必須） |
| `DumpWorldPartitionCells` | 現在の WP ストリーミングセルグリッドを JSON アーティファクトとしてダンプ |
| `ListExternalActors` | 外部パッケージとして保存されたアクター一覧を返す（WP 外部アクターワークフロー） |

### Data Layer（15 コマンド）

| コマンド | 説明 |
|---|---|
| `ListDataLayers` | 現在のレベルに存在する全 Data Layer インスタンスを一覧表示 |
| `GetDataLayerInfo` | Data Layer インスタンスの詳細情報を取得 — タイプ・読み込みフィルタ・ランタイム状態・可視性・親階層 |
| `CreateDataLayerAsset` | コンテンツブラウザに新しい Data Layer アセットを作成（`DataLayerEdit` 必須） |
| `DeleteDataLayerAsset` | Data Layer アセットを削除（`DataLayerEdit` 必須）。`DisableSave` が有効なときは `PolicyViolation` で拒否 |
| `CreateDataLayerInstance` | Data Layer アセットから現在のレベルに Data Layer インスタンスを追加（`DataLayerEdit` 必須） |
| `DeleteDataLayerInstance` | 現在のレベルから Data Layer インスタンスを削除（`DataLayerEdit` 必須） |
| `SetDataLayerType` | Data Layer インスタンスのタイプを設定 — Editor または Runtime（`DataLayerEdit` 必須） |
| `SetDataLayerInitialRuntimeState` | Data Layer の初期ランタイム状態を設定 — Unloaded / Loaded / Activated（`DataLayerEdit` 必須） |
| `SetDataLayerIsLoadedInEditor` | エディタビューポートで Data Layer をロードするかどうかを設定（`DataLayerEdit` 必須） |
| `SetDataLayerVisibility` | エディタ内の Data Layer の可視性を設定（`DataLayerEdit` 必須） |
| `SetParentDataLayerInstance` | 親 Data Layer インスタンスを設定して階層を構築（最大 64 レベル・`DataLayerEdit` 必須）。親にできない組み合わせは理由を添えて拒否されます |
| `GetActorDataLayers` | アクターに割り当てられた Data Layer インスタンスを取得 |
| `AddActorToDataLayer` | アクターを Data Layer インスタンスに追加（`DataLayerEdit` 必須） |
| `RemoveActorFromDataLayer` | アクターを Data Layer インスタンスから除外（`DataLayerEdit` 必須） |
| `GetActorsInDataLayer` | 指定した Data Layer インスタンスに割り当てられた全アクターを一覧表示 |

### HLOD（7 コマンド）

| コマンド | 説明 |
|---|---|
| `ListHLODLayers` | プロジェクト内の全 HLOD Layer アセットを一覧表示 |
| `CreateHLODLayer` | `/Game/` 配下に新しい HLOD Layer アセットを作成（`HLODBuild` 必須） |
| `DeleteHLODs` | 指定した HLOD Layer のビルド済み HLOD データを削除（`HLODBuild` 必須）。`DisableSave` が有効なときは `PolicyViolation` で拒否 |
| `SetActorHLODLayer` | アクターを HLOD Layer アセットに割り当て（`HLODBuild` 必須） |
| `BuildHLODs` | 現在のワールドの HLOD ビルドジョブを開始。`HLODBuildJobId` を返す（`HLODBuild` 必須） |
| `CancelHLODBuild` | ジョブ ID を指定して進行中の HLOD ビルドジョブをキャンセル（`HLODBuild` 必須） |
| `GetHLODBuildStatus` | HLOD ビルドジョブの現在の状態を取得 — 実行中・完了・未発見 |

---

## UAIP.Editor.Foliage

エディタでのフォリッジタイプ管理とインスタンス配置。観測系コマンドは PIE 中でも実行可能。編集系コマンドはエディタ停止中（PIE・SIE 以外）でのみ実行可能。

### フォリッジ観測（4 コマンド）

| コマンド | 説明 |
|---|---|
| `ListFoliageTypes` | 現在のレベルの `AInstancedFoliageActor` に登録されているフォリッジタイプをインスタンス数つきで一覧表示 |
| `GetFoliageTypeInfo` | フォリッジタイプの詳細設定を取得 — メッシュパス・密度・スケール範囲・カリング距離・法線整合・傾斜角・インスタンス数 |
| `GetFoliageInstanceCount` | 配置済みインスタンスの合計数を取得。フォリッジタイプ指定でフィルタリング可能（未指定時はタイプ別内訳付きで全合計を返す） |
| `GetFoliageInstances` | 指定バウンディングボックス内のフォリッジインスタンス一覧を取得 — 位置・回転・スケールを返す |

### フォリッジタイプ管理（3 コマンド）

| コマンド | 説明 |
|---|---|
| `AddFoliageTypeToLevel` | フォリッジタイプアセットを現在のレベルの `AInstancedFoliageActor` に登録（`FoliageTypeEdit` 必須） |
| `RemoveFoliageTypeFromLevel` | フォリッジタイプの登録を解除し、全インスタンスを現在のレベルから削除（`FoliageTypeEdit` 必須） |
| `SetFoliageTypeSettings` | フォリッジタイプの設定を更新 — 密度・スケール範囲・カリング距離・法線整合・傾斜角・メッシュ（ISM タイプのみ）（`FoliageTypeEdit` 必須） |

### フォリッジインスタンス操作（4 コマンド）

| コマンド | 説明 |
|---|---|
| `AddFoliageInstances` | 指定トランスフォームにフォリッジインスタンスを配置。World Partition 対応 — 各インスタンスを正しい `AInstancedFoliageActor` セルにルーティング（`FoliageInstanceEdit` 必須） |
| `RemoveFoliageInstances` | バウンディングボックスまたは球体内のフォリッジインスタンスを `MaxRemoveCount` 件まで削除（`FoliageInstanceEdit` 必須） |
| `DeleteAllFoliageInstances` | フォリッジタイプの配置済みインスタンスをすべて削除（`FoliageBulkDelete` 必須） |
| `ResimulateProceduralFoliage` 🧩 | `ProceduralFoliageVolume` を再シミュレーションして結果インスタンスを配置（`ProceduralFoliage` プラグインおよび `FoliageInstanceEdit` 必須） |

---

## UAIP.Editor.DataRegistry 🧩

UE 5.8 Data Registry のエディタ時観測 — 一覧・スキーマ取得・機密フィールドマスキング付きキャッシュ済みアイテム取得。`DataRegistry` プラグインが必要（ブリッジ版はさらに `DataRegistryToolset` + `ToolsetRegistry` が必要）。

### ネイティブ（9 コマンド）

| コマンド | 説明 |
|---|---|
| `ListRegistries` | 登録済みの全 Data Registry を一覧表示。アイテム構造体名でのフィルタ（`StructFilter`）に対応。`IsDataRegistrySystemEnabled` / `AreRegistriesInitialized` の診断情報を同梱 |
| `GetRegistryInfo` | レジストリの ID 数・最低ソース可用性・説明・ID フォーマットを取得 |
| `GetSchema` | アイテム構造体のプロパティスキーマ（名前・型・`IsSecret` フラグ）を取得 |
| `ListItems` | レジストリに登録済みのアイテム ID を一覧表示（キャッシュ済みとは限らない） |
| `ListDataSources` | レジストリの編集時定義データソースを一覧表示 |
| `ListRuntimeSources` | レジストリの実行時展開後データソースを一覧表示 |
| `GetItems` | 指定名のキャッシュ済みアイテムを機密フィールドマスキング付きで取得。未キャッシュのアイテムは黙って省略せず `MissingItems` に理由付きで報告 |
| `GetAllCachedItems` | アイテム名を事前指定せず、現在キャッシュ済みの全アイテムを取得（1000件・1MiB を上限。Toolset に対応なし） |
| `AcquireItems` | 指定アイテムの非同期キャッシュロードをトリガー — カスタム/Remote ソースで必要（DataTable ソースは自動事前ロード済み。Toolset に対応なし） |

### Toolset ブリッジ（7 コマンド）🧩

`DataRegistryToolset` プラグイン（UE 5.8+）経由でネイティブコマンドのうち先頭7個をミラー。プロバイダ: `Toolset.Editor.DataRegistry.*`。`GetItems` はここでは挙動が異なる: 見つからないアイテムは黙って省略され、機密マスキングも適用されない — マスキングや欠損明示が必要な場合はネイティブの `GetItems` を使用すること。

> `ListRegistries` は `StructFilter` を引き続き文字列で受けます。ブリッジは Toolset へ `{"refPath": ...}` で送り、空または省略のときは何も送りません（フィルタなし）。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.DataRegistry.ListRegistries` | `DataRegistryToolset` への passthrough |
| `Toolset.Editor.DataRegistry.GetRegistryInfo` | `DataRegistryToolset` への passthrough |
| `Toolset.Editor.DataRegistry.GetSchema` | `DataRegistryToolset` への passthrough（生 JSON 文字列、`IsSecret` フラグなし） |
| `Toolset.Editor.DataRegistry.ListItems` | `DataRegistryToolset` への passthrough |
| `Toolset.Editor.DataRegistry.ListDataSources` | `DataRegistryToolset` への passthrough |
| `Toolset.Editor.DataRegistry.ListRuntimeSources` | `DataRegistryToolset` への passthrough |
| `Toolset.Editor.DataRegistry.GetItems` | `DataRegistryToolset` への passthrough。欠損アイテムは黙って省略、マスキングなし |

---

## UAIP.Editor.MotionMatching 🧩

Pose Search プラグイン向けの Motion Matching 編集機能 — `UPoseSearchDatabase` へのアニメーション登録、`UPoseSearchSchema` の構造（ロール付きスケルトンとフィーチャーチャンネルツリー）、`UPoseSearchNormalizationSet` のメンバーシップ、非同期インデックスビルド。`PoseSearch` プラグインが必要。

> **Note**: このドメインの編集系コマンドは、自分自身の変更が反映された時点で `Success: true` を返す。これは Schema の `Finalize()` が後続で失敗して巻き戻る場合（スケルトンが未割り当て、あるいは `UPoseSearchFeatureChannel_Group` が空になった場合など）でも同じ。インデックスが構築できる状態かどうかは `Success` 単体ではなく応答の `bSchemaReadyForIndexBuild` を確認すること — ロール付きスケルトンが 1 つもない Schema は、チャンネルをいくつ追加しても `bSchemaReadyForIndexBuild: false` のままなので、先に `AddSkeletonToPoseSearchSchema` でスケルトンを設定すること。`bSchemaReadyForIndexBuild` が保証するのはこの Schema 単体の前提条件のみで、実際のインデックスビルドには Database 側が Schema を参照していること（`SetPoseSearchDatabaseSchema`）とアニメーションが登録済みであること（`AddAnimationToPoseSearchDatabase`）も必要。

### Database（6 コマンド）

| コマンド | 説明 |
|---|---|
| `GetPoseSearchDatabaseInfo` | `UPoseSearchDatabase` の構造情報を取得 — Schema/NormalizationSet 参照、PoseSearchMode、PCA/KDTree 設定、`AnimationAssets` の各エントリ（パス・クラス・有効フラグ・ミラーオプション・サンプリング範囲/グリッド）。Chooser 内包データベースは拒否 |
| `AddAnimationToPoseSearchDatabase`（要 `PoseSearchAssetEdit`） | アニメーションアセットを `InsertAt` に追加。任意のエントリ設定（有効フラグ・ミラーオプション・サンプリング範囲/グリッド）を指定可能。通常（非 BranchIn）エントリとしてすでに登録済みの場合は既定で冪等。`bAllowDuplicate: true` を指定するとこの判定を迂回し、常に新しいエントリを追加する |
| `RemoveAnimationFromPoseSearchDatabase`（要 `PoseSearchAssetEdit`） | 指定アニメーションアセットを参照する全エントリを削除。全体成功/全体失敗方式 — 一致したエントリのいずれかが PoseSearchBranchIn アニメーション通知で作成されたものだった場合は失敗 |
| `SetPoseSearchDatabaseAnimationSettings`（要 `PoseSearchAssetEdit`） | 既存の `AnimationAssets` エントリ 1 件の設定を部分更新。アニメーションパスで対象を解決し、必要な場合は `Index` で一意化。UE 5.8 限定（UE 5.7 では `Available: false`） |
| `SetPoseSearchDatabaseSchema`（要 `PoseSearchAssetEdit`） | データベースの `Schema` 参照を設定。既存の Schema を差し替えるには `bAllowOverwrite` が必要 |
| `SynchronizePoseSearchDatabase`（要 `PoseSearchAssetEdit`） | PoseSearchBranchIn アニメーション通知を持つ全 `UAnimSequenceBase` の `BranchInId != 0` エントリを、データベースの `AnimationAssets` へ明示的にマージする。エンジンにはこのマージが自動的に起きたことを観測できる確実な手段がないため、`PoseSearchBranchIn` 通知の追加・編集後（アニメーションアセットの保存後）、`GetPoseSearchDatabaseInfo` を読む前に本コマンドを呼ぶこと。⚠️ 保存と同じリクエスト内で呼ぶと 0 件になる場合がある — アセットレジストリの参照インデックスは保存後に非同期で再構築されるため、保存が落ち着いてから再実行すること。冪等 — マージ対象がなければデータベースは変更されない。Chooser 内包データベースは `NotAllowed` で拒否 |

### Schema（11 コマンド）

| コマンド | 説明 |
|---|---|
| `GetPoseSearchSchemaInfo` | `UPoseSearchSchema` の構造情報を取得 — SampleRate、DataPreprocessor、SchemaCardinality、ロール付き `Skeletons` 配列、`Finalize()` 展開後の `Channels` 配列、そして編集系コマンドが実際に対象とする finalize 前の `RawChannels` ツリー（`ChannelPath` / `ClassPath`）。各 `RawChannels[]` エントリ（ネストしたものも含む）は `Admission` / `RequiredCapabilities` / `MissingCapabilities` も返すようになった — そのチャンネルのプロパティを編集する場合の基準で判定される。詳細は下の Note を参照 |
| `SetPoseSearchSchemaDataPreprocessor`（要 `PoseSearchAssetEdit`） | `DataPreprocessor` を変更（`None` / `Normalize` / `NormalizeOnlyByDeviation` / `NormalizeWithCommonSchema`）。応答にはこの Schema を参照していると見つかった全データベース（ベストエフォート）を列挙 |
| `AddPoseSearchSchemaChannel`（要 `PoseSearchAssetEdit`） | `ChannelClass` のチャンネルを作成し、チャンネルツリーへ挿入。任意で `ParentChannelPath` の下へネストし、`InsertAt` で挿入位置を指定可能。冪等ではない — 同じクラスで 2 回呼ぶとチャンネルが 2 つできる。`/Script/PoseSearch` 以外のモジュール由来のクラスにはさらに `MotionMatchingCustomTypeEdit` が必要 — 詳細は下の Note を参照 |
| `RemovePoseSearchSchemaChannel`（要 `PoseSearchAssetEdit`） | `ChannelPath` のチャンネルを、ネストされた子孫チャンネルもろとも削除。任意の `ExpectedChannelClass` で、古いパスによる誤削除を防止できる。削除対象のチャンネル、またはネストする子孫のいずれかのクラスがこのドメインの出荷対象外の場合は `MotionMatchingCustomTypeEdit` が必要 |
| `MovePoseSearchSchemaChannel`（要 `PoseSearchAssetEdit`） | `SourceChannelPath` のチャンネルを、その親の中で `TargetIndex` へ並べ替え。別の親への移動は非対応 — 削除して追加し直すこと。移動対象のチャンネル自身のクラスがこのドメインの出荷対象外の場合は `MotionMatchingCustomTypeEdit` が必要 — ネストする子孫は並べ替えで動かないため再確認しない。`TargetIndex` が現在位置と同じ（no-op になる）場合も確認は行われるため、権限のないセッションがこの確認を回避してゲート済みチャンネルの位置を探ることはできない |
| `SetPoseSearchSchemaChannelProperty`（要 `PoseSearchAssetEdit`） | `ChannelPath` のチャンネルのトップレベルプロパティへ書き込む — `Value`（UE テキストインポート形式、最大 4 KiB）または `ValueJson`（JSON）で値を渡し、`Operation` / `ElementIndex` / `ElementKeyJson` でコンテナの要素 1 つを操作できる（[参照・構造体・コンテナの書き込み](#参照構造体コンテナの書き込み) を参照）。構造体・コンテナにはさらに `PropertyStructuredEdit` が必要。参照を内包する型はセッションの保有 Capability に関わらず `PolicyViolation` で拒否される — チャンネルのサブチャンネル配列へ直接書けると `AddPoseSearchSchemaChannel` のクラス許可リストを迂回できてしまうため、チャンネルの追加は専用コマンドで行うこと。書き込み後の検証に失敗した場合は書き込みをロールバック。チャンネル自身のクラス、または書き込み対象プロパティを宣言しているクラスのいずれかがこのドメインの出荷対象外の場合は `MotionMatchingCustomTypeEdit` が必要 — なぜこれが新規の制限なのかは下の Note を参照 |
| `AddDefaultPoseSearchSchemaChannels`（要 `PoseSearchAssetEdit`） | エディタの Schema ファクトリが作成するのと同じ既定チャンネル（Trajectory + Pose）を追加。既存チャンネルは削除されず維持される — 2 回呼ぶと重複したペアが追加される。追加されるのは常にエンジン自身の 2 チャンネルで呼び出し元が指定できるクラスは無いため、`MotionMatchingCustomTypeEdit` は一切要求しない |
| `GetAvailablePoseSearchChannelClasses` | 構造的なチェックだけでチャンネルとして認められる `UPoseSearchFeatureChannel` サブクラスをすべて一覧表示する — `AddPoseSearchSchemaChannel` が `ChannelClass` を解決する集合と同じ — このセッションが今すぐ配置できるかどうかを問わない。各エントリは `Admission`（`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`）と `RequiredCapabilities` / `MissingCapabilities`、そして有効な `ParentChannelPath` の対象を示す `bCanHostSubChannels` を返す。エントリはフルクラスパス（`/Script/<Module>.<Class>`）順に整列され、アーティファクトは `TotalCount`、`ReturnedCount`、`Truncated`（上限 500）を報告する。Heavy コマンド — ロード済みの全 `UClass` を走査するため、結果をキャッシュすること |
| `GetPoseSearchChannelClassSchema` | チャンネルクラスの Details パネル表示プロパティを一覧表示。各プロパティは入れ子の `WriteRequirements` オブジェクトを持ち、`SetPoseSearchSchemaChannelProperty` で書き込み可能かを `IsWritable` / `RefusalReason` で示し、`WriteInputForm`（`TextOrJson` / `JsonOnly` / `None`）と、構造化形式での書き込みが要求する `RequiredCapabilities` / `HeldCapabilities` / `MissingCapabilities` を返す（[書き込みに何が必要かを知る](#書き込みに何が必要かを知る)を参照）。`DefaultValueText` はそのまま使えるテキストインポート形式の例を提供 |
| `AddSkeletonToPoseSearchSchema`（要 `PoseSearchAssetEdit`） | `Role` のロール付きスケルトンエントリを追加または置き換え。任意で `MirrorDataTablePath` を指定可能。既存の `Role` を置き換えるには `bAllowOverwrite` が必要 |
| `RemoveSkeletonFromPoseSearchSchema`（要 `PoseSearchAssetEdit`） | `Skeletons` 配列から `Role` のロール付きスケルトンエントリを削除 |

> **Note**: `AddPoseSearchSchemaChannel` の `ChannelClass`、および各編集コマンドの `ExpectedChannelClass` には**完全修飾クラスパス**（例: `/Script/PoseSearch.PoseSearchFeatureChannel_Position`）を渡すこと — `GetPoseSearchSchemaInfo` の `RawChannels[].ClassPath` または `GetAvailablePoseSearchChannelClasses` の `ClassPath` を使い、同じエントリの短い `ChannelClass` フィールドは使わないこと。`ChannelPath` は `RawChannels[]` に対する `/` 区切りのインデックスパス（例: `"0"`、`"2/0"`）であり、`Finalize()` 展開後の `Channels[]` に対するものでは**ない**。編集のたびに後続の兄弟チャンネルの `ChannelPath` がずれうるため、呼び出し前に取得したパスを使い回さず、都度 `RawChannels` を読み直すこと。
>
> **Note — このドメインはチャンネルクラスを 1 箇所、1 つの Capability（`MotionMatchingCustomTypeEdit`）だけでゲートします。** チャンネルクラスの配置・削除・操作と、書き込み対象のチャンネルプロパティを宣言するクラスは同じ基準で判定され、名前も共有する — プロジェクト自身のチャンネルは自分自身のプロパティを宣言するため、プロパティ面に別の Capability を要求する理由がない。`/Script/PoseSearch` 以外のクラス（プロジェクトモジュール、プラグインモジュール、Blueprint 生成クラス）で必要になる。Blueprint 生成のチャンネルクラスはこの Capability を保有していても常に拒否される — このドメインが解禁できる種類のカスタム型ではない。このドメインには「危険な型」用の対になる Capability は存在しない — チャンネルクラスの `Finalize` / `BuildQuery` / `IndexAsset` はそのクラスの作者が書いたコードであり、リクエストが持ち込むものではない。既定では付与されない。[Safety & Capabilities](safety.md#motion-matching--pose-search-編集) を参照。
>
> **Schema に既に置かれているプロパティへの書き込みにも、この Capability が新たに必要になりました — これは既存の制限の維持ではなく、新規の制限です。** この変更以前、`SetPoseSearchSchemaChannelProperty` はプロパティの書き込みフラグと値種別だけを確認しており、プロジェクト定義チャンネルの自身のプロパティは Capability なしで書き込めていた。宣言クラスが `/Script/PoseSearch` 自身でない場合、今後は `MotionMatchingCustomTypeEdit` も必要になる。
>
> **チャンネルの削除・移動も追加と同様にゲートされ、インデックスビルドの開始もゲートされます。** `RemovePoseSearchSchemaChannel` と `MovePoseSearchSchemaChannel` は従来、チャンネルのクラスに関わらずアセットへ到達できていたが、今後は同じ Capability があらためて確認される。削除はそれが持ち去るネストしたサブツリー全体について判定される（すべての子孫が一緒に消えるため）。移動は移動対象のチャンネル自身のクラスだけを判定する（並べ替えではネストしたものは一切動かないため）。`StartPoseSearchDatabaseIndexBuild` も同じ理由でゲートされる — エンジン自身のビルドパイプラインは対象 Schema が保持する全チャンネルクラスのコードを実行するため、ビルドの開始はそれらのクラスを追加するのと同じ基準で判定される。Schema が保持する全クラスが確認対象であり、追加時に呼び出し元が指定したクラスだけではない。
>
> ⚠️ **破壊的変更**: このドメインの出荷対象外のチャンネルクラスは、従来は無条件で `PolicyViolation` として拒否されており、`RemovePoseSearchSchemaChannel` / `MovePoseSearchSchemaChannel` / `SetPoseSearchSchemaChannelProperty` は出自を理由にした拒否を一切行っていなかった。今後は `AddPoseSearchSchemaChannel` / `RemovePoseSearchSchemaChannel` / `MovePoseSearchSchemaChannel` / `SetPoseSearchSchemaChannelProperty` / `StartPoseSearchDatabaseIndexBuild` が `CapabilityNotAvailable` を返し不足している Capability 名を明示するようになった — そして Capability を付与すれば実際に成功するようになった（従来の `AddPoseSearchSchemaChannel` の実装ではそうならなかった）。現在ロードされていないクラスパスは引き続き `NotFound` になる — このドメインは未解決のクラスを副作用として読み込むことは一切ない。
>
> ⚠️ **破壊的変更 — `GetAvailablePoseSearchChannelClasses` の応答形状が変わりました。** `NumClasses` フィールド（アーティファクト・`CommandResponse.Result` の両方）が廃止され、`CommandResponse.Result` 自体も設定されなくなった。代わりにアーティファクト上の `TotalCount` / `ReturnedCount` / `Truncated` を読むこと。一覧はまた、`MotionMatchingCustomTypeEdit` でゲートされたクラスを黙って除外しなくなった — `AddPoseSearchSchemaChannel` が答えるのと同じ基準で `Admission: RequiresCapabilities` として一覧に載り、必要な Capability が名指しされる。フルクラスパスによる整列後に新設された 500 件の上限が適用される（従来は上限なし）。
>
> **`GetPoseSearchSchemaInfo` の `RawChannels[]` エントリは、ネストしたものも含めて `Admission` / `RequiredCapabilities` / `MissingCapabilities` を新たに返すようになりました** — 各チャンネル自身のクラスについて、`SetPoseSearchSchemaChannelProperty` / `RemovePoseSearchSchemaChannel` が問うのと同じ質問。追加のみで、既存フィールドはすべて変更されていません。

### NormalizationSet（4 コマンド）

| コマンド | 説明 |
|---|---|
| `GetPoseSearchNormalizationSetInfo` | `UPoseSearchNormalizationSet` の `Databases` 配列（`Index` / `DatabasePath` / `bIsNull`）を格納順で一覧表示 |
| `SetPoseSearchDatabaseNormalizationSet`（要 `PoseSearchAssetEdit`） | データベースの `NormalizationSet` 参照を設定またはクリア（`NormalizationSetPath` と `bClearNormalizationSet` は排他）。データベース側のみを編集する — 両側を一致させたい場合は `AddDatabaseToPoseSearchNormalizationSet` と併用すること |
| `AddDatabaseToPoseSearchNormalizationSet`（要 `PoseSearchAssetEdit`） | `UPoseSearchNormalizationSet` の `Databases` 配列にデータベースを追加。冪等。NormalizationSet 側のみを編集する — `SetPoseSearchDatabaseNormalizationSet` と併用すること |
| `RemoveDatabaseFromPoseSearchNormalizationSet`（要 `PoseSearchAssetEdit`） | 指定データベースを参照する全スロットを削除。一致したスロットは詰めずに null にクリアされるため、他のスロットの `Index` は変化しない |

### Index Build（2 コマンド）

| コマンド | 説明 |
|---|---|
| `StartPoseSearchDatabaseIndexBuild`（要 `PoseSearchAssetEdit`） | データベースのインデックスビルドを非同期で開始し、ポーリング用の `BuildId` を返す。対象データベースによらずエディタ全体で同時に走るビルドは 1 件のみ |
| `GetPoseSearchDatabaseIndexBuildStatus` | 1 件のビルドの `State`（`Running` / `Succeeded` / `Failed`）と `ElapsedSeconds` を取得。`Succeeded` になると `NumPoses` / `SchemaCardinality` も報告 |

> **Note**: `StartPoseSearchDatabaseIndexBuild` と `GetPoseSearchDatabaseIndexBuildStatus` は、いずれも明示的な `SessionId` を指定して呼び出す必要があり、両方で**同じ** `SessionId` を使うこと。自動生成されるセッションは呼び出しごとに異なるため、そのセッションで開始したビルドを後からポーリングできない。両コマンドとも、匿名または未指定の `SessionId` を `InvalidParams` で拒否する。

---

## UAIP.Editor.Chooser 🧩

`UChooserTable` アセットのオーサリング — 行・列・各行が各列に持つセル・行が選択する結果オブジェクト・列が何を参照するかを決める入力バインディング。**Chooser** プラグインが必要。

アドレッシングは位置ベース。`ColumnIndex` / `RowIndex` は読み取り系コマンドが報告する現在の 0 始まりインデックスであり、存在しないインデックスはテーブルの現在の件数を添えた `InvalidParams` で拒否される。値は往復可能で、読み取りがセルの `Value`・行の `ResultType` / `ResultValue`・列の入力バインディングとして報告した内容が、そのまま対応する書き込みの入力になる。したがって、ある行・列・テーブルから読んだ値を別のものへそのまま書き込める。

> **Note**: 以下の編集系コマンドはすべて任意の `Fingerprint`（読み取り系コマンドが報告する構造フィンガープリント）を受け取る。テーブルの現在の構造と一致しなくなっている場合、編集は `Conflict` で拒否され、再実行に使う現在値が応答に含まれる。`CompileChooserTable` のみ例外で、行も列も触らないため `Fingerprint` を受け取らない。編集系はすべて、プレイセッション実行中および `/Game/` 外のアセットに対して拒否される。
>
> `ChooserTableEdit` に加えて、編集は「実際に何を指定したか」に応じて呼び出しごとに判定される。**`ChooserCustomTypeEdit`**: 列の型・結果の型・入力バインディングの型が、本ドメインが標準で提供するモジュール群の外から来ている場合（書き込む型だけでなく、すでにテーブルに入っている型についても判定される）。**`ChooserReferenceEdit`**: オブジェクト参照を保持できる型に対して値を指定した場合。**`ChooserFunctionBindingEdit`**: プロパティチェーンが、評価パスが呼び出す関数へ解決される場合（プレーンなプロパティではなく）。chooser エディタが関数を提示しないバインディング経由で関数に到達するチェーンは、Capability では解除できない `NotAllowed` として拒否される。以下の一覧系コマンドが返す `Admission` フィールドが、型ごとに「その型を指定した呼び出しに何が必要か」を報告する。

| コマンド | 説明 |
|---|---|
| `GetChooserTableInfo` | テーブル全体のサマリ: 行数・列数、出力の種別とそれを制約するクラス、コンテキストパラメータ数、フォールバック結果の有無とその内容、構造フィンガープリント。構造のみで、行・列・セルの値は報告しない。読み取り専用、`EditorInspect` が必要 |
| `GetChooserTableRow` | 1 行分: 結果オブジェクト・無効フラグ・列ごとに 1 件のセルエントリと、テーブルの現在の件数およびフィンガープリント。行ごとのデータを保持しない列、またはプレーンな値として往復できない列のセルは、省略ではなく `Value` を null にし `bCellValueUnavailable` を立てて報告する。読み取り専用、`EditorInspect` が必要 |
| `ListChooserTableRows` | 行を 1 ページ分（各行の結果オブジェクト・無効フラグ・列ごとのセル）JSON artifact として返す。`StartIndex` / `Count` でページングする。範囲外の `StartIndex` はエラーではなく空または短いページを返すため、空ページが返るまで辿れば終端が分かる。読み取り専用、`EditorInspect` が必要 |
| `ListChooserColumns` | 全列を JSON artifact として返す（インデックス・列自身の型・参照先を決める入力バインディング・無効かどうか・セルがプレーンな値として往復できるか）。テーブルの件数とフィンガープリントも報告する。ここで報告される `ColumnIndex` が、列を対象とする全編集コマンドの受け取るインデックス。読み取り専用、`EditorInspect` が必要 |
| `ListChooserContextData` | テーブルの評価コンテキストが宣言する全コンテキストパラメータ（列の入力バインディングの向け先候補）を、それぞれのインデックス・公開する型・読み取り/書き込み/両方の区別とともに返す。ネストされたテーブルの場合は chooser チェーンのルートから解決する。読み取り専用、`EditorInspect` が必要 |
| `ListChooserColumnTypes` | 現在検出されている `FChooserColumnBase` 派生構造体をすべて返す（chooser エディタの Add Column メニューが提示するものと同じ集合）。結果の `ClassPath` を `AddChooserColumn` の `ColumnType` に渡す。各エントリは `Admission`（`Allowed` / `RequiresCapabilities` / `NotAddable` / `CompatibilityUnknownUntilAuthorized`）と `RequiredCapabilities` / `MissingCapabilities` を持ち、`TotalCount` / `ReturnedCount` / `Truncated` が上限による打ち切りの有無を報告する。`ClassPath` 順で並ぶため、打ち切られた結果でも常に同じ先頭集合になる。`AssetPath` は任意で一覧を絞り込まないが、指定した場合は解決され、実在する chooser テーブルでなければ `NotFound` で拒否される。読み取り専用、`EditorInspect` が必要 |
| `ListChooserResultTypes` | `AddChooserTableRow` / `SetChooserTableResult` / `SetChooserFallbackResult` が `ResultType` として受け取る `FObjectChooserBase` 派生構造体をすべて返す（現在のセッションが使用できるかどうかに関わらず）。`AssetPath` は受け取るが解決しない（結果型のファミリはどのテーブルでも同じため）。`Admission` / 件数 / 並び順の契約は `ListChooserColumnTypes` と同じ。読み取り専用、`EditorInspect` が必要 |
| `ListChooserInputTypes` | `ColumnIndex` が指す列にバインドできる入力バインディング型をすべて返す（エディタのバインディングウィジェットが提示する候補と同じ）。結果の `ClassPath` を `SetChooserColumnInput` に渡す。上記 2 つの一覧と異なり候補が指定した列に完全に依存するため、`AssetPath` と `ColumnIndex` の両方が必須。主入力を持たない列（エディタからも author がバインドできない列）は拒否ではなく空の一覧として報告される。`Admission` / 件数 / 並び順の契約は同じ。読み取り専用、`EditorInspect` が必要 |
| `AddChooserColumn`（`ChooserTableEdit` が必要） | 指定した型の列を 1 つ追加し、収まったインデックス・追加後の件数・新しいフィンガープリントを報告する。新しい列には既存の行ごとに 1 つのセルが与えられるため、テーブルは既存の全行に対して引き続き回答できる。`ColumnType` は `ListChooserColumnTypes` が報告する型のいずれかである必要がある。`InsertAt` で位置を指定し、省略すると末尾に追加する |
| `RemoveChooserColumn`（`ChooserTableEdit` が必要） | 列 1 つを、それが保持するセルごと削除する。各列は自身のセルのみを保持するため、他の列は影響を受けない |
| `MoveChooserColumn`（`ChooserTableEdit` が必要） | 列 1 つを、保持する全セルごと `ToIndex` の位置へ移動する。`ToIndex` は移動**後**に列が占める位置であり、移動前の位置ではない。自身の現在のインデックスへの移動は成功する no-op |
| `SetChooserColumnInput`（`ChooserTableEdit` が必要） | 列の入力バインディング（その列が何を参照するかを決めるパラメータ）を設定する。`InputType` / `InputValue` は `ListChooserColumns` が列について報告した内容をそのまま受け取る。`InputValue` を null にすると指定型自身のデフォルトが書き込まれ、これはエディタでパラメータ型を選んだ直後の未バインド状態と同じ。`InputType` は**その列について** `ListChooserInputTypes` が報告する型のいずれかである必要があり、列が値として読めないファミリの型は `InvalidParams` で拒否される。入力バインディングを一切持たない列に対しては、あらゆる型が同様に拒否される |
| `AddChooserTableRow`（`ChooserTableEdit` が必要） | 行を 1 つ追加し、収まったインデックスを報告する。`InsertAt` で位置を指定し、省略すると末尾に追加する。`ResultType` / `ResultValue` は読み取り系コマンドが報告するのと同じ形で新しい行に結果オブジェクトを与えるため、あるテーブルから読んだ行を別のテーブルへ追加できる。両方省略すると結果が空の行を追加する |
| `RemoveChooserTableRows`（`ChooserTableEdit` が必要） | 1 つ以上の行を単一の変更として削除する。`RowIndices` は削除対象の行を現在のインデックスで列挙する。順序は問わないが、各エントリは相異なりかつ範囲内である必要があり、そうでなければリクエスト全体が拒否される。複数行の削除は 1 つの変更なので、1 回の Undo ですべて復元される |
| `MoveChooserTableRow`（`ChooserTableEdit` が必要） | 行 1 つを、その結果・無効フラグ・全列のセルごと `ToIndex` の位置へ移動する。`ToIndex` の「移動後の位置」という意味は `MoveChooserColumn` と同じ |
| `SetChooserTableCell`（`ChooserTableEdit` が必要） | セルを 1 つ書き込む（ある行がある列に持つ値）。行ごとのデータを保持しない列、またはセルがプレーンな値として往復できない列（読み取りが `bCellValueUnavailable` を立てて報告する列）は、書き込まれず拒否される |
| `SetChooserTableResult`（`ChooserTableEdit` が必要） | 1 行が選択する結果オブジェクトを差し替える。`ResultType` を省略または空にすると、再構築ではなく行の結果を空にする（エディタの結果ピッカーが行を戻す状態と同じ）。この場合 `ResultValue` は省略または null である必要がある。行が保持していたネスト chooser は新しい結果の書き込み前にテーブルから登録解除され、書き込まれるネスト chooser は書き込み後に登録されるため、所有権は差し替えに追随する |
| `SetChooserFallbackResult`（`ChooserTableEdit` が必要） | どの行にもマッチしなかったときにテーブルが返す結果（エディタの Fallback Result）を差し替える。フォールバックは行ではなくテーブルに属するため、このコマンドはインデックスを取らない。`ResultType` 省略による空化とネスト chooser の所有権の扱いは `SetChooserTableResult` と同じ |
| `SetChooserRowDisabled`（`ChooserTableEdit` が必要） | 行 1 つを評価対象から外す / 戻す。行を移動せず、結果も変更せず、セルにも一切触れない。フィンガープリントも変化しない（行の無効フラグはフィンガープリントが記述する対象ではないため）。列・結果・入力バインディングの型を一切指定しないコマンドのため、必要なのは `ChooserTableEdit` のみ |
| `CompileChooserTable`（`ChooserTableEdit` が必要） | テーブルを明示的にコンパイルする。アセット保存時にコンパイルは強制されないため、本ドメインの他コマンドで行った編集は、何かが再コンパイルを要求するまで列の入力バインディングが古いオフセットに解決されたまま残ることがある。このコマンドはそのためにある。テーブルに既にある列・結果・バインディングの型を出自の観点で再判定することはなく、テーブルが保持する全入力バインディングを、本ドメインの全書き込みが使うのと同じバインディングチェーン解決器に通すだけ。そのうち 1 つでも評価パスが呼び出す関数へ解決される場合、追加で `ChooserFunctionBindingEdit` が必要になる |

---

## UAIP.Editor.AnimSequence

`UAnimSequence` / `UAnimMontage` / `UAnimComposite` アセットの AnimNotify / AnimNotifyState エントリと通知トラックの追加・削除・編集。エンジン標準の型のみで構成されており、オプションプラグインは不要。

> **Note**: `NotifyGuid` はハイフンなしの 32 桁 16 進数（`FGuid::ToString(EGuidFormats::Digits)`）— `GetAnimNotifyInfo` が報告し、本ドメインの他の全コマンドが受け取る形式と同じ。`SetAnimNotifyProperty` はすべての書き込みで `AnimNotifyEdit` を必要とし、書き込むプロパティが参照であるか、それを内包する場合は追加で `AnimNotifyReferenceEdit` が（`GetAnimNotifyClassSchema` がプロパティごとに `bIsObjectReference` として報告）、値カタログ外の構造体・配列・セット・マップ・オプショナルの場合はさらに `PropertyStructuredEdit` が必要。`GetAnimNotifyClassSchema` は両者をプロパティごとに `WriteRequirements.RequiredCapabilities` として、値をどちらの入力欄で渡すかを `WriteRequirements.WriteInputForm` として返す。`GetAnimNotifyProperty` も同じ内容を同じ形で、通知インスタンス自体に対して判定して返す。`GetAnimNotifyProperty` は読み取り専用の対となるコマンドで、`NotifyGuid` / `PropertyName` によるアドレッシングも、`SetAnimNotifyProperty` の `Value` および `GetAnimNotifyClassSchema` の `DefaultValueText` と同じテキスト形式も共通であり、ゼロ値のプロパティ（空文字列ではなく "0" / "False" / "None"）も含めて 3 コマンド間でバイト単位に往復できる。本ドメインの編集系コマンドはすべて、PIE または SIE 実行中は拒否される。

| コマンド | 説明 |
|---|---|
| `GetAnimNotifyInfo` | アセット上の全通知トラック（`TrackIndex` / `TrackName` / `TrackColor`）と全通知/通知ステートエントリ（guid・クラス・タイミング・Montage 固有フィールド）、およびアセットレベルのスカラー値（`AssetKind` / `PlayLength` / `NumTracks` / `NumNotifies` / `NumInvalidGuids`）を取得。`UAnimComposite` の場合、対象はアセット自身の `Notifies` 配列のみで、セグメントの `AnimSequence` が持つ通知は含まれない。読み取り専用、要 `EditorInspect` |
| `GetAvailableAnimNotifyClasses` | `AddAnimNotify` / `AddAnimNotifyState` が `ClassPath` として受け付ける全 `UAnimNotify` / `UAnimNotifyState` サブクラスを一覧表示。`bIsNotifyState` / `bCanBePlaced` / `NotPlaceableReason` を付与。現在ロード済みのクラスのみが対象。Heavy コマンド — ロード済みの全 `UClass` を走査するため、結果をキャッシュすること。読み取り専用、要 `EditorInspect` |
| `GetAnimNotifyClassSchema` | `UAnimNotify` / `UAnimNotifyState` サブクラスの Details パネル表示プロパティを一覧表示。各プロパティは入れ子の `WriteRequirements` オブジェクトを持ち、`SetAnimNotifyProperty` で書き込み可能かを `IsWritable` / `RefusalReason` で示し、`WriteInputForm`（`TextOrJson` / `JsonOnly` / `None`）と `RequiredCapabilities` / `HeldCapabilities` / `MissingCapabilities` を返す（[書き込みに何が必要かを知る](#書き込みに何が必要かを知る)を参照）。加えて `bIsObjectReference` と、そのまま使えるテキストインポート形式の例 `DefaultValueText` を提供。読み取り専用、要 `EditorInspect` |
| `GetAnimNotifyProperty` | `NotifyGuid` で識別される通知インスタンスについて、プロパティ 1 件（`PropertyName`）、または省略時・空文字時は `GetAnimNotifyClassSchema` が列挙する全プロパティを読み取る。全件読み取りは `PropertyName` / `Value` の代わりに `NumProperties` / `bTruncated` を報告し、上限超過時は切り詰める。単一プロパティ読み取りは切り詰めず、上限超過は `InvalidParams` で拒否する。秘密扱いの値は `GetAnimNotifyClassSchema` の `DefaultValueText` や `SetAnimNotifyProperty` の `AppliedValue` と同じ方式でマスクされる。各プロパティは入れ子の `WriteRequirements` オブジェクトも持ち（`GetAnimNotifyClassSchema` と同じキー名・同じ入れ子の形。判定はクラスのデフォルトではなく通知インスタンスに対して行われる）、`IsWritable` / `RefusalReason`、`WriteInputForm`（`TextOrJson` / `JsonOnly` / `None`）、`RequiredCapabilities` / `HeldCapabilities` / `MissingCapabilities` を返す。単一プロパティ読み取りでは `Data` に直接載る（[書き込みに何が必要かを知る](#書き込みに何が必要かを知る)を参照）。アセットを変更しない。読み取り専用かつ冪等、要 `EditorInspect` |
| `AddAnimNotifyTrack`（要 `AnimNotifyEdit`） | `TrackName` という名前の通知トラックが存在することを保証し、存在しない場合は作成する（任意の `TrackColor`、既定は白）。既存判定に対して冪等 — 既存トラックの `TrackIndex` はそのまま返され、`TrackColor` は無視される。PIE/SIE 実行中は拒否 |
| `RemoveAnimNotifyTrack`（要 `AnimNotifyEdit`） | `TrackName` という名前の通知トラックを削除し、その上に置かれた全通知も削除する。以降のトラックのインデックスは 1 つずつ繰り上がる — 応答の `RemovedNotifyGuids` / `ReindexedNotifies` が影響範囲全体を報告する。すでに削除済みのトラックには `NotFound` で失敗。PIE/SIE 実行中は拒否 |
| `AddAnimNotify`（要 `AnimNotifyEdit`） | `TrackName` の `StartTime` へ単発の点通知を追加する。`ClassPath`（`UAnimNotify` サブクラス）/ `NotifyName`（クラスなし、`bRegisterOnSkeleton` で Skeleton へ任意登録可能）のいずれか一方が必須。冪等ではない — 繰り返し呼ぶと新しい `NotifyGuid` を持つ独立した通知が作成される。PIE/SIE 実行中は拒否 |
| `AddAnimNotifyState`（要 `AnimNotifyEdit`） | `TrackName` へ `[StartTime, StartTime + Duration]` にまたがる単発の通知ステートを追加する。`ClassPath` は `UAnimNotifyState` サブクラスを解決する必要がある。冪等ではない — 繰り返し呼ぶと新しい `NotifyGuid` を持つ独立した通知ステートが作成される。PIE/SIE 実行中は拒否 |
| `RemoveAnimNotify`（要 `AnimNotifyEdit`） | `NotifyGuid` で識別される通知を 1 件だけ削除する。任意の `ExpectedNotifyClassPath` / `ExpectedNotifyName` は楽観的並行性制御のガード。guid が解決できなくなった場合は no-op 成功ではなく `NotFound` で失敗する。PIE/SIE 実行中は `NotAllowed` で拒否 |
| `SetAnimNotifyEvent`（要 `AnimNotifyEdit`） | `NotifyGuid` で識別される通知のイベントフィールド（`StartTime` / `Duration` / `TrackName` / `NotifyName` / `MontageTickType` / トリガー・フィルタ設定）を部分更新する — 指定したフィールドのみが変更される。`Duration` は点通知に対しては拒否、`MontageTickType` は `UAnimMontage` 以外では拒否。PIE/SIE 実行中は `NotAllowed` で拒否 |
| `SetAnimNotifyProperty`（要 `AnimNotifyEdit`。ハードなオブジェクト/クラス参照の書き込みは追加で `AnimNotifyReferenceEdit` が必要） | `NotifyGuid` で識別される通知インスタンスのトップレベルプロパティ 1 件を、`GetAnimNotifyClassSchema` が `DefaultValueText` として報告するのと同じテキストインポート形式で書き込む。新たに `FGameplayTag` / `FGameplayTagContainer` / `FGameplayCueTag`（未登録タグ、`Categories` / `GameplayTagFilter` の範囲外のタグ、コンテナ内の重複タグはいずれも `InvalidParams` で拒否）と `FBoneReference`（対象スケルトンに存在しないボーン名、または照合先スケルトンを解決できない場合は `InvalidParams` で拒否）も書き込み可能。ソフト/ウィーク/レイジー参照、マップ、セット、オプショナル、参照を含むものも含めたその他の構造体/配列は `ValueJson` で書き込み、コンテナの要素 1 つは `Operation` / `ElementIndex` / `ElementKeyJson` で指定する（[参照・構造体・コンテナの書き込み](#参照構造体コンテナの書き込み) を参照）。ハード参照の値は**既にロード済み**のアセットを指すもので、書き込みが副作用でアセットをロードすることはない。PIE/SIE 実行中は `NotAllowed` で拒否 |
| `FixupAnimNotifyGuids`（要 `AnimNotifyEdit`） | guid が現在無効な全通知に新しい guid を割り当てる。レガシー通知はこれを実行してアセットを保存するまで、リロードのたびに不安定な guid を持ち続ける。冪等 — 修復対象がない場合も `NumFixed: 0` で成功する。PIE/SIE 実行中は拒否 |
| `SelectAnimNotify`（要 `EditorUIAutomation`） | `NotifyGuid` で識別される通知を、すでに開いているそのアセットのアニメーションエディタ内で選択し、そのエディタの Details パネルにプロパティが表示されるようにする — エンジンに該当 API が無いため、通知のタイムラインウィジェットへ人間が行うクリックをシミュレートする。アセットは変更しない。UE 5.8 以降専用: UE 5.7 では通知ウィジェットの型とそのノードオブジェクトインターフェースが Persona モジュール内部限定のため、任意の通知を選ぶのではなく `Available: false`（`UnavailableDetail: "EngineVersion"`）を返す — [UnavailableDetail](#unavailabledetail--handlerunavailable-の8つの詳細理由) 参照。冪等 |

---

## UAIP.Editor.ChaosDestruction

Geometry Collection（Chaos Destruction）編集 — `UGeometryCollection` アセットの構造・階層・ダメージ設定の読み取り、アセットの新規作成・マージ、フラクチャ（Uniform / Voronoi / Plane / Slice / Brick / Mesh / Mesh Array）、ボーンのクラスタ階層編集、ジオメトリ属性のクリーンアップ・編集、ダメージモデルとクラスタリング設定の変更。Fracture Editor Mode のツール群に対応します。本ドメインに Toolset ブリッジはありません。

書き込み系コマンドは 3 つの DefaultDenied capability で保護されています — `GeometryCollectionCreate`（2 コマンド）、`GeometryCollectionFracture`（12 コマンド）、`GeometryCollectionEdit`（11 コマンド）。詳細は [Safety & Capabilities](safety.md) を参照してください。29 コマンド中 20 コマンド（🧩 印）は追加で `Fracture` プラグインを、1 コマンド（🧩 印）は `GeometryCollectionPlugin` を必要とします。印の無いコマンドにプラグイン依存はありません。書き込み系コマンドはすべて PIE/SIE 実行中は拒否され、また設定系・マージ系コマンド（`bAllowOverwrite` を使用）を除き、対象アセットが Dataflow グラフを参照している場合は `AllowOverwrite` を指定しない限り拒否されます。

#### Observation（4）— 要 `EditorInspect`

| コマンド | 説明 |
|---|---|
| `GetGeometryCollectionInfo` | 構造サマリ — `TransformCount`・`GeometryCount`・`HierarchyDepth`・`MaterialCount`・Dataflow グラフアセットのパス・未保存変更の有無・破壊設定サマリを取得 |
| `GetGeometryCollectionClusterInfo` | ボーン単位の階層をエントリ配列として取得（`BoneIndex`・`Parent`・`Children`・`SimulationType`・`BoneName`・`Level`・`BoundingBox`）。上限 256 件、超過時は `bTruncated` を設定 |
| `GetGeometryCollectionDestructionSettings` | 完全なダメージモデル・クラスタリング設定を取得 — `DamageModel`・階層レベルごとの `DamageThreshold` 配列・`SizeSpecificData`・クラスタリング設定 |
| `SelectGeometryCollectionBones` 🧩 | ボーン選択クエリを 1 件実行（`Root` / `Parent` / `Children` / `Siblings` / `Level` / `Contact` / `Leaf` / `Cluster` / `BySize` / `ByVolume` / `ByPercentage`）し、結果のボーンインデックス配列を返す。他コマンドの `BoneIndices` パラメータへそのまま渡せる。読み取り専用だが `Fracture` プラグインが必要 |

#### Creation（2）— 要 `GeometryCollectionCreate`

| コマンド | 説明 |
|---|---|
| `CreateGeometryCollectionFromStaticMesh` 🧩 | `UStaticMesh` を変換して新規 `UGeometryCollection` アセットを作成する。`ChaosEditor` プラグインが利用可能な場合はプロジェクトの Fracture Mode 既定設定を適用する。出力先パスが既存アセットと衝突する場合は拒否する。`GeometryCollectionPlugin` が必要。新規アセットは未保存のまま残る |
| `MergeGeometryCollectionAssets` | 片方のジオメトリをもう片方へ追加する（`UGeometryCollection::AppendGeometry`）。既存データはどちらのアセットでも失われない。2 つのアセットは異なる必要がある。対象アセットは未保存のまま残る |

#### Fracture（7）— 要 `GeometryCollectionFracture`、すべて 🧩

各コマンドは選択したボーン（`BoneIndices` 省略時はルート以下すべて）をフラクチャし、切断された各ボーンをフラクチャ片で置き換えます。

| コマンド | 説明 |
|---|---|
| `FractureGeometryCollectionUniform` 🧩 | 選択した全ボーンが 1 つのランダムなサイト配置を共有する Voronoi 図でフラクチャする。Fracture Editor Mode の Uniform ツールに対応 |
| `FractureGeometryCollectionVoronoi` 🧩 | 呼び出し側が指定した Voronoi サイト（全選択ボーンで共有）でフラクチャする |
| `FractureGeometryCollectionPlane` 🧩 | 1 つ以上の切断平面でフラクチャする — 明示的な平面（`CutPlaneTransforms`）とランダム配置の平面（`NumPlanes`）は加算方式 |
| `FractureGeometryCollectionSlice` 🧩 | 軸整列グリッド状の切断平面（`SlicesX` × `SlicesY` × `SlicesZ`）でフラクチャする。Slice ツールに対応 |
| `FractureGeometryCollectionBrick` 🧩 | レンガ状パターンの切断セルグリッドでフラクチャする。Brick ツールに対応 |
| `FractureGeometryCollectionWithMesh` 🧩 | 1 つの `UStaticMesh` を切断カッターとして使用し、`CutterMeshTransforms` エントリごとに 1 回フラクチャする。Mesh Cut ツールに対応 |
| `FractureGeometryCollectionWithMeshArray` 🧩 | 1 つ以上の `UStaticMesh` アセットを切断カッターとして使用してフラクチャする。`FractureGeometryCollectionWithMesh` を複数カッターメッシュに拡張したもの |

#### Cluster hierarchy（4）— 要 `GeometryCollectionEdit`

ボーンの再親子付け・リネーム・グループ化のみを行い、ジオメトリとトポロジーは変更されません。

| コマンド | 説明 |
|---|---|
| `ClusterGeometryCollectionBones` | 選択したボーンを新しいクラスタノードの下に再親子付けする（`NewNodeAtIndex` / `NewNodeWithParent` / `AllBonesUnderNewRoot`） |
| `AutoClusterGeometryCollection` 🧩 | 選択したボーンを自動的に新しいクラスタノードへグループ化する（`AutoCluster` / `ConvexityBasedCluster` / `ClusterMagnet`）。`Fracture` プラグインが必要 |
| `UnclusterGeometryCollectionBones` | 中間クラスタノードの削除、またはボーンをルート方向へ移動する（5 モード: `MoveUpOneHierarchyLevel` / `CollapseHierarchyOneLevel` / `CollapseLevelHierarchy` / `RemoveDanglingClusters` / `RemoveClustersOfOnlyOneChild`）。ジオメトリを持つボーンが削除されることはない |
| `RenameGeometryCollectionBone` | ボーンを 1 件リネームする。任意で全子孫へも新しい名前を伝播できる（`UpdateChildren`、既定 true） |

#### Geometry editing & clean-up（11）

| コマンド | 説明 |
|---|---|
| `MergeGeometryCollectionBones` 🧩 | 選択した 2 件以上のボーンをマージする — 1 つの生存ボーンへジオメトリごと統合する（`MergeAllSelectedBones`）か、ジオメトリに触れず共有クラスタの下へ再親子付けする（`MergeSelectedClusters`）。`GeometryCollectionFracture` と `Fracture` プラグインが必要 |
| `DeleteGeometryCollectionBranch` 🧩 | 選択したボーンとその全子孫を削除する。Prune ツールに対応。選択ボーン自身がコレクションのルートの場合は削除されない。`GeometryCollectionFracture` と `Fracture` プラグインが必要 |
| `FixGeometryCollectionTinyGeometry` 🧩 | サイズ閾値未満のジオメトリ（`MergeGeometry`）またはクラスタ（`MergeClusters`）を隣接ボーンへマージする。Geometry Merge ツールに対応。`NeighborSelection` の値 `LargestContactArea` は UE 5.8 以降が必要。`GeometryCollectionFracture` と `Fracture` プラグインが必要 |
| `SplitGeometryCollectionIslands` 🧩 | 選択したボーンを非連結成分ごとに分割する。Split Islands ツールに対応。分割対象が無い場合は成功扱いの no-op となる。`GeometryCollectionFracture` と `Fracture` プラグインが必要 |
| `ValidateGeometryCollection` 🧩 | コレクション全体を対象に、未参照ジオメトリ・単一子クラスタ・孤立クラスタをクリーンアップする（少なくとも 1 つのフラグが必要）。対象が無い場合は成功扱いの no-op となる。`GeometryCollectionFracture` と `Fracture` プラグインが必要 |
| `SetGeometryCollectionBoneVisibility` 🧩 | ボーン選択（`SelectionMode: Transform`）または明示的な面選択（`SelectionMode: Face`）で面の `Visible` フラグを切り替える。`GeometryCollectionEdit` と `Fracture` プラグインが必要 |
| `SetGeometryCollectionBoneMaterial` 🧩 | ボーン選択の内側 / 外側 / 全面（`TargetFaces`）へ `MaterialID` を割り当てる — フラクチャで新たに露出した面（`TargetFaces` の `InternalFaces`）へ専用の内部マテリアルを指定する用途に有用。`GeometryCollectionEdit` と `Fracture` プラグインが必要 |
| `RecomputeGeometryCollectionNormals` 🧩 | ボーン選択の法線（`OnlyTangents` 未指定時は接線も）を再計算する — 値が古くなる操作の後に実行しても安全。`GeometryCollectionEdit` と `Fracture` プラグインが必要 |
| `SimplifyGeometryCollectionConvexHulls` 🧩 | 凸包コリジョンの三角形数を削減する（`MeshQSlim` または `AngleTolerance`）。コレクションに凸包データが無い場合は `ExecutionFailed` で失敗する。`GeometryCollectionEdit` と `Fracture` プラグインが必要 |
| `GenerateGeometryCollectionExplodedView` 🧩 | Fracture Mode ビューポートの「View Exploded Amount」スライダーが駆動する分解ビュー表示属性を書き込む。表示専用。`GeometryCollectionEdit` と `Fracture` プラグインが必要 |
| `SetGeometryCollectionBoneColors` 🧩 | 7 種類のアルゴリズム（`ByParent` / `ByLevel` / `ByCluster` / `ByLeafLevel` / `ByLeaf` / `ByAttr` / `Random`）のいずれかでボーンカラー表示属性を割り当てる。任意で頂点カラーへも転送できる。表示専用。`GeometryCollectionEdit` と `Fracture` プラグインが必要 |

#### Settings（1）— 要 `GeometryCollectionEdit`

| コマンド | 説明 |
|---|---|
| `SetGeometryCollectionDestructionSettings` | ダメージモデルとクラスタリング設定を原子的に置き換える — `DamageModel`・階層レベルごとの `DamageThreshold` 配列・`SizeSpecificData`・クラスタリング設定。部分更新モードは無い。事前に `GetGeometryCollectionDestructionSettings` で現在の設定を読み取ること |

---

## UAIP.Editor.Subsonic 🧩

Subsonic オーディオイベントシステム向け `USubsonicEventCollection` アセットの構造編集 — イベント、そのアクションシーケンス、アクションごとの Modifier、Collection/Event スコープのパラメータ、プロパティ⇔パラメータのバインディング — に加え、エディタを離れずにイベントを試聴できます。UE 5.8 以降かつ `Subsonic` プラグイン（Experimental）が必要です。UE 5.7、またはプラグイン無効時はドメイン全体が存在しません。本ドメインに Toolset ブリッジはありません。

> **Note**: アクションまたは Modifier へのインデックスベースの書き込み（`RemoveSubsonicEventAction`、`MoveSubsonicEventAction`、`SetSubsonicEventActionProperty`、`AddSubsonicActionModifier`、`RemoveSubsonicActionModifier`、`MoveSubsonicActionModifier`、`SetSubsonicActionModifierProperty`、および `InsertIndex` を明示指定した `AddSubsonicEventAction`）はすべて `ExpectedActionFingerprint`（`Move*` 系コマンドと挿入位置指定を伴う呼び出しではさらに `ExpectedActionsFingerprint`）を要求し、呼び出し側が直前に観測した値と一致しない場合は拒否されます。これは権限チェックではなく楽観的並行性制御です — インデックスベースのアドレッシングは、そうしなければ同時編集によって別のアクションを黙って壊しうるため安全ではありません。拒否された場合はコレクションを読み直すか、直前の書き込みが返した `ActionsFingerprint` / `Actions[]` を使って現在値を取得してください。
>
> `AuditionSubsonicEvent` の応答フィールドは「再生された」ではなく `EventDispatched` です — イベントが解決され、public であり、そのアクションの `Execute()` が呼ばれたことを意味するだけで、実際に何か聞こえたことを保証しません。`StopSubsonicAudition` はその executor 自身のスコープが所有する音のみを解放します — `Global` 実行スコープで開始された音は**停止しません**。試聴の発行前に、イベントから静的に到達可能な `FGameplayTag` 参照を走査し、循環している、またはチェーン深度・到達可能アクション数の上限を超える場合は `ExecutionFailed`（応答に `CyclePath`）で拒否します — 実行時にタグを組み立てるプロジェクト独自のアクション型は、このチェックからは見えません。
>
> プロパティ⇔パラメータのバインディング（`AddSubsonicPropertyBinding`）に `ParameterScope` 引数はありません — 対象の `ParameterName` は名前のみで解決され、Event スコープのパラメータは同名の Collection スコープのパラメータを覆い隠します。

#### Observation（4 コマンド）— 要 `EditorInspect`

| コマンド | 説明 |
|---|---|
| `ListSubsonicEventCollections` | AssetRegistry 経由で `USubsonicEventCollection` アセットを `AssetPath` 順に一覧表示。各エントリは `AssetPath` のみ — 詳細には `GetSubsonicEventCollectionInfo` を使用。`PageIndex` / `PageSize` でページング、`PathFilter` でコンテンツブラウザのパスプレフィックスによる絞り込みが可能 |
| `GetSubsonicEventCollectionInfo` | 1 つのコレクションの完全な event/action/modifier/parameter/binding 内訳を取得。`EventTagFilter` は `EventTag` に対するプレフィックス一致で絞り込む。`MaxEvents` / `MaxTotalItems` / `MaxResponseBytes` / `MaxContainerElements` / `MaxRecursionDepth` で上限を設定できる（下げることのみ可能、ハード上限は超えられない）。応答本文は artifact として保存され、`Data` にはサマリのみが入る。PIE 実行中でも呼び出し可能 |
| `ListSubsonicActionTypes` | 検出可能な Subsonic アクション構造体型（非 `Abstract` / 非 `Hidden` / 非 `Deprecated`）を、各型ごとに `SetSubsonicEventActionProperty` が受け付けるプロパティスキーマとともに一覧表示。必須入力は無し。`MaxTotalItems` / `MaxResponseBytes` で上限を設定可能 |
| `ListSubsonicModifierTypes` | `ActionStructPath` / `PropertyName` で指定された、ネストされた instanced-struct 配列の検出可能な派生型をすべて一覧表示し、各型について `SetSubsonicActionModifierProperty` が受け付けるプロパティスキーマを付与する。基底型はプロパティの `BaseStruct` メタデータから解決されるため、任意の `TArray<TInstancedStruct<...>>` プロパティに対して機能する |

#### Event & Action editing（7 コマンド）— 要 `SubsonicEventEdit`

| コマンド | 説明 |
|---|---|
| `AddSubsonicEvent` | `EventTag` のイベントを追加する。冪等 — 既に存在するタグの場合は何も変更せず `AlreadyExisted: true` を返す。`EventTag` は登録済みの GameplayTag である必要がある。プレイセッション実行中は拒否 |
| `RemoveSubsonicEvent` | `EventTag` のイベントを、それが所有する全アクション・Event スコープのパラメータ・プロパティバインディングごと削除し、それぞれの削除件数を報告する。`EventTag` を持つイベントが無い場合は `NotFound` で失敗。`AffectedEvents` は常に空 — イベントの削除はそのイベントにスコープされた状態のみを削除する。プレイセッション実行中は拒否 |
| `SetSubsonicEventSettings` | `EventTag` のイベントの設定を更新する。現在設定可能なフィールドは `IsPublic` のみ。少なくとも 1 つの設定を指定する必要があり、何も変更しないリクエストは no-op として成功するのではなく `InvalidParams` で拒否される。プレイセッション実行中は拒否 |
| `AddSubsonicEventAction` | `ActionStructPath` をインスタンス化し、`EventTag` のアクションシーケンスの `InsertIndex` へ挿入、省略時は末尾に追加する。`ExpectedActionsFingerprint` は `InsertIndex` を指定した場合のみ必須。更新後の `ActionsFingerprint` と、上限付きの `Actions[]` を返す。プレイセッション実行中は拒否 |
| `RemoveSubsonicEventAction` | `EventTag` のアクションシーケンスから `Index` のアクション（およびそのプロパティバインディング）を削除する。`ExpectedActionFingerprint` は常に必須。更新後の `ActionsFingerprint` と `Actions[]` を返す。プレイセッション実行中は拒否 |
| `MoveSubsonicEventAction` | `FromIndex` のアクションを移動し、`ToIndex`（移動対象を取り除いた後の配列における位置）へ配置する。`FromIndex == ToIndex` は成功する no-op。`ExpectedActionFingerprint` と `ExpectedActionsFingerprint` の両方が常に必須。プレイセッション実行中は拒否 |
| `SetSubsonicEventActionProperty` | `Index` のアクションのトップレベルプロパティ `PropertyName` へ `Value` を書き込む。`Value` は元から JSON 値で構造化された値をそのまま運べるため、このコマンドに `ValueJson` は無い。`Operation` / `ElementIndex` / `ElementKeyJson` でコンテナの要素 1 つを操作できる（[参照・構造体・コンテナの書き込み](#参照構造体コンテナの書き込み) を参照）。構造体・コンテナにはさらに `PropertyStructuredEdit` が必要。参照の値は**既にロード済み**のアセットを指すもので、このコマンドは参照先を暗黙にロードしなくなったため、以前は通っていた書き込みが先にアセットを開かないと通らなくなる場合がある。ネストされた `TArray<TInstancedStruct<...>>`（`Modifiers`）プロパティは拒否される — 代わりに専用の `AddSubsonicActionModifier` / `RemoveSubsonicActionModifier` / `MoveSubsonicActionModifier` / `SetSubsonicActionModifierProperty` を使用すること。`ExpectedActionFingerprint` は常に必須。プレイセッション実行中は拒否 |

#### Action Modifier editing（4 コマンド）— 要 `SubsonicEventEdit`

| コマンド | 説明 |
|---|---|
| `AddSubsonicActionModifier` | `ModifierStructPath` をインスタンス化し、`Index` のアクションの `ModifiersPropertyName` 配列へ、`InsertIndex` または末尾に挿入する。冪等ではない — 同じ引数で繰り返し呼ぶと複数の Modifier が追加される。Modifier 配列はその所有アクションの fingerprint の一部であるため、常に `ExpectedActionFingerprint` が必須。プレイセッション実行中は拒否 |
| `RemoveSubsonicActionModifier` | `Index` のアクションの `ModifiersPropertyName` 配列から `ModifierIndex` の Modifier を削除する。常に `ExpectedActionFingerprint` が必須。プレイセッション実行中は拒否 |
| `MoveSubsonicActionModifier` | `Index` のアクションの `ModifiersPropertyName` 配列内で、`ModifierFromIndex` の Modifier を `ModifierToIndex` へ移動する。同一インデックスの指定はトランザクションを開かず成功する no-op。常に `ExpectedActionFingerprint` が必須。プレイセッション実行中は拒否 |
| `SetSubsonicActionModifierProperty` | `ModifierIndex` の Modifier のトップレベルプロパティ `PropertyName` へ `Value` を書き込む。`Value` は元から JSON 値のため `ValueJson` は無く、`Operation` / `ElementIndex` / `ElementKeyJson` でコンテナの要素 1 つを操作できる（[参照・構造体・コンテナの書き込み](#参照構造体コンテナの書き込み) を参照）。構造体・コンテナにはさらに `PropertyStructuredEdit` が必要で、参照の値は**既にロード済み**のアセットを指す（参照先は暗黙にロードされなくなった）。常に `ExpectedActionFingerprint` が必須。プレイセッション実行中は拒否 |

#### Parameter editing（3 コマンド）— 要 `SubsonicEventEdit`

| コマンド | 説明 |
|---|---|
| `AddSubsonicParameter` | `Scope`（`Collection` または `Event`。`Event` の場合は `EventTag` が必須）で選択された `FInstancedPropertyBag` へ、`ParameterName` という名前のパラメータを追加する。`ParameterType` は `EPropertyBagPropertyType` の列挙子名（`Bool` / `Int32` / `Int64` / `Float` / `Double` / `Name` / `String` / `Enum` / `Object` / `Struct`）。`ValueTypePath` は `Enum` / `Object` / `Struct` でのみ必須で、それ以外では省略が必要 — struct 型の `ValueTypePath` はさらに `FGameplayTag`（現時点で書き込み可能な唯一の struct 型）に限定される。既存のパラメータ名を再度追加しようとした場合は、上書きではなく拒否される。プレイセッション実行中は拒否 |
| `RemoveSubsonicParameter` | 選択された `Scope` のバッグから `ParameterName` のパラメータを削除する。`UnboundPropertyCount` / `ReboundPropertyCount` は、そのパラメータにバインドされていた全アクションプロパティの結果を分類する — rebind されたプロパティは、同名かつ型互換の Collection レベルのパラメータが引き継いだために解決を維持できたもの（`Scope: "Event"` の場合のみ発生しうる）。選択したスコープに `ParameterName` のパラメータが無い場合は `NotFound` で失敗。プレイセッション実行中は拒否 |
| `SetSubsonicParameterValue` | 選択された `Scope` のバッグにある既存パラメータ `ParameterName` の既定値を設定する。`Value` はアクションプロパティの setter と同じ許可リストで検証され、`Float` / `Double` の NaN/Inf も拒否される。`Value` は元から JSON 値のため `ValueJson` は無く、`Operation` / `ElementIndex` / `ElementKeyJson` でコンテナの要素 1 つを操作できる（[参照・構造体・コンテナの書き込み](#参照構造体コンテナの書き込み) を参照）。構造体・コンテナにはさらに `PropertyStructuredEdit` が必要で、参照の値は**既にロード済み**のアセットを指す（参照先は暗黙にロードされなくなった）。選択したスコープに `ParameterName` のパラメータが無い場合は `NotFound` で失敗。プレイセッション実行中は拒否 |

#### Property Binding editing（2 コマンド）— 要 `SubsonicEventEdit`

| コマンド | 説明 |
|---|---|
| `AddSubsonicPropertyBinding` | イベント `EventTag` の `Index` のアクションが持つ、`PropertyName` という名前のアクションプロパティを `ParameterName` のパラメータへバインドし、既存のバインディングを置き換える。プロパティが `NoBinding` メタデータを持つ場合、値の許可リスト外である場合、またはパラメータと型が非互換の場合は拒否される。`ExpectedActionFingerprint` は常に必須。プレイセッション実行中は拒否 |
| `RemoveSubsonicPropertyBinding` | イベント `EventTag` の `Index` のアクションが持つ、`PropertyName` という名前のアクションプロパティのバインディングを削除する。現在バインドされていないプロパティは no-op 成功ではなく `NotFound` として報告される。`ExpectedActionFingerprint` は常に必須。プレイセッション実行中は拒否 |

#### Audition（2 コマンド）— 要 `SubsonicEventAudition`

| コマンド | 説明 |
|---|---|
| `AuditionSubsonicEvent` | `USubsonicEventCollection` アセット内の `EventTag` のイベントを試聴する。このセッションが以前保持していた試聴があれば置き換える。`EventDispatched` の意味と到達可能性の循環チェックについては上記の Note を参照。プレイセッション実行中は拒否 |
| `StopSubsonicAudition` | このセッションが現在試聴しているものを、保持している executor の登録解除・解放によって停止する。入力は不要 — 停止対象は常にリクエスト自身の `SessionId`。冪等 — 試聴していないセッションでもコマンドが失敗するのではなく `AuditionWasActive: false` で成功する。`Global` 実行スコープで開始された音は**停止しない** — 解放されるのは executor 自身のスコープが所有するソースのみ |

---

## UAIP.Editor.GroomAsset 🧩

`UGroomAsset`（Strand-Based Hair）アセットの構造編集 — グループ/LOD/シミュレーション/補間/レンダリング設定、カード/メッシュのソース設定と派生データビルド、ガイド/ストランドのカーブ制御点、Dataflow グラフの割り当てと実行、毛根マスク/ストランドテクスチャの生成、対象メッシュへのバインディング生成、再取り込み、RBF 変形の焼き込み。`HairStrands` プラグイン（Optional・既定無効）が必要です。プラグインが無効な場合はドメイン全体が利用できません。本ドメインに Toolset ブリッジはありません — エンジンが Groom ドメイン向けの Toolset を出荷していないためです。

4 つの DefaultDenied Capability が書き込み系コマンドを制御します — `GroomAssetEdit`（12 コマンド）、`GroomAssetCreate`（3 コマンド）、`GroomCurveEdit`（4 コマンド）、`GroomBindingEdit`（3 コマンド）。詳細は [Safety & Capabilities](safety.md) を参照してください。書き込み系コマンドはすべて PIE / SIE 実行中は拒否されます。ほとんどの書き込みコマンドは対象アセットを未保存のまま残します（各コマンドの説明にその旨が明記されています）。永続化するには `UAIP.Editor.Workspace.SaveAllPackages` を使用してください。新規アセットを生成する 5 コマンド（`GenerateGroomFollicleMaskTexture`、`GenerateGroomStrandsTextures`、`CreateGroomBinding`、`CreateGeometryCacheGroomBinding`、`BakeGroomRBFDeformation`）は、応答を返す前に生成物を保存します。

#### Observation（13 コマンド）— 要 `EditorInspect`

| コマンド | 説明 |
|---|---|
| `GetGroomAssetInfo` | グループ数、グループごとの `FHairGroupInfo` フィールド（カーブ/ガイド/頂点数、最大カーブ長）、グループ自身の LOD スロット数（グループ間の最大値ではない）、アセット全体の設定（マテリアルスロット数、Dataflow アセットパス、未保存フラグ、グローバル補間 / シミュレーションキャッシュ / ヘア補間種別） |
| `GetGroomLODSettings` | 各グループの `AutoLODBias` と、全 LOD スロットの `FHairLODSettings` 全体。出力の形は `SetGroomLODSettings` の入力と一致する |
| `GetGroomSimulationSettings` | 各グループの `FHairGroupsPhysics` 全体（ソルバー、外力、曲げ/伸び/衝突拘束、ストランドパラメータ）。4 種のスカラーカーブをキー単位でシリアライズする。出力の形は `SetGroomSimulationSettings` の入力と一致する |
| `GetGroomInterpolationSettings` | 各グループの `FHairGroupsInterpolation` 全体（デシメーション・補間設定）。出力の形は `SetGroomInterpolationSettings` の入力と一致する |
| `GetGroomRenderingSettings` | 各グループの `FHairGroupsRendering` 全体（ジオメトリ/シャドウ/上級者向け設定）。出力の形は `SetGroomRenderingSettings` の入力と一致する |
| `GetGroomCardsInfo` | 全 `FHairGroupsCardsSourceDescription` エントリ（元メッシュ、ガイド種別、テクスチャレイアウトとパス、カード/頂点数）と、`"HairCardGenerator"` 実装が現在登録されているかどうか |
| `GetGroomMeshesInfo` | 全 `FHairGroupsMeshesSourceDescription` エントリ（元メッシュ、テクスチャレイアウトとパス） |
| `GetGroomGuideCurves` | 1 グループのガイドカーブ制御点を、呼び出し側が指定した 1 つ以上の範囲で取得する（「全件ダンプ」モードは無い）。範囲が 1 応答あたりの上限を超える場合は拒否ではなく切り詰め、`bTruncated` と実際に返した範囲を報告する |
| `GetGroomStrandCurves` | ストランドカーブの制御点。範囲・切り詰めの契約は `GetGroomGuideCurves` と同じで、頂点ごとの色/ラフネス/AO とカーブごとのガイドウェイトフィールドが加わる |
| `GetGroomDataflowInfo` | 現在割り当てられている `UDataflow` アセット（未割り当てなら空）と、設定されたターミナルノード名。未割り当ては通常の結果でありエラーではない |
| `GetGroomBindingInfo` | `UGroomBindingAsset` 自体のプロパティ — バインディング種別、元/対象メッシュのパス、補間点数、グループごとの `GroupInfos`、コンパイル中かどうか、有効性 |
| `ListGroomBindings` | 対象の `UGroomAsset` を参照する全 `UGroomBindingAsset`。Asset Registry のタグのみから回答し、候補となるバインディングは一切ロードしない |
| `GetGroomCacheInfo` | `UGroomCache` 自体の内容 — 種別（Strands/Guides）、フレーム範囲、尺、保存されているアニメーション情報の属性フラグ |

#### Settings & LOD writes（7 コマンド）— 要 `GroomAssetEdit`

| コマンド | 説明 |
|---|---|
| `SetGroomSimulationSettings` | 1 グループの物理設定への部分パッチ。4 種のスカラーカーブは全キー置換となる。`GetGroomSimulationSettings` が返す形をそのまま受け付けるため、Get → 編集 → Set の往復ができる |
| `SetGroomLODSettings` | 既存の 1 LOD スロットのフィールドと、所属グループの `AutoLODBias` への部分パッチ。スロットの追加・削除は行わない |
| `SetGroomInterpolationSettings` | 1 グループのデシメーション/補間設定への部分パッチ。対象が Dataflow アセットを参照している場合、`bAllowOverwrite` を指定しない限り拒否される — `GuideType` はまさに Dataflow の実行が上書きする値のため |
| `SetGroomRenderingSettings` | 1 グループのジオメトリ/シャドウ/上級者向けレンダリング設定への部分パッチ |
| `SetGroomAssetSettings` | アセット全体の 3 フィールド（`EnableGlobalInterpolation`、`EnableSimulationCache`、`HairInterpolationType`）への部分パッチ — 上記のグループ単位の書き込みと異なり `GroupIndex` を持たない |
| `AddGroomLOD` | 既定値で構築した LOD スロットを 1 つグループへ追加し、新スロットのインデックスを返す。以後の設定は `SetGroomLODSettings` で行う |
| `RemoveGroomLOD` | LOD スロットを 1 つ削除する。失われるのはそのスロット自身の設定値のみ — グループのカーブデータは無傷 — だが元に戻すには削除前の全フィールドを `AddGroomLOD` + `SetGroomLODSettings` で再適用する必要がある |

#### Cards / Meshes（4 コマンド）— 要 `GroomAssetEdit`

| コマンド | 説明 |
|---|---|
| `SetGroomCardsSource` | `FHairGroupsCardsSourceDescription` エントリを 1 つ upsert する（ガイド種別、取り込み済みメッシュ、テクスチャレイアウト/パス）— 既存の（グループ, LOD）エントリがあればパッチし、無ければ新規追加する。カードの派生データはビルドしない |
| `SetGroomMeshesSource` | `FHairGroupsMeshesSourceDescription` エントリを 1 つ upsert する。パッチ/追加の契約は同じ。メッシュの派生データはビルドしない |
| `BuildGroomCardsData` | `UGroomAsset::BuildCardsData()` を強制実行する（Derived Data Cache の参照/ビルド、Heavy、上限時間なし）。ソース記述が `GuideType == Generated` を要求しており `"HairCardGenerator"` 実装が未登録の場合、事前に `NotAllowed` で拒否する |
| `BuildGroomMeshesData` | `UGroomAsset::BuildMeshesData()` を強制実行する（Derived Data Cache の参照/ビルド、Heavy、上限時間なし） |

#### Texture generation（2 コマンド）— 要 `GroomAssetCreate`

| コマンド | 説明 |
|---|---|
| `GenerateGroomFollicleMaskTexture` | 元の Groom 自身のパッケージの隣に新規の毛根マスク `UTexture2D` を作成し、そのピクセル生成を投入する。保証されるのは投入のみ — GPU での生成/読み戻しは以降の複数フレームにわたって完了するが、エンジンは完了シグナルを一切公開しない。生成したテクスチャを Groom へ紐付けはしない — 紐付けには `SetGroomCardsSource`/`SetGroomMeshesSource` を使用する |
| `GenerateGroomStrandsTextures` | 選択した Layout が要求するスロット数分の新規ストランドテクスチャ（`UTexture2D`）を作成し、SkeletalMesh または StaticMesh に対してストランド形状をトレースして生成を投入する。投入のみ保証・自動紐付けなしという契約は `GenerateGroomFollicleMaskTexture` と同じ |

#### Curve editing & Dataflow（4 コマンド）

| コマンド | Capability | 説明 |
|---|---|---|
| `SetGroomGuideCurves` | `GroomCurveEdit` | グループ内の 1 つ以上の範囲について、ガイドカーブの制御点を単一の `ConvertFromGroomAsset` → `ConvertToGroomAsset` 往復で差し替える。`GetGroomGuideCurves` が返す形をそのまま受け付ける。書き込みはカーブの追加・削除を一切行わず、（読み取りと異なり）範囲がグループの終端を越える場合は切り詰めではなく拒否される。対象が Dataflow アセットを参照している場合、`bAllowOverwrite` を指定しない限り拒否される |
| `SetGroomStrandCurves` | `GroomCurveEdit` | `SetGroomGuideCurves` と同じ契約で、ストランドカーブを対象とする |
| `SetGroomDataflowAsset` | `GroomAssetEdit` | Dataflow 割り当て（アセットパス / ターミナルノード名）への部分パッチ。非破壊 — 割り当てを変更するだけで、グラフを実行したりカーブデータに触れたりはしない |
| `EvaluateGroomDataflow` ⚠️ | `GroomCurveEdit` | **Experimental — 現時点で有用な結果を生みません。** 割り当てられた Dataflow グラフを実行する（`FDataflowInstance::UpdateOwnerAsset()`）。全グループのガイド/ストランドのカーブ形状と `GuideType` をグラフの出力で上書きする — 実行前のカーブはこのコマンドでは復元できない。Dataflow アセットが割り当てられていない場合は `NotFound` を返す。**既知のエンジン側の不具合**: Groom の終端ノードは `FDataflowTerminalNode` の 2 引数版 `Evaluate()` しか実装しておらず、`UpdateOwnerAsset()` が呼ぶ 1 引数版の基底実装は `ensure(false)` である。そのためグラフは評価されないまま終端ノードが空の結果を書き込み、**対象のヘアグループが消える**。エンジン自身の経路（コンテンツブラウザの Re-evaluate Dataflow、`RegenerateAssetFromDataflow` / `EvaluateTerminalNodeByName`）でも同じ結果になるため、本コマンド固有の問題ではない。UE 5.8 で確認。成功応答は「要求がエンジンへ届いた」ことを示すに留まるので、実行後にグループ数を確認すること |

#### Bindings（3 コマンド）— 要 `GroomBindingEdit`

| コマンド | 説明 |
|---|---|
| `CreateGroomBinding` | Groom を対象の `USkeletalMesh` にバインドする新規 `UGroomBindingAsset` を作成し、ビルド完了まで待ってから結果を保存する。元メッシュ（Source）を省略すると、後で `BakeGroomRBFDeformation` に使えないバインディングになる。指定パスが既存アセットと衝突した場合は上書きせず別名（連番）で作成し、応答が実際のパスを報告する |
| `CreateGeometryCacheGroomBinding` | `CreateGroomBinding` と同じ契約で、代わりに `UGeometryCache` へバインドする（このバインディング種別ではビルドは同期実行） |
| `RebuildGroomBinding` | 既存バインディングの派生データをその場で再ビルドし、ビルド完了まで待ってから応答する。同じバインディングを別のリクエストが既にビルド中の場合は待たずに即座に `TooManyRequests` を返す。再ビルドの失敗は元に戻せない — エンジンは再生成の前に既存の派生データを破棄するため |

#### Import / Bake（2 コマンド）

| コマンド | Capability | 説明 |
|---|---|---|
| `ReimportGroom` | `GroomCurveEdit` | Groom のヘア記述を、元ファイル（省略時はアセット自身の既存の取り込みファイル）から新たに翻訳した内容で置き換え、派生データをその場で再ビルドする。元ファイルの翻訳自体が失敗した場合、アセットは変更されない。翻訳は成功したが後続の取り込み/再ビルドが失敗した場合、アセットの以前の内容が保たれる保証はない。対象が Dataflow アセットを参照している場合は `bAllowOverwrite` を指定して再取り込みする |
| `BakeGroomRBFDeformation` | `GroomAssetCreate` | バインディングの RBF 変形を、そのバインディングの元 Groom から複製した（カード/メッシュのジオメトリを含む）新規の `UGroomAsset` へ焼き込む。元の Groom とバインディングは一切変更しない。バインディングが元/対象両方の SkeletalMesh を持ち、かつ全グループのデシメーションが無効（`VertexDecimation=1`、`CurveDecimation=1`）であることを要求し、満たさない場合は事前に拒否する。**検証可能な前提条件をすべて満たしていても、エンジン自身の RBF ルートデータ生成が予測不能な形で失敗し、エディタプロセスがクラッシュすることがある** — このコマンドが `GroomAssetCreate`（既定無効）の背後にあるのは、まさにこの残存リスクのためである |

---

## UAIP.Editor.Validation 🧩

プロジェクトが登録したアセットバリデータを、少数のアセットに対してもコンテンツフォルダ全体に対しても実行し、検出された内容を読み、バリデータが提供する修正を適用します。何が「正しい」かを UAIP が決めることはありません — 判定はすべて `UEditorValidatorSubsystem` と、そこにエンジンおよびプロジェクトが登録したバリデータに由来します。`DataValidation` プラグインが必要です。このドメインに Toolset ブリッジは存在しません。

> **前提条件**: `DataValidation` はエンジン同梱で既定有効です。エディタビルドでは UAIP がその対応を自動的にコンパイルへ含めます — `.uproject` の `Plugins` 配列への追加もリビルドも不要になりました。プロジェクトが明示的に無効化している場合は、**Edit → Plugins** から有効化してエディタを再起動してください。プラグインが無効な間はドメインごと `uaip_list_commands` に現れず、これらのコマンドを呼ぶと有効化すべきプラグイン名を含む `CommandNotFound` が返ります。`UAIP.Core.ListIntegrations` でもこのドメインの状態を直接確認できます。

> **Note — マテリアル検証にはさらに設定が必要です**: エンジンのマテリアルバリデータは、プロジェクトの `MaterialValidationPlatforms` 設定が空の間はすべてのマテリアルをスキップします。このプラットフォーム一覧はバリデータのクラスデフォルトオブジェクトの構築時に 1 度だけ作られるため、**設定変更はエディタを再起動するまで反映されません**。`ListValidators` はこれについて観測できる内容を `MaterialValidation` として返しますが、`EffectivelyRunnable` は答えではなく推定値です — バリデータが実際に保持している一覧は外部から読めないため、すべてのフラグが true でもマテリアルがスキップされることがあります。
>
> **Note — この設定は UAIP からは書き込めません**: `UAIP.Editor.Engine.ConfigSettings.SetSettingsValues` は `MaterialValidationPlatforms` を受け付けて `ChangedCount: 1` を返し、続く `SaveSettings` も成功し、その直後の `ListValidators` は `PlatformsConfigured: true` を返します — しかし値はメモリ上の設定オブジェクトにしか届いていません。どの `.ini` にも書き込まれず、エディタを再起動すると失われます。設定は **Project Settings → Editor → Data Validation → Material Validation Platforms** から行うか、`Config/DefaultEditor.ini`（`[/Script/DataValidation.DataValidationSettings]` セクション）を直接編集し、その後エディタを再起動してください。
>
> **Note — ジョブの結果は 1 回の呼び出しと一致するとは保証されません**: `StartValidationJob` はエディタを操作可能なまま保つために少しずつ検証しますが、エンジンはバッチ単位の検証フックをチャンクごとに発火させます。そのため、バッチ全体を集約するプロジェクト独自バリデータは 1 つのバッチではなく複数のバッチを見ることになります。一致が重要な場合は `ValidateAssets`（1 回の呼び出しで検証。最大 8 件）を使ってください。
>
> **Note — 修正はエンジンではなくプロジェクトが提供するものです**: エンジン同梱のバリデータは修正を 1 つも生成しないため、`Assets[].Fixes[]` が空なのは異常ではなく通常の状態です。修正は、それを提供するバリデータをプロジェクトが自作している場合にのみ現れます。また、検証と修正の届く範囲は意図的に異なります — 検証はエンジン・プラグインコンテンツを含むすべてのマウント済みコンテンツルートを読みますが、`ApplyValidationFix` は UAIP が書き込まないルート（`/Engine/` など）配下のアセットを `NotAllowed` で拒否します。その種のアセットはプロジェクトコンテンツへ複写してから修正してください。
>
> **Note — `ListValidators` 以外のすべてのコマンドは明示的な `SessionId` を要求します**。検証は開始した呼び出しの後から追跡・取得・修正されるものであり、それに到達できるのは開始したセッションだけだからです。呼び出し元セッションが到達できない識別子は、理由を問わず（不明・期限切れ・他セッションのもの・ジョブ系コマンドへ `ResultId` を渡した場合）すべて `NotFound` となります。なお `ListValidators` が列挙できるのはエンジンが**有効とみなす**バリデータだけで、無効なものが何件あるかは観測できません。

#### Validator observation（1 コマンド）— 要 `EditorInspect`

| コマンド | 説明 |
|---|---|
| `ListValidators` | エディタが現在有効とみなしているバリデータを、`ClassPath` / `ClassName` / `IsEnabled` とともに列挙し、`EnabledCount` と `MaterialValidation` ブロック（`ValidatorPresent`、`SettingsEnabled`、`PlatformsConfigured`、`EffectivelyRunnable`、`Note`）を返します。「問題がなかった」のか「そもそも検査されていない」のかを切り分けるために使います。このドメインで唯一、明示的な `SessionId` なしで呼べるコマンドです |

#### Validation（2 コマンド）— 要 `AssetValidation`

| コマンド | 説明 |
|---|---|
| `ValidateAssets` | 1〜8 件のアセットを同期的に検証して結果を返します。無効だったアセット、警告のあるアセット、検査されなかったアセットは個別に列挙され、何も見つからなかったアセットは `Summary` に集計され、`IncludeValid` が true のときにのみ列挙されます。結果 JSON は 64 KiB 未満の間はインラインで返され、いずれにせよ artifact としても書き出されます。⚠️ 本コマンドには時間予算も中断点も進捗取得もありません — マテリアル 1 件の検証だけでシェーダーコンパイルを伴い数秒かかりうるため、重いアセットを含む呼び出しはエディタを数秒〜数十秒応答させなくしうることに注意してください。`ResultId` は、結果に修正が 1 件以上含まれるときにのみ返ります。`AssetPaths` 内で重複したパスは、黙って重複除去せず `InvalidParams` で拒否します（8 件を明示指定したのに 7 件しか検証されない結果は分かりにくいため） |
| `StartValidationJob` | フォルダ（`PackagePath` + `Recursive`）または明示的な `AssetPaths` リスト — どちらか一方だけであり、両方指定も両方省略も不可 — を複数フレームに分けて検証し、結果ではなく `JobId` を返します。`MaxAssets` は、リダイレクタ解決と外部オブジェクトの所有者への畳み込みの後に残る件数を制限します（切り捨てた場合は `Summary.AssetLimitReached` が立ちます）。列挙だけで内部上限を超えるほど広いフォルダは、先頭の一部を検証するのではなく `EnumerationLimitExceeded` で失敗しますので、`MaxAssets` を下げるのではなくフォルダを絞ってください。同一セッションのジョブが実行中に 2 つ目を開始すると前のジョブが中断され `ReplacedPreviousJob` が返り、前回からの間隔が短すぎる場合は `TooManyRequests` が返ります。`Recursive` は `PackagePath` と併用したときにのみ意味を持つため、`AssetPaths` と同時に指定した場合は黙って無視せず拒否します（20,000 件を超える `AssetPaths` も同様です）。`PackagePath` は `/Game` のようなコンテンツのルートも、その下のフォルダも受け付ける（末尾の `/` は外される）。拒否されたパスは `InvalidParams` で、文は `'PackagePath' value '…': <理由>` の形になる |

#### Job observation & control（3 コマンド）— 要 `EditorInspect`

| コマンド | 説明 |
|---|---|
| `GetValidationJobStatus` | ジョブの進捗を問い合わせます。`State`（`Preparing` / `Enumerating` / `Normalizing` / `Validating` / `Finalizing` / `Completed` / `Failed` / `Aborted`）、`PhaseLabel`、`ProcessedCount` / `TotalCount`、`ElapsedSeconds`、`FailureReason`（固定の列挙値。失敗するまでは `None`）、および途中集計の `NumInvalid` / `NumWarnings` を返します。返されるのは件数・状態・経過秒だけで、バリデータのメッセージもアセットパスも含まれません。応答コストはジョブの規模によらず一定なので、ポーリングが検証を遅くすることはありません |
| `GetValidationJobResult` | ジョブが生成した結果を取得します。ジョブ全体の集計をインラインで、完全な結果を JSON artifact として返します（無効だったアセット・警告のあるアセット・検査されなかったアセットの明細）。ここで再検証・再走査は行いません。完了したジョブだけでなく、失敗したジョブや中断されたジョブに対しても結果を返します — 停止するまでに検証されていた分は artifact に含まれ、何が落ちたかは `Truncation` が説明します。未完了のジョブに対して部分結果を返すことはありませんので、先にステータスをポーリングしてください。読み取りに成功するとジョブの保持期限が延長されます |
| `CancelValidationJob` | ジョブを次のチャンク境界で停止します — **即時ではありません**。エンジンの検証呼び出しは一度入ると中断できないため、実行中のチャンク 1 つ分は最後まで走り、その結果も保持されます。直後に進捗を見るとまだ実行中に見えることがあります。ジョブは識別子と結果を保持したまま `Aborted` になります（長い実行を途中で止める目的は通常これです）。すでに終了したジョブへの中断要求は成功し、`WasRunning: false` を返して何もしません。⚠️ ジョブを `Aborted` へ遷移させる状態変更を伴いますが、観測系コマンドと同じく read-only 宣言・`EditorInspect` ゲートです。これを境界づけているのはジョブの所有権です |

#### Fix application（1 コマンド）— 要 `AssetValidationFix`

| コマンド | 説明 |
|---|---|
| `ApplyValidationFix` | バリデータがメッセージに添えて提供した修正を 1 件適用します。`ResultId`（`StartValidationJob` が返した `JobId`、または `ValidateAssets` が返した `ResultId`）と、その結果の `Assets[].Fixes[]` から引いた `FixId` で指定します。修正は 1 件ずつ適用します。ある修正を適用すると排他関係にあった他の修正が適用不可になりうるため、応答には `UpdatedFixes`（その結果が保持する全修正の適用可否を適用後に再取得したもの）が含まれます。修正へはそれを生成した結果経由でしか到達できません — その結果が保持していない識別子は `NotFound` となり、識別子の文字列からアセットを引き当てることはありません（検証していないアセットの修正に結果をチケットとして使えないため）。`AssetSaved` はアセットがディスクへ保存されたかを表します。このドメインで唯一 read-only ではないコマンドで、`DisableSave` が有効な間は一律に拒否されます（修正が保存を伴うかどうかを fixer に事前に問う手段がないため） |

---

## UAIP.Editor.LiveLink 🧩

エディタ側の LiveLink 作業 — プリセットアセット、配置済みアクターの LiveLink コントローラーコンポーネントへの Subject 割り当て、MessageBus の探索と接続、Take Recorder による録画。**`LiveLink` と `Takes` の両プラグインが必要**です。エディタビルドでは、両プラグインがエンジンに存在してさえいれば UAIP が自動的にその対応をコンパイルへ含めます（両方ともエンジン同梱のため実質的に常に該当します）— `.uproject` への明示宣言は不要です。必要なのはプロジェクトで両方が**有効**になっていることだけです。どちらかが無効だとドメインごと登録されず、これらのコマンドは有効化すべきプラグイン名を含む `CommandNotFound` を返します — 両方を有効にしてエディタを再起動すれば直り、リビルドは不要です（万一そのプラグインがこのエンジン版に本当に存在しない場合はどの設定を変えても直らず、代わりに `UnavailableDetail: "OptionalPluginDisabled"` を返します — [UnavailableDetail](#unavailabledetail--handlerunavailable-の8つの詳細理由) 参照）。ドメインが登録された後も、録画系の 4 コマンド（`StartLiveLinkRecording` / `StopLiveLinkRecording` / `CancelLiveLinkRecording` / `GetLiveLinkRecordingStatus`）は、`TakeRecorder` モジュールがこのプロセスにまだ読み込まれていない場合、個別に `Available: false`（`UnavailableDetail: "ExecutionEnvironment"`）を返すことがあります — こちらもリビルドではなく再起動で直ります。

LiveLink の観測系は [UAIP.Runtime.LiveLink](#uaipruntimelivelink) にあり、そちらにプラグイン要件はありません。

LiveLink の構成変更は同時に 1 つしか走りません。プリセット適用中と録画中は、このセクションと `UAIP.Runtime.LiveLink` の変更系コマンドが拒否されます。**読み取りは決して拒否されない**ため、`GetLiveLinkPresetInfo` と `GetLiveLinkRecordingStatus` は常時応答します。待てば解消する拒否は `TooManyRequests`、進行中の操作を先に終わらせる必要がある拒否は `NotAllowed` で返ります。

### プリセット（4）

| コマンド | 説明 |
|---|---|
| `GetLiveLinkPresetInfo` | `ULiveLinkPreset` アセットが保持する Source と Subject を、実行中のクライアントに触れずに返す。`ApplyLiveLinkPreset` の前に取るスナップショット。保存された設定オブジェクトはクラスパスだけを返し、接続文字列を含むその値は一切返さない。read-only（`EditorInspect`）で、PIE 中も、プリセット適用中・録画中も許可される |
| `ApplyLiveLinkPreset` | ⚠️ **破壊的。** クライアントの構成全体をプリセットの内容で置き換える。**既存の Source をすべて取り除いてから作り直すため、途中で失敗すると一部だけ取り除かれた構成が残る** — 元の構成には戻らない。エンジンが元の構成を保持していないため UAIP からも復元できない。非同期で、エンジン側の適用が終わった時点で応答する。他のプリセット適用が進行中なら `TooManyRequests`（待てば通る）、録画中なら `NotAllowed`（先に停止が必要）で、いずれの拒否でもクライアントには手を触れない。`LiveLinkPresetApply` が必要 |
| `AddLiveLinkPresetToClient` | プリセットの Source と Subject を現在の構成へ同期的に追加する。既定では追加のみで非破壊。`RecreateExisting` を指定すると、プリセットに載っている Source と Subject を一度消してから作り直すため破壊的になり、`LiveLinkPresetApply` が追加で必要になる（Capability 名は全応答の `RecreateExistingRequiredCapability` に含まれる）。`LiveLinkPresetAdd` が必要 |
| `SaveLiveLinkPreset` | クライアントの現在の構成を `PresetPath` のプリセットアセットへ書き出す。新規作成と既存プリセットの上書きの両方に対応し、どちらだったかを応答が返す。**LiveLink プリセット以外のアセットが既にあるパスは、上書きせず拒否する。** プロジェクトコンテンツのパスのみ受け付ける。PIE / SIE 中は拒否。`LiveLinkPresetSave` が必要 |

### コンポーネントへの割り当て（1）

| コマンド | 説明 |
|---|---|
| `SetLiveLinkComponentSubject` | 配置済みアクターの LiveLink コントローラーコンポーネントに Subject を割り当て、あわせて制御対象のコンポーネントを指定する。`ComponentId` と `ExpectedComponentClass` は `ListActorComponents` / `AddActorComponent`（[UAIP.Editor.Level](#uaipeditorlevel)）から得る。期待クラスを再確認するため、古くなった識別子は追従せず拒否される。`SubjectName` は現在有効な Subject に対して解決し、同名が複数ある場合は `Candidates` を列挙して `InvalidParams` で拒否する（解決結果は応答に含まれる）。そのアクター上のコンポーネントのみ受け付ける — Blueprint 側のものは Blueprint コンポーネントコマンドの担当。PIE / SIE 中は拒否。Undo 可能。`LiveLinkComponentEdit` が必要 |

### MessageBus の探索と接続（2）

| コマンド | 説明 |
|---|---|
| `DiscoverLiveLinkMessageBusProviders` | 探索 ping をブロードキャストし、`DurationSeconds`（[1, 30] に切り詰め。適用値は `EffectiveDurationSeconds` として返る）以内に応答した提供元を返す。各応答は不透明な `Token` と `ProviderName` として返り、**ネットワークアドレスそのものは返さない**。Token はその探索を行ったセッションでのみ、かつ短い TTL の間だけ解決でき、他のセッションからは見えも使えもしない。`IncludeSensitiveDetails: true` は各提供元の `MachineName` を追加し、`LiveLinkNetworkDiscovery` に**加えて** `LiveLinkSourceInspectSensitive` が必要（要求の有無にかかわらず Capability 名は `SensitiveDetailsRequiredCapability` として返る）。探索は同時に 1 つまで（`TooManyRequests`）。非同期。`LiveLinkNetworkDiscovery` が必要 |
| `ConnectLiveLinkMessageBusSource` | 探索で見つかった提供元を、探索が返した `Token` で指定してクライアントへ新しい Source として接続する。Token の所有者・TTL・提供元の有効性は構築前に再検証され、どれで失敗しても `InvalidParams` として返る。返すのは新しい `SourceGuid` と `ProviderName` のみで、**Subject が現れたかどうかは待たないし報告もしない** — 正常な接続でもしばらく Subject が 0 件のことがあるため。それは `ListLiveLinkSources` / `ListLiveLinkSubjects` で確認する。`LiveLinkSourceConnect` が必要 |

### 録画（4）

| コマンド | 説明 |
|---|---|
| `StartLiveLinkRecording` | `UTakeRecorderSubsystem` 経由で 1 つ以上の LiveLink Subject を新しい LevelSequence へ録画する。**Sequencer は開かず、モーダルダイアログも出さない。** `SubjectNames` の各要素は現在有効な Subject に解決し、一致 0 件なら `NotFound`、複数一致なら候補を `ResolvedSubjects` に列挙して `InvalidParams`。プリセット適用中・別の録画中は `NotAllowed` / `TooManyRequests`、UAIP の管理外で Take Recorder の録画が既に走っている場合は `ExecutionFailed` で、いずれも副作用は残さない。**保存先は `UTakeRecorderProjectSettings` に従い、任意の保存パスは受け付けない。** PIE 中も許可。`LiveLinkRecording` が必要 |
| `StopLiveLinkRecording` | UAIP 自身が始めた録画を停止し、生成された LevelSequence のパッケージパスを返す。UAIP が所有する録画が進行中でない場合は `NotAllowed`（何も録画していない場合と、進行中の録画が UAIP 外——Take Recorder パネルや他プラグイン——で始まった場合の両方）。PIE 中も許可。`LiveLinkRecording` が必要 |
| `CancelLiveLinkRecording` | UAIP 自身が始めた録画を中止し、そこまでの内容を LevelSequence として確定させずに**破棄する**。`NotAllowed` の条件は `StopLiveLinkRecording` と同じ。PIE 中も許可。`LiveLinkRecording` が必要 |
| `GetLiveLinkRecordingStatus` | `IsRecording`（誰が始めたかに関わらず Take Recorder の録画が進行中か）と `StartedByUAIP` を返す。`StartedByUAIP` が true のときに限り `ResolvedSubjects`・`ElapsedSeconds`・`TargetSequencePath` も返る — 外部で始まった録画の開始時刻や対象を観測する手段が無いため、推測せずフィールドごと省略する。read-only（`EditorInspect`） |

> **UAIP が始めた録画を人間が止めた場合も検知します。** UAIP が始めた録画を Take Recorder パネルから停止した場合や自然に終わった場合、UAIP はそれを検知して「録画中」の扱いを解除します。止め方が違うせいで他の操作がブロックされ続けることはありません。逆方向も同様に守られます — UAIP が始めていない録画が、これらのコマンドで停止・中止されることはありません。

---

## UAIP.Runtime.PIE

PIE セッションのライフサイクル。実行中ワールドの操作は [`UAIP.Runtime.World`](#uaipruntimeworld) にあります。

| コマンド | 説明 |
|---|---|
| 🆓 `StartPIE` | Play-in-Editor セッションを開始 |
| 🆓 `StopPIE` | アクティブな PIE セッションを停止 |
| 🆓 `PausePIE` | アクティブな PIE セッションを一時停止 |
| 🆓 `ResumePIE` | 一時停止中の PIE セッションを再開 |
| 🆓 `LoadMap` | アクティブな PIE セッションでマップをロードし完了を待つ |
| 🆓 `GetPIEState` | 現在の PIE 状態を返す — `Running`・`Stopped`・`Paused`・`Simulating` |

### Toolset ブリッジ（3 件）🧩

`EditorAppToolset`（UE 5.8+、EditorToolset プラグイン）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.Toolset.PIE.*`。

> `StartPIE` は呼び出し側から見て変わりません（`bSimulateInEditor` は任意のまま）。ブリッジが Toolset の必須のセッションオプション（`bSimulate`・`playMode` = `PlayMode_InViewPort`・`warmupSeconds` = `2.0`）を送るようになりました。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.Toolset.PIE.StartPIE` | PIE セッションを開始（非同期、`PIEControl` 必要） |
| `Toolset.Editor.Toolset.PIE.StopPIE` | PIE セッションを停止（非同期、`PIEControl` 必要） |
| `Toolset.Editor.Toolset.PIE.IsPIERunning` | PIE が実行中かどうかを返す |

---

## UAIP.Runtime.World

**実行中**のゲームワールドの操作・検査。旧バージョンではこれらは `UAIP.Runtime.PIE` 配下に登録されていました。

このドメインのコマンドは、`QuitGame` と `ListPlayWorlds`、および CVar 系 2 つを除き、任意パラメータ `TargetNetRole` / `TargetPIEInstance` を受け付けます — [実行時コマンドの対象プレイワールドを指定する](#実行時コマンドの対象プレイワールドを指定する) を参照してください。

| コマンド | 説明 |
|---|---|
| `SpawnActor` | アクティブな PIE ワールドに指定クラスのアクターをスポーン（`RuntimeActorManipulation` 必要） |
| `DestroyActor` | アクティブな PIE ワールドのアクターを破棄（`RuntimeActorManipulation` 必要） |
| `TeleportActor` | アクターをワールド空間の指定位置 / 回転にテレポート |
| `PossessActor` | プレイヤーコントローラーにアクターを憑依させる |
| `SetTimeScale` | アクティブなゲームワールドのグローバル時間スケールを設定 |
| `QuitGame` | 実行中のゲームプロセスの正常終了をリクエスト（`RuntimeActorManipulation` 必要）。PIE 実行中は PIE セッションを停止します。ゲームを実行していないエディタでは `ExecutionFailed` を返し、エディタは閉じません — `QuitGame` が終了させるのは実行中のゲームであってエディタではありません。エディタを閉じるには [`ShutdownEditor`](#uaipeditorworkspace)（`UAIP.Editor.Workspace.ShutdownEditor`）を使ってください。この場合、以前は何もせずに `Success: true` を返していました |
| `ExecuteConsoleCommand` | アクティブなゲームワールドでコンソールコマンドを実行（`RuntimeExecCommand` 必要） |
| 🆓 `GetConsoleVariable` | ⚠️ **非推奨** — `UAIP.Runtime.Engine.CVar.GetConsoleVariable` を使用してください。コンソール変数の値・型・ヘルプテキストを取得。機微な名前は not found 扱い（`RuntimeCVarRead` 必要） |
| 🆓 `SearchConsoleVariables` | ⚠️ **非推奨** — `UAIP.Runtime.Engine.CVar.SearchConsoleVariables` を使用してください。ワイルドカード（`*`）でコンソール変数を検索。`MaxResults` は既定 50・最大 200、機微な名前は除外 |
| `ListPlayWorlds` | エンジンがいま保持しているプレイワールドをすべて返します — `PIEInstance`、`NetMode`（`Standalone` / `DedicatedServer` / `ListenServer` / `Client`）、`MapName`、`bIsPrimaryPIEInstance`、および `Count`。プレイしていないときもエラーではなく空のリストを返すため、プレイ開始前に呼んでも安全です。パラメータは一切取りません。ここで返る値がそのまま `TargetNetRole` / `TargetPIEInstance` に渡せます。Capability 不要 |

> ⚠️ **破壊的変更 — `SetTimeScale` / `TeleportActor` / `PossessActor` / `ExecuteConsoleCommand` はエディタで開いているレベルに作用しなくなりました。** この 4 つは対象ワールドを世界種別で絞らずに解決していたため、プレイしていない状態では最初に見つかったワールド — つまり**編集中のレベル** — を掴み、実際にそこへ変更を適用していました。今後は適用されません。プレイセッションの外では失敗し、何も変更しません。拒否の形も変わり、`ExecutionFailed` ＋ `No active game world found.` から **`NotAllowed` ＋ `PIE is not running.`** になりました。この 4 つは実行中のゲームを対象とするコマンドです。編集中のレベルを変更したい場合は、対応する `UAIP.Editor.*` コマンドを使ってください。旧エラーコードや旧メッセージ文字列でパターンマッチしている箇所は更新が必要です。

> ⚠️ **`TeleportActor` は、移動できないアクターに対して成功を返さなくなりました。** `AActor::TeleportTo` は、root コンポーネントが `UPrimitiveComponent` でない場合や衝突チェックを省く経路では、移動が行われなくても `true` を返します。可動設定（Mobility）が `Movable` でないアクターはプレイ中に移動できないため、これまではコマンドが成功を報告しながらアクターが動いていませんでした。今後は移動の前後で位置と回転を突き合わせ、何も変わっていなければ **`ExecutionFailed`** を返します。拒否メッセージは原因も名指しします（**可動設定**／**root コンポーネントが無い**／**要求した場所に置けなかった**）。従来はこの 3 通りが「移動に失敗した」の一文に押し込められていました。衝突で目的地から近くへずらされた場合は、これまでと同じく成功です。同じ理由で `UAIP.Editor.Level.SetActorTransform` も、適用できなかった場合（root コンポーネントを持たないアクター）に `ExecutionFailed` を返すようになりました。

> **エディタのプレイセッションではないゲームワールドは `PIEInstance: -1` を返します**（パッケージ実行時の単一ワールドなど）。この `-1` はここでは実在の番号であり、**そのまま `TargetPIEInstance` に渡せます**。「インスタンス無し」を表す番兵値として除外しないでください。

### Data Layer ランタイム状態（4 件）

**実行中のプレイワールド**における World Partition Data Layer の状態を扱います。Data Layer のオーサリング — 作成・親子付け・レベル開始時の状態指定 — は [`UAIP.Editor.WorldPartition`](#uaipeditorworldpartition) の担当で、このグループはディスクへ何も書き込みません。`DataLayerInstanceId` はエディタ側コマンドと同じ識別子なので、プレイ開始前に調べておいたものをそのまま渡せます。

| コマンド | 説明 |
|---|---|
| `SetDataLayerRuntimeState` | ランタイム Data Layer インスタンス 1 つの状態を設定します。`RuntimeState` は `Activated` / `Loaded` / `Unloaded`（大文字小文字は区別せず、それ以外の綴りは受理値 3 つを列挙した `InvalidParams`）。`bIsRecursive: true` で同じ状態を全子孫へ適用し、応答に `AffectedCount`、`bPartialSuccess`、`RejectedDescendants[]` が加わります（各要素は `DataLayerInstanceId` と短い `RejectionReason` トークン `NotRuntime` / `ClientOnlyFromServer` / `ServerOnlyFromClient` / `AuthoritativeFromClient` / `Unknown`）。ただし*指定した*インスタンス自身が拒否された場合は、部分成功ではなくコマンド全体が失敗します。応答には `PreviousRuntimeState`、`RequestedRuntimeState`、`EffectiveRuntimeState`、`bStateChanged`、`bEffectiveStateDiffers`、`LimitingAncestorId`（祖先を実際に特定できたときのみ）、ストリーミングフラグ 2 つ、作用したワールドの情報が含まれます。識別子が未知なら `NotFound`。**実行時状態を持たない Data Layer（編集専用・非公開）も同じく `NotFound`** です。エンジンはプレイ開始時にそれらをワールドから取り除くため、プレイワールドから見ると最初から存在しません。World Partition 無効なワールドなら `ExecutionFailed`、ワールドのネットワーク役割が変更を許さない場合は `NotAllowed`。`RuntimeDataLayerControl` 必要 |
| `ListDataLayerRuntimeStates` | 対象プレイワールドの全 Data Layer インスタンスを、`DataLayerInstanceName`、`DataLayerType`、`RuntimeState`、`EffectiveRuntimeState`、`ParentInstanceId`（ルートでは省略）、`bIsClientOnly`、`bIsServerOnly` 付きで返します。**配列本体は JSON Artifact 側にあり**、応答には配列の要素数である `Count` と、`bIsWorldPartitionEnabled`、`NetMode`、`WorldContext`、`PIEInstance` が含まれるため、Artifact を取得しなくても分岐できます。一覧に現れるのは実行時状態を持つ Data Layer だけです。編集専用・非公開のものはプレイ開始時にワールドから取り除かれるためここには出ません。種別込みで見たい場合はエディタ側の [`ListDataLayers`](#uaipeditorworldpartition) を使ってください。World Partition 無効なレベルではエラーではなく、空リスト ＋ `bIsWorldPartitionEnabled: false` を返します。Capability 不要 |
| `GetDataLayerRuntimeState` | インスタンス 1 つの完全な記述を返します。`ListDataLayerRuntimeStates` と同じ項目に加えて `bEffectiveStateDiffers`、`LimitingAncestorId`、ストリーミングフラグ 2 つ。小さいので全体が Artifact と応答の両方に入ります。World Partition 無効なレベルでは `NotFound` ではなく `bIsWorldPartitionEnabled: false` を返します — これが「このレベルには Data Layer が存在しない」と「その識別子の Data Layer が無い」を区別します。Capability 不要 |
| `WaitForDataLayerStreaming` | `DataLayerInstanceIds` で指定したインスタンス群 — 省略または空なら対象ワールドの全ランタイム Data Layer インスタンス — のストリーミングが落ち着くまでポーリングします。完了すると `ElapsedSeconds` と空の `IncompleteDataLayerInstanceIds[]` を伴う `Success`、時間切れなら同じ項目に未完了分を列挙した `Timeout` を返します。待機中にプレイワールドが破棄された場合は `ExecutionFailed` となり、待機がセッションより長生きすることはありません。World Partition 無効なレベルでは待たずに `bIsWorldPartitionEnabled: false` で完了します。Capability 不要 |

> **`WaitForDataLayerStreaming` の上限は待機開始前に検査され、違反は `Timeout` ではなく `InvalidParams` になります。** `TimeoutSeconds` は既定 30、0 より大きい有限の数値で**最大 60** — `WaitForCondition` と同じ上限で、待機系コマンドの契約を揃えています。`PollIntervalSeconds` は既定 0.1 で 0.05〜1.0 の範囲。`DataLayerInstanceIds` は**最大 64 件**で、それ以上必要な場合はパラメータを省略してワールド全体を待つよう切り替える合図です。リスト中に存在しない識別子があれば、これも待機前に `NotFound` となります。

> **2 つのストリーミングフラグは別々の問いに答えており、どちらも他方を包含しません。** `bStreamingCompleted` は対象の Data Layer に絞られていますが、位置に応じて読み込まれるセルを見ません。`bWorldStreamingCompleted` はワールド全体を見ますが、対象の Data Layer には絞れません。`SetDataLayerRuntimeState` / `GetDataLayerRuntimeState` / `WaitForDataLayerStreaming` がいずれも両方を返すのはこのためです — **確実を期すなら両方が完了になるまで待ってください**。

> **`bStateChanged` は成功フラグではありません。** 「状態が以前と変わったか」に答えるものなので、すでに要求と同じ状態だった Data Layer は、完全に成功した呼び出しでも `bStateChanged: false` を返します。要求が効いたかどうかは `RequestedRuntimeState` と `EffectiveRuntimeState` の一致で判定してください。両者が食い違う場合は `bEffectiveStateDiffers` が `true` になり、`LimitingAncestorId` が実効状態を抑えている祖先を示します — 未読み込みの親は子が到達できる状態に上限を課しますが、要求自体は失われず記録されています。

### Toolset ブリッジ（1 件）🧩

`EditorAppToolset`（UE 5.8+、EditorToolset プラグイン）経由のブリッジコマンド。プロバイダ：`Toolset.Editor.Toolset.World.*`。

| コマンド | 説明 |
|---|---|
| `Toolset.Editor.Toolset.World.SearchCVars` | ⚠️ **非推奨** — `Toolset.Editor.Toolset.EngineManagement.SearchCVars` を使用してください。コンソール変数を名前の部分一致で検索。機微な変数は除外（`CVarInspect` 必要）。現在は `UAIPEditorEngineManagement` モジュールが提供し、移行先のコマンドと同じ動作をします。応答には `SensitiveExclusionCount` が付きます |

---

## UAIP.Runtime.Observation

ランタイムキャプチャと状態ダンプ。

| コマンド | 説明 |
|---|---|
| 🆓 `CaptureViewportImage` | 指定プレイヤーのゲームビューポートを PNG キャプチャ |
| 🆓 `DumpWorldState` | アクティブな PIE ワールドの全アクター / コンポーネントのスナップショット（JSON） |
| 🆓 `DumpActorState` | 指定アクターの状態（任意でコンポーネント含む）。見つからないアクターは `ExecutionFailed` ではなく `NotFound` になるため、シナリオの `RetryCount` では再試行されません |
| 🆓 `DumpComponentState` | 指定アクターコンポーネントの状態。見つからないコンポーネントは `ExecutionFailed` ではなく `NotFound` になるため、シナリオの `RetryCount` では再試行されません |
| 🆓 `DumpRuntimeLog` | バッファリングされた Runtime ログ（テキスト Artifact） |
| 🆓 `CapturePerformanceSnapshot` | CPU / GPU パフォーマンススナップショット（FPS・メモリ・ドローコール） |
| 🆓 `CheckpointCapture` | スクリーンショット + 状態ダンプの複合（シナリオ primitive） |
| 🆓 `SearchLoadedClasses` | ロード済みクラスを検索（ランタイム内省用） |
| 🆓 `DumpGameViewportWidgets` | プレイワールドのゲームビューポートの Widget ツリーを返します。ゲーム自身の UI だけで、エディタのツールバーやタブは混ざりません。ツリー全体は JSON artifact に保存し、応答にはノード数、`MaxDepth` / `MaxNodes` で走査が途中で止まったか・どこで止まったか、上位のユーザー Widget の先頭 50 件、各ローカルプレイヤーのキーボード / ゲームパッドのフォーカスと画面領域、`Limitations` が入ります。各ノードは Slate の型、UMG の名前とクラス、矩形、実際に見えているか、どのレイヤーにあるかを持ちます。テキストは `IncludeText: true` のときだけ読みます。[ゲームビューポートの UI と HUD](#ゲームビューポートの-ui-と-hud4) を参照 |
| 🆓 `FindGameViewportWidgets` | 同じツリーから、指定した条件をすべて満たすノードを探します（`WidgetClass`・`SlateType`・`WidgetName` / `WidgetNameContains`・`OwningPlayerIndex`。1 つ以上が必須）。`WithinWidgetPath` を渡すと、CommonUI の画面など 1 つの Widget の部分木に探す範囲を絞れます。一致には、`ClickGameViewportWidget`・`PressGameViewportUIKey`・`TypeGameViewportText` に渡し直す `TypePath` と `Fingerprint` が付きます。何も見つからなくても成功です。一覧を切ったか、走査が途中で止まったかは `ResultLimitReached` と `SearchIncomplete` の limitation で分かります。テキストは読みません |
| 🆓 `DumpGameViewportWidgetTexts` | ゲームビューポートの**すべての**テキスト Widget のテキストと、入力欄の値を、画面に出ているかどうかを問わず JSON artifact として返します。各エントリに、そのテキストが画面に出ているかの印が付きます。`RuntimeWidgetTextRead`（DefaultDenied）が必要です。パスワード欄の平文は artifact には書かれず、セッションが `RuntimeWidgetPasswordTextRead` も持ち、かつ安全設定 `AllowRuntimePasswordFieldRead` がオンのときだけ応答（`PasswordFieldValues`）に入ります |
| 🆓 `DumpHUDState` | 各ローカルプレイヤーの HUD の状態を JSON artifact として返します: HUD のクラス、表示フラグ、`ShowDebug` の状態、デバッグテキスト、ヒットボックスの名前、HUD が参照している Widget、プレイヤーコントローラーが画面に出している Widget。HUD が描いた内容（線・文字・ボックス）とヒットボックスの位置は読めず、`Limitations` で報告します |
| 🆓 `ListSubsystems` | エンジン・GameInstance・プレイワールド・ローカルプレイヤーの下で生きている Subsystem を、実体ごとに 1 行（クラス・クラスパス・実体のパス・所有者・状態）で返します。行は決まった 1 つの順に並び、`StartIndex` / `MaxEntries` でページに区切られます。`IncludeNotCreated: true` を付けると、ロード済みで所有者の下に実体が無いクラスも載ります。`Engine` 種別だけの要求ならプレイワールド無しで動きます。プロパティの値は読みません |
| 🆓 `DumpSubsystemState` | 1 つの Subsystem の実体のプロパティの値を JSON artifact として返します。`RuntimeInspect` と `SubsystemStateDump`（DefaultDenied）が必要です。応答には要約だけが載り、値は artifact に入ります。⚠️ `SubsystemStateDump` を外しても、すでに作られた artifact は残ります — [Safety & Capabilities](safety.md#runtime-subsystem) を参照 |

### ゲームビューポートの UI と HUD（4）

実行中のゲームの UI を読み取ります: ゲームビューポートにどの Widget があるか、どこにあるか、見えているか、HUD が何を表示する状態か。返るのはゲーム自身の UI だけで、エディタのツールバーやタブは混ざりません。エディタ全体を対象にする `DumpSlateTree` との違いはここです。PIE でも `-game` 起動でもパッケージ版でも、同じコマンドで使えます。4 つとも [`TargetNetRole` / `TargetPIEInstance`](#実行時コマンドの対象プレイワールドを指定する) を受け付け、読み取り専用です: 安全ポリシーが `ReadOnly` のときもモーダルが開いている間も動きます。ゲームビューポートを持たないワールド（サーバーのワールド）は `NotAllowed` で拒否され、選び直せるクライアント側のプレイワールドが応答に添えられます。

**Capability。** `DumpGameViewportWidgets`・`FindGameViewportWidgets`・`DumpHUDState` は `RuntimeInspect`（DefaultAllow）が必要です。`DumpGameViewportWidgetTexts` は `RuntimeWidgetTextRead`（DefaultDenied）が必要で、応答にパスワード欄の平文を入れるには、さらに `RuntimeWidgetPasswordTextRead`（DefaultDenied）が必要です。足りない場合は、その名前を示した `CapabilityNotAvailable` になります。`DeniedCapabilities` で明示的に拒否している場合は `PolicyViolation` です。詳細は [安全性と Capability](safety.md#runtime-ゲームビューポートの-ui) を参照してください。パスワード欄の平文には、安全設定 `AllowRuntimePasswordFieldRead=True` も必要です。Capability だけでは値は伏せられ、`PasswordTextWithheldBySafetyPolicy` の limitation が件数を示します。

**見つけた Widget を操作するには**、一致の `TypePath` と `Fingerprint` を [`ClickGameViewportWidget`・`PressGameViewportUIKey`・`TypeGameViewportText`](#ゲームビューポートの-ui-入力3) に渡し、効果はもう一度ツリーを読んで確かめます。

#### 読み取りが表すもの

- **矩形**は、ゲームビューポート左上を原点とした物理ピクセルで、直前に描いたフレームの位置です。操作の直後は古い位置のことがあります。描画しない環境（`-nullrhi`）ではツリーは取れても矩形は取れず、`Limitations` に理由が出ます。
- **テキスト。** `DumpGameViewportWidgets` を `IncludeText: true` で呼んだとき平文になるのは、**画面に出ている**テキストだけです。256 文字で切り詰め、制御文字は除きます。次のものは画面に出ていないとみなします: 非表示、UI の不透明度・色の設定で完全に透明（マテリアルなど色以外の手段で透明にしたものは判定できません）、スクロールの外やビューポートの外などで切り取られている・大きさが 0、描画できない環境。他の Widget に**覆われている**かどうかは判定しません。覆われたテキストも平文になり、その旨が注記されます。入力欄は、長さの区分 — `Empty`、`NonEmpty`（1〜127 文字）、`Long`（128 文字以上）— と、パスワード欄かどうかだけを返します。パスワード欄かどうか判定できない欄は、パスワード欄として扱います。
- **`DumpGameViewportWidgetTexts` はすべてを返します。** 画面に出ているかを問わず、各エントリに出ているかの印が付きます。結果は artifact に保存され、既定では 24 時間残り、既定の HTTP 設定では ID を知っていれば誰でも取得できます。パスワード欄の平文は artifact には書かれず、`RuntimeWidgetPasswordTextRead` があり、かつ安全設定 `AllowRuntimePasswordFieldRead` がオンのときだけ応答の `PasswordFieldValues`（最大 16 件・各 256 文字。残りは件数だけ）に入ります。Capability が無いときは `PasswordTextWithheld` の limitation が、Capability はあるが安全設定がオフのときは `PasswordTextWithheldBySafetyPolicy` の limitation が、伏せた欄の数を示します。
- **Blueprint のバインディングが呼ばれることがあります。** Widget が何を表示するかを求める過程で、ゲームの Blueprint のバインディング関数が呼ばれることがあります。Widget の観測の応答は、常に `Limitations` でそれを知らせます。
- **`FindGameViewportWidgets` は既定で見えている Widget だけを探します**（`VisibleOnly: true`）。ここでの「見えている」は、自分と親の表示の設定で非表示になっていないことです。不透明度が 0 の Widget や画面の外にある Widget も含むので、テキストの「画面に出ている」より広い意味です。何も見つからなくても成功です。応答は、一覧を切ったか（`ResultLimitReached`）、走査が途中で止まったか（`SearchIncomplete`）、見えている Widget だけを探した結果の 0 件か、を示すので、「無い」と「見ていない」を区別できます。
- **開いているドロップダウン**（ゲーム自身のメニュー）の中身もツリーに含まれます。
- **フォーカス。** 応答は、各ローカルプレイヤーのフォーカスが UI にあるか、ゲームビューポートそのものにあるか、ゲームビューポートの外にあるか、どこにも無いかを返します。

#### パラメータ

| パラメータ | コマンド | 意味 |
|---|---|---|
| `MaxDepth` | `DumpGameViewportWidgets`・`FindGameViewportWidgets`・`DumpGameViewportWidgetTexts` | 走査する最大の深さ。1〜128（ルートが 0）。既定 64。範囲外は切り詰めずに `InvalidParams` で拒否されます |
| `MaxNodes` | 同じ 3 つ | 走査するノード数の上限。1〜20000。既定 5000。範囲外は拒否されます |
| `IncludeDebugLayer` | 同じ 3 つ | ウィンドウのオーバーレイより下のデバッグ層も走査します。既定 `false` |
| `IncludeCollapsed` | 同じ 3 つ | 自身の表示が `Collapsed` の枝も走査します。既定 `true` |
| `IncludeText` | `DumpGameViewportWidgets` | 画面に出ているテキストを含めます（上記）。既定 `false` |
| `WidgetClass` | `FindGameViewportWidgets` | UMG Widget のクラス名（大文字小文字を区別しない）。クラスはロードしないため、親クラスでの一致はすでにロード済みのクラスに限られます |
| `IncludeSubclasses` | `FindGameViewportWidgets` | UMG Widget の親クラスも `WidgetClass` と比べます。既定 `true` |
| `SlateType` | `FindGameViewportWidgets` | Slate の型名。完全一致（例: `STextBlock`） |
| `WidgetName`・`WidgetNameContains` | `FindGameViewportWidgets` | UMG Widget の名前の完全一致 / 部分一致（大文字小文字を区別しない）。同時には指定できません |
| `OwningPlayerIndex` | `FindGameViewportWidgets` | そのノードが属するユーザー Widget を持つ**ローカルプレイヤー**の番号（0 以上）。何も持たない、またはいないプレイヤーは一致 0 件で、成功です |
| `VisibleOnly` | `FindGameViewportWidgets` | 実際に見えている Widget だけを対象にします。既定 `true` |
| `MaxResults` | `FindGameViewportWidgets` | 返す一致の上限。1〜500。既定 50。超えた分は数えるだけで返しません |
| `WithinWidgetPath` | `FindGameViewportWidgets` | 中を探す UMG Widget のオブジェクトパス（4096 文字以内）。たとえば [`UAIP.Runtime.CommonUI.DumpActivatableStacks`](#uaipruntimecommonui-) が画面ごとに返す `WidgetPath`。探す範囲を絞るもので、それだけでは条件になりません。ゲーム層の全体を走査することに変わりはないので、`MaxDepth` / `MaxNodes` はゲーム層の根から数え、`TypePath` もその根からの相対のままです。ゲーム層の下の Widget に行き着かないパスは、パラメータ名を挙げて `NotFound` です。走査がその Widget に届かなかった場合（非表示・折りたたみ・表示されていないページ・上限の外）は、一致なしで limitation `ScopeRootNotTraversed` が付きます。渡した値は `Result` と artifact にそのまま返します |
| `RootTypePath` | `DumpGameViewportWidgetTexts` | サブツリーをダンプする Widget の `TypePath`。ゲーム層の全体を走査することに変わりはないので、`MaxDepth` / `MaxNodes` はゲーム層のルートから数えます。Widget に至らない経路は `NotFound`。既定はゲーム層全体 |
| `PlayerIndex` | `DumpHUDState` | 調べる**ローカルプレイヤー**の番号（0 が 1 人目）。省略すると全ローカルプレイヤー。いない番号は `NotFound` |
| `TargetNetRole`・`TargetPIEInstance` | 4 つすべて | どのプレイワールドか。[対象プレイワールドを指定する](#実行時コマンドの対象プレイワールドを指定する) を参照 |

`FindGameViewportWidgets` は、`WidgetClass`・`SlateType`・`WidgetName`・`WidgetNameContains`・`OwningPlayerIndex` のうち 1 つ以上を必要とします。1 つも無い場合や、`WidgetName` と `WidgetNameContains` を同時に指定した場合は `InvalidParams` です。`WithinWidgetPath` は条件に数えないので、それだけを渡した場合も `InvalidParams` です。

#### 拒否される場合

| 状況 | 結果 |
|---|---|
| プレイワールドが無い、`TargetPIEInstance` に合うワールドが無い、サーバーのワールド | `NotAllowed`（サーバーのワールドには選び直せるクライアント側の候補が添えられます） |
| `TargetNetRole` と `TargetPIEInstance` が矛盾する、または複数のワールドに当てはまる | `InvalidParams` |
| ゲーム層がまだ無い（起動直後） | `PreconditionFailed`。少し待って再試行します（シナリオでは自動で再試行されます） |
| ゲーム層の場所を特定できない（プロジェクトが標準の UI 層を置き換えている） | `NotAllowed`。対応するのは標準のゲーム層だけです |
| `DumpHUDState` の `PlayerIndex` がいないプレイヤーを指す | `NotFound` |
| `FindGameViewportWidgets` の `WithinWidgetPath` がゲーム層の下の Widget に行き着かない | `NotFound`（`WithinWidgetPath` を名指しする） |

#### HUD

`DumpHUDState` は、ローカルプレイヤーごとに、HUD のクラスと表示フラグ、`ShowDebug` の状態、デバッグテキスト（HUD が描かれていないときも返り、その場合は結果にそう注記されます）、ヒットボックスの名前、HUD が参照している Widget（最大 64 件）、プレイヤーが画面に出している Widget を返します。これらの一覧にはそれぞれ件数の上限があり、切ったときはそう注記されます。エンジンの版が提供しない欄は、理由とともに省かれます。ゲームビューポートの Canvas の描画統計（描画のまとまりの数）は、`DefaultUAIP.ini` の `[UAIP.RuntimeObservation]` で `EnableHUDCanvasStats=True` にしたときだけ添えられます（起動時に読むので、再起動が必要です）。無効のときは、`Limitations` が有効にする方法を示します。統計は、そのゲームビューポートに HUD が描かれた直近のフレームの値で、フレームをまたいで足し上がりません。分割画面では、そのフレームにそのビューポートへ描いた全 HUD の合計になります。まだ HUD が一度も描かれていないゲームビューポートには統計が無く、結果にそう注記されます。[安全性と Capability](safety.md#runtime-ゲームビューポートの-ui) を参照してください。

### Subsystem（2）

実行中のゲームの Subsystem を読み取ります: どの Subsystem がどの所有者の下で生きているか、そして（許可した場合に）その 1 つの中身の値です。Subsystem は 4 種類の所有者のいずれかの下にあります: `Engine`、`GameInstance`、`World`（プレイワールド）、`LocalPlayer`。どちらのコマンドも読み取り専用で、安全ポリシーが `ReadOnly` のときも実行できます。

**Capability。** `ListSubsystems` は `RuntimeInspect`（DefaultAllow）を必要とします。`DumpSubsystemState` は `RuntimeInspect` に加えて `SubsystemStateDump`（DefaultDenied）を必要とします。値はプロジェクトが保持しているものそのままで、秘密が含まれることもあるためです。足りない Capability は、その名前を示した `CapabilityNotAvailable` になります。`DeniedCapabilities` で明示的に拒否している場合は `PolicyViolation` です。[Safety & Capabilities](safety.md#runtime-subsystem) を参照してください。

**プレイワールド。** `Engine` 種別だけの要求はプレイワールドを必要とせず、`TargetNetRole` も `TargetPIEInstance` も受け付けません。応答にもワールドの情報（ネットモード・PIE インスタンス）は載りません。それ以外の種別はプレイワールドが必要で、対象は [`TargetNetRole` / `TargetPIEInstance`](#実行時コマンドの対象プレイワールドを指定する) で選びます。プレイワールドが無いときはそのような要求は `NotAllowed` になり、代わりに `Engine` の結果を返すことはしません。

**デモ版。** 2 つのコマンドはどちらもデモ版に含まれます。デモ版の既定の設定は `SubsystemStateDump` を許可していません。`DumpSubsystemState` を使うには、自分で `+AllowedCapabilities=SubsystemStateDump` を追加してください。

#### 読み取りの内容

- `ListSubsystems` の **行** には、`Scope`・`ClassName`・`ClassPath`・`ObjectPath`・`Owner`（所有者が持つ部分だけ: `PIEInstance`・`PlayerIndex`）・`Status`・`IsTickableWorldSubsystem` が載ります。`Status` は `Created`（生きている実体）、`NonAuthoritativeClass`（ホットリロード・Live Coding・Blueprint の再コンパイルでクラスが新しい版に置き換わった後も残っている、改名された旧クラスの実体）、`NotCreated`（ロード済みで所有者の下に実体が無いクラス。`IncludeNotCreated: true` のときだけ）のいずれかです。
- **並び順。** 行は種別（`Engine`・`GameInstance`・`World`・`LocalPlayer`）、PIE インスタンス、プレイヤー番号、状態、クラスパス、実体のパスの順に並びます。同じ状態なら、いつ呼んでも同じ行が同じ順で返ります。
- **ページ。** 応答にはそのページの先頭 50 行が載り、JSON artifact にはページ全体が入ります。`Truncated: true` は続きのページがあることを示します。`NextStartIndex` を `StartIndex` に指定して呼び直してください（残りが無いときは `NextStartIndex` は省かれます）。`DataEntriesTruncated` は、応答の行数がページより少ないことを示します。`StartIndex` が全件数以上なら空のページが返り、これは成功です。
- **件数。** `TotalCount`・`CreatedCount`・`NonAuthoritativeCount`・`NotCreatedCount` は、`ClassNameContains` で絞った後、ページに区切る前の件数です。`Scopes[]` は要求した種別ごとに 1 件で、`Scope`・`Availability`（`Available` または `Unavailable`）・`Count`、利用できないときは `Reason` が載ります。
- **`IncludeNotCreated`** は、ロード済みのクラスと各所有者の下の実体を突き合わせます。ロードされていないクラスは載りません。`Engine` 種別には `NotCreated` の行は出ません。作られなかった理由は返りません。まだ Subsystem を作っていない所有者（GameInstance やプレイヤーを追加した直後など）は、行が 0 件になるだけです。どれが当てはまるかは `Limitations` に書かれます。
- **`DumpSubsystemState`** が選ぶのは、指定したクラスそのものだけです。基底クラスを指定しても、派生クラスの実体は選ばれません。応答の Data には、識別（`Scope`・`ClassName`・`ClassPath`・`ObjectPath`）、`Owner`、`Status`、`PropertyCount`、`IncludedCount`、`Truncated`、`StopReason`（ダンプが途中で止まったときだけ）、`Limitations` が載ります。プロパティは artifact の `Properties[]` にだけ入り、それぞれ `Name`・`DeclaredBy`・`Type`・`Flags`（Transient・Config・BlueprintVisible・BlueprintReadOnly・Net・SaveGame のうち立っているもの）・`Value` を持ち、基底クラス側から宣言順に並びます。Subsystem の共通の基底クラスが持つプロパティと、エディタ専用のプロパティは載りません。
- **大きさ。** ダンプは約 256 KiB で打ち切られます。それでも成功で、`Truncated: true` と `StopReason`（実際には `TotalBudget`）が付き、`PropertyCount` には省かれたプロパティも数えられます。コンテナは先頭 32 要素、文字列は 1024 文字で切られ、構造体は 1 段だけ展開され、参照は参照先のパスで書かれます（辿りません）。
- **リロードの後。** ホットリロードや Live Coding の前から残っている Subsystem は、改名後のクラス名で `NonAuthoritativeClass` として一覧に出ます。ダンプするには、その改名後の名前かパスを指定します。現行のクラスに実体が無く、同じ所有者に古い実体が残っているときは、`NotFound` の結果の `Candidates` に改名後のクラス名が並びます（最大 16 件）。

#### パラメータ

| パラメータ | コマンド | 意味 |
|---|---|---|
| `Scopes` | `ListSubsystems` | `Engine`・`GameInstance`・`World`・`LocalPlayer` のうち、重複しない 1〜4 個の名前（大文字小文字は区別しません）。既定は 4 種類すべて。プレイワールド無しで動くのは `Engine` だけです |
| `PlayerIndex` | 両方 | **ローカルプレイヤー**の番号（0 は GameInstance の最初のローカルプレイヤー）。`ListSubsystems` では `Scopes` に `LocalPlayer` を含むときだけ指定でき、省くと全ローカルプレイヤーを一覧します。`DumpSubsystemState` では `Scope: LocalPlayer` のときだけ指定でき、ローカルプレイヤーがちょうど 1 人のあいだに限り省けます |
| `ClassNameContains` | `ListSubsystems` | クラス名に含まれていなければならない文字列。1〜256 文字、大文字小文字は区別しません。行を集める段階で適用されます |
| `IncludeNotCreated` | `ListSubsystems` | 所有者の下に実体が無いロード済みのクラスも、状態 `NotCreated` で一覧に加えます。既定は `false`。`Engine` 種別には適用されません |
| `StartIndex` | `ListSubsystems` | 並べ替えた一覧の中で、ページの最初の行の位置。0 以上、既定は 0 |
| `MaxEntries` | `ListSubsystems` | 1 ページの行数の上限。1〜4096、既定は 256。範囲外の値は丸められず `InvalidParams` で拒否されます |
| `Scope`（必須） | `DumpSubsystemState` | `Engine`・`GameInstance`・`World`・`LocalPlayer`（大文字小文字は区別しません） |
| `SubsystemClass`（必須） | `DumpSubsystemState` | Subsystem のクラス。`A-Z a-z 0-9 _ . / : -` の 1〜1024 文字。スラッシュを含む値はクラスパス、それ以外はクラスのオブジェクト名と完全一致で（大文字小文字は区別せず）比べる短いクラス名です。C++ の型名の頭の `U` は付けても外してもかまいません。Blueprint のクラスは `_C` 付きの名前が必要です。対象にできるのはロード済みのクラスだけです |
| `TargetNetRole`、`TargetPIEInstance` | 両方 | どのプレイワールドか。[対象プレイワールドの指定](#実行時コマンドの対象プレイワールドを指定する)を参照してください。`Engine` 種別だけを指定した要求では受け付けません |

#### エラー

| ErrorCode | 発生条件 |
|---|---|
| `InvalidParams` | パラメータが欠けている・型が違う・範囲外・未知のキー。未知または重複した種別。`LocalPlayer` 以外の種別に付けた `PlayerIndex`。`Engine` 種別だけの要求に付けたプレイワールドの指定。`TargetNetRole` / `TargetPIEInstance` が互いに矛盾する、または複数のワールドに一致する。`ListSubsystems` では、`ClassNameContains` で絞った後も 65536 行を超える要求（`IncludeNotCreated` を外すか、要求を絞ってください）。`DumpSubsystemState` では、複数の場所のクラスに一致する短い `SubsystemClass`（クラスパスが `Candidates` に入ります。そのうち 1 つを指定して呼び直してください）と、ローカルプレイヤーが 2 人以上いるのに `PlayerIndex` を省いた `Scope: LocalPlayer` |
| `NotAllowed` | `Engine` 以外の種別を指定したのにプレイワールドが動いていない、または `TargetNetRole` / `TargetPIEInstance` に一致するものが無い |
| `NotFound` | `DumpSubsystemState`: 対象が存在しない。結果の `Reason` が理由を示す（下記）。`ListSubsystems`: どのローカルプレイヤーも持たない `PlayerIndex`（`Reason` は `PlayerNotFound`。プレイワールドに GameInstance が無いときは `NoGameInstance`） |
| `CapabilityNotAvailable` | `RuntimeInspect`、`DumpSubsystemState` では `SubsystemStateDump` も、許可されていない |
| `PolicyViolation` | Capability が安全ポリシーで拒否されている |

`NotFound` の結果には、機械で読める `Reason` が付きます。

| `Reason` | 意味 |
|---|---|
| `NotInstantiated` | クラスはロード済みだが、その種別・所有者の下に実体が無い。`Candidates` には、リロード前から残っている改名後の実体が載ることがあります |
| `ClassNotFound` | 名前やパスに一致するロード済みのクラスが無い。`Candidates` には、その種別・所有者の下に実在するクラス名が載ります（最大 16 件）。ロードされていないクラスは対象にできません |
| `NoGameInstance` | プレイワールドに GameInstance が無いため、GameInstance もローカルプレイヤーも存在しない |
| `NoLocalPlayer` | GameInstance にローカルプレイヤーがおらず（専用サーバーなど）、`PlayerIndex` も指定されていない |
| `PlayerNotFound` | `PlayerIndex` を指定したが、その番号のローカルプレイヤーがいない |

同じ 5 つの値は、`Unavailable` になった `ListSubsystems` の `Scopes[]` の `Reason` にも現れます。`PlayerIndex` を指定しない `ListSubsystems` はこれらの理由では失敗せず、その種別が理由付きで `Unavailable` と報告され、他の種別は通常どおり返ります。

成功した呼び出しは必ず JSON artifact を 1 つ保存します。失敗した呼び出しは保存しません。

---

## UAIP.Runtime.Execution

PIE / Standalone でのテスト実行。

| コマンド | 説明 |
|---|---|
| `RunFunctionalTest` | PIE ワールドの `AFunctionalTest` アクターを表示名（アクターラベル）で指定して実行し JSON レポートを返す |
| `RunRuntimeAutomationTest` | PIE 文脈で UE Automation Test を実行し、テストごとのレポート（Pass / Fail / Skipped / Error / Cancelled。[レポートの共通契約](#automation-test-のレポートの共通契約) を参照）を返す |
| `RunGauntletTest` | RunUAT 経由で Gauntlet テストを外部プロセスとして起動 |

> **`RunFunctionalTest`** は、PIE ワールドの `AFunctionalTest` アクターのうち、表示名（アクターラベル）が `TestPath` と大文字小文字を無視して完全一致するものを実行します。名前はファイルパスではないため、`..` を含む名前も使えます。
>
> **`RunGauntletTest`** は `TestName`（必須）、`TestParams`（任意）、`TimeoutSec`（任意。1 から 1800、既定 600）を受け取ります。`GauntletExecution` Capability が必要です。以下の書式の外にあるものは `InvalidParams` で拒否され、何も起動されません。
>
> **`TestName`** は 512 文字以下で、カンマ区切りのテスト指定の並びです。例は `UE.BootTest` です。
>
> - 各指定はドット区切りの名前です。各部分は ASCII の英字か `_` で始まり、その後ろは ASCII の英字・数字・`_` です。
> - 指定の後ろに、括弧で囲んだテスト単位のパラメータリストを 1 つ付けられます。リストには ASCII の英字・数字と `_ . , = + - '` を書けますが、`..` と括弧の入れ子は使えません。
> - `/`、`\`、`:`、空白、引用符などの文字は拒否されます。
>
> **`TestParams`** は 32 件以下のオブジェクトで、値はすべて文字列です。パラメータは Gauntlet に `-Key="Value"` の形で渡されます。
>
> - **キー**: 1 から 128 文字で `[A-Za-z][A-Za-z0-9_]*` に一致するもの。先頭に `-` を付けずに書きます。`.` は使えません。
> - **値**: `[A-Za-z0-9_.:/+-]` の文字だけで 1024 文字以下。`..` は含められません。空の値は許可されます。
>
> 書式が正しくても、テストやその子プロセスの動作を変えるものがあります。これらには `GauntletUnrestrictedArguments` Capability が必要で、既定では拒否されます（[Safety & Capabilities](safety.md) 参照）。持っていない場合は `CapabilityNotAvailable` で失敗します。以下の照合はすべて大文字小文字を無視します。
>
> - `TestName` の括弧によるテスト単位のパラメータリスト。
> - 末尾が次のいずれかのキー: `Args`、`ExecCmds`、`Cmds`、`CommandLine`、`Cmdline`、`Platform`、`Configuration`、`Flavor`、`Dir`、`Directory`、`Path`、`Root`、`File`、`URL`。
> - 先頭が次のいずれかのキー: `Skip`、`Editor`、`Script`、`Automation`、`Horde`、`Telemetry`、`Device`、`P4`。
> - 次のいずれかに完全一致するキー: `NoCompileUAT`、`noturnkeyvariables`、`profile`、`ScriptsForProject`、`Bootstrap`、`Build`、`Builds`、`Project`、`ProjectName`、`Target`、`CustomModuleRoles`、`Sandbox`、`Clean`、`FullClean`、`cleardevices`、`Reboot`、`FirmwareVersion`、`UpdateFirmware`、`TryUpdateFirmware`、`VerifyLogin`、`test`、`tests`、`Namespaces`、`RunTest`、`TestFilter`、`TagFilter`、`Map`、`Controller`、`EnablePlugins`、`DDC`、`RHI`、`UseEditor`、`CookedEditor`、`packaged`、`staged`、`bulk`、`notbulk`、`devices`、`PerfSpec`、`PrefSpec`、`PerfModel`、`PrefModel`、`RequiredDeviceTags`、`PreferredDeviceTags`、`UndesiredDeviceTags`、`BlockedDeviceTags`、`WorkerJobID`、`LocalDeviceIndex`、`MaxLocalDevices`、`MaxVirtualDevices`、`username`、`password`、`JobDetails`、`PublishTelemetryTo`、`PerfReportServer`、`uploadreport`、`UseAgentTag`、`EnableHordeDeviceReservations`、`clientip`、`serverip`、`hostip`、`EpicApp`、`McpRegion`、`McpSubRegion`、`BuildIDOverride`、`NoMCP`、`RemoteServer`、`RequiresLogin`、`PreAssignAccount`、`ArtifactName`、`ArtifactPostfix`、`PgcFilenamePrefix`、`LocalReplay`、`MemPro`、`EditorTraces`、`ClientTraces`、`ServerTraces`、`VerboseLogCategories`、`Compile`、`NoCompile`、`CompileOnly`、`Submit`、`NoSubmit`、`NoKill`、`BuildMachine`、`UseLocalBuildStorage`、`WaitForDebugger`、`List`、`Help`、`forcestepfail`、`listargs`、`listallargs`。
> - Gauntlet が子プロセスへ転送するキー: `TestName` の各ドット区切りの部分、および既定の名前空間（`Gauntlet`、`UnrealTest`、`UnrealGame`、`UnrealEditor`）の各部分について、最初の `test` より前の文字列（`test` を含まない部分は部分全体）で始まるキー。`UE.BootTest` では `UE` と `Boot` などが該当します。`test` で始まる部分があると、すべてのキーが転送されます。
> - `:` を含む値、または `+` で区切った要素のどれかが `/` で始まる値（絶対パス・UNC パス・URL）。
> - `-` と ASCII の英字で始まる値。RunUAT.bat が自身のスイッチとして読むためです。
>
> シェルやバッチの特殊文字は、この Capability があっても拒否されたままです。
>
> パラメータの値と、テスト単位のパラメータリストの中身は、ログ・エラー・成果物のどこにも残りません。パラメータリストは `(<redacted>)` と表示され、記録されるのはパラメータのキーだけです。
>
> エラー: 引数の拒否は `InvalidParams`、`GauntletUnrestrictedArguments` が要るのに持っていない場合は `CapabilityNotAvailable`（その Capability が `DeniedCapabilities` で明示的に拒否されているなら `PolicyViolation`）、起動できなかった場合（別の Gauntlet テストが実行中、RunUAT やシェルが見つからない、RunUAT.bat が運べないパス、プロセスの起動失敗）は `ExecutionFailed` です。

---

## UAIP.Runtime.Assertion

シナリオ primitive — 待機とアサート。

| コマンド | 説明 |
|---|---|
| 🆓 `WaitSeconds` | 指定秒数だけ待機（シナリオ primitive） |
| 🆓 `WaitForCondition` | 条件が真になるまでポーリング |
| 🆓 `AssertActorProperty` | アクタープロパティが期待値と一致することをアサート |
| 🆓 `AssertWorldState` | 複数プロパティを 1 回でバッチアサート |

---

## UAIP.Runtime.GAS 🧩

GameplayAbilities 状態の検査と実行時操作。`GameplayAbilities` プラグインが必要で、注記のあるもの以外は PIE 必須です。

#### 検査（8）

| コマンド | 説明 |
|---|---|
| `GetAttributeValues` 🧩 | アクターの全 AttributeSet 属性値（currentValue / baseValue） |
| `GetActiveEffects` 🧩 | アクターの有効中ゲームプレイエフェクト（Level・StackCount・残時間） |
| `GetGrantedAbilities` 🧩 | アクターに付与されているアビリティ（Class・IsActive・ActiveCount・InputID） |
| `GetActiveTags` 🧩 | アクターが所有する GameplayTags |
| `FindAttributeSetClasses` 🧩 | PIE ワールド内アクターを走査し `UAttributeSet` クラス一覧を返す（MaxActors 上限） |
| `ListAttributes` 🧩 | AttributeSet クラスに定義されている全属性名 |
| `GetAbilityAssetInfo` 🧩 | `UGameplayAbility` クラスの CDO レベルのメタデータ（コスト・クールダウン・タグ）。**PIE 不要** |
| `GetEffectAssetInfo` 🧩 | `UGameplayEffect` クラスの CDO レベルのメタデータ（Duration Policy・Modifier・付与タグ）。**PIE 不要** |

#### 操作（9）

いずれも `RuntimeGASManipulation` Capability と PIE セッションが必要です。

| コマンド | 説明 |
|---|---|
| `GrantAbility` 🧩 | アクターの AbilitySystemComponent に GameplayAbility を付与 |
| `RemoveAbility` 🧩 | 付与済みの GameplayAbility を削除 |
| `ClearGrantedAbilities` 🧩 | アクターの付与済み GameplayAbility をすべて削除 |
| `ApplyEffect` 🧩 | アクターに GameplayEffect を適用 |
| `RemoveEffect` 🧩 | 指定 GameplayEffect クラスの有効インスタンスをすべて削除 |
| `ClearActiveEffects` 🧩 | 有効な GameplayEffect をすべて削除（`TagFilter` で絞り込み可） |
| `SetAttributeValue` 🧩 | 属性の base 値を設定（`AttributeName` は `Health` と、`GetAttributeValues` が返す `MyAttributeSet.Health` 形式の両方を受け付ける） |
| `ResetAttributesToBase` 🧩 | 全属性の current 値を base 値へリセット |
| `SendGameplayEvent` 🧩 | アクターへ GameplayEvent を送信（magnitude 任意） |

---

## UAIP.Runtime.Input

Runtime での入力注入と Enhanced Input 状態検査。PIE 必須。

| コマンド | 説明 |
|---|---|
| `InjectInputKey` | アクティブな PIE ビューポートに生のキー押下/解放を注入 |
| `InjectEnhancedInputAction` | Enhanced Input Action を値付きで発火（Bool / Axis1D / Axis2D / Axis3D） |
| `InjectLegacyAction` | レガシーアクションマッピングイベントを注入 |
| `InjectLegacyAxisInput` | レガシー軸入力を注入 |
| `InjectLegacySpeechInput` | レガシー音声入力を注入 |
| `AddMappingContext` | ローカルプレイヤーに Input Mapping Context を追加 |
| `RemoveMappingContext` | ローカルプレイヤーから Input Mapping Context を削除 |
| `SetInputMode` | 入力モードを設定（GameOnly / UIOnly / GameAndUI） |
| `FlushInput` | テスト終了時の押下中キー状態をフラッシュ |
| 🆓 `DumpInputState` | 現在の入力状態（押下中キー・軸値・優先度付きの有効 Mapping Context・推定した入力モードの根拠・注入ゲートの判定、`IncludeActionStates=true` 指定時はアクション単位の Trigger 状態も含む）をダンプ。プロジェクトのコードは実行しません。[注入ゲート](#注入ゲート) を参照 |
| 🆓 `GetEnhancedInputActionValue` | Enhanced Input Action の現在値を取得 |
| `EvaluateInputGateWithProjectCode` | 注入ゲートを、実際の注入と同じく**ゲームビューポートクライアントのプロジェクトの override を実行して**評価し、何も注入せずに判定を返します。`PlayerIndex` はプレイヤーコントローラの番号（既定 0）。ゲートが止める場合も成功です（`Decision: "Blocked"`）。`RuntimeInspect` と `InputProjectCodeExecution`（DefaultDenied）が必要です。読み取り専用のコマンドではないので、安全設定の読み取り専用モードでは拒否されます。デモ版にはありません |
| `ClickGameViewportWidget` | 実行中のゲームの UI の Widget をマウスでクリックします。押す位置へポインターを動かし、カーソルの真下にあるのが対象（またはその中身）であることを確かめてから、ボタンを押して離します。対象は UMG の `WidgetPath`、`ViewportPosition`、または `FindGameViewportWidgets` が返した `TypePath` と `Fingerprint` で指定します。`RuntimeUIInputInjection` が必要です。[ゲームビューポートの UI 入力](#ゲームビューポートの-ui-入力3) を参照 |
| `PressGameViewportUIKey` | ローカルプレイヤーの Slate ユーザーとして、UI 用のキー（矢印・Tab・Enter・Space・Escape・ゲームパッドのボタン）を押します: キーを押す → 安全の再確認 → キーを離す。対象を指定しないと、そのプレイヤーのフォーカスがある Widget に届き、指定すると先にフォーカスをそこへ移します。`RuntimeUIInputInjection` が必要です |
| `TypeGameViewportText` | 実行中のゲームの UI の入力欄へ、ローカルプレイヤーの Slate ユーザーとして 1 文字ずつ文字を打ちます。確定はしません（確定には `PressGameViewportUIKey` で Enter を送ります）。欄の値を直接書き換えることもしません。打った文字列はログにも応答にも記録にも残りません。`RuntimeUIInputInjection` が必要で、パスワード欄に打つには安全設定 `AllowRuntimePasswordFieldWrite` も要ります |

---

> **Note**: `DumpInputState` は常に `ActiveMappingContexts`（`Priority` 降順・同値は `Path` 昇順でソート）と `EnhancedInputState`（`"Available"` / `"Unavailable"`。「取得できて 0 件」と「そもそも取得できない」を区別する）を返します。`IncludeActionStates=true` を渡すと、有効な Mapping Context から到達できるアクションごとに `ActionStates[]` が追加されます。各エントリは `Trigger`（`ETriggerEvent` の全 6 値のいずれか。発火していないアクションを表す `"None"` を含む）、`ValueX`/`ValueY`/`ValueZ`、`SourceContexts[]`（どの有効 Context がそのアクションを設定しているか）、`ConfiguredKeys[]`（重複排除・ソート済み）を持ち、`ActionStatesTotalCount` と `ActionStatesTruncated`（`ActionPath` 昇順で最大 256 件に打ち切り）も併せて返されます。`IncludeActionStates` を既定の `false` のままにすると呼び出しは軽量なままです — このパラメータが opt-in なのは、コストがロード済み Mapping Context 数ではなくマッピング済みアクション数に比例して増えるためです。

### `DumpInputState` の出力

`DumpInputState` はプロジェクトのコードを実行しません。Mapping Context は、サブシステムの override できる関数を通さず、Enhanced Input の評価そのものが使うデータから読みます。そのため、それらの関数を override しているプロジェクトでも、入力の処理が実際に適用している Context が見えます。`PlayerIndex` の解決も同じで、プロジェクトが override できる関数を通さず、ゲームインスタンスのローカルプレイヤー一覧とゲームステートのプレイヤー配列から読みます。実行中のエンジンの版でそのデータを読めないときは、`EnhancedInputState` が `"Unavailable"` になり、`EnhancedInputUnavailableReason` が理由を示します（例 `"ReflectedFieldUnavailable:AppliedInputContextData"`）。この欄はそのときだけ付きます。

| 欄 | 意味 |
|---|---|
| `InputModeEvidence` | 入力モードを推定した根拠。`Viewport`（`IgnoreInput`・`MouseCaptureMode`・`MouseLockMode`・`HideCursorDuringCapture`。ゲームビューポートが無ければ `null`）、`PlayerController`（`IgnoreMoveInput`・`IgnoreLookInput`・`ShowMouseCursor`）、`LastSetInputModeDebugString`（開発用ビルドだけ） |
| `PlayerControllerPath` | `PlayerIndex` が指したプレイヤーコントローラのオブジェクトパス。`PlayerIndex` はプレイヤーの出入りで変わる番号付けの中の位置なので、どのプレイヤーコントローラのダンプか、2 つのダンプが同じプレイヤーコントローラのものかは、このパスで見分けます。ローカルのプレイヤーコントローラにもリモートのものにも付きます |
| `ViewportClientClass` | ゲームビューポートクライアントのクラス |
| `ViewportClientIsVerifiedEngineClass` | そのクラスがエンジンのクラス（またはゲートの差し込みが確かめたクラス）と完全に一致するときに `true`。`false` のときは、上のビューポートの値はプロジェクトの override ではなくエンジンの実装の値です — `GameInputGate` を参照 |
| `GameInputGate` | 注入ゲートが下す判定。`Decision`（`Allowed` / `Blocked`）、`Source`（`Bypass` / `ViewportInference` / `Contributor`）、`InferredInputMode`、`ViewportReadStatus`（`Read` / `NoViewport` / `ChangedDuringProjectCode` / `OutOfRangeValue`）、`ContributorInstalled`、`Contributor`（`Name`・`Applicability`・`AllowsGameInput`・`Reason`・`Evidence`。差し込みが無ければ `null`）。確かめていないビューポートクライアントのクラスでは、`RequiresCapabilities: ["InputProjectCodeExecution"]` と `SeeCommand: "UAIP.Runtime.Input.EvaluateInputGateWithProjectCode"` が付きます（デモ版では `RequiresCapabilities: ["NotInThisEdition"]` で、`SeeCommand` は付きません） |
| `Limitations[]` | `{Code}`: `ViewportClientOverridesNotEvaluated`・`ViewportInputStateOutOfRange`・`ViewportChangedDuringProjectCode`・`InputModeDebugStringUnavailableInThisBuild`・`ReflectedFieldUnavailable:<欄>` |

`Result` は `{PlayerIndex, InferredInputMode, GameInputGate: {Decision, Source}}` です。

引数はプレイワールドを探す前に検査します。負の `PlayerIndex` や bool でない `IncludeActionStates` は `InvalidParams` です。どのプレイヤーコントローラも持たない `PlayerIndex` は `NotFound` で、存在する番号を挙げます。

### 注入ゲート

注入の 5 コマンド（`InjectInputKey`・`InjectEnhancedInputAction`・`InjectLegacyAction`・`InjectLegacyAxisInput`・`InjectLegacySpeechInput`）は、ゲームがゲーム入力を受け付けていない間は注入を断ります。ゲートは 2 つの判定を合わせ、どちらかが止めれば止めます。

- **ViewportInference** — ゲームビューポートクライアントとプレイヤーコントローラから推定した入力モード。
- **差し込み（contributor）** — UI フレームワーク自身の入力の振り分けを知っている任意の連携。[CommonUI 連携](#uaipruntimecommonui-) が `CommonUIRouter` という名前で差し込みます。たとえば CommonUI のアクションルーターがメニューモードの間は、ゲーム入力を止めます。差し込めるのは 1 つまでです。

注入は、実際の入力と同じ読み方でゲームビューポートクライアントを読みます。`IgnoreInput`・`GetMouseCaptureMode`・`HideCursorDuringCapture` のプロジェクトの override も実行します。`DumpInputState` はエンジンの実装だけを読むので、これらを override しているプロジェクトのビューポートクライアントでは、その `GameInputGate` が注入の判定と食い違うことがあります。注入そのものの判定は `EvaluateInputGateWithProjectCode` が返します。読み取りの途中で実行されたプロジェクトのコードが、プレイヤーコントローラ・ローカルプレイヤー・ワールド・ビューポートクライアントのどれかを入れ替えた場合、ゲートは `ViewportReadStatus: "ChangedDuringProjectCode"` で止めます。

拒否は `NotAllowed` で、メッセージは止めた判定（`ViewportInference` または差し込みの名前）とその理由を示します。安全設定のバイパスを許していないときの `BypassInputMode=true` に対する `PolicyViolation` は変わりません。注入ごとの監査記録には `GateSource`・`GateContributorReason`・`GateViewportReadStatus` が入ります。

ゲートはすべてを写すわけではありません。人が押したキーは、ゲーム入力に届く前に UI のアクションのバインド（CommonUI のものなど）に消費されることがありますが、ゲートはそれを再現しません。コンソールを有効にしたビルドでビューポートのコンソールのオブジェクトが無いときは、ゲートはエンジンより厳しく判定します。

`EvaluateInputGateWithProjectCode` はフレームの安全な地点を待ちません — 注入が評価するのと同じ地点で評価するので、注入が受ける判定をそのまま返します。プロジェクトのコードを実行するため、読み取り専用モードでは `PolicyViolation`、モーダルダイアログが開いている間やエンジンの tick が止まっている間は `NotAllowed` で拒否されます。

### ゲームビューポートの UI 入力（3）

実行中のゲームの UI を、人と同じ入力経路で操作します。ポインターを対象の上へ動かし、押下は Slate の入力ルーティングを通り、フォーカスはゲーム自身の UI が動かす規則どおりに動きます。ボタンの処理を直接呼ぶことも、入力欄の値を直接書き換えることもしないので、ゲームの入力処理（CommonUI やプロジェクト独自の入力処理）も関与します。OS のカーソルは動かず、Unreal Editor が背面にあっても動きます。PIE でも `-game` 起動でもパッケージ版でも動作します（パッケージ版で HTTP を使うには `-uaip-http-enable` が必要です）。3 つとも [`TargetNetRole` / `TargetPIEInstance`](#実行時コマンドの対象プレイワールドを指定する) を受け付け、選んだワールドのゲームビューポートの中にだけ送ります。

**Capability。** 3 つとも `RuntimeUIInputInjection`（DefaultDenied）が必要です。これは **`RuntimeInputInjection` とは別**で、後者を許可しても UI は操作できません。エディタ内の PIE では、エディタが PIE 用のショートカットに割り当てているキー（既定では PIE を停止する Escape）を送るには、さらに `RuntimeUIEditorReservedKeyInput`（DefaultDenied）が必要です。Standalone とパッケージ版では制限されません。Capability は、要求を受け付けたときと、実際に送る直前の 2 回確かめます。詳細は [安全性と Capability](safety.md#runtime-ゲームビューポートの-ui) を参照してください。

#### 対象の指定

`ClickGameViewportWidget` は対象をちょうど 1 つ指定します。`PressGameViewportUIKey` と `TypeGameViewportText` は省略でき、その場合はそのプレイヤーのフォーカスがある Widget に届きます。

| パラメータ | 意味 |
|---|---|
| `WidgetPath` | 画面に出ている UMG Widget のオブジェクトパス。名前のある Widget ではこれが最も確実です |
| `ViewportPosition` | ゲームビューポート左上からの物理ピクセルでの `{X, Y}`。その位置の最前面の Widget が対象になります |
| `TypePath` + `Fingerprint` | `FindGameViewportWidgets` が一致に付けて返した値。`TypePath` にある Widget が Fingerprint の示すものと違う場合（画面が作り直された）は `Conflict` で拒否されます。検索し直してください。名前も Tag も無い同じ型の Widget が並んでいると、入れ替わりを見分けられないことがあります |
| `LocalX` + `LocalY` | `ClickGameViewportWidget` のみ。対象の矩形の左上からのオフセットで押す位置を指定します。両方を同時に、矩形の内側で、`ViewportPosition` とは併用しません。省略時は中央 |
| `MouseButton` | `ClickGameViewportWidget` のみ。`Left`（既定）または `Right` |
| `Key`（必須） | `PressGameViewportUIKey` のみ。UI 用の許可リストのキー: 矢印キー、`Tab`、`Enter`、`SpaceBar`、`Escape`、ゲームパッドの十字キー・フェイスボタン・ショルダー・トリガー・特殊ボタン、`Virtual_Gamepad_Accept` / `Virtual_Gamepad_Back`。それ以外のキー（修飾キーはすべて）は、許可される名前を `AllowedKeys` に添えて拒否されます。修飾キーが付くことはありません |
| `Text`（必須） | `TypeGameViewportText` のみ。1〜1024 コードポイント（結合した絵文字や国旗は複数と数えます）。制御文字は不可で、改行は打てません |
| `PlayerIndex` | `PressGameViewportUIKey` と `TypeGameViewportText`。操作するプレイヤーの**ローカルプレイヤー**の番号。既定 0 |

**`PlayerIndex` はプレイヤーコントローラーの番号ではありません。** 既存の入力コマンド（`InjectInputKey` など）はワールドの**プレイヤーコントローラー**の番号を取ります。この 2 つはゲームインスタンスの**ローカルプレイヤー**の一覧の番号（0 が 1 人目）を取ります。負の数は `InvalidParams`、いないローカルプレイヤーの番号は `NotFound` です。クリックは常にマウスを持つユーザー（通常は 1 人目のローカルプレイヤー）として送られるため、他のローカルプレイヤーの画面の UI も押せます。その場合は応答に注意書きが付きます。

#### 操作の流れ

1. **クリック。** ポインターを押す位置へ動かし、カーソルの真下にあるのが対象（またはその中身）であることを確かめます。違えば何も押さず（`ExecutionFailed`、最前面の Widget を添える）、合っていればボタンを押して離します。
2. **キー。** 対象を指定した場合は、先にフォーカスを移して移ったことを確かめます。キーを押し、安全の再確認をしてから離します。`ReachedGameViewport` は、UI が処理せずにキーがゲーム側へ届いたかを示します: `true`・`false`・`Unknown`。`false` のときは `ReachedGameViewportReason` が `HandledBeforeGameViewport` になります。フォーカスのある Widget か、それを含む Widget がキーを処理したため、ゲームビューポートで入力を読むもの（プレイヤーコントローラーの入力や、ゲームがビューポートクライアント経由で結び付けた入力アクション）には届いていません。コマンド自体は成功します。`FocusAfter` と、その画面がキーを自分で結び付けているかを確かめてください。`Unknown`（別のビューポートへ行った可能性がある）には理由を付けません。
3. **文字。** 対象を指定した場合は、先にフォーカスを移します。文字は人がキーボードで打つのと同じ形で 1 文字ずつ送ります（IME の変換は送りません）。1 文字ごとに、フォーカスが同じ欄にあること、パスワード欄かどうかが変わっていないことを確かめ、変わっていれば止めます。パスワード欄かどうかは送る時点で判定し、判定できない欄はパスワード欄として扱います。

応答は、入力を送り終えてから返ります。何に当たったか（`HitWidget`・`HitWidgetIsTarget`）、操作後のフォーカス（`FocusAfter`）、入力がゲームまで届いたか（`ReachedGameViewport`）、モーダルが開いたか（`ModalOpened`）、`Limitations` が入ります。`TypeGameViewportText` はさらに、送った文字数（`CharactersDelivered`）、止まった理由、操作の前後の入力欄の長さの区分（`Empty`・`NonEmpty`・`Long`）を返します。文字列そのものは返しません。

#### `Success` の意味

`Success` は**人の入力と同じ経路で入力を送り終えた**という意味です。ボタンの処理が実際に動いたことや、画面が変わったことは保証しません。途中にある処理（CommonUI、プロジェクト独自の入力処理、エディタの入力の監視）は、人の入力と同じく入力を消費・変換しうるためです。効果はもう一度ツリー（`DumpGameViewportWidgets`）を読んで確かめてください。UI が処理しなかった入力は、人の操作と同じくゲーム側の入力（移動・攻撃など）になることがあります。各操作の応答にはその旨が必ず付きます。要求を受け付けてから送るまでの間に、呼び出し側がまだ待っていること、およびワールド・セッション・Capability・対象が変わっていないことを確かめます。呼び出し側が待つのをやめていた場合は何も送りません。二重押しは減りますが、確かめた直後のタイムアウトとの行き違いまでは防げません。

#### 拒否される場合

特に書かない限り、どの場合も何も送られません。

| 状況 | 結果 |
|---|---|
| プレイワールドが無い、サーバーのワールド、指定に合うワールドが無い | `NotAllowed`（サーバーのワールドには選び直せるクライアント側の候補が添えられます）。指定が矛盾・曖昧な場合は `InvalidParams`。専用サーバーのプロセスでは、これらのコマンドは使えず、拒否の文が理由を示します |
| ゲーム層がまだ無い | `PreconditionFailed`（再試行）。場所を特定できない場合は `NotAllowed` |
| Capability が許可されていない | 名前を示した `CapabilityNotAvailable`（エディタ用に予約されたキーでは、当たったショートカットの名前と、ゲームパッドの「戻る」を使う案内も添えられます）。明示的に拒否している場合は `PolicyViolation` |
| クリックでゲームビューポートがマウスを掴んでいる（入力モードがゲーム専用）、対象なしのキー・文字でフォーカスがゲームビューポートそのものにある、ドラッグ中、モーダルがどれか開いている、ゲームビューポートの外のメニューが開いている | `NotAllowed`。フォーカスとマウスキャプチャの状態が添えられます。入力モードは勝手に変えません（`SetInputMode` を使ってください）。ゲーム自身の UI のドロップダウンが開いているだけなら妨げになりません |
| ゲームを載せているウィンドウが最小化または非表示（`Reason: HostWindowUnavailable`。[キャプチャが断られるとき](#キャプチャが断られるとき)を参照） | `NotAllowed`。ホストウィンドウがまだ無い場合は `PreconditionFailed` |
| 対象が無い、またはビューポートに追加されていない | `NotFound` |
| 検索の後で画面が作り直された | `Conflict`（検索し直す） |
| 対象が非表示または無効 | `NotAllowed` |
| 対象の前に別の Widget がある（エディタ内の PIE では、エディタのビューポート用のツールバーやメッセージも含む） | 最前面の Widget を示した `ExecutionFailed`。ツールチップなどホバーによる反応は起きています |
| 座標で指定した位置の最前面がエディタの表示や別のウィンドウ、キー・文字の送り先のフォーカスがゲームビューポートの外 | `NotAllowed` |
| 対象なしのキー・文字で、そのプレイヤーのフォーカスがどこにも無い | `NotFound` |
| フォーカスを対象へ移せなかった | `NotAllowed`（移した後のフォーカスを添える） |
| 押してから離すまでの間に状況が変わった（画面・ワールド・モーダル） | `PartialDelivery`（クリックは `DownOnly`、キーは `KeyDownOnly`）を添えた `NotAllowed`。離す操作は送らず、押下状態を解除します |
| 押した操作そのものでモーダルが開いた | `ModalOpened` と `PartialDelivery` を添えた**成功**。離す操作は送りません |
| パスワード欄、またはパスワード欄かどうか判定できない欄に、`AllowRuntimePasswordFieldWrite` なしで文字を打つ | フォーカスを移す前に `PolicyViolation`。拒否の文が、どちらだったかを区別します |
| 入力欄ではない、読み取り専用、または無効なものに文字を打つ | `NotAllowed` |
| 文字入力の途中で止まった（フォーカスが移った、パスワード欄かどうかが変わった、アプリの状態が変わった） | 1 文字以上送っていれば、送った文字数を `CharactersDelivered` に入れた `NotAllowed`。まだ 1 文字も送っていなければ、上の該当する状況の拒否。2 つに分けて送る文字（絵文字など）の途中で止まった場合は、その旨が返ります。送った文字でモーダルが開いた場合は**成功**で、`ModalOpened` と送った文字数を添え、入力欄の操作後の長さの区分は返しません |
| `PlayerIndex` のローカルプレイヤーがいない | `NotFound` |
| 許可リストに無いキー、空または長すぎる文字列、制御文字、対象の外を指す位置、`LocalX` / `LocalY` の片方だけ、`LocalX` / `LocalY` と `ViewportPosition` の併用、クリックで対象が無い・2 つ以上ある、`Fingerprint` の無い `TypePath`、負の `PlayerIndex` | 違反した項目と許される範囲を示した `InvalidParams` |
| Unreal Engine が終了処理に入った | `ExecutionFailed`（終了による取り消し） |

シナリオが自動で再試行するのは、`ExecutionFailed` と `PreconditionFailed` の後だけです。途中まで届いた場合を `NotAllowed` にしているのはこのためで、再試行されると二度押しや文字の重複になるからです。

キーを押し、ゲーム側がその押下を見た後で止まった場合は、そのプレイヤーのゲーム側の押下状態も解除します。このとき、利用者が実際にキーボードで押しているキーの状態も一緒に消えます。ゲーム側が押下を見たか判定できない場合と、プレイヤーがもういない場合は解除せず、応答にそう注記されます。

#### 知っておくこと

- **分割画面。** ツリーとフォーカスは、各ローカルプレイヤーの画面領域を報告します。キーと文字は指定したプレイヤーとして、クリックは常にマウスを持つユーザーとして送られます。
- **同じプロセスの複数の PIE。** 入力は選んだワールドのビューポートの中にだけ送られますが、入力の通り道の一部（CommonUI の全体処理）は PIE 同士で共有されます。「ゲームパッドを 2 つ目のウィンドウへ送る」が有効だと、ゲームパッドのキーが別の PIE に届くことがあり、そのとき `ReachedGameViewport` は `Unknown` です。別々の PIE で同時にゲーム内のメニューが開いていると、どちらのメニューかを見分けられないことがあります。
- **描画しない環境（`-nullrhi`）。** ツリーに矩形が無く、操作は `NotAllowed` で拒否されます（待っても通りません）。起動直後でまだ何も描かれていないだけなら `PreconditionFailed` です。
- **機微な値。** `DescribeCommand` は、完了通知・監査記録で伏せるパラメータ（`SensitiveParams`。`TypeGameViewportText` は `Text`）と、同様に伏せる応答の項目（`SensitiveResponseData`。`DumpGameViewportWidgetTexts` はパスワード欄の平文）を示します。購読者・監査記録には、長さも載らない `"<redacted>"` が渡ります。伏せるパラメータを確かめられないときはパラメータ全体が、伏せる応答の項目を確かめられないときはトップレベルの項目名を残して応答の `Data` 全体が伏せられます。シナリオで、前のステップの応答から取ったこうした値を後のステップに埋め込むと、そのステップと、その応答を受け取る後続のステップは丸ごと伏せられます。対象のコマンドが結果として保存するファイルは対象外です。[機微な値と伏せる場所](#機微な値と伏せる場所) を参照してください。
- **CLI では入力が残ります。** コマンドライン（`-uaip-request=`）やリクエストファイル（`-uaip-request-file=`）に渡した文字列、および応答ファイルは、そこに残ります。呼び出し側が選んだコマンドラインやファイルは UAIP では伏せられません。秘密はそこに渡さないか、HTTP / MCP を使ってください。

## UAIP.Runtime.Niagara 🧩

PIE 中の Niagara コンポーネント検査とパラメータ上書き。`Niagara` プラグインが必要。

### ネイティブ（4）

| コマンド | 説明 |
|---|---|
| `GetUserVariables` 🧩 | Niagara System Component のユーザー公開変数を取得 |
| `GetVariable` 🧩 | 特定のユーザー変数の値を取得 |
| `SetVariable` 🧩 | ユーザー変数の値を Runtime で設定 |
| `SetSystem` 🧩 | コンポーネントの Niagara System アセットを Runtime で差し替え |

### Toolset ブリッジ（4）🧩

プロバイダ：`Toolset.Runtime.Niagara.*`。UE 5.8+ と `NiagaraToolsets` が必要。ネイティブコマンドをミラー。

---

## UAIP.Runtime.LiveLink

LiveLink の Source / Subject 観測、クライアント状態の制御、UAIP 所有の合成 Source。エディタでも Runtime でも動作し、PIE は不要です。

**プラグイン要件は無く、🧩 も付きません。** これらのコマンドが使うクライアントインターフェースは、オプションの `LiveLink` プラグインではなくエンジン常設の `LiveLinkInterface` モジュールに含まれるため、コマンドは**常に登録されます**。LiveLink クライアントが存在しない場合（`LiveLink` プラグイン無効時）は、一覧から消えるのではなく `uaip_list_commands` / `uaip_describe_command` で `Available: false` として現れ、`ListLiveLinkSources` が `LiveLinkAvailable` を返すため、**1 回の呼び出しでこの環境で LiveLink が使えるかを判定できます**。この状態では `uaip_describe_command` がこのドメインの全 14 コマンドに対して `UnavailableDetail: "ExecutionEnvironment"` も返します — このモジュールでコンパイルから除外されているものはなく、不足しているのは実行中プロセスの `ILiveLinkClient` です — [UnavailableDetail](#unavailabledetail--handlerunavailable-の8つの詳細理由) 参照。プリセット・接続・録画は [UAIP.Editor.LiveLink](#uaipeditorlivelink-) にあり、そちらにはプラグイン要件があります。

**Subject の指定方法。** 別々の Source が同名の Subject を出すことがあります。読み取りは `SubjectName` だけを受け付けて解決しますが、複数一致した場合は候補を `Candidates` に列挙して `InvalidParams` で拒否します — 勝手にどれかを選ぶことはありません。変更系は代わりに `SubjectKey`（`SourceGuid` + `SubjectName`）を取ります。エンジン側が名前しか扱えない 3 箇所（仮想 Subject の構成メンバー、`StartLiveLinkRecording` の対象、`SetLiveLinkComponentSubject`）は、現在**有効な** Subject に対して解決し、曖昧なら拒否し、何に解決したかを応答に記録します。

**排他制御。** 以下の変更系コマンドは、プリセット適用中と録画中は拒否されます（[UAIP.Editor.LiveLink](#uaipeditorlivelink-) 参照）。`PushLiveLinkSyntheticFrame` は意図的な例外で、この理由で拒否されることはありません。読み取りも同様に拒否されません。

### 観測（6）— `RuntimeInspect` が必要

| コマンド | 説明 |
|---|---|
| `ListLiveLinkSources` | クライアントに登録されている全 Source（実 Source と仮想 Subject の入れ物の両方）— `Guid`・可読な `Type`・`IsStillValid`・`IsVirtual`・`FactoryClassPath`。`LiveLinkAvailable` はクライアント実装が登録されているかどうかを返すため、まずこのコマンドから始めるとよい。⚠️ `IncludeSensitiveDetails: true` は `ConnectionString` / `StatusText` / `MachineName` を追加する — これらは Source 実装が自由に決められるフィールドで、ホストアドレスや資格情報を含みうるため `LiveLinkSourceInspectSensitive` が必要。要求の有無にかかわらず、全応答が Capability 名を `SensitiveDetailsRequiredCapability` として返す |
| `ListLiveLinkSubjects` | クライアントが把握している全 Subject を `IncludeDisabled` / `IncludeVirtual` で絞って返す。各エントリは `SubjectKey`・`RoleClassPath`・`EnabledConfigured`（永続的な設定値）・`IsSubjectValid` を持つ。`State` は `EnabledConfigured` が true のときだけ含まれる — エンジンの状態取得は名前をキーにしており、同名のうち現在有効なものについて答えるため、無効な行に載せると別の Subject を説明することになるため |
| `GetLiveLinkSubjectFrame` | Subject の現在の static data と frame data を指定 Role で評価し、Role の構造に沿った JSON として返す（`SubjectKey`・`RoleClassPath`・`StaticData`・`FrameData`・`CapturedAt`）。`SourceGuid` を指定するとその Source に対して評価し、省略すると名前で評価する（同名のうち現在有効なものについて答える）。`Role` は既定で Subject 自身の Role。エンジン標準の Role はフィールド単位で構造化して返り、プロジェクト・プラグイン定義の Role は全 Role 共通の項目（カーブ値・時刻・タイムコード）だけにフォールバックする — どちらかは `ListLiveLinkRoles` で分かる |
| `GetLiveLinkSubjectStatus` | Subject の接続状態 — `State`（解決した Subject が同名のうち有効なものである場合のみ。理由は上記と同じ）・`IsSubjectTimeSynchronized`・`SceneTime`（フレームが届いていれば直近フレームのもの）・`FrameArrivalTimes`・`CapturedAt`。⚠️ **フレームレートは一切算出しない。** `FrameArrivalTimes` はエンジンが公開する生の到着時刻の並びをそのまま返したもので（エンジン自身がデバッグ用途と明記しており、フレームレートを返す API も無い）、そこから何を読み取るかは利用者に委ねられる |
| `GetLiveLinkSubjectSettings` | Subject の `ULiveLinkSubjectSettings` レベルの設定を返す。現時点では `InterpolationProcessorClassPath` のみで、Subject に設定されている `ULiveLinkFrameInterpolationProcessor` のクラスパス、未設定なら `null`。`SubjectName` の裸名解決は `GetLiveLinkSubjectStatus` と同じ（`SourceGuid` で絞り込み可能。曖昧なら `Candidates` を列挙して `InvalidParams` — 勝手にどれかを選ぶことはない）。**そもそも設定オブジェクトを持たない対象（仮想 Subject 等）でも `null` を返す**ため、`null` だけでは「設定できるが未設定」と「そもそも設定を持てない」を区別できない。区別が必要なら、同じ Subject に対して `SetLiveLinkSubjectInterpolationProcessor` を試みればよい（後者は `NotAllowed` になる） |
| `ListLiveLinkRoles` | 登録済みの全 `ULiveLinkRole` サブクラス — `RoleClassPath`・`DisplayName`・`StaticDataStructPath`・`FrameDataStructPath`・`IsFullySupported`（その Role のフレームをフィールド単位で読めるか、共通項目だけか）。あわせて**具象**の `ULiveLinkVirtualSubject` サブクラスを `VirtualSubjectClasses` として列挙する。`AddLiveLinkVirtualSubject` はこのいずれかを要求する（抽象基底はインスタンス化できないため） |

### クライアント状態（5）

| コマンド | 説明 |
|---|---|
| `SetLiveLinkSubjectEnabled` | `SubjectKey` で指定した Subject の Enabled フラグを設定する。**同じ名前の Subject のうち有効にできるのは 1 つだけ**のため、有効化すると同名の別の Subject が暗黙的に無効化されることがある。そのキーは `ImplicitlyDisabledSubjectKey` として返る（該当なしなら `null`）。`EnabledConfigured` は即座に反映されるが、クライアントが実際に評価する `EnabledThisFrame` は次のティックまで変わらない — この 2 つを別々に返すのはそのため。`LiveLinkClientControl` が必要 |
| `RemoveLiveLinkSource` | ⚠️ **取り消せません。** `Guid` で Source を削除し、その Source が持つ Subject もすべて道連れにする。削除した Source を同じ `Guid` で作り直すことはできない。UAIP が作った Source の場合は台帳のエントリも削除する（`WasSyntheticSource`）。登録されていない `SourceGuid` は `NotFound`。`LiveLinkSourceDelete` が必要 — この一群で唯一の不可逆な操作であるため、意図的に `LiveLinkClientControl` と分けてある |
| `AddLiveLinkVirtualSubject` | 既存の Subject を 1 つ以上組み合わせた仮想 Subject を、UAIP 共有の仮想 Subject 入れ物 Source へ追加する。`VirtualSubjectClass` は具象の `ULiveLinkVirtualSubject` サブクラスのクラスパス（`ListLiveLinkRoles` が列挙する）。`MemberSubjectNames` の各要素は同名のうち現在有効な Subject に解決し、一致 0 件なら `NotFound`、複数一致なら候補を列挙して `InvalidParams`。解決したキーは `Members` として返る。メンバーは 64 件まで、名前は 256 文字まで。**仮想 Subject は本物のクライアント構成であり、作成したセッションが終わっても残ります** — 不要になったら明示的に削除すること。`LiveLinkClientControl` が必要 |
| `RemoveLiveLinkVirtualSubject` | `SubjectKey` で仮想 Subject を削除する。冪等で、仮想 Subject を指していないキーは `WasPresent: false` で成功する。入れ物 Source に仮想 Subject が 1 つも残らなくなった場合は Source 自体も削除する（`WasContainerSourceRemoved`）— ただし**それが最後の仮想 Source になる場合は残す**（エディタの LiveLink 画面が仮想 Source の存在を前提にしているため）。`SubjectKey` が実 Subject を指す場合は `InvalidParams`（そちらは `RemoveLiveLinkSource` を使う）。`LiveLinkClientControl` が必要 |
| `SetLiveLinkSubjectInterpolationProcessor` | Subject の設定オブジェクトに構成されている `ULiveLinkFrameInterpolationProcessor` を設定・解除する。対象は完全な `SubjectKey`（`SourceGuid` + `SubjectName`）で指定し、ここに裸名解決は無い。**`InterpolationProcessorClassPath` を省略すると補間を解除するが、空文字列は省略と同義に扱わず `InvalidParams` で拒否する** — クラスパスを組み立てたつもりが空だったという取り違えが、黙って補間を解除する操作になるのを防ぐため。指定する場合、クラスは `FindObject` のみで解決し（ロードはしない）、`ULiveLinkFrameInterpolationProcessor` の具象（非 Abstract）のサブクラスである必要がある（最大 512 文字）。それ以外はすべて `InvalidParams`。`SubjectKey` が登録済みの Subject を指していなければ `NotFound`、解決した Subject が設定オブジェクトを持たない場合（`GetLiveLinkSubjectSettings` の説明を参照）は `NotAllowed`。プリセット適用中または録画中は、**補間の設定を一切変えずに**拒否される。`LiveLinkClientControl` が必要 |

### 合成 Source（3）

合成 Source は UAIP 自身が登録する最小限の Source です。これにより、**実機のキャプチャ機材も LiveLink Hub もネットワークも無しに**、プロセス内だけで Subject を成立させて LiveLink 経路全体を検証できます。合成 Source は作成したセッションが所有し、セッション終了時に片付けられます（このドメインで自動的に片付けられるのはこれだけです）。

| コマンド | 説明 |
|---|---|
| `CreateLiveLinkSyntheticSource` | UAIP 所有の Source をクライアントへ登録し、その `SourceGuid` を返す。Source は要求したセッションの所有として記録され、**そのセッションだけがフレームを流し込み、削除できる**。セッションが保持できる合成 Source の上限に達すると `TooManyRequests`。`LiveLinkSyntheticSource` が必要 |
| `PushLiveLinkSyntheticFrame` | このセッションが作成した合成 Source へ、1 つの Role の `StaticData` と `FrameData` を流し込む（名前付き Subject は初回に作られる）。⚠️ **どちらの流し込みもキューに積むだけ**で、クライアントは自身の次のティックでキューを処理する。そのため成功したほぼ全ての呼び出しで `IsSubjectValidImmediately` は `false` になる。この Subject のフレームを評価する前に、クライアントのティックを最低 1 回待つこと（`WaitForCondition` など）。`SourceGuid` がこのセッションの作成でない場合は `NotAllowed`。存在しない Source への流し込みはエンジンが黙って捨てるため、応答では Subject が実際に成立したかを確認して返す。セッション単位の Subject 数と流し込み頻度（`TooManyRequests`）、ペイロード単位の配列長・名前長・非有限値（`NaN` / `Inf`）（`InvalidParams`）で制限される。プリセット適用中・録画中も拒否されない。`LiveLinkFrameInjection` が必要 — Source を作ることとデータを流し込むことは別の権限であるため、意図的に `LiveLinkSyntheticSource` と分けてある |
| `RemoveLiveLinkSyntheticSource` | このセッションが作成した合成 Source を削除する。冪等で、登録されたことのない `SourceGuid` も既に削除済みのものも `Removed: false` で成功する。別セッションのものは `NotAllowed`。`LiveLinkSyntheticSource` が必要 |

---

## UAIP.Editor.Mass 🧩

Mass シミュレーションの元になるデータの読み取りと組み立てを行うコマンド群です。対象は、セッションが選べる Trait クラス、Mass のエンティティ構成アセット（宣言している内容、継承している内容、有効かどうか）、エンティティを配置するスポナーです。**MassGameplay** プラグインが必要です。このプラグインなしで作ったビルドでも 7 コマンドは一覧に出ますが、`Available: false`（`UnavailableDetail: OptionalPluginDisabled`）になります。デモ版には含まれません。実行中のゲームのエンティティを観測するには [`UAIP.Runtime.Mass`](#uaipruntimemass) を使います。

**Capability。** 読み取りの 3 コマンドは `EditorInspect`（DefaultAllow）を必要とします。書き込みの 4 コマンドは `MassAssetEdit`（DefaultDenied）を必要とし、呼び出しごとに、リクエストが指す内容に応じて追加の Capability が要ることがあります。エンジン自身の Mass モジュールの外にある Trait・スポナーの生成器クラスには `MassCustomTypeEdit`、呼び出しがプロジェクトのコードを走らせる場合は `MassProjectCodeExecution` です。Capability が足りない場合は `CapabilityNotAvailable` で、`RequiredCapabilities` と `MissingCapabilities` を載せ、何も変更しません。`MassProjectCodeExecution` を許可すると何にさらされるかは [安全性と Capability](safety.md#mass-の観測と編集) を参照してください。

**読み取りはエディタのワールドを変えません。** `DumpMassEntityConfig`・`ValidateMassEntityConfig`・`ListMassEntityTraits` は、構成が何を組み立てるかを、呼び出しの間だけ存在する専用の空のワールドで各 Trait を組み立てて求めます。そのため、エディタのワールドもアセットも変わりません。結果は実行モード `EditorWorld`（`EvaluatedExecutionMode`）のものです。ワールドの実行モードで振る舞いを変える Trait は、実行中のゲームでは別のものを組み立てることがあり、`Limitations` がそれを伝えます。エンジンの Mass モジュールの外にある Trait は、`MassProjectCodeExecution` を持たないセッションでは、組み立ても、プロパティ値の読み取りもされず、`SkippedTraits`（または `ElementsOmittedReason`）に載ります。このとき `ValidateMassEntityConfig` は `IsComplete: false` を返し、`Verdict` は `Inconclusive` になります。ただし、省かれた Trait では取り消せないエラーがすでにあれば `Invalid` です。読み取りは PIE 中でも許可されます。

**出力の上限。** 上限のある一覧 `<List>`（`OwnTraits`・`CombinedTraits`・`Composition`・`PerTrait`・`SkippedTraits`・`Issues`・`EntityTypes`・`SpawnDataGenerators`）には `<List>TotalCount`、`<List>Truncated`、Data のみ `<List>DataEntriesTruncated` が付きます。`<List>Truncated` は、**応答が返した結果（Data と成果物を合わせたもの）の外に**まだ要素があるときに true で、Data と成果物で同じ値です。`<List>DataEntriesTruncated` は Data の件数が成果物の件数より少ないときに true で、残りは成果物にあります。`ListMassEntityTraits` は接頭辞の無い `TotalCount`・`Truncated`・`DataEntriesTruncated` を使い、`MaxClasses` で一覧を切った場合もここでは `Truncated` が true になります。`ReturnedCount` はそのドキュメント自身の件数で、`Truncated` の判定の基準にする件数とは別です。`ArtifactTruncated` / `ArtifactTruncationIndex` は成果物がサイズ予算で止まったことを示します。

**曖昧な要素名。** `ListMassEntityTraits` の `AddsElement` が複数の要素の型に一致する短い名前だと、このコマンドは `InvalidParams` で失敗します。その失敗応答の `Result` には、`AmbiguousName`（指定された名前）、`Candidates`（候補の型パス。並べ替え済み、最大 10 件）、`TotalCandidateCount`（一致した型の総数）が載ります。候補の型パスのどれかで指定し直すと、曖昧さが解けます。

**書き込み。** 書き込みは元に戻せる 1 ステップです。断られたリクエストは何も変えません（アセットも、そのパッケージのダーティフラグも、Undo 履歴も変わりません）。プレイセッション中、および読み取り専用の場所（`/Engine` 配下など）にあるアセットへの書き込みは `NotAllowed` で断られます。構成への書き込みが成功すると、その構成と、読み込み済みの子孫の構成について、エディタのワールドが覚えているテンプレートを外します。応答は `RemovedEditorWorldTemplates`・`UnloadedDescendantCount`・`TemplateRegistryUnavailable` を返します。汎用のプロパティコマンド、手による編集、Undo / Redo では外しません。

> **Mass Debugger のタブ。** Mass Debugger のタブが開いていると、一時ワールドの作成でエンジン内部のチェック（`ensure`）が 1 回失敗し、ログにコールスタックが出ます（デバッガーを付けて起動しているとそこで止まります）。エンジン自身も、Trait の一覧のために作る一時ワールドで同じことをします。コマンドは成功し、一時ワールドは Mass Debugger の環境の一覧には出ません。避けたいときは、先にタブを閉じてください。

| コマンド | 説明 |
|---|---|
| `ListMassEntityTraits` | セッションが選べる Mass の Trait クラスを一覧する。各エントリは `ClassPath`・`DisplayName`・`Admission`（`Allowed`・`RequiresCapabilities`・`NotAddable`・`CompatibilityUnknownUntilAuthorized`）、追加に要る `RequiredCapabilities` / `MissingCapabilities`、要素の読み取りに要る `EvaluationRequiredCapabilities`、`Deprecated`、Trait が追加・要求する要素（`AddedElements` / `RequiredElements`）を持つ。セッションが置けないクラスも、断る理由付きで一覧に残る。`AddsElement` はその要素を追加する Trait だけに絞り（読めずに判定から漏れた Trait の数が `UnevaluatedTraitCount`）、`NameFilter` はクラスパスまたは表示名に大文字小文字を区別せず一致させ、`MaxClasses`（1〜1000、既定 200）が件数の上限（`TotalCount` / `Truncated`。応答が返した結果の外にクラスが残るとき true）。クラスパス順。Data は先頭のエントリを、成果物はサイズ予算までの残りを持ち、Data の件数が成果物より少ないときは `DataEntriesTruncated`（Data のみ）が true になる。読み取り専用。`EditorInspect` が必要で、プロジェクトの Trait の要素を読むときだけ `MassProjectCodeExecution` も必要 |
| `DumpMassEntityConfig` | Mass のエンティティ構成アセット（`AssetPath`）を読み、宣言している内容を保存する。`OwnTraits`、`ParentChain`（近い順）、`InheritanceCycle`、`CombinedTraits`（親の連なりのすべての Trait。`OverriddenBy` と `Effective` 付き）、`Composition`（有効な Trait が組み立てるテンプレートの要素）、`PerTrait`（有効な Trait ごとの追加・要求・除去）、`SkippedTraits`。親の連なりが循環していると、`CombinedTraits`・`Composition`・`PerTrait` は空になり、`Limitations` に `CompositionNotComputedDueToCycle` が付く。読み取り専用。`EditorInspect` が必要で、プロジェクトの Trait を評価するときだけ `MassProjectCodeExecution` も必要 |
| `ValidateMassEntityConfig` | 構成（`AssetPath`）を、エンジンが Trait の組み立てるエンティティテンプレートを検証するのと同じ方法で検証する。`Verdict` は `Valid`・`Invalid`・`Inconclusive`。`IsComplete` はすべての Trait を評価できたかを示し、true なら `Verdict` はエンジン自身の検証と一致する。`Issues` の各エントリは `Kind`（`MissingElement`・`DuplicateElement`・`TraitValidationFailed`・`InheritanceCycle`・`TraitOverridden`）と `Severity` を持ち、足りない要素には `SuggestedTraits` が付く。`SuggestionsComplete` と `UnevaluatedTraitCount` は、候補がすべての Trait クラスに基づくかを示す。Trait 固有の検証が失敗した理由はエンジンのログにしか出ない（`TraitValidationReasonOnlyInLog`）。読み取り専用。`EditorInspect` が必要で、プロジェクトの Trait を評価するときだけ `MassProjectCodeExecution` も必要 |
| `AddMassEntityConfigTrait`（`MassAssetEdit` が必要） | 構成に Trait を追加する。`TraitClass` は `ListMassEntityTraits` が返す、読み込み済みの Trait クラスのパス（未読み込みのクラスは読み込まずに `NotFound`）。`InitialProperties`（任意、最大 64 件）は追加の前に新しい Trait へ書き込まれ、1 件でも断られれば追加全体を取り消す。`ValidTargetConfig`（任意）は対象フラグ（`Standalone`・`Server`・`Client`・`Editor`・`EditorWorld` をカンマ区切り、または `None`）。UE 5.7 には無く `NotApplicable` だけを受け付ける。同じ対象ですでに構成が宣言している Trait は `InvalidParams` で `CandidateIndices` を返し、親が宣言している Trait は上書きとなり `OverridesParentTrait` が示す。クラスがエンジンの Mass モジュールの外にあるときは `MassCustomTypeEdit` も、`InitialProperties` を渡すときはクラスを問わず `MassProjectCodeExecution` も必要 |
| `RemoveMassEntityConfigTrait`（`MassAssetEdit` が必要） | 構成が自分で宣言している Trait を外す。`Index`（構成自身の Trait の中での位置。`DumpMassEntityConfig` の `OwnTraits` と同じ）か `TraitClass` のどちらか 1 つだけで指定する。構成自身の複数の Trait に一致するクラスは `InvalidParams` で `CandidateIndices` を返し、親だけが宣言している Trait は `InvalidParams` で `ParentAssetPaths`（代わりに編集すべき構成）を返す。Trait の処理は走らないので、ほかの Capability は要らない |
| `SetMassEntityConfigTraitProperty`（`MassAssetEdit` と `MassProjectCodeExecution` が必要） | 構成が自分で宣言している Trait のプロパティを 1 つ設定する。Trait の指定は `RemoveMassEntityConfigTrait` と同じ。`PropertyPath`（1024 文字まで）と `Value`（null は不可）で書き込む内容を指す。文字列はプロパティがテキストを受け付けるときテキストとして、それ以外の JSON 値は構造化ドキュメントとして書く。値によって Trait が構成のほかの Trait と重複する場合は `InvalidParams`、プロパティの書き込み経路が断った値はその経路自身のエラーコードで返す。**Trait のクラスを問わず**両方の Capability が要る。Trait のすべてのメンバーは共通のプロパティ書き込み経路で書かれ、エンジンの Mass モジュールの外の Trait では、その書き込みがプロジェクト自身のコードを走らせるため。参照や入れ子のオブジェクトを含む値は、`PropertyReferenceEdit` または `PropertyStructuredEdit` も要ることがある |
| `ConfigureMassSpawner`（`MassAssetEdit` が必要） | エディタのワールドにある Mass スポナー（`ActorIdentifier` はそのラベルまたはオブジェクトパス）の `Count`・`EntityTypes`・`SpawnDataGenerators`・`AutoSpawnOnBeginPlay` を設定する。少なくとも 1 つが必要で、指定したものだけが置き換わる。リストを指定すると全体が置き換わり（最大 64 件、`Proportion` の既定は 1）、エントリごとに新しい生成器が作られる。生成器のクラスは読み込み済みであること。生成器のクラスがエンジンの Mass モジュールの外にあるときは `MassCustomTypeEdit` も、エンティティの種類を置き換えた結果、エディタのワールドが、そのような Trait（受け継いだ Trait を含む）に行き着くテンプレートを登録するときは `MassProjectCodeExecution` も必要。テンプレートがすでにある構成は再利用され、どちらも要らない。応答は、作ったものと再利用したものを示す（`TemplatesBuiltInEditorWorld`・`ExistingTemplatesReused`）。`ExistingTemplatesReused` が 0 でなければ、古いテンプレートが使われている可能性がある（`ExistingEditorWorldTemplateReused`） |

**エラー。**

| ErrorCode | 発生条件 |
|---|---|
| `NotAllowed` | プレイセッション中の書き込み、または読み取り専用の場所にあるアセットへの書き込み |
| `NotFound` | アセット・Trait・クラス（未読み込み）・スポナーが存在しない。複数のアクターが持つラベルは `NotFound` で、該当するアクターを `CandidateActorPaths` に列挙する |
| `InvalidParams` | Trait の重複、曖昧な Trait や親だけが持つ Trait、構成ではないアセット、Trait や生成器ではないクラス、不正または範囲外のパラメータ |
| `CapabilityNotAvailable` / `PolicyViolation` | 必要な Capability が与えられていない / セーフティポリシーで拒否されている |

**Mass のアセットと汎用コマンド。** エンティティ構成アセットの作成、スポナーの配置、構成の親の設定は、既存の汎用コマンドで行います。このドメインの追加以降、Mass のアセット（構成・スポナー・Trait・生成器、およびそれらの設定を運ぶ構造体）に対する汎用のプロパティ書き込みには、`MassAssetEdit` と `MassProjectCodeExecution` も必要です。[安全性と Capability](safety.md#mass-の観測と編集) を参照してください。

---

## UAIP.Runtime.Engine.Log

ランタイム環境でのログ詳細レベル取得・ログカテゴリ一覧取得。`UAIP.Editor.Engine.Log` の Runtime 版に相当します。

| コマンド | 説明 |
|---|---|
| 🆓 `GetLogVerbosity` | 指定ログカテゴリの現在の詳細レベルを取得 |
| 🆓 `GetLogCategories` | 登録済みログカテゴリ名をすべて一覧表示 |
| `SetLogVerbosity` | ログカテゴリの詳細レベルを設定（`LogVerbosityEdit` 必要） |

---

## UAIP.Runtime.Engine.Plugin

エディタ / パッケージ版ビルド共通で使えるプラグイン観測コマンド（読み取り専用）。

| コマンド | 説明 |
|---|---|
| 🆓 `ListPlugins` | インストール済みプラグインと有効 / 無効状態の一覧 |
| 🆓 `GetPluginInfo` | プラグインの基本情報（名前・バージョン・有効状態）を取得 |
| 🆓 `IsEnabled` | プラグインが現在有効か確認 |
| 🆓 `GetPluginDependencies` | プラグインが依存するプラグイン一覧を返す |
| 🆓 `GetPluginForAsset` | 指定アセットを提供するプラグインを返す |

---

## UAIP.Runtime.Engine.CVar

エンジン全体のコンソール変数（CVar）を取得・検索・設定するコマンド。CVar は World 非依存のグローバル状態です。機密パターンの CVar は自動除外されます。

🔒 は `RuntimeCVarRead`（DefaultDenied）が必要。✏️ は `RuntimeCVarWrite`（DefaultDenied）が必要。デモ版配布物の `Config/DefaultUAIP.ini` は `RuntimeCVarRead` を事前付与しているため、以下の 🆓 コマンドはデモ版でもそのまま利用できます。

| コマンド | 説明 |
|---|---|
| 🆓🔒 `GetConsoleVariable` | 指定した CVar の名前・現在値・型・ヘルプテキストを返す（機密名は `NotFound`） |
| 🆓🔒 `SearchConsoleVariables` | ワイルドカード（`*`）パターンで CVar を検索（デフォルト 50 件・上限 200 件） |
| ✏️ `SetConsoleVariable` | 指定した CVar の値を設定（機密名・`ECVF_ReadOnly` 付きは拒否。`ECVF_Cheat` 付きは `AllowCheatCVarWrite` が有効でない限り拒否） |
| ✏️ `ResetConsoleVariable` | 指定した CVar をデフォルト値にリセット（機密名・`ECVF_ReadOnly` 付きは拒否。`ECVF_Cheat` 付きは `AllowCheatCVarWrite` が有効でない限り拒否） |

> **注意**: `UAIP.Runtime.World` にある旧 `GetConsoleVariable` / `SearchConsoleVariables` コマンド（旧バージョンでは `UAIP.Runtime.PIE` 配下に登録されていました）は非推奨です。引き続き動作しますが、本コマンド群を使用してください。

---

## UAIP.Runtime.Engine.Config

ランタイムおよびパッケージ版ビルドで ini キーを直接読み書きするコマンド群。`ISettingsModule` を経由せず ini ファイルに直接アクセスします。書き込みコマンドはパッケージ版ビルドでは実行できません。

| コマンド | 説明 |
|---|---|
| 🆓 `GetConfigValue` | セクション名とキー名を指定して ini キーの文字列値を読み取る。Capability 不要。シークレットのキーは `***` と `IsMasked: true` で返る。セクションが設定クラス（`/Script/<モジュール>.<クラス>`）ならそのクラスのプロパティで、そうでなければキー名で判定する。`IncludeSecretValues` を取る — [シークレット値の読み取り](#reading-secret-values)を参照 |
| `SetConfigValue` | raw ini キーを書き込みまたは削除。`ConfigSettingsEdit` 必要。パッケージ版ビルドでは実行不可。キー・値フィールドへの ini インジェクション文字（`[`・`]`）は拒否 応答の `OldValue` は、シークレットのキーなら `GetConfigValue` と同じ判定で `***` と `IsMasked: true` になり、`IncludeSecretValues` で平文を返せる — [シークレット値の読み取り](#reading-secret-values)を参照。隠れるのはこの `OldValue` だけで、書き込む値は監査ログでは伏せられない |

---

## UAIP.Runtime.Insights.Trace

Unreal Insights のトレース採取を制御するコマンド群。トレースは常に `Saved/Profiling/UAIP/` 配下のファイルへ書き出されます — **本モジュールのどのコマンドもトレースをネットワーク宛先へ送出できません**。UAIP が開始していないトレースは一切変更しません。`GetTraceStatus` は「他者が採取中である」ことのみを報告し、`StopTrace`（明示的に拒否）を除く制御コマンドはそのトレースに触れません。

読み取り 3 コマンドは `RuntimeInsightsInspect`（DefaultAllow）が必要です。制御 8 コマンドは `RuntimeInsightsControl`（DefaultDenied）が必要です。採取した `.utrace` ファイルの添付にはさらに `RuntimeInsightsAttachTraceFile`（DefaultDenied）が必要です — 詳細は [安全性と Capability](safety.md#runtime-insights-トレース採取) を参照してください。

トレース採取は PIE のライフサイクルから独立しています。PIE の開始・停止はトレースを開始も停止もせず、トレースは PIE セッションをまたいで採取を続けます。

### 読み取り（3）

| コマンド | 説明 |
|---|---|
| 🆓 `ListTraceChannels` | このビルドが認識するすべてのトレースチャネルを一覧（説明・現在の有効状態・切り替え可否・開示しうる内容）。エンジンが宣言するチャネルプリセットも、展開後のチャネルとその開示クラスとともに一覧します。エンジンのプリセットは大半がログチャネルを含むため、プリセットを `StartTrace` に渡す前に展開後の開示クラスを確認してください |
| 🆓 `GetTraceStatus` | エンジンが採取中か・採取が一時停止中か・稼働中のトレースが UAIP の開始したものかを報告。UAIP が開始したトレースについてはラベル・ファイル名・チャネル・開示クラス・経過時間・ファイルサイズ・自動停止の上限も報告します。UAIP が開始していないトレースについては活動の種別のみを報告し、宛先・チャネル集合・経過時間・サイズは秘匿します。経過時間とサイズは監視間隔ごとに更新されるため、最大で 1 間隔分古い値になりえます |
| 🆓 `ListTraceFiles` | UAIP が採取したトレースファイルを新しい順に一覧（ラベル・サイズ・ファイル名に埋め込まれた UTC タイムスタンプ。`MaxCount` は既定 50・上限 500）。ここに出た `FileName` が `AnalyzeTrace` の受け付ける値です。SafetyPolicy で外部トレース解析が有効な場合は、設定された外部ディレクトリ内の `.utrace` も `Source: External` として一覧します。一覧は何も削除しません（ローテーションはトレース開始時に行われます） |

### トレース制御（8）

| コマンド | 説明 |
|---|---|
| `StartTrace` | 指定したチャネル / チャネルプリセットを有効にして UAIP 専用のトレースディレクトリへ採取を開始し、書き込み先のファイル名を返します。`Channels` は必須、`Label`・`MaxDurationSeconds`（既定 300、範囲 1〜3600）・`MaxFileSizeMB`（既定 448、範囲 1〜4096）は省略可。UAIP が既に開始しているトレースは再起動されず、追加分のチャネルを有効化して `AlreadyRunning` / `LimitsIgnored` を報告するだけです。**実効チャネル集合**（既に有効 ∪ 要求）がログテキストを記録し `AllowLogDump` が false の場合は `PolicyViolation` で拒否します（要求を通すためにチャネルを無効化することはありません）。同じ集合に、ポリシーが生ファイルの引き渡しを認めない内容が含まれる場合は、`Warnings` に該当チャネル名と設定名を含む `AttachDisabledByPolicy` を返します（持ち出す前提の採取を無駄に始めずに済みます）。両上限は 1 秒ごとの確認のため、サイズ上限は厳密な天井ではありません。既定値はこの超過分の余裕を見込んであるため、サイズ上限を指定せずに採取したトレースは `AnalyzeTrace` が受け付ける 512 MB に収まります。それより大きい上限を指定した場合は `TraceTooLargeToAnalyze` の警告を返します |
| `StopTrace` | UAIP が開始したトレースを停止し、`AttachTraceFile` が true なら採取した `.utrace` を artifact として引き渡します。停止は常に成功します（何も採取していなければ成功の no-op、停止直後に再度停止した場合も同じ no-op — エンジンはトレースの後始末が終わるまで接続を稼働中として報告し続けますが、呼び出し元から見れば既に終わっています。ファイルを引き渡せない場合も `AttachSkippedReason` を付けてスキップし停止自体は成功）。UAIP が開始していないトレースは停止せず `NotAllowed` を返します。⚠️ ファイルの添付は、チャネル構成に関わらず**プロセスのコマンドラインを必ず開示します**。採取中にチャネル集合が変更されたトレース、未分類チャネルを含む集合、64 MB を超えるファイルは添付を拒否します。ログテキストを含む集合には `AllowLogDump`、ホスト側パス / 画面内容 / ネットワークアドレスを含む集合には `AllowDisclosingTraceAttachment` が必要です（エディタではエンジンが log / screenshot チャネルを自分で有効化するため、通常は両方必要になります）。停止しただけでは採取ファイルは閉じられません — エンジンのトレースライタが少し遅れて別スレッドで閉じます — そのためファイルを要求した場合は最大 3 秒まで解放を待ち、それでも書き込み中なら `AttachSkippedReason: "TraceFileStillOpen"` を返します（少し待ってから再度要求する価値があります）。ファイルを要求しなかった場合は待機しません |
| `PauseTrace` | 本モジュールが開始したトレースの採取を、停止せずに一時停止します。冪等（既に一時停止中なら `WasPaused: false`）、UAIP が開始したトレースが稼働していなければ成功の no-op、UAIP が開始していないトレースには `NotAllowed`。一時停止中もチャネル監視は動き続け、時間上限は実際に採取していた秒数のみを消費します |
| `ResumeTrace` | `PauseTrace` で一時停止した採取を再開します。冪等（一時停止中でなければ `WasResumed: false`）、UAIP が開始していないトレースには `NotAllowed`。名前が `Channel` で終わらないチャネルが再開時に復帰しないというエンジン側の既知不具合があるため、復帰しなかったチャネルは `Warnings` に `ChannelNotRestoredAfterResume` として報告されます（`SetTraceChannels` で再有効化できます） |
| `SetTraceChannels` | 本モジュールが開始したトレースの採取を続けたままチャネルを有効化 / 無効化します。`EnableChannels` / `DisableChannels` の少なくとも一方が非空である必要があります。チャネル状態はトレースより長く残るため、トレース非稼働時および UAIP が開始していないトレースに対しては `NotAllowed`。判定は「適用後に有効となる集合」に対して行うため、開示するチャネルを**無効化する**要求がそれ自体で拒否されることはありません。⚠️ 本コマンドを使うとトレースのチャネル集合が外部変更済みとしてマークされ、`StopTrace` はファイルの添付を拒否するようになります |
| `AddTraceBookmark` | 採取中のトレースへ時点マーカー（`Text`）を書き込みます。ブックマークチャネルが無効な場合（何も採取していない時点を含む）は何も書き込まず、`Written: false` で成功します。テキストは解析済みトレースからログテキストと同じポリシーで読み出されるため、`AllowLogDump` が false のときは `PolicyViolation` で拒否します。テキスト中の絶対パスは可搬なプレースホルダに置換されます |
| `BeginTraceRegion` | 採取中のトレースに名前付き区間（`Name`、省略可の `Category`）を開き、それを閉じるための `RegionId` を返します。区間は名前ではなく id で対応付けるため、入れ子の区間や同名の区間も区別されます。区間チャネルが無効でも `RegionId` は返り（`Written: false`）、閉じ方は同じです。開いたままの区間はトレース停止時とモジュール終了時に自動で閉じられます。`AddTraceBookmark` と同じく `AllowLogDump` でゲートされます |
| `EndTraceRegion` | `BeginTraceRegion` が開いた区間を `RegionId` で閉じます（開いている区間を指さない id は `NotFound`。自動クローズ済みの id を含む）。`DurationSeconds` はプロセス内で計測するため、区間チャネルが無効で何も書き込まれていなくても報告されます。自身はテキストを持たないため、ログダンプポリシーで拒否されることはありません |

---

## UAIP.Runtime.Insights.Analysis

採取済み `.utrace` ファイルのオフライン解析。本 Provider はトレース解析が有効なビルド構成でのみ登録されます。それ以外（デモ版を含む）ではコマンド自体が存在せず、呼び出すたびに失敗するのではなく `CommandNotFound` を返します。

3 コマンドすべてが `RuntimeInsightsAnalyze`（DefaultDenied）を必要とします（ステータス取得も同様。トレースを解析できない呼び出し元にとって解析の進捗は用途がないため）。

解析は非同期です。`AnalyzeTrace` で `AnalysisId` を取得し、`GetTraceAnalysisStatus` を `State` が `Completed` になるまでポーリングしてから `GetTraceAnalysisResult` を読みます。同時に実行できる解析は 1 件のみで、パース中 / 抽出中に届いた要求は `TooManyRequests` で拒否されます。このときエラーメッセージには枠を占有している解析の `AnalysisId` が含まれるため、当てずっぽうに再試行するのではなく `GetTraceAnalysisStatus` でその解析を監視できます。実行中の解析をキャンセルする手段はありません。完了した解析は枠を占有しません（保持時間の間は読み取り可能なまま残りますが、次の解析の開始を妨げません）。

また、解析は開始したセッションに属します。`GetTraceAnalysisStatus` と `GetTraceAnalysisResult` が `AnalysisId` を見つけられるのは、`AnalyzeTrace` を呼んだときと同じ `SessionId` で呼び出した場合だけです。それ以外のセッションから見た同じ識別子は `NotFound` になります。これは存在しない識別子に対する応答と意図的に同一です。未知の `AnalysisId`・保持時間が切れた `AnalysisId`・他セッションが所有する `AnalysisId` は区別されないため、この 2 コマンドで他の呼び出し元の識別子の存在を確かめることはできません。ひとつの `SessionId` を使い続けている限り、呼び出し方は従来どおりで構いません。ただし `SessionId` を省略すると、トランスポートが呼び出しごとに別々の匿名セッションを作るため、そうして開始した解析は二度と照会できなくなります。これはアセット監査ジョブのコマンドと同じ性質の要求です。

| コマンド | 説明 |
|---|---|
| `AnalyzeTrace` | トレースファイルの解析を開始し `AnalysisId` を返します。**開始した解析はこの呼び出しの `SessionId` に紐づき**、以後の照会・取得も同じ `SessionId` からのみ行えます。`FileName` は `ListTraceFiles` が報告した名前（パスではない）である必要があります。UAIP 以外が採取したトレースは `ExternalTracePath` を渡して解析しますが、これには外部解析のポリシー設定が必要です。省略可のパラメータは `Sections`・`StartTimeSeconds` / `EndTimeSeconds`・`TopN`（既定 32）・`MaxSeries`（既定 256）・`MaxSamplesPerSeries`（既定 1024）・`NameFilter`・`HitchThresholdMs`（既定 33.3）。512 MB を超えるトレースは拒否します。要求された各セクションは完了した順に個別の JSON artifact として書き出されるため、本コマンドは read-only ではありません。チャネルが記録されていないセクションや SafetyPolicy が秘匿するセクションは、実行を失敗させるのではなく理由付きで unavailable として報告されます |
| `GetTraceAnalysisStatus` | 解析の進行状況を報告します — `Running`（パース中）・`Extracting`（セクション抽出中）・`Completed`・`Failed` と経過時間、`CompletedSections`・`AvailableSections`・`UnavailableSections`（それぞれ理由付き）。`FailureReason` は固定の値集合から選ばれ、`State` が `Failed` のときのみ意味を持ちます。解析エンジン自身が報告したメッセージは絶対パスを含みうるため返さず、出力ログにのみ記録します。**開始時と同じ `SessionId` が必須** — 未知・保持時間切れ・他セッションの `AnalysisId` はいずれも区別されず `NotFound` になります。read-only |
| `GetTraceAnalysisResult` | 完了した解析が生成した artifact をセクションごとに返します（セクションごとの `TotalCount` / `ReturnedCount`、いずれかが上限に達した場合の `Truncated` を含む）。読めるのは `State` が `Completed` の解析のみで、**開始時と同じ `SessionId` からのみ**読めます（それ以外のセッションからは未知の識別子と同じく `NotFound`）。本コマンドは参照を返すだけで何も読まないため、必要なセクションだけを取得できます。元の `AnalyzeTrace` が要求しなかったセクションは、ここで解析し直すのではなく拒否されます。結果を読むたびに保持時間が延長されます（1 回の読み取りにつき 15 分、絶対上限 1 時間） |

`Sections` が受け付けるセクション名: `Frames`・`Counters`・`Timers`・`Threads`・`StackSamples`・`LoadTime`・`Memory`・`Allocations`・`Tasks`・`FileActivity`・`NetProfiler`・`CsvProfiler`・`ContextSwitches`・`CookProfiler`・`Bookmarks`・`Regions`・`Diagnostics`・`Channels`・`Log`・`Screenshots`、および `Objects`（UE 5.8 以降のみ。UE 5.7 には対応する Provider が存在しません）。

結果を読む前に知っておくとよいセクション個別の挙動が 3 点あります。

- **`Frames`** は開始と終了の両方が揃ったフレームだけを数えます。採取はフレームの途中で止まるため、各フレーム種別の最後のフレームはほぼ常に開いたままで報告できる長さを持ちません。そうしたフレームは統計からも `TotalCount` からも同様に除外されます。したがって `TotalCount` と `ReturnedCount` が食い違うのは時間範囲を指定したときだけで、本セクションが切り詰めを行うことはありません。
- **`Screenshots`** はメタデータのみを報告します（各スクリーンショットの識別子・名前・時刻・幅・高さと `ImageDataIncluded: false`）。エンコード済みの画像バイト列は返しません。画像が後から届くことはないため、メタデータ以外に待つものはありません。
- **`Diagnostics`** は UE 5.7 では `EngineVersion` キー自体を出力しません。UE 5.7 のトレース形式はエンジンバージョンを一切運んでいないため、空文字列（本当に記録がなかった採取と区別できない）ではなくキーの省略で表現しています。

---

## UAIP.Runtime.SaveGame

ゲームのセーブスロット（エンジンのセーブの仕組みがスロット名ごとに保存する `USaveGame` オブジェクト）を、一覧・確認・読み出し・退避・用意・削除・復元するコマンド群です。「特定のセーブから始める」「セーブが無い状態から始める」テストを組み、終わったら元に戻すために使います。エディタ（PIE の有無を問わない）でも、`-game` 起動やパッケージ版でも動作し、プラグインの依存はありません。

**何も読み込みません。** スロットを読むときにクラスやアセットを読み込むことはありません。スロットが指す SaveGame クラスと、その中のハード参照が指すオブジェクトは、すべてプロセス内に読み込み済みである必要があります。C++ のクラスはエディタでプロジェクトを開いていれば通常は読み込まれていますが、Blueprint のクラスはそのアセットを開くまで読み込まれていないことがあります。また、スロットの読み書きは実行中のゲームの状態を一切変えません。UAIP が担うのはスロットの読み書きまでで、読み込んだスロットをどう反映するかはゲーム側が決めます。

**Capability。** `ListSaveGameSlots`・`GetSaveGameInfo`・`ListSaveGameSnapshots` は `RuntimeSaveGameInspect`（DefaultAllow）が必要です。`DumpSaveGame` は `RuntimeSaveGameContentRead`（DefaultDenied）が必要です。スロットやスナップショットを変えるコマンドはすべて `RuntimeSaveGameWrite`（DefaultDenied）が必要です。`SnapshotSaveGame` も、スロットの生のバイト列を UAIP の作業ディレクトリへ複製するため、これに含まれます。さらに 2 つの引数が Capability を追加で要求します。`WriteSaveGame` で `BaseSlotName` を指定すると `RuntimeSaveGameContentRead` も必要になり、`CopySaveGameSlot` / `RestoreSaveGame` で `SkipValidation: true` を指定すると `RuntimeSaveGameUnvalidatedWrite`（DefaultDenied）が必要になります。足りない場合は `CapabilityNotAvailable` です。詳細は [安全性と Capability](safety.md#runtime-savegame-スロット) を参照してください。

**名前。** コマンドに渡すスロット名・スナップショット名は、`A-Z`・`a-z`・`0-9`・`_`・`-` からなる 1〜64 文字で、Windows の予約デバイス名（`CON`・`PRN`・`AUX`・`NUL`・`COM0`〜`COM9`・`LPT0`〜`LPT9`）ではないものに限ります。それ以外は `InvalidParams` です。スロット名とスナップショット名は別の名前空間なので、スナップショットに元のスロットと同じ名前を付けても構いません。`UserIndex` は 0 以上の整数（既定 0）です。Windows の標準のセーブの仕組みはこれを無視し、すべてのユーザー番号を同じファイルに保存します。

**典型的な流れ。** `SnapshotSaveGame` でスロットを退避 → スロットを変更（`DeleteSaveGame`・`WriteSaveGame`・`CopySaveGameSlot`）→ テストを実行して PIE を止める → `RestoreSaveGame` でスナップショットを戻す（スロットがあれば `Overwrite: true`）→ 不要になったら `DeleteSaveGameSnapshot`。変更前にスロットが無かった場合は退避するものがありません。後片付けは、作ったスロットの削除で行います。

### 確認（3）— `RuntimeSaveGameInspect` が必要

| コマンド | 説明 |
|---|---|
| `ListSaveGameSlots` | 設定中のセーブの仕組みが持つスロット名を、名前の昇順（大文字小文字を区別しない）で返します。`MaxResults` は 1〜1024（既定 256）で、漏れたスロットがあれば `Truncated` が `true` になります。`Slots[]` の各要素は `Name`・`Addressable`（他のコマンドに渡せない名前なら `false`。そのスロットは一覧には出ますが詳細は付きません）・`NameTruncated`（ファイル由来の名前は無害化したうえで 256 文字で切り詰めます）を持ちます。`IncludeDetails: true` を指定すると、指定できるスロットごとに `Status`・`ByteCount`・`ModifiedAt`・`Format`・`SaveGameClassName`・`ClassNameIsGuess`・`SaveGameClassNameTruncated` が付きます。読むのはスロットの先頭部分だけです（標準のセーブの仕組みでは先頭 1 MiB）。読んだ量の合計が 256 MiB に達すると、残りのスロットは詳細なしで返し、`DetailsTruncated` が `true` になります。`SaveGameSystem` には `ConfiguredSaveGameSystemModule` と `GenericPathsAvailable`（プロジェクトが標準のセーブの仕組みを使っているか。サイズと更新日時が得られるのはこのときです）が入ります。異常なスロットがあってもコマンドは失敗しません。セーブの仕組みがスロットの一覧に対応していないプロジェクトでは `UnsupportedOperation` を返します。スロット名が分かっていれば、他のコマンドは使えます |
| `GetSaveGameInfo` | 1 つのスロットのメタ情報を、クラスを読み込まずに返します。`Status`・`Format`・`StoppedAtStage`・`FileVersion`・`PackageFileUEVersion`・`EngineVersion`・`CustomVersionFormat`・`UnregisteredCustomVersionCount`・`SaveGameClassName`・`ClassNameIsGuess`・`SaveGameClassNameTruncated`・`ClassLoaded`（そのクラスが今読み込まれているか。探すだけで読み込みはしません）・`ByteCount`・`ModifiedAt`・`ContentHash`（SHA-1 を 16 進 40 桁で表したもの。`ExpectedHash` に渡す値です）。壊れている・大きすぎる・読めないスロットでもコマンドは失敗せず、`Status` でそれを示し、読めたところまでを返します。`ContentHash` はスロット全体を読めたときだけ返すため、`TooLarge` と `Unreadable` では付きません。`ModifiedAt` は標準のセーブの仕組みのときだけです。存在しないスロットは `NotFound` です |
| `ListSaveGameSnapshots` | `SnapshotSaveGame` が作ったスナップショットを、名前の昇順（大文字小文字を区別しない）で返します。`MaxResults` は 1〜1024（既定 256）で、`Truncated` も返します。読むのはメタ情報だけで、スロットのバイト列は読みません。`Snapshots[]` の各要素は `Name`・`NameTruncated`・`Status` を持ちます。`Status` は `OK`、またはメタ情報を読めないスナップショットファイルなら `Corrupt` です。`OK` の要素には `SourceSlotName`・`UserIndex`・`CreatedAt`（UTC）・`ByteCount`・`ContentHash`・`Format` と、ヘッダにクラス名があれば `SaveGameClassName`（切り詰めた場合は `SaveGameClassNameTruncated` も）が付きます。`Corrupt` の要素は上の 3 つのキーだけを持ち、見つけて削除できるように一覧に残します |

### 中身の読み出し（1）— `RuntimeSaveGameContentRead` が必要

| コマンド | 説明 |
|---|---|
| `DumpSaveGame` | 1 つのスロットを読み、プロパティの値を JSON の artifact として返します。artifact には `Properties`（プロパティ名 → 値）・`PropertyCount`・`UnresolvedReferences` / `ClearedSoftReferences` とその件数が入り、応答には `PropertyCount`・`UnresolvedReferenceCount`・`ClearedSoftReferenceCount` が入ります。読み込まれていないオブジェクトへのハード参照は `null` になり、そのパスを `UnresolvedReferences` に挙げます。ソフト参照は通常パスのまま残り、例外的に空にしたものを `ClearedSoftReferences` に挙げます。どちらの一覧も重複を除いて先頭 64 件までで、件数は全件を数えます。1023 文字を超えるパスは切り詰めて末尾に `...` を付けます。文字列テーブルを参照するテキストは、文字列テーブルを読み込まずに出力します。本体を読む前に拒否するもの: このコマンドが扱えないヘッダ（`ExecutionFailed`）、読み込まれていない SaveGame クラス（`NotFound`）や使えない SaveGame クラス、`MaxSaveFileBytes` を超えるスロット（`NotAllowed`）。⚠️ artifact にはセーブの中身がそのまま入ります — 後述の [DumpSaveGame の artifact とスナップショット](#dumpsavegame-の-artifact-とスナップショットはセーブをそのまま持つ) を参照してください |

### スロットの変更（3）— `RuntimeSaveGameWrite` が必要

| コマンド | 説明 |
|---|---|
| `DeleteSaveGame` | 1 つのスロットを削除します。存在しないスロットは、`ExpectedHash` の有無にかかわらず `NotFound` です。`ExpectedHash` を渡すと、先にスロット全体を 1 回読んで比較し、一致しなければ `Conflict` です。削除したスロットは元に戻せません。大事なデータなら先にスナップショットを取ってください。応答は `Deleted`・`PreviousContentHash`（スロットを読んだときだけ）・`PlayWorldActive` |
| `CopySaveGameSlot` | `SourceSlotName` のバイト列を、そのまま `TargetSlotName` へ複製します。2 つが同じスロット（大文字小文字を区別せずに比較）であってはいけません。複製するバイト列は SaveGame のヘッダ（形式・バージョン・クラス）まで確かめ、ヘッダが指すクラスは読み込み済みである必要があります。ヘッダより後ろの本体は確かめないため、本体が壊れたスロットも複製でき、それを後で読み込んだゲームが止まることがあります。`SkipValidation: true` でヘッダの確認を省けます — 後述の [SkipValidation](#skipvalidation) を参照してください。応答は `ByteCount`・`Overwritten`・`ContentHash`・`PreviousContentHash`（`ExpectedHash` のために複製先を読んだときだけ）・`ValidationSkipped`・`ValidationSkipReason`（省いたときは `RequestedByCaller`）・`PlayWorldActive` |
| `WriteSaveGame` | JSON オブジェクト `Values` からスロットを書きます。次のどちらか一方だけを指定します。**`SaveGameClass`** — そのクラスの新しいオブジェクトをクラスの初期値で作り、`Values` を適用します。クラスはフルパス（`/Script/<Module>.<Class>` または `/Game/<Path>/<Blueprint>.<Blueprint>_C`）で指定し、短い名前は拒否します。**`BaseSlotName`** — そのスロットを読んで復元し、`Values` を上書きした結果を `SlotName` へ保存します。`SlotName` は同じスロットでも（このときは `Overwrite: true` が必要）別のスロットでも構いません。一部書き換えは元のスロットの中身を読むため、`RuntimeSaveGameContentRead` も必要です。書き込む前にすべてのキーと値を確かめ、1 つでも拒否された値があれば何も書きません。配列・セット・マップは丸ごと置き換わり（要素を 1 つだけ指定すると他の要素は消えます）、構造体は指定した項目だけが変わります。保存するバイト列は SaveGame のヘッダまで確かめ、本体は確かめません。応答は `ByteCount`・`Overwritten`・`ContentHash`・`PreviousContentHash`（書き先を読んだときだけ）・`ValidationSkipped`（常に `false`）・`PlayWorldActive`。`Values` に書けるものは後述の [WriteSaveGame の Values](#writesavegame-の-values) を参照してください |

### スナップショット（3）— `RuntimeSaveGameWrite` が必要

| コマンド | 説明 |
|---|---|
| `SnapshotSaveGame` | スロットのバイト列を、そのまま名前付きのスナップショット（退避データ）へ複製します。保存先は UAIP 作業ディレクトリの `SaveGameSnapshots` フォルダ内のファイルです（[`AllowedArtifactDirectory`](config.md#allowedartifactdirectory-オーバーライド) で移していなければ `Saved/UAIP/SaveGameSnapshots/`）。バイト列は確かめないため、壊れたスロットやゲーム独自形式のスロットも退避できます。拒否するのは `MaxSaveFileBytes` を超えるスロットだけです（`NotAllowed`）。スナップショットには、退避元のスロット・ユーザー番号・退避した日時（UTC）・サイズ・内容のハッシュ・`Format`、ヘッダにあれば SaveGame クラスを記録します。同じ名前のスナップショットがあれば、`Overwrite: true` のときだけ置き換えます。置き換えは不可分ではありませんが、どこで止まっても古いものか新しいもののどちらかが残ります。スロットは読むだけなので、エディタでプレイ中でも `DisableSave` 下でも使えます。応答は `ByteCount`・`ContentHash`・`Format`（`SaveGameHeader`・`Legacy`・`Unknown`）・`Overwritten`・`PlayWorldActive`（`true` なら実行中のゲームも同じスロットへ書きうるため、ゲームが次に保存する内容とスナップショットが一致しないことがあります） |
| `RestoreSaveGame` | スナップショットのバイト列をスロットへ書き戻します。スロットに触れる前にスナップショットを確かめ、壊れていれば `ExecutionFailed`（理由 `SnapshotCorrupt`）です。`SlotName` と `UserIndex` はそれぞれ省略するとスナップショットに記録された値を使うため、省略すれば退避元のスロットへ戻ります。退避元と同じスロット・同じユーザー番号へ戻し（スロット名は大文字小文字を区別せずに比較）、バイト列のハッシュがスナップショットに記録したものから変わっていなければ、ヘッダの確認は自動的に省かれます（`ValidationSkipReason: "SameSourceSlot"`。追加の Capability は不要）。以前そこにあった中身を戻すだけなので、独自形式のセーブを使うゲームでもスナップショットを使えます。別のスロットへ戻す場合と、ハッシュが一致しない場合は通常どおり確かめるため、独自形式なら `SkipValidation: true` を指定しない限り失敗します。スナップショットは残るので、何度でも復元できます。応答のキーは `CopySaveGameSlot` と同じで、確認を省いたときの `ValidationSkipReason` は `SameSourceSlot` か `RequestedByCaller` です |
| `DeleteSaveGameSnapshot` | 1 つのスナップショットを、そのバックアップと、中断された退避が残した一時ファイルとともに削除します。存在しないスナップショットは `NotFound` です。壊れたスナップショットも削除できます。スロットには触れないため、エディタでプレイ中でも `DisableSave` 下でも使えます。応答は `Deleted` |

#### スロットの状態（Status）

| `Status` | 意味 |
|---|---|
| `OK` | ヘッダを最後まで読め、すべての確認を通った |
| `LegacyOrUnknown` | バイト列が SaveGame のヘッダで始まっていない（ゲーム独自の形式、または古いエンジンの形式）。報告されるクラス名は推定値（`ClassNameIsGuess: true`） |
| `UnsupportedVersion` | ヘッダがこのエンジンより新しい形式、または意図的に読まない古い版（UE4・UE 5.0 など）を示している |
| `Corrupt` | ヘッダが途中で切れている、形が崩れている、または範囲外の値を含む |
| `TooLarge` | ファイルが `MaxSaveFileBytes` を超えており、読んでいない |
| `Unreadable` | セーブの仕組みがスロットの読み込みに失敗した |

**確かめるのはファイルの先頭部分だけ**なので、`OK` はファイルの残りを復元できることを保証しません。また、スロットの保存は不可分ではないため、ゲームがちょうど書いている最中のスロットは `Corrupt` と読めることがあります。安定した複製が必要なら、先にスナップショットを取ってください。

**`PackageFileUEVersion` は数値ではなく文字列です。** `"UE4=<n>"`、またはヘッダが UE5 のバージョンも持つ場合は `"UE4=<n> UE5=<m>"` の形です。ヘッダの読み取りがそこまで届かなかった場合は省略されます。`StoppedAtStage` は読み取りが到達した段階（`ByteCount`・`Tag`・`FileVersion`・`EngineVersion`・`CustomVersionFormat`・`CustomVersions`・`ClassName`・`Completed`）を示し、`Corrupt` のヘッダをどこまで読めたかが分かります。

**`SaveGameClassNameTruncated`。** クラス名はファイルから来るため、無害化したうえで 256 文字で切り詰めてから返します。切り詰めた場合は、その隣に `SaveGameClassNameTruncated: true` が付きます。対象は `GetSaveGameInfo`、`IncludeDetails` を指定した `ListSaveGameSlots`、`ListSaveGameSnapshots` です。切り詰めていなければこのキーは付きません。切り詰めた名前はクラスの本当のパスではないため、そのまま `SaveGameClass` に渡さないでください。

#### DumpSaveGame の artifact とスナップショットはセーブをそのまま持つ

> ⚠️ **`DumpSaveGame` の artifact は、セーブの中身をそのまま JSON にしたものです。** セーブファイルには個人情報（プレイヤー名・アカウントの識別子など、ゲームが保存するあらゆるもの）が入りうるうえ、ランタイムには**秘密の値を伏せる仕組みがありません**。実行時には、どの値が秘密かを判別する情報が無いためです。`RuntimeSaveGameContentRead` が既定で無効なのはこのためです。artifact は Artifact の自動 GC が消すまで artifact ストアに残り（[設定リファレンス](config.md) の `[UAIP.ArtifactGC]`）、UAIP の作業ディレクトリを読める人なら誰でも読めます。
>
> **スナップショットも同じものを生のバイト列のまま持ち**、`DeleteSaveGameSnapshot` で削除するまで残ります。件数や合計サイズの上限は無く、自動では削除されません。不要になったスナップショットは削除してください。

#### WriteSaveGame の Values

- キーはプロパティ名と大文字小文字を区別せずに照合します（入れ子の構造体の中も同様）。存在しないキーや、一時的（Transient）・非推奨・保存対象外のプロパティは、無視せずに拒否します。
- JSON は最大 49152 バイト、入れ子は 16 段、値は 4096 個までです。名前・列挙子名・参照パスは 1023 文字までです。
- 数値はプロパティの型に収まる必要があります。64 ビット整数は ±2^53 まで受け付けます（JSON の数値で正確に表せる範囲です。それを超える値は丸まってしまうため拒否します）。浮動小数点数は文字列 `"NaN"`・`"Infinity"`・`"-Infinity"` も受け付けます。列挙型は列挙子名か宣言された値で指定します。
- テキストは指定した文字列がそのまま保存されます。文字列テーブル参照の書式で書いても参照としては扱わず、文字列テーブルも読み込みません。
- オブジェクト・クラス・ソフト参照は `/` で始まるフルパスで指定します（`DumpSaveGame` が出力する `Class'/Path.Obj'` の形もそのまま使えます）。ハード参照は読み込み済みのオブジェクトに解決できる必要があり、できなければ `NotFound` です。空文字列 `""` を渡すと参照は何も指さなくなります。
- 構造体は文字列ではなく JSON オブジェクトで指定します。セットに同じ要素を、マップに同じキーを 2 回指定してはいけません。
- 書けないもの: インターフェース・Lazy・デリゲート・フィールドパスのプロパティと、セーブが持つ入れ子のオブジェクト（`_ClassName` を持つオブジェクト）。作ると任意のクラスを読み込むことになるためです。
- 拒否された値が 1 つでもあれば、リクエスト全体が `InvalidParams` で失敗します。失敗診断の artifact には、どこがなぜ拒否されたか（`RejectedValues`・`RejectedValueCount`）が入り、値そのものは入りません。

> ⚠️ **`null` は片方向にしか通りません。** 何も指していない参照は `DumpSaveGame` では `null` として出力されますが、`WriteSaveGame` は `null` をどこでも拒否します。そのため、読み出した JSON をそのまま書き戻せないことがあります。参照を空にするには `""` を渡してください。`BaseSlotName` で一部書き換えをする場合は、そのキーを `Values` から外せば、元のスロットの値がそのまま残ります。

> ⚠️ **大文字小文字だけが違うキーは、重複として拒否されません。** `Values` はキーの大文字小文字を区別せずに読むため、`{"Score": 1, "score": 2}` は受け付けられ、後に書いた方だけが残ります。文字列をキーにするマップも同じ結果になります。ゲーム側でもそのキーを大文字小文字を区別せずに扱うため、保存される結果は変わりません。送る前に、大文字小文字だけが違うキーが無いか確かめてください。

**読み出した JSON をそのまま書き戻せない場合。** `null` のほかに、±2^53 を超える 64 ビット整数は `DumpSaveGame` の出力で丸まっており、ここでは拒否されます。テキストは単なる文字列として書かれます（文字列テーブル参照やローカライズ情報は残りません）。入れ子のオブジェクト（`_ClassName`）と、インターフェース・Lazy・デリゲート・フィールドパスのプロパティは書けません。

**参照が失われるスロットの一部書き換え。** 元のスロットに、`DumpSaveGame` なら `UnresolvedReferences` か `ClearedSoftReferences` に挙がる参照が 1 件でもあれば、`WriteSaveGame` は `NotFound` で拒否し、失敗診断の artifact にそのパスを挙げます。そのまま保存すると、変えていない参照まで消えるためです。先に参照先のアセットを読み込んでください。

#### 本体を読む前に拒否するもの

`DumpSaveGame` と、`BaseSlotName` を指定した `WriteSaveGame` は、スロットをそのクラスのオブジェクトへ復元します。その前に保存されたプロパティの並びを走査し、読み込むとエディタが止まるスロットを `ExecutionFailed` で拒否します。エラーには該当したプロパティの位置と理由が入り、値は入りません。

- クラス側で文字列でも文章（`FText`）でもない型に変わったプロパティ（配列・セット・マップの要素を含む）や、クラスから無くなったプロパティに、1024 文字以上の文字列が保存されている
- クラス側で名前（`FName`）型に変わったプロパティに、文章が保存されている（長さを問わない）
- クラス側でフィールドパス型に変わったプロパティに、オブジェクト参照が保存されている
- 並びの構造が壊れている（値の大きさが範囲外、要素数が負など）

ゲーム自身は、このうち一部（特に、無くなったプロパティに残った長い文字列）を問題なく読めることがあります。UAIP はこれらを読みません。独自の方法で直列化する構造体（`InstancedStruct` など）の内側までは確かめません — [残るリスク](safety.md#runtime-savegame-スロット) を参照してください。

#### 上書きと ExpectedHash

`CopySaveGameSlot`・`WriteSaveGame`・`RestoreSaveGame` と、既存のスナップショットに対する `SnapshotSaveGame` は、`Overwrite: true` を指定しない限り既にあるものを置き換えません（`NotAllowed`）。同じスロットへの一部書き換えには常に必要です。置き換えた場合、応答の `Overwritten` が `true` になります。

`DeleteSaveGame`・`CopySaveGameSlot`・`WriteSaveGame`・`RestoreSaveGame` の `ExpectedHash` は、書き込む直前に**書き先のスロット**（複製元・一部書き換えの元・スナップショットではない）が持っているべき内容のハッシュです。16 進 40 桁で、大文字小文字を区別せずに比較し、`GetSaveGameInfo` が返す値をそのまま使えます。一致しない場合や、書き先が無い場合は `Conflict` で、何も書きません（`DeleteSaveGame` で対象が無い場合は `NotFound`）。`ExpectedHash` を渡すと書き先を全部読むため、読み取りの上限がかかります。渡さなければ書き先を読まないので、上限を超えるスロットでも置き換え・削除できます。確認は書き込む直前の 1 回だけです。確認と書き込みの間にゲームが非同期で保存したり、別のプロセスが書き込んだりすることまでは防げません。

#### プレイ中と DisableSave 下

`DeleteSaveGame`・`CopySaveGameSlot`・`WriteSaveGame`・`RestoreSaveGame` は、エディタでプレイ中は `NotAllowed` で拒否します。実行中のゲームが同じスロットを読んだり上書きしたりしうるためです。エラーには、許可する設定 `[UAIP.SaveGame]` の `bAllowWritesDuringPIE` の名前が入ります。プレイを止めてから再実行してください。`-game` 起動やパッケージ版ではこの拒否はありません（ゲームが後から同じスロットを上書きすることはあります）。同じ 4 つは、SafetyPolicy が `DisableSave` のとき `PolicyViolation` で拒否します。

`ListSaveGameSlots`・`GetSaveGameInfo`・`DumpSaveGame`・`SnapshotSaveGame`・`ListSaveGameSnapshots`・`DeleteSaveGameSnapshot` は、どちらの場合も使えます。スロットを変える 4 つと `SnapshotSaveGame` の応答にある `PlayWorldActive` は、その時点でゲームが同じスロットへ書きうる状態だったか（エディタでプレイ中、または `-game` 起動やパッケージ版で動作中）を示します。

**書き込みは不可分ではありません。** 書き込みの途中で失敗すると（ディスクの容量不足、ファイルのロックなど）、書き先のスロットが壊れることがあります。残したいスロットは、置き換える前にスナップショットを取ってください。スナップショットから戻せます。

#### SkipValidation

`CopySaveGameSlot` と `RestoreSaveGame` は `SkipValidation: true` を受け付けます。ヘッダの確認を省くため、ゲーム独自形式・壊れている・対応していない版・クラスが読み込まれていないスロットでも、任意のスロットへ複製・復元できます。`RuntimeSaveGameUnvalidatedWrite`（DefaultDenied）が必要で、無ければ `CapabilityNotAvailable`（`DeniedCapabilities` で明示的に拒否されていれば `PolicyViolation`）で失敗します。復元が `SameSourceSlot` に当たる場合でも同じです。応答は `ValidationSkipped: true` と `ValidationSkipReason: "RequestedByCaller"`（`SameSourceSlot` にも当たる場合は `"SameSourceSlot"`）です。サイズの上限は省けません。⚠️ **こうして書いたスロットは、それを読み込んだゲームを止めることがあります。**

#### エラー

| ErrorCode | 発生する場面 |
|---|---|
| `InvalidParams` | 名前・`UserIndex`・`MaxResults`・ハッシュ・クラスパス・値が正しくない。`SourceSlotName` と `TargetSlotName` が同じスロット。`WriteSaveGame` に `SaveGameClass` と `BaseSlotName` を両方指定した、またはどちらも指定しなかった。クラスが `USaveGame` の具象で現行のサブクラスではない |
| `NotFound` | スロットやスナップショットが無い。SaveGame クラスや、値が参照するオブジェクトが読み込まれていない。一部書き換えの元のスロットに、失われる参照がある |
| `NotAllowed` | 書き先があるのに `Overwrite` が `true` でない。エディタでプレイ中。ファイルが `MaxSaveFileBytes` を超えている（エラーに設定名が入る） |
| `Conflict` | `ExpectedHash` が一致しない、または指定した書き先が無い |
| `PolicyViolation` | SafetyPolicy が `DisableSave`（スロットの変更のみ）、または必要な Capability が `DeniedCapabilities` で明示的に拒否されている（`CapabilityNotAvailable` より先に判定されるため、こちらが優先） |
| `CapabilityNotAvailable` | 必要な Capability（引数が追加で要求するものを含む）が無い。エラーにその名前が入る |
| `ExecutionFailed` | ヘッダを扱えない、データが示すクラスを使えない、本体を読めない（上記の拒否を含む）、スナップショットが壊れている、スロットやスナップショットの読み書きに失敗した |
| `UnsupportedOperation` | スロットの一覧に対応していないセーブの仕組みで `ListSaveGameSlots` を呼んだ |

失敗したコマンドは失敗診断の artifact を付けます。中身は `Command`・`FailedStage`・`Reason`（原因。例: `SnapshotCorrupt`）・`ErrorMessage` と、失敗した段階が報告した内容です（扱えなかったヘッダの各項目、解決できない参照のパス、拒否した `Values` の `RejectedValues` / `RejectedValueCount` など）。セーブに保存された値が含まれることはありません。

---

## UAIP.Runtime.AI

このドメインは、実行中のゲームの AI を観測します。AI 感知システムのほか、BehaviorTree と Blackboard も観測します（下の [BehaviorTree と Blackboard の観測](#behaviortree-と-blackboard-の観測) を参照）。そのセクションの手前までは、感知の 6 コマンドの説明です。

実行中のゲームの AI 感知システム（AI Perception）を観測するコマンド群です。1 体の AI がいま何を感知しているか、ある Actor をどの AI が感知しているか、感知システム自体の状態、視覚がなぜ対象を見る／見ないのか、感覚設定の値を返します。感知のコマンドはどれも読むだけで、AI の感知内容を変えることはありません。エディタでは PIE の実行中に、また `-game` 起動やパッケージ版でも動作し、プラグインの依存はありません。感知の 6 コマンドすべてが [`TargetNetRole` / `TargetPIEInstance`](#実行時コマンドの対象プレイワールドを指定する) を受け付けます。

**Capability。** 感知の 6 コマンドすべてが `RuntimeInspect`（DefaultAllow）を必要とします。`DumpAIPerceptionSenseConfigs` は、プロジェクト独自の感覚クラスのものを含めて感覚設定の値をすべて書き出すため、`AIPerceptionConfigDump`（DefaultDenied）も必要です。足りない場合は `CapabilityNotAvailable` です。詳細は [安全性と Capability](safety.md#runtime-ai-の感知) を参照してください。

**感知はサーバーにしかありません。** AI コントローラーと感知システムが存在するのはスタンドアロンかサーバーのワールドだけです。ネットワークプレイの PIE では `TargetNetRole: "Server"` または `TargetPIEInstance` でサーバーを指定してください。クライアントのワールドを観測してもコマンドは成功しますが、`Availability.State: "Unavailable"`・`Reason: "ClientWorld"` を返し、再実行先となるサーバー側のプレイワールドを列挙します — [感知システムが使えないとき](#感知システムが使えないとき) を参照してください。

### 感知の状態（5）— `RuntimeInspect` が必要

| コマンド | 説明 |
|---|---|
| 🆓 `DumpAIPerceptionState` | 1 体の AI の感知コンポーネントが持つ内容をすべて返します。`ActorIdentifier` には Pawn・AI コントローラー・その他の感知コンポーネントを持つ Actor を指定します（[感知コンポーネントの探し方](#感知コンポーネントの探し方) を参照）。artifact には設定された感覚（`Senses[]`）・`ListenerId`（登録済みのとき）・`TeamId`（`255` はチームなし）・`DominantSense`・感知中の Actor とその刺激（`Targets[]`）・`AgeUnitNote` が入ります。`MaxTargets` は 1〜4096（既定 256）。期限切れの刺激は `IncludeInactiveStimuli: true` を指定しない限り除外し、その場合は刺激がすべて期限切れの Actor は一覧にも件数にも含めません。応答には `ListenerRegistered`・`TargetCount`・`TargetsTotalCount`・`TargetsTruncated` が入ります |
| 🆓 `GetPerceivedActors` | 1 体の AI がいま感知している Actor（`Mode: "Current"`、既定）か、感知を失ってもまだ覚えている Actor を含めたもの（`Mode: "Known"`）を返します。`Mode` の大文字小文字は区別しません。`Sense` を指定すると、コンポーネントに設定された感覚の 1 つに絞り込み、状態もその感覚だけで判定します。指定は短い名前（`Sight` など。大文字小文字を区別しない）かクラスパス（完全一致）です。設定された感覚のどれにも一致しない、または複数に一致する名前は `InvalidParams` で、メッセージに設定されている感覚を列挙します。`HostileOnly: true` はエンジンが敵対と記録した Actor だけを残します。`MaxActors` は 1〜4096（既定 256）。応答には `Actors[]`（`Name`・`Label`・`Path`・`Senses[]`・`IsHostile`）の先頭 50 件・`ActorsTotalCount`・`ActorsTruncated`・`Mode`、指定したときは `Sense` が入り、artifact には全件が入ります。返った `Name` はそのまま `ActorIdentifier` に渡せます。ただし別の Actor のラベルが同じ文字列の場合は除きます |
| 🆓 `GetActorPerceivers` | 逆方向の問い合わせです。`ActorIdentifier` の Actor をどの AI が感知しているかを返します。この Actor 自身は感知コンポーネントを持っていなくて構いません。`Perceivers[]` には感知しているコンポーネント（`ComponentOwner`）ごとに、その Actor について持っている刺激が入ります。期限切れの刺激は常に除外します。`Source` は刺激の発生源としての Actor を表します。`ConfiguredOnSourceComponent[]`（Actor が持つ刺激源コンポーネントと、その `AutoRegister`・登録先の感覚）、`ObservedBySight[]`（ワールドで動いている視覚の実装ごとに、Actor が視覚の対象として登録されているか。感知システムが使えない間は省略）、`OtherSenses: "Unknown"`（他の感覚に登録されているかは読み取れません）です。`MaxPerceivers` は 1〜4096（既定 256）。応答には先頭 50 件・`PerceiversTotalCount`・`PerceiversTruncated` が入り、artifact には全件が入ります |
| 🆓 `DumpAIPerceptionSystemState` | ワールド全体の感知システムを返します。応答には `HasBegunPlay`・`HasAuthGameMode`・`ComponentsWithValidListenerId`（近似値。リスナー ID を持つコンポーネントの数）・`SightStatistics[]`（視覚の実装ごとの `ObservedTargetCount`・`QueriesInRangeCount`・`QueriesOutOfRangeCount`・`QueriesPendingCount`）・`ComponentCount`・`ComponentsTotalCount`・`ComponentsTruncated` が入ります。artifact にはさらに `PerceptionAgingRate`・`Senses[]`（感覚ごとの `IsInstantiated`。設定されたが生成されていない感覚も含む）・`Components[]`（感知コンポーネントごとの `ListenerRegistered` と `EnabledSenses[]`）が入ります。`MaxComponents` は 1〜4096（既定 256） |
| 🆓 `ExplainSightPerception` | `ObserverIdentifier` から見て `TargetIdentifier` が視覚で見える／見えない理由を、順序付きの 14 段階で返します。対象は感知コンポーネントを持っていなくて構いません。応答と artifact は同じオブジェクトです。説明は現在の状態から計算し直したもので、**エンジンの判定そのものではありません** — [ExplainSightPerception の読み方](#explainsightperception-の読み方) を参照してください |

### 感覚設定の値（1）— `RuntimeInspect` と `AIPerceptionConfigDump` が必要

| コマンド | 説明 |
|---|---|
| `DumpAIPerceptionSenseConfigs` | 1 体の AI の感知コンポーネントにある感覚設定すべてについて、全プロパティの値を返します。プロジェクト独自の感覚クラスの設定も含みます。応答には `SenseCount` と `Truncated` が入り、値は artifact の `Senses[]` に入ります — [DumpAIPerceptionSenseConfigs の値](#dumpaiperceptionsenseconfigs-の値) を参照してください。感知システムが使えるかどうかの影響を受けません。⚠️ artifact は `AIPerceptionConfigDump` を外した後も残ります — [安全性と Capability](safety.md#runtime-ai-の感知) を参照してください |

#### パラメータ

| パラメータ | コマンド | 意味 |
|---|---|---|
| `ActorIdentifier`（必須） | `DumpAIPerceptionState`、`GetPerceivedActors`、`DumpAIPerceptionSenseConfigs` | 感知コンポーネントを読む Pawn・AI コントローラー・その他の Actor のラベルまたはオブジェクト名 |
| `ActorIdentifier`（必須） | `GetActorPerceivers` | 感知される側の Actor のラベルまたはオブジェクト名 |
| `ObserverIdentifier`、`TargetIdentifier`（どちらも必須） | `ExplainSightPerception` | 見る側の Actor（`ActorIdentifier` と同じ方法で探します）と、見えるかを説明する Actor のラベルまたはオブジェクト名 |
| `MaxTargets` / `MaxActors` / `MaxPerceivers` / `MaxComponents` | それぞれ 1 つ | 主となる一覧の上限。1〜4096 の整数で、既定 256 |
| `IncludeInactiveStimuli` | `DumpAIPerceptionState` | 真偽値、既定 `false`。`true` で期限切れの刺激も返します |
| `Mode` | `GetPerceivedActors` | `"Current"`（既定）または `"Known"`。大文字小文字は区別しません |
| `Sense` | `GetPerceivedActors` | 感覚の短い名前かクラスパス。`A-Z`・`a-z`・`0-9`・`_ . / : -` からなる 256 文字以内 |
| `HostileOnly` | `GetPerceivedActors` | 真偽値、既定 `false` |

識別子は制御文字を含まない 1〜256 文字です。真偽値は JSON の真偽値、上限値は JSON の整数でなければならず、それ以外の型・未知のキー・1〜4096 の範囲外の上限値は `InvalidParams` です。パラメータはプレイワールドを探す前に検査するため、PIE が動いていなくても不正な要求は拒否されます。

#### 感知コンポーネントの探し方

`DumpAIPerceptionState`・`GetPerceivedActors`・`ExplainSightPerception`（見る側）・`DumpAIPerceptionSenseConfigs` には、Pawn・その AI コントローラー・感知コンポーネントを持つその他の Actor のどれを指定しても構いません。コンポーネントは指定した Actor と、それと対になるコントローラーまたは Pawn から探し、両方が持っている場合はコントローラー側を使います。使ったコンポーネントは応答の `ComponentOwner`（`Name`・`Path`・`ComponentPath`）で示し、他に見つかったものは `OtherComponentsFound[]` に `OtherComponentsFoundTotalCount`・`OtherComponentsFoundTruncated` と共に挙げます。対のどちらも感知コンポーネントを持っていない場合は `NotFound` です。

#### すべての応答に入るフィールド

| フィールド | 意味 |
|---|---|
| `CapturedAt` | 状態を読んだ時刻（ISO 8601、UTC） |
| `Frame` | そのときのエンジンのフレーム番号 |
| `NetMode` | 観測したワールドのネットモード |
| `WorldContext` | コマンドが読んだワールドコンテキスト |
| `PIEInstance` | 観測したワールドの PIE インスタンス。PIE 以外では省略 |
| `Availability` | `State` は `Available` か `Unavailable`。使えないときは `Reason` が付き、`ClientWorld` のときはさらに `ServerCandidates[]`（サーバー側プレイワールドごとの `PIEInstance`・`NetMode`・`MapName`・`IsPrimaryPIEInstance`）が付きます |
| `DegradedSections[]` | 埋められなかった部分。各要素は `Section` と `Cause`（`PerceptionSystemUnavailable` または `UnreadableField`）を持ちます。空の配列なら欠けた部分はありません |
| `Limitations[]` | 返した内容についての注意事項。各要素は `Code` と、場合によって `Detail` を持ちます |

`Limitations[].Code` は次のいずれかです。

| `Code` | 意味 |
|---|---|
| `UnreadableField` | このエンジンバージョンではエンジン側の値を読めませんでした。`Detail` がそのフィールドを示し、それに依存する部分は省きます |
| `UnknownStimulusExcludedFromMode` | 状態を分類できない刺激があります。`GetPerceivedActors` はこれをどの `Mode` にも一致させません |
| `StaleTargetsSkipped` | もう存在しない Actor の項目を飛ばしました。`Detail` は飛ばした件数です |
| `CustomSightImplementation` | 視覚がエンジン標準の視覚クラスで実装されていません。`Detail` が使われているクラスを示します |
| `RecomputedFromCurrentState` | `ExplainSightPerception` のみで、常に付きます。説明が現在の状態から計算し直したものであることを示します |

#### 感知システムが使えないとき

使える感知システムが無いワールドはエラーになりません。コマンドは成功し、`Availability.State` が `Unavailable`、`Availability.Reason` がその理由を示します。

| `Reason` | 意味 |
|---|---|
| `ClientWorld` | クライアントのワールドです。AI はサーバーにしかありません。`ServerCandidates[]` がサーバー側のプレイワールドを列挙します |
| `AISystemDisabled` | ワールド設定で AI が無効になっており、AI システムがありません |
| `CustomAISystem` | ワールドの AI システムがエンジン標準のものではなく、その感知システムに届きません |
| `Unknown` | 上記以外の理由で、AI システムまたは感知システムがありません |

このとき感知システムに依存する部分は `DegradedSections[]` に挙げ、結果から省きます。

| コマンド | `Section`（原因 `PerceptionSystemUnavailable`） | `Section`（原因 `UnreadableField`） |
|---|---|---|
| `DumpAIPerceptionState` | `Targets`、`Senses` | `Targets` |
| `GetPerceivedActors` | `Actors` | `Actors` |
| `GetActorPerceivers` | `Perceivers`、`Source.ObservedBySight` | `Perceivers` |
| `DumpAIPerceptionSystemState` | `Senses`、`SightStatistics`、`ComponentsWithValidListenerId` | — |
| `ExplainSightPerception` | —（常に空。代わりに最初の段階が失敗します） | — |
| `DumpAIPerceptionSenseConfigs` | —（常に空。影響を受けません） | — |

`ListenerRegistered` と各感覚の `IsInstantiated` は、感知システムが使えるときだけ書き出します。Actor とコンポーネントの確認が先に行われるため、感知システムの無いワールドでも、存在しない Actor は `NotFound` になります。

#### 一覧・件数・値の無い項目

- **値が無い項目は省略し、`null` にはしません。** エンジンの「未設定」を表す番兵値（一度も設定されていない位置など）や、有限でない数値も同様です。このドメインで `null` になるのは `ExplainSightPerception` の `Diverged` だけです。
- **一覧の並び順**は `Name`（大文字小文字を区別しない）、次に `Path` です。コンポーネントは所有者の名前、次に `ComponentPath` の順です。感覚設定は設定された順のままです。
- **内側の一覧**（対象ごとの刺激、Actor ごとの感覚、他に見つかったコンポーネントなど）は最大 64 件で、`<Key>TotalCount` と `<Key>Truncated` が付きます。
- **`<Key>Truncated` は `Max*` の上限で一覧が切られたことだけを表します。** `GetPerceivedActors` と `GetActorPerceivers` は、何も切られていなくても応答には先頭 50 件しか入れません。取得した全件は artifact に入ります。たとえば `ActorsTruncated: false` で `Actors[]` が 50 件、`ActorsTotalCount: 120` なら、件数と配列の長さを比べ、残りは artifact から読んでください。

#### 刺激

刺激ごとに `SenseClass`（感覚が生成されていれば `SenseName` も）・`StimulusState`・`Strength`・`Age`・`ExpirationAge`・`StimulusLocation`・`ReceiverLocation`・`Tag`・`WasSuccessfullySensed`・`IsExpired` が入ります。値が無い項目は省略します。

| `StimulusState` | 意味 |
|---|---|
| `Sensing` | いま感知している |
| `LostButRemembered` | 感知を失ったが、まだ期限切れではない |
| `Expired` | 最大経過時間を過ぎた。`IncludeInactiveStimuli: true` のときだけ返します |
| `Unknown` | 分類できない。一覧と件数には含めますが、どの `Mode` にも一致させず、`UnknownStimulusExcludedFromMode` を付けます |

不具合に見えるがエンジンの仕様どおりのもの:

- **出来事を通知する感覚（聴覚など）は、刺激が期限切れになるまで `Sensing` のままです。** こうした感覚は自分から「失った」と通知しません。
- **最大経過時間が 0（感覚設定の既定値）の刺激は期限切れになりません。** そのため `LostButRemembered` のまま残り続けます。
- **経過時間は段階的に進みます。** 感知システムが刺激の経過時間を進めるのは `PerceptionAgingRate` 秒（既定 0.3 秒）ごとなので、`Age` と `ExpirationAge`（ゲーム時間の秒）は、刺激からの実際の経過時間より最大でその間隔ぶん遅れることがあります。artifact の `AgeUnitNote` も同じことを述べています。
- **AI システムの「古い Actor を忘れる」設定が有効な場合、`Expired` は現れません。** エンジンは刺激がすべて期限切れになった Actor を、期限切れとして残さずに取り除きます。

#### ExplainSightPerception の読み方

応答は**現在の状態**から作ります。1〜9 段階はエンジンがいま持っている状態を読み、10〜14 段階は現在の設定・位置・チームから視覚の判定を計算し直します。これは**エンジン自身の判定記録ではなく**、エンジンが最後に更新したときの判定と食い違うことがあります — その後に見る側が動いた、クエリがまだ再評価されていない、トレースが非同期で走っている、実行中に設定が変わった、といった場合です。判定そのものではなく、診断の手掛かりとして使ってください。`Limitations` には常に `RecomputedFromCurrentState` が付きます。

`AlgorithmRevision`（整数。現在は `1`）は段階の評価方法を識別します。段階の意味が変わるたびに上がるので、説明どうしを比べるのはこの値が同じときだけにしてください。`EvaluationBasis` は常に `"CurrentState"` です。

`Steps[]` の各要素は `Step`・`Basis`（`EngineState` または `Recomputed`）・`Result`、場合によって `Detail` を持ちます。14 段階すべてが常にこの順で入ります。

| # | `Step` | `Basis` | 確認する内容 |
|---:|---|---|---|
| 1 | `PerceptionSystemAvailable` | `EngineState` | ワールドに使える感知システムがある |
| 2 | `ListenerRegistered` | `EngineState` | 見る側の感知コンポーネントがリスナーとして登録されている |
| 3 | `SightConfigured` | `EngineState` | コンポーネントに視覚の設定がある |
| 4 | `SightEnabled` | `EngineState` | コンポーネントで視覚が有効になっている |
| 5 | `SightInstantiated` | `EngineState` | 感知システムに視覚の感覚が生成されている |
| 6 | `TargetIsNotSelf` | `EngineState` | 対象が見る側自身ではない |
| 7 | `DigestAvailable` | `EngineState` | 視覚の感覚が、見る側の設定を取り込んだもの（ダイジェスト）を持っている |
| 8 | `ObservedBySight` | `EngineState` | 対象が視覚の対象として登録されている |
| 9 | `QueryExists` | `EngineState` | この見る側と対象の組の視覚クエリがある |
| 10 | `Affiliation` | `Recomputed` | チームの関係が対象の感知を許している |
| 11 | `AutoSuccess` | `Recomputed` | 対象が最後に見えた位置からの自動成功範囲内にいる |
| 12 | `Distance` | `Recomputed` | 対象が視覚の範囲内にいる |
| 13 | `PeripheralAngle` | `Recomputed` | 対象が周辺視野角の内側にいる |
| 14 | `Occlusion` | `Recomputed` | 視線を遮るものがない |

`Result` は `Pass`・`Fail`・`Skipped`（前の段階の結果により評価しなかった）・`NotApplied`（その段階が当てはまらない）・`Delegated`（対象が自分で判断する）のいずれかです。段階どうしの関係は次のとおりです。

- 1〜8 段階は最初の `Fail` で止まり、それ以降はすべて `Skipped` になります。
- `QueryExists` が失敗した場合は、候補となる理由として `Affiliation` だけを評価し（クエリが作られない理由はたいていチームの関係です）、残りは `Skipped` です。
- `QueryExists` が通った場合は、クエリがある時点でチームの関係はすでに作成を許しているので `Affiliation` は `Skipped` になり、11〜14 段階を評価します。
- `AutoSuccess` は失敗しません。`Pass` なら残りの段階は `Skipped` になり、そうでなければ `NotApplied` です（既定の設定では常に `NotApplied`）。
- `Distance` は、エンジンが前回対象を見ていた場合は視覚を失う半径を、そうでなければ視覚の半径を使います。
- `Distance` か `PeripheralAngle` が `Fail` なら `Occlusion` は `Skipped` です。
- 視覚対象のインターフェースを実装した対象は自分で見えるかを判断するため、`Occlusion` は `Delegated` になり、その判定関数は呼びません。

`QueryExists` には `QueryList`（`SightQueriesInRange`・`SightQueriesOutOfRange`・`SightQueriesPending` のいずれか）・`Pending`・`LastSeenLocation`・`LastResult`（クエリが保留中でないときだけ）・`AsynchronousTrace` が付きます。`Affiliation` には `TeamAgent`（`Owner`・`BodyActor`・`None` のいずれか。どのチームを使ったか）が付きます。`Occlusion` には、視線を遮るものがあれば `HitActor` が付きます。

各フィールドが入る条件:

| フィールド | 入る条件 |
|---|---|
| `Observer`、`Target`（`Name`・`Label`・`Path`）、`ComponentOwner`、`OtherComponentsFound[]` | 常に |
| `EvaluationBasis`、`AlgorithmRevision`、`Steps[]` | 常に |
| `Diverged` | 常に。計算し直した結果をエンジンの前回の結果と比べられるときは `true` か `false`、比べられないとき（エンジン状態の段階が失敗した、クエリが保留中、`Occlusion` が `Delegated`）は `null` |
| `DivergenceCandidates[]` | 常に。要素が入るのは `Diverged` が `true` のときだけです。入りうる要素: `StaleListenerLocation`・`QueryNotYetReevaluated`・`AsynchronousTrace`・`ConfigChangedAtRuntime`・`CustomSightImplementation` |
| `ConfigDigestMismatch[]` | 常に。視覚の設定と、視覚の感覚がそれを取り込んだ値とで食い違う項目ごとに `{Field, FromConfig, Digested}` が 1 つ入ります（`SightRadiusSq`・`LoseSightRadiusSq`・`NearClippingRadiusSq`・`PeripheralVisionAngleCos`・`PointOfViewBackwardOffset`・`AutoSuccessRangeSqFromLastSeenLocation`・`AffiliationFlags`） |
| `ListenerRegistered` | `ListenerRegistered` 段階を評価したとき |
| `FirstFailingStep` | 失敗した段階があるとき。`QueryExists` が失敗した場合は `QueryExists` で、`Affiliation` がその候補となる理由です |
| `SightConfigUsed`（`ConfigClass`・`ImplementationClass`・`OtherSightConfigs[]`） | `SightConfigured` が通ったとき。最初の視覚設定を使い、他は一覧に挙げます |
| `EngineLastResult` | `QueryExists` が通り、クエリが保留中でないとき |
| `EngineConeCheck` | `DigestAvailable` が通ったとき |

視覚がエンジン標準の視覚クラスで実装されていない場合は、`Limitations` に `CustomSightImplementation` が付き、計算し直した段階は目安にとどまります。**視覚対象のインターフェースが、保留中の見え方の判定を別スレッドで完了させる対象には対応していません。** そのような対象についてこのコマンドが返す内容は保証されません。

#### DumpAIPerceptionSenseConfigs の値

`Senses[]` の各要素は `SenseName`（生成されているとき）・`SenseClass`・`ConfigClass`・`IsEnabled`・`IsInstantiated`（感知システムが使えるときだけ）・`Properties[]`（`Name`・`Type`・`Value`）・`Truncated` を持ちます。プロパティは基底クラスのものが先で、各クラス内は宣言順です。エディタ専用のプロパティは挙げません。値は次の形で書き出します。

| プロパティ | 書き出し方 |
|---|---|
| 数値、真偽値 | 値そのもの。有限でない浮動小数点数は文字列 `"NaN"`・`"Infinity"`・`"-Infinity"` |
| 列挙型 | 項目名。名前の無い値は数値 |
| Name、文字列、テキスト | 文字列。1024 文字で切り詰め |
| 構造体 | 1 階層だけ展開したオブジェクト。それより深い構造体や、コンテナ要素としての構造体は `{"Type": "<型>"}` |
| 配列、Set、Map、固定長配列 | 先頭 32 要素を持つ `{"Value": [...], "TotalCount": N, "Truncated": bool}`。Map の要素は `[キー, 値]`、Set と Map は格納順 |
| オブジェクト・クラス・ソフト・ウィーク・レイジー・インターフェースの参照 | パスの文字列。空なら `"None"`。何も読み込みません |
| デリゲートなど対応しない型 | `{"Unsupported": "<型>"}` |

上限は感覚 64 個、感覚ごとに 64 KiB、合計 256 KiB です。自分の上限に達した感覚は収まった分を残して `Truncated: true` を返し、合計の上限を使い切った後の感覚は識別情報だけを持つ `Omitted: true` として書き出します。応答の `SenseCount` は書き出した感覚の数（`Omitted` のものを含む）で、`Truncated` はこれらの上限のどれかでダンプが切られたときに `true` です。

`DumpAIPerceptionState` も同じ設定を `Senses[]` に、より簡略な形で挙げます。エンジンが宣言したプロパティは値を示し（それを継承したプロジェクト独自の設定クラスでも同様）、プロジェクトが宣言したプロパティは `Name` と `Type` だけで `Value` キーを持ちません。その値は `DumpAIPerceptionSenseConfigs` で読んでください。

#### エラー

| ErrorCode | 発生条件 |
|---|---|
| `InvalidParams` | パラメータが欠けている・型が違う・範囲外・未知のキー。`Sense` が設定された感覚のどれにも一致しない、または複数に一致する。`TargetNetRole` / `TargetPIEInstance` を満たせない |
| `NotAllowed` | プレイワールドが動いていない（`PIE is not running.`）、または `TargetNetRole` / `TargetPIEInstance` に一致するものが無い |
| `NotFound` | 識別子に一致する Actor が無い。Actor とそれと対になるコントローラーまたは Pawn のどれも感知コンポーネントを持っていない（"The actor has no AI perception component, and neither does the controller or pawn it is paired with."）。`ExplainSightPerception` ではメッセージが `The observer actor could not be resolved.` または `The target actor could not be resolved.` で始まり、コンポーネントのメッセージは見る側の Actor を指します |
| `ExecutionFailed` | 識別子に一致する Actor が複数ある。artifact を書き出せなかった |
| `CapabilityNotAvailable` | `RuntimeInspect`、または `DumpAIPerceptionSenseConfigs` の場合は `AIPerceptionConfigDump` が付与されていない |
| `PolicyViolation` | Capability が安全ポリシーで拒否されている |

観測したワールドがクライアントの場合、ワールドを見つけた後のエラーメッセージの末尾に、AI はサーバーにしかないことと、`TargetPIEInstance` で再実行する先のサーバー側プレイワールドが付きます。

成功した呼び出しは JSON の artifact をちょうど 1 つ保存し、失敗した呼び出しは何も保存しません。

### BehaviorTree と Blackboard の観測

AI が実行している BehaviorTree と、それが読む Blackboard を観測します。どのノードがアクティブか、どの Decorator が通るか、Blackboard が何を持っているか、ツリーが時間とともにどう動いたかが分かります。8 つのうち 7 つは読むだけです。`DescribeBehaviorTreeWithProjectCode` だけは例外で、プロジェクトのコードを実行するため、下で別に説明します。コマンドは、プレイワールドの 1 つのアクターを対象にし（検証しているのは PIE で、`-game` 起動とパッケージ版は未検証）、[`TargetNetRole` / `TargetPIEInstance`](#実行時コマンドの対象プレイワールドを指定する) を受け付けます。ただし `GetBehaviorTreeEventLog` と `StopBehaviorTreeCapture` は `CaptureId` を受け取り、プレイワールドを解決しないので、プレイセッションの終了後も使えます。アクターは `ActorIdentifier` に、AI コントローラー・その Pawn・コンポーネントを持つ任意のアクターのラベルまたはオブジェクト名で指定します。名前が分からないときは `ListBehaviorTreeAgents` が使うべき名前を返します。

**Capability。** 8 つすべてが `RuntimeInspect`（DefaultAllow）を必要とします。`GetBlackboardValues` は、Blackboard の値がプロジェクトのデータであるため、`BlackboardValueRead`（DefaultDenied）も必要です。`DescribeBehaviorTreeWithProjectCode` はさらに `AIBehaviorProjectCodeExecution`（DefaultDenied）も必要です。足りない場合は `CapabilityNotAvailable` です。詳細は [安全性と Capability](safety.md#runtime-ai-のビヘイビアツリーと-blackboard) を参照してください。

**デモ版。** `DescribeBehaviorTreeWithProjectCode` と Capability `AIBehaviorProjectCodeExecution` はデモバイナリに含まれません。コマンドは存在せず `CommandNotFound` を返します。残りの 7 コマンドは含まれます。`BlackboardValueRead` はデモにも登録されていますが、デモの ini はこれを付与しないため、値を読むには利用者自身の ini 追記が要ります。製品版の応答が、省いた説明を読むのに必要な許可として `AIBehaviorProjectCodeExecution` を挙げる箇所で、デモ版は代わりに `NotInThisEdition` を返します。

#### 現在の状態（3）— `RuntimeInspect` が必要

| コマンド | 説明 |
|---|---|
| 🆓 `ListBehaviorTreeAgents` | 対象のプレイワールドで BehaviorTree を実行しているアクターを、それぞれの BehaviorTree コンポーネントと、ツリーが一時停止中かどうかとともに列挙します。一時停止中のツリーは含まれ、停止済みのツリーや一度も開始されていないツリーは含まれません。`MaxEntries` は 1〜4096（既定 256）。応答には `AgentCount`・`AgentsTotalCount`・`AgentsTruncated` が入り、artifact に全件が入ります。クライアント側のプレイワールドのように AI システムが無いワールドでは空の一覧を返します。エンジンの状態が更新の途中かもしれない間（モーダルダイアログや長い処理がゲームループを止めている、またはワールドが Tick の途中）は何も読まず、`Availability` は `NotAtSafePoint` です。返った名前を、ほかのコマンドの `ActorIdentifier` に使います |
| 🆓 `GetActiveBehaviorTreeNode` | 1 つのアクターの BehaviorTree のアクティブなノードと、そこからルートまでの経路を、`IsRunning` と `IsPaused` とともに返します。`DumpBehaviorTreeState` の軽量版で、説明も判定も Blackboard も読まず、返しません。応答と artifact は同じ結果を持ちます |
| 🆓 `DumpBehaviorTreeState` | 既定の観測が答えてよい範囲の、1 つのアクターの BehaviorTree の全体像。`IsRunning`・`IsPaused`・`IsRestartPending`・`IsAbortPending`、ツリーインスタンスのスタック（サブツリーは別のインスタンス）— 各インスタンスの `TreeAsset`、アクティブなノードとルートまでの経路、`ActiveNodeType`（`Composite`・`ActiveTask`・`AbortingTask`・`InactiveTask`）、有効な補助ノード（Decorator と Service）、並列タスクとその `Status` — を返します。Blackboard のキー定義は、Blackboard に届く限り、ツリーが動いていなくても返ります。各ノードは `InstanceIndex`・`TreeAsset`・`ExecutionIndex`・`NodeName`・`ClassPath`・`NodeRole` を持ちます。既定の観測で説明してよいノードには `StaticDescription` と `RuntimeDescription` を付け、アクティブノードからルートまでの経路上の Decorator と有効な補助 Decorator には `Verdict`（`Passed`・`Failed`・`Unknown`）を付けます。それ以外のノードには、省いた理由（`DescriptionOmittedReason` / `VerdictUnknownReason`）と、それを出せる Capability（`RequiresCapabilities[]`）を返します — [既定の観測が省くもの](#既定の観測が省くもの) を参照してください。`MaxEntries`（1〜4096、既定 256）が説明するノード数の上限です。応答には各一覧の先頭の項目が入り、artifact に全件が入ります。ツリーが開始されていない（`Availability: NotRunning`）、またはエンジンの状態が更新の途中かもしれず読まなかった（`NotAtSafePoint`）場合は、エラーではなく縮退した結果を返します |

#### Blackboard の値（1）— `RuntimeInspect` と `BlackboardValueRead` が必要

| コマンド | 説明 |
|---|---|
| 🆓 `GetBlackboardValues` | 1 つのアクターの Blackboard の全キーの値と、実行中のノードのうち Blackboard の値を表示する説明文の全文を返します。標準のキー型は型付きの値で返ります（`Bool`・`Int`・`Float`・`Name`・`String`・`Vector`・`Rotator`・`Enum`・`NativeEnum`・`Object`・`Class`・`Struct`）。`Object` / `Class` キーは、空の参照（`Empty`）、生きている参照（`Live`）、破棄済みの参照（`Destroyed`）を区別します。`Struct` キーは、構造体の書き出し関数を呼ばず、決まった上限の中でフィールドごとに書き出します。プロジェクトが定義した型のキーは型名だけを返し、`RequiresCapabilities: ["AIBehaviorProjectCodeExecution"]` を付けます（デモ版は `NotInThisEdition`）。ここで説明文を作れないノードは、理由と、それを出せる Capability とともに列挙します。`MaxEntries`（1〜4096、既定 256）がキー数の上限です。Blackboard アセットが未設定の Blackboard コンポーネントは、キー無しと `BlackboardAvailability: NoAsset` を返します。Blackboard コンポーネントが無いアクターは `NotFound` です。[Blackboard の値の読み方](#blackboard-の値の読み方) を参照してください |

#### プロジェクトのコード（1）— `RuntimeInspect`・`BlackboardValueRead`・`AIBehaviorProjectCodeExecution` が必要

デモ版には含まれません。

| コマンド | 説明 |
|---|---|
| `DescribeBehaviorTreeWithProjectCode` | 他のコマンドが、作るのにプロジェクトのコードを実行するため省いたものを、1 つのアクターについて説明します。プロジェクトのノードと Blueprint ノードの静的・実行時の説明、プロジェクトのコードに届くエンジンの Decorator の判定、プロジェクトが派生させた BehaviorTree コンポーネントクラスの実行時の説明と判定、プロジェクトが定義した型の Blackboard キーの値です。これらのいずれかが当てはまる実行中のノードだけを列挙します。裏にあるエンジンのコードを確かめていないため、どのコマンドも作らない出力は、呼ばずに理由（`EngineCallNotVerified`）とともに列挙します。`MaxEntries`（1〜4096、既定 256）が説明するノード数の上限で、上限を超えたノードは呼びません。⚠️ **プロジェクトのコードを実行するため、実行中にツリーが変わることがあります。** 呼び出しの前にそのつど、ツリーを確かめ直します。実行中でなくなったノードは省いて `NodeDeactivatedDuringProjectCode` で報告し、ツリーや Blackboard が変わった場合（ツリーが停止した、Blackboard アセットが差し替えられた、キーの型が変わった、アクターを指すキーの指す先が変わった）は `TreeChangedDuringProjectCode` で説明を打ち切り、それまでに作った結果を返します。Blackboard の値が書き換えられただけでは打ち切らず、以降の説明は書き換え後の値で作ります。読み取り専用ではありません。安全ポリシーの読み取り専用モードでは `PolicyViolation`、モーダルダイアログや長い処理がゲームループを止めている間は `NotAllowed` で拒否されます（運用者の starved tick 許可リストでその間も実行できるようにしていても、何も読まず `NotAtSafePoint` を返します）。BehaviorTree コンポーネントが無いアクターは `NotFound` です |

#### 記録（3）— `RuntimeInspect` が必要

記録は、開始したセッションのものです。ほかのセッションからはその ID が `NotFound` になり、存在するかどうかも分かりません。記録は、ワールドの Tick ごとに、全アクターの Tick が終わった後でツリーを 1 回読み、変化したものを保存します。Blackboard の値は記録しません。

| コマンド | 説明 |
|---|---|
| 🆓 `StartBehaviorTreeCapture` | 1 つのアクターの BehaviorTree が時間とともにどう変わるかを、呼び出したセッションが所有する記録として開始し、その `CaptureId` を返します。ツリーが停止中・未開始でも始められ、開始されたときにその開始が記録されます。`MaxDurationSeconds`（1〜600、既定 120）、`BufferCapacity`（64〜16384、既定 4096。古いものを捨てて数えるまでに保持するエントリ数）、`ReplaceExisting`（既定 `false`。同じコンポーネントの 2 本目の記録を拒否して最初のものを示す。`true` ならその記録を止めて新しく始める）。1 セッションが同時に記録できる BehaviorTree は 8 本、1 ワールドの記録中の capture は全セッション合計で 32 本までで、停止した capture は 30 分保持されます。最初のエントリは開始時点の状態を表す `Baseline` です。その時点でエンジンの状態が更新の途中かもしれない場合も記録は始まり、Baseline はゲームが進んだ後の最初の読み取りで取られ、応答は `BaselinePending: true` を返します。記録は、`MaxDurationSeconds` に達したとき、プレイセッションが終わったとき、コンポーネントが破棄されたときに自動で止まります。アクターに BehaviorTree コンポーネントが無ければ `NotFound` です |
| 🆓 `GetBehaviorTreeEventLog` | capture のエントリを、古いものから、`SinceSequence`（既定 0）以降について読みます。`CaptureId`（必須）は `StartBehaviorTreeCapture` が返した ID です。`MaxEntries` は 1〜4096（既定 256）。応答には読んだ分の先頭 50 件が入り、artifact にはその読み取りの全エントリが入ります。`NextSequence` は artifact の最後のエントリの続きを読むための `SinceSequence` です。`SinceSequence` 以降のエントリが読まれる前に捨てられた場合は `bGap` が true になり、`DroppedCount` は capture の容量、または 1 回のツリー読み取りが生むエントリ数の上限のために捨てられた件数を数えます。応答には capture の `State`、停止した理由（`EndReason`）、`OldestAvailableSequence`、`BaselinePending`、`RecordingSeconds`、`Limitations[]` も入ります。プレイセッションの終了後も使えます。未知・期限切れ・他人の `CaptureId` は、どれなのかを明かさず `NotFound` です |
| 🆓 `StopBehaviorTreeCapture` | capture を止め、その最終状態 — 止まった理由、Baseline が取れたか、記録時間、連番の管理 — を返します。すでに止まっている capture の停止は成功し、最初の終了理由（`Stopped`・`DurationLimit`・`WorldTornDown`・`Replaced`・`TargetDestroyed`）を保ちます。プレイセッションの終了後も使えます。1 セッションが保持する停止済み capture は最大 4 本で、古いものから捨てられます。未知・期限切れ・他人の `CaptureId` は、どれなのかを明かさず `NotFound` です |

#### 既定の観測が省くもの

`DumpBehaviorTreeState` と記録は、安全だと確かめられたノードだけを説明します。ノードのクラスがプラグインの確認済みのもので、参照する Blackboard キーがすべて標準の型であることが条件です。それ以外のノードは、説明が空、判定は `Unknown` になり、応答に理由と、それを出せる許可が入ります。

| 理由（`DescriptionOmittedReason` / `VerdictUnknownReason`） | 意味 | 読む方法 |
|---|---|---|
| `BlackboardValueReadRequired` | 説明が Blackboard の値を表示してしまう — キーの値を表示するエンジンのノードや、Blackboard キーに結び付けたパラメータ（残り時間などが値から導かれる） | `GetBlackboardValues`（`BlackboardValueRead` が必要） |
| `ProjectCodeExecutionRequired` | 作るのにプロジェクトのコードを実行する — プロジェクトや Blueprint が定義したノード、プロジェクトが定義した型・構造体・列挙型のキーを参照するノード、判定がプロジェクト側のオブジェクトを呼ぶエンジンの Decorator（たとえば Blackboard キーが指すアクターのゲームプレイタグを調べるもの） | `DescribeBehaviorTreeWithProjectCode`（`AIBehaviorProjectCodeExecution` が必要） |
| `ProjectDerivedComponent` | プロジェクトが派生させた BehaviorTree コンポーネントクラスで動いていて、その実行時の説明と判定をエンジンのものと同じとは扱えない | `DescribeBehaviorTreeWithProjectCode` |
| `EngineCallNotVerified` | 説明や判定を呼んで安全か確かめていない、または安全でないと分かっているエンジンのノード（たとえばループ Decorator の実行時の説明）。どのコマンドも呼ばない | なし |
| `NodeMemoryUnavailable` | ノードが実行中のツリーのために持つメモリに届かなかったため、そのノードに問い合わせなかった | なし |

Blackboard キーに結び付いたノードでも、キーの型を確かめられない場合 — BehaviorTree コンポーネントに Blackboard アセットが無い、キーがアセットに無い、ノードが期待する型がキーの型と食い違う — は、許可を与えても読めるようにならないため、許可の理由ではなく `EngineCallNotVerified` になります。デモ版では `RequiresCapabilities` に `AIBehaviorProjectCodeExecution` は現れず、`NotInThisEdition` になります。

#### Blackboard の値の読み方

- **キー定義の `IsSet`**（`DumpBehaviorTreeState`・`GetBlackboardValues`）は、`Vector`・`Rotator`・`Object`・`Class` のキーでは `true` / `false`、それ以外の型では `null`（不明）です。ゼロや空の値と未設定を区別できないためです。`Object` / `Class` では、破棄済みのオブジェクトを指す参照も未設定として数えます。`GetBlackboardValues` は、空の参照と破棄済みの参照を区別して返します。`Limitations` の `IsSetNotDeterminable` がこれを示します。
- **構造体のキー**は、フィールドごとに書き出します。入れ子の構造体はさらに 1 段だけ展開し、それより深いものは型名で書きます。構造体の中の、実行時に種類が決まる構造体（インスタンス化された構造体やプロパティバッグ）は展開せず、`NestedInstancedStructNotExpanded` が示します。
- **列挙型のキー**は、数値と列挙子の名前を返します。Blueprint で定義した列挙型では、名前はエディタで付けた表示名ではなく内部名です（`UserDefinedEnumNamesAreInternal`）。エンジンで非推奨のネイティブ列挙型キーは値の領域を持たないため、値の代わりに `ValueOmittedReason` で読めない理由を返します。
- **上限。** 構造体キーの中のコンテナは先頭 32 要素まで、文字列は 1024 文字で切り、1 つのキーの値は 64 KiB、1 回の応答は 256 KiB までです。収まらないものは切るか省き、その旨の印を付けます。参照はパスとして書き、たどりません。
- **アセットが無い Blackboard コンポーネント**は、キー無しの `BlackboardAvailability: NoAsset` を返します。**Blackboard コンポーネントが無い**場合、`DumpBehaviorTreeState` は `NoComponent`、`GetBlackboardValues` は `NotFound` です。

#### 実行時のノードをエディタのアセットと突き合わせる

実行時の応答のノードは、`TreeAsset` と `ExecutionIndex` の組で識別されます。同じ番号を Editor コマンドの `GetBehaviorTreeNodeList` と `GetBehaviorTreeSubtree`（[`UAIP.Editor.BehaviorTree`](#uaipeditorbehaviortree)）が、そのアセットをトップレベルのツリーとして実行したときの番号として、PIE を開かず、アセットを保存せずに返します。実行時の組をそこで探せば、アセット上のノードが分かります。`GetBehaviorTreeNodeProperties` に出る番号は別の値で、突き合わせには使えません。

番号を付けられないノードは `ExecutionIndex: null` と `ExecutionIndexUnavailableReason` を返します。理由は次のどれかです。

| `ExecutionIndexUnavailableReason` | 意味 |
|---|---|
| `ContextDependentInjectedDecorator` | アセットの根に付いた Decorator。別のツリーから呼ばれたときにだけ働き、番号は呼ぶ側のツリーで決まるので、呼ぶ側のアセットで探します |
| `NotInCompiledTree` | グラフにはあるが、アセットが実行するツリーにはまだ入っていないノード（追加した直後など） |

#### BehaviorTree の応答に共通のフィールド

| フィールド | 意味 |
|---|---|
| `CapturedAt`・`Frame`・`NetMode`・`WorldContext`・`PIEInstance`・`WorldTimeSeconds` | 状態をいつ・どこで読んだか: ISO 8601 の UTC 時刻、エンジンのフレーム番号、ネットモードとワールドコンテキスト、PIE インスタンス（PIE 外では省略）、ワールドの時間 |
| `Actor`・`Component` | 観測したアクターと BehaviorTree コンポーネント |
| `Availability` | `Running`、`NotRunning`（ツリーが未開始、または停止済み。インスタンスとノードは空、Blackboard のキー定義は返る）、`NotAtSafePoint`（エンジンの状態が更新の途中かもしれず、何も読まなかった。ダイアログや読み込みが終わってから呼び直す）。一時停止中のツリーは `IsPaused: true` の `Running` です。`AvailabilityReason` に理由が文章で入ります |
| `BlackboardAvailability` | `Available`・`NoAsset`・`NoComponent`・`NotAtSafePoint` |
| `Limitations[]` | 返した内容についての注意。`Code` と、場合によって `Detail` を持つ |

`Limitations[].Code` は次のいずれかです。

| `Code` | 意味 |
|---|---|
| `InstanceWithoutTasksNotVisible` | タスクを 1 つも含まないツリーインスタンス（サブツリーの段）は見えない。検出できたときに報告され、検出できない並び方もある |
| `SubTickTransitionsNotVisible` | 記録は Tick ごとに 1 回ツリーを読むので、1 フレームの中でツリーが何度も動いても最後の状態しか見えない |
| `ReasonNotRecorded` | 記録は何が変わったかを残すが、なぜ変わったかは残さない |
| `NotPolledWhileWorldPaused` | ゲームの一時停止中は記録を読まない。その間の変化は再開後にまとめて現れる |
| `BaselineNotTaken` | 最初の読み取りの前に記録が止まったため、`Baseline` エントリが無い |
| `NodeDeactivatedDuringProjectCode` | プロジェクトのコードの実行中に実行中でなくなったノードを、`DescribeBehaviorTreeWithProjectCode` が省いた |
| `TreeChangedDuringProjectCode` | プロジェクトのコードがツリーや Blackboard を変えたため、`DescribeBehaviorTreeWithProjectCode` が打ち切った。応答にはそれまでの結果が入る |
| `NotAtSafePoint` | エンジンの状態が更新の途中かもしれなかったため、読まなかった |
| `NestedInstancedStructNotExpanded` | 構造体の値の中の、実行時に種類が決まる構造体は展開されない |
| `IsSetNotDeterminable` | 未設定とゼロ値を区別できないキー型では `IsSet` が `null` |
| `UserDefinedEnumNamesAreInternal` | Blueprint で定義した列挙型の列挙子の名前は内部名 |

記録のエントリは `Sequence`・フレーム・時刻と `Kind` を持ちます。`Kind` は `Baseline`・`TreeStarted`・`TreeStopped`・`Paused`・`Resumed`・`InstancePushed`・`InstancePopped`・`ActiveNodeChanged`・`ActiveNodeTypeChanged`・`AuxNodeActivated`・`AuxNodeDeactivated`・`ParallelTaskChanged`・`RestartPendingChanged`・`AbortPendingChanged` です。`Baseline` エントリはツリーの状態を `Snapshot` に持ち、開始時ではなく開始後の最初の読み取りで取った `Baseline` には `Deferred` が付きます。

#### エラー

| ErrorCode | 発生条件 |
|---|---|
| `InvalidParams` | パラメータが欠けている・型が違う・範囲外・未知のキー。`TargetNetRole` / `TargetPIEInstance` を満たせない。範囲外の記録時間・容量・上限は丸めずに拒否 |
| `NotAllowed` | プレイワールドが動いていない（`PIE is not running.`）、または `TargetNetRole` / `TargetPIEInstance` に一致するものが無い。記録の上限（セッション単位・ワールド単位）に達した、またはコンポーネントがすでに記録中で `ReplaceExisting` が無い。モーダルダイアログや長い処理がゲームループを止めている間の `DescribeBehaviorTreeWithProjectCode` |
| `NotFound` | 識別子に一致するアクターが無い（クライアント側のワールドでは、サーバー側の候補をメッセージに添える）。アクターとそれと対になるコントローラーまたは Pawn のどれも BehaviorTree / Blackboard コンポーネントを持っていない。未知・期限切れ・形式不正・他人の `CaptureId` |
| `ExecutionFailed` | 識別子に一致するアクターが複数ある。artifact を書き出せなかった（`StartBehaviorTreeCapture` と `StopBehaviorTreeCapture` では、保存先そのものを解決できない場合に限る） |
| `CapabilityNotAvailable` | `RuntimeInspect`・`BlackboardValueRead`・`AIBehaviorProjectCodeExecution` のいずれかが付与されていない。メッセージに足りないものの名前が入る |
| `PolicyViolation` | 必要な Capability が安全ポリシーで拒否されている、または `DescribeBehaviorTreeWithProjectCode` を読み取り専用モードで呼んだ |

成功した呼び出しは JSON の artifact をちょうど 1 つ保存します（記録の `StartBehaviorTreeCapture` と `StopBehaviorTreeCapture` は補助の artifact を保存します）。失敗した呼び出しは何も保存しません。

---

## UAIP.Runtime.StateTree 🧩

AI が実行している StateTree を観測するコマンド群です。どの状態がアクティブか、どのタスクが動いているか、どの遅延遷移が待っているか、ツリーが時間とともにどう動いたか、そして許可すれば保持している値が分かります。`StateTree` と `GameplayStateTree` の両プラグインが必要です。どちらかが無効だとコマンドは登録されず、呼ぶとプラグイン名を添えた `CommandNotFound` を返します（状態は `UAIP.Core.ListIntegrations` で分かります）。デモ版には含まれません。どのコマンドも読むだけです。コマンドは、プレイワールドのアクターの `UStateTreeComponent` 系（`UStateTreeAIComponent` を含む）を対象にし、[`TargetNetRole` / `TargetPIEInstance`](#実行時コマンドの対象プレイワールドを指定する) を受け付けます。ただし `GetStateTreeEventLog` と `StopStateTreeCapture` は `CaptureId` を受け取り、プレイワールドを解決しないので、プレイセッションの終了後も使えます。

**Capability。** 7 つすべてが `RuntimeInspect`（DefaultAllow）を必要とします。`DumpStateTreeInstanceData` は、ツリーのパラメータやノードの値がプロジェクトのデータであるため、`StateTreeInstanceDataDump`（DefaultDenied）も必要です。足りない場合は `CapabilityNotAvailable` です。詳細は [安全性と Capability](safety.md#runtime-statetree-の観測) を参照してください。

**コンポーネントの探し方。** `ActorIdentifier` はアクターのラベルまたはオブジェクト名です。コンポーネントはまずそのアクターから探し、無ければ、Pawn なら AI コントローラーから、AI コントローラーならその Pawn から探します（`UStateTreeAIComponent` は AI コントローラーに、`UStateTreeComponent` は Pawn に付くことが多いためです）。複数見つかった場合は `ComponentName`（コンポーネントのオブジェクト名）で 1 つを選ぶ必要があります。省略すると `InvalidParams` で失敗して候補を列挙し、どの候補にも一致しない名前は候補付きの `NotFound` です。`ListStateTreeComponents` が使うべき名前を返します。

**プロジェクトが派生させたコンポーネントクラスは読みません。** そのクラスがエンジンのコンポーネントと同じ方法でツリーを動かしているかを確かめる手段がエンジンに無く、誤って読むとエンジン自身の検証機能を止めてしまうためです。観測のコマンドは読まずに成功し、その旨を返します（`Availability: ProjectDerivedComponent` と、`Limitations` の `ProjectDerivedComponentNotVerified`）。`ListStateTreeComponents` は `RunStatus: null` と理由付きでそれを列挙します。`StartStateTreeCapture` は記録を始められますが、そのクラスが別の Owner や Tree の組でツリーを動かしていると何も記録されません。

#### 現在の状態（3）— `RuntimeInspect` が必要

| コマンド | 説明 |
|---|---|
| `ListStateTreeComponents` 🧩 | 対象のプレイワールドのアクターの StateTree コンポーネントを、アクター・コンポーネント・クラス・実行するよう設定されたツリーアセット・`RunStatus` とともに列挙します。読まないコンポーネント（プロジェクトが派生させたクラス、リンクされていないツリー）の実行状態は `null` で、`RunStatusUnavailableReason` が付きます。`MaxEntries` は 1〜4096（既定 256）。応答には先頭のコンポーネントが入り、artifact に全件が入ります。エンジンの状態が更新の途中かもしれない間（モーダルダイアログや長い処理がゲームループを止めている、またはワールドが Tick の途中）はアクターを走査せず、一覧も返さず、`Availability` は `NotAtSafePoint` です |
| `GetActiveStateTreeState` 🧩 | 1 つのコンポーネントの StateTree のアクティブな状態を返します。`RunStatus` と、アクティブなフレームスタックのフレームごとに、ツリーアセットとルートから各アクティブ状態までの経路です。`DumpStateTreeState` の軽量版で、タスク・遅延遷移・次の Tick は含みません。応答と artifact は同じ内容です |
| `DumpStateTreeState` 🧩 | 1 つのコンポーネントの StateTree の全体像。`RunStatus`（`Running`・`Stopped`・`Succeeded`・`Failed`・`Unset`）と `LastTickStatus`、アクティブなフレームスタックの `Frames[]`（各フレームのツリーアセットと、アクティブな状態の名前・タグ・`StateType`（`State`・`Group`・`Linked`・`LinkedAsset`・`Subtree`）・経路）、アクティブな状態のタスクとその `Status`、待機中の遅延遷移（遷移先の状態と `RemainingSeconds`）、`NextScheduledTickSeconds` を返します。応答には先頭のフレームが入り、artifact に全件が入ります。ツリーが開始されていない、コンポーネントにツリーが無い・実行の準備ができていない、プロジェクトが派生させたクラスである、またはエンジンの状態が更新の途中かもしれず読まなかった場合は、エラーではなく縮退した結果を返します |

#### インスタンスデータ（1）— `RuntimeInspect` と `StateTreeInstanceDataDump` が必要

| コマンド | 説明 |
|---|---|
| `DumpStateTreeInstanceData` 🧩 | 1 つのコンポーネントが持つ値 — ツリーのパラメータ、各アクティブな状態のパラメータ、各アクティブなノードのインスタンスデータ — を、値を持つプロパティのブロック（`Blocks[]`。それぞれ `BlockKind` を持つ）として返します。値はリフレクションで読み、ノードやその他のプロジェクトの型の関数は実行しません。構造体は 1 段展開し、配列・セット・マップは先頭の要素を残し、長い文字列は切り、バイト予算に収まらない値は切るか省きます（`bOmitted`）。切ったものは元の件数とともに報告します。構造体の中の、実行時に種類が決まる構造体は展開しません（`NestedInstancedStructNotExpanded`）。`MaxEntries`（1〜4096、既定 256）がブロック数の上限です。応答には先頭のブロックが入り、artifact に全件が入ります。縮退の仕方は `DumpStateTreeState` と同じです。出てくるものについては [安全性と Capability](safety.md#runtime-statetree-の観測) を参照してください |

#### 記録（3）— `RuntimeInspect` が必要

記録は、開始したセッションのものです。ほかのセッションからはその ID が `NotFound` になり、存在するかどうかも分かりません。

| コマンド | 説明 |
|---|---|
| `StartStateTreeCapture` 🧩 | 1 つのコンポーネントの StateTree が時間とともに何をするかを、呼び出したセッションが所有する記録として開始し、その `CaptureId` を返します。記録はエンジンの StateTree のデバッグ通知から作られます。`Kinds` で記録するエントリの種類を絞れます（既定は全種類。空の一覧や未知の種類は `InvalidParams`）。種類は `StateEntered`・`StateExited`・`StateCompleted`・`StateSelected`・`Transition`・`EventSent` です。`MaxDurationSeconds`（1〜600、既定 120）、`BufferCapacity`（64〜16384、既定 4096）、`ReplaceExisting`（既定 `false`）は `StartBehaviorTreeCapture` と同じです。1 セッションが同時に記録できる StateTree コンポーネントは 8 本、1 ワールドの記録中の capture は全セッション合計で 32 本までで、停止した capture は 30 分保持されます。未開始のツリーや、インスタンスデータが未初期化のツリーも記録でき、開始された後の動きが記録されます。記録は、`MaxDurationSeconds` に達したとき、プレイセッションが終わったとき、コンポーネントが破棄されたとき、コンポーネントが別のツリーを実行するよう設定されたとき（`TargetChanged`）に自動で止まります。**次の場合は `NotAllowed` で失敗します** — 安全な地点でない瞬間（ダイアログや読み込みが終わってから呼び直す）、コンポーネントに StateTree が設定されていないとき（設定してから開始し直す）、エンジンが StateTree のデバッグ通知を提供しない構成のビルド（開発用のエディタビルド（Development または DebugGame）を使う。ほかのコマンドは影響を受けない）。アクターに StateTree コンポーネントが無ければ `NotFound` です |
| `GetStateTreeEventLog` 🧩 | capture のエントリを、古いものから、`SinceSequence`（既定 0）以降について読みます。`CaptureId`（必須）は `StartStateTreeCapture` が返した ID です。`MaxEntries` は 1〜4096（既定 256）。応答には読んだ分の先頭 50 件が入り、artifact にはその読み取りの全エントリが入ります。`NextSequence` は artifact の最後のエントリの続きを読むための `SinceSequence` です。`bGap` と `DroppedCount` は `GetBehaviorTreeEventLog` と同じです。応答には capture の状態、停止した理由、記録時間、`Limitations[]` も入ります。プレイセッションの終了後や、エンジンがデバッグ通知を提供しない構成のビルドでも使えます。未知・期限切れ・他人の `CaptureId` は、どれなのかを明かさず `NotFound` です |
| `StopStateTreeCapture` 🧩 | capture を止め、その最終状態 — 止まった理由、記録時間、連番の管理 — を返します。すでに止まっている capture の停止は成功し、最初の終了理由（`Stopped`・`DurationLimit`・`WorldTornDown`・`Replaced`・`TargetDestroyed`・`TargetChanged`）を保ちます。プレイセッションの終了後も使えます。1 セッションが保持する停止済み capture は最大 4 本で、古いものから捨てられます。未知・期限切れ・他人の `CaptureId` は、どれなのかを明かさず `NotFound` です |

エントリの種類の意味。名前から受ける印象と違うものがあります。

| `Kind` | 意味 |
|---|---|
| `StateEntered` / `StateExited` | 状態に入った・出た。同じ状態が選び直されて実際には何も変わらないときにも記録される |
| `StateCompleted` | 状態が完了した。1 回の完了で、アクティブな経路上のすべての状態について記録される |
| `StateSelected` | 状態が選ばれた。選択を試みた時点の通知で、その選択が後で取り消されることがある。状態の名前は、選ばれた状態が属するフレームのツリーから引く。そのツリーを確実に特定できないとき、または記録が登録していないリンク先アセットのときは、名前を付けず状態の番号だけを記録する |
| `Transition` | 遷移が起きた: 遷移元の状態（分かる場合。`SourceState`）、遷移先の状態、きっかけの種類 `Trigger`（`OnStateCompleted`・`OnStateSucceeded`・`OnStateFailed`・`OnTick`・`OnEvent`・`OnDelegate`）、遷移が待つよう設定された `RequiredEventTag`、`Priority`、`DelaySeconds`、遷移の出どころ `SourceType`（`Asset`・`ExternalRequest`・`Internal`）。ツリーの開始・停止や強制的な遷移による状態の変化は遷移として記録されず、入った・出たのエントリだけが残る |
| `EventSent` | ツリーにイベントが送られた: `EventTag` と、中身の型名（`EventPayloadType`）。中身の値は記録しない |

状態に入ってからの経過時間はどこにも保持されていません。その状態の `StateEntered` エントリの時刻から計算してください。

#### StateTree の応答に共通のフィールド

| フィールド | 意味 |
|---|---|
| `CapturedAt`・`Frame`・`NetMode`・`WorldContext`・`PIEInstance`・`WorldTimeSeconds` | 状態をいつ・どこで読んだか。BehaviorTree のコマンドと同じ |
| `Actor`・`Component`・`TreeAssetPath` | 観測したアクター・StateTree コンポーネント・ツリーアセット |
| `Availability` | `Running`、`NotRunning`（ツリーが未開始）、`NoTree`（コンポーネントにツリーが無い）、`NotInitialized`（インスタンスデータが未初期化）、`Unreadable`（コンポーネントを読めなかった — 所有者がいない、破棄中、エンジンの更新で読み取りに必要な内部の項目が見つからない。`NotInitialized` とは別）、`ProjectDerivedComponent`、`NotAtSafePoint`。`AvailabilityReason` に理由が文章で入ります |
| `Limitations[]` | 返した内容についての注意。`Code` と、場合によって `Detail` を持つ |

`Limitations[].Code` は次のいずれかです。

| `Code` | 意味 |
|---|---|
| `ProjectDerivedComponentNotVerified` | コンポーネントクラスをプロジェクトが派生させている。観測では状態を読まなかった。記録では、そのクラスが別の Owner や Tree でツリーを動かしていると何も記録されないことがある |
| `NotAtSafePoint` | エンジンの状態が更新の途中かもしれなかったため、読まなかった |
| `EventSentMatchedByOwnerAndTree` | イベントは Owner と Tree だけで記録に結び付けるため、同じ Owner の上で同じツリーの別の実行（コンポーネントが複数ある、BehaviorTree のタスクの中で同じツリーが動いている）に送られたイベントも記録される |
| `TriggeringEventNotRecorded` | 遷移を実際に発火させたイベントは記録されない。遷移には、それが待つよう設定されたイベントだけが書かれる。直前の `EventSent` エントリが手がかりになる |
| `NestedInstancedStructNotExpanded` | 構造体の値の中の、実行時に種類が決まる構造体は展開されない |
| `TreeNotStarted` | ツリーが開始されていないので、報告する状態が無い |

StateTree の記録中は、プロセス内のすべての StateTree のデバッグ通知にわずかな処理が入るため、その分 StateTree の実行が遅れ、複数のスレッドで動く StateTree の通知は 1 本ずつ順に処理されます。必要なものだけを記録し、終わったら止めてください。

#### エラー

| ErrorCode | 発生条件 |
|---|---|
| `InvalidParams` | パラメータが欠けている・型が違う・範囲外・未知のキー。`Kinds` が空、または未知の種類を指している。アクターに StateTree コンポーネントが複数あるのに `ComponentName` が無い（候補を列挙する） |
| `NotAllowed` | プレイワールドが動いていない、または `TargetNetRole` / `TargetPIEInstance` に一致するものが無い。`StartStateTreeCapture` が、安全な地点でない瞬間・ツリーが無いコンポーネント・StateTree のデバッグ通知が無い構成のビルドで呼ばれた。記録の上限に達した、またはコンポーネントがすでに記録中で `ReplaceExisting` が無い |
| `NotFound` | 識別子に一致するアクターが無い。アクターとそれと対になるコントローラーまたは Pawn のどれも StateTree コンポーネントを持っていない。`ComponentName` がどの候補にも一致しない。未知・期限切れ・形式不正・他人の `CaptureId` |
| `ExecutionFailed` | 識別子に一致するアクターが複数ある。artifact を書き出せなかった |
| `CapabilityNotAvailable` | `RuntimeInspect`、または `DumpStateTreeInstanceData` の場合は `StateTreeInstanceDataDump` が付与されていない |
| `PolicyViolation` | 必要な Capability が安全ポリシーで拒否されている |

成功した呼び出しは JSON の artifact をちょうど 1 つ保存します（記録の `StartStateTreeCapture` と `StopStateTreeCapture` は補助の artifact を保存します）。失敗した呼び出しは何も保存しません。

---

## UAIP.Runtime.CommonUI 🧩

実行中のゲームの CommonUI の状態を観測します。活性化ウィジェットのコンテナ（スタックとキュー）とそれぞれが表示しているウィジェット、ローカルプレイヤーごとに CommonUI が持つ入力の状態（アクションルーターが適用している入力モード・最前面の活性化ウィジェット・フォーカス・入力の種類・バインドされたアクション）、アクションの表示テキストです。`CommonUI` プラグイン（と、CommonUI 自身が要求する `EnhancedInput`）が必要です。無効ならコマンドは登録されず、呼ぶとプラグイン名を示した `CommandNotFound` になります。状態は `UAIP.Core.ListIntegrations` が報告します。CommonUI なしでビルドした UAIP では、コマンドは一覧に出たまま `UnavailableDetail: OptionalPluginDisabled` で断ります。デモ版にはありません。4 つとも [`TargetNetRole` / `TargetPIEInstance`](#実行時コマンドの対象プレイワールドを指定する) を受け付け、未知のパラメータは拒否します。PIE でも `-game` やパッケージ版でも動きます。

**Capability。** 4 つとも `RuntimeInspect`（DefaultAllow）が必要です。`GetActionDisplayNames` は、テキストがゲームの表示するものなので、さらに `RuntimeWidgetTextRead`（DefaultDenied）が必要です — [ゲームビューポートの Widget](#ゲームビューポートの-ui-と-hud4) のテキストと同じ Capability です。`DescribeActivatableWidgetsWithProjectCode` は、さらに `CommonUIProjectCodeExecution`（DefaultDenied）が必要です。[安全性と Capability](safety.md#runtime-commonui-の観測) を参照してください。

**既定ではプロジェクトのコードを実行しません。** 最初の 3 つのコマンドは、プロジェクトが override しうる関数を呼びません。活性化ウィジェットの getter（そのウィジェットが求める入力設定とフォーカス先）は省き、どの応答も `ProjectCodeFields`（`Omitted`・`OmittedReason: "ProjectCodeExecutionRequired"`・`RequiresCapabilities: ["CommonUIProjectCodeExecution"]`・`Command`）でそれを示します。ルーターの判定は、プロジェクトがルーターを派生させていても CommonUI 自身の判定です。それでも、エンジンの 2 つの経路は virtual 関数を通じてプロジェクトのコードに届きえます。Widget のツリーの走査（子の列挙を override したプロジェクトの Widget）と、Slate の Widget を持つ活性化ウィジェットの検索（プロジェクト独自の Slate メタデータの型）です。override しうる getter を呼ぶのは `DescribeActivatableWidgetsWithProjectCode` だけです。

**`PlayerIndex` はローカルプレイヤーの番号です。** `GetInputState` と `GetActionDisplayNames` は、`PressGameViewportUIKey` と同じく、ゲームインスタンスの**ローカルプレイヤー**に番号を振ります（0 が最初）。`DumpInputState` と `EvaluateInputGateWithProjectCode` は、ワールドの**プレイヤーコントローラ**に番号を振ります。順序は、このマシンのローカルプレイヤーが先（ゲームのローカルプレイヤーの順）、ほかのプレイヤーが後（ゲームステートが挙げる順）で、どちらもいないときだけワールド自身のプレイヤーコントローラの一覧の順になります。負の番号は `InvalidParams`、どのローカルプレイヤーも持たない番号は `NotFound` で、メッセージが存在する番号を挙げます。省略すると全ローカルプレイヤーを読みます。

| コマンド | 説明 |
|---|---|
| `DumpActivatableStacks` 🧩 | コンテナごとに、種類と順序、所有するローカルプレイヤー（`OwningPlayerIndex`。分からなければ `null`）、Slate の Widget が構築済みか・ゲーム層にあるか、それを持つ活性化ウィジェット（`ParentActivatable`）、表示しているウィジェット（`ActiveWidget`・`ActiveWidgetIsActivated`）、2 つのウィジェットの切り替えの途中か（`IsTransitioning`。切り替えの前半では `ActiveWidgetIsOutgoing` も）、スタックの RootContent、追加された順のエントリ（`IsDisplayed`・`IsActivated`・`IsModal`・`SupportsActivationFocus`・`AutoRestoresFocus`・`IsBackHandler`・`AutoActivate`）を返します。どのコンテナにも入っていない活性化ウィジェットは `UncontainedActivatedWidgets` に入ります。除いたウィジェットとコンテナは、理由ごとに `ExcludedCounts` で数えます（`PendingKill`・`DesignTime`・`NoWorld`・`OtherWorld`、まだ構築されていないコンテナは `Unconstructed`）。`IncludeUnconstructed`（既定 `false`）を渡すと、それらのコンテナも列挙します。上限: コンテナ 64、コンテナあたりのエントリ 256（表示中のエントリは必ず残す）、コンテナに入っていないウィジェット 64。`Result` は件数・`ExcludedCounts`・`Limitations` と、最初の 16 コンテナが表示しているウィジェットです |
| `GetInputState` 🧩 | ローカルプレイヤーごとに、アクションルーターのクラス（`RouterClass`・`RouterIsEngineBaseClass`）、適用している入力モード（`InputMode`: `Menu`・`Game`・`All`・`NotApplied`）、適用しているマウスキャプチャ、活性化ウィジェットのツリーを組み直している最中か、`RouterAllowsGameInput` と判定に使った値（`GameInputDecisionEvidence`）、CommonUI が最前面として扱う活性化ウィジェット（`Leafmost`。UE 5.8 以降）、Slate ユーザーの実際のフォーカス（`Focus`）とそれが `Leafmost` の中にあるか、入力の種類（`InputType`・`RawInputType`・`GamepadName`・`IsUsingPointerInput`）、プレイヤーコントローラが無視しているもの・表示しているものを返します。ワールドに 1 つ: ゲームビューポートの入力の状態（`ViewportState`）、そのクラス、CommonUI のゲームビューポートクライアントの派生か、確かめたエンジンのクラスか、CommonUI の判定が[注入ゲート](#注入ゲート)に差し込まれているか（`GameInputGateContributorInstalled`）。`IncludeActions`（既定 `false`）を渡すと、プレイヤーごとにバインドされたアクション（名前・識別子・入力イベント・入力モード・キー・バインド先の Widget）を、表示テキスト抜きで加えます。上限: プレイヤーあたりのアクション 128、アクションあたりのキー 8（通常のキーと長押しのキーで別々に数える）。`Result` は各プレイヤーの番号・状態・入力モード・`RouterAllowsGameInput`・`Leafmost` のパスと、`ViewportClientIsCommonUIBased`・`Limitations` です |
| `GetActionDisplayNames` 🧩 | バインドされたアクションの表示テキストです。アクションごとに、出どころの違う 3 つのテキストを返します: `ActionDisplayName`（バインドが持つ表示名）、`LegacyRowDisplayName`（アクションを定義する DataTable の行の表示名）、`InputActionDescription`（アクションを定義する Enhanced Input のアクションの説明）。無い出どころは `null` です。画面がどれを表示するかはゲーム次第なので、コマンドは選びません。プロジェクトがクラスを派生させた DataTable の行は読みません（`LegacyRowNotReadFromProjectDataTable`）。`ActionName`・`ActionIdentifier`・`InputEvent`・`InputMode`・`BoundWidget.WidgetPath` の組で、`GetInputState` の `Actions` の同じアクションと突き合わせられます。2 つのコマンドは別の時点で読むので、片方にだけアクションが出ることがあります。アクションルーターの無いプレイヤーは `Status: "Unavailable"` です。テキストは artifact にだけ書きます。`Result` は各プレイヤーの番号・状態・アクションの数と、limitation です。`RuntimeWidgetTextRead` が必要です |
| `DescribeActivatableWidgetsWithProjectCode` 🧩 | **プロジェクトのコードを実行します。** 活性化ウィジェットが override しうる getter を呼び、`DesiredInputConfig`（`InputMode`・`MouseCaptureMode`・`MouseLockMode`・`HideCursorDuringViewportCapture`・`IgnoreMoveInput`・`IgnoreLookInput`。何も求めていなければ `null`）と `DesiredFocusTarget`（指していなければ `null`。破棄中や別のワールドの Widget なら省いて `DesiredFocusTargetExcludedReason` を付ける）を返します。`WidgetPaths` は `DumpActivatableStacks` が返す `WidgetPath` でウィジェットを指定します。1〜32 件で、各要素は `/` で始まり、単一引用符と制御文字を含まず、1023 文字以下の完全なオブジェクトパスです（外れれば要求全体が `InvalidParams`）。重複はそのまま保ち、指定したウィジェットは活性化していなくても評価します。省略するとワールドの活性化ウィジェットをすべて評価します（ゲーム層のものが先）。各対象には `Status` が付きます: `Evaluated`、`NotEvaluated`（その前でコマンドが止まった）、`NotFound`、`Excluded` と `ExcludedReason`（`PendingKill`・`DesignTime`・`NoWorld`・`OtherWorld`）。呼び出しの前後ごとにワールドとウィジェットを確かめ直します。活性化が外れただけのウィジェットは `DeactivatedDuringProjectCode` を付けて評価を続けます。ワールドかウィジェットが変わればコマンドは止まり、そこまでに評価した結果で成功を返します。`StoppedAt` がウィジェットと getter を示し、`Limitations` に `ScreenChangedDuringProjectCode`（または `NotAtSafePoint`）が入ります。上限: 対象 32。読み取り専用のコマンドではないので、安全設定の読み取り専用モードでは拒否されます。`CommonUIProjectCodeExecution` が必要です。デモ版にはありません |

#### CommonUI のすべての応答に付く欄

| 欄 | 意味 |
|---|---|
| `CapturedAt`・`Frame`・`NetMode`・`WorldContext`・`PIEInstance` | 状態を読んだ時点と場所 |
| `Availability` | エンジンの状態が更新の途中かもしれないとき（モーダルダイアログや長い処理がゲームループを止めている、またはワールドが tick の途中）は `NotAtSafePoint`。何も読まず、成功して一覧を返しません。呼び直してください |
| `WidgetPath` | すべてのウィジェットに付きます。`FindGameViewportWidgets` に `WithinWidgetPath` として渡すと、そのウィジェットの中を探せます |
| `TypePath`・`Fingerprint` | ゲーム層にある構築済みのウィジェットに付きます。[ゲームビューポートの UI 入力](#ゲームビューポートの-ui-入力3)のコマンドに対象として渡せます。ゲーム層の根を解決できないときは `InGameLayer` とともに省きます（`GameLayerRootUnresolved`） |
| `ProjectCodeFields` | プロジェクトのコードでしか作れない欄と、それを作る Capability とコマンド |
| `XTruncated`・`XTotalCount` | 一覧を切ったときだけ、切る前の件数とともに付きます |
| `ActionDisplayNameTruncated`・`LegacyRowDisplayNameTruncated`・`InputActionDescriptionTruncated` | テキストを切った。テキストは制御文字を除き、256 文字で切ります |
| `Limitations[]` | 返した内容の注意点。それぞれ `Code` と、場合により `Detail` を持ちます |

`Limitations[].Code` は次のいずれかです:

| `Code` | 意味 |
|---|---|
| `NotAtSafePoint` | エンジンの状態が更新の途中だったかもしれないので読まなかった（`DescribeActivatableWidgetsWithProjectCode` では、プロジェクトのコードの実行中にエンジンが安全な地点を離れた） |
| `GeometryFromPreviousFrame` | 位置と大きさは、最後にレイアウトしたフレームの値 |
| `GameLayerRootUnresolved` | ゲーム層の根を解決できなかった。`InGameLayer`・`TypePath`・`Fingerprint` を省いた |
| `TransitionStateUnavailable` | コンテナが切り替えの途中かどうかを読めなかった |
| `ReflectedFieldUnavailable:<欄>` | 名前で読むエンジンの欄が、このエンジンの版に無かった。それに依存するものを省いた |
| `NoLocalPlayers` | ワールドにローカルプレイヤーがいない |
| `SlateUnavailable` | Slate が初期化されていない（描画の無いプロセスなど） |
| `LeafmostUnavailableOnThisEngineVersion` | UE 5.7: エンジンが最前面の活性化ウィジェットを公開していないので、`Leafmost` を省いた |
| `InputModeNotEnforced` | ゲームビューポートクライアントが CommonUI のものの派生ではないので、CommonUI の入力モードがゲーム入力の経路で適用されない |
| `GameInputGateContributorNotInstalled` | このプロセスでは、CommonUI の判定が注入ゲートに入っていない |
| `ViewportClientOverridesNotEvaluated` | ゲームビューポートクライアントがプロジェクトのクラス。その override は実行していないので、ビューポートの値はエンジンの実装の値 |
| `ScreenChangedDuringProjectCode` | プロジェクトのコードの実行中にワールドかウィジェットが変わり、コマンドが止まった |
| `LegacyRowNotReadFromProjectDataTable` | DataTable のクラスをプロジェクトが派生させているので、その行を読まなかった |

#### エラー

| ErrorCode | 発生条件 |
|---|---|
| `InvalidParams` | パラメータの型が違う・範囲外・未知のキー。`WidgetPaths` の要素が上の規則に外れる |
| `NotAllowed` | プレイワールドが動いていない、または `TargetNetRole` / `TargetPIEInstance` に一致するものが無い。`DescribeActivatableWidgetsWithProjectCode` で、モーダルダイアログが開いている、またはエンジンの tick が止まっている |
| `NotFound` | `PlayerIndex` がどのローカルプレイヤーも指さない（メッセージが存在する番号を挙げる） |
| `CapabilityNotAvailable` | 必要な Capability が付与されていない |
| `PolicyViolation` | 必要な Capability が安全ポリシーで拒否されている。読み取り専用モードでの `DescribeActivatableWidgetsWithProjectCode` |
| `CommandNotFound` | `CommonUI` プラグインが無効。デモ版 |

Fab で配布された UAIP をエンジンに入れてパッケージしたゲームでは、任意の連携は組み込まれず、ほかの任意の連携と同じく、4 つのコマンドは一覧に出たまま `OptionalPluginDisabled` で断ります。プロジェクトと一緒にコンパイルされるよう、UAIP をプロジェクトの `Plugins` フォルダーに置いてください。[Capability リファレンス](safety.md#capability-リファレンス) を参照してください。

---

## UAIP.Runtime.ChaosDestruction

実行中のゲームの Chaos 破壊を観測するコマンド群です。ワールドにどの Geometry Collection コンポーネントがあってどれだけ壊れているか、ピースごとの状態、ワールドに作用する物理 Field、破壊イベントの時系列、各ピースが抱えるひずみを返します。破壊そのものを変えることはありません。観測コマンドは読むだけで、ゲームの通知を有効にする唯一のコマンド（`EnableForcedDestructionNotify`）は後述のとおり別扱いです。エディタでは PIE の実行中に、また `-game` 起動やパッケージ版でも動作し、プラグインの依存はありません。

**Capability。** すべてのコマンドが `RuntimeInspect`（DefaultAllow）を必要とします。`EnableForcedDestructionNotify` は `ChaosDestructionForceNotify`（DefaultDenied）も必要です。足りない場合は `CapabilityNotAvailable` です。詳細は [安全性と Capability](safety.md#runtime-chaos-destruction) を参照してください。

**デモ版。** `EnableForcedDestructionNotify` と Capability `ChaosDestructionForceNotify` はデモ版では提供されません。残りの 7 コマンドは提供されます。デモ版ではこのコマンドは存在せず、`CommandNotFound` を返します。

**プレイワールド。** `ListGeometryCollections`、`DumpGeometryCollectionState`、`DumpChaosFieldState`、`StartDestructionCapture`、`CaptureGeometryCollectionStrain` は [`TargetNetRole` / `TargetPIEInstance`](#実行時コマンドの対象プレイワールドを指定する) を受け付けます。`CaptureId` を取る 3 つの記録コマンド（`GetDestructionEventLog`、`StopDestructionCapture`、`EnableForcedDestructionNotify`）の宛先はワールドではなく記録です。

**ゲーム側で破壊の通知が無効のことがあります。** Geometry Collection コンポーネントは、ゲームが対応する通知を有効にしたときだけ破壊・崩壊・衝突・除去を通知し、エンジンの既定は無効です。状態を返すコマンド（`ListGeometryCollections`、`DumpGeometryCollectionState`）はピースを直接読むので影響を受けません。記録（capture）は、サンプリングで検出できるピース単位のイベントは記録し、記録できた種類とできなかった種類、その理由を各応答の `Coverage` で報告します。ゲームを変えずにエンジン自身のイベントデータを記録したいときは `EnableForcedDestructionNotify` を参照してください。

### 現在の状態（3）— `RuntimeInspect` が必要

| コマンド | 説明 |
|---|---|
| 🆓 `ListGeometryCollections` | 対象プレイワールドの Geometry Collection コンポーネントを、アクターパス、続いてコンポーネント名の順に 1 コンポーネント 1 エントリで列挙します。各エントリは、アクター、コンポーネント、レストコレクションのアセット、トランスフォーム数、ルートが壊れたか・どれだけ前か、状態別のピース数、ゲームが設定した通知フラグ、コンポーネントが読めるかどうかを持ちます。`StartIndex`（既定 0）と `MaxEntries` 1〜4096（既定 256）でページを選び、`IncludeClassification: false` でピース数を省けます（既定 `true`）。Data には当該ページの先頭 50 件、成果物にはページ全体が入り、続きのコンポーネントがあるうちは `NextStartIndex` がその次を指します。1 コマンドで分類するトランスフォームは最大 262144 個で、それを超えるコンポーネントは `ClassificationSkipped` を付けて数なしで列挙します。物理状態を持たないコンポーネントは、エラーではなく読めない理由つきで列挙します |
| 🆓 `DumpGeometryCollectionState` | 1 つの Geometry Collection コンポーネントをダンプします。同じアクターの他のコンポーネントを含むコンポーネントの概要、階層レベルごとのピース数、ピースごとの状態（Active、Broken、Decayed、ClusterReleased）・動的状態・位置・回転・速度、ダメージ設定、アセットがアンカーしているトランスフォーム、コンポーネントを初期化する Field を返します。`ActorIdentifier`（必須）でアクターをラベルかオブジェクト名で指定し、アクターに複数ある場合は `ComponentName` でコンポーネントを指定します。`Indices`（トランスフォームインデックス 1〜4096 個）と `States`（`Sleeping`、`Kinematic`、`Static`、`Dynamic`、`Broken`、`Decayed`、`ClusterReleased`、`Active`、`Inactive` のいずれか。大文字小文字は区別しません）でピースを絞り、`StartIndex` と `MaxEntries` 1〜4096（既定 256）でページを選び、`IncludeTransforms` と `IncludeVelocities`（既定 `true`）で位置・回転、または速度を省けます。Data には当該ページの先頭 50 ピース、成果物にはページ全体が入り、続きのピースがあるうちは `NextStartIndex` がその次を指します。ピースがキネマティックや静的である理由（アセット・Field・スクリプト）は区別できません。物理状態を持たないコンポーネントは、エラーではなく読めない理由つきでダンプします |
| 🆓 `DumpChaosFieldState` | 対象プレイワールドに作用する Field をダンプします。ワールドの物理 Field が持つ永続・構築時・直近 tick の一時コマンドについて、物理タイプ、対象属性、発生元アクター名、範囲、大きさ、中心、メタデータ、ノードツリーを返し、レベルに置かれた Field System アクターとそれが持つコマンドも返します。種類ごとに `MaxEntries` 1〜4096（既定 256）で個別に上限をかけ、総数と切り詰めの有無を併記します。`IncludeNodeTrees: false` でノードツリーを省けます（既定 `true`）。Data には各リストの先頭 50 件、成果物には `MaxEntries` が許す分がすべて入ります。物理 Field が無効なワールドは、空のコマンドリストと理由つきで成功し、Field System アクターは列挙します。GPU 上にしかない Field は観測できません |

### イベントの記録（3）— `RuntimeInspect` が必要

記録（capture）はそれを開始したセッションのものです。他のセッションがその ID を指定すると、存在するかどうかを教えずに `NotFound` になります。

| コマンド | 説明 |
|---|---|
| 🆓 `StartDestructionCapture` | 対象プレイワールドの破壊を、呼び出したセッションが持つ記録へ書き始め、その `CaptureId` を返します。`Targets`（1〜64 個のオブジェクト。各 `ActorIdentifier` と任意の `ComponentName`）で指定した Geometry Collection コンポーネントを、`Targets` を省略したときはワールドのすべてのコンポーネント（後から現れるものも含む）を、`StopDestructionCapture` が呼ばれる、実時間で `MaxDurationSeconds`（1〜600、既定 120）が経つ、またはプレイセッションが終わるまで記録します。`Kinds` で記録するイベントの種類を `RootBroken`、`ClusterReleased`、`PieceBrokenOff`、`PieceDecayed`、`AnchorReleased`、`PieceStateChanged`、`CollectionReset`、`Break`、`Crumble`、`Removal`、`Collision`、`FieldApplied` から選びます。既定は `PieceStateChanged` 以外のすべてです。`BufferCapacity`（64〜16384、既定 4096）は保持するイベント数で、超えると古いものから捨て、その数を数えます。1 つのワールドが持てる記録中の capture は全セッション合わせて 8 件、追跡するトランスフォームは 65536 個までで、1 つのセッションがワールドごとに持てる記録中の capture は 1 件です。`ReplaceExisting: true` なら、その capture を止めて新しく始めます（既定 `false`。開始を拒否し、その capture を示します）。トランスフォームの上限を超えるコレクションは追跡されず、`Coverage` と `Limitations` で報告します。ワールドに物理シーンやソルバーが無いときは `PreconditionFailed` で失敗します |
| 🆓 `GetDestructionEventLog` | 記録のイベントを、`SinceSequence`（既定 0）以降、古い順に読みます。`CaptureId`（必須）は `StartDestructionCapture` が返した ID です。プレイセッションが終わった後も使えます。停止した記録はイベントを 30 分保持し、1 セッションは直近の停止済み 4 件を保持します。`MaxEntries` 1〜4096（既定 256）で読むイベント数に上限をかけます。Data には読んだ分の先頭 50 件、成果物にはその全件が入り、`NextSequence` は成果物の最後のイベントの次から続けるための `SinceSequence` です。`SinceSequence` 以降のイベントが読まれる前に捨てられていたときは `Gap` が true になります。応答には、記録の状態、止まった理由、追跡しているコレクションとトランスフォーム、サンプルしたフレーム、記録した秒数、イベントの種類ごとのカバレッジも入ります。異なる発生源のイベントの順序が因果の順であるとは限りません。未知・失効・他人の `CaptureId` は、どれかを教えずに `NotFound` で失敗します |
| 🆓 `StopDestructionCapture` | 記録を止め、最終状態を返します。止まった理由、追跡したコレクションとトランスフォーム、サンプルしたフレーム、記録した秒数、シーケンスの管理情報、イベントの種類ごとのカバレッジを含みます。すでに止まっている記録を止めても成功し、最初に止まった理由（`Stopped`、`DurationLimit`、`WorldTornDown`、`Replaced`）を保ちます。プレイセッションが終わった後も使えます。停止した記録はイベントを 30 分保持し、その間は `GetDestructionEventLog` で読めます。未知・失効・他人の `CaptureId` は、どれかを教えずに `NotFound` で失敗します |

止め忘れた記録は、`MaxDurationSeconds` に達したとき、またはプレイワールドが片付けられたときに自動で止まります。

### ひずみのスナップショット（1）— `RuntimeInspect` が必要

| コマンド | 説明 |
|---|---|
| 🆓 `CaptureGeometryCollectionStrain` | 1 つの Geometry Collection コンポーネントのピースが抱えるひずみを、次の物理ステップで取得します。ピースごとに、内部ひずみ（親から外れるまでに残っている強度。外れないものは `Unbreakable`）、前ステップの衝突インパルス（または `ForcedBreakMarker`）、外部ひずみ、適用された最大値、余裕、壊れるかどうかを、コンポーネントのダメージ設定とともに返します。`ActorIdentifier`（必須）と `ComponentName` は `DumpGeometryCollectionState` と同じ指定で、`Indices`（1〜4096 個）、`StartIndex`、`MaxEntries` 1〜4096（既定 256）でピースを選びます。物理ステップを最大 `TimeoutSeconds`（0 より大きく 60 まで、既定 5）まで、`PollIntervalSeconds`（0.05〜1、既定 0.05）ごとに確認しながら待ち、ゲームがポーズ中は `NotAllowed` で拒否します。Data には当該ページの先頭 50 ピース、成果物にはページ全体が入ります。トランスフォームインデックスを持たない内部クラスターは報告しません。物理プロキシが無い、または既定以外のソルバーで動くコンポーネントは、エラーではなく理由とダメージ設定つきで報告します。タイムアウトしたときは、`Executed` が false の `Result` とゲームがポーズ中だったかを返します |

### 破壊の通知を強制的に有効にする（1）— `RuntimeInspect` と `ChaosDestructionForceNotify` が必要

デモ版では提供されません。

| コマンド | 説明 |
|---|---|
| `EnableForcedDestructionNotify` | `Kinds`（`Breaks`、`Crumblings`、`Collisions`、`Removals`。大文字小文字は区別せず、各 1 回まで）で指定した破壊の通知を、呼び出したセッションの記録中の capture が既定の物理ソルバー上で追跡している Geometry Collection コンポーネント（capture が後から追跡し始めるものを含む）で、その capture が止まるまで有効にします。`CaptureId`（必須）で capture を指定します。その通知で得られるイベント（壊れたピースの質量・速度・範囲、崩壊が解放した子、衝突の相手とインパルスなど）は、その capture だけが記録します。同じワールドの他の capture には、ゲーム自身の設定のままに見えます。強制できるのは、capture が記録するイベントの種類に対応する通知だけです（`Breaks` は `Break`、`Crumblings` は `Crumble`、`Collisions` は `Collision`、`Removals` は `Removal`）。それ以外は `InvalidParams` で拒否し、何も強制しません。同じ capture に再度呼ぶと種類が追加されます。ゲームがすでに有効にしている通知には触れません。capture の状態を返します。この capture が強制したセルは `Coverage` に `ForcedByUAIP` が付き、`Limitations` に `ForceNotifySideEffects` が入ります。読み取り専用モードでは拒否されます。未知・失効・他人の `CaptureId` は `NotFound`、すでに停止した capture は `NotAllowed` で失敗します。⚠️ 副作用と戻せない点は [強制した破壊の通知](#強制した破壊の通知) を参照してください |

#### 強制した破壊の通知

- **ゲーム自身のリスナーにもイベントが届きます。** 通知を強制している間は、ゲームがその通知に登録したリスナーにも、capture だけでなくイベントが届きます。エンジンは、通知を有効にするたび、および元に戻すときに、コンポーネントの Chaos イベントをすべて登録解除して登録し直すので、別の経路で登録したリスナーに影響が出ることがあります。
- **戻せない部分があります。** 通知を有効にすると、ソルバーのイベントフィルターが上がります。エンジンにはこれを下げる手段がありません。capture が止まった後も、プレイセッションが終わるまで、ソルバーはそのイベントデータを作り続けます。
- **復元。** capture が止まる（`StopDestructionCapture`、時間切れ、置き換え、セッション終了）と、どの capture も強制しなくなった通知は、強制した値のままなら元に戻します。その間にゲームが切った通知はゲームが設定したままにします。ゲームが有効に書き戻した通知は区別できないので、同じく元に戻します。プレイワールドが片付けられるときは何も戻しません。
- **独自の衝突プロファイルを持つコンポーネントでは、衝突の通知を強制しません。** パーツごと・レベルごとの衝突プロファイル、またはレプリケートするコンポーネントの Abandoned 用プロファイルを設定している場合です。強制するとそれらのプロファイルが物理状態を作り直すまで上書きされるため、そのコンポーネントでは `Collisions` を受け付けてもカバレッジが `NotGenerated`（`ForceNotSupported`）になり、衝突の設定はそのまま残ります。同じ記録の他のコンポーネントと、他の種類の通知は強制されます。

Capability の付与方法は [安全性と Capability](safety.md#runtime-chaos-destruction) を参照してください。

#### すべての応答に含まれるフィールド

各応答には、いつ・どこを読んだか（観測した capture やプレイワールド、フレーム、時刻）が入ります。埋められなかった部分は黙って省かず、`Limitations[]` に（`Code` つきで）返ったものの注意点を載せ、記録系の応答は `Coverage[]`（イベントの種類とコレクションごとの 1 セル）で、その種類のイベントを記録できたかどうかを示します。

パラメーターはプレイワールドを探す前に検証するので、PIE が動いていなくても、不正なリクエストは `InvalidParams` で拒否されます。未知のキー、JSON の型違い、範囲外の値、空の配列は `InvalidParams` です。

成功した呼び出しは必ず JSON の成果物を 1 つ保存し、失敗した呼び出しは何も保存しません。

---

## UAIP.Runtime.Navigation

ワールドの NavMesh と経路探索を観測するコマンド群です。ナビゲーションシステムがあるか・どう設定されているか、ある地点から別の地点へ行けるか・行けないならなぜか、経路そのものとエリアごとのコスト、メッシュのタイル、メッシュを形作るモディファイア、AI が経路上で何をしているか、メッシュの再生成が落ち着いたか、を返します。7 つのコマンドは観測だけを行い、8 つ目の `RebuildNavigation` はメッシュの再生成を予約します（下で別に説明します）。エディタ（PIE の有無を問わない）でも、`-game` 起動やパッケージ版でも動作し、プラグインの依存はありません。

**Capability。** 7 つのコマンドは `RuntimeInspect`（DefaultAllow）を必要とします。`RebuildNavigation` は `RuntimeNavigationRebuild`（DefaultDenied）を必要とします。`FindPath` と `IsLocationReachable` は、`MaxSearchNodes` が 8192 を超えるとき**だけ**、さらに `RuntimeNavigationExtendedSearch`（DefaultDenied）を必要とします。この Capability は要求ごとに判定するため、コマンドが宣言する `RequiredCapabilities` には現れません。足りない場合は、その名前を示した `CapabilityNotAvailable` になります。詳細は [安全性と Capability](safety.md#runtime-ナビゲーション) を参照してください。

**デモ版。** `RebuildNavigation` と `RuntimeNavigationRebuild` Capability はデモ版に含まれません。ほかの 7 コマンドは提供されます。デモ版ではこのコマンドは存在せず、`CommandNotFound` を返します。

**どのワールドを読むか。** `DumpNavigationSystemState`・`FindPath`・`IsLocationReachable`・`DumpNavMeshTiles`・`QueryNavModifiers`・`WaitForNavigationBuild` は、プレイワールドが動いていればそれを、動いていなければエディタワールドを読みます — NavMesh はエディタで生成・保存されるため、PIE を起動せずに確かめられます。`GetPathFollowingState`（AI コントローラーはプレイワールドにしか存在しません）と `RebuildNavigation`（エディタのレベルは変更しません）は、プレイワールドだけを対象にします。8 つすべてが [`TargetNetRole` / `TargetPIEInstance`](#実行時コマンドの対象プレイワールドを指定する) を受け付けます。存在しないプレイワールドを指定すると `NotAllowed` になり、エディタワールドへ切り替わることはありません。

### 観測（6）— `RuntimeInspect` が必要

| コマンド | 説明 |
|---|---|
| 🆓 `DumpNavigationSystemState` | 対象ワールドのナビゲーションシステムの状態を返します。プレイワールド選択子以外のパラメータはありません。応答には `NavDataCount` と `NavData[]`（最大 64 件。`Name`・`IsMain`・`IsRecast`・`HasValidNavMesh`・`AgentName`・`AgentRadius`・`AgentHeight`・`StepHeight`・`MaxSlopeDegrees`・`RuntimeGeneration`（`Static` / `DynamicModifiersOnly` / `Dynamic`）・`ActiveTilesOnly`・`TileCount`・`TilePoolCapacity`、および `CellSize`・`CellHeight`・`TileSizeUU`・`TilePoolSize` などの `GenerationParameters`）、3 種類の境界 — `NavigationBounds[]`（システムに登録されたボリューム。最大 256 件）・`NavigableBounds`（各ナビゲーションデータが対象とする範囲）・`NavMeshBounds`（生成されたメッシュが実際に覆う範囲）—、`Areas[]`（最大 64 件。`DefaultCost` と `FixedAreaEnteringCost`）、`BuildState`、`SearchLimits` が入ります。`SearchLimits` は経路探索がどこまで探せるかを示します: `DefaultCeiling`（8192）・`ExtendedCeiling`（65534）・`ExtendedSearchCapability`（上限を引き上げる Capability の名前）・`ExtendedSearchGranted`（呼び出したセッションがそれを持っているか）・`EngineDefaultMaxSearchNodes`。artifact には全項目が入ります |
| 🆓 `FindPath` | 2 点間の経路と、終点に到達できるかを返します。各点は座標（`StartLocation` / `EndLocation`）かアクター（`StartActor` / `EndActor`）で指定します。`AgentActor`（Pawn またはそのコントローラー）は、クエリに Owner・ナビゲーションデータ・既定フィルタを貸し、省略された始点の代わりにもなります。応答には `Reachable`（`true`・`false`、判定できないときは `null`）、`Reason`（[到達判定の読み方](#到達判定の読み方) を参照）、`Result`、`QueryConditions`（クエリが実際に使った条件: `Owner`・`NavData`・`Filter{Class, Source, QuerierPresent}`・`StartSource`・`EndSource`・`RequireNavigableEndLocation`・`AllowPartialPath`・`MaxSearchNodes{Value, Source, Ceiling}`）が入り、経路が得られる `Reason` では `IsPartial`・`Length`・`Cost`・先頭 50 件の `PathPoints` と `PathPointsTotalCount`・`AreaBreakdown[]`（経路上の各エリアが占めるコストと長さ。除外されたエリアは `Traversable: false` と `ExclusionSource`）も入ります。点をメッシュへ投影できなかったときは、`StartProjection` / `EndProjection` がどちらが失敗したかを示し、`TileExistsAtLocation` にその地点にタイルがあるかを入れます。artifact には最大 `MaxPathPoints` 個の点とコリドーが入ります |
| 🆓 `IsLocationReachable` | `FindPath` と同じ問いを、同じパラメータ（`MaxPathPoints` を除く）で行い、`Reachable`・`Reason`・`QueryConditions`・着地に失敗した点の投影結果は同じものを返します。経路・長さ・コスト・エリア内訳は返しません |
| 🆓 `DumpNavMeshTiles` | 1 つのナビゲーションメッシュのタイルを (X, Y, Layer) の順に返します。各タイルの `X`・`Y`・`Layer`・`Bounds`・`Resolution`・`PolygonCount` が入ります。`Box` を指定するとそれに重なるタイルだけに絞り、`NavDataName` でナビゲーションデータを選び（既定はメインのもの）、`MaxTiles` は 1〜4096（既定 256）です。応答には先頭 50 件の `Tiles[]` と `TotalCount`（`MaxTiles` を適用する前に数えた正確な件数）が入り、artifact には一覧に載せた全タイルが入ります。ポリゴン数は一覧に載せるタイルについてだけ読みます |
| 🆓 `QueryNavModifiers` | 必須の `Box` に触れるナビゲーションモディファイアと、その領域のメッシュのポリゴンがエリアにどう分かれているかを返します。各モディファイアには発生源（`Name`・`Path`・`Label`）・`Bounds`・エリアクラス・置き換え対象のエリアクラス・`Shape`・`ApplyMode` が入ります。エンジンがまだ収集していないモディファイアは `PendingLazyGathering` が付き、コンポーネントが宣言している `DeclaredAreaClass` を添えます。`AreaBreakdown` はエリアごとのポリゴン数で、`MaxPolygons`（1〜16384、既定 4096）まで数えます。`AreaBreakdown.CountComplete: false` は件数が下限であることを示します。`MaxModifiers` は 1〜4096（既定 256）です。応答には先頭 50 件のモディファイアと `TotalCount` が入り、artifact には捕捉した全モディファイアが入ります |
| 🆓 `GetPathFollowingState` | 1 体の AI の PathFollowingComponent がいま何をしているかを返します（プレイワールドのみ）。`Status`（`Idle`・`Waiting`・`Paused`・`Moving`）・`HasPath`・`RequestId`・目標（`GoalLocation` はたどっている経路の終点で、`PathPoints` が打ち切られても経路の終点を返し、経路が無いときは省きます。`MoveGoal` はアクターへ向かうときのそのアクターです）・いま向かっている区間の終点（`CurrentTargetLocation`）・いまの区間（`CurrentPathIndex`・`NextPathIndex`）・`AcceptanceRadius`・`HasPartialPath`・経路を作ったナビゲーションデータ（`NavDataUsed`）・先頭 50 件の `PathPoints`・経路の `AreaBreakdown[]` が入ります。`ActorIdentifier`（必須）には Pawn かその AI コントローラーを指定します。`MaxPathPoints` は 1〜4096（既定 256）で、artifact に書く点数の上限です。ナビゲーションシステムやメッシュが使えない間も追従状態は返し、エリア内訳だけを省きます |

### 待機（1）— `RuntimeInspect` が必要

| コマンド | 説明 |
|---|---|
| 🆓 `WaitForNavigationBuild` | 対象ワールドのナビゲーションシステムが静止するまで待ちます。静止とは、残っている生成タスクが無く、処理待ちの dirty area も無い状態です。このコマンドは観測だけを行い（ポーリングするだけで、ワールドは進めません）、受動待機なのでトランスポートの単一コマンド枠を占有しません。`TimeoutSeconds` は 0 より大きく 60 以下（既定 30）、`PollIntervalSeconds` は 0.05〜1.0（既定 0.1）です。`WaitOutcome` は `NotApplicable`（ナビゲーションシステムが無い、または有効なナビゲーションデータが無い）・`AlreadyQuiescent`（何も生成していなかった）・`Quiescent`（待つ間に落ち着いた）のいずれかで、先に `TimeoutSeconds` が過ぎたときは `Timeout` で失敗し、結果と artifact は返します。応答には `CompletionScope: "NavigationSystemQuiescent"`・`ElapsedSeconds`・`BuildStateAtStart`・`BuildStateAtEnd`・`World` が入ります。**待機の完了が保証するのは**ナビゲーションシステム全体の静止であって、特定の領域の完了ではありません。エンジンが観測できない形で保留している更新もあり（`Limitations: UnobservablePendingUpdates`）、確認の直後に生成が始まることがあります |

### 再生成の予約（1）— `RuntimeNavigationRebuild` が必要

デモ版では提供されません。

| コマンド | 説明 |
|---|---|
| `RebuildNavigation` | 対象の**プレイ**ワールドのナビゲーションメッシュの再生成を予約し、待たずにすぐ応答します（`IsReadOnly` は false）。`Box` を省くと登録済みの全ナビゲーション範囲を、指定するとその領域だけを予約します。応答には `Queued`・`Scope`（`Full` / `Box`）・`QueuedAreaCount`・`NextStep: "WaitForNavigationBuild"`（その後にこのコマンドを実行し、静止したと返ってから改めて問い合わせてください）・`BuildState` が入り、ナビゲーションデータごとに `Eligible`（再生成の対象か）・`GeometryRebuild`（ジオメトリまで作り直すか。`DynamicModifiersOnly` はモディファイアの再適用だけ）・`ActiveTilesOnly`（Invoker や読み込み済みの World Partition セルの周りのタイルに限って作り直すか）を返します。ワールドにナビゲーションシステムが無い、生成する先が無い、ゲーム中に再生成するナビゲーションデータが無い（`Static`）ときは、何も予約せず `PreconditionFailed` で失敗します。`ErrorMessage` は理由（`NavigationSystemMissing`・`NothingToBuild`・`NoRuntimeGeneration`）で始まり、その説明が続きます。失敗応答に `Data` はありません。ビルドロック・一時停止中のワールド・どの範囲にも入らない領域・生成状態に現れない予約は、失敗ではなく `Limitations[]` で知らせます。artifact は応答と同じ内容で、保存に失敗してもコマンドは成功のままです |

#### パラメータ

| パラメータ | コマンド | 意味 |
|---|---|---|
| `StartLocation` / `EndLocation` | `FindPath`、`IsLocationReachable` | `{X, Y, Z}` のワールド座標。それぞれ `StartActor` / `EndActor` とは排他です。座標は有限で ±2097152 以内でなければなりません |
| `StartActor` / `EndActor` | `FindPath`、`IsLocationReachable` | 経路の始点・終点にするアクターのラベルまたはオブジェクト名（1〜256 文字、制御文字なし）。ナビゲーションエージェントならその足元の位置、そうでなければアクターの位置を使います |
| `AgentActor` | `FindPath`、`IsLocationReachable` | Pawn かそのコントローラーのラベルまたはオブジェクト名。クエリに Owner・ナビゲーションデータ・既定フィルタを貸し、`StartLocation` / `StartActor` が無いときは始点の代わりになります。`NavDataName` とは排他です。Pawn を持たないコントローラーや、ナビゲーションエージェントでない Pawn は `InvalidParams` です |
| `NavDataName` | `FindPath`、`IsLocationReachable`、`DumpNavMeshTiles`、`QueryNavModifiers` | 使うナビゲーションデータのオブジェクト名（1〜256 文字）。省略するとメインのナビゲーションデータを使います。どれにも一致しない名前は `InvalidParams` で、存在する名前を列挙します |
| `FilterClass` | `FindPath`、`IsLocationReachable` | ナビゲーションクエリフィルタのクラスパス（例: `/Script/MyGame.MyQueryFilter`）。すでに読み込まれているクラスだけを受け付け、何も読み込みません。省略するとエージェント（またはナビゲーションデータ）の既定フィルタを使います |
| `RequireNavigableEndLocation` | `FindPath`、`IsLocationReachable` | 真偽値、既定 `true`。メッシュ外の終点でクエリを失敗させるか |
| `AllowPartialPath` | `FindPath`、`IsLocationReachable` | 真偽値、既定 `true`。終点の手前で止まる経路を受け付けるか |
| `MaxSearchNodes` | `FindPath`、`IsLocationReachable` | 4〜65534 の整数。省略するとフィルタ自身の値を使い、`RuntimeNavigationExtendedSearch` が無ければ 8192 を上限に丸め、4 未満なら 4 に引き上げます（どちらも `Limitations: SearchNodesClamped`）。8192 を超える値には Capability が必要で、65534 を超える値や 4 未満の値は、セッションの権限に関わらず `InvalidParams` です。4 ノード未満では、ナビゲーションメッシュが探索ノードプールの範囲外へ書き込むためです。`QueryConditions.MaxSearchNodes.Value` には、クエリが実際に使ったノード数が入ります |
| `MaxPathPoints` | `FindPath`、`GetPathFollowingState` | 1〜4096 の整数、既定 256。artifact に書く経路の点数 |
| `Box` | `DumpNavMeshTiles`（任意）、`QueryNavModifiers`（必須）、`RebuildNavigation`（任意） | `{Min: {X, Y, Z}, Max: {X, Y, Z}}`。どの軸でも `Min` は `Max` を超えてはならず（角を入れ替えることはしません）、X と Y には幅が必要です。高さが 0 なのは許されます |
| `MaxTiles` | `DumpNavMeshTiles` | 1〜4096 の整数、既定 256 |
| `MaxModifiers` | `QueryNavModifiers` | 1〜4096 の整数、既定 256 |
| `MaxPolygons` | `QueryNavModifiers` | 1〜16384 の整数、既定 4096。エリア内訳のために数えるポリゴン数 |
| `ActorIdentifier`（必須） | `GetPathFollowingState` | Pawn または AI コントローラーのラベルまたはオブジェクト名 |
| `TimeoutSeconds` / `PollIntervalSeconds` | `WaitForNavigationBuild` | 数値。上のコマンドの説明を参照 |

始点は `StartLocation`・`StartActor`・（どちらも無いとき）`AgentActor` の Pawn のうちちょうど 1 つ、終点は `EndLocation` と `EndActor` のうちちょうど 1 つです（`AgentActor` は終点の代わりにはなりません）。1 つの点に両方の形を指定する、どれも指定しない、`AgentActor` と `NavDataName` を両方指定する、のいずれも `InvalidParams` です。真偽値は JSON の真偽値、上限値は JSON の整数でなければならず、それ以外の型・未知のキー・範囲外の値は `InvalidParams` です。パラメータはプレイワールドを探す前に検査するため、PIE が動いていなくても不正な要求は拒否されます。

#### すべての応答に入る項目

| 項目 | 意味 |
|---|---|
| `CapturedAt` / `Frame` | 状態を読んだ時刻（ISO 8601、UTC）と、その時点のエンジンのフレーム番号 |
| `NetMode` / `WorldContext` / `PIEInstance` | 読んだワールド。`WorldContext` は `PIE`・`Editor`・`Game` のいずれかで、PIE 以外では `PIEInstance` は省かれます |
| `WorldPartitioned` | 観測したワールドが World Partition を使っているか |
| `Availability` | `State`: `Available`・`Degraded`・`Unavailable`。`Reason` は `NavigationSystemMissing`（`Detail` は `ClientWorld`（再実行先のサーバー側プレイワールドを `ServerCandidates[]` に列挙）・`NoNavigationSystemConfig`・`Unknown`）・`NoNavigationData`・`NoNavigationDataForAgent`・`NavMeshNotBuilt` のいずれか、または — `DumpNavigationSystemState` だけで、一部のナビゲーションデータにだけメッシュがあるとき — `SomeNavDataNotBuilt`（`Degraded`） |
| `BuildState` | `RemainingTasks`・`RunningTasks`・`DirtyAreasQueued`・`Locks[]`（`NoUpdateInEditor`・`NoUpdateInPIE`・`InitialLock`・`Custom`、UE 5.8 では `AsyncLoadLock`）・`AutoUpdateEnabled`・`WorldPaused`・`Quiescent`。ナビゲーションシステムが無いときは省かれます |
| `DegradedSections[]` | 埋められなかった部分。それぞれ `Section` と `Cause`（`NavigationUnavailable`・`SomeNavDataNotBuilt`・`UnreadableField`） |
| `Limitations[]` | 返した内容に関する注意。それぞれ `Code` と `Detail` を持ちます（下を参照） |

ナビゲーションシステムが無いワールドや、ナビゲーションデータにメッシュが生成されていないワールドは、観測コマンドにとって**エラーではありません**。コマンドは成功し、ナビゲーションシステム由来の項目を省いて、理由を `Availability` で示します。このとき `NavDataName` や `FilterClass` の名前は何とも照合されず（`Limitations: SelectionNotEvaluated`）、入力の誤りとして報告されることはありません。判定できない値は、既定値で埋めずに省きます。

#### 到達判定の読み方

`Reachable` は三値で、`null` は「到達できない」ではありません。`SearchLimitReached`・`Unknown`・`NavigationUnavailable`・`NavMeshNotBuilt` は、問いに決着がつかなかったことを意味します。`Reason` は、当てはまる最初の行です。

| `Reason` | `Reachable` | 意味 |
|---|---|---|
| `NavigationUnavailable` | `null` | ワールドにナビゲーションシステムが無い、または有効なナビゲーションデータが無い。経路は計算していない |
| `NavMeshNotBuilt` | `null` | 選んだナビゲーションデータにメッシュが生成されていない。経路は計算していない |
| `StartNotOnNavMesh` | `false` | 始点をメッシュへ投影できなかった |
| `EndNotOnNavMesh` | `false` | 終点をメッシュへ投影できなかった（`RequireNavigableEndLocation: false` のときは起きない） |
| `Reachable` | `true` | 完全な経路がある。始点と終点がほぼ同じ点のときは、長さ 0 の 1 点の経路になる |
| `SearchLimitReached` | `null` | 探索ノードを使い切った。`IsPartial` は true で、経路は探索できたところまで。`MaxSearchNodes` を上げる（8192 超には `RuntimeNavigationExtendedSearch` が必要） |
| `PartialPathOnly` | `false` | 手前で止まる経路しかなく、`AllowPartialPath` は true。部分経路を返す |
| `NoPath` | `false` | 経路が無い、または `AllowPartialPath` が false で部分経路しかない。経路は返さない |
| `Unknown` | `null` | 経路探索の答えが上のどれにも当てはまらない |

`StartNotOnNavMesh` / `EndNotOnNavMesh` では、`StartProjection` / `EndProjection` がどちらの点が失敗したか（`Projected: false`）を示し、`TileExistsAtLocation` がその地点にタイルがあるかを示します — タイルが無いときは、座標の誤りよりも、World Partition の未読み込みの範囲を疑ってください。

`AgentActor` を指定しないクエリには Querier が無いため、ナビゲーションデータの既定以外のフィルタは Querier なしで初期化され、メタフィルタは解決されません。その場合、応答に `Limitations: QuerierlessFilter` が付きます。AI と同じ結果を見るには `AgentActor` を指定してください。AI が入れないエリアは、巨大なコストではなく `Traversable: false` と `ExclusionSource`（`AreaCost`・`AreaFlags`・`NullArea`）で示します。

#### Limitations のコード

| コード | 意味 |
|---|---|
| `UnreadableField` | 項目をエンジンから読めなかったので省いた |
| `CountIncomplete` | `TotalCount` が下限である（`CountComplete` が false） |
| `SelectionNotEvaluated` | ナビゲーションシステムやそのデータが使えないため、`NavDataName` / `FilterClass` を何とも照合しなかった |
| `NonRecastNavData` | Recast メッシュでないナビゲーションデータがあり、メッシュ固有の項目を省いた |
| `DefaultAgentNameUnreadable` | エンジンの既定エージェント名を読めなかったので、それを条件にせずメインのナビゲーションデータを選んだ |
| `QuerierlessFilter` | フィルタが Querier なしで初期化された（上を参照） |
| `SearchNodesClamped` | フィルタ自身の探索ノード数が 8192 を超えていたので下げた、または 4 未満だったので引き上げた。`Detail` にフィルタの値と実際に使った値、下げたときは上限とそれを引き上げる Capability が入る |
| `ActivePathRegistered` | エディタワールドでは、クエリの経路がナビゲーションデータへ登録され、そこでは掃除されない |
| `StaleCorridor` | 経路のコリドーの一部が、その後に再生成されたタイルを指している。該当する項目は `Valid: false` になる |
| `DeclaredAreaUnreadable` | モディファイアのコンポーネントが宣言するエリアを読めなかった |
| `UnobservablePendingUpdates` | エンジンが観測できない更新を保留しているため、静止と答えた直後に生成が始まることがある |
| `NavMeshNotBuiltAtQuiescence` | 静止したが、メッシュが無いナビゲーションデータが残っている。`Detail` にその名前が入る |
| `BuildLocked` | ビルドロックが掛かっている。`Detail` にそのロックが入る。予約した範囲はロックの解除後に処理される |
| `WorldPaused` | ワールドが一時停止している。その間、予約した範囲は処理されないことがある |
| `AutoUpdateDisabled` | エディタワールドで自動更新が無効。dirty area が捨てられ、何も生成しないまま静止に見えることがある |
| `OutsideNavigationBounds` | `RebuildNavigation`: `Box` がどの登録済みナビゲーション範囲の外にある |
| `ModifiersOnlyRebuild` | `RebuildNavigation`: モディファイアの再適用だけを行うナビゲーションデータがある（`DynamicModifiersOnly`） |
| `ActiveTilesGenerationOnly` | `RebuildNavigation`: アクティブなタイルに限って再生成するナビゲーションデータがある |
| `QueueNotObserved` | `RebuildNavigation`: 予約の直後に読んだ生成状態に予約中の範囲が現れず、エンジンが要求を捨てた可能性がある。`Detail` に予約した範囲の数が入る |

#### 出力の上限

`Data` に直接載せる一覧は先頭 50 件までで、捕捉した全件は artifact に入ります。件数の上限は、タイルとモディファイアが 4096、経路の点が 4096、ナビゲーションデータが 64、登録済みの範囲が 256、エリアが 64 です。上限で切った一覧は `TotalCount` を併記し、内側の配列は 64 件で切って `Truncated` を付けます。1 回の要求の作業量にも上限があります: 処理するポリゴン数（`MaxPolygons`）と探索ノード数（8192。`RuntimeNavigationExtendedSearch` があれば 65534）です。

#### エラー

| ErrorCode | 発生条件 |
|---|---|
| `InvalidParams` | パラメータが欠けている・型が違う・範囲外・未知のキー。上の排他の組み合わせ。どれにも一致しない `NavDataName`（メッセージに存在する名前を列挙）。読み込まれていない、またはナビゲーションクエリフィルタでない `FilterClass`。65534 を超える、または 4 未満の `MaxSearchNodes`。`TargetNetRole` / `TargetPIEInstance` を満たせない |
| `CapabilityNotAvailable` | `RuntimeInspect`、（`RebuildNavigation` では）`RuntimeNavigationRebuild`、（`MaxSearchNodes` が 8192 を超えるときは）`RuntimeNavigationExtendedSearch` が付与されていない。メッセージにその名前が入る |
| `PolicyViolation` | その Capability が安全ポリシーで明示的に拒否されている |
| `NotAllowed` | プレイワールドを必要とするコマンドでプレイワールドが動いていない、または `TargetNetRole` / `TargetPIEInstance` に一致するものが無い |
| `NotFound` | `StartActor`・`EndActor`・`AgentActor`・`ActorIdentifier` に一致するアクターが無い。`GetPathFollowingState` では、アクターが AI コントローラーに動かされていない場合と、AI コントローラーに PathFollowingComponent が無い場合（それぞれ別のメッセージ） |
| `ExecutionFailed` | 識別子に複数のアクターが一致する。フィルタを解決できなかった。観測コマンドの artifact を書けなかった。`WaitForNavigationBuild` の待機中にワールドが破棄された |
| `PreconditionFailed` | `RebuildNavigation` のみ: ワールドにナビゲーションシステムが無い、生成する先が無い、またはゲーム中に再生成するナビゲーションデータが無いため、何も予約しなかった |
| `Timeout` | `WaitForNavigationBuild` のみ: `TimeoutSeconds` 以内に静止しなかった。結果と artifact は返す |

観測コマンドは、成功した呼び出しごとにちょうど 1 つの JSON artifact を保存し、失敗した呼び出しは何も保存しません。

---

## UAIP.Runtime.Animation

実行中のゲームでキャラクターのアニメーション状態を観測するコマンド群です。ステートマシンごとのアクティブな State、ブレンドのウェイト、再生中のモンタージュ、アニメーションカーブの値、アニメーションがそもそも更新されているか、AnimInstance の変数の値、そして Motion Matching では直近の検索がどのポーズを選んだか、を返します。どのコマンドも読むだけで、アニメーションの挙動を変えることはありません。エディタでは PIE の実行中に、また `-game` 起動やパッケージ版でも動作します。7 つすべてが [`TargetNetRole` / `TargetPIEInstance`](#実行時コマンドの対象プレイワールドを指定する) を受け付けます。ステートマシン名と State 名は Anim Blueprint エディタと同じ綴りで返るため、ここで見た State をエディタ側で名前から探せます。

**Capability。** 7 つすべてが `RuntimeInspect`（DefaultAllow）を必要とします。`DumpAnimInstanceVariables` は、さらに `AnimInstanceVariableDump`（DefaultDenied）を必要とします。プロジェクト自身の AnimInstance クラスが宣言した変数の値を書き出し、それにはプロジェクトの任意のデータが入りうるためです。足りない場合は、その名前を示した `CapabilityNotAvailable` になります。詳細は [安全性と Capability](safety.md#runtime-アニメーション) を参照してください。

**オプションのプラグイン。** `GetMotionMatchingState` 🧩 は、PoseSearch プラグインが有効なときだけ登録されます。無効なときはこのコマンドが存在せず（必要なプラグインを示す案内付きの `CommandNotFound`）、ほかの 6 コマンドは影響を受けません。デモ版には含まれません。

**読み取りが表すもの。** 値は呼び出した瞬間のものです。履歴は返しません。モンタージュがいつブレンドアウトに入ったかは分からず、ブレンドアウトが終わったモンタージュは残っていません。応答の識別子（`InstanceId`、`MachineId`、`NodeId`、`MontageInstanceId`）は、その応答の中で項目を区別するためのものです。Anim Blueprint の再コンパイルや別のプレイセッションをまたいでは保たれないので、保存して後の照合に使わず、次に調べるときはステートマシン名・State 名で絞り込んでください。

### 観測（5）— `RuntimeInspect` が必要

| コマンド | 説明 |
|---|---|
| 🆓 `DumpAnimInstanceState` | 以下のすべてを 1 回の読み取りでまとめて返すので、各節が同じフレームを表します。1 つのスケルタルメッシュコンポーネントの本体・Linked・Post Process の AnimInstance について、更新状態・ステートマシン・ブレンドのウェイト・モンタージュ・カーブです。ステートマシン（`StateMachineName`）とカーブ（`CurveType`、`CurveNameContains`）を絞り込めます。Motion Matching と変数は含みません — それぞれ `GetMotionMatchingState` と `DumpAnimInstanceVariables` を使ってください。応答には要約と各一覧の先頭の項目が載り、成果物には残した項目がすべて入ります |
| 🆓 `GetAnimStateMachineStates` | ステートマシンの状態です。マシンごとに、アクティブな State（`ActiveState`）とその State にいる経過時間（`ActiveStateElapsedSeconds`）、ウェイトを持つ State（`StateWeights`）、進行中の遷移（`ActiveTransitions`: `PreviousState` → `NextState` と `NextStateWeight`）、マシン自体のウェイトを返します。アクティブと報告される State には、ブレンドアウト中の State も含まれます。遷移には名前も経過時間もなく、進み具合は遷移先の State のウェイトで示します。まだ動き出していないマシンは、ウェイトも遷移も無い `Uninitialized` として返ります。`StateMachineName` で絞り込め、同じ名前のマシンはすべて返ります |
| 🆓 `GetAnimBlendWeights` | 再生中のアセットとその最終ブレンドウェイト（`Players`。ブレンドスペースは座標とサンプルのウェイト付き）、ブレンドスペースのプレイヤーノード（`BlendSpaceNodes`）、レイヤードブレンドのノードと各ブレンドポーズのウェイト（`LayeredBlends`）、単一ノードの AnimInstance では再生中のアセット（`SingleNode`）を返します。ブレンドアウト中のモンタージュも有効として数えるため、そのブレンドはブレンドアウトが終わるまでウェイトに含まれます。絞り込みはありません |
| 🆓 `GetActiveMontages` | 有効なモンタージュ（ブレンドアウト中を含む）です。モンタージュのインスタンスごとに、`State`（`BlendingIn`、`Playing`、`BlendingDown`、`BlendingOut`、`Stopped`、`HoldingAtEnd`、`Paused`、`Unknown`）、`PositionSeconds` と `PlayLengthSeconds`、`PlayRate`、現在と次のセクション、`Weight` と `DesiredWeight`、グループ、再生しているスロットとそのウェイトを返します。本体のモンタージュのデータを使う Linked の AnimInstance は、繰り返さずに `SharedWithMain` の印を付けます。絞り込みはありません |
| 🆓 `GetAnimCurveValues` | アニメーションカーブを名前順に、名前・値・種別（`Types`）で返します。すべてのカーブは `Attribute` で、マテリアルパラメータやモーフターゲットも駆動するカーブには、さらに `Material` または `MorphTarget` が付きます。`CurveType` で絞り込めます（`Material` か `MorphTarget`。`All` と `Attribute` はすべてのカーブを残します）。`CurveNameContains` は名前に指定の文字列を含むカーブを残します。`TotalCount` はフィルターを通ったカーブの数、`UnfilteredCount` は通す前の数です。値は最後に完了した評価のもので、更新レートの最適化で評価を省いた箇所では補間された値か直前の値です。カーブの一覧は `MaxEntries` で変えない限り 1024 件で切ります。Linked の AnimInstance と、本体があるときの Post Process の AnimInstance は、カーブを繰り返さずに `SharedWithMain` の印を付けます |

### 変数の値の観測（1）— `RuntimeInspect` と `AnimInstanceVariableDump` が必要

| コマンド | 説明 |
|---|---|
| `DumpAnimInstanceVariables` | プロジェクトが持つ AnimInstance クラスが宣言した変数の値を、本体と、`InstanceScope` が `Main` でなければ Linked・Post Process の AnimInstance について、それぞれ自分の値で返します。変数ごとに名前・宣言したクラス・型・値を返します。**プロジェクトが持つ**とは、プロジェクトの Anim Blueprint と C++ クラス、およびプロジェクトの `Plugins/` に入れたプラグインのものです。エンジン本体・エンジンに同梱されたプラグイン・エンジン側にある親クラスが宣言した変数は出ません（親がエンジン側のクラスであるプロジェクトの Anim Blueprint でも、親が宣言した変数は出ません）。ノードの内部構造も出しません。オブジェクト参照は参照先のパスで書き、辿りません。大きな値は切り詰めます: 配列は 32 要素、文字列は 1024 文字、構造体は 1 段まで展開します。サイズの予算を使い切ったときは、変数や AnimInstance ごと省き、省いたことを示す印を付けます。`VariableNameContains` は名前に指定の文字列を含む変数を残します。応答には AnimInstance ごとに先頭 50 個の変数が載り、成果物には残した変数がすべて入ります。⚠️ **この Capability を解禁すると、変数に入っている文字列やパスがそのまま成果物に出ます** — [安全性と Capability](safety.md#runtime-アニメーション) を参照してください |

### Motion Matching（1）🧩 — `RuntimeInspect` が必要

デモ版には含まれません。PoseSearch プラグインが有効なときだけ登録されます。

| コマンド | 説明 |
|---|---|
| `GetMotionMatchingState` | 直近のポーズ検索が Motion Matching のノードごとに残した状態です。選ばれたアニメーション（`SelectedAnimationPath`）とその中の時刻（`SelectedTimeSeconds`）、ミラーかどうか（`Mirrored`）、ブレンドスペースの座標（`BlendParameters`）、選ばれた元のポーズ検索データベース（`SelectedDatabasePath`）、合計コスト（`SearchCost`）、検索が再生中のポーズを継続したか（`IsContinuingPoseSearch`）、検索が望む再生速度（`WantedPlayRate`）、最後にポーズが切り替わってからの秒数（`ElapsedPoseSearchTimeSeconds`）を返します。まだ何も選んでいないノードは `HasSearchResult: false` で、選択に関する項目はすべて `null` です。AnimInstance ごとに自分のエントリで読み、ノードはその `MotionMatching` の下に入ります。Motion Matching を使っていないキャラクターは、失敗ではなく空の一覧と制限事項 `NoMotionMatchingNode` を返す成功です — ただし、対象のすべての AnimInstance を読めたときだけ言います。読めなかった AnimInstance があれば、その理由だけを示します。ノードは `MaxEntries` まで並べ、切った後ろのノードは数えないため、一覧を切ったときの `TotalCount` は `null` です。コストの内訳・候補ポーズ・検索したデータベースの一覧・ポーズの番号は返しません |

#### パラメータ

| パラメータ | コマンド | 意味 |
|---|---|---|
| `ActorIdentifier`（必須） | すべて | 観測するスケルタルメッシュコンポーネントを持つアクターのラベルまたは名前（1〜256 文字） |
| `ComponentName` | すべて | スケルタルメッシュコンポーネントの名前。大文字小文字を区別しない完全一致（1〜256 文字）。省略したときは [読むメッシュの選び方](#読むメッシュの選び方) に従って選びます |
| `InstanceScope` | すべて | `Main`（本体の AnimInstance だけ）または `All`（本体と Linked・Post Process）。既定は `All` |
| `MaxEntries` | すべて | カーブを含むすべての一覧の件数の上限。1〜4096 の整数。既定はカーブ以外が 256、カーブが 1024。値はすべての一覧に効くため、`300` を指定するとカーブの上限も 1024 から 300 になります |
| `StateMachineName` | `GetAnimStateMachineStates`、`DumpAnimInstanceState` | 返すステートマシンの名前。大文字小文字を区別しない完全一致（1〜256 文字）。同じ名前のマシンはすべて返ります |
| `CurveType` | `GetAnimCurveValues`、`DumpAnimInstanceState` | `All`（既定）、`Attribute`、`Material`、`MorphTarget` |
| `CurveNameContains` | `GetAnimCurveValues`、`DumpAnimInstanceState` | カーブ名に含まれるべき文字列。大文字小文字を区別しない部分一致（1〜256 文字） |
| `VariableNameContains` | `DumpAnimInstanceVariables` | 変数名に含まれるべき文字列。大文字小文字を区別しない部分一致（1〜256 文字） |
| `TargetNetRole` / `TargetPIEInstance` | すべて | [実行時コマンドの対象プレイワールドを指定する](#実行時コマンドの対象プレイワールドを指定する) を参照 |

絞り込みのパラメータは、対応するコマンドだけが受け付けます。それ以外のコマンドに渡す、知らないキー、空の文字列、256 文字を超える名前、1〜4096 の外の件数、知らない種別は `InvalidParams` です。パラメータはプレイワールドを探す前に検査されるため、PIE が動いていなくても不正な要求は拒否されます。

#### 読むメッシュの選び方

`ComponentName` を省略したときは、次の順で選びます。アニメーションを持つスケルタルメッシュコンポーネントが 1 つだけならそれ。複数あるときは、キャラクター本体のメッシュ（持つアクターの場合）。アニメーションを持つものが 1 つも無く、メッシュが 1 つだけならそのメッシュです。応答には、どう選んだか（`ByName`、`OnlyAnimated`、`CharacterMesh`、`OnlyMesh`）と、ほかの候補の一覧が載ります。どの規則でも 1 つに絞れないときは、候補の一覧付きの `InvalidParams` で失敗するので、名前を選んで指定し直してください。MetaHuman のように顔が別のメッシュのキャラクターでは、既定では体のメッシュを読みます。顔のメッシュを読むには、その名前を指定します。

AnimInstance を持たないメッシュはエラーではありません。アニメーションの節を空にし、`NoAnimInstance` と、メッシュのアニメーションの設定（Anim Blueprint を使う / 単一アセット / なし）を示す成功になります。`ComponentName` で名前を指定した、本体に追従するだけのメッシュでも同じです。

#### すべての応答に含まれるフィールド

| フィールド | 意味 |
|---|---|
| `CapturedAt` / `Frame` | 状態を読んだ時刻（ISO 8601、UTC）と、そのときのエンジンのフレーム番号 |
| `NetMode` / `WorldContext` / `PIEInstance` | 読んだワールド。`PIEInstance` は PIE 以外では省略されます |
| `Actor` / `Component` / `ComponentSelection` / `Candidates[]` | 読んだアクターとメッシュコンポーネント、メッシュの選び方、アクターのほかのスケルタルメッシュコンポーネント |
| `Instances[]` | AnimInstance ごとに 1 項目。本体 → Linked → Post Process の順です: `InstanceId`、`Role`（`Main`、`Linked`、`PostProcess`）、`ClassPath`、`IsAnimBlueprintClass`、`Initialized`、`SharedWithMain`、そのコマンドが読む節。1 つのメッシュで読む AnimInstance は 64 個までで、超えた分は「省いた」と示されます |
| `UpdateState` | アニメーションが更新されているか。止まっているときは `Details` にその理由が並びます: `AnimationDisabled`、`AnimationPaused`、`SkeletonUpdateDisabled`、`ComponentTickDisabled`、`WorldPaused`、`NotRendered`。更新レートの最適化の状態も併記されます。更新レートの最適化で今回のフレームだけ更新を飛ばしている場合は、止まっているとは扱わず `UpdateSkippedByURO` で示します |
| `ValueBasis` | 値がどの時点のものかに依存する項目で、その基準を示します: `NodeLastUpdate`、`RecordedReadBuffer`、`InstanceCurrent`、`LastCompletedEvaluation` |
| `DegradedSections[]` / `Limitations[]` | 埋められなかった部分とその理由、および返した内容に関する注意。それぞれ `Code` と、場合により `Detail` を持ちます。同じ理由が何度も出るときは 1 つにまとめて `Count` を付けます |

読めない節があるときは、その部分だけを省いて理由を示し、コマンド自体は成功します。例: 初期化されていない AnimInstance は中身を読まずに列挙します（`AnimInstanceNotInitialized`）。動き出していないステートマシンは `Uninitialized` です。アニメーションが無効のメッシュでは、マシンのウェイトだけを省きます。非数や無限大の数値は `null` にします。Anim Blueprint を使わない AnimInstance（C++ だけのもの、単一アセットの再生）はステートマシンもノードも持たず、その理由を示します（`NativeAnimInstance`、`SingleNodeInstance`）。モンタージュ・カーブ・再生中のアセットは読めますが、C++ だけの AnimInstance では再生中のアセットの位置が空になることがあります。単一アセットの再生でモンタージュを再生しているときは、`SingleNode` が `null` になり、モンタージュとして返ります。モンタージュ以外を再生していて別のモンタージュが有効なときは、位置がモンタージュのものである可能性があります（`SingleNodePositionFromMontage`）。

#### 出力の上限

一覧は `MaxEntries`（既定は 256、カーブは 1024、最大 4096）で、決まった順序で打ち切り、`TotalCount` を報告します。入れ子の一覧（ブレンドスペースのサンプル、モンタージュのスロット、メッシュの候補）は 64 件までです。1 つのコマンドの量は全体でも上限があり、達したらそれより後ろの一覧は読まずに「省いた」と示すため、空だった一覧と省いた一覧を区別できます。応答には各一覧の先頭 50 件が載り、成果物には上限の範囲で読めたものがすべて入ります。

#### Linked Anim Layer と Post Process

既定では、本体・Linked・Post Process のすべての AnimInstance を、本体を先頭にして返します。Linked のカーブは本体の複製なので繰り返しません。Post Process のカーブも、本体があるあいだは繰り返しません。Linked のモンタージュは、本体のモンタージュのデータを使う設定のときは繰り返しません。変数はすべての AnimInstance について、それぞれ自分の値を返します。Linked Anim Layer を差し替えた直後の 1 回は、再生位置に 1 フレーム古い値が混じることがあります。

#### エラー

| ErrorCode | 発生条件 |
|---|---|
| `InvalidParams` | パラメータの型の誤り・空・長すぎる・範囲外・未知。対応しないコマンドに絞り込みを渡した。メッシュを 1 つに絞れない（メッセージに候補の一覧が付く）。`TargetNetRole` / `TargetPIEInstance` を満たせない |
| `CapabilityNotAvailable` | `RuntimeInspect`、または `DumpAnimInstanceVariables` の `AnimInstanceVariableDump` が許可されていない。メッセージに名前が付く |
| `PolicyViolation` | 安全ポリシーでその Capability が明示的に拒否されている |
| `NotAllowed` | プレイワールドが動いていない、または `TargetNetRole` / `TargetPIEInstance` に一致するものが無い |
| `NotFound` | アクターが見つからない、スケルタルメッシュコンポーネントを持たない、または `ComponentName` の名前のコンポーネントが無い（メッセージに候補の一覧が付く） |
| `PreconditionFailed` | 呼び出した瞬間に、メッシュのアニメーションがワーカースレッドで評価中だった。何も読まず、成果物も保存しません。待つと観測のせいでゲームのイベントが早まって発火するため、待ちません。もう一度呼んでください |
| `ExecutionFailed` | 識別子に一致するアクターが複数ある、または成果物を保存できなかった |

成功した呼び出しは必ず JSON の成果物を 1 つ保存します。失敗した呼び出しは何も保存しません。

---

## UAIP.Runtime.Network

実行中のゲームのネットワークを観測するコマンド群です。ワールドの NetDriver とその合計値、NetDriver が持つコネクションとそれぞれの往復時間・損失・通信量、アクターのレプリケーション設定と、その送信についてサーバーが把握している状態を返します。観測に加えて、レプリケートされるプロパティの値を読み、サーバーとクライアントの間でその値を比べ、パケットを遅延・損失・重複・順序入れ替えさせて回線の悪い状態を再現するパケットエミュレーションを変更できます。エディタでは PIE の実行中に、また `-game` 起動やパッケージ版でも動作します。7 つすべてが [`TargetNetRole` / `TargetPIEInstance`](#実行時コマンドの対象プレイワールドを指定する) を受け付け、ネットワークを使う Play-in-Editor セッションのサーバーワールドか、クライアントワールドの 1 つを選べます。

**Capability。** `GetNetDriverState`・`ListNetConnections`・`DumpActorReplication`・`DumpReplicatedPropertyValues`・`CompareReplicatedProperties` は `RuntimeInspect`（DefaultAllow）を必要とします。`DumpReplicatedPropertyValues` と `CompareReplicatedProperties` は、さらに `RuntimeReplicatedPropertyValueRead`（DefaultDenied）を必要とします。値にはプレイヤーのプラットフォームアカウント識別子（`PlayerState` のレプリケートされる `UniqueId`）やプレイヤー名が入りうるためです。`ListNetConnections` は、`IncludeRemoteAddress` が `true` のとき**だけ**、さらに `RuntimeNetConnectionAddressRead`（DefaultDenied）を必要とします。この Capability は要求ごとに判定するため、コマンドが宣言する `RequiredCapabilities` には現れません。`SetNetworkEmulation` と `ResetNetworkEmulation` は `RuntimeNetworkEmulationControl`（DefaultDenied）を必要とし、読み取り専用ではないため、安全ポリシーが読み取り専用モードのときは拒否されます。足りない場合は、その名前を示した `CapabilityNotAvailable` になります。詳細は [安全性と Capability](safety.md#runtime-ネットワークとレプリケーション) を参照してください。

**デモ版。** `GetNetDriverState`・`ListNetConnections`・`DumpActorReplication` と `RuntimeNetConnectionAddressRead` はデモ版でも提供されます。`DumpReplicatedPropertyValues`・`CompareReplicatedProperties`・`SetNetworkEmulation`・`ResetNetworkEmulation` は含まれず、デモ版ではこれらのコマンドは存在せず `CommandNotFound` を返します。その Capability（`RuntimeReplicatedPropertyValueRead`、`RuntimeNetworkEmulationControl`）はデモ版にも登録されますが、この版では使えない印が付くため、ini で許可しても効果はありません。

**Shipping ビルド。** `SetNetworkEmulation`・`ResetNetworkEmulation`・`RuntimeNetworkEmulationControl` は、エンジンのパケットエミュレーションを使えるビルドでだけ登録されます。Shipping ビルドでは登録されません（`CommandNotFound`）。

**読み取りが表すもの。** 観測は呼び出した瞬間の状態を読み、履歴は持ちません。どのコマンドもコネクションの確立を待ちません。クライアントの参加を待つには、`GetNetDriverState` を繰り返し呼び、サーバーでは `LoggedInConnectionCount`、クライアントでは `Availability` を見てください。コネクション番号（`ConnectionIndex`）は、`ListNetConnections` が並べる NetDriver 内での位置です。サーバーはクライアントとのコネクションを NetDriver が保持する順に並べ、クライアントはサーバーとの 1 本のコネクションを並べます。閉じたコネクションも NetDriver が手放すまでは番号を保つため、その後に番号がずれることがあります。後で番号を使う前に、もう一度一覧を取り直してください。分割画面の 2 人目以降のプレイヤーのコネクションは並びません。NetDriver 名（`NetDriverName`）は大文字小文字を区別せずに照合します。

**Iris。** Iris レプリケーションシステムでは、汎用のレプリケーションシステムにしか無い構造から読む項目があります。それらは `null` で返り、応答に `Limitations: IrisReplicationActive` が付きます: `ListNetConnections` の `ActorChannelCount`、`DumpActorReplication` の `Connections` と `NetworkObjectInfo`、そして `CompareReplicatedProperties` では、実行時に条件が変わりうるプロパティが `NotComparable` になります。`GetNetDriverState` は、NetDriver のどれかが Iris を使っているときに同じ制限事項を付けます。

### 観測（3）— `RuntimeInspect` が必要

| コマンド | 説明 |
|---|---|
| 🆓 `GetNetDriverState` | 対象ワールドの NetDriver を返します。プレイワールド選択子以外のパラメータはありません。`Availability.State` は `Available`・`Connecting`（クライアントが参加中。`Reason: PendingNetGame`）・`Unavailable`（`Reason: NoNetDriver`: ワールドにゲーム用の NetDriver が無い）のいずれかで、`Available` のときは `Reason` を省きます。`RunAsDedicated` と `HasGameViewport` は、ワールドがどんな種類のプロセスで動いているかを示します。`NetDrivers[]` の各項目には、`NetDriverName`・`NetDriverDefinition`・`IsServer`・`ReplicationSystem`（`Generic` / `Iris`）・`ConnectionCount`・`LoggedInConnectionCount`・`MaxClientRate`・`MaxInternetClientRate`・`MaxNetTickRate`・`NetServerMaxTickRate`・`ConnectionTimeoutSeconds`・コネクション全体の `Totals`（`InBytesPerSecond`・`OutBytesPerSecond`・`InPacketsPerSecond`・`OutPacketsPerSecond`、毎秒のパケット数で重み付けした `InLossRatioWeighted` / `OutLossRatioWeighted`、最も悪いコネクションの `InLossRatioMax` / `OutLossRatioMax`、合計に含めた統計の準備ができたコネクションの数 `StatsReadyConnectionCount`）・`MaxPlayers` / `MaxSpectators`（ゲームセッションを持つサーバーのときだけ。それ以外は省きます）・NetDriver の `PacketSimulation` 設定・`EmulationModifiedByUAIP`（`SetNetworkEmulation` がこの NetDriver かそのコネクションの元の設定を保存しているか）・`EmulationDisabledByConfig`（NetDriver が設定でエミュレーションを無視するか）が入ります。ゲーム用の NetDriver が無いワールドも成功で、ほかの NetDriver は並び、理由を `Availability` で示します。応答と成果物は同じ内容です |
| 🆓 `ListNetConnections` | 1 つの NetDriver（`NetDriverName`、既定 `GameNetDriver`）のコネクションを、ページ単位（`StartIndex`、`MaxEntries`）で返します。各項目には、`ConnectionIndex`・`Direction`（`ToClient` / `ToServer`）・`ConnectionState`・`ClientLoginState`・`LoggedIn`・`PlayerController`・`PlayerState`・`ConnectedSeconds`・`LastReceiveAgeSeconds`・`StatsReady`・`RttMs`・`RawPingMs`・`PlayerPingMs`・`JitterMs`・`InLossRatio`・`OutLossRatio`・`InLossRatioAvg`・`OutLossRatioAvg`・`InBytesPerSecond`・`OutBytesPerSecond`・`InPacketsPerSecond`・`OutPacketsPerSecond`・累計の `InTotalBytes`・`OutTotalBytes`・`InTotalPackets`・`OutTotalPackets`・`InTotalPacketsLost`・`OutTotalPacketsLost`・`CurrentNetSpeedBytesPerSecond`・`QueuedBits`・`IsNetReady`・`OpenChannelCount`・`ActorChannelCount`・コネクションに実際に効いている `PacketSimulation`・`AddressKind`（`Loopback`・`Private`・`Public`、アドレスが 4 バイトでも 16 バイトでもないときは `Unknown`）が入ります。生の IP アドレスとポートである `RemoteAddress` は、`IncludeRemoteAddress` が `true` のときだけ書きます。`StatsReady` が false のあいだは、往復時間・ジッター・4 つの損失率・4 つの毎秒の値が `null` です。`RttMs` は直近の統計期間の平均で、次の期間が終わるまでは前の値を保ちます。累計のカウンターはエンジン内で 32 ビット整数のため、長いセッションでは一周することがあります。成果物には、ページ全体と `TotalCount`・`ReturnedCount`、残りがあるあいだは `NextStartIndex` が入ります。応答には同じ項目とページの先頭 50 件のコネクションが入り、ページにそれより多く入っているときは `Truncated: true` です。ゲーム用の NetDriver が無いワールドでは、`NetDriverName` を省いたときは空の一覧で成功し、理由を `Availability` で示します |
| 🆓 `DumpActorReplication` | 1 つのアクター（`ActorIdentifier`）のレプリケーション設定と、その送信についてサーバーが把握している状態を返します。`Actor` には `Name`・`Path`・`Class` が入ります。`Replication` には `Replicates`・`LocalRole`・`RemoteRole`・`NetOwner`・`HasOwningConnection`・`NetDormancy`・`NetUpdateFrequency`・`MinNetUpdateFrequency`・`NetCullDistance`（二乗ではなく距離そのもの）・`NetPriority`・`AlwaysRelevant`・`OnlyRelevantToOwner`・`IsNetStartupActor`・`ReplicateMovement` が入ります。`Properties[]` にアクターの、`Components[]` にレプリケートされる各コンポーネントの、レプリケートされるプロパティが並び、それぞれ `Name`・`Type`・`DeclaredBy`・`ArrayDim`・`DeclaredCondition`（`COND_` を除いた条件名）・`DeclaredRepNotifyCondition`（`OnChanged` / `Always`）・`RepNotifyFunction`（無いときは `null`）・`PushBased` を持ちます。サーバーでは、`Connections[]` がコネクションごとに、アクターチャンネルが開いているか（`ActorChannelOpen`）、見つかった変更をまだ送っていないか（`HasUnsentComparedChanges`）、アクター自身のどのプロパティが非アクティブか（`InactiveProperties`。エンジンが評価するまでは `null`）、直前の更新が空だったか（`LastUpdateEmpty`）を示し、`NetworkObjectInfo` に `NextUpdateTime`・`LastNetReplicateTime`・`PendingNetUpdate`・`DormantConnectionCount` が入ります。`Connections` と `NetworkObjectInfo` は、クライアント、Iris、NetDriver の無いワールド（理由は `Availability`）では `null` です。`HasUnsentComparedChanges: false` は、クライアントが同期していることを意味しません。ライフタイムプロパティに登録されていないレプリケート対象のプロパティは `DeclaredCondition: null` で、応答に `Limitations: PropertyMissingFromLifetimeProps` が付きます。`MaxProperties` はアクターとコンポーネントのプロパティを合わせた件数を、`MaxConnections` はコネクションの件数を制限し、切った一覧は `PropertiesTruncated` / `TotalPropertyCount` または `ConnectionsTruncated` / `TotalConnectionCount` を報告します。ページングはありません。応答と成果物は同じ内容です |

### プロパティの値の観測（2）— `RuntimeInspect` と `RuntimeReplicatedPropertyValueRead` が必要

デモ版では提供されません。

| コマンド | 説明 |
|---|---|
| `DumpReplicatedPropertyValues` | 選んだワールドで、1 つのアクター（`ActorIdentifier`）とレプリケートされる各コンポーネントの、レプリケートされるプロパティ（レプリケーション指定のあるプロパティだけ）の値を返します。クライアントワールドではクライアントが受け取った値なので、サーバーワールドとクライアントワールドで呼べば両者を並べて見られます。`Actor` には `Name`・`Path`・`Class` が入り、アクターのプロパティは `Properties[]`（`Name`・`Type`・`Value`）に、各コンポーネントのプロパティは `Components[]` のその項目（`Name` と同じ項目）に入ります。長い文字列・大きなコンテナ・入れ子の構造体は切り詰めます。各オブジェクトは `PropertiesTruncated`・`PropertiesOmitted`・`TotalPropertyCount` と、サイズの予算で止まったときは `StopReason`（`PerObjectBudget`・`TotalBudget`・`ExternalBudget`）を報告し、どれかのオブジェクトを切った、またはプロパティを省いたときは最上位の `Truncated` が `true` です。64 ビット整数は、絶対値が 2^53 を超えて JSON の数値では正確に表せないときだけ文字列で書きます。±2^53 ちょうどは数値のままです。ワールドに NetDriver が無くても、`Availability.State: Unavailable`（`Reason: NoNetDriver`）を添えて値を返します。応答と成果物は同じ内容です。⚠️ **値には `PlayerState` のレプリケートされる `UniqueId`（プラットフォームのアカウント識別子）やプレイヤー名が入りえます** — [安全性と Capability](safety.md#runtime-ネットワークとレプリケーション) を参照してください |
| `CompareReplicatedProperties` | サーバーワールドのアクターのレプリケートされるプロパティを、1 つのクライアントが受け取った同じアクターと比べ、アクターとレプリケートされるコンポーネントのプロパティごとに `Equal`・`Different`・`NotComparable`（理由 `Reason` 付き）を返します。値は返しません。プレイワールド選択子は**クライアント**ワールドを、`ActorIdentifier` は**サーバー**ワールドのアクターを指します。サーバーワールドは、このプロセス内でただ 1 つのリッスンサーバーまたは専用サーバーでなければなりません（Play-in-Editor の **Run Under One Process**）。下の [比較結果の読み方](#比較結果の読み方) を参照してください |

### パケットエミュレーション（2）— `RuntimeNetworkEmulationControl` が必要

デモ版と Shipping ビルドでは提供されません。

| コマンド | 説明 |
|---|---|
| `SetNetworkEmulation` | 対象プレイワールドの NetDriver の、または `ConnectionIndex` を指定したときはそのコネクションの、パケットエミュレーション設定（遅延・損失・ジッター・重複・順序入れ替え）を変更します。変わるのは指定した項目だけで、ほかの項目は今の値を保ちます。`ConnectionIndex` を省くと NetDriver 全体の設定を変え、すべてのコネクションへ写します。最初の変更の前にあった設定は保存され、`ResetNetworkEmulation` で戻せます。変更は、戻すか NetDriver が破棄される（プレイセッションの終了時、またはクライアントが別のマップへ移動して再接続したとき）まで残ります。応答には `Availability`・`Target`（`PIEInstance`・`NetDriverName`、指定したときは `ConnectionIndex`）・`Before` と `After`（読み取り専用の `PktFrameDelay`・`PktBufferBloatInMS`・`PktIncomingFrameDelay`・`PktIncomingBufferBloatInMS`・`PktLossMinSize`・`PktLossMaxSize` を含む、エンジンの設定の全項目）・`Limitations[]` が入ります。下の [パケットエミュレーション](#パケットエミュレーション) を参照してください |
| `ResetNetworkEmulation` | NetDriver（`NetDriverName`、既定 `GameNetDriver`）とそのすべてのコネクションを、最初の `SetNetworkEmulation` の変更の前に保存した設定へ無条件に戻します。その後にコンソールから行った変更も失われます。1 つのコネクションだけを戻す方法はありません。応答には `Availability`・`NetDriverName`・`Restored[]`（NetDriver が先頭で、続いてコネクション。それぞれ `Scope`（`Driver` / `Connection`）、コネクションの `ConnectionIndex`（もう番号が付いていないときは `null`）、`After`）・`Discarded`（NetDriver やコネクションがもう無いために捨てた保存項目の数。以前の呼び出しがすでに捨てていることもあります）・`Limitations[]`（NetDriver そのものを戻したときは `ForcedPacketSettingsRemains`）が入ります。戻すものが無いときは、空の `Restored` で成功します: `NetDriverName` を省いた、ゲーム用の NetDriver が無いワールド、一度も変更していない NetDriver、すでに終わったプレイセッションで保存した設定、のいずれかです |

#### パラメータ

| パラメータ | コマンド | 意味 |
|---|---|---|
| `NetDriverName` | `ListNetConnections`、`SetNetworkEmulation`、`ResetNetworkEmulation` | `GetNetDriverState` が並べる NetDriver の名前。1〜256 文字で、大文字小文字を区別せずに照合します。既定 `GameNetDriver`。明示した名前をワールドが持たないときは `NotFound` で、メッセージにワールドの NetDriver を列挙します |
| `StartIndex` | `ListNetConnections` | 0 から int32 の最大値までの整数、既定 0。ページの最初のコネクション。コネクションの数以上の値は空のページを返します |
| `MaxEntries` | `ListNetConnections` | 1〜500 の整数、既定 50。ページに入れるコネクションの数 |
| `IncludeRemoteAddress` | `ListNetConnections` | 真偽値、既定 `false`。`RemoteAddress` を書くか。`true` には `RuntimeNetConnectionAddressRead` が必要で、プレイワールドを探す前に判定します |
| `ActorIdentifier`（必須） | `DumpActorReplication`、`DumpReplicatedPropertyValues`、`CompareReplicatedProperties` | アクターのラベルまたはオブジェクト名（1〜256 文字）。[読むアクターの選び方](#読むアクターの選び方) を参照 |
| `MaxProperties` | `DumpActorReplication`、`CompareReplicatedProperties` | 1〜1024 の整数、既定 256。`DumpActorReplication` ではアクターとコンポーネントのプロパティを合わせた件数を、`CompareReplicatedProperties` では `Properties` の一覧だけを制限し、比較と `Summary` はすべてのプロパティを対象にします |
| `MaxConnections` | `DumpActorReplication` | 1〜256 の整数、既定 16 |
| `ConnectionIndex` | `SetNetworkEmulation` | 0 から int32 の最大値までの整数で、`ListNetConnections` と同じ番号付け。省くと NetDriver 全体を変更します。NetDriver が持たない番号は `NotFound` です |
| `PktLag`、`PktLagVariance`、`PktLagMin`、`PktLagMax`、`PktIncomingLagMin`、`PktIncomingLagMax`、`PktJitter` | `SetNetworkEmulation` | ミリ秒単位の整数、0〜10000 |
| `PktLoss`、`PktIncomingLoss`、`PktDup` | `SetNetworkEmulation` | パーセント単位の整数、0〜100 |
| `PktOrder` | `SetNetworkEmulation` | 真偽値。送信するパケットの順序を入れ替えます |
| `TargetNetRole` / `TargetPIEInstance` | すべて | [実行時コマンドの対象プレイワールドを指定する](#実行時コマンドの対象プレイワールドを指定する) を参照。`CompareReplicatedProperties` ではクライアントワールドを指します |

`SetNetworkEmulation` には、エミュレーションの項目が少なくとも 1 つ必要です。最小値が最大値を超える（`PktLagMin` / `PktLagMax`、`PktIncomingLagMin` / `PktIncomingLagMax`）と `InvalidParams` で、片方だけを指定したときはもう片方の今の値と比べます。真偽値は JSON の真偽値、上限値は JSON の整数でなければならず、それ以外の型・空の文字列・未知のキー・範囲外の値は `InvalidParams` で、何も変更しません。

#### 読むアクターの選び方

`ActorIdentifier` は、ラベル（エディタビルドのとき）またはオブジェクト名が文字列と大文字小文字を区別せずに完全一致するアクターに一致します。部分一致は受け付けません。完全一致するものが無いときは `NotFound` で失敗し、名前かラベルにその文字列を含むアクターを最大 10 件、メッセージで候補として示します。完全一致するアクターが複数あるときは `ExecutionFailed` で失敗します。1 つのアクターだけに一致する識別子を指定してください。

#### すべての応答に含まれるフィールド

| フィールド | 意味 |
|---|---|
| `CapturedAt` / `Frame` | 状態を読んだ時刻（ISO 8601、UTC）と、そのときのエンジンのフレーム番号 |
| `NetMode` / `WorldContext` / `PIEInstance` | 読んだワールド。`CompareReplicatedProperties` ではクライアントワールドで、サーバーワールドは `ServerWorld` に入ります |
| `Availability` | `CompareReplicatedProperties` 以外のすべて: `State`（`Available`・`Connecting`・`Unavailable`）と、`Available` 以外のときは `Reason`（`PendingNetGame`・`NoNetDriver`） |
| `Limitations[]` | 返した内容に関する注意のコード（下を参照）。`DumpReplicatedPropertyValues` にはありません |

#### Limitations のコード

| コード | コマンド | 意味 |
|---|---|---|
| `IrisReplicationActive` | `GetNetDriverState`、`ListNetConnections`、`DumpActorReplication`、`CompareReplicatedProperties` | Iris を使っている。上の **Iris** で挙げた項目が `null` または比較不能になる |
| `NetTestDisabledInBuild` | `GetNetDriverState`、`ListNetConnections` | ビルドにパケットエミュレーションの機能が無いため、`PacketSimulation`（と `EmulationDisabledByConfig`）が `null` |
| `LossRatioDenominatorsDiffer` | `GetNetDriverState`（常に） | 受信の損失率は受信したパケットと失ったパケットの合計を、送信の損失率は確認応答を受けたパケットを分母にしている。両者を直接比べないこと |
| `PropertyMissingFromLifetimeProps` | `DumpActorReplication`、`CompareReplicatedProperties` | レプリケーション指定があるのにライフタイムプロパティに登録されていないプロパティがあり、その条件が分からない。エンジンはこのプロパティを送らない |
| `CustomActiveStateNotObserved` | `CompareReplicatedProperties`（常に） | ゲームはカスタムのアクティブ状態でプロパティの送信を止められるが、それは観測していないため、そうしたプロパティも `Different` と報告されうる |
| `DriverWideChangeOverwritesConnection` | `SetNetworkEmulation` | 1 つのコネクションに対して変更した。その後の NetDriver 全体への変更（このコマンドでも、コンソールの `Net PktLag=...` などでも）で上書きされる |
| `ForcedPacketSettingsRemains` | `SetNetworkEmulation`、`ResetNetworkEmulation` | NetDriver 全体を変更した、または戻した。エンジンは NetDriver が破棄されるまで、戻した後も、プロジェクト設定から設定を読み直さなくなる |
| `PacketLagSettingIgnored` | `SetNetworkEmulation` | `After` の遅延の項目が 0 ではないが、ほかの項目が優先されるためエンジンはそれを無視する（下を参照） |

#### 比較結果の読み方

`CompareReplicatedProperties` は、まずクライアント側のアクターの複製を探します。見つかれば `Counterpart.Status` は `Resolved` です。見つからないときはコマンドは成功して何も比べず、ステータスで理由を示します: `NotReplicated`（サーバーがアクターのネットワーク識別子を持たない）、`NotReached`（クライアントがまだその識別子を知らない）、`Pending`（クライアントがまだ読み込み中）、`Broken`（クライアントが壊れていると印を付けた）、`Destroyed`（クライアント側の複製がもう有効でない）、`ConnectionNotFound`（ログイン前など、クライアントワールドに対応するサーバー側のコネクションが見つからない）。`Pending` と `Broken` は汎用のレプリケーションシステムでだけ起きます。`Components[]` の各項目は、それぞれ自分の `Counterpart.Status` を持ちます。

応答には `ServerWorld`（`PIEInstance`、`NetMode`）・`ClientWorld`（`PIEInstance`）・`Actor`（`Name`、`ServerPath`）・`ReplicationSystem`・`Counterpart`（`Status`、`ClientPath`）・`Summary`（すべてのプロパティについての `Equal`・`Different`・`NotComparable` の件数）・`Different`・`NotComparable`・`Equal` の順に並べた `Properties[]`（`Name`・`Owner`・`Result`、`NotComparable` のときは `Reason`）・`PropertiesTruncated`・`TotalPropertyCount`・`Limitations[]` が入ります。応答と成果物は同じ内容です。

⚠️ **比較結果は、アクターが「同期している」とは決して言いません。** 比べるのは評価できるプロパティだけで、`Equal` は呼び出した瞬間に 2 つの値が同じだったことしか示しません。`Different` もバグの証明ではありません。値は送信中や、更新頻度・休眠のために正当に遅れますし、ゲームがカスタムのアクティブ状態で送信を止めたプロパティは `Different` と報告されます（`Limitations` には常に `CustomActiveStateNotObserved` が付きます）。独自のネットワークシリアライズを持つ型が `NotComparable` になるのは、プロパティそのものがその型のときだけです。要素がそうした型の配列 — たとえば `TArray<FVector_NetQuantize>` — は値ごとに比べるため、量子化による正当な丸めでも `Different` と報告されることがあります。

評価できないプロパティは、次のいずれかの理由付きで `NotComparable` になります。

| `Reason` | 意味 |
|---|---|
| `InitialOnly` | オブジェクトの生成時に 1 回だけレプリケートされるプロパティ |
| `ConditionUnknown` | 条件が実行時に決まる（カスタムまたはダイナミック）もので、エンジンがこのコネクションについてまだ評価していない。コンポーネントのプロパティと、Iris のときは常にこれになる |
| `ConditionNotApplicable` | 条件がこのクライアントに当てはまらず、プロパティが送られない。ライフタイムプロパティに登録されていないプロパティ（`Limitations: PropertyMissingFromLifetimeProps`）も含む |
| `DeltaSerialized` | 差分でシリアライズされる（Fast Array）ため、比べられる値全体が無い |
| `ObjectReference` | オブジェクト参照で、参照先を 2 つのワールドの間で対応付けられなかった |
| `NestedObjectReference` | コンテナや構造体の中にオブジェクト参照を持つ |
| `CustomNetSerialization` | 独自のネットワークシリアライズを持つ型で、値を正当に丸めることがあり、値が一致しなかった。一致したものは `Equal` になる |
| `ClassMismatch` | サーバー側とクライアント側のオブジェクトのクラスが違う |

**拒否。** クライアントがまだ接続中（`Connecting`）、選んだワールドに NetDriver が無い（`NoNetDriver`）またはクライアントでない（`TargetIsNotClient`）、プロセスにサーバーワールドが無い（`NoServerWorld`）または複数ある（`MultipleServerWorlds`。メッセージにプレイワールドを最大 8 件列挙）ときは、何も保存せず `NotAllowed` で拒否します。`ErrorMessage` はその理由で始まり、`nothing was compared` が続きます。ゲーム用の NetDriver を持たないサーバーワールドは `ExecutionFailed` です。

#### パケットエミュレーション

エンジンは送信側の遅延の項目を次の優先順で読みます。`SetNetworkEmulation` は、無視される項目が 0 でないときに `PacketLagSettingIgnored` を付けます。

1. `PktFrameDelay`（ここでは読み取り専用）が 0 より大きい、または `PktOrder` が有効なときは、`PktLag`・`PktLagVariance`・`PktLagMin`・`PktLagMax`・`PktJitter` を無視します。
2. そうでなく `PktJitter` が 0 でないときは、`PktLagMin` を基準にジッターと揺らぎで広げた遅延を使い、`PktLag` と `PktLagMax` を無視します。
3. そうでなく `PktLag` が 0 でないときは、それを `PktLagVariance` とともに使い、`PktLagMin` と `PktLagMax` を無視します。
4. それ以外は `PktLagMin` から `PktLagMax` の間で遅延を決め、`PktLagVariance` を無視します。

受信側の項目（`PktIncomingLagMin`・`PktIncomingLagMax`・`PktIncomingLoss`）は、これとは独立です。

1 つのコネクションに対する設定は、その後の NetDriver 全体への変更（このコマンドでも、コンソールからでも）で上書きされます（`DriverWideChangeOverwritesConnection`）。NetDriver 全体を変更すると、エンジンはその NetDriver が破棄されるまで、`ResetNetworkEmulation` の後も、プロジェクト設定から設定を読み直さなくなります（`ForcedPacketSettingsRemains`）。

⚠️ **`RuntimeNetworkEmulationControl` の解禁を取り消す前に `ResetNetworkEmulation` を呼んでください。** 戻すにも同じ Capability が必要なため、取り消した後は NetDriver が破棄されるまで変更が残ります。

**成果物の保存。** 成果物を保存する時点では、変更（または復元）はすでに済んでいます。そのため保存に失敗しても、`SetNetworkEmulation` と `ResetNetworkEmulation` は成果物なしで成功します。唯一の例外は、成果物は書けたもののその場所を解決できなかった場合で、このときコマンドは `ExecutionFailed` で失敗し、メッセージに、設定はすでに変更済みで `ResetNetworkEmulation` で戻せること（`ResetNetworkEmulation` では、保存していた設定はすでに戻して破棄したこと）が入ります。

#### 完了通知と監査記録で伏せるもの

生のアドレスとプロパティの値は、呼び出し元にはそのまま返り、成果物にもそのまま保存されます。エディタの完了通知に流す応答の写し（エディタ自身の通知と、コマンドを記録するコード — 監査記録・ログ — が受け取るもの）では伏せます。`ListNetConnections` の `Connections[]` の各 `RemoteAddress` と、`DumpReplicatedPropertyValues` の `Properties[]` と `Components[].Properties[]` の各 `Value` が `"<redacted>"` になります。ほかの項目はそのままです。`IncludeRemoteAddress` を指定しない `ListNetConnections` には伏せるアドレスが無いので、写しは元と同じです。`CompareReplicatedProperties` は値を返さないので、伏せるものはありません。シナリオで、前のステップの応答からアドレスや値を取ったステップは、パラメータと応答の `Data` を伏せて記録されます。`DescribeCommand` はこれらの位置を `SensitiveResponseData` に示します。[機微な値と伏せる場所](#機微な値と伏せる場所) を参照してください。

#### エラー

| ErrorCode | 発生条件 |
|---|---|
| `InvalidParams` | パラメータの型の誤り・空・長すぎる・範囲外・未知。エミュレーションの項目を 1 つも指定しない、または最小値が最大値を超える `SetNetworkEmulation`。`TargetNetRole` / `TargetPIEInstance` を満たせない |
| `CapabilityNotAvailable` | `RuntimeInspect`・`RuntimeReplicatedPropertyValueRead`・`RuntimeNetworkEmulationControl`、または（`IncludeRemoteAddress: true` のときは）`RuntimeNetConnectionAddressRead` が許可されていない。メッセージに名前が付く |
| `PolicyViolation` | 安全ポリシーでその Capability が明示的に拒否されている、または読み取り専用モードで `SetNetworkEmulation` / `ResetNetworkEmulation` を呼んだ |
| `NotAllowed` | プレイワールドが動いていない、または `TargetNetRole` / `TargetPIEInstance` に一致するものが無い。`CompareReplicatedProperties` の拒否（上を参照）。設定でエミュレーションを禁じている NetDriver への `SetNetworkEmulation`（`EmulationDisabledByConfig`） |
| `NotFound` | `ActorIdentifier` に一致するアクターが無い（メッセージに候補が付く）。明示した `NetDriverName` をワールドが持たない（メッセージに NetDriver の一覧が付く）。`NetDriverName` を省いた `SetNetworkEmulation` で、ワールドにゲーム用の NetDriver が無い（スタンドアロンのゲーム）、または NetDriver が持たない `ConnectionIndex` |
| `ExecutionFailed` | 識別子に一致するアクターが複数ある。観測コマンドの成果物を保存できなかった。`CompareReplicatedProperties` のサーバーワールドにゲーム用の NetDriver が無い。`SetNetworkEmulation` / `ResetNetworkEmulation` の成果物は書けたが、その場所を解決できなかった |
| `CommandNotFound` | ビルドが提供していないコマンド: デモ版での値の読み取り・比較・エミュレーションのコマンドと、Shipping ビルドでのエミュレーションのコマンド |

観測コマンドは、成功した呼び出しごとにちょうど 1 つの JSON 成果物を保存し、失敗した呼び出しは何も保存しません。拒否された要求も何も保存しません。

---

## UAIP.Runtime.Mass

プレイワールドの Mass シミュレーションを観測するコマンド群です。エンティティがいくつあるか、どのアーキタイプにまとまっているか、どのプロセッサがどの順で動くか、1 体のエンティティがどの要素の型を持つか、そして許可すればその要素の値が分かります。このモジュールが必要とするのはエンジン同梱の `MassEntity` モジュールだけで、`MassGameplay` プラグインは要らないため、🧩 は付きません。エディタでのみ読み込まれ（ゲームのビルドには含まれません）、デモ版にも含まれません。すべてのコマンドは読み取りだけを行います。シミュレーションの元になるアセットの読み取りと組み立ては [`UAIP.Editor.Mass`](#uaipeditormass-) を参照してください。

6 つのうち 5 つは、エディタ上のプレイワールドの Mass エンティティマネージャーに作用し、[`TargetNetRole` / `TargetPIEInstance`](#実行時コマンドの対象プレイワールドを指定する) を受け付けます。`DumpMassEntitySettings` はエンジンの設定を読むので、パラメータを取りません。

**Capability。** 6 つすべてが `RuntimeInspect`（DefaultAllow）を必要とします。`GetMassEntityFragments` は、フラグメントの値がプロジェクトのデータであるため、`RuntimeMassFragmentValueRead`（DefaultDenied）も必要です。足りない場合は `CapabilityNotAvailable` です。詳細は [安全性と Capability](safety.md#mass-の観測と編集) を参照してください。

**エンティティの指定。** エンティティは、先に返った応答が示した `EntityIndex` と `EntitySerialNumber` の組で指定します（見本は `DumpMassEntityArchetypes` の `SampleEntitiesPerArchetype` で求めます）。プレイワールドについての応答には、観測したワールドを識別する `WorldToken` が付きます。これをそのまま返してください。`GetMassEntityFragments` は必須で、別のワールド（たとえば PIE を再起動した後）について答えることを `Conflict` で断ります。`DescribeMassEntity` は渡されれば検証し、渡されなければ `WorldTokenNotVerified` の制限事項でそれを示します。

**安全点での読み取り。** エンジンの状態が更新の途中かもしれないとき（モーダルダイアログや長い処理がゲームループを止めている、またはワールドがティックの途中）は、何も読まずに、`Availability: NotAtSafePoint` とデータなしで**成功**を返します。これは空のワールドとは別物で、`DescribeMassEntity` / `GetMassEntityFragments` ではエンティティが存在するかどうかも分かりません。もう一度呼んでください。

**出力の上限。** 上限は設定できません。Data は先頭のエントリを、成果物はサイズ予算までの残りを持ちます。上限のある一覧 `<List>`（`Archetypes`・`Processors`・`PrunedProcessors`・`Observers`・`Elements`・`ProcessorCDOs`）には次のキーが付きます。

- `<List>TotalCount` — 切り捨て前の件数。
- `<List>Truncated` — **応答が返した結果（Data と成果物を合わせたもの）の外に**まだ要素がある。Data と成果物で同じ値になる。続きのページがある（`NextStartIndex`）とき、または総数が二つの一覧の大きい方より多いときに true。成果物が全件を持っていれば、Data がどれだけ短くても false のまま。
- `<List>DataEntriesTruncated` — Data のみ。Data の件数が成果物の件数より少ないとき true。true のとき、残りは成果物にある。
- `ArtifactTruncated` / `ArtifactTruncationIndex` — 成果物がサイズ予算で止まったこと（とその位置）。`NextStartIndex` は変わらない。

例: アーキタイプが 60 件あり、続きのページが無く、成果物が 60 件すべてを持つ場合は、`ArchetypesTruncated` は false、Data の `ArchetypesDataEntriesTruncated` は true になります。成果物が予算で止まっても Data が全件を持つ場合は、`ArchetypesTruncated` は false、`ArtifactTruncated` は true です。

**曖昧な要素名。** 短い要素名が複数の型に一致すると、`GetMassEntityCount`・`DumpMassEntityArchetypes`・`GetMassEntityFragments` は `InvalidParams` で失敗します。その失敗応答の `Result` には、`AmbiguousName`（指定された名前）、`Candidates`（候補の型パス。並べ替え済み、最大 10 件）、`TotalCandidateCount`（一致した型の総数。載せた 10 件より多いことがある）が載ります。候補の型パスのどれかで指定し直すと、曖昧さが解けます。

**デバッグ用インターフェース。** `GetMassEntityCount`・`DumpMassEntityArchetypes`・`DumpMassProcessorGraph` は Mass のデバッグ用インターフェースを必要とします。ビルド構成によっては含まれません（Shipping ビルドのように `WITH_MASSENTITY_DEBUG` が 0 のエンジンビルド）。その場合、これらは `Available: false`（`UnavailableDetail: BuildConfiguration`）で、理由を示すメッセージ付きで一覧に出ます。

**Mass が動いていないとき。** プロジェクト設定やコンソール変数（たとえば `mass.RuntimeSubsystemsEnabled`）でプレイワールドの Mass のサブシステムが無効になっていると、それを必要とするコマンドは、設定の名前を示した `PreconditionFailed` で断られます。`DumpMassEntitySettings` は影響を受けません。

**TEDS を無効にしているとき。** エディタの Typed Elements Data Storage（TEDS）が有効（既定）なら、このモジュールによる新たな副作用はありません。TEDS を無効にしていると、このモジュールの読み込みでエディタが `MassEntity` モジュールを読み込み、エディタ側のワールド（エディタのワールドなど）に Mass のサブシステムが作られることがあります。影響はエディタの中に限られ、ゲームには及びません。

| コマンド | 説明 |
|---|---|
| `DumpMassEntitySettings` | エンジンの Mass 設定を JSON 成果物として保存する。`ChunkMemorySize`（エンティティメモリ 1 チャンクのバイト数）、`ProcessingPhases`（`Phase` と `PhaseGroupClassPath`。設定が並べる順）、設定が集めたプロセッサクラスの `ProcessorCDOs`（`ClassPath`・`Phase`・`Group`/`Before`/`After` 付きの `ExecutionOrder`・`ExecutionFlags`・`AutoRegisterWithProcessingPhases`）。設定はクラスのデフォルトオブジェクトから読むため、プレイワールドは不要で、応答に `WorldToken` は付かず、`Availability` は常に `Available`。Data は先頭 50 件のプロセッサクラスと `ProcessorCDOsTotalCount`・`ProcessorCDOsTruncated`・`ProcessorCDOsDataEntriesTruncated` を持つ。読み取り専用。`RuntimeInspect` が必要 |
| `GetMassEntityCount` | 対象プレイワールドのエンティティ数を数える。`TotalEntityCount`（ワールド全体）、`MatchingEntityCount`、`MatchingArchetypeCount`、`Archetypes`（条件に合うアーキタイプごとの `ArchetypeId` と `EntityCount`。多い順）。`RequiredElements` は列挙した要素の型をすべて持つアーキタイプに絞り、`ExcludedElements` はどれかを持つものを除く。名前は `TransformFragment` のような短い名前、または `/Script/MassCommon.TransformFragment` のような完全なパスで、不明・曖昧・要素の型でない名前は断られる（1 つのリストにつき 64 個まで、各 512 文字まで）。エンティティが無いワールドは件数 0 になる。Data は先頭 50 件のアーキタイプを持つ（`ArchetypesTruncated`・`ArchetypesDataEntriesTruncated`）。読み取り専用。`RuntimeInspect` が必要 |
| `DumpMassEntityArchetypes` | 対象プレイワールドのアーキタイプを 1 ページずつ一覧する。各アーキタイプに `ArchetypeId`・`Composition`（各要素の `Kind` と `Type`）・`EntityCount`・`ChunkCount`・`EntitiesPerChunk`・`AllocatedSizeBytes`・`WastedEntityMemoryBytes`・`BytesPerEntity`・`DebugNames`・`SampleEntities`（`SampleEntitiesPerArchetype` 個までのエンティティの `Index` と `SerialNumber`。既定では無し）。`RequiredElements` / `ExcludedElements` の絞り込みは上と同じ。`StartIndex`・`MaxArchetypes`（1〜500、既定 50）・`SampleEntitiesPerArchetype`（0〜16）で、安定した順序の中をページ送りする。応答は `TotalArchetypeCount`・`TotalEntityCount`（絞り込み前）・`MatchingArchetypeCount`・`NextStartIndex`（アーキタイプが残っているときだけ）・`ArchetypesTruncated`・Data のみ `ArchetypesDataEntriesTruncated` を持つ。ページの間にアーキタイプが変わることがある。読み取り専用。`RuntimeInspect` が必要 |
| `DumpMassProcessorGraph` | 対象プレイワールドのプロセッサグラフ。処理フェーズごとに、実行される順のプロセッサ、続いてエンジンが除いたプロセッサと、要素の追加・除去を監視するプロセッサ。各プロセッサは、クラス、位置、自分より前に走るべきプロセッサ、宣言しているグループ・順序・実行フラグ、クエリの要件（要素の型と種類、読み取りか読み書きか、エンティティが持つ必要があるか）を持つ。Data は先頭のエントリを、成果物は残りを持ち、各フェーズの `Processors` と `PrunedProcessors`・`Observers` には「出力の上限」のフラグが付く。Mass デバッガーの処理環境が無いワールドは、制限事項 `ProcessingEnvironmentNotFound` 付きの空のグラフを返す。これはプロセッサが無いワールドとは別物。読み取り専用。`RuntimeInspect` が必要 |
| `DescribeMassEntity` | 1 体のエンティティがどの要素の型を持つかを、値を読まずに返す。所属するアーキタイプのハッシュと、Fragment・Tag・Shared Fragment・Const Shared Fragment・Chunk Fragment を、種類と型パスの組で返す。UE 5.8 以降では、sparse Fragment（型のみ）も列挙し、常に `SparseTagsNotListed` を返す。エンティティ単位の sparse Tag は列挙できないので、Tag の一覧が空でも持っていないという意味ではない。要素の一覧には「出力の上限」のフラグ（`ElementsTotalCount`・`ElementsTruncated`・`ElementsDataEntriesTruncated`）が付く。`EntityIndex` と `EntitySerialNumber` が必要で、`WorldToken` は任意。エンティティが存在しないと `NotFound`。読み取り専用。`RuntimeInspect` が必要。値は `GetMassEntityFragments` で読む |
| `GetMassEntityFragments` | 1 体のエンティティの Fragment・Shared Fragment・Const Shared Fragment の値。`EntityIndex`・`EntitySerialNumber`・`WorldToken` が必要。`ElementTypes`（最大 64 個）で、名前を挙げた型だけに読み取りを絞る。Tag と Chunk Fragment は 1 体のエンティティについて読む値が無いので `InvalidParams`、エンティティが持たない型は `MissingRequestedElements` に載る。`Elements` には「出力の上限」のフラグ（`ElementsTotalCount`・`ElementsTruncated`・`ElementsDataEntriesTruncated`）が付く。`Elements` の各エントリは `Kind`・`Type` を持ち、読めた場合は `Value`（構造体のメンバーの一覧。`Name`・`Type`・`Value`）、1 つの Fragment の予算（16 KiB）で切ったときは `ValueTruncated`、省いたときは `ValueOmittedReason` を持つ。1 回の応答の値は 256 KiB の予算を共有し、尽きた後の要素は型だけと `ValueBudgetExceeded` を返す。`Limitations` が省いたものを示す。強参照のオブジェクトは読まない（`ObjectReferenceOmitted`）、実行時に型が決まる構造体は展開しない（`NestedInstancedStructNotExpanded`）、リフレクションされないメンバーは出力しない（`NonReflectedMembersOmitted`）、展開が 4 段を超える入れ子の構造体は型名だけを返す（`StructDepthTruncated`。`Detail` は要素の型パスで、型ごとに 1 回。値の中に印は無いので、打ち切られたかどうかは `Limitations` で判断する）、UE 5.8 以降の sparse 要素は型のみ（`SparseElementValuesNotRead`）。読み取り専用。`RuntimeInspect` と `RuntimeMassFragmentValueRead` が必要 |

**エラー。**

| ErrorCode | 発生条件 |
|---|---|
| `NotAllowed` | プレイワールドが動いていない、または `TargetNetRole` / `TargetPIEInstance` に合うものが無い |
| `PreconditionFailed` | プレイワールドで Mass が無効になっている（プロジェクト設定やコンソール変数） |
| `NotFound` | エンティティが存在しない、破棄済み、またはシリアル番号がインデックスに属さない |
| `Conflict` | `WorldToken` が今観測しているワールドを指していない |
| `InvalidParams` | 不明・曖昧・要素の型でない名前、`ElementTypes` の Tag や Chunk Fragment、範囲外のパラメータ |
| `CapabilityNotAvailable` / `PolicyViolation` | 必要な Capability が与えられていない / セーフティポリシーで拒否されている |

---

## シナリオ実行ルート

シナリオは単一コマンドではなく、複数コマンドを順序付きリストとして 1 リクエストで送信する独立ルートです。詳細は [シナリオ実行](scenario.md) を参照してください。利用可能なエントリポイント：

| トランスポート | エントリポイント |
|---|---|
| MCP | `uaip_run_scenario` |
| HTTP | `POST /uaip/scenarios`（`-uaip-enable-scenario` 必須） |
| WebSocket | フレーム `Type: "ScenarioRequest"` |
| CLI | `-uaip-scenario=<json>` / `-uaip-scenario-file=<path>` |

シナリオの各ステップは `uaip_execute` と同じ `CommandDispatcher` を通って実行されるため、Capability と SafetyPolicy のルールが同様に適用されます。

---

> スキーマやパラメータの詳細は本ページでは意図的に省略しています。任意のコマンドの完全スキーマは `{"Command": "UAIP.Core.DescribeCommand", "Params": {"Name": "<コマンド名>"}}`（HTTP / WebSocket / CLI）または `uaip_describe_command(CommandName="<コマンド名>")`（MCP）（引数名は前者が `Name`、後者が `CommandName` で異なります） で取得してください。

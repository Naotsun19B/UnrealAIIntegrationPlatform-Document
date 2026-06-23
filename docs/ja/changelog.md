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

現行バージョンは **1.0.0**（1.x.y 系列の初回エントリ）で、UAIP は **Fab で製品版として公開済み**（[リスティング](https://www.fab.com/listings/0eedf909-00ac-4d95-b109-8fda51800fff)）です。

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

> **現在 `next` ブランチを閲覧中です。** このページは次回 Fab リリースに向けて開発中のコンテンツを追跡しています。最終リリース版は [`master` ブランチの更新履歴](https://github.com/Naotsun19B/UnrealAIIntegrationPlatform-Document/blob/master/docs/ja/changelog.md) を参照してください。

### Unreleased

プラグインリポジトリには取り込み済みですが、Fab 未リリースの変更です。

#### UAIP Plugin

**追加**

- **Sandbox 編集統合**（`UAIPEditorSandbox` モジュール、**Pro 版限定** — `FileSandbox` プラグイン必須、デモ版では利用不可）: AI エージェントが FileSandbox セッションにアセット変更を仮置きし、人間が確認後にコミットまたはリバートできるようになりました。`UAIP.Editor.Sandbox` 配下に 6 コマンド（`BeginSandboxSession`、`EndSandboxSession`、`GetSandboxStatus`、`GetSandboxChanges`、`CommitSandboxChanges`、`RevertSandboxChanges`）と、4 Capability（`SandboxObserve`（DefaultAllow）、`SandboxSessionControl`、`SandboxPersist`、`SandboxRevert`（いずれも DefaultDenied））を追加しました。読み取り専用の observe 系コマンド（`GetSandboxStatus`・`GetSandboxChanges`）を含む全 6 コマンドが `FileSandbox` プラグインを必要とし、デモ版モジュールホワイトリストには含まれません。

**変更**

- **Niagara モジュールが UE 5.7 に対応**: `UAIP.Editor.Niagara` および `UAIP.Runtime.Niagara` 配下の全コマンド（UAIP ネイティブ 36 本 + Toolset ブリッジ）が UE 5.7 で利用可能になりました。従来 UE 5.7 ではモジュール全体が未登録となり、全コマンドが `CommandNotFound` を返していました。
- **Niagara `default_value` が適用されるように**: `AddSetParametersModule` および `AddSetParameterEntry` で `default_value` フィールドが一般的な型（float / int / bool / `UScriptStruct`）について解析・適用されます。従来は指定値にかかわらず型のデフォルト値でエントリが作成されていました。

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

![UE Version](https://img.shields.io/badge/Unreal%20Engine-5.7%20%2F%205.8-0e1128?logo=unrealengine&logoColor=white)
[![License: Fab Standard License (Fab EULA)](https://img.shields.io/badge/License-Fab%20Standard%20License%20%28Fab%20EULA%29-blue)](https://www.fab.com/ja/eula)
[![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/Naotsun_UE?style=social)](https://twitter.com/Naotsun_UE)

**[English](../../README.md)**

<p align="center">
  <img src="../../images/hero-banner.png" alt="Unreal AI Integration Platform" width="100%">
</p>

<video src="https://github.com/user-attachments/assets/58e03ed1-6dc5-4068-8789-4b3e81bbb1f8" autoplay loop muted playsinline controls width="100%"></video>

<p align="center">
  <a href="https://youtu.be/o-33jgYLF0A">
    <img src="https://img.youtube.com/vi/o-33jgYLF0A/maxresdefault.jpg" alt="YouTube でローンチトレーラーを見る" width="100%">
  </a>
</p>

# UnrealAIIntegrationPlatform

<!--ts-->
   * [概要](#概要)
   * [動作環境](#動作環境)
   * [インストール](#インストール)
   * [セットアップ](#セットアップ)
   * [ドキュメント](#ドキュメント)
   * [ライセンス](#ライセンス)
   * [作者](#作者)
   * [更新履歴](#更新履歴)
<!--te-->

## 概要

**UnrealAIIntegrationPlatform (UAIP)** は、AI エージェントから UE Editor と Runtime を **操作・観測・実行・検証** するための Unreal Engine プラグインです。

Claude Code・Codex CLI・Cursor・Windsurf・GitHub Copilot といった AI ツールが **Model Context Protocol (MCP)** 経由で接続し、意味レベルのコマンドを発行できます。座標クリックや壊れやすい UI スクリプトに頼る必要はありません。

主な機能：
- **Editor 操作** — アセットの開閉・保存、Blueprint 編集、アクター操作、Automation Test の実行、Sequencer の制御まで、540 以上の UAIP コマンド（公式 UE 5.8 [Toolset](glossary.md#toolset--toolset-bridge) への 190+ ブリッジコマンドを含め合計 730+）で Editor のほとんどの機能をカバー
- **視覚的・構造的な観測** — 任意の Editor タブやビューポートのスクリーンショット取得、ワールド状態 / Slate ウィジェットツリー / エディタ状態の JSON ダンプを [Artifact](glossary.md#artifactアーティファクト) として返却
- **Runtime / [PIE](glossary.md#pieplay-in-editor) 制御** — PIE の開始と停止、アクターのスポーン、入力の注入、Gauntlet テストの実行、アクタープロパティのアサート
- **[シナリオ](glossary.md#scenarioシナリオ)実行** — 複数のコマンドを順序付きリストとして一括送信。失敗時の中断・リトライ・ステップごとのタイムアウトに対応
- **マルチ Transport** — [MCP](glossary.md#mcpmodel-context-protocol)・HTTP・WebSocket・CLI のいずれからでも操作可能
- **Safety & Capability Policy** — [セッション](glossary.md#sessionセッション)単位の [Capability](glossary.md#capability) ゲートと、プロセス単位の [SafetyPolicy](glossary.md#safetypolicy) スイッチで権限を細かく制御

<video src="https://github.com/user-attachments/assets/1e4f4ab9-8cf1-4a0a-ba69-bee81b322a31" muted controls width="100%"></video>

### アーキテクチャ

```mermaid
flowchart LR
    AI["AI クライアント<br/>Claude Code / Codex / Cursor / Windsurf / Copilot"]
    Bridge["MCP Bridge<br/>(thin_proxy.py)"]
    Editor["UE Editor<br/>UAIP プラグイン"]
    Artifacts[("Artifacts<br/>PNG / JSON / Log / Report")]

    AI <-->|MCP| Bridge
    Bridge <-->|HTTP /mcp| Editor
    Editor -->|生成| Artifacts
    Artifacts -.->|/uaip/artifacts/*| Bridge
```

MCP Bridge は AI クライアントからのツール呼び出しを、エディタへの HTTP リクエストへと変換します。キャプチャやダンプ系のコマンドは結果を Artifact として書き出し、Bridge は ID で AI クライアントへ返却します。HTTP API・WebSocket・CLI を直接使う方法は [接続方法](connections.md) を参照してください。

## 動作環境

対象バージョン : UE 5.7 / 5.8  
対象プラットフォーム : Windows  
Python : 3.10 以降（MCP Bridge に必要）

## インストール

UAIP には **デモ版** と **製品版** の 2 つの配布形式があります。

### デモ版（GitHub Releases から無償）

機能制限付きのバイナリ配布で、AI エージェントをレビューやテストのワークフローに組み込むのに十分な機能（MCP 接続・観測・PIE 制御・シナリオ実行・UI 自動化・アサーション）をそろえています。詳しいコマンド一覧と制限事項は [デモ版ガイド](demo.md) を参照してください。

1. このリポジトリの [Releases](../../../releases) から `UAIP-Demo-UE<バージョン>-Win64.zip` をダウンロード
2. zip を展開し、UE プロジェクトの `Plugins/UnrealAIIntegrationPlatform/` に配置
3. プロジェクトを開き、**編集 > プラグイン** で **UnrealAIIntegrationPlatform** が有効になっているか確認

### 製品版（Fab で公開中）

完全版（全トランスポート・Editor / Runtime の編集機能・透かしなし）は **[Fab で公開中](https://www.fab.com/listings/0eedf909-00ac-4d95-b109-8fda51800fff)** です。Fab の Code Plugin 形式でソース付き配布です。Fab からインストールして、同じく `Plugins/UnrealAIIntegrationPlatform/` に配置してください。

## セットアップ

MCP Bridge は UE Editor と AI クライアントをつなぐ Python プロキシです。**プラグイン本体とは別配布** で、このリポジトリの [Releases](../../../releases) から `UAIP-MCPBridge-<version>.zip`（UE バージョン非依存）をダウンロードします。

1. `UAIP-MCPBridge-<version>.zip` をダウンロードして任意の場所に展開
2. 展開したフォルダから `install/install.ps1`（Windows / PowerShell の実行ポリシー制限がある場合は `install/install.cmd` ラッパー）を実行し、対話プロンプトに `.uproject` パスまたはエンジンパスを入力。インストーラは Bridge を `<UAIP-parent>/UAIPMCPBridge/`（UAIP プラグインと同階層）に展開し、Python venv を作成し、MCP クライアント登録用スニペットを表示します
3. 表示されたスニペットを AI クライアントの MCP 設定ファイルに貼り付け
4. AI に「UAIP の HealthCheck を実行して」と聞いて動作確認

5 分で動かす最短ルートは [クイックスタート](quickstart.md) を、クライアント別の詳細な設定は [接続方法](connections.md) を参照してください。インストーラの詳細は Bridge zip 同梱の `install/SETUP.md` を参照。

## ドキュメント

| ドキュメント | 内容 |
|---|---|
| [クイックスタート](quickstart.md) | インストールから最初のコマンド実行まで 5 分 |
| [接続方法](connections.md) | 全トランスポート：MCP Bridge のセットアップ + HTTP / WebSocket / CLI（製品版） |
| &nbsp;&nbsp;↳ [Claude Code](clients/claude-code.md) / [Codex CLI](clients/codex.md) / [Claude Desktop](clients/claude-desktop.md) / [Cursor](clients/cursor.md) / [Windsurf](clients/windsurf.md) / [Copilot](clients/copilot.md) | クライアント別設定 JSON と動作確認手順 |
| [ユースケース](use-cases.md) | 誰が UAIP を何のために使うか — テスト・レビュー・監査・ペアプロ |
| [使用例集 / レシピ集](cookbook.md) | レシピ集 — PIE スモーク・AI レビュー・アセット監査・BP 編集・UI 自動化 |
| [コマンドリファレンス](commands.md) | ドメイン別 730 以上のコマンド一覧 |
| [API リファレンス](api.md) | コマンド完全スキーマ（JSON）— ツール作成・コード生成・バリデーション用 |
| [シナリオ実行](scenario.md) | 複数ステップのコマンド一括実行 |
| [Artifacts（成果物）](artifacts.md) | スクリーンショット・JSON ダンプ・ログの読み方 |
| [Safety & Capabilities](safety.md) | SafetyPolicy と Capability の設定リファレンス |
| [設定リファレンス](config.md) | ini セクション（Session / ArtifactGC / CommandNotification）・CLI 起動フラグ・MCP Bridge `config.json` |
| [セキュリティ](security.md) | 脅威モデル・認証・推奨セキュリティプロファイル |
| [アーキテクチャ](architecture.md) | レイヤー・ディスパッチシーケンス・Capability 決定フロー |
| [デモ版ガイド](demo.md) | デモ版コマンド一覧・制限事項・インストール手順 |
| [FAQ](faq.md) | デモ/Pro・Capability・ワークフロー・CI などのよくある質問 |
| [トラブルシューティング](troubleshooting.md) | エラーコードリファレンスと典型的な失敗パターン |
| [用語集](glossary.md) | Capability・Artifact・Scenario・Toolset 等の定義 |
| [ロードマップ](roadmap.md) | 今後追加予定の機能と開発方針 |
| [更新履歴](changelog.md) | バージョニング方針とリリースごとの変更履歴 |

## ライセンス

本リポジトリの [Releases](https://github.com/Naotsun19B/UnrealAIIntegrationPlatform-Document/releases?q=Demo)（`Demo-v<X.Y.Z>` タグ）で配布するデモバイナリは、リリースアーカイブに同梱の `EULA.txt` に従って提供されます。  
Fab で配布される製品版は [Fab Standard License (Fab EULA)](https://www.fab.com/ja/eula) に基づいて提供されます。  
**MCP Bridge**（本リポジトリの [Releases](https://github.com/Naotsun19B/UnrealAIIntegrationPlatform-Document/releases?q=MCPBridge) で `MCPBridge-v<X.Y.Z>` タグとして配布する `UAIP-MCPBridge-<version>.zip`）は [MIT License](https://opensource.org/licenses/MIT) のもとで提供されます。ライセンス全文はアーカイブ内に `LICENSE` として同梱されています。  
特に明記がない限り、本リポジトリ内のドキュメントの著作権は © 2026 Naotsun に帰属し、無断転載は禁止です。

## 作者

[Naotsun](https://twitter.com/Naotsun_UE)

## 更新履歴

**現在のバージョン**: 1.0.0（2026-06-18 リリース）― 製品版は [Fab で公開中](https://www.fab.com/listings/0eedf909-00ac-4d95-b109-8fda51800fff) です。詳細な更新履歴とバージョニング方針は [更新履歴](changelog.md) を参照してください。

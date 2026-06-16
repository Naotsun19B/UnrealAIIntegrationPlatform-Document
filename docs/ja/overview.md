![UE Version](https://img.shields.io/badge/Unreal%20Engine-5.7%20%2F%205.8-0e1128?logo=unrealengine&logoColor=white)
[![License: Fab Standard License (Fab EULA)](https://img.shields.io/badge/License-Fab%20Standard%20License%20%28Fab%20EULA%29-blue)](https://www.fab.com/ja/eula)
[![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/Naotsun_UE?style=social)](https://twitter.com/Naotsun_UE)

**[English](../../README.md)**

<p align="center">
  <img src="../../images/hero-banner.png" alt="Unreal AI Integration Platform" width="100%">
</p>

# UnrealAIIntegrationPlatform

<!--ts-->
   * [概要](#概要)
   * [動作環境](#動作環境)
   * [インストール](#インストール)
   * [セットアップ](#セットアップ)
   * [デモ版](#デモ版)
   * [ドキュメント](#ドキュメント)
   * [ライセンス](#ライセンス)
   * [作者](#作者)
   * [履歴](#履歴)
<!--te-->

## 概要

**UnrealAIIntegrationPlatform (UAIP)** は、AI エージェントが UE Editor と Runtime を **操作・観測・実行・検証** できるようにする Unreal Engine プラグインです。

Claude Code、Cursor、Windsurf、GitHub Copilot などの AI ツールが **Model Context Protocol (MCP)** 経由で接続し、意味的なコマンドを発行できます。座標クリックや脆弱な UI スクリプトは不要です。

主な機能：
- **Editor 操作** — アセットの開閉・保存、Blueprint 編集、アクター操作、Automation Test の実行、Sequencer の制御など、200 以上の登録済みコマンドで Editor のほぼすべての機能を網羅
- **視覚的・構造的な観測** — 任意の Editor タブやビューポートのスクリーンショット取得、ワールド状態・Slate ウィジェットツリー・エディタ状態の JSON ダンプ
- **Runtime / PIE 制御** — PIE の開始・停止、アクターのスポーン、入力インジェクト、Gauntlet テストの実行、アクタープロパティのアサート
- **シナリオ実行** — 複数コマンドを順序付きリストとして一括送信。失敗時の中断・リトライ・ステップごとのタイムアウトに対応
- **マルチ Transport** — MCP・HTTP・WebSocket・CLI から操作可能
- **Safety & Capability Policy** — セッション単位の Capability ゲートとプロセス単位の SafetyPolicy スイッチ

### アーキテクチャ

```mermaid
flowchart LR
    AI["AI クライアント<br/>Claude Code / Cursor / Windsurf / Copilot"]
    Bridge["MCP Bridge<br/>(thin_proxy.py)"]
    Editor["UE Editor<br/>UAIP プラグイン"]
    Artifacts[("Artifacts<br/>PNG / JSON / Log / Report")]

    AI <-->|MCP| Bridge
    Bridge <-->|HTTP /mcp| Editor
    Editor -->|生成| Artifacts
    Artifacts -.->|/uaip/artifacts/*| Bridge
```

MCP Bridge は AI クライアントのツール呼び出しをエディタへの HTTP リクエストに変換します。キャプチャ・ダンプ系コマンドは結果を Artifact として書き出し、Bridge が ID で AI クライアントに返却します。HTTP API・WebSocket・CLI を直接使う方法は [接続方法](connections.md) を参照してください。

## 動作環境

対象バージョン : UE 5.7 / 5.8  
対象プラットフォーム : Windows  
Python : 3.10 以降（MCP Bridge に必要）

## インストール

プロジェクトの `Plugins` フォルダに `Plugins/UnrealAIIntegrationPlatform` フォルダを入れてください。  
プラグインのインストール後に機能が使用できない場合は、**編集 > プラグイン** からプラグインが有効になっているかご確認ください。

## セットアップ

MCP Bridge（`Scripts/MCPBridge/`）は UE Editor と AI クライアントを HTTP 経由でつなぐ Python プロキシです。

1. `Scripts/MCPBridge/install/install.ps1`（Windows）または `install.sh`（macOS / Linux）を実行
2. AI クライアントの設定ファイルに MCP サーバーを登録
3. `Scripts/MCPBridge/install/guides/` の AI 使用ガイドを配置（推奨）
4. AI に「UAIP の HealthCheck を実行して」と聞いて動作確認

詳細な手順は [セットアップガイド](setup.md) を参照してください。

## デモ版

デモ版バイナリはこのリポジトリの [Releases](../../../releases) で無償配布しています。

観測・PIE 制御・アサーション・シナリオ実行・UI 自動化コマンドを提供しており、AI エージェントをレビューやテストのワークフローに組み込むのに十分な機能があります。

| | デモ版 | Pro 版（Fab） |
|---|:---:|:---:|
| MCP 接続 | ✅ | ✅ |
| HTTP / WebSocket / CLI | — | ✅ |
| 観測コマンド | ✅ | ✅ |
| PIE 制御 | ✅ | ✅ |
| シナリオ実行 | ✅ | ✅ |
| UI 自動化 | ✅ | ✅ |
| Editor 編集（Blueprint、Level、Assets など） | — | ✅ |
| Runtime ワールド編集（Spawn、GAS、Input など） | — | ✅ |
| Python スクリプト実行 | — | ✅ |
| キャプチャ画像への透かし | ✅ | — |
| ユーザー拡張ポイント（`ICommandProvider`） | ✅ | ✅ |
| 対応 UE バージョン | 5.7 / 5.8 | 5.7 / 5.8 |

コマンド全一覧・制限事項・インストール手順は [デモ版ガイド](demo.md) を参照してください。

## ドキュメント

| ドキュメント | 内容 |
|---|---|
| [クイックスタート](quickstart.md) | インストールから最初のコマンド実行まで 5 分 |
| [セットアップガイド](setup.md) | MCP Bridge のインストール・クライアント別設定 |
| &nbsp;&nbsp;↳ [Claude Code](clients/claude-code.md) / [Claude Desktop](clients/claude-desktop.md) / [Cursor](clients/cursor.md) / [Windsurf](clients/windsurf.md) / [Copilot](clients/copilot.md) | クライアント別設定 JSON と動作確認手順 |
| [接続方法](connections.md) | HTTP API・WebSocket・CLI トランスポートの使い方（Pro 版） |
| [ユースケース](use-cases.md) | 誰が UAIP を何のために使うか — テスト・レビュー・監査・ペアプロ |
| [Examples / Cookbook](cookbook.md) | レシピ集 — PIE スモーク・AI レビュー・アセット監査・BP 編集・UI 自動化 |
| [コマンドリファレンス](commands.md) | ドメイン別 730 以上のコマンド一覧 |
| [API リファレンス](api.md) | コマンド完全スキーマ（JSON）— ツール作成・コード生成・バリデーション用 |
| [シナリオ実行](scenario.md) | 複数ステップのコマンド一括実行 |
| [Artifacts（成果物）](artifacts.md) | スクリーンショット・JSON ダンプ・ログの読み方 |
| [Safety & Capabilities](safety.md) | SafetyPolicy と Capability の設定リファレンス |
| [セキュリティ](security.md) | 脅威モデル・認証・推奨セキュリティプロファイル |
| [アーキテクチャ](architecture.md) | レイヤー・ディスパッチシーケンス・Capability 決定フロー |
| [デモ版ガイド](demo.md) | デモ版コマンド一覧・制限事項・インストール手順 |
| [FAQ](faq.md) | デモ/Pro・Capability・ワークフロー・CI などのよくある質問 |
| [トラブルシューティング](troubleshooting.md) | エラーコードリファレンスと典型的な失敗パターン |
| [用語集](glossary.md) | Capability・Artifact・Scenario・Toolset 等の定義 |
| [ロードマップ](roadmap.md) | 今後追加予定の機能と開発方針 |

## ライセンス

本リポジトリの Releases で配布するデモバイナリは、リリースアーカイブに同梱の `EULA.txt` に従って提供されます。  
Fab で配布される製品版は [Fab Standard License (Fab EULA)](https://www.fab.com/ja/eula) に基づいて提供されます。  
特に明記がない限り、本リポジトリ内のドキュメントの著作権は © 2026 Naotsun に帰属し、無断転載は禁止です。

## 作者

[Naotsun](https://twitter.com/Naotsun_UE)

## 履歴

- (2026/06/16) v1.0  
  初版公開

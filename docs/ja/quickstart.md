**[English](../en/quickstart.md)** | [概要に戻る](overview.md)

# クイックスタート — 5 分で AI から最初のコマンドを実行

このページは、まっさらな状態から AI クライアント経由で UAIP コマンドを実行するまでの最短ルートをまとめたものです。所要時間は約 5 分。詳細なインストール手順・トラブルシューティング・クライアント別設定は [セットアップガイド](setup.md) を参照してください。

---

## 必要なもの

- **UE 5.7 または 5.8** プロジェクト（Windows）
- **Python 3.10 以降**（`PATH` 通っていること。MCP Bridge が使用）
- 次のいずれか：**Claude Code** / **Cursor** / **Windsurf** / **GitHub Copilot Chat**（MCP 対応 AI クライアントなら他も可）

---

## 1. プラグインを配置（30 秒）

### デモ版（無償）

[Releases](../../../releases) から最新の `UAIP-Demo-UE<バージョン>-Win64.zip` をダウンロードし、以下に展開：

```
<プロジェクト>/Plugins/UnrealAIIntegrationPlatform/
```

### Pro 版

[Fab](https://www.fab.com) からインストールし、同じパス配下に配置します。

---

## 2. プラグインを有効化（30 秒）

`.uproject` を UE で開き、**Edit > Plugins** で **UnrealAIIntegrationPlatform** が有効になっていることを確認します。フォルダを置いただけの場合は一度エディタを再起動してください。

デモ版の場合は、リリース zip 内の `Config/DefaultUAIP.ini` をプロジェクトの `Config/` フォルダにコピーします（デモ用 Capability `PIEControl` / `SlateUIAutomation` / `ObservationCapture` が有効化済み）。

---

## 3. MCP Bridge をインストール（1 分）

Bridge は AI クライアントと UE Editor をつなぐ薄い Python プロキシです。エディタが起動していなければ自動で立ち上げる役割も持ちます。

```powershell
cd <プロジェクト>/Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/install
./install.ps1            # Windows
# ./install.sh           # macOS / Linux（Pro 版のみ — デモ版は Windows 専用）
```

インストーラは仮想環境を作成して `mcp[cli]` を導入し、`thin_proxy.py` の隣に `config.json` を生成します（エディタパスと uproject パスは自動検出）。

---

## 4. AI クライアントに MCP サーバを登録（1 分）

使用する AI クライアントの MCP 設定ファイルに、以下を追加します。設定ファイルの正確な場所はクライアント毎に異なるため、[セットアップガイド](setup.md#クライアント別設定ファイル) を参照してください。

```json
{
  "mcpServers": {
    "uaip": {
      "command": "<プロジェクト>/Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/install/.venv/Scripts/python.exe",
      "args": ["<プロジェクト>/Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/thin_proxy.py"]
    }
  }
}
```

設定を反映するため、AI クライアントを再起動します。

> **ヒント**: 手順 3 のインストーラ最後にコピペ用 JSON が出力されます。そのまま貼り付けることもできます。

---

## 5. 動作確認（30 秒）

AI クライアントで以下のように尋ねます：

> 「UAIP の HealthCheck を実行して」

エージェントが `uaip_execute(CommandName="UAIP.Core.HealthCheck")` を呼び、以下のような結果を返します：

```json
{
  "Success": true,
  "Data": {
    "Status": "Healthy",
    "UAIPVersion": "1.0.0",
    "EngineVersion": "5.8.0",
    "BuildConfig": "Development"
  }
}
```

エディタは初回呼び出し時に自動起動します。初回は 30〜60 秒程度かかります。

---

## 動作確認完了。次は？

| 目的 | 移動先 |
|---|---|
| UAIP で何ができるか実例で見たい | [Examples / Cookbook](cookbook.md) |
| AI から Editor / PIE をシナリオで動かしたい | [シナリオ実行](scenario.md) |
| 特定のコマンドを調べたい | [コマンドリファレンス](commands.md) |
| MCP 以外（HTTP / WebSocket / CLI）を使いたい（Pro） | [接続方法](connections.md) |
| 編集系 Capability を有効化する前に安全モデルを理解しておきたい | [Safety & Capabilities](safety.md) |
| 動かない・エラーが出た | [トラブルシューティング](troubleshooting.md) |

---

> **デモ版と Pro 版**: デモ版は MCP 接続・観測・PIE 制御・シナリオ実行・UI 自動化・アサーションが利用可能で、AI エージェントをレビュー・テストワークフローに組み込むのに十分な機能を備えています。Editor 編集（Blueprint・Level・アセット 等）、Runtime ワールド編集（Spawn・GAS・Input 等）、HTTP / WebSocket / CLI トランスポート、Python スクリプト実行は [デモ版ガイド](demo.md) を参照のうえ、[Fab Pro 版](https://www.fab.com) をご検討ください。

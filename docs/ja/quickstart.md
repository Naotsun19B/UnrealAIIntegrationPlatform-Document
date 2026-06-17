**[English](../en/quickstart.md)** | [概要に戻る](overview.md)

# クイックスタート — 5 分で AI から最初のコマンドを実行する

このページは、まっさらな状態から AI クライアント経由で UAIP コマンドを実行できるようになるまでの最短ルートをまとめたものです。所要時間はおよそ 5 分です。詳細なインストール手順・トラブルシューティング・クライアント別の設定は [接続方法 → MCP Bridge](connections.md#mcp-bridge) を参照してください。

---

## 必要なもの

- **UE 5.7 または 5.8** のプロジェクト（Windows）
- **Python 3.10 以降**（`PATH` を通しておくこと。MCP Bridge が使用します）
- 以下のいずれかの AI クライアント：**Claude Code** / **Codex CLI** / **Cursor** / **Windsurf** / **GitHub Copilot Chat**（その他 MCP 対応クライアントも可）

---

## 1. プラグインを配置する（30 秒）

### デモ版（無償）

[Releases](../../../releases) から最新の `UAIP-Demo-UE<バージョン>-Win64.zip` をダウンロードし、以下のパスに展開してください：

```
<プロジェクト>/Plugins/UnrealAIIntegrationPlatform/
```

### 製品版

製品版は **Fab で近日公開予定** です。公開後は同じパスに配置してください。

---

## 2. プラグインを有効化する（30 秒）

`.uproject` を UE で開き、**Edit > Plugins** から **UnrealAIIntegrationPlatform** が有効になっていることを確認してください。フォルダを置いただけの場合は、エディタを一度再起動する必要があります。

デモ版を使う場合は、リリース zip 内の `Config/DefaultUAIP.ini` をプロジェクトの `Config/` フォルダにコピーしてください。これにはデモ用の Capability（`PIEControl`・`SlateUIAutomation`・`ObservationCapture`）が有効化済みの状態で入っています。

---

## 3. MCP Bridge をインストールする（1 分）

Bridge は AI クライアントと UE Editor をつなぐ薄い Python プロキシです。エディタが起動していなければ自動で立ち上げる役割も担います。

```powershell
cd <プロジェクト>/Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/install
./install.ps1
```

> **対応プラットフォーム**：v1.0 は **Windows (Win64) のみ** が対象です。macOS / Linux 対応は将来検討項目です。

このインストーラは仮想環境を作成して `mcp[cli]` を導入し、`thin_proxy.py` の隣に `config.json` を生成します（エディタパスと uproject パスは自動検出されます）。

---

## 4. AI クライアントに MCP サーバを登録する（1 分）

利用する AI クライアントの MCP 設定ファイルに、以下を追加します。設定ファイルの正確なパスはクライアントごとに異なるので、[接続方法 → MCP Bridge](connections.md#mcp-bridge) を参照してください。

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

設定を反映するため、AI クライアントを再起動してください。

> **ヒント**：手順 3 のインストーラの最後にコピペできる JSON が出力されるので、そのまま貼り付けることもできます。

---

## 5. 動作を確認する（30 秒）

AI クライアントで次のように依頼してみてください：

> 「UAIP の HealthCheck を実行して」

エージェントが `uaip_execute(CommandName="UAIP.Core.HealthCheck")` を呼び、次のような結果を返します：

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

エディタは初回呼び出し時に自動で起動します。初回は 30〜60 秒程度かかります。

---

## 動作確認完了。次に何をすればよいですか？

| 目的 | 移動先 |
|---|---|
| UAIP で何ができるかを実例で見たい | [使用例集 / レシピ集](cookbook.md) |
| AI から Editor / PIE をシナリオで動かしたい | [シナリオ実行](scenario.md) |
| 特定のコマンドを調べたい | [コマンドリファレンス](commands.md) |
| MCP 以外（HTTP / WebSocket / CLI）を使いたい（製品版） | [接続方法](connections.md) |
| 編集系の Capability を有効化する前に安全モデルを理解しておきたい | [Safety & Capabilities](safety.md) |
| うまく動かない、エラーが出る | [トラブルシューティング](troubleshooting.md) |

---

> **デモ版と製品版**：デモ版は MCP 接続・観測・PIE 制御・シナリオ実行・UI 自動化・アサーションが利用可能で、AI エージェントをレビューやテストのワークフローに組み込むのに十分な機能をそろえています。Editor 編集（Blueprint・Level・アセットなど）・Runtime ワールド編集（Spawn・GAS・Input など）・HTTP / WebSocket / CLI トランスポート・Python スクリプト実行が必要なら、[デモ版ガイド](demo.md) を参照のうえ製品版もご検討ください（Fab で近日公開予定）。

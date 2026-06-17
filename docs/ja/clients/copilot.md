**[English](../../en/clients/copilot.md)** | [接続方法に戻る](../connections.md#mcp-bridge)

# GitHub Copilot（VS Code）

VS Code の [GitHub Copilot Chat](https://docs.github.com/ja/copilot) は VS Code 1.99 以降で MCP サーバに対応しました。UAIP はワークスペースローカルのサーバとして統合します。

---

## 設定ファイル位置

| スコープ | パス |
|---|---|
| ワークスペース | `.vscode/mcp.json`（`.vscode/settings.json` の隣） |

---

## 設定

```json
{
  "servers": {
    "uaip-MyGame": {
      "type": "stdio",
      "command": "python",
      "args": [
        "E:/MyProjects/MyGame/Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/thin_proxy.py"
      ],
      "env": {
        "UAIP_UE_EDITOR_PATH": "E:/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe",
        "UAIP_UPROJECT_PATH":  "E:/MyProjects/MyGame/MyGame.uproject"
      }
    }
  }
}
```

> **注意**：Copilot のスキーマは `servers`（`mcpServers` ではありません）を使い、`type: "stdio"` フィールドも必要です。Claude / Cursor / Windsurf とは形式が異なるので、これらのクライアントの JSON をそのまま流用しないでください。

- `uaip-MyGame` は自分のサーバキーに置き換えてください
- パスは絶対パスを、フォワードスラッシュ区切りで記述してください
- `python` が `PATH` に通っていない場合は、Python インタプリタの完全パスに置き換えてください

保存すると、VS Code から MCP サーバの起動を確認するプロンプトが出ます。承認するか、**コマンドパレット → MCP: Restart Server** を実行してください。

---

## AI 利用ガイド（`.github/copilot-instructions.md`）

Copilot はリポジトリ全体のカスタム指示として `.github/copilot-instructions.md` を読み込みます。UAIP ガイドの要約を次のように追記してください：

```powershell
mkdir -Force .github
Get-Content Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/install/guides/usage.md | Add-Content .github/copilot-instructions.md
```

Copilot はカスタム指示用のコンテキスト予算が他のクライアントより小さめです。`usage.md` と、ワークフローに直結するガイド（シナリオを多用するなら `scenario.md` など）に絞って貼り付けてください。すべてのガイドを一度に貼るのは避けたほうが無難です。

---

## 動作確認

1. VS Code のウィンドウをリロードする（コマンドパレット → "Reload Window"）
2. Copilot Chat パネルを開く
3. サーバステータスを確認する：コマンドパレット → **MCP: List Servers** → `uaip-MyGame` が `Running` になっていれば OK
4. Copilot に「UAIP の HealthCheck を実行して」と依頼する

---

## トラブルシューティング

| 症状 | 対処 |
|---|---|
| コマンドパレットに MCP コマンドが見当たらない | VS Code のバージョンが古い可能性があります。1.99 以降にアップデートしてください |
| `MCP: List Servers` でサーバが Failed と出る | サーバ名をクリックして **View Logs** を確認してください。選択した Python に `mcp` パッケージが入っていないのが典型的な原因です |
| Copilot が UAIP コンテキストを無視している | `.github/copilot-instructions.md` がロードされていません。**GitHub Copilot Chat: Use Instruction Files** が有効になっているか確認してください |
| ツール呼び出しが提案されない | 「UAIP をチェックして」ではなく「UAIP の HealthCheck ツールを使って」のように、具体的に依頼してみてください |

完全なエラーコードリファレンスは [トラブルシューティング](../troubleshooting.md) を参照。

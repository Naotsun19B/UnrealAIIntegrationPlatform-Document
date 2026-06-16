**[English](../../en/clients/copilot.md)** | [セットアップに戻る](../setup.md)

# GitHub Copilot（VS Code）

VS Code の [GitHub Copilot Chat](https://docs.github.com/ja/copilot) は VS Code 1.99+ から MCP サーバーをサポート。UAIP はワークスペースローカルサーバーとして統合。

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

> **注**: Copilot のスキーマは `servers`（`mcpServers` ではない）を使用し、`type: "stdio"` フィールドが必要 — Claude / Cursor / Windsurf とは異なります。これらのクライアントの JSON をそのまま流用しないでください。

- `uaip-MyGame` は自分のサーバーキーに置き換え
- 絶対パスをフォワードスラッシュで記述
- `python` が `PATH` にない場合は Python インタプリタの完全パスに置換

保存後、VS Code が MCP サーバー起動を確認するプロンプトを表示。承認するか、**コマンドパレット → MCP: Restart Server** を実行。

---

## AI 利用ガイド（`.github/copilot-instructions.md`）

Copilot はリポジトリ全体のカスタム指示として `.github/copilot-instructions.md` を読み込みます。UAIP ガイドの要約を追記：

```powershell
mkdir -Force .github
Get-Content Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/install/guides/usage.md | Add-Content .github/copilot-instructions.md
```

Copilot は他クライアントよりカスタム指示用のコンテキスト予算が小さいです — `usage.md` とワークフローに最も関連するガイド（シナリオを多用するなら `scenario.md` 等）に限定してください。全ガイドを一度に貼らないこと。

---

## 動作確認

1. VS Code ウィンドウをリロード（コマンドパレット → "Reload Window"）
2. Copilot Chat パネルを開く
3. サーバーステータスを確認：コマンドパレット → **MCP: List Servers** → `uaip-MyGame` が `Running` であること
4. Copilot に依頼：**「UAIP の HealthCheck を実行して」**

---

## トラブルシューティング

| 症状 | 対処 |
|---|---|
| コマンドパレットに MCP コマンドが無い | VS Code バージョン古い。1.99+ にアップデート |
| `MCP: List Servers` でサーバーが Failed | サーバー名クリック → **View Logs**。よくある原因：選択した Python に `mcp` パッケージ未導入 |
| Copilot が UAIP コンテキストを無視 | `.github/copilot-instructions.md` 未ロード。**GitHub Copilot Chat: Use Instruction Files** が有効か確認 |
| ツール呼び出しが提案されない | 「UAIP をチェック」ではなく「UAIP HealthCheck ツールを使って」のように具体的に依頼 |

完全なエラーコードリファレンスは [トラブルシューティング](../troubleshooting.md) を参照。

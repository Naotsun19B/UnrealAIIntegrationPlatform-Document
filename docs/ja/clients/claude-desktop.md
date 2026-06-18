**[English](../../en/clients/claude-desktop.md)** | [接続方法に戻る](../connections.md#mcp-bridge)

# Claude Desktop

Claude Desktop はスタンドアロンのデスクトップチャットアプリです。MCP サーバの登録は `claude_desktop_config.json` 経由で行います。

---

## 設定ファイル位置

| OS | パス |
|---|---|
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |

ファイルがなければ作成してください。

---

## 設定

インストーラが表示したスニペットを貼り付けます：

```json
{
  "mcpServers": {
    "uaip-MyGame": {
      "command": "E:/MyProjects/MyGame/Plugins/UAIPMCPBridge/.venv/Scripts/python.exe",
      "args": [
        "E:/MyProjects/MyGame/Plugins/UAIPMCPBridge/thin_proxy.py"
      ],
      "env": {
        "UAIP_UE_EDITOR_PATH": "E:/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe",
        "UAIP_UPROJECT_PATH":  "E:/MyProjects/MyGame/MyGame.uproject"
      }
    }
  }
}
```

- `uaip-MyGame` は自分のサーバキーに置き換えてください
- パスは **絶対パスを、フォワードスラッシュ区切りで** JSON に書いてください
- `command` にはインストーラが作成した venv の Python を指定するため、system-wide な Python が `PATH` に通っている必要はありません

保存できたら、システムトレイから **Claude Desktop を完全に終了** したうえで再起動してください。

---

## AI 利用ガイド

Claude Desktop にはプロジェクト単位のルール機構がありません。次の 2 つの方法から選んでください：

- **インラインで貼り付ける**：各会話の冒頭で `Plugins/UAIPMCPBridge/install/guides/usage.md` の内容を貼り付ける
- **システムプロンプトに設定する**（Claude Pro / Team プラン）：プロジェクト全体のカスタム指示として利用ガイドラインを登録する

この点については、CLI ベースの [Claude Code](claude-code.md) のほうが扱いやすくなっています。UAIP を頻繁に使う予定なら、そちらの利用も検討してください。

---

## 動作確認

1. Claude Desktop を一度終了して、再度起動する
2. 新規チャットを開始したときに入力欄の下に **🔌 1 MCP server connected** が表示されることを確認する
3. 「UAIP の HealthCheck を実行して」と依頼する
4. 初回はエディタの起動に 30〜60 秒ほどかかります。次回以降は高速です

---

## トラブルシューティング

| 症状 | 対処 |
|---|---|
| 🔌 が 0 サーバと表示される | 設定ファイルのパス、もしくは JSON の構文に誤りがあります。JSON を検証してから Claude Desktop を再起動してください |
| サーバアイコンが赤になっている | アイコンをクリックすると `thin_proxy.py` の stderr が確認できます。`python` が `PATH` に通っていないのが典型的な原因です — 絶対パスで `python.exe` を指定してください |
| AI が UAIP コマンドを認識しない | 利用ガイドがロードされていません。会話の冒頭で `usage.md` の内容をインライン貼り付けしてください |

完全なエラーコードリファレンスは [トラブルシューティング](../troubleshooting.md) を参照。

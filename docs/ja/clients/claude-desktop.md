**[English](../../en/clients/claude-desktop.md)** | [セットアップに戻る](../setup.md)

# Claude Desktop

Claude Desktop はスタンドアロンのデスクトップチャットアプリ。MCP サポートは `claude_desktop_config.json` 経由。

---

## 設定ファイル位置

| OS | パス |
|---|---|
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |

ファイルがなければ作成してください。

---

## 設定

```json
{
  "mcpServers": {
    "uaip-MyGame": {
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

- `uaip-MyGame` は自分のサーバーキーに置き換え
- **絶対パスをフォワードスラッシュで** JSON に記述
- `python` が `PATH` にない場合は Python インタプリタの完全パスに置換

保存後、**Claude Desktop を完全終了**（システムトレイ → Quit）して再起動。

---

## AI 利用ガイド

Claude Desktop にはプロジェクト毎のルールシステムはありません。2 つの選択肢：

- **インライン**: 各会話の冒頭で `Scripts/MCPBridge/install/guides/usage.md` の内容を貼り付け
- **システムプロンプト**（Claude Pro / Team）: プロジェクト全体のカスタム指示として利用ガイドラインを設定

CLI ベースの [Claude Code](claude-code.md) の方がこの点では優れています。UAIP 作業が多いなら検討してください。

---

## 動作確認

1. Claude Desktop を終了して再起動
2. 新規チャット時に入力欄の下に **🔌 1 MCP server connected** が表示される
3. 依頼：**「UAIP の HealthCheck を実行して」**
4. 初回はエディタ起動（30〜60 秒）。以降は高速

---

## トラブルシューティング

| 症状 | 対処 |
|---|---|
| 🔌 が 0 サーバー表示 | 設定ファイルパスまたは JSON 構文エラー。JSON を検証し Claude Desktop 再起動 |
| サーバーアイコンが赤 | クリックして `thin_proxy.py` の stderr を確認。よくある原因：`python` が `PATH` にない → 絶対パスの `python.exe` を使用 |
| AI が UAIP コマンドを認識しない | 利用ガイドが未ロード。会話冒頭で `usage.md` をインライン貼り付け |

完全なエラーコードリファレンスは [トラブルシューティング](../troubleshooting.md) を参照。

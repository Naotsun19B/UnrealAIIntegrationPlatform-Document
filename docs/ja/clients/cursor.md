**[English](../../en/clients/cursor.md)** | [セットアップに戻る](../setup.md)

# Cursor

[Cursor](https://cursor.sh/) は VS Code ベースの AI ファースト IDE。MCP サポートは `mcp.json` 経由。

---

## 設定ファイル位置

| スコープ | パス |
|---|---|
| ユーザー全体 | `~/.cursor/mcp.json` |
| プロジェクト | `.cursor/mcp.json`（`.uproject` の隣） |

プロジェクトスコープが推奨 — 複数 UE プロジェクトが衝突しません。

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

保存後、**Cursor → Settings → Cursor Settings → Features → MCP** に `uaip-MyGame` が表示されます。表示されない場合は更新アイコンクリックか Cursor 再起動。

---

## AI 利用ガイド（.cursor/rules）

ガイドファイルを `.cursor/rules/` にコピーし、`.mdc` 拡張子にリネーム：

```powershell
mkdir -Force .cursor/rules
Get-ChildItem Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/install/guides/*.md | ForEach-Object {
    Copy-Item $_.FullName -Destination ".cursor/rules/$($_.BaseName).mdc"
}
```

`.mdc` 拡張子が Cursor のルールとしてロードされる必須条件。Cursor はプロジェクト毎にこのフォルダ内の `.mdc` ファイルを自動読み込みします — 手動の `@include` は不要。

---

## 動作確認

1. Cursor を再起動（またはサーバー横の更新アイコンをクリック）
2. Cursor チャットパネルを開く
3. 依頼：**「UAIP の HealthCheck を実行して」**
4. Cursor が UAIP を呼ぶときに tool-use インジケータが表示される

---

## トラブルシューティング

| 症状 | 対処 |
|---|---|
| サーバーが Settings → MCP に出ない | JSON 構文エラーまたはパス誤り。JSON 検証して Cursor 再起動 |
| サーバーは出るが "Failed to start" | サーバー名クリックで stderr 確認。よくある原因：Python パス誤りや `mcp` パッケージ未導入 |
| ツール呼び出しは成功するがルールが適用されない | ガイドファイルの `.mdc` 拡張子忘れ。リネームして再起動 |
| 初回呼び出しでエディタ起動せず | `env` ブロックの `UAIP_UE_EDITOR_PATH` と `UAIP_UPROJECT_PATH` を検証 |

完全なエラーコードリファレンスは [トラブルシューティング](../troubleshooting.md) を参照。

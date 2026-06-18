**[English](../../en/clients/cursor.md)** | [接続方法に戻る](../connections.md#mcp-bridge)

# Cursor

[Cursor](https://cursor.sh/) は VS Code ベースの AI ファースト IDE です。MCP サーバの登録は `mcp.json` 経由で行います。

---

## 設定ファイル位置

| スコープ | パス |
|---|---|
| ユーザー全体 | `~/.cursor/mcp.json` |
| プロジェクト | `.cursor/mcp.json`（`.uproject` の隣） |

プロジェクトスコープがおすすめです — 複数の UE プロジェクトを使い分けても衝突しません。

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

保存できたら、**Cursor → Settings → Cursor Settings → Features → MCP** に `uaip-MyGame` が表示されているはずです。表示されない場合は、更新アイコンをクリックするか Cursor を再起動してみてください。

---

## AI 利用ガイド（.cursor/rules）

ガイドファイルを `.cursor/rules/` にコピーし、`.mdc` 拡張子にリネーム：

```powershell
mkdir -Force .cursor/rules
Get-ChildItem Plugins/UAIPMCPBridge/install/guides/*.md | ForEach-Object {
    Copy-Item $_.FullName -Destination ".cursor/rules/$($_.BaseName).mdc"
}
```

Cursor がルールとして読み込んでくれるためには `.mdc` 拡張子であることが必須です。プロジェクトごとにこのフォルダ内の `.mdc` ファイルを自動的に読み込むため、`@include` のような手動の指定は要りません。

---

## 動作確認

1. Cursor を再起動するか、サーバ横の更新アイコンをクリックする
2. Cursor のチャットパネルを開く
3. 「UAIP の HealthCheck を実行して」と依頼する
4. Cursor が UAIP を呼び出すタイミングで、tool-use インジケータが表示されます

---

## トラブルシューティング

| 症状 | 対処 |
|---|---|
| サーバが Settings → MCP に表示されない | JSON の構文エラーかパスの誤りが原因です。JSON を検証してから Cursor を再起動してください |
| サーバは表示されるが "Failed to start" になる | サーバ名をクリックすると stderr を確認できます。Python のパス誤りや `mcp` パッケージ未導入がよくある原因です |
| ツール呼び出しは成功するが、ルールが効いていない | ガイドファイルの拡張子を `.mdc` にし忘れている可能性があります。リネームしてから再起動してください |
| 初回呼び出しでエディタが起動しない | `env` ブロックの `UAIP_UE_EDITOR_PATH` と `UAIP_UPROJECT_PATH` を再確認してください |

完全なエラーコードリファレンスは [トラブルシューティング](../troubleshooting.md) を参照。

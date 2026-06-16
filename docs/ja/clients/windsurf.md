**[English](../../en/clients/windsurf.md)** | [セットアップに戻る](../setup.md)

# Windsurf

[Windsurf](https://codeium.com/windsurf) は Codeium が開発する AI ファースト IDE です。MCP サーバの登録は `mcp_config.json` 経由で行います。

---

## 設定ファイル位置

| スコープ | パス |
|---|---|
| ユーザー全体 | `~/.codeium/windsurf/mcp_config.json` |

Windsurf は現状ユーザー全体の設定 1 つしかサポートしていないため、複数の UE プロジェクトを使う場合も同じ `mcpServers` セクションに並べる形になります。

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

- `uaip-MyGame` は自分のサーバキーに置き換えてください
- パスは **絶対パスを、フォワードスラッシュ区切りで** JSON に書いてください
- `python` が `PATH` に通っていない場合は、Python インタプリタの完全パスに置き換えてください

複数のプロジェクトを扱う場合は、`mcpServers` 配下にプロジェクトごとに別のキー（`uaip-GameA`・`uaip-GameB` など）でエントリを追加してください。

---

## AI 利用ガイド（`.windsurfrules`）

Windsurf はワークスペースルートにある `.windsurfrules` を読み込みます。次のように `usage.md` の内容を追記してください：

```powershell
Get-Content Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/install/guides/usage.md | Add-Content .windsurfrules
```

シナリオや Capability などのコンテキストも追加したい場合は、`guides/` フォルダ内のほかの `.md` ファイルも同じ要領で追記してください。

---

## 動作確認

1. Windsurf を再起動する
2. Cascade パネルを開く
3. パネル上部の MCP サーバステータスに `uaip-MyGame ✓` が表示されているか確認する
4. 「UAIP の HealthCheck を実行して」と依頼する

---

## トラブルシューティング

| 症状 | 対処 |
|---|---|
| Cascade にサーバが表示されない | JSON の構文エラーかパスの誤りが原因です。JSON を検証してから Windsurf を再起動してください |
| サーバが赤く表示される | Windsurf のログ（`~/.codeium/windsurf/logs/`）で `thin_proxy.py` の stderr を確認してください |
| ツール呼び出しは成功するが、AI が UAIP コンテキストを無視している | `.windsurfrules` がワークスペースルートにないか、内容が追記されていない可能性があります。`Add-Content` を再実行してください |
| エディタが起動しない | `UAIP_UE_EDITOR_PATH` と `UAIP_UPROJECT_PATH` を再確認してください |

完全なエラーコードリファレンスは [トラブルシューティング](../troubleshooting.md) を参照。

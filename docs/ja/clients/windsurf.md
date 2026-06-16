**[English](../../en/clients/windsurf.md)** | [セットアップに戻る](../setup.md)

# Windsurf

[Windsurf](https://codeium.com/windsurf) は Codeium 製の AI ファースト IDE。MCP サポートは `mcp_config.json` 経由。

---

## 設定ファイル位置

| スコープ | パス |
|---|---|
| ユーザー全体 | `~/.codeium/windsurf/mcp_config.json` |

Windsurf は現状ユーザー全体の設定 1 つのみ — 複数 UE プロジェクトが同じ MCP サーバーエントリを共有します。

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

複数プロジェクトには `mcpServers` 配下に異なるキー（`uaip-GameA`・`uaip-GameB` …）でプロジェクト毎にエントリを追加してください。

---

## AI 利用ガイド（`.windsurfrules`）

Windsurf はワークスペースルートの `.windsurfrules` を読み込みます。`usage.md` の内容を追記：

```powershell
Get-Content Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/install/guides/usage.md | Add-Content .windsurfrules
```

さらにコンテキストが必要なら（シナリオ・Capability 等）`guides/` フォルダ内の他 `.md` ファイルも同様に追記。

---

## 動作確認

1. Windsurf を再起動
2. Cascade パネルを開く
3. パネル上部の MCP サーバーステータスを確認 — `uaip-MyGame ✓` が表示される
4. 依頼：**「UAIP の HealthCheck を実行して」**

---

## トラブルシューティング

| 症状 | 対処 |
|---|---|
| Cascade にサーバー出ない | JSON 構文エラーまたはパス誤り。JSON 検証して Windsurf 再起動 |
| サーバーが赤表示 | Windsurf ログ（`~/.codeium/windsurf/logs/`）で `thin_proxy.py` の stderr 確認 |
| ツール呼び出し成功するが AI が UAIP コンテキストを無視 | `.windsurfrules` がワークスペースルートにない、または内容追記されていない。`Add-Content` を再実行 |
| エディタ起動せず | `UAIP_UE_EDITOR_PATH` と `UAIP_UPROJECT_PATH` を検証 |

完全なエラーコードリファレンスは [トラブルシューティング](../troubleshooting.md) を参照。

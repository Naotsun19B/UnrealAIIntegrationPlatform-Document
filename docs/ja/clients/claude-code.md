**[English](../../en/clients/claude-code.md)** | [セットアップに戻る](../setup.md)

# Claude Code

[Claude Code](https://claude.com/claude-code) は Anthropic 製の CLI / IDE 拡張。本ページ掲載クライアントの中で MCP サポートが最も成熟しており、プロジェクトローカルの `.mcp.json` を自動的に読みます。

---

## 前提

[セットアップ ステップ 1](../setup.md#ステップ-1--インストールスクリプトを実行) を完了済み。`config.json` は以下に存在：

```
Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/config.json
```

---

## オプション A — プロジェクト毎（推奨）

`.uproject` の隣に `.mcp.json` を作成：

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

- `uaip-MyGame` は自分のサーバーキーに置き換え（[セットアップ ステップ 2](../setup.md#ステップ-2--mcp-サーバーキーを決定) 参照）
- **絶対パスをフォワードスラッシュで** 使用（Windows でも JSON はフォワードスラッシュを受理）
- `python` が `PATH` にない場合は Python インタプリタの完全パスに置換

Claude Code はプロジェクトディレクトリから起動した次回からこれを読み込みます。

---

## オプション B — グローバル（複数プロジェクトで共通サーバー）

`~/.claude.json` を編集してトップレベルに同じ `mcpServers` ブロックを追加。`editor_path` と `uproject_path` が複数プロジェクトで同じ場合のみ — 通常は当てはまりません。

---

## ステップ — AI 利用ガイドを配置（推奨）

`Scripts/MCPBridge/install/guides/` には Claude に UAIP の慣用的な使い方（シナリオ・Capability・artifact・グラフ編集・安全性）を教える Markdown が含まれます。配置しないと Claude が会話毎に手探りでターン消費します。

```powershell
# ガイドファイルをグローバル Claude ルールフォルダにコピー
mkdir -Force ~/.claude/rules/uaip
cp Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/install/guides/*.md ~/.claude/rules/uaip/
```

`~/.claude/CLAUDE.md` で参照し、毎会話でロード：

```markdown
@rules/uaip/usage.md
@rules/uaip/scenario.md
@rules/uaip/safety-and-capabilities.md
@rules/uaip/command-discovery.md
@rules/uaip/artifacts.md
@rules/uaip/graph-editing.md
```

---

## 動作確認

1. プロジェクトディレクトリで新しい Claude Code セッションを開始
2. サーバーが表示されているか確認：`claude mcp list` で `uaip-MyGame: ✔ connected` が出る
3. Claude に依頼：**「UAIP の HealthCheck を実行して」**
4. 初回呼び出しでエディタ起動（30〜60 秒）。以降は高速

期待されるレスポンス：

```json
{
  "Success": true,
  "Data": {
    "Status": "Healthy",
    "UAIPVersion": "1.0.0",
    "EngineVersion": "5.8.0"
  }
}
```

---

## トラブルシューティング

| 症状 | 対処 |
|---|---|
| `claude mcp list` でサーバーが failed | `python <thin_proxy.py のパス>` を直接実行 — stderr にエラーが出ます |
| `thin_proxy.py` 起動時に `TypeError: ...` | Python バージョンが古い。`python --version` が 3.10+ か確認 |
| `HealthCheck` は 1 回成功、その後ハング | エディタクラッシュで Bridge が再接続中。60 秒待つか `Saved/Crashes/` を確認 |
| エディタ再起動後に "Couldn't reach MCP" | 前回の `taskkill` で残った `mcp_proxy.lock` が原因。`Saved/UAIP/` から削除して再起動 |

完全なエラーコードリファレンスは [トラブルシューティング](../troubleshooting.md) を参照。

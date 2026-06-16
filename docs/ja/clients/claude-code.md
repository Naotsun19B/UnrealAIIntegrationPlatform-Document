**[English](../../en/clients/claude-code.md)** | [セットアップに戻る](../setup.md)

# Claude Code

[Claude Code](https://claude.com/claude-code) は Anthropic が提供する CLI / IDE 拡張です。本ページで紹介しているクライアントのなかでも MCP サポートがもっとも成熟しており、プロジェクトローカルの `.mcp.json` を自動で読み込んでくれます。

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

- `uaip-MyGame` は自分のサーバキーに置き換えてください（[セットアップ ステップ 2](../setup.md#ステップ-2--mcp-サーバーキーを決定) を参照）
- パスは **絶対パスを、フォワードスラッシュ区切りで** 書いてください（Windows でも JSON ではフォワードスラッシュをそのまま受け付けます）
- `python` が `PATH` に通っていない場合は、Python インタプリタの完全パスに置き換えてください

Claude Code は次回プロジェクトディレクトリから起動したときに、この設定を読み込みます。

---

## オプション B — グローバル（複数プロジェクトで共通のサーバを使う）

`~/.claude.json` を編集し、トップレベルに同じ `mcpServers` ブロックを追加します。ただしこれが有効なのは、`editor_path` と `uproject_path` が複数プロジェクトで共通になる場合に限られます — 通常はそうならないので、プロジェクトごとの設定（オプション A）が無難です。

---

## ステップ — AI 利用ガイドを配置（推奨）

`Scripts/MCPBridge/install/guides/` には、Claude に UAIP の使い方（シナリオ・Capability・Artifact・グラフ編集・安全性）を教えるための Markdown が同梱されています。配置しないと、Claude は会話のたびに手探りでターンを消費してしまいます。

```powershell
# ガイドファイルを、グローバルの Claude ルールフォルダにコピー
mkdir -Force ~/.claude/rules/uaip
cp Plugins/UnrealAIIntegrationPlatform/Scripts/MCPBridge/install/guides/*.md ~/.claude/rules/uaip/
```

`~/.claude/CLAUDE.md` から参照しておけば、すべての会話で自動的にロードされます：

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

1. プロジェクトディレクトリで Claude Code を新しいセッションとして起動する
2. サーバが認識されているか `claude mcp list` で確認する（`uaip-MyGame: ✔ connected` が表示されれば OK）
3. Claude に「UAIP の HealthCheck を実行して」と依頼する
4. 初回の呼び出しでエディタが起動します（30〜60 秒ほど）。次回以降は高速です

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
| `claude mcp list` でサーバが Failed と表示される | `python <thin_proxy.py のパス>` を直接実行してみてください。stderr にエラーが出力されます |
| `thin_proxy.py` 起動時に `TypeError: ...` が出る | Python のバージョンが古い可能性があります。`python --version` で 3.10 以上か確認してください |
| `HealthCheck` は 1 回成功したのに、その後ハングする | エディタがクラッシュして Bridge が再接続中の可能性があります。60 秒ほど待つか `Saved/Crashes/` を確認してください |
| エディタ再起動後に "Couldn't reach MCP" になる | 前回の `taskkill` で `mcp_proxy.lock` が残っているのが原因です。`Saved/UAIP/` から削除して再起動してください |

完全なエラーコードリファレンスは [トラブルシューティング](../troubleshooting.md) を参照。
